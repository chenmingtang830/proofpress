import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def evidence_payload():
    quote = "The liability cap is one year of fees."
    return {
        "schema_version": "proofpress/retrieval-evidence/v1",
        "source": {"uri": "workspace://msa.pdf",
                   "content_digest": "sha256:" + "a" * 64},
        "evidence": {"quote": quote, "locator": {
            "kind": "text_span", "start": 0, "end": len(quote),
            "text_digest": "sha256:" + hashlib.sha256(quote.encode()).hexdigest()}},
        "retrieval": {"adapter": "partner", "version": "1", "query": "cap?",
                      "config_digest": "sha256:" + "b" * 64},
    }


def operation(name, parameters, key=None):
    request = {"schema_version": "proofpress/local-operation/v1alpha1",
               "operation": name, "parameters": parameters}
    if key:
        request["idempotency_key"] = key
    return request


class HostedAuthorityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        sys.path.insert(0, str(ROOT))
        from proofpress.hosted import control_plane
        self.hosted = control_plane
        self.database = Path(self.tmp.name) / "hosted.db"
        self.control = control_plane.HostedControlPlane(self.database)
        self.owner = self.control.bootstrap(
            "workspace:example", "human:owner", "Example Owner")
        self.agent = self.control.issue_agent_credential(
            self.owner["token"], "agent:codex-laptop", "Codex laptop")

    def tearDown(self):
        self.tmp.cleanup()

    def test_agent_identity_is_server_derived_and_owner_approval_is_separate(self):
        imported = self.control.execute(
            self.agent["token"],
            operation("evidence.submit", {"payload": evidence_payload()}, "evidence-1"))
        self.assertTrue(imported["ok"])
        evidence_id = imported["result"]["evidence"][0]
        proposed = self.control.execute(
            self.agent["token"], operation("conclusion.propose", {
                "statement": "The liability cap is one year of fees.",
                "evidence_refs": [evidence_id], "scope": "contract-review",
                "proposer": "human:owner",
            }, "proposal-1"))
        self.assertTrue(proposed["ok"])
        conclusion = proposed["result"]["conclusion"]
        self.assertEqual(conclusion["proposer"], "agent:codex-laptop")

        evaluated = self.control.execute(
            self.agent["token"], operation(
                "conclusion.evaluate", {"conclusion_id": conclusion["id"]}))
        self.assertTrue(evaluated["ok"])
        forbidden = self.control.execute(
            self.agent["token"], operation("conclusion.review", {
                "conclusion_id": conclusion["id"], "decision": "admit",
                "reviewer": "human:owner",
            }))
        self.assertFalse(forbidden["ok"])
        self.assertEqual(forbidden["error"]["code"], "operation_forbidden")

        reviewed = self.control.execute(
            self.owner["token"], operation("conclusion.review", {
                "conclusion_id": conclusion["id"], "decision": "admit",
                "reviewer": "agent:codex-laptop", "request_id": "review-1",
            }))
        self.assertTrue(reviewed["ok"])
        self.assertEqual(reviewed["result"]["review"]["reviewer"], "human:owner")
        context = self.control.execute(
            self.agent["token"], operation("context.get", {
                "scope": "contract-review", "actor": "human:owner"}))
        self.assertEqual(context["result"]["actor"], "agent:codex-laptop")
        self.assertEqual(context["result"]["knowledge"][0]["id"], conclusion["id"])

    def test_hosted_discovery_uses_server_identity_and_never_requires_scope(self):
        imported = self.control.execute(
            self.agent["token"], operation("evidence.submit", {
                "payload": evidence_payload()}, "discovery-evidence"))
        proposed = self.control.execute(
            self.agent["token"], operation("conclusion.propose", {
                "statement": "The Acme liability cap is one year of fees.",
                "evidence_refs": [imported["result"]["evidence"][0]],
                "proposer": "spoofed",
                "applicability": {
                    "title": "Acme liability-cap interpretation",
                    "keywords": ["Acme", "liability cap"],
                    "when_relevant": ["Reviewing Acme commercial contracts"],
                },
            }, "discovery-proposal"))
        self.assertTrue(proposed["ok"])
        conclusion = proposed["result"]["conclusion"]
        self.assertIsNone(conclusion["scope"])
        self.assertTrue(self.control.execute(
            self.agent["token"], operation("conclusion.evaluate", {
                "conclusion_id": conclusion["id"]}))["ok"])
        self.assertTrue(self.control.execute(
            self.owner["token"], operation("conclusion.review", {
                "conclusion_id": conclusion["id"], "decision": "admit",
                "reviewer": "spoofed", "request_id": "discovery-review"}))["ok"])

        discovery = self.control.execute(
            self.agent["token"], operation("context.discover", {
                "actor": "agent:other", "task": "Acme liability cap"}))
        self.assertTrue(discovery["ok"])
        self.assertEqual(discovery["result"]["actor"], "agent:codex-laptop")
        self.assertEqual(discovery["result"]["cards"][0]["id"], conclusion["id"])

    def test_revocation_is_immediate_and_agent_cannot_administer_credentials(self):
        with self.assertRaises(self.hosted.HostedAuthError):
            self.control.issue_agent_credential(
                self.agent["token"], "agent:forbidden", "forbidden")
        self.control.revoke_credential(
            self.owner["token"], self.agent["credential_id"])
        denied = self.control.execute(
            self.agent["token"], operation("capabilities.get", {}))
        self.assertFalse(denied["ok"])
        self.assertEqual(denied["error"]["code"], "invalid_credential")

    def test_agent_rotation_and_offline_owner_recovery_revoke_old_secrets(self):
        rotated = self.control.rotate_agent_credential(
            self.owner["token"], self.agent["credential_id"], "Codex rotated")
        old_agent = self.control.execute(
            self.agent["token"], operation("capabilities.get", {}))
        self.assertEqual(old_agent["error"]["code"], "invalid_credential")
        self.assertTrue(self.control.execute(
            rotated["token"], operation("capabilities.get", {}))["ok"])

        recovered = self.control.recover_owner(
            self.owner["workspace_id"], self.owner["recovery_secret"])
        old_owner = self.control.execute(
            self.owner["token"], operation("capabilities.get", {}))
        self.assertEqual(old_owner["error"]["code"], "invalid_credential")
        self.assertTrue(self.control.execute(
            recovered["token"], operation("capabilities.get", {}))["ok"])
        with self.assertRaises(self.hosted.HostedAuthError):
            self.control.recover_owner(
                self.owner["workspace_id"], self.owner["recovery_secret"])

    def test_remote_file_import_and_unsafe_permission_grants_fail_closed(self):
        denied = self.control.execute(
            self.agent["token"], operation("evidence.import", {"path": "/tmp/raw"}))
        self.assertFalse(denied["ok"])
        self.assertEqual(denied["error"]["code"], "operation_forbidden")
        owner_denied = self.control.execute(
            self.owner["token"], operation("evidence.import", {"path": "/tmp/raw"}))
        self.assertEqual(owner_denied["error"]["code"], "operation_forbidden")
        with self.assertRaisesRegex(ValueError, "safe-operation subset"):
            self.control.issue_agent_credential(
                self.owner["token"], "agent:unsafe", "unsafe",
                permissions={"conclusion.review"})

    def test_credentials_are_slow_hashes_and_audit_excludes_payloads(self):
        connection = sqlite3.connect(self.database)
        connection.row_factory = sqlite3.Row
        try:
            credential = connection.execute(
                "SELECT * FROM hosted_credentials WHERE credential_id = ?",
                (self.agent["credential_id"],)).fetchone()
            columns = set(credential.keys())
            self.assertNotIn("token", columns)
            self.assertNotIn("secret", columns)
            self.assertNotIn(self.agent["token"], json.dumps(dict(credential), default=str))
            self.control.execute(
                self.agent["token"], operation("capabilities.get", {}))
            audit = connection.execute("SELECT * FROM hosted_audit").fetchall()
            self.assertTrue(audit)
            self.assertNotIn("payload", set(audit[0].keys()))
        finally:
            connection.close()

    def test_idempotency_is_principal_scoped(self):
        second = self.control.issue_agent_credential(
            self.owner["token"], "agent:claude-desktop", "Claude desktop")
        request = operation(
            "evidence.submit", {"payload": evidence_payload()}, "shared-retry-key")
        first = self.control.execute(self.agent["token"], request)
        other = self.control.execute(second["token"], request)
        self.assertTrue(first["ok"])
        self.assertTrue(other["ok"])


if __name__ == "__main__":
    unittest.main()

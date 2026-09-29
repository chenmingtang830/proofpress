"""Shared-database isolation at the hosted service and mutation boundaries."""
from dataclasses import replace
import json
import os
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from proofpress.hosted import execution, review_policy
from proofpress.hosted.control_plane import HostedControlPlane
from proofpress.hosted.service import create_hosted_server
from proofpress.kernel import operations as kernel
from proofpress.kernel.events import SQLiteEventStore
from test_hosted_authority import evidence_payload, operation


class WorkspaceIsolationTests(unittest.TestCase):
    def configure_b(self):
        return self.control.save_review_policy(self.b_owner, {
            "mode": "off", "provider": "openrouter", "endpoint": "",
            "model": "", "criteria": "", "zdr": True,
            "rubric": "evidence-support/v1", "external_consent": False,
            "require_judge": False}, 0)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.database = Path(self.temp.name) / "shared.db"
        self.control = HostedControlPlane(self.database)
        self.a_owner = self.control.bootstrap("workspace:A", "human:owner")["token"]
        self.a_agent = self.control.issue_agent_credential(
            self.a_owner, "agent:same", "A agent")["token"]
        # A test fixture may add B to the same database; production bootstrap
        # must still refuse a second workspace.
        with self.control._db() as connection:
            connection.execute("INSERT INTO hosted_workspaces VALUES (?, ?)",
                               ("workspace:B", "2026-01-01T00:00:00Z"))
            for principal, role in (("human:owner", "owner"), ("agent:same", "agent")):
                connection.execute("INSERT INTO hosted_principals VALUES (?, ?, ?, ?, ?)",
                    ("workspace:B", principal, role, principal, "2026-01-01T00:00:00Z"))
                cred_id, token, salt, secret_hash = self.control._new_credential_values()
                connection.execute("INSERT INTO hosted_credentials VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL)",
                    (cred_id, "workspace:B", principal, principal, salt, secret_hash,
                     json.dumps(["*"] if role == "owner" else ["evidence.submit", "claim.propose",
                         "claim.evaluate", "review.receipt", "context.get", "capabilities.get"]),
                     "2026-01-01T00:00:00Z"))
                if role == "owner":
                    self.b_owner = token
                else:
                    self.b_agent = token

    def test_context_identity_is_revalidated_before_read_or_audit(self):
        self.configure_b()
        submitted = self.control.execute(self.b_agent, operation(
            "evidence.submit", {"payload": evidence_payload()}))
        self.assertTrue(submitted["ok"])
        b_context = self.control.authenticate(self.b_agent)
        a_context = self.control.authenticate(self.a_agent)
        with self.control._db() as connection:
            before = connection.execute("SELECT COUNT(*) FROM hosted_audit WHERE workspace_id='workspace:B'").fetchone()[0]
        for forged in (replace(a_context, workspace_id="workspace:B"),
                       replace(a_context, role="owner", permissions=frozenset({"*"})),
                       replace(a_context, credential_id=b_context.credential_id)):
            denied = self.control.execute_as(forged, operation(
                "claim.review", {"claim_id": "foreign", "decision": "admit",
                                 "reviewer": "human:owner", "request_id": "forged"}))
            self.assertFalse(denied["ok"])
            self.assertIn(denied["error"]["code"], {"invalid_credential", "operation_forbidden"})
        with self.control._db() as connection:
            after = connection.execute("SELECT COUNT(*) FROM hosted_audit WHERE workspace_id='workspace:B'").fetchone()[0]
        self.assertEqual(before, after)
        with self.assertRaisesRegex(ValueError, "already bootstrapped"):
            self.control.bootstrap("workspace:C", "human:owner")

    def test_policy_and_deployment_key_do_not_cross_workspace(self):
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "synthetic-a-only",
                                  "PROOFPRESS_JUDGE_MODEL": "synthetic-model"}):
            with self.control._db() as connection:
                a = self.control._current_policy(connection, "workspace:A")
                self.assertEqual(a["version"], 0)
                self.assertEqual(self.control._provider_credential(
                    connection, "workspace:A", "openrouter"), "synthetic-a-only")
                self.assertIsNone(self.control._provider_credential(
                    connection, "workspace:B", "openrouter"))
                self.assertFalse(self.control._credential_status(
                    connection, "workspace:B", "openrouter")["configured"])
                with kernel.using_policy({"digest": "ambient-other-workspace"}):
                    self.assertEqual(self.control._current_policy(
                        connection, "workspace:A")["policy"]["digest"], a["policy"]["digest"])
                    with self.assertRaisesRegex(ValueError, "workspace_policy_missing"):
                        self.control._current_policy(connection, "workspace:B")
                    with self.assertRaisesRegex(ValueError, "workspace_policy_missing"):
                        self.control._current_policy(connection, "workspace:missing")
                self.assertFalse(review_policy.public(a, {"configured": False})
                                 ["credential"]["configured"])
        self.assertEqual(self.control.execute(self.b_agent, operation(
            "capabilities.get", {}))["error"]["code"], "workspace_policy_missing")
        restarted = HostedControlPlane(self.database)
        self.assertIsNone(restarted.legacy_default_workspace_id)
        with self.assertRaisesRegex(ValueError, "workspace_policy_missing"):
            restarted._policy("workspace:A")
        explicit = HostedControlPlane(self.database, legacy_default_workspace_id="workspace:A")
        self.assertEqual(explicit._policy("workspace:A")["version"], 0)

    def test_identical_ids_and_retry_keys_remain_workspace_local(self):
        request = operation("evidence.submit", {"payload": evidence_payload()}, "shared-key")
        a = self.control.execute(self.a_agent, request)
        b = self.control.execute(self.b_agent, request)
        self.assertTrue(a["ok"])
        # B must first receive its own explicit policy; never copy A's defaults.
        self.assertFalse(b["ok"])
        self.configure_b()
        b = self.control.execute(self.b_agent, request)
        self.assertTrue(b["ok"])
        self.assertEqual(a["result"]["evidence"], b["result"]["evidence"])
        self.assertEqual(len(self.control.list_executions(self.a_owner)), 1)
        self.assertEqual(len(self.control.list_executions(self.b_owner)), 1)
        self.assertEqual(len(SQLiteEventStore(self.database, "workspace:A", "agent:same").list_events()),
                         len(SQLiteEventStore(self.database, "workspace:B", "agent:same").list_events()))

    def test_foreign_claim_reads_writes_and_context_are_isolated(self):
        self.configure_b()
        payload = evidence_payload()
        payload["source"]["uri"] = "workspace://b-private.pdf"
        payload["source"]["content_digest"] = "sha256:" + "c" * 64
        evidence = self.control.execute(self.b_agent, operation(
            "evidence.submit", {"payload": payload}))["result"]["evidence"][0]
        proposed = self.control.execute(self.b_agent, operation("claim.propose", {
            "title": "B private", "statement": "B-only governed content marker",
            "evidence_refs": [evidence], "proposer": "agent:same", "scope": "shared-topic",
        }))
        self.assertTrue(proposed["ok"])
        claim_id = proposed["result"]["claim"]["id"]
        self.assertTrue(self.control.execute(self.b_agent, operation(
            "claim.evaluate", {"claim_id": claim_id}))["ok"])
        self.assertTrue(self.control.execute(self.b_owner, operation(
            "claim.review", {"claim_id": claim_id, "decision": "admit",
                              "reviewer": "human:owner", "request_id": "b-review"}))["ok"])
        b_store = SQLiteEventStore(self.database, "workspace:B", "agent:same")
        b_head = b_store.head()
        for token, name, parameters in (
            (self.a_owner, "review.receipt", {"claim_id": claim_id}),
            (self.a_agent, "claim.evaluate", {"claim_id": claim_id}),
            (self.a_owner, "claim.review", {"claim_id": claim_id,
                                              "decision": "admit", "request_id": "a-foreign"}),
        ):
            result = self.control.execute(token, operation(name, parameters))
            self.assertFalse(result["ok"], (name, result))
            self.assertNotIn("B-only governed content marker", json.dumps(result))
        context = self.control.execute(self.a_agent, operation(
            "context.get", {"scope": "shared-topic"}))
        self.assertTrue(context["ok"])
        self.assertNotIn("B-only governed content marker", json.dumps(context))
        self.assertEqual(b_store.head(), b_head)

    def test_credential_administration_stays_with_owner_workspace(self):
        b_id = self.control.authenticate(self.b_agent).credential_id
        self.assertNotIn(b_id, [row["credential_id"] for row in
                           self.control.list_credentials(self.a_owner)])
        with self.assertRaisesRegex(ValueError, "active credential not found"):
            self.control.revoke_credential(self.a_owner, b_id)
        with self.assertRaisesRegex(ValueError, "active agent credential not found"):
            self.control.rotate_agent_credential(self.a_owner, b_id)
        self.assertEqual(self.control.authenticate(self.b_agent).credential_id, b_id)

    def test_owner_session_and_assistant_default_are_workspace_bound(self):
        server = create_hosted_server(
            self.database, port=0, legacy_default_workspace_id="workspace:A")
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            for name, token in (("a", self.a_owner), ("b", self.b_owner)):
                server.proofpress_owner_sessions[name] = {
                    "context": server.proofpress_control.authenticate(token),
                    "csrf": "synthetic-csrf", "expires_at": time.time() + 60}
            with patch.dict(os.environ, {"OPENROUTER_API_KEY": "synthetic-key",
                                      "PROOFPRESS_WORKSPACE_LABEL": "A label"}):
                base = f"http://127.0.0.1:{server.server_port}"
                def session(name):
                    with urlopen(Request(base + "/owner/api/session",
                                         headers={"Cookie": "pp_owner=" + name})) as response:
                        return json.loads(response.read())["result"]
                a, b = session("a"), session("b")
                self.assertEqual(a["workspace_id"], "workspace:A")
                self.assertEqual(a["workspace"], "A label")
                self.assertTrue(a["capabilities"]["assistant"])
                self.assertEqual(b["workspace_id"], "workspace:B")
                self.assertEqual(b["workspace"], "workspace:B")
                self.assertFalse(b["capabilities"]["assistant"])
                with urlopen(Request(base + "/owner/api/review-policy",
                                     headers={"Cookie": "pp_owner=b"})) as response:
                    initial_policy = json.loads(response.read())["result"]
                self.assertEqual(initial_policy["version"], 0)
                self.assertFalse(initial_policy["credential"]["configured"])
                request = Request(base + "/owner/api/ask",
                    data=json.dumps({"csrf": "synthetic-csrf", "question": "test",
                                     "snapshot": {"private": "B"}}).encode(),
                    headers={"Cookie": "pp_owner=b", "Content-Type": "application/json"},
                    method="POST")
                with self.assertRaises(HTTPError) as failed:
                    urlopen(request)
                self.assertEqual(failed.exception.code, 503)
                self.assertEqual(json.loads(failed.exception.read())["error"]["code"],
                                 "assistant_unconfigured")
                failed.exception.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_finish_and_recovery_reject_foreign_attempt(self):
        with self.control._db() as connection:
            a_id, error = execution.begin(connection, workspace_id="workspace:A",
                principal_id="agent:same", idempotency_key="same", operation="claim.evaluate",
                fingerprint="fingerprint", versions={}, input_refs={})
            self.assertIsNone(error)
            connection.commit()
            b_id, error = execution.begin(connection, workspace_id="workspace:B",
                principal_id="agent:same", idempotency_key="same", operation="claim.evaluate",
                fingerprint="fingerprint", versions={}, input_refs={})
            self.assertIsNone(error)
            with self.assertRaisesRegex(ValueError, "execution_attempt_not_found"):
                execution.finish(connection, b_id, {"ok": True},
                                 workspace_id="workspace:A", principal_id="agent:same")
            execution.resume(connection, workspace_id="workspace:A")
            states = connection.execute("SELECT workspace_id,state FROM hosted_executions").fetchall()
            self.assertEqual({row["workspace_id"]: row["state"] for row in states},
                             {"workspace:A": "interrupted", "workspace:B": "running"})
            execution.finish(connection, b_id, {"ok": True},
                             workspace_id="workspace:B", principal_id="agent:same")
            self.assertEqual(connection.execute(
                "SELECT state FROM hosted_execution_attempts WHERE attempt_id=?", (a_id,)).fetchone()[0],
                "interrupted")

    def test_judge_queue_and_recovery_are_scoped(self):
        with self.control._db() as connection:
            for workspace in ("workspace:A", "workspace:B"):
                connection.execute("INSERT INTO hosted_judge_jobs VALUES (?, ?, ?, ?, ?, 'running', ?, ?, '')",
                    (workspace, workspace, "claim", "digest", "agent:same", "2026-01-01", "2026-01-01"))
        with patch("proofpress.hosted.control_plane.threading.Thread"):
            self.control.resume_judge_jobs(workspace_id="workspace:A")
        with self.control._db() as connection:
            rows = connection.execute("SELECT workspace_id,state FROM hosted_judge_jobs").fetchall()
        self.assertEqual({row["workspace_id"]: row["state"] for row in rows},
                         {"workspace:A": "interrupted", "workspace:B": "running"})
        with self.control._db() as connection:
            connection.execute("UPDATE hosted_judge_jobs SET state='queued' WHERE workspace_id='workspace:B'")
        self.control.run_judge_jobs(workspace_id="workspace:A")
        with self.control._db() as connection:
            self.assertEqual(connection.execute(
                "SELECT state FROM hosted_judge_jobs WHERE workspace_id='workspace:B'").fetchone()[0],
                "queued")
        with self.assertRaisesRegex(ValueError, "workspace_id required"):
            self.control.run_judge_jobs()


if __name__ == "__main__":
    unittest.main()

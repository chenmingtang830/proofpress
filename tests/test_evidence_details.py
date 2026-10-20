"""Readable source labels never replace bound evidence or admission authority."""
import copy
from pathlib import Path
import tempfile
import unittest

from proofpress.hosted import mcp_http
from proofpress.hosted.control_plane import HostedControlPlane


def request(operation, parameters):
    return {"schema_version": "proofpress/local-operation/v1alpha1",
            "operation": operation, "parameters": parameters}


class EvidenceDetailsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.control = HostedControlPlane(Path(self.tmp.name) / "workspace.db")
        self.owner = self.control.bootstrap("workspace:labels", "human:owner")["token"]
        # Pre-existing evidence-submit permission must work without key rotation.
        self.agent = self.control.issue_agent_credential(
            self.owner, "agent:research", "Research",
            permissions={"evidence.submit", "claim.propose", "review.receipt"})["token"]
        quote = "Flat week: -2.4bn. Short-term pivot: 5200."
        payload = {"schema_version": "proofpress/retrieval-evidence/v1",
                   "source": {"uri": "urn:source:opaque-id", "content_digest": "sha256:" + "a" * 64},
                   "evidence": {"quote": quote, "locator": {"kind": "text_span", "start": 0, "end": len(quote), "text_digest": "sha256:" + "a" * 64}},
                   "retrieval": {"adapter": "test", "version": "1", "query": "flows", "config_digest": "sha256:" + "b" * 64}}
        imported = self.execute("evidence.submit", {"payload": payload})["result"]
        self.evidence_id = imported["imported_evidence"][0]
        proposed = self.execute("claim.propose", {"title": "Reported scenario", "statement": quote,
                                "evidence_refs": [self.evidence_id], "proposer": "spoofed"})["result"]
        self.claim_id = proposed["claim"]["id"]
        self.before = self.receipt()
        self.params = {"claim_id": self.claim_id, "evidence_id": self.evidence_id,
                       "evidence_digest": self.before["evidence"][0]["digest"],
                       "details": {"filename": "daily-research-example.md", "location": "Appendix · scenario table",
                                   "fields": [{"name": "US · flat week", "value": "-$2.4bn"}]},
                       "actor": "human:owner"}

    def execute(self, operation, parameters, token=None):
        return self.control.execute(token or self.agent, request(operation, parameters))

    def receipt(self):
        return self.execute("review.receipt", {"claim_id": self.claim_id})["result"]

    def test_mcp_records_attributed_labels_without_mutating_evidence_or_admission(self):
        args = {k: v for k, v in self.params.items() if k != "actor"}
        result = mcp_http.call_tool(self.control, self.control.authenticate(self.agent),
                                   "proofpress_describe_evidence", args, "https://example.test")
        after = self.receipt()
        self.assertEqual(result["description"]["actor"], "agent:research")
        self.assertEqual(after["evidence"], self.before["evidence"])
        self.assertEqual(after["claim"], self.before["claim"])
        self.assertEqual(after["evaluation"], self.before["evaluation"])
        self.assertIsNone(after["admission"])
        self.assertEqual(after["state"], "needs_review")
        self.assertEqual(after["evidence_details"][self.evidence_id]["details"], self.params["details"])
        self.assertEqual(after["evidence_details"][self.evidence_id]["authority"], "presentation_only")
        replay = self.execute("evidence.describe", self.params)["result"]
        self.assertEqual(replay["description"]["event_id"], result["description"]["event_id"])
        self.assertEqual(self.receipt()["ledger_head"], after["ledger_head"])

    def test_no_rebinding_hidden_claim_or_overwriting_original_description(self):
        for key, value in [("evidence_id", "evd_" + "f" * 16),
                           ("evidence_digest", "sha256:" + "f" * 64)]:
            with self.subTest(key=key):
                self.assertFalse(self.execute("evidence.describe", {**self.params, key: value})["ok"])
        self.assertTrue(self.execute("evidence.describe", self.params)["ok"])
        changed = copy.deepcopy(self.params)
        changed["details"]["filename"] = "different.md"
        self.assertFalse(self.execute("evidence.describe", changed)["ok"])
        self.assertEqual(self.receipt()["evidence_details"][self.evidence_id]["details"]["filename"], "daily-research-example.md")

    def test_read_only_credential_and_revocation_do_not_gain_metadata_writes(self):
        read_only = self.control.issue_agent_credential(
            self.owner, "agent:reader", "Reader", permissions={"review.receipt"})["token"]
        result = self.execute("evidence.describe", self.params, read_only)
        self.assertEqual(result["error"]["code"], "operation_forbidden")
        credential = self.control.authenticate(self.agent)
        self.control.revoke_credential(self.owner, credential.credential_id)
        self.assertEqual(self.execute("evidence.describe", self.params)["error"]["code"], "invalid_credential")

    def test_another_submitter_cannot_lock_the_proposers_source_description(self):
        other = self.control.issue_agent_credential(
            self.owner, "agent:other", "Other submitter")["token"]
        result = self.execute("evidence.describe", self.params, other)
        self.assertFalse(result["ok"])
        self.assertIn("claim proposer", result["error"]["message"])
        self.assertEqual(self.receipt()["evidence_details"], {})

    def test_descriptions_are_bounded_and_paths_are_not_filenames(self):
        for details in [
            {**self.params["details"], "filename": "/private/report.md"},
            {**self.params["details"], "filename": "C:\\private\\report.md"},
            {**self.params["details"], "fields": []},
            {**self.params["details"], "location": "x" * 601},
            {**self.params["details"], "approve": True},
        ]:
            with self.subTest(details=details):
                self.assertFalse(self.execute("evidence.describe", {**self.params, "details": details})["ok"])
        self.assertEqual(self.receipt()["evidence_details"], {})

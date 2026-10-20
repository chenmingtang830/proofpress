"""Submission checks are automatic; advice and admission remain independent."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from proofpress.hosted.control_plane import HostedControlPlane
from proofpress.kernel import operations as kernel
from proofpress.kernel.events import SQLiteEventStore
from test_hosted_authority import evidence_payload, operation


class AutomaticChecksTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.control = HostedControlPlane(Path(self.tmp.name) / "workspace.db")
        self.owner = self.control.bootstrap("workspace:checks", "human:owner")["token"]
        # A submitter does not need a new evaluate permission to receive checks.
        self.agent = self.control.issue_agent_credential(
            self.owner, "agent:research", "Research", permissions={
                "evidence.submit", "claim.propose", "review.receipt", "context.get"})["token"]
        evidence = self.control.execute(self.agent, operation(
            "evidence.submit", {"payload": evidence_payload()}))["result"]["evidence"]
        self.request = operation("claim.propose", {
            "title": "Liability cap",
            "statement": "The liability cap is one year of fees.",
            "scope": "test", "evidence_refs": evidence, "proposer": "spoofed",
        }, "proposal-one")
        self.store = SQLiteEventStore(self.control.database, "workspace:checks")

    def receipt(self, cid):
        return self.control.execute(self.agent, operation(
            "review.receipt", {"claim_id": cid}))["result"]

    def test_new_submission_checks_without_model_or_admission_and_replays_once(self):
        with patch.object(kernel, "judge_v2", side_effect=AssertionError("No model call")):
            proposed = self.control.execute(self.agent, self.request)
        self.assertTrue(proposed["ok"])
        result = proposed["result"]
        self.assertTrue(result["evaluation"]["eligible"])
        receipt = self.receipt(result["claim"]["id"])
        self.assertEqual(receipt["evaluation"], result["evaluation"])
        self.assertEqual(receipt["state"], "needs_review")
        self.assertIsNone(receipt["admission"])
        self.assertIsNone(receipt["recommendation"])
        self.assertIsNone(receipt["judge_job"])
        context = self.control.execute(self.agent, operation("context.get", {"scope": "test"}))
        self.assertEqual(context["result"]["governed_context"], [])
        events = self.store.list_events()
        replay = self.control.execute(self.agent, self.request)
        self.assertTrue(replay["ok"])
        self.assertEqual(replay["result"]["evaluation"], result["evaluation"])
        self.assertEqual(self.store.list_events(), events)

    def test_failed_requirements_are_recorded_instead_of_assumed_to_pass(self):
        self.request["parameters"]["expires_at"] = "2000-01-01T00:00:00Z"
        result = self.control.execute(self.agent, self.request)["result"]
        self.assertFalse(result["evaluation"]["eligible"])
        self.assertFalse(result["evaluation"]["checks"]["not_expired"])
        self.assertIsNone(self.receipt(result["claim"]["id"])["admission"])

    def test_replay_recovers_a_committed_proposal_missing_its_checks(self):
        with patch.object(kernel, "evaluate_v2", side_effect=SystemExit("interrupted")):
            with self.assertRaises(SystemExit):
                self.control.execute(self.agent, self.request)
        self.assertEqual(sum(e["type"] == "claim_proposed" for e in self.store.list_events()), 1)
        self.assertFalse(any(e["type"] == "policy_evaluated" for e in self.store.list_events()))
        # Recover the interrupted execution tracker as the server does on restart.
        from proofpress.hosted import execution
        with self.control._db() as connection:
            execution.resume(connection, workspace_id="workspace:checks")
        replay = self.control.execute(self.agent, self.request)
        self.assertTrue(replay["ok"])
        self.assertTrue(replay["result"]["evaluation"]["eligible"])
        self.assertEqual(sum(e["type"] == "claim_proposed" for e in self.store.list_events()), 1)
        self.assertEqual(sum(e["type"] == "policy_evaluated" for e in self.store.list_events()), 1)

    def test_check_execution_error_does_not_hide_the_saved_candidate(self):
        with patch.object(kernel, "evaluate_v2", side_effect=ValueError("verification unavailable")):
            proposed = self.control.execute(self.agent, self.request)
        self.assertTrue(proposed["ok"])
        self.assertIsNone(proposed["result"]["evaluation"])
        self.assertEqual(proposed["result"]["evaluation_error"]["message"], "verification unavailable")
        cid = proposed["result"]["claim"]["id"]
        self.assertIsNone(self.receipt(cid)["admission"])
        recovered = self.control.execute(self.agent, self.request)
        self.assertTrue(recovered["result"]["evaluation"]["eligible"])


if __name__ == "__main__":
    unittest.main()

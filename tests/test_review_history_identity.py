import unittest
from unittest.mock import patch
from proofpress.kernel import operations


class ReviewHistoryIdentityTests(unittest.TestCase):
    def test_receipt_preserves_recorded_roles_without_inventing_actor(self):
        row = {"id": "knw_test", "statement": "Finding", "evidence_refs": []}
        events = [
            {"type": "conclusion_proposed", "conclusion": {"proposer": "agent:codex"}},
            {"type": "policy_evaluated", "verifier": "verifier:deterministic"},
            {"type": "judge_recommended", "judge": "judge:independent", "model": "test-model"},
            {"type": "human_reviewed", "reviewer": "owner:richard", "note": "Narrow the scope"},
            {"type": "legacy_event"},
        ]
        for i, event in enumerate(events):
            event.update(event_id=str(i), subject_ref="knw_test", created_at="2026-09-02")
        projection = {name: {} for name in ["revision_requests", "evidence", "evaluations", "recommendations", "reviews", "admissions", "rejections", "supersessions"]}
        projection.update(conclusions={"knw_test": row}, events=events)
        with patch.object(operations, "v2_projection", return_value=projection), patch.object(operations, "v2_state", return_value="needs_review"):
            history = operations.receipt_v2("knw_test")["history"]
        self.assertEqual([event["actor"] for event in history], ["agent:codex", "verifier:deterministic", "judge:independent", "owner:richard", None])
        self.assertEqual(history[2]["model"], "test-model")
        self.assertEqual(history[3]["note"], "Narrow the scope")

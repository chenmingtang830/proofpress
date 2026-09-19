import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from proofpress.kernel import operations as kernel_ops
from proofpress.kernel.events import GitEventStore, MemoryEventStore, SQLiteEventStore, using_event_store


class DependencyLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.store = MemoryEventStore()
        self.context = using_event_store(self.store)
        self.context.__enter__()
        source = {"id": "src_test", "kind": "source", "name": "fixture"}
        source["record_hash"] = kernel_ops.digest(source)
        kernel_ops.append_v2({"type": "source_recorded", "subject_ref": source["id"], "record": source})
        evidence = {"id": "evd_test", "kind": "evidence", "source_ref": source["id"],
                    "source_digest": source["record_hash"], "observation": {"bounded": True}}
        evidence["digest"] = kernel_ops.digest(evidence)
        kernel_ops.append_v2({"type": "evidence_bound", "subject_ref": evidence["id"], "evidence": evidence})
        self.evidence = evidence["id"]

    def tearDown(self):
        self.context.__exit__(None, None, None)

    def claim(self, statement, allowed_actors=None):
        cid = kernel_ops.propose_v2(
            statement, [self.evidence], "repo:test", "agent:author",
        )["claim"]["id"]
        kernel_ops.review_v2(cid, "admit", "human:owner")
        if allowed_actors is not None:
            event = next(row for row in self.store.events
                         if row.get("type") == "claim_proposed" and row.get("subject_ref") == cid)
            event["claim"]["allowed_actors"] = allowed_actors
        return cid

    def dependency(self, dependent, upstream):
        rid = kernel_ops.propose_relation_v2(dependent, upstream, "depends_on", "agent:author")["relation"]["id"]
        kernel_ops.review_relation_v2(rid, "admit", "human:owner")
        return rid

    def reaffirm(self, cid):
        kernel_ops.reassess_v2(cid, "retain", "human:owner", "Fresh dependency approval",
                               "reaffirm-" + cid + "-" + str(len(kernel_ops.v2_events())),
                               kernel_ops.v2_head(), [])

    def test_withdrawal_invalidates_transitively_and_reassessment_restores_reuse(self):
        upstream = self.claim("B remains required")
        dependent = self.claim("A depends on B")
        transitive = self.claim("C depends on A")
        relation = self.dependency(dependent, upstream)
        self.dependency(transitive, dependent)
        self.reaffirm(dependent)
        self.reaffirm(transitive)

        before = kernel_ops.context_v2("repo:test")
        self.assertEqual({row["id"] for row in before["governed_context"]},
                         {upstream, dependent, transitive})
        withdrawn = kernel_ops.withdraw_v2(
            upstream, "human:owner", "Source was retracted", "withdraw-1", kernel_ops.v2_head())
        self.assertEqual(withdrawn["impact"]["direct"], [dependent])
        self.assertEqual(withdrawn["impact"]["transitive"], [transitive])
        projection = kernel_ops.v2_projection()
        self.assertEqual(kernel_ops.v2_state(projection, projection["claims"][upstream]), "withdrawn")
        self.assertEqual(kernel_ops.v2_state(projection, projection["claims"][dependent]), "dependency_invalidated")
        self.assertEqual(kernel_ops.v2_state(projection, projection["claims"][transitive]), "dependency_invalidated")
        self.assertNotIn(dependent, {row["id"] for row in kernel_ops.context_v2("repo:test")["governed_context"]})

        kernel_ops.reassess_v2(dependent, "retain", "human:owner",
                               "Independent evidence remains sufficient", "retain-1",
                               kernel_ops.v2_head(), [relation])
        projection = kernel_ops.v2_projection()
        self.assertEqual(kernel_ops.relation_state(projection, projection["relations"][relation]), "retired")
        self.assertEqual(kernel_ops.v2_state(projection, projection["claims"][dependent]), "admitted")
        self.assertEqual(kernel_ops.v2_state(projection, projection["claims"][transitive]), "dependency_invalidated")
        kernel_ops.reassess_v2(transitive, "retain", "human:owner",
                               "Reaffirm after upstream reassessment", "retain-2",
                               kernel_ops.v2_head(), [])
        receipt = kernel_ops.receipt_v2(dependent)
        self.assertTrue(receipt["prior_admissions"])
        self.assertEqual(receipt["admission"]["reassessment"], True)
        self.assertEqual(kernel_ops.v2_state(kernel_ops.v2_projection(),
                                             kernel_ops.v2_projection()["claims"][transitive]), "admitted")

    def test_reassessment_fails_closed_when_invalid_dependency_remains(self):
        upstream = self.claim("Required source")
        dependent = self.claim("Dependent conclusion")
        self.dependency(dependent, upstream)
        self.reaffirm(dependent)
        kernel_ops.withdraw_v2(upstream, "human:owner", "Retracted", "withdraw-2", kernel_ops.v2_head())
        with self.assertRaisesRegex(ValueError, "active invalid dependencies remain"):
            kernel_ops.reassess_v2(dependent, "retain", "human:owner", "Keep it", "retain-3",
                                   kernel_ops.v2_head(), [])

    def test_approved_dependency_cannot_disappear_through_general_rereview(self):
        upstream = self.claim("Required source")
        dependent = self.claim("Dependent conclusion")
        relation = self.dependency(dependent, upstream)
        self.reaffirm(dependent)
        for decision in ("reject", "request_changes"):
            with self.subTest(decision=decision), self.assertRaisesRegex(
                    ValueError, "only transition through claim reassessment"):
                kernel_ops.review_relation_v2(
                    relation, decision, "human:owner", "Change authority state",
                    request_id="relation-rereview-" + decision,
                    expected_head=kernel_ops.v2_head(),
                )
        self.assertEqual(
            kernel_ops.v2_state(kernel_ops.v2_projection(),
                                kernel_ops.v2_projection()["claims"][dependent]),
            "admitted",
        )

    def test_governance_request_id_conflicts_when_payload_changes(self):
        claim = self.claim("Withdrawn claim")
        head = kernel_ops.v2_head()
        kernel_ops.withdraw_v2(claim, "human:owner", "First reason", "same-request", head)
        with self.assertRaisesRegex(ValueError, "IDEMPOTENCY_KEY_CONFLICT"):
            kernel_ops.withdraw_v2(
                claim, "human:owner", "Different reason", "same-request", head)

    def test_receipt_redacts_dependents_hidden_from_actor(self):
        upstream = self.claim("Visible upstream")
        hidden = self.claim("Hidden dependent", ["agent:author"])
        self.dependency(hidden, upstream)
        receipt = kernel_ops.receipt_v2(upstream, "agent:reader")
        self.assertEqual(receipt["dependent_impact"]["direct_ids"], [])
        self.assertEqual(receipt["dependent_impact"]["transitive_ids"], [])
        self.assertEqual(receipt["dependent_impact"]["redacted"], 1)

    def test_memory_git_and_sqlite_replay_the_same_atomic_lifecycle(self):
        # The production operation is one physical event containing logical
        # lifecycle events, so every backend has the same failure boundary.
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
            os.chdir(root)
            try:
                stores = [MemoryEventStore(), GitEventStore("refs/proofpress/parity"),
                          SQLiteEventStore(root / "events.sqlite3", "workspace")]
                results = []
                for store in stores:
                    with using_event_store(store):
                        at = "2026-09-11T00:00:00Z"
                        relation = {"id": "rel_x", "type": "depends_on", "from": "a", "to": "b", "digest": "rd"}
                        events = [
                            {"type": "claim_proposed", "subject_ref": "a", "claim": {"id": "a"}},
                            {"type": "claim_proposed", "subject_ref": "b", "claim": {"id": "b"}},
                            {"type": "relation_proposed", "subject_ref": "rel_x", "relation": relation},
                            {"type": "relation_admitted", "subject_ref": "rel_x", "relation_digest": "rd", "policy_digest": kernel_ops.load_v2_policy()["digest"]},
                            {"type": "governance_transaction", "subject_ref": "a", "operation": "claim.reassess", "events": [
                                kernel_ops._transaction_child({"type": "relation_retired", "subject_ref": "rel_x", "claim_ref": "a", "reviewer": "human:owner"}, at),
                                kernel_ops._transaction_child({"type": "human_reviewed", "subject_ref": "a", "decision": "retain", "reviewer": "human:owner"}, at),
                                kernel_ops._transaction_child({"type": "claim_admitted", "subject_ref": "a", "reviewer": "human:owner"}, at),
                            ]},
                        ]
                        for event in events: kernel_ops.append_v2(event)
                        replay = kernel_ops.v2_projection(store.list_events())
                        results.append((kernel_ops.relation_state(replay, relation),
                                        replay["reviews"]["a"]["decision"],
                                        len(store.list_events())))
                self.assertEqual(results, [("retired", "retain", 5)] * 3)
            finally:
                os.chdir(previous)


if __name__ == "__main__":
    unittest.main()

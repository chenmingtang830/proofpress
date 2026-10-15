"""Blocked context entries follow a claim's lineage, not only its own state.

A claim that was sent back, re-proposed, or superseded is answered by later
claims. Agents act on ``required_action``, so it must point at the claim that
settles the lineage (and name it when the actor may read it) instead of asking
for another revision of a claim whose revision was already approved.
"""
import unittest

from proofpress.kernel import operations as kernel_ops
from proofpress.kernel.events import MemoryEventStore, using_event_store

SCOPE = "repo:lineage"


class ContextLineageTests(unittest.TestCase):
    def setUp(self):
        self.store = MemoryEventStore()
        self.context = using_event_store(self.store)
        self.context.__enter__()
        source = {"id": "src_lineage", "kind": "source", "name": "fixture"}
        source["record_hash"] = kernel_ops.digest(source)
        kernel_ops.append_v2({"type": "source_recorded", "subject_ref": source["id"],
                              "record": source})
        self.evidence = []
        for index in range(3):
            evidence = {"id": f"evd_lineage_{index}", "kind": "evidence",
                        "source_ref": source["id"], "source_digest": source["record_hash"],
                        "observation": {"bounded": True, "index": index}}
            evidence["digest"] = kernel_ops.digest(evidence)
            kernel_ops.append_v2({"type": "evidence_bound", "subject_ref": evidence["id"],
                                  "evidence": evidence})
            self.evidence.append(evidence["id"])

    def tearDown(self):
        self.context.__exit__(None, None, None)

    # Ledger builders: every step goes through the public kernel operations.

    def propose(self, statement, **kwargs):
        evidence = kwargs.pop("evidence", [self.evidence[0]])
        return kernel_ops.propose_v2(statement, evidence, SCOPE, "agent:author",
                                     **kwargs)["claim"]["id"]

    def revise(self, parent, statement):
        request = kernel_ops.v2_projection()["revision_requests"][parent]["event_id"]
        return self.propose(statement, qualifiers={"revision_of": parent,
                                                   "revision_request_ref": request})

    def send_back(self, cid):
        kernel_ops.review_v2(cid, "request_changes", "human:owner", "Narrow the claim.")

    def admit(self, cid):
        kernel_ops.review_v2(cid, "admit", "human:owner")

    def reject(self, cid):
        kernel_ops.review_v2(cid, "reject", "human:owner", "Evidence does not support it.")

    def restrict(self, cid, actors):
        event = next(row for row in self.store.events
                     if row.get("type") == "claim_proposed" and row.get("subject_ref") == cid)
        event["claim"]["allowed_actors"] = actors

    def blocked(self, actor="agent:reader"):
        packet = kernel_ops.context_v2(SCOPE, actor)
        return {row["id"]: row for row in packet["blocked"]}, \
            [row["id"] for row in packet["governed_context"]]

    def sent_back_twice_then_approved(self):
        original = self.propose("Original claim")
        self.send_back(original)
        middle = self.revise(original, "First revision")
        self.send_back(middle)
        approved = self.revise(middle, "Second revision")
        self.admit(approved)
        return original, middle, approved

    # context_v2 blocked entries.

    def test_approved_revision_settles_every_earlier_claim_in_the_line(self):
        original, middle, approved = self.sent_back_twice_then_approved()
        blocked, governed = self.blocked()
        self.assertEqual(governed, [approved])
        self.assertEqual(blocked[original]["reason"], "needs_revision")
        self.assertEqual(blocked[original]["required_action"], "use_successor")
        self.assertEqual(blocked[original]["successor_id"], approved)
        self.assertEqual(blocked[original]["successor_state"], "admitted")
        self.assertEqual(blocked[original]["lineage_path"], [original, middle, approved])
        self.assertEqual((blocked[middle]["required_action"], blocked[middle]["successor_id"],
                          blocked[middle]["lineage_path"]),
                         ("use_successor", approved, [middle, approved]))

    def test_pending_revision_asks_for_review_not_another_revision(self):
        original = self.propose("Original claim")
        self.send_back(original)
        pending = self.revise(original, "Revision awaiting review")
        blocked, _ = self.blocked()
        self.assertEqual((blocked[original]["required_action"], blocked[original]["successor_id"],
                          blocked[original]["successor_state"]),
                         ("review_successor", pending, "needs_review"))
        self.assertEqual(blocked[pending]["required_action"], "human_review")
        self.assertNotIn("successor_id", blocked[pending])

    def test_sent_back_revisions_name_the_latest_one_to_revise(self):
        original = self.propose("Original claim")
        self.send_back(original)
        latest = self.revise(original, "Revision also sent back")
        self.send_back(latest)
        blocked, _ = self.blocked()
        self.assertEqual((blocked[original]["required_action"], blocked[original]["successor_id"],
                          blocked[original]["successor_state"]),
                         ("propose_revision", latest, "needs_revision"))
        self.assertEqual(blocked[latest]["required_action"], "propose_revision")
        self.assertNotIn("successor_id", blocked[latest])

    def test_rejected_revision_leaves_the_original_request_open(self):
        original = self.propose("Original claim")
        self.send_back(original)
        rejected = self.revise(original, "Rejected revision")
        self.reject(rejected)
        blocked, _ = self.blocked()
        self.assertEqual(blocked[original]["required_action"], "propose_revision")
        self.assertNotIn("successor_id", blocked[original])
        self.revise(original, "Fresh revision after the rejection")

    def test_superseded_claim_names_its_approved_successor(self):
        old = self.propose("Old claim")
        self.admit(old)
        correction = self.propose("Correction", evidence=[self.evidence[1]])
        self.admit(correction)
        kernel_ops.supersede_v2(old, correction, "human:owner")
        blocked, governed = self.blocked()
        self.assertEqual(governed, [correction])
        self.assertEqual((blocked[old]["reason"], blocked[old]["required_action"],
                          blocked[old]["successor_id"]),
                         ("superseded", "use_successor", correction))

    def test_supersession_follows_the_replacement_state(self):
        old = self.propose("Old claim")
        self.admit(old)
        replacement = self.propose("Unreviewed replacement", evidence=[self.evidence[1]])
        kernel_ops.supersede_v2(old, replacement, "human:owner")
        blocked, _ = self.blocked()
        self.assertEqual((blocked[old]["required_action"], blocked[old]["successor_id"]),
                         ("review_successor", replacement))
        self.reject(replacement)
        blocked, _ = self.blocked()
        self.assertEqual(blocked[old]["required_action"], "human_review")
        self.assertNotIn("successor_id", blocked[old])

    def test_withdrawn_claim_without_successor_needs_no_agent_action(self):
        withdrawn = self.propose("Retracted claim")
        self.admit(withdrawn)
        kernel_ops.withdraw_v2(withdrawn, "human:owner", "Source was retracted",
                               "withdraw-lineage", kernel_ops.v2_head())
        blocked, _ = self.blocked()
        self.assertEqual((blocked[withdrawn]["reason"], blocked[withdrawn]["required_action"]),
                         ("withdrawn", "none"))
        self.assertNotIn("successor_id", blocked[withdrawn])

    def test_reproposal_that_was_approved_settles_the_rejected_claim(self):
        rejected = self.propose("Rejected claim")
        self.reject(rejected)
        successor = self.propose(
            "Corrected claim", evidence=[self.evidence[0], self.evidence[1]],
            reproposal_of=rejected,
            qualifiers={"reproposal_response": "Adds the operative schedule."})
        self.admit(successor)
        blocked, _ = self.blocked()
        self.assertEqual((blocked[rejected]["required_action"], blocked[rejected]["successor_id"]),
                         ("use_successor", successor))

    def test_supersession_cycle_terminates_without_naming_a_successor(self):
        first = self.propose("First claim")
        self.admit(first)
        second = self.propose("Second claim", evidence=[self.evidence[1]])
        self.admit(second)
        kernel_ops.supersede_v2(first, second, "human:owner")
        kernel_ops.supersede_v2(second, first, "human:owner")
        blocked, governed = self.blocked()
        self.assertEqual(governed, [])
        for cid in (first, second):
            self.assertEqual(blocked[cid]["required_action"], "human_review")
            self.assertNotIn("successor_id", blocked[cid])

    def test_successor_the_actor_may_not_read_is_never_named(self):
        original, middle, approved = self.sent_back_twice_then_approved()
        self.restrict(approved, ["agent:owner"])
        blocked, governed = self.blocked("agent:outsider")
        self.assertEqual(governed, [])
        self.assertNotIn(approved, blocked)
        for cid in (original, middle):
            self.assertEqual(blocked[cid]["required_action"], "human_review")
            for field in ("successor_id", "successor_state", "lineage_path"):
                self.assertNotIn(field, blocked[cid])
        blocked, _ = self.blocked("agent:owner")
        self.assertEqual(blocked[original]["successor_id"], approved)

    def test_restricted_claim_inside_the_path_hides_the_successor(self):
        original, middle, approved = self.sent_back_twice_then_approved()
        self.restrict(middle, ["agent:owner"])
        blocked, governed = self.blocked("agent:outsider")
        self.assertEqual(governed, [approved])
        self.assertEqual(blocked[original]["required_action"], "human_review")
        self.assertNotIn("successor_id", blocked[original])

    def test_quarantined_successor_is_not_offered_for_use(self):
        old = self.propose("Old claim")
        self.admit(old)
        correction = self.propose("Correction", evidence=[self.evidence[1]])
        self.admit(correction)
        kernel_ops.supersede_v2(old, correction, "human:owner")
        rival = self.propose("Rival reading", evidence=[self.evidence[2]])
        self.admit(rival)
        relation = kernel_ops.propose_relation_v2(correction, rival, "contradicts",
                                                  "agent:author")["relation"]["id"]
        kernel_ops.review_relation_v2(relation, "admit", "human:owner")
        blocked, governed = self.blocked()
        self.assertNotIn(correction, governed)
        self.assertEqual(blocked[old]["required_action"], "human_review")
        self.assertNotIn("successor_id", blocked[old])

    def test_dependency_invalidated_successor_is_not_offered_for_use(self):
        old = self.propose("Old claim")
        self.admit(old)
        correction = self.propose("Correction", evidence=[self.evidence[1]])
        self.admit(correction)
        upstream = self.propose("Upstream claim", evidence=[self.evidence[2]])
        self.admit(upstream)
        relation = kernel_ops.propose_relation_v2(correction, upstream, "depends_on",
                                                  "agent:author")["relation"]["id"]
        kernel_ops.review_relation_v2(relation, "admit", "human:owner")
        kernel_ops.supersede_v2(old, correction, "human:owner")
        blocked, governed = self.blocked()
        self.assertNotIn(correction, governed)
        self.assertEqual(blocked[correction]["required_action"], "reassess")
        self.assertEqual(blocked[old]["required_action"], "human_review")

    def test_successor_in_another_scope_is_still_named(self):
        old = self.propose("Old claim")
        self.admit(old)
        elsewhere = kernel_ops.propose_v2("Correction filed elsewhere", [self.evidence[1]],
                                          "repo:other", "agent:author")["claim"]["id"]
        self.admit(elsewhere)
        kernel_ops.supersede_v2(old, elsewhere, "human:owner")
        blocked, governed = self.blocked()
        self.assertEqual(governed, [])
        self.assertEqual((blocked[old]["required_action"], blocked[old]["successor_id"]),
                         ("use_successor", elsewhere))

    def test_line_forked_before_the_guard_resolves_to_the_approved_branch(self):
        original = self.propose("Original claim")
        self.send_back(original)
        approved = self.revise(original, "Approved revision")
        request = kernel_ops.v2_projection()["revision_requests"][original]["event_id"]
        fork = {"id": "clm_legacyfork00000", "kind": "claim", "statement": "Legacy fork",
                "evidence_refs": [self.evidence[1]], "artifact_refs": [], "scope": SCOPE,
                "proposer": "agent:author", "expires_at": None, "applicability": None,
                "reproposal_of": None, "created_at": kernel_ops.now(),
                "qualifiers": {"revision_of": original, "revision_request_ref": request}}
        fork["digest"] = kernel_ops.digest(fork)
        kernel_ops.append_v2({"type": "claim_proposed", "subject_ref": fork["id"], "claim": fork})
        self.admit(approved)
        blocked, _ = self.blocked()
        self.assertEqual((blocked[original]["required_action"], blocked[original]["successor_id"]),
                         ("use_successor", approved))
        self.assertEqual(blocked[fork["id"]]["required_action"], "human_review")


if __name__ == "__main__":
    unittest.main()

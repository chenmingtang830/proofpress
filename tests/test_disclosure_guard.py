"""Read operations never name a claim the reader may not read.

The ledger links restricted claims to readable ones through every edge a read
path follows: requested revisions, re-proposals, supersessions, contradictions
and their resolutions, dependencies, and run receipts and reliances. An
outsider then calls every read operation that takes a reader identity; no
restricted claim ID or statement may appear in anything that comes back. A new
read operation fails ``test_every_read_operation_with_a_reader_is_covered``
until it is added here.
"""
import json
import unittest

from proofpress.kernel import operations as kernel_ops
from proofpress.kernel.events import MemoryEventStore, using_event_store

SCOPE = "repo:disclosure"
OWNER, OUTSIDER = "agent:owner", "agent:outsider"
COVERED_READS = {"context.get", "context.discover", "graph.get", "graph.traverse",
                 "review.summary", "review.receipt", "run.get", "run.list"}


class DisclosureGuardTests(unittest.TestCase):
    def setUp(self):
        self.store = MemoryEventStore()
        self.context = using_event_store(self.store)
        self.context.__enter__()
        source = {"id": "src_disclosure", "kind": "source", "name": "fixture"}
        source["record_hash"] = kernel_ops.digest(source)
        kernel_ops.append_v2({"type": "source_recorded", "subject_ref": source["id"],
                              "record": source})
        self.evidence = []
        for index in range(2):
            evidence = {"id": f"evd_disclosure_{index}", "kind": "evidence",
                        "source_ref": source["id"], "source_digest": source["record_hash"],
                        "observation": {"bounded": True, "index": index}}
            evidence["digest"] = kernel_ops.digest(evidence)
            kernel_ops.append_v2({"type": "evidence_bound", "subject_ref": evidence["id"],
                                  "evidence": evidence})
            self.evidence.append(evidence["id"])
        self.secret, self.public = [], []

    def tearDown(self):
        self.context.__exit__(None, None, None)

    def claim(self, statement, new_evidence=False, **kwargs):
        refs = self.evidence if new_evidence else self.evidence[:1]
        cid = kernel_ops.propose_v2(statement, refs, SCOPE, "agent:author",
                                    **kwargs)["claim"]["id"]
        (self.secret if statement.startswith("SECRET") else self.public).append(cid)
        return cid

    def admitted(self, statement):
        cid = self.claim(statement)
        kernel_ops.review_v2(cid, "admit", "human:owner")
        return cid

    def stage(self, cid):
        """Give a candidate passing checks and current accepting advice (staged context)."""
        kernel_ops.evaluate_v2(cid)
        row = kernel_ops.v2_projection()["claims"][cid]
        kernel_ops.append_v2({"type": "judge_recommended", "subject_ref": cid,
                              "claim_digest": row["digest"],
                              "policy_digest": kernel_ops.load_v2_policy()["digest"],
                              "recommendation": "accept", "rationale": "test advice",
                              "judge": "judge:test"})
        return cid

    def send_back(self, cid):
        kernel_ops.review_v2(cid, "request_changes", "human:owner", "Narrow the claim.")

    def reject(self, cid):
        kernel_ops.review_v2(cid, "reject", "human:owner", "Evidence does not support it.")

    def revise(self, parent, statement):
        request = kernel_ops.v2_projection()["revision_requests"][parent]["event_id"]
        return self.claim(statement, qualifiers={"revision_of": parent,
                                                 "revision_request_ref": request})

    def repropose(self, rejected, statement):
        return self.claim(statement, new_evidence=True, reproposal_of=rejected,
                          qualifiers={"reproposal_response": "Adds the second receipt."})

    def relate(self, source, target, relation_type):
        rid = kernel_ops.propose_relation_v2(source, target, relation_type,
                                             "agent:author")["relation"]["id"]
        kernel_ops.review_relation_v2(rid, "admit", "human:owner")
        return rid

    def restrict_secrets(self):
        for cid in self.secret:
            event = next(row for row in self.store.events
                         if row.get("type") == "claim_proposed" and row.get("subject_ref") == cid)
            event["claim"]["allowed_actors"] = [OWNER]

    def build(self):
        """Link restricted and readable claims through every edge; return a run ID."""
        public_parent = self.claim("Public parent sent back")
        self.send_back(public_parent)
        self.revise(public_parent, "SECRET revision of a public claim")
        secret_parent = self.claim("SECRET parent sent back")
        self.send_back(secret_parent)
        self.stage(self.revise(secret_parent, "Public revision of a secret claim"))

        public_old = self.admitted("Public claim replaced by a secret one")
        kernel_ops.supersede_v2(public_old, self.admitted("SECRET replacement"), "human:owner")
        secret_old = self.admitted("SECRET claim replaced by a public one")
        kernel_ops.supersede_v2(secret_old, self.admitted("Public replacement"), "human:owner")

        secret_rejected = self.claim("SECRET rejected claim")
        self.reject(secret_rejected)
        self.repropose(secret_rejected, "Public re-proposal of a secret claim")
        public_rejected = self.claim("Public rejected claim")
        self.reject(public_rejected)
        self.repropose(public_rejected, "SECRET re-proposal of a public claim")

        self.relate(self.admitted("Public contested claim"),
                    self.admitted("SECRET contested claim"), "contradicts")
        winner = self.admitted("Public conflict winner")
        conflict = self.relate(winner, self.admitted("SECRET conflict loser"), "contradicts")
        kernel_ops.resolve_contradiction_v2(conflict, "supersede", "human:owner", winner,
                                            "The public reading wins.")

        dependent = self.admitted("Public claim that depends on a secret one")
        upstream = self.admitted("SECRET upstream claim")
        self.relate(dependent, upstream, "depends_on")
        kernel_ops.withdraw_v2(upstream, "human:owner", "Upstream was retracted",
                               "withdraw-upstream", kernel_ops.v2_head())
        self.relate(self.admitted("SECRET claim that depends on a public one"),
                    self.admitted("Public upstream claim"), "depends_on")

        self.restrict_secrets()
        run = kernel_ops.start_run_v1("Disclosure run", OWNER)
        receipt = kernel_ops.capture_context_v1(run["id"], OWNER, SCOPE)
        relied = next(row for row in receipt["claims"] if row["claim_id"] in self.secret)
        kernel_ops.record_reliance_v1(run["id"], receipt["id"], relied["claim_id"],
                                      relied["claim_digest"], "The owner relied on it.", OWNER)
        return run["id"]

    def reads(self, actor, run_id):
        return {
            "context.get": kernel_ops.context_v2(SCOPE, actor, "public claim", True),
            "context.discover": kernel_ops.discover_context_v2(actor, "public claim"),
            "graph.get": kernel_ops.graph_v2(SCOPE, actor),
            "graph.traverse": kernel_ops.traverse_graph_v2(self.public, SCOPE, actor,
                                                           None, 3, 48),
            "graph.traverse staged": kernel_ops.traverse_graph_v2(self.public, SCOPE, actor,
                                                                  None, 3, 48, "staged"),
            "review.summary": kernel_ops.summary_v2(SCOPE, actor),
            "review.receipt": [kernel_ops.receipt_v2(cid, actor) for cid in self.public],
            "run.get": kernel_ops.get_run_v1(run_id, actor),
            "run.list": kernel_ops.list_runs_v1(actor),
            "disclose": kernel_ops.disclose_v1("public claim", actor, SCOPE,
                                               seeds=self.public),
        }

    def test_no_read_operation_names_a_restricted_claim(self):
        reads = self.reads(OUTSIDER, self.build())
        self.assertEqual(set(reads) - {"disclose", "graph.traverse staged"}, COVERED_READS)
        staged = [row["statement"] for row in reads["context.get"]["staged_context"]]
        self.assertIn("Public revision of a secret claim", staged)
        for name, result in reads.items():
            text = json.dumps(result, default=str)
            with self.subTest(read=name):
                self.assertNotIn("SECRET", text)
                for cid in self.secret:
                    self.assertNotIn(cid, text)

    def test_the_owner_still_sees_restricted_claims(self):
        run_id = self.build()
        text = json.dumps(self.reads(OWNER, run_id), default=str)
        for cid in self.secret:
            self.assertIn(cid, text)
        owner_run = kernel_ops.get_run_v1(run_id, OWNER)
        self.assertNotIn("redacted_reliances", owner_run)
        self.assertNotIn("redacted_claims", owner_run["context_receipts"][0])
        outsider_run = kernel_ops.get_run_v1(run_id, OUTSIDER)
        self.assertEqual(outsider_run["redacted_reliances"], 1)
        self.assertGreater(outsider_run["context_receipts"][0]["redacted_claims"], 0)

    def test_unreadable_seed_reads_like_an_unknown_one(self):
        self.build()
        hidden, unknown = self.secret[0], "clm_unknown00000000"
        traversal = kernel_ops.traverse_graph_v2(self.public + [hidden, unknown], SCOPE,
                                                 OUTSIDER)
        entries = {row["claim_id"]: {k: v for k, v in row.items() if k != "claim_id"}
                   for row in traversal["blocked_neighbors"]
                   if row["claim_id"] in {hidden, unknown}}
        self.assertEqual(entries[hidden], entries[unknown])
        self.assertEqual(entries[hidden], {"reason": "not_found",
                                           "required_action": "human_review"})
        with self.assertRaisesRegex(ValueError, "claim not found"):
            kernel_ops.receipt_v2(hidden, OUTSIDER)

    def test_proposer_learns_nothing_about_claims_they_may_not_read(self):
        parent = self.claim("Public parent sent back")
        self.send_back(parent)
        kernel_ops.review_v2(self.revise(parent, "SECRET approved revision"), "admit", "human:owner")
        secret_parent = self.claim("SECRET parent sent back")
        self.send_back(secret_parent)
        secret_rejected = self.claim("SECRET rejected claim")
        self.reject(secret_rejected)
        self.restrict_secrets()
        requests = kernel_ops.v2_projection()["revision_requests"]

        def propose_as_outsider(statement, **kwargs):
            return kernel_ops.propose_v2(statement, self.evidence, SCOPE, OUTSIDER, **kwargs)

        with self.assertRaisesRegex(ValueError, "^this lineage is already answered; ask an owner how to proceed$"):
            propose_as_outsider("Another revision", qualifiers={
                "revision_of": parent, "revision_request_ref": requests[parent]["event_id"]})
        with self.assertRaisesRegex(ValueError, "^revision requires an existing request for changes$"):
            propose_as_outsider("Revision of a hidden claim", qualifiers={
                "revision_of": secret_parent,
                "revision_request_ref": requests[secret_parent]["event_id"]})
        with self.assertRaisesRegex(ValueError, "^re-proposal requires an existing rejected claim$"):
            propose_as_outsider("Re-proposal of a hidden claim", reproposal_of=secret_rejected,
                                qualifiers={"reproposal_response": "Adds the second receipt."})

    def test_guessing_a_hidden_revision_reads_like_any_other_refusal(self):
        parent = self.claim("Public parent sent back")
        self.send_back(parent)
        hidden = self.revise(parent, "SECRET approved revision")
        kernel_ops.review_v2(hidden, "admit", "human:owner")
        self.restrict_secrets()
        request = kernel_ops.v2_projection()["revision_requests"][parent]["event_id"]
        qualifiers = {"revision_of": parent, "revision_request_ref": request}
        for proposer in (OUTSIDER, "agent:author"):
            errors = []
            for guess in ("A wrong guess", "SECRET approved revision"):
                with self.assertRaises(ValueError) as caught:
                    kernel_ops.propose_v2(guess, self.evidence[:1], SCOPE, proposer,
                                          qualifiers=qualifiers)
                errors.append(str(caught.exception))
            with self.subTest(proposer=proposer):
                self.assertEqual(errors[0], errors[1])
                self.assertNotIn(hidden, errors[1])

    def test_immutable_conflict_does_not_name_a_hidden_claim(self):
        hidden = self.admitted("SECRET standalone claim")
        self.restrict_secrets()
        with self.assertRaises(ValueError) as caught:
            kernel_ops.propose_v2("SECRET standalone claim", self.evidence[:1], SCOPE, OUTSIDER)
        self.assertNotIn(hidden, str(caught.exception))

    def test_replay_does_not_return_a_claim_the_proposer_may_no_longer_read(self):
        self.claim("SECRET claim its author may no longer read")
        self.restrict_secrets()
        with self.assertRaisesRegex(ValueError, "^immutable claim conflict$"):
            kernel_ops.propose_v2("SECRET claim its author may no longer read", self.evidence[:1],
                                  SCOPE, "agent:author")

    def test_every_read_operation_with_a_reader_is_covered(self):
        reads = {name for name, spec in kernel_ops.LOCAL_OPERATION_SPECS.items()
                 if not spec["mutates"] and "actor" in spec["required"] + spec["optional"]}
        self.assertEqual(reads, COVERED_READS)


if __name__ == "__main__":
    unittest.main()

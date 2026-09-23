import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def evidence_payload():
    quote = "The Acme liability cap is one year of fees."
    return {
        "schema_version": "proofpress/retrieval-evidence/v1",
        "source": {"uri": "workspace://acme-msa.pdf",
                   "content_digest": "sha256:" + "a" * 64},
        "evidence": {"quote": quote, "locator": {
            "kind": "text_span", "start": 0, "end": len(quote),
            "text_digest": "sha256:" + hashlib.sha256(quote.encode()).hexdigest()}},
        "retrieval": {"adapter": "contract-review", "version": "1",
                      "query": "Acme liability cap",
                      "config_digest": "sha256:" + "b" * 64},
    }


class ContextDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"],
                       cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"],
                       cwd=self.repo, check=True)
        sys.path.insert(0, str(ROOT))
        from proofpress.kernel import operations
        self.kernel_ops = operations
        self.previous = Path.cwd()
        os.chdir(self.repo)

    def tearDown(self):
        os.chdir(self.previous)
        self.tmp.cleanup()

    def test_optional_claim_title_is_immutable_and_legacy_compatible(self):
        evidence = self.kernel_ops.submit_evidence_v2(evidence_payload())["evidence"][0]
        args = ("The Acme liability cap is one year of fees.", [evidence])
        old = self.kernel_ops.propose_v2(*args, proposer="agent:test")["claim"]
        self.assertNotIn("title", old)
        repeated = self.kernel_ops.propose_v2(*args, proposer="agent:test", title=None)["claim"]
        self.assertEqual(old, repeated)
        titled = self.kernel_ops.propose_v2(*args, proposer="agent:test", title="  Acme liability cap  ")["claim"]
        self.assertEqual(titled["title"], "Acme liability cap")
        self.assertEqual(titled["statement"], old["statement"])
        self.assertNotEqual(titled["id"], old["id"])
        self.assertNotEqual(titled["digest"], old["digest"])
        for invalid in ("", " ", 12, "a" * 121):
            with self.assertRaises(ValueError):
                self.kernel_ops.propose_v2(*args, proposer="agent:test", title=invalid)

    def test_public_proposals_require_title_and_statement(self):
        evidence = self.kernel_ops.submit_evidence_v2(evidence_payload())["evidence"][0]
        valid = {"title": "Acme cap", "statement": "One year of fees.", "evidence_refs": [evidence], "proposer": "agent:test"}
        def submit(parameters):
            return self.kernel_ops.execute_local_operation({"schema_version": self.kernel_ops.LOCAL_OPERATION_SCHEMA, "operation": "claim.propose", "parameters": parameters})
        self.assertTrue(submit(valid)["ok"])
        for field in ("title", "statement"):
            for value in (None, "", " ", 12):
                result = submit({**valid, field: value})
                self.assertFalse(result["ok"])
            missing = dict(valid)
            del missing[field]
            self.assertFalse(submit(missing)["ok"])

    def test_frontmatter_card_is_discoverable_without_a_scope(self):
        evidence = self.kernel_ops.submit_evidence_v2(evidence_payload())["evidence"][0]
        proposal = self.kernel_ops.propose_v2(
            "The Acme liability cap is one year of fees.", [evidence],
            proposer="agent:contract-review",
            applicability={
                "title": "Acme liability-cap interpretation",
                "description": "Current interpretation of Acme's MSA liability cap.",
                "when_relevant": ["Reviewing Acme commercial contracts"],
                "keywords": ["Acme", "MSA", "liability cap"],
                "validity_conditions": ["Only for the identified contract revision"],
            })
        claim = proposal["claim"]
        self.assertIsNone(claim["scope"])
        self.kernel_ops.evaluate_v2(claim["id"])
        self.kernel_ops.review_v2(claim["id"], "admit", "human:legal")

        visible = self.kernel_ops.discover_context_v2(
            actor="agent:legal", task="Review the Acme MSA liability cap")
        self.assertEqual([card["id"] for card in visible["cards"]], [claim["id"]])
        card = visible["cards"][0]
        self.assertEqual(card["legacy_scope"], None)
        self.assertEqual(card["title"], "Acme liability-cap interpretation")
        self.assertIn("acme", card["match"]["terms"])
        self.assertIn("liability", card["match"]["terms"])

        context = self.kernel_ops.context_v2(actor="agent:legal")
        self.assertEqual([row["id"] for row in context["governed_context"]], [claim["id"]])
        self.assertEqual([card["id"] for card in self.kernel_ops.discover_context_v2(
            actor="agent:other", task="Acme liability cap")["cards"]], [claim["id"]])

    def test_staged_context_is_separate_and_requires_current_accept_or_escalate(self):
        evidence = self.kernel_ops.submit_evidence_v2(evidence_payload())["evidence"][0]
        claim = self.kernel_ops.propose_v2(
            "The Acme liability cap is one year of fees.", [evidence],
            proposer="agent:contract-review", scope="contract-review")["claim"]
        evaluation = self.kernel_ops.evaluate_v2(claim["id"])
        policy = self.kernel_ops.load_v2_policy()

        def recommend(decision, *, claim_digest=None, policy_digest=None):
            return self.kernel_ops.append_v2({
                "type": "judge_recommended", "subject_ref": claim["id"],
                "claim_digest": claim_digest or claim["digest"],
                "policy_digest": policy_digest or policy["digest"],
                "recommendation": decision, "rationale": "test recommendation",
                "judge": "judge:test"})

        self.assertEqual(self.kernel_ops.context_v2(actor="agent:contract-review")["staged_context"], [])
        recommend("accept")
        packet = self.kernel_ops.context_v2(actor="agent:contract-review")
        self.assertEqual(packet["governed_context"], [])
        self.assertEqual([row["id"] for row in packet["staged_context"]], [claim["id"]])
        self.assertEqual(packet["staged_context"][0]["staging"]["status"], "ready_for_draft")
        restricted = {**policy, "allowed_actors": ["agent:contract-review"]}
        with self.kernel_ops.using_policy(restricted):
            self.assertEqual(self.kernel_ops.context_v2(actor="agent:other")["staged_context"], [])
        self.assertEqual(self.kernel_ops.context_v2(actor="agent:contract-review", scope="other")["staged_context"], [])

        recommend("escalate")
        escalated = self.kernel_ops.context_v2(actor="agent:contract-review")["staged_context"][0]
        self.assertEqual(escalated["staging"]["status"], "needs_attention")
        recommend("accept", claim_digest="sha256:stale")
        self.assertEqual(self.kernel_ops.context_v2(actor="agent:contract-review")["staged_context"], [])

    def test_a_reuse_boundary_requires_a_legacy_scope_or_applicability(self):
        evidence = self.kernel_ops.submit_evidence_v2(evidence_payload())["evidence"][0]
        proposal = self.kernel_ops.propose_v2(
            "An unbounded statement is not reusable.", [evidence],
            proposer="agent:contract-review")
        evaluation = self.kernel_ops.evaluate_v2(proposal["claim"]["id"])
        self.assertFalse(evaluation["checks"]["reuse_boundary_present"])
        receipt = evaluation["check_receipts"]["reuse_boundary_present"]
        self.assertIn("legacy scope", receipt["rule"])
        self.assertEqual(receipt["inputs"]["candidate"], proposal["claim"]["id"])
        self.assertEqual(receipt["inputs"]["bound_evidence"], [evidence])

    def test_relations_are_not_constrained_by_legacy_scope(self):
        evidence = self.kernel_ops.submit_evidence_v2(evidence_payload())["evidence"][0]
        left = self.kernel_ops.propose_v2(
            "The Acme MSA has a one-year cap.", [evidence], "contract",
            "agent:one", applicability={"keywords": ["Acme", "liability"]})["claim"]["id"]
        right = self.kernel_ops.propose_v2(
            "A product policy may impose a stricter exception.", [evidence], "policy",
            "agent:two", applicability={"keywords": ["policy", "exception"]})["claim"]["id"]
        relation = self.kernel_ops.propose_relation_v2(
            left, right, "qualifies", "agent:relation")["relation"]["id"]
        evaluation = self.kernel_ops.evaluate_relation_v2(relation)
        self.assertTrue(evaluation["eligible"])
        self.assertNotIn("same_scope", evaluation["checks"])

if __name__ == "__main__":
    unittest.main()

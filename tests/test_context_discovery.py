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
        self.knowledge = operations
        self.previous = Path.cwd()
        os.chdir(self.repo)

    def tearDown(self):
        os.chdir(self.previous)
        self.tmp.cleanup()

    def test_frontmatter_card_is_discoverable_without_a_scope(self):
        evidence = self.knowledge.submit_evidence_v2(evidence_payload())["evidence"][0]
        proposal = self.knowledge.propose_v2(
            "The Acme liability cap is one year of fees.", [evidence],
            proposer="agent:contract-review",
            applicability={
                "title": "Acme liability-cap interpretation",
                "description": "Current interpretation of Acme's MSA liability cap.",
                "when_relevant": ["Reviewing Acme commercial contracts"],
                "keywords": ["Acme", "MSA", "liability cap"],
                "validity_conditions": ["Only for the identified contract revision"],
            })
        conclusion = proposal["conclusion"]
        self.assertIsNone(conclusion["scope"])
        self.knowledge.evaluate_v2(conclusion["id"])
        self.knowledge.review_v2(conclusion["id"], "admit", "human:legal")

        visible = self.knowledge.discover_context_v2(
            actor="agent:legal", task="Review the Acme MSA liability cap")
        self.assertEqual([card["id"] for card in visible["cards"]], [conclusion["id"]])
        card = visible["cards"][0]
        self.assertEqual(card["legacy_scope"], None)
        self.assertEqual(card["title"], "Acme liability-cap interpretation")
        self.assertIn("acme", card["match"]["terms"])
        self.assertIn("liability", card["match"]["terms"])

        context = self.knowledge.context_v2(actor="agent:legal")
        self.assertEqual([row["id"] for row in context["knowledge"]], [conclusion["id"]])
        self.assertEqual([card["id"] for card in self.knowledge.discover_context_v2(
            actor="agent:other", task="Acme liability cap")["cards"]], [conclusion["id"]])

    def test_a_reuse_boundary_requires_a_legacy_scope_or_applicability(self):
        evidence = self.knowledge.submit_evidence_v2(evidence_payload())["evidence"][0]
        proposal = self.knowledge.propose_v2(
            "An unbounded statement is not reusable.", [evidence],
            proposer="agent:contract-review")
        evaluation = self.knowledge.evaluate_v2(proposal["conclusion"]["id"])
        self.assertFalse(evaluation["checks"]["reuse_boundary_present"])

    def test_relations_are_not_constrained_by_legacy_scope(self):
        evidence = self.knowledge.submit_evidence_v2(evidence_payload())["evidence"][0]
        left = self.knowledge.propose_v2(
            "The Acme MSA has a one-year cap.", [evidence], "contract",
            "agent:one", applicability={"keywords": ["Acme", "liability"]})["conclusion"]["id"]
        right = self.knowledge.propose_v2(
            "A product policy may impose a stricter exception.", [evidence], "policy",
            "agent:two", applicability={"keywords": ["policy", "exception"]})["conclusion"]["id"]
        relation = self.knowledge.propose_relation_v2(
            left, right, "qualifies", "agent:relation")["relation"]["id"]
        evaluation = self.knowledge.evaluate_relation_v2(relation)
        self.assertTrue(evaluation["eligible"])
        self.assertNotIn("same_scope", evaluation["checks"])

if __name__ == "__main__":
    unittest.main()

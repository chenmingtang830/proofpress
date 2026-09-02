import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/attribute_claim_failures_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("attribution", PATH)
module = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(module)


class ClaimFailureAttributionTests(unittest.TestCase):
    def test_attributes_shape_qualification_type_and_critic(self):
        claim = {"id": "C1", "requirement_id": "R1", "statement": "Buyer pays $10 and fees",
                 "claim_type": "observed_fact", "atom_ids": ["A1"], "evidence_ids": ["E1"],
                 "qualification": None}
        construction = {
            "evidence_atoms": [{"atom_id": "A1", "support_mode": "explicit",
                                "exact_excerpt": "Buyer pays $10 at closing", "qualification": "at closing"}],
            "evidence": [{"evidence_id": "E1"}],
            "requirements": [{"requirement_id": "R1", "type": "risk_signal"}],
            "critic_verdicts": {"C1": {"verdict": "supported"}},
        }
        categories = module.classify(claim, construction, "Review closing risk")
        self.assertIn("proposer_external_fact", categories)
        self.assertIn("overbroad_or_compound_claim", categories)
        self.assertIn("qualification_loss", categories)
        self.assertIn("fact_risk_conclusion_confusion", categories)
        self.assertIn("critic_false_accept", categories)

    def test_missing_receipt_and_atom_is_retrieval_and_atom_failure(self):
        categories = module.classify(
            {"id": "C", "requirement_id": "R", "statement": "Fact",
             "claim_type": "observed_fact", "atom_ids": [], "evidence_ids": []},
            {"evidence_atoms": [], "evidence": [], "requirements": [], "critic_verdicts": {}}, "")
        self.assertIn("retrieval_miss", categories)
        self.assertIn("erroneous_evidence_atom", categories)


if __name__ == "__main__":
    unittest.main()

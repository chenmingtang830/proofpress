import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/adapt_v10_semantic_candidate_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("v10_semantic_adapter", PATH)
runner = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(runner)


class V10SemanticCandidateAdapterTests(unittest.TestCase):
    def test_adapter_keeps_only_profile_eligible_supported_claims(self):
        source = {"requirements": [{"requirement_id": "F", "type": "factual_input",
                                    "required_evidence_type": "signed agreement"},
                                   {"requirement_id": "R", "type": "risk_signal"}],
                  "claims": [{"id": "C1", "requirement_id": "F", "claim_type": "observed_fact",
                              "statement": "x", "atom_ids": ["A1"]},
                             {"id": "C2", "requirement_id": "R", "claim_type": "risk_signal",
                              "statement": "y", "atom_ids": ["A2"]}],
                  "verdicts": [{"claim_id": "C1", "verdict": "supported"},
                               {"claim_id": "C2", "verdict": "supported"}],
                  "atoms": [{"atom_id": "A1", "evidence_id": "E1"},
                            {"atom_id": "A2", "evidence_id": "E2"}],
                  "receipts": {"E1": {"quote": "x", "locator": {}, "source": {}},
                               "E2": {"quote": "y", "locator": {}, "source": {}}}}
        result = runner.adapt(source, [{"requirement_id": "F", "status": "partial"}])["construction"]
        self.assertEqual([row["id"] for row in result["claims"]], ["C1"])
        self.assertEqual(result["authority"], "non-authoritative")
        self.assertEqual(result["requirements"][0]["status"], "partial")
        self.assertEqual(result["requirements"][0]["gap_reason"],
                         "supported_claim_set_is_incomplete")
        self.assertEqual(result["requirements"][1]["gap_reason"],
                         "profile_requires_domain_analysis")
        self.assertEqual(result["requirements"][1]["status"], "gap")
        self.assertTrue(result["requirements"][0]["missing_evidence"])
        self.assertIn("signed agreement", result["requirements"][0]["missing_evidence"])


if __name__ == "__main__":
    unittest.main()

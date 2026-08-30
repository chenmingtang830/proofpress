import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/regrade_lawyer_asks_private.py"
SPEC = importlib.util.spec_from_file_location("lawyer_regrade", PATH)
regrade = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(regrade)


class LawyerAskRegradeTests(unittest.TestCase):
    def grade(self, category):
        applicable = regrade.applicable_atoms(category)
        return {"atoms": [{"atom_id": atom_id, "applicable": atom_id in applicable,
                            "score": 1 if atom_id in applicable else 0, "finding": "ok"}
                           for atom_id, _ in regrade.RUBRIC_ATOMS],
                "unsupported_claims": 0, "citation_errors": 0, "authority_errors": 0}

    def test_category_applicability_is_frozen(self):
        self.assertIn("relation_reasoning", regrade.applicable_atoms("relation-dependent"))
        self.assertNotIn("relation_reasoning", regrade.applicable_atoms("novel"))
        self.assertIn("gap_handling", regrade.applicable_atoms("partial-gap"))

    def test_normalization_scores_only_applicable_atoms(self):
        result = regrade.normalize_grade(self.grade("novel"), "novel")
        self.assertEqual(result["rubric_fraction"], 1)
        self.assertEqual(sum(row["applicable"] for row in result["atoms"]), 4)

    def test_normalization_rejects_changed_applicability(self):
        grade = self.grade("novel")
        grade["atoms"][0]["applicable"] = False
        grade["atoms"][0]["score"] = 0
        with self.assertRaisesRegex(ValueError, "changed applicability"):
            regrade.normalize_grade(grade, "novel")

    def test_bounded_reference_excludes_unexpected_claims(self):
        graph = {"construction": {"claims": [
            {"id": "C1", "statement": "expected", "evidence_ids": ["E1"]},
            {"id": "C2", "statement": "excluded", "evidence_ids": ["E2"]}],
            "relations": [], "requirements": []}}
        ask = {"category": "graph-fully-covered", "expected_claim_ids": ["C1"],
               "expected_relation_ids": [], "expected_gap_ids": []}
        reference = regrade.bounded_reference(graph, ask)
        self.assertEqual([row["id"] for row in reference["expected_governed_claims"]], ["C1"])


if __name__ == "__main__":
    unittest.main()

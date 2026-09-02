import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/run_v10_extractor_ablation_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("v10_extractor_ablation", PATH)
runner = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(runner)


class V10ExtractorAblationTests(unittest.TestCase):
    def test_score_atoms_conditions_on_independent_sufficiency(self):
        atoms = [{"requirement_id": "covered"}, {"requirement_id": "partial-gap"}]
        reference = [
            {"requirement_id": "covered", "evidence_sufficient": True},
            {"requirement_id": "missed", "evidence_sufficient": True},
            {"requirement_id": "partial-gap", "evidence_sufficient": False},
        ]
        score = runner.score_atoms(atoms, reference)
        self.assertEqual(score["sufficient_atom_recall"], 0.5)
        self.assertEqual(score["gap_partial_atom_rate"], 1.0)

    def test_ablation_does_not_use_sol_as_extractor(self):
        self.assertNotIn("sol", {model for model, _ in runner.CONDITIONS.values()})

    def test_condition_labels_freeze_batch_size(self):
        self.assertEqual(runner.CONDITIONS["deepseek-b1"], ("deepseek", 1))
        self.assertEqual(runner.CONDITIONS["deepseek-b4"], ("deepseek", 4))


if __name__ == "__main__":
    unittest.main()

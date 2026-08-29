import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/aggregate_semantic_adjudications_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("semantic_majority", PATH)
runner = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(runner)


class SemanticMajorityTests(unittest.TestCase):
    def test_majority_set_requires_two_of_three(self):
        self.assertEqual(runner.majority_set([["a", "b"], ["a"], ["b", "c"]]), ["a", "b"])

    def test_majority_mapping_preserves_covered_rubric(self):
        rows = [[{"rubric_id": "rubric-1", "requirement_ids": ["R1"]}],
                [{"rubric_id": "rubric-1", "requirement_ids": ["R1", "R2"]}],
                []]
        self.assertEqual(runner.majority_mappings(rows),
                         [{"rubric_id": "rubric-1", "requirement_ids": ["R1"]}])


if __name__ == "__main__":
    unittest.main()

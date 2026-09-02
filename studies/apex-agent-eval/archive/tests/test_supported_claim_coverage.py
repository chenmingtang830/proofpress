import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/score_supported_claim_coverage_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("supported_coverage", PATH)
runner = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(runner)


class SupportedClaimCoverageTests(unittest.TestCase):
    def test_coverage_requires_a_non_unsupported_claim(self):
        labels = {"requirement_to_rubric": [
            {"rubric_id": "A", "requirement_ids": ["R1"]},
            {"rubric_id": "B", "requirement_ids": ["R2"]}],
            "factual_claim_ids": ["C1", "C2"],
            "unsupported_factual_claim_ids": ["C1"]}
        raw = {"construction": {"claims": [
            {"id": "C1", "requirement_id": "R1"},
            {"id": "C2", "requirement_id": "R2"}]}}
        self.assertEqual(runner.task_coverage(labels, raw), (1, 2, .5))

    def test_non_factual_claim_does_not_count_as_supported(self):
        labels = {"requirement_to_rubric": [{"rubric_id": "A", "requirement_ids": ["R1"]}],
                  "factual_claim_ids": [], "unsupported_factual_claim_ids": []}
        raw = {"construction": {"claims": [{"id": "C1", "requirement_id": "R1"}]}}
        self.assertEqual(runner.task_coverage(labels, raw), (0, 1, 0.0))

    def test_bootstrap_is_deterministic(self):
        self.assertEqual(runner.paired_bootstrap([.1, .2]), runner.paired_bootstrap([.1, .2]))


if __name__ == "__main__":
    unittest.main()

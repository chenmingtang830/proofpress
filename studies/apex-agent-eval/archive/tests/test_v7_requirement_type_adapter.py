import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/classify_v7_requirements_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("v7_types", PATH)
runner = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(runner)


class V7RequirementTypeAdapterTests(unittest.TestCase):
    def test_assignments_preserve_requirement_text_and_order(self):
        requirements = [{"requirement_id": "R1", "requirement": "one"},
                        {"requirement_id": "R2", "requirement": "two"}]
        result = runner.apply_assignments(requirements, {"assignments": [
            {"requirement_id": "R2", "requirement_type": "risk_signal"},
            {"requirement_id": "R1", "requirement_type": "factual_input"}]})
        self.assertEqual([row["requirement"] for row in result], ["one", "two"])
        self.assertEqual([row["type"] for row in result], ["factual_input", "risk_signal"])

    def test_assignment_requires_exact_id_coverage(self):
        with self.assertRaisesRegex(ValueError, "coverage"):
            runner.apply_assignments([{"requirement_id": "R1"}], {"assignments": []})


if __name__ == "__main__":
    unittest.main()

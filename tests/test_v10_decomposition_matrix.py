import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/run_v10_decomposition_matrix_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("v10_decomposition", PATH)
matrix = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(matrix)


class V10DecompositionMatrixTests(unittest.TestCase):
    def test_schema_requires_evidence_type_and_atomic_limit(self):
        self.assertIn("required_evidence_type", matrix.REQUIREMENT_ITEM["required"])
        self.assertEqual(matrix.DECOMPOSITION_OUTPUT["properties"]["requirements"]["maxItems"], 40)
        self.assertIn("conflict", matrix.EVIDENCE_TYPES)


if __name__ == "__main__":
    unittest.main()

import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/rescore_v10_construction_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("v10_rescore", PATH)
runner = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(runner)


class V10ConstructionRescoreTests(unittest.TestCase):
    def test_rescore_has_distinct_schema(self):
        self.assertEqual(runner.SCHEMA, "proofpress/v10-construction-frozen-rescore/v1")


if __name__ == "__main__":
    unittest.main()

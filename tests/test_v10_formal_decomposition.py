import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/run_v10_formal_decomposition_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("v10_formal_decomposition", PATH)
runner = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(runner)


class V10FormalDecompositionTests(unittest.TestCase):
    def test_formal_route_is_frozen_qwen(self):
        self.assertEqual(runner.MODEL_LABEL, "qwen")
        self.assertEqual(runner.TASK_COUNT, 12)

    def test_task_manifest_requires_exact_unique_panel(self):
        with self.assertRaisesRegex(ValueError, "twelve"):
            runner.tasks_from_manifest([{"task_id": "one", "prompt": "p"}])


if __name__ == "__main__":
    unittest.main()

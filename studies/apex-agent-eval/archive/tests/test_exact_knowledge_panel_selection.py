import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "studies/apex-agent-eval/retrieval_adapter"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ADAPTER))
SPEC = importlib.util.spec_from_file_location(
    "exact_knowledge_stage_a", ADAPTER / "run_exact_knowledge_stage_a_private.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class ExactKnowledgePanelSelectionTests(unittest.TestCase):
    def test_future_construction_defaults_to_the_pinned_low_cost_deepseek_route(self):
        self.assertEqual(module.ROUTE, {"model": "deepseek/deepseek-v4-flash",
                                        "provider": "alibaba", "reasoning": "high"})

    def test_development_panel_uses_the_fixed_development_set(self):
        self.assertEqual(module._resolve_task_ids(None, "development"), module.TASK_IDS)

    def test_task_heldout_requires_an_explicit_frozen_id_file(self):
        with self.assertRaisesRegex(ValueError, "requires an explicit"):
            module._resolve_task_ids(None, "task-heldout")

    def test_custom_frozen_panel_cannot_be_mislabeled_as_development(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "panel.json"
            path.write_text(json.dumps(["task_private"]))
            with self.assertRaisesRegex(ValueError, "only valid for the task-heldout"):
                module._resolve_task_ids(path, "development")

    def test_task_heldout_panel_rejects_duplicate_task_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "panel.json"
            path.write_text(json.dumps(["task_private", "task_private"]))
            with self.assertRaisesRegex(ValueError, "duplicate"):
                module._resolve_task_ids(path, "task-heldout")


if __name__ == "__main__":
    unittest.main()

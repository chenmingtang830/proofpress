import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/build_nonlegal_transfer_panel_private.py"
SPEC = importlib.util.spec_from_file_location("nonlegal_panel", PATH)
panel = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(panel)


class NonlegalTransferPanelTests(unittest.TestCase):
    def test_panel_covers_every_family_and_variant(self):
        tasks = panel.build_tasks(); panel.validate_tasks(tasks)
        self.assertEqual(len(tasks), 9)
        self.assertEqual({row["family"] for row in tasks}, set(panel.FAMILIES))
        self.assertEqual({row["variant"] for row in tasks}, set(panel.VARIANTS))

    def test_sanitized_panel_omits_prompt_and_gold(self):
        with tempfile.TemporaryDirectory() as temp:
            result = panel.write_panel(Path(temp))
        encoded = panel.canonical(result).decode()
        self.assertNotIn("gross margin", encoded)
        self.assertNotIn("40.00%", encoded)
        self.assertFalse(result["automatic_admission"])
        self.assertTrue(result["human_approval_required"])


if __name__ == "__main__":
    unittest.main()

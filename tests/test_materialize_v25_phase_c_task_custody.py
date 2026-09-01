import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "studies/apex-agent-eval/retrieval_adapter"
sys.path.insert(0, str(ROOT))
SPEC = importlib.util.spec_from_file_location(
    "v25_task_custody", ADAPTER / "materialize_v25_phase_c_task_custody_private.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


DEVELOPMENT = [f"dev_{index}" for index in range(5)]
HELDOUT = [f"heldout_{index}" for index in range(7)]


def source_task(task_id, *, overlay=False):
    return {"task_id": task_id, "prompt": "private prompt", "expected_output": "respond",
            "rubric": [{"criteria": "private"}], "task_name": "Private task",
            "world_id": "private_world", "gold_response": "must never copy",
            "task_input_files": ["private-input"] if overlay else []}


class MaterializeV25TaskCustodyTests(unittest.TestCase):
    def test_only_frozen_fields_are_copied_and_overlay_is_task_scoped(self):
        manifest = {"development_task_ids": DEVELOPMENT, "held_out_task_ids": HELDOUT}
        source = [source_task(task_id, overlay=task_id == HELDOUT[0]) for task_id in HELDOUT]
        with tempfile.TemporaryDirectory() as tmp:
            files = Path(tmp) / "task-files"
            (files / HELDOUT[0]).mkdir(parents=True)
            custody, overlays, receipt = module.build(frozen_manifest=manifest, source_tasks=source,
                                                       task_files_root=files)
        self.assertEqual(set(custody), set(HELDOUT))
        self.assertNotIn("gold_response", custody[HELDOUT[0]]["task"])
        self.assertIn("rubric", custody[HELDOUT[0]]["task"])
        self.assertEqual(receipt["overlay_task_count"], 1)
        scoped = {row["task_id"]: row["overlay_root"] for row in overlays["overlays"]}
        self.assertIsNotNone(scoped[HELDOUT[0]])
        self.assertIsNone(scoped[HELDOUT[1]])

    def test_missing_expected_overlay_fails_closed(self):
        manifest = {"development_task_ids": DEVELOPMENT, "held_out_task_ids": HELDOUT}
        source = [source_task(task_id, overlay=task_id == HELDOUT[0]) for task_id in HELDOUT]
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "overlay is missing"):
                module.build(frozen_manifest=manifest, source_tasks=source,
                             task_files_root=Path(tmp) / "task-files")

    def test_single_path_overlay_metadata_is_supported_without_copying_it(self):
        manifest = {"development_task_ids": DEVELOPMENT, "held_out_task_ids": HELDOUT}
        source = [source_task(task_id, overlay=task_id == HELDOUT[0]) for task_id in HELDOUT]
        source[0]["task_input_files"] = "private/path/is-not-copied"
        with tempfile.TemporaryDirectory() as tmp:
            files = Path(tmp) / "task-files"
            (files / HELDOUT[0]).mkdir(parents=True)
            _, overlays, _ = module.build(frozen_manifest=manifest, source_tasks=source,
                                          task_files_root=files)
        self.assertIsNotNone(overlays["overlays"][0]["overlay_root"])


if __name__ == "__main__":
    unittest.main()

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/build_phase_c_task_controls_private.py"
SPEC = importlib.util.spec_from_file_location("phase_c_task_controls", BUILDER_PATH)
builder = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(builder)
MANIFEST = json.loads((ROOT / "studies/apex-agent-eval/results/exact-knowledge-transfer-v25-manifest.json").read_text())


class PhaseCTaskControlTests(unittest.TestCase):
    def write_tasks(self, root: Path):
        identifiers = MANIFEST["development_task_ids"] + MANIFEST["held_out_task_ids"]
        for index, task_id in enumerate(identifiers):
            value = {"task": {"task_id": task_id, "prompt": f"private prompt {index}",
                                "expected_output": "message_in_console", "rubric": [{"id": f"r{index}"}],
                                "gold_response": "must not be copied"}}
            (root / f"{index}.json").write_text(json.dumps(value))

    def test_compiles_disjoint_executor_and_grader_controls(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); self.write_tasks(root)
            source, rubrics, receipt = builder.build(manifest=MANIFEST, task_root=root)
        self.assertEqual(len(source["tasks"]), 12)
        self.assertEqual(len(rubrics["rubrics"]), 12)
        self.assertTrue(all("rubric" not in row for row in source["tasks"]))
        self.assertNotIn("gold_response", json.dumps(source))
        self.assertTrue(all("prompt" not in row for row in rubrics["rubrics"]))
        self.assertFalse(receipt["automatic_admission"])
        self.assertTrue(receipt["task_source_digest"].startswith("sha256:"))

    def test_rejects_missing_or_unexpected_task_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); self.write_tasks(root)
            (root / "0.json").unlink()
            with self.assertRaisesRegex(ValueError, "do not match frozen panel"):
                builder.build(manifest=MANIFEST, task_root=root)


if __name__ == "__main__":
    unittest.main()

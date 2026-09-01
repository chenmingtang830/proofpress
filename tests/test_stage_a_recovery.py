import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "studies/apex-agent-eval/retrieval_adapter"
sys.path.insert(0, str(ADAPTER))
SPEC = importlib.util.spec_from_file_location(
    "stage_a_recovery", ADAPTER / "run_exact_knowledge_stage_a_private.py")
stage = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(stage)


class StageARecoveryTests(unittest.TestCase):
    def test_constructor_task_payload_excludes_custody_rubric(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for task_id in stage.TASK_IDS:
                (root / f"{task_id}.json").write_text(json.dumps({"task": {
                    "task_id": task_id, "prompt": "private prompt",
                    "expected_output": "make_new_doc", "rubric": {"gold": "must not reach constructor"},
                }}))
            tasks = stage._load_tasks(root, stage.TASK_IDS)
        self.assertEqual(len(tasks), len(stage.TASK_IDS))
        self.assertTrue(all(set(task) == {"task_id", "prompt", "expected_output"} for task in tasks))
        self.assertTrue(all("rubric" not in task and "gold" not in task for task in tasks))

    def test_session_reuse_requires_identical_controls(self):
        controls = {"route": {"model": "fixed"}, "task_input_digest": "sha256:abc"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first, resumed_first = stage._initialize_or_validate_session(root, controls)
            second, resumed_second = stage._initialize_or_validate_session(root, controls)
            self.assertFalse(resumed_first)
            self.assertTrue(resumed_second)
            self.assertEqual(first, second)
            with self.assertRaisesRegex(ValueError, "incompatible controls"):
                stage._initialize_or_validate_session(root, {**controls, "timeout_seconds": 361})

    def test_checkpoint_requires_private_artifact_digest_for_ok_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = root / "raw"; raw.mkdir()
            checkpoints = root / "checkpoints"; checkpoints.mkdir()
            private = {"schema_version": "private", "only": "custody"}
            stage._write_private_json(raw / "task_1.json", private)
            summary = {"task_id": "task_1", "status": "ok",
                       "private_artifact_digest": stage.digest(private)}
            stage._write_checkpoint(checkpoints, "sha256:controls", summary)
            self.assertEqual(stage._load_checkpoint(checkpoints, raw, "task_1", "sha256:controls"), summary)
            stage._write_private_json(raw / "task_1.json", {"schema_version": "changed"})
            with self.assertRaisesRegex(ValueError, "digest mismatches"):
                stage._load_checkpoint(checkpoints, raw, "task_1", "sha256:controls")


if __name__ == "__main__":
    unittest.main()

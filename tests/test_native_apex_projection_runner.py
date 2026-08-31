import importlib.util
import subprocess
import tempfile
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "studies/apex-agent-eval/retrieval_adapter"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ADAPTER))
SPEC = importlib.util.spec_from_file_location(
    "native_apex_projection_runner", ADAPTER / "run_native_apex_projection_private.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class NativeApexProjectionRunnerTests(unittest.TestCase):
    def test_executor_messages_exclude_rubric_and_preserve_projection_boundary(self):
        task = {"task_id": "task_1", "prompt": "private task", "expected_output": "make_new_doc",
                "rubric": [{"criteria": "private score", "verifier_id": "v1"}]}
        projection = {"condition": "ordinary-claim", "automatic_admission": False,
                      "human_approval_required": True, "claims": [{"claim_id": "c1"}]}
        messages = module.initial_messages(task, projection)
        rendered = "\n".join(row["content"] for row in messages)
        self.assertEqual(messages[-1]["content"], "private task")
        self.assertNotIn("private score", rendered)
        self.assertIn("not admitted knowledge", messages[1]["content"])

    def test_executor_task_rejects_missing_native_output_contract(self):
        with self.assertRaisesRegex(ValueError, "expected_output"):
            module._executor_task({"task_id": "task_1", "prompt": "private"})

    def test_official_grader_receives_the_executor_trajectory_id(self):
        # The private runner must preserve the native lifecycle identity rather
        # than manufacture a different ID after the snapshot exists.
        self.assertIn("trajectory_id=trajectory_id", Path(module.__file__).read_text())

    def test_private_world_metadata_does_not_expand_executor_task(self):
        task = module._with_world_id({"task_id": "task_1", "prompt": "private",
                                      "expected_output": "make_new_doc"}, "world_private")
        self.assertEqual(task["world_id"], "world_private")
        self.assertNotIn("world_id", module._executor_task(task))

    def test_process_receipt_exposes_hashes_not_raw_diagnostics(self):
        with tempfile.TemporaryDirectory() as tmp:
            receipt = module._private_process_receipt(
                Path(tmp), "agent", subprocess.CompletedProcess([], 1, "private stdout", "private stderr"))
            self.assertEqual(receipt["returncode"], 1)
            self.assertNotIn("private stdout", str(receipt))
            self.assertTrue((Path(tmp) / "agent_stderr_private.log").is_file())

    def test_loads_the_official_all_oss_mcp_configuration(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Path(tmp)
            config = harness / "examples/hugging_face_task/mcp_config_all_oss_servers.json"
            config.parent.mkdir(parents=True)
            config.write_text(json.dumps({"mcpServers": {"filesystem": {"transport": "stdio"}}}))
            loaded = module._official_mcp_config(harness)
            self.assertEqual(sorted(loaded["mcpServers"]), ["filesystem"])

    def test_native_reset_force_recreates_without_a_build_or_volume_teardown(self):
        source = Path(module.__file__).read_text()
        self.assertIn('"--force-recreate", "--no-build"', source)
        self.assertNotIn('"compose", "down", "-v"', source)
        self.assertEqual(module.ENVIRONMENT_START_ATTEMPTS, 3)
        self.assertIn('environment_start_{attempt}', source)

    def test_agent_step_budget_is_not_a_low_experimental_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = json.loads(module._agent_config(Path(tmp)).read_text())
        values = config["agent_config_values"]
        self.assertEqual(values["timeout"], 3600)
        self.assertGreaterEqual(values["max_steps"], 10_000)


if __name__ == "__main__":
    unittest.main()

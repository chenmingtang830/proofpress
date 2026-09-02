import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/build_phase_c_gateway_config_private.py"
SPEC = importlib.util.spec_from_file_location("build_phase_c_gateway_config", BUILDER_PATH)
builder = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(builder)


class BuildPhaseCGatewayConfigTests(unittest.TestCase):
    def test_pins_bridge_adapter_and_no_fallback_policy(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            adapter, bridge = root / "adapter.py", root / "bridge.mjs"
            adapter.write_text("adapter")
            bridge.write_text("bridge")
            value = builder.build(role="grader", adapter=adapter, bridge=bridge,
                                  model="openai/gpt-5.6-terra", provider="openai",
                                  reasoning_effort="high", max_output_tokens=100, timeout_seconds=5)
            self.assertEqual(value["blind_grades_per_artifact"], 3)
            self.assertEqual(value["gateway_policy"]["fallback"], "forbidden")
            self.assertIn("--gateway-provider-only", value["command"])
            self.assertEqual(value["implementation_files"][0]["digest"], builder.file_digest(adapter))

    def test_rejects_missing_implementation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bridge = root / "bridge.mjs"; bridge.write_text("bridge")
            with self.assertRaisesRegex(ValueError, "regular files"):
                builder.build(role="executor", adapter=root / "missing.py", bridge=bridge,
                              model="openai/gpt-5.6-terra", provider="openai",
                              reasoning_effort="high", max_output_tokens=100, timeout_seconds=5)


if __name__ == "__main__":
    unittest.main()

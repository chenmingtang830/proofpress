import importlib.util
import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/run_phase_c_gateway_canary_private.py"
SPEC = importlib.util.spec_from_file_location("phase_c_gateway_canary", PATH)
canary = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(canary)


class PhaseCGatewayCanaryTests(unittest.TestCase):
    def config(self, root: Path, role: str, *, bad_grade=False):
        worker = root / "worker.py"
        worker.write_text(
            "import json,sys\n"
            "request=json.load(sys.stdin)\n"
            "if request['kind']=='executor':\n"
            " assert 'rubric' not in json.dumps(request); response={'artifact':{'answer':'synthetic'},'telemetry':{'cost_usd':0.01,'input_tokens':2,'output_tokens':1}}\n"
            "else:\n"
            " assert 'projection' not in request; response={'grade':{'rubric_fraction':1.0,'unsupported_claims':0,'citation_errors':0,'authority_errors':0},'telemetry':{'cost_usd':0.01,'input_tokens':2,'output_tokens':1}}\n"
            "print(json.dumps(response))\n"
        )
        worker.chmod(stat.S_IRWXU)
        config = {"schema_version": "proofpress/phase-c-gateway-config/v1", "role": role,
                  "model": "test/model", "provider": "test-provider", "reasoning_effort": "test",
                  "max_output_tokens": 12, "timeout_seconds": 5,
                  "gateway_policy": {"gateway_provider_only": "test-provider", "retries": "forbidden",
                                     "fallback": "forbidden", "routing_receipt": "one-successful-attempt-required"},
                  "command": [sys.executable, str(worker), "--bridge", str(worker), "--model", "test/model",
                              "--gateway-provider-only", "test-provider"],
                  "implementation_files": [{"path": str(worker), "digest": canary.file_digest(worker)}]}
        if role == "grader": config["blind_grades_per_artifact"] = 3
        path = root / f"{role}.json"; path.write_text(json.dumps(config))
        return path

    def test_executor_request_is_synthetic_and_sanitizes_artifact(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); path = self.config(root, "executor")
            result = canary.run(config_path=path, role="executor")
        self.assertEqual(result["status"], "pass")
        self.assertNotIn("artifact", result)
        self.assertEqual(result["telemetry"]["input_tokens"], 2)

    def test_grader_request_excludes_projection_and_sanitizes_grade(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); path = self.config(root, "grader")
            result = canary.run(config_path=path, role="grader")
        self.assertEqual(result["status"], "pass")
        self.assertNotIn("grade", result)

    def test_rejects_config_that_lacks_no_fallback_policy(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); path = self.config(root, "executor")
            value = json.loads(path.read_text()); value["gateway_policy"]["fallback"] = "allowed"; path.write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError, "forbid retries and fallback"):
                canary.run(config_path=path, role="executor")


if __name__ == "__main__":
    unittest.main()

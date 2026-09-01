import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/phase_c_gateway_adapter_private.py"
SPEC = importlib.util.spec_from_file_location("phase_c_gateway_adapter", ADAPTER_PATH)
adapter = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(adapter)
MODEL = "openai/gpt-5.6-terra"; PROVIDER = "openai"


def receipt():
    return {"generation_id": "safe-id", "original_model_id": MODEL, "canonical_slug": MODEL,
            "resolved_provider": PROVIDER, "final_provider": PROVIDER,
            "model_attempt_count": 1, "total_provider_attempt_count": 1,
            "model_attempts": [{"canonical_slug": MODEL, "success": True, "provider_attempt_count": 1,
                                "provider_attempts": [{"provider": PROVIDER, "success": True}]}]}


class PhaseCGatewayAdapterTests(unittest.TestCase):
    def request(self, kind):
        value = {"schema_version": "proofpress/frozen-phase-c-run/v1", "kind": kind,
                 "instruction": "private instruction"}
        if kind == "executor":
            value.update({"task": {"prompt": "private prompt"}, "projection": {"claims": []},
                          "executor_budget": {}, "native_output_contract": {}})
        else:
            value.update({"task": {"prompt": "private prompt", "rubric": []}, "candidate": {"answer": "x"}, "replica": 1})
        return value

    def test_executor_request_excludes_rubric_and_pins_provider(self):
        value = adapter.build_gateway_request(self.request("executor"), model=MODEL, provider=PROVIDER,
                                              max_output_tokens=10, timeout_seconds=1, reasoning_effort="high")
        self.assertEqual(value["gateway_provider_only"], PROVIDER)
        rendered = value["messages"][1]["content"]
        self.assertNotIn("rubric", rendered)
        self.assertIn("projection", rendered)

    def test_grader_request_contains_no_projection(self):
        value = adapter.build_gateway_request(self.request("grader"), model=MODEL, provider=PROVIDER,
                                              max_output_tokens=10, timeout_seconds=1, reasoning_effort="high")
        rendered = value["messages"][1]["content"]
        self.assertIn("rubric", rendered)
        self.assertNotIn("projection", rendered)

    def test_normalizes_telemetry_only_after_no_fallback_receipt(self):
        response = {"gateway_routing_receipt": receipt(), "choices": [{"message": {"content": '{"artifact":{"answer":"ok"}}'}}],
                    "usage": {"cost": 0.01, "prompt_tokens": 5, "completion_tokens": 3}}
        value = adapter.normalize_response(response, role="executor", model=MODEL, provider=PROVIDER)
        self.assertEqual(value["artifact"]["answer"], "ok")
        self.assertEqual(value["telemetry"]["cost_usd"], .01)

    def test_preserves_only_integer_token_receipts(self):
        response = {"gateway_routing_receipt": receipt(), "choices": [{"message": {"content": '{"artifact":{"answer":"ok"}}'}}],
                    "usage": {"cost": 0.01, "prompt_tokens": 5.5, "completion_tokens": 3}}
        value = adapter.normalize_response(response, role="executor", model=MODEL, provider=PROVIDER)
        self.assertIsNone(value["telemetry"]["input_tokens"])
        self.assertEqual(value["telemetry"]["output_tokens"], 3)

    def test_rejects_fallback_receipt(self):
        value = receipt(); value["total_provider_attempt_count"] = 2
        with self.assertRaisesRegex(ValueError, "retry or fallback"):
            adapter.validate_routing_receipt(value, model=MODEL, provider=PROVIDER)


if __name__ == "__main__":
    unittest.main()

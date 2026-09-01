import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "studies/apex-agent-eval/retrieval_adapter"
sys.path.insert(0, str(ADAPTER))
PATH = ADAPTER / "run_model_routing_qualification_private.py"
SPEC = importlib.util.spec_from_file_location("routing_qualification", PATH)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class FakeGateway:
    calls = [{}, {}]

    def receipt_rows(self):
        return [
            {"input_tokens": 100, "uncached_input_tokens": 60,
             "cache_read_input_tokens": 40, "cache_write_input_tokens": 5,
             "output_tokens": 30, "text_output_tokens": 20,
             "reasoning_output_tokens": 10, "cost_usd": 0.1, "latency_ms": 1200},
            {"input_tokens": 80, "uncached_input_tokens": 80,
             "cache_read_input_tokens": 0, "cache_write_input_tokens": 0,
             "output_tokens": 20, "text_output_tokens": 20,
             "reasoning_output_tokens": 0, "cost_usd": 0.2, "latency_ms": 800},
        ]


class TerminalTelemetryTests(unittest.TestCase):
    def test_preserves_detailed_token_cost_and_latency_telemetry(self):
        result = module.terminal_telemetry({"role": FakeGateway()})
        self.assertEqual(result["input_tokens"], 180)
        self.assertEqual(result["output_tokens"], 50)
        self.assertEqual(result["cache_read_input_tokens"], 40)
        self.assertEqual(result["reasoning_output_tokens"], 10)
        self.assertEqual(result["missing_token_calls"], 0)
        self.assertEqual(result["missing_detailed_token_calls"]["reasoning_output_tokens"], 0)
        self.assertAlmostEqual(result["known_cost_usd"], 0.3)
        self.assertEqual(result["by_model"]["role"]["latency_ms_mean"], 1000)


if __name__ == "__main__":
    unittest.main()

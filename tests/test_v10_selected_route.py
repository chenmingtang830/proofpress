import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/run_v10_selected_route_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("v10_selected", PATH)
selected = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(selected)


class V10SelectedRouteTests(unittest.TestCase):
    def test_selected_route_is_independent_and_canary_qualified(self):
        self.assertEqual(selected.EXTRACTOR, "deepseek")
        self.assertEqual(selected.PROPOSER, "deepseek")
        self.assertEqual(selected.CRITIC, "sol")
        self.assertNotEqual(selected.PROPOSER, selected.CRITIC)
        self.assertEqual(selected.COVERAGE_MODELS, ("qwen", "sol"))

    def test_coverage_schema_requires_explicit_resolution(self):
        item = selected.COVERAGE_OUTPUT["properties"]["resolutions"]["items"]
        self.assertEqual(set(item["properties"]["status"]["enum"]),
                         {"covered", "partial", "gap"})
        self.assertIn("supporting_claim_ids", item["required"])

    def test_coverage_normalizer_fail_closes_non_object_rows(self):
        class FakeGateway:
            def call(self, *args, **kwargs):
                return {"ok": True, "value": {"resolutions": ["bad-row"]}, "record": {"status": "ok"}}

        rows, status = selected.call_coverage(
            FakeGateway(), "task", [{"requirement_id": "R1", "requirement": "r"}], []
        )
        self.assertEqual(rows, [{"requirement_id": "R1", "status": "gap", "supporting_claim_ids": []}])
        self.assertEqual(status["status"], "ok")


if __name__ == "__main__":
    unittest.main()

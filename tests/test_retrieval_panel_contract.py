import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


panel = load("private_panel", ROOT / "studies/apex-agent-eval/retrieval_adapter/run_private_panel.py")
contract = load("legal_contract", ROOT / "studies/apex-agent-eval/retrieval_adapter/legal_pipeline_contract.py")
panel_manifest = load("panel_manifest", ROOT / "studies/apex-agent-eval/retrieval_adapter/panel_manifest.py")


class RetrievalPanelContractTests(unittest.TestCase):
    def test_rrf_is_deterministic_and_deduplicates(self):
        left = {"source": {"uri": "a", "content_digest": "sha256:" + "a" * 64},
                "evidence": {"locator": {"kind": "page_span", "page_start": 1, "page_end": 1}}}
        duplicate = {"source": dict(left["source"]), "evidence": dict(left["evidence"])}
        right = {"source": {"uri": "b", "content_digest": "sha256:" + "b" * 64},
                 "evidence": {"locator": {"kind": "page_span", "page_start": 2, "page_end": 2}}}
        result = panel.hybrid_rrf([left, duplicate], [right], 2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["source"]["uri"], "a")

    def test_decomposition_contract_forbids_rubric_and_freezes_limits(self):
        inventory = [{"uri": "private://source-1", "media_type": "application/pdf"}]
        requirements = [{"requirement_id": "req-1", "requirement": "Identify parties",
                         "applicability": "applicable", "rationale": "lifecycle checklist"}]
        result = contract.validate_decomposition("review authority", inventory, requirements)
        self.assertFalse(result["frozen"])
        frozen = contract.freeze_requirements(contract.coverage_pass(requirements, []))
        self.assertTrue(frozen["frozen"])
        with self.assertRaisesRegex(ValueError, "rubric"):
            contract.validate_decomposition("review authority", inventory, requirements, rubric={})

    def test_conformance_manifest_has_the_24_frozen_cases(self):
        manifest = panel_manifest.manifest()
        self.assertEqual(manifest["case_count"], 24)
        self.assertEqual(len(manifest["cases"]), 24)
        self.assertEqual(sum(case["pageindex_should_call"] for case in manifest["cases"]), 12)
        self.assertTrue(all(case["expected_automatic_admission"] is False for case in manifest["cases"]))


if __name__ == "__main__":
    unittest.main()

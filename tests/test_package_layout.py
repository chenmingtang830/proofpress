import importlib
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PackageLayoutTests(unittest.TestCase):
    def test_public_client_and_canonical_modules_import(self):
        from proofpress import ProofpressClient, ProofpressError
        self.assertTrue(ProofpressClient)
        self.assertTrue(ProofpressError)
        for name in (
            "proofpress.profiles.experiment",
            "proofpress.integrations.repository",
            "proofpress.integrations.matter_catalog",
            "proofpress.integrations.research_blueprint",
            "proofpress.integrations.document_extraction",
            "proofpress.transports.http",
            "proofpress.transports.mcp",
            "proofpress.hosted.service",
        ):
            self.assertTrue(importlib.import_module(name))

    def test_compatibility_imports_remain_available_for_06(self):
        for name in (
            "proofpress_sdk", "proofpress_service", "proofpress_mcp",
            "proofpress_repo", "proofpress_knowledge", "proofpress_event_store",
            "proofpress_experiment", "proofpress_evidence",
            "proofpress_rd",
            "document_extraction_contract", "document_extraction_adapters",
            "document_extraction_gate", "document_extraction_qualification",
            "proofpress_self_hosted",
        ):
            self.assertTrue(importlib.import_module(name))

    def test_product_implementation_is_not_flattened_at_repository_root(self):
        self.assertEqual({path.name for path in ROOT.glob("proofpress_*.py")}, set())
        self.assertFalse(list(ROOT.glob("document_extraction_*.py")))
        self.assertFalse((ROOT / "phase_c_ablation_contract.py").exists())


if __name__ == "__main__":
    unittest.main()

import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (ROOT / "studies/apex-agent-eval/retrieval_adapter" /
               "transfer_validation_contract.py")
SPEC = importlib.util.spec_from_file_location("transfer_validation_contract", MODULE_PATH)
contract = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(contract)
MANIFEST_PATH = (ROOT / "studies/apex-agent-eval/results" /
                 "exact-knowledge-transfer-v25-manifest.json")


class TransferValidationContractTests(unittest.TestCase):
    def manifest(self):
        return json.loads(MANIFEST_PATH.read_text())

    def test_committed_manifest_is_disjoint_and_frozen(self):
        receipt = contract.validate_transfer_manifest(self.manifest())
        self.assertEqual(receipt["status"], "frozen")
        self.assertEqual(receipt["development_task_count"], 5)
        self.assertEqual(receipt["held_out_task_count"], 7)
        self.assertTrue(receipt["manifest_digest"].startswith("sha256:"))

    def test_rejects_development_task_in_held_out_panel(self):
        manifest = self.manifest()
        manifest["held_out_task_ids"][0] = manifest["development_task_ids"][0]
        with self.assertRaisesRegex(ValueError, "panels overlap"):
            contract.validate_transfer_manifest(manifest)

    def test_rejects_condition_reordering(self):
        manifest = self.manifest()
        manifest["conditions"].reverse()
        with self.assertRaisesRegex(ValueError, "condition order changed"):
            contract.validate_transfer_manifest(manifest)

    def test_rejects_outcome_access_before_freeze(self):
        manifest = self.manifest()
        manifest["outcome_access_before_freeze"] = True
        with self.assertRaisesRegex(ValueError, "outcomes must remain inaccessible"):
            contract.validate_transfer_manifest(manifest)


if __name__ == "__main__":
    unittest.main()

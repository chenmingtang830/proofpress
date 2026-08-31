import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/freeze_v25_phase_c_inputs_private.py"
SPEC = importlib.util.spec_from_file_location("freeze_phase_c", PATH)
freeze_phase_c = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(freeze_phase_c)
MANIFEST = ROOT / "studies/apex-agent-eval/results/exact-knowledge-transfer-v25-manifest.json"


class FreezeV25PhaseCInputsTests(unittest.TestCase):
    def gateway_config(self, role):
        return {"model": "test/model", "provider": "test-provider", "role": role}

    def gateway_canary(self, role, config_path):
        return {"schema_version": "proofpress/phase-c-gateway-canary/v1", "status": "pass", "role": role,
                "config_digest": freeze_phase_c.file_digest(config_path), "model": "test/model", "provider": "test-provider",
                "telemetry": {"cost_usd": 0.01, "input_tokens": 2, "output_tokens": 1},
                "automatic_admission": False, "human_approval_required": True}

    def extraction_report(self, key, route):
        return {
            "automatic_admission": False, "human_approval_required": True,
            key: {"route": route,
                  "development_gate": {"status": "pass", "heldout_authorized": True},
                  "heldout_conformance": {"documents_scored": 4, "text_blocks_f1": .9,
                                          "table_cells_f1": 1, "numeric_values_f1": 1,
                                          "locator_rate": .9, "reading_order_rate": .8,
                                          "cross_page_continuations_f1": 1},
                  "ecological": {"documents": 4, "failed": 0},
                  "envelope_provenance": {"provider": "test", "model": "test-model", "version": "1",
                                            "license": "test-license", "model_revision": "rev",
                                            "config_digest": "sha256:" + "b" * 64,
                                            "envelope_count": 4, "envelope_set_digest": "sha256:" + "c" * 64,
                                            "status": "not_governed_candidate", "admitted": False,
                                            "human_approval_required": True}},
        }

    def test_freeze_replaces_every_control_with_a_digest(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); controls = {}
            for index, field in enumerate(freeze_phase_c.CONTROL_ARGUMENTS):
                path = root / f"control-{index}.json"
                if field == "primary_extraction_qualification":
                    value = self.extraction_report("paddleocr_vl_1_6_mlx", "PaddlePaddle/PaddleOCR-VL-1.6/mlx-vlm-server")
                elif field == "executor":
                    value = self.gateway_config("executor")
                elif field == "grader":
                    value = self.gateway_config("grader")
                elif field in {"executor_gateway_canary", "grader_gateway_canary"}:
                    role = field.removesuffix("_gateway_canary")
                    value = self.gateway_canary(role, controls[role])
                else:
                    value = {"index": index}
                path.write_text(json.dumps(value))
                controls[field] = path
            frozen, receipt = freeze_phase_c.freeze(json.loads(MANIFEST.read_text()), controls)
        self.assertEqual(receipt["status"], "frozen")
        self.assertFalse(receipt["executor_called"])
        self.assertFalse(receipt["grader_called"])
        self.assertTrue(all(value.startswith("sha256:") for value in frozen["frozen_controls"].values()))

    def test_freeze_rejects_canary_for_a_different_config(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); executor = root / "executor.json"; executor.write_text(json.dumps(self.gateway_config("executor")))
            report = self.gateway_canary("executor", executor); executor.write_text(json.dumps({**self.gateway_config("executor"), "model": "changed"}))
            with self.assertRaisesRegex(ValueError, "does not match"):
                freeze_phase_c.validate_gateway_canary(report, role="executor", config_path=executor,
                                                       config=json.loads(executor.read_text()))

    def test_freeze_rejects_missing_control(self):
        with self.assertRaisesRegex(ValueError, "every Phase C control"):
            freeze_phase_c.freeze({}, {})

if __name__ == "__main__":
    unittest.main()

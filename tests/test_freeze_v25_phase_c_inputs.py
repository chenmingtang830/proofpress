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
    def extraction_report(self, key, route):
        return {
            "automatic_admission": False, "human_approval_required": True,
            key: {"route": route,
                  "development_gate": {"status": "pass", "heldout_authorized": True},
                  "heldout_conformance": {"documents_scored": 4, "text_blocks_f1": .9,
                                          "table_cells_f1": 1, "numeric_values_f1": 1,
                                          "locator_rate": .9, "reading_order_rate": .8,
                                          "cross_page_continuations_f1": 1},
                  "ecological": {"documents": 4, "failed": 0}},
        }

    def test_freeze_replaces_every_control_with_a_digest(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); controls = {}
            for index, field in enumerate(freeze_phase_c.CONTROL_ARGUMENTS):
                path = root / f"control-{index}.json"
                if field == "primary_extraction_qualification":
                    value = self.extraction_report("paddleocr_vl_1_6_mlx", "PaddlePaddle/PaddleOCR-VL-1.6/mlx-vlm-server")
                elif field == "sensitivity_extraction_qualification":
                    value = self.extraction_report("deepseek_ocr_2_sensitivity", "deepseek-ai/DeepSeek-OCR-2")
                else:
                    value = {"index": index}
                path.write_text(json.dumps(value))
                controls[field] = path
            frozen, receipt = freeze_phase_c.freeze(json.loads(MANIFEST.read_text()), controls)
        self.assertEqual(receipt["status"], "frozen")
        self.assertFalse(receipt["executor_called"])
        self.assertFalse(receipt["grader_called"])
        self.assertTrue(all(value.startswith("sha256:") for value in frozen["frozen_controls"].values()))

    def test_freeze_rejects_missing_control(self):
        with self.assertRaisesRegex(ValueError, "every Phase C control"):
            freeze_phase_c.freeze({}, {})

    def test_freeze_rejects_unexecuted_sensitivity_route(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); controls = {}
            for index, field in enumerate(freeze_phase_c.CONTROL_ARGUMENTS):
                path = root / f"control-{index}.json"; path.write_text(json.dumps({"index": index}))
                controls[field] = path
            controls["primary_extraction_qualification"].write_text(json.dumps(
                self.extraction_report("paddleocr_vl_1_6_mlx", "PaddlePaddle/PaddleOCR-VL-1.6/mlx-vlm-server")))
            controls["sensitivity_extraction_qualification"].write_text(json.dumps({
                "automatic_admission": False, "human_approval_required": True,
                "deepseek_ocr_2_sensitivity": {"route": "deepseek-ai/DeepSeek-OCR-2",
                                                  "integration_status": "implemented-but-not-executed"},
            }))
            with self.assertRaisesRegex(ValueError, "development gate did not pass"):
                freeze_phase_c.freeze(json.loads(MANIFEST.read_text()), controls)


if __name__ == "__main__":
    unittest.main()

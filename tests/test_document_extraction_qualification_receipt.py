import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/build_document_extraction_qualification_receipt_private.py"
BUILDER_SPEC = importlib.util.spec_from_file_location("qualification_receipt", BUILDER_PATH)
builder = importlib.util.module_from_spec(BUILDER_SPEC); BUILDER_SPEC.loader.exec_module(builder)
FREEZE_PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/freeze_v25_phase_c_inputs_private.py"
FREEZE_SPEC = importlib.util.spec_from_file_location("freeze_phase_c", FREEZE_PATH)
freeze = importlib.util.module_from_spec(FREEZE_SPEC); FREEZE_SPEC.loader.exec_module(freeze)
CONTRACT_PATH = ROOT / "document_extraction_contract.py"
CONTRACT_SPEC = importlib.util.spec_from_file_location("document_extraction_contract", CONTRACT_PATH)
contract = importlib.util.module_from_spec(CONTRACT_SPEC); CONTRACT_SPEC.loader.exec_module(contract)


class QualificationReceiptTests(unittest.TestCase):
    def envelope(self):
        return contract.build_envelope(
            source={"uri": "private://source", "content_digest": "sha256:" + "a" * 64},
            extractor={"provider": "PaddlePaddle", "model": "PaddleOCR-VL", "version": "1.6",
                       "license": "Apache-2.0", "config_digest": "sha256:" + "b" * 64},
            pages=[{"page": 1, "render_digest": "sha256:" + "c" * 64}],
            blocks=[{"id": "block", "text": "private", "locator": {"page": 1}}])

    def test_compiles_private_envelopes_to_source_safe_passed_receipt(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); nested = root / "source" / "isolated"; nested.mkdir(parents=True)
            (nested / "extraction-envelope.json").write_text(json.dumps(self.envelope()))
            receipt = builder.build(
                key="paddleocr_vl_1_6_mlx", route="PaddlePaddle/PaddleOCR-VL-1.6/mlx-vlm-server",
                model_revision="revision", envelope_root=root,
                development_gate={"status": "pass", "heldout_authorized": True},
                heldout={"split": "heldout", "documents_scored": 1, "documents_expected": 1,
                         "metrics": {"text_blocks": {"f1": .9}, "table_cells": {"f1": 1},
                                     "numeric_values": {"f1": 1}, "locators": {"rate": .9},
                                     "reading_order": {"rate": .8}, "cross_page_continuations": {"f1": 1}}},
                ecological={"documents": 1, "attempted": 1, "pending": 0, "complete": 1, "failed": 0,
                            "automatic_admission": False, "human_approval_required": True})
        self.assertFalse(receipt["automatic_admission"])
        self.assertNotIn("private", json.dumps(receipt))
        freeze.validate_extraction_qualification(receipt, route="PaddlePaddle/PaddleOCR-VL-1.6/mlx-vlm-server",
                                                  key="paddleocr_vl_1_6_mlx")

    def test_rejects_mixed_extractor_configuration(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for index, digest in enumerate(("b", "d")):
                target = root / str(index); target.mkdir()
                envelope = self.envelope(); envelope["extractor"]["config_digest"] = "sha256:" + digest * 64
                envelope["extraction_digest"] = contract.digest({key: value for key, value in envelope.items()
                                                                  if key != "extraction_digest"})
                (target / "extraction-envelope.json").write_text(json.dumps(envelope))
            with self.assertRaisesRegex(ValueError, "different extractor configurations"):
                builder.collect_envelopes(root, model_revision="revision")


if __name__ == "__main__":
    unittest.main()

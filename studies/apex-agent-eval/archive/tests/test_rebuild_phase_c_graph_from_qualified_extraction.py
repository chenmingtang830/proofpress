import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/rebuild_phase_c_graph_from_qualified_extraction_private.py"
SPEC = importlib.util.spec_from_file_location("rebuild_phase_c_graph", PATH)
rebuild = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(rebuild)
ENVELOPE_PATH = ROOT / "document_extraction_contract.py"
ENVELOPE_SPEC = importlib.util.spec_from_file_location("document_extraction_contract", ENVELOPE_PATH)
envelopes = importlib.util.module_from_spec(ENVELOPE_SPEC); ENVELOPE_SPEC.loader.exec_module(envelopes)
MANIFEST = json.loads((ROOT / "studies/apex-agent-eval/results/exact-knowledge-transfer-v25-manifest.json").read_text())
DIGEST = "sha256:" + "a" * 64


class QualifiedExtractionGraphRebuildTests(unittest.TestCase):
    def qualification(self, envelope_set_digest, config_digest):
        return {"qualification_digest": "sha256:" + "q".replace("q", "c") * 64,
                "automatic_admission": False, "human_approval_required": True,
                "paddleocr_vl_1_6_mlx": {"route": "PaddlePaddle/PaddleOCR-VL-1.6/mlx-vlm-server",
                    "development_gate": {"status": "pass", "heldout_authorized": True},
                    "heldout_conformance": {"documents_scored": 1, "text_blocks_f1": .9, "table_cells_f1": 1,
                        "numeric_values_f1": 1, "locator_rate": .9, "reading_order_rate": .8,
                        "cross_page_continuations_f1": 1}, "ecological": {"documents": 1, "failed": 0},
                    "envelope_provenance": {"provider": "PaddlePaddle", "model": "PaddleOCR-VL", "version": "1.6",
                        "license": "Apache-2.0", "model_revision": "revision", "config_digest": config_digest,
                        "envelope_count": 1, "envelope_set_digest": envelope_set_digest,
                        "status": "not_governed_candidate", "admitted": False, "human_approval_required": True},
                    "conflict_status": "not_compared"}}

    def fixture(self, root: Path):
        config_digest = envelopes.digest({"config": "paddle"})
        envelope = envelopes.build_envelope(source={"uri": "private://source", "content_digest": DIGEST},
            extractor={"provider": "PaddlePaddle", "model": "PaddleOCR-VL", "version": "1.6",
                       "license": "Apache-2.0", "config_digest": config_digest},
            pages=[{"page": 1, "render_digest": DIGEST}], blocks=[],
            tables=[{"id": "table-1", "locator": {"page": 1}, "cells": [
                {"row": 0, "column": 0, "raw_text": "12", "locator": {"page": 1}}]}])
        envelope_root = root / "envelopes"; envelope_path = envelope_root / "one" / "extraction-envelope.json"
        envelope_path.parent.mkdir(parents=True); envelope_path.write_text(json.dumps(envelope))
        qualification = self.qualification(rebuild.digest([envelope["extraction_digest"]]), config_digest)
        qualification_path = root / "qualification.json"; qualification_path.write_text(json.dumps(qualification))
        base_graph = {"graph_digest": DIGEST, "source_manifest_digest": DIGEST,
                      "automatic_admission": False, "human_approval_required": True,
                      "claims": [{"claim_id": "claim-1", "text": "ordinary claim"}],
                      "authority_nodes": [{"authority_id": "authority-1", "source_content_digest": DIGEST}],
                      "table_cells": [{"cell_id": "old-cell", "source_content_digest": DIGEST,
                                       "locator": {"page": 1}, "row": 0, "column": 0}], "derivations": []}
        base_path = root / "base-graph.json"; base_path.write_text(json.dumps(base_graph))
        frozen = json.loads(json.dumps(MANIFEST))
        frozen["frozen_controls"] = {key: DIGEST for key in frozen["frozen_controls"]}
        frozen["frozen_controls"]["graph_digest"] = rebuild.file_digest(base_path)
        frozen["execution_status"] = "frozen-pre-run-no-executor-called"
        result = {"status": "complete", "automatic_admission": False, "human_approval_required": True,
                  "frozen_manifest_digest": rebuild.transfer.digest(frozen), "conditions": list(rebuild.projection.CONDITIONS),
                  "planned_cells": 36, "scored_cells": 36, "inconclusive_cells": 0}
        derivatives = {"schema_version": rebuild.DERIVATION_SCHEMA, "automatic_admission": False,
                       "human_approval_required": True, "derivations": [{"derivation_id": "derived-1", "formula": "input_1",
                         "input_cells": [{"source_content_digest": DIGEST, "table_id": "table-1", "row": 0, "column": 0}]}]}
        return base_graph, base_path, frozen, result, qualification, envelope_root, derivatives

    def test_rebuilds_new_cells_only_after_complete_first_panel(self):
        with tempfile.TemporaryDirectory() as temp:
            fixture = self.fixture(Path(temp))
            graph, receipt = rebuild.rebuild(base_graph=fixture[0], base_graph_path=fixture[1],
                first_frozen_manifest=fixture[2], first_result=fixture[3], qualification=fixture[4],
                envelope_root=fixture[5], derivation_manifest=fixture[6])
        self.assertEqual(receipt["status"], "rebuilt-private-graph")
        self.assertEqual(len(graph["table_cells"]), 1)
        self.assertNotEqual(graph["table_cells"][0]["cell_id"], "old-cell")
        self.assertEqual(graph["derivations"][0]["input_cell_ids"], [graph["table_cells"][0]["cell_id"]])
        self.assertFalse(graph["automatic_admission"])

    def test_rejects_rebuild_before_complete_first_panel(self):
        with tempfile.TemporaryDirectory() as temp:
            fixture = self.fixture(Path(temp)); result = {**fixture[3], "status": "inconclusive", "scored_cells": 0}
            with self.assertRaisesRegex(ValueError, "complete first Phase C result"):
                rebuild.rebuild(base_graph=fixture[0], base_graph_path=fixture[1], first_frozen_manifest=fixture[2],
                    first_result=result, qualification=fixture[4], envelope_root=fixture[5], derivation_manifest=fixture[6])

    def test_rejects_first_result_with_inconclusive_cells(self):
        with tempfile.TemporaryDirectory() as temp:
            fixture = self.fixture(Path(temp)); result = {**fixture[3], "inconclusive_cells": 1, "scored_cells": 35}
            with self.assertRaisesRegex(ValueError, "complete task-by-condition panel"):
                rebuild.rebuild(base_graph=fixture[0], base_graph_path=fixture[1], first_frozen_manifest=fixture[2],
                    first_result=result, qualification=fixture[4], envelope_root=fixture[5], derivation_manifest=fixture[6])

    def test_rejects_envelope_set_outside_passed_qualification(self):
        with tempfile.TemporaryDirectory() as temp:
            fixture = self.fixture(Path(temp)); qualification = json.loads(json.dumps(fixture[4]))
            qualification["paddleocr_vl_1_6_mlx"]["envelope_provenance"]["envelope_set_digest"] = DIGEST
            with self.assertRaisesRegex(ValueError, "does not exactly match"):
                rebuild.rebuild(base_graph=fixture[0], base_graph_path=fixture[1], first_frozen_manifest=fixture[2],
                    first_result=fixture[3], qualification=qualification, envelope_root=fixture[5], derivation_manifest=fixture[6])


if __name__ == "__main__":
    unittest.main()

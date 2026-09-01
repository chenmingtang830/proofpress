import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/run_phase_c_v25_private.py"
SPEC = importlib.util.spec_from_file_location("run_phase_c_v25", PATH)
phase_c = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(phase_c)
MANIFEST = ROOT / "studies/apex-agent-eval/results/exact-knowledge-transfer-v25-manifest.json"
DIGEST = "sha256:" + "a" * 64


class PhaseCV25OrchestrationTests(unittest.TestCase):
    def inputs(self, root: Path):
        manifest = json.loads(MANIFEST.read_text())
        task_root = root / "tasks"; task_root.mkdir()
        for index, task_id in enumerate(manifest["held_out_task_ids"]):
            (task_root / f"{index}.json").write_text(json.dumps({"task_id": task_id, "prompt": f"prompt-{index}",
                "expected_output": "message_in_console", "rubric": [{"id": "r"}], "gold_response": "never copied"}))
        graph = {"graph_digest": DIGEST, "source_manifest_digest": DIGEST, "automatic_admission": False,
                 "human_approval_required": True, "claims": [{"claim_id": "claim", "text": "claim"}],
                 "authority_nodes": [], "table_cells": [], "derivations": []}
        graph_path = root / "graph.json"; graph_path.write_text(json.dumps(graph))
        bridge = root / "bridge.mjs"; bridge.write_text("// private bridge placeholder")
        qualification = {"automatic_admission": False, "human_approval_required": True,
            "paddleocr_vl_1_6_mlx": {"route": "PaddlePaddle/PaddleOCR-VL-1.6/mlx-vlm-server",
             "development_gate": {"status": "pass", "heldout_authorized": True},
             "heldout_conformance": {"documents_scored": 1, "text_blocks_f1": .9, "table_cells_f1": 1,
              "numeric_values_f1": 1, "locator_rate": .9, "reading_order_rate": .8, "cross_page_continuations_f1": 1},
             "ecological": {"documents": 1, "failed": 0}, "envelope_provenance": {"provider": "PaddlePaddle",
              "model": "PaddleOCR-VL", "version": "1.6", "license": "Apache-2.0", "model_revision": "test",
              "config_digest": DIGEST, "envelope_count": 1, "envelope_set_digest": DIGEST,
              "status": "not_governed_candidate", "admitted": False, "human_approval_required": True}}}
        qualification_path = root / "qualification.json"; qualification_path.write_text(json.dumps(qualification))
        extras = {}
        for name, value in (("retry", {"fallback": "forbidden", "terminal_receipt_required": True}),
                            ("disclosure", {"max_projection_bytes": 1000}), ("executor_budget", {"max": 1}),
                            ("native_output", {"version": 1})):
            path = root / f"{name}.json"; path.write_text(json.dumps(value)); extras[name] = path
        return {"manifest_path": MANIFEST, "task_root": task_root, "graph": graph_path, "bridge": bridge,
                "primary_extraction_qualification": qualification_path, "retry_policy": extras["retry"],
                "disclosure_budget": extras["disclosure"], "executor_budget": extras["executor_budget"],
                "native_output_contract": extras["native_output"], "out": root / "out",
                "settings": {"executor_model": "openai/gpt-5.6-terra", "executor_provider": "openai",
                 "executor_reasoning_effort": "high", "executor_max_output_tokens": 10, "executor_timeout_seconds": 1,
                 "grader_model": "openai/gpt-5.6-terra", "grader_provider": "openai",
                 "grader_reasoning_effort": "high", "grader_max_output_tokens": 10, "grader_timeout_seconds": 1}}

    def test_prepare_compiles_blind_controls_without_a_model_call(self):
        with tempfile.TemporaryDirectory() as temp:
            controls, receipt = phase_c.prepare(**self.inputs(Path(temp)))
            source = json.loads(controls["task_source_manifest_digest"].read_text())
            rubrics = json.loads(controls["rubric_digest"].read_text())
            self.assertTrue(controls["executor"].is_file())
        self.assertEqual(receipt["status"], "prepared-no-model-call")
        self.assertTrue(all("rubric" not in task and "gold_response" not in task for task in source["tasks"]))
        self.assertTrue(all("prompt" not in row for row in rubrics["rubrics"]))

    def test_prepare_refuses_to_mix_a_new_run_into_existing_output(self):
        with tempfile.TemporaryDirectory() as temp:
            values = self.inputs(Path(temp)); values["out"].mkdir(); (values["out"] / "prior.json").write_text("{}")
            with self.assertRaisesRegex(ValueError, "must be empty"):
                phase_c.prepare(**values)


if __name__ == "__main__":
    unittest.main()

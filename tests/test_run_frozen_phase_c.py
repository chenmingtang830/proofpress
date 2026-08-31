import importlib.util
import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FREEZE_PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/freeze_v25_phase_c_inputs_private.py"
FREEZE_SPEC = importlib.util.spec_from_file_location("freeze_v25", FREEZE_PATH)
freeze = importlib.util.module_from_spec(FREEZE_SPEC); FREEZE_SPEC.loader.exec_module(freeze)
RUNNER_PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/run_frozen_phase_c_private.py"
RUNNER_SPEC = importlib.util.spec_from_file_location("run_frozen_phase_c", RUNNER_PATH)
runner = importlib.util.module_from_spec(RUNNER_SPEC); RUNNER_SPEC.loader.exec_module(runner)
MANIFEST = ROOT / "studies/apex-agent-eval/results/exact-knowledge-transfer-v25-manifest.json"
DIGEST = "sha256:" + "a" * 64


class FrozenPhaseCRunnerTests(unittest.TestCase):
    def extraction(self, key, route):
        return {"automatic_admission": False, "human_approval_required": True,
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
                                                "human_approval_required": True}}}

    def controls(self, root):
        control = {}
        graph = {"graph_digest": DIGEST, "source_manifest_digest": DIGEST,
                 "automatic_admission": False, "human_approval_required": True,
                 "claims": [{"claim_id": "c1", "text": "claim"}],
                 "authority_nodes": [{"authority_id": "a1", "source_content_digest": DIGEST}],
                 "table_cells": [{"cell_id": "cell1", "source_content_digest": DIGEST,
                                  "locator": {"page": 1}, "row": 0, "column": 0}],
                 "derivations": [{"derivation_id": "d1", "input_cell_ids": ["cell1"],
                                  "derivation_digest": DIGEST}]}
        task_ids = (json.loads(MANIFEST.read_text())["development_task_ids"] +
                    json.loads(MANIFEST.read_text())["held_out_task_ids"])
        tasks = [{"task_id": task_id, "prompt": f"prompt {index}"}
                 for index, task_id in enumerate(json.loads(MANIFEST.read_text())["development_task_ids"] +
                                                  json.loads(MANIFEST.read_text())["held_out_task_ids"])]
        rubrics = [{"task_id": task_id, "rubric": [{"id": "r1"}]} for task_id in task_ids]
        source = root / "runner.py"
        source.write_text("import json,sys\nr=json.load(sys.stdin)\nif r['kind']=='grader': assert 'projection' not in r\nt={'cost_usd':0.01,'input_tokens':10,'output_tokens':5}\nprint(json.dumps({'grade':{'rubric_fraction':1.0,'unsupported_claims':0,'citation_errors':0,'authority_errors':0},'telemetry':t} if r['kind']=='grader' else {'artifact':{'answer':'ok'},'telemetry':t}))\n")
        source.chmod(stat.S_IRWXU)
        config = {"schema_version": "proofpress/phase-c-gateway-config/v1", "role": "executor",
                  "command": [sys.executable, str(source), "--model", "test/model",
                              "--gateway-provider-only", "test-provider"], "timeout_seconds": 5,
                  "model": "test/model", "provider": "test-provider", "reasoning_effort": "test",
                  "max_output_tokens": 32,
                  "gateway_policy": {"gateway_provider_only": "test-provider", "retries": "forbidden",
                                     "fallback": "forbidden", "routing_receipt": "one-successful-attempt-required"},
                  "implementation_files": [{"path": str(source), "digest": runner.file_digest(source)}]}
        grader_config = {**config, "role": "grader", "blind_grades_per_artifact": 3}
        values = {"task_source_manifest_digest": {"tasks": tasks}, "graph_digest": graph,
                  "executor": config, "grader": grader_config,
                  "rubric_digest": {"rubrics": rubrics},
                  "retry_policy": {"fallback": "forbidden", "terminal_receipt_required": True},
                  "disclosure_budget": {"max_projection_bytes": 10000}, "executor_budget": {"max": 1},
                  "native_output_contract": {"version": 1},
                  "primary_extraction_qualification": self.extraction("paddleocr_vl_1_6_mlx", "PaddlePaddle/PaddleOCR-VL-1.6/mlx-vlm-server")}
        for field, value in values.items():
            path = root / f"{field}.json"; path.write_text(json.dumps(value)); control[field] = path
        for role in ("executor", "grader"):
            config_path = control[role]
            canary = {"schema_version": "proofpress/phase-c-gateway-canary/v1", "status": "pass", "role": role,
                      "config_digest": runner.file_digest(config_path), "model": "test/model", "provider": "test-provider",
                      "telemetry": {"cost_usd": .01, "input_tokens": 2, "output_tokens": 1},
                      "automatic_admission": False, "human_approval_required": True}
            path = root / f"{role}_gateway_canary.json"; path.write_text(json.dumps(canary)); control[f"{role}_gateway_canary"] = path
        return control

    def frozen(self, root):
        controls = self.controls(root)
        manifest, receipt = freeze.freeze(json.loads(MANIFEST.read_text()), controls)
        manifest_path = root / "manifest.json"; manifest_path.write_text(json.dumps(manifest))
        receipt_path = root / "receipt.json"; receipt_path.write_text(json.dumps(receipt))
        return controls, manifest_path, receipt_path

    def test_preflight_validates_all_gates_without_calling_models(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); controls, manifest, receipt = self.frozen(root)
            prepared = runner.validate_preflight(frozen_manifest_path=manifest,
                                                  freeze_receipt_path=receipt, control_paths=controls)
        self.assertEqual(len(prepared["tasks"]), 12)

    def test_run_uses_only_deterministic_projection_deltas(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); controls, manifest, receipt = self.frozen(root)
            result = runner.run(runner.validate_preflight(frozen_manifest_path=manifest,
                                                           freeze_receipt_path=receipt, control_paths=controls),
                                out=root / "out")
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["planned_cells"], 36)
        self.assertTrue(all(row["status"] == "scored" for row in result["cells"]))
        self.assertEqual(result["aggregate"]["ordinary-claim"]["known_cost_usd"], .48)

    def test_preflight_rejects_mutated_command_implementation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); controls, manifest, receipt = self.frozen(root)
            source = next(root.glob("runner.py")); source.write_text("changed")
            with self.assertRaisesRegex(ValueError, "implementation file digest mismatch"):
                runner.validate_preflight(frozen_manifest_path=manifest,
                                         freeze_receipt_path=receipt, control_paths=controls)

    def test_preflight_rejects_unpinned_gateway_policy(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); controls, manifest, receipt = self.frozen(root)
            config_path = controls["executor"]
            config = json.loads(config_path.read_text())
            config["gateway_policy"]["fallback"] = "allowed"
            config_path.write_text(json.dumps(config))
            executor_canary_path = controls["executor_gateway_canary"]
            executor_canary = json.loads(executor_canary_path.read_text())
            executor_canary["config_digest"] = runner.file_digest(config_path)
            executor_canary_path.write_text(json.dumps(executor_canary))
            # Re-freeze the mutated config so this tests the semantic preflight,
            # not merely its content-addressed digest mismatch.
            frozen, refreshed = freeze.freeze(json.loads(MANIFEST.read_text()), controls)
            manifest.write_text(json.dumps(frozen)); receipt.write_text(json.dumps(refreshed))
            with self.assertRaisesRegex(ValueError, "forbid retries and fallback"):
                runner.validate_preflight(frozen_manifest_path=manifest,
                                         freeze_receipt_path=receipt, control_paths=controls)


if __name__ == "__main__":
    unittest.main()

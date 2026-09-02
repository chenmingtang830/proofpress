import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "studies/apex-agent-eval/retrieval_adapter"
sys.path[:0] = [str(ROOT), str(ADAPTER)]
SPEC = importlib.util.spec_from_file_location(
    "native_diagnostic", ADAPTER / "run_native_apex_development_diagnostic_private.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def sha(char):
    return "sha256:" + char * 64


def graph(task_id):
    atom = {"atom_id": "atom", "source_content_digest": sha("c"), "display": "10",
            "normalized_value": "10", "kind": "amount", "unit": "USD", "entity": "x",
            "period": "current", "status": "not_governed_candidate", "admitted": False}
    cell = {"cell_id": "cell", "source_content_digest": sha("d"),
            "locator": {"page": 1}, "row": 1, "column": 1}
    derivation = {"derivation_id": "derive", "input_refs": [
        {"object_kind": "numeric_atom", "object_id": "atom"}], "derivation_digest": sha("e")}
    return {"task_id": task_id, "graph_digest": sha("a"), "source_manifest_digest": sha("b"),
            "claims": [{"claim_id": "claim"}], "numeric_atoms": [atom], "table_cells": [cell],
            "derivations": [derivation], "authority_nodes": [], "task_parameters": [],
            "automatic_admission": False, "human_approval_required": True}


class DiagnosticTests(unittest.TestCase):
    def fixture(self, root):
        tasks, graphs, world = root / "tasks", root / "graphs", root / "world"
        tasks.mkdir(); graphs.mkdir(); world.mkdir()
        (world / "source").write_text("private")
        (root / "initial.zip").write_bytes(b"private")
        ids = ["task_a", "task_b", "task_c"]
        (root / "ids.json").write_text(json.dumps(ids))
        (root / "overlays.json").write_text(json.dumps({"overlays": [
            {"task_id": task_id, "overlay_root": None} for task_id in ids]}))
        for task_id in ids:
            task = {"task": {"task_id": task_id, "prompt": "private", "expected_output": "reply",
                             "world_id": "world", "rubric": [{"criteria": "private"}]}}
            (tasks / f"{task_id}.json").write_text(json.dumps(task))
            (graphs / f"{task_id}.json").write_text(json.dumps(graph(task_id)))
        return ids, tasks, graphs, world

    def prepare(self, root):
        _, tasks, graphs, world = self.fixture(root)
        return module.prepare(ids_path=root / "ids.json", task_root=tasks, graph_root=graphs,
                              overlays_path=root / "overlays.json", world_root=world,
                              initial_snapshot=root / "initial.zip",
                              executor=("deepseek", "provider", "high"),
                              grader=("gemini", "provider", "high"), max_known_cost_usd=20)

    def test_preflight_freezes_exactly_three_tasks_two_conditions(self):
        with tempfile.TemporaryDirectory() as tmp:
            frozen = self.prepare(Path(tmp))
        self.assertEqual(frozen["study_kind"], "development-diagnostic-not-heldout")
        self.assertEqual(frozen["conditions"], list(module.CONDITIONS))
        self.assertEqual(frozen["planned_cells"], 6)
        self.assertEqual(frozen["cell_timeout_seconds"], 1800)
        self.assertEqual(frozen["typed_object_counts"],
                         {"numeric_atoms": 3, "table_cells": 3, "derivations": 3})

    def test_preflight_rejects_missing_typed_treatment(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); _, tasks, graphs, world = self.fixture(root)
            value = graph("task_c"); value["derivations"] = []
            for task_id in ("task_a", "task_b"):
                other = graph(task_id); other["derivations"] = []
                (graphs / f"{task_id}.json").write_text(json.dumps(other))
            (graphs / "task_c.json").write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError, "aggregate nonzero"):
                module.prepare(ids_path=root / "ids.json", task_root=tasks, graph_root=graphs,
                               overlays_path=root / "overlays.json", world_root=world,
                               initial_snapshot=root / "initial.zip", executor=("m", "p", "r"),
                               grader=("g", "p", "r"), max_known_cost_usd=20)

    def test_summary_includes_task_criterion_and_full_telemetry(self):
        with tempfile.TemporaryDirectory() as tmp:
            frozen = self.prepare(Path(tmp))
        telemetry = {"calls": 2, "known_cost_usd": .5, "input_tokens": 10, "output_tokens": 4}
        cells = []
        for task_id in frozen["task_ids"]:
            for condition in module.CONDITIONS:
                cells.append({"task_id": task_id, "condition": condition, "status": "complete",
                              "official_final_score": .5, "criterion_scores": [
                                  {"criterion_index": 0, "score": 1.0, "status": "completed"}],
                              "executor": {"telemetry": telemetry}, "grader": {"telemetry": telemetry}})
        result = module.summarize(frozen, cells)
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["known_cost_usd"], 6.0)
        self.assertEqual(result["conditions"][0]["mean_task_score"], .5)
        self.assertEqual(result["conditions"][0]["mean_criterion_score"], 1.0)
        self.assertEqual(result["conditions"][0]["executor"]["calls"], 6)

    def test_six_inconclusive_attempts_are_not_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            frozen = self.prepare(Path(tmp))
        cells = [{"task_id": task_id, "condition": condition,
                  "status": "inconclusive", "criterion_scores": []}
                 for task_id in frozen["task_ids"] for condition in module.CONDITIONS]
        result = module.summarize(frozen, cells)
        self.assertEqual(result["status"], "inconclusive")
        self.assertEqual(result["complete_cells"], 0)

    def test_criterion_receipt_excludes_private_rubric_and_rationale(self):
        with tempfile.TemporaryDirectory() as tmp:
            cell = Path(tmp)
            (cell / "grades_private.json").write_text(json.dumps({"verifier_results": [{
                "score": .75, "status": "completed",
                "verifier_result_values": {"grade_rationale": "private", "criteria": "private"},
            }]}))
            rows = module._criterion_scores(cell)
        self.assertEqual(rows, [{"criterion_index": 0, "score": .75, "status": "completed"}])
        self.assertNotIn("private", json.dumps(rows))

    def test_execute_checkpoints_and_stops_at_known_cost_ceiling_without_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); frozen = self.prepare(root)
            frozen["max_total_known_cost_usd"] = 1.0
            calls = []
            original_run, original_httpx = module.native.run, module.native.httpx
            module.native.httpx = object()
            def fake_run(**kwargs):
                calls.append((kwargs["task"]["task_id"], kwargs["condition"]))
                return {"task_id": kwargs["task"]["task_id"], "condition": kwargs["condition"],
                        "status": "complete", "official_final_score": 1.0,
                        "executor": {"telemetry": {"calls": 1, "known_cost_usd": .6,
                                                    "input_tokens": 1, "output_tokens": 1}},
                        "grader": {"telemetry": {"calls": 1, "known_cost_usd": .4,
                                                  "input_tokens": 1, "output_tokens": 1}}}
            module.native.run = fake_run
            try:
                result = module.execute(frozen=frozen, harness=root, task_root=root / "tasks",
                                        graph_root=root / "graphs", overlays_path=root / "overlays.json",
                                        world_root=root / "world", initial_snapshot=root / "initial.zip",
                                        bridge=root / "bridge", out=root / "out")
            finally:
                module.native.run, module.native.httpx = original_run, original_httpx
            self.assertEqual(len(calls), 1)
            self.assertEqual(result["status"], "cost-ceiling-reached")
            self.assertTrue((root / "out/progress-sanitized.json").is_file())
            self.assertTrue((root / "out/result-sanitized.json").is_file())


if __name__ == "__main__":
    unittest.main()

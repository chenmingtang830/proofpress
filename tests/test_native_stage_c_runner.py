import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "studies/apex-agent-eval/retrieval_adapter"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ADAPTER))
SPEC = importlib.util.spec_from_file_location(
    "native_stage_c", ADAPTER / "run_native_stage_c_v25_private.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def cell(task_id, condition, score):
    telemetry = {"calls": 1, "known_cost_usd": .25, "input_tokens": 10, "output_tokens": 4}
    return {"task_id": task_id, "condition": condition, "status": "complete",
            "agent_status": "completed", "official_grading_status": "completed",
            "official_final_score": score, "graph_digest": "sha256:" + "a" * 64,
            "executor": {"telemetry": telemetry}, "grader": {"telemetry": telemetry}}


class NativeStageCRunnerTests(unittest.TestCase):
    def test_summary_preserves_each_frozen_condition_and_full_costs(self):
        frozen = {"frozen_controls_digest": "sha256:" + "b" * 64,
                  "task_ids": ["task_a", "task_b"], "conditions": list(module.CONDITIONS)}
        cells = [cell(task_id, condition, score)
                 for condition, score in zip(module.CONDITIONS, (.0, .5, 1.0), strict=True)
                 for task_id in frozen["task_ids"]]
        result = module.summarize(frozen=frozen, cells=cells)
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["planned_cells"], 6)
        self.assertEqual([row["mean_official_final_score"] for row in result["conditions"]], [.0, .5, 1.0])
        self.assertEqual(result["conditions"][2]["executor"]["calls"], 2)
        self.assertEqual(result["conditions"][2]["grader"]["known_cost_usd"], .5)

    def test_runner_does_not_embed_a_retry_loop(self):
        source = Path(module.__file__).read_text()
        self.assertIn("one native attempt per frozen task-condition cell", source)
        self.assertNotIn("for retry", source)
        self.assertIn("Archipelago harness virtual environment", source)

    def test_one_condition_freeze_is_labeled_descriptive(self):
        original = module.controls.expected_heldout_ids
        module.controls.expected_heldout_ids = lambda _: ("task_a",)
        try:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); task_root = root / "tasks"; graph_root = root / "graphs"
                task_root.mkdir(); graph_root.mkdir(); world = root / "world"; world.mkdir()
                (world / "source.txt").write_text("private")
                (root / "initial.zip").write_bytes(b"private")
                task = {"task": {"task_id": "task_a", "prompt": "private",
                                 "expected_output": "respond", "world_id": "world",
                                 "rubric": [{"criteria": "private"}]}}
                graph = {"task_id": "task_a", "graph_digest": "sha256:" + "a" * 64,
                         "source_manifest_digest": "sha256:" + "b" * 64,
                         "claims": [{"claim_id": "claim_a"}], "table_cells": [],
                         "derivations": [], "authority_nodes": [],
                         "automatic_admission": False, "human_approval_required": True}
                (task_root / "task_a.json").write_text(json.dumps(task))
                (graph_root / "task_a.json").write_text(json.dumps(graph))
                overlays = root / "overlays.json"
                overlays.write_text(json.dumps({"overlays": [{"task_id": "task_a", "overlay_root": None}]}))
                frozen, _ = module.prepare(frozen_manifest={}, task_root=task_root, overlays_path=overlays,
                                           graph_root=graph_root, world_root=world,
                                           initial_snapshot=root / "initial.zip",
                                           executor=("model", "provider", "high"),
                                           grader=("judge", "provider", "low"),
                                           conditions=("ordinary-claim",))
        finally:
            module.controls.expected_heldout_ids = original
        self.assertEqual(frozen["study_kind"], "descriptive-heldout-projection-panel")
        self.assertEqual(frozen["conditions"], ["ordinary-claim"])
        result = module.summarize(frozen=frozen, cells=[cell("task_a", "ordinary-claim", 1.0)])
        self.assertEqual(result["planned_cells"], 1)
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["study_kind"], "descriptive-heldout-projection-panel")

    def test_preflight_rejects_zero_treatment_variation(self):
        original = module.controls.expected_heldout_ids
        module.controls.expected_heldout_ids = lambda _: ("task_a",)
        try:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); task_root = root / "tasks"; graph_root = root / "graphs"
                task_root.mkdir(); graph_root.mkdir(); world = root / "world"; world.mkdir()
                (world / "source.txt").write_text("private")
                (root / "initial.zip").write_bytes(b"private")
                task = {"task": {"task_id": "task_a", "prompt": "private", "expected_output": "respond",
                                 "world_id": "world", "rubric": [{"criteria": "private"}]}}
                graph = {"task_id": "task_a", "graph_digest": "sha256:" + "a" * 64,
                         "source_manifest_digest": "sha256:" + "b" * 64,
                         "claims": [{"claim_id": "claim_a"}], "table_cells": [],
                         "derivations": [], "authority_nodes": [], "task_parameters": [],
                         "automatic_admission": False, "human_approval_required": True}
                (task_root / "task_a.json").write_text(json.dumps(task))
                (graph_root / "task_a.json").write_text(json.dumps(graph))
                overlays = root / "overlays.json"
                overlays.write_text(json.dumps({"overlays": [{"task_id": "task_a", "overlay_root": None}]}))
                with self.assertRaisesRegex(ValueError, "no payload/treatment variation|nonzero table cells"):
                    module.prepare(frozen_manifest={}, task_root=task_root, overlays_path=overlays,
                                   graph_root=graph_root, world_root=world,
                                   initial_snapshot=root / "initial.zip",
                                   executor=("model", "provider", "high"),
                                   grader=("judge", "provider", "low"),
                                   conditions=("ordinary-claim", "claim-plus-table-cells"))
        finally:
            module.controls.expected_heldout_ids = original

    def test_numeric_only_graph_has_real_exact_treatment_variation(self):
        graph = {"graph_digest": "sha256:" + "a" * 64, "source_manifest_digest": "sha256:" + "b" * 64,
                 "claims": [{"claim_id": "claim_a", "basis_object_id": "atom_a",
                             "basis_object_kind": "numeric_atom"}],
                 "numeric_atoms": [{"atom_id": "atom_a", "display": "42", "normalized_value": "42",
                                    "kind": "count", "unit": "people", "entity": "Company", "period": "current",
                                    "source_content_digest": "sha256:" + "c" * 64,
                                    "status": "not_governed_candidate", "admitted": False}],
                 "table_cells": [], "derivations": [], "authority_nodes": [], "task_parameters": [],
                 "automatic_admission": False, "human_approval_required": True}
        ordinary = module.project(graph, "ordinary-claim")
        exact_projection = module.project(graph, "claim-plus-table-cells")
        self.assertNotEqual(ordinary["projection_digest"], exact_projection["projection_digest"])
        self.assertNotIn("numeric_atoms", ordinary)
        self.assertEqual(len(exact_projection["numeric_atoms"]), 1)


if __name__ == "__main__":
    unittest.main()

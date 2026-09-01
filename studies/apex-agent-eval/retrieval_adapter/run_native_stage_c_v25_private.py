#!/usr/bin/env python3
"""Run the frozen v25 7-task × 3-projection panel through native APEX.

This runner has one job: bind the already-constructed, source-bound candidate
graphs to the preregistered task panel and execute each cell through the
official Archipelago lifecycle.  It never selects tasks after seeing an
outcome, retries a failed cell, substitutes a console result, or admits a
candidate into governed knowledge.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
ADAPTER = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ADAPTER) not in sys.path:
    sys.path.insert(0, str(ADAPTER))

from phase_c_ablation_contract import CONDITIONS, project, validate_graph
import run_native_apex_projection_private as native

CONTROLS_PATH = ADAPTER / "build_phase_c_task_controls_private.py"
SPEC = importlib.util.spec_from_file_location("phase_c_task_controls", CONTROLS_PATH)
controls = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(controls)

SCHEMA = "proofpress/native-stage-c-v25/v1"


def digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return "sha256:" + value.hexdigest()


def tree_digest(root: Path) -> str:
    if not root.is_dir():
        raise ValueError("native source root must be a directory")
    rows = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            rows.append({"path": str(path.relative_to(root)), "digest": file_digest(path)})
    return digest(rows)


def _read(path: Path, label: str) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def _write_private(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.parent.chmod(0o700)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    path.chmod(0o600)


def _task(value: dict[str, Any]) -> dict[str, Any]:
    task = value.get("task") if isinstance(value.get("task"), dict) else value
    if not isinstance(task, dict):
        raise ValueError("private native task custody is malformed")
    if any("gold" in str(key).lower() for key in task):
        raise ValueError("native task custody must not carry gold")
    required = ("task_id", "prompt", "expected_output", "world_id")
    if not all(isinstance(task.get(key), str) and task[key] for key in required):
        raise ValueError("native task custody is missing executor/world fields")
    if not isinstance(task.get("rubric"), list) or not task["rubric"]:
        raise ValueError("native task custody is missing the official rubric")
    return task


def _overlays(path: Path, task_ids: tuple[str, ...]) -> dict[str, Path | None]:
    value = _read(path, "private task overlay index")
    rows = value.get("overlays")
    if not isinstance(rows, list):
        raise ValueError("private task overlay index is missing overlays")
    result: dict[str, Path | None] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("task_id"), str):
            raise ValueError("private task overlay index is malformed")
        raw = row.get("overlay_root")
        if raw is not None and (not isinstance(raw, str) or not Path(raw).is_dir()):
            raise ValueError("private task overlay root is missing")
        if row["task_id"] in result:
            raise ValueError("private task overlay index has duplicate task IDs")
        result[row["task_id"]] = Path(raw) if raw else None
    if tuple(result) != task_ids:
        raise ValueError("private task overlay index does not match the frozen task order")
    return result


def prepare(*, frozen_manifest: dict[str, Any], task_root: Path, overlays_path: Path,
            graph_root: Path, world_root: Path, initial_snapshot: Path,
            executor: tuple[str, str, str], grader: tuple[str, str, str],
            conditions: tuple[str, ...] = CONDITIONS) -> tuple[dict[str, Any], dict[str, Any]]:
    """Validate and content-address every input before a native model call."""
    task_ids = controls.expected_heldout_ids(frozen_manifest)
    if not conditions or any(condition not in CONDITIONS for condition in conditions):
        raise ValueError("native Stage C requires one or more known projection conditions")
    if len(set(conditions)) != len(conditions):
        raise ValueError("native Stage C projection conditions must be unique")
    if not initial_snapshot.is_file():
        raise ValueError("private initial snapshot is missing")
    overlays = _overlays(overlays_path, task_ids)
    tasks: dict[str, dict[str, Any]] = {}
    graphs: dict[str, dict[str, Any]] = {}
    task_digests: dict[str, str] = {}
    graph_digests: dict[str, str] = {}
    overlay_digests: dict[str, str | None] = {}
    projection_digests: dict[str, dict[str, str]] = {}
    typed_counts = {"numeric_atoms": 0, "table_cells": 0, "derivations": 0}
    for task_id in task_ids:
        task_path = task_root / f"{task_id}.json"
        graph_path = graph_root / f"{task_id}.json"
        if not task_path.is_file() or not graph_path.is_file():
            raise ValueError("frozen held-out task or projection graph is missing")
        task = _task(_read(task_path, "private task custody"))
        graph = _read(graph_path, "private projection graph")
        validate_graph(graph)
        if task["task_id"] != task_id or graph.get("task_id") != task_id:
            raise ValueError("frozen held-out control has a task identity mismatch")
        tasks[task_id] = task
        graphs[task_id] = graph
        task_digests[task_id] = file_digest(task_path)
        graph_digests[task_id] = file_digest(graph_path)
        overlay_digests[task_id] = tree_digest(overlays[task_id]) if overlays[task_id] else None
        typed_counts["numeric_atoms"] += len(graph.get("numeric_atoms", []))
        typed_counts["table_cells"] += len(graph.get("table_cells", []))
        typed_counts["derivations"] += len(graph.get("derivations", []))
        projections = [project(graph, condition) for condition in conditions]
        projection_digests[task_id] = {condition: value["projection_digest"]
                                       for condition, value in zip(conditions, projections, strict=True)}
        treatment_payloads = []
        for value in projections:
            treatment_payloads.append({key: row for key, row in value.items()
                                       if key not in {"condition", "projection_digest"}
                                       and not (key in {"numeric_atoms", "table_cells", "derivations",
                                                       "task_parameters"} and row == [])})
        if len(treatment_payloads) > 1 and len({digest(row) for row in treatment_payloads}) != len(treatment_payloads):
            raise ValueError(f"native Stage C conditions have no payload/treatment variation for {task_id}")
    if (any(condition in CONDITIONS[1:] for condition in conditions)
            and typed_counts["numeric_atoms"] + typed_counts["table_cells"] == 0):
        raise ValueError("native Stage C exact treatment requires nonzero numeric atoms or table cells")
    if CONDITIONS[2] in conditions and typed_counts["derivations"] == 0:
        raise ValueError("native Stage C derivation treatment requires nonzero derivations")
    controls_value = {
        "schema_version": SCHEMA,
        "task_ids": list(task_ids),
        "conditions": list(conditions),
        "task_custody_digests": task_digests,
        "projection_graph_digests": graph_digests,
        "projection_digests": projection_digests,
        "typed_object_counts": typed_counts,
        "overlay_source_tree_digests": overlay_digests,
        "world_source_tree_digest": tree_digest(world_root),
        "initial_snapshot_digest": file_digest(initial_snapshot),
        "executor": {"model": executor[0], "provider": executor[1], "reasoning": executor[2],
                     "fallback_allowed": False},
        "grader": {"model": grader[0], "provider": grader[1], "reasoning": grader[2],
                   "fallback_allowed": False},
        "official_lifecycle": True,
        "agent_step_budget": native.AGENT_MAX_STEPS,
        "agent_wall_clock_timeout_seconds": native.AGENT_TIMEOUT_SECONDS,
        "retry_policy": "one native attempt per frozen task-condition cell; inconclusive cells are retained",
        "study_kind": ("three-condition-causal-ablation" if conditions == CONDITIONS
                       else "descriptive-heldout-projection-panel"),
        "automatic_admission": False,
        "human_approval_required": True,
    }
    frozen = {**controls_value, "frozen_controls_digest": digest(controls_value)}
    receipt = {"schema_version": SCHEMA, "status": "frozen-pre-run-no-native-model-call",
               "task_count": len(task_ids), "planned_cells": len(task_ids) * len(conditions),
               "frozen_controls_digest": frozen["frozen_controls_digest"],
               "task_ids_digest": digest(list(task_ids)), "automatic_admission": False,
               "human_approval_required": True,
               "rubric_in_executor": False, "gold_in_custody": False,
               "decision_boundary": ("Every held-out control is frozen before native executor or grader calls. "
                                     "A one-condition panel is descriptive and cannot establish a representation contrast.")}
    return frozen, receipt


def _cell_summary(result: dict[str, Any]) -> dict[str, Any]:
    return {key: result.get(key) for key in ("task_id", "condition", "status", "agent_status",
                                              "official_grading_status", "official_final_score",
                                              "graph_digest")}


def summarize(*, frozen: dict[str, Any], cells: list[dict[str, Any]]) -> dict[str, Any]:
    by_condition: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for cell in cells:
        by_condition[str(cell["condition"])].append(cell)
    rows = []
    for condition in frozen["conditions"]:
        group = by_condition[condition]
        scores = [row.get("official_final_score") for row in group
                  if row.get("status") == "complete" and isinstance(row.get("official_final_score"), (int, float))]
        executor = [row.get("executor", {}).get("telemetry", {}) for row in group]
        grader = [row.get("grader", {}).get("telemetry", {}) for row in group]
        def total(items: list[dict[str, Any]], field: str) -> float | int:
            values = [item.get(field) for item in items]
            if field in ("known_cost_usd",):
                return round(sum(value for value in values if isinstance(value, (int, float))), 12)
            return sum(value for value in values if isinstance(value, int))
        rows.append({"condition": condition, "planned_cells": len(frozen["task_ids"]),
                     "complete_cells": sum(row.get("status") == "complete" for row in group),
                     "inconclusive_cells": sum(row.get("status") != "complete" for row in group),
                     "scored_cells": len(scores),
                     "mean_official_final_score": round(sum(scores) / len(scores), 12) if scores else None,
                     "executor": {"calls": total(executor, "calls"),
                                  "known_cost_usd": total(executor, "known_cost_usd"),
                                  "input_tokens": total(executor, "input_tokens"),
                                  "output_tokens": total(executor, "output_tokens")},
                     "grader": {"calls": total(grader, "calls"),
                                "known_cost_usd": total(grader, "known_cost_usd"),
                                "input_tokens": total(grader, "input_tokens"),
                                "output_tokens": total(grader, "output_tokens")}})
    return {"schema_version": SCHEMA,
            "status": "complete" if all(row["complete_cells"] == row["planned_cells"] for row in rows) else "inconclusive",
            "frozen_controls_digest": frozen["frozen_controls_digest"],
            "study_kind": frozen.get("study_kind"),
            "task_count": len(frozen["task_ids"]),
            "planned_cells": len(frozen["task_ids"]) * len(frozen["conditions"]),
            "scored_cells": sum(row["scored_cells"] for row in rows),
            "inconclusive_cells": sum(row["inconclusive_cells"] for row in rows),
            "conditions": rows, "cells": [_cell_summary(row) for row in cells],
            "automatic_admission": False, "human_approval_required": True,
            "decision_boundary": "Official native APEX scores are evaluation evidence, not admission of candidate knowledge."}


def execute(*, harness: Path, frozen: dict[str, Any], task_root: Path, overlays_path: Path,
            graph_root: Path, world_root: Path, initial_snapshot: Path, bridge: Path,
            out: Path) -> dict[str, Any]:
    """Execute every cell once in frozen order, preserving a durable receipt per cell."""
    if native.httpx is None:
        raise RuntimeError("native Stage C must run under the Archipelago harness virtual environment")
    if out.exists() and any(out.iterdir()):
        raise ValueError("native Stage C output must be fresh")
    out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    _write_private(out / "native-stage-c-frozen-controls-private.json", frozen)
    _write_private(out / "native-stage-c-preflight-sanitized.json", {
        "schema_version": SCHEMA, "status": "passed-before-native-model-call",
        "planned_cells": len(frozen["task_ids"]) * len(frozen["conditions"]),
        "frozen_controls_digest": frozen["frozen_controls_digest"],
        "automatic_admission": False, "human_approval_required": True,
    })
    overlays = _overlays(overlays_path, tuple(frozen["task_ids"]))
    cells: list[dict[str, Any]] = []
    for task_id in frozen["task_ids"]:
        task = _task(_read(task_root / f"{task_id}.json", "private task custody"))
        graph = _read(graph_root / f"{task_id}.json", "private projection graph")
        for condition in frozen["conditions"]:
            cell_out = out / "cells" / task_id / condition
            result = native.run(harness=harness, task=task, world_root=world_root,
                                initial_snapshot=initial_snapshot, task_overlay=overlays[task_id], graph=graph,
                                condition=condition, out=cell_out, bridge=bridge,
                                executor=(frozen["executor"]["model"], frozen["executor"]["provider"],
                                          frozen["executor"]["reasoning"]),
                                grader=(frozen["grader"]["model"], frozen["grader"]["provider"],
                                        frozen["grader"]["reasoning"]), endpoint="http://localhost:8080")
            cells.append(result)
            _write_private(out / "native-stage-c-progress-sanitized.json", summarize(frozen=frozen, cells=cells))
    result = summarize(frozen=frozen, cells=cells)
    _write_private(out / "native-stage-c-result-sanitized.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen-manifest", required=True, type=Path)
    parser.add_argument("--task-root", required=True, type=Path)
    parser.add_argument("--overlays", required=True, type=Path)
    parser.add_argument("--graph-root", required=True, type=Path)
    parser.add_argument("--harness", required=True, type=Path)
    parser.add_argument("--world-root", required=True, type=Path)
    parser.add_argument("--initial-snapshot", required=True, type=Path)
    parser.add_argument("--bridge", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--execute", action="store_true", help="Authorize the frozen paid native APEX cells.")
    parser.add_argument("--condition", choices=CONDITIONS, action="append",
                        help="Run a frozen subset only when the resulting study is explicitly descriptive.")
    for role in ("executor", "grader"):
        parser.add_argument(f"--{role}-model", required=True)
        parser.add_argument(f"--{role}-provider", required=True)
        parser.add_argument(f"--{role}-reasoning", required=True)
    args = parser.parse_args()
    selected_conditions = tuple(args.condition) if args.condition else CONDITIONS
    frozen, receipt = prepare(frozen_manifest=_read(args.frozen_manifest, "frozen v25 manifest"),
                              task_root=args.task_root, overlays_path=args.overlays,
                              graph_root=args.graph_root, world_root=args.world_root,
                              initial_snapshot=args.initial_snapshot,
                              executor=(args.executor_model, args.executor_provider, args.executor_reasoning),
                              grader=(args.grader_model, args.grader_provider, args.grader_reasoning),
                              conditions=selected_conditions)
    if not args.execute:
        _write_private(args.out / "native-stage-c-preflight-sanitized.json", receipt)
        print(json.dumps({key: receipt[key] for key in ("status", "task_count", "planned_cells",
                                                         "frozen_controls_digest")}, sort_keys=True))
        return
    result = execute(harness=args.harness, frozen=frozen, task_root=args.task_root,
                     overlays_path=args.overlays, graph_root=args.graph_root,
                     world_root=args.world_root, initial_snapshot=args.initial_snapshot,
                     bridge=args.bridge, out=args.out)
    print(json.dumps({key: result[key] for key in ("status", "task_count", "planned_cells",
                                                    "scored_cells", "inconclusive_cells")}, sort_keys=True))
    if result["status"] != "complete":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

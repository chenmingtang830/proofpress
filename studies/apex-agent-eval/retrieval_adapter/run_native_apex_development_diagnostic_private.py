#!/usr/bin/env python3
"""Run a frozen three-task, two-condition native APEX development diagnostic.

This is deliberately not a held-out study.  Task order is supplied explicitly,
the treatment must vary for every task, and every attempted cell is checkpointed.
No model call occurs unless ``--execute`` is supplied.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import signal
import sys
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parents[3]
ADAPTER = Path(__file__).resolve().parent
for value in (ROOT, ADAPTER):
    if str(value) not in sys.path:
        sys.path.insert(0, str(value))

from phase_c_ablation_contract import project, validate_graph
import run_native_apex_projection_private as native


SCHEMA = "proofpress/native-apex-development-diagnostic/v1"
STUDY_KIND = "development-diagnostic-not-heldout"
CONDITIONS = ("ordinary-claim", "claim-plus-table-cells-plus-derivation")
CELL_TIMEOUT_SECONDS = 30 * 60


def digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _read(path: Path, label: str) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def _write_private(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.parent.chmod(0o700)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2,
                               sort_keys=True) + "\n")
    path.chmod(0o600)


def task_ids(path: Path) -> tuple[str, str, str]:
    """Read an explicit ordered JSON list (or {task_ids: [...]}) of three IDs."""
    value = json.loads(path.read_text())
    rows = value.get("task_ids") if isinstance(value, dict) else value
    if (not isinstance(rows, list) or len(rows) != 3
            or any(not isinstance(row, str) or not row for row in rows)):
        raise ValueError("development diagnostic requires exactly three ordered task IDs")
    if len(set(rows)) != 3:
        raise ValueError("development diagnostic task IDs must be unique")
    return tuple(rows)  # type: ignore[return-value]


def _task(value: dict[str, Any]) -> dict[str, Any]:
    result = value.get("task") if isinstance(value.get("task"), dict) else value
    if not isinstance(result, dict):
        raise ValueError("private task custody is malformed")
    required = ("task_id", "prompt", "expected_output", "world_id")
    if not all(isinstance(result.get(key), str) and result[key] for key in required):
        raise ValueError("private task custody is missing executor/world fields")
    if not isinstance(result.get("rubric"), list) or not result["rubric"]:
        raise ValueError("private task custody is missing the official rubric")
    if any("gold" in str(key).lower() for key in result):
        raise ValueError("native task custody must not carry gold")
    return result


def _overlays(path: Path, ordered_ids: tuple[str, str, str]) -> dict[str, Path | None]:
    rows = _read(path, "private overlay index").get("overlays")
    if not isinstance(rows, list):
        raise ValueError("private overlay index is missing overlays")
    result: dict[str, Path | None] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("task_id"), str):
            raise ValueError("private overlay index is malformed")
        raw = row.get("overlay_root")
        if raw is not None and (not isinstance(raw, str) or not Path(raw).is_dir()):
            raise ValueError("private task overlay root is missing")
        result[row["task_id"]] = Path(raw) if raw else None
    if tuple(result) != ordered_ids:
        raise ValueError("private overlay index must match the frozen task order")
    return result


def prepare(*, ids_path: Path, task_root: Path, graph_root: Path,
            overlays_path: Path, world_root: Path, initial_snapshot: Path,
            executor: tuple[str, str, str], grader: tuple[str, str, str],
            max_known_cost_usd: float) -> dict[str, Any]:
    """Fail closed on structure and treatment before any paid/model call."""
    if max_known_cost_usd <= 0:
        raise ValueError("known-cost ceiling must be positive")
    ordered_ids = task_ids(ids_path)
    if not world_root.is_dir() or not initial_snapshot.is_file():
        raise ValueError("native development world and initial snapshot must exist")
    _overlays(overlays_path, ordered_ids)
    counts = {"numeric_atoms": 0, "table_cells": 0, "derivations": 0}
    projections: dict[str, dict[str, str]] = {}
    graph_digests: dict[str, str] = {}
    for task_id in ordered_ids:
        task_path, graph_path = task_root / f"{task_id}.json", graph_root / f"{task_id}.json"
        if not task_path.is_file() or not graph_path.is_file():
            raise ValueError(f"development diagnostic input is missing for {task_id}")
        task = _task(_read(task_path, "private task custody"))
        graph = _read(graph_path, "private projection graph")
        validate_graph(graph)
        if task["task_id"] != task_id or graph.get("task_id") != task_id:
            raise ValueError("development diagnostic task identity mismatch")
        for field in counts:
            counts[field] += len(graph.get(field, []))
        values = [project(graph, condition) for condition in CONDITIONS]
        payloads = [{key: item for key, item in value.items()
                     if key not in {"condition", "projection_digest"}} for value in values]
        if digest(payloads[0]) == digest(payloads[1]):
            raise ValueError(f"projection treatment does not vary for {task_id}")
        projections[task_id] = {condition: value["projection_digest"]
                                for condition, value in zip(CONDITIONS, values, strict=True)}
        graph_digests[task_id] = graph["graph_digest"]
    if any(counts[field] == 0 for field in counts):
        raise ValueError("diagnostic panel requires aggregate nonzero numeric_atoms, table_cells, and derivations")
    controls = {
        "schema_version": SCHEMA, "study_kind": STUDY_KIND,
        "task_ids": list(ordered_ids), "conditions": list(CONDITIONS),
        "projection_digests": projections, "graph_digests": graph_digests,
        "typed_object_counts": counts, "planned_cells": 6,
        "executor": {"model": executor[0], "provider": executor[1], "reasoning": executor[2],
                     "fallback_allowed": False},
        "grader": {"model": grader[0], "provider": grader[1], "reasoning": grader[2],
                    "fallback_allowed": False},
        "cell_timeout_seconds": CELL_TIMEOUT_SECONDS,
        "max_total_known_cost_usd": max_known_cost_usd,
        "retry_policy": "exactly one attempt per frozen task-condition cell; no retries",
        "automatic_admission": False, "human_approval_required": True,
    }
    return {**controls, "frozen_controls_digest": digest(controls)}


def _telemetry(cell: dict[str, Any], role: str) -> dict[str, Any]:
    value = cell.get(role, {})
    return value.get("telemetry", {}) if isinstance(value, dict) else {}


def known_cost(cells: list[dict[str, Any]]) -> float:
    return round(sum(value for cell in cells for role in ("executor", "grader")
                     if isinstance((value := _telemetry(cell, role).get("known_cost_usd")), (int, float))), 12)


def _criterion_scores(cell_out: Path) -> list[dict[str, Any]]:
    path = cell_out / "grades_private.json"
    if not path.is_file():
        return []
    rows = _read(path, "official native grades").get("verifier_results")
    if not isinstance(rows, list):
        return []
    return [{"criterion_index": index, "score": row.get("score"), "status": row.get("status")}
            for index, row in enumerate(rows) if isinstance(row, dict)]


def summarize(frozen: dict[str, Any], cells: list[dict[str, Any]], *, stopped_for_cost: bool = False) -> dict[str, Any]:
    by_condition: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for cell in cells:
        by_condition[str(cell.get("condition"))].append(cell)

    def totals(group: list[dict[str, Any]], role: str) -> dict[str, Any]:
        telemetry = [_telemetry(cell, role) for cell in group]
        return {
            "calls": sum(row.get("calls", 0) for row in telemetry if isinstance(row.get("calls", 0), int)),
            "input_tokens": sum(row.get("input_tokens", 0) for row in telemetry
                                if isinstance(row.get("input_tokens", 0), int)),
            "output_tokens": sum(row.get("output_tokens", 0) for row in telemetry
                                 if isinstance(row.get("output_tokens", 0), int)),
            "known_cost_usd": round(sum(row.get("known_cost_usd", 0) for row in telemetry
                                        if isinstance(row.get("known_cost_usd", 0), (int, float))), 12),
        }

    conditions = []
    for condition in CONDITIONS:
        group = by_condition[condition]
        scores = [cell["official_final_score"] for cell in group
                  if isinstance(cell.get("official_final_score"), (int, float))]
        criterion = [row for cell in group for row in cell.get("criterion_scores", [])
                     if isinstance(row, dict)]
        criterion_values = [row["score"] for row in criterion if isinstance(row.get("score"), (int, float))]
        conditions.append({
            "condition": condition, "attempted_cells": len(group), "scored_tasks": len(scores),
            "mean_task_score": round(sum(scores) / len(scores), 12) if scores else None,
            "scored_criteria": len(criterion_values),
            "mean_criterion_score": round(sum(criterion_values) / len(criterion_values), 12)
            if criterion_values else None,
            "executor": totals(group, "executor"), "grader": totals(group, "grader"),
        })
    attempted = len(cells)
    complete = sum(cell.get("status") == "complete" for cell in cells)
    status = ("cost-ceiling-reached" if stopped_for_cost else
              "complete" if attempted == 6 and complete == 6 else "inconclusive")
    return {
        "schema_version": SCHEMA, "study_kind": STUDY_KIND, "status": status,
        "frozen_controls_digest": frozen["frozen_controls_digest"],
        "task_count": 3, "planned_cells": 6, "attempted_cells": attempted,
        "complete_cells": complete,
        "known_cost_usd": known_cost(cells), "max_total_known_cost_usd": frozen["max_total_known_cost_usd"],
        "conditions": conditions,
        "tasks": [{"task_id": cell.get("task_id"), "condition": cell.get("condition"),
                   "status": cell.get("status"), "official_final_score": cell.get("official_final_score"),
                   "criterion_scores": cell.get("criterion_scores", [])} for cell in cells],
        "automatic_admission": False, "human_approval_required": True,
    }


class CellDeadline(TimeoutError):
    pass


@contextmanager
def cell_deadline(seconds: int = CELL_TIMEOUT_SECONDS) -> Iterator[None]:
    """Interrupt native.run safely so its own finally block can stop gateways."""
    if not hasattr(signal, "SIGALRM"):
        yield
        return
    previous = signal.getsignal(signal.SIGALRM)
    def expired(_signum: int, _frame: Any) -> None:
        raise CellDeadline(f"native diagnostic cell exceeded {seconds} seconds")
    signal.signal(signal.SIGALRM, expired)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


def execute(*, frozen: dict[str, Any], harness: Path, task_root: Path,
            graph_root: Path, overlays_path: Path, world_root: Path,
            initial_snapshot: Path, bridge: Path, out: Path) -> dict[str, Any]:
    if native.httpx is None:
        raise RuntimeError("diagnostic must run under the Archipelago harness virtual environment")
    if out.exists() and any(out.iterdir()):
        raise ValueError("diagnostic output must be fresh")
    out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    _write_private(out / "frozen-controls-private.json", frozen)
    overlays = _overlays(overlays_path, tuple(frozen["task_ids"]))
    cells: list[dict[str, Any]] = []
    stopped = False
    old_timeout = native.AGENT_TIMEOUT_SECONDS
    native.AGENT_TIMEOUT_SECONDS = CELL_TIMEOUT_SECONDS
    try:
        for task_id in frozen["task_ids"]:
            task = _task(_read(task_root / f"{task_id}.json", "private task custody"))
            graph = _read(graph_root / f"{task_id}.json", "private projection graph")
            for condition in CONDITIONS:
                if known_cost(cells) >= frozen["max_total_known_cost_usd"]:
                    stopped = True
                    break
                cell_out = out / "cells" / task_id / condition
                with cell_deadline():
                    result = native.run(
                        harness=harness, task=task, world_root=world_root,
                        initial_snapshot=initial_snapshot, task_overlay=overlays[task_id],
                        graph=graph, condition=condition, out=cell_out, bridge=bridge,
                        executor=(frozen["executor"]["model"], frozen["executor"]["provider"],
                                  frozen["executor"]["reasoning"]),
                        grader=(frozen["grader"]["model"], frozen["grader"]["provider"],
                                frozen["grader"]["reasoning"]), endpoint="http://localhost:8080")
                result["criterion_scores"] = _criterion_scores(cell_out)
                cells.append(result)
                _write_private(out / "progress-sanitized.json", summarize(frozen, cells))
                if known_cost(cells) >= frozen["max_total_known_cost_usd"]:
                    stopped = True
                    break
            if stopped:
                break
    finally:
        native.AGENT_TIMEOUT_SECONDS = old_timeout
    result = summarize(frozen, cells, stopped_for_cost=stopped)
    _write_private(out / "result-sanitized.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-ids", required=True, type=Path)
    parser.add_argument("--task-root", required=True, type=Path)
    parser.add_argument("--graph-root", required=True, type=Path)
    parser.add_argument("--overlays", required=True, type=Path)
    parser.add_argument("--harness", required=True, type=Path)
    parser.add_argument("--world-root", required=True, type=Path)
    parser.add_argument("--initial-snapshot", required=True, type=Path)
    parser.add_argument("--bridge", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--max-known-cost-usd", required=True, type=float)
    parser.add_argument("--execute", action="store_true")
    for role in ("executor", "grader"):
        parser.add_argument(f"--{role}-model", required=True)
        parser.add_argument(f"--{role}-provider", required=True)
        parser.add_argument(f"--{role}-reasoning", required=True)
    args = parser.parse_args()
    frozen = prepare(ids_path=args.task_ids, task_root=args.task_root, graph_root=args.graph_root,
                     overlays_path=args.overlays, world_root=args.world_root,
                     initial_snapshot=args.initial_snapshot,
                     executor=(args.executor_model, args.executor_provider, args.executor_reasoning),
                     grader=(args.grader_model, args.grader_provider, args.grader_reasoning),
                     max_known_cost_usd=args.max_known_cost_usd)
    if not args.execute:
        receipt = {"schema_version": SCHEMA, "study_kind": STUDY_KIND,
                   "status": "preflight-passed-no-model-call", "task_count": 3,
                   "planned_cells": 6, "frozen_controls_digest": frozen["frozen_controls_digest"],
                   "typed_object_counts": frozen["typed_object_counts"]}
        _write_private(args.out / "preflight-sanitized.json", receipt)
        print(json.dumps(receipt, sort_keys=True))
        return
    result = execute(frozen=frozen, harness=args.harness, task_root=args.task_root,
                     graph_root=args.graph_root, overlays_path=args.overlays,
                     world_root=args.world_root, initial_snapshot=args.initial_snapshot,
                     bridge=args.bridge, out=args.out)
    print(json.dumps({key: result[key] for key in ("status", "planned_cells", "attempted_cells",
                                                    "known_cost_usd")}, sort_keys=True))
    if result["status"] != "complete":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

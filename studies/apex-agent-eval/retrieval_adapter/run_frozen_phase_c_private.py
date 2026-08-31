#!/usr/bin/env python3
"""Run the v25 Phase C ablation only from a content-addressed freeze receipt.

The three treatments differ exclusively by the deterministic projection in
``phase_c_ablation_contract.py``.  All source text, task prompts, rubrics,
candidate artifacts, and model completions remain in the caller-owned private
output directory.  The committed report contains only digests, counts,
terminal statuses, and cost telemetry.

The command protocol intentionally keeps the Gateway implementation outside
this repository.  A frozen executor/grader configuration identifies an
executable command and hashes every implementation file it invokes; this lets
the private Proofpress development checkout supply the AI Gateway bridge
without copying credentials or source material into this repository.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from phase_c_ablation_contract import CONDITIONS, digest as projection_digest, project, validate_graph, validate_projection

FREEZE_PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/freeze_v25_phase_c_inputs_private.py"
FREEZE_SPEC = importlib.util.spec_from_file_location("freeze_v25_phase_c_inputs", FREEZE_PATH)
freeze_v25 = importlib.util.module_from_spec(FREEZE_SPEC); FREEZE_SPEC.loader.exec_module(freeze_v25)
CONTRACT_PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/transfer_validation_contract.py"
CONTRACT_SPEC = importlib.util.spec_from_file_location("transfer_validation_contract", CONTRACT_PATH)
transfer_contract = importlib.util.module_from_spec(CONTRACT_SPEC); CONTRACT_SPEC.loader.exec_module(transfer_contract)

SCHEMA = "proofpress/frozen-phase-c-run/v1"
TERMINAL = {"scored", "inconclusive"}


def file_digest(path: Path) -> str:
    return freeze_v25.file_digest(path)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def _required_object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a JSON object")
    return value


def _validate_command_config(config: dict[str, Any], *, role: str) -> None:
    command = config.get("command")
    if not isinstance(command, list) or not command or any(not isinstance(item, str) or not item for item in command):
        raise ValueError(f"{role} config requires a non-empty command array")
    implementations = config.get("implementation_files")
    if not isinstance(implementations, list) or not implementations:
        raise ValueError(f"{role} config requires content-addressed implementation_files")
    for row in implementations:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str) or not isinstance(row.get("digest"), str):
            raise ValueError(f"{role} implementation_files entries require path and digest")
        path = Path(row["path"])
        if not path.is_file() or file_digest(path) != row["digest"]:
            raise ValueError(f"{role} implementation file digest mismatch")
    if not isinstance(config.get("timeout_seconds"), (int, float)) or config["timeout_seconds"] <= 0:
        raise ValueError(f"{role} config requires a positive timeout_seconds")
    if not all(isinstance(config.get(field), str) and config[field]
               for field in ("model", "provider")):
        raise ValueError(f"{role} config requires exact model and provider")
    if not isinstance(config.get("max_output_tokens"), int) or config["max_output_tokens"] < 1:
        raise ValueError(f"{role} config requires positive max_output_tokens")
    if role == "grader" and config.get("blind_grades_per_artifact") != 3:
        raise ValueError("grader config requires exactly three blind grades per artifact")


def _command(config: dict[str, Any]) -> list[str]:
    return list(config["command"])


def _run_command(command: list[str], request: dict[str, Any], timeout: float) -> tuple[dict[str, Any], dict[str, Any]]:
    """Execute one frozen adapter invocation with no fallback or retry."""
    started = time.monotonic()
    try:
        result = subprocess.run(command, input=json.dumps(request, ensure_ascii=False), text=True,
                                capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        return {}, {"status": "inconclusive", "reason": "command_timeout",
                    "latency_ms": round((time.monotonic() - started) * 1000, 3)}
    elapsed = round((time.monotonic() - started) * 1000, 3)
    if result.returncode != 0:
        return {}, {"status": "inconclusive", "reason": "command_nonzero_exit",
                    "exit_code": result.returncode, "latency_ms": elapsed}
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}, {"status": "inconclusive", "reason": "command_invalid_json", "latency_ms": elapsed}
    if not isinstance(value, dict):
        return {}, {"status": "inconclusive", "reason": "command_nonobject_json", "latency_ms": elapsed}
    return value, {"status": "ok", "latency_ms": elapsed}


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _valid_grade(value: dict[str, Any]) -> bool:
    return (_number(value.get("rubric_fraction")) and 0 <= value["rubric_fraction"] <= 1
            and all(isinstance(value.get(name), int) and value[name] >= 0
                    for name in ("unsupported_claims", "citation_errors", "authority_errors")))


def _telemetry(value: Any) -> dict[str, float | int | None]:
    """Accept a complete receipt or preserve an explicit unknown cost state."""
    row = value if isinstance(value, dict) else {}
    cost = row.get("cost_usd")
    inputs, outputs = row.get("input_tokens"), row.get("output_tokens")
    if cost is not None and (not _number(cost) or cost < 0):
        raise ValueError("model telemetry cost_usd must be a non-negative number or null")
    for name, token_count in (("input_tokens", inputs), ("output_tokens", outputs)):
        if token_count is not None and (not isinstance(token_count, int) or token_count < 0):
            raise ValueError(f"model telemetry {name} must be a non-negative integer or null")
    return {"cost_usd": cost, "input_tokens": inputs, "output_tokens": outputs}


def _executor_response(value: dict[str, Any]) -> tuple[dict[str, Any], dict[str, float | int | None]]:
    if not isinstance(value.get("artifact"), dict):
        raise ValueError("executor response requires an artifact object")
    return value["artifact"], _telemetry(value.get("telemetry"))


def _grader_response(value: dict[str, Any]) -> tuple[dict[str, Any], dict[str, float | int | None]]:
    if not isinstance(value.get("grade"), dict) or not _valid_grade(value["grade"]):
        raise ValueError("grader response requires a valid grade object")
    return value["grade"], _telemetry(value.get("telemetry"))


def _task_rows(value: dict[str, Any], rubric_manifest: dict[str, Any],
               manifest: dict[str, Any]) -> list[dict[str, Any]]:
    tasks = value.get("tasks")
    if not isinstance(tasks, list):
        raise ValueError("task source manifest requires a tasks array")
    expected = list(manifest["development_task_ids"]) + list(manifest["held_out_task_ids"])
    by_id = {}
    for task in tasks:
        if not isinstance(task, dict) or not isinstance(task.get("task_id"), str):
            raise ValueError("task source manifest task requires task_id")
        if task["task_id"] in by_id:
            raise ValueError("task source manifest task IDs must be unique")
        if not isinstance(task.get("prompt"), str):
            raise ValueError("task source manifest requires a private prompt per task")
        by_id[task["task_id"]] = task
    if set(by_id) != set(expected):
        raise ValueError("task source manifest task IDs do not match the frozen panel")
    rubric_rows = rubric_manifest.get("rubrics")
    if not isinstance(rubric_rows, list):
        raise ValueError("rubric manifest requires a rubrics array")
    rubrics = {}
    for row in rubric_rows:
        if not isinstance(row, dict) or not isinstance(row.get("task_id"), str) or not isinstance(row.get("rubric"), list):
            raise ValueError("rubric manifest entries require task_id and rubric")
        if row["task_id"] in rubrics:
            raise ValueError("rubric manifest task IDs must be unique")
        rubrics[row["task_id"]] = row["rubric"]
    if set(rubrics) != set(expected):
        raise ValueError("rubric manifest task IDs do not match the frozen panel")
    return [{**by_id[task_id], "rubric": rubrics[task_id]} for task_id in expected]


def validate_preflight(*, frozen_manifest_path: Path, freeze_receipt_path: Path,
                       control_paths: dict[str, Path]) -> dict[str, Any]:
    """Check all frozen bytes and gates before opening a task payload or model route."""
    frozen = read_json(frozen_manifest_path)
    receipt = read_json(freeze_receipt_path)
    expected = transfer_contract.validate_transfer_manifest(frozen)
    if receipt.get("status") != "frozen" or receipt.get("manifest_digest") != expected["manifest_digest"]:
        raise ValueError("Phase C freeze receipt does not authenticate the frozen manifest")
    if receipt.get("executor_called") is not False or receipt.get("grader_called") is not False:
        raise ValueError("Phase C pre-run receipt unexpectedly records model execution")
    if set(control_paths) != set(freeze_v25.CONTROL_ARGUMENTS):
        raise ValueError("every frozen Phase C control path is required")
    # Gate reports are checked first, before any private Phase C task/source
    # bytes are opened.  This mirrors the DeepSeek runner's CUDA preflight:
    # unqualified routes cannot gain access merely by appearing in a receipt.
    for field in ("primary_extraction_qualification", "sensitivity_extraction_qualification"):
        path = control_paths[field]
        if not path.is_file() or file_digest(path) != frozen["frozen_controls"].get(field):
            raise ValueError(f"frozen control digest mismatch: {field}")
    # This repeats semantic inspection after byte verification.  It prevents a
    # manually composed receipt from binding an extraction report that merely
    # looks complete while lacking passed dev + held-out sensitivity evidence.
    freeze_v25.validate_extraction_qualification(
        read_json(control_paths["primary_extraction_qualification"]),
        route=frozen["stage_b5_extraction"]["primary_route"], key="paddleocr_vl_1_6_mlx")
    freeze_v25.validate_extraction_qualification(
        read_json(control_paths["sensitivity_extraction_qualification"]),
        route=frozen["stage_b5_extraction"]["sensitivity_route"], key="deepseek_ocr_2_sensitivity")
    for field, path in control_paths.items():
        if field in {"primary_extraction_qualification", "sensitivity_extraction_qualification"}:
            continue
        if not path.is_file() or file_digest(path) != frozen["frozen_controls"].get(field):
            raise ValueError(f"frozen control digest mismatch: {field}")
    graph = read_json(control_paths["graph_digest"]); validate_graph(graph)
    rubric_manifest = read_json(control_paths["rubric_digest"])
    tasks = _task_rows(read_json(control_paths["task_source_manifest_digest"]), rubric_manifest, frozen)
    _validate_command_config(read_json(control_paths["executor"]), role="executor")
    _validate_command_config(read_json(control_paths["grader"]), role="grader")
    retry = _required_object(read_json(control_paths["retry_policy"]), "retry policy")
    if retry.get("fallback") != "forbidden" or retry.get("terminal_receipt_required") is not True:
        raise ValueError("Phase C requires fallback-forbidden terminal receipt policy")
    for field in ("disclosure_budget", "executor_budget", "native_output_contract"):
        _required_object(read_json(control_paths[field]), field)
    disclosure_budget = read_json(control_paths["disclosure_budget"])
    if not isinstance(disclosure_budget.get("max_projection_bytes"), int) or disclosure_budget["max_projection_bytes"] < 1:
        raise ValueError("disclosure budget requires positive max_projection_bytes")
    return {"frozen": frozen, "receipt": receipt, "graph": graph, "tasks": tasks,
            "executor": read_json(control_paths["executor"]),
            "grader": read_json(control_paths["grader"]),
            "rubric_manifest": rubric_manifest, "disclosure_budget": disclosure_budget,
            "executor_budget": read_json(control_paths["executor_budget"]),
            "native_output_contract": read_json(control_paths["native_output_contract"])}


def _safe_private_write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.parent.chmod(0o700)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    path.chmod(0o600)


def run(preflight: dict[str, Any], *, out: Path) -> dict[str, Any]:
    """Run the complete frozen panel in fixed task × condition order."""
    out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw = out / "raw"; raw.mkdir(exist_ok=True); raw.chmod(0o700)
    graph, executor, grader = preflight["graph"], preflight["executor"], preflight["grader"]
    projections = {condition: project(graph, condition) for condition in CONDITIONS}
    for projection in projections.values():
        validate_projection(projection, graph)
        if len(json.dumps(projection, ensure_ascii=False, sort_keys=True).encode()) > preflight["disclosure_budget"]["max_projection_bytes"]:
            raise ValueError("one or more frozen Phase C projections exceed the shared disclosure budget")
    cells = []
    for task in preflight["tasks"]:
        # Never pass the rubric or any task outcome to the execution command.
        executor_task = {key: task[key] for key in ("task_id", "prompt", "expected_output") if key in task}
        for condition in CONDITIONS:
            projection = projections[condition]
            request = {"schema_version": SCHEMA, "kind": "executor", "task": executor_task,
                       "projection": projection, "executor_budget": preflight["executor_budget"],
                       "native_output_contract": preflight["native_output_contract"],
                       "instruction": "Use only the supplied projection. Preserve not_governed and Human Approval boundaries."}
            executor_response, execution = _run_command(_command(executor), request, float(executor["timeout_seconds"]))
            cell = {"task_id": task["task_id"], "condition": condition,
                    "projection_digest": projection["projection_digest"],
                    "execution": execution, "status": "inconclusive"}
            if execution["status"] != "ok":
                cells.append(cell); continue
            try:
                artifact, executor_telemetry = _executor_response(executor_response)
            except ValueError as exc:
                cell["execution"] = {**execution, "status": "inconclusive", "reason": str(exc)}
                cells.append(cell); continue
            cell["executor_telemetry"] = executor_telemetry
            artifact_path = raw / f"{task['task_id']}-{condition}-artifact.json"
            _safe_private_write(artifact_path, artifact)
            grade_request = {"schema_version": SCHEMA, "kind": "grader",
                             "task": {"task_id": task["task_id"], "prompt": task["prompt"], "rubric": task["rubric"]},
                             "candidate": artifact,
                             "instruction": "Blindly grade only this candidate against this frozen rubric."}
            grades, grade_telemetry = [], []
            grade_failure = None
            for replica in range(grader["blind_grades_per_artifact"]):
                grade_response, grading = _run_command(_command(grader), {**grade_request, "replica": replica + 1},
                                                       float(grader["timeout_seconds"]))
                if grading["status"] != "ok":
                    grade_failure = grading.get("reason", "grader_call_failed")
                    break
                try:
                    grade, telemetry = _grader_response(grade_response)
                except ValueError as exc:
                    grade_failure = str(exc)
                    break
                grades.append(grade); grade_telemetry.append(telemetry)
            cell["grading"] = {"status": "ok" if grade_failure is None else "inconclusive",
                               "valid_grade_count": len(grades), "replicas_required": grader["blind_grades_per_artifact"]}
            if grade_failure is not None or len(grades) != grader["blind_grades_per_artifact"]:
                cell["grading"]["reason"] = grade_failure or "fewer_than_three_valid_blind_grades"
                cells.append(cell); continue
            cell.update({"status": "scored",
                         "rubric_fraction": statistics.mean(grade["rubric_fraction"] for grade in grades),
                         "unsupported_claims": statistics.mean(grade["unsupported_claims"] for grade in grades),
                         "citation_errors": statistics.mean(grade["citation_errors"] for grade in grades),
                         "authority_errors": statistics.mean(grade["authority_errors"] for grade in grades),
                         "grader_telemetry": grade_telemetry,
                         "artifact_digest": projection_digest(artifact)})
            cells.append(cell)
    scored = [row for row in cells if row["status"] == "scored"]
    def totals(rows: list[dict[str, Any]], field: str) -> float | int | None:
        values = [row["executor_telemetry"].get(field) for row in rows]
        values.extend(item.get(field) for row in rows for item in row["grader_telemetry"])
        return sum(values) if values and all(value is not None for value in values) else None
    aggregate = {condition: {"scored_tasks": len(rows),
                             "rubric_fraction": (statistics.mean(row["rubric_fraction"] for row in rows)
                                                  if rows else None),
                             "known_cost_usd": totals(rows, "cost_usd"),
                             "input_tokens": totals(rows, "input_tokens"),
                             "output_tokens": totals(rows, "output_tokens")}
                 for condition in CONDITIONS
                 for rows in [[row for row in scored if row["condition"] == condition]]}
    return {"schema_version": SCHEMA, "status": "complete" if len(scored) == len(cells) else "inconclusive",
            "automatic_admission": False, "human_approval_required": True,
            "frozen_manifest_digest": preflight["receipt"]["manifest_digest"],
            "conditions": list(CONDITIONS), "executor": {key: executor[key] for key in ("model", "provider", "max_output_tokens")},
            "grader": {key: grader[key] for key in ("model", "provider", "max_output_tokens", "blind_grades_per_artifact")},
            "planned_cells": len(cells), "scored_cells": len(scored),
            "inconclusive_cells": len(cells) - len(scored), "aggregate": aggregate,
            "cells": cells,
            "decision_boundary": "Private evaluation only; no candidate, extraction, or model output is admitted."}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen-manifest", required=True, type=Path)
    parser.add_argument("--freeze-receipt", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--preflight-only", action="store_true")
    for argument in freeze_v25.CONTROL_ARGUMENTS.values():
        parser.add_argument("--" + argument.replace("_", "-"), required=True, type=Path)
    args = parser.parse_args()
    controls = {field: getattr(args, argument) for field, argument in freeze_v25.CONTROL_ARGUMENTS.items()}
    preflight = validate_preflight(frozen_manifest_path=args.frozen_manifest,
                                   freeze_receipt_path=args.freeze_receipt, control_paths=controls)
    if args.preflight_only:
        print(json.dumps({"status": "pass", "executor_called": False, "grader_called": False,
                          "task_count": len(preflight["tasks"]), "conditions": list(CONDITIONS),
                          "manifest_digest": preflight["receipt"]["manifest_digest"]}, sort_keys=True))
        return
    result = run(preflight, out=args.out)
    _safe_private_write(args.out / "phase-c-result-sanitized.json", result)
    print(json.dumps({key: result[key] for key in ("status", "planned_cells", "scored_cells", "inconclusive_cells")}, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Private-run entrypoint for Finance evidence-first E2E v2 qualification."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import random
import shutil
import subprocess
import zipfile
import hashlib

from pp_eval.apex_ib_pr36 import (
    ENVIRONMENT_IMAGE,
    EXECUTOR_MODEL,
    FINANCE_E2E_V2_FORMAL_TASK_IDS,
    QUALIFICATION_TASK_ID,
    MERGER_MODEL,
    JUDGE_MODEL,
    TASK_SPECS,
    compact_apex_output,
    host_preflight,
    load_public_task,
    majority_native_result,
    repeat_native_grading,
    run_apex_stage,
    write_json,
)
from pp_eval.finance_e2e_v2 import executor_qualification, freeze_formal_tasks, fresh_task_audit, legacy_working_set_preflight, summarize_formal_cells
from pp_eval.finance_gateway import FinanceGateway, ROUTES, audit_receipts
from pp_eval.finance_workflow_private import materialize_compiler_data_room, run_task_quality


SCHEMA = "proofpress/finance-e2e-v2/executor-qualification/v1"
MIN_FREE_BYTES = 20 * 1024**3
CANARY_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["role", "safe_to_continue"],
    "properties": {"role": {"type": "string"},
                   "safe_to_continue": {"type": "boolean"}},
}
EXECUTOR_CANARY_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["adapter", "safe_to_continue"],
    "properties": {"adapter": {"type": "string"},
                   "safe_to_continue": {"type": "boolean"}},
}


def _read_env_value(path: Path, key: str) -> str:
    for line in path.read_text().splitlines():
        if line.startswith(key + "="):
            return line.split("=", 1)[1].strip().strip("'\"")
    raise RuntimeError(f"{key} is missing from the selected env file")


def run_upstream_canary(repo: Path, output: Path, env_file: Path,
                        roles: list[str]) -> dict:
    output.mkdir(parents=True, exist_ok=False)
    api_key = _read_env_value(env_file, "AI_GATEWAY_API_KEY")
    cells = []
    for role in roles:
        if role not in ROUTES:
            raise ValueError(f"unknown upstream role: {role}")
        route = ROUTES[role]
        gateway = FinanceGateway(repo=repo, route=route, output=output / role,
                                 api_key=api_key)
        semantic_ok = False
        error_type = None
        try:
            value = gateway.call(
                system="Return only the schema-bound transport canary. No task data.",
                prompt=f"Set role exactly to {role} and safe_to_continue to true.",
                schema=CANARY_SCHEMA, schema_name="finance_route_canary", max_tokens=256)
            semantic_ok = value == {"role": role, "safe_to_continue": True}
        except Exception as error:
            error_type = type(error).__name__
        finally:
            gateway.stop()
        receipt_audit = audit_receipts(gateway.rows(), route, 1)
        cells.append({
            "role": role, "route": route,
            "semantic_status": "pass" if semantic_ok else "inconclusive",
            "error_type": error_type, "receipt_audit": receipt_audit,
            "decision": "allow" if semantic_ok and receipt_audit["decision"] == "allow" else "block",
        })
    report = {
        "schema_version": "proofpress/finance-upstream-route-canary/v1",
        "boundary": "Transport and schema qualification only; zero treatment, calibration, grader, or formal artifacts.",
        "formal_denominator": 0, "calibration_denominator": 0,
        "cells": cells,
        "decision": "allow" if cells and all(row["decision"] == "allow" for row in cells) else "block",
        "known_cost_usd": sum(row["receipt_audit"]["known_cost_usd"] for row in cells),
    }
    write_json(output / "report.json", report)
    return report


def run_executor_canary(repo: Path, output: Path, env_file: Path,
                        model: str, provider: str) -> dict:
    """Task-free fixed-route canary before an expensive executor qualification."""
    output.mkdir(parents=True, exist_ok=False)
    route = {"model": model, "provider": provider, "reasoning": "none"}
    gateway = FinanceGateway(
        repo=repo, route=route, output=output,
        api_key=_read_env_value(env_file, "AI_GATEWAY_API_KEY"))
    semantic_ok = False
    error_type = None
    try:
        value = gateway.call(
            system="Return only the schema-bound adapter canary. No task data.",
            prompt="Set adapter exactly to apex_ib and safe_to_continue to true.",
            schema=EXECUTOR_CANARY_SCHEMA,
            schema_name="finance_executor_adapter_canary", max_tokens=256)
        semantic_ok = value == {"adapter": "apex_ib", "safe_to_continue": True}
    except Exception as error:
        error_type = type(error).__name__
    finally:
        gateway.stop()
    receipt_audit = audit_receipts(gateway.rows(), route, 1)
    report = {
        "schema_version": "proofpress/finance-executor-adapter-canary/v1",
        "boundary": "Task-free route qualification; zero executor, grader, calibration, or formal artifacts.",
        "route": route,
        "semantic_status": "pass" if semantic_ok else "inconclusive",
        "error_type": error_type,
        "receipt_audit": receipt_audit,
        "decision": "allow" if semantic_ok and receipt_audit["decision"] == "allow" else "block",
        "executor_qualification_denominator": 0,
        "calibration_denominator": 0,
        "formal_denominator": 0,
    }
    write_json(output / "report.json", report)
    return report


def _valid_required_outputs(run_dir: Path, task_id: str) -> bool:
    package = run_dir / "output" / "neutral_final.zip"
    if not package.is_file():
        return False
    with zipfile.ZipFile(package) as archive:
        names = set(archive.namelist())
    return all(member in names for member in TASK_SPECS[task_id].final_artifact_allowlist)


def normalized_cell(result: dict) -> dict:
    telemetry = result.get("telemetry") or {}
    completed = result.get("status") == "completed"
    run_dir = Path(result["run_dir"])
    log_path = run_dir / "launcher.log"
    log = log_path.read_text(errors="replace") if log_path.is_file() else ""
    upstream_durations = [float(value) for value in
                          re.findall(r"time taken=([0-9]+(?:\.[0-9]+)?) seconds", log)]
    host_suspend = any(value > 720 for value in upstream_durations)
    if host_suspend:
        failure_kind = "host_suspend_or_clock_gap"
    elif result.get("watchdog_timeout"):
        failure_kind = "watchdog"
    elif not completed and "after 2 attempts" in log and "Connection error" in log:
        failure_kind = "transport"
    elif not completed and ("maximum number of steps" in log.casefold()
                            or "60/60" in log):
        failure_kind = "step_cap"
    elif not completed and telemetry.get("calls", 0) > 0:
        failure_kind = "model_error"
    elif not completed:
        failure_kind = "infrastructure"
    else:
        failure_kind = None
    return {
        "run_id": result["run_id"],
        "model": result.get("agent_model"),
        "provider": telemetry.get("providers", []),
        "terminal_telemetry_complete": telemetry.get("status") == "complete",
        "workbook_finalized": completed,
        "required_outputs_valid": completed and _valid_required_outputs(
            run_dir, result["task_id"]),
        "failure_kind": failure_kind,
        "infrastructure_invalid": host_suspend,
        "unauthorized_source_access": False,
        "elapsed_seconds": result.get("elapsed_seconds"),
        "calls": telemetry.get("calls"),
        "tokens": telemetry.get("total_tokens"),
        "known_cost_usd": telemetry.get("known_cost_usd"),
        "no_fallback_observed": telemetry.get("no_fallback_observed"),
        "manifest": str(run_dir / "manifest.json"),
    }


def host_gate(checkout: Path) -> dict:
    docker = Path("/Applications/Docker.app/Contents/Resources/bin/docker")
    free = shutil.disk_usage(checkout).free
    import subprocess
    info = subprocess.run([str(docker), "info"], capture_output=True, check=False)
    image = subprocess.run(
        [str(docker), "image", "inspect", ENVIRONMENT_IMAGE],
        capture_output=True, check=False,
    )
    return {
        "free_bytes": free,
        "required_free_bytes": MIN_FREE_BYTES,
        "docker_healthy": info.returncode == 0,
        "environment_image_present": image.returncode == 0,
        "decision": "allow" if (free >= MIN_FREE_BYTES and info.returncode == 0
                                  and image.returncode == 0) else "block",
    }


def _zip_member_digest(path: Path, member: str) -> str:
    with zipfile.ZipFile(path) as archive:
        return hashlib.sha256(archive.read(member)).hexdigest()


def run_calibration_pair_v2(checkout: Path, results_root: Path, env_file: Path,
                            world_zip: Path, overlay: Path, *, seed: int = 20260829,
                            executor_model: str = "openai/gpt-5.6-luna",
                            executor_provider: str = "openai") -> dict:
    """Run and independently release-audit one v2 Normal/Proofpress pair."""
    results_root.mkdir(parents=True, exist_ok=False)
    preflight = host_preflight(checkout, world_zip, formal=False)
    report = {
        "schema_version": "proofpress/finance-e2e-v2/calibration/v1",
        "task_id": QUALIFICATION_TASK_ID, "executor_model": executor_model,
        "executor_provider": executor_provider, "formal_denominator": 0,
        "calibration_scheduled_artifacts": 2, "calibration_valid_artifacts": 0,
        "preflight": preflight, "cells": [], "status": "preflight_blocked",
    }
    write_json(results_root / "report.json", report)
    gate_path = overlay / "filesystem" / "Governed" / "execution_receipt.json"
    if preflight.get("status") != "passed" or not gate_path.is_file():
        return report
    governed_gate = json.loads(gate_path.read_text())
    if governed_gate.get("decision") != "allow":
        report["status"] = "governed_overlay_blocked"
        write_json(results_root / "report.json", report)
        return report
    order = ["normal", "proofpress"]
    random.Random(seed).shuffle(order)
    report["status"] = "running"
    report["arm_order"] = order
    write_json(results_root / "report.json", report)
    for arm in order:
        report["active_cell"] = {"arm": arm, "state": "executor_running"}
        write_json(results_root / "report.json", report)
        cell = run_apex_stage(
            checkout, results_root, QUALIFICATION_TASK_ID, f"v2-calibration-{arm}",
            overlay=overlay if arm == "proofpress" else None,
            instruction=("Complete the public task using only the mounted governed working set and "
                         "permitted extracts. Verify source-bound inputs; do not copy governance "
                         "sidecars into the client deliverable.") if arm == "proofpress" else "",
            bounded_world=arm == "proofpress", env_file=env_file,
            agent_model=executor_model,
        )
        cell_record = {"arm": arm, "result": cell}
        if cell.get("status") == "completed":
            grades = repeat_native_grading(checkout, Path(cell["run_dir"]), env_file=env_file)
            cell_record["grading_repetitions"] = grades
            cell_record["initial_target_sha256"] = _zip_member_digest(
                Path(cell["run_dir"]) / "output" / "neutral_initial.zip", MERGER_MODEL)
            cell_record["compaction"] = compact_apex_output(
                Path(cell["run_dir"]) / "output", preserve_final_tar=False)
        report["cells"].append(cell_record)
        report.pop("active_cell", None)
        write_json(results_root / "report.json", report)
    valid = [row for row in report["cells"] if row["result"].get("status") == "completed"]
    report["calibration_valid_artifacts"] = len(valid)
    target_digests = {row.get("initial_target_sha256") for row in valid}
    executor_routes_ok = all(
        row["result"].get("agent_model") == executor_model
        and row["result"].get("executor_model") == executor_model
        and row["result"].get("telemetry", {}).get("providers") == [executor_provider]
        and row["result"].get("telemetry", {}).get("no_fallback_observed") is True
        for row in valid)
    grading_ok = all(
        row.get("grading_repetitions", {}).get("status") == "completed"
        and len(row.get("grading_repetitions", {}).get("records", [])) == 3
        and all(rep.get("telemetry", {}).get("no_fallback_observed") is True
                for rep in row["grading_repetitions"]["records"])
        for row in valid)
    isolation_ok = ({row["arm"]: row["result"].get("bounded_world") for row in valid}
                    == {"normal": False, "proofpress": True})
    release = {
        "two_valid_artifacts": len(valid) == 2,
        "byte_identical_pristine_target": len(target_digests) == 1 and len(valid) == 2,
        "executor_route_exact": executor_routes_ok and len(valid) == 2,
        "three_complete_blinded_grades_per_artifact": grading_ok and len(valid) == 2,
        "arm_access_isolation": isolation_ok,
    }
    release["decision"] = "allow" if all(release.values()) else "block"
    release["audit_digest"] = "sha256:" + hashlib.sha256(
        json.dumps(release, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    report["release_audit"] = release
    report["status"] = "completed" if release["decision"] == "allow" else "incomplete"
    write_json(results_root / "report.json", report)
    return report


def run_formal_matrix_v2(checkout: Path, results_root: Path, env_file: Path,
                         world_zip: Path, task_freeze: Path, calibration_report: Path,
                         overlays: dict[str, Path], *, seed: int = 20260829,
                         executor_model: str = "openai/gpt-5.6-luna",
                         executor_provider: str = "openai") -> dict:
    """Execute the frozen Finance v2 2-task × 2-arm × 3-attempt matrix serially."""
    results_root.mkdir(parents=True, exist_ok=False)
    freeze = json.loads(task_freeze.read_text())
    calibration = json.loads(calibration_report.read_text())
    preflight = host_preflight(checkout, world_zip, formal=True)
    selected = [row["task_id"] for row in freeze.get("selected_tasks", [])]
    expected = list(FINANCE_E2E_V2_FORMAL_TASK_IDS)
    schedule = []
    randomizer = random.Random(seed)
    for task_id in expected:
        for attempt in range(1, 4):
            order = ["normal", "proofpress"]
            randomizer.shuffle(order)
            schedule.append({"task_id": task_id, "attempt": attempt, "arm_order": order})
    overlay_receipts = {}
    for task_id, path in overlays.items():
        gate_path = path / "filesystem" / "Governed" / "execution_receipt.json"
        package_path = path / "package_manifest.json"
        overlay_receipts[task_id] = {
            "path": str(path),
            "gate": json.loads(gate_path.read_text()) if gate_path.is_file() else None,
            "package": json.loads(package_path.read_text()) if package_path.is_file() else None,
        }
    protocol = {
        "schema_version": "proofpress/finance-e2e-v2/formal-protocol/v1",
        "world_id": freeze.get("world_id"),
        "world_sha256": preflight.get("world_zip_sha256"),
        "task_freeze_digest": freeze.get("freeze_digest"),
        "calibration_release_audit_digest": calibration.get("release_audit", {}).get("audit_digest"),
        "executor_model": executor_model, "executor_provider": executor_provider,
        "judge_model": JUDGE_MODEL, "fallback": "forbidden",
        "tasks": freeze.get("selected_tasks"), "schedule": schedule,
        "scheduled_executor_cells": 12, "grader_repetitions_per_valid_artifact": 3,
        "seed": seed, "serial": True, "official_apex_score_claim": False,
    }
    protocol["protocol_digest"] = "sha256:" + hashlib.sha256(
        json.dumps(protocol, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    write_json(results_root / "frozen_protocol.json", protocol)
    release_inputs_ok = (
        freeze.get("formal_tasks_frozen") is True
        and selected == expected
        and freeze.get("scheduled_executor_cells") == 12
        and freeze.get("executor_model") == executor_model
        and calibration.get("release_audit", {}).get("decision") == "allow"
        and calibration.get("status") == "completed"
        and preflight.get("status") == "passed"
        and set(overlays) == set(expected)
        and all(row.get("gate", {}).get("decision") == "allow"
                and row.get("package", {}).get("task_id") == task_id
                for task_id, row in overlay_receipts.items())
    )
    report = {
        "schema_version": "proofpress/finance-e2e-v2/formal-report/v1",
        "status": "running" if release_inputs_ok else "release_blocked",
        "protocol_digest": protocol["protocol_digest"], "preflight": preflight,
        "overlay_receipts": overlay_receipts, "cells": [],
        "summary": summarize_formal_cells([], 12),
    }
    write_json(results_root / "report.json", report)
    if not release_inputs_ok:
        return report
    for block in schedule:
        for arm in block["arm_order"]:
            result = run_apex_stage(
                checkout, results_root, block["task_id"],
                f"v2-formal-a{block['attempt']}-{arm}",
                overlay=overlays[block["task_id"]] if arm == "proofpress" else None,
                instruction=("Complete the public task using only the mounted governed working set and "
                             "permitted extracts. Verify source-bound inputs; do not copy governance "
                             "sidecars into the client deliverable.") if arm == "proofpress" else "",
                bounded_world=arm == "proofpress", env_file=env_file,
                agent_model=executor_model,
            )
            cell = {"task_id": block["task_id"], "attempt": block["attempt"],
                    "arm": arm, "result": result}
            if result.get("status") == "completed":
                grading = repeat_native_grading(checkout, Path(result["run_dir"]), env_file=env_file)
                cell["grading_repetitions"] = grading
                if grading.get("status") == "completed":
                    cell["majority_result"] = majority_native_result(Path(result["run_dir"]))
            cell["compaction"] = compact_apex_output(
                Path(result["run_dir"]) / "output",
                preserve_final_tar=result.get("status") != "completed")
            report["cells"].append(cell)
            report["summary"] = summarize_formal_cells(report["cells"], 12)
            write_json(results_root / "report.json", report)
    report["status"] = "schedule_completed"
    report["outcome_class"] = (
        "complete_matrix" if report["summary"]["majority_graded_artifacts"] == 12
        else "bounded_incomplete")
    write_json(results_root / "report.json", report)
    return report


def run_executor_qualification(checkout: Path, results_root: Path,
                               env_file: Path, attempts: int = 6,
                               executor_model: str = EXECUTOR_MODEL,
                               executor_provider: str | None = None) -> dict:
    results_root.mkdir(parents=True, exist_ok=False)
    gate = host_gate(checkout)
    report = {
        "schema_version": SCHEMA,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "running" if gate["decision"] == "allow" else "blocked",
        "formal_denominator": 0,
        "calibration_denominator": 0,
        "task_id": QUALIFICATION_TASK_ID,
        "executor_model": executor_model,
        "executor_provider": executor_provider,
        "scheduled_cells": attempts,
        "host_gate": gate,
        "cells": [],
    }
    write_json(results_root / "report.json", report)
    if gate["decision"] != "allow":
        return report

    keep_awake = subprocess.Popen(
        ["/usr/bin/caffeinate", "-dimsu", "-w", str(os.getpid())],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    report["caffeinate_pid"] = keep_awake.pid
    write_json(results_root / "report.json", report)
    try:
        for attempt in range(1, attempts + 1):
            result = run_apex_stage(
                checkout, results_root, QUALIFICATION_TASK_ID,
                f"executor-qualification-a{attempt}",
                bounded_world=False, skip_grading=True, env_file=env_file,
                agent_model=executor_model,
            )
            cell = normalized_cell(result)
            output = Path(result["run_dir"]) / "output"
            if output.is_dir():
                cell["compaction"] = compact_apex_output(
                    output, preserve_final_tar=False)
            report["cells"].append(cell)
            report["completed_cells"] = len(report["cells"])
            report["updated_at"] = datetime.now(timezone.utc).isoformat()
            write_json(results_root / "report.json", report)
            if (results_root / "STOP_AFTER_CURRENT_CELL").is_file():
                report["status"] = "stopped_after_current_cell"
                report["stop_reason"] = "operator_stop_sentinel"
                report["updated_at"] = datetime.now(timezone.utc).isoformat()
                write_json(results_root / "report.json", report)
                return report
    finally:
        if keep_awake.poll() is None:
            keep_awake.terminate()

    report["qualification"] = executor_qualification(
        report["cells"], required=attempts,
        minimum_completed=5 if attempts == 6 else attempts,
        maximum_transport_failures=1 if attempts == 6 else 0,
        expected_model=executor_model,
        expected_provider=executor_provider,
    )
    report["status"] = "completed"
    report["updated_at"] = datetime.now(timezone.utc).isoformat()
    write_json(results_root / "report.json", report)
    return report


def audit_executor_qualification(results_root: Path, output: Path) -> dict:
    original = results_root / "report.json"
    original_bytes = original.read_bytes()
    source = json.loads(original_bytes)
    audited = []
    for cell in source.get("cells", []):
        manifest_path = Path(cell["manifest"])
        manifest = json.loads(manifest_path.read_text())
        result = dict(manifest)
        result["run_dir"] = str(manifest_path.parent)
        result["agent_model"] = manifest.get("agent_model")
        audited.append(normalized_cell(result))
    infrastructure_invalid = sum(row.get("infrastructure_invalid") is True for row in audited)
    required = source.get("scheduled_cells", 6)
    qualification = None
    if len(audited) == required and not infrastructure_invalid:
        qualification = executor_qualification(
            audited, required=required,
            minimum_completed=5 if required == 6 else required,
            maximum_transport_failures=1 if required == 6 else 0,
            expected_model=source.get("executor_model"),
            expected_provider=source.get("executor_provider"),
        )
    report = {
        "schema_version": "proofpress/finance-executor-qualification-audit/v1",
        "source_report_sha256": "sha256:" + hashlib.sha256(original_bytes).hexdigest(),
        "source_status": source.get("status"),
        "scheduled_cells": source.get("scheduled_cells"),
        "persisted_cells": len(audited),
        "cells": audited,
        "infrastructure_invalid_cells": infrastructure_invalid,
        "qualification": qualification,
        "qualification_decision": (
            "invalid_root" if infrastructure_invalid else
            qualification["decision"] if qualification is not None else
            "not_yet_qualified"
        ),
        "formal_denominator": 0, "calibration_denominator": 0,
    }
    report["audit_digest"] = "sha256:" + hashlib.sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    output.parent.mkdir(parents=True, exist_ok=True)
    write_json(output, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    qualify = sub.add_parser("executor-qualification")
    qualify.add_argument("--checkout", required=True, type=Path)
    qualify.add_argument("--results-root", required=True, type=Path)
    qualify.add_argument("--env-file", required=True, type=Path)
    qualify.add_argument("--attempts", type=int, default=6)
    qualify.add_argument("--executor-model", default=EXECUTOR_MODEL)
    qualify.add_argument("--executor-provider")
    executor_canary = sub.add_parser("executor-canary")
    executor_canary.add_argument("--repo", required=True, type=Path)
    executor_canary.add_argument("--output", required=True, type=Path)
    executor_canary.add_argument("--env-file", required=True, type=Path)
    executor_canary.add_argument("--executor-model", required=True)
    executor_canary.add_argument("--executor-provider", required=True)
    legacy = sub.add_parser("legacy-gap-diagnostic")
    legacy.add_argument("--working-set", action="append", required=True, type=Path)
    legacy.add_argument("--output", required=True, type=Path)
    canary = sub.add_parser("upstream-canary")
    canary.add_argument("--repo", required=True, type=Path)
    canary.add_argument("--output", required=True, type=Path)
    canary.add_argument("--env-file", required=True, type=Path)
    canary.add_argument("--roles", default=",".join(ROUTES))
    task_quality = sub.add_parser("upstream-task-quality")
    task_quality.add_argument("--repo", required=True, type=Path)
    task_quality.add_argument("--evidence-root", required=True, type=Path)
    task_quality.add_argument("--output", required=True, type=Path)
    task_quality.add_argument("--env-file", required=True, type=Path)
    task_quality.add_argument("--task-id", required=True)
    compiler = sub.add_parser("compiler-data-room")
    compiler.add_argument("--tasks-json", required=True, type=Path)
    compiler.add_argument("--world-zip", required=True, type=Path)
    compiler.add_argument("--output", required=True, type=Path)
    compiler.add_argument("--task-id", required=True)
    audit = sub.add_parser("audit-executor-qualification")
    audit.add_argument("--results-root", required=True, type=Path)
    audit.add_argument("--output", required=True, type=Path)
    freshness = sub.add_parser("fresh-task-audit")
    freshness.add_argument("--tasks-json", required=True, type=Path)
    freshness.add_argument("--world-id", required=True)
    freshness.add_argument("--manifest-root", action="append", required=True, type=Path)
    freshness.add_argument("--executor-model", default=EXECUTOR_MODEL)
    freshness.add_argument("--output", required=True, type=Path)
    freeze = sub.add_parser("freeze-formal-tasks")
    freeze.add_argument("--freshness-report", required=True, type=Path)
    freeze.add_argument("--output", required=True, type=Path)
    calibration = sub.add_parser("calibration")
    calibration.add_argument("--checkout", required=True, type=Path)
    calibration.add_argument("--results-root", required=True, type=Path)
    calibration.add_argument("--env-file", required=True, type=Path)
    calibration.add_argument("--world-zip", required=True, type=Path)
    calibration.add_argument("--overlay", required=True, type=Path)
    calibration.add_argument("--executor-model", default="openai/gpt-5.6-luna")
    calibration.add_argument("--executor-provider", default="openai")
    formal = sub.add_parser("formal")
    formal.add_argument("--checkout", required=True, type=Path)
    formal.add_argument("--results-root", required=True, type=Path)
    formal.add_argument("--env-file", required=True, type=Path)
    formal.add_argument("--world-zip", required=True, type=Path)
    formal.add_argument("--task-freeze", required=True, type=Path)
    formal.add_argument("--calibration-report", required=True, type=Path)
    formal.add_argument("--overlay", action="append", required=True)
    formal.add_argument("--executor-model", default="openai/gpt-5.6-luna")
    formal.add_argument("--executor-provider", default="openai")
    args = parser.parse_args()
    if args.command == "executor-qualification":
        report = run_executor_qualification(
            args.checkout, args.results_root, args.env_file, args.attempts,
            args.executor_model, args.executor_provider)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report.get("status") != "blocked" else 2
    if args.command == "executor-canary":
        report = run_executor_canary(
            args.repo, args.output, args.env_file,
            args.executor_model, args.executor_provider)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["decision"] == "allow" else 2
    if args.command == "legacy-gap-diagnostic":
        rows = []
        for path in args.working_set:
            value = json.loads(path.read_text())
            rows.append(legacy_working_set_preflight(value))
        report = {
            "schema_version": "proofpress/finance-e2e-v2/legacy-gap-diagnostic/v1",
            "boundary": "Development-only diagnostic; no v2 executor, grader, calibration, or formal artifact.",
            "working_set_count": len(rows),
            "formal_denominator": 0,
            "calibration_denominator": 0,
            "results": rows,
            "decision": "block" if any(row["decision"] == "block" for row in rows) else "allow",
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        write_json(args.output, report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    if args.command == "upstream-canary":
        report = run_upstream_canary(
            args.repo, args.output, args.env_file,
            [value.strip() for value in args.roles.split(",") if value.strip()])
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["decision"] == "allow" else 2
    if args.command == "upstream-task-quality":
        report = run_task_quality(
            repo=args.repo, evidence_root=args.evidence_root, output=args.output,
            api_key=_read_env_value(args.env_file, "AI_GATEWAY_API_KEY"),
            task_id=args.task_id,
            target_artifacts=list(TASK_SPECS[args.task_id].final_artifact_allowlist))
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["decision"] == "allow" else 2
    if args.command == "compiler-data-room":
        public_task = load_public_task(args.tasks_json, args.task_id)
        report = materialize_compiler_data_room(
            world_zip=args.world_zip, destination=args.output,
            public_task=public_task)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    if args.command == "audit-executor-qualification":
        report = audit_executor_qualification(args.results_root, args.output)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    if args.command == "fresh-task-audit":
        report = fresh_task_audit(
            task_rows=json.loads(args.tasks_json.read_text()), world_id=args.world_id,
            manifest_roots=args.manifest_root, executor_model=args.executor_model)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        write_json(args.output, report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    if args.command == "freeze-formal-tasks":
        report = freeze_formal_tasks(
            freshness=json.loads(args.freshness_report.read_text()),
            task_ids=list(FINANCE_E2E_V2_FORMAL_TASK_IDS),
            prior_executor_caveats={
                FINANCE_E2E_V2_FORMAL_TASK_IDS[0]:
                    "Observed in PR #54 only under inclusionai/ling-3.0-flash-fin; not consumed by the selected Luna executor and not used to tune the v2 governed route."
            },
        )
        args.output.mkdir(parents=True, exist_ok=False)
        write_json(args.output / "formal-task-freeze.json", report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    if args.command == "calibration":
        report = run_calibration_pair_v2(
            args.checkout, args.results_root, args.env_file, args.world_zip, args.overlay,
            executor_model=args.executor_model, executor_provider=args.executor_provider)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report.get("status") == "completed" else 2
    if args.command == "formal":
        overlays = {}
        for value in args.overlay:
            task_id, separator, path = value.partition("=")
            if not separator or not task_id or not path or task_id in overlays:
                raise ValueError("--overlay must be unique task_id=/absolute/path")
            overlays[task_id] = Path(path)
        report = run_formal_matrix_v2(
            args.checkout, args.results_root, args.env_file, args.world_zip,
            args.task_freeze, args.calibration_report, overlays,
            executor_model=args.executor_model, executor_provider=args.executor_provider)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report.get("status") == "schedule_completed" else 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

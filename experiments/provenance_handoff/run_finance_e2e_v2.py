#!/usr/bin/env python3
"""Private-run entrypoint for Finance evidence-first E2E v2 qualification."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import zipfile
import hashlib

from pp_eval.apex_ib_pr36 import (
    ENVIRONMENT_IMAGE,
    EXECUTOR_MODEL,
    QUALIFICATION_TASK_ID,
    TASK_SPECS,
    compact_apex_output,
    run_apex_stage,
    write_json,
)
from pp_eval.finance_e2e_v2 import executor_qualification, fresh_task_audit, legacy_working_set_preflight
from pp_eval.finance_gateway import FinanceGateway, ROUTES, audit_receipts
from pp_eval.finance_workflow_private import run_task_quality


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
    audit = sub.add_parser("audit-executor-qualification")
    audit.add_argument("--results-root", required=True, type=Path)
    audit.add_argument("--output", required=True, type=Path)
    freshness = sub.add_parser("fresh-task-audit")
    freshness.add_argument("--tasks-json", required=True, type=Path)
    freshness.add_argument("--world-id", required=True)
    freshness.add_argument("--manifest-root", action="append", required=True, type=Path)
    freshness.add_argument("--executor-model", default=EXECUTOR_MODEL)
    freshness.add_argument("--output", required=True, type=Path)
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
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

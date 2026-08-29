#!/usr/bin/env python3
"""Private-run entrypoint for Finance evidence-first E2E v2 qualification."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import zipfile

from pp_eval.apex_ib_pr36 import (
    ENVIRONMENT_IMAGE,
    EXECUTOR_MODEL,
    QUALIFICATION_TASK_ID,
    TASK_SPECS,
    compact_apex_output,
    run_apex_stage,
    write_json,
)
from pp_eval.finance_e2e_v2 import executor_qualification, legacy_working_set_preflight


SCHEMA = "proofpress/finance-e2e-v2/executor-qualification/v1"
MIN_FREE_BYTES = 20 * 1024**3


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
    if result.get("watchdog_timeout"):
        failure_kind = "watchdog"
    elif not completed and telemetry.get("calls", 0) > 0:
        failure_kind = "model_or_transport"
    elif not completed:
        failure_kind = "infrastructure"
    else:
        failure_kind = None
    run_dir = Path(result["run_dir"])
    return {
        "run_id": result["run_id"],
        "model": result.get("agent_model"),
        "provider": telemetry.get("providers", []),
        "terminal_telemetry_complete": telemetry.get("status") == "complete",
        "workbook_finalized": completed,
        "required_outputs_valid": completed and _valid_required_outputs(
            run_dir, result["task_id"]),
        "failure_kind": failure_kind,
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
                               env_file: Path, attempts: int = 6) -> dict:
    results_root.mkdir(parents=True, exist_ok=False)
    gate = host_gate(checkout)
    report = {
        "schema_version": SCHEMA,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "running" if gate["decision"] == "allow" else "blocked",
        "formal_denominator": 0,
        "calibration_denominator": 0,
        "task_id": QUALIFICATION_TASK_ID,
        "executor_model": EXECUTOR_MODEL,
        "scheduled_cells": attempts,
        "host_gate": gate,
        "cells": [],
    }
    write_json(results_root / "report.json", report)
    if gate["decision"] != "allow":
        return report

    for attempt in range(1, attempts + 1):
        result = run_apex_stage(
            checkout, results_root, QUALIFICATION_TASK_ID,
            f"executor-qualification-a{attempt}",
            bounded_world=False, skip_grading=True, env_file=env_file,
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

    decision_input = []
    for cell in report["cells"]:
        value = dict(cell)
        if value.get("failure_kind") == "model_or_transport":
            value["failure_kind"] = "transport"
        decision_input.append(value)
    report["qualification"] = executor_qualification(
        decision_input, required=attempts,
        minimum_completed=5 if attempts == 6 else attempts,
        maximum_transport_failures=1 if attempts == 6 else 0,
    )
    report["status"] = "completed"
    report["updated_at"] = datetime.now(timezone.utc).isoformat()
    write_json(results_root / "report.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    qualify = sub.add_parser("executor-qualification")
    qualify.add_argument("--checkout", required=True, type=Path)
    qualify.add_argument("--results-root", required=True, type=Path)
    qualify.add_argument("--env-file", required=True, type=Path)
    qualify.add_argument("--attempts", type=int, default=6)
    legacy = sub.add_parser("legacy-gap-diagnostic")
    legacy.add_argument("--working-set", action="append", required=True, type=Path)
    legacy.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.command == "executor-qualification":
        report = run_executor_qualification(
            args.checkout, args.results_root, args.env_file, args.attempts)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report.get("status") != "blocked" else 2
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
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

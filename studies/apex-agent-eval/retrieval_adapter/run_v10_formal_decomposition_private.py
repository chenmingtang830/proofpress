#!/usr/bin/env python3
"""Run the frozen Qwen v10 decomposition on the twelve-task formal panel."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from typing import Any

from governed_workflow_contract import digest, validate_profile
from run_claim_construction_private import Gateway, SectionIndex
from run_model_routing_qualification_private import terminal_telemetry
from run_v10_decomposition_matrix_private import call_decomposer
from run_v10_role_matrix_private import MODELS

SCHEMA = "proofpress/v10-formal-decomposition/v1"
MODEL_LABEL = "qwen"
TASK_COUNT = 12
PARALLELISM = 4


def tasks_from_manifest(value: Any) -> list[dict[str, Any]]:
    rows = value.get("tasks", value) if isinstance(value, dict) else value
    if not isinstance(rows, list):
        raise ValueError("task manifest must be an array")
    tasks = [row for row in rows if isinstance(row, dict) and row.get("task_id") and row.get("prompt")]
    if len(tasks) != TASK_COUNT or len({row["task_id"] for row in tasks}) != TASK_COUNT:
        raise ValueError("formal decomposition requires twelve unique tasks")
    return sorted(tasks, key=lambda row: row["task_id"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks-json", required=True)
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--gateway-server", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--budget-usd", type=float, default=6.0)
    parser.add_argument("--timeout", type=float, default=180)
    args = parser.parse_args()
    tasks = tasks_from_manifest(json.loads(Path(args.tasks_json).read_text()))
    catalog = json.loads(Path(args.catalog).read_text())
    profile = validate_profile(json.loads(Path(args.profile).read_text()))
    inventory = SectionIndex(catalog).inventory()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw = out / "raw"; raw.mkdir(exist_ok=True); raw.chmod(0o700)
    route = MODELS[MODEL_LABEL]
    gateways = {f"decomposer_{index}": Gateway(
        args.gateway_server, route["model"], route["provider"], out,
        args.timeout, route["reasoning"], structured_output=True,
    ) for index in range(PARALLELISM)}

    def run_shard(index: int) -> list[dict[str, Any]]:
        gateway = gateways[f"decomposer_{index}"]
        summaries = []
        for task in tasks[index::PARALLELISM]:
            requirements, status = call_decomposer(gateway, task, inventory, profile)
            private = {"schema_version": SCHEMA, "task_id": task["task_id"],
                       "requirements": requirements, "status": status,
                       "config_digest": digest({"route": route, "profile": profile["profile_digest"],
                                                "inventory": digest(inventory)})}
            target = raw / f'{task["task_id"]}.json'
            target.write_text(json.dumps(private, indent=2, sort_keys=True) + "\n"); target.chmod(0o600)
            summaries.append({"task_id": task["task_id"], "status": status["status"],
                              "requirement_count": len(requirements),
                              "artifact_digest": digest(private)})
        return summaries

    try:
        with ThreadPoolExecutor(max_workers=PARALLELISM) as pool:
            results = [row for shard in pool.map(run_shard, range(PARALLELISM)) for row in shard]
    finally:
        for gateway in gateways.values(): gateway.stop()
    results.sort(key=lambda row: row["task_id"])
    telemetry = terminal_telemetry(gateways)
    if telemetry["known_cost_usd"] > args.budget_usd:
        raise RuntimeError("formal decomposition exceeded hard budget")
    completed = [row for row in results if row["status"] == "ok"]
    report = {"schema_version": SCHEMA,
              "boundary": "Twelve-task formal decomposition. Task prompts, inventory, and legal profile enter generation; rubric, gold, silver, and answers do not.",
              "route": route, "profile_digest": profile["profile_digest"],
              "catalog_digest": digest(catalog), "task_manifest_digest": digest(tasks),
              "tasks": results,
              "denominators": {"tasks": len(results), "completed_tasks": len(completed),
                               "requirements": sum(row["requirement_count"] for row in completed)},
              "telemetry": {**telemetry, "budget_usd": args.budget_usd},
              "qualification": {"status": "pass" if len(completed) == TASK_COUNT and not telemetry["missing_cost_calls"] else "inconclusive"},
              "raw_private_dir": str(raw)}
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["qualification"]["status"],
                      "requirements": report["denominators"]["requirements"],
                      "cost_usd": telemetry["known_cost_usd"]}, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Assign legal-profile requirement types to frozen PR36-v7 requirements."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from governed_workflow_contract import digest
from run_claim_construction_private import Gateway, _model_call
from run_model_routing_qualification_private import terminal_telemetry
from run_v10_role_matrix_private import MODELS

SCHEMA = "proofpress/v7-requirement-type-adapter/v1"
TYPES = ("factual_input", "risk_signal", "contract_allocation", "quantitative_term",
         "obligation", "condition", "exception", "conflict", "domain_analysis", "missing_input")
OUTPUT = {"type": "object", "additionalProperties": False, "required": ["assignments"],
          "properties": {"assignments": {"type": "array", "maxItems": 40, "items": {
              "type": "object", "additionalProperties": False,
              "required": ["requirement_id", "requirement_type"],
              "properties": {"requirement_id": {"type": "string", "maxLength": 128},
                             "requirement_type": {"type": "string", "enum": list(TYPES)}}}}}}


def apply_assignments(requirements: list[dict[str, Any]], value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict) and isinstance(value.get("output"), dict):
        value = value["output"]
    rows = value.get("assignments", []) if isinstance(value, dict) else []
    expected = {row["requirement_id"] for row in requirements}
    assignments: dict[str, str] = {}
    for row in rows:
        requirement_id = str(row.get("requirement_id", ""))
        requirement_type = row.get("requirement_type")
        if requirement_id not in expected or requirement_id in assignments or requirement_type not in TYPES:
            raise ValueError("invalid requirement type assignment")
        assignments[requirement_id] = requirement_type
    if set(assignments) != expected:
        raise ValueError("requirement type assignment coverage is incomplete")
    return [{**row, "type": assignments[row["requirement_id"]]} for row in requirements]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decomposition-raw", required=True)
    parser.add_argument("--gateway-server", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--budget-usd", type=float, default=1.0)
    parser.add_argument("--timeout", type=float, default=240)
    args = parser.parse_args()
    paths = sorted(Path(args.decomposition_raw).glob("*.json"))
    if len(paths) != 4:
        raise SystemExit("v7 requirement type qualification requires four frozen tasks")
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw = out / "raw"; raw.mkdir(exist_ok=True); raw.chmod(0o700)
    route = MODELS["qwen"]
    gateway = Gateway(args.gateway_server, route["model"], route["provider"], out,
                      args.timeout, route["reasoning"], structured_output=True)
    tasks = []
    try:
        for path in paths:
            source = json.loads(path.read_text())
            requirements = source["variants"]["v7"]["requirements"]
            payload = {"requirements": [{key: row.get(key) for key in
                                          ("requirement_id", "requirement", "lifecycle_category", "applicability")}
                                         for row in requirements],
                       "allowed_types": list(TYPES),
                       "instruction": "Assign exactly one requirement_type to every supplied ID. Do not rewrite, add, remove, answer, infer facts, or grant authority."}
            result = _model_call(gateway, "Classify frozen legal requirements by function. Return assignments only.",
                                 json.dumps(payload, ensure_ascii=False), 8000, OUTPUT,
                                 "proofpress_v7_requirement_types", 2)
            if not result["ok"]:
                tasks.append({"task_id": path.stem, "status": "inconclusive",
                              "failure_digest": digest(result["record"])}); continue
            try:
                typed = apply_assignments(requirements, result["value"])
            except ValueError as exc:
                tasks.append({"task_id": path.stem, "status": "schema_failure",
                              "failure_digest": digest(str(exc))}); continue
            private = {"schema_version": SCHEMA, "task_id": path.stem, "requirements": typed,
                       "source_decomposition_digest": digest(source)}
            target = raw / path.name
            target.write_text(json.dumps(private, indent=2, sort_keys=True) + "\n"); target.chmod(0o600)
            tasks.append({"task_id": path.stem, "status": "ok", "requirement_count": len(typed),
                          "type_counts": {kind: sum(row["type"] == kind for row in typed) for kind in TYPES},
                          "artifact_digest": digest(private)})
    finally:
        gateway.stop()
    telemetry = terminal_telemetry({"classifier": gateway})
    report = {"schema_version": SCHEMA,
              "boundary": "Four-task development type-only adapter. Frozen v7 requirement text is unchanged; classifications carry no authority or admission.",
              "route": route, "tasks": tasks,
              "denominators": {"tasks": len(tasks), "completed_tasks": sum(row["status"] == "ok" for row in tasks),
                               "requirements": sum(row.get("requirement_count", 0) for row in tasks)},
              "telemetry": {**telemetry, "budget_usd": args.budget_usd},
              "qualification": {"status": "pass" if all(row["status"] == "ok" for row in tasks)
                                 and not telemetry["missing_cost_calls"] else "inconclusive"},
              "raw_private_dir": str(raw)}
    if telemetry["known_cost_usd"] > args.budget_usd:
        raise RuntimeError("v7 requirement type adapter exceeded hard budget")
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["qualification"]["status"],
                      "cost_usd": telemetry["known_cost_usd"]}, sort_keys=True))


if __name__ == "__main__":
    main()

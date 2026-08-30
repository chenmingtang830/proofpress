#!/usr/bin/env python3
"""Qualify a legal-profile gate that blocks inferred analysis from automatic claim construction."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from governed_workflow_contract import digest
from run_claim_construction_private import Gateway
from run_model_routing_qualification_private import terminal_telemetry
from run_v10_construction_qualification_private import score_requirement_opportunities
from run_v10_role_matrix_private import MODELS
from run_v10_selected_route_private import COVERAGE_MODELS, call_coverage

SCHEMA = "proofpress/v10-legal-profile-filter-qualification/v1"
AUTO_CONSTRUCTION_REQUIREMENT_TYPES = frozenset({
    "factual_input", "quantitative_term", "obligation", "condition", "exception",
    "contract_allocation",
})


def filter_claims(source: dict) -> tuple[list[dict], list[dict]]:
    requirement_types = {row["requirement_id"]: row.get("type") for row in source["requirements"]}
    claims = [row for row in source["claims"]
              if requirement_types.get(row["requirement_id"]) in AUTO_CONSTRUCTION_REQUIREMENT_TYPES]
    verdicts = {row["claim_id"]: row for row in source["verdicts"]}
    supported = [row for row in claims if verdicts.get(row["id"], {}).get("verdict") == "supported"]
    return claims, supported


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-raw", required=True)
    parser.add_argument("--reference-raw", required=True)
    parser.add_argument("--task-source-raw", required=True)
    parser.add_argument("--gateway-server", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--budget-usd", type=float, default=3.0)
    parser.add_argument("--timeout", type=float, default=180)
    args = parser.parse_args()
    paths = sorted(Path(args.candidate_raw).glob("*.json"))
    if len(paths) != 4:
        raise SystemExit("profile filter qualification requires four frozen tasks")
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw_out = out / "raw"; raw_out.mkdir(exist_ok=True); raw_out.chmod(0o700)
    routes = {label: MODELS[label] for label in COVERAGE_MODELS}
    gateways = {label: Gateway(args.gateway_server, route["model"], route["provider"], out,
                               args.timeout, route["reasoning"], structured_output=True)
                for label, route in routes.items()}
    tasks = []
    try:
        for path in paths:
            source = json.loads(path.read_text())
            reference = json.loads((Path(args.reference_raw) / path.name).read_text())["gap_reference"]
            task_source = json.loads((Path(args.task_source_raw) / path.name).read_text())
            claims, supported = filter_claims(source)
            verdicts = {row["claim_id"]: row for row in source["verdicts"]}
            resolutions = {}; statuses = {}; scores = {}
            for label in COVERAGE_MODELS:
                resolutions[label], statuses[label] = call_coverage(
                    gateways[label], task_source["task"]["prompt"], source["requirements"], supported,
                )
                scores[label] = score_requirement_opportunities(
                    reference, resolutions[label], source["atoms"], source["gates"], claims, supported,
                )
            factual = [row for row in claims if row["claim_type"] == "observed_fact"]
            unsupported = [row for row in claims if verdicts.get(row["id"], {}).get("verdict") != "supported"]
            unsupported_factual = [row for row in factual if verdicts.get(row["id"], {}).get("verdict") != "supported"]
            private = {"task_id": source["task_id"], "claim_ids": [row["id"] for row in claims],
                       "supported_claim_ids": [row["id"] for row in supported],
                       "requirement_resolutions": resolutions, "reference_digest": digest(reference)}
            target = raw_out / path.name
            target.write_text(json.dumps(private, indent=2, sort_keys=True) + "\n"); target.chmod(0o600)
            tasks.append({"task_id": source["task_id"],
                          "status": "ok" if all(row["status"] == "ok" for row in statuses.values()) else "inconclusive",
                          "claim_count": len(claims), "unsupported_claim_count": len(unsupported),
                          "factual_claim_count": len(factual),
                          "unsupported_factual_claim_count": len(unsupported_factual),
                          "coverage": scores, "coverage_status": statuses,
                          "artifact_digest": digest({"claim_ids": [row["id"] for row in claims],
                                                     "resolutions": resolutions})})
    finally:
        for gateway in gateways.values(): gateway.stop()
    telemetry = terminal_telemetry(gateways)
    completed = [row for row in tasks if row["status"] == "ok"]
    claims = sum(row["claim_count"] for row in completed)
    factual = sum(row["factual_claim_count"] for row in completed)
    expected_gaps = sum(row["coverage"][COVERAGE_MODELS[0]]["expected_gap_count"] for row in completed) if completed else 0
    metrics = {
        "unsupported_claim_rate": sum(row["unsupported_claim_count"] for row in completed) / claims if claims else None,
        "unsupported_factual_claim_rate": sum(row["unsupported_factual_claim_count"] for row in completed) / factual if factual else None,
        "coverage_models": {},
    }
    for label in COVERAGE_MODELS:
        expected_covered = sum(row["coverage"][label]["expected_covered_count"] for row in completed)
        true_covered = sum(row["coverage"][label]["true_covered_count"] for row in completed)
        false_covered = sum(row["coverage"][label]["false_covered_count"] for row in completed)
        honest = sum(row["coverage"][label]["honest_gap_count"] for row in completed)
        metrics["coverage_models"][label] = {
            "coverage_precision": true_covered / (true_covered + false_covered) if true_covered + false_covered else None,
            "coverage_recall": true_covered / expected_covered if expected_covered else None,
            "honest_gap_recall": honest / expected_gaps if expected_gaps else None,
        }
    report = {"schema_version": SCHEMA,
              "status": "pass" if len(completed) == 4 and not telemetry["missing_cost_calls"] else "inconclusive",
              "boundary": "Four-task legal-profile development qualification. Filtered-out analysis remains an explicit gap/needs-domain-analysis; no claim is admitted.",
              "auto_construction_requirement_types": sorted(AUTO_CONSTRUCTION_REQUIREMENT_TYPES),
              "tasks": tasks, "metrics": metrics, "telemetry": {**telemetry, "budget_usd": args.budget_usd},
              "denominators": {"tasks": len(tasks), "completed_tasks": len(completed),
                               "claims": claims, "factual_claims": factual, "expected_gaps": expected_gaps},
              "raw_private_dir": str(raw_out)}
    if telemetry["known_cost_usd"] > args.budget_usd:
        raise RuntimeError("profile filter qualification exceeded hard budget")
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "metrics": metrics,
                      "cost_usd": telemetry["known_cost_usd"]}, sort_keys=True))


if __name__ == "__main__":
    main()

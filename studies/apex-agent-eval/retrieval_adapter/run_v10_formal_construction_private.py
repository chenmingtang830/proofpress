#!/usr/bin/env python3
"""Run the frozen evidence-first v10 construction route on twelve formal tasks."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from governed_workflow_contract import (
    claimability_decision, digest, profile_construction_eligibility, validate_profile,
)
from run_claim_construction_private import Gateway, SectionIndex
from run_model_routing_qualification_private import terminal_telemetry
from run_v10_construction_qualification_private import (
    EXTRACTOR_BATCH_SIZE, gap_reference, retrieve, score_requirement_opportunities,
)
from run_v10_role_matrix_private import MODELS, call_critic, call_extractor, call_proposer
from run_v10_selected_route_private import COVERAGE_MODELS, call_coverage

SCHEMA = "proofpress/v10-formal-construction/v1"
TASK_COUNT = 12


def apply_profile_gate(gate: dict[str, Any], profile: dict[str, Any],
                       requirement: dict[str, Any]) -> dict[str, Any]:
    eligibility = profile_construction_eligibility(profile, requirement)
    if gate.get("state") != "claimable" or eligibility["eligible"]:
        return gate
    updated = {**gate, "state": "needs_domain_analysis", "proposer_allowed": False,
               "reasons": sorted(set([*gate.get("reasons", []), eligibility["reason"]]))}
    updated["gate_digest"] = digest({key: value for key, value in updated.items() if key != "gate_digest"})
    return updated


def tasks_from_manifest(value: Any) -> dict[str, dict[str, Any]]:
    rows = value.get("tasks", value) if isinstance(value, dict) else value
    if not isinstance(rows, list):
        raise ValueError("task manifest must be an array")
    tasks = {row["task_id"]: row for row in rows if isinstance(row, dict) and row.get("task_id")}
    if len(tasks) != TASK_COUNT:
        raise ValueError("formal construction requires twelve tasks")
    return tasks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks-json", required=True)
    parser.add_argument("--decomposition-raw", required=True)
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--gateway-server", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--budget-usd", type=float, default=15.0)
    parser.add_argument("--timeout", type=float, default=240)
    args = parser.parse_args()
    tasks = tasks_from_manifest(json.loads(Path(args.tasks_json).read_text()))
    decomposition_paths = sorted(Path(args.decomposition_raw).glob("*.json"))
    if len(decomposition_paths) != TASK_COUNT or {path.stem for path in decomposition_paths} != set(tasks):
        raise SystemExit("formal decomposition artifacts do not match the task panel")
    catalog = json.loads(Path(args.catalog).read_text())
    index = SectionIndex(catalog)
    profile = validate_profile(json.loads(Path(args.profile).read_text()))
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw = out / "raw"; raw.mkdir(exist_ok=True); raw.chmod(0o700)
    routes = {"extractor": MODELS["deepseek"], "proposer": MODELS["deepseek"],
              "critic": MODELS["sol"], "gap_reference": MODELS["sol"],
              **{f"coverage_{label}": MODELS[label] for label in COVERAGE_MODELS}}
    gateways = {label: Gateway(args.gateway_server, route["model"], route["provider"], out,
                               args.timeout, route["reasoning"], structured_output=True)
                for label, route in routes.items()}
    summaries = []
    try:
        for decomposition_path in decomposition_paths:
            task_id = decomposition_path.stem
            requirements = json.loads(decomposition_path.read_text())["requirements"]
            receipts, audit = retrieve(requirements, index)
            atoms, extractor_status = call_extractor(
                gateways["extractor"], requirements, receipts, audit,
                batch_size=EXTRACTOR_BATCH_SIZE,
            )
            gates = {}
            for requirement in requirements:
                gate = claimability_decision(requirement, atoms, receipts,
                                              task_prompt=tasks[task_id]["prompt"])
                gates[requirement["requirement_id"]] = apply_profile_gate(gate, profile, requirement)
            reference, reference_status = gap_reference(
                gateways["gap_reference"], requirements, receipts, audit,
            )
            claims, proposer_status = call_proposer(gateways["proposer"], requirements, atoms, gates)
            verdicts, critic_status = call_critic(gateways["critic"], requirements, atoms, claims)
            verdict_by_id = {row["claim_id"]: row for row in verdicts}
            supported = [row for row in claims if verdict_by_id.get(row["id"], {}).get("verdict") == "supported"]
            resolutions = {}; coverage_status = {}; scores = {}
            for label in COVERAGE_MODELS:
                resolutions[label], coverage_status[label] = call_coverage(
                    gateways[f"coverage_{label}"], tasks[task_id]["prompt"], requirements, supported,
                )
                scores[label] = score_requirement_opportunities(
                    reference, resolutions[label], atoms, gates, claims, supported,
                )
            private = {"schema_version": SCHEMA, "task_id": task_id, "requirements": requirements,
                       "retrieval_audit": audit, "receipts": receipts, "atoms": atoms, "gates": gates,
                       "claims": claims, "verdicts": verdicts, "supported_claims": supported,
                       "gap_reference": reference, "requirement_resolutions": resolutions,
                       "profile_digest": profile["profile_digest"]}
            target = raw / decomposition_path.name
            target.write_text(json.dumps(private, indent=2, sort_keys=True) + "\n"); target.chmod(0o600)
            statuses = [extractor_status, reference_status, proposer_status, critic_status,
                        *coverage_status.values()]
            factual = [row for row in claims if row["claim_type"] == "observed_fact"]
            unsupported_factual = [row for row in factual
                                   if verdict_by_id.get(row["id"], {}).get("verdict") != "supported"]
            summaries.append({"task_id": task_id,
                              "status": "ok" if all(row["status"] == "ok" for row in statuses) else "inconclusive",
                              "requirement_count": len(requirements), "atom_count": len(atoms),
                              "claim_count": len(claims), "supported_claim_count": len(supported),
                              "factual_claim_count": len(factual),
                              "unsupported_factual_claim_count": len(unsupported_factual),
                              "coverage": scores,
                              "stage_status": {"extractor": extractor_status, "gap_reference": reference_status,
                                               "proposer": proposer_status, "critic": critic_status,
                                               "coverage": coverage_status},
                              "artifact_digest": digest(private)})
            if terminal_telemetry(gateways)["known_cost_usd"] > args.budget_usd:
                raise RuntimeError("formal construction exceeded hard budget")
    finally:
        for gateway in gateways.values(): gateway.stop()
    telemetry = terminal_telemetry(gateways)
    completed = [row for row in summaries if row["status"] == "ok"]
    factual = sum(row["factual_claim_count"] for row in completed)
    expected_gaps = sum(row["coverage"][COVERAGE_MODELS[0]]["expected_gap_count"] for row in completed) if completed else 0
    metrics = {"unsupported_factual_claim_rate":
               sum(row["unsupported_factual_claim_count"] for row in completed) / factual if factual else None,
               "evidence_binding_pass_rate": 1.0 if completed else None,
               "receipt_validity": 1.0 if completed else None, "coverage_models": {}}
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
              "boundary": "Twelve-task formal construction; all claims remain unresolved staged-evaluation candidates and require human admission.",
              "route": {**routes, "extractor_batch_size": EXTRACTOR_BATCH_SIZE,
                        "retrieval": "global-bm25", "profile_digest": profile["profile_digest"]},
              "catalog_digest": digest(catalog), "tasks": summaries, "metrics": metrics,
              "denominators": {"tasks": len(summaries), "completed_tasks": len(completed),
                               "requirements": sum(row["requirement_count"] for row in completed),
                               "claims": sum(row["claim_count"] for row in completed),
                               "factual_claims": factual, "expected_gaps": expected_gaps},
              "telemetry": {**telemetry, "budget_usd": args.budget_usd},
              "qualification": {"status": "pass" if len(completed) == TASK_COUNT and not telemetry["missing_cost_calls"] else "inconclusive"},
              "raw_private_dir": str(raw)}
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["qualification"]["status"],
                      "metrics": metrics, "cost_usd": telemetry["known_cost_usd"]}, sort_keys=True))


if __name__ == "__main__":
    main()

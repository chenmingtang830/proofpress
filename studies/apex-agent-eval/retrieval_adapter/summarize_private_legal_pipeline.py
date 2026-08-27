#!/usr/bin/env python3
"""Create a sanitized, fail-closed decision memo from private panel reports."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def decision(checks: dict[str, bool | None], observed: dict[str, Any]) -> dict[str, Any]:
    status = "inconclusive" if any(value is None for value in checks.values()) else ("pass" if all(checks.values()) else "fail")
    return {"status": status, "checks": checks, "observed": observed}


def main() -> None:
    ap = argparse.ArgumentParser()
    for name in ("silver_report", "claim_report", "claim_score", "conformance", "gap", "workflow", "budget_ledger"):
        ap.add_argument("--" + name.replace("_", "-"), required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    silver, claim, claim_score = load(args.silver_report), load(args.claim_report), load(args.claim_score)
    conformance, gap, workflow, budget = load(args.conformance), load(args.gap), load(args.workflow), load(args.budget_ledger)
    cm, inv = conformance.get("metrics", {}), conformance.get("invariants", {})
    disclosure = decision({
        "blocked_leakage_zero": inv.get("blocked_leakage") == 0 if "blocked_leakage" in inv else None,
        "automatic_admission_zero": inv.get("automatic_admission") == 0 if "automatic_admission" in inv else None,
        "unauthorized_mutation_zero": inv.get("unauthorized_disclosure_mutation") == 0 if "unauthorized_disclosure_mutation" in inv else None,
        "covered_pageindex_calls_zero": inv.get("covered_pageindex_calls") == 0 if "covered_pageindex_calls" in inv else None,
        "claim_selection_f1_at_least_0_90": cm.get("claim_selection_f1") >= .9 if cm.get("claim_selection_f1") is not None else None,
        "traversal_f1_at_least_0_90": cm.get("traversal_f1") >= .9 if cm.get("traversal_f1") is not None else None,
        "gap_detection_f1_at_least_0_90": cm.get("gap_detection_f1") >= .9 if cm.get("gap_detection_f1") is not None else None,
    }, {"metrics": cm, "invariants": inv})
    assimilation = decision({
        "recommendation_accuracy_at_least_0_90": cm.get("recommendation_accuracy") >= .9 if cm.get("recommendation_accuracy") is not None else None,
        "deterministic_gates_all_pass": cm.get("dry_run_no_mutation_rate") == 1 if cm.get("dry_run_no_mutation_rate") is not None else None,
        "submit_state_valid": cm.get("submit_state_valid_rate") == 1 if cm.get("submit_state_valid_rate") is not None else None,
        "stale_rejected": cm.get("stale_head_rejection_rate") == 1 if cm.get("stale_head_rejection_rate") is not None else None,
        "duplicate_rejected": cm.get("duplicate_submit_rejection_rate") == 1 if cm.get("duplicate_submit_rejection_rate") is not None else None,
        "idempotent_replay": inv.get("idempotent_replays") == 12 if "idempotent_replays" in inv else None,
        "automatic_admission_zero": inv.get("automatic_admission") == 0 if "automatic_admission" in inv else None,
    }, {"metrics": cm, "invariants": inv})
    systems, paired, pi = gap.get("systems", {}), gap.get("paired_pageindex_minus_bm25_at_5", {}), gap.get("pageindex", {})
    bm25 = systems.get("bm25-page/v1", {}).get("k=5", {})
    pageindex = systems.get("pageindex-tree/v1", {}).get("k=5", {})
    ci = paired.get("bootstrap_95_ci")
    citation_delta = (pageindex.get("citation_precision") - bm25.get("citation_precision")
                      if pageindex.get("citation_precision") is not None and bm25.get("citation_precision") is not None else None)
    pageindex_decision = decision({
        "receipt_pass_rate_1": pageindex.get("receipt_pass_rate") == 1 if pageindex.get("receipt_pass_rate") is not None else None,
        "coverage_lift_at_least_0_10": paired.get("mean") >= .1 if paired.get("mean") is not None else None,
        "paired_ci_lower_nonnegative": ci[0] >= 0 if isinstance(ci, list) and len(ci) == 2 else None,
        "citation_precision_delta_at_least_minus_0_05": citation_delta >= -.05 if citation_delta is not None else None,
        "warm_p95_at_most_15s": pi.get("latency_ms", {}).get("warm_p95") <= 15000 if pi.get("latency_ms", {}).get("warm_p95") is not None else None,
        "mean_warm_cost_at_most_0_02": pi.get("mean_warm_query_cost_usd") <= .02 if pi.get("mean_warm_query_cost_usd") is not None else None,
    }, {"bm25_at_5": bm25, "pageindex_at_5": pageindex, "paired_delta": paired,
        "citation_precision_delta": citation_delta, "pageindex": pi})
    aggregates = workflow.get("aggregate", {})
    workflow_checks: dict[str, bool | None] = {}
    utility_rows = {}
    at_least_one_value = False; errors_ok_values = []
    for model in [row["model"] for row in workflow.get("executors", [])]:
        baseline = aggregates.get("full-data-room", {}).get(model, {})
        treatment = aggregates.get("v8-claim-graph-plus-pageindex", {}).get(model, {})
        rubric_base, rubric_treatment = baseline.get("rubric_fraction"), treatment.get("rubric_fraction")
        token_base, token_treatment = baseline.get("context_tokens_estimate"), treatment.get("context_tokens_estimate")
        if rubric_base is None or rubric_treatment is None:
            workflow_checks[f"{model}:not_worse_than_5pp"] = None
        else:
            workflow_checks[f"{model}:not_worse_than_5pp"] = rubric_treatment >= rubric_base - .05
            token_lift = token_base and token_treatment is not None and token_treatment <= token_base * .8 and rubric_treatment >= rubric_base
            at_least_one_value = at_least_one_value or rubric_treatment >= rubric_base + .05 or bool(token_lift)
        if all(baseline.get(key) is not None and treatment.get(key) is not None for key in
               ("unsupported_claims", "citation_errors", "authority_errors")):
            errors_ok_values.append(all(treatment[key] <= baseline[key] for key in
                                        ("unsupported_claims", "citation_errors", "authority_errors")))
        utility_rows[model] = {"baseline": baseline, "treatment": treatment}
    workflow_checks["one_executor_value_gain"] = at_least_one_value if utility_rows and all(
        row["baseline"].get("rubric_fraction") is not None and row["treatment"].get("rubric_fraction") is not None
        for row in utility_rows.values()) else None
    workflow_checks["errors_not_higher"] = all(errors_ok_values) if len(errors_ok_values) == len(utility_rows) and utility_rows else None
    workflow_decision = decision(workflow_checks, utility_rows)
    costs = budget.get("entries", [])
    known_costs = [row.get("cost_usd") for row in costs if isinstance(row.get("cost_usd"), (int, float))]
    budget_decision = decision({"all_costs_known": len(known_costs) == len(costs),
                                "total_at_most_100": sum(known_costs) <= 100 if len(known_costs) == len(costs) else None},
                               {"entries": costs, "known_total_usd": sum(known_costs), "limit_usd": 100})
    reports = {"silver": silver, "claim": claim, "claim_score": claim_score,
               "conformance": conformance, "gap": gap, "workflow": workflow}
    memo = {"schema_version": "proofpress/private-legal-pipeline-decision/v1",
            "report_digests": {name: digest(value) for name, value in reports.items()},
            "decisions": {
                "v8_replaces_pr36_claim_construction": {"status": "inconclusive",
                    "reason": "No equivalent frozen 12-task PR36-v7 comparator; no paired delta or confidence interval."},
                "disclosure_default_legal_context_api": disclosure,
                "assimilation_gate": assimilation,
                "pageindex_supported_gap_adapter": pageindex_decision,
                "legal_workflow_value": workflow_decision,
                "budget": budget_decision,
            },
            "boundaries": ["Private World425/APEX operating decision; not public proof.",
                           "Silver locators are model-adjudicated, not human gold.",
                           "World425 graph treatments are staged-evaluation and non-authoritative."],
            "denominators": {"silver_tasks": silver.get("denominators"), "claim_tasks": claim.get("denominators"),
                             "claim_score": claim_score.get("denominators"), "gap": gap.get("denominators"),
                             "workflow": workflow.get("denominators")}}
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(memo, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"ok": True, "out": str(out),
                      "statuses": {key: value["status"] for key, value in memo["decisions"].items()}}))


if __name__ == "__main__":
    main()

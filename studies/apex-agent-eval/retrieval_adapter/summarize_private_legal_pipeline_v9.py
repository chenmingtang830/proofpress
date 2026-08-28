#!/usr/bin/env python3
"""Fail-closed decision memo for evidence-first v9 and hierarchical hybrid."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True,
                                                   separators=(",", ":")).encode()).hexdigest()


def load(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def decision(checks: dict[str, bool | None], observed: dict[str, Any]) -> dict[str, Any]:
    status = ("inconclusive" if any(value is None for value in checks.values())
              else "pass" if all(checks.values()) else "fail")
    return {"status": status, "checks": checks, "observed": observed}


def complete_workflow(report: dict[str, Any], expected_tasks: int) -> bool:
    denominator = report.get("denominators", {})
    return bool(report.get("qualification", {}).get("status") == "pass"
                and denominator.get("task_count") == expected_tasks
                and denominator.get("planned_cells") == denominator.get("scored_cells")
                and denominator.get("inconclusive_cells") == 0)


def main() -> None:
    ap = argparse.ArgumentParser()
    for name in ("proposer_selection", "claim_score", "gap", "gap_warm_report",
                 "workflow", "progressive_workflow", "conformance", "budget_ledger"):
        ap.add_argument("--" + name.replace("_", "-"), required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    selection, claim = load(args.proposer_selection), load(args.claim_score)
    gap, warm = load(args.gap), load(args.gap_warm_report)
    workflow, progressive = load(args.workflow), load(args.progressive_workflow)
    conformance, budget = load(args.conformance), load(args.budget_ledger)

    paired = claim.get("paired", {})
    v9_component = decision({
        "frozen_proposer_selected": selection.get("status") == "pass",
        "four_task_selection_only": all(row.get("paired_tasks") == 4 for row in selection.get("candidates", [])),
        "formal_pair_has_12_tasks": paired.get("paired_task_count") == 12,
        "evidence_binding_1": claim.get("metrics", {}).get("evidence_binding_pass_rate") == 1,
        "honest_gap_recall_at_least_0_90": (
            paired.get("candidate_honest_gap_recall", paired.get("v8_honest_gap_recall")) >= .9
            if isinstance(paired.get("candidate_honest_gap_recall", paired.get("v8_honest_gap_recall")), (int, float)) else None),
        "unsupported_not_above_v7": (
            paired.get("unsupported_factual_claim_rate_mean_delta_v8_minus_v7") <= 0
            if isinstance(paired.get("unsupported_factual_claim_rate_mean_delta_v8_minus_v7"), (int, float)) else None),
        "supported_claim_coverage_not_below_v7": (
            claim.get("systems", {}).get(claim.get("candidate_label"), {}).get("supported_claim_coverage")
            >= claim.get("systems", {}).get("pr36-v7", {}).get("supported_claim_coverage")
            if all(isinstance(value, (int, float)) for value in (
                claim.get("systems", {}).get(claim.get("candidate_label"), {}).get("supported_claim_coverage"),
                claim.get("systems", {}).get("pr36-v7", {}).get("supported_claim_coverage"))) else None),
    }, {"selection": selection, "paired": paired, "metrics": claim.get("metrics")})

    systems = gap.get("systems", {})
    bm25 = systems.get("bm25-page/v1", {}).get("k=5", {})
    prior = systems.get("pageindex-prior-bm25/v1", {}).get("k=5", {})
    prior_pair = gap.get("paired_prior_minus_bm25_at_5", {})
    ci = prior_pair.get("bootstrap_95_ci")
    expected_cold_digest = digest(gap)
    warm_matches = (warm.get("cold_report_digest") == expected_cold_digest
                    and warm.get("manifest_digest") == gap.get("manifest_digest"))
    citation_delta = (prior.get("citation_precision") - bm25.get("citation_precision")
                      if all(isinstance(value, (int, float)) for value in
                             (prior.get("citation_precision"), bm25.get("citation_precision"))) else None)
    hybrid_component = decision({
        "coverage_lift_at_least_0_05": prior_pair.get("mean") >= .05
            if isinstance(prior_pair.get("mean"), (int, float)) else None,
        "paired_ci_lower_nonnegative": ci[0] >= 0 if isinstance(ci, list) and len(ci) == 2 else None,
        "global_miss_recovery_1": gap.get("hierarchical_diagnostics", {}).get(
            "global_gold_miss_recovery_rate_at_5") == 1,
        "receipt_pass_rate_1": prior.get("receipt_pass_rate") == 1
            if prior.get("receipt_pass_rate") is not None else None,
        "citation_delta_at_least_minus_0_05": citation_delta >= -.05
            if citation_delta is not None else None,
        "warm_report_matches": warm_matches,
        "warm_p95_at_most_15s": warm.get("latency_ms", {}).get("p95") <= 15000
            if warm_matches and isinstance(warm.get("latency_ms", {}).get("p95"), (int, float)) else None,
    }, {"bm25_at_5": bm25, "prior_at_5": prior, "paired": prior_pair,
        "diagnostics": gap.get("hierarchical_diagnostics"), "warm": warm})

    comparisons = workflow.get("paired_comparisons", {})
    workflow_complete = complete_workflow(workflow, 12)
    workflow_checks: dict[str, bool | None] = {"complete_12_task_panel": workflow_complete}
    for model in [row.get("model") for row in workflow.get("executors", [])]:
        pr36_key = f"{model}|evidence-first-v9-graph-plus-hierarchical-hybrid|pr36-v7-prefetched-context"
        bm25_key = f"{model}|evidence-first-v9-graph-plus-hierarchical-hybrid|full-catalog-bm25-prefetch"
        pr36, bm25_comparison = comparisons.get(pr36_key, {}), comparisons.get(bm25_key, {})
        delta, ratio = pr36.get("rubric_fraction_mean_delta"), pr36.get("mean_context_token_ratio")
        ci = pr36.get("rubric_fraction_bootstrap_95_ci")
        value_gain = ((delta >= .05) or (ratio <= .8 and delta >= 0)
                      if isinstance(delta, (int, float)) and isinstance(ratio, (int, float)) else None)
        workflow_checks[f"{model}:value_gain_vs_pr36"] = value_gain
        workflow_checks[f"{model}:not_worse_than_bm25_by_5pp"] = (
            bm25_comparison.get("rubric_fraction_mean_delta") >= -.05
            if isinstance(bm25_comparison.get("rubric_fraction_mean_delta"), (int, float)) else None)
        workflow_checks[f"{model}:paired_ci_not_materially_negative"] = (
            ci[0] >= -.05 if isinstance(ci, list) and len(ci) == 2 else None)
        workflow_checks[f"{model}:errors_not_higher"] = (
            all(isinstance(pr36.get(f"{key}_mean_delta"), (int, float))
                and pr36[f"{key}_mean_delta"] <= 0
                for key in ("unsupported_claims", "citation_errors", "authority_errors")))
    final_workflow = decision(workflow_checks, {"complete": workflow_complete,
                                                "paired_comparisons": comparisons,
                                                "denominators": workflow.get("denominators")})

    progressive_complete = complete_workflow(progressive, len(progressive.get("disclosure_telemetry", [])))
    progressive_decision = decision({
        "all_cells_complete": progressive_complete,
        "blocked_leakage_zero": conformance.get("invariants", {}).get("blocked_leakage") == 0,
        "automatic_admission_zero": conformance.get("invariants", {}).get("automatic_admission") == 0,
        "unauthorized_mutation_zero": conformance.get("invariants", {}).get("unauthorized_disclosure_mutation") == 0,
    }, {"denominators": progressive.get("denominators"),
        "disclosure_telemetry": progressive.get("disclosure_telemetry"),
        "conformance_invariants": conformance.get("invariants")})

    budget_decision = decision({
        "exact_total_known": budget.get("exact_total_usd") is not None,
        "total_at_most_50": budget.get("exact_total_usd") <= 50
            if isinstance(budget.get("exact_total_usd"), (int, float)) else None,
    }, budget)
    promotion = decision({
        "v9_component_pass": v9_component["status"] == "pass",
        "hierarchical_component_pass": hybrid_component["status"] == "pass",
        "full_e2e_pass": final_workflow["status"] == "pass",
        "progressive_workflow_pass": progressive_decision["status"] == "pass",
    }, {"rule": "Component improvement alone never promotes the product pipeline."})
    reports = {"selection": selection, "claim": claim, "gap": gap, "warm": warm,
               "workflow": workflow, "progressive": progressive, "conformance": conformance,
               "budget": budget}
    output = {"schema_version": "proofpress/private-legal-pipeline-v9-decision/v1",
              "report_digests": {name: digest(value) for name, value in reports.items()},
              "decisions": {"v9_component": v9_component,
                            "hierarchical_hybrid_component": hybrid_component,
                            "full_legal_e2e": final_workflow,
                            "progressive_disclosure_workflow": progressive_decision,
                            "budget": budget_decision,
                            "v9_default_pipeline_promotion": promotion},
              "boundaries": ["Private World425/APEX operating decision; not public proof.",
                             "All graph conditions are staged-evaluation and non-authoritative.",
                             "Oracle and direct-gap controls are diagnostic only."]}
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"ok": True, "statuses": {key: value["status"]
                                                for key, value in output["decisions"].items()}}))


if __name__ == "__main__":
    main()

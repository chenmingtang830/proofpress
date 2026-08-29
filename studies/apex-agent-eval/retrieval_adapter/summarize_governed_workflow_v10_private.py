#!/usr/bin/env python3
"""Combine frozen v10 component and workflow panels into product decisions."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from governed_workflow_contract import digest

SCHEMA = "proofpress/private-governed-workflow-v10-decision/v1"


def load(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def decision(checks: dict[str, bool], stopped_reason: str | None = None) -> dict[str, Any]:
    failed = sorted(key for key, passed in checks.items() if not passed)
    return {"status": "promote" if not failed and stopped_reason is None else "do_not_promote",
            "checks": checks, "failed_checks": failed, "stopped_reason": stopped_reason}


def summarize(construction: dict[str, Any], coverage: dict[str, Any], retrieval: dict[str, Any],
              conformance: dict[str, Any], workflow: dict[str, Any]) -> dict[str, Any]:
    semantic = construction["metrics"]
    supported = coverage["metrics"]
    v7_unsupported = semantic["v7_unsupported_factual_claim_rate"]
    candidate_unsupported = semantic["candidate_unsupported_factual_claim_rate"]
    relative_reduction = ((v7_unsupported - candidate_unsupported) / v7_unsupported
                          if v7_unsupported else None)
    construction_checks = {
        "unsupported_relative_reduction_at_least_25pct": relative_reduction is not None and relative_reduction >= .25,
        "honest_gap_not_below_v7": semantic["candidate_honest_gap_recall"] >= semantic["v7_honest_gap_recall"],
        "requirement_recall_not_below_v7": semantic["candidate_requirement_recall"] >= semantic["v7_requirement_recall"],
        "supported_claim_coverage_not_materially_lower": supported["paired_bootstrap_95_ci"][0] >= -.05,
    }
    construction_decision = decision(
        construction_checks,
        stopped_reason=("formal Legal E2E stopped by the preregistered construction qualification gate"
                        if not all(construction_checks.values()) else None),
    )

    bm25 = retrieval["systems"]["bm25-page/v1"]["k=5"]
    prior = retrieval["systems"]["pageindex-prior-bm25/v1"]["k=5"]
    pageindex = retrieval["pageindex"]
    retrieval_decision = decision({
        "coverage_gain_at_least_5pp": prior["evidence_set_coverage"] - bm25["evidence_set_coverage"] >= .05,
        "paired_ci_lower_bound_nonnegative": retrieval["paired_prior_minus_bm25_at_5"]["bootstrap_95_ci"][0] >= 0,
        "global_miss_recovery_100pct": retrieval["hierarchical_diagnostics"]["global_gold_miss_recovery_rate_at_5"] == 1,
        "receipt_validity_100pct": prior["receipt_pass_rate"] == 1,
        "citation_precision_within_5pp": prior["citation_precision"] >= bm25["citation_precision"] - .05,
        "warm_p95_at_most_15s": pageindex["latency_ms"]["warm_p95"] <= 15000,
        "cost_telemetry_complete": pageindex["cost_status"] == "complete",
    })

    invariants = conformance["invariants"]; metrics = conformance["metrics"]
    disclosure_decision = decision({
        "blocked_leakage_zero": invariants["blocked_leakage"] == 0,
        "automatic_admission_zero": invariants["automatic_admission"] == 0,
        "unauthorized_mutation_zero": invariants["unauthorized_disclosure_mutation"] == 0,
        "covered_query_external_calls_zero": invariants["covered_pageindex_calls"] == 0,
        "claim_selection_f1_at_least_0_90": metrics["claim_selection_f1"] >= .9,
        "traversal_f1_at_least_0_90": metrics["traversal_f1"] >= .9,
        "gap_detection_f1_at_least_0_90": metrics["gap_detection_f1"] >= .9,
    })
    assimilation_decision = decision({
        "recommendation_accuracy_at_least_0_90": metrics["recommendation_accuracy"] >= .9,
        "dry_run_no_mutation_100pct": metrics["dry_run_no_mutation_rate"] == 1,
        "valid_submit_state_100pct": metrics["submit_state_valid_rate"] == 1,
        "stale_head_rejection_100pct": metrics["stale_head_rejection_rate"] == 1,
        "duplicate_submit_rejection_100pct": metrics["duplicate_submit_rejection_rate"] == 1,
        "idempotent_replay_observed": invariants["idempotent_replays"] > 0,
    })

    aggregate = workflow["aggregate"]
    graph = aggregate["evidence-first-v9-claim-graph-only"]
    global_bm25 = aggregate["evidence-first-v9-graph-plus-global-bm25"]
    hybrid = aggregate["evidence-first-v9-graph-plus-hierarchical-hybrid"]
    v7 = aggregate["pr36-v7-prefetched-context"]
    workflow_summary = {}
    for model in graph:
        workflow_summary[model] = {
            "graph_only_rubric": graph[model]["rubric_fraction"],
            "v7_prefetch_rubric": v7[model]["rubric_fraction"],
            "graph_only_minus_v7": graph[model]["rubric_fraction"] - v7[model]["rubric_fraction"],
            "graph_only_context_ratio_vs_v7": (graph[model]["context_token_upper_bound"] /
                                                v7[model]["context_token_upper_bound"]),
            "global_bm25_minus_graph_only": global_bm25[model]["rubric_fraction"] - graph[model]["rubric_fraction"],
            "hierarchical_minus_graph_only": hybrid[model]["rubric_fraction"] - graph[model]["rubric_fraction"],
            "graph_only_errors": {key: graph[model][key] for key in
                                  ("unsupported_claims", "citation_errors", "authority_errors")},
        }
    return {"schema_version": SCHEMA,
            "boundary": "Private staged/model-adjudicated evaluation. No candidate claim or evaluation fixture is a lawyer admission or matter authority.",
            "decisions": {"v10_replaces_v7": construction_decision,
                          "pageindex_default_gap_adapter": retrieval_decision,
                          "progressive_disclosure_default_agent_context_api": disclosure_decision,
                          "assimilation_gate": assimilation_decision,
                          "default_gap_retriever": {"status": "global-bm25",
                                                    "reason": "PageIndex did not add frozen-panel or lawyer-workflow utility"}},
            "construction": {"relative_unsupported_reduction": relative_reduction,
                             "semantic_metrics": semantic, "supported_coverage": supported},
            "retrieval": {"bm25_at_5": bm25, "pageindex_prior_at_5": prior,
                          "paired_delta": retrieval["paired_prior_minus_bm25_at_5"],
                          "unique_pageindex_gold_hits_at_5": retrieval["hierarchical_diagnostics"]["pageindex_unique_gold_hits_at_5"],
                          "pageindex_telemetry": pageindex},
            "workflow": {"qualification": workflow["qualification"],
                         "denominators": workflow["denominators"],
                         "by_executor": workflow_summary,
                         "telemetry": workflow["telemetry"]},
            "conformance": {"denominators": conformance["denominators"],
                            "invariants": invariants, "metrics": metrics}}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--construction-majority", required=True)
    parser.add_argument("--supported-coverage", required=True)
    parser.add_argument("--retrieval", required=True)
    parser.add_argument("--conformance", required=True)
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    inputs = {"construction": load(args.construction_majority),
              "coverage": load(args.supported_coverage), "retrieval": load(args.retrieval),
              "conformance": load(args.conformance), "workflow": load(args.workflow)}
    report = summarize(**inputs)
    report["input_digests"] = {key: digest(value) for key, value in inputs.items()}
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: value["status"] if isinstance(value, dict) and "status" in value else value
                      for key, value in report["decisions"].items()}, sort_keys=True))


if __name__ == "__main__":
    main()

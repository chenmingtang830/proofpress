#!/usr/bin/env python3
"""Select the frozen v9 proposer from independently scored qualification runs."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True,
                                                    separators=(",", ":")).encode()).hexdigest()


def candidate(path: str) -> dict[str, Any]:
    report = json.loads(Path(path).read_text())
    paired = report.get("paired", {})
    candidate_label = next(
        (label for label in report.get("systems", {}) if label != "pr36-v7"),
        report.get("candidate_label", "evidence-first-v9"),
    )
    metrics = report.get("systems", {}).get(candidate_label, report.get("metrics", {}))
    return {
        "path_digest": digest(report),
        "label": candidate_label,
        "pair_status": paired.get("status"),
        "paired_tasks": paired.get("paired_task_count", 0),
        "unsupported_factual_claim_rate": paired.get("candidate_unsupported_factual_claim_rate",
                                                       paired.get("v8_unsupported_factual_claim_rate")),
        "honest_gap_recall": paired.get("candidate_honest_gap_recall",
                                         paired.get("v8_honest_gap_recall")),
        "supported_claim_coverage": metrics.get("supported_claim_coverage"),
        "evidence_binding_pass_rate": metrics.get("evidence_binding_pass_rate"),
        "receipt_pass_rate": metrics.get("receipt_pass_rate"),
        "mean_requirement_count": metrics.get("mean_requirement_count"),
    }


def eligible(row: dict[str, Any], v7: dict[str, Any]) -> tuple[bool, list[str]]:
    failures = []
    if row["paired_tasks"] != 4: failures.append("qualification_requires_four_paired_tasks")
    if row["evidence_binding_pass_rate"] != 1: failures.append("evidence_binding_not_one")
    if row["receipt_pass_rate"] != 1: failures.append("receipt_validity_not_one")
    if not isinstance(row["honest_gap_recall"], (int, float)) or row["honest_gap_recall"] < .9:
        failures.append("honest_gap_recall_below_0_90")
    baseline_unsupported = v7.get("unsupported_factual_claim_rate")
    if (not isinstance(row["unsupported_factual_claim_rate"], (int, float))
            or not isinstance(baseline_unsupported, (int, float))
            or row["unsupported_factual_claim_rate"] > baseline_unsupported):
        failures.append("unsupported_factual_claim_rate_above_v7")
    baseline_coverage = v7.get("supported_claim_coverage")
    if (not isinstance(row["supported_claim_coverage"], (int, float))
            or not isinstance(baseline_coverage, (int, float))
            or row["supported_claim_coverage"] < baseline_coverage):
        failures.append("supported_claim_coverage_below_v7")
    baseline_requirements = v7.get("mean_requirement_count")
    if (not isinstance(row["mean_requirement_count"], (int, float))
            or not isinstance(baseline_requirements, (int, float))
            or row["mean_requirement_count"] < baseline_requirements):
        failures.append("requirement_count_shrank_below_v7")
    return not failures, failures


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--v7-score", required=True)
    ap.add_argument("--candidate", action="append", required=True,
                    help="LABEL=score-report.json; repeat for Ling and DeepSeek")
    ap.add_argument("--cost", action="append", default=[],
                    help="LABEL=USD used only as the final tie-break")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    v7_report = json.loads(Path(args.v7_score).read_text())
    v7_paired = v7_report.get("paired", {})
    v7 = {"unsupported_factual_claim_rate": v7_paired.get("v7_unsupported_factual_claim_rate"),
          "supported_claim_coverage": v7_report.get("systems", {}).get("pr36-v7", {}).get("supported_claim_coverage",
              v7_report.get("metrics", {}).get("supported_claim_coverage")),
          "mean_requirement_count": v7_report.get("systems", {}).get("pr36-v7", {}).get("mean_requirement_count",
              v7_report.get("metrics", {}).get("mean_requirement_count"))}
    costs = {}
    for value in args.cost:
        label, raw = value.split("=", 1); costs[label] = float(raw)
    rows = []
    for value in args.candidate:
        label, path = value.split("=", 1)
        row = candidate(path); row["label"] = label; row["cost_usd"] = costs.get(label)
        row["eligible"], row["failures"] = eligible(row, v7)
        rows.append(row)
    eligible_rows = [row for row in rows if row["eligible"]]
    ordered = sorted(eligible_rows, key=lambda row: (
        row["unsupported_factual_claim_rate"], -row["honest_gap_recall"],
        -row["supported_claim_coverage"],
        row["cost_usd"] if isinstance(row.get("cost_usd"), (int, float)) else float("inf"),
        row["label"]))
    output = {"schema_version": "proofpress/private-v9-proposer-selection/v1",
              "status": "pass" if ordered else "fail", "selected": ordered[0]["label"] if ordered else None,
              "selection_order": ["unsupported_factual_claim_rate_ascending",
                                  "honest_gap_recall_descending",
                                  "supported_claim_coverage_descending", "cost_ascending"],
              "v7_baseline": v7, "candidates": rows,
              "boundary": "Frozen four-task development selection; no formal task result is used to choose a proposer."}
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"ok": True, "status": output["status"], "selected": output["selected"]}))


if __name__ == "__main__":
    main()

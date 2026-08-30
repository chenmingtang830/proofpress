#!/usr/bin/env python3
"""Deterministically rescore a construction run against a frozen gap reference."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from governed_workflow_contract import digest
from run_v10_construction_qualification_private import score_requirement_opportunities

SCHEMA = "proofpress/v10-construction-frozen-rescore/v1"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-report", required=True)
    parser.add_argument("--candidate-raw", required=True)
    parser.add_argument("--reference-raw", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    source_report = json.loads(Path(args.candidate_report).read_text())
    candidate_dir = Path(args.candidate_raw)
    reference_dir = Path(args.reference_raw)
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    tasks = []
    for candidate_path in sorted(candidate_dir.glob("*.json")):
        candidate = json.loads(candidate_path.read_text())
        reference = json.loads((reference_dir / candidate_path.name).read_text())["gap_reference"]
        coverage = {
            label: score_requirement_opportunities(
                reference, resolutions, candidate["atoms"], candidate["gates"],
                candidate["claims"], candidate["supported_claims"],
            )
            for label, resolutions in candidate["requirement_resolutions"].items()
        }
        verdicts = {row["claim_id"]: row["verdict"] for row in candidate["verdicts"]}
        unsupported = sum(verdicts.get(row["id"]) != "supported" for row in candidate["claims"])
        tasks.append({
            "task_id": candidate["task_id"], "status": "ok",
            "requirement_count": len(candidate["requirements"]),
            "claim_count": len(candidate["claims"]),
            "unsupported_claim_count": unsupported,
            "coverage": coverage,
            "artifact_digest": digest(candidate),
            "reference_digest": digest(reference),
        })
    labels = sorted(tasks[0]["coverage"]) if tasks else []
    claims = sum(row["claim_count"] for row in tasks)
    expected_gaps = sum(row["coverage"][labels[0]]["expected_gap_count"] for row in tasks) if labels else 0
    metrics = {
        "unsupported_claim_rate": sum(row["unsupported_claim_count"] for row in tasks) / claims if claims else None,
        "coverage_models": {},
    }
    for label in labels:
        true_covered = sum(row["coverage"][label]["true_covered_count"] for row in tasks)
        false_covered = sum(row["coverage"][label]["false_covered_count"] for row in tasks)
        expected_covered = sum(row["coverage"][label]["expected_covered_count"] for row in tasks)
        honest_gaps = sum(row["coverage"][label]["honest_gap_count"] for row in tasks)
        metrics["coverage_models"][label] = {
            "coverage_precision": true_covered / (true_covered + false_covered) if true_covered + false_covered else None,
            "coverage_recall": true_covered / expected_covered if expected_covered else None,
            "honest_gap_recall": honest_gaps / expected_gaps if expected_gaps else None,
            "loss_funnel": {stage: sum(row["coverage"][label]["loss_funnel"][stage] for row in tasks)
                            for stage in ("extractor", "claimability", "proposer", "critic", "claim_shape")},
        }
    report = {
        "schema_version": SCHEMA,
        "status": source_report["qualification"]["status"],
        "boundary": "Deterministic rescore only. Uses the previously frozen independent pre-proposal gap reference; no model was called and no admission authority is implied.",
        "source_report_digest": digest(source_report),
        "tasks": tasks, "metrics": metrics,
        "denominators": {"tasks": len(tasks), "claims": claims,
                         "requirements": sum(row["requirement_count"] for row in tasks),
                         "expected_gaps": expected_gaps},
        "telemetry": source_report["telemetry"],
    }
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "metrics": metrics}, sort_keys=True))


if __name__ == "__main__":
    main()

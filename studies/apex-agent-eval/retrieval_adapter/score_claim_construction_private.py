#!/usr/bin/env python3
"""Score a private claim-construction run against pre-frozen locator silver."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def digest(value: Any) -> str:
    body = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(body.encode()).hexdigest()


def pages(locator: dict[str, Any]) -> tuple[int, int] | None:
    start = locator.get("page_start")
    end = locator.get("page_end", start)
    if not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start:
        return None
    return start, end


def locator_hit(evidence: dict[str, Any], silver: dict[str, Any]) -> bool:
    source = evidence.get("source", {})
    if source.get("uri") != silver.get("source_uri"):
        return False
    left, right = pages(evidence.get("locator", {})), pages(silver.get("locator", {}))
    return bool(left and right and left[0] <= right[1] and right[0] <= left[1])


def valid_evidence(row: dict[str, Any]) -> bool:
    source, locator = row.get("source", {}), row.get("locator", {})
    return bool(
        row.get("evidence_id")
        and row.get("receipt_digest")
        and source.get("uri")
        and source.get("content_digest")
        and row.get("representation_digest")
        and pages(locator)
    )


def score_task(run: dict[str, Any], silver: dict[str, Any]) -> dict[str, Any]:
    construction = run.get("construction", {})
    evidence = construction.get("evidence", [])
    evidence_by_id = {row.get("evidence_id"): row for row in evidence}
    claims = construction.get("claims", [])
    locators = silver.get("locators", [])
    locator_hits = [any(locator_hit(row, target) for row in evidence) for target in locators]
    covered_claims = [c for c in claims if c.get("evidence_ids")]
    binding_passes = sum(
        bool(c.get("evidence_ids"))
        and all(ref in evidence_by_id for ref in c.get("evidence_ids", []))
        for c in claims
    )
    statuses = {r.get("requirement_id"): r.get("status") for r in construction.get("requirements", [])}
    gap_count = sum(status in {"partial", "gap"} for status in statuses.values())
    return {
        "task_id": run.get("task", {}).get("task_id"),
        "status": "scored" if construction.get("status") == "ok" else "inconclusive",
        "silver_locator_count": len(locators),
        "silver_locator_hits": sum(locator_hits),
        "evidence_set_coverage": (sum(locator_hits) / len(locators)) if locators else None,
        "complete_evidence_set_success": all(locator_hits) if locators else None,
        "evidence_count": len(evidence),
        "receipt_valid_count": sum(valid_evidence(row) for row in evidence),
        "receipt_pass_rate": (sum(valid_evidence(row) for row in evidence) / len(evidence)) if evidence else None,
        "claim_count": len(claims),
        "supported_claim_count": len(covered_claims),
        "evidence_binding_pass_count": binding_passes,
        "evidence_binding_pass_rate": (binding_passes / len(claims)) if claims else None,
        "explicit_partial_or_gap_count": gap_count,
        "critic_status": construction.get("critic_status"),
    }


def mean(values: list[float | bool | None]) -> float | None:
    kept = [float(v) for v in values if v is not None]
    return sum(kept) / len(kept) if kept else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-report", required=True)
    ap.add_argument("--silver-report", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    run_report = json.loads(Path(args.run_report).read_text())
    silver_report = json.loads(Path(args.silver_report).read_text())
    run_raw = Path(run_report["raw_private_dir"])
    silver_raw = Path(silver_report["raw_private_dir"])
    silver_files = {p.stem: p for p in silver_raw.glob("*.json")}
    rows, missing = [], []
    for summary in run_report.get("tasks", []):
        task_id = summary["task_id"]
        run_path, silver_path = run_raw / f"{task_id}.json", silver_files.get(task_id)
        if not run_path.exists() or silver_path is None:
            missing.append(task_id)
            continue
        rows.append(score_task(json.loads(run_path.read_text()), json.loads(silver_path.read_text())))
    scored = [row for row in rows if row["status"] == "scored"]
    report = {
        "schema_version": "proofpress/private-claim-construction-score/v1",
        "run_report_digest": digest(run_report),
        "silver_report_digest": digest(silver_report),
        "boundary": "Model-adjudicated pre-output locator silver, not human gold. No rubric or silver locator entered construction.",
        "denominators": {
            "expected_tasks": len(silver_report.get("tasks", [])),
            "matched_tasks": len(rows),
            "scored_tasks": len(scored),
            "inconclusive_tasks": len(rows) - len(scored) + len(missing),
            "tasks_with_locator_silver": sum(row["silver_locator_count"] > 0 for row in scored),
        },
        "metrics": {
            "macro_evidence_set_coverage": mean([r["evidence_set_coverage"] for r in scored]),
            "complete_evidence_set_success_rate": mean([r["complete_evidence_set_success"] for r in scored]),
            "receipt_pass_rate": mean([r["receipt_pass_rate"] for r in scored]),
            "evidence_binding_pass_rate": mean([r["evidence_binding_pass_rate"] for r in scored]),
        },
        "tasks": rows,
        "missing_task_ids": missing,
        "unscored_metrics": {
            "v7_paired_delta": "inconclusive: no equivalent frozen 12-task PR36-v7 run",
            "unsupported_factual_claim_rate": "inconclusive: requires independent semantic adjudication",
            "requirement_to_rubric_recall": "inconclusive: frozen artifact does not bind generated requirement IDs",
            "honest_gap_recall": "inconclusive: frozen artifact does not label expected gaps by generated requirement ID",
        },
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"ok": True, "out": str(out), "scored_tasks": len(scored), "inconclusive_tasks": report["denominators"]["inconclusive_tasks"]}))


if __name__ == "__main__":
    main()

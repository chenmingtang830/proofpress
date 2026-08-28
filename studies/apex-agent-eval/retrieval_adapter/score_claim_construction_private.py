#!/usr/bin/env python3
"""Score a private claim-construction run against pre-frozen locator silver."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import Any

PR36_V7_PROTOCOL = {
    "source_revision": "proofpress-pr36@9f6e3f1",
    "implementation": "frozen-reimplementation-v1",
    "decomposition_model": "gpt-5.6-luna",
    "retrieval": "bounded-lexical",
    "retrieval_config": {"max_documents_per_requirement": 10, "max_sections_per_requirement": 6},
    "proposer_model": "deepseek/deepseek-v4-flash",
    "critic_model": "gpt-5.6-sol",
}


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
    supported_requirement_ids = {claim.get("requirement_id") for claim in covered_claims
                                 if claim.get("requirement_id")}
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
        "supported_claim_coverage": (len(supported_requirement_ids) / len(statuses)) if statuses else None,
        "requirement_count": len(statuses),
        "evidence_binding_pass_count": binding_passes,
        "evidence_binding_pass_rate": (binding_passes / len(claims)) if claims else None,
        "explicit_partial_or_gap_count": gap_count,
        "critic_status": construction.get("critic_status"),
    }


def mean(values: list[float | bool | None]) -> float | None:
    kept = [float(v) for v in values if v is not None]
    return sum(kept) / len(kept) if kept else None


def bootstrap_95_ci(values: list[float], *, samples: int = 10_000) -> list[float] | None:
    """Return a deterministic paired bootstrap interval without inventing missing pairs."""
    if not values:
        return None
    if len(values) == 1:
        return [values[0], values[0]]
    rng = random.Random(0)
    draws = sorted(sum(rng.choice(values) for _ in values) / len(values) for _ in range(samples))
    return [draws[int(.025 * (samples - 1))], draws[int(.975 * (samples - 1))]]


def load_scored_tasks(run_report: dict[str, Any], silver_report: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    """Bind one frozen system run to silver without assuming the run is v7 or v8."""
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
    return rows, missing


def paired_metrics(v7_rows: list[dict[str, Any]], v8_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate paired denominators only for independently materialized, scored artifacts."""
    left = {row["task_id"]: row for row in v7_rows if row["status"] == "scored"}
    right = {row["task_id"]: row for row in v8_rows if row["status"] == "scored"}
    task_ids = sorted(left.keys() & right.keys())
    coverage_deltas = []
    binding_deltas = []
    receipt_deltas = []
    complete_set_deltas = []
    for task_id in task_ids:
        for key, target in (("evidence_set_coverage", coverage_deltas),
                            ("evidence_binding_pass_rate", binding_deltas),
                            ("receipt_pass_rate", receipt_deltas),
                            ("complete_evidence_set_success", complete_set_deltas)):
            a, b = left[task_id].get(key), right[task_id].get(key)
            if a is not None and b is not None:
                target.append(float(b) - float(a))
    return {
        "paired_task_ids": task_ids,
        "paired_task_count": len(task_ids),
        "confidence_interval_method": "paired_nonparametric_bootstrap_seed_0",
        "confidence_interval_samples": 10_000,
        "evidence_coverage_pair_count": len(coverage_deltas),
        "evidence_set_coverage_mean_delta_v8_minus_v7": mean(coverage_deltas),
        "evidence_set_coverage_delta_bootstrap_95_ci": bootstrap_95_ci(coverage_deltas),
        "evidence_binding_pair_count": len(binding_deltas),
        "evidence_binding_mean_delta_v8_minus_v7": mean(binding_deltas),
        "evidence_binding_delta_bootstrap_95_ci": bootstrap_95_ci(binding_deltas),
        "receipt_pass_pair_count": len(receipt_deltas),
        "receipt_pass_rate_mean_delta_v8_minus_v7": mean(receipt_deltas),
        "receipt_pass_rate_delta_bootstrap_95_ci": bootstrap_95_ci(receipt_deltas),
        "complete_evidence_set_pair_count": len(complete_set_deltas),
        "complete_evidence_set_success_mean_delta_v8_minus_v7": mean(complete_set_deltas),
        "complete_evidence_set_success_delta_bootstrap_95_ci": bootstrap_95_ci(complete_set_deltas),
        "v7_evidence_binding_pass_rate": mean([left[task_id].get("evidence_binding_pass_rate") for task_id in task_ids]),
        "v8_evidence_binding_pass_rate": mean([right[task_id].get("evidence_binding_pass_rate") for task_id in task_ids]),
        "requirement_recall_mean_delta_v8_minus_v7": None,
        "requirement_recall_delta_bootstrap_95_ci": None,
        "unsupported_factual_claim_rate_mean_delta_v8_minus_v7": None,
        "v8_honest_gap_recall": None,
        "missing_semantic_adjudication": ["requirement_to_rubric_mapping",
                                           "unsupported_factual_claim_labels",
                                           "expected_gap_labels"],
        "status": "locator_metrics_scored_semantic_metrics_missing" if task_ids else "inconclusive_no_common_scored_tasks",
    }


def semantic_paired_metrics(report: dict[str, Any], task_ids: list[str], candidate_label: str = "v8") -> dict[str, Any]:
    raw_dir = Path(report["raw_private_dir"])
    per_system: dict[str, dict[str, dict[str, float | None]]] = {"v7": {}, candidate_label: {}}
    missing = []
    for task_id in task_ids:
        path = raw_dir / f"{task_id}.json"
        if not path.is_file():
            missing.append(task_id); continue
        row = json.loads(path.read_text())
        rubric_ids = set(row.get("rubric_atom_ids", []))
        for system in ("v7", candidate_label):
            labels = row.get("labels", {}).get("systems", {}).get(system, {})
            mapped = {mapping.get("rubric_id") for mapping in labels.get("requirement_to_rubric", [])
                      if mapping.get("requirement_ids")}
            factual = set(labels.get("factual_claim_ids", []))
            unsupported = set(labels.get("unsupported_factual_claim_ids", []))
            expected = set(labels.get("expected_open_gap_requirement_ids", []))
            honest = set(labels.get("honest_open_gap_requirement_ids", []))
            per_system[system][task_id] = {
                "requirement_recall": len(mapped & rubric_ids) / len(rubric_ids) if rubric_ids else None,
                # A system that emits no factual claims has zero unsupported
                # factual claims.  Supported-claim coverage is scored
                # separately, so this cannot manufacture a qualification pass
                # by suppressing claims.
                "unsupported_factual_claim_rate": len(unsupported) / len(factual) if factual else 0.0,
                "honest_gap_recall": len(honest & expected) / len(expected) if expected else None,
            }
    output: dict[str, Any] = {"semantic_adjudication_status": "scored" if not missing else "partial",
                              "semantic_missing_task_ids": missing}
    for metric in ("requirement_recall", "unsupported_factual_claim_rate", "honest_gap_recall"):
        pairs = [(per_system["v7"].get(task_id, {}).get(metric),
                  per_system[candidate_label].get(task_id, {}).get(metric)) for task_id in task_ids]
        pairs = [(left, right) for left, right in pairs if left is not None and right is not None]
        deltas = [float(right) - float(left) for left, right in pairs]
        output[f"{metric}_pair_count"] = len(deltas)
        output[f"v7_{metric}"] = mean([left for left, _ in pairs])
        output[f"v8_{metric}"] = mean([right for _, right in pairs])
        output[f"candidate_{metric}"] = mean([right for _, right in pairs])
        output[f"{metric}_mean_delta_v8_minus_v7"] = mean(deltas)
        output[f"{metric}_delta_bootstrap_95_ci"] = bootstrap_95_ci(deltas)
    return output


def qualify_pair_reports(v7: dict[str, Any], v8: dict[str, Any]) -> dict[str, Any]:
    """Fail closed before pairing reports produced on different panels or corpora."""
    v7_ids = sorted(str(row.get("task_id")) for row in v7.get("tasks", []))
    v8_ids = sorted(str(row.get("task_id")) for row in v8.get("tasks", []))
    qualification_subset = bool(v8.get("qualification", {}).get("requested"))
    task_set_compatible = (set(v8_ids).issubset(v7_ids) if qualification_subset else v7_ids == v8_ids)
    checks = {
        "same_catalog_digest": bool(v7.get("catalog_digest")) and v7.get("catalog_digest") == v8.get("catalog_digest"),
        "task_set_compatible": bool(v8_ids) and task_set_compatible,
        "v7_system_labeled": v7.get("system") == "pr36-v7",
        "v7_protocol_frozen": all(v7.get("protocol", {}).get(key) == value
                                  for key, value in PR36_V7_PROTOCOL.items()),
        "candidate_system_labeled": v8.get("system") in {"v8", "evidence-first-v9"},
        "independent_raw_directories": bool(v7.get("raw_private_dir")) and
            Path(v7.get("raw_private_dir", "")).resolve() != Path(v8.get("raw_private_dir", "")).resolve(),
    }
    failures = [key for key, passed in checks.items() if not passed]
    return {"status": "pass" if not failures else "fail", "checks": checks,
            "failures": failures, "task_count": len(v8_ids),
            "task_set_mode": "qualification_v8_subset_of_v7" if qualification_subset else "formal_exact"}


def score_denominators(run_report: dict[str, Any], silver_report: dict[str, Any],
                       rows: list[dict[str, Any]], missing: list[str]) -> tuple[dict[str, int], list[str]]:
    run_task_ids = {str(row.get("task_id")) for row in run_report.get("tasks", [])}
    silver_task_ids = {str(row.get("task_id")) for row in silver_report.get("tasks", [])}
    absent_from_run = sorted(silver_task_ids - run_task_ids)
    scored = [row for row in rows if row["status"] == "scored"]
    return {
        "panel_expected_tasks": len(silver_task_ids),
        "run_expected_tasks": len(run_task_ids),
        "matched_tasks": len(rows),
        "scored_tasks": len(scored),
        "inconclusive_tasks": len(rows) - len(scored) + len(missing),
        "panel_tasks_absent_from_run": len(absent_from_run),
        "tasks_with_locator_silver": sum(row["silver_locator_count"] > 0 for row in scored),
    }, absent_from_run


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-report", required=True)
    ap.add_argument("--v7-run-report",
                    help="Independent frozen PR36-v7 report. Never synthesize v7 from v8 artifacts.")
    ap.add_argument("--silver-report", required=True)
    ap.add_argument("--semantic-report",
                    help="Optional post-output model-adjudicated semantic labels; never treated as pre-output silver.")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    run_report = json.loads(Path(args.run_report).read_text())
    silver_report = json.loads(Path(args.silver_report).read_text())
    rows, missing = load_scored_tasks(run_report, silver_report)
    scored = [row for row in rows if row["status"] == "scored"]
    denominators, absent_from_run = score_denominators(run_report, silver_report, rows, missing)
    report = {
        "schema_version": "proofpress/private-claim-construction-score/v2",
        "run_report_digest": digest(run_report),
        "silver_report_digest": digest(silver_report),
        "boundary": "Model-adjudicated pre-output locator silver, not human gold. No rubric or silver locator entered construction.",
        "denominators": denominators,
        "metrics": {
            "macro_evidence_set_coverage": mean([r["evidence_set_coverage"] for r in scored]),
            "complete_evidence_set_success_rate": mean([r["complete_evidence_set_success"] for r in scored]),
            "receipt_pass_rate": mean([r["receipt_pass_rate"] for r in scored]),
            "evidence_binding_pass_rate": mean([r["evidence_binding_pass_rate"] for r in scored]),
            "supported_claim_coverage": mean([r["supported_claim_coverage"] for r in scored]),
            "mean_requirement_count": mean([r["requirement_count"] for r in scored]),
        },
        "tasks": rows,
        "missing_task_ids": missing,
        "panel_task_ids_absent_from_run": absent_from_run,
        "unscored_metrics": {
            "unsupported_factual_claim_rate": "inconclusive: requires independent semantic adjudication",
            "requirement_to_rubric_recall": "inconclusive: frozen artifact does not bind generated requirement IDs",
            "honest_gap_recall": "inconclusive: frozen artifact does not label expected gaps by generated requirement ID",
        },
    }
    if args.v7_run_report:
        v7_report = json.loads(Path(args.v7_run_report).read_text())
        v7_rows, v7_missing = load_scored_tasks(v7_report, silver_report)
        report["v7_run_report_digest"] = digest(v7_report)
        candidate_label = run_report.get("system", "v8")
        report["candidate_label"] = candidate_label
        def system_summary(system_rows: list[dict[str, Any]], system_missing: list[str]) -> dict[str, Any]:
            scored_rows = [row for row in system_rows if row.get("status") == "scored"]
            return {"tasks": system_rows, "missing_task_ids": system_missing,
                    "supported_claim_coverage": mean([row.get("supported_claim_coverage") for row in scored_rows]),
                    "mean_requirement_count": mean([row.get("requirement_count") for row in scored_rows]),
                    "receipt_pass_rate": mean([row.get("receipt_pass_rate") for row in scored_rows]),
                    "evidence_binding_pass_rate": mean([row.get("evidence_binding_pass_rate") for row in scored_rows])}
        report["systems"] = {"pr36-v7": system_summary(v7_rows, v7_missing),
                             candidate_label: system_summary(rows, missing)}
        qualification = qualify_pair_reports(v7_report, run_report)
        report["pair_qualification"] = qualification
        report["paired"] = (paired_metrics(v7_rows, rows) if qualification["status"] == "pass"
                            else {"status": "inconclusive_pair_qualification_failed",
                                  "paired_task_count": 0, "failures": qualification["failures"]})
        if args.semantic_report and qualification["status"] == "pass":
            semantic_report = json.loads(Path(args.semantic_report).read_text())
            semantic_checks = {
                "schema": semantic_report.get("schema_version") == "proofpress/private-claim-semantic-adjudication/v1",
                "v7_report_digest": semantic_report.get("v7_report_digest") == digest(v7_report),
                "candidate_report_digest": (
                    semantic_report.get("candidate_report_digest", semantic_report.get("v8_report_digest"))
                    == digest(run_report)),
                "post_output_boundary": "Post-output" in str(semantic_report.get("boundary", "")),
            }
            report["semantic_qualification"] = {"status": "pass" if all(semantic_checks.values()) else "fail",
                                                "checks": semantic_checks}
            if all(semantic_checks.values()):
                semantic = semantic_paired_metrics(semantic_report, report["paired"]["paired_task_ids"],
                                                   semantic_report.get("candidate_label", candidate_label))
                complete = (semantic.get("semantic_adjudication_status") == "scored" and
                            semantic.get("requirement_recall_pair_count") == report["paired"]["paired_task_count"] and
                            semantic.get("unsupported_factual_claim_rate_pair_count") == report["paired"]["paired_task_count"])
                report["semantic_qualification"]["complete_paired_denominators"] = complete
                report["paired"].update(semantic)
                if complete:
                    report["paired"]["status"] = "scored_with_post_output_semantic_adjudication"
                    report["paired"]["requirement_recall_delta_bootstrap_95_ci"] = semantic.get("requirement_recall_delta_bootstrap_95_ci")
                    report["paired"]["unsupported_factual_claim_rate_mean_delta_v8_minus_v7"] = semantic.get("unsupported_factual_claim_rate_mean_delta_v8_minus_v7")
                    report["paired"]["v8_honest_gap_recall"] = semantic.get("v8_honest_gap_recall")
                    report["paired"]["missing_semantic_adjudication"] = []
                    report["unscored_metrics"] = {}
    else:
        report["paired"] = {"status": "inconclusive_missing_independent_v7_run",
                            "paired_task_count": 0,
                            "boundary": "No v7 values are imputed or reconstructed from v8."}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"ok": True, "out": str(out), "scored_tasks": len(scored), "inconclusive_tasks": report["denominators"]["inconclusive_tasks"]}))


if __name__ == "__main__":
    main()

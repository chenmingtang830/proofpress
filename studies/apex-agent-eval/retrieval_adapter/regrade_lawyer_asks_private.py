#!/usr/bin/env python3
"""Regrade frozen lawyer-ask artifacts without rerunning an executor.

This panel deliberately excludes the parent APEX task gold response and rubric.
It grades the answer to each frozen follow-up ask against an ask-specific rubric
and a bounded reference projection from the staged claim graph.
"""
from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from run_claim_construction_private import Gateway, _model_call, digest

SCHEMA = "proofpress/private-lawyer-ask-regrade/v1"
RUBRIC_VERSION = "proofpress/lawyer-follow-up-rubric/v1"
GRADER = ("google/gemini-3.1-pro-preview", "google", "low")
RUBRIC_ATOMS = (
    ("direct_answer", "Directly answers the frozen lawyer ask and stays relevant."),
    ("governed_claim_coverage", "Uses every material governed claim identified by the frozen ask reference, without substituting ungoverned material."),
    ("relation_reasoning", "Accurately explains the interaction between the referenced governed positions without inventing a legal conclusion."),
    ("gap_handling", "Clearly identifies what is unresolved or absent and does not turn missing evidence into a factual conclusion."),
    ("citation_traceability", "Material factual statements are traceable to supplied claim, evidence, source, or gap identifiers."),
    ("authority_boundary", "Keeps governed, staged, not_governed, proposed, and admitted authority states distinct."),
    ("lawyer_actionability", "States a usable conclusion or the concrete review, evidence, or decision needed next."),
)
CATEGORY_ATOMS = {
    "graph-fully-covered": {"direct_answer", "governed_claim_coverage", "citation_traceability", "authority_boundary", "lawyer_actionability"},
    "relation-dependent": {"direct_answer", "governed_claim_coverage", "relation_reasoning", "citation_traceability", "authority_boundary", "lawyer_actionability"},
    "partial-gap": {"direct_answer", "gap_handling", "citation_traceability", "authority_boundary", "lawyer_actionability"},
    "novel": {"direct_answer", "gap_handling", "authority_boundary", "lawyer_actionability"},
}

ATOM_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["atom_id", "applicable", "score", "finding"],
    "properties": {
        "atom_id": {"type": "string", "enum": [row[0] for row in RUBRIC_ATOMS]},
        "applicable": {"type": "boolean"},
        "score": {"type": "number", "enum": [0, 0.5, 1]},
        "finding": {"type": "string", "maxLength": 800},
    },
}
GRADE_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["atoms", "unsupported_claims", "citation_errors", "authority_errors"],
    "properties": {
        "atoms": {"type": "array", "minItems": len(RUBRIC_ATOMS),
                  "maxItems": len(RUBRIC_ATOMS), "items": ATOM_SCHEMA},
        "unsupported_claims": {"type": "integer", "minimum": 0},
        "citation_errors": {"type": "integer", "minimum": 0},
        "authority_errors": {"type": "integer", "minimum": 0},
    },
}


def applicable_atoms(category: str) -> set[str]:
    if category not in CATEGORY_ATOMS:
        raise ValueError(f"unknown lawyer-ask category: {category}")
    return CATEGORY_ATOMS[category]


def normalize_grade(value: Any, category: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not isinstance(value.get("atoms"), list):
        raise ValueError("grader omitted rubric atoms")
    expected_ids = {row[0] for row in RUBRIC_ATOMS}
    rows = value["atoms"]
    ids = [row.get("atom_id") for row in rows if isinstance(row, dict)]
    if len(ids) != len(expected_ids) or set(ids) != expected_ids:
        raise ValueError("grader must return each frozen rubric atom exactly once")
    applicable = applicable_atoms(category)
    normalized = []
    for row in rows:
        atom_id = row["atom_id"]
        should_apply = atom_id in applicable
        if row.get("applicable") is not should_apply:
            raise ValueError(f"grader changed applicability for {atom_id}")
        score = row.get("score")
        if score not in {0, 0.5, 1} or (not should_apply and score != 0):
            raise ValueError(f"invalid score for {atom_id}")
        normalized.append({"atom_id": atom_id, "applicable": should_apply,
                           "score": float(score), "finding": str(row.get("finding", ""))})
    counts = {}
    for key in ("unsupported_claims", "citation_errors", "authority_errors"):
        count = value.get(key)
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise ValueError(f"invalid {key}")
        counts[key] = count
    scored = [row["score"] for row in normalized if row["applicable"]]
    return {"rubric_fraction": sum(scored) / len(scored), "atoms": normalized, **counts}


def paired_bootstrap(values: list[float], samples: int = 10_000) -> list[float] | None:
    if not values:
        return None
    if len(values) == 1:
        return [values[0], values[0]]
    rng = random.Random(0)
    draws = sorted(statistics.mean(rng.choice(values) for _ in values) for _ in range(samples))
    return [draws[int(.025 * (samples - 1))], draws[int(.975 * (samples - 1))]]


def bounded_reference(graph: dict[str, Any], ask: dict[str, Any]) -> dict[str, Any]:
    construction = graph.get("construction", {})
    expected_claims = set(map(str, ask.get("expected_claim_ids", [])))
    expected_relations = set(map(str, ask.get("expected_relation_ids", [])))
    expected_gaps = set(map(str, ask.get("expected_gap_ids", [])))
    claims = [{key: row.get(key) for key in ("id", "statement", "claim_type", "status", "evidence_ids")}
              for row in construction.get("claims", []) if str(row.get("id")) in expected_claims]
    relations = []
    for row in construction.get("relations", []):
        relation_id = str(row.get("id") or digest(row))
        if relation_id in expected_relations:
            relations.append({**{key: row.get(key) for key in ("from", "to", "type", "status")},
                              "id": relation_id})
    gaps = [{key: row.get(key) for key in ("requirement_id", "requirement", "status", "gap_reason", "missing_evidence")}
            for row in construction.get("requirements", [])
            if str(row.get("requirement_id")) in expected_gaps]
    return {"expected_governed_claims": claims, "expected_relations": relations,
            "expected_gaps": gaps,
            "novel_absence_expected": ask.get("category") == "novel"}


def artifact_path(raw: Path, cell: dict[str, Any]) -> Path:
    model = str(cell["executor_model"]).replace("/", "_")
    return raw / f"{cell['ask_id']}-{cell['condition']}-{model}.json"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prior-report", required=True)
    ap.add_argument("--claim-report", required=True)
    ap.add_argument("--ask-manifest", required=True)
    ap.add_argument("--gateway-server", required=True)
    ap.add_argument("--receipt-log", action="append", default=[],
                    help="Receipt JSONL from an earlier resumable grading process")
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=1)
    args = ap.parse_args()
    if args.workers != 1:
        raise SystemExit("regrade is intentionally serial to avoid shared-provider load")

    prior_path = Path(args.prior_report)
    prior = json.loads(prior_path.read_text())
    claim_report = json.loads(Path(args.claim_report).read_text())
    manifest = json.loads(Path(args.ask_manifest).read_text())
    asks = {row["ask_id"]: row for row in manifest.get("asks", [])}
    graph_raw = Path(claim_report["raw_private_dir"])
    graphs = {task_id: json.loads((graph_raw / f"{task_id}.json").read_text())
              for task_id in manifest.get("task_ids", [])}
    prior_raw = prior_path.parent / "raw"
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw_out = out / "raw"; raw_out.mkdir(exist_ok=True); raw_out.chmod(0o700)
    gateway = Gateway(args.gateway_server, GRADER[0], GRADER[1], out, 300, GRADER[2],
                      structured_output=True)
    cells = []
    try:
        for prior_cell in prior.get("cells", []):
            if prior_cell.get("status") != "scored":
                continue
            ask = asks.get(prior_cell.get("ask_id"))
            if not ask:
                cells.append({**prior_cell, "status": "inconclusive", "reason": "ask missing from frozen manifest"})
                continue
            source = artifact_path(prior_raw, prior_cell)
            saved = json.loads(source.read_text())
            artifact = saved.get("artifact")
            reference = bounded_reference(graphs[ask["task_id"]], ask)
            rubric = [{"atom_id": atom_id, "criterion": criterion,
                       "applicable": atom_id in applicable_atoms(ask["category"])}
                      for atom_id, criterion in RUBRIC_ATOMS]
            prompt = {"ask": {key: ask.get(key) for key in ("ask_id", "category", "query")},
                      "rubric_version": RUBRIC_VERSION, "rubric_atoms": rubric,
                      "bounded_reference": reference, "candidate": artifact,
                      "instruction": ("Grade only the frozen follow-up ask. Do not grade the parent APEX task and do not infer missing gold content. "
                                      "Return every rubric atom exactly once. For non-applicable atoms set applicable=false and score=0. "
                                      "Use scores 0, 0.5, or 1. Count concrete unsupported claims, citation errors, and authority errors.")}
            grade_path = raw_out / source.name
            grades = []
            if grade_path.is_file():
                resumed = json.loads(grade_path.read_text())
                for value in resumed.get("grades", []):
                    try:
                        grades.append(normalize_grade(value, ask["category"]))
                    except ValueError:
                        pass
                grades = grades[:3]
            failures = []
            missing = 3 - len(grades)
            attempts = 0
            while len(grades) < 3 and attempts < missing * 3:
                attempts += 1
                attempt_prompt = dict(prompt)
                attempt_prompt["required_atom_order"] = [row[0] for row in RUBRIC_ATOMS]
                if failures:
                    attempt_prompt["correction"] = ("The previous grade was structurally invalid. Return exactly the seven atom IDs in required_atom_order, once each, without omissions or duplicates.")
                result = _model_call(gateway,
                    "You are an independent lawyer-follow-up evaluator. Use the required output tool.",
                    json.dumps(attempt_prompt, ensure_ascii=False), 6000, GRADE_SCHEMA,
                    "proofpress_lawyer_followup_grade")
                if not result["ok"]:
                    failures.append(str(result.get("record", {}).get("error_type") or "unknown")); continue
                try:
                    grades.append(normalize_grade(result["value"], ask["category"]))
                except ValueError as exc:
                    failures.append(str(exc))
            base = {key: prior_cell.get(key) for key in
                    ("task_id", "ask_id", "condition", "executor_model", "executor_provider", "executor_role",
                     "context_token_upper_bound", "artifact_digest")}
            if len(grades) != 3:
                cell = {**base, "status": "inconclusive", "valid_grade_count": len(grades),
                        "grade_failures": failures}
            else:
                cell = {**base, "status": "scored",
                        "rubric_fraction": statistics.mean(row["rubric_fraction"] for row in grades),
                        **{key: statistics.mean(row[key] for row in grades)
                           for key in ("unsupported_claims", "citation_errors", "authority_errors")}}
            cells.append(cell)
            grade_path.write_text(json.dumps({"source_artifact_digest": prior_cell.get("artifact_digest"),
                                               "grades": grades}, indent=2) + "\n")
    finally:
        gateway.stop()

    scored = [row for row in cells if row["status"] == "scored"]
    aggregate: dict[str, Any] = {}
    for condition in sorted({row["condition"] for row in scored}):
        rows = [row for row in scored if row["condition"] == condition]
        aggregate[condition] = {"scored_asks": len(rows),
            **{key: statistics.mean(row[key] for row in rows) for key in
               ("rubric_fraction", "unsupported_claims", "citation_errors", "authority_errors")}}
    comparisons = {}
    conditions = sorted(aggregate)
    by_key = {(row["ask_id"], row["condition"]): row for row in scored}
    for treatment in conditions:
        for baseline in conditions:
            if treatment >= baseline:
                continue
            ids = sorted({row["ask_id"] for row in scored
                          if (row["ask_id"], treatment) in by_key and (row["ask_id"], baseline) in by_key})
            deltas = [by_key[(unit, treatment)]["rubric_fraction"] - by_key[(unit, baseline)]["rubric_fraction"]
                      for unit in ids]
            comparisons[f"{treatment}|{baseline}"] = {"paired_asks": len(ids),
                "rubric_fraction_mean_delta": statistics.mean(deltas) if deltas else None,
                "rubric_fraction_bootstrap_95_ci": paired_bootstrap(deltas)}
    receipts = []
    for value in args.receipt_log:
        path = Path(value)
        if not path.is_file():
            raise SystemExit(f"receipt log unavailable: {path}")
        receipts.extend(json.loads(line) for line in path.read_text().splitlines() if line.strip())
    current_receipts = gateway.receipt_rows()
    receipts.extend(current_receipts)
    report = {"schema_version": SCHEMA, "rubric_version": RUBRIC_VERSION,
              "boundary": "Ask-specific regrade of frozen executor artifacts; parent task gold and rubric excluded.",
              "source_report_digest": digest(prior), "ask_manifest_digest": manifest.get("manifest_digest"),
              "rubric": [{"atom_id": atom_id, "criterion": criterion} for atom_id, criterion in RUBRIC_ATOMS],
              "category_applicability": {key: sorted(value) for key, value in CATEGORY_ATOMS.items()},
              "denominators": {"planned_cells": len([row for row in prior.get("cells", []) if row.get("status") == "scored"]),
                               "scored_cells": len(scored), "inconclusive_cells": len(cells) - len(scored),
                               "grades_per_artifact": 3},
              "aggregate": aggregate, "paired_comparisons": comparisons, "cells": cells,
              "grader": {"model": GRADER[0], "provider": GRADER[1], "reasoning": GRADER[2]},
              "telemetry": {"model_calls": len(receipts), "gateway_receipts": len(receipts),
                            "resumed_receipt_logs": len(args.receipt_log),
                            "unreceipted_model_calls": max(0, len(gateway.calls) - len(current_receipts)),
                            "nonterminal_receipts": sum(row.get("status") not in {"ok", "inconclusive"}
                                                        for row in receipts),
                            "missing_cost_receipts": sum(not isinstance(row.get("cost_usd"), (int, float))
                                                         for row in receipts),
                            "known_model_cost_usd": sum(row["cost_usd"] for row in receipts
                                                        if isinstance(row.get("cost_usd"), (int, float)))}}
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"ok": len(scored) == report["denominators"]["planned_cells"],
                      **report["denominators"], "report": str(out / "sanitized-report.json")}, sort_keys=True))


if __name__ == "__main__":
    main()

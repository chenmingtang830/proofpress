#!/usr/bin/env python3
"""Run one evaluation-only governed-reuse hop over an admitted native artifact."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from governed_workflow_contract import digest
from native_legal_artifact import file_digest
from run_claim_construction_private import Gateway, _model_call
from run_workflow_utility_private import bounded_json, normalize_grade


SCHEMA_VERSION = "proofpress/private-apex-legal-governed-reuse/v1"
REUSE_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["title", "authority_scope", "relied_on_artifact_digest",
                 "admission_receipt_digest", "actions", "gaps"],
    "properties": {
        "title": {"type": "string"},
        "authority_scope": {"type": "string"},
        "relied_on_artifact_digest": {"type": "string"},
        "admission_receipt_digest": {"type": "string"},
        "actions": {"type": "array", "minItems": 1, "items": {
            "type": "object", "additionalProperties": False,
            "required": ["action", "owner", "timing", "basis_ids"],
            "properties": {"action": {"type": "string"}, "owner": {"type": "string"},
                           "timing": {"type": "string"}, "basis_ids": {
                               "type": "array", "minItems": 1, "items": {"type": "string"}}}}},
        "gaps": {"type": "array", "items": {"type": "string"}},
    },
}
GRADE_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["rubric_fraction", "unsupported_claims", "citation_errors", "authority_errors"],
    "properties": {"rubric_fraction": {"type": "number", "minimum": 0, "maximum": 1},
                   "unsupported_claims": {"type": "integer", "minimum": 0},
                   "citation_errors": {"type": "integer", "minimum": 0},
                   "authority_errors": {"type": "integer", "minimum": 0}},
}


def select_source_cell(report: dict[str, Any], task_id: str, condition: str,
                       model: str) -> dict[str, Any]:
    rows = [row for row in report.get("cells", [])
            if row.get("task_id") == task_id and row.get("condition") == condition
            and row.get("executor_model") == model]
    if len(rows) != 1:
        raise ValueError("governed reuse requires exactly one source cell")
    row = rows[0]
    if (report.get("qualification", {}).get("status") != "pass" or row.get("status") != "scored"
            or not row.get("artifact_checks", {}).get("artifact_valid")
            or any(float(row.get(key, 1)) != 0 for key in
                   ("unsupported_claims", "citation_errors", "authority_errors"))):
        raise ValueError("source cell did not pass the preregistered admission gate")
    return row


def validate_reuse(value: dict[str, Any], artifact_digest: str,
                   receipt_digest: str) -> list[str]:
    failures = []
    authority_scope = str(value.get("authority_scope") or "").lower()
    if not all(term in authority_scope for term in
               ("evaluation-only", "governed reuse", "not matter authority")):
        failures.append("authority scope mismatch")
    if value.get("relied_on_artifact_digest") != artifact_digest:
        failures.append("artifact digest mismatch")
    if value.get("admission_receipt_digest") != receipt_digest:
        failures.append("admission receipt digest mismatch")
    allowed = {artifact_digest, receipt_digest}
    actions = value.get("actions") if isinstance(value.get("actions"), list) else []
    if not actions:
        failures.append("no downstream actions")
    for action in actions:
        basis = action.get("basis_ids") if isinstance(action, dict) else None
        if not isinstance(basis, list) or not basis or not set(map(str, basis)) <= allowed:
            failures.append("downstream action has an invalid governed basis")
            break
    return failures


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--formal-report", required=True)
    ap.add_argument("--artifact-json", required=True)
    ap.add_argument("--artifact-docx", required=True)
    ap.add_argument("--gateway-server", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--task-id", required=True)
    ap.add_argument("--condition", required=True)
    ap.add_argument("--resume-artifact",
                    help="Reuse a prior raw governed-reuse artifact for deterministic revalidation.")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw = out / "raw"; raw.mkdir(exist_ok=True); raw.chmod(0o700)
    report = json.loads(Path(args.formal_report).read_text())
    model, provider, reasoning = "openai/gpt-5.6-sol", "openai", "high"
    cell = select_source_cell(report, args.task_id, args.condition, model)
    artifact_docx = Path(args.artifact_docx)
    if file_digest(artifact_docx) != cell["artifact_digest"]:
        raise ValueError("materialized source artifact digest mismatch")
    persisted = json.loads(Path(args.artifact_json).read_text())
    artifact = persisted.get("artifact")
    if not isinstance(artifact, dict):
        raise ValueError("source artifact payload unavailable")
    admission = {
        "schema_version": "proofpress/evaluation-admission-receipt/v1",
        "state": "admitted",
        "scope": "evaluation-only:downstream-governed-reuse",
        "artifact_digest": cell["artifact_digest"],
        "reviewed_by": "human:staged-evaluation-reviewer",
        "attribution_basis": "explicit evaluation-fixture admission after native checks and three blind grades",
        "limitations": ["not lawyer approval", "not matter authority", "not reusable outside this isolated evaluation"],
        "source_report_digest": digest(report),
    }
    admission_digest = digest(admission)
    bounded_artifact, artifact_tokens = bounded_json(artifact, max_tokens=20_000)
    prompt = {
        "downstream_task": ("Prepare a buyer-side closing-counsel handoff checklist from the admitted amendment. "
                            "Include concrete pre-closing, post-closing, tax-risk, and indemnification actions. "
                            "Do not elevate this evaluation fixture into matter authority and preserve any gaps."),
        "governed_context": {"admission_receipt": admission,
                             "admission_receipt_digest": admission_digest,
                             "artifact": json.loads(bounded_artifact)},
        "required_authority_scope": "evaluation-only governed reuse; not matter authority",
        "required_basis_ids": [cell["artifact_digest"], admission_digest],
    }
    executor = grader = None
    calls: list[dict[str, Any]] = []
    receipts: list[dict[str, Any]] = []
    grade_failures: dict[str, int] = {}
    artifact_reused = bool(args.resume_artifact)
    if args.resume_artifact:
        prior = json.loads(Path(args.resume_artifact).read_text())
        value = prior["downstream_artifact"]
        grades = [normalize_grade(row) for row in prior.get("grades", [])]
    else:
        executor = Gateway(args.gateway_server, model, provider, out, 300, reasoning,
                           structured_output=True)
        grader = Gateway(args.gateway_server, "google/gemini-3.1-pro-preview", "google",
                         out, 300, "low", structured_output=True)
        try:
            generated = _model_call(executor, "You are downstream buyer's closing counsel in an isolated evaluation. Use only admitted governed context and the required output tool.",
                                    json.dumps(prompt, ensure_ascii=False), 8000,
                                    REUSE_SCHEMA, "proofpress_governed_reuse_handoff")
            if not generated["ok"]:
                raise RuntimeError("governed reuse executor failed closed")
            value = generated["value"]
            grades = []
            grade_prompt = {"task": prompt["downstream_task"], "candidate": value,
                            "admitted_artifact": json.loads(bounded_artifact),
                            "admission_receipt": admission,
                            "rubric": ["actionable pre-closing obligations", "actionable post-closing cooperation",
                                       "S-corporation tax-risk allocation", "seller indemnification protection",
                                       "exact governed basis digests", "evaluation-only authority boundary"],
                            "instruction": "Blindly grade only this downstream governed-reuse handoff."}
            for _ in range(3):
                graded = _model_call(grader, "You are the blind governed-reuse grader. Use the required output tool.",
                                     json.dumps(grade_prompt, ensure_ascii=False), 4096,
                                     GRADE_SCHEMA, "proofpress_governed_reuse_grade")
                if graded["ok"]:
                    try: grades.append(normalize_grade(graded["value"]))
                    except ValueError: grade_failures["InvalidSemanticGrade"] = grade_failures.get("InvalidSemanticGrade", 0) + 1
                else:
                    kind = str(graded.get("record", {}).get("error_type") or "unknown")
                    grade_failures[kind] = grade_failures.get(kind, 0) + 1
        finally:
            executor.stop(); grader.stop()
        calls = executor.calls + grader.calls
        receipts = executor.receipt_rows() + grader.receipt_rows()
    deterministic_failures = validate_reuse(value, cell["artifact_digest"], admission_digest)
    receipt_complete = (len(calls) == len(receipts)
                        and all(row.get("terminal") is True and row.get("fallback_used") is False
                                and row.get("cost_usd") is not None for row in receipts))
    passed = not deterministic_failures and len(grades) == 3 and receipt_complete
    (raw / "governed-reuse-artifact.json").write_text(json.dumps({"admission": admission,
        "admission_receipt_digest": admission_digest, "downstream_artifact": value,
        "grades": grades}, indent=2) + "\n")
    sanitized = {"schema_version": SCHEMA_VERSION, "status": "pass" if passed else "inconclusive",
        "boundary": "Isolated staged evaluation; explicit fixture admission is not lawyer approval or matter authority.",
        "source": {"task_id": args.task_id, "condition": args.condition, "executor_model": model,
                   "artifact_digest": cell["artifact_digest"], "source_rubric_fraction": cell["rubric_fraction"],
                   "source_governance_errors": {key: cell[key] for key in
                                                ("unsupported_claims", "citation_errors", "authority_errors")}},
        "admission": {"state": admission["state"], "scope": admission["scope"],
                      "reviewed_by": admission["reviewed_by"], "receipt_digest": admission_digest},
        "context_token_upper_bound": artifact_tokens,
        "deterministic_failures": deterministic_failures,
        "grades": {"valid": len(grades), "failure_types": grade_failures,
                   "rubric_fraction": sum(row["rubric_fraction"] for row in grades) / len(grades) if grades else None,
                   **{key: sum(row[key] for row in grades) / len(grades) if grades else None
                      for key in ("unsupported_claims", "citation_errors", "authority_errors")}},
        "telemetry": {"model_calls": len(calls), "terminal_receipts": len(receipts),
                      "receipt_complete": receipt_complete,
                      "artifact_and_grades_reused": artifact_reused,
                      "model_cost_usd": sum(float(row["cost_usd"]) for row in receipts
                                            if isinstance(row.get("cost_usd"), (int, float)))},
    }
    sanitized["report_digest"] = digest(sanitized)
    (out / "sanitized-report.json").write_text(json.dumps(sanitized, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": sanitized["status"], "valid_grades": len(grades),
                      "receipt_complete": receipt_complete}, sort_keys=True))


if __name__ == "__main__":
    main()

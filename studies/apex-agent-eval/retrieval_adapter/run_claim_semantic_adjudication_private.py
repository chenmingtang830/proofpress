#!/usr/bin/env python3
"""Post-output, model-adjudicated semantic labels for paired claim construction.

This is deliberately not pre-output silver. Rubric text, claims, prompts, and
item-level labels remain in the caller-owned private directory.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from run_claim_construction_private import Gateway, _model_call, _write_private, digest

SCHEMA = "proofpress/private-claim-semantic-adjudication/v1"
MODEL = "gpt-5.6-sol"
SYSTEM_LABEL_SCHEMA = {
    "type": "object", "required": ["requirement_to_rubric", "factual_claim_ids",
        "unsupported_factual_claim_ids", "expected_open_gap_requirement_ids",
        "honest_open_gap_requirement_ids", "gap_to_silver_candidates"],
    "properties": {
        "requirement_to_rubric": {"type": "array", "maxItems": 75, "items": {
            "type": "object", "required": ["rubric_id", "requirement_ids"],
            "properties": {"rubric_id": {"type": "string", "maxLength": 128},
                           "requirement_ids": {"type": "array", "maxItems": 40,
                                               "items": {"type": "string", "maxLength": 128}}},
            "additionalProperties": False}},
        "factual_claim_ids": {"type": "array", "maxItems": 64,
                              "items": {"type": "string", "maxLength": 128}},
        "unsupported_factual_claim_ids": {"type": "array", "maxItems": 64,
                                          "items": {"type": "string", "maxLength": 128}},
        "expected_open_gap_requirement_ids": {"type": "array", "maxItems": 40,
                                              "items": {"type": "string", "maxLength": 128}},
        "honest_open_gap_requirement_ids": {"type": "array", "maxItems": 40,
                                            "items": {"type": "string", "maxLength": 128}},
        "gap_to_silver_candidates": {"type": "array", "maxItems": 40, "items": {
            "type": "object", "required": ["requirement_id", "candidate_ids"],
            "properties": {"requirement_id": {"type": "string", "maxLength": 128},
                           "candidate_ids": {"type": "array", "maxItems": 30,
                                             "items": {"type": "string", "maxLength": 128}}},
            "additionalProperties": False}},
    }, "additionalProperties": False,
}
ADJUDICATION_SCHEMA = {
    "type": "object", "required": ["systems"],
    "properties": {"systems": {"type": "object", "required": ["system_a", "system_b"],
        "properties": {"system_a": SYSTEM_LABEL_SCHEMA, "system_b": SYSTEM_LABEL_SCHEMA},
        "additionalProperties": False}},
    "additionalProperties": False,
}


def _tasks(value: Any) -> list[dict[str, Any]]:
    rows = value.get("tasks", value) if isinstance(value, dict) else value
    if not isinstance(rows, list):
        raise ValueError("tasks manifest must contain an array")
    return [row for row in rows if isinstance(row, dict) and row.get("task_id")]


def _blind_order(task_id: str, candidate_label: str = "v8") -> tuple[str, str]:
    return (("v7", candidate_label) if int(digest(task_id)[-1], 16) % 2 == 0
            else (candidate_label, "v7"))


def _compact_system(raw: dict[str, Any]) -> dict[str, Any]:
    construction = raw.get("construction", {})
    evidence = {row.get("evidence_id"): {"quote": row.get("quote", "")[:600],
                                         "source_uri": row.get("source", {}).get("uri"),
                                         "locator": row.get("locator")}
                for row in construction.get("evidence", []) if row.get("evidence_id")}
    return {
        "requirements": [{key: row.get(key) for key in
                          ("requirement_id", "requirement", "applicability", "status")}
                         for row in construction.get("requirements", [])],
        "claims": [{key: row.get(key) for key in
                    ("id", "requirement_id", "claim_type", "statement", "evidence_ids")}
                   for row in construction.get("claims", [])],
        "evidence": evidence,
    }


def _ids(system: dict[str, Any]) -> tuple[set[str], set[str]]:
    return ({str(row.get("requirement_id")) for row in system["requirements"] if row.get("requirement_id")},
            {str(row.get("id")) for row in system["claims"] if row.get("id")})


def _normalize_labels(value: Any, aliases: dict[str, str], systems: dict[str, dict[str, Any]],
                      rubric_ids: set[str], silver_candidate_ids: set[str]) -> dict[str, Any]:
    if isinstance(value, dict) and isinstance(value.get("output"), dict):
        value = value["output"]
    if not isinstance(value, dict) or not isinstance(value.get("systems"), dict):
        raise ValueError("semantic adjudication must contain systems")
    normalized = {"systems": {}}
    for alias, real in aliases.items():
        row = value["systems"].get(alias)
        if not isinstance(row, dict):
            raise ValueError(f"missing blinded system {alias}")
        requirement_ids, claim_ids = _ids(systems[real])
        mappings = []
        for mapping in row.get("requirement_to_rubric", []):
            if not isinstance(mapping, dict) or mapping.get("rubric_id") not in rubric_ids:
                raise ValueError("unknown rubric mapping")
            refs = [str(x) for x in mapping.get("requirement_ids", [])]
            if not set(refs).issubset(requirement_ids):
                raise ValueError("unknown mapped requirement")
            mappings.append({"rubric_id": mapping["rubric_id"], "requirement_ids": sorted(set(refs))})
        factual = {str(x) for x in row.get("factual_claim_ids", [])}
        unsupported = {str(x) for x in row.get("unsupported_factual_claim_ids", [])}
        expected = {str(x) for x in row.get("expected_open_gap_requirement_ids", [])}
        honest = {str(x) for x in row.get("honest_open_gap_requirement_ids", [])}
        if not factual.issubset(claim_ids) or not unsupported.issubset(factual):
            raise ValueError("invalid factual claim labels")
        if not expected.issubset(requirement_ids) or not honest.issubset(expected):
            raise ValueError("invalid gap labels")
        gap_bindings = []
        for binding in row.get("gap_to_silver_candidates", []):
            if not isinstance(binding, dict) or str(binding.get("requirement_id")) not in expected:
                raise ValueError("invalid gap binding requirement")
            candidates = {str(x) for x in binding.get("candidate_ids", [])}
            if not candidates.issubset(silver_candidate_ids):
                raise ValueError("unknown silver candidate in gap binding")
            gap_bindings.append({"requirement_id": str(binding["requirement_id"]),
                                 "candidate_ids": sorted(candidates)})
        normalized["systems"][real] = {
            "requirement_to_rubric": mappings,
            "factual_claim_ids": sorted(factual),
            "unsupported_factual_claim_ids": sorted(unsupported),
            "expected_open_gap_requirement_ids": sorted(expected),
            "honest_open_gap_requirement_ids": sorted(honest),
            "gap_to_silver_candidates": gap_bindings,
        }
    return normalized


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks-json", required=True)
    ap.add_argument("--v7-report", required=True)
    ap.add_argument("--v8-report", help="Legacy candidate report flag")
    ap.add_argument("--candidate-report", help="Candidate report compared with frozen v7")
    ap.add_argument("--candidate-label", default="v8")
    ap.add_argument("--silver-report", required=True)
    ap.add_argument("--gateway-server", required=True)
    ap.add_argument("--provider", default="openai")
    ap.add_argument("--reasoning", default="low")
    ap.add_argument("--timeout", type=float, default=180)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    candidate_path = args.candidate_report or args.v8_report
    if not candidate_path:
        ap.error("--candidate-report is required")
    if args.candidate_label == "v7" or not args.candidate_label:
        ap.error("--candidate-label must identify the non-v7 system")
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    task_rows = _tasks(json.loads(Path(args.tasks_json).read_text()))
    task_by_id = {row["task_id"]: row for row in task_rows}
    candidate_label = args.candidate_label
    reports = {"v7": json.loads(Path(args.v7_report).read_text()),
               candidate_label: json.loads(Path(candidate_path).read_text())}
    silver = json.loads(Path(args.silver_report).read_text())
    silver_ids = {row.get("task_id") for row in silver.get("tasks", [])}
    report_ids = [{row.get("task_id") for row in reports[name].get("tasks", [])}
                  for name in ("v7", candidate_label)]
    candidate_ids = report_ids[1]
    candidate_is_qualification = bool(reports[candidate_label].get("qualification", {}).get("requested"))
    if candidate_is_qualification:
        if not candidate_ids.issubset(report_ids[0]):
            raise SystemExit("qualification candidate tasks must be a subset of the frozen v7 task set")
    elif report_ids[0] != candidate_ids:
        raise SystemExit("formal semantic adjudication requires an exact paired task set")
    missing_tasks = sorted(candidate_ids - set(task_by_id))
    missing_silver = sorted(candidate_ids - silver_ids)
    if missing_tasks or missing_silver:
        raise SystemExit(f"paired tasks missing from frozen inputs: tasks={missing_tasks}, silver={missing_silver}")
    task_ids = sorted(candidate_ids)
    if not task_ids or len(task_ids) > 40:
        raise SystemExit("semantic adjudication requires 1..40 paired tasks")
    gateway = Gateway(args.gateway_server, MODEL, args.provider, out, args.timeout, args.reasoning,
                      structured_output=True)
    summaries = []
    try:
        for task_id in task_ids:
            systems = {}
            for name in ("v7", candidate_label):
                raw = Path(reports[name]["raw_private_dir"]) / f"{task_id}.json"
                if not raw.is_file():
                    systems = {}; break
                systems[name] = _compact_system(json.loads(raw.read_text()))
            if len(systems) != 2:
                summaries.append({"task_id": task_id, "status": "inconclusive_missing_raw"}); continue
            first, second = _blind_order(task_id, candidate_label)
            aliases = {"system_a": first, "system_b": second}
            task = task_by_id[task_id]
            rubric = [{"rubric_id": row.get("verifier_id"), "criteria": row.get("criteria")}
                      for row in task.get("rubric", []) if row.get("verifier_id")]
            silver_raw_path = Path(args.silver_report).parent / "raw" / f"{task_id}.json"
            silver_raw = json.loads(silver_raw_path.read_text()) if silver_raw_path.is_file() else {}
            silver_locators = [{"candidate_id": row.get("candidate_id"),
                                "source_uri": row.get("source_uri"), "locator": row.get("locator")}
                               for row in silver_raw.get("locators", []) if row.get("candidate_id")]
            payload = {"task": task.get("prompt"), "rubric_atoms": rubric,
                       "frozen_silver_locators": silver_locators,
                       "systems": {alias: systems[real] for alias, real in aliases.items()},
                       "instruction": "Post-output semantic adjudication only. For each blinded system return requirement_to_rubric mappings, factual_claim_ids, unsupported_factual_claim_ids, expected_open_gap_requirement_ids, the subset honest_open_gap_requirement_ids, and gap_to_silver_candidates binding each expected gap to only the frozen silver candidate IDs needed to resolve it. Use only supplied IDs. Do not answer the task."}
            labels = None
            result = None
            semantic_validation_failures: list[str] = []
            # JSON Schema cannot express cross-field set constraints such as
            # unsupported_factual_claim_ids being a subset of
            # factual_claim_ids.  Retry the same fixed route with a compact
            # correction, rather than silently dropping unknown IDs or making
            # the whole task inconclusive after one otherwise valid tool call.
            for semantic_attempt in range(3):
                attempt_payload = dict(payload)
                if semantic_validation_failures:
                    attempt_payload["correction"] = {
                        "attempt": semantic_attempt + 1,
                        "previous_validation_failure": semantic_validation_failures[-1],
                        "instruction": "Return the complete adjudication again. Use only supplied IDs and satisfy every cross-field subset constraint.",
                    }
                result = _model_call(
                    gateway,
                    "You are an independent legal coverage adjudicator. Systems are blinded. Return compact JSON only.",
                    json.dumps(attempt_payload, ensure_ascii=False), 16000,
                    ADJUDICATION_SCHEMA, "proofpress_claim_semantic_adjudication")
                if not result["ok"]:
                    break
                try:
                    labels = _normalize_labels(
                        result["value"], aliases, systems,
                        {row["rubric_id"] for row in rubric},
                        {row["candidate_id"] for row in silver_locators})
                    break
                except ValueError as exc:
                    semantic_validation_failures.append(str(exc))
            if result is None or not result["ok"]:
                summaries.append({"task_id": task_id, "status": "inconclusive_model",
                                  "semantic_attempts": len(semantic_validation_failures) + 1,
                                  "semantic_correction_retries": len(semantic_validation_failures),
                                  "reason_digest": digest(result["record"] if result else {"missing": True})}); continue
            if labels is None:
                summaries.append({"task_id": task_id, "status": "inconclusive_schema",
                                  "semantic_attempts": len(semantic_validation_failures),
                                  "semantic_correction_retries": max(0, len(semantic_validation_failures) - 1),
                                  "validation_failure_types": sorted(set(semantic_validation_failures)),
                                  "reason_digest": digest({"failures": semantic_validation_failures})}); continue
            private_row = {"schema_version": SCHEMA, "task_id": task_id,
                           "boundary": "post-output model-adjudicated; not pre-output silver or human gold",
                           "blind_order_digest": digest(aliases),
                           "rubric_atom_ids": sorted(row["rubric_id"] for row in rubric),
                           "labels": labels}
            _write_private(out / "raw" / f"{task_id}.json", private_row)
            summaries.append({"task_id": task_id, "status": "ok", "label_digest": digest(labels),
                              "semantic_attempts": len(semantic_validation_failures) + 1,
                              "semantic_correction_retries": len(semantic_validation_failures),
                              "rubric_atom_count": len(rubric),
                              "v7_requirement_mapping_count": len(labels["systems"]["v7"]["requirement_to_rubric"]),
                              "candidate_requirement_mapping_count": len(labels["systems"][candidate_label]["requirement_to_rubric"])})
    finally:
        gateway.stop()
    calls, receipts = gateway.calls, gateway.receipt_rows()
    known_costs = [float(row["cost_usd"]) for row in receipts
                   if isinstance(row.get("cost_usd"), (int, float))]
    sanitized = {"schema_version": SCHEMA,
                 "boundary": "Post-output Sol model-adjudicated semantic labels; not pre-output silver, human gold, or admission.",
                 "model": MODEL, "provider": args.provider, "fallback": "forbidden",
                 "task_set_digest": digest(task_ids), "v7_report_digest": digest(reports["v7"]),
                 "candidate_label": candidate_label,
                 "candidate_report_digest": digest(reports[candidate_label]),
                 "v8_report_digest": digest(reports[candidate_label]) if candidate_label == "v8" else None,
                 "silver_report_digest": digest(silver),
                 "denominators": {"eligible_tasks": len(task_ids),
                                  "completed_tasks": sum(row["status"] == "ok" for row in summaries),
                                  "inconclusive_tasks": sum(row["status"] != "ok" for row in summaries)},
                 "tasks": summaries, "telemetry": {"calls": len(calls), "terminal_receipts": len(receipts),
                                                    "semantic_correction_retries": sum(
                                                        int(row.get("semantic_correction_retries", 0))
                                                        for row in summaries),
                                                    "known_cost_usd": sum(known_costs),
                                                    "cost_usd": sum(known_costs) if len(known_costs) == len(receipts) == len(calls) else None},
                 "raw_private_dir": str(out / "raw")}
    _write_private(out / "sanitized-report.json", sanitized)
    print(json.dumps({"ok": True, "report": str(out / "sanitized-report.json"),
                      "completed": sanitized["denominators"]["completed_tasks"]}))


if __name__ == "__main__":
    main()

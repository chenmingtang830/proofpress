#!/usr/bin/env python3
"""Qualify atomic v10 legal requirement decomposition on the frozen dev split."""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
from typing import Any

from governed_workflow_contract import digest, validate_profile
from run_claim_construction_private import Gateway, SectionIndex, _model_call
from run_model_routing_qualification_private import terminal_telemetry
from run_v10_role_matrix_private import MODELS

SCHEMA = "proofpress/v10-decomposition-matrix/v1"
EVIDENCE_TYPES = ("document_fact", "quantitative_term", "obligation", "condition",
                  "exception", "conflict", "missing_input", "domain_analysis")
REQUIREMENT_ITEM = {
    "type": "object", "additionalProperties": False,
    "required": ["requirement_id", "requirement", "category", "type",
                 "lifecycle_category", "evidence_search_queries", "applicability",
                 "rationale", "required_evidence_type"],
    "properties": {
        "requirement_id": {"type": "string", "maxLength": 96},
        "requirement": {"type": "string", "maxLength": 500},
        "category": {"type": "string", "maxLength": 96},
        "type": {"type": "string", "enum": ["factual_input", "risk_signal", "contract_allocation"]},
        "lifecycle_category": {"type": "string", "maxLength": 96},
        "evidence_search_queries": {"type": "array", "minItems": 1, "maxItems": 4,
                                    "items": {"type": "string", "maxLength": 300}},
        "applicability": {"type": "string", "enum": ["applicable", "not_applicable", "uncertain"]},
        "rationale": {"type": "string", "maxLength": 500},
        "required_evidence_type": {"type": "string", "enum": list(EVIDENCE_TYPES)},
    },
}
DECOMPOSITION_OUTPUT = {"type": "object", "additionalProperties": False,
                        "required": ["requirements"],
                        "properties": {"requirements": {"type": "array", "minItems": 1,
                                                          "maxItems": 40,
                                                          "items": REQUIREMENT_ITEM}}}
JUDGMENT_OUTPUT = {
    "type": "object", "additionalProperties": False,
    "required": ["rubric_mappings", "requirement_judgments"],
    "properties": {
        "rubric_mappings": {"type": "array", "maxItems": 80, "items": {
            "type": "object", "additionalProperties": False,
            "required": ["rubric_id", "requirement_ids"],
            "properties": {"rubric_id": {"type": "string", "maxLength": 96},
                           "requirement_ids": {"type": "array", "maxItems": 8,
                                               "items": {"type": "string", "maxLength": 96}}}}},
        "requirement_judgments": {"type": "array", "maxItems": 40, "items": {
            "type": "object", "additionalProperties": False,
            "required": ["requirement_id", "atomic", "overbroad", "duplicate_of",
                         "applicability_correct"],
            "properties": {"requirement_id": {"type": "string", "maxLength": 96},
                           "atomic": {"type": "boolean"}, "overbroad": {"type": "boolean"},
                           "duplicate_of": {"type": ["string", "null"], "maxLength": 96},
                           "applicability_correct": {"type": "boolean"}}}},
    },
}


def safe_requirements(value: Any, profile: dict[str, Any]) -> list[dict[str, Any]]:
    rows = value.get("requirements", []) if isinstance(value, dict) else []
    categories = set(profile["requirement_categories"])
    result = []; seen = set()
    for index, raw in enumerate(rows, 1):
        if not isinstance(raw, dict):
            continue
        row = dict(raw); requirement_id = str(row.get("requirement_id") or f"req_{index:02d}")
        if requirement_id in seen or not str(row.get("requirement", "")).strip():
            continue
        if row.get("lifecycle_category") not in categories:
            row["lifecycle_category"] = "missing_evidence_negotiated_inputs"
        row["requirement_id"] = requirement_id; seen.add(requirement_id); result.append(row)
    return result[:40]


def call_decomposer(gateway: Gateway, task: dict[str, Any], inventory: list[dict[str, Any]],
                    profile: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    payload = {"task": task["prompt"], "source_inventory": inventory,
               "domain_profile": {"profile_id": profile["profile_id"],
                                  "requirement_categories": profile["requirement_categories"],
                                  "conflict_rules": profile["conflict_rules"]},
               "instruction": "Return atomic evidence requirements, not an answer. Split independent facts, obligations, exceptions, and conflicts. required_evidence_type must state what would make the requirement complete. Do not use rubric, gold, silver locators, or task instructions as facts."}
    result = _model_call(gateway, "Decompose a legal-matter task into frozen atomic retrieval requirements.",
                         json.dumps(payload, ensure_ascii=False), 16000,
                         DECOMPOSITION_OUTPUT, "proofpress_v10_requirements", 2)
    if not result["ok"]:
        return [], {"status": "inconclusive", "failure": result["record"]}
    rows = safe_requirements(result["value"], profile)
    return rows, {"status": "ok" if rows else "schema_failure", "requirement_count": len(rows)}


def rubric_atoms(task: dict[str, Any]) -> list[dict[str, str]]:
    rows = task.get("rubric") or []
    result = []
    for index, row in enumerate(rows, 1):
        if isinstance(row, str):
            result.append({"rubric_id": f"rubric_{index:02d}", "text": row})
        elif isinstance(row, dict):
            result.append({"rubric_id": str(row.get("rubric_id") or row.get("id") or f"rubric_{index:02d}"),
                           "text": str(row.get("text") or row.get("requirement") or row.get("description") or row)})
    return result


def call_judge(gateway: Gateway, task: dict[str, Any], requirements: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    rubric = rubric_atoms(task)
    payload = {"task": task["prompt"], "rubric_atoms": rubric,
               "requirements": requirements,
               "instruction": "This is post-output development scoring. Map each rubric atom to responsive requirements and judge each requirement's atomicity, breadth, duplication, and applicability. Do not rewrite requirements or grant authority."}
    result = _model_call(gateway, "You are a blinded decomposition quality adjudicator.",
                         json.dumps(payload, ensure_ascii=False), 14000,
                         JUDGMENT_OUTPUT, "proofpress_v10_decomposition_judgment", 2)
    if not result["ok"]:
        return {}, {"status": "inconclusive", "failure": result["record"]}
    known_requirements = {row["requirement_id"] for row in requirements}
    known_rubric = {row["rubric_id"] for row in rubric}
    mappings = []
    for row in result["value"].get("rubric_mappings", []):
        rubric_id = row.get("rubric_id")
        ids = [rid for rid in dict.fromkeys(row.get("requirement_ids", [])) if rid in known_requirements]
        if rubric_id in known_rubric:
            mappings.append({"rubric_id": rubric_id, "requirement_ids": ids})
    by_requirement = {row.get("requirement_id"): row for row in result["value"].get("requirement_judgments", [])
                      if row.get("requirement_id") in known_requirements}
    judgments = [by_requirement.get(rid, {"requirement_id": rid, "atomic": False,
                                         "overbroad": True, "duplicate_of": None,
                                         "applicability_correct": False})
                 for rid in sorted(known_requirements)]
    mapped_rubric = {row["rubric_id"] for row in mappings if row["requirement_ids"]}
    mapped_requirements = {rid for row in mappings for rid in row["requirement_ids"]}
    metrics = {"rubric_count": len(rubric), "requirement_count": len(requirements),
               "rubric_recall": len(mapped_rubric) / len(rubric) if rubric else None,
               "requirement_precision": len(mapped_requirements) / len(requirements) if requirements else None,
               "atomicity_rate": sum(row["atomic"] for row in judgments) / len(judgments) if judgments else None,
               "overbroad_rate": sum(row["overbroad"] for row in judgments) / len(judgments) if judgments else None,
               "duplicate_rate": sum(row.get("duplicate_of") is not None for row in judgments) / len(judgments) if judgments else None,
               "applicability_accuracy": sum(row["applicability_correct"] for row in judgments) / len(judgments) if judgments else None}
    return {"mappings": mappings, "judgments": judgments, "metrics": metrics}, {"status": "ok"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--diagnostic", required=True)
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--v7-raw", required=True)
    parser.add_argument("--gateway-server", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--budget-usd", type=float, default=10.0)
    parser.add_argument("--timeout", type=float, default=300)
    args = parser.parse_args()
    diagnostic = Path(args.diagnostic).resolve()
    source_paths = sorted((diagnostic.parent / "raw" / "sol" / "receipt_preproposal").glob("*.json"))
    if len(source_paths) != 4:
        raise SystemExit("decomposition matrix requires four frozen tasks")
    missing_v7 = [path.name for path in source_paths
                  if not (Path(args.v7_raw) / path.name).is_file()]
    if missing_v7:
        raise SystemExit("v7 comparator task set is incomplete: " + ",".join(missing_v7))
    profile = validate_profile(json.loads(Path(args.profile).read_text()))
    inventory = SectionIndex(json.loads(Path(args.catalog).read_text())).inventory()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw = out / "raw"; raw.mkdir(exist_ok=True); raw.chmod(0o700)
    decomposers = {label: Gateway(args.gateway_server, route["model"], route["provider"], out,
                                  args.timeout, route["reasoning"], structured_output=True)
                   for label, route in MODELS.items()}
    judges = {label: Gateway(args.gateway_server, MODELS["sol"]["model"], MODELS["sol"]["provider"], out,
                             args.timeout, MODELS["sol"]["reasoning"], structured_output=True)
              for label in (*MODELS, "v7")}
    gateways = {**{f"decomposer_{key}": value for key, value in decomposers.items()},
                **{f"judge_{key}": value for key, value in judges.items()}}
    tasks = []
    try:
        for source_path in source_paths:
            source = json.loads(source_path.read_text()); task = source["task"]
            variants = {}; statuses = {}
            with ThreadPoolExecutor(max_workers=4) as pool:
                futures = {pool.submit(call_decomposer, gateway, task, inventory, profile): label
                           for label, gateway in decomposers.items()}
                for future in as_completed(futures):
                    label = futures[future]; rows, status = future.result()
                    variants[label] = {"requirements": rows}; statuses[f"decomposer_{label}"] = status
            v7_path = Path(args.v7_raw) / source_path.name
            v7 = json.loads(v7_path.read_text())
            variants["v7"] = {"requirements": v7["decomposition"]["requirements"]}
            with ThreadPoolExecutor(max_workers=5) as pool:
                futures = {pool.submit(call_judge, judges[label], task, value["requirements"]): label
                           for label, value in variants.items()}
                for future in as_completed(futures):
                    label = futures[future]; judgment, status = future.result()
                    variants[label]["judgment"] = judgment; statuses[f"judge_{label}"] = status
            private = {"task_id": source_path.stem, "variants": variants, "statuses": statuses}
            target = raw / source_path.name
            target.write_text(json.dumps(private, ensure_ascii=False, indent=2, sort_keys=True) + "\n"); target.chmod(0o600)
            tasks.append({"task_id": source_path.stem,
                          "status": "ok" if all(row["status"] == "ok" for row in statuses.values()) else "inconclusive",
                          "variants": {label: value.get("judgment", {}).get("metrics", {})
                                       for label, value in variants.items()},
                          "artifact_digest": digest(private)})
            telemetry = terminal_telemetry(gateways)
            if telemetry["known_cost_usd"] > args.budget_usd:
                raise RuntimeError("decomposition matrix exceeded hard budget")
    finally:
        for gateway in gateways.values(): gateway.stop()
    telemetry = terminal_telemetry(gateways); summary = []
    for label in (*MODELS, "v7"):
        rows = [task["variants"][label] for task in tasks if task["status"] == "ok"]
        weights = sum(row.get("rubric_count", 0) for row in rows)
        requirements = sum(row.get("requirement_count", 0) for row in rows)
        summary.append({"system": label, "tasks": len(rows), "requirements": requirements,
                        "rubric_recall": sum((row.get("rubric_recall") or 0) * row.get("rubric_count", 0) for row in rows) / weights if weights else None,
                        "requirement_precision": sum((row.get("requirement_precision") or 0) * row.get("requirement_count", 0) for row in rows) / requirements if requirements else None,
                        "atomicity_rate": sum((row.get("atomicity_rate") or 0) * row.get("requirement_count", 0) for row in rows) / requirements if requirements else None,
                        "overbroad_rate": sum((row.get("overbroad_rate") or 0) * row.get("requirement_count", 0) for row in rows) / requirements if requirements else None,
                        "duplicate_rate": sum((row.get("duplicate_rate") or 0) * row.get("requirement_count", 0) for row in rows) / requirements if requirements else None,
                        "applicability_accuracy": sum((row.get("applicability_accuracy") or 0) * row.get("requirement_count", 0) for row in rows) / requirements if requirements else None})
    report = {"schema_version": SCHEMA,
              "boundary": "Four-task development tuning; rubric is used only by post-output Sol adjudication and is model reference, not human gold.",
              "models": MODELS, "profile_digest": profile["profile_digest"],
              "catalog_digest": digest(json.loads(Path(args.catalog).read_text())),
              "summary": summary,
              "tasks": [{key: row[key] for key in ("task_id", "status", "variants", "artifact_digest")} for row in tasks],
              "telemetry": {**telemetry, "budget_usd": args.budget_usd},
              "qualification": {"status": "pass" if len(tasks) == 4 and all(row["status"] == "ok" for row in tasks) and not telemetry["missing_cost_calls"] else "inconclusive"},
              "raw_private_dir": str(raw)}
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["qualification"]["status"], "cost_usd": telemetry["known_cost_usd"]}, sort_keys=True))


if __name__ == "__main__":
    main()

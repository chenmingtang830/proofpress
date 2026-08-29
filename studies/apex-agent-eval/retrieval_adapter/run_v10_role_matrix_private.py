#!/usr/bin/env python3
"""Run the frozen four-task v10 extractor/proposer/critic role matrix privately."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import time
from typing import Any

from governed_workflow_contract import (
    ATOM_SCHEMA, CRITIC_FIELDS, CRITIC_SCHEMA, apply_layered_verdicts,
    claimability_decision, digest, validate_compiled_claim,
)
from run_claim_construction_private import Gateway, _model_call
from run_model_routing_qualification_private import terminal_telemetry

SCHEMA = "proofpress/v10-role-matrix/v1"
MODELS = {
    "deepseek": {"model": "deepseek/deepseek-v4-flash", "provider": "alibaba", "reasoning": "none"},
    "ling": {"model": "inclusionai/ling-3.0-flash-fin", "provider": "novita", "reasoning": "high"},
    "qwen": {"model": "alibaba/qwen3.8-27b", "provider": "alibaba", "reasoning": "high"},
    "sol": {"model": "openai/gpt-5.6-sol", "provider": "openai", "reasoning": "low"},
}
ATOM_ITEM = {
    "type": "object", "additionalProperties": False,
    "required": ["requirement_id", "evidence_id", "exact_excerpt", "subject",
                 "predicate", "value", "effective_date", "qualification",
                 "document_version", "support_mode", "conflict_group"],
    "properties": {
        "requirement_id": {"type": "string", "maxLength": 96},
        "evidence_id": {"type": "string", "maxLength": 96},
        "exact_excerpt": {"type": "string", "maxLength": 1200},
        "subject": {"type": "string", "maxLength": 300},
        "predicate": {"type": "string", "maxLength": 240},
        "value": {"type": "string", "maxLength": 500},
        "effective_date": {"type": ["string", "null"], "maxLength": 96},
        "qualification": {"type": ["string", "null"], "maxLength": 500},
        "document_version": {"type": ["string", "null"], "maxLength": 160},
        "support_mode": {"type": "string", "enum": ["explicit", "inferred"]},
        "conflict_group": {"type": ["string", "null"], "maxLength": 96},
    },
}
ATOM_OUTPUT = {"type": "object", "additionalProperties": False, "required": ["atoms"],
               "properties": {"atoms": {"type": "array", "maxItems": 32,
                                           "items": ATOM_ITEM}}}
CLAIM_ITEM = {
    "type": "object", "additionalProperties": False,
    "required": ["requirement_id", "claim_type", "statement", "atom_ids",
                 "qualification", "status"],
    "properties": {
        "requirement_id": {"type": "string", "maxLength": 96},
        "claim_type": {"type": "string", "enum": ["observed_fact", "risk_signal",
                                                       "domain_conclusion", "allocation"]},
        "statement": {"type": "string", "maxLength": 800},
        "atom_ids": {"type": "array", "minItems": 1, "maxItems": 4,
                     "items": {"type": "string", "maxLength": 96}},
        "qualification": {"type": ["string", "null"], "maxLength": 500},
        "status": {"type": "string", "enum": ["unresolved"]},
    },
}
CLAIM_OUTPUT = {"type": "object", "additionalProperties": False, "required": ["claims"],
                "properties": {"claims": {"type": "array", "maxItems": 32,
                                            "items": CLAIM_ITEM}}}
VERDICT_ITEM = {
    "type": "object", "additionalProperties": False,
    "required": ["claim_id", *CRITIC_FIELDS, "verdict", "failure_reasons"],
    "properties": {
        "claim_id": {"type": "string", "maxLength": 96},
        **{field: {"type": "boolean"} for field in CRITIC_FIELDS},
        "verdict": {"type": "string", "enum": ["supported", "unsupported"]},
        "failure_reasons": {"type": "array", "maxItems": 8,
                            "items": {"type": "string", "maxLength": 160}},
    },
}
VERDICT_OUTPUT = {"type": "object", "additionalProperties": False, "required": ["verdicts"],
                  "properties": {"verdicts": {"type": "array", "maxItems": 64,
                                                "items": VERDICT_ITEM}}}


def _receipts(construction: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result = {}
    for row in construction.get("evidence", []):
        source = row.get("source") or {}
        result[row["evidence_id"]] = {
            "evidence_id": row["evidence_id"], "receipt_digest": row["receipt_digest"],
            "source_digest": source.get("content_digest"), "custody_valid": True,
            "quote": row["quote"], "locator": row["locator"],
        }
    return result


def _span(excerpt: str, value: str) -> dict[str, int] | None:
    start = excerpt.casefold().find(value.strip().casefold())
    return None if start < 0 else {"start": start, "end": start + len(value.strip())}


def normalize_atoms(value: Any, requirements: list[dict[str, Any]],
                    receipts: dict[str, dict[str, Any]], audit: list[dict[str, Any]]) -> list[dict[str, Any]]:
    known_requirements = {row["requirement_id"] for row in requirements}
    allowed = {row["requirement_id"]: set(row.get("evidence_ids", [])) for row in audit}
    rows = value.get("atoms", []) if isinstance(value, dict) else []
    atoms = []
    seen = set()
    for raw in rows:
        requirement_id, evidence_id = raw.get("requirement_id"), raw.get("evidence_id")
        if requirement_id not in known_requirements or evidence_id not in allowed.get(requirement_id, set()):
            continue
        receipt = receipts[evidence_id]
        excerpt = str(raw.get("exact_excerpt", ""))
        if not excerpt or excerpt not in receipt["quote"]:
            continue
        bindings = {field: _span(excerpt, str(raw.get(field, "")))
                    for field in ("subject", "predicate", "value")}
        if any(value is None for value in bindings.values()):
            continue
        atom = {**raw, "schema_version": ATOM_SCHEMA, "receipt_digest": receipt["receipt_digest"],
                "locator": receipt["locator"], "field_bindings": bindings}
        atom["atom_id"] = "atom_" + digest({key: atom.get(key) for key in
            ("requirement_id", "evidence_id", "exact_excerpt", "subject", "predicate", "value",
             "effective_date", "qualification", "document_version", "support_mode")})[7:27]
        key = (requirement_id, evidence_id, atom["subject"], atom["predicate"], atom["value"])
        if key not in seen:
            atoms.append(atom); seen.add(key)
    return atoms


def call_extractor(gateway: Gateway, requirements: list[dict[str, Any]],
                   receipts: dict[str, dict[str, Any]], audit: list[dict[str, Any]],
                   *, batch_size: int = 8) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if batch_size < 1 or batch_size > 8:
        raise ValueError("extractor batch_size must be between 1 and 8")
    by_requirement = {row["requirement_id"]: row for row in requirements}
    audit_by_requirement = {row["requirement_id"]: row for row in audit}
    atoms = []; failures = []
    for start in range(0, len(requirements), batch_size):
        batch = requirements[start:start + batch_size]; selected = []
        for requirement in batch:
            row = audit_by_requirement.get(requirement["requirement_id"], {})
            for evidence_id in row.get("evidence_ids", [])[:3]:
                receipt = receipts[evidence_id]
                selected.append({"requirement_id": requirement["requirement_id"], "evidence_id": evidence_id,
                                 "quote": receipt["quote"][:1200], "locator": receipt["locator"],
                                 "receipt_digest": receipt["receipt_digest"]})
        payload = {"requirements": [{"requirement_id": row["requirement_id"],
                                      "requirement": row.get("requirement"), "type": row.get("type"),
                                      "required_evidence_type": row.get("required_evidence_type"),
                                      "lifecycle_category": row.get("lifecycle_category")}
                                     for row in batch],
                   "receipts": selected,
                   "instruction": "Extract every relevant explicit atomic fact present in the receipts, including partial evidence that does not fully satisfy the requirement. Do not judge requirement coverage. subject, predicate, and value must each be non-empty exact substrings of exact_excerpt. Do not answer the task, infer missing facts, or assign authority."}
        result = _model_call(gateway, "Extract source-bound evidence atoms only.",
                             json.dumps(payload, ensure_ascii=False), max(3000, 2000 * len(batch)),
                             ATOM_OUTPUT, "proofpress_v10_atoms", 2)
        if not result["ok"]:
            failures.append(result["record"]); continue
        batch_audit = [audit_by_requirement[row["requirement_id"]] for row in batch
                       if row["requirement_id"] in audit_by_requirement]
        atoms.extend(normalize_atoms(result["value"], batch, receipts, batch_audit))
    return atoms, {"status": "ok" if not failures else "inconclusive",
                   "atom_count": len(atoms), "batch_size": batch_size,
                   "batch_count": (len(requirements) + batch_size - 1) // batch_size,
                   "failed_batch_count": len(failures)}


def call_proposer(gateway: Gateway, requirements: list[dict[str, Any]],
                  atoms: list[dict[str, Any]], gates: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    eligible = {rid for rid, row in gates.items() if row["state"] == "claimable"}
    selected = [row for row in atoms if row["requirement_id"] in eligible]
    atom_by_id = {row["atom_id"]: row for row in selected}
    eligible_requirements = [row for row in requirements if row["requirement_id"] in eligible]
    claims = []; rejected = Counter(); failures = []; truncated = 0
    for start in range(0, len(eligible_requirements), 8):
        batch = eligible_requirements[start:start + 8]
        requirement_ids = {row["requirement_id"] for row in batch}
        payload = {"requirements": batch,
                   "evidence_atoms": [row for row in selected if row["requirement_id"] in requirement_ids],
                   "instruction": "Compile narrow atomic unresolved candidates only. Preserve qualifications. Do not add background facts, legal conclusions, authority, or admission."}
        result = _model_call(gateway, "You are an evidence compiler, not an answer generator.",
                             json.dumps(payload, ensure_ascii=False), 12000,
                             CLAIM_OUTPUT, "proofpress_v10_claims", 2)
        if not result["ok"]:
            failures.append(result["record"]); continue
        for raw in result["value"].get("claims", []):
            if len(claims) >= 64:
                truncated += 1
                continue
            requirement_id = raw.get("requirement_id")
            claim = {**raw, "id": f"claim_{len(claims) + 1:03d}_{digest(raw)[7:15]}"}
            try:
                validate_compiled_claim(claim, atom_by_id, gates.get(requirement_id, {}))
            except ValueError as exc:
                rejected[type(exc).__name__] += 1
                continue
            claims.append(claim)
    return claims, {"status": "ok" if not failures else "inconclusive",
                    "claim_count": len(claims), "failed_batch_count": len(failures),
                    "rejected_count": sum(rejected.values()), "truncated_count": truncated}


def call_critic(gateway: Gateway, requirements: list[dict[str, Any]],
                atoms: list[dict[str, Any]], claims: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    selected_ids = {atom_id for claim in claims for atom_id in claim.get("atom_ids", [])}
    payload = {"requirements": requirements, "evidence_atoms": [row for row in atoms if row["atom_id"] in selected_ids],
               "claims": claims,
               "instruction": "Judge every field independently. supported is allowed only when all seven booleans are true. Do not rewrite or admit claims."}
    result = _model_call(gateway, "Return layered evidence-fidelity verdicts only.",
                         json.dumps(payload, ensure_ascii=False), 12000,
                         VERDICT_OUTPUT, "proofpress_v10_layered_verdicts", 2)
    if not result["ok"]:
        return [], {"status": "inconclusive", "failure": result["record"]}
    verdicts = []
    for raw in result["value"].get("verdicts", []):
        if not isinstance(raw, dict):
            continue
        row = {**raw, "schema_version": CRITIC_SCHEMA}
        false_fields = [field for field in CRITIC_FIELDS if row.get(field) is False]
        row["verdict"] = "unsupported" if false_fields else "supported"
        row["failure_reasons"] = false_fields
        verdicts.append(row)
    try:
        applied = apply_layered_verdicts(requirements, claims, verdicts)
    except ValueError as exc:
        return [], {"status": "schema_failure", "failure_digest": digest(str(exc))}
    return verdicts, {"status": "ok", "supported_claim_count": len(applied["supported_claims"]),
                      "supported_requirement_count": sum(row["status"] == "covered"
                                                         for row in applied["requirement_statuses"])}


def agreement(candidate: list[dict[str, Any]], reference: list[dict[str, Any]]) -> dict[str, Any]:
    left = {row["claim_id"]: row for row in candidate}; right = {row["claim_id"]: row for row in reference}
    ids = sorted(set(left) & set(right))
    exact = sum(left[cid]["verdict"] == right[cid]["verdict"] for cid in ids)
    unsupported = {cid for cid in ids if right[cid]["verdict"] == "unsupported"}
    detected = {cid for cid in ids if left[cid]["verdict"] == "unsupported"}
    return {"claim_count": len(ids), "exact_verdict_agreement": exact / len(ids) if ids else None,
            "unsupported_detection_recall": len(unsupported & detected) / len(unsupported) if unsupported else 1.0,
            "supported_false_rejection_rate": len({cid for cid in ids if right[cid]["verdict"] == "supported"} & detected) /
                max(1, len({cid for cid in ids if right[cid]["verdict"] == "supported"}))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--diagnostic", required=True)
    parser.add_argument("--gateway-server", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--budget-usd", type=float, default=20.0)
    parser.add_argument("--timeout", type=float, default=300)
    parser.add_argument("--resume-extractors-dir",
                        help="private failed-run raw directory; reuses only validated extractor atoms")
    args = parser.parse_args()
    diagnostic = Path(args.diagnostic).resolve()
    source_paths = sorted((diagnostic.parent / "raw" / "sol" / "receipt_preproposal").glob("*.json"))
    if len(source_paths) != 4:
        raise SystemExit("v10 matrix requires exactly four frozen tasks")
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw_root = out / "raw"; raw_root.mkdir(exist_ok=True); raw_root.chmod(0o700)
    gateways = {f"{role}_{label}": Gateway(args.gateway_server, route["model"], route["provider"], out,
                    args.timeout, route["reasoning"], structured_output=True)
                for role in ("extractor", "proposer", "critic") for label, route in MODELS.items()}
    tasks = []
    try:
        for source_path in source_paths:
            source = json.loads(source_path.read_text()); construction = source["construction"]
            requirements = construction["requirements"]; receipts = _receipts(construction)
            audit = construction["retrieval_audit"]
            resume_path = (Path(args.resume_extractors_dir) / source_path.name
                           if args.resume_extractors_dir else None)
            if resume_path and resume_path.is_file():
                saved = json.loads(resume_path.read_text())
                extractors = saved.get("extractors", {})
                extractor_status = {label: {"status": "reused_private_failed_run",
                                            "atom_count": len(extractors.get(label, []))}
                                    for label in MODELS}
            else:
                extractors = {}; extractor_status = {}
                with ThreadPoolExecutor(max_workers=4) as pool:
                    futures = {pool.submit(call_extractor, gateways[f"extractor_{label}"], requirements,
                                           receipts, audit): label for label in MODELS}
                    for future in as_completed(futures):
                        label = futures[future]; extractors[label], extractor_status[label] = future.result()
            variants = {}; calls = {"extractor": extractor_status}
            for extractor_label, atoms in extractors.items():
                gates = {row["requirement_id"]: claimability_decision(row, atoms, receipts)
                         for row in requirements}
                proposer_outputs = {}; proposer_status = {}
                with ThreadPoolExecutor(max_workers=4) as pool:
                    futures = {pool.submit(call_proposer, gateways[f"proposer_{label}"], requirements,
                                           atoms, gates): label for label in MODELS}
                    for future in as_completed(futures):
                        label = futures[future]; proposer_outputs[label], proposer_status[label] = future.result()
                calls.setdefault("proposer", {})[extractor_label] = proposer_status
                for proposer_label, claims in proposer_outputs.items():
                    critic_outputs = {}; critic_status = {}
                    with ThreadPoolExecutor(max_workers=4) as pool:
                        futures = {pool.submit(call_critic, gateways[f"critic_{label}"], requirements,
                                               atoms, claims): label for label in MODELS}
                        for future in as_completed(futures):
                            label = futures[future]; critic_outputs[label], critic_status[label] = future.result()
                    calls.setdefault("critic", {})[f"{extractor_label}+{proposer_label}"] = critic_status
                    key = f"{extractor_label}+{proposer_label}"
                    reference = critic_outputs.get("sol", [])
                    supported = {claim["requirement_id"] for claim in claims
                                 if next((row for row in reference if row["claim_id"] == claim["id"]), {}).get("verdict") == "supported"}
                    variants[key] = {
                        "extractor": extractor_label, "proposer": proposer_label,
                        "atom_count": len(atoms), "atom_requirement_count": len({row["requirement_id"] for row in atoms}),
                        "claim_count": len(claims),
                        "sol_supported_claim_count": sum(row.get("verdict") == "supported" for row in reference),
                        "sol_supported_requirement_count": len(supported),
                        "sol_supported_requirement_coverage": len(supported) / len(requirements) if requirements else None,
                        "sol_unsupported_rate": sum(row.get("verdict") == "unsupported" for row in reference) / len(reference) if reference else None,
                        "critic_agreement": {label: agreement(rows, reference) for label, rows in critic_outputs.items()},
                    }
            private = {"task_id": source_path.stem, "requirements": requirements,
                       "extractors": extractors, "variants": variants, "calls": calls}
            target = raw_root / f"{source_path.stem}.json"
            target.write_text(json.dumps(private, ensure_ascii=False, indent=2, sort_keys=True) + "\n"); target.chmod(0o600)
            tasks.append({"task_id": source_path.stem, "status": "ok",
                          "requirement_count": len(requirements), "variants": variants,
                          "artifact_digest": digest(private)})
            telemetry = terminal_telemetry(gateways)
            if telemetry["known_cost_usd"] > args.budget_usd:
                raise RuntimeError("v10 role matrix exceeded its hard budget")
    finally:
        for gateway in gateways.values(): gateway.stop()
    telemetry = terminal_telemetry(gateways)
    summaries = []
    for key in sorted(next(iter(tasks))["variants"]):
        rows = [task["variants"][key] for task in tasks]
        requirement_total = sum(task["requirement_count"] for task in tasks)
        claim_total = sum(row["claim_count"] for row in rows)
        summaries.append({"route": key, "tasks": len(rows), "requirements": requirement_total,
                          "atoms": sum(row["atom_count"] for row in rows),
                          "claims": claim_total,
                          "supported_claims": sum(row["sol_supported_claim_count"] for row in rows),
                          "supported_requirement_coverage": sum(row["sol_supported_requirement_count"] for row in rows) / requirement_total,
                          "unsupported_claim_rate": sum((row["sol_unsupported_rate"] or 0) * row["claim_count"] for row in rows) / claim_total if claim_total else None})
    report = {"schema_version": SCHEMA,
              "boundary": "Frozen four-task development matrix; Sol layered verdict is a model reference, not gold or admission.",
              "models": MODELS, "tasks": [{key: row[key] for key in ("task_id", "status", "requirement_count", "artifact_digest")} for row in tasks],
              "denominators": {"tasks": len(tasks), "requirements": sum(row["requirement_count"] for row in tasks),
                               "routes": len(summaries)},
              "route_summary": summaries,
              "telemetry": {**telemetry, "budget_usd": args.budget_usd},
              "qualification": {"status": "pass" if len(tasks) == 4 and not telemetry["missing_cost_calls"] else "inconclusive",
                                "quality_cells_may_be_reported_when_cost_inconclusive": True},
              "raw_private_dir": str(raw_root)}
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["qualification"]["status"], "cost_usd": telemetry["known_cost_usd"],
                      "routes": len(summaries)}, sort_keys=True))


if __name__ == "__main__":
    main()

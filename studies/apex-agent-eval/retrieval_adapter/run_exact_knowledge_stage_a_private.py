#!/usr/bin/env python3
"""Run v18 Stage A exact-knowledge construction without an answer executor."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import time
from typing import Any

from exact_knowledge_contract import (
    AUTHORITY_LEVELS,
    AUTHORITY_NODE_SCHEMA,
    NUMERIC_KINDS,
    OUTPUT_TYPES,
    PRECISION_STATES,
    SLOT_OBJECT_KINDS,
    assess_requirement_readiness,
    bind_evidence_atom,
    bind_numeric_atom,
    bind_requirement_objects,
    bind_task_numeric_parameter,
    build_exact_derivation,
    compile_requirement_plan,
    digest,
    extract_numeric_candidates,
    validate_authority_node,
)
from run_claim_construction_private import Gateway, SectionIndex, _model_call
from run_model_routing_qualification_private import terminal_telemetry
from run_v10_construction_qualification_private import retrieve
from build_official_authority_catalog_private import CATALOG_SCHEMA as AUTHORITY_CATALOG_SCHEMA


SCHEMA = "proofpress/exact-knowledge-stage-a/v1"
TASK_IDS = (
    "task_b78c4510be784e6a8b8f0394aafd785d",
    "task_8d501efe0f924f69aeee070f2e08b576",
    "task_8ab8c8d7662747d696d52706a8b3de55",
    "task_11893dcabbe34b0aa991516dfe7edcba",
    "task_f8f47a9c94874854a24936d81a89fdfb",
)
ROUTE = {"model": "openai/gpt-5.6-sol", "provider": "openai", "reasoning": "high"}


SLOT_ITEM = {
    "type": "object", "additionalProperties": False,
    "required": ["slot_id", "slot_type", "description", "exactness", "expected_periods",
                 "required_object_kinds", "output_format", "search_queries"],
    "properties": {
        "slot_id": {"type": "string", "maxLength": 64},
        "slot_type": {"type": "string", "enum": sorted(SLOT_OBJECT_KINDS)},
        "description": {"type": "string", "maxLength": 500},
        "exactness": {"type": "string", "enum": ["exact", "bounded", "qualitative"]},
        "expected_periods": {"type": "array", "maxItems": 16,
                             "items": {"type": "string", "maxLength": 96}},
        "required_object_kinds": {"type": "array", "maxItems": 3,
                                  "items": {"type": "string", "enum": [
                                      "evidence_atom", "authority_node", "derivation_node"]}},
        "output_format": {"type": "string", "maxLength": 160},
        "search_queries": {"type": "array", "minItems": 1, "maxItems": 4,
                           "items": {"type": "string", "maxLength": 300}},
    },
}
COMPILER_OUTPUT = {"type": "object", "additionalProperties": False,
                   "required": ["slots"],
                   "properties": {"slots": {"type": "array", "minItems": 2,
                                                "maxItems": 20, "items": SLOT_ITEM}}}

ATOM_PAYLOAD = {
    "type": "object", "additionalProperties": False,
    "required": ["requirement_id", "evidence_id", "subject", "predicate", "value",
                 "effective_date", "qualification", "document_version", "exact_excerpt"],
    "properties": {
        "requirement_id": {"type": "string"}, "evidence_id": {"type": "string"},
        "subject": {"type": "string"}, "predicate": {"type": "string"},
        "value": {"type": "string"},
        "effective_date": {"type": ["string", "null"]},
        "qualification": {"type": ["string", "null"]},
        "document_version": {"type": ["string", "null"]},
        "exact_excerpt": {"type": "string", "maxLength": 1600},
    },
}
NUMERIC_PAYLOAD = {
    "type": "object", "additionalProperties": False,
    "required": ["requirement_id", "evidence_id", "subject", "predicate", "display",
                 "kind", "currency", "unit", "entity", "period", "precision",
                 "effective_date", "qualification", "document_version", "exact_excerpt"],
    "properties": {
        "requirement_id": {"type": "string"}, "evidence_id": {"type": "string"},
        "subject": {"type": "string"}, "predicate": {"type": "string"},
        "display": {"type": "string"}, "kind": {"type": "string", "enum": sorted(NUMERIC_KINDS)},
        "currency": {"type": ["string", "null"]}, "unit": {"type": "string"},
        "entity": {"type": "string"}, "period": {"type": "string"},
        "precision": {"type": "string", "enum": sorted(PRECISION_STATES)},
        "effective_date": {"type": ["string", "null"]},
        "qualification": {"type": ["string", "null"]},
        "document_version": {"type": ["string", "null"]},
        "exact_excerpt": {"type": "string", "maxLength": 1600},
    },
}
PARAMETER_PAYLOAD = {
    "type": "object", "additionalProperties": False,
    "required": ["requirement_id", "display", "kind", "currency", "unit", "entity",
                 "period", "precision", "parameter_role"],
    "properties": {
        "requirement_id": {"type": "string"}, "display": {"type": "string"},
        "kind": {"type": "string", "enum": sorted(NUMERIC_KINDS)},
        "currency": {"type": ["string", "null"]}, "unit": {"type": "string"},
        "entity": {"type": "string"}, "period": {"type": "string"},
        "precision": {"type": "string", "enum": sorted(PRECISION_STATES)},
        "parameter_role": {"type": "string", "enum": ["explicit_assumption", "requested_scope"]},
    },
}
AUTHORITY_PAYLOAD = {
    "type": "object", "additionalProperties": False,
    "required": ["requirement_id", "evidence_id", "citation", "proposition", "jurisdiction",
                 "effective_date", "authority_level", "exact_excerpt"],
    "properties": {
        "requirement_id": {"type": "string"}, "evidence_id": {"type": "string"},
        "citation": {"type": "string"}, "proposition": {"type": "string"},
        "jurisdiction": {"type": "string"}, "effective_date": {"type": "string"},
        "authority_level": {"type": "string", "enum": sorted(AUTHORITY_LEVELS)},
        "exact_excerpt": {"type": "string", "maxLength": 2000},
    },
}
AUTHORITY_OUTPUT = {"type": "object", "additionalProperties": False,
                    "required": ["authority_nodes"],
                    "properties": {"authority_nodes": {"type": "array", "maxItems": 48,
                                                           "items": AUTHORITY_PAYLOAD}}}
EXTRACTION_OUTPUT = {
    "type": "object", "additionalProperties": False,
    "required": ["evidence_atoms", "numeric_atoms", "task_parameters", "authority_nodes"],
    "properties": {
        "evidence_atoms": {"type": "array", "maxItems": 48, "items": ATOM_PAYLOAD},
        "numeric_atoms": {"type": "array", "maxItems": 48, "items": NUMERIC_PAYLOAD},
        "task_parameters": {"type": "array", "maxItems": 24, "items": PARAMETER_PAYLOAD},
        "authority_nodes": {"type": "array", "maxItems": 48, "items": AUTHORITY_PAYLOAD},
    },
}
DERIVATION_ITEM = {
    "type": "object", "additionalProperties": False,
    "required": ["requirement_id", "expression", "variables", "input_bindings", "output_unit",
                 "entity", "period", "round_places"],
    "properties": {
        "requirement_id": {"type": "string"}, "expression": {"type": "string"},
        "variables": {"type": "object", "additionalProperties": {"type": "string"}},
        "input_bindings": {"type": "object", "additionalProperties": {"type": "string"}},
        "output_unit": {"type": "string"}, "entity": {"type": "string"},
        "period": {"type": "string"}, "round_places": {"type": "integer", "minimum": 0, "maximum": 12},
    },
}
DERIVATION_OUTPUT = {"type": "object", "additionalProperties": False,
                     "required": ["derivations"],
                     "properties": {"derivations": {"type": "array", "maxItems": 24,
                                                        "items": DERIVATION_ITEM}}}


def _compile(gateway: Gateway, task: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    payload = {"task_prompt": task["prompt"], "native_output_type": task["expected_output"],
               "instruction": (
                   "Compile the minimum atomic deliverable requirements needed to perform the task. "
                   "Use only the prompt, never rubric, gold, expected answer, source inventory, or prior answer. "
                   "Create exactly one output_structure slot. Split exact values, each period series, factual status, "
                   "controlling authority, legal consequence, and recommended action. Search queries describe evidence "
                   "needed; they are not facts. exact_value and value_by_period should normally require a derivation_node "
                   "when calculation is requested. controlling_authority requires authority_node." )}
    result = _model_call(gateway, "Compile a prompt-only exact legal-task requirement plan.",
                         json.dumps(payload, ensure_ascii=False), 10000,
                         COMPILER_OUTPUT, "proofpress_exact_requirement_slots", 2)
    if not result["ok"]:
        return [], {"status": "inconclusive", "failure": result["record"]}
    slots = result["value"].get("slots", [])
    normalized_kinds = 0
    for row in slots:
        slot_type = row.get("slot_type")
        compatible = SLOT_OBJECT_KINDS.get(slot_type, set())
        requested = list(dict.fromkeys(row.get("required_object_kinds", [])))
        selected = [kind for kind in requested if kind in compatible]
        if slot_type == "output_structure":
            selected = []
        elif not selected and compatible:
            defaults = {
                "exact_value": ["derivation_node"],
                "value_by_period": ["derivation_node"],
                "ratio_or_threshold": ["derivation_node"],
                "factual_status": ["evidence_atom"],
                "controlling_authority": ["authority_node"],
                "legal_consequence": ["authority_node", "evidence_atom"],
                "recommended_action": ["authority_node", "evidence_atom"],
            }
            selected = [kind for kind in defaults.get(slot_type, []) if kind in compatible]
        if selected != requested:
            normalized_kinds += 1
        row["required_object_kinds"] = selected
    plan_slots = [{key: row[key] for key in ("slot_id", "slot_type", "description", "exactness",
                                              "expected_periods", "required_object_kinds", "output_format")}
                  for row in slots]
    try:
        plan = compile_requirement_plan(task["prompt"], plan_slots,
                                        output_type=task["expected_output"])
    except ValueError as exc:
        return [], {"status": "inconclusive", "failure_type": type(exc).__name__,
                    "failure_digest": digest(str(exc))}
    by_id = {row["slot_id"]: row for row in slots}
    for row in plan["slots"]:
        row["search_queries"] = by_id[row["slot_id"]]["search_queries"]
    plan["plan_digest"] = digest({key: value for key, value in plan.items() if key != "plan_digest"})
    return plan["slots"], {"status": "ok", "slot_count": len(plan["slots"]),
                           "normalized_object_kind_slots": normalized_kinds}


def _source_requirements(slots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"requirement_id": row["slot_id"], "requirement": row["description"],
             "evidence_search_queries": row["search_queries"]}
            for row in slots if row["slot_type"] != "output_structure"]


def _authority_requirements(slots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"requirement_id": row["slot_id"], "requirement": row["description"],
             "evidence_search_queries": row["search_queries"]}
            for row in slots if "authority_node" in row["required_object_kinds"]]


def _merge_retrieval(primary_receipts: dict[str, dict[str, Any]],
                     primary_audit: list[dict[str, Any]],
                     added_receipts: dict[str, dict[str, Any]],
                     added_audit: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    receipts = {**primary_receipts, **added_receipts}
    by_requirement = {row["requirement_id"]: dict(row) for row in primary_audit}
    for row in added_audit:
        existing = by_requirement.setdefault(row["requirement_id"], {
            "requirement_id": row["requirement_id"], "evidence_ids": [],
            "ranked_section_count": 0, "considered_document_count": 0})
        existing["evidence_ids"] = list(dict.fromkeys(
            [*existing.get("evidence_ids", []), *row.get("evidence_ids", [])]))
        existing["ranked_section_count"] += row.get("ranked_section_count", 0)
        existing["considered_document_count"] += row.get("considered_document_count", 0)
        existing["controlled_authority_section_count"] = row.get("ranked_section_count", 0)
    return receipts, [by_requirement[key] for key in sorted(by_requirement)]


def _extract(gateway: Gateway, task: dict[str, Any], slots: list[dict[str, Any]],
             receipts: dict[str, dict[str, Any]], audit: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    by_slot = {row["requirement_id"]: row for row in audit}
    selected = []
    for slot in slots:
        for evidence_id in by_slot.get(slot["slot_id"], {}).get("evidence_ids", [])[:4]:
            receipt = receipts[evidence_id]
            selected.append({"requirement_id": slot["slot_id"], "evidence_id": evidence_id,
                             "quote": receipt["quote"][:1800], "locator": receipt["locator"],
                             "receipt_digest": receipt["receipt_digest"],
                             "authority_metadata": (receipt.get("source") or {}).get("official_authority")})
    payload = {
        "task_prompt": task["prompt"],
        "prompt_numeric_inventory": extract_numeric_candidates(task["prompt"]),
        "requirement_slots": slots,
        "retrieval_receipts": selected,
        "instruction": (
            "Construct candidates, not an answer. General and numeric evidence atoms must be explicit in one receipt; "
            "subject, predicate, value/display must each be exact substrings of exact_excerpt, which itself must be an "
            "exact receipt substring. Task parameters may use only numeric text explicitly present in the task prompt and "
            "must be assumptions or requested scope, never matter evidence. Authority citation must be an exact substring "
            "of its receipt excerpt. For an official authority receipt, copy jurisdiction, effective_on, authority_level, "
            "and one canonical_citations value exactly from authority_metadata; do not independently upgrade its level or "
            "confirm that it controls the matter. Assign every object to its responsive slot. "
            "Do not infer missing values, calculate results, admit knowledge, or use rubric/gold/silver data."),
    }
    result = _model_call(gateway, "Extract exact typed candidate knowledge with source fidelity.",
                         json.dumps(payload, ensure_ascii=False), 24000,
                         EXTRACTION_OUTPUT, "proofpress_exact_typed_candidates", 2)
    if not result["ok"]:
        return {}, {"status": "inconclusive", "failure": result["record"]}
    return result["value"], {"status": "ok"}


def _authority(raw: dict[str, Any], receipts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    receipt = receipts[raw["evidence_id"]]
    metadata = (receipt.get("source") or {}).get("official_authority")
    if isinstance(metadata, dict):
        for key, source_key in (("jurisdiction", "jurisdiction"),
                                ("effective_date", "effective_on"),
                                ("authority_level", "authority_level")):
            expected = metadata.get(source_key)
            if raw.get(key) and raw[key] != expected:
                raise ValueError("authority extraction disagrees with controlled source metadata")
            raw[key] = expected
    basis = {**raw, "receipt_digest": receipt["receipt_digest"], "locator": receipt["locator"],
             "status": "not_governed_candidate", "normative_authority_confirmed": False,
             "admission_authority": False}
    node = {"schema_version": AUTHORITY_NODE_SCHEMA,
            "authority_id": "authority_" + digest(basis).split(":", 1)[1][:20], **basis}
    return validate_authority_node(node, receipts)


def _extract_authorities(gateway: Gateway, slots: list[dict[str, Any]],
                         receipts: dict[str, dict[str, Any]],
                         audit: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    by_slot = {row["requirement_id"]: row for row in audit}
    selected = []
    for slot in slots:
        if "authority_node" not in slot["required_object_kinds"]:
            continue
        count = 0
        for evidence_id in by_slot.get(slot["slot_id"], {}).get("evidence_ids", []):
            receipt = receipts[evidence_id]
            metadata = (receipt.get("source") or {}).get("official_authority")
            if not isinstance(metadata, dict):
                continue
            selected.append({"requirement_id": slot["slot_id"], "requirement": slot["description"],
                             "evidence_id": evidence_id, "quote": receipt["quote"][:3000],
                             "locator": receipt["locator"], "receipt_digest": receipt["receipt_digest"],
                             "authority_metadata": metadata})
            count += 1
            if count >= 4:
                break
    if not selected:
        return [], {"status": "ok", "authority_candidate_count": 0,
                    "official_receipt_count": 0}
    payload = {"official_authority_receipts": selected,
               "instruction": (
                   "Construct only source-bound authority candidates responsive to each requirement. Copy evidence_id, "
                   "jurisdiction, effective_on into effective_date, authority_level, and one canonical_citations value "
                   "exactly from that receipt's authority_metadata. The citation must also appear in exact_excerpt, and "
                   "exact_excerpt must be copied from quote. State a narrow proposition supported by that excerpt. "
                   "Do not claim the candidate controls the matter, do not apply it to facts, and do not admit it.")}
    result = _model_call(gateway, "Extract narrow candidates from controlled official authority receipts.",
                         json.dumps(payload, ensure_ascii=False), 16000,
                         AUTHORITY_OUTPUT, "proofpress_controlled_authority_candidates", 2)
    if not result["ok"]:
        return [], {"status": "inconclusive", "failure": result["record"]}
    return result["value"].get("authority_nodes", []), {
        "status": "ok", "authority_candidate_count": len(result["value"].get("authority_nodes", [])),
        "official_receipt_count": len(selected)}


def _frozen_slots(task: dict[str, Any], frozen_plan_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source = json.loads((frozen_plan_dir / f'{task["task_id"]}.json').read_text())
    if source.get("task", {}).get("task_id") != task["task_id"]:
        raise ValueError("frozen requirement plan task mismatch")
    slots = []
    for row in source["plan"]["slots"]:
        slots.append({key: row[key] for key in ("slot_id", "slot_type", "description", "exactness",
                                                 "expected_periods", "required_object_kinds", "output_format")})
        slots[-1]["search_queries"] = [row["description"]]
    plan_slots = [{key: row[key] for key in ("slot_id", "slot_type", "description", "exactness",
                                              "expected_periods", "required_object_kinds", "output_format")}
                  for row in slots]
    compile_requirement_plan(task["prompt"], plan_slots, output_type=task["expected_output"])
    return slots, {"status": "ok", "slot_count": len(slots), "frozen_plan": True,
                   "source_plan_digest": source["plan"]["plan_digest"]}


def _validated_objects(task: dict[str, Any], slots: list[dict[str, Any]], value: dict[str, Any],
                       receipts: dict[str, dict[str, Any]]) -> tuple[dict[str, list[dict[str, Any]]], list[str]]:
    known = {row["slot_id"] for row in slots}; failures = []
    result: dict[str, list[dict[str, Any]]] = {key: [] for key in
        ("evidence_atoms", "numeric_atoms", "task_parameters", "authority_nodes")}
    builders = (
        ("evidence_atoms", lambda row: bind_evidence_atom(row, receipts)),
        ("numeric_atoms", lambda row: bind_numeric_atom(row, receipts)),
        ("task_parameters", lambda row: bind_task_numeric_parameter(task["prompt"], row)),
        ("authority_nodes", lambda row: _authority(row, receipts)),
    )

    def repair_excerpt(label: str, raw: dict[str, Any]) -> dict[str, Any]:
        if label not in {"evidence_atoms", "numeric_atoms"}:
            return raw
        receipt = receipts.get(raw.get("evidence_id"))
        quote = str((receipt or {}).get("quote") or "")
        excerpt = str(raw.get("exact_excerpt") or "")
        if excerpt and excerpt in quote:
            return raw
        value_key = "display" if label == "numeric_atoms" else "value"
        fields = [str(raw.get(key) or "") for key in ("subject", "predicate", value_key)]
        positions = [(quote.find(field), len(field)) for field in fields if field]
        if len(positions) == 3 and all(start >= 0 for start, _ in positions):
            start = min(row[0] for row in positions)
            end = max(row[0] + row[1] for row in positions)
            if end - start <= 1600:
                return {**raw, "exact_excerpt": quote[start:end]}
        return raw

    def failure_code(exc: Exception) -> str:
        message = str(exc)
        codes = {
            "not present in the exact excerpt": "field_not_exact",
            "exact excerpt is not receipt-bound": "excerpt_not_receipt_bound",
            "numeric value is not decimal-compatible": "numeric_not_decimal_compatible",
            "required fields are missing": "required_fields_missing",
            "controlled source metadata": "controlled_metadata_mismatch",
            "outside the controlled source metadata": "controlled_citation_mismatch",
        }
        return next((code for fragment, code in codes.items() if fragment in message),
                    "other_validation_failure")

    for label, builder in builders:
        seen = set()
        for raw in value.get(label, []):
            raw = repair_excerpt(label, raw)
            if raw.get("requirement_id") not in known:
                failures.append(f"{label}:unknown_requirement"); continue
            try:
                built = builder(raw)
                object_id = built.get("atom_id") or built.get("parameter_id") or built.get("authority_id")
                if object_id not in seen:
                    result[label].append(built); seen.add(object_id)
            except (KeyError, TypeError, ValueError) as exc:
                failures.append(f"{label}:{failure_code(exc)}:{digest(str(exc))[-12:]}")
    return result, failures


def _plan_derivations(gateway: Gateway, slots: list[dict[str, Any]], objects: dict[str, list[dict[str, Any]]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    exact_slots = [row for row in slots if "derivation_node" in row["required_object_kinds"]]
    inputs = []
    for row in [*objects["numeric_atoms"], *objects["task_parameters"]]:
        inputs.append({"object_id": row.get("atom_id") or row.get("parameter_id"),
                       "requirement_id": row["requirement_id"], "numeric": row["numeric"],
                       "input_kind": "task_parameter" if row.get("parameter_id") else "evidence_atom"})
    if not exact_slots or not inputs:
        return [], {"status": "ok", "derivation_count": 0}
    payload = {"requirement_slots": exact_slots, "validated_numeric_inputs": inputs,
               "instruction": (
                   "Plan only calculations fully supported by the validated inputs. Variables must copy decimal_value "
                   "exactly and bind its object_id. Use only + - * / parentheses and declared variable names. Create one "
                   "derivation per required period when possible. Do not invent inputs or legal rules. Omit a derivation "
                   "when inputs are insufficient; deterministic code will recompute every result.")}
    result = _model_call(gateway, "Plan deterministic decimal derivations over validated inputs.",
                         json.dumps(payload, ensure_ascii=False), 12000,
                         DERIVATION_OUTPUT, "proofpress_exact_derivations", 2)
    if not result["ok"]:
        return [], {"status": "inconclusive", "failure": result["record"]}
    atoms = {row["atom_id"]: row for row in objects["numeric_atoms"]}
    params = {row["parameter_id"]: row for row in objects["task_parameters"]}
    derivations = []; failures = []
    for spec in result["value"].get("derivations", []):
        try:
            derivations.append(build_exact_derivation(
                requirement_id=spec["requirement_id"], expression=spec["expression"],
                variables=spec["variables"], input_bindings=spec["input_bindings"],
                numeric_atoms=atoms, task_parameters=params, output_unit=spec["output_unit"],
                entity=spec["entity"], period=spec["period"], round_places=spec["round_places"]))
        except (KeyError, TypeError, ValueError) as exc:
            failures.append(f"derivation:{type(exc).__name__}:{digest(str(exc))[-12:]}")
    return derivations, {"status": "ok", "derivation_count": len(derivations),
                         "invariant_failures": failures}


def _task_audit(gateways: dict[str, Gateway], task: dict[str, Any], index: SectionIndex,
                raw_dir: Path, authority_index: SectionIndex | None = None,
                frozen_plan_dir: Path | None = None) -> dict[str, Any]:
    started = time.monotonic()
    slots, compiler = (_frozen_slots(task, frozen_plan_dir) if frozen_plan_dir
                       else _compile(gateways["compiler"], task))
    if compiler["status"] != "ok":
        return {"task_id": task["task_id"], "status": "inconclusive", "compiler": compiler}
    plan_slots = [{key: row[key] for key in ("slot_id", "slot_type", "description", "exactness",
                                              "expected_periods", "required_object_kinds", "output_format")}
                  for row in slots]
    plan = compile_requirement_plan(task["prompt"], plan_slots, output_type=task["expected_output"])
    receipts, audit = retrieve(_source_requirements(slots), index, max_sections=8,
                               mode="multiquery_rrf")
    if authority_index is not None:
        authority_receipts, authority_audit = retrieve(
            _authority_requirements(slots), authority_index, max_sections=12,
            mode="multiquery_rrf")
        receipts, audit = _merge_retrieval(receipts, audit, authority_receipts, authority_audit)
    extracted, extraction = _extract(gateways["extractor"], task, slots, receipts, audit)
    if extraction["status"] != "ok":
        return {"task_id": task["task_id"], "status": "inconclusive",
                "compiler": compiler, "extraction": extraction}
    authority_raw, authority_extraction = _extract_authorities(
        gateways["authority"], slots, receipts, audit) if authority_index is not None else ([], {"status": "ok"})
    if authority_extraction["status"] != "ok":
        return {"task_id": task["task_id"], "status": "inconclusive",
                "compiler": compiler, "extraction": extraction,
                "authority_extraction": authority_extraction}
    extracted["authority_nodes"] = [*extracted.get("authority_nodes", []), *authority_raw]
    objects, failures = _validated_objects(task, slots, extracted, receipts)
    derivations, derivation_status = _plan_derivations(gateways["derivation"], slots, objects)
    failures.extend(derivation_status.get("invariant_failures", []))
    allowed = {row["slot_id"]: set(row["required_object_kinds"]) for row in slots}
    assignments: dict[str, list[str]] = {row["slot_id"]: [] for row in slots}
    for label, kind, id_key in (("evidence_atoms", "evidence_atom", "atom_id"),
                                ("numeric_atoms", "evidence_atom", "atom_id"),
                                ("authority_nodes", "authority_node", "authority_id")):
        for row in objects[label]:
            if kind in allowed[row["requirement_id"]]:
                assignments[row["requirement_id"]].append(row[id_key])
    for row in derivations:
        if "derivation_node" in allowed[row["requirement_id"]]:
            assignments[row["requirement_id"]].append(row["derivation_id"])
    plan = bind_requirement_objects(plan, assignments)
    readiness = assess_requirement_readiness(
        plan, evidence_atoms=[*objects["evidence_atoms"], *objects["numeric_atoms"]],
        authority_nodes=objects["authority_nodes"], derivations=derivations)
    private = {"schema_version": SCHEMA, "task": task, "plan": plan, "receipts": receipts,
               "retrieval_audit": audit, "objects": objects, "derivations": derivations,
               "readiness": readiness, "invariant_failures": failures,
               "stage_status": {"compiler": compiler, "extraction": extraction,
                                "authority_extraction": authority_extraction,
                                "derivation": derivation_status}}
    target = raw_dir / f'{task["task_id"]}.json'
    target.write_text(json.dumps(private, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    target.chmod(0o600)
    states = Counter(row["state"] for row in readiness["slots"])
    paths = Counter()
    for slot_id, ids in assignments.items():
        for object_id in ids:
            paths["derivation_node" if object_id.startswith("derivation_") else
                  "authority_node" if object_id.startswith("authority_") else "evidence_atom"] += 1
    return {"task_id": task["task_id"], "task_name": task.get("task_name"), "status": "ok",
            "output_type": task["expected_output"], "plan_digest": plan["plan_digest"],
            "slot_count": len(plan["slots"]), "slot_states": dict(sorted(states.items())),
            "slots": [{"slot_id": row["slot_id"], "slot_type": next(
                slot["slot_type"] for slot in plan["slots"] if slot["slot_id"] == row["slot_id"]),
                       "state": row["state"], "object_count": len(row["object_ids"])}
                      for row in readiness["slots"]],
            "object_counts": {"evidence_atoms": len(objects["evidence_atoms"]),
                              "numeric_atoms": len(objects["numeric_atoms"]),
                              "task_parameters": len(objects["task_parameters"]),
                              "authority_nodes": len(objects["authority_nodes"]),
                              "derivations": len(derivations)},
            "completion_paths": dict(sorted(paths.items())),
            "invariant_failure_count": len(failures),
            "invariant_failure_types": dict(sorted(Counter(row.split(":", 2)[0] for row in failures).items())),
            "candidate_coverage": readiness["candidate_coverage"],
            "governed_coverage": readiness["governed_coverage"],
            "executor_ready": readiness["executor_ready"],
            "elapsed_ms": round((time.monotonic() - started) * 1000, 3),
            "private_artifact_digest": digest(private)}


def _load_tasks(raw_dir: Path) -> list[dict[str, Any]]:
    tasks = []
    for task_id in TASK_IDS:
        value = json.loads((raw_dir / f"{task_id}.json").read_text())
        task = dict(value["task"])
        if task.get("task_id") != task_id or task.get("expected_output") not in OUTPUT_TYPES:
            raise ValueError("frozen Stage A task input is invalid")
        tasks.append(task)
    return tasks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim-raw", required=True, type=Path)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--authority-catalog", type=Path)
    parser.add_argument("--frozen-plan-dir", type=Path)
    parser.add_argument("--gateway-server", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--budget-usd", type=float, default=15.0)
    parser.add_argument("--timeout", type=float, default=360)
    args = parser.parse_args()
    tasks = _load_tasks(args.claim_raw)
    catalog = json.loads(args.catalog.read_text())
    index = SectionIndex(catalog)
    authority_catalog = None
    authority_index = None
    if args.authority_catalog:
        authority_catalog = json.loads(args.authority_catalog.read_text())
        if authority_catalog.get("schema_version") != AUTHORITY_CATALOG_SCHEMA:
            raise ValueError("official authority catalog schema is required")
        authority_index = SectionIndex(authority_catalog)
    args.out.mkdir(parents=True, exist_ok=True); args.out.chmod(0o700)
    raw_dir = args.out / "raw"; raw_dir.mkdir(exist_ok=True); raw_dir.chmod(0o700)
    gateways = {role: Gateway(args.gateway_server, ROUTE["model"], ROUTE["provider"],
                              args.out, args.timeout, ROUTE["reasoning"], structured_output=True)
                for role in ("compiler", "extractor", "authority", "derivation")}
    summaries = []
    try:
        for task in tasks:
            summaries.append(_task_audit(gateways, task, index, raw_dir, authority_index,
                                         args.frozen_plan_dir))
            if terminal_telemetry(gateways)["known_cost_usd"] > args.budget_usd:
                raise RuntimeError("Stage A exceeded the hard model budget")
    finally:
        for gateway in gateways.values():
            gateway.stop()
    telemetry = terminal_telemetry(gateways)
    frozen_plan_digest = None
    if args.frozen_plan_dir:
        frozen_plan_digest = digest([
            json.loads((args.frozen_plan_dir / f"{task_id}.json").read_text())["plan"]["plan_digest"]
            for task_id in TASK_IDS
        ])
    serialized = json.dumps(summaries, ensure_ascii=False, sort_keys=True)
    leaked = []
    for task in tasks:
        if task["prompt"] in serialized:
            leaked.append("task_prompt")
    for path in raw_dir.glob("*.json"):
        private = json.loads(path.read_text())
        for receipt in private.get("receipts", {}).values():
            quote = str(receipt.get("quote") or "")
            if quote and quote in serialized:
                leaked.append("source_quote")
    invalid = sum(row.get("slot_states", {}).get("invalid_binding", 0) for row in summaries)
    completed = [row for row in summaries if row.get("status") == "ok"]
    output_slots_valid = all(sum(slot["slot_type"] == "output_structure" for slot in row["slots"]) == 1
                             for row in completed)
    qualification = ("pass" if len(completed) == len(TASK_IDS) and not invalid and not leaked
                     and output_slots_valid and not telemetry["missing_cost_calls"]
                     and not telemetry["missing_token_calls"] else "inconclusive")
    report = {"schema_version": SCHEMA,
              "boundary": ("Five-task prompt-only exact-knowledge substrate audit without an answer executor. "
                           "All objects remain not_governed candidates; Human Approval is the only admission path."),
              "task_ids": list(TASK_IDS), "task_input_digest": digest(tasks),
              "catalog_digest": digest(catalog), "route": ROUTE, "tasks": summaries,
              "authority_catalog_digest": (authority_catalog or {}).get("catalog_digest"),
              "frozen_plan_dir_digest": frozen_plan_digest,
              "denominators": {"tasks": len(summaries), "completed_tasks": len(completed),
                               "slots": sum(row.get("slot_count", 0) for row in completed),
                               "candidate_covered_slots": sum(row.get("candidate_coverage", 0) for row in completed),
                               "governed_covered_slots": sum(row.get("governed_coverage", 0) for row in completed),
                               "gaps": sum(row.get("slot_states", {}).get("gap", 0) for row in completed),
                               "invalid_bindings": invalid,
                               "proposed_claims": 0, "numeric_gate_failures": 0},
              "telemetry": {**telemetry, "budget_usd": args.budget_usd,
                            "construction_only_no_executor": True},
              "privacy": {"sanitized_report_leak_types": sorted(set(leaked)),
                          "task_prompts_included": False, "source_quotes_included": False,
                          "numeric_values_included": False, "authority_text_included": False},
              "governance": {"automatic_admission": False, "admission_authority": False,
                             "human_approval_only": True, "executor_ready_tasks": 0},
              "qualification": {"status": qualification,
                                "output_structure_gate": output_slots_valid,
                                "invalid_binding_gate": invalid == 0,
                                "privacy_gate": not leaked,
                                "cost_completeness_gate": not telemetry["missing_cost_calls"],
                                "token_completeness_gate": not telemetry["missing_token_calls"],
                                "gaps_allowed_and_explicit": True},
              "raw_private_dir": str(raw_dir)}
    (args.out / "sanitized-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": qualification, "tasks": len(completed),
                      "slots": report["denominators"]["slots"],
                      "candidate_covered": report["denominators"]["candidate_covered_slots"],
                      "gaps": report["denominators"]["gaps"],
                      "cost_usd": telemetry["known_cost_usd"]}, sort_keys=True))


if __name__ == "__main__":
    main()

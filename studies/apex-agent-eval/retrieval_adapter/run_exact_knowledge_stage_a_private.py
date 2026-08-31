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
    bind_independent_authority_review,
    bind_numeric_atom,
    bind_period_domain,
    bind_candidate_objects,
    bind_task_numeric_parameter,
    build_exact_derivation,
    compile_requirement_plan,
    digest,
    extract_numeric_candidates,
    extract_period_domain_candidates,
    extract_tabular_schedule_series,
    screen_authority_applicability,
    validate_authority_node,
)
from run_claim_construction_private import Gateway, SectionIndex, _evidence, _model_call
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
PERIOD_DOMAIN_PAYLOAD = {
    "type": "object", "additionalProperties": False,
    "required": ["requirement_id", "evidence_id", "exact_excerpt", "periods"],
    "properties": {
        "requirement_id": {"type": "string"}, "evidence_id": {"type": "string"},
        "exact_excerpt": {"type": "string", "maxLength": 2000},
        "periods": {"type": "array", "minItems": 1, "maxItems": 32,
                    "items": {"type": "string", "pattern": "^(19|20)[0-9]{2}$"}},
    },
}
AUTHORITY_OUTPUT = {"type": "object", "additionalProperties": False,
                    "required": ["authority_nodes"],
                    "properties": {"authority_nodes": {"type": "array", "maxItems": 48,
                                                           "items": AUTHORITY_PAYLOAD}}}
PERIOD_DOMAIN_SELECTION_ITEM = {
    "type": "object", "additionalProperties": False,
    "required": ["requirement_id", "evidence_id", "candidate_id"],
    "properties": {
        "requirement_id": {"type": "string"},
        "evidence_id": {"type": "string"},
        "candidate_id": {"type": "string"},
    },
}
PERIOD_DOMAIN_OUTPUT = {
    "type": "object", "additionalProperties": False,
    "required": ["period_domain_selections"],
    "properties": {"period_domain_selections": {"type": "array", "maxItems": 16,
                                                   "items": PERIOD_DOMAIN_SELECTION_ITEM}},
}
NUMERIC_SELECTION_ITEM = {
    "type": "object", "additionalProperties": False,
    "required": ["requirement_id", "evidence_id", "candidate_id", "subject", "predicate",
                 "currency", "unit", "entity", "period", "precision", "effective_date",
                 "qualification", "document_version", "exact_excerpt"],
    "properties": {
        "requirement_id": {"type": "string"}, "evidence_id": {"type": "string"},
        "candidate_id": {"type": "string"}, "subject": {"type": "string"},
        "predicate": {"type": "string"}, "currency": {"type": ["string", "null"]},
        "unit": {"type": "string"}, "entity": {"type": "string"},
        "period": {"type": "string"},
        "precision": {"type": "string", "enum": sorted(PRECISION_STATES)},
        "effective_date": {"type": ["string", "null"]},
        "qualification": {"type": ["string", "null"]},
        "document_version": {"type": ["string", "null"]},
        "exact_excerpt": {"type": "string", "maxLength": 1600},
    },
}
NUMERIC_SELECTION_OUTPUT = {
    "type": "object", "additionalProperties": False,
    "required": ["numeric_selections"],
    "properties": {"numeric_selections": {"type": "array", "maxItems": 64,
                                               "items": NUMERIC_SELECTION_ITEM}},
}
TABLE_SERIES_SELECTION_OUTPUT = {
    "type": "object", "additionalProperties": False,
    "required": ["table_series_selections"],
    "properties": {"table_series_selections": {"type": "array", "maxItems": 16,
        "items": {"type": "object", "additionalProperties": False,
                  "required": ["requirement_id", "evidence_id", "series_candidate_id"],
                  "properties": {"requirement_id": {"type": "string"},
                                 "evidence_id": {"type": "string"},
                                 "series_candidate_id": {"type": "string"}}}}},
}
EXTRACTION_OUTPUT = {
    "type": "object", "additionalProperties": False,
    "required": ["evidence_atoms", "numeric_atoms", "task_parameters", "authority_nodes",
                 "period_domains"],
    "properties": {
        "evidence_atoms": {"type": "array", "maxItems": 48, "items": ATOM_PAYLOAD},
        "numeric_atoms": {"type": "array", "maxItems": 48, "items": NUMERIC_PAYLOAD},
        "task_parameters": {"type": "array", "maxItems": 24, "items": PARAMETER_PAYLOAD},
        "authority_nodes": {"type": "array", "maxItems": 48, "items": AUTHORITY_PAYLOAD},
        "period_domains": {"type": "array", "maxItems": 16,
                           "items": PERIOD_DOMAIN_PAYLOAD},
    },
}
DERIVATION_ITEM = {
    "type": "object", "additionalProperties": False,
    "required": ["requirement_id", "expression", "variables", "input_bindings",
                 "input_requirement_ids", "output_unit", "entity", "period", "round_places"],
    "properties": {
        "requirement_id": {"type": "string"}, "expression": {"type": "string"},
        "variables": {"type": "object", "additionalProperties": {"type": "string"}},
        "input_bindings": {"type": "object", "additionalProperties": {"type": "string"}},
        "input_requirement_ids": {"type": "object",
                                  "additionalProperties": {"type": "string"}},
        "output_unit": {"type": "string"}, "entity": {"type": "string"},
        "period": {"type": "string"}, "round_places": {"type": "integer", "minimum": 0, "maximum": 12},
    },
}
DERIVATION_OUTPUT = {"type": "object", "additionalProperties": False,
                     "required": ["derivations"],
                     "properties": {"derivations": {"type": "array", "maxItems": 24,
                                                        "items": DERIVATION_ITEM}}}
PERIOD_DERIVATION_TEMPLATE_OUTPUT = {
    "type": "object", "additionalProperties": False,
    "required": ["templates"],
    "properties": {"templates": {"type": "array", "maxItems": 1, "items": {
        "type": "object", "additionalProperties": False,
        "required": ["requirement_id", "expression", "variable_requirement_ids",
                     "output_unit", "entity", "round_places"],
        "properties": {
            "requirement_id": {"type": "string"},
            "expression": {"type": "string"},
            "variable_requirement_ids": {
                "type": "object", "additionalProperties": {"type": "string"}},
            "output_unit": {"type": "string"},
            "entity": {"type": "string"},
            "round_places": {"type": "integer", "minimum": 0, "maximum": 12},
        },
    }}},
}
AUTHORITY_REVIEW_OUTPUT = {
    "type": "object", "additionalProperties": False,
    "required": ["decisions"],
    "properties": {"decisions": {"type": "array", "maxItems": 48, "items": {
        "type": "object", "additionalProperties": False,
        "required": ["authority_id", "supports_candidate"],
        "properties": {"authority_id": {"type": "string"},
                       "supports_candidate": {"type": "boolean"}},
    }}},
}


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


def _unbounded_period_retrieval(slots: list[dict[str, Any]],
                                index: SectionIndex) -> tuple[dict[str, dict[str, Any]],
                                                              list[dict[str, Any]]]:
    """Scan every BM25 match, retaining only sections with exact period spans.

    This lane removes retrieval top-k as a completeness confound.  Projection
    remains chunked later for provider context, but no matching candidate is
    discarded because of rank.
    """
    receipts: dict[str, dict[str, Any]] = {}
    audit = []
    for slot in slots:
        if slot["slot_type"] != "value_by_period":
            continue
        queries = [str(row) for row in slot.get("search_queries", []) if str(row).strip()]
        description = str(slot.get("description") or "").strip()
        if description:
            queries.append(description)
        queries = list(dict.fromkeys(queries))
        seen_sections: set[tuple[str, str]] = set()
        selected = []
        matching_section_count = 0
        for query in queries:
            hits = index.search(query, max_documents=len(index.doc_meta),
                                max_sections=len(index.sections))
            for hit in hits:
                section = hit["section"]
                key = (section["uri"], section["id"])
                if key in seen_sections:
                    continue
                seen_sections.add(key)
                matching_section_count += 1
                if not extract_period_domain_candidates(str(section.get("text") or "")):
                    continue
                selected.append(_evidence(slot["slot_id"], hit, query))
        for row in selected:
            source = row.get("source") or {}
            receipts[row["evidence_id"]] = {
                "evidence_id": row["evidence_id"], "receipt_digest": row["receipt_digest"],
                "source_digest": source.get("content_digest"), "custody_valid": True,
                "quote": row["quote"], "locator": row["locator"], "source": source,
            }
        audit.append({"requirement_id": slot["slot_id"],
                      "evidence_ids": [row["evidence_id"] for row in selected],
                      "ranked_section_count": matching_section_count,
                      "period_candidate_section_count": len(selected),
                      "retrieval_limit": None})
    return receipts, audit


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
            "For every value_by_period slot, construct a period_domain only when one receipt contains an explicit "
            "schedule enumeration: copy every four-digit year in that closed schedule into periods and bind the exact "
            "excerpt. Do not turn phrases like each affected year or two endpoints into a closed domain. "
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


def _controlled_authority_candidates(slots: list[dict[str, Any]],
                                     receipts: dict[str, dict[str, Any]],
                                     audit: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Project deterministic candidates from controlled official receipts.

    The source manifest already fixes citation, jurisdiction, effective date,
    and authority level.  Re-generating those fields with a model only creates
    invalid variants.  Responsiveness remains a separate independent screen.
    """
    by_slot = {row["requirement_id"]: row for row in audit}
    candidates = []
    selected_count = 0
    for slot in slots:
        if "authority_node" not in slot["required_object_kinds"]:
            continue
        count = 0
        for evidence_id in by_slot.get(slot["slot_id"], {}).get("evidence_ids", []):
            receipt = receipts[evidence_id]
            metadata = (receipt.get("source") or {}).get("official_authority")
            if not isinstance(metadata, dict):
                continue
            citations = metadata.get("canonical_citations") or []
            if not citations:
                continue
            citation = citations[0]
            quote = str(receipt.get("quote") or "")
            citation_start = quote.find(citation)
            if citation_start < 0:
                continue
            excerpt_start = max(0, citation_start - 200)
            excerpt = quote[excerpt_start:excerpt_start + 2000]
            candidates.append({
                "requirement_id": slot["slot_id"], "evidence_id": evidence_id,
                "citation": citation, "proposition": excerpt,
                "jurisdiction": metadata["jurisdiction"],
                "effective_date": metadata["effective_on"],
                "authority_level": metadata["authority_level"],
                "exact_excerpt": excerpt,
            })
            count += 1
            selected_count += 1
            if count >= 4:
                break
    return candidates, {"status": "ok", "authority_candidate_count": len(candidates),
                        "official_receipt_count": selected_count,
                        "construction_mode": "deterministic_controlled_metadata_projection"}


def _extract_period_domains(gateway: Gateway, slots: list[dict[str, Any]],
                            receipts: dict[str, dict[str, Any]],
                            audit: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    by_slot = {row["requirement_id"]: row for row in audit}
    inventory_index: dict[tuple[str, str], dict[str, Any]] = {}
    candidates_by_requirement: dict[str, list[dict[str, Any]]] = {}
    period_slots = [row for row in slots if row["slot_type"] == "value_by_period"]
    for slot in period_slots:
        requirement_id = slot["slot_id"]
        routed: set[tuple[str, str]] = set()
        candidates_by_requirement[requirement_id] = []
        for evidence_id in by_slot.get(requirement_id, {}).get("evidence_ids", []):
            receipt = receipts[evidence_id]
            inventory = extract_period_domain_candidates(str(receipt.get("quote") or ""))
            for candidate in inventory:
                inventory_index[(evidence_id, candidate["candidate_id"])] = candidate
                key = (evidence_id, candidate["candidate_id"])
                if key in routed:
                    continue
                routed.add(key)
                candidates_by_requirement[requirement_id].append({
                    "requirement_id": requirement_id,
                    "evidence_id": evidence_id,
                    "candidate_id": candidate["candidate_id"],
                    "exact_excerpt": candidate["exact_excerpt"],
                    "periods": candidate["periods"],
                })
    inventory_counts = {key: len(value) for key, value in sorted(candidates_by_requirement.items())}
    candidate_receipts = {row["evidence_id"] for values in candidates_by_requirement.values()
                          for row in values}
    if not period_slots or not any(candidates_by_requirement.values()):
        return [], {"status": "ok", "period_domain_count": 0,
                    "candidate_receipt_count": len(candidate_receipts),
                    "inventory_candidate_count": len(inventory_index),
                    "inventory_candidate_count_by_requirement": inventory_counts,
                    "selected_requirement_ids": [],
                    "selection_batch_count": 0,
                    "provisional_selection_count": 0,
                    "invariant_failures": []}

    slot_by_id = {row["slot_id"]: row for row in period_slots}
    failures: list[str] = []
    provisional: dict[str, list[dict[str, Any]]] = {key: [] for key in candidates_by_requirement}
    batch_count = 0

    def chunks(values: list[dict[str, Any]], character_budget: int = 28000):
        batch: list[dict[str, Any]] = []
        size = 0
        for value in values:
            value_size = len(json.dumps(value, ensure_ascii=False))
            if batch and size + value_size > character_budget:
                yield batch
                batch, size = [], 0
            batch.append(value); size += value_size
        if batch:
            yield batch

    def accepted_selections(value: dict[str, Any], requirement_id: str,
                            allowed: set[tuple[str, str]]) -> list[dict[str, Any]]:
        accepted = []
        for selection in value.get("period_domain_selections", []):
            evidence_id = str(selection.get("evidence_id") or "")
            candidate_id = str(selection.get("candidate_id") or "")
            if (selection.get("requirement_id") != requirement_id
                    or (evidence_id, candidate_id) not in allowed):
                failures.append("period_selection:unknown_candidate_or_requirement_id")
                continue
            candidate = inventory_index[(evidence_id, candidate_id)]
            accepted.append({"requirement_id": requirement_id, "evidence_id": evidence_id,
                             "candidate_id": candidate_id,
                             "exact_excerpt": candidate["exact_excerpt"],
                             "periods": candidate["periods"]})
        if len(accepted) > 1:
            failures.append("period_selection:duplicate_requirement_id")
            return []
        return accepted

    instruction = (
        "Select at most one candidate only when its exact excerpt explicitly enumerates the complete annual schedule "
        "needed by this requirement. Copy requirement_id, evidence_id, and candidate_id exactly. Reject publication "
        "years, citation years, isolated endpoints, inferred intermediate years, task-prompt periods, and incomplete "
        "schedules. Omit the requirement when no candidate proves a closed domain.")
    for requirement_id, candidates in candidates_by_requirement.items():
        allowed = {(row["evidence_id"], row["candidate_id"]) for row in candidates}
        for batch in chunks(candidates):
            batch_count += 1
            payload = {"requirement": {"requirement_id": requirement_id,
                                        "description": slot_by_id[requirement_id]["description"]},
                       "period_domain_candidates": batch, "instruction": instruction}
            result = _model_call(gateway, "Select a source-bound closed annual period domain.",
                                 json.dumps(payload, ensure_ascii=False), 6000,
                                 PERIOD_DOMAIN_OUTPUT,
                                 "proofpress_period_domain_candidate_selection", 2)
            if not result["ok"]:
                return [], {"status": "inconclusive", "period_domain_count": 0,
                            "candidate_receipt_count": len(candidate_receipts),
                            "inventory_candidate_count": len(inventory_index),
                            "inventory_candidate_count_by_requirement": inventory_counts,
                            "selected_requirement_ids": [],
                            "selection_batch_count": batch_count,
                            "provisional_selection_count": sum(map(len, provisional.values())),
                            "invariant_failures": failures, "failure": result["record"]}
            provisional[requirement_id].extend(
                accepted_selections(result["value"], requirement_id, allowed))

    rows = []
    seen_requirements = set()
    for requirement_id, candidates in provisional.items():
        unique = {(row["evidence_id"], row["candidate_id"]): row for row in candidates}
        finalists = list(unique.values())
        if not finalists:
            continue
        chosen = finalists
        if len(finalists) > 1:
            batch_count += 1
            allowed = set(unique)
            payload = {"requirement": {"requirement_id": requirement_id,
                                        "description": slot_by_id[requirement_id]["description"]},
                       "period_domain_candidates": finalists,
                       "instruction": instruction + " These candidates survived independent batch screening; choose at most one."}
            result = _model_call(gateway, "Resolve a source-bound closed annual period domain.",
                                 json.dumps(payload, ensure_ascii=False), 6000,
                                 PERIOD_DOMAIN_OUTPUT,
                                 "proofpress_period_domain_candidate_resolution", 2)
            if not result["ok"]:
                return [], {"status": "inconclusive", "period_domain_count": 0,
                            "candidate_receipt_count": len(candidate_receipts),
                            "inventory_candidate_count": len(inventory_index),
                            "inventory_candidate_count_by_requirement": inventory_counts,
                            "selected_requirement_ids": [],
                            "selection_batch_count": batch_count,
                            "provisional_selection_count": sum(map(len, provisional.values())),
                            "invariant_failures": failures, "failure": result["record"]}
            chosen = accepted_selections(result["value"], requirement_id, allowed)
        if chosen:
            seen_requirements.add(requirement_id)
            row = chosen[0]
            rows.append({key: row[key] for key in
                         ("requirement_id", "evidence_id", "exact_excerpt", "periods")})
    return rows, {"status": "ok", "period_domain_count": len(rows),
                  "candidate_receipt_count": len(candidate_receipts),
                  "inventory_candidate_count": len(inventory_index),
                  "inventory_candidate_count_by_requirement": inventory_counts,
                  "selected_requirement_ids": sorted(seen_requirements),
                  "selection_batch_count": batch_count,
                  "provisional_selection_count": sum(map(len, provisional.values())),
                  "invariant_failures": failures}


def _extract_numeric_atoms(gateway: Gateway, slots: list[dict[str, Any]],
                           receipts: dict[str, dict[str, Any]],
                           audit: list[dict[str, Any]],
                           period_domains: list[dict[str, Any]] = ()) -> tuple[list[dict[str, Any]],
                                                                             dict[str, Any]]:
    """Select semantic numbers, prioritizing every number in a chosen schedule span."""
    by_slot = {row["requirement_id"]: row for row in audit}
    periods_by_slot: dict[str, list[dict[str, Any]]] = {}
    for domain in period_domains:
        periods_by_slot.setdefault(domain["requirement_id"], []).append(domain)
    selected_by_evidence: dict[str, dict[str, Any]] = {}
    inventory_index: dict[tuple[str, str], dict[str, Any]] = {}
    context_index: dict[tuple[str, str], str] = {}
    priority_inventory_count = 0
    for slot in slots:
        if slot["slot_type"] == "output_structure":
            continue
        priority = periods_by_slot.get(slot["slot_id"], [])
        routed = [(row["evidence_id"], row["exact_excerpt"], True) for row in priority]
        priority_ids = {row[0] for row in routed}
        routed.extend((evidence_id, str(receipts[evidence_id].get("quote") or ""), False)
                      for evidence_id in by_slot.get(slot["slot_id"], {}).get("evidence_ids", [])[:6]
                      if evidence_id not in priority_ids)
        for evidence_id, inventory_text, is_priority in routed:
            inventory = [row for row in extract_numeric_candidates(inventory_text)
                         if row.get("normalized_value") is not None]
            if not inventory:
                continue
            projected_inventory = inventory if is_priority else inventory[:48]
            if is_priority:
                priority_inventory_count += len(projected_inventory)
            row = selected_by_evidence.setdefault(
                evidence_id, {"evidence_id": evidence_id,
                              "numeric_candidate_contexts": [], "requirements": []})
            known = {candidate["candidate_id"] for candidate in row["numeric_candidate_contexts"]}
            for candidate in projected_inventory:
                inventory_index[(evidence_id, candidate["candidate_id"])] = candidate
                if candidate["candidate_id"] in known:
                    continue
                start = max(0, int(candidate["start"]) - 260)
                end = min(len(inventory_text), int(candidate["end"]) + 420)
                exact_context = inventory_text[start:end]
                context_index[(evidence_id, candidate["candidate_id"])] = exact_context
                row["numeric_candidate_contexts"].append(
                    {**candidate, "exact_context": exact_context,
                     "priority_period_source": is_priority})
                known.add(candidate["candidate_id"])
            requirement = {"requirement_id": slot["slot_id"],
                           "requirement": slot["description"],
                           "required_periods": sorted({period for domain in priority
                                                       for period in domain["periods"]})}
            if requirement not in row["requirements"]:
                row["requirements"].append(requirement)
    selected = list(selected_by_evidence.values())
    if not selected:
        return [], {"status": "ok", "selection_count": 0,
                    "inventory_candidate_count": 0,
                    "priority_period_inventory_candidate_count": 0,
                    "invariant_failures": []}
    payload = {
        "requirement_receipts": selected,
        "instruction": (
            "Each receipt carries the requirements it may support. Select only material numeric candidates that "
            "directly support one listed requirement or a deterministic calculation for it. Copy requirement_id, "
            "evidence_id, and candidate_id exactly; do not rewrite the numeric display. Subject and predicate must be "
            "exact_context substrings, and exact_excerpt must be an exact_context substring containing subject, "
            "predicate, and the selected candidate. Record entity, period, unit/currency, precision, qualifications, "
            "and version without calculating or inferring missing values. When required_periods is non-empty, select "
            "the material value for every explicitly supported required period and copy its four-digit period exactly. "
            "Years used only in citations or document "
            "metadata are not matter-value atoms. Omit ambiguous candidates."),
    }
    result = _model_call(gateway, "Select source-bound numeric atoms from deterministic inventories.",
                         json.dumps(payload, ensure_ascii=False), 20000,
                         NUMERIC_SELECTION_OUTPUT, "proofpress_numeric_candidate_selection", 2)
    if not result["ok"]:
        return [], {"status": "inconclusive", "selection_count": 0,
                    "inventory_candidate_count": len(inventory_index),
                    "priority_period_inventory_candidate_count": priority_inventory_count,
                    "invariant_failures": [], "failure": result["record"]}
    rows = []
    failures = []
    for selection in result["value"].get("numeric_selections", []):
        key = (str(selection.get("evidence_id") or ""),
               str(selection.get("candidate_id") or ""))
        candidate = inventory_index.get(key)
        if candidate is None:
            failures.append("numeric_selection:unknown_candidate_id")
            continue
        context = context_index.get(key, "")
        fields = [str(selection.get(field) or "") for field in ("subject", "predicate")]
        fields.append(candidate["raw_text"])
        positions = [(context.find(field), len(field)) for field in fields if field]
        exact_excerpt = selection.get("exact_excerpt")
        if len(positions) == 3 and all(start >= 0 for start, _ in positions):
            start = min(row[0] for row in positions)
            end = max(row[0] + row[1] for row in positions)
            exact_excerpt = context[start:end]
        rows.append({
            **{field: selection.get(field) for field in (
                "requirement_id", "evidence_id", "subject", "predicate", "currency", "unit",
                "entity", "period", "precision", "effective_date", "qualification",
                "document_version")},
            "exact_excerpt": exact_excerpt,
            "display": candidate["raw_text"], "kind": candidate["kind_hint"],
        })
    malformed_count = 0
    for receipt in receipts.values():
        malformed_count += sum(row.get("normalization_error") is not None
                               for row in extract_numeric_candidates(str(receipt.get("quote") or "")))
    if malformed_count:
        failures.append(f"numeric_inventory:normalization_error_count_{malformed_count}")
    return rows, {"status": "ok", "selection_count": len(rows),
                  "inventory_candidate_count": len(inventory_index),
                  "priority_period_inventory_candidate_count": priority_inventory_count,
                  "malformed_inventory_count": malformed_count,
                  "invariant_failures": failures}


def _extract_period_numeric_atoms(gateway: Gateway,
                                  slots: list[dict[str, Any]],
                                  receipts: dict[str, dict[str, Any]],
                                  period_domains: list[dict[str, Any]]) -> tuple[list[dict[str, Any]],
                                                                               dict[str, Any]]:
    """Bind one requirement-aware TSV series, then construct every cell deterministically."""
    slot_by_id = {row["slot_id"]: row for row in slots}
    rows: list[dict[str, Any]] = []
    failures: list[str] = []
    series_inventory_count = 0
    complete_series_count = 0
    selected_series_count = 0
    missing_complete_table_count = 0
    call_count = 0
    for domain in period_domains:
        requirement_id = domain["requirement_id"]
        evidence_id = domain["evidence_id"]
        receipt = receipts[evidence_id]
        inventory = extract_tabular_schedule_series(str(receipt.get("quote") or ""))
        series_inventory_count += len(inventory)
        required_periods = sorted(domain["periods"])
        complete = [candidate for candidate in inventory
                    if sorted(value["period"] for value in candidate["period_values"])
                    == required_periods]
        complete_series_count += len(complete)
        if not complete:
            missing_complete_table_count += 1
            failures.append("period_table_series:no_complete_series_candidate")
            continue
        index = {row["series_candidate_id"]: row for row in complete}
        payload = {
            "requirement": {"requirement_id": requirement_id,
                            "description": slot_by_id[requirement_id]["description"],
                            "required_periods": required_periods},
            "evidence_id": evidence_id,
            "table_series_candidates": [
                {"series_candidate_id": candidate["series_candidate_id"],
                 "table_candidate_id": candidate["table_candidate_id"],
                 "orientation": candidate["orientation"],
                 "label": candidate["label"],
                 "periods": [value["period"] for value in candidate["period_values"]],
                 "value_count": len(candidate["period_values"])}
                for candidate in complete],
            "instruction": (
                "Select at most one complete table series whose exact source label directly names the values requested "
                "by this requirement. Copy requirement_id, evidence_id, and series_candidate_id exactly. Do not select "
                "a related column, a calculated output absent from the source table, or a series based only on similar "
                "numbers. Omit the requirement when no label directly identifies the requested series. Cell values "
                "are deliberately withheld here because deterministic code will bind them after column selection."),
        }
        call_count += 1
        result = _model_call(gateway, "Select one requirement-aware source table series.",
                             json.dumps(payload, ensure_ascii=False), 6000,
                             TABLE_SERIES_SELECTION_OUTPUT,
                             "proofpress_table_series_selection", 2)
        if not result["ok"]:
            return [], {"status": "inconclusive", "selection_count": 0,
                        "table_series_candidate_count": series_inventory_count,
                        "complete_table_series_candidate_count": complete_series_count,
                        "selected_series_count": selected_series_count,
                        "constructed_cell_count": len(rows),
                        "missing_complete_table_count": missing_complete_table_count,
                        "call_count": call_count, "invariant_failures": failures,
                        "failure": result["record"]}
        accepted = []
        for selection in result["value"].get("table_series_selections", []):
            candidate_id = str(selection.get("series_candidate_id") or "")
            candidate = index.get(candidate_id)
            if (selection.get("requirement_id") != requirement_id
                    or selection.get("evidence_id") != evidence_id
                    or candidate is None):
                failures.append("period_table_series:unknown_candidate_or_route")
                continue
            if candidate_id in {row["series_candidate_id"] for row in accepted}:
                failures.append("period_table_series:duplicate_candidate")
                continue
            accepted.append(candidate)
        if len(accepted) > 1:
            failures.append("period_table_series:multiple_series_for_requirement")
            continue
        if not accepted:
            continue
        selected_series_count += 1
        candidate = accepted[0]
        excerpt = candidate["exact_excerpt"]
        explicit_currency = any(value["kind_hint"] == "currency"
                                for value in candidate["period_values"])
        for value in candidate["period_values"]:
            table_binding = {
                "table_candidate_id": candidate["table_candidate_id"],
                "series_candidate_id": candidate["series_candidate_id"],
                "orientation": candidate["orientation"],
                "row_index": value["row_index"],
                "column_index": value["column_index"],
                "label_span": candidate["label_span"],
                "period_span": value["period_span"],
                "value_span": value["value_span"],
            }
            rows.append({
                "requirement_id": requirement_id, "evidence_id": evidence_id,
                "subject": candidate["label"], "predicate": value["period"],
                "currency": "USD" if explicit_currency else None,
                "unit": "USD" if explicit_currency else "source-table units",
                "entity": candidate["label"], "period": value["period"],
                "precision": "exact", "effective_date": value["period"],
                "qualification": None, "document_version": "unknown",
                "exact_excerpt": excerpt, "display": value["display"],
                "kind": "currency" if explicit_currency else value["kind_hint"],
                "table_cell_binding": table_binding,
            })
    return rows, {"status": "ok", "selection_count": len(rows),
                  "table_series_candidate_count": series_inventory_count,
                  "complete_table_series_candidate_count": complete_series_count,
                  "selected_series_count": selected_series_count,
                  "constructed_cell_count": len(rows),
                  "missing_complete_table_count": missing_complete_table_count,
                  "call_count": call_count, "invariant_failures": failures}


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
        ("evidence_atoms", "numeric_atoms", "task_parameters", "authority_nodes",
         "period_domains")}
    builders = (
        ("evidence_atoms", lambda row: bind_evidence_atom(row, receipts)),
        ("numeric_atoms", lambda row: bind_numeric_atom(row, receipts)),
        ("task_parameters", lambda row: bind_task_numeric_parameter(task["prompt"], row)),
        ("authority_nodes", lambda row: _authority(row, receipts)),
        ("period_domains", lambda row: bind_period_domain(row, receipts)),
    )

    def repair_excerpt(label: str, raw: dict[str, Any]) -> dict[str, Any]:
        if label == "period_domains":
            receipt = receipts.get(raw.get("evidence_id"))
            quote = str((receipt or {}).get("quote") or "")
            excerpt = str(raw.get("exact_excerpt") or "")
            if excerpt and excerpt in quote:
                return raw
            positions = [(quote.find(str(period)), len(str(period)))
                         for period in raw.get("periods", [])]
            if positions and all(start >= 0 for start, _ in positions):
                start = min(row[0] for row in positions)
                end = max(row[0] + row[1] for row in positions)
                if end - start <= 2000:
                    return {**raw, "exact_excerpt": quote[start:end]}
            return raw
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
            "period domain": "period_domain_invalid",
            "every period": "period_domain_not_explicit",
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
                object_id = (built.get("atom_id") or built.get("parameter_id")
                             or built.get("authority_id") or built.get("period_domain_id"))
                if object_id not in seen:
                    result[label].append(built); seen.add(object_id)
            except (KeyError, TypeError, ValueError) as exc:
                failures.append(f"{label}:{failure_code(exc)}:{digest(str(exc))[-12:]}")
    return result, failures


def _plan_derivations(gateway: Gateway, slots: list[dict[str, Any]],
                      objects: dict[str, list[dict[str, Any]]]) -> tuple[list[dict[str, Any]],
                                                                        dict[str, Any]]:
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
                   "exactly, bind its object_id, and copy the input object's requirement_id into input_requirement_ids. "
                   "Inputs may come from supporting factual or rate slots; the output requirement_id remains the slot "
                   "being calculated. Use only + - * / parentheses and declared variable names. Create one "
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
                input_requirement_ids=spec["input_requirement_ids"],
                numeric_atoms=atoms, task_parameters=params, output_unit=spec["output_unit"],
                entity=spec["entity"], period=spec["period"], round_places=spec["round_places"]))
        except (KeyError, TypeError, ValueError) as exc:
            failures.append(f"derivation:{type(exc).__name__}:{digest(str(exc))[-12:]}")
    return derivations, {"status": "ok", "derivation_count": len(derivations),
                         "invariant_failures": failures}


def _plan_period_derivations(
        gateway: Gateway, slots: list[dict[str, Any]],
        objects: dict[str, list[dict[str, Any]]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Select one formula template, then bind every period deterministically."""
    slot_by_id = {row["slot_id"]: row for row in slots}
    atoms_by_requirement: dict[str, list[dict[str, Any]]] = {}
    for atom in objects["numeric_atoms"]:
        atoms_by_requirement.setdefault(atom["requirement_id"], []).append(atom)
    for parameter in objects["task_parameters"]:
        atoms_by_requirement.setdefault(parameter["requirement_id"], []).append(parameter)
    derivations = []
    failures = []
    call_count = 0
    skipped_source_complete = 0
    attempted_requirement_ids = []
    excluded_conflicting_input_requirement_count = 0
    for domain in objects.get("period_domains", []):
        requirement_id = domain["requirement_id"]
        slot = slot_by_id[requirement_id]
        if "derivation_node" not in slot["required_object_kinds"]:
            continue
        required_periods = sorted(domain["periods"])
        direct_periods = sorted({row["numeric"]["period"]
                                 for row in atoms_by_requirement.get(requirement_id, [])})
        if direct_periods == required_periods:
            skipped_source_complete += 1
            continue
        attempted_requirement_ids.append(requirement_id)
        input_catalog = []
        allowed_source_requirement_ids = set()
        for source_requirement_id, candidates in sorted(atoms_by_requirement.items()):
            if source_requirement_id == requirement_id:
                continue
            resolvable = True
            for period in required_periods:
                same_period = [row for row in candidates if row["numeric"]["period"] == period]
                eligible = same_period or [row for row in candidates
                                           if not str(row["numeric"]["period"]).isdigit()]
                if (not eligible
                        or len({row["numeric"]["decimal_value"] for row in eligible}) != 1):
                    resolvable = False
                    break
            if not resolvable:
                excluded_conflicting_input_requirement_count += 1
                continue
            allowed_source_requirement_ids.add(source_requirement_id)
            input_catalog.append({
                "source_requirement_id": source_requirement_id,
                "description": slot_by_id.get(source_requirement_id, {}).get("description"),
                "available_periods": sorted({row["numeric"]["period"] for row in candidates}),
                "numeric_kinds": sorted({row["numeric"]["kind"] for row in candidates}),
                "units": sorted({str(row["numeric"].get("unit") or "") for row in candidates}),
                "input_kinds": sorted({"task_parameter" if row.get("parameter_id")
                                       else "evidence_atom" for row in candidates}),
            })
        payload = {
            "target_requirement": {"requirement_id": requirement_id,
                                   "description": slot["description"],
                                   "required_periods": required_periods,
                                   "output_format": slot.get("output_format")},
            "available_input_requirements": input_catalog,
            "instruction": (
                "Return at most one algebraic formula template only when the target description explicitly states "
                "the calculation and the listed source requirements supply every needed input. Map each variable "
                "name to one source_requirement_id exactly; never copy object IDs or numeric values. The expression "
                "may use + - * / parentheses and numeric constants. Do not use the target requirement as its own "
                "input, invent a legal rule, or fill a missing source requirement. The same formula must apply to "
                "every required period. Deterministic code will bind exact same-period cells and recompute results."),
        }
        call_count += 1
        result = _model_call(
            gateway, "Select one requirement-aware annual derivation template.",
            json.dumps(payload, ensure_ascii=False), 6000,
            PERIOD_DERIVATION_TEMPLATE_OUTPUT,
            "proofpress_period_derivation_template", 2)
        if not result["ok"]:
            return [], {"status": "inconclusive", "derivation_count": 0,
                        "call_count": call_count,
                        "attempted_requirement_ids": attempted_requirement_ids,
                        "skipped_source_complete": skipped_source_complete,
                        "excluded_conflicting_input_requirement_count":
                            excluded_conflicting_input_requirement_count,
                        "invariant_failures": failures,
                        "failure": result["record"]}
        templates = result["value"].get("templates", [])
        if not templates:
            failures.append("period_derivation:incomplete_period_set")
            continue
        template = templates[0]
        sources = template.get("variable_requirement_ids") or {}
        if (template.get("requirement_id") != requirement_id or not sources
                or requirement_id in set(sources.values())
                or any(source_id not in allowed_source_requirement_ids
                       for source_id in sources.values())):
            failures.append("period_derivation:invalid_template_route")
            continue
        planned = []
        for period in required_periods:
            bindings = {}
            variables = {}
            input_requirement_ids = {}
            unresolved = False
            for variable, source_requirement_id in sources.items():
                candidates = atoms_by_requirement[source_requirement_id]
                same_period = [row for row in candidates if row["numeric"]["period"] == period]
                eligible = same_period or [row for row in candidates
                                           if not str(row["numeric"]["period"]).isdigit()]
                values = {row["numeric"]["decimal_value"] for row in eligible}
                if not eligible or len(values) != 1:
                    unresolved = True
                    break
                chosen = sorted(eligible, key=lambda row: row.get("atom_id")
                                or row.get("parameter_id"))[0]
                object_id = chosen.get("atom_id") or chosen.get("parameter_id")
                bindings[variable] = object_id
                variables[variable] = chosen["numeric"]["decimal_value"]
                input_requirement_ids[variable] = source_requirement_id
            if unresolved:
                failures.append("period_derivation:missing_or_conflicting_period_input")
                planned = []
                break
            try:
                planned.append(build_exact_derivation(
                    requirement_id=requirement_id,
                    expression=template["expression"], variables=variables,
                    input_bindings=bindings,
                    input_requirement_ids=input_requirement_ids,
                    numeric_atoms={row["atom_id"]: row for row in objects["numeric_atoms"]},
                    task_parameters={row["parameter_id"]: row
                                     for row in objects["task_parameters"]},
                    output_unit=template["output_unit"], entity=template["entity"],
                    period=period, round_places=template["round_places"]))
            except (KeyError, TypeError, ValueError) as exc:
                failures.append("period_derivation:template_validation_"
                                + type(exc).__name__ + ":" + digest(str(exc))[-12:])
                planned = []
                break
        if len(planned) != len(required_periods):
            failures.append("period_derivation:incomplete_period_set")
            continue
        derivations.extend(planned)
    return derivations, {"status": "ok", "derivation_count": len(derivations),
                         "call_count": call_count,
                         "attempted_requirement_ids": attempted_requirement_ids,
                         "skipped_source_complete": skipped_source_complete,
                         "excluded_conflicting_input_requirement_count":
                             excluded_conflicting_input_requirement_count,
                         "invariant_failures": failures}


def _review_authority_applicability(
        gateway: Gateway, slots: list[dict[str, Any]],
        authority_nodes: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    slot_by_id = {row["slot_id"]: row for row in slots}
    deterministic = [screen_authority_applicability(
        slot_by_id[row["requirement_id"]]["description"], row) for row in authority_nodes]
    pending = []
    node_by_id = {row["authority_id"]: row for row in authority_nodes}
    for node, screen in zip(authority_nodes, deterministic):
        if screen["outcome"] != "independent_legal_review_required":
            continue
        pending.append({
            "authority_id": node["authority_id"],
            "requirement": slot_by_id[node["requirement_id"]]["description"],
            "citation": node["citation"],
            "proposition": node["proposition"],
            "exact_official_excerpt": node["exact_excerpt"][:2000],
            "jurisdiction": node["jurisdiction"],
            "effective_date": node["effective_date"],
            "authority_level": node["authority_level"],
        })
    if not pending:
        return deterministic, {"status": "ok", "reviewed": 0,
                               "supported_candidates": sum(
                                   row["outcome"] == "exact_reference_match_candidate"
                                   for row in deterministic),
                               "invariant_failures": []}
    payload = {
        "authority_candidates": pending,
        "instruction": (
            "Independently screen whether each official-source candidate directly supplies the legal authority "
            "requested by its requirement. This is requirement-to-proposition responsiveness only: do not apply facts, "
            "do not say the source controls the matter, and do not approve or admit anything. supports_candidate may be "
            "true only when the exact excerpt and proposition directly address the requested legal rule; related topics, "
            "procedural guidance, secondary authority, or missing conditions must be false. Return one decision per ID."),
    }
    result = _model_call(gateway, "Screen authority candidate responsiveness independently.",
                         json.dumps(payload, ensure_ascii=False), 14000,
                         AUTHORITY_REVIEW_OUTPUT, "proofpress_authority_applicability_review", 2)
    if not result["ok"]:
        return deterministic, {"status": "inconclusive", "reviewed": 0,
                               "supported_candidates": 0,
                               "failure": result["record"], "invariant_failures": []}
    decisions = result["value"].get("decisions", [])
    by_id: dict[str, bool] = {}
    failures = []
    pending_ids = {row["authority_id"] for row in pending}
    for row in decisions:
        authority_id = str(row.get("authority_id") or "")
        if authority_id not in pending_ids or authority_id in by_id:
            failures.append("authority_review:invalid_or_duplicate_authority_id")
            continue
        by_id[authority_id] = bool(row.get("supports_candidate"))
    if set(by_id) != pending_ids:
        failures.append("authority_review:incomplete_decision_set")
    record_digest = digest(result["record"])
    reviews = []
    for screen in deterministic:
        if screen["outcome"] != "independent_legal_review_required":
            reviews.append(screen)
            continue
        authority_id = screen["authority_id"]
        if authority_id not in by_id:
            reviews.append(screen)
            continue
        node = node_by_id[authority_id]
        reviews.append(bind_independent_authority_review(
            slot_by_id[node["requirement_id"]]["description"], node,
            supports_candidate=by_id[authority_id], review_record_digest=record_digest,
            reviewer_route=f'{ROUTE["model"]}@{ROUTE["provider"]}/{ROUTE["reasoning"]}'))
    return reviews, {"status": "ok", "reviewed": len(by_id),
                     "supported_candidates": sum(row["outcome"] in {
                         "exact_reference_match_candidate", "independent_review_supports_candidate"}
                         for row in reviews),
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
    authority_raw, authority_extraction = _controlled_authority_candidates(
        slots, receipts, audit) if authority_index is not None else ([], {"status": "ok"})
    # Controlled catalog metadata is the sole authority-candidate constructor
    # when the lane is enabled.  General extraction cannot add a parallel path.
    extracted["authority_nodes"] = authority_raw
    period_receipts, period_audit = _unbounded_period_retrieval(slots, index)
    period_raw, period_extraction = _extract_period_domains(
        gateways["period"], slots, period_receipts, period_audit)
    if period_extraction["status"] != "ok":
        return {"task_id": task["task_id"], "status": "inconclusive",
                "compiler": compiler, "extraction": extraction,
                "authority_extraction": authority_extraction,
                "period_extraction": period_extraction}
    selected_period_evidence = {row["evidence_id"] for row in period_raw}
    receipts.update({evidence_id: period_receipts[evidence_id]
                     for evidence_id in selected_period_evidence})
    extracted["period_domains"] = period_raw
    period_numeric_raw, period_numeric_extraction = _extract_period_numeric_atoms(
        gateways["numeric"], slots, receipts, period_raw)
    period_requirement_ids = {row["requirement_id"] for row in period_raw}
    general_numeric_raw, general_numeric_extraction = _extract_numeric_atoms(
        gateways["numeric"], [row for row in slots if row["slot_id"] not in period_requirement_ids],
        receipts, audit)
    numeric_raw = [*period_numeric_raw, *general_numeric_raw]
    numeric_extraction = {
        "status": ("ok" if period_numeric_extraction["status"] == "ok"
                   and general_numeric_extraction["status"] == "ok" else "inconclusive"),
        "selection_count": len(numeric_raw),
        "period_column_selection": period_numeric_extraction,
        "general_selection": general_numeric_extraction,
        "priority_period_inventory_candidate_count":
            period_numeric_extraction.get("complete_table_series_candidate_count", 0),
        "invariant_failures": [
            *period_numeric_extraction.get("invariant_failures", []),
            *general_numeric_extraction.get("invariant_failures", []),
        ],
    }
    if numeric_extraction["status"] != "ok":
        return {"task_id": task["task_id"], "status": "inconclusive",
                "compiler": compiler, "extraction": extraction,
                "authority_extraction": authority_extraction,
                "period_extraction": period_extraction,
                "numeric_extraction": numeric_extraction}
    extracted["numeric_atoms"] = numeric_raw
    objects, failures = _validated_objects(task, slots, extracted, receipts)
    failures.extend(period_extraction.get("invariant_failures", []))
    failures.extend(numeric_extraction.get("invariant_failures", []))
    authority_screens, authority_review_status = _review_authority_applicability(
        gateways["authority_reviewer"], slots, objects["authority_nodes"])
    failures.extend(authority_review_status.get("invariant_failures", []))
    period_derivations, period_derivation_status = _plan_period_derivations(
        gateways["derivation"], slots, objects)
    period_requirement_ids = {row["slot_id"] for row in slots
                              if row["slot_type"] == "value_by_period"}
    general_derivations, general_derivation_status = _plan_derivations(
        gateways["derivation"],
        [row for row in slots if row["slot_id"] not in period_requirement_ids], objects)
    derivations = [*period_derivations, *general_derivations]
    derivation_status = {
        "status": ("ok" if period_derivation_status["status"] == "ok"
                   and general_derivation_status["status"] == "ok" else "inconclusive"),
        "derivation_count": len(derivations),
        "period": period_derivation_status,
        "general": general_derivation_status,
        "invariant_failures": [*period_derivation_status.get("invariant_failures", []),
                               *general_derivation_status.get("invariant_failures", [])],
    }
    failures.extend(derivation_status["invariant_failures"])
    plan = bind_candidate_objects(
        plan, evidence_atoms=[*objects["evidence_atoms"], *objects["numeric_atoms"]],
        authority_nodes=objects["authority_nodes"], derivations=derivations,
        authority_screens=authority_screens)
    readiness = assess_requirement_readiness(
        plan, evidence_atoms=[*objects["evidence_atoms"], *objects["numeric_atoms"]],
        authority_nodes=objects["authority_nodes"], derivations=derivations,
        period_domains=objects["period_domains"], authority_screens=authority_screens)
    private = {"schema_version": SCHEMA, "task": task, "plan": plan, "receipts": receipts,
               "retrieval_audit": audit, "period_retrieval_audit": period_audit,
               "objects": objects, "derivations": derivations,
               "authority_screens": authority_screens,
               "readiness": readiness, "invariant_failures": failures,
               "stage_status": {"compiler": compiler, "extraction": extraction,
                                "authority_extraction": authority_extraction,
                                "authority_review": authority_review_status,
                                "period_extraction": period_extraction,
                                "numeric_extraction": numeric_extraction,
                                "derivation": derivation_status}}
    target = raw_dir / f'{task["task_id"]}.json'
    target.write_text(json.dumps(private, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    target.chmod(0o600)
    states = Counter(row["state"] for row in readiness["slots"])
    paths = Counter()
    for slot in plan["slots"]:
        slot_id = slot["slot_id"]
        ids = slot["object_ids"]
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
                              "period_domains": len(objects["period_domains"]),
                              "authority_screens": len(authority_screens),
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
                for role in ("compiler", "extractor", "authority_reviewer",
                             "period", "numeric", "derivation")}
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

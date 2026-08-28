"""Frozen contracts for the private legal knowledge-pipeline panel.

This module contains no corpus or model output.  It validates the boundary
between decomposition, retrieval, proposal, independent critique, disclosure,
and assimilation so a scored run cannot accidentally feed rubric/gold data
back into construction.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

SCHEMA = "proofpress/legal-pipeline-contract/v1"
MODEL_ROLES = {
    "decomposition": "inclusionai/ling-3.0-flash-fin",
    "candidate_proposer_repair": "inclusionai/ling-3.0-flash-fin",
    "coverage_critic": "gpt-5.6-sol",
    "pageindex": "deepseek/deepseek-v4-flash",
    "primary_executor": "deepseek/deepseek-v4-flash",
    "sensitivity_executor": "inclusionai/ling-3.0-flash-fin",
    "native_grader": "google/gemini-3.1-pro-preview",
}
EVIDENCE_ATOM_SCHEMA = "proofpress/evidence-atom/v1"
CLAIMABILITY_STATES = {
    "claimable", "partial", "gap", "conflict", "needs_legal_analysis",
}
LIFECYCLE_CHECKLIST = (
    "parties_capacity_authority", "economics_calculations",
    "representations_warranties", "pre_post_closing_covenants",
    "conditions_deliveries", "disclosure_schedules", "termination_remedies",
    "indemnity_liability_limits", "tax_regulatory",
    "employment_ip_privacy_compliance_litigation", "document_version_conflicts",
    "missing_evidence_negotiated_inputs",
)


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(value, ensure_ascii=False,
                                                   sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate_decomposition(task: str, inventory: list[dict[str, Any]], requirements: list[dict[str, Any]], *, rubric: Any = None, gold: Any = None) -> dict[str, Any]:
    if not isinstance(task, str) or not task.strip(): raise ValueError("task is required")
    if rubric is not None or gold is not None: raise ValueError("rubric and gold are forbidden during decomposition")
    if not isinstance(inventory, list) or not inventory: raise ValueError("source inventory is required")
    if not isinstance(requirements, list) or not 1 <= len(requirements) <= 32:
        raise ValueError("decomposition must contain at most 32 requirements")
    seen = set()
    for row in requirements:
        if not isinstance(row, dict) or not isinstance(row.get("requirement_id"), str) or row["requirement_id"] in seen:
            raise ValueError("requirements need unique requirement_id values")
        seen.add(row["requirement_id"])
        if not row.get("requirement") or row.get("applicability") not in {"applicable", "not_applicable", "uncertain"}:
            raise ValueError("requirement text and applicability are required")
        if row["applicability"] == "not_applicable" and not row.get("rationale"):
            raise ValueError("not_applicable requires an explicit rationale")
    return {"schema_version": SCHEMA, "task_digest": _digest(task),
            "inventory_digest": _digest(inventory), "requirement_count": len(requirements),
            "requirement_digest": _digest(requirements), "checklist": list(LIFECYCLE_CHECKLIST),
            "model": MODEL_ROLES["decomposition"], "frozen": False}


def coverage_pass(requirements: list[dict[str, Any]], additions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(additions, list) or len(additions) > 8: raise ValueError("coverage pass may add at most 8 requirements")
    existing = {row["requirement_id"] for row in requirements}
    for row in additions:
        if row.get("requirement_id") in existing: raise ValueError("coverage pass returned a duplicate requirement")
        existing.add(row.get("requirement_id"))
    merged = requirements + additions
    if len(merged) > 40: raise ValueError("frozen requirements cannot exceed 40")
    return merged


def freeze_requirements(requirements: list[dict[str, Any]]) -> dict[str, Any]:
    if len(requirements) > 40: raise ValueError("frozen requirements cannot exceed 40")
    return {"schema_version": SCHEMA, "requirements": requirements,
            "requirement_digest": _digest(requirements), "frozen": True,
            "models": MODEL_ROLES, "checklist": list(LIFECYCLE_CHECKLIST)}


def validate_candidate_claims(requirements: list[dict[str, Any]], claims: list[dict[str, Any]], relations: list[dict[str, Any]]) -> None:
    if len(claims) > 64 or len(relations) > 80: raise ValueError("candidate claim/relation limits exceeded")
    allowed = {"supports", "depends_on", "qualifies", "contradicts", "supersedes", "same_as"}
    for relation in relations:
        if relation.get("type") not in allowed: raise ValueError("unsupported claim relation")
    covered = {row.get("requirement_id") for row in claims if row.get("requirement_id")}
    for req in requirements:
        status = req.get("status")
        if status == "covered" and req.get("requirement_id") not in covered:
            raise ValueError("covered requirement must bind a candidate claim")


def validate_evidence_atom(atom: dict[str, Any], receipts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Validate a source-bound atom without granting it authority or admission."""
    if not isinstance(atom, dict) or atom.get("schema_version") != EVIDENCE_ATOM_SCHEMA:
        raise ValueError("evidence atom schema is required")
    required = ("atom_id", "requirement_id", "receipt_digest", "evidence_id",
                "subject", "predicate", "value", "support_mode")
    if any(not isinstance(atom.get(key), str) or not atom[key].strip() for key in required):
        raise ValueError("evidence atom required fields are missing")
    if atom["support_mode"] not in {"explicit", "inferred"}:
        raise ValueError("evidence atom support_mode is invalid")
    evidence = receipts.get(atom["evidence_id"])
    if not evidence or evidence.get("receipt_digest") != atom["receipt_digest"]:
        raise ValueError("evidence atom receipt binding is invalid")
    if atom.get("authority") is not None or atom.get("admission") is not None:
        raise ValueError("evidence atoms cannot carry authority or admission")
    atom_locator = atom.get("locator")
    if atom_locator != evidence.get("locator"):
        raise ValueError("evidence atom locator does not match its receipt")
    excerpt = atom.get("exact_excerpt")
    quote = evidence.get("quote")
    if not isinstance(excerpt, str) or not excerpt.strip() or not isinstance(quote, str) or excerpt not in quote:
        raise ValueError("evidence atom excerpt must be an exact receipt substring")
    return atom


def claimability_gate(requirement: dict[str, Any], atoms: list[dict[str, Any]], *,
                      conflict: bool = False) -> dict[str, Any]:
    """Return the only deterministic states allowed before proposal."""
    requirement_id = str(requirement.get("requirement_id", ""))
    bound = [row for row in atoms if row.get("requirement_id") == requirement_id]
    explicit = [row for row in bound if row.get("support_mode") == "explicit"]
    if conflict:
        state, reason = "conflict", "material_conflict_preserved"
    elif not bound:
        state, reason = "gap", "no_valid_evidence_atom"
    elif not explicit:
        state, reason = "needs_legal_analysis", "inference_without_explicit_factual_support"
    elif any(not all(str(row.get(key, "")).strip() for key in ("subject", "predicate", "value"))
             for row in explicit):
        state, reason = "partial", "incomplete_atomic_binding"
    else:
        state, reason = "claimable", "explicit_atomic_binding"
    return {"requirement_id": requirement_id, "state": state, "reason": reason,
            "atom_ids": [row["atom_id"] for row in bound],
            "gate_digest": _digest({"requirement_id": requirement_id, "state": state,
                                     "reason": reason, "atom_ids": [row["atom_id"] for row in bound]})}

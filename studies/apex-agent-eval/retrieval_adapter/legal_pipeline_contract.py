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
    "decomposition": "zai/glm-5.3-flash",
    "candidate_proposer_repair": "zai/glm-5.3-flash",
    "coverage_critic": "gpt-5.6-sol",
    "pageindex": "deepseek/deepseek-v4-flash",
    "primary_executor": "deepseek/deepseek-v4-flash",
    "sensitivity_executor": "zai/glm-5.3-flash",
    "native_grader": "google/gemini-3.1-pro-preview",
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

"""Domain-neutral contracts for evidence-first governed workflows.

This module deliberately has no legal taxonomy, model identifier, corpus path,
or admission shortcut.  Domain profiles and model routes are caller inputs.
"""
from __future__ import annotations

from collections import defaultdict
import hashlib
import json
import re
from typing import Any

WORKFLOW_SCHEMA = "proofpress/governed-workflow-contract/v1"
ATOM_SCHEMA = "proofpress/evidence-atom/v2"
GATE_SCHEMA = "proofpress/claimability-decision/v2"
CRITIC_SCHEMA = "proofpress/layered-critic-verdict/v1"
PROFILE_SCHEMA = "proofpress/domain-profile/v1"

CLAIMABILITY_STATES = {
    "claimable", "partial", "gap", "conflict", "needs_domain_analysis",
}
CRITIC_FIELDS = (
    "subject_supported", "predicate_supported", "value_supported",
    "temporal_scope_supported", "qualification_preserved",
    "claim_type_correct", "citation_entails_entire_claim",
)
CLAIM_TYPES = {
    "observed_fact", "risk_signal", "domain_conclusion", "allocation",
}
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_MONEY_OR_DATE = re.compile(
    r"(?:[$€£]\s?\d|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|"
    r"\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
    r"jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|"
    r"dec(?:ember)?)\s+\d{1,2}(?:,\s*\d{4})?\b)", re.IGNORECASE)


def digest(value: Any) -> str:
    body = json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(body).hexdigest()


def validate_profile(profile: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(profile, dict) or profile.get("schema_version") != PROFILE_SCHEMA:
        raise ValueError("domain profile schema is required")
    required = ("profile_id", "version", "requirement_categories", "claim_types")
    if any(not profile.get(key) for key in required):
        raise ValueError("domain profile required fields are missing")
    if not isinstance(profile["requirement_categories"], list):
        raise ValueError("requirement_categories must be a list")
    if not isinstance(profile["claim_types"], list):
        raise ValueError("claim_types must be a list")
    normalized = dict(profile)
    supplied = normalized.pop("profile_digest", None)
    calculated = digest(normalized)
    if supplied is not None and supplied != calculated:
        raise ValueError("domain profile digest mismatch")
    normalized["profile_digest"] = calculated
    return normalized


def _receipt_valid(receipt: dict[str, Any]) -> bool:
    if not isinstance(receipt, dict):
        return False
    locator = receipt.get("locator")
    return (
        isinstance(receipt.get("evidence_id"), str)
        and bool(receipt["evidence_id"].strip())
        and isinstance(receipt.get("quote"), str)
        and bool(receipt["quote"].strip())
        and isinstance(locator, dict)
        and locator.get("kind") in {"page_span", "section_span"}
        and bool(_DIGEST.fullmatch(str(receipt.get("receipt_digest", ""))))
        and bool(_DIGEST.fullmatch(str(receipt.get("source_digest", ""))))
        and bool(receipt.get("custody_valid"))
    )


def validate_atom(atom: dict[str, Any], receipts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(atom, dict) or atom.get("schema_version") != ATOM_SCHEMA:
        raise ValueError("evidence atom v2 schema is required")
    required = ("atom_id", "requirement_id", "evidence_id", "receipt_digest",
                "subject", "predicate", "value", "exact_excerpt", "support_mode")
    if any(not isinstance(atom.get(key), str) or not atom[key].strip()
           for key in required):
        raise ValueError("evidence atom required fields are missing")
    if atom["support_mode"] not in {"explicit", "inferred"}:
        raise ValueError("evidence atom support_mode is invalid")
    receipt = receipts.get(atom["evidence_id"])
    if not _receipt_valid(receipt or {}):
        raise ValueError("evidence receipt or custody is invalid")
    if atom["receipt_digest"] != receipt["receipt_digest"]:
        raise ValueError("evidence atom receipt digest mismatch")
    if atom.get("locator") != receipt["locator"]:
        raise ValueError("evidence atom locator mismatch")
    if atom["exact_excerpt"] not in receipt["quote"]:
        raise ValueError("evidence atom excerpt is not receipt-bound")
    if atom.get("authority") is not None or atom.get("admission") is not None:
        raise ValueError("evidence atoms cannot carry authority or admission")
    normalized = dict(atom)
    supplied = normalized.pop("atom_digest", None)
    calculated = digest(normalized)
    if supplied is not None and supplied != calculated:
        raise ValueError("evidence atom digest mismatch")
    normalized["atom_digest"] = calculated
    return normalized


def _field_binding(atom: dict[str, Any], field: str) -> bool:
    bindings = atom.get("field_bindings")
    if not isinstance(bindings, dict):
        return False
    span = bindings.get(field)
    excerpt = atom.get("exact_excerpt", "")
    if not isinstance(span, dict):
        return False
    start, end = span.get("start"), span.get("end")
    return (isinstance(start, int) and isinstance(end, int) and
            0 <= start < end <= len(excerpt) and
            excerpt[start:end].strip().casefold() == str(atom.get(field, "")).strip().casefold())


def claimability_decision(requirement: dict[str, Any], atoms: list[dict[str, Any]],
                          receipts: dict[str, dict[str, Any]], *,
                          task_prompt: str = "") -> dict[str, Any]:
    """Fail closed before any proposer call and expose exact failure reasons."""
    requirement_id = str(requirement.get("requirement_id", ""))
    bound = [row for row in atoms if row.get("requirement_id") == requirement_id]
    reasons: list[str] = []
    valid: list[dict[str, Any]] = []
    for atom in bound:
        try:
            checked = validate_atom(atom, receipts)
        except ValueError:
            reasons.append("invalid_atom_or_receipt")
            continue
        valid.append(checked)
    explicit = [row for row in valid if row["support_mode"] == "explicit"]
    conflicts = {str(row.get("conflict_group")) for row in valid if row.get("conflict_group")}
    versions = {str(row.get("document_version")) for row in valid if row.get("document_version")}
    if conflicts or len(versions) > 1:
        state = "conflict"
        reasons.append("conflict_or_version_difference_preserved")
    elif not valid:
        state = "gap"
        reasons.append("no_valid_evidence_atom")
    elif not explicit:
        state = "needs_domain_analysis"
        reasons.append("inference_without_explicit_support")
    else:
        for atom in explicit:
            for field in ("subject", "predicate", "value"):
                if not _field_binding(atom, field):
                    reasons.append(f"unbound_{field}")
            prompt_only = task_prompt and atom["value"].casefold() in task_prompt.casefold()
            evidence_has_value = atom["value"].casefold() in atom["exact_excerpt"].casefold()
            if prompt_only and not evidence_has_value:
                reasons.append("task_prompt_used_as_fact")
            for token in _MONEY_OR_DATE.findall(" ".join(
                    str(atom.get(key) or "") for key in ("value", "effective_date"))):
                if token.casefold() not in atom["exact_excerpt"].casefold():
                    reasons.append("unbound_date_or_amount")
            qualification = atom.get("qualification")
            if qualification and str(qualification).casefold() not in atom["exact_excerpt"].casefold():
                reasons.append("unbound_qualification")
        state = "partial" if reasons else "claimable"
    reasons = sorted(set(reasons))
    result = {
        "schema_version": GATE_SCHEMA,
        "requirement_id": requirement_id,
        "state": state,
        "reasons": reasons,
        "atom_ids": [row["atom_id"] for row in valid],
        "proposer_allowed": state == "claimable",
    }
    result["gate_digest"] = digest(result)
    return result


def validate_compiled_claim(claim: dict[str, Any], atoms: dict[str, dict[str, Any]],
                            gate: dict[str, Any]) -> dict[str, Any]:
    if gate.get("state") != "claimable" or not gate.get("proposer_allowed"):
        raise ValueError("proposer is forbidden for a non-claimable requirement")
    if claim.get("status") != "unresolved":
        raise ValueError("compiled claims must remain unresolved")
    if claim.get("claim_type") not in CLAIM_TYPES:
        raise ValueError("compiled claim type is invalid")
    atom_ids = claim.get("atom_ids")
    if not isinstance(atom_ids, list) or not atom_ids or any(row not in atoms for row in atom_ids):
        raise ValueError("compiled claim must bind valid atoms")
    if set(atom_ids) - set(gate.get("atom_ids", [])):
        raise ValueError("compiled claim uses atoms outside its claimability gate")
    if claim.get("requirement_id") != gate.get("requirement_id"):
        raise ValueError("compiled claim requirement does not match gate")
    if claim.get("authority") is not None or claim.get("admission") is not None:
        raise ValueError("candidate claims cannot carry authority or admission")
    return claim


def validate_layered_verdict(claim: dict[str, Any], verdict: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(verdict, dict) or verdict.get("schema_version") != CRITIC_SCHEMA:
        raise ValueError("layered critic verdict schema is required")
    if verdict.get("claim_id") != claim.get("id"):
        raise ValueError("critic claim binding mismatch")
    missing = [field for field in CRITIC_FIELDS if not isinstance(verdict.get(field), bool)]
    if missing:
        raise ValueError("critic must return every field verdict")
    expected = "supported" if all(verdict[field] for field in CRITIC_FIELDS) else "unsupported"
    if verdict.get("verdict") != expected:
        raise ValueError("critic aggregate verdict contradicts field verdicts")
    if expected != "supported" and not verdict.get("failure_reasons"):
        raise ValueError("unsupported verdict requires failure reasons")
    return verdict


def apply_layered_verdicts(requirements: list[dict[str, Any]], claims: list[dict[str, Any]],
                           verdicts: list[dict[str, Any]]) -> dict[str, Any]:
    by_claim = {row["id"]: row for row in claims}
    if len(verdicts) != len(by_claim):
        raise ValueError("critic verdict coverage is incomplete")
    checked: dict[str, dict[str, Any]] = {}
    for row in verdicts:
        claim_id = row.get("claim_id")
        if claim_id in checked or claim_id not in by_claim:
            raise ValueError("critic returned duplicate or unknown claim")
        checked[claim_id] = validate_layered_verdict(by_claim[claim_id], row)
    supported = [by_claim[cid] for cid, row in checked.items() if row["verdict"] == "supported"]
    failed_by_requirement: dict[str, list[str]] = defaultdict(list)
    for cid, row in checked.items():
        if row["verdict"] != "supported":
            failed_by_requirement[str(by_claim[cid]["requirement_id"])].extend(row["failure_reasons"])
    statuses = []
    supported_requirements = {row["requirement_id"] for row in supported}
    for requirement in requirements:
        requirement_id = requirement["requirement_id"]
        if requirement_id in supported_requirements:
            status, reasons = "covered", []
        elif requirement_id in failed_by_requirement:
            status, reasons = "partial", sorted(set(failed_by_requirement[requirement_id]))
        else:
            status, reasons = "gap", ["no_supported_candidate"]
        statuses.append({"requirement_id": requirement_id, "status": status,
                         "reasons": reasons})
    return {"supported_claims": supported, "requirement_statuses": statuses,
            "verdict_digest": digest(checked)}


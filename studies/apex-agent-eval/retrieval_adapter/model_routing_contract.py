"""Deterministic contracts for legal-workflow model routing qualification."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from typing import Any

SCHEMA = "proofpress/model-routing-evaluation/v1"
CLAIM_SCHEMA = "proofpress/deterministic-atom-claim/v1"
VERDICTS = {"supported", "partially_supported", "unsupported", "conflicted", "misclassified"}
CLAIM_TYPES = {"observed_fact", "risk_signal", "legal_conclusion", "contract_allocation"}
MATERIAL_LIFECYCLES = {
    "parties_capacity_authority", "economics_calculations",
    "conditions_deliveries", "termination_remedies",
    "indemnity_liability_limits", "tax_regulatory",
    "document_version_conflicts",
}


def digest(value: Any) -> str:
    body = json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(body).hexdigest()


def atom_to_observed_claim(atom: dict[str, Any], requirement: dict[str, Any],
                           ordinal: int) -> dict[str, Any]:
    """Construct the narrowest observed-fact candidate without model prose."""
    if atom.get("support_mode") != "explicit":
        raise ValueError("only explicit atoms can become observed-fact claims")
    required = ("atom_id", "requirement_id", "evidence_id", "subject",
                "predicate", "value", "receipt_digest", "exact_excerpt")
    if any(not isinstance(atom.get(key), str) or not atom[key].strip()
           for key in required):
        raise ValueError("atom is missing deterministic claim fields")
    statement = " ".join((atom["subject"].strip(), atom["predicate"].strip(),
                          atom["value"].strip()))
    # Qualifications remain a separate bound field. Appending model-written
    # qualifications to the factual sentence was a major source of overreach.
    claim = {
        "schema_version": CLAIM_SCHEMA,
        "id": f"atom_claim_{ordinal:03d}_{atom['atom_id'][-8:]}",
        "requirement_id": atom["requirement_id"],
        "claim_type": "observed_fact",
        "statement": statement,
        "evidence_ids": [atom["evidence_id"]],
        "atom_ids": [atom["atom_id"]],
        "receipt_digests": [atom["receipt_digest"]],
        "qualification": atom.get("qualification"),
        "effective_date": atom.get("effective_date"),
        "document_version": atom.get("document_version"),
        "scope": requirement.get("requirement"),
        "category": requirement.get("lifecycle_category"),
        "status": "unresolved",
    }
    claim["construction_digest"] = digest(claim)
    return claim


def construct_observed_claims(atoms: list[dict[str, Any]],
                              requirements: list[dict[str, Any]],
                              max_per_requirement: int = 4) -> list[dict[str, Any]]:
    by_requirement = {row["requirement_id"]: row for row in requirements}
    seen: set[tuple[str, str, str, str, str]] = set()
    counts: Counter[str] = Counter()
    claims: list[dict[str, Any]] = []
    for atom in sorted(atoms, key=lambda row: (str(row.get("requirement_id")),
                                               str(row.get("atom_id")))):
        requirement_id = atom.get("requirement_id")
        if atom.get("support_mode") != "explicit" or requirement_id not in by_requirement:
            continue
        key = (str(requirement_id), str(atom.get("evidence_id")),
               str(atom.get("subject")), str(atom.get("predicate")),
               str(atom.get("value")))
        if key in seen or counts[str(requirement_id)] >= max_per_requirement:
            continue
        seen.add(key); counts[str(requirement_id)] += 1
        claims.append(atom_to_observed_claim(atom, by_requirement[str(requirement_id)],
                                             len(claims) + 1))
    return claims


def validate_verdicts(claims: list[dict[str, Any]], value: dict[str, Any]) -> dict[str, dict[str, Any]]:
    claim_ids = {row["id"] for row in claims}
    rows = value.get("verdicts") if isinstance(value, dict) else None
    if not isinstance(rows, list) or len(rows) != len(claims):
        raise ValueError("critic must return exactly one verdict per claim")
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        claim_id = row.get("claim_id")
        if claim_id not in claim_ids or claim_id in result or row.get("verdict") not in VERDICTS:
            raise ValueError("critic returned an invalid or duplicate verdict")
        result[claim_id] = row
    if set(result) != claim_ids:
        raise ValueError("critic verdict coverage is incomplete")
    return result


def apply_type_assignments(claims: list[dict[str, Any]], value: dict[str, Any]) -> list[dict[str, Any]]:
    """Apply type-only model output without allowing prose or binding changes."""
    rows = value.get("assignments") if isinstance(value, dict) else None
    if not isinstance(rows, list) or len(rows) != len(claims):
        raise ValueError("classifier must return exactly one assignment per claim")
    assignments: dict[str, str] = {}
    known = {row["id"] for row in claims}
    for row in rows:
        claim_id, claim_type = row.get("claim_id"), row.get("claim_type")
        if claim_id not in known or claim_id in assignments or claim_type not in CLAIM_TYPES:
            raise ValueError("classifier returned an invalid or duplicate assignment")
        assignments[claim_id] = claim_type
    if set(assignments) != known:
        raise ValueError("classifier assignment coverage is incomplete")
    result = []
    for claim in claims:
        updated = dict(claim); updated["claim_type"] = assignments[claim["id"]]
        updated["type_assignment_digest"] = digest({"claim_id": claim["id"],
                                                     "claim_type": updated["claim_type"]})
        result.append(updated)
    return result


def route_verdicts(claims: list[dict[str, Any]], primary: dict[str, dict[str, Any]],
                   premium: dict[str, dict[str, Any]], *, mode: str) -> tuple[dict[str, dict[str, Any]], set[str]]:
    """Apply a frozen escalation policy and return final verdicts and escalations."""
    if mode not in {"primary_only", "non_supported_or_material_to_premium"}:
        raise ValueError("unknown routing mode")
    final: dict[str, dict[str, Any]] = {}
    escalated: set[str] = set()
    for claim in claims:
        claim_id = claim["id"]
        first = primary[claim_id]
        material = claim.get("category") in MATERIAL_LIFECYCLES
        escalate = mode != "primary_only" and (
            first.get("verdict") != "supported" or material)
        if escalate:
            escalated.add(claim_id)
            final[claim_id] = premium[claim_id]
        else:
            final[claim_id] = first
    return final, escalated


def classification_metrics(candidate: dict[str, dict[str, Any]],
                           reference: dict[str, dict[str, Any]]) -> dict[str, Any]:
    ids = sorted(set(candidate) & set(reference))
    exact = sum(candidate[row]["verdict"] == reference[row]["verdict"] for row in ids)
    candidate_supported = {row for row in ids if candidate[row]["verdict"] == "supported"}
    reference_supported = {row for row in ids if reference[row]["verdict"] == "supported"}
    true_supported = len(candidate_supported & reference_supported)
    precision = true_supported / len(candidate_supported) if candidate_supported else 1.0
    recall = true_supported / len(reference_supported) if reference_supported else 1.0
    return {
        "claim_count": len(ids),
        "exact_verdict_agreement": exact / len(ids) if ids else None,
        "supported_precision": precision,
        "supported_recall": recall,
        "supported_f1": (2 * precision * recall / (precision + recall)
                         if precision + recall else 0.0),
        "candidate_supported": len(candidate_supported),
        "reference_supported": len(reference_supported),
    }

"""Deterministic contracts for the Finance evidence-first E2E v2 study.

This module contains no private corpus, prompts, model outputs, or admission
decisions.  It validates the boundary between source receipts, Finance atoms,
deterministically constructed facts, model classifications, completeness, and
the pre-executor release gate.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
from typing import Any


ATOM_SCHEMA = "proofpress/finance-evidence-atom/v2"
FACT_SCHEMA = "proofpress/finance-observed-fact/v2"
GATE_SCHEMA = "proofpress/finance-execution-gate/v2"
RECORD_TYPES = {
    "observed_fact",
    "derived_calculation",
    "calculation_choice",
    "assumption",
    "risk_signal",
    "banking_analysis",
}
CRITIC_VERDICTS = {
    "supported",
    "partially_supported",
    "unsupported",
    "conflicted",
    "misclassified",
}
MATERIAL_GAP_KINDS = {
    "missing_input",
    "unresolved_methodology",
    "ambiguous_basis",
    "circular_dependency",
    "source_version_conflict",
}


def digest(value: Any) -> str:
    body = json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(body).hexdigest()


def validate_finance_atom(atom: dict[str, Any],
                          receipts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Validate a source-bound atom without granting authority or admission."""
    if not isinstance(atom, dict) or atom.get("schema_version") != ATOM_SCHEMA:
        raise ValueError("finance evidence atom schema is required")
    required = (
        "atom_id", "requirement_id", "evidence_id", "receipt_digest",
        "subject", "predicate", "value", "support_mode", "locator",
    )
    if any(not isinstance(atom.get(key), str) or not atom[key].strip()
           for key in required):
        raise ValueError("finance atom required fields are missing")
    if atom["support_mode"] not in {"explicit", "inferred"}:
        raise ValueError("finance atom support_mode is invalid")
    receipt = receipts.get(atom["evidence_id"])
    if not receipt or receipt.get("receipt_digest") != atom["receipt_digest"]:
        raise ValueError("finance atom receipt binding is invalid")
    if atom["locator"] != receipt.get("locator"):
        raise ValueError("finance atom locator does not match its receipt")
    if atom.get("authority") is not None or atom.get("admission") is not None:
        raise ValueError("finance atoms cannot carry authority or admission")

    source_value = receipt.get("source_value")
    excerpt = receipt.get("quote")
    exact = atom.get("exact_source_value")
    if source_value is not None:
        if exact != source_value:
            raise ValueError("finance atom value must exactly match its receipt")
    elif not (isinstance(excerpt, str) and isinstance(exact, str)
              and exact.strip() and exact in excerpt):
        raise ValueError("finance atom excerpt must be an exact receipt substring")

    for field in ("unit", "currency", "period", "as_of_date", "source_version"):
        receipt_value = receipt.get(field)
        if receipt_value is not None and atom.get(field) != receipt_value:
            raise ValueError(f"finance atom {field} does not match its receipt")
    return atom


def atom_to_observed_fact(atom: dict[str, Any], ordinal: int) -> dict[str, Any]:
    """Construct a narrow fact without model-authored factual prose."""
    if atom.get("support_mode") != "explicit":
        raise ValueError("only explicit atoms can become observed facts")
    statement = " ".join((atom["subject"].strip(), atom["predicate"].strip(),
                          str(atom["value"]).strip()))
    fact = {
        "schema_version": FACT_SCHEMA,
        "id": f"finance_fact_{ordinal:04d}_{atom['atom_id'][-8:]}",
        "requirement_id": atom["requirement_id"],
        "record_type": "observed_fact",
        "statement": statement,
        "atom_ids": [atom["atom_id"]],
        "evidence_ids": [atom["evidence_id"]],
        "receipt_digests": [atom["receipt_digest"]],
        "unit": atom.get("unit"),
        "currency": atom.get("currency"),
        "period": atom.get("period"),
        "as_of_date": atom.get("as_of_date"),
        "source_version": atom.get("source_version"),
        "qualification": atom.get("qualification"),
        "status": "unresolved",
    }
    fact["construction_digest"] = digest(fact)
    return fact


def construct_observed_facts(atoms: list[dict[str, Any]],
                             max_per_requirement: int = 12) -> list[dict[str, Any]]:
    seen: set[tuple[Any, ...]] = set()
    counts: Counter[str] = Counter()
    facts: list[dict[str, Any]] = []
    for atom in sorted(atoms, key=lambda row: (str(row.get("requirement_id")),
                                               str(row.get("atom_id")))):
        requirement_id = str(atom.get("requirement_id", ""))
        if atom.get("support_mode") != "explicit":
            continue
        key = tuple(atom.get(field) for field in (
            "requirement_id", "evidence_id", "subject", "predicate", "value",
            "unit", "currency", "period", "as_of_date", "source_version",
        ))
        if key in seen or counts[requirement_id] >= max_per_requirement:
            continue
        seen.add(key)
        counts[requirement_id] += 1
        facts.append(atom_to_observed_fact(atom, len(facts) + 1))
    return facts


def apply_type_assignments(records: list[dict[str, Any]],
                           value: dict[str, Any]) -> list[dict[str, Any]]:
    """Apply type-only output while preserving prose, bindings, and metadata."""
    rows = value.get("assignments") if isinstance(value, dict) else None
    if not isinstance(rows, list) or len(rows) != len(records):
        raise ValueError("classifier must return one assignment per record")
    known = {row["id"] for row in records}
    assignments: dict[str, str] = {}
    for row in rows:
        record_id, record_type = row.get("record_id"), row.get("record_type")
        if (record_id not in known or record_id in assignments
                or record_type not in RECORD_TYPES):
            raise ValueError("classifier returned an invalid assignment")
        if set(row) != {"record_id", "record_type"}:
            raise ValueError("classifier may only assign a record type")
        assignments[record_id] = record_type
    result = []
    for record in records:
        updated = dict(record)
        updated["record_type"] = assignments[record["id"]]
        updated["type_assignment_digest"] = digest({
            "record_id": record["id"], "record_type": updated["record_type"],
        })
        result.append(updated)
    return result


def validate_critic_verdicts(records: list[dict[str, Any]],
                             value: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = value.get("verdicts") if isinstance(value, dict) else None
    if not isinstance(rows, list) or len(rows) != len(records):
        raise ValueError("critic must return one verdict per record")
    known = {row["id"] for row in records}
    verdicts: dict[str, dict[str, Any]] = {}
    for row in rows:
        record_id = row.get("record_id")
        if (record_id not in known or record_id in verdicts
                or row.get("verdict") not in CRITIC_VERDICTS):
            raise ValueError("critic returned an invalid verdict")
        verdicts[record_id] = row
    return verdicts


def detect_material_conflicts(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Detect incompatible explicit facts at the same Finance scope."""
    buckets: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        if record.get("record_type") != "observed_fact":
            continue
        key = tuple(record.get(field) for field in (
            "requirement_id", "statement_subject", "statement_predicate",
            "period", "as_of_date",
        ))
        # Constructed facts retain the canonical statement. Private adapters may
        # additionally preserve subject/predicate for stronger bucketing.
        if key[1] is None or key[2] is None:
            statement = str(record.get("statement", ""))
            key = (record.get("requirement_id"), statement.rsplit(" ", 1)[0],
                   "value", record.get("period"), record.get("as_of_date"))
        buckets[key].append(record)

    conflicts = []
    for key, rows in buckets.items():
        signatures = {
            (row.get("statement"), row.get("unit"), row.get("currency"),
             row.get("source_version")) for row in rows
        }
        if len(signatures) > 1:
            record_ids = sorted(row["id"] for row in rows)
            conflicts.append({
                "scope": key,
                "record_ids": record_ids,
                "reason": "incompatible_same_scope_finance_facts",
                "material": True,
                "conflict_digest": digest(record_ids),
            })
    return conflicts


def requirement_completeness(requirements: list[dict[str, Any]],
                             records: list[dict[str, Any]],
                             gaps: list[dict[str, Any]]) -> dict[str, Any]:
    known = {row["requirement_id"] for row in requirements}
    covered = {row.get("requirement_id") for row in records
               if row.get("status") == "supported"}
    gap_by_requirement: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for gap in gaps:
        requirement_id = gap.get("requirement_id")
        if requirement_id not in known:
            raise ValueError("gap references an unknown requirement")
        if gap.get("kind") not in MATERIAL_GAP_KINDS | {"immaterial_residual"}:
            raise ValueError("gap kind is invalid")
        gap_by_requirement[requirement_id].append(gap)
    rows = []
    for requirement in requirements:
        requirement_id = requirement["requirement_id"]
        bound_gaps = gap_by_requirement.get(requirement_id, [])
        material = [gap for gap in bound_gaps if gap.get("material") is True]
        if material:
            state = "material_gap"
        elif requirement_id in covered:
            state = "covered"
        else:
            state = "unexplained_gap"
        rows.append({"requirement_id": requirement_id, "state": state,
                     "gap_ids": [gap.get("gap_id") for gap in bound_gaps]})
    return {"requirements": rows,
            "complete": all(row["state"] == "covered" for row in rows),
            "digest": digest(rows)}


def executor_qualification(cells: list[dict[str, Any]],
                           *, required: int = 6, minimum_completed: int = 5,
                           maximum_transport_failures: int = 1) -> dict[str, Any]:
    if len(cells) != required:
        raise ValueError(f"executor qualification requires exactly {required} cells")
    if any(not cell.get("terminal_telemetry_complete") for cell in cells):
        return {"decision": "block", "reason": "incomplete_terminal_telemetry"}
    completed = sum(cell.get("workbook_finalized") is True
                    and cell.get("required_outputs_valid") is True for cell in cells)
    transport_failures = sum(cell.get("failure_kind") == "transport" for cell in cells)
    unauthorized = sum(cell.get("unauthorized_source_access") is True for cell in cells)
    allow = (completed >= minimum_completed
             and transport_failures <= maximum_transport_failures
             and unauthorized == 0)
    return {
        "decision": "allow" if allow else "block",
        "completed": completed,
        "scheduled": required,
        "transport_failures": transport_failures,
        "unauthorized_source_access": unauthorized,
        "criteria": {"minimum_completed": minimum_completed,
                     "maximum_transport_failures": maximum_transport_failures},
    }


def execution_gate(*, records: list[dict[str, Any]],
                   critic_verdicts: dict[str, dict[str, Any]],
                   completeness: dict[str, Any], conflicts: list[dict[str, Any]],
                   source_bindings_complete: bool, telemetry_complete: bool,
                   requested_output_leakage: bool) -> dict[str, Any]:
    reasons: list[str] = []
    if not source_bindings_complete:
        reasons.append("incomplete_source_binding")
    if not telemetry_complete:
        reasons.append("incomplete_terminal_telemetry")
    if requested_output_leakage:
        reasons.append("requested_output_leakage")
    if conflicts:
        reasons.append("unresolved_material_conflict")
    if not completeness.get("complete"):
        reasons.append("requirement_or_material_gap_incomplete")
    allowed_ids = {row["id"] for row in records}
    if set(critic_verdicts) != allowed_ids:
        reasons.append("incomplete_critic_coverage")
    elif any(row.get("verdict") != "supported"
             for row in critic_verdicts.values()):
        reasons.append("non_supported_record_in_allowed_set")
    result = {
        "schema_version": GATE_SCHEMA,
        "decision": "block" if reasons else "allow",
        "reasons": reasons,
        "record_count": len(records),
        "conflict_count": len(conflicts),
    }
    result["gate_digest"] = digest(result)
    return result


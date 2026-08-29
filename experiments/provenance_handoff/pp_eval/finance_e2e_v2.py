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
import math
import re
import subprocess
from pathlib import Path
import os
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
_CELL = re.compile(r"^([A-Z]+)([1-9][0-9]*)$")
_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9_./%-]{1,}|[0-9]+(?:\.[0-9]+)?")


def _cell_position(address: str) -> tuple[int, int] | None:
    match = _CELL.fullmatch(address.upper())
    if not match:
        return None
    column = 0
    for character in match.group(1):
        column = column * 26 + ord(character) - 64
    return column, int(match.group(2))


def workbook_index_to_receipts(*, artifact: str, source_sha256: str,
                               sheets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert deterministic XLSX cell extraction into source receipts.

    Cached values and formulas are retained separately.  The function never
    recalculates a workbook and therefore cannot silently promote a stale cache
    into a derived fact.
    """
    if not artifact or not source_sha256.startswith("sha256:"):
        raise ValueError("workbook artifact and sha256 digest are required")
    receipts = []
    seen: set[str] = set()
    for sheet in sheets:
        sheet_name = sheet.get("sheet")
        if not isinstance(sheet_name, str) or not sheet_name:
            raise ValueError("workbook sheet name is required")
        cells = sheet.get("cells", [])
        positioned = [(cell, _cell_position(str(cell.get("cell", "")))) for cell in cells]
        for cell, position in positioned:
            address = cell.get("cell")
            if not isinstance(address, str) or not address:
                raise ValueError("workbook cell address is required")
            locator = f"{artifact}#{sheet_name}!{address}"
            if locator in seen:
                raise ValueError("duplicate workbook locator")
            seen.add(locator)
            receipt = {
                "schema_version": "proofpress/finance-source-receipt/v2",
                "evidence_id": "finance_ev_" + hashlib.sha256(
                    locator.encode()).hexdigest()[:16],
                "artifact": artifact,
                "source_sha256": source_sha256,
                "locator": locator,
                "source_value": cell.get("value"),
                "formula": cell.get("formula"),
                "value_semantics": ("cached_formula_result"
                                    if cell.get("formula") else "literal_cell_value"),
            }
            if position:
                column, row = position
                receipt["local_context"] = [
                    {"cell": neighbor["cell"], "value": neighbor.get("value"),
                     "formula": neighbor.get("formula")}
                    for neighbor, neighbor_position in positioned
                    if neighbor_position
                    and abs(neighbor_position[0] - column) <= 2
                    and abs(neighbor_position[1] - row) <= 1
                ][:15]
            receipt["receipt_digest"] = digest(receipt)
            receipts.append(receipt)
    return receipts


def retrieve_receipts(requirements: list[dict[str, Any]],
                      receipts: list[dict[str, Any]],
                      *, limit_per_requirement: int = 40) -> dict[str, list[dict[str, Any]]]:
    """Deterministic lexical retrieval over receipt-bound cell neighborhoods."""
    if limit_per_requirement < 1:
        raise ValueError("receipt retrieval limit must be positive")
    documents: list[tuple[dict[str, Any], list[str]]] = []
    frequencies: Counter[str] = Counter()
    for receipt in receipts:
        searchable = json.dumps({
            "artifact": receipt.get("artifact"), "locator": receipt.get("locator"),
            "value": receipt.get("source_value"), "formula": receipt.get("formula"),
            "context": receipt.get("local_context", []),
        }, ensure_ascii=False)
        tokens = [value.casefold() for value in _TOKEN.findall(searchable)]
        unique = set(tokens)
        frequencies.update(unique)
        documents.append((receipt, tokens))
    total = max(1, len(documents))
    result: dict[str, list[dict[str, Any]]] = {}
    for requirement in requirements:
        requirement_id = str(requirement["requirement_id"])
        query = [value.casefold() for value in _TOKEN.findall(
            str(requirement.get("requirement", "")))]
        scored = []
        for receipt, tokens in documents:
            counts = Counter(tokens)
            score = 0.0
            for token in set(query):
                if counts[token]:
                    inverse = math.log(1 + total / (1 + frequencies[token]))
                    score += inverse * (1 + math.log(counts[token]))
            if score > 0:
                scored.append((score, str(receipt["locator"]), receipt))
        scored.sort(key=lambda row: (-row[0], row[1]))
        result[requirement_id] = [row[2] for row in scored[:limit_per_requirement]]
    return result


def pdf_pages_to_receipts(*, artifact: str, source_sha256: str,
                          pages: list[str], max_block_chars: int = 1600) -> list[dict[str, Any]]:
    """Create page-addressable exact-excerpt receipts from extracted PDF text."""
    if not artifact.lower().endswith(".pdf") or not source_sha256.startswith("sha256:"):
        raise ValueError("PDF artifact and sha256 digest are required")
    receipts = []
    for page_number, page in enumerate(pages, start=1):
        paragraphs = [re.sub(r"\s+", " ", value).strip()
                      for value in re.split(r"\n\s*\n", page) if value.strip()]
        blocks: list[str] = []
        for paragraph in paragraphs:
            if len(paragraph) <= max_block_chars:
                blocks.append(paragraph)
            else:
                blocks.extend(paragraph[index:index + max_block_chars]
                              for index in range(0, len(paragraph), max_block_chars))
        for block_number, quote in enumerate(blocks, start=1):
            locator = f"{artifact}#page={page_number}&block={block_number}"
            receipt = {
                "schema_version": "proofpress/finance-source-receipt/v2",
                "evidence_id": "finance_ev_" + hashlib.sha256(locator.encode()).hexdigest()[:16],
                "artifact": artifact, "source_sha256": source_sha256,
                "locator": locator, "quote": quote,
                "value_semantics": "exact_pdf_text_excerpt",
            }
            receipt["receipt_digest"] = digest(receipt)
            receipts.append(receipt)
    return receipts


def extract_pdf_receipts(*, path: str, artifact: str,
                         source_sha256: str) -> list[dict[str, Any]]:
    """Read a PDF with Poppler without altering or re-exporting the source."""
    result = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", path, "-"],
        capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError("Poppler PDF extraction failed")
    pages = result.stdout.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pdf_pages_to_receipts(
        artifact=artifact, source_sha256=source_sha256, pages=pages)


def fresh_task_audit(*, task_rows: list[dict[str, Any]], world_id: str,
                     manifest_roots: list[Path], executor_model: str) -> dict[str, Any]:
    """Audit task freshness without retaining rubric, gold, or prior answers."""
    consumed: dict[str, list[str]] = defaultdict(list)
    for search_root in manifest_roots:
        if not search_root.exists():
            continue
        for root, directories, files in os.walk(search_root):
            directories[:] = [name for name in directories
                               if name not in {".git", "node_modules", ".venv", "venv", "__pycache__"}]
            if "manifest.json" not in files:
                continue
            path = Path(root) / "manifest.json"
            try:
                value = json.loads(path.read_text())
            except (OSError, json.JSONDecodeError):
                continue
            if (value.get("world_id") == world_id
                    and executor_model in {value.get("agent_model"), value.get("executor_model")}
                    and isinstance(value.get("task_id"), str)):
                consumed[value["task_id"]].append(digest({
                    "manifest": str(path), "status": value.get("status"),
                    "stage": value.get("stage"),
                }))
    candidates = []
    excluded = []
    for task in task_rows:
        if task.get("world_id") != world_id or task.get("domain") != "Investment Banking":
            continue
        public = {key: task.get(key) for key in
                  ("task_id", "task_name", "world_id", "domain", "expected_output", "prompt")}
        row = {
            "task_id": task.get("task_id"), "task_name": task.get("task_name"),
            "expected_output": task.get("expected_output"),
            "public_contract_digest": digest(public),
        }
        if task.get("task_id") in consumed:
            row["reason"] = "executor_previously_consumed_task"
            row["manifest_receipt_digests"] = sorted(consumed[task["task_id"]])
            excluded.append(row)
        else:
            candidates.append(row)
    result = {
        "schema_version": "proofpress/finance-formal-task-freshness/v1",
        "world_id": world_id, "executor_model": executor_model,
        "candidate_count": len(candidates), "excluded_count": len(excluded),
        "candidates": sorted(candidates, key=lambda row: row["task_id"]),
        "excluded": sorted(excluded, key=lambda row: row["task_id"]),
        "hidden_material_retained": False,
        "formal_tasks_frozen": False,
        "formal_denominator": 0,
    }
    result["audit_digest"] = digest(result)
    return result


def validate_requirements(requirements: list[dict[str, Any]]) -> dict[str, Any]:
    """Freeze task decomposition without hidden evaluation material."""
    if not isinstance(requirements, list) or not 1 <= len(requirements) <= 40:
        raise ValueError("Finance decomposition must contain 1 to 40 requirements")
    allowed = {"deliverable", "calculation", "input", "output", "validation"}
    seen = set()
    for row in requirements:
        requirement_id = row.get("requirement_id")
        if (not isinstance(requirement_id, str) or not requirement_id
                or requirement_id in seen):
            raise ValueError("requirements need unique non-empty IDs")
        seen.add(requirement_id)
        if row.get("kind") not in allowed or not str(row.get("requirement", "")).strip():
            raise ValueError("requirement kind and text are required")
        if any(key in row for key in ("rubric", "gold", "reference_answer")):
            raise ValueError("hidden evaluation material is forbidden")
    frozen = {"requirements": requirements, "count": len(requirements)}
    frozen["requirement_digest"] = digest(frozen)
    return frozen


def validate_derived_calculation(record: dict[str, Any],
                                 known_record_ids: set[str]) -> dict[str, Any]:
    """Require auditable dependencies for non-observed numeric records."""
    if record.get("record_type") != "derived_calculation":
        raise ValueError("record is not a derived calculation")
    formula = record.get("formula")
    dependencies = record.get("dependency_ids")
    if not isinstance(formula, str) or not formula.strip():
        raise ValueError("derived calculation formula is required")
    if not isinstance(dependencies, list) or not dependencies:
        raise ValueError("derived calculation dependencies are required")
    if any(item not in known_record_ids for item in dependencies):
        raise ValueError("derived calculation references an unknown dependency")
    if record.get("unit") is None and record.get("currency") is None:
        raise ValueError("derived calculation unit or currency is required")
    return record


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
                             gaps: list[dict[str, Any]], *,
                             covered_requirement_ids: set[str] | None = None) -> dict[str, Any]:
    known = {row["requirement_id"] for row in requirements}
    covered = (set(covered_requirement_ids) if covered_requirement_ids is not None else
               {row.get("requirement_id") for row in records
                if row.get("status") == "supported"})
    if not covered <= known:
        raise ValueError("covered requirement references an unknown requirement")
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


def legacy_working_set_preflight(value: dict[str, Any]) -> dict[str, Any]:
    """Diagnose v1 residual gaps under the stricter v2 release boundary.

    Legacy packages did not bind every gap to a requirement or declare frozen
    materiality.  V2 cannot infer that missing governance state is harmless,
    so each such gap is preserved as an unresolved blocker.  The returned
    value contains no descriptions or source content.
    """
    gaps = value.get("residual_gaps")
    if not isinstance(gaps, list):
        gaps = []
    blockers = []
    immaterial = 0
    for ordinal, gap in enumerate(gaps, start=1):
        if not isinstance(gap, dict):
            blockers.append({"ordinal": ordinal, "reason": "invalid_gap_shape"})
            continue
        kind = gap.get("kind")
        material = gap.get("material")
        requirement_id = gap.get("requirement_id")
        if kind == "immaterial_residual" and material is False and requirement_id:
            immaterial += 1
            continue
        reasons = []
        if kind not in MATERIAL_GAP_KINDS | {"immaterial_residual"}:
            reasons.append("unfrozen_gap_kind")
        if not isinstance(material, bool):
            reasons.append("undeclared_materiality")
        elif material:
            reasons.append("material_gap")
        if not requirement_id:
            reasons.append("unbound_requirement")
        if kind == "immaterial_residual" and material is not False:
            reasons.append("invalid_immaterial_declaration")
        if reasons:
            blockers.append({"ordinal": ordinal, "reasons": sorted(set(reasons)),
                             "gap_digest": digest(gap)})
    result = {
        "task_id": value.get("task_id"),
        "gap_count": len(gaps),
        "explicit_immaterial_gap_count": immaterial,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "decision": "block" if blockers else "allow",
    }
    result["diagnostic_digest"] = digest(result)
    return result


def executor_qualification(cells: list[dict[str, Any]],
                           *, required: int = 6, minimum_completed: int = 5,
                           maximum_transport_failures: int = 1) -> dict[str, Any]:
    if len(cells) != required:
        raise ValueError(f"executor qualification requires exactly {required} cells")
    infrastructure_invalid = sum(cell.get("infrastructure_invalid") is True
                                 for cell in cells)
    if infrastructure_invalid:
        return {"decision": "block", "reason": "infrastructure_invalid_cells",
                "infrastructure_invalid_cells": infrastructure_invalid,
                "scheduled": required}
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
        "infrastructure_invalid_cells": infrastructure_invalid,
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

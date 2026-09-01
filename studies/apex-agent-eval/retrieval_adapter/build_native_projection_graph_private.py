#!/usr/bin/env python3
"""Compile one private exact-knowledge artifact into a frozen native projection graph.

This is deliberately a representation compiler, not an answer generator.  It
accepts only the source-bound candidates emitted by exact-knowledge
construction and preserves their ``not_governed`` state.  The output is
private because its claims, locators, and table cells can contain matter data;
the accompanying receipt contains digests and counts only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
ADAPTER = Path(__file__).resolve().parent
if str(ADAPTER) not in sys.path:
    sys.path.insert(0, str(ADAPTER))

from exact_knowledge_contract import match_numeric_payload_to_table_cell
from phase_c_ablation_contract import digest, validate_graph


SCHEMA = "proofpress/native-apex-task-projection-graph/v1"


def _write_private(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.parent.chmod(0o700)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    path.chmod(0o600)


def _require_digest(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
        raise ValueError(f"{field} must be a sha256 digest")
    try:
        int(value[7:], 16)
    except ValueError as exc:
        raise ValueError(f"{field} must be a sha256 digest") from exc
    return value


def _safe_page(locator: Any) -> int:
    if not isinstance(locator, dict):
        return 1
    for field in ("page", "page_start"):
        value = locator.get(field)
        if isinstance(value, int) and value >= 1:
            return value
    return 1


def _atom_claim(atom: dict[str, Any], receipt: dict[str, Any], object_kind: str) -> dict[str, Any]:
    atom_id = str(atom.get("atom_id") or "")
    if not atom_id:
        raise ValueError("candidate atom is missing atom_id")
    source_digest = _require_digest(receipt.get("source_digest"), "receipt source_digest")
    statement = " ".join(str(atom.get(field) or "") for field in ("subject", "predicate", "value")).strip()
    if not statement:
        raise ValueError("candidate atom is missing a source-bound statement")
    return {
        "claim_id": "claim_" + hashlib.sha256(atom_id.encode()).hexdigest()[:20],
        "basis_object_id": atom_id,
        "basis_object_kind": object_kind,
        "statement": statement,
        "source_content_digest": source_digest,
        "receipt_digest": _require_digest(atom.get("receipt_digest"), "atom receipt_digest"),
        "locator": atom.get("locator"),
        "support_mode": atom.get("support_mode"),
        "status": "not_governed_candidate",
        "admitted": False,
        "human_approval_required": True,
    }


def build(*, exact_artifact: dict[str, Any], catalog: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Create one source-bound graph for one task without accessing its rubric."""
    task = exact_artifact.get("task")
    receipts = exact_artifact.get("receipts")
    objects = exact_artifact.get("objects")
    if (not isinstance(task, dict) or not isinstance(task.get("task_id"), str)
            or not isinstance(receipts, dict) or not isinstance(objects, dict)):
        raise ValueError("exact artifact must contain a task, receipts, and objects")
    if "rubric" in task or "gold" in task:
        raise ValueError("native projection compiler rejects rubric or gold-bearing task artifacts")
    catalog_digest = _require_digest(catalog.get("catalog_digest"), "catalog_digest")

    claims: list[dict[str, Any]] = []
    seen_claims: set[str] = set()
    atom_rows = [(row, "evidence_atom") for row in objects.get("evidence_atoms", [])]
    atom_rows.extend((row, "numeric_atom") for row in objects.get("numeric_atoms", []))
    for atom, object_kind in atom_rows:
        if not isinstance(atom, dict):
            raise ValueError("candidate atoms must be objects")
        evidence_id = atom.get("evidence_id")
        receipt = receipts.get(evidence_id)
        if not isinstance(receipt, dict):
            raise ValueError("candidate atom is missing its source receipt")
        row = _atom_claim(atom, receipt, object_kind)
        if row["claim_id"] not in seen_claims:
            seen_claims.add(row["claim_id"])
            claims.append(row)
    if not claims:
        raise ValueError("native projection graph requires source-bound ordinary claims")

    numeric_atoms: list[dict[str, Any]] = []
    for atom in objects.get("numeric_atoms", []):
        if not isinstance(atom, dict):
            raise ValueError("numeric atoms must be objects")
        atom_id = str(atom.get("atom_id") or "")
        receipt = receipts.get(atom.get("evidence_id"))
        numeric = atom.get("numeric")
        if not atom_id or not isinstance(receipt, dict) or not isinstance(numeric, dict):
            raise ValueError("numeric atom is missing identity, receipt, or numeric metadata")
        required = ("display", "decimal_value", "kind", "unit", "entity", "period")
        if any(not isinstance(numeric.get(key), str) for key in required):
            raise ValueError("numeric atom metadata is incomplete")
        numeric_atoms.append({
            "atom_id": atom_id,
            "display": numeric["display"],
            "normalized_value": numeric["decimal_value"],
            "kind": numeric["kind"],
            "unit": numeric["unit"],
            "currency": numeric.get("currency"),
            "entity": numeric["entity"],
            "period": numeric["period"],
            "source_content_digest": _require_digest(receipt.get("source_digest"), "numeric atom source_digest"),
            "receipt_digest": _require_digest(atom.get("receipt_digest"), "numeric atom receipt_digest"),
            "locator": atom.get("locator"),
            "status": "not_governed_candidate",
            "admitted": False,
            "human_approval_required": True,
        })
    numeric_atoms.sort(key=lambda row: row["atom_id"])

    cells: list[dict[str, Any]] = []
    atom_cells: dict[str, str] = {}
    recovered_generic_bindings = 0
    for atom in objects.get("numeric_atoms", []):
        if not isinstance(atom, dict):
            continue
        evidence_id = atom.get("evidence_id")
        receipt = receipts.get(evidence_id)
        if not isinstance(receipt, dict):
            raise ValueError("table cell candidate is missing its source receipt")
        binding = atom.get("table_cell_binding")
        if not isinstance(binding, dict):
            binding, match_status = match_numeric_payload_to_table_cell(atom, receipt)
            if match_status == "bound":
                recovered_generic_bindings += 1
        if not isinstance(binding, dict):
            continue
        if not isinstance(binding.get("row_index"), int) or not isinstance(binding.get("column_index"), int):
            continue
        atom_id = str(atom.get("atom_id") or "")
        if not atom_id:
            raise ValueError("table cell candidate is missing atom_id")
        cell_id = "cell_" + hashlib.sha256(atom_id.encode()).hexdigest()[:20]
        atom_cells[atom_id] = cell_id
        cells.append({
            "cell_id": cell_id,
            "basis_object_id": atom_id,
            "source_content_digest": _require_digest(receipt.get("source_digest"), "table cell source_digest"),
            "locator": {"page": _safe_page(atom.get("locator")),
                        "section_id": (atom.get("locator") or {}).get("section_id")},
            "row": binding["row_index"],
            "column": binding["column_index"],
            "raw_text": atom.get("value"),
            "status": "not_governed_candidate",
            "admitted": False,
            "human_approval_required": True,
        })
    cells.sort(key=lambda row: row["cell_id"])

    derivations: list[dict[str, Any]] = []
    skipped_derivations = 0
    numeric_ids = {str(row.get("atom_id")) for row in objects.get("numeric_atoms", [])
                   if isinstance(row, dict) and row.get("atom_id")}
    parameter_ids = {str(row.get("parameter_id")) for row in objects.get("task_parameters", [])
                     if isinstance(row, dict) and row.get("parameter_id")}
    for row in exact_artifact.get("derivations", []):
        if not isinstance(row, dict):
            raise ValueError("derivations must be objects")
        source_ids = row.get("basis_object_ids")
        if not isinstance(source_ids, list) or not source_ids:
            skipped_derivations += 1
            continue
        input_refs = []
        for value in source_ids:
            object_id = str(value)
            if object_id in atom_cells:
                input_refs.append({"object_kind": "table_cell", "object_id": atom_cells[object_id],
                                   "basis_object_id": object_id})
            elif object_id in numeric_ids:
                input_refs.append({"object_kind": "numeric_atom", "object_id": object_id})
            elif object_id in parameter_ids:
                input_refs.append({"object_kind": "task_parameter", "object_id": object_id})
            else:
                input_refs = []
                break
        if not input_refs:
            skipped_derivations += 1
            continue
        derivation_id = row.get("derivation_id")
        if not isinstance(derivation_id, str) or not derivation_id:
            raise ValueError("derivation is missing derivation_id")
        derivations.append({
            "derivation_id": derivation_id,
            "formula": row.get("expression"),
            "input_refs": input_refs,
            "derivation_digest": _require_digest(row.get("derivation_digest"), "derivation_digest"),
            "status": "not_governed_candidate",
            "admitted": False,
            "human_approval_required": True,
        })
    derivations.sort(key=lambda row: row["derivation_id"])

    authorities: list[dict[str, Any]] = []
    for row in objects.get("authority_nodes", []):
        if not isinstance(row, dict):
            raise ValueError("authority nodes must be objects")
        receipt = receipts.get(row.get("evidence_id"))
        if not isinstance(receipt, dict):
            raise ValueError("authority node is missing its source receipt")
        authority_id = row.get("authority_id")
        if not isinstance(authority_id, str) or not authority_id:
            raise ValueError("authority node is missing authority_id")
        authorities.append({
            "authority_id": authority_id,
            "citation": row.get("citation"),
            "proposition": row.get("proposition"),
            "source_content_digest": _require_digest(receipt.get("source_digest"), "authority source_digest"),
            "locator": row.get("locator"),
            "status": "not_governed_candidate",
            "admitted": False,
            "human_approval_required": True,
        })
    authorities.sort(key=lambda row: row["authority_id"])

    source_manifest = {
        "catalog_digest": catalog_digest,
        "exact_artifact_digest": digest(exact_artifact),
        "task_id": task["task_id"],
    }
    graph = {
        "schema_version": SCHEMA,
        "task_id": task["task_id"],
        "source_manifest_digest": digest(source_manifest),
        "claims": sorted(claims, key=lambda row: row["claim_id"]),
        "numeric_atoms": numeric_atoms,
        "table_cells": cells,
        "derivations": derivations,
        "authority_nodes": authorities,
        "task_parameters": [row for row in objects.get("task_parameters", []) if isinstance(row, dict)],
        "automatic_admission": False,
        "human_approval_required": True,
    }
    graph["graph_digest"] = digest(graph)
    validate_graph(graph)
    receipt = {
        "schema_version": SCHEMA,
        "task_id": task["task_id"],
        "status": "compiled-private-task-projection-graph",
        "graph_digest": graph["graph_digest"],
        "source_manifest_digest": graph["source_manifest_digest"],
        "claim_count": len(graph["claims"]),
        "numeric_atom_count": len(graph["numeric_atoms"]),
        "table_cell_count": len(graph["table_cells"]),
        "generic_table_cell_bindings_recovered": recovered_generic_bindings,
        "derivation_count": len(graph["derivations"]),
        "derivations_skipped_with_unknown_inputs": skipped_derivations,
        "authority_count": len(graph["authority_nodes"]),
        "automatic_admission": False,
        "human_approval_required": True,
        "decision_boundary": "Task prompt may select candidates; rubric and gold are absent, and no candidate is admitted.",
    }
    return graph, receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exact-artifact", required=True, type=Path)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--receipt-out", required=True, type=Path)
    args = parser.parse_args()
    graph, receipt = build(exact_artifact=json.loads(args.exact_artifact.read_text()),
                           catalog=json.loads(args.catalog.read_text()))
    _write_private(args.out, graph)
    _write_private(args.receipt_out, receipt)
    print(json.dumps({key: receipt[key] for key in ("status", "task_id", "graph_digest",
                                                     "claim_count", "numeric_atom_count", "table_cell_count",
                                                     "derivation_count")},
                     sort_keys=True))


if __name__ == "__main__":
    main()

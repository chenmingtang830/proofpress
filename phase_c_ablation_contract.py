#!/usr/bin/env python3
"""Fail-closed representation contract for the frozen Phase C ablation.

The treatment is a projection over one frozen research graph.  This module
does not admit candidates, call models, read rubrics, or choose an answer.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any


SCHEMA = "proofpress/phase-c-ablation-projection/v1"
CONDITIONS = ("ordinary-claim", "claim-plus-table-cells", "claim-plus-table-cells-plus-derivation")


def digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _digest(value: Any, field: str) -> None:
    if not isinstance(value, str) or len(value) != 71 or not value.startswith("sha256:"):
        raise ValueError(f"{field} must be a sha256 digest")
    try:
        int(value[7:], 16)
    except ValueError as exc:
        raise ValueError(f"{field} must be a sha256 digest") from exc


def _id_rows(rows: Any, field: str, id_key: str) -> list[dict[str, Any]]:
    if not isinstance(rows, list):
        raise ValueError(f"{field} must be a list")
    values = []
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get(id_key), str) or not row[id_key]:
            raise ValueError(f"{field} entries require {id_key}")
        if row[id_key] in seen:
            raise ValueError(f"{field} ids must be unique")
        seen.add(row[id_key]); values.append(row)
    return values


def validate_graph(graph: dict[str, Any]) -> None:
    if not isinstance(graph, dict):
        raise ValueError("Phase C graph must be an object")
    for field in ("graph_digest", "source_manifest_digest"):
        _digest(graph.get(field), field)
    if graph.get("automatic_admission") is not False or graph.get("human_approval_required") is not True:
        raise ValueError("Phase C graph must retain no-admission and Human Approval boundaries")
    claims = _id_rows(graph.get("claims"), "claims", "claim_id")
    table_cells = _id_rows(graph.get("table_cells"), "table_cells", "cell_id")
    derivations = _id_rows(graph.get("derivations"), "derivations", "derivation_id")
    authorities = _id_rows(graph.get("authority_nodes"), "authority_nodes", "authority_id")
    for cell in table_cells:
        _digest(cell.get("source_content_digest"), "table cell source_content_digest")
        locator = cell.get("locator")
        if not isinstance(locator, dict) or not isinstance(locator.get("page"), int) or locator["page"] < 1:
            raise ValueError("table cell requires a positive-page source locator")
        if not all(isinstance(cell.get(key), int) and cell[key] >= 0 for key in ("row", "column")):
            raise ValueError("table cell requires non-negative row and column")
    cell_ids = {row["cell_id"] for row in table_cells}
    for derivation in derivations:
        input_ids = derivation.get("input_cell_ids")
        if not isinstance(input_ids, list) or not input_ids or any(value not in cell_ids for value in input_ids):
            raise ValueError("derivation inputs must bind known table cells")
        _digest(derivation.get("derivation_digest"), "derivation_digest")
    for authority in authorities:
        _digest(authority.get("source_content_digest"), "authority source_content_digest")
    if not claims:
        raise ValueError("Phase C graph requires at least one ordinary claim")


def project(graph: dict[str, Any], condition: str) -> dict[str, Any]:
    """Create one deterministic working-set projection, without promotion."""
    validate_graph(graph)
    if condition not in CONDITIONS:
        raise ValueError("unknown Phase C condition")
    projection = {"schema_version": SCHEMA, "condition": condition,
                  "graph_digest": graph["graph_digest"], "source_manifest_digest": graph["source_manifest_digest"],
                  "claims": graph["claims"], "authority_nodes": graph["authority_nodes"],
                  "automatic_admission": False, "human_approval_required": True}
    if condition in CONDITIONS[1:]:
        projection["table_cells"] = graph["table_cells"]
    if condition == CONDITIONS[2]:
        projection["derivations"] = graph["derivations"]
    projection["projection_digest"] = digest(projection)
    return projection


def validate_projection(projection: dict[str, Any], graph: dict[str, Any]) -> None:
    validate_graph(graph)
    expected = project(graph, projection.get("condition"))
    if projection != expected:
        raise ValueError("Phase C projection does not match its frozen graph and condition")

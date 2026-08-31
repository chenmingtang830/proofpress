#!/usr/bin/env python3
"""Provider-neutral, source-bound document extraction envelopes.

Extraction output is evidence-candidate material only.  A valid envelope binds
every block and cell to immutable source bytes, extractor configuration, and a
page locator.  Validation never admits the output to governed knowledge.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any


SCHEMA = "proofpress/document-extraction-envelope/v1"
STATUS = "not_governed_candidate"


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canon(value)).hexdigest()


def _sha256(value: str, field: str) -> None:
    if not isinstance(value, str) or len(value) != 71 or not value.startswith("sha256:"):
        raise ValueError(f"{field} must be a sha256 digest")
    try:
        int(value[7:], 16)
    except ValueError as exc:
        raise ValueError(f"{field} must be a sha256 digest") from exc


def _locator(value: Any, field: str) -> None:
    if not isinstance(value, dict) or not isinstance(value.get("page"), int) or value["page"] < 1:
        raise ValueError(f"{field} requires a positive page")
    bbox = value.get("bbox")
    if bbox is not None:
        if (not isinstance(bbox, list) or len(bbox) != 4
                or any(not isinstance(x, (int, float)) for x in bbox)):
            raise ValueError(f"{field}.bbox must contain four numbers")
        if bbox[0] > bbox[2] or bbox[1] > bbox[3]:
            raise ValueError(f"{field}.bbox coordinates are inverted")


def build_envelope(*, source: dict[str, Any], extractor: dict[str, Any],
                   pages: list[dict[str, Any]], blocks: list[dict[str, Any]],
                   tables: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Build and validate a canonical extraction candidate envelope."""
    payload = {
        "schema_version": SCHEMA,
        "status": STATUS,
        "admitted": False,
        "human_approval_required": True,
        "source": source,
        "extractor": extractor,
        "pages": pages,
        "blocks": blocks,
        "tables": tables or [],
    }
    payload["extraction_digest"] = digest(payload)
    validate_envelope(payload)
    return payload


def validate_envelope(value: Any) -> None:
    """Fail closed on missing custody, provenance, locators, or governance state."""
    if not isinstance(value, dict) or value.get("schema_version") != SCHEMA:
        raise ValueError("document extraction envelope schema is required")
    if value.get("status") != STATUS or value.get("admitted") is not False:
        raise ValueError("extraction output must remain not governed and unadmitted")
    if value.get("human_approval_required") is not True:
        raise ValueError("Human Approval must remain required")
    source = value.get("source")
    if not isinstance(source, dict) or not isinstance(source.get("uri"), str):
        raise ValueError("source uri is required")
    _sha256(source.get("content_digest"), "source.content_digest")
    extractor = value.get("extractor")
    required = ("provider", "model", "version", "license", "config_digest")
    if not isinstance(extractor, dict) or any(not extractor.get(key) for key in required):
        raise ValueError("extractor provider, model, version, license, and config digest are required")
    _sha256(extractor["config_digest"], "extractor.config_digest")
    pages = value.get("pages")
    if not isinstance(pages, list) or not pages:
        raise ValueError("at least one extracted page is required")
    page_numbers = set()
    for index, page in enumerate(pages):
        if not isinstance(page, dict) or not isinstance(page.get("page"), int) or page["page"] < 1:
            raise ValueError(f"pages[{index}] requires a positive page")
        if page["page"] in page_numbers:
            raise ValueError("page numbers must be unique")
        page_numbers.add(page["page"])
        _sha256(page.get("render_digest"), f"pages[{index}].render_digest")
    blocks = value.get("blocks")
    if not isinstance(blocks, list):
        raise ValueError("blocks must be a list")
    block_ids = set()
    for index, block in enumerate(blocks):
        if not isinstance(block, dict) or not isinstance(block.get("id"), str) or not block["id"]:
            raise ValueError(f"blocks[{index}] requires an id")
        if block["id"] in block_ids:
            raise ValueError("block ids must be unique")
        block_ids.add(block["id"])
        if not isinstance(block.get("text"), str):
            raise ValueError(f"blocks[{index}].text must be text")
        _locator(block.get("locator"), f"blocks[{index}].locator")
        if block["locator"]["page"] not in page_numbers:
            raise ValueError(f"blocks[{index}] refers to an unknown page")
    tables = value.get("tables")
    if not isinstance(tables, list):
        raise ValueError("tables must be a list")
    table_ids = set()
    for table_index, table in enumerate(tables):
        if not isinstance(table, dict) or not isinstance(table.get("id"), str) or not table["id"]:
            raise ValueError(f"tables[{table_index}] requires an id")
        if table["id"] in table_ids:
            raise ValueError("table ids must be unique")
        table_ids.add(table["id"])
        _locator(table.get("locator"), f"tables[{table_index}].locator")
        cells = table.get("cells")
        if not isinstance(cells, list) or not cells:
            raise ValueError(f"tables[{table_index}] requires cells")
        coordinates = set()
        for cell_index, cell in enumerate(cells):
            if not isinstance(cell, dict):
                raise ValueError("table cell must be an object")
            coordinate = (cell.get("row"), cell.get("column"))
            if (not all(isinstance(x, int) and x >= 0 for x in coordinate)
                    or coordinate in coordinates):
                raise ValueError("table cell coordinates must be unique non-negative integers")
            coordinates.add(coordinate)
            if not isinstance(cell.get("raw_text"), str):
                raise ValueError("table cell raw_text is required")
            _locator(cell.get("locator"), f"tables[{table_index}].cells[{cell_index}].locator")
            if cell["locator"]["page"] not in page_numbers:
                raise ValueError("table cell refers to an unknown page")
    expected = value.get("extraction_digest")
    _sha256(expected, "extraction_digest")
    body = {key: item for key, item in value.items() if key != "extraction_digest"}
    if expected != digest(body):
        raise ValueError("extraction digest mismatch")


def compare_envelopes(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    """Create a deterministic conflict receipt without choosing a winner."""
    validate_envelope(left)
    validate_envelope(right)
    if left["source"]["content_digest"] != right["source"]["content_digest"]:
        raise ValueError("cannot compare extraction envelopes for different source bytes")
    left_cells = {(table["id"], cell["row"], cell["column"]): cell["raw_text"]
                  for table in left["tables"] for cell in table["cells"]}
    right_cells = {(table["id"], cell["row"], cell["column"]): cell["raw_text"]
                   for table in right["tables"] for cell in table["cells"]}
    keys = sorted(set(left_cells) | set(right_cells))
    conflicts = [{"table_id": key[0], "row": key[1], "column": key[2],
                  "left": left_cells.get(key), "right": right_cells.get(key)}
                 for key in keys if left_cells.get(key) != right_cells.get(key)]
    receipt = {"schema_version": "proofpress/document-extraction-conflict/v1",
               "source_content_digest": left["source"]["content_digest"],
               "left_extraction_digest": left["extraction_digest"],
               "right_extraction_digest": right["extraction_digest"],
               "resolution": "human_review_required" if conflicts else "no_cell_conflict",
               "conflicts": conflicts}
    receipt["conflict_digest"] = digest(receipt)
    return receipt

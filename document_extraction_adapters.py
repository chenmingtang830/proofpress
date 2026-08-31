#!/usr/bin/env python3
"""Normalization adapters for provider document-extraction outputs."""
from __future__ import annotations

import hashlib
import re
from html.parser import HTMLParser
from typing import Any

from document_extraction_contract import build_envelope, digest


class _TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(); self.rows: list[list[str]] = []; self.row: list[str] | None = None
        self.cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr": self.row = []
        elif tag in {"td", "th"} and self.row is not None: self.cell = []

    def handle_data(self, data: str) -> None:
        if self.cell is not None: self.cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self.row is not None and self.cell is not None:
            self.row.append("".join(self.cell).strip()); self.cell = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row); self.row = None


def _table_rows(text: str) -> list[list[str]]:
    if "<table" in text.lower():
        parser = _TableParser(); parser.feed(text)
        return [row for row in parser.rows if row]
    lines = [line.strip() for line in text.splitlines() if "|" in line]
    rows = [[cell.strip() for cell in line.strip("|").split("|")] for line in lines]
    return [row for row in rows if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in row)]


def paddle_result_to_envelope(result: dict[str, Any], *, source: dict[str, Any],
                              version: str = "1.6", config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Normalize PaddleOCR-VL page results without granting governance status."""
    config = config or {}
    page_results = result.get("pages") if isinstance(result.get("pages"), list) else [result]
    pages, blocks, tables = [], [], []
    for page_result in page_results:
        page = int(page_result.get("page_index", 0)) + 1
        render_basis = {"source_content_digest": source["content_digest"], "page": page,
                        "width": page_result.get("width"), "height": page_result.get("height")}
        pages.append({"page": page, "render_digest": digest(render_basis),
                      "width": page_result.get("width"), "height": page_result.get("height")})
        for index, raw in enumerate(page_result.get("parsing_res_list", [])):
            bbox = [float(value) for value in raw.get("block_bbox", [])]
            locator = {"page": page, "bbox": bbox} if len(bbox) == 4 else {"page": page}
            text = str(raw.get("block_content", ""))
            basis = {"page": page, "index": index, "label": raw.get("block_label"),
                     "text": text, "locator": locator}
            block_id = "block_" + hashlib.sha256(repr(basis).encode()).hexdigest()[:20]
            blocks.append({"id": block_id, "kind": raw.get("block_label", "unknown"),
                           "text": text, "locator": locator})
            if raw.get("block_label") == "table":
                rows = _table_rows(text)
                if rows:
                    cells = [{"row": row_index, "column": column_index,
                              "raw_text": cell, "locator": locator}
                             for row_index, row in enumerate(rows)
                             for column_index, cell in enumerate(row)]
                    tables.append({"id": "table_" + block_id[6:], "locator": locator,
                                   "source_block_id": block_id, "cells": cells})
    header_groups: dict[tuple[str, ...], list[dict[str, Any]]] = {}
    for table in tables:
        header = tuple(cell["raw_text"].strip().casefold() for cell in table["cells"] if cell["row"] == 0)
        if header: header_groups.setdefault(header, []).append(table)
    for header, group in header_groups.items():
        ordered = sorted(group, key=lambda table: table["locator"]["page"])
        if len(ordered) > 1 and all(right["locator"]["page"] == left["locator"]["page"] + 1
                                    for left, right in zip(ordered, ordered[1:])):
            continuation_id = "continuation_" + digest({"header": header})[7:27]
            for table in ordered: table["continuation_id"] = continuation_id
    return build_envelope(source=source,
                          extractor={"provider": "PaddlePaddle", "model": "PaddleOCR-VL",
                                     "version": version, "license": "Apache-2.0",
                                     "config_digest": digest(config)},
                          pages=pages, blocks=blocks, tables=tables)


def deepseek_markdown_to_envelope(markdown_pages: list[dict[str, Any]], *,
                                  source: dict[str, Any], version: str = "2",
                                  config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Normalize DeepSeek OCR Markdown while marking missing geometry honestly."""
    config = config or {}
    pages, blocks, tables = [], [], []
    for raw in markdown_pages:
        page = raw["page"]; text = raw["markdown"]
        pages.append({"page": page, "render_digest": raw["render_digest"]})
        locator = {"page": page}
        block_id = "block_" + hashlib.sha256(f"{page}\n{text}".encode()).hexdigest()[:20]
        blocks.append({"id": block_id, "kind": "markdown_page", "text": text,
                       "locator": locator, "geometry_status": "page_only"})
        rows = _table_rows(text)
        if rows:
            tables.append({"id": "table_" + block_id[6:], "locator": locator,
                           "geometry_status": "page_only",
                           "cells": [{"row": i, "column": j, "raw_text": cell,
                                      "locator": locator}
                                     for i, row in enumerate(rows) for j, cell in enumerate(row)]})
    return build_envelope(source=source,
                          extractor={"provider": "DeepSeek", "model": "DeepSeek-OCR-2",
                                     "version": version, "license": "Apache-2.0",
                                     "config_digest": digest(config)},
                          pages=pages, blocks=blocks, tables=tables)


def native_text_to_envelope(pages_text: list[dict[str, Any]], *, source: dict[str, Any],
                            version: str = "1", config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Normalize the existing page-text representation as a no-table control.

    This is deliberately conservative: native PDF text has a page locator but
    does not infer table cells, geometry, or cross-page table identity.
    """
    config = config or {}
    pages, blocks = [], []
    for raw in pages_text:
        page = int(raw["page"])
        text = str(raw.get("text", ""))
        render_digest = digest({"source_content_digest": source["content_digest"],
                                "page": page, "native_text": text})
        pages.append({"page": page, "render_digest": render_digest})
        block_id = "block_" + hashlib.sha256(f"native\n{page}\n{text}".encode()).hexdigest()[:20]
        blocks.append({"id": block_id, "kind": "native_pdf_text", "text": text,
                       "locator": {"page": page}, "geometry_status": "page_only"})
    return build_envelope(source=source,
                          extractor={"provider": "Proofpress", "model": "native-pdf-text",
                                     "version": version, "license": "project-internal",
                                     "config_digest": digest(config)},
                          pages=pages, blocks=blocks, tables=[])

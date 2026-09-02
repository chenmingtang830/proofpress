#!/usr/bin/env python3
"""Deterministic structure-ground-truth scoring for extraction envelopes."""
from __future__ import annotations

from collections import Counter
from decimal import Decimal, InvalidOperation
import re
from typing import Any

from proofpress.integrations.document_extraction.contract import validate_envelope


GOLD_SCHEMA = "proofpress/document-extraction-ground-truth/v1"
SCORE_SCHEMA = "proofpress/document-extraction-qualification-score/v1"
_NUMBER = re.compile(r"(?:[$€£]\s*)?\(?[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?\)?")


def _text(value: str) -> str:
    return " ".join(value.split()).casefold()


def _cell_text(value: Any) -> str:
    if isinstance(value, str): return value
    if isinstance(value, dict) and isinstance(value.get("raw_text"), str): return value["raw_text"]
    raise ValueError("ground truth cell must be text or contain raw_text")


def _number(value: str) -> str | None:
    raw = value.strip().replace(",", "")
    negative = raw.startswith("(") and raw.endswith(")")
    if negative: raw = raw[1:-1]
    raw = re.sub(r"^[$€£]\s*", "", raw); raw = raw.removesuffix("%")
    try:
        parsed = Decimal(raw)
    except InvalidOperation:
        return None
    if negative: parsed = -parsed
    normalized = format(parsed, "f").rstrip("0").rstrip(".")
    return normalized or "0"


def _numbers(text: str) -> Counter[str]:
    values = []
    for match in _NUMBER.finditer(text):
        normalized = _number(match.group(0))
        if normalized is not None: values.append(normalized)
    return Counter(values)


def _prf(expected: Counter[Any], observed: Counter[Any]) -> dict[str, Any]:
    matched = sum((expected & observed).values())
    expected_total = sum(expected.values()); observed_total = sum(observed.values())
    precision = matched / observed_total if observed_total else (1.0 if not expected_total else 0.0)
    recall = matched / expected_total if expected_total else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"matched": matched, "expected": expected_total, "observed": observed_total,
            "precision": precision, "recall": recall, "f1": f1}


def _iou(left: list[float], right: list[float]) -> float:
    x1=max(left[0],right[0]); y1=max(left[1],right[1]); x2=min(left[2],right[2]); y2=min(left[3],right[3])
    intersection=max(0,x2-x1)*max(0,y2-y1)
    left_area=max(0,left[2]-left[0])*max(0,left[3]-left[1])
    right_area=max(0,right[2]-right[0])*max(0,right[3]-right[1])
    union=left_area+right_area-intersection
    return intersection/union if union else 0.0


def _continuation_classes(tables: list[dict[str, Any]], *, gold: bool) -> Counter[Any]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for table in tables:
        continuation_id=table.get("continuation_id")
        if continuation_id: groups.setdefault(continuation_id,[]).append(table)
    classes=[]
    for group in groups.values():
        pages=tuple(sorted(table["page"] if gold else table["locator"]["page"] for table in group))
        headers=[]
        for table in group:
            if gold:
                first=table["cells"][0] if table["cells"] else []
                header=tuple(_text(_cell_text(cell)) for cell in first)
            else:
                header=tuple(_text(cell["raw_text"]) for cell in table["cells"] if cell["row"]==0)
            headers.append(header)
        classes.append((pages,tuple(sorted(headers))))
    return Counter(classes)


def validate_ground_truth(gold: Any) -> None:
    if not isinstance(gold, dict) or gold.get("schema_version") != GOLD_SCHEMA:
        raise ValueError("document extraction ground-truth schema is required")
    if not isinstance(gold.get("source_content_digest"), str):
        raise ValueError("ground truth source digest is required")
    if not isinstance(gold.get("blocks"), list) or not isinstance(gold.get("tables"), list):
        raise ValueError("ground truth blocks and tables are required")
    for block in gold["blocks"]:
        if not isinstance(block.get("text"), str) or not isinstance(block.get("page"), int):
            raise ValueError("ground truth block text and page are required")
        if not isinstance(block.get("order"), int):
            raise ValueError("ground truth block order is required")
    for table in gold["tables"]:
        if not isinstance(table.get("cells"), list) or not isinstance(table.get("page"), int):
            raise ValueError("ground truth table page and cells are required")


def score_envelope(envelope: dict[str, Any], gold: dict[str, Any], *,
                   repeat_extraction_digest: str | None = None) -> dict[str, Any]:
    validate_envelope(envelope); validate_ground_truth(gold)
    if envelope["source"]["content_digest"] != gold["source_content_digest"]:
        raise ValueError("ground truth and extraction source digests differ")
    expected_blocks = Counter(_text(row["text"]) for row in gold["blocks"])
    observed_blocks = Counter(_text(row["text"]) for row in envelope["blocks"]
                              if row.get("kind") != "table")
    expected_cells = Counter((row_index, column_index, _text(_cell_text(cell)))
        for table in gold["tables"] for row_index, row in enumerate(table["cells"])
        for column_index, cell in enumerate(row))
    observed_cells = Counter((cell["row"], cell["column"], _text(cell["raw_text"]))
        for table in envelope["tables"] for cell in table["cells"])
    expected_numeric = Counter()
    for block in gold["blocks"]: expected_numeric += _numbers(block["text"])
    for table in gold["tables"]:
        for row in table["cells"]:
            for cell in row: expected_numeric += _numbers(_cell_text(cell))
    observed_numeric = Counter()
    for block in envelope["blocks"]:
        if block.get("kind") != "table": observed_numeric += _numbers(block["text"])
    for table in envelope["tables"]:
        for cell in table["cells"]: observed_numeric += _numbers(cell["raw_text"])

    observed_by_text: dict[str, list[dict[str, Any]]] = {}
    for block in envelope["blocks"]: observed_by_text.setdefault(_text(block["text"]), []).append(block)
    locator_expected=0; locator_matched=0; order_expected=0; order_matched=0
    for block in gold["blocks"]:
        matches=observed_by_text.get(_text(block["text"]), [])
        locator_expected += 1
        if matches:
            candidate=matches[0]; locator=candidate["locator"]
            page_ok=locator["page"] == block["page"]
            bbox_ok=("bbox" not in block or (locator.get("bbox") is not None
                     and _iou(block["bbox"], locator["bbox"]) >= 0.5))
            locator_matched += int(page_ok and bbox_ok)
    for page in sorted({row["page"] for row in gold["blocks"]}):
        ordered=sorted((row for row in gold["blocks"] if row["page"]==page),key=lambda row:row["order"])
        for left,right in zip(ordered,ordered[1:]):
            left_matches=observed_by_text.get(_text(left["text"]),[]); right_matches=observed_by_text.get(_text(right["text"]),[])
            order_expected += 1
            if left_matches and right_matches:
                actual_ids=[row["id"] for row in envelope["blocks"] if row["locator"]["page"]==page]
                order_matched += int(actual_ids.index(left_matches[0]["id"]) < actual_ids.index(right_matches[0]["id"]))
    expected_continuations=_continuation_classes(gold["tables"],gold=True)
    observed_continuations=_continuation_classes(envelope["tables"],gold=False)
    result={"schema_version":SCORE_SCHEMA,"source_content_digest":gold["source_content_digest"],
            "text_blocks":_prf(expected_blocks,observed_blocks),"table_cells":_prf(expected_cells,observed_cells),
            "numeric_values":_prf(expected_numeric,observed_numeric),
            "locators":{"matched":locator_matched,"expected":locator_expected,
                        "rate":locator_matched/locator_expected if locator_expected else 1.0},
            "reading_order":{"matched":order_matched,"expected":order_expected,
                             "rate":order_matched/order_expected if order_expected else 1.0},
            "cross_page_continuations":_prf(expected_continuations,observed_continuations),
            "repeatability":{"comparable":repeat_extraction_digest is not None,
                             "identical":repeat_extraction_digest == envelope["extraction_digest"] if repeat_extraction_digest else None},
            "automatic_admission":False,"human_approval_required":True}
    return result

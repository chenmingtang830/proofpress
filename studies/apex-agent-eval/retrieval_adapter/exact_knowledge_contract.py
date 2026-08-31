"""Fail-closed contracts for exact numeric, authority, and derivation knowledge.

The module is task-domain neutral.  It does not admit knowledge, expose a gold
answer, or allow an executor to turn retrieved material into governed matter
knowledge.  It makes exact task primitives machine-checkable before a claim is
proposed or disclosed.
"""
from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, InvalidOperation
import re
from typing import Any, Iterable
from urllib.parse import urlparse

from governed_workflow_contract import ATOM_SCHEMA, digest, validate_atom
from open_discovery_private import calculate_derivation


REQUIREMENT_PLAN_SCHEMA = "proofpress/exact-requirement-plan/v1"
READINESS_SCHEMA = "proofpress/exact-knowledge-readiness/v1"
AUTHORITY_NODE_SCHEMA = "proofpress/authority-node/v1"
DERIVATION_NODE_SCHEMA = "proofpress/derivation-node/v1"
NUMERIC_BINDING_GATE_SCHEMA = "proofpress/numeric-binding-gate/v1"
TASK_PARAMETER_SCHEMA = "proofpress/task-parameter/v1"
PERIOD_DOMAIN_SCHEMA = "proofpress/period-domain/v1"
AUTHORITY_APPLICABILITY_SCHEMA = "proofpress/authority-applicability-screen/v1"
AUTHORITY_CANDIDATE_OUTCOMES = frozenset({
    "exact_reference_match_candidate",
    "independent_review_supports_candidate",
})

SLOT_OBJECT_KINDS = {
    "exact_value": {"evidence_atom", "derivation_node"},
    "value_by_period": {"evidence_atom", "derivation_node"},
    "ratio_or_threshold": {"evidence_atom", "derivation_node", "authority_node"},
    "factual_status": {"evidence_atom"},
    "controlling_authority": {"authority_node"},
    "legal_consequence": {"evidence_atom", "authority_node", "derivation_node"},
    "recommended_action": {"evidence_atom", "authority_node"},
    "output_structure": set(),
}
OUTPUT_TYPES = {"message_in_console", "make_new_doc", "edit_existing_doc"}
PRECISION_STATES = {"exact", "rounded", "estimated", "disputed"}
EXACTNESS_STATES = {"exact", "bounded", "qualitative"}
NUMERIC_KINDS = {"currency", "percentage", "year", "count", "decimal"}
AUTHORITY_LEVELS = {"statute", "regulation", "case", "administrative", "secondary"}
OFFICIAL_AUTHORITY_HOSTS = {
    "ecfr.gov", "www.ecfr.gov", "govinfo.gov", "www.govinfo.gov",
    "irs.gov", "www.irs.gov", "uscode.house.gov",
}

_NUMBER = re.compile(
    r"(?P<currency>(?:[$€£])\s*(?:\([+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[kKmMbB])?\)"
    r"|[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[kKmMbB])?))"
    r"|(?P<percentage>(?:\([+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?\s*%\)"
    r"|[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?\s*%))"
    r"|(?P<year>\b(?:19|20)\d{2}\b)"
    r"|(?P<number>\b[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[kKmMbB])?\b)"
)
_PERIOD = re.compile(r"^(?:19|20)\d{2}$")
_PERIOD_IN_TEXT = re.compile(r"\b(?:19|20)\d{2}\b")
_AUTHORITY_REFERENCE = re.compile(
    r"(?:\b\d+\s+C\.?F\.?R\.?\s*§?\s*[\d.]+(?:-\d+)?(?:\([a-zA-Z0-9]+\))*"
    r"|\b\d+\s+U\.?S\.?C\.?\s*§?\s*\d+[A-Za-z]?(?:\([a-zA-Z0-9]+\))*"
    r"|§{1,2}\s*[\d.]+(?:-\d+)?(?:\([a-zA-Z0-9]+\))*"
    r"|\bRev\.?\s+Proc\.?\s+\d{4}-\d+)",
    re.IGNORECASE,
)


def _decimal_text(value: Any) -> str:
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("numeric value is not decimal-compatible") from exc
    normalized = format(parsed, "f")
    if "." in normalized:
        normalized = normalized.rstrip("0").rstrip(".")
    return normalized or "0"


def normalize_numeric_text(raw_text: str) -> str:
    """Normalize display text without losing its semantic scale.

    Percentages remain percentage-point values (``26%`` -> ``26``), rather
    than silently becoming fractions.  Currency symbols and grouping commas
    are display metadata and do not alter the decimal value.
    """
    if not isinstance(raw_text, str) or not raw_text.strip():
        raise ValueError("numeric display text is required")
    value = raw_text.strip().replace(",", "")
    negative_parentheses = value.startswith("(") and value.endswith(")")
    if negative_parentheses:
        value = value[1:-1].strip()
    value = re.sub(r"^[$€£]\s*", "", value)
    value = re.sub(r"\s*%$", "", value)
    multiplier = Decimal(1)
    if value and value[-1:] in "kKmMbB":
        multiplier = {"k": Decimal(1_000), "m": Decimal(1_000_000),
                      "b": Decimal(1_000_000_000)}[value[-1].lower()]
        value = value[:-1]
    normalized = _decimal_text(Decimal(_decimal_text(value)) * multiplier)
    if negative_parentheses and not normalized.startswith("-") and normalized != "0":
        normalized = "-" + normalized
    return normalized


def extract_numeric_candidates(text: str) -> list[dict[str, Any]]:
    """Inventory every number-like source span before semantic selection.

    Citation section numbers are deliberately retained.  A later semantic
    stage must bind them as authority mentions instead of dropping them during
    source inventory.
    """
    if not isinstance(text, str):
        raise ValueError("numeric inventory input must be text")
    rows: list[dict[str, Any]] = []
    for match in _NUMBER.finditer(text):
        group = match.lastgroup or "number"
        raw = match.group(0)
        kind = {"currency": "currency", "percentage": "percentage",
                "year": "year", "number": "decimal"}[group]
        try:
            normalized_value = normalize_numeric_text(raw)
            normalization_error = None
        except ValueError as exc:
            normalized_value = None
            normalization_error = digest({"type": type(exc).__name__, "raw_text": raw})
        basis = {"start": match.start(), "end": match.end(), "raw_text": raw,
                 "normalized_value": normalized_value, "kind_hint": kind,
                 "normalization_error": normalization_error}
        rows.append({"candidate_id": "number_" + digest(basis).split(":", 1)[1][:20], **basis})
    return rows


def extract_period_domain_candidates(text: str) -> list[dict[str, Any]]:
    """Inventory exact receipt spans that explicitly contain multiple years.

    The inventory is syntactic only.  It does not decide whether a span is a
    complete schedule; a separate selector may only choose one of these exact
    candidates and Human Approval remains required before governed reliance.
    """
    if not isinstance(text, str) or not text:
        return []
    spans: set[tuple[int, int]] = set()

    def add_span(start: int, end: int) -> None:
        while start < end and text[start].isspace():
            start += 1
        while end > start and text[end - 1].isspace():
            end -= 1
        if 0 <= start < end <= len(text) and end - start <= 2000:
            spans.add((start, end))

    for match in re.finditer(r"(?:^|\n\s*\n)(.*?)(?=\n\s*\n|$)", text,
                             flags=re.DOTALL):
        add_span(match.start(1), match.end(1))
    for match in re.finditer(r"[^\n]+", text):
        add_span(match.start(), match.end())

    year_matches = list(_PERIOD_IN_TEXT.finditer(text))
    cluster: list[re.Match[str]] = []
    for match in year_matches:
        if cluster and match.start() - cluster[-1].end() > 480:
            first, last = cluster[0], cluster[-1]
            start = text.rfind("\n", 0, first.start()) + 1
            line_end = text.find("\n", last.end())
            add_span(start, len(text) if line_end < 0 else line_end)
            cluster = []
        cluster.append(match)
    if cluster:
        first, last = cluster[0], cluster[-1]
        start = text.rfind("\n", 0, first.start()) + 1
        line_end = text.find("\n", last.end())
        add_span(start, len(text) if line_end < 0 else line_end)

    rows = []
    for start, end in sorted(spans):
        excerpt = text[start:end]
        periods = sorted(set(_PERIOD_IN_TEXT.findall(excerpt)))
        if not 2 <= len(periods) <= 32:
            continue
        basis = {"start": start, "end": end, "exact_excerpt": excerpt, "periods": periods}
        rows.append({"candidate_id": "period_candidate_" + digest(basis).split(":", 1)[1][:20],
                     "start": start, "end": end, "exact_excerpt": excerpt,
                     "periods": periods})
    return rows


def extract_tabular_schedule_series(text: str) -> list[dict[str, Any]]:
    """Inventory exact TSV schedule series with deterministic cell coordinates.

    The private APEX catalog preserves table cells with tab delimiters.  This
    inventory supports periods down the first column and periods across a
    header row.  It performs no semantic selection and grants no governance
    status; a later stage may only select a content-addressed series candidate.
    """
    if not isinstance(text, str):
        raise ValueError("tabular schedule inventory input must be text")
    if not text:
        return []

    line_rows: list[dict[str, Any]] = []
    offset = 0
    for raw_line in text.splitlines(keepends=True):
        content = raw_line.rstrip("\r\n")
        line_rows.append({"start": offset, "end": offset + len(content),
                          "text": content, "tabular": "\t" in content})
        offset += len(raw_line)
    if offset < len(text):
        content = text[offset:]
        line_rows.append({"start": offset, "end": len(text),
                          "text": content, "tabular": "\t" in content})

    groups: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    for line in line_rows:
        if line["tabular"]:
            current.append(line)
        elif current:
            groups.append(current)
            current = []
    if current:
        groups.append(current)

    def cells_for(line: dict[str, Any], table_start: int) -> list[dict[str, Any]]:
        cells = []
        cursor = 0
        for raw in line["text"].split("\t"):
            leading = len(raw) - len(raw.lstrip())
            trailing = len(raw.rstrip())
            start = line["start"] - table_start + cursor + leading
            end = line["start"] - table_start + cursor + trailing
            cells.append({"text": raw.strip(), "span": {"start": start, "end": end}})
            cursor += len(raw) + 1
        return cells

    def exact_number(cell: dict[str, Any]) -> dict[str, Any] | None:
        value = cell["text"]
        inventory = extract_numeric_candidates(value)
        if len(inventory) != 1:
            return None
        candidate = inventory[0]
        if ((candidate["start"], candidate["end"]) != (0, len(value))
                or candidate.get("normalized_value") is None):
            return None
        return candidate

    output: list[dict[str, Any]] = []
    seen: set[str] = set()
    for group in groups:
        table_start = group[0]["start"]
        table_end = group[-1]["end"]
        table_excerpt = text[table_start:table_end]
        parsed = [{"line_index": index, "cells": cells_for(line, table_start)}
                  for index, line in enumerate(group)]
        table_basis = {"exact_excerpt": table_excerpt, "line_count": len(parsed)}
        table_id = "table_candidate_" + digest(table_basis).split(":", 1)[1][:20]

        period_rows = [row for row in parsed
                       if row["cells"] and _PERIOD.fullmatch(row["cells"][0]["text"])]
        if len(period_rows) >= 2:
            first_index = min(row["line_index"] for row in period_rows)
            header = parsed[first_index - 1] if first_index else None
            if header is not None:
                width = min(len(header["cells"]), *(len(row["cells"]) for row in period_rows))
                for column_index in range(1, width):
                    label_cell = header["cells"][column_index]
                    if not label_cell["text"]:
                        continue
                    values = []
                    for row in period_rows:
                        period_cell = row["cells"][0]
                        value_cell = row["cells"][column_index]
                        numeric = exact_number(value_cell)
                        if numeric is None:
                            values = []
                            break
                        values.append({"period": period_cell["text"],
                                       "display": value_cell["text"],
                                       "kind_hint": numeric["kind_hint"],
                                       "normalized_value": numeric["normalized_value"],
                                       "period_span": period_cell["span"],
                                       "value_span": value_cell["span"],
                                       "row_index": row["line_index"],
                                       "column_index": column_index})
                    if len(values) < 2:
                        continue
                    basis = {"table_candidate_id": table_id,
                             "orientation": "period_rows",
                             "label": label_cell["text"],
                             "label_span": label_cell["span"],
                             "period_values": values}
                    series_id = "table_series_" + digest(basis).split(":", 1)[1][:20]
                    if series_id not in seen:
                        output.append({"series_candidate_id": series_id,
                                       "table_candidate_id": table_id,
                                       "orientation": "period_rows",
                                       "exact_excerpt": table_excerpt,
                                       "label": label_cell["text"],
                                       "label_span": label_cell["span"],
                                       "period_values": values})
                        seen.add(series_id)

        for header in parsed:
            period_columns = [(index, cell) for index, cell in enumerate(header["cells"])
                              if _PERIOD.fullmatch(cell["text"])]
            if len(period_columns) < 2:
                continue
            first_period_column = min(index for index, _ in period_columns)
            if first_period_column < 1:
                continue
            for row in parsed[header["line_index"] + 1:]:
                if len(row["cells"]) <= max(index for index, _ in period_columns):
                    continue
                label_cells = [cell for cell in row["cells"][:first_period_column]
                               if cell["text"]]
                if not label_cells:
                    continue
                values = []
                for column_index, period_cell in period_columns:
                    value_cell = row["cells"][column_index]
                    numeric = exact_number(value_cell)
                    if numeric is None:
                        values = []
                        break
                    values.append({"period": period_cell["text"],
                                   "display": value_cell["text"],
                                   "kind_hint": numeric["kind_hint"],
                                   "normalized_value": numeric["normalized_value"],
                                   "period_span": period_cell["span"],
                                   "value_span": value_cell["span"],
                                   "row_index": row["line_index"],
                                   "column_index": column_index})
                if len(values) < 2:
                    continue
                label_span = {"start": label_cells[0]["span"]["start"],
                              "end": label_cells[-1]["span"]["end"]}
                label = table_excerpt[label_span["start"]:label_span["end"]]
                basis = {"table_candidate_id": table_id,
                         "orientation": "period_columns",
                         "label": label, "label_span": label_span,
                         "period_values": values}
                series_id = "table_series_" + digest(basis).split(":", 1)[1][:20]
                if series_id not in seen:
                    output.append({"series_candidate_id": series_id,
                                   "table_candidate_id": table_id,
                                   "orientation": "period_columns",
                                   "exact_excerpt": table_excerpt,
                                   "label": label, "label_span": label_span,
                                   "period_values": values})
                    seen.add(series_id)
    return output


def extract_tabular_numeric_cells(text: str) -> list[dict[str, Any]]:
    """Inventory every exact numeric TSV cell, without requiring a period series.

    Coordinates are syntactic source facts.  This function does not infer a
    header, metric, period, or unit, and it does not select a cell for a task.
    A caller may bind a previously selected numeric atom only when its exact
    source span identifies one unique candidate from this inventory.
    """
    if not isinstance(text, str):
        raise ValueError("tabular numeric cell inventory input must be text")
    rows: list[dict[str, Any]] = []
    lines: list[tuple[int, str]] = []
    offset = 0
    for raw_line in text.splitlines(keepends=True):
        content = raw_line.rstrip("\r\n")
        lines.append((offset, content))
        offset += len(raw_line)
    if offset < len(text):
        lines.append((offset, text[offset:]))

    groups: list[list[tuple[int, str]]] = []
    current: list[tuple[int, str]] = []
    for line in lines:
        if "\t" in line[1]:
            current.append(line)
        elif current:
            groups.append(current); current = []
    if current:
        groups.append(current)

    for group in groups:
        table_start = group[0][0]
        table_end = group[-1][0] + len(group[-1][1])
        table_excerpt = text[table_start:table_end]
        table_basis = {"exact_excerpt": table_excerpt, "line_count": len(group)}
        table_id = "table_candidate_" + digest(table_basis).split(":", 1)[1][:20]
        for row_index, (line_start, content) in enumerate(group):
            cursor = 0
            for column_index, raw_cell in enumerate(content.split("\t")):
                leading = len(raw_cell) - len(raw_cell.lstrip())
                stripped = raw_cell.strip()
                cell_start = line_start + cursor + leading
                cell_end = cell_start + len(stripped)
                cursor += len(raw_cell) + 1
                candidates = extract_numeric_candidates(stripped)
                if len(candidates) != 1 or not stripped:
                    continue
                candidate = candidates[0]
                if ((candidate["start"], candidate["end"]) != (0, len(stripped))
                        or candidate.get("normalized_value") is None):
                    continue
                basis = {"table_candidate_id": table_id, "row_index": row_index,
                         "column_index": column_index, "start": cell_start,
                         "end": cell_end, "raw_text": stripped,
                         "normalized_value": candidate["normalized_value"]}
                rows.append({"cell_candidate_id": "table_cell_" + digest(basis).split(":", 1)[1][:20],
                             **basis, "kind_hint": candidate["kind_hint"],
                             "table_exact_excerpt": table_excerpt,
                             "table_span": {"start": table_start, "end": table_end}})
    return rows


def match_numeric_payload_to_table_cell(payload: dict[str, Any],
                                        receipt: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
    """Return one exact coordinate binding, or fail closed on absence/ambiguity."""
    quote = str(receipt.get("quote") or "")
    excerpt = str(payload.get("exact_excerpt") or "")
    display = str(payload.get("display") or (payload.get("numeric") or {}).get("display") or "")
    if not quote or not excerpt or not display:
        return None, "no_match"
    excerpt_starts = [match.start() for match in re.finditer(re.escape(excerpt), quote)]
    matches: dict[tuple[str, int], tuple[dict[str, Any], int]] = {}
    for candidate in extract_tabular_numeric_cells(quote):
        if candidate["raw_text"] != display:
            continue
        for excerpt_start in excerpt_starts:
            if (excerpt_start <= candidate["start"]
                    and candidate["end"] <= excerpt_start + len(excerpt)):
                matches[(candidate["cell_candidate_id"], excerpt_start)] = (candidate, excerpt_start)
    if not matches:
        return None, "no_match"
    if len(matches) != 1:
        return None, "ambiguous"
    candidate, excerpt_start = next(iter(matches.values()))
    value_span = {"start": candidate["start"] - excerpt_start,
                  "end": candidate["end"] - excerpt_start}
    if excerpt[value_span["start"]:value_span["end"]] != display:
        return None, "no_match"
    return {"table_candidate_id": candidate["table_candidate_id"],
            "orientation": "generic_tsv_cell", "row_index": candidate["row_index"],
            "column_index": candidate["column_index"], "value_span": value_span}, "bound"


def validate_numeric_atom(atom: dict[str, Any],
                          receipts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Validate a number-specialized evidence atom against exact custody."""
    checked = validate_atom(atom, receipts)
    numeric = checked.get("numeric")
    if not isinstance(numeric, dict):
        raise ValueError("numeric evidence atom requires numeric metadata")
    required = ("display", "decimal_value", "kind", "entity", "period", "precision")
    if any(not isinstance(numeric.get(key), str) or not numeric[key].strip() for key in required):
        raise ValueError("numeric evidence atom metadata is incomplete")
    if numeric["kind"] not in NUMERIC_KINDS:
        raise ValueError("numeric evidence atom kind is invalid")
    if numeric["precision"] not in PRECISION_STATES:
        raise ValueError("numeric evidence atom precision is invalid")
    if numeric["display"] not in checked["exact_excerpt"]:
        raise ValueError("numeric display is not bound to the exact excerpt")
    if normalize_numeric_text(numeric["display"]) != _decimal_text(numeric["decimal_value"]):
        raise ValueError("numeric display and decimal value disagree")
    if checked["value"] != numeric["display"]:
        raise ValueError("evidence atom value must preserve the numeric display")
    if numeric["kind"] == "currency" and not str(numeric.get("currency") or "").strip():
        raise ValueError("currency atoms require an explicit currency")
    if checked.get("status") not in (None, "unresolved", "not_governed_candidate"):
        raise ValueError("numeric evidence atom has an invalid candidate status")
    if checked.get("admission_authority") not in (None, False):
        raise ValueError("numeric evidence atom cannot carry admission authority")
    table_binding = checked.get("table_cell_binding")
    if table_binding is not None:
        if not isinstance(table_binding, dict):
            raise ValueError("numeric table cell binding must be an object")
        expected = {"table_candidate_id", "row_index", "column_index", "value_span"}
        if not expected.issubset(table_binding):
            raise ValueError("numeric table cell binding is incomplete")
        excerpt = checked["exact_excerpt"]
        spans = [("value", table_binding["value_span"])]
        if "label_span" in table_binding or "period_span" in table_binding:
            if "label_span" not in table_binding or "period_span" not in table_binding:
                raise ValueError("numeric table semantic spans must be provided together")
            spans = [("label", table_binding["label_span"]),
                     ("period", table_binding["period_span"]), *spans]
        for label, value in spans:
            if (not isinstance(value, dict) or not isinstance(value.get("start"), int)
                    or not isinstance(value.get("end"), int)
                    or not 0 <= value["start"] < value["end"] <= len(excerpt)):
                raise ValueError(f"numeric table {label} span is invalid")
        if excerpt[table_binding["value_span"]["start"]:table_binding["value_span"]["end"]] != numeric["display"]:
            raise ValueError("numeric table value span disagrees with display")
        if "label_span" in table_binding:
            if excerpt[table_binding["label_span"]["start"]:table_binding["label_span"]["end"]] != checked["subject"]:
                raise ValueError("numeric table label span disagrees with subject")
            if excerpt[table_binding["period_span"]["start"]:table_binding["period_span"]["end"]] != numeric["period"]:
                raise ValueError("numeric table period span disagrees with period")
            expected_bindings = {"subject": table_binding["label_span"],
                                 "predicate": table_binding["period_span"],
                                 "value": table_binding["value_span"]}
            if checked.get("field_bindings") != expected_bindings:
                raise ValueError("numeric table field bindings disagree with cell coordinates")
    return checked


def _exact_field_bindings(excerpt: str, values: dict[str, str]) -> dict[str, dict[str, int]]:
    bindings: dict[str, dict[str, int]] = {}
    for field, value in values.items():
        start = excerpt.find(value)
        if start < 0:
            raise ValueError(f"evidence atom {field} is not present in the exact excerpt")
        bindings[field] = {"start": start, "end": start + len(value)}
    return bindings


def bind_evidence_atom(payload: dict[str, Any],
                       receipts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Construct a general unresolved evidence atom from one exact source span."""
    required = ("requirement_id", "evidence_id", "subject", "predicate", "value")
    if any(not isinstance(payload.get(key), str) or not payload[key].strip() for key in required):
        raise ValueError("evidence atom binding payload is incomplete")
    receipt = receipts.get(payload["evidence_id"])
    if not isinstance(receipt, dict):
        raise ValueError("evidence atom receipt is missing")
    excerpt = str(payload.get("exact_excerpt") or "")
    if not excerpt or excerpt not in str(receipt.get("quote") or ""):
        raise ValueError("evidence atom exact excerpt is not receipt-bound")
    values = {key: payload[key] for key in ("subject", "predicate", "value")}
    basis = {"requirement_id": payload["requirement_id"],
             "evidence_id": payload["evidence_id"],
             "receipt_digest": receipt.get("receipt_digest"), **values,
             "effective_date": payload.get("effective_date"),
             "qualification": payload.get("qualification"),
             "document_version": str(payload.get("document_version") or "unknown"),
             "exact_excerpt": excerpt, "locator": receipt.get("locator"),
             "support_mode": "explicit",
             "field_bindings": _exact_field_bindings(excerpt, values),
             "status": "not_governed_candidate", "admission_authority": False}
    atom = {"schema_version": ATOM_SCHEMA,
            "atom_id": "atom_" + digest(basis).split(":", 1)[1][:20], **basis}
    return validate_atom(atom, receipts)


def bind_numeric_atom(payload: dict[str, Any],
                      receipts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Construct an unresolved numeric atom from an exact custody-valid span."""
    required = ("requirement_id", "evidence_id", "subject", "predicate", "display",
                "kind", "entity", "period", "precision")
    if any(not isinstance(payload.get(key), str) or not payload[key].strip() for key in required):
        raise ValueError("numeric atom binding payload is incomplete")
    receipt = receipts.get(payload["evidence_id"])
    if not isinstance(receipt, dict):
        raise ValueError("numeric atom receipt is missing")
    excerpt = str(payload.get("exact_excerpt") or "")
    if not excerpt or excerpt not in str(receipt.get("quote") or ""):
        raise ValueError("numeric atom exact excerpt is not receipt-bound")
    display = payload["display"]
    values = {"subject": payload["subject"], "predicate": payload["predicate"],
              "value": display}
    table_binding = payload.get("table_cell_binding")
    semantic_table_binding = (isinstance(table_binding, dict)
                              and "label_span" in table_binding and "period_span" in table_binding)
    field_bindings = (_exact_field_bindings(excerpt, values) if not semantic_table_binding else
                      {"subject": table_binding.get("label_span"),
                       "predicate": table_binding.get("period_span"),
                       "value": table_binding.get("value_span")})
    basis = {"requirement_id": payload["requirement_id"], "evidence_id": payload["evidence_id"],
             "receipt_digest": receipt.get("receipt_digest"), **values,
             "effective_date": payload.get("effective_date"),
             "qualification": payload.get("qualification"),
             "document_version": str(payload.get("document_version") or "unknown"),
             "exact_excerpt": excerpt, "locator": receipt.get("locator"),
             "support_mode": "explicit", "field_bindings": field_bindings,
             "status": "not_governed_candidate", "admission_authority": False,
             "numeric": {"display": display,
                         "decimal_value": normalize_numeric_text(display),
                         "kind": payload["kind"], "currency": payload.get("currency"),
                         "unit": str(payload.get("unit") or ""), "entity": payload["entity"],
                         "period": payload["period"], "precision": payload["precision"]}}
    if table_binding is not None:
        basis["table_cell_binding"] = table_binding
    atom = {"schema_version": ATOM_SCHEMA,
            "atom_id": "atom_" + digest(basis).split(":", 1)[1][:20], **basis}
    return validate_numeric_atom(atom, receipts)


def bind_task_numeric_parameter(task_prompt: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Bind an explicit numeric instruction or assumption without treating it as evidence."""
    required = ("requirement_id", "display", "kind", "entity", "period", "precision",
                "parameter_role")
    if not isinstance(task_prompt, str) or not task_prompt:
        raise ValueError("task prompt is required for a task parameter")
    if any(not isinstance(payload.get(key), str) or not payload[key].strip() for key in required):
        raise ValueError("task parameter binding payload is incomplete")
    display = payload["display"]
    start = task_prompt.find(display)
    if start < 0:
        raise ValueError("task parameter display is not present in the task prompt")
    if payload["kind"] not in NUMERIC_KINDS or payload["precision"] not in PRECISION_STATES:
        raise ValueError("task parameter numeric metadata is invalid")
    if payload["kind"] == "currency" and not str(payload.get("currency") or "").strip():
        raise ValueError("currency task parameters require an explicit currency")
    basis = {
        "requirement_id": payload["requirement_id"],
        "task_prompt_digest": digest(task_prompt),
        "display_span": {"start": start, "end": start + len(display)},
        "numeric": {"display": display, "decimal_value": normalize_numeric_text(display),
                    "kind": payload["kind"], "currency": payload.get("currency"),
                    "unit": str(payload.get("unit") or ""), "entity": payload["entity"],
                    "period": payload["period"], "precision": payload["precision"]},
        "parameter_role": payload["parameter_role"],
        "status": "task_instruction_not_governed",
        "governed_reliance_allowed": False,
        "automatic_admission": False,
        "admission_authority": False,
    }
    node = {"schema_version": TASK_PARAMETER_SCHEMA,
            "parameter_id": "param_" + digest(basis).split(":", 1)[1][:20], **basis}
    node["parameter_digest"] = digest(node)
    return node


def bind_period_domain(payload: dict[str, Any],
                       receipts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Bind a closed annual domain to an explicit source schedule.

    The function deliberately supports only explicit enumeration.  A phrase
    such as ``each affected year`` is not a closed domain, and a model may not
    infer missing intermediate years from two endpoints.  Broader temporal
    interpretation remains a review question.
    """
    required = ("requirement_id", "evidence_id", "exact_excerpt", "periods")
    if any(key not in payload for key in required):
        raise ValueError("period domain required fields are missing")
    requirement_id = str(payload.get("requirement_id") or "").strip()
    evidence_id = str(payload.get("evidence_id") or "").strip()
    excerpt = str(payload.get("exact_excerpt") or "")
    periods = payload.get("periods")
    if not requirement_id or not evidence_id or not excerpt:
        raise ValueError("period domain required fields are missing")
    if (not isinstance(periods, list) or not periods
            or any(not isinstance(row, str) or not _PERIOD.fullmatch(row) for row in periods)
            or len(set(periods)) != len(periods)):
        raise ValueError("period domain requires unique four-digit years")
    receipt = receipts.get(evidence_id)
    if not isinstance(receipt, dict) or not receipt.get("custody_valid"):
        raise ValueError("period domain receipt is missing or custody-invalid")
    if excerpt not in str(receipt.get("quote") or ""):
        raise ValueError("period domain excerpt is not receipt-bound")
    if any(period not in excerpt for period in periods):
        raise ValueError("every period must be explicit in the bound schedule excerpt")
    basis = {
        "requirement_id": requirement_id,
        "evidence_id": evidence_id,
        "receipt_digest": receipt.get("receipt_digest"),
        "locator": receipt.get("locator"),
        "exact_excerpt": excerpt,
        "periods": sorted(periods),
        "closure_basis": "explicit_source_schedule_enumeration",
        "status": "not_governed_candidate",
        "governed_reliance_allowed": False,
        "automatic_admission": False,
        "admission_authority": False,
    }
    node = {"schema_version": PERIOD_DOMAIN_SCHEMA,
            "period_domain_id": "period_domain_" + digest(basis).split(":", 1)[1][:20],
            **basis}
    node["period_domain_digest"] = digest(node)
    return node


def _authority_reference_tokens(text: str) -> list[str]:
    def normalize(value: str) -> str:
        value = value.lower().replace("§", " ")
        return re.sub(r"[^a-z0-9.-]+", "", value)
    return sorted(set(normalize(match.group(0)) for match in _AUTHORITY_REFERENCE.finditer(text)))


def screen_authority_applicability(requirement_description: str,
                                   authority_node: dict[str, Any]) -> dict[str, Any]:
    """Screen exact citation identity without deciding legal applicability.

    Exact-reference requirements can be rejected deterministically when the
    candidate cites a different provision.  A match remains a candidate and
    still requires an independent applicability decision and Human Approval.
    Requirements without an explicit reference always remain pending review.
    """
    if not isinstance(requirement_description, str) or not requirement_description.strip():
        raise ValueError("authority applicability requires a requirement description")
    if (not isinstance(authority_node, dict)
            or authority_node.get("schema_version") != AUTHORITY_NODE_SCHEMA
            or not _embedded_digest_valid(authority_node, "authority_digest")):
        raise ValueError("authority applicability requires a digest-valid authority node")
    expected = _authority_reference_tokens(requirement_description)
    observed = _authority_reference_tokens(str(authority_node.get("citation") or ""))
    if expected and not set(expected).intersection(observed):
        outcome = "citation_mismatch"
    elif expected:
        outcome = "exact_reference_match_candidate"
    else:
        outcome = "independent_legal_review_required"
    basis = {
        "requirement_id": authority_node["requirement_id"],
        "authority_id": authority_node["authority_id"],
        "authority_digest": authority_node["authority_digest"],
        "requirement_description_digest": digest(requirement_description),
        "expected_reference_tokens": expected,
        "observed_reference_tokens": observed,
        "outcome": outcome,
        "legal_applicability_confirmed": False,
        "human_review_required": True,
        "governed_reliance_allowed": False,
        "automatic_admission": False,
        "admission_authority": False,
    }
    screen = {"schema_version": AUTHORITY_APPLICABILITY_SCHEMA,
              "screen_id": "authority_screen_" + digest(basis).split(":", 1)[1][:20],
              **basis}
    screen["screen_digest"] = digest(screen)
    return screen


def bind_independent_authority_review(requirement_description: str,
                                      authority_node: dict[str, Any], *,
                                      supports_candidate: bool,
                                      review_record_digest: str,
                                      reviewer_route: str) -> dict[str, Any]:
    """Bind an independent semantic screen while preserving human authority.

    This object records a model-review result; it is not a legal conclusion or
    an approval.  An explicit citation mismatch cannot be overridden by the
    semantic reviewer.
    """
    deterministic = screen_authority_applicability(requirement_description, authority_node)
    if deterministic["outcome"] == "citation_mismatch" and supports_candidate:
        raise ValueError("independent review cannot override an exact citation mismatch")
    if (not isinstance(review_record_digest, str)
            or not review_record_digest.startswith("sha256:")):
        raise ValueError("independent authority review requires a record digest")
    if not isinstance(reviewer_route, str) or not reviewer_route.strip():
        raise ValueError("independent authority review requires a reviewer route")
    outcome = ("independent_review_supports_candidate" if supports_candidate
               else "independent_review_rejects_candidate")
    basis = {
        "requirement_id": authority_node["requirement_id"],
        "authority_id": authority_node["authority_id"],
        "authority_digest": authority_node["authority_digest"],
        "requirement_description_digest": digest(requirement_description),
        "deterministic_screen_id": deterministic["screen_id"],
        "deterministic_outcome": deterministic["outcome"],
        "review_record_digest": review_record_digest,
        "reviewer_route": reviewer_route,
        "outcome": outcome,
        "legal_applicability_confirmed": False,
        "human_review_required": True,
        "governed_reliance_allowed": False,
        "automatic_admission": False,
        "admission_authority": False,
    }
    screen = {"schema_version": AUTHORITY_APPLICABILITY_SCHEMA,
              "screen_id": "authority_screen_" + digest(basis).split(":", 1)[1][:20],
              **basis}
    screen["screen_digest"] = digest(screen)
    return screen


def validate_authority_node(node: dict[str, Any],
                            receipts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Bind an authority candidate to custody without confirming normativity."""
    if not isinstance(node, dict) or node.get("schema_version") != AUTHORITY_NODE_SCHEMA:
        raise ValueError("authority node schema is required")
    required = ("authority_id", "requirement_id", "evidence_id", "receipt_digest",
                "citation", "proposition", "jurisdiction", "effective_date",
                "authority_level", "exact_excerpt")
    if any(not isinstance(node.get(key), str) or not node[key].strip() for key in required):
        raise ValueError("authority node required fields are missing")
    if node["authority_level"] not in AUTHORITY_LEVELS:
        raise ValueError("authority level is invalid")
    receipt = receipts.get(node["evidence_id"])
    if not isinstance(receipt, dict):
        raise ValueError("authority receipt is missing")
    if node["receipt_digest"] != receipt.get("receipt_digest"):
        raise ValueError("authority receipt digest mismatch")
    if node.get("locator") != receipt.get("locator"):
        raise ValueError("authority locator mismatch")
    if not receipt.get("custody_valid") or node["exact_excerpt"] not in str(receipt.get("quote") or ""):
        raise ValueError("authority text is not bound to valid custody")
    if node["citation"] not in node["exact_excerpt"]:
        raise ValueError("authority citation is not present in the exact excerpt")
    metadata = (receipt.get("source") or {}).get("official_authority")
    if metadata is not None:
        if not isinstance(metadata, dict) or metadata.get("official") is not True:
            raise ValueError("controlled authority metadata is invalid")
        host = urlparse(str((receipt.get("source") or {}).get("uri") or "")).hostname
        if host not in OFFICIAL_AUTHORITY_HOSTS:
            raise ValueError("controlled authority source host is not allowed")
        expected = {
            "jurisdiction": metadata.get("jurisdiction"),
            "effective_date": metadata.get("effective_on"),
            "authority_level": metadata.get("authority_level"),
        }
        if any(node.get(key) != value for key, value in expected.items()):
            raise ValueError("authority node disagrees with controlled source metadata")
        citations = metadata.get("canonical_citations")
        if not isinstance(citations, list) or node["citation"] not in citations:
            raise ValueError("authority citation is outside the controlled source metadata")
    if node.get("normative_authority_confirmed") is not False:
        raise ValueError("candidate authority cannot self-confirm normativity")
    if node.get("admission_authority") is not False:
        raise ValueError("authority candidate cannot carry admission authority")
    checked = dict(node)
    supplied = checked.pop("authority_digest", None)
    calculated = digest(checked)
    if supplied is not None and supplied != calculated:
        raise ValueError("authority node digest mismatch")
    checked["authority_digest"] = calculated
    return checked


def compile_requirement_plan(task_prompt: str, slots: list[dict[str, Any]], *,
                             output_type: str) -> dict[str, Any]:
    """Bind a prompt-only atomic requirement plan without rubric or gold data."""
    if not isinstance(task_prompt, str) or not task_prompt.strip():
        raise ValueError("task prompt is required")
    if output_type not in OUTPUT_TYPES:
        raise ValueError("native output type is invalid")
    if not isinstance(slots, list) or not slots:
        raise ValueError("at least one atomic requirement slot is required")
    checked: list[dict[str, Any]] = []
    seen: set[str] = set()
    forbidden = {"rubric", "gold", "silver_locator", "expected_answer"}
    for raw in slots:
        if not isinstance(raw, dict) or forbidden.intersection(raw):
            raise ValueError("requirement slots cannot carry rubric, gold, or silver data")
        slot_id = str(raw.get("slot_id") or "").strip()
        slot_type = str(raw.get("slot_type") or "").strip()
        description = str(raw.get("description") or "").strip()
        if not slot_id or slot_id in seen or slot_type not in SLOT_OBJECT_KINDS or not description:
            raise ValueError("requirement slot identity, type, or description is invalid")
        seen.add(slot_id)
        requested = raw.get("required_object_kinds")
        if not isinstance(requested, list):
            raise ValueError("requirement slot object kinds must be explicit")
        requested_set = {str(row) for row in requested}
        if requested_set - SLOT_OBJECT_KINDS[slot_type]:
            raise ValueError("requirement slot requests an incompatible object kind")
        if slot_type != "output_structure" and not requested_set:
            raise ValueError("substantive requirement slots need a typed completion path")
        expected_periods = raw.get("expected_periods", [])
        if not isinstance(expected_periods, list) or any(not isinstance(row, str) for row in expected_periods):
            raise ValueError("expected periods must be a string list")
        exactness = str(raw.get("exactness") or "exact")
        if exactness not in EXACTNESS_STATES:
            raise ValueError("requirement slot exactness is invalid")
        if slot_type == "value_by_period" and not expected_periods:
            raise ValueError("value-by-period requirements need explicit periods")
        checked.append({
            "slot_id": slot_id,
            "slot_type": slot_type,
            "description": description,
            "exactness": exactness,
            "expected_periods": expected_periods,
            "required_object_kinds": sorted(requested_set),
            "output_format": str(raw.get("output_format") or ""),
            "object_ids": [],
            "status": "unresolved",
        })
    if sum(row["slot_type"] == "output_structure" for row in checked) != 1:
        raise ValueError("requirement plans need exactly one output-structure slot")
    plan = {
        "schema_version": REQUIREMENT_PLAN_SCHEMA,
        "task_prompt_digest": digest(task_prompt),
        "source_basis": "task_prompt_only_no_rubric_or_gold",
        "output_type": output_type,
        "slots": checked,
        "automatic_admission": False,
        "admission_authority": False,
    }
    plan["plan_digest"] = digest(plan)
    return plan


def bind_requirement_objects(plan: dict[str, Any],
                             assignments: dict[str, list[str]]) -> dict[str, Any]:
    """Attach typed candidate IDs to known slots without changing authority."""
    checked = deepcopy(plan)
    supplied_digest = checked.pop("plan_digest", None)
    if checked.get("schema_version") != REQUIREMENT_PLAN_SCHEMA or supplied_digest != digest(checked):
        raise ValueError("requirement plan digest mismatch")
    slots = {row["slot_id"]: row for row in checked.get("slots", [])}
    if set(assignments) - set(slots):
        raise ValueError("assignment references an unknown requirement slot")
    for slot_id, object_ids in assignments.items():
        if not isinstance(object_ids, list) or any(not isinstance(row, str) or not row for row in object_ids):
            raise ValueError("requirement object IDs must be a non-empty string list")
        slots[slot_id]["object_ids"] = list(dict.fromkeys(object_ids))
        slots[slot_id]["status"] = "candidate_bound" if object_ids else "unresolved"
    checked["plan_digest"] = digest(checked)
    return checked


def bind_candidate_objects(plan: dict[str, Any], *,
                           evidence_atoms: Iterable[dict[str, Any]] = (),
                           authority_nodes: Iterable[dict[str, Any]] = (),
                           derivations: Iterable[dict[str, Any]] = (),
                           authority_screens: Iterable[dict[str, Any]] = ()) -> dict[str, Any]:
    """Deterministically bind only typed candidates eligible for each slot.

    An independent responsiveness screen can make an authority node eligible as
    a not-governed candidate.  It never confirms legal applicability, admits the
    node, or makes governed reliance available.
    """
    supplied_digest = plan.get("plan_digest")
    digest_basis = {key: value for key, value in plan.items() if key != "plan_digest"}
    if plan.get("schema_version") != REQUIREMENT_PLAN_SCHEMA or supplied_digest != digest(digest_basis):
        raise ValueError("requirement plan digest mismatch")
    slots = {row["slot_id"]: row for row in plan.get("slots", [])}
    assignments: dict[str, list[str]] = {slot_id: [] for slot_id in slots}
    screens_by_authority: dict[str, list[dict[str, Any]]] = {}
    for screen in authority_screens:
        if (not isinstance(screen, dict)
                or screen.get("schema_version") != AUTHORITY_APPLICABILITY_SCHEMA
                or not _embedded_digest_valid(screen, "screen_digest")):
            raise ValueError("authority applicability screen must be digest-valid")
        screens_by_authority.setdefault(str(screen.get("authority_id") or ""), []).append(screen)

    for kind, rows, id_key in (
        ("evidence_atom", evidence_atoms, "atom_id"),
        ("authority_node", authority_nodes, "authority_id"),
        ("derivation_node", derivations, "derivation_id"),
    ):
        for row in rows:
            requirement_id = str(row.get("requirement_id") or "")
            if requirement_id not in slots or kind not in set(slots[requirement_id]["required_object_kinds"]):
                continue
            object_id = str(row.get(id_key) or "")
            if not object_id:
                raise ValueError("typed candidate object ID is required")
            if kind == "authority_node":
                screens = screens_by_authority.get(object_id, [])
                if (len(screens) != 1
                        or screens[0].get("outcome") not in AUTHORITY_CANDIDATE_OUTCOMES):
                    continue
            assignments[requirement_id].append(object_id)
    return bind_requirement_objects(plan, assignments)


def _object_index(evidence_atoms: Iterable[dict[str, Any]], authority_nodes: Iterable[dict[str, Any]],
                  derivations: Iterable[dict[str, Any]]) -> dict[str, tuple[str, dict[str, Any]]]:
    rows: dict[str, tuple[str, dict[str, Any]]] = {}
    for kind, values, id_key in (
        ("evidence_atom", evidence_atoms, "atom_id"),
        ("authority_node", authority_nodes, "authority_id"),
        ("derivation_node", derivations, "derivation_id"),
    ):
        for value in values:
            object_id = str(value.get(id_key) or "")
            if not object_id or object_id in rows:
                raise ValueError("typed knowledge object IDs must be unique")
            rows[object_id] = (kind, value)
    return rows


def assess_requirement_readiness(plan: dict[str, Any], *,
                                 evidence_atoms: Iterable[dict[str, Any]] = (),
                                 authority_nodes: Iterable[dict[str, Any]] = (),
                                 derivations: Iterable[dict[str, Any]] = (),
                                 period_domains: Iterable[dict[str, Any]] = (),
                                 authority_screens: Iterable[dict[str, Any]] = (),
                                 governed_object_ids: Iterable[str] = ()) -> dict[str, Any]:
    """Separate candidate coverage from governed executor readiness."""
    supplied_digest = plan.get("plan_digest")
    digest_basis = {key: value for key, value in plan.items() if key != "plan_digest"}
    if plan.get("schema_version") != REQUIREMENT_PLAN_SCHEMA or supplied_digest != digest(digest_basis):
        raise ValueError("requirement plan digest mismatch")
    objects = _object_index(evidence_atoms, authority_nodes, derivations)
    domains_by_requirement: dict[str, list[dict[str, Any]]] = {}
    for domain in period_domains:
        if (not isinstance(domain, dict) or domain.get("schema_version") != PERIOD_DOMAIN_SCHEMA
                or not _embedded_digest_valid(domain, "period_domain_digest")):
            raise ValueError("period domain must be digest-valid")
        domains_by_requirement.setdefault(str(domain.get("requirement_id") or ""), []).append(domain)
    screens_by_authority: dict[str, list[dict[str, Any]]] = {}
    for screen in authority_screens:
        if (not isinstance(screen, dict)
                or screen.get("schema_version") != AUTHORITY_APPLICABILITY_SCHEMA
                or not _embedded_digest_valid(screen, "screen_digest")):
            raise ValueError("authority applicability screen must be digest-valid")
        screens_by_authority.setdefault(str(screen.get("authority_id") or ""), []).append(screen)
    governed = set(governed_object_ids)
    rows: list[dict[str, Any]] = []
    for slot in plan.get("slots", []):
        object_ids = slot.get("object_ids", [])
        missing = [row for row in object_ids if row not in objects]
        wrong_kind = [row for row in object_ids
                      if row in objects and objects[row][0] not in set(slot["required_object_kinds"])]
        wrong_requirement = [row for row in object_ids if row in objects
                             and objects[row][1].get("requirement_id") != slot["slot_id"]]
        observed_periods = {str((objects[row][1].get("numeric") or {}).get("period")
                                or objects[row][1].get("period")
                                or objects[row][1].get("effective_date") or "")
                            for row in object_ids if row in objects}
        slot_domains = domains_by_requirement.get(slot["slot_id"], [])
        period_domain_invalid = slot["slot_type"] == "value_by_period" and len(slot_domains) != 1
        expected_periods = set(slot_domains[0]["periods"]) if len(slot_domains) == 1 else set()
        missing_periods = sorted(expected_periods - observed_periods)
        authority_ids = [row for row in object_ids
                         if row in objects and objects[row][0] == "authority_node"]
        qualified_authority_ids = []
        qualified_screen_ids = []
        for authority_id in authority_ids:
            screens = screens_by_authority.get(authority_id, [])
            if len(screens) == 1 and screens[0].get("outcome") in AUTHORITY_CANDIDATE_OUTCOMES:
                qualified_authority_ids.append(authority_id)
                qualified_screen_ids.append(screens[0]["screen_id"])
        unqualified_authority_ids = sorted(set(authority_ids) - set(qualified_authority_ids))
        non_authority_ids = [row for row in object_ids
                             if row in objects and objects[row][0] != "authority_node"]
        eligible_ids = [*non_authority_ids, *qualified_authority_ids]
        if missing or wrong_kind or wrong_requirement:
            state = "invalid_binding"
        elif slot["slot_type"] == "output_structure":
            state = "covered_governed"
        elif not eligible_ids:
            state = "gap"
        elif slot["slot_type"] == "value_by_period" and (period_domain_invalid or missing_periods):
            state = "gap"
        elif (set(eligible_ids).issubset(governed)
              and set(qualified_screen_ids).issubset(governed)
              and (not slot_domains or slot_domains[0]["period_domain_id"] in governed)):
            state = "covered_governed"
        else:
            state = "covered_candidate_not_governed"
        rows.append({"slot_id": slot["slot_id"], "state": state, "object_ids": object_ids,
                     "missing_object_ids": missing, "wrong_kind_object_ids": wrong_kind,
                     "wrong_requirement_object_ids": wrong_requirement,
                     "eligible_object_ids": eligible_ids,
                     "unqualified_authority_ids": unqualified_authority_ids,
                     "period_domain_ids": [row["period_domain_id"] for row in slot_domains],
                     "period_domain_invalid": period_domain_invalid,
                     "missing_periods": missing_periods})
    result = {
        "schema_version": READINESS_SCHEMA,
        "plan_digest": plan.get("plan_digest"),
        "slots": rows,
        "candidate_coverage": sum(row["state"].startswith("covered_") for row in rows),
        "governed_coverage": sum(row["state"] == "covered_governed" for row in rows),
        "executor_ready": bool(rows) and all(row["state"] == "covered_governed" for row in rows),
        "automatic_admission": False,
        "admission_authority": False,
    }
    result["readiness_digest"] = digest(result)
    return result


def build_exact_derivation(*, requirement_id: str, expression: str,
                           variables: dict[str, Any], input_bindings: dict[str, str],
                           numeric_atoms: dict[str, dict[str, Any]], output_unit: str,
                           entity: str, period: str, round_places: int = 2,
                           input_requirement_ids: dict[str, str] | None = None,
                           task_parameters: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    """Calculate only when every variable binds the same value in a numeric atom."""
    if not requirement_id or not output_unit or not entity or not period:
        raise ValueError("derivation requirement, unit, entity, and period are required")
    if not isinstance(round_places, int) or not 0 <= round_places <= 12:
        raise ValueError("derivation rounding precision is invalid")
    declared_requirements = input_requirement_ids or {name: requirement_id for name in variables}
    if set(variables) != set(input_bindings) or set(variables) != set(declared_requirements):
        raise ValueError("every derivation variable requires exactly one atom binding")
    parameters = task_parameters or {}
    inputs = {**numeric_atoms, **parameters}
    if set(numeric_atoms).intersection(parameters):
        raise ValueError("derivation input IDs must be unique across atoms and parameters")
    for name, object_id in input_bindings.items():
        atom = inputs.get(object_id)
        valid_atom = (isinstance(atom, dict) and atom.get("schema_version") == ATOM_SCHEMA
                      and _embedded_digest_valid(atom, "atom_digest"))
        valid_parameter = (isinstance(atom, dict)
                           and atom.get("schema_version") == TASK_PARAMETER_SCHEMA
                           and _embedded_digest_valid(atom, "parameter_digest")
                           and atom.get("governed_reliance_allowed") is False)
        if (not (valid_atom or valid_parameter) or not isinstance(atom.get("numeric"), dict)
                or atom.get("admission_authority") not in (None, False)):
            raise ValueError("derivation input is not a numeric evidence atom")
        if atom.get("requirement_id") != declared_requirements[name]:
            raise ValueError("derivation input disagrees with its declared source requirement")
        if _decimal_text(variables[name]) != _decimal_text(atom["numeric"].get("decimal_value")):
            raise ValueError("derivation variable disagrees with its bound atom")
    value = calculate_derivation(expression, variables, output_unit=output_unit,
                                 round_places=round_places,
                                 basis_object_ids=list(input_bindings.values()))
    value.update({"requirement_id": requirement_id,
                  "input_bindings": dict(sorted(input_bindings.items())),
                  "input_requirement_ids": dict(sorted(declared_requirements.items())),
                  "input_kinds": {name: ("task_parameter" if object_id in parameters else "evidence_atom")
                                  for name, object_id in sorted(input_bindings.items())},
                  "input_units": {name: str(inputs[object_id]["numeric"].get("unit") or "")
                                  for name, object_id in sorted(input_bindings.items())},
                  "entity": entity, "period": period,
                  "status": "not_governed_derived", "admission_authority": False,
                  "governed_reliance_allowed": False})
    value["derivation_digest"] = digest({key: row for key, row in value.items()
                                         if key != "derivation_digest"})
    return value


def validate_exact_derivation(node: dict[str, Any],
                              numeric_atoms: dict[str, dict[str, Any]],
                              task_parameters: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    """Recompute a derivation and reject result, input, or digest drift."""
    if not isinstance(node, dict) or node.get("schema_version") != DERIVATION_NODE_SCHEMA:
        raise ValueError("derivation node schema is required")
    rebuilt = build_exact_derivation(
        requirement_id=str(node.get("requirement_id") or ""),
        expression=str(node.get("expression") or ""),
        variables=dict(node.get("variables") or {}),
        input_bindings=dict(node.get("input_bindings") or {}),
        input_requirement_ids=dict(node.get("input_requirement_ids") or {}),
        numeric_atoms=numeric_atoms,
        output_unit=str(node.get("output_unit") or ""),
        entity=str(node.get("entity") or ""), period=str(node.get("period") or ""),
        round_places=node.get("round_places"),
        task_parameters=task_parameters,
    )
    required_equal = ("derivation_id", "raw_result", "result", "basis_object_ids",
                      "input_bindings", "input_requirement_ids", "input_kinds", "input_units",
                      "derivation_digest")
    if any(node.get(key) != rebuilt.get(key) for key in required_equal):
        raise ValueError("derivation result, inputs, or digest do not recompute")
    return dict(node)


def _span_covers(span: dict[str, Any], start: int, end: int) -> bool:
    return (isinstance(span.get("start"), int) and isinstance(span.get("end"), int)
            and span["start"] <= start and span["end"] >= end)


def _embedded_digest_valid(value: dict[str, Any], digest_key: str) -> bool:
    supplied = value.get(digest_key)
    basis = {key: row for key, row in value.items() if key != digest_key}
    return isinstance(supplied, str) and supplied == digest(basis)


def numeric_binding_gate(claim: dict[str, Any], *,
                         numeric_atoms: dict[str, dict[str, Any]],
                         derivations: dict[str, dict[str, Any]],
                         authority_nodes: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Require every number in a proposed claim to bind evidence, derivation, or authority."""
    statement = str(claim.get("statement") or "")
    requirement_id = str(claim.get("requirement_id") or "")
    reasons: list[str] = []
    if not statement or not requirement_id:
        reasons.append("claim_identity_or_statement_missing")
    if claim.get("status") != "unresolved":
        reasons.append("candidate_claim_must_remain_unresolved")
    if claim.get("admission") is not None or claim.get("admission_authority") not in (None, False):
        reasons.append("candidate_claim_cannot_carry_admission")
    numeric_mentions = claim.get("numeric_mentions", [])
    authority_mentions = claim.get("authority_mentions", [])
    if not isinstance(numeric_mentions, list) or not isinstance(authority_mentions, list):
        reasons.append("claim_mentions_must_be_lists")
        numeric_mentions, authority_mentions = [], []

    for mention in numeric_mentions:
        if not isinstance(mention, dict):
            reasons.append("invalid_numeric_mention")
            continue
        object_id = str(mention.get("object_id") or "")
        obj = numeric_atoms.get(object_id) or derivations.get(object_id)
        start, end = mention.get("start"), mention.get("end")
        valid_atom = (object_id in numeric_atoms
                      and obj.get("schema_version") == ATOM_SCHEMA
                      and _embedded_digest_valid(obj, "atom_digest")
                      and obj.get("admission_authority") in (None, False))
        try:
            valid_derivation = (object_id in derivations
                                and validate_exact_derivation(obj, numeric_atoms) is not None
                                and obj.get("admission_authority") is False)
        except ValueError:
            valid_derivation = False
        if (obj is None or not (valid_atom or valid_derivation)
                or not isinstance(start, int) or not isinstance(end, int)
                or not 0 <= start < end <= len(statement)):
            reasons.append("invalid_numeric_mention")
            continue
        raw = statement[start:end]
        expected = (obj.get("numeric", {}).get("decimal_value")
                    if object_id in numeric_atoms else obj.get("result"))
        if normalize_numeric_text(raw) != _decimal_text(expected):
            reasons.append("numeric_mention_value_mismatch")
        if obj.get("requirement_id") != requirement_id:
            reasons.append("numeric_mention_requirement_mismatch")

    for mention in authority_mentions:
        if not isinstance(mention, dict):
            reasons.append("invalid_authority_mention")
            continue
        object_id = str(mention.get("object_id") or "")
        obj = authority_nodes.get(object_id)
        start, end = mention.get("start"), mention.get("end")
        valid_authority = (obj is not None and obj.get("schema_version") == AUTHORITY_NODE_SCHEMA
                           and _embedded_digest_valid(obj, "authority_digest")
                           and obj.get("normative_authority_confirmed") is False
                           and obj.get("admission_authority") is False)
        if (not valid_authority or not isinstance(start, int) or not isinstance(end, int)
                or not 0 <= start < end <= len(statement)):
            reasons.append("invalid_authority_mention")
            continue
        if obj.get("requirement_id") != requirement_id or str(obj.get("citation") or "") not in statement[start:end]:
            reasons.append("authority_mention_binding_mismatch")

    candidates = extract_numeric_candidates(statement)
    uncovered = []
    for candidate in candidates:
        covered = any(_span_covers(row, candidate["start"], candidate["end"])
                      for row in numeric_mentions + authority_mentions if isinstance(row, dict))
        if not covered:
            uncovered.append(candidate)
    if uncovered:
        reasons.append("unbound_material_number")
    reasons = sorted(set(reasons))
    result = {
        "schema_version": NUMERIC_BINDING_GATE_SCHEMA,
        "claim_id": claim.get("id"),
        "requirement_id": requirement_id,
        "state": "claimable" if not reasons else "partial",
        "proposer_allowed": not reasons,
        "reasons": reasons,
        "numeric_candidate_count": len(candidates),
        "unbound_candidates": uncovered,
        "automatic_admission": False,
        "admission_authority": False,
    }
    result["gate_digest"] = digest(result)
    return result

#!/usr/bin/env python3
"""Quality-first discovery and typed working-set objects for private APEX Legal.

The module is intentionally read-only. Retrieved evidence, authority candidates,
and deterministic derivations do not acquire admission or matter authority.
"""
from __future__ import annotations

import ast
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any

from run_claim_construction_private import SectionIndex, digest


EVIDENCE_ATOM_SCHEMA = "proofpress/evidence-atom/v1"
AUTHORITY_NODE_SCHEMA = "proofpress/authority-node/v1"
DERIVATION_NODE_SCHEMA = "proofpress/derivation-node/v1"
OPEN_DISCOVERY_STATE_TOKEN_UPPER_BOUND = 96_000
OPEN_DISCOVERY_WALL_SECONDS = 1_800
DEFAULT_RESULT_PAGE_SIZE = 20

OPEN_DISCOVERY_DECISION_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["action", "reason"],
    "properties": {
        "action": {"type": "string", "enum": [
            "traverse_graph", "search_gap", "search_authority",
            "get_evidence_atoms", "get_authority_nodes", "get_derivation_nodes",
            "create_evidence_atom", "create_authority_node", "calculate", "answer"]},
        "query": {"type": "string"},
        "seed_claim_ids": {"type": "array", "items": {"type": "string"}},
        "relation_types": {"type": "array", "items": {"type": "string"}},
        "object_ids": {"type": "array", "items": {"type": "string"}},
        "offset": {"type": "integer", "minimum": 0},
        "page_size": {"type": "integer", "minimum": 1},
        "expression": {"type": "string"},
        "variables": {"type": "object", "additionalProperties": {"type": "number"}},
        "basis_object_ids": {"type": "array", "items": {"type": "string"}},
        "receipt_digest": {"type": "string"},
        "requirement_id": {"type": "string"},
        "subject": {"type": "string"},
        "predicate": {"type": "string"},
        "value": {"type": "string"},
        "exact_excerpt": {"type": "string"},
        "citation": {"type": "string"},
        "proposition": {"type": "string"},
        "jurisdiction": {"type": "string"},
        "effective_date": {"type": "string"},
        "output_unit": {"type": "string"},
        "round_places": {"type": "integer", "minimum": 0, "maximum": 12},
        "reason": {"type": "string", "maxLength": 640},
    },
}


def task_knowledge_objects(graph: dict[str, Any]) -> dict[str, Any]:
    """Project typed objects already present in construction without inventing them."""
    construction = graph.get("construction", {})
    atoms = [row for row in construction.get("evidence_atoms", [])
             if isinstance(row, dict) and row.get("schema_version") == EVIDENCE_ATOM_SCHEMA]
    authorities = [row for row in construction.get("authority_nodes", [])
                   if isinstance(row, dict) and row.get("schema_version") == AUTHORITY_NODE_SCHEMA]
    derivations = [row for row in construction.get("derivation_nodes", [])
                   if isinstance(row, dict) and row.get("schema_version") == DERIVATION_NODE_SCHEMA]
    return {
        "schema_version": "proofpress/task-knowledge-objects/v1",
        "task_id": graph.get("task", {}).get("task_id"),
        "evidence_atoms": atoms,
        "authority_nodes": authorities,
        "derivation_nodes": derivations,
        "availability": {
            "evidence_atom_count": len(atoms),
            "authority_node_count": len(authorities),
            "derivation_node_count": len(derivations),
        },
        "admission_authority": False,
    }


def select_objects(objects: dict[str, Any], kind: str, object_ids: list[str] | None = None,
                   query: str = "") -> dict[str, Any]:
    """Return typed objects by ID or lexical query; selection never changes status."""
    rows = [row for row in objects.get(kind, []) if isinstance(row, dict)]
    wanted = {str(value) for value in (object_ids or []) if str(value)}
    if wanted:
        def row_id(row: dict[str, Any]) -> str:
            return str(row.get("atom_id") or row.get("authority_id") or row.get("derivation_id") or "")
        rows = [row for row in rows if row_id(row) in wanted]
    elif query.strip():
        terms = {term.lower() for term in query.split() if term.strip()}
        rows = [row for row in rows if terms & set(str(row).lower().split())]
    return {"schema_version": "proofpress/typed-object-disclosure/v1", "object_kind": kind,
            "objects": rows, "object_count": len(rows), "admission_authority": False,
            "governed_reliance_allowed": False}


def paged_bm25(index: SectionIndex, query: str, *, offset: int = 0,
               page_size: int = DEFAULT_RESULT_PAGE_SIZE,
               authority_candidate: bool = False) -> dict[str, Any]:
    """Return a requested result page; callers may request more pages without a lifetime cap."""
    if not isinstance(query, str) or not query.strip():
        raise ValueError("BM25 discovery requires a non-empty query")
    if offset < 0 or page_size < 1:
        raise ValueError("BM25 pagination values are invalid")
    hits = index.search(query, max_documents=max(1, len(index.doc_meta)),
                        max_sections=offset + page_size)
    page = hits[offset:offset + page_size]
    candidates = []
    for hit in page:
        section, source = hit["section"], hit["section"]["source"]
        evidence = {"quote": section.get("text", ""), "locator": {
            "kind": "section_span", "section_id": section["id"],
            "section_digest": section["text_digest"], "page_start": section["page_start"],
            "page_end": section["page_end"]}}
        row = {
            "status": "not_governed",
            "object_kind": "authority_candidate" if authority_candidate else "evidence_candidate",
            "source": {"uri": source["uri"], "content_digest": source["content_digest"],
                       "media_type": source["media_type"]},
            "evidence": evidence,
            "retrieval": {"adapter": "bm25-open-discovery/v1", "rank": hit["rank"],
                          "score": round(hit["score"], 8), "query_digest": digest(query),
                          "result_offset": offset, "requested_page_size": page_size,
                          "section_heading": section.get("heading")},
            "required_action": "import_evidence_then_propose_evaluate_judge_review",
            "admission_authority": False,
        }
        row["receipt_digest"] = digest(row)
        candidates.append(row)
    return {"schema_version": "proofpress/open-discovery-results/v1",
            "query_digest": digest(query), "offset": offset, "requested_page_size": page_size,
            "returned_count": len(candidates), "next_offset": offset + len(candidates),
            "has_more": len(hits) > offset + len(candidates), "candidate_evidence": candidates,
            "admission_authority": False, "governed_reliance_allowed": False}


def bind_evidence_atom(payload: dict[str, Any], visible_receipts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Bind a candidate atom to an exact visible receipt substring without admitting it."""
    receipt_digest = str(payload.get("receipt_digest") or "")
    receipt = visible_receipts.get(receipt_digest)
    if receipt is None:
        raise ValueError("evidence atom receipt is not visible")
    excerpt = str(payload.get("exact_excerpt") or "")
    quote = str(receipt.get("evidence", {}).get("quote") or "")
    required = {key: str(payload.get(key) or "").strip()
                for key in ("requirement_id", "subject", "predicate", "value")}
    if not excerpt.strip() or excerpt not in quote or any(not value for value in required.values()):
        raise ValueError("evidence atom lacks an exact visible binding")
    basis = {**required, "receipt_digest": receipt_digest, "exact_excerpt": excerpt,
             "locator": receipt.get("evidence", {}).get("locator"),
             "source": receipt.get("source")}
    return {"schema_version": EVIDENCE_ATOM_SCHEMA,
            "atom_id": "atom_" + digest(basis).split(":", 1)[1][:20], **basis,
            "support_mode": "explicit", "status": "not_governed_candidate",
            "required_action": "propose_evaluate_judge_review", "admission_authority": False,
            "governed_reliance_allowed": False}


def bind_authority_node(payload: dict[str, Any], visible_receipts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Bind a candidate authority proposition to exact retrieved text without granting authority."""
    receipt_digest = str(payload.get("receipt_digest") or "")
    receipt = visible_receipts.get(receipt_digest)
    if receipt is None:
        raise ValueError("authority receipt is not visible")
    excerpt = str(payload.get("exact_excerpt") or "")
    quote = str(receipt.get("evidence", {}).get("quote") or "")
    required = {key: str(payload.get(key) or "").strip()
                for key in ("citation", "proposition", "jurisdiction")}
    if not excerpt.strip() or excerpt not in quote or any(not value for value in required.values()):
        raise ValueError("authority node lacks an exact visible binding")
    basis = {**required, "effective_date": str(payload.get("effective_date") or "unknown"),
             "receipt_digest": receipt_digest, "exact_excerpt": excerpt,
             "locator": receipt.get("evidence", {}).get("locator"), "source": receipt.get("source")}
    return {"schema_version": AUTHORITY_NODE_SCHEMA,
            "authority_id": "authority_" + digest(basis).split(":", 1)[1][:20], **basis,
            "status": "not_governed_candidate", "normative_authority_confirmed": False,
            "required_action": "evaluate_judge_review", "admission_authority": False,
            "governed_reliance_allowed": False}


def _decimal(value: Any) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("calculation variable is not decimal-compatible") from exc


def _evaluate(node: ast.AST, variables: dict[str, Decimal]) -> Decimal:
    if isinstance(node, ast.Expression):
        return _evaluate(node.body, variables)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return _decimal(node.value)
    if isinstance(node, ast.Name) and node.id in variables:
        return variables[node.id]
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _evaluate(node.operand, variables)
        return value if isinstance(node.op, ast.UAdd) else -value
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
        left, right = _evaluate(node.left, variables), _evaluate(node.right, variables)
        if isinstance(node.op, ast.Add): return left + right
        if isinstance(node.op, ast.Sub): return left - right
        if isinstance(node.op, ast.Mult): return left * right
        if right == 0: raise ValueError("division by zero")
        return left / right
    raise ValueError("calculation expression uses an unsupported operation")


def calculate_derivation(expression: str, variables: dict[str, Any], *, output_unit: str = "",
                         round_places: int = 2, basis_object_ids: list[str] | None = None) -> dict[str, Any]:
    """Create a deterministic, non-admitted derivation receipt."""
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("calculation expression is required")
    if not isinstance(variables, dict) or not variables:
        raise ValueError("calculation variables are required")
    decimals = {str(key): _decimal(value) for key, value in variables.items()}
    try:
        parsed = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError("calculation expression is invalid") from exc
    raw = _evaluate(parsed, decimals)
    quantum = Decimal(1).scaleb(-round_places)
    rounded = raw.quantize(quantum, rounding=ROUND_HALF_UP)
    basis = {"expression": expression, "variables": {key: str(value) for key, value in decimals.items()},
             "basis_object_ids": list(dict.fromkeys(basis_object_ids or [])),
             "output_unit": output_unit, "round_places": round_places}
    return {"schema_version": DERIVATION_NODE_SCHEMA,
            "derivation_id": "derivation_" + digest(basis).split(":", 1)[1][:20],
            **basis, "raw_result": str(raw), "result": str(rounded),
            "status": "not_governed_derived", "deterministic": True,
            "derivation_digest": digest({**basis, "result": str(rounded)}),
            "required_action": "bind_governed_inputs_then_evaluate_judge_review",
            "admission_authority": False, "governed_reliance_allowed": False}

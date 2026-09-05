"""Stateless Streamable HTTP MCP surface over the hosted control plane."""
from __future__ import annotations

import json
import re
from typing import Any

from proofpress.kernel import operations as knowledge


PROTOCOL_VERSION = "2025-06-18"
SERVER_INFO = {"name": "Proofpress", "version": "0.6.0a1"}
EVIDENCE_ID_PATTERN = r"^evd_[0-9a-f]{16}$"
SHA256_PATTERN = r"^sha256:[0-9a-f]{64}$"

RETRIEVAL_EVIDENCE_SCHEMA = {
    "type": "object",
    "description": (
        "A proofpress/retrieval-evidence/v1 envelope. Use profile=experiment "
        "only for an experiment-profile payload."
    ),
    "properties": {
        "schema_version": {
            "type": "string", "const": "proofpress/retrieval-evidence/v1",
        },
        "source": {
            "type": "object",
            "properties": {
                "uri": {"type": "string", "minLength": 1},
                "content_digest": {"type": "string", "pattern": SHA256_PATTERN},
                "media_type": {"type": "string", "minLength": 1},
            },
            "required": ["uri", "content_digest"],
        },
        "evidence": {
            "type": "object",
            "properties": {
                "quote": {"type": "string", "minLength": 1},
                "locator": {
                    "type": "object",
                    "description": "A text_span, page_span, or section_span locator bound to the source.",
                },
            },
            "required": ["quote", "locator"],
        },
        "retrieval": {
            "type": "object",
            "properties": {
                "adapter": {"type": "string", "minLength": 1},
                "version": {"type": "string", "minLength": 1},
                "query": {"type": "string", "minLength": 1},
                "config_digest": {"type": "string", "pattern": SHA256_PATTERN},
                "selection_reason": {"type": "string", "minLength": 1},
            },
            "required": ["adapter", "version", "query", "config_digest"],
        },
    },
    "required": ["schema_version", "source", "evidence", "retrieval"],
}


TOOLS = [
    {"name": "proofpress_capabilities", "description": "Describe the safe agent surface and authenticated principal.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "proofpress_submit_evidence", "description": "Submit one bounded retrieval or experiment evidence envelope. With no profile, payload must use proofpress/retrieval-evidence/v1. The only supported evidence profile is experiment.", "inputSchema": {"type": "object", "properties": {"payload": {"type": "object"}, "profile": {"type": "string", "enum": ["experiment"], "description": "Omit for retrieval evidence; use experiment only for a valid experiment-profile payload."}, "idempotency_key": {"type": "string"}}, "required": ["payload"], "allOf": [{"if": {"not": {"required": ["profile"]}}, "then": {"properties": {"payload": RETRIEVAL_EVIDENCE_SCHEMA}}}]}},
    {"name": "proofpress_propose_conclusion", "description": "Propose an evidence-bound conclusion; this never approves it. evidence_refs must be evd_ IDs returned by proofpress_submit_evidence. Scope is an optional legacy exact filter; use applicability for a discoverable reuse card. Set reproposal_of only when correcting a rejected conclusion; the rejection remains immutable and the new candidate needs review.", "inputSchema": {"type": "object", "properties": {"statement": {"type": "string", "minLength": 1}, "evidence_refs": {"type": "array", "minItems": 1, "items": {"type": "string", "pattern": EVIDENCE_ID_PATTERN, "description": "An evd_ ID returned by proofpress_submit_evidence."}}, "scope": {"type": "string", "minLength": 1}, "applicability": {"type": "object", "description": "Discovery card: title, description, when_relevant, keywords, validity_conditions."}, "reproposal_of": {"type": "string", "pattern": "^knw_[A-Za-z0-9]+$", "description": "Rejected conclusion this new candidate corrects."}, "expires_at": {"type": "string"}, "artifact_refs": {"type": "array", "items": {"type": "string"}}, "qualifiers": {"type": "object"}, "profile": {"type": "string", "enum": ["legal", "repo", "experiment"]}, "idempotency_key": {"type": "string"}}, "required": ["statement", "evidence_refs"]}},
    {"name": "proofpress_discover_context", "description": "List only admitted, current, actor-eligible context cards. Use task to rank semantic relevance; visibility is still enforced before discovery.", "inputSchema": {"type": "object", "properties": {"task": {"type": "string"}, "limit": {"type": "integer", "minimum": 1, "maximum": 100}}}},
    {"name": "proofpress_get_context", "description": "Return admitted, current context eligible for this agent. Scope is an optional legacy exact filter, not required for discovery.", "inputSchema": {"type": "object", "properties": {"scope": {"type": "string"}, "task": {"type": "string"}}}},
    {"name": "proofpress_get_graph", "description": "Return the bounded evidence, conclusion, review, and governance graph for a scope.", "inputSchema": {"type": "object", "properties": {"scope": {"type": "string"}}}},
    {"name": "proofpress_traverse_graph", "description": "Traverse admitted conclusion relations from seed conclusions with server-enforced eligibility limits.", "inputSchema": {"type": "object", "properties": {"seed_ids": {"type": "array", "items": {"type": "string"}}, "scope": {"type": "string"}, "task": {"type": "string"}, "max_depth": {"type": "integer", "minimum": 0}, "max_claims": {"type": "integer", "minimum": 1}}, "required": ["seed_ids"]}},
    {"name": "proofpress_get_lineage", "description": "Trace one conclusion back through all bound and derived evidence to its source records.", "inputSchema": {"type": "object", "properties": {"conclusion_id": {"type": "string"}}, "required": ["conclusion_id"]}},
    {"name": "proofpress_get_review_summary", "description": "Read review-state counts without making an authority decision.", "inputSchema": {"type": "object", "properties": {"scope": {"type": "string"}}}},
    {"name": "proofpress_get_review_receipt", "description": "Read evidence, checks, advice, state, and authority receipt for a conclusion.", "inputSchema": {"type": "object", "properties": {"conclusion_id": {"type": "string"}}, "required": ["conclusion_id"]}},
    {"name": "proofpress_get_review_link", "description": "Create a browser link for the human owner; this tool cannot approve.", "inputSchema": {"type": "object", "properties": {"conclusion_id": {"type": "string"}}, "required": ["conclusion_id"]}},
]


def _request(operation: str, parameters: dict[str, Any], args: dict[str, Any]):
    request = {"schema_version": knowledge.LOCAL_OPERATION_SCHEMA,
               "operation": operation, "parameters": parameters}
    if args.get("idempotency_key"):
        request["idempotency_key"] = args["idempotency_key"]
    return request


def _execute(control, context, operation, parameters, args=None):
    envelope = control.execute_as(
        context, _request(operation, parameters, args or {}))
    if not envelope.get("ok"):
        raise ValueError(envelope.get("error", {}).get("message", "operation failed"))
    return envelope["result"]


def _lineage(control, context, conclusion_id: str):
    receipt = _execute(control, context, "review.receipt",
                       {"conclusion_id": conclusion_id, "actor": "server-derived"})
    graph = _execute(control, context, "graph.get",
                     {"scope": receipt["conclusion"].get("scope"), "actor": "server-derived"})
    incoming: dict[str, list[dict[str, Any]]] = {}
    for edge in graph.get("edges", []):
        incoming.setdefault(edge["to"], []).append(edge)
    wanted = {conclusion_id}
    pending = [conclusion_id]
    lineage_edges = []
    while pending:
        current = pending.pop()
        for edge in incoming.get(current, []):
            if edge.get("type") not in {"supports", "derived_from", "bound_as",
                                        "re_proposed_as"}:
                continue
            lineage_edges.append(edge)
            if edge["from"] not in wanted:
                wanted.add(edge["from"])
                pending.append(edge["from"])
    nodes = [row for row in graph.get("nodes", []) if row["id"] in wanted]
    return {"conclusion_id": conclusion_id, "state": receipt["state"],
            "scope": receipt["conclusion"].get("scope"),
            "nodes": nodes, "edges": lineage_edges,
            "evidence": receipt.get("evidence", []),
            "ledger_head": receipt.get("ledger_head")}


def call_tool(control, context, name: str, args: dict[str, Any], base_url: str):
    if name == "proofpress_capabilities":
        return _execute(control, context, "capabilities.get", {})
    if name == "proofpress_submit_evidence":
        profile = args.get("profile")
        if profile not in {None, "experiment"}:
            raise ValueError(
                "unsupported evidence profile: " + str(profile) +
                "; omit profile for proofpress/retrieval-evidence/v1 or use experiment")
        return _execute(control, context, "evidence.submit", {
            "payload": args["payload"], "profile": profile}, args)
    if name == "proofpress_propose_conclusion":
        evidence_refs = args.get("evidence_refs")
        if (not isinstance(evidence_refs, list) or not evidence_refs or
                any(not isinstance(ref, str) or
                    re.fullmatch(EVIDENCE_ID_PATTERN, ref) is None
                    for ref in evidence_refs)):
            raise ValueError(
                "evidence_refs must contain evd_ IDs returned by "
                "proofpress_submit_evidence; source and artifact URLs are not evidence IDs")
        parameters = {key: args.get(key) for key in (
            "statement", "evidence_refs", "scope", "expires_at",
            "artifact_refs", "applicability", "reproposal_of", "qualifiers", "profile")}
        parameters["proposer"] = "server-derived"
        return _execute(control, context, "conclusion.propose", parameters, args)
    if name == "proofpress_discover_context":
        return _execute(control, context, "context.discover", {
            "actor": "server-derived", "task": args.get("task"),
            "limit": args.get("limit", 24)})
    if name == "proofpress_get_context":
        return _execute(control, context, "context.get", {
            "scope": args.get("scope"), "task": args.get("task"),
            "actor": "server-derived", "include_blocked_statements": False})
    if name == "proofpress_get_graph":
        return _execute(control, context, "graph.get", {
            "scope": args.get("scope"), "actor": "server-derived"})
    if name == "proofpress_traverse_graph":
        return _execute(control, context, "graph.traverse", {
            "seed_ids": args["seed_ids"], "scope": args.get("scope"),
            "actor": "server-derived", "task": args.get("task"),
            "max_depth": args.get("max_depth", 2),
            "max_claims": args.get("max_claims", 48), "state": "admitted"})
    if name == "proofpress_get_lineage":
        return _lineage(control, context, args["conclusion_id"])
    if name == "proofpress_get_review_summary":
        return _execute(control, context, "review.summary", {
            "scope": args.get("scope"), "actor": "server-derived"})
    if name == "proofpress_get_review_receipt":
        return _execute(control, context, "review.receipt", {
            "conclusion_id": args["conclusion_id"], "actor": "server-derived"})
    if name == "proofpress_get_review_link":
        conclusion_id = args["conclusion_id"]
        receipt = _execute(control, context, "review.receipt", {
            "conclusion_id": conclusion_id, "actor": "server-derived"})
        return {"conclusion_id": conclusion_id, "state": receipt["state"],
                "requires_human_owner": True,
                "url": base_url.rstrip("/") + "/review?conclusion_id=" + conclusion_id}
    raise ValueError("unknown Proofpress MCP tool")


def handle_rpc(control, context, request: dict[str, Any], base_url: str):
    request_id = request.get("id")
    method = request.get("method")
    if request_id is None:
        return None
    try:
        if method == "initialize":
            result = {"protocolVersion": PROTOCOL_VERSION,
                      "capabilities": {"tools": {"listChanged": False}},
                      "serverInfo": SERVER_INFO,
                      "instructions": "Submit bounded evidence, propose conclusions, and retrieve only governed context. Human Approval is never exposed."}
        elif method == "ping":
            result = {}
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            params = request.get("params") or {}
            value = call_tool(control, context, params.get("name", ""),
                              params.get("arguments") or {}, base_url)
            result = {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False)}],
                      "structuredContent": value, "isError": False}
        else:
            return {"jsonrpc": "2.0", "id": request_id,
                    "error": {"code": -32601, "message": "Method not found"}}
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    except (KeyError, TypeError, ValueError) as exc:
        error = {"ok": False, "error": {
            "code": "invalid_tool_request", "message": str(exc)}}
        return {"jsonrpc": "2.0", "id": request_id,
                "result": {"content": [{"type": "text", "text": json.dumps(error)}],
                           "structuredContent": error,
                           "isError": True}}

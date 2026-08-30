#!/usr/bin/env python3
"""Bounded executor-driven disclosure tools for the private legal evaluation."""
from __future__ import annotations

from typing import Any, Callable

import proofpress_knowledge as knowledge
from run_claim_construction_private import SectionIndex, digest
from run_gap_retrieval_private import bm25_receipts

MAX_AGENT_TOOL_CALLS = 3
MAX_AGENT_RESULTS_PER_CALL = 5

TOOL_DECISION_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["action", "query", "seed_claim_ids", "relation_types", "reason"],
    "properties": {
        "action": {"type": "string", "enum": ["traverse_graph", "search_gap", "answer"]},
        "query": {"type": "string"},
        "seed_claim_ids": {"type": "array", "maxItems": MAX_AGENT_RESULTS_PER_CALL,
                           "items": {"type": "string"}},
        "relation_types": {"type": "array", "maxItems": MAX_AGENT_RESULTS_PER_CALL,
                           "items": {"type": "string"}},
        "reason": {"type": "string", "maxLength": 320},
    },
}


def compact_tool_result(value: dict[str, Any]) -> dict[str, Any]:
    """Expose enough evidence to reason without forwarding unbounded ledger records."""
    if "governed_context" in value:
        governed = [{key: row.get(key) for key in ("id", "statement", "scope", "qualifiers", "digest")
                     if key in row}
                    for row in value.get("governed_context", [])[:MAX_AGENT_RESULTS_PER_CALL]
                    if isinstance(row, dict)]
        relations = value.get("traversal", {}).get("relations", []) if isinstance(value.get("traversal"), dict) else []
        return {"coverage": value.get("coverage"), "governed_context": governed,
                "relations": relations[:MAX_AGENT_RESULTS_PER_CALL], "gaps": value.get("gaps", []),
                "blocked_count": len(value.get("blocked", [])),
                "admission_authority": False, "governed_reliance_allowed": True}
    candidates = []
    for row in value.get("candidate_evidence", [])[:MAX_AGENT_RESULTS_PER_CALL]:
        evidence = dict(row.get("evidence") or {})
        quote = evidence.get("quote")
        if isinstance(quote, str) and len(quote) > 1600:
            evidence["quote"] = quote[:1600] + "…"
            evidence["quote_truncated"] = True
        candidates.append({**row, "evidence": evidence})
    return {"query_digest": value.get("query_digest"), "candidate_evidence": candidates,
            "candidate_count": len(candidates), "admission_authority": False,
            "governed_reliance_allowed": False}


def initial_context(query: str, scope: str) -> dict[str, Any]:
    """Return a small governed seed without invoking discovery."""
    return knowledge.disclose_v1(query, "agent:workflow-executor", scope,
                                 max_claims=1, max_depth=0, max_discovered=0)


def traverse_graph(query: str, scope: str, seed_claim_ids: list[str],
                   relation_types: list[str]) -> dict[str, Any]:
    """Execute a read-only, admitted-only traversal from visible seed claims."""
    bounded_seeds = list(dict.fromkeys(seed_claim_ids))[:MAX_AGENT_RESULTS_PER_CALL]
    if not bounded_seeds:
        raise ValueError("traverse_graph requires at least one seed claim")
    tool_query = query.strip()
    if relation_types:
        tool_query += "\nRelevant relation types: " + ", ".join(relation_types[:MAX_AGENT_RESULTS_PER_CALL])
    return knowledge.disclose_v1(tool_query, "agent:workflow-executor", scope,
                                 seeds=bounded_seeds, max_claims=MAX_AGENT_RESULTS_PER_CALL,
                                 max_depth=2, max_discovered=0)


def search_gap(index: SectionIndex, query: str) -> dict[str, Any]:
    """Return bounded candidate evidence; retrieval never upgrades governance state."""
    if not isinstance(query, str) or not query.strip():
        raise ValueError("search_gap requires a non-empty query")
    candidates = []
    for row in bm25_receipts(index, query)[:MAX_AGENT_RESULTS_PER_CALL]:
        candidates.append({
            "status": "not_governed",
            "source": row.get("source"),
            "evidence": row.get("evidence"),
            "retrieval": row.get("retrieval"),
            "receipt_digest": digest(row),
            "required_action": "import_evidence_then_propose_evaluate_judge_review",
        })
    return {"query_digest": digest(query), "candidate_evidence": candidates,
            "candidate_count": len(candidates), "admission_authority": False}


def run_agentic_disclosure(
    *, query: str, scope: str, index: SectionIndex,
    decide: Callable[[dict[str, Any]], dict[str, Any]],
) -> dict[str, Any]:
    """Let an executor choose bounded tools while the host enforces every boundary."""
    seed = compact_tool_result(initial_context(query, scope))
    state: dict[str, Any] = {"ask": query, "initial_context": seed, "tool_results": [],
                             "limits": {"max_tool_calls": MAX_AGENT_TOOL_CALLS,
                                        "max_results_per_call": MAX_AGENT_RESULTS_PER_CALL}}
    trace = []
    stop_reason = "tool_budget_exhausted"
    for call_index in range(MAX_AGENT_TOOL_CALLS + 1):
        decision = decide(state)
        action = decision.get("action")
        trace_row = {"decision_index": call_index, "action": action,
                     "query_digest": digest(str(decision.get("query", ""))),
                     "seed_claim_count": len(decision.get("seed_claim_ids", [])),
                     "relation_type_count": len(decision.get("relation_types", [])),
                     "reason_digest": digest(str(decision.get("reason", "")))}
        if action == "answer":
            trace.append({**trace_row, "status": "accepted"})
            stop_reason = "executor_ready"
            break
        if call_index >= MAX_AGENT_TOOL_CALLS:
            trace.append({**trace_row, "status": "blocked", "reason": "tool_budget_exhausted",
                          "next_action": "finalize_without_more_tools"})
            stop_reason = "executor_ready_forced_finalization"
            break
        try:
            if action == "traverse_graph":
                visible_ids = {str(row.get("id")) for row in state["initial_context"].get("governed_context", [])}
                for prior in state["tool_results"]:
                    visible_ids.update(str(row.get("id")) for row in
                                       prior.get("result", {}).get("governed_context", []))
                requested_seeds = list(decision.get("seed_claim_ids", []))
                if not requested_seeds or any(seed_id not in visible_ids for seed_id in requested_seeds):
                    raise ValueError("traverse_graph seed was not disclosed to the executor")
                result = traverse_graph(str(decision.get("query", "")), scope,
                                        requested_seeds,
                                        list(decision.get("relation_types", [])))
            elif action == "search_gap":
                result = search_gap(index, str(decision.get("query", "")))
            else:
                raise ValueError("unknown agentic disclosure action")
        except (TypeError, ValueError) as exc:
            trace.append({**trace_row, "status": "blocked", "reason": type(exc).__name__})
            state["tool_results"].append({"action": action, "status": "blocked",
                                          "reason": type(exc).__name__})
            continue
        state["tool_results"].append({"action": action, "status": "ok",
                                      "result": compact_tool_result(result)})
        trace.append({**trace_row, "status": "ok", "result_digest": digest(result)})
    return {"state": state, "trace": trace, "tool_call_count": sum(
                row.get("status") == "ok" and row.get("action") != "answer" for row in trace),
            "stop_reason": stop_reason,
            "used_traverse_graph": any(row.get("action") == "traverse_graph" and row.get("status") == "ok" for row in trace),
            "used_search_gap": any(row.get("action") == "search_gap" and row.get("status") == "ok" for row in trace)}

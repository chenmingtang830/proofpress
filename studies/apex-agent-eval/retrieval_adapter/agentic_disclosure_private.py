#!/usr/bin/env python3
"""Bounded executor-driven disclosure tools for the private legal evaluation."""
from __future__ import annotations

import json
import time
from typing import Any, Callable

import proofpress_knowledge as knowledge
from run_claim_construction_private import SectionIndex, digest
from run_gap_retrieval_private import bm25_receipts
from open_discovery_private import (DEFAULT_RESULT_PAGE_SIZE,
                                    OPEN_DISCOVERY_STATE_TOKEN_UPPER_BOUND,
                                    OPEN_DISCOVERY_WALL_SECONDS, bind_authority_node,
                                    bind_evidence_atom, calculate_derivation, paged_bm25,
                                    select_objects, task_knowledge_objects)

MAX_AGENT_TOOL_CALLS = 3
MAX_AGENT_RESULTS_PER_CALL = 5
OPEN_LOOP_INITIAL_CLAIMS = 5
OPEN_LOOP_INITIAL_DEPTH = 1
OPEN_LOOP_STATE_TOKEN_UPPER_BOUND = 24_000
STATIC_OPEN_LOOP_STATE_TOKEN_UPPER_BOUND = 32_000
OPEN_LOOP_WALL_SECONDS = 600

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


def open_loop_initial_context(query: str, scope: str) -> dict[str, Any]:
    """Return a useful governed working set before executor-driven expansion."""
    return knowledge.disclose_v1(query, "agent:workflow-executor", scope,
                                 max_claims=OPEN_LOOP_INITIAL_CLAIMS,
                                 max_depth=OPEN_LOOP_INITIAL_DEPTH, max_discovered=0)


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
        try:
            decision = decide(state)
        except RuntimeError:
            trace.append({"decision_index": call_index, "action": "decision_provider",
                          "status": "blocked", "reason": "fixed_route_attempts_exhausted"})
            stop_reason = "executor_ready_decision_provider_guard_finalization"
            break
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


def state_token_upper_bound(value: dict[str, Any]) -> int:
    return max(1, len(json.dumps(value, ensure_ascii=False, sort_keys=True)) // 4)


def visible_governed_claim_ids(value: Any) -> set[str]:
    """Collect only claim IDs already present in the executor-visible state."""
    visible: set[str] = set()
    if isinstance(value, dict):
        governed = value.get("governed_context", [])
        if isinstance(governed, list):
            visible.update(str(row.get("id")) for row in governed
                           if isinstance(row, dict) and row.get("id") is not None)
        for child in value.values():
            visible.update(visible_governed_claim_ids(child))
    elif isinstance(value, list):
        for child in value:
            visible.update(visible_governed_claim_ids(child))
    return visible


def visible_candidate_receipts(value: Any) -> dict[str, dict[str, Any]]:
    """Collect only retrieval receipts actually present in executor-visible state."""
    output: dict[str, dict[str, Any]] = {}
    if isinstance(value, dict):
        if value.get("receipt_digest") and isinstance(value.get("evidence"), dict):
            output[str(value["receipt_digest"])] = value
        for child in value.values():
            output.update(visible_candidate_receipts(child))
    elif isinstance(value, list):
        for child in value:
            output.update(visible_candidate_receipts(child))
    return output


def run_open_loop_agentic_disclosure(
    *, query: str, scope: str, index: SectionIndex,
    decide: Callable[[dict[str, Any]], dict[str, Any]],
    initial_state_context: Any | None = None,
    state_token_limit: int = OPEN_LOOP_STATE_TOKEN_UPPER_BOUND,
) -> dict[str, Any]:
    """Run executor-directed tools without a fixed tool-call-count limit.

    Termination is answer-driven. The host still fails closed on a repeated
    identical decision, the configured state boundary, or elapsed wall time.
    None of those guards is a tool-call-count budget.
    """
    seed = (compact_tool_result(open_loop_initial_context(query, scope))
            if initial_state_context is None else initial_state_context)
    state: dict[str, Any] = {"ask": query, "initial_context": seed, "tool_results": [],
                             "limits": {"max_tool_calls": None,
                                        "max_results_per_call": MAX_AGENT_RESULTS_PER_CALL,
                                        "state_token_upper_bound": state_token_limit,
                                        "wall_seconds": OPEN_LOOP_WALL_SECONDS}}
    trace: list[dict[str, Any]] = []
    seen_decisions: set[str] = set()
    started = time.monotonic()
    stop_reason = "executor_ready"
    decision_index = 0
    while True:
        if time.monotonic() - started >= OPEN_LOOP_WALL_SECONDS:
            stop_reason = "executor_ready_wall_guard_finalization"
            break
        if state_token_upper_bound(state) >= state_token_limit:
            stop_reason = "executor_ready_context_guard_finalization"
            break
        try:
            decision = decide(state)
        except RuntimeError:
            trace.append({"decision_index": decision_index, "action": "decision_provider",
                          "status": "blocked", "reason": "fixed_route_attempts_exhausted"})
            stop_reason = "executor_ready_decision_provider_guard_finalization"
            break
        action = decision.get("action")
        signature = digest({key: decision.get(key) for key in
                            ("action", "query", "seed_claim_ids", "relation_types")})
        trace_row = {"decision_index": decision_index, "action": action,
                     "query_digest": digest(str(decision.get("query", ""))),
                     "seed_claim_count": len(decision.get("seed_claim_ids", [])),
                     "relation_type_count": len(decision.get("relation_types", [])),
                     "reason_digest": digest(str(decision.get("reason", "")))}
        decision_index += 1
        if action == "answer":
            trace.append({**trace_row, "status": "accepted"})
            stop_reason = "executor_ready"
            break
        if signature in seen_decisions:
            trace.append({**trace_row, "status": "blocked", "reason": "repeated_identical_decision",
                          "next_action": "finalize_without_more_tools"})
            stop_reason = "executor_ready_cycle_guard_finalization"
            break
        seen_decisions.add(signature)
        try:
            if action == "traverse_graph":
                visible_ids = visible_governed_claim_ids(state["initial_context"])
                for prior in state["tool_results"]:
                    visible_ids.update(visible_governed_claim_ids(prior.get("result", {})))
                requested_seeds = list(decision.get("seed_claim_ids", []))
                if not requested_seeds or any(seed_id not in visible_ids for seed_id in requested_seeds):
                    raise ValueError("traverse_graph seed was not disclosed to the executor")
                result = traverse_graph(str(decision.get("query", "")), scope,
                                        requested_seeds, list(decision.get("relation_types", [])))
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
    return {"state": state, "trace": trace,
            "tool_call_count": sum(row.get("status") == "ok" and row.get("action") != "answer" for row in trace),
            "stop_reason": stop_reason,
            "used_traverse_graph": any(row.get("action") == "traverse_graph" and row.get("status") == "ok" for row in trace),
            "used_search_gap": any(row.get("action") == "search_gap" and row.get("status") == "ok" for row in trace)}


def run_quality_open_discovery(
    *, query: str, scope: str, index: SectionIndex,
    decide: Callable[[dict[str, Any]], dict[str, Any]], graph: dict[str, Any],
    raw_corpus_control: bool = False,
    state_token_limit: int = OPEN_DISCOVERY_STATE_TOKEN_UPPER_BOUND,
    wall_seconds: int = OPEN_DISCOVERY_WALL_SECONDS,
) -> dict[str, Any]:
    """Find a quality ceiling without fixed calls, result pages, or lifetime evidence caps."""
    objects = task_knowledge_objects(graph)
    if raw_corpus_control:
        seed: Any = {"mode": "raw-corpus-open-discovery-control",
                     "source_inventory": index.inventory(),
                     "governed_context": [], "admission_authority": False}
    else:
        seed = compact_tool_result(open_loop_initial_context(query, scope))
        seed["typed_object_availability"] = objects["availability"]
    state: dict[str, Any] = {
        "ask": query, "initial_context": seed, "tool_results": [],
        "limits": {"max_tool_calls": None, "max_lifetime_results": None,
                   "fixed_bm25_top_k": None, "state_token_upper_bound": state_token_limit,
                   "wall_seconds": wall_seconds},
        "governance_boundary": {"read_only": True, "retrieval_status": "not_governed",
                                "automatic_admission": False},
    }
    trace: list[dict[str, Any]] = []
    seen_decisions: set[str] = set()
    started = time.monotonic()
    stop_reason = "executor_ready"
    decision_index = 0

    def context_fitted_page_size(requested: int) -> int:
        """Fit one response to the remaining model context, never to a lifetime quota."""
        if requested < 1:
            raise ValueError("page_size must be positive")
        remaining = max(0, state_token_limit - state_token_upper_bound(state))
        # A receipt/claim can be long. Reserve the final quarter of the window for
        # the executor answer and use a conservative per-item projection. The model
        # can request the next page indefinitely until the context guard is reached.
        context_capacity = max(1, (remaining * 3 // 4) // 1_200)
        return min(requested, context_capacity)

    while True:
        if time.monotonic() - started >= wall_seconds:
            stop_reason = "executor_ready_wall_guard_finalization"
            break
        if state_token_upper_bound(state) >= state_token_limit:
            stop_reason = "executor_ready_context_guard_finalization"
            break
        try:
            decision = decide(state)
        except RuntimeError:
            trace.append({"decision_index": decision_index, "action": "decision_provider",
                          "status": "blocked", "reason": "fixed_route_attempts_exhausted"})
            stop_reason = "executor_ready_decision_provider_guard_finalization"
            break
        action = str(decision.get("action") or "")
        signature = digest({key: decision.get(key) for key in (
            "action", "query", "seed_claim_ids", "relation_types", "object_ids",
            "offset", "page_size", "expression", "variables", "output_unit", "round_places")})
        trace_row = {"decision_index": decision_index, "action": action,
                     "query_digest": digest(str(decision.get("query", ""))),
                     "offset": int(decision.get("offset") or 0),
                     "page_size": int(decision.get("page_size") or DEFAULT_RESULT_PAGE_SIZE),
                     "reason_digest": digest(str(decision.get("reason", "")))}
        decision_index += 1
        if action == "answer":
            trace.append({**trace_row, "status": "accepted"})
            break
        if signature in seen_decisions:
            trace.append({**trace_row, "status": "blocked", "reason": "repeated_identical_decision",
                          "next_action": "reformulate_or_finalize"})
            stop_reason = "executor_ready_cycle_guard_finalization"
            break
        seen_decisions.add(signature)
        try:
            if action == "traverse_graph":
                if raw_corpus_control:
                    raise ValueError("raw corpus control cannot traverse the governed graph")
                visible_ids = visible_governed_claim_ids(state)
                requested_seeds = list(decision.get("seed_claim_ids") or [])
                if not requested_seeds or any(seed_id not in visible_ids for seed_id in requested_seeds):
                    raise ValueError("traverse_graph seed was not disclosed to the executor")
                page_size = context_fitted_page_size(
                    int(decision.get("page_size") or DEFAULT_RESULT_PAGE_SIZE))
                result = knowledge.disclose_v1(
                    str(decision.get("query") or ""), "agent:workflow-executor", scope,
                    seeds=list(dict.fromkeys(requested_seeds)), max_claims=page_size,
                    max_depth=2, max_discovered=0)
                result = compact_tool_result(result)
            elif action in {"search_gap", "search_authority"}:
                result = paged_bm25(
                    index, str(decision.get("query") or ""),
                    offset=int(decision.get("offset") or 0),
                    page_size=context_fitted_page_size(
                        int(decision.get("page_size") or DEFAULT_RESULT_PAGE_SIZE)),
                    authority_candidate=action == "search_authority")
            elif action == "get_evidence_atoms":
                result = select_objects(objects, "evidence_atoms", list(decision.get("object_ids") or []),
                                        str(decision.get("query") or ""))
            elif action == "get_authority_nodes":
                result = select_objects(objects, "authority_nodes", list(decision.get("object_ids") or []),
                                        str(decision.get("query") or ""))
            elif action == "get_derivation_nodes":
                result = select_objects(objects, "derivation_nodes", list(decision.get("object_ids") or []),
                                        str(decision.get("query") or ""))
            elif action == "create_evidence_atom":
                result = bind_evidence_atom(decision, visible_candidate_receipts(state))
                objects["evidence_atoms"].append(result)
                objects["availability"]["evidence_atom_count"] = len(objects["evidence_atoms"])
            elif action == "create_authority_node":
                result = bind_authority_node(decision, visible_candidate_receipts(state))
                objects["authority_nodes"].append(result)
                objects["availability"]["authority_node_count"] = len(objects["authority_nodes"])
            elif action == "calculate":
                result = calculate_derivation(
                    str(decision.get("expression") or ""), dict(decision.get("variables") or {}),
                    output_unit=str(decision.get("output_unit") or ""),
                    round_places=int(decision.get("round_places") if decision.get("round_places") is not None else 2),
                    basis_object_ids=list(decision.get("basis_object_ids") or []))
                objects["derivation_nodes"].append(result)
                objects["availability"]["derivation_node_count"] = len(objects["derivation_nodes"])
            else:
                raise ValueError("unknown open-discovery action")
        except (TypeError, ValueError, SyntaxError) as exc:
            trace.append({**trace_row, "status": "blocked", "reason": type(exc).__name__})
            state["tool_results"].append({"action": action, "status": "blocked",
                                          "reason": type(exc).__name__})
            continue
        state["tool_results"].append({"action": action, "status": "ok", "result": result})
        trace.append({**trace_row, "status": "ok", "result_digest": digest(result),
                      "result_count": int(result.get("returned_count", result.get("object_count", 1)))})
    used_actions = sorted({row["action"] for row in trace if row.get("status") == "ok"})
    return {"state": state, "trace": trace,
            "tool_call_count": sum(row.get("status") == "ok" for row in trace),
            "stop_reason": stop_reason, "used_actions": used_actions,
            "used_traverse_graph": "traverse_graph" in used_actions,
            "used_search_gap": "search_gap" in used_actions,
            "used_search_authority": "search_authority" in used_actions,
            "used_calculate": "calculate" in used_actions,
            "typed_object_availability": objects["availability"]}

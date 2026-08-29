#!/usr/bin/env python3
"""Run the private two-task legal workflow utility panel."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import stat
import statistics
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import proofpress_knowledge as knowledge
import run_private_panel as private_panel
from run_claim_construction_private import Gateway, SectionIndex, _model_call, digest
from run_gap_retrieval_private import (
    ROUTED_DOCUMENT_LIMIT,
    bm25_receipts,
    classify_query,
    gateway_cost_summary,
    materialize_pageindex_sources,
    prior_bm25,
    route_pageindex_sources,
)

EXECUTOR_ROUTES = {
    "deepseek": ("deepseek/deepseek-v4-flash", "alibaba", "primary-reasoning", "high", 16000),
    "muse": ("meta/muse-spark-1.2", "meta", "cross-model-sensitivity", "medium", 16000),
    "glm": ("zai/glm-5.3-flash", "baseten", "cross-model-sensitivity", "high", 16000),
    "qwen": ("alibaba/qwen3.8-27b", "alibaba", "cross-model-sensitivity", "high", 16000),
}
GRADER = ("google/gemini-3.1-pro-preview", "google")
CONDITIONS = ("pr36-v7-prefetched-context", "full-catalog-bm25-prefetch",
              "evidence-first-v9-prefetched-context", "evidence-first-v9-claim-graph-only",
              "evidence-first-v9-graph-plus-global-bm25",
              "evidence-first-v9-graph-plus-hierarchical-hybrid")
ORACLE_CONDITIONS = ("oracle-claim-graph", "v9-claim-graph-plus-direct-gap-evidence")
PROGRESSIVE_CONDITIONS = ("pr36-v7-prefetched-context", "evidence-first-v9-claim-graph-only",
                          "evidence-first-v9-graph-plus-global-bm25",
                          "evidence-first-v9-graph-plus-hierarchical-hybrid")
MAX_DISCLOSURES_PER_TASK = 3
MAX_DISCOVERED_PER_CALL = 5
MAX_CONTEXT_TOKEN_UPPER_BOUND = 24000

EXECUTOR_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["answer", "ask_answers", "citations", "gaps"],
    "properties": {
        "answer": {"type": "string"},
        "ask_answers": {
            "type": "array",
            "items": {
                "type": "object", "additionalProperties": False,
                "required": ["ask_id", "answer", "citations", "gaps"],
                "properties": {
                    "ask_id": {"type": "string"},
                    "answer": {"type": "string"},
                    "citations": {"type": "array", "items": {"type": "string"}},
                    "gaps": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        "citations": {"type": "array", "items": {"type": "string"}},
        "gaps": {"type": "array", "items": {"type": "string"}},
    },
}

GRADER_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["rubric_fraction", "unsupported_claims", "citation_errors", "authority_errors"],
    "properties": {
        "rubric_fraction": {"type": "number", "minimum": 0, "maximum": 1},
        "unsupported_claims": {"type": "integer", "minimum": 0},
        "citation_errors": {"type": "integer", "minimum": 0},
        "authority_errors": {"type": "integer", "minimum": 0},
    },
}


def resolve_runtime_path(value: str) -> str:
    """Resolve a runtime dependency before the runner changes cwd."""
    return str(Path(value).resolve())


def gateway_bridge_values(shared: str | None, pageindex: str | None,
                          claim: str | None) -> tuple[str, str]:
    pageindex_value = pageindex or shared
    claim_value = claim or shared
    if not pageindex_value or not claim_value:
        raise ValueError("both PageIndex and claim Gateway bridges are required")
    return pageindex_value, claim_value


def sha_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode()).hexdigest()


def bounded_json(value: Any, max_tokens: int = MAX_CONTEXT_TOKEN_UPPER_BOUND) -> tuple[str, int]:
    """Return valid JSON under a conservative UTF-8-byte token upper bound."""
    current = json.loads(json.dumps(value, ensure_ascii=False))
    def render() -> str:
        return json.dumps(current, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    text = render()
    while len(text.encode()) > max_tokens:
        candidates: list[tuple[int, tuple[Any, ...], str]] = []
        def visit(node: Any, path: tuple[Any, ...] = ()) -> None:
            if isinstance(node, str) and len(node) > 16:
                candidates.append((len(node.encode()), path, "string"))
            elif isinstance(node, list) and node:
                # A one-item list is commonly the structural envelope for a
                # disclosure packet.  Dropping that only item turns a valid
                # bounded packet into ``[]`` and makes qualification report an
                # empty graph.  Shrink fields inside singleton lists; only
                # truncate a list when at least one representative item can
                # remain.
                if len(node) > 1:
                    candidates.append((len(json.dumps(node, ensure_ascii=False).encode()), path, "list"))
                for index, child in enumerate(node): visit(child, path + (index,))
            elif isinstance(node, dict):
                for key, child in node.items(): visit(child, path + (key,))
        visit(current)
        if not candidates:
            raise ValueError("context metadata alone exceeds 24k token upper bound")
        # Preserve structural/cardinality information for as long as possible:
        # large text is expendable context, whereas deleting an entire packet
        # changes the condition being evaluated.
        string_candidates = [row for row in candidates if row[2] == "string"]
        pool = string_candidates or candidates
        _, path, kind = max(pool, key=lambda row: (row[0], tuple(map(str, row[1]))))
        if not path:
            target = current
            current = ((target[:len(target) // 2] + "…") if kind == "string" and len(target) > 32
                       else "…" if kind == "string"
                       else target[:max(1, len(target) // 2)])
        else:
            parent = current
            for part in path[:-1]: parent = parent[part]
            key = path[-1]
            target = parent[key]
            if kind == "string": parent[key] = target[:len(target) // 2] + "…" if len(target) > 32 else "…"
            else: parent[key] = target[:max(1, len(target) // 2)]
        text = render()
    # Any tokenizer token consumes at least one UTF-8 byte. Byte length is a
    # deliberately conservative upper bound, not a vendor-token estimate.
    return text, len(text.encode())


def git_init(path: Path) -> None:
    for args in (("init", "-q"), ("config", "user.email", "workflow-eval@example.com"),
                 ("config", "user.name", "Workflow Evaluation Fixture")):
        subprocess.run(["git", *args], cwd=path, check=True, stdout=subprocess.DEVNULL)


def stage_graph(graph: dict[str, Any], navigation: dict[str, str]) -> tuple[dict[str, str], dict[str, Any]]:
    construction = graph["construction"]
    evidence_by_id = {row["evidence_id"]: row for row in construction.get("evidence", [])}
    imported: dict[str, str] = {}
    retrieval_config_digest = digest({"adapter": "bm25-page/v1", "version": "1",
                                      "top_documents": 10, "top_sections": 6})
    for evidence_id, evidence in evidence_by_id.items():
        source = evidence.get("source", {})
        if source.get("uri") not in navigation:
            continue
        retrieval = evidence.get("retrieval", {})
        payload = {
            "schema_version": knowledge.RETRIEVAL_EVIDENCE_SCHEMA,
            "source": source,
            "evidence": {"quote": evidence.get("quote"), "locator": evidence.get("locator")},
            "retrieval": {"adapter": "bm25-page", "version": "1",
                          "query": retrieval.get("query") or "frozen requirement retrieval",
                          "config_digest": retrieval_config_digest},
        }
        try:
            events = knowledge._import_retrieval_evidence_v2(payload)
        except (KeyError, TypeError, ValueError):
            continue
        imported[evidence_id] = events[-1]["evidence"]["id"]
    mapping = {}
    scope = graph["task"]["task_id"]
    for claim in construction.get("claims", []):
        refs = []
        for evidence_id in claim.get("evidence_ids", []):
            if evidence_id in imported:
                refs.append(imported[evidence_id])
        if not refs:
            continue
        proposed = knowledge.propose_v2(claim["statement"], refs, scope, "agent:v8-constructor")
        new_id = proposed["conclusion"]["id"]
        knowledge.review_v2(new_id, "admit", "human:staged-evaluation-reviewer")
        mapping[claim["id"]] = new_id
    relation_diagnostics: dict[str, Any] = {
        "candidate_count": len(construction.get("relations", [])),
        "admitted_count": 0,
        "rejected_counts": {},
        "rejected_relation_digest": None,
    }
    rejected_relations: list[dict[str, Any]] = []

    def reject_relation(relation: dict[str, Any], reason: str) -> None:
        counts = relation_diagnostics["rejected_counts"]
        counts[reason] = counts.get(reason, 0) + 1
        rejected_relations.append({
            "from": relation.get("from"),
            "to": relation.get("to"),
            "type": relation.get("type"),
            "reason": reason,
        })

    for relation in construction.get("relations", []):
        left, right = mapping.get(relation.get("from")), mapping.get(relation.get("to"))
        if not left or not right:
            reject_relation(relation, "unmapped_endpoint")
            continue
        if left == right:
            reject_relation(relation, "self_relation")
            continue
        try:
            proposed = knowledge.propose_relation_v2(left, right, relation["type"], "agent:v8-constructor")
        except (KeyError, TypeError, ValueError):
            reject_relation(relation, "core_validation_rejected")
            continue
        relation_id = proposed["relation"]["id"]
        try:
            knowledge.review_relation_v2(relation_id, "admit", "human:staged-evaluation-reviewer")
        except ValueError:
            reject_relation(relation, "policy_admission_rejected")
            try:
                knowledge.review_relation_v2(relation_id, "reject", "human:staged-evaluation-reviewer")
            except ValueError:
                pass
            continue
        relation_diagnostics["admitted_count"] += 1
    if rejected_relations:
        relation_diagnostics["rejected_relation_digest"] = digest(rejected_relations)
    return mapping, relation_diagnostics


def compact_disclosure_packet(packet: dict[str, Any], max_chars: int = 46000) -> dict[str, Any]:
    """Keep executor-relevant trust data without dropping an oversized packet."""
    def trim(value: Any, limit: int) -> Any:
        if isinstance(value, str) and len(value) > limit:
            return value[:limit] + "…"
        return value

    governed = []
    for row in packet.get("governed_context", []):
        governed.append({key: trim(row.get(key), 4000) for key in
                         ("id", "statement", "scope", "qualifiers", "digest", "receipt")
                         if key in row})
    lineage = []
    for row in packet.get("lineage", []):
        conclusion = row.get("conclusion", {})
        evidence_rows = []
        for evidence in row.get("evidence", []):
            if not isinstance(evidence, dict):
                continue
            compact_evidence = {key: evidence.get(key) for key in
                                ("id", "kind", "source_ref", "source_content_digest",
                                 "quote_digest", "retrieval_receipt_digest", "digest")
                                if key in evidence}
            receipt = evidence.get("retrieval_receipt")
            if isinstance(receipt, dict):
                receipt_view = {
                    **{key: receipt.get(key) for key in ("schema_version", "source", "locator", "retrieval")
                       if key in receipt},
                    "quote_digest": receipt.get("quote_digest"),
                }
                quote = receipt.get("quote")
                if isinstance(quote, str) and len(quote) > 1600:
                    receipt_view.update({"quote_excerpt": trim(quote, 1600),
                                         "receipt_view_truncated": True})
                else:
                    receipt_view["quote"] = quote
                compact_evidence["retrieval_receipt_view"] = receipt_view
            evidence_rows.append(compact_evidence)
        lineage.append({"conclusion_id": conclusion.get("id"), "state": row.get("state"),
                        "evidence": evidence_rows,
                        "admission": row.get("admission"), "review": row.get("review")})
    discovered = []
    for row in packet.get("discovered_evidence", []):
        item = dict(row)
        receipt = dict(item.get("receipt", {}))
        if isinstance(receipt.get("quote"), str) and len(receipt["quote"]) > 1600:
            receipt["quote_excerpt"] = trim(receipt.pop("quote"), 1600)
            receipt["receipt_view_truncated"] = True
        item["receipt_view"] = receipt
        item.pop("receipt", None)
        discovered.append(item)
    compact = {key: packet.get(key) for key in
               ("schema_version", "scope", "coverage", "gaps", "blocked", "actions",
                "ledger_head", "policy_digest", "config_digest", "traversal", "discovery")}
    compact.update({"governed_context": governed, "lineage": lineage,
                    "discovered_evidence": discovered})
    while len(json.dumps(compact, ensure_ascii=False, sort_keys=True)) > max_chars and governed:
        removed = governed.pop()
        removed_id = removed.get("id")
        lineage[:] = [row for row in lineage if row.get("conclusion_id") != removed_id]
        compact["truncated_claim_count"] = compact.get("truncated_claim_count", 0) + 1
    return compact


def pdf_sources(catalog: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    navigation = {row["uri"]: row["path"] for row in catalog.get("source_navigation", [])}
    sources = []
    for representation in catalog.get("representations", []):
        source = representation["source"]
        if source.get("media_type") != "application/pdf" or source.get("uri") not in navigation:
            continue
        sources.append({"source_id": sha_text(source["uri"])[7:23], "path": navigation[source["uri"]],
                        "uri": source["uri"], "content_digest": source["content_digest"],
                        "media_type": source["media_type"],
                        "representation_digest": representation["representation_digest"],
                        "transform_digest": representation["transform_digest"],
                        "page_count": representation["page_count"]})
    return sources, navigation


def oracle_diagnostic_contexts(graph: dict[str, Any], silver: dict[str, Any],
                               catalog: dict[str, Any], graph_packets: list[dict[str, Any]]) -> dict[str, Any]:
    """Build explicitly leaky oracle controls that localize workflow failures.

    These controls are diagnostics only: rubric atoms and model-adjudicated
    silver locators are forbidden from every scored product condition.
    """
    by_uri: dict[str, list[dict[str, Any]]] = {}
    for representation in catalog.get("representations", []):
        uri = representation.get("source", {}).get("uri")
        if isinstance(uri, str):
            by_uri[uri] = representation.get("sections", [])
    receipts = []
    for locator in silver.get("locators", []):
        uri = locator.get("source_uri")
        page = locator.get("locator", {})
        start, end = page.get("page_start"), page.get("page_end")
        hits = [row for row in by_uri.get(uri, [])
                if isinstance(start, int) and isinstance(end, int)
                and row.get("page_start", 0) <= end and row.get("page_end", 0) >= start]
        if hits:
            row = hits[0]
            receipts.append({"oracle_evidence_id": f"oracle-evidence-{len(receipts) + 1}",
                             "candidate_id": locator.get("candidate_id"),
                             "source_uri": uri, "locator": page, "section_id": row.get("section_id"),
                             "text": row.get("text", ""), "oracle_silver": True})
    construction = graph.get("construction", {})
    gaps = [row for row in construction.get("requirements", []) if row.get("status") in {"partial", "gap"}]
    judgment_rows = silver.get("judgments", {})
    final_judgment = judgment_rows.get("arbitration") or judgment_rows.get("a") or {}
    minimum_sets = [row.get("candidate_ids", []) for row in final_judgment.get("minimum_evidence_sets", [])
                    if isinstance(row, dict) and row.get("candidate_ids")]
    explicit = silver.get("gap_mapping", {}) if isinstance(silver.get("gap_mapping"), dict) else {}
    receipt_by_candidate = {row.get("candidate_id"): row for row in receipts if row.get("candidate_id")}
    gap_bindings = []
    for index, gap in enumerate(gaps):
        gap_id = gap.get("requirement_id")
        candidate_ids = explicit.get(gap_id)
        basis = "frozen_gap_mapping"
        if not isinstance(candidate_ids, list):
            candidate_ids = minimum_sets[index % len(minimum_sets)] if minimum_sets else []
            basis = "model_adjudicated_minimum_evidence_set"
        bound = [receipt_by_candidate[candidate] for candidate in candidate_ids if candidate in receipt_by_candidate]
        gap_bindings.append({"gap_id": gap_id, "binding_basis": basis,
                             "evidence_ids": [row["oracle_evidence_id"] for row in bound]})
    bound_ids = {evidence_id for row in gap_bindings for evidence_id in row["evidence_ids"]}
    bound_receipts = [{**row, "gap_ids": [binding["gap_id"] for binding in gap_bindings
                                           if row["oracle_evidence_id"] in binding["evidence_ids"]]}
                      for row in receipts if row["oracle_evidence_id"] in bound_ids]
    oracle_claims = [{key: claim.get(key) for key in ("id", "statement", "type", "scope", "evidence_ids")}
                     for claim in construction.get("claims", [])]
    return {
        "oracle-claim-graph": {"diagnostic_only": True, "rubric_leakage": False,
                               "silver_leakage": True, "claims": oracle_claims,
                               "relations": construction.get("relations", []),
                               "gap_bindings": gap_bindings, "evidence": bound_receipts},
        "v9-claim-graph-plus-direct-gap-evidence": {
            "diagnostic_only": True, "silver_leakage": True,
            "governed_packets": graph_packets, "gap_bindings": gap_bindings,
            "direct_gap_evidence": bound_receipts},
    }


def qualification_preflight(contexts: dict[str, str | None], task_ids: list[str],
                            silver_by_task: dict[str, dict[str, Any]] | None) -> dict[str, Any]:
    failures = []
    for name, context in contexts.items():
        if name == "pr36-v7-prefetched-context" and context is None:
            failures.append({"condition": name, "reason": "missing frozen comparator context"})
        elif context is None or not context.strip() or context.strip() in ("[]", "{}"):
            failures.append({"condition": name, "reason": "empty context"})
    if silver_by_task is not None:
        for task_id in task_ids:
            if not silver_by_task.get(task_id, {}).get("locators"):
                failures.append({"task_id": task_id, "reason": "no frozen silver locator for oracle control"})
    return {"status": "pass" if not failures else "fail", "failures": failures}


def prefetched_context_from_construction_artifact(value: Any) -> dict[str, Any]:
    """Normalize either a v7 raw run artifact or an already-extracted context."""
    if not isinstance(value, dict):
        raise ValueError("PR36 v7 context artifact must be a JSON object")
    construction = value.get("construction", value)
    if not isinstance(construction, dict):
        raise ValueError("PR36 v7 construction must be a JSON object")
    required = ("claims", "relations", "evidence")
    if not all(isinstance(construction.get(key), list) for key in required):
        raise ValueError("PR36 v7 artifact must contain construction claims, relations, and evidence arrays")
    return {key: construction[key] for key in required}


def disclosure_bundles(asks: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    bundles = [asks[i:i + 4] for i in range(0, len(asks), 4)]
    if len(bundles) > MAX_DISCLOSURES_PER_TASK:
        raise ValueError(f"workflow disclosure limit exceeded: {len(bundles)} > {MAX_DISCLOSURES_PER_TASK}")
    return bundles


def custody_manifest_sources(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    """Use original source bytes for disclose custody verification.

    PageIndex may search a digest-bound canonical Markdown representation, but
    the replayed receipt navigates to the original source. The agent-facing
    corpus manifest must therefore bind the original file/digest rather than
    pretending the canonical file has the original source digest.
    """
    navigation = {row["uri"]: row["path"] for row in catalog.get("source_navigation", [])}
    rows = []
    for representation in catalog.get("representations", []):
        source = representation.get("source", {})
        uri = source.get("uri")
        path = navigation.get(uri)
        if not uri or not path:
            continue
        rows.append({"uri": uri, "path": path,
                     "content_digest": source.get("content_digest"),
                     "media_type": source.get("media_type")})
    return rows


def replay_sidecar(path: Path, mapping: dict[str, list[dict[str, Any]]], label: str = "pageindex") -> str:
    data = path / f"{label}-replay-private.json"
    data.write_text(json.dumps(mapping))
    script = path / f"{label}-replay.py"
    script.write_text(f"""#!/usr/bin/env python3
import hashlib,json,sys
from pathlib import Path
request=json.load(sys.stdin); rows=json.loads(Path(__file__).with_name('{label}-replay-private.json').read_text()).get(hashlib.sha256(request['query'].encode()).hexdigest(),[])
for row in rows:
 row['retrieval']['query']=request['query']; row['retrieval']['config_digest']=request['config']['config_digest']
print(json.dumps({{'schema_version':'proofpress/pageindex-sidecar/v1','fallback_used':False,'sidecar':{{'adapter':'{label}-private-replay','version':'1'}},'telemetry':{{'latency_ms':0,'replayed_real_receipts':len(rows)}},'receipts':rows[:request['max_results']]}}))
""")
    script.chmod(stat.S_IRWXU)
    return str(script)


def disclosure_receipt(row: dict[str, Any], query: str, config_digest: str) -> dict[str, Any]:
    """Normalize retrieval-panel rows to the agent-facing portable receipt."""
    evidence = row.get("evidence")
    if not isinstance(evidence, dict):
        evidence = {"quote": row.get("quote"), "locator": row.get("locator")}
    retrieval = row.get("retrieval") if isinstance(row.get("retrieval"), dict) else {}
    return {"schema_version": knowledge.RETRIEVAL_EVIDENCE_SCHEMA,
            "source": row.get("source"),
            "evidence": evidence,
            "retrieval": {"adapter": str(retrieval.get("adapter") or "unknown-retrieval"),
                          "version": str(retrieval.get("version") or "1"),
                          "query": query, "config_digest": config_digest}}


def build_contexts(graph: dict[str, Any], asks: list[dict[str, Any]], catalog: dict[str, Any],
                   sidecar: str, gateway_server: str, workspace: Path,
                   gateway_receipts: Path, silver: dict[str, Any] | None = None,
                   requested_conditions: set[str] | None = None,
                   ) -> tuple[dict[str, str | None], dict[str, int], list[dict[str, Any]], float, dict[str, Any]]:
    index = SectionIndex(catalog)
    combined = "\n".join([graph["task"]["prompt"]] + [row["query"] for row in asks])
    full_rows = []
    for hit in index.search(combined, max_documents=20, max_sections=40):
        section = hit["section"]
        full_rows.append({"source_uri": section["uri"], "page_start": section["page_start"],
                          "page_end": section["page_end"], "text": section.get("text", "")})
    construction = graph["construction"]
    prefetched = {"claims": construction.get("claims", []), "relations": construction.get("relations", []),
                  "evidence": construction.get("evidence", [])}
    bundles = disclosure_bundles(asks)
    graph_packets_raw = [knowledge.disclose_v1("\n".join(row["query"] for row in bundle), "agent:workflow-executor",
                                               graph["task"]["task_id"], max_claims=24, max_depth=2)
                         for bundle in bundles]
    requested = requested_conditions or set(CONDITIONS)
    contexts, tokens = {}, {}
    for name, value in (("full-catalog-bm25-prefetch", full_rows),
                        ("evidence-first-v9-prefetched-context", prefetched),
                        ("evidence-first-v9-claim-graph-only",
                         [compact_disclosure_packet(row) for row in graph_packets_raw])):
        if name in requested:
            contexts[name], tokens[name] = bounded_json(value)
    contexts["pr36-v7-prefetched-context"] = None
    tokens["pr36-v7-prefetched-context"] = 0
    retrieval_conditions = {"evidence-first-v9-graph-plus-global-bm25",
                            "evidence-first-v9-graph-plus-hierarchical-hybrid"}
    if not (requested & retrieval_conditions):
        disclosure_telemetry = {"calls": len(bundles), "max_calls": MAX_DISCLOSURES_PER_TASK,
                                "discovered_per_call": [0 for _ in bundles],
                                "max_discovered_per_call": MAX_DISCOVERED_PER_CALL,
                                "total_discovered": 0}
        return contexts, tokens, [], 0.0, disclosure_telemetry
    sources = materialize_pageindex_sources(catalog, workspace / "canonical-pageindex-inputs")
    if not sources:
        raise ValueError("workflow qualification failed: catalog has no PageIndex-readable representations")
    corpus = workspace / "pageindex-corpus-private.json"
    custody_sources = custody_manifest_sources(catalog)
    if len(custody_sources) != len(sources):
        raise ValueError("workflow custody manifest does not cover every PageIndex representation")
    corpus.write_text(json.dumps({"sources": custody_sources}))
    config = {"adapter": "proofpress.pageindex", "version": "1", "requested_model": "deepseek/deepseek-v4-flash",
              "provider": "proofpress-dev-ai-gateway", "fallback": "forbidden", "max_sections": 5,
              "max_pages": 5, "toc_check_pages": 1, "max_pages_per_node": 1, "max_tokens_per_node": 2500,
              "document_router": "bm25-document-router/v1",
              "max_routed_documents": min(ROUTED_DOCUMENT_LIMIT, len(sources)),
              "node_summary": False, "document_description": False}
    config["config_digest"] = knowledge.digest(config)
    private_panel.MODEL, private_panel.PROVIDER = "deepseek/deepseek-v4-flash", "deepinfra"
    bridge_proc, base_url = private_panel.bridge(gateway_server, gateway_receipts)
    real_receipts, global_receipts, hybrid_receipts = {}, {}, {}
    pageindex_events, cost = [], 0.0
    try:
        for packet, bundle in zip(graph_packets_raw, bundles):
            query = "\n".join(row["query"] for row in bundle)
            global_rows = bm25_receipts(index, query)[:20]
            query_key = hashlib.sha256(query.encode()).hexdigest()
            global_receipts[query_key] = [disclosure_receipt(row, query, config["config_digest"])
                                          for row in global_rows[:MAX_DISCOVERED_PER_CALL]]
            if packet["coverage"] == "covered":
                hybrid_receipts[query_key] = []
                continue
            if classify_query(query) == "exact":
                hybrid_receipts[query_key] = [disclosure_receipt(row, query, config["config_digest"])
                                              for row in global_rows[:MAX_DISCOVERED_PER_CALL]]
                pageindex_events.append({"query_digest": sha_text(query), "status": "bypassed_exact_query",
                                         "receipt_count": len(global_rows[:MAX_DISCOVERED_PER_CALL])})
                continue
            routed_sources, route_audit = route_pageindex_sources(
                index, query, sources, min(ROUTED_DOCUMENT_LIMIT, len(sources)))
            if not routed_sources:
                pageindex_events.append({"query_digest": sha_text(query), "status": "inconclusive",
                                         "reason_type": "EmptyDocumentRoute",
                                         "reason_digest": sha_text("bounded PageIndex route was empty")})
                continue
            offset = len(gateway_receipts.read_text().splitlines()) if gateway_receipts.exists() else 0
            try:
                rows, telemetry = private_panel.tree(query, routed_sources, sidecar, config, 5, base_url,
                                                     workspace / "pageindex-cache", 1800)
                cost_summary = gateway_cost_summary(
                    gateway_receipts, offset, private_panel.MODEL, private_panel.PROVIDER)
                cost += float(cost_summary["known_cost_usd"])
                real_receipts[query_key] = [disclosure_receipt(row, query, config["config_digest"])
                                            for row in rows]
                hybrid_receipts[query_key] = [disclosure_receipt(row, query, config["config_digest"])
                                              for row in prior_bm25(
                                                  index, query, global_rows, rows)[:MAX_DISCOVERED_PER_CALL]]
                pageindex_events.append({"query_digest": sha_text(query), "status": "ok", "receipt_count": len(rows),
                                         "latency_ms": telemetry.get("latency_ms"),
                                         "document_route_digest": route_audit["route_digest"],
                                         "routed_source_count": len(routed_sources),
                                         "source_build_retries": telemetry.get("source_build_retries", 0),
                                         **cost_summary})
            except Exception as exc:
                hybrid_receipts[query_key] = [disclosure_receipt(row, query, config["config_digest"])
                                              for row in global_rows[:MAX_DISCOVERED_PER_CALL]]
                pageindex_events.append({"query_digest": sha_text(query), "status": "inconclusive",
                                         "reason_type": type(exc).__name__, "reason_digest": sha_text(str(exc))})
    finally:
        bridge_proc.terminate()
        try: bridge_proc.wait(timeout=5)
        except subprocess.TimeoutExpired: bridge_proc.kill()
    global_replay = replay_sidecar(workspace, global_receipts, "global-bm25")
    hybrid_replay = replay_sidecar(workspace, hybrid_receipts, "hierarchical-hybrid")
    global_packets_raw = [knowledge.disclose_v1("\n".join(row["query"] for row in bundle),
                                                   "agent:workflow-executor", graph["task"]["task_id"],
                                                   corpus_manifest=str(corpus), sidecar=global_replay,
                                                   max_claims=24, max_depth=2,
                                                   max_discovered=MAX_DISCOVERED_PER_CALL)
                          for bundle in bundles]
    hybrid_packets_raw = [knowledge.disclose_v1("\n".join(row["query"] for row in bundle),
                                                   "agent:workflow-executor", graph["task"]["task_id"],
                                                   corpus_manifest=str(corpus), sidecar=hybrid_replay,
                                                   max_claims=24, max_depth=2,
                                                   max_discovered=MAX_DISCOVERED_PER_CALL)
                             for bundle in bundles]
    discovered_counts = [len(row.get("discovered_evidence", [])) for row in hybrid_packets_raw]
    if any(count > MAX_DISCOVERED_PER_CALL for count in discovered_counts):
        raise ValueError("workflow disclosure returned more discovered evidence than permitted")
    graph_packets = [compact_disclosure_packet(row) for row in graph_packets_raw]
    global_packets = [compact_disclosure_packet(row) for row in global_packets_raw]
    hybrid_packets = [compact_disclosure_packet(row) for row in hybrid_packets_raw]
    for name, value in (("evidence-first-v9-graph-plus-global-bm25", global_packets),
                        ("evidence-first-v9-graph-plus-hierarchical-hybrid", hybrid_packets)):
        if name in requested:
            contexts[name], tokens[name] = bounded_json(value)
    if silver is not None:
        oracle = oracle_diagnostic_contexts(graph, silver, catalog, graph_packets)
        for name, value in oracle.items():
            contexts[name], tokens[name] = bounded_json(value)
    disclosure_telemetry = {"calls": len(bundles), "max_calls": MAX_DISCLOSURES_PER_TASK,
                            "discovered_per_call": discovered_counts,
                            "max_discovered_per_call": MAX_DISCOVERED_PER_CALL,
                            "total_discovered": sum(discovered_counts)}
    return contexts, tokens, pageindex_events, cost, disclosure_telemetry


def normalize_grade(value: Any) -> dict[str, Any]:
    value = value if isinstance(value, dict) else {}
    fraction = value.get("rubric_fraction")
    if not isinstance(fraction, (int, float)) or not 0 <= fraction <= 1:
        raise ValueError("grader omitted rubric_fraction")
    counts: dict[str, int] = {}
    for key in ("unsupported_claims", "citation_errors", "authority_errors"):
        count = value.get(key, 0)
        # Gemini sometimes represents a requested count as the explicit list
        # of findings. Cardinality is a deterministic normalization; every
        # other non-numeric shape still fails closed.
        if isinstance(count, list):
            count = len(count)
        if (isinstance(count, bool) or not isinstance(count, (int, float))
                or int(count) != count or count < 0):
            raise ValueError(f"grader returned invalid {key}")
        counts[key] = int(count)
    return {"rubric_fraction": float(fraction), **counts}


def paired_bootstrap(values: list[float], samples: int = 10_000) -> list[float] | None:
    if not values: return None
    if len(values) == 1: return [values[0], values[0]]
    rng = random.Random(0)
    draws = sorted(statistics.mean(rng.choice(values) for _ in values) for _ in range(samples))
    return [draws[int(.025 * (samples - 1))], draws[int(.975 * (samples - 1))]]


def paired_workflow_comparisons(cells: list[dict[str, Any]],
                                executors: tuple[tuple[str, str, str, str, int], ...]
                                ) -> dict[str, Any]:
    output = {}
    for model, _, _, _, _ in executors:
        model_cells = {(row["task_id"], row["condition"]): row for row in cells
                       if row.get("executor_model") == model and row.get("status") == "scored"}
        for treatment in ("evidence-first-v9-graph-plus-global-bm25",
                          "evidence-first-v9-graph-plus-hierarchical-hybrid"):
            for baseline in ("pr36-v7-prefetched-context", "full-catalog-bm25-prefetch"):
                task_ids = sorted({task_id for task_id, condition in model_cells if condition == treatment}
                                  & {task_id for task_id, condition in model_cells if condition == baseline})
                rubric = [model_cells[(task_id, treatment)]["rubric_fraction"]
                          - model_cells[(task_id, baseline)]["rubric_fraction"] for task_id in task_ids]
                token_ratios = [model_cells[(task_id, treatment)]["context_token_upper_bound"]
                                / max(1, model_cells[(task_id, baseline)]["context_token_upper_bound"])
                                for task_id in task_ids]
                error_deltas = {key: [model_cells[(task_id, treatment)][key]
                                      - model_cells[(task_id, baseline)][key] for task_id in task_ids]
                                for key in ("unsupported_claims", "citation_errors", "authority_errors")}
                output[f"{model}|{treatment}|{baseline}"] = {
                    "paired_tasks": len(task_ids), "task_ids": task_ids,
                    "rubric_fraction_mean_delta": statistics.mean(rubric) if rubric else None,
                    "rubric_fraction_bootstrap_95_ci": paired_bootstrap(rubric),
                    "mean_context_token_ratio": statistics.mean(token_ratios) if token_ratios else None,
                    **{f"{key}_mean_delta": statistics.mean(values) if values else None
                       for key, values in error_deltas.items()},
                }
    return output


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--claim-report", required=True); ap.add_argument("--ask-manifest", required=True)
    ap.add_argument("--catalog", required=True); ap.add_argument("--sidecar", required=True)
    ap.add_argument("--gateway-server", help="Legacy shared bridge; prefer both role-specific bridges")
    ap.add_argument("--pageindex-gateway-server")
    ap.add_argument("--claim-gateway-server")
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--resume-artifacts")
    ap.add_argument("--silver-report", help="Enable diagnostic oracle controls from frozen private silver")
    ap.add_argument("--pr36-context-dir", help="Directory containing one frozen v7 context JSON per task")
    ap.add_argument("--qualification-only", action="store_true")
    ap.add_argument("--full-claim-task-panel", action="store_true",
                    help="Run every completed task in the claim report; tasks without lawyer asks use the task prompt for disclosure.")
    ap.add_argument("--progressive-only", action="store_true",
                    help="Run only the four frozen lawyer-ask progressive-disclosure conditions.")
    ap.add_argument("--qualification-max-asks", type=int, default=4,
                    help="Per-task ask cap for end-to-end qualification mode")
    ap.add_argument("--executors", default=",".join(EXECUTOR_ROUTES),
                    help="Comma-separated frozen executor labels: " + ",".join(EXECUTOR_ROUTES))
    ap.add_argument("--conditions",
                    help="Comma-separated scored product conditions; defaults to the selected panel mode")
    args = ap.parse_args()
    if not os.environ.get("AI_GATEWAY_API_KEY"):
        raise SystemExit("AI_GATEWAY_API_KEY unavailable")
    # The runner changes into a temporary git workspace before PageIndex is
    # invoked. Resolve executable/script paths against the caller's cwd first;
    # otherwise a valid relative gateway path fails only at the late bridge
    # bootstrap boundary.
    sidecar = resolve_runtime_path(args.sidecar)
    try:
        pageindex_gateway_value, claim_gateway_value = gateway_bridge_values(
            args.gateway_server, args.pageindex_gateway_server, args.claim_gateway_server)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    pageindex_gateway_server = resolve_runtime_path(pageindex_gateway_value)
    claim_gateway_server = resolve_runtime_path(claim_gateway_value)
    report = json.loads(Path(args.claim_report).read_text()); asks_manifest = json.loads(Path(args.ask_manifest).read_text())
    executor_labels = [value.strip() for value in args.executors.split(",") if value.strip()]
    unknown_executors = sorted(set(executor_labels) - set(EXECUTOR_ROUTES))
    if unknown_executors or not executor_labels:
        raise SystemExit("unknown or empty frozen executor selection: " + ",".join(unknown_executors))
    executors = tuple(EXECUTOR_ROUTES[label] for label in executor_labels)
    catalog = json.loads(Path(args.catalog).read_text()); raw_dir = Path(report["raw_private_dir"])
    silver_by_task = None
    if args.silver_report:
        silver_report = json.loads(Path(args.silver_report).read_text())
        silver_raw = Path(silver_report["raw_private_dir"])
        silver_by_task = {path.stem: json.loads(path.read_text()) for path in silver_raw.glob("*.json")}
    default_conditions = PROGRESSIVE_CONDITIONS if args.progressive_only else CONDITIONS
    product_conditions = tuple(value.strip() for value in args.conditions.split(",") if value.strip()) if args.conditions else default_conditions
    unknown_conditions = sorted(set(product_conditions) - set(default_conditions))
    if unknown_conditions or not product_conditions:
        raise SystemExit("unknown or empty product condition selection: " + ",".join(unknown_conditions))
    active_conditions = product_conditions + (ORACLE_CONDITIONS if silver_by_task is not None and not args.progressive_only else ())
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw_out = out / "raw"; raw_out.mkdir(exist_ok=True); raw_out.chmod(0o700)
    executor_gateways: dict[str, Gateway] = {}; grader = None
    results, pageindex_events, pageindex_cost, disclosure_telemetry = [], [], 0.0, []
    task_ids = ([row["task_id"] for row in report.get("tasks", []) if row.get("status") == "ok"]
                if args.full_claim_task_panel else list(asks_manifest["task_ids"]))
    if args.full_claim_task_panel and len(task_ids) != 12:
        raise ValueError(f"formal workflow requires exactly 12 completed claim tasks, got {len(task_ids)}")
    previous = Path.cwd()
    try:
        executor_gateways = {
            model: Gateway(claim_gateway_server, model, provider, out, 300, reasoning,
                           structured_output=True)
            for model, provider, _, reasoning, _ in executors
        }
        grader = Gateway(claim_gateway_server, GRADER[0], GRADER[1], out, 300, "low",
                         structured_output=True)
        _, navigation = pdf_sources(catalog)
        navigation.update({row["uri"]: row["path"] for row in catalog.get("source_navigation", [])})
        with tempfile.TemporaryDirectory(prefix="proofpress-workflow-") as tmp:
            workspace = Path(tmp); git_init(workspace); os.chdir(workspace)
            work_items = []
            for task_id in task_ids:
                graph = json.loads((raw_dir / f"{task_id}.json").read_text())
                _, relation_diagnostics = stage_graph(graph, navigation)
                asks = [row for row in asks_manifest["asks"] if row["task_id"] == task_id]
                if args.qualification_only:
                    asks = asks[:max(1, args.qualification_max_asks)]
                context_asks = asks or [{"ask_id": f"{task_id}-task", "query": graph["task"]["prompt"]}]
                contexts, context_tokens, events, pi_cost, disclosure_stats = build_contexts(
                    graph, context_asks, catalog, sidecar, pageindex_gateway_server, workspace,
                    out / "workflow-pageindex-gateway-receipts.jsonl",
                    silver_by_task.get(task_id) if silver_by_task is not None else None,
                    set(active_conditions))
                disclosure_telemetry.append({
                    "task_id": task_id,
                    "staged_relation_diagnostics": relation_diagnostics,
                    **disclosure_stats,
                })
                if args.pr36_context_dir:
                    v7_path = Path(args.pr36_context_dir) / f"{task_id}.json"
                    if v7_path.is_file():
                        v7_context = prefetched_context_from_construction_artifact(json.loads(v7_path.read_text()))
                        contexts["pr36-v7-prefetched-context"], context_tokens["pr36-v7-prefetched-context"] = bounded_json(v7_context)
                pageindex_events.extend(events); pageindex_cost += pi_cost
                preflight = qualification_preflight(contexts, [task_id], silver_by_task)
                failed_pageindex = [row for row in events if row.get("status") == "inconclusive"]
                if failed_pageindex:
                    preflight["warnings"] = [{"reason": "hierarchical route fell back to global BM25",
                                               "failed_event_count": len(failed_pageindex)}]
                (raw_out / f"{task_id}-qualification.json").write_text(json.dumps(preflight, indent=2))
                if preflight["status"] != "pass":
                    for condition in active_conditions:
                        for model, provider, role, _, _ in executors:
                            results.append({"task_id": task_id, "condition": condition,
                                            "executor_model": model, "executor_provider": provider,
                                            "executor_role": role, "status": "inconclusive",
                                            "reason": "qualification preflight failed"})
                    continue
                for condition in active_conditions:
                    if contexts[condition] is None:
                        for model, provider, role, _, _ in executors:
                            results.append({"task_id": task_id, "condition": condition, "executor_model": model,
                                            "executor_provider": provider, "executor_role": role, "status": "inconclusive",
                                            "reason": "no equivalent frozen PR36-v7 context artifact"})
                        continue
                    for model, provider, role, reasoning, max_output_tokens in executors:
                        work_items.append((task_id, graph, asks, condition, contexts[condition],
                                           context_tokens[condition], model, provider, role,
                                           reasoning, max_output_tokens))

            def run_cell(item: tuple[Any, ...]) -> dict[str, Any]:
                task_id, graph, asks, condition, context, tokens, model, provider, role, reasoning, max_output_tokens = item
                cell = {"task_id": task_id, "condition": condition, "executor_model": model,
                        "executor_provider": provider, "executor_role": role,
                        "context_token_upper_bound": tokens,
                        "context_limit_tokens": MAX_CONTEXT_TOKEN_UPPER_BOUND}
                prompt = {"task": graph["task"]["prompt"], "expected_output": graph["task"].get("expected_output"),
                          "lawyer_asks": [{"ask_id": row["ask_id"], "query": row["query"]} for row in asks],
                          "context": context,
                          "instruction": "Produce the requested legal work product and answer the lawyer asks. Use only supplied context, distinguish governed from not_governed material, preserve gaps, and cite source/evidence IDs. Return JSON with answer, ask_answers, citations."}
                artifact_name = f"{task_id}-{condition}-{model.replace('/', '_')}.json"
                resume_path = Path(args.resume_artifacts) / artifact_name if args.resume_artifacts else None
                artifact = None
                resumed_grades: list[dict[str, Any]] = []
                if resume_path and resume_path.is_file():
                    resumed = json.loads(resume_path.read_text())
                    if isinstance(resumed, dict) and isinstance(resumed.get("artifact"), (dict, list)):
                        artifact = resumed["artifact"]
                        cell["executor_reused"] = True
                        for prior_grade in resumed.get("grades", []):
                            try:
                                resumed_grades.append(normalize_grade(prior_grade))
                            except ValueError:
                                pass
                if artifact is None:
                    generated = _model_call(
                        executor_gateways[model], "You are a legal workflow executor. Use the required output tool.",
                        json.dumps(prompt, ensure_ascii=False), max_output_tokens,
                        EXECUTOR_SCHEMA, "proofpress_legal_workflow_artifact")
                    if not generated["ok"]:
                        cell.update({"status": "inconclusive", "reason": "executor call failed closed"})
                        return cell
                    artifact = generated["value"]
                    cell["executor_reused"] = False
                grades = resumed_grades[:3]
                cell["grades_reused"] = len(grades)
                grade_failure_types: dict[str, int] = {}
                invalid_grade_count = 0
                grade_prompt = {"task": graph["task"]["prompt"], "gold_response": graph["task"].get("gold_response"),
                                "rubric": graph["task"].get("rubric"), "candidate": artifact,
                                "instruction": "Blindly grade the candidate. Return JSON with rubric_fraction in [0,1]. unsupported_claims, citation_errors, and authority_errors must each be either a nonnegative integer count or an array containing exactly the individual findings counted. Do not infer authority for staged or not_governed evidence."}
                for _ in range(3 - len(grades)):
                    graded = _model_call(
                        grader, "You are the native legal artifact grader. Use the required output tool.",
                        json.dumps(grade_prompt, ensure_ascii=False), 4096,
                        GRADER_SCHEMA, "proofpress_legal_workflow_grade")
                    if graded["ok"]:
                        try:
                            grades.append(normalize_grade(graded["value"]))
                        except ValueError:
                            invalid_grade_count += 1
                    else:
                        kind = str(graded.get("record", {}).get("error_type") or "unknown")
                        grade_failure_types[kind] = grade_failure_types.get(kind, 0) + 1
                if len(grades) != 3:
                    cell.update({"status": "inconclusive", "reason": "fewer than three valid blind grades",
                                 "valid_grade_count": len(grades),
                                 "grade_failure_types": grade_failure_types,
                                 "invalid_semantic_grade_count": invalid_grade_count})
                else:
                    cell.update({"status": "scored", "rubric_fraction": sum(g["rubric_fraction"] for g in grades) / 3,
                                 "unsupported_claims": sum(g["unsupported_claims"] for g in grades) / 3,
                                 "citation_errors": sum(g["citation_errors"] for g in grades) / 3,
                                 "authority_errors": sum(g["authority_errors"] for g in grades) / 3})
                artifact_path = raw_out / artifact_name
                artifact_path.write_text(json.dumps({"artifact": artifact, "grades": grades}, indent=2))
                cell["artifact_digest"] = digest(artifact)
                return cell

            with ThreadPoolExecutor(max_workers=max(1, min(args.workers, len(work_items)))) as pool:
                futures = {pool.submit(run_cell, item): item for item in work_items}
                for future in as_completed(futures):
                    item = futures[future]
                    try:
                        results.append(future.result())
                    except Exception as exc:
                        results.append({"task_id": item[0], "condition": item[3],
                                        "executor_model": item[6], "executor_provider": item[7],
                                        "executor_role": item[8], "context_token_upper_bound": item[5],
                                        "status": "inconclusive", "reason": "cell runner failed closed",
                                        "reason_type": type(exc).__name__, "reason_digest": sha_text(str(exc))})
    finally:
        os.chdir(previous)
        for gateway in (*executor_gateways.values(), grader):
            if gateway: gateway.stop()
    all_gateways = (*executor_gateways.values(), grader)
    calls = sum((gateway.calls for gateway in all_gateways if gateway), [])
    receipts = sum((gateway.receipt_rows() for gateway in all_gateways if gateway), [])
    known = [row["cost_usd"] for row in receipts if isinstance(row.get("cost_usd"), (int, float))]
    cells = [row for row in results if row["status"] == "scored"]
    aggregate = {}
    for condition in active_conditions:
        aggregate[condition] = {}
        for model, _, _, _, _ in executors:
            rows = [r for r in cells if r["condition"] == condition and r["executor_model"] == model]
            aggregate[condition][model] = {"scored_tasks": len(rows),
                                           "rubric_fraction": sum(r["rubric_fraction"] for r in rows) / len(rows) if rows else None,
                                           "context_token_upper_bound": sum(r["context_token_upper_bound"] for r in rows) / len(rows) if rows else None,
                                           "unsupported_claims": sum(r["unsupported_claims"] for r in rows) / len(rows) if rows else None,
                                           "citation_errors": sum(r["citation_errors"] for r in rows) / len(rows) if rows else None,
                                           "authority_errors": sum(r["authority_errors"] for r in rows) / len(rows) if rows else None}
    configuration = {
        "executors": [{"model": m, "provider": p, "role": r,
                       "reasoning": reasoning, "max_output_tokens": max_tokens}
                      for m, p, r, reasoning, max_tokens in executors],
        "grader": {"model": GRADER[0], "provider": GRADER[1], "reasoning": "low",
                   "max_output_tokens": 4096, "blind_grades_per_artifact": 3},
        "pageindex": {"model": private_panel.MODEL, "provider": private_panel.PROVIDER,
                      "reasoning": "medium", "max_routed_documents": ROUTED_DOCUMENT_LIMIT},
        "fallback": "forbidden",
        "output_protocol": "provider-structured-json-schema/v1",
        "max_disclosure_calls": 3,
        "max_context_token_upper_bound": MAX_CONTEXT_TOKEN_UPPER_BOUND,
    }
    configuration["config_digest"] = digest(configuration)
    sanitized = {"schema_version": "proofpress/private-legal-workflow-utility/v1",
                 "ask_manifest_digest": asks_manifest["manifest_digest"], "conditions": list(active_conditions),
                 "executors": [{"model": m, "provider": p, "role": r,
                                "reasoning": reasoning, "max_output_tokens": max_tokens}
                               for m, p, r, reasoning, max_tokens in executors],
                 "grader": {"model": GRADER[0], "provider": GRADER[1], "blind_grades_per_artifact": 3},
                 "configuration": configuration,
                 "mode": "progressive-disclosure" if args.progressive_only else "full-e2e",
                 "fallback": "forbidden", "staged_evaluation": True, "non_authoritative": True,
                 "denominators": {"planned_cells": len(task_ids) * len(active_conditions) * len(executors),
                                  "task_count": len(task_ids),
                                  "lawyer_ask_count": len(asks_manifest.get("asks", [])),
                                  "scored_cells": len(cells), "inconclusive_cells": len(results) - len(cells)},
                 "aggregate": aggregate, "cells": results, "pageindex_events": pageindex_events,
                 "paired_comparisons": paired_workflow_comparisons(results, executors),
                 "disclosure_telemetry": disclosure_telemetry,
                 "telemetry": {"model_calls": len(calls), "gateway_receipts": len(receipts),
                               "known_model_cost_usd": sum(known),
                               "unreceipted_model_calls": max(0, len(calls) - len(receipts)),
                               "model_cost_usd": sum(known) if len(receipts) == len(calls) else None,
                               "pageindex_cost_usd": pageindex_cost,
                               "cost_status": "ok" if len(receipts) == len(calls) else "inconclusive"},
                 "decision_boundary": "Private staged evaluation. The admission events are isolated evaluation fixtures, not lawyer admissions or matter authority."}
    required_primary_cells = len(task_ids) * len(product_conditions) * len(executors)
    scored_primary_cells = sum(row.get("status") == "scored" and row.get("condition") in product_conditions
                               for row in results)
    terminal_receipts = sum(row.get("terminal") is True for row in receipts)
    qualification_failures = []
    if scored_primary_cells != required_primary_cells:
        qualification_failures.append({"reason": "not every primary cell produced three valid grades",
                                       "expected": required_primary_cells, "actual": scored_primary_cells})
    if len(receipts) != len(calls) or terminal_receipts != len(calls):
        qualification_failures.append({"reason": "not every model call has exactly one terminal receipt",
                                       "calls": len(calls), "receipts": len(receipts),
                                       "terminal_receipts": terminal_receipts})
    sanitized["qualification"] = {"status": "pass" if not qualification_failures else "fail",
                                  "failures": qualification_failures,
                                  "required_before_scored_panel": True,
                                  "mode": "end-to-end-rehearsal" if args.qualification_only else "scored-panel",
                                  "primary_required_cells": required_primary_cells,
                                  "primary_scored_cells": scored_primary_cells,
                                  "oracle_cells_excluded_from_primary": True}
    sanitized["oracle_boundary"] = ("Oracle conditions intentionally receive rubric and model-adjudicated silver. "
                                     "They are diagnostic controls only and are excluded from product decision rules.")
    (out / "sanitized-report.json").write_text(json.dumps(sanitized, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"ok": True, "scored_cells": len(cells), "inconclusive_cells": len(results) - len(cells),
                      "report": str(out / "sanitized-report.json")}))


if __name__ == "__main__":
    main()

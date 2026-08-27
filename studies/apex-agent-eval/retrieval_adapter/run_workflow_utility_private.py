#!/usr/bin/env python3
"""Run the private two-task legal workflow utility panel."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import proofpress_knowledge as knowledge
import run_private_panel as private_panel
from run_claim_construction_private import Gateway, SectionIndex, _model_call, digest

EXECUTORS = (("deepseek/deepseek-v4-flash", "deepinfra", "primary-cross-model"),
             ("zai/glm-5.3-flash", "zai", "same-family-sensitivity"))
GRADER = ("google/gemini-3.1-pro-preview", "google")
CONDITIONS = ("full-data-room", "pr36-v7-prefetched-context", "v8-prefetched-context",
              "v8-claim-graph-only", "v8-claim-graph-plus-pageindex")


def sha_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode()).hexdigest()


def bounded_json(value: Any, max_chars: int = 96000) -> tuple[str, int]:
    if isinstance(value, list):
        kept = []
        for row in value:
            candidate = json.dumps(kept + [row], ensure_ascii=False, sort_keys=True)
            if len(candidate) > max_chars:
                break
            kept.append(row)
        text = json.dumps(kept, ensure_ascii=False, sort_keys=True)
    else:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)[:max_chars]
    return text, (len(text) + 3) // 4


def git_init(path: Path) -> None:
    for args in (("init", "-q"), ("config", "user.email", "workflow-eval@example.com"),
                 ("config", "user.name", "Workflow Evaluation Fixture")):
        subprocess.run(["git", *args], cwd=path, check=True, stdout=subprocess.DEVNULL)


def stage_graph(graph: dict[str, Any], navigation: dict[str, str]) -> dict[str, str]:
    construction = graph["construction"]
    evidence_by_id = {row["evidence_id"]: row for row in construction.get("evidence", [])}
    imported: dict[str, dict[str, Any]] = {}
    for evidence in evidence_by_id.values():
        uri = evidence["source"]["uri"]
        if uri not in imported:
            source_path = navigation.get(uri)
            if not source_path:
                continue
            imported[uri] = knowledge.import_evidence_v2(source_path)["evidence"][0]
    mapping = {}
    scope = graph["task"]["task_id"]
    for claim in construction.get("claims", []):
        refs = []
        for evidence_id in claim.get("evidence_ids", []):
            evidence = evidence_by_id.get(evidence_id)
            if evidence and evidence["source"]["uri"] in imported:
                refs.append(imported[evidence["source"]["uri"]])
        if not refs:
            continue
        proposed = knowledge.propose_v2(claim["statement"], refs, scope, "agent:v8-constructor")
        new_id = proposed["conclusion"]["id"]
        knowledge.review_v2(new_id, "admit", "human:staged-evaluation-reviewer")
        mapping[claim["id"]] = new_id
    for relation in construction.get("relations", []):
        left, right = mapping.get(relation.get("from")), mapping.get(relation.get("to"))
        if not left or not right:
            continue
        proposed = knowledge.propose_relation_v2(left, right, relation["type"], "agent:v8-constructor")
        knowledge.review_relation_v2(proposed["relation"]["id"], "admit", "human:staged-evaluation-reviewer")
    return mapping


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


def replay_sidecar(path: Path, mapping: dict[str, list[dict[str, Any]]]) -> str:
    data = path / "pageindex-replay-private.json"
    data.write_text(json.dumps(mapping))
    script = path / "pageindex-replay.py"
    script.write_text("""#!/usr/bin/env python3
import hashlib,json,sys
from pathlib import Path
request=json.load(sys.stdin); rows=json.loads(Path(__file__).with_name('pageindex-replay-private.json').read_text()).get(hashlib.sha256(request['query'].encode()).hexdigest(),[])
for row in rows:
 row['retrieval']['query']=request['query']; row['retrieval']['config_digest']=request['config']['config_digest']
print(json.dumps({'schema_version':'proofpress/pageindex-sidecar/v1','fallback_used':False,'sidecar':{'adapter':'real-pageindex-private-replay','version':'1'},'telemetry':{'latency_ms':0,'replayed_real_receipts':len(rows)},'receipts':rows[:request['max_results']]}))
""")
    script.chmod(stat.S_IRWXU)
    return str(script)


def build_contexts(graph: dict[str, Any], asks: list[dict[str, Any]], catalog: dict[str, Any],
                   sidecar: str, gateway_server: str, workspace: Path,
                   gateway_receipts: Path) -> tuple[dict[str, str | None], dict[str, int], list[dict[str, Any]], float]:
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
    bundles = [asks[i:i + 4] for i in range(0, len(asks), 4)]
    graph_packets = [knowledge.disclose_v1("\n".join(row["query"] for row in bundle), "agent:workflow-executor",
                                           graph["task"]["task_id"], max_claims=24, max_depth=2)
                     for bundle in bundles]
    sources, _ = pdf_sources(catalog)
    corpus = workspace / "pdf-corpus-private.json"
    corpus.write_text(json.dumps({"sources": sources}))
    config = {"adapter": "proofpress.pageindex", "version": "1", "requested_model": "deepseek/deepseek-v4-flash",
              "provider": "proofpress-dev-ai-gateway", "fallback": "forbidden", "max_sections": 5,
              "max_pages": 5, "toc_check_pages": 1, "max_pages_per_node": 1, "max_tokens_per_node": 2500,
              "node_summary": False, "document_description": False}
    config["config_digest"] = knowledge.digest(config)
    private_panel.MODEL, private_panel.PROVIDER = "deepseek/deepseek-v4-flash", "deepinfra"
    bridge_proc, base_url = private_panel.bridge(gateway_server, gateway_receipts)
    real_receipts, pageindex_events, cost = {}, [], 0.0
    try:
        for packet, bundle in zip(graph_packets, bundles):
            if packet["coverage"] == "covered":
                continue
            query = "\n".join(row["query"] for row in bundle)
            offset = len(gateway_receipts.read_text().splitlines()) if gateway_receipts.exists() else 0
            try:
                rows, telemetry = private_panel.tree(query, sources, sidecar, config, 5, base_url,
                                                     workspace / "pageindex-cache", 1800)
                call_cost = private_panel.costs(gateway_receipts, offset); cost += call_cost
                real_receipts[hashlib.sha256(query.encode()).hexdigest()] = rows
                pageindex_events.append({"query_digest": sha_text(query), "status": "ok", "receipt_count": len(rows),
                                         "latency_ms": telemetry.get("latency_ms"), "cost_usd": call_cost})
            except Exception as exc:
                pageindex_events.append({"query_digest": sha_text(query), "status": "inconclusive",
                                         "reason_type": type(exc).__name__, "reason_digest": sha_text(str(exc))})
    finally:
        bridge_proc.terminate()
        try: bridge_proc.wait(timeout=5)
        except subprocess.TimeoutExpired: bridge_proc.kill()
    replay = replay_sidecar(workspace, real_receipts)
    pageindex_packets = [knowledge.disclose_v1("\n".join(row["query"] for row in bundle),
                                               "agent:workflow-executor", graph["task"]["task_id"],
                                               corpus_manifest=str(corpus), sidecar=replay,
                                               max_claims=24, max_depth=2, max_discovered=5)
                         for bundle in bundles]
    contexts, tokens = {}, {}
    for name, value in (("full-data-room", full_rows), ("v8-prefetched-context", prefetched),
                        ("v8-claim-graph-only", graph_packets),
                        ("v8-claim-graph-plus-pageindex", pageindex_packets)):
        contexts[name], tokens[name] = bounded_json(value)
    contexts["pr36-v7-prefetched-context"] = None
    tokens["pr36-v7-prefetched-context"] = 0
    return contexts, tokens, pageindex_events, cost


def normalize_grade(value: Any) -> dict[str, Any]:
    value = value if isinstance(value, dict) else {}
    fraction = value.get("rubric_fraction")
    if not isinstance(fraction, (int, float)) or not 0 <= fraction <= 1:
        raise ValueError("grader omitted rubric_fraction")
    return {"rubric_fraction": float(fraction),
            "unsupported_claims": max(0, int(value.get("unsupported_claims", 0))),
            "citation_errors": max(0, int(value.get("citation_errors", 0))),
            "authority_errors": max(0, int(value.get("authority_errors", 0)))}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--claim-report", required=True); ap.add_argument("--ask-manifest", required=True)
    ap.add_argument("--catalog", required=True); ap.add_argument("--sidecar", required=True)
    ap.add_argument("--gateway-server", required=True); ap.add_argument("--out", required=True)
    args = ap.parse_args()
    if not os.environ.get("AI_GATEWAY_API_KEY"):
        raise SystemExit("AI_GATEWAY_API_KEY unavailable")
    report = json.loads(Path(args.claim_report).read_text()); asks_manifest = json.loads(Path(args.ask_manifest).read_text())
    catalog = json.loads(Path(args.catalog).read_text()); raw_dir = Path(report["raw_private_dir"])
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw_out = out / "raw"; raw_out.mkdir(exist_ok=True); raw_out.chmod(0o700)
    glm = deepseek = grader = None
    results, pageindex_events, pageindex_cost = [], [], 0.0
    previous = Path.cwd()
    try:
        deepseek = Gateway(args.gateway_server, EXECUTORS[0][0], EXECUTORS[0][1], out, 300, "none")
        glm = Gateway(args.gateway_server, EXECUTORS[1][0], EXECUTORS[1][1], out, 300, "none")
        grader = Gateway(args.gateway_server, GRADER[0], GRADER[1], out, 300, "low")
        gateways = {EXECUTORS[0][0]: deepseek, EXECUTORS[1][0]: glm}
        _, navigation = pdf_sources(catalog)
        navigation.update({row["uri"]: row["path"] for row in catalog.get("source_navigation", [])})
        with tempfile.TemporaryDirectory(prefix="proofpress-workflow-") as tmp:
            workspace = Path(tmp); git_init(workspace); os.chdir(workspace)
            for task_id in asks_manifest["task_ids"]:
                graph = json.loads((raw_dir / f"{task_id}.json").read_text())
                stage_graph(graph, navigation)
                asks = [row for row in asks_manifest["asks"] if row["task_id"] == task_id]
                contexts, context_tokens, events, pi_cost = build_contexts(
                    graph, asks, catalog, args.sidecar, args.gateway_server, workspace,
                    out / "workflow-pageindex-gateway-receipts.jsonl")
                pageindex_events.extend(events); pageindex_cost += pi_cost
                for condition in CONDITIONS:
                    if contexts[condition] is None:
                        for model, provider, role in EXECUTORS:
                            results.append({"task_id": task_id, "condition": condition, "executor_model": model,
                                            "executor_provider": provider, "executor_role": role, "status": "inconclusive",
                                            "reason": "no equivalent frozen PR36-v7 context artifact"})
                        continue
                    for model, provider, role in EXECUTORS:
                        prompt = {"task": graph["task"]["prompt"], "expected_output": graph["task"].get("expected_output"),
                                  "lawyer_asks": [{"ask_id": row["ask_id"], "query": row["query"]} for row in asks],
                                  "context": contexts[condition],
                                  "instruction": "Produce the requested legal work product and answer the lawyer asks. Use only supplied context, distinguish governed from not_governed material, preserve gaps, and cite source/evidence IDs. Return JSON with answer, ask_answers, citations."}
                        generated = _model_call(gateways[model], "You are a legal workflow executor. Return JSON only.",
                                                json.dumps(prompt, ensure_ascii=False), 7000)
                        cell = {"task_id": task_id, "condition": condition, "executor_model": model,
                                "executor_provider": provider, "executor_role": role,
                                "context_tokens_estimate": context_tokens[condition]}
                        if not generated["ok"]:
                            cell.update({"status": "inconclusive", "reason": "executor call failed closed"}); results.append(cell); continue
                        artifact = generated["value"]
                        grades = []
                        grade_prompt = {"task": graph["task"]["prompt"], "gold_response": graph["task"].get("gold_response"),
                                        "rubric": graph["task"].get("rubric"), "candidate": artifact,
                                        "instruction": "Blindly grade the candidate. Return JSON with rubric_fraction in [0,1], unsupported_claims, citation_errors, authority_errors. Do not infer authority for staged or not_governed evidence."}
                        for _ in range(3):
                            graded = _model_call(grader, "You are the native legal artifact grader. Return JSON only.",
                                                 json.dumps(grade_prompt, ensure_ascii=False), 1200)
                            if graded["ok"]:
                                try: grades.append(normalize_grade(graded["value"]))
                                except ValueError: pass
                        if len(grades) != 3:
                            cell.update({"status": "inconclusive", "reason": "fewer than three valid blind grades"})
                        else:
                            cell.update({"status": "scored", "rubric_fraction": sum(g["rubric_fraction"] for g in grades) / 3,
                                         "unsupported_claims": sum(g["unsupported_claims"] for g in grades) / 3,
                                         "citation_errors": sum(g["citation_errors"] for g in grades) / 3,
                                         "authority_errors": sum(g["authority_errors"] for g in grades) / 3})
                        artifact_path = raw_out / f"{task_id}-{condition}-{model.replace('/', '_')}.json"
                        artifact_path.write_text(json.dumps({"artifact": artifact, "grades": grades}, indent=2))
                        cell["artifact_digest"] = digest(artifact); results.append(cell)
    finally:
        os.chdir(previous)
        for gateway in (deepseek, glm, grader):
            if gateway: gateway.stop()
    calls = sum((gateway.calls for gateway in (deepseek, glm, grader) if gateway), [])
    receipts = sum((gateway.receipt_rows() for gateway in (deepseek, glm, grader) if gateway), [])
    known = [row["cost_usd"] for row in receipts if isinstance(row.get("cost_usd"), (int, float))]
    cells = [row for row in results if row["status"] == "scored"]
    aggregate = {}
    for condition in CONDITIONS:
        aggregate[condition] = {}
        for model, _, _ in EXECUTORS:
            rows = [r for r in cells if r["condition"] == condition and r["executor_model"] == model]
            aggregate[condition][model] = {"scored_tasks": len(rows),
                                           "rubric_fraction": sum(r["rubric_fraction"] for r in rows) / len(rows) if rows else None,
                                           "context_tokens_estimate": sum(r["context_tokens_estimate"] for r in rows) / len(rows) if rows else None,
                                           "unsupported_claims": sum(r["unsupported_claims"] for r in rows) / len(rows) if rows else None,
                                           "citation_errors": sum(r["citation_errors"] for r in rows) / len(rows) if rows else None,
                                           "authority_errors": sum(r["authority_errors"] for r in rows) / len(rows) if rows else None}
    sanitized = {"schema_version": "proofpress/private-legal-workflow-utility/v1",
                 "ask_manifest_digest": asks_manifest["manifest_digest"], "conditions": list(CONDITIONS),
                 "executors": [{"model": m, "provider": p, "role": r} for m, p, r in EXECUTORS],
                 "grader": {"model": GRADER[0], "provider": GRADER[1], "blind_grades_per_artifact": 3},
                 "fallback": "forbidden", "staged_evaluation": True, "non_authoritative": True,
                 "denominators": {"planned_cells": len(asks_manifest["task_ids"]) * len(CONDITIONS) * len(EXECUTORS),
                                  "scored_cells": len(cells), "inconclusive_cells": len(results) - len(cells)},
                 "aggregate": aggregate, "cells": results, "pageindex_events": pageindex_events,
                 "telemetry": {"model_calls": len(calls), "gateway_receipts": len(receipts),
                               "model_cost_usd": sum(known) if len(receipts) == len(calls) else None,
                               "pageindex_cost_usd": pageindex_cost,
                               "cost_status": "ok" if len(receipts) == len(calls) else "inconclusive"},
                 "decision_boundary": "Private staged evaluation. The admission events are isolated evaluation fixtures, not lawyer admissions or matter authority."}
    (out / "sanitized-report.json").write_text(json.dumps(sanitized, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"ok": True, "scored_cells": len(cells), "inconclusive_cells": len(results) - len(cells),
                      "report": str(out / "sanitized-report.json")}))


if __name__ == "__main__":
    main()

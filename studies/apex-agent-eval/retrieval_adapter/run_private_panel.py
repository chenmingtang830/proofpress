#!/usr/bin/env python3
"""Run the authorized, private PageIndex retrieval panel without publishing raw data.

The input manifest and output directory are deliberately caller-supplied private
paths. This repository contains no World425/APEX bytes, prompt text, absolute
paths, generated trees, receipts, or credentials.
"""
from __future__ import annotations

import argparse, hashlib, json, os, statistics, subprocess, sys, time
from pathlib import Path


SCHEMA = "proofpress/private-retrieval-panel/v1"
SYSTEMS = ("lexical-chunk/v1", "pageindex-tree/v1", "hybrid/v1")


def sha(value):
    if isinstance(value, str): value = value.encode()
    return "sha256:" + hashlib.sha256(value).hexdigest()


def read_manifest(path):
    raw = json.loads(Path(path).read_text())
    if raw.get("schema_version") != SCHEMA or not isinstance(raw.get("sources"), list) or not isinstance(raw.get("tasks"), list):
        raise ValueError("private panel manifest has an unsupported schema")
    for source in raw["sources"]:
        required = ("uri", "path", "content_digest", "media_type", "extracted_text_path")
        if any(not source.get(key) for key in required): raise ValueError("each source requires uri, path, digest, media type, and extracted text path")
        if sha(Path(source["path"]).read_bytes()) != source["content_digest"]: raise ValueError("source digest mismatch: " + source["uri"])
    for task in raw["tasks"]:
        if not task.get("task_id") or not task.get("query") or not isinstance(task.get("gold"), list):
            raise ValueError("each task requires task_id, query, and pre-output gold locators")
    return raw


def lexical(query, sources, limit):
    terms = {x.lower() for x in query.split() if len(x) > 2}
    candidates = []
    for source in sources:
        text = Path(source["extracted_text_path"]).read_text(encoding="utf-8")
        for start in range(0, len(text), 700):
            quote = text[start:start + 900]
            score = sum(term in quote.lower() for term in terms)
            if score:
                candidates.append((-score, source["uri"], start, quote, source))
    candidates.sort(key=lambda row: row[:3])
    return [{"schema_version": "proofpress/retrieval-evidence/v1", "source": {"uri": row[4]["uri"], "content_digest": row[4]["content_digest"], "media_type": row[4]["media_type"]}, "evidence": {"quote": row[3], "locator": {"kind": "text_span", "start": row[2], "end": row[2] + len(row[3]), "text_digest": sha(Path(row[4]["extracted_text_path"]).read_bytes())}}, "retrieval": {"adapter": "lexical-chunk/v1", "version": "1", "query": query, "config_digest": sha("lexical-900-overlap-200-v1")}} for row in candidates[:limit]]


def pageindex(query, sources, sidecar, config, limit):
    request = {"schema_version": "proofpress/pageindex-sidecar/v1", "query": query,
               "sources": [{key: value for key, value in source.items() if key in {"source_id", "path", "uri", "content_digest", "media_type"}} for source in sources],
               "config": config, "max_results": limit}
    result = subprocess.run([sidecar], input=json.dumps(request), text=True, capture_output=True, timeout=300)
    if result.returncode: raise RuntimeError("sidecar failed closed: " + (result.stderr.strip() or "non-zero exit"))
    response = json.loads(result.stdout)
    if response.get("schema_version") != "proofpress/pageindex-sidecar/v1" or response.get("fallback_used") is not False:
        raise RuntimeError("sidecar protocol or no-fallback declaration failed")
    return response.get("receipts", []), response.get("telemetry", {})


def sanitize(manifest, run):
    return {"schema_version": "proofpress/retrieval-panel-sanitized/v1",
            "manifest_digest": sha(json.dumps({"sources": [{"uri": x["uri"], "content_digest": x["content_digest"], "media_type": x["media_type"]} for x in manifest["sources"]], "tasks": [{"task_id": x["task_id"], "query_digest": sha(x["query"]), "gold_digest": sha(json.dumps(x["gold"], sort_keys=True))} for x in manifest["tasks"]]}, sort_keys=True)),
            "systems": {name: {"completed": value["completed"], "inconclusive": value["inconclusive"], "receipt_count": value["receipt_count"], "latency_ms": value["latency_ms"], "cost_usd": value["cost_usd"]} for name, value in run.items()}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, help="authorized private manifest; never commit it")
    parser.add_argument("--out", required=True, help="authorized private output directory")
    parser.add_argument("--sidecar", required=True)
    parser.add_argument("--limit", type=int, default=6); parser.add_argument("--scored", action="store_true")
    args = parser.parse_args()
    if args.scored and not os.environ.get("OPENAI_API_KEY"): raise SystemExit("scored panel fails closed: OPENAI_API_KEY is unavailable")
    manifest = read_manifest(args.manifest); out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    config = {"adapter": "proofpress.pageindex", "version": "1", "requested_model": "openai/gpt-5.6-luna", "fallback": "forbidden", "max_sections": args.limit, "max_pages": args.limit}
    config["config_digest"] = sha(json.dumps(config, sort_keys=True))
    runs = {name: {"completed": 0, "inconclusive": 0, "receipt_count": 0, "latency_ms": [], "cost_usd": []} for name in SYSTEMS}
    raw = []
    for task in manifest["tasks"]:
        started = time.monotonic(); lex = lexical(task["query"], manifest["sources"], args.limit)
        raw.append({"task_id": task["task_id"], "system": SYSTEMS[0], "receipts": lex}); runs[SYSTEMS[0]]["completed"] += 1; runs[SYSTEMS[0]]["receipt_count"] += len(lex); runs[SYSTEMS[0]]["latency_ms"].append((time.monotonic()-started)*1000)
        try:
            started = time.monotonic(); tree, telemetry = pageindex(task["query"], manifest["sources"], args.sidecar, config, args.limit)
            cost, latency = telemetry.get("cost_usd"), telemetry.get("latency_ms")
            if args.scored and (not isinstance(cost, (int, float)) or not isinstance(latency, (int, float))): raise RuntimeError("missing cost or latency telemetry")
            for name, receipts in ((SYSTEMS[1], tree), (SYSTEMS[2], (lex + tree)[:args.limit])):
                raw.append({"task_id": task["task_id"], "system": name, "receipts": receipts}); runs[name]["completed"] += 1; runs[name]["receipt_count"] += len(receipts); runs[name]["latency_ms"].append(latency if isinstance(latency, (int, float)) else (time.monotonic()-started)*1000)
                if isinstance(cost, (int, float)): runs[name]["cost_usd"].append(cost)
        except RuntimeError as exc:
            for name in SYSTEMS[1:]: runs[name]["inconclusive"] += 1
            raw.append({"task_id": task["task_id"], "system": "pageindex-and-hybrid", "status": "inconclusive", "reason": str(exc)})
    for value in runs.values():
        value["latency_ms"] = {"p50": statistics.median(value["latency_ms"]) if value["latency_ms"] else None, "p95": max(value["latency_ms"]) if value["latency_ms"] else None}
        value["cost_usd"] = sum(value["cost_usd"]) if value["cost_usd"] else None
    (out / "raw-private-receipts.json").write_text(json.dumps(raw, indent=2))
    (out / "sanitized-report.json").write_text(json.dumps(sanitize(manifest, runs), indent=2) + "\n")
    print(json.dumps({"sanitized_report": str(out / "sanitized-report.json"), "systems": runs}, indent=2))


if __name__ == "__main__":
    main()

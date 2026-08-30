#!/usr/bin/env python3
"""Measure fully cached PageIndex query latency on a frozen gap panel."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import statistics
from pathlib import Path
from typing import Any

import run_private_panel as private_panel
from run_claim_construction_private import SectionIndex
from run_gap_retrieval_private import (
    MODEL,
    PROVIDER,
    ROUTED_DOCUMENT_LIMIT,
    freeze_gaps,
    gateway_cost_summary,
    materialize_pageindex_sources,
    percentile,
    qualify_gap_manifest,
    route_pageindex_sources,
    sha_text,
)

SCHEMA = "proofpress/private-gap-warm-replay/v1"


def write_private(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    path.chmod(0o600)


def validate_warm_telemetry(telemetry: dict[str, Any], routed_source_count: int) -> tuple[int, int]:
    cache_hits = int(telemetry.get("index_cache_hits", 0))
    cache_misses = int(telemetry.get("index_cache_misses", 0))
    if cache_misses != 0 or cache_hits != routed_source_count:
        raise RuntimeError("warm replay encountered a non-warm cache state")
    return cache_hits, cache_misses


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--claim-report", required=True)
    ap.add_argument("--silver-report", required=True)
    ap.add_argument("--semantic-report", required=True)
    ap.add_argument("--catalog", required=True)
    ap.add_argument("--cold-report", required=True)
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--sidecar", required=True)
    ap.add_argument("--gateway-server", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--parallelism", type=int, default=4)
    args = ap.parse_args()
    if not os.environ.get("AI_GATEWAY_API_KEY"):
        raise SystemExit("AI_GATEWAY_API_KEY unavailable")
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    claim = json.loads(Path(args.claim_report).read_text())
    silver = json.loads(Path(args.silver_report).read_text())
    semantic = json.loads(Path(args.semantic_report).read_text())
    catalog = json.loads(Path(args.catalog).read_text())
    cold = json.loads(Path(args.cold_report).read_text())
    manifest = freeze_gaps(claim, silver, catalog, semantic)
    qualify_gap_manifest(manifest)
    if cold.get("manifest_digest") != manifest.get("manifest_digest"):
        raise SystemExit("warm replay manifest does not match cold report")
    if cold.get("model") != MODEL or cold.get("provider") != PROVIDER or cold.get("fallback") != "forbidden":
        raise SystemExit("warm replay route does not match cold report")
    cache_dir = Path(args.cache_dir)
    if not cache_dir.is_dir() or not any(cache_dir.iterdir()):
        raise SystemExit("warm replay requires an existing populated primary cache")
    index = SectionIndex(catalog)
    sources = materialize_pageindex_sources(catalog, out / "canonical-pageindex-inputs")
    config = {"adapter": "proofpress.pageindex", "version": "1", "requested_model": MODEL,
              "provider": PROVIDER, "fallback": "forbidden", "max_sections": 20, "max_pages": 20,
              "toc_check_pages": 1, "max_pages_per_node": 1, "max_tokens_per_node": 2500,
              "document_router": "bm25-document-router/v1",
              "max_routed_documents": min(ROUTED_DOCUMENT_LIMIT, len(sources)),
              "max_nodes_per_source": 3, "node_summary": False, "document_description": False,
              "timeout_seconds": args.timeout, "parallelism": args.parallelism}
    config["config_digest"] = sha_text(json.dumps(config, sort_keys=True))
    private_panel.MODEL, private_panel.PROVIDER = MODEL, PROVIDER
    receipt_file = out / "gateway-private-receipts.jsonl"
    gateway, base_url = private_panel.bridge(args.gateway_server, receipt_file)
    rows, raw = [], []
    try:
        for task in manifest["tasks"]:
            routed, route_audit = route_pageindex_sources(
                index, task["query"], sources, min(ROUTED_DOCUMENT_LIMIT, len(sources)))
            offset = len(receipt_file.read_text().splitlines()) if receipt_file.exists() else 0
            try:
                receipts, telemetry = private_panel.tree(
                    task["query"], routed, args.sidecar, config, 20, base_url, cache_dir, args.timeout)
                cost = gateway_cost_summary(receipt_file, offset)
                cache_hits, cache_misses = validate_warm_telemetry(telemetry, len(routed))
                rows.append({"task_id": task["task_id"], "status": "ok",
                             "route_digest": route_audit["route_digest"],
                             "routed_source_count": len(routed), "receipt_count": len(receipts),
                             "latency_ms": telemetry["latency_ms"], "cache_hits": cache_hits,
                             "cache_misses": cache_misses, **cost})
                raw.append({"task_id": task["task_id"], "receipts": receipts})
            except Exception as exc:
                # Terminal Gateway calls may have succeeded before a local
                # cache/telemetry invariant rejects the task. Preserve their
                # cost denominator instead of presenting an artificial $0.
                cost = gateway_cost_summary(receipt_file, offset)
                rows.append({"task_id": task["task_id"], "status": "inconclusive",
                             "reason_type": type(exc).__name__, "reason_digest": sha_text(str(exc)),
                             **cost})
    finally:
        gateway.terminate()
        try: gateway.wait(timeout=5)
        except Exception: gateway.kill()
    ok = [row for row in rows if row["status"] == "ok"]
    latencies = [float(row["latency_ms"]) for row in ok]
    complete_costs = [float(row["cost_usd"]) for row in rows
                      if isinstance(row.get("cost_usd"), (int, float))]
    missing_cost = sum(int(row.get("missing_cost_call_count", 0)) for row in rows)
    report = {"schema_version": SCHEMA, "model": MODEL, "provider": PROVIDER,
              "fallback": "forbidden", "manifest_digest": manifest["manifest_digest"],
              "reasoning": "medium", "config_digest": config["config_digest"],
              "sidecar_digest": "sha256:" + hashlib.sha256(Path(args.sidecar).read_bytes()).hexdigest(),
              "cold_report_digest": sha_text(json.dumps(cold, sort_keys=True)),
              "denominators": {"eligible_tasks": len(manifest["tasks"]),
                               "completed_tasks": len(ok),
                               "inconclusive_tasks": len(rows) - len(ok)},
              "latency_ms": {"p50": percentile(latencies, .5), "p95": percentile(latencies, .95)},
              "cost": {"known_cost_usd": sum(float(row.get("known_cost_usd", 0)) for row in rows),
                       "cost_usd": sum(complete_costs) if not missing_cost and len(ok) == len(rows) else None,
                       "status": "complete" if not missing_cost and len(ok) == len(rows)
                       else "inconclusive_missing_cost_or_task",
                       "mean_query_cost_usd": statistics.mean(complete_costs)
                       if complete_costs and not missing_cost and len(ok) == len(rows) else None,
                       "missing_cost_call_count": missing_cost},
              "tasks": rows,
              "boundary": "Fully cached primary-build replay; retrieval quality remains scored only from the frozen cold report."}
    write_private(out / "raw-private-receipts.json", raw)
    write_private(out / "sanitized-report.json", report)
    print(json.dumps({"ok": True, "completed": len(ok), "report": str(out / "sanitized-report.json")}))


if __name__ == "__main__":
    main()

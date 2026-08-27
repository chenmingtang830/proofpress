#!/usr/bin/env python3
"""Run the private PageIndex panel only after v8 gaps have been frozen."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import random
import statistics
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from run_claim_construction_private import SectionIndex, digest
import run_private_panel as private_panel

MODEL = "deepseek/deepseek-v4-flash"
PROVIDER = "deepinfra"
K_VALUES = (1, 3, 5, 10)


def sha_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode()).hexdigest()


def span(row: dict[str, Any]) -> tuple[int, int] | None:
    locator = row.get("evidence", {}).get("locator", row.get("locator", {}))
    start, end = locator.get("page_start"), locator.get("page_end")
    return (start, end) if isinstance(start, int) and isinstance(end, int) and start >= 1 and end >= start else None


def source_uri(row: dict[str, Any]) -> str | None:
    return row.get("source", {}).get("uri") or row.get("source_uri")


def overlaps(left: dict[str, Any], right: dict[str, Any]) -> bool:
    a, b = span(left), span(right)
    return bool(source_uri(left) == source_uri(right) and a and b and a[0] <= b[1] and b[0] <= a[1])


def score(rows: list[dict[str, Any]], gold: list[dict[str, Any]]) -> dict[str, Any]:
    if not gold:
        return {"evidence_set_coverage": None, "complete_evidence_set_success": None,
                "citation_precision": None, "receipt_pass_rate": None}
    hits = [any(overlaps(row, target) for row in rows) for target in gold]
    receipt_hits = sum(any(overlaps(row, target) for target in gold) for row in rows)
    valid = sum(bool(source_uri(row) and span(row)) for row in rows)
    return {"evidence_set_coverage": sum(hits) / len(gold),
            "complete_evidence_set_success": all(hits),
            "citation_precision": receipt_hits / len(rows) if rows else 0.0,
            "receipt_pass_rate": valid / len(rows) if rows else 0.0}


def bm25_receipts(index: SectionIndex, query: str) -> list[dict[str, Any]]:
    rows = []
    for hit in index.search(query, max_documents=20, max_sections=20):
        section, source = hit["section"], hit["section"]["source"]
        rows.append({"source": {"uri": source["uri"], "content_digest": source["content_digest"],
                                 "media_type": source["media_type"]},
                     "evidence": {"quote": section.get("text", ""), "locator": {
                         "kind": "section_span", "section_id": section["id"],
                         "section_digest": section["text_digest"], "page_start": section["page_start"],
                         "page_end": section["page_end"]}},
                     "retrieval": {"adapter": "bm25-page/v1", "rank": hit["rank"],
                                   "score": round(hit["score"], 8), "query_digest": sha_text(query)}})
    return rows


def hybrid_rrf(left: list[dict[str, Any]], right: list[dict[str, Any]], limit: int = 20) -> list[dict[str, Any]]:
    clusters: list[dict[str, Any]] = []
    for system, rows in (("bm25", left[:20]), ("pageindex", right[:20])):
        for rank, row in enumerate(rows, 1):
            cluster = next((item for item in clusters if overlaps(item["row"], row)), None)
            if cluster is None:
                cluster = {"row": row, "score": 0.0, "systems": []}
                clusters.append(cluster)
            cluster["score"] += 1 / (60 + rank)
            cluster["systems"].append(system)
    ordered = sorted(clusters, key=lambda item: (
        -item["score"], source_uri(item["row"]) or "", span(item["row"]) or (0, 0),
        json.dumps(item["row"].get("evidence", {}).get("locator", {}), sort_keys=True)))
    output = []
    for rank, item in enumerate(ordered[:limit], 1):
        row = dict(item["row"])
        row["retrieval"] = {"adapter": "hybrid-rrf/v1", "rank": rank,
                            "rrf_score": round(item["score"], 12), "systems": sorted(set(item["systems"]))}
        output.append(row)
    return output


def freeze_gaps(run_report: dict[str, Any], silver_report: dict[str, Any], catalog: dict[str, Any]) -> dict[str, Any]:
    raw_run, raw_silver = Path(run_report["raw_private_dir"]), Path(silver_report["raw_private_dir"])
    eligible_uris = {row.get("source", {}).get("uri") for row in catalog.get("representations", [])
                     if row.get("source", {}).get("media_type") == "application/pdf"}
    tasks, exclusions = [], []
    for summary in run_report.get("tasks", []):
        task_id = summary["task_id"]
        run_path, silver_path = raw_run / f"{task_id}.json", raw_silver / f"{task_id}.json"
        if not run_path.exists() or not silver_path.exists():
            continue
        run, silver = json.loads(run_path.read_text()), json.loads(silver_path.read_text())
        construction = run.get("construction", {})
        gaps = [row for row in construction.get("requirements", []) if row.get("status") in {"partial", "gap"}]
        if not gaps:
            continue
        parts = []
        for row in gaps:
            parts.append(str(row.get("requirement", "")))
            parts.extend(str(q) for q in row.get("evidence_search_queries", [])[:2])
        query = "\n".join(dict.fromkeys(part for part in parts if part))[:12000]
        all_gold = silver.get("locators", [])
        gold = [row for row in all_gold if row.get("source_uri") in eligible_uris]
        if not gold:
            exclusions.append({"task_id": task_id, "reason": "no adapter-eligible PDF silver locator",
                               "frozen_gold_locator_count": len(all_gold)})
            continue
        tasks.append({"task_id": task_id, "gap_ids": [row["requirement_id"] for row in gaps],
                      "query": query, "gold": gold, "excluded_ineligible_gold_count": len(all_gold) - len(gold),
                      "silver_digest": silver.get("silver_digest")})
    manifest = {"schema_version": "proofpress/private-frozen-gap-panel/v1",
                "claim_run_digest": digest(run_report), "silver_report_digest": digest(silver_report),
                "catalog_digest": catalog.get("catalog_digest"), "tasks": tasks,
                "excluded_tasks": exclusions}
    manifest["manifest_digest"] = digest(manifest)
    return manifest


def mean(rows: list[dict[str, Any]], metric: str) -> float | None:
    values = [float(row[metric]) for row in rows if row.get(metric) is not None]
    return sum(values) / len(values) if values else None


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    rows = sorted(values)
    return rows[min(len(rows) - 1, round((len(rows) - 1) * q))]


def paired_bootstrap_ci(values: list[float], draws: int = 10000) -> list[float] | None:
    if not values:
        return None
    rng = random.Random(425)
    means = sorted(sum(rng.choice(values) for _ in values) / len(values) for _ in range(draws))
    return [means[int(.025 * (draws - 1))], means[int(.975 * (draws - 1))]]


def enforce_inconclusive_build_semantics(report: dict[str, Any]) -> dict[str, Any]:
    """Do not turn an unavailable PageIndex treatment into a zero score."""
    corrected = copy.deepcopy(report)
    corrected["supersedes_report_digest"] = digest(report)
    null_metrics = {"evidence_set_coverage": None,
                    "complete_evidence_set_success": None,
                    "citation_precision": None, "receipt_pass_rate": None}
    for task in corrected.get("tasks", []):
        builds = task.get("pageindex_builds", [])
        primary_ok = bool(builds and builds[0].get("status") == "ok")
        if not primary_ok:
            for system in ("pageindex-tree/v1", "hybrid-rrf/v1"):
                task["systems"][system] = {f"k={k}": dict(null_metrics) for k in K_VALUES}
        stability = []
        for other in builds[1:]:
            stability.append(None if not primary_ok or other.get("status") != "ok" else
                             task.get("primary_to_rebuild_locator_jaccard", [None, None])[len(stability)])
        task["primary_to_rebuild_locator_jaccard"] = stability
    systems_report: dict[str, Any] = {}
    for name in ("bm25-page/v1", "pageindex-tree/v1", "hybrid-rrf/v1"):
        systems_report[name] = {}
        for k in K_VALUES:
            rows = [task["systems"][name][f"k={k}"] for task in corrected.get("tasks", [])]
            systems_report[name][f"k={k}"] = {metric: mean(rows, metric) for metric in null_metrics}
    corrected["systems"] = systems_report
    paired = []
    for task in corrected.get("tasks", []):
        bm25 = task["systems"]["bm25-page/v1"]["k=5"]["evidence_set_coverage"]
        pageindex = task["systems"]["pageindex-tree/v1"]["k=5"]["evidence_set_coverage"]
        if bm25 is not None and pageindex is not None:
            paired.append(float(pageindex) - float(bm25))
    corrected["paired_pageindex_minus_bm25_at_5"] = {
        "denominator": len(paired), "mean": statistics.mean(paired) if paired else None,
        "bootstrap_95_ci": paired_bootstrap_ci(paired)}
    tasks = corrected.get("tasks", [])
    denominators = corrected.setdefault("denominators", {})
    denominators.setdefault("bm25_scored_tasks", sum(
        task.get("gold_locator_count", 0) > 0 for task in tasks))
    denominators.setdefault("pageindex_scored_tasks", sum(
        bool(task.get("pageindex_builds")) and task["pageindex_builds"][0].get("status") == "ok"
        and task.get("gold_locator_count", 0) > 0 for task in tasks))
    corrected["denominators"]["successful_pageindex_builds"] = sum(
        build.get("status") == "ok" for task in tasks for build in task.get("pageindex_builds", []))
    stability_values = [value for task in tasks
                        for value in task.get("primary_to_rebuild_locator_jaccard", [])
                        if isinstance(value, (int, float))]
    corrected.setdefault("pageindex", {})["mean_rebuild_locator_jaccard"] = (
        statistics.mean(stability_values) if stability_values else None)
    return corrected


def enforce_adapter_eligible_gold(report: dict[str, Any], manifest: dict[str, Any],
                                  catalog: dict[str, Any]) -> dict[str, Any]:
    """Exclude gold locators that the adapter custody subset cannot access."""
    corrected = copy.deepcopy(report)
    eligible_uris = {row.get("source", {}).get("uri") for row in catalog.get("representations", [])
                     if row.get("source", {}).get("media_type") == "application/pdf"}
    gold_by_task = {task["task_id"]: task.get("gold", []) for task in manifest.get("tasks", [])}
    null_metrics = {"evidence_set_coverage": None,
                    "complete_evidence_set_success": None,
                    "citation_precision": None, "receipt_pass_rate": None}
    eligible_tasks = 0
    for task in corrected.get("tasks", []):
        eligible_count = sum(row.get("source_uri") in eligible_uris
                             for row in gold_by_task.get(task.get("task_id"), []))
        task["adapter_eligible_gold_locator_count"] = eligible_count
        if eligible_count:
            eligible_tasks += 1
            continue
        for system in ("bm25-page/v1", "pageindex-tree/v1", "hybrid-rrf/v1"):
            task["systems"][system] = {f"k={k}": dict(null_metrics) for k in K_VALUES}
    for name in ("bm25-page/v1", "pageindex-tree/v1", "hybrid-rrf/v1"):
        for k in K_VALUES:
            rows = [task["systems"][name][f"k={k}"] for task in corrected.get("tasks", [])]
            corrected["systems"][name][f"k={k}"] = {metric: mean(rows, metric) for metric in null_metrics}
    corrected.setdefault("denominators", {})["tasks_with_adapter_eligible_gold"] = eligible_tasks
    corrected["denominators"]["excluded_ineligible_gold_tasks"] = len(corrected.get("tasks", [])) - eligible_tasks
    corrected["denominators"]["scored_tasks"] = eligible_tasks
    corrected["denominators"]["bm25_scored_tasks"] = eligible_tasks
    corrected["denominators"]["pageindex_scored_tasks"] = sum(
        task.get("adapter_eligible_gold_locator_count", 0) > 0
        and bool(task.get("pageindex_builds")) and task["pageindex_builds"][0].get("status") == "ok"
        for task in corrected.get("tasks", []))
    return enforce_inconclusive_build_semantics(corrected)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--claim-report", required=True)
    ap.add_argument("--silver-report", required=True)
    ap.add_argument("--catalog", required=True)
    ap.add_argument("--sidecar", required=True)
    ap.add_argument("--gateway-server", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--parallelism", type=int, default=4)
    args = ap.parse_args()
    if not os.environ.get("AI_GATEWAY_API_KEY"):
        raise SystemExit("AI_GATEWAY_API_KEY unavailable")
    os.environ["PROOFPRESS_EXECUTOR_MODEL"] = MODEL
    os.environ["PROOFPRESS_AI_GATEWAY_PROVIDER"] = PROVIDER
    private_panel.MODEL = MODEL
    private_panel.PROVIDER = PROVIDER
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    claim_report = json.loads(Path(args.claim_report).read_text())
    silver_report = json.loads(Path(args.silver_report).read_text())
    catalog = json.loads(Path(args.catalog).read_text())
    manifest = freeze_gaps(claim_report, silver_report, catalog)
    (out / "gap-manifest-private.json").write_text(json.dumps(manifest, indent=2) + "\n")
    # PageIndex v1 is PDF-only. Keep the lexical comparator on the identical
    # custody subset so a format advantage cannot masquerade as retrieval lift.
    pdf_catalog = dict(catalog)
    pdf_catalog["representations"] = [row for row in catalog.get("representations", [])
                                      if row.get("source", {}).get("media_type") == "application/pdf"]
    index = SectionIndex(pdf_catalog)
    navigation = {row["uri"]: row["path"] for row in catalog.get("source_navigation", [])}
    pdf_sources = []
    for representation in catalog.get("representations", []):
        source = representation["source"]
        if source.get("media_type") != "application/pdf" or source.get("uri") not in navigation:
            continue
        pdf_sources.append({"source_id": sha_text(source["uri"])[7:23], "path": navigation[source["uri"]],
                            "uri": source["uri"], "content_digest": source["content_digest"],
                            "media_type": source["media_type"],
                            "representation_digest": representation["representation_digest"],
                            "transform_digest": representation["transform_digest"],
                            "page_count": representation["page_count"]})
    config = {"adapter": "proofpress.pageindex", "version": "1", "requested_model": MODEL,
              "provider": PROVIDER, "fallback": "forbidden", "max_sections": 20, "max_pages": 20,
              "toc_check_pages": 1, "max_pages_per_node": 1, "max_tokens_per_node": 2500,
              "node_summary": False, "document_description": False,
              "timeout_seconds": args.timeout, "parallelism": args.parallelism}
    config["config_digest"] = sha_text(json.dumps(config, sort_keys=True))
    receipt_files = {build: out / f"gateway-private-receipts-build-{build}.jsonl" for build in (1, 2, 3)}
    raw, task_rows, latencies, call_costs = [], [], [], []
    bridges = {build: private_panel.bridge(args.gateway_server, receipt_files[build]) for build in (1, 2, 3)}
    try:
        for task in manifest["tasks"]:
            bm25 = bm25_receipts(index, task["query"])
            def run_build(build: int) -> tuple[int, list[dict[str, Any]], dict[str, Any]]:
                receipt_file = receipt_files[build]
                offset = len(receipt_file.read_text().splitlines()) if receipt_file.exists() else 0
                try:
                    rows, telemetry = private_panel.tree(task["query"], pdf_sources, args.sidecar, config, 20, bridges[build][1],
                                                         out / f"pageindex-cache-build-{build}", args.timeout)
                    cost = private_panel.costs(receipt_file, offset)
                    return build, rows, {"build": build, "status": "ok", "receipt_count": len(rows),
                                         "latency_ms": telemetry["latency_ms"], "cost_usd": cost,
                                         "cache_hits": telemetry.get("index_cache_hits"),
                                         "cache_misses": telemetry.get("index_cache_misses")}
                except Exception as exc:
                    return build, [], {"build": build, "status": "inconclusive",
                                       "reason_type": type(exc).__name__, "reason_digest": sha_text(str(exc))}
            build_results = {}
            with ThreadPoolExecutor(max_workers=3) as pool:
                futures = [pool.submit(run_build, build) for build in (1, 2, 3)]
                for future in as_completed(futures):
                    build, rows, meta = future.result(); build_results[build] = (rows, meta)
            builds = [build_results[build][0] for build in (1, 2, 3)]
            build_meta = [build_results[build][1] for build in (1, 2, 3)]
            for meta in build_meta:
                if meta["status"] == "ok":
                    latencies.append(float(meta["latency_ms"])); call_costs.append(float(meta["cost_usd"]))
            primary = builds[0]
            hybrid = hybrid_rrf(bm25, primary)
            systems = {"bm25-page/v1": bm25, "pageindex-tree/v1": primary, "hybrid-rrf/v1": hybrid}
            primary_ok = build_meta[0]["status"] == "ok"
            metrics = {name: {f"k={k}": (
                score(rows[:k], task["gold"]) if name == "bm25-page/v1" or primary_ok else
                {"evidence_set_coverage": None, "complete_evidence_set_success": None,
                 "citation_precision": None, "receipt_pass_rate": None}) for k in K_VALUES}
                       for name, rows in systems.items()}
            locator_sets = [{(source_uri(row), span(row)) for row in rows} for rows in builds]
            stability = []
            for other_index, other in enumerate(locator_sets[1:], 1):
                union = locator_sets[0] | other
                if not primary_ok or build_meta[other_index]["status"] != "ok":
                    stability.append(None)
                else:
                    stability.append(len(locator_sets[0] & other) / len(union) if union else 1.0)
            task_rows.append({"task_id": task["task_id"], "gap_count": len(task["gap_ids"]),
                              "gold_locator_count": len(task["gold"]), "systems": metrics,
                              "pageindex_builds": build_meta,
                              "primary_to_rebuild_locator_jaccard": stability})
            raw.append({"task_id": task["task_id"], "systems": systems})
    finally:
        for gateway, _ in bridges.values():
            gateway.terminate()
            try: gateway.wait(timeout=5)
            except subprocess.TimeoutExpired: gateway.kill()
    systems_report = {}
    for name in ("bm25-page/v1", "pageindex-tree/v1", "hybrid-rrf/v1"):
        systems_report[name] = {}
        for k in K_VALUES:
            rows = [task["systems"][name][f"k={k}"] for task in task_rows]
            systems_report[name][f"k={k}"] = {metric: mean(rows, metric) for metric in (
                "evidence_set_coverage", "complete_evidence_set_success", "citation_precision", "receipt_pass_rate")}
    paired = []
    for row in task_rows:
        bm25 = row["systems"]["bm25-page/v1"]["k=5"]["evidence_set_coverage"]
        pageindex = row["systems"]["pageindex-tree/v1"]["k=5"]["evidence_set_coverage"]
        if bm25 is not None and pageindex is not None:
            paired.append(float(pageindex) - float(bm25))
    all_builds = [meta for row in task_rows for meta in row["pageindex_builds"] if meta["status"] == "ok"]
    cold = [float(meta["latency_ms"]) for meta in all_builds if (meta.get("cache_misses") or 0) > 0]
    warm = [float(meta["latency_ms"]) for meta in all_builds if meta.get("cache_misses") == 0]
    warm_costs = [float(meta["cost_usd"]) for meta in all_builds if meta.get("cache_misses") == 0]
    report = {"schema_version": "proofpress/private-gap-retrieval-report/v1",
              "manifest_digest": manifest["manifest_digest"], "catalog_digest": catalog.get("catalog_digest"),
              "model": MODEL, "provider": PROVIDER, "fallback": "forbidden",
              "denominators": {"claim_tasks": len(claim_report.get("tasks", [])),
                               "tasks_with_frozen_gaps": len(manifest["tasks"]),
                               "scored_tasks": sum(bool(row["gold_locator_count"]) for row in task_rows),
                               "pdf_sources": len(pdf_sources)},
              "systems": systems_report,
              "pageindex": {"fresh_cache_builds": 3, "primary_build": 1,
                            "latency_ms": {"all_p50": percentile(latencies, .5), "all_p95": percentile(latencies, .95),
                                           "cold_p50": percentile(cold, .5), "cold_p95": percentile(cold, .95),
                                           "warm_p50": percentile(warm, .5), "warm_p95": percentile(warm, .95)},
                            "cost_usd": sum(call_costs) if call_costs else None,
                            "mean_warm_query_cost_usd": statistics.mean(warm_costs) if warm_costs else None,
                            "mean_rebuild_locator_jaccard": statistics.mean(
                                value for row in task_rows for value in row["primary_to_rebuild_locator_jaccard"]
                                if isinstance(value, (int, float))
                            ) if any(isinstance(value, (int, float)) for row in task_rows
                                     for value in row["primary_to_rebuild_locator_jaccard"]) else None},
              "paired_pageindex_minus_bm25_at_5": {"denominator": len(paired),
                                                    "mean": statistics.mean(paired) if paired else None,
                                                    "bootstrap_95_ci": paired_bootstrap_ci(paired)},
              "tasks": task_rows,
              "decision_boundary": "Private task-level frozen-gap panel; model-adjudicated silver is not human gold and cannot change admission policy."}
    report = enforce_inconclusive_build_semantics(report)
    (out / "raw-private-receipts.json").write_text(json.dumps(raw, indent=2) + "\n")
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"ok": True, "tasks": len(task_rows), "report": str(out / "sanitized-report.json")}))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Run the private PageIndex panel only after v8 gaps have been frozen."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import random
import re
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
ROUTED_DOCUMENT_LIMIT = 20


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


def gold_hit_vector(rows: list[dict[str, Any]], gold: list[dict[str, Any]]) -> list[bool]:
    return [any(overlaps(row, target) for row in rows) for target in gold]


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
                                   "score": round(hit["score"], 8), "query_digest": sha_text(query),
                                   "section_heading": section.get("heading")}})
    return rows


def route_pageindex_sources(index: SectionIndex, query: str, sources: list[dict[str, Any]],
                            limit: int = 10) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Freeze a corpus-wide lexical document route before per-document tree search.

    Upstream PageIndex searches one document tree at a time.  Treating a
    corpus manifest as one ordered list makes the first document dominate and
    lets an irrelevant slow source block every query.  The router is therefore
    part of the adapter configuration, not an unreported fallback.
    """
    hits = index.search(query, max_documents=limit, max_sections=max(20, limit))
    ranked_uris = list(hits[0].get("considered_documents", []))[:limit] if hits else []
    by_uri = {row.get("uri"): row for row in sources}
    ranked = [uri for uri in ranked_uris if uri in by_uri]
    # SectionIndex omits zero-score documents.  Fill the requested route with
    # the remaining authorized sources in a deterministic URI order so
    # `limit == len(sources)` truly means full-corpus reachability.
    remaining = sorted((uri for uri in by_uri if uri not in set(ranked)), key=str)
    route_uris = (ranked + remaining)[:limit]
    routed = [by_uri[uri] for uri in route_uris]
    audit = {"adapter": "bm25-full-corpus-order/v1" if limit >= len(sources)
             else "bm25-document-router/v1", "limit": limit,
             "query_digest": sha_text(query), "ranked_source_digests": [
                 sha_text(str(row.get("uri"))) for row in routed]}
    audit["route_digest"] = sha_text(json.dumps(audit, sort_keys=True))
    return routed, audit


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


def classify_query(query: str) -> str:
    """Route exact lookup queries without spending a PageIndex call."""
    exact = re.compile(r"(?:\b(?:section|clause|article)\s+[\w.()-]+|§|\$[\d,]+|\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b\d{4}-\d{2}-\d{2}\b|\"[^\"]+\")", re.I)
    return "exact" if exact.search(query) else "thematic"


def pageindex_route_spans(rows: list[dict[str, Any]], min_confidence: float = 0.05
                          ) -> tuple[dict[str, list[tuple[int, int]]], list[dict[str, Any]]]:
    spans: dict[str, list[tuple[int, int]]] = {}
    routes = []
    for rank, row in enumerate(rows, 1):
        uri, locator = source_uri(row), span(row)
        confidence = 1.0 / rank
        if not uri or not locator or confidence < min_confidence:
            continue
        spans.setdefault(uri, []).append(locator)
        routes.append({"route_id": sha_text(f"{uri}:{locator[0]}:{locator[1]}")[7:27],
                       "source_uri_digest": sha_text(uri), "page_start": locator[0],
                       "page_end": locator[1], "confidence": round(confidence, 8),
                       "config_digest": row.get("retrieval", {}).get("config_digest")})
    return spans, routes


def scoped_bm25_receipts(index: SectionIndex, query: str,
                         route_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    spans, routes = pageindex_route_spans(route_rows)
    if not spans:
        return [], routes
    rows = []
    for hit in index.search(query, max_documents=20, max_sections=20,
                            allowed_uris=set(spans), allowed_spans=spans):
        section, source = hit["section"], hit["section"]["source"]
        rows.append({"source": {"uri": source["uri"], "content_digest": source["content_digest"],
                                 "media_type": source["media_type"]},
                     "evidence": {"quote": section.get("text", ""), "locator": {
                         "kind": "section_span", "section_id": section["id"],
                         "section_digest": section["text_digest"], "page_start": section["page_start"],
                         "page_end": section["page_end"]}},
                     "retrieval": {"adapter": "pageindex-scoped-bm25/v1", "rank": hit["rank"],
                                   "score": round(hit["score"], 8), "query_digest": sha_text(query),
                                   "section_heading": section.get("heading")}})
    return rows, routes


def hard_route_bm25(index: SectionIndex, query: str, global_rows: list[dict[str, Any]],
                    pageindex_rows: list[dict[str, Any]], limit: int = 20) -> list[dict[str, Any]]:
    if classify_query(query) == "exact":
        output = copy.deepcopy(global_rows[:limit])
        for rank, row in enumerate(output, 1):
            row["retrieval"] = {**row.get("retrieval", {}), "adapter": "pageindex-hard-route-bm25/v1",
                                "rank": rank, "route_bypassed": "exact_query"}
        return output
    scoped, routes = scoped_bm25_receipts(index, query, pageindex_rows)
    output = copy.deepcopy((scoped or global_rows)[:limit])
    for rank, row in enumerate(output, 1):
        row["retrieval"] = {**row.get("retrieval", {}), "adapter": "pageindex-hard-route-bm25/v1",
                            "rank": rank, "route_count": len(routes),
                            "fallback_to_global": not bool(scoped)}
    return output


def prior_bm25(index: SectionIndex, query: str, global_rows: list[dict[str, Any]],
               pageindex_rows: list[dict[str, Any]], limit: int = 20,
               safety_slots_at_5: int = 2) -> list[dict[str, Any]]:
    """Use PageIndex as a soft hierarchy prior; global BM25 can never be removed."""
    if classify_query(query) == "exact" or not pageindex_rows:
        output = copy.deepcopy(global_rows[:limit])
        for rank, row in enumerate(output, 1):
            row["retrieval"] = {**row.get("retrieval", {}), "adapter": "pageindex-prior-bm25/v1",
                                "rank": rank, "route_bypassed": "exact_query" if classify_query(query) == "exact" else "empty_route",
                                "global_safety_lane": True}
        return output
    scoped, routes = scoped_bm25_receipts(index, query, pageindex_rows)
    route_spans, _ = pageindex_route_spans(pageindex_rows)
    candidates: list[dict[str, Any]] = []
    for origin, rows in (("global", global_rows), ("scoped", scoped)):
        for row in rows[:20]:
            existing = next((item for item in candidates if overlaps(item["row"], row)), None)
            if existing is None:
                existing = {"row": copy.deepcopy(row), "origins": set(), "global_rank": None,
                            "scoped_rank": None}
                candidates.append(existing)
            existing["origins"].add(origin)
            existing[f"{origin}_rank"] = row.get("retrieval", {}).get("rank")
    query_terms = set(re.findall(r"[a-z0-9]+", query.lower()))
    max_score = max((float(item["row"].get("retrieval", {}).get("score", 0)) for item in candidates), default=1.0) or 1.0
    for item in candidates:
        row = item["row"]; uri = source_uri(row); locator = span(row)
        bm25 = float(row.get("retrieval", {}).get("score", 0)) / max_score
        routed = bool(uri and locator and any(locator[0] <= end and locator[1] >= start
                                              for start, end in route_spans.get(uri, [])))
        heading_terms = set(re.findall(r"[a-z0-9]+", str(row.get("retrieval", {}).get("section_heading", "")).lower()))
        heading_bonus = 0.05 if query_terms & heading_terms else 0.0
        item["score"] = bm25 + (0.15 if routed else 0.0) + heading_bonus
        item["routed"] = routed; item["heading_bonus"] = heading_bonus
    ordered = sorted(candidates, key=lambda item: (-item["score"], source_uri(item["row"]) or "",
                                                   span(item["row"]) or (0, 0)))
    top = ordered[:limit]
    first_five = top[:5]
    global_count = sum("global" in item["origins"] for item in first_five)
    if global_count < safety_slots_at_5:
        replacements = [item for item in ordered[5:] if "global" in item["origins"]]
        for replacement in replacements[:safety_slots_at_5 - global_count]:
            replace_index = next((index for index in range(min(5, len(top)) - 1, -1, -1)
                                  if "global" not in top[index]["origins"]), None)
            if replace_index is not None:
                top[replace_index] = replacement
    output = []
    seen_sources: set[str] = set()
    for rank, item in enumerate(top, 1):
        row = item["row"]; uri = source_uri(row)
        diversity_bonus = 0.02 if uri not in seen_sources else 0.0
        if uri: seen_sources.add(uri)
        row["retrieval"] = {**row.get("retrieval", {}), "adapter": "pageindex-prior-bm25/v1",
                            "rank": rank, "normalized_score": round(item["score"] + diversity_bonus, 8),
                            "route_bonus": 0.15 if item["routed"] else 0.0,
                            "heading_bonus": item["heading_bonus"], "source_diversity_bonus": diversity_bonus,
                            "global_safety_lane": "global" in item["origins"],
                            "route_count": len(routes)}
        output.append(row)
    return output


def freeze_gaps(run_report: dict[str, Any], silver_report: dict[str, Any], catalog: dict[str, Any],
                semantic_report: dict[str, Any] | None = None) -> dict[str, Any]:
    raw_run, raw_silver = Path(run_report["raw_private_dir"]), Path(silver_report["raw_private_dir"])
    eligible_uris = {row.get("source", {}).get("uri") for row in catalog.get("representations", [])
                     if row.get("sections")}
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
        all_gold = silver.get("locators", [])
        gap_bindings = []
        if semantic_report is not None:
            semantic_path = Path(semantic_report["raw_private_dir"]) / f"{task_id}.json"
            if not semantic_path.is_file():
                exclusions.append({"task_id": task_id, "reason": "missing post-output gap-to-silver adjudication"})
                continue
            semantic = json.loads(semantic_path.read_text())
            labels = semantic.get("labels", {}).get("systems", {}).get("v8", {})
            expected_gap_ids = set(labels.get("expected_open_gap_requirement_ids", []))
            # PageIndex is evaluated only on independently adjudicated open
            # retrieval gaps, not every conservative `partial` status emitted
            # by the critic.  A task with no such gap is outside the retrieval
            # panel rather than a failed retrieval task.
            gaps = [row for row in gaps if row.get("requirement_id") in expected_gap_ids]
            if not gaps:
                exclusions.append({"task_id": task_id,
                                   "reason": "no adjudicated open retrieval gap",
                                   "qualification_blocking": False})
                continue
            gap_ids = {row["requirement_id"] for row in gaps}
            for binding in labels.get("gap_to_silver_candidates", []):
                if binding.get("requirement_id") in gap_ids:
                    gap_bindings.append({"gap_id": binding["requirement_id"],
                                         "candidate_ids": list(binding.get("candidate_ids", []))})
            bound_candidate_ids = {candidate for binding in gap_bindings
                                   for candidate in binding["candidate_ids"]}
            all_gold = [row for row in all_gold if row.get("candidate_id") in bound_candidate_ids]
            if not gap_bindings or not all_gold:
                exclusions.append({"task_id": task_id,
                                   "reason": "open gaps have no frozen retrievable silver target",
                                   "qualification_blocking": False})
                continue
        parts = []
        for row in gaps:
            parts.extend(str(row.get(key, "")) for key in ("requirement", "finding", "reason", "rationale"))
            parts.extend(str(q) for q in row.get("evidence_search_queries", [])[:2])
        query = "\n".join(dict.fromkeys(part for part in parts if part))[:12000]
        if not query:
            query = str(run.get("task", {}).get("prompt", ""))[:12000]
        gold = [row for row in all_gold if row.get("source_uri") in eligible_uris]
        if not gold:
            exclusions.append({"task_id": task_id, "reason": "no adapter-eligible canonical-representation silver locator",
                               "frozen_gold_locator_count": len(all_gold)})
            continue
        tasks.append({"task_id": task_id, "gap_ids": [row["requirement_id"] for row in gaps],
                      "gap_bindings": gap_bindings, "query": query, "gold": gold,
                      "excluded_ineligible_gold_count": len(all_gold) - len(gold),
                      "silver_digest": silver.get("silver_digest")})
    manifest = {"schema_version": "proofpress/private-frozen-gap-panel/v1",
                "claim_run_digest": digest(run_report), "silver_report_digest": digest(silver_report),
                "semantic_report_digest": digest(semantic_report) if semantic_report is not None else None,
                "catalog_digest": catalog.get("catalog_digest"), "tasks": tasks,
                "excluded_tasks": exclusions}
    manifest["manifest_digest"] = digest(manifest)
    return manifest


def qualify_gap_manifest(manifest: dict[str, Any]) -> None:
    """Fail before inference unless every frozen-gap task has searchable gold."""
    blocking_exclusions = [row for row in manifest.get("excluded_tasks", [])
                           if row.get("qualification_blocking", True)]
    if blocking_exclusions:
        ids = ",".join(sorted(str(row.get("task_id")) for row in blocking_exclusions))
        raise ValueError(f"gap qualification failed: frozen-gap tasks lack adapter-eligible gold: {ids}")
    tasks = manifest.get("tasks", [])
    if not tasks:
        raise ValueError("gap qualification failed: no frozen-gap tasks with adapter-eligible gold")
    for task in tasks:
        if not task.get("query") or not task.get("gold"):
            raise ValueError(f"gap qualification failed: incomplete frozen task {task.get('task_id')}")


def route_reachability_preflight(manifest: dict[str, Any], index: SectionIndex,
                                 sources: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], float]:
    """Measure the locator-level ceiling imposed by the document router."""
    rows = []
    for task in manifest["tasks"]:
        routed, audit = route_pageindex_sources(
            index, task["query"], sources, min(ROUTED_DOCUMENT_LIMIT, len(sources)))
        if not routed:
            raise ValueError("gap qualification failed: document router produced no sources")
        routed_uris = {row.get("uri") for row in routed}
        gold = task.get("gold", [])
        gold_uris = {row.get("source_uri") for row in gold}
        reachable_locators = sum(row.get("source_uri") in routed_uris for row in gold)
        rows.append({"task_id": task["task_id"], "route_digest": audit["route_digest"],
                     "routed_source_count": len(routed), "gold_source_count": len(gold_uris),
                     "gold_sources_routed": len(gold_uris & routed_uris),
                     "gold_locator_count": len(gold),
                     "gold_locators_routed": reachable_locators,
                     "locator_route_reachability_ceiling": reachable_locators / len(gold)})
    total = sum(row["gold_locator_count"] for row in rows)
    reachable = sum(row["gold_locators_routed"] for row in rows)
    return rows, reachable / total if total else 0.0


def require_fresh_cache_dirs(out: Path) -> list[Path]:
    """A scored stability build must never inherit a prior PageIndex tree."""
    paths = [out / f"pageindex-cache-build-{build}" for build in (1, 2, 3)]
    reused = [path for path in paths if path.exists()]
    if reused:
        raise ValueError("fresh-cache preflight failed: cache build directories already exist: " +
                         ", ".join(path.name for path in reused))
    return paths


def qualify_route_ceiling(ceiling: float, allow_diagnostic: bool) -> tuple[bool, bool]:
    """Classify an explicit bounded route without using gold to tune it.

    A retrieval system is allowed to miss gold.  Preflight must expose the
    route ceiling and formal scoring must count unreachable locators as misses;
    requiring 100% reachability would use the gold set to select a larger route
    before evaluation.  The diagnostic override remains available for callers
    that do not want to score a bounded treatment.
    """
    if not isinstance(ceiling, (int, float)) or not 0 <= ceiling <= 1:
        raise ValueError("gap qualification failed: invalid locator route reachability ceiling")
    incomplete = ceiling < 1.0
    return incomplete, bool(incomplete and allow_diagnostic)


def materialize_pageindex_sources(catalog: dict[str, Any], root: Path) -> list[dict[str, Any]]:
    """Bind every catalog source to a PageIndex-readable canonical representation."""
    root.mkdir(parents=True, exist_ok=True)
    root.chmod(0o700)
    navigation = {row["uri"]: row["path"] for row in catalog.get("source_navigation", [])}
    sources = []
    for representation in catalog.get("representations", []):
        source = representation.get("source", {})
        uri = source.get("uri")
        sections = representation.get("sections", [])
        if not uri or not sections:
            continue
        common = {"source_id": sha_text(uri)[7:23], "uri": uri,
                  "content_digest": source["content_digest"], "media_type": source["media_type"],
                  "representation_digest": representation["representation_digest"],
                  "transform_digest": representation["transform_digest"],
                  "page_count": representation["page_count"]}
        if source.get("media_type") == "application/pdf" and uri in navigation:
            common["path"] = navigation[uri]
            sources.append(common)
            continue
        path = root / f"{common['source_id']}.md"
        lines, locator_map = [], []
        for section in sections:
            heading = str(section.get("heading") or section["id"]).replace("\n", " ").strip()
            locator_map.append({"line": len(lines) + 1, "section_id": section["id"],
                                "section_digest": section["text_digest"],
                                "page_start": section["page_start"], "page_end": section["page_end"]})
            lines.extend([f"## {heading}", str(section.get("text", "")).rstrip(), ""])
        payload = "\n".join(lines).rstrip() + "\n"
        path.write_text(payload, encoding="utf-8")
        path.chmod(0o600)
        common.update({"path": str(path), "path_digest": sha_text(payload),
                       "representation_kind": "canonical_markdown", "locator_map": locator_map})
        sources.append(common)
    return sources


def mean(rows: list[dict[str, Any]], metric: str) -> float | None:
    values = [float(row[metric]) for row in rows if row.get(metric) is not None]
    return sum(values) / len(values) if values else None


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    rows = sorted(values)
    return rows[min(len(rows) - 1, round((len(rows) - 1) * q))]


def gateway_cost_summary(receipt_file: Path, offset: int, expected_model: str = MODEL,
                         expected_provider: str = PROVIDER) -> dict[str, Any]:
    """Separate valid retrieval output from incomplete billing telemetry."""
    rows = ([json.loads(line) for line in receipt_file.read_text(encoding="utf-8").splitlines()[offset:]]
            if receipt_file.exists() else [])
    route_valid = bool(rows) and all(
        row.get("model") == expected_model and row.get("provider") == expected_provider and
        row.get("fallback_used") is False and row.get("terminal") is True
        for row in rows)
    if not route_valid:
        raise RuntimeError("Gateway terminal route telemetry incomplete")
    known = [float(row["cost_usd"]) for row in rows
             if isinstance(row.get("cost_usd"), (int, float))]
    missing = len(rows) - len(known)
    return {"known_cost_usd": sum(known),
            "cost_usd": sum(known) if not missing else None,
            "cost_status": "complete" if not missing else "inconclusive_missing_cost",
            "terminal_call_count": len(rows), "missing_cost_call_count": missing}


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
    for name in ("bm25-page/v1", "pageindex-tree/v1", "hybrid-rrf/v1",
                 "pageindex-hard-route-bm25/v1", "pageindex-prior-bm25/v1"):
        if not all(name in task.get("systems", {}) for task in corrected.get("tasks", [])):
            continue
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
        for system in ("bm25-page/v1", "pageindex-tree/v1", "hybrid-rrf/v1",
                       "pageindex-hard-route-bm25/v1", "pageindex-prior-bm25/v1"):
            if system not in task.get("systems", {}):
                continue
            task["systems"][system] = {f"k={k}": dict(null_metrics) for k in K_VALUES}
    for name in ("bm25-page/v1", "pageindex-tree/v1", "hybrid-rrf/v1",
                 "pageindex-hard-route-bm25/v1", "pageindex-prior-bm25/v1"):
        if name not in corrected.get("systems", {}):
            continue
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
    ap.add_argument("--semantic-report",
                    help="Post-output adjudication containing v8 gap-to-frozen-silver bindings.")
    ap.add_argument("--catalog", required=True)
    ap.add_argument("--sidecar", required=True)
    ap.add_argument("--gateway-server", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--parallelism", type=int, default=4)
    ap.add_argument("--build-workers", type=int, default=1,
                    help="Number of fresh-cache stability builds to run concurrently; default serializes them to avoid cross-build rate-limit interference.")
    ap.add_argument("--qualification-only", action="store_true",
                    help="Validate frozen gaps and materialize full-catalog custody without starting Gateway inference.")
    ap.add_argument("--allow-incomplete-route-diagnostic", action="store_true",
                    help="Label a bounded route below 1.0 diagnostic-only instead of scoring unreachable gold as misses.")
    args = ap.parse_args()
    if args.parallelism < 1 or args.build_workers < 1 or args.build_workers > 3:
        ap.error("--parallelism must be positive and --build-workers must be between 1 and 3")
    os.environ["PROOFPRESS_EXECUTOR_MODEL"] = MODEL
    os.environ["PROOFPRESS_AI_GATEWAY_PROVIDER"] = PROVIDER
    private_panel.MODEL = MODEL
    private_panel.PROVIDER = PROVIDER
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    claim_report = json.loads(Path(args.claim_report).read_text())
    silver_report = json.loads(Path(args.silver_report).read_text())
    semantic_report = json.loads(Path(args.semantic_report).read_text()) if args.semantic_report else None
    catalog = json.loads(Path(args.catalog).read_text())
    manifest = freeze_gaps(claim_report, silver_report, catalog, semantic_report)
    (out / "gap-manifest-private.json").write_text(json.dumps(manifest, indent=2) + "\n")
    qualify_gap_manifest(manifest)
    index = SectionIndex(catalog)
    pageindex_sources = materialize_pageindex_sources(catalog, out / "canonical-pageindex-inputs")
    if not pageindex_sources:
        raise ValueError("gap qualification failed: catalog has no PageIndex-readable representations")
    route_preflight, locator_ceiling = route_reachability_preflight(
        manifest, index, pageindex_sources)
    incomplete_route, diagnostic_only = qualify_route_ceiling(
        locator_ceiling, args.allow_incomplete_route_diagnostic)
    qualification = {
        "schema_version": "proofpress/private-gap-qualification/v1",
        "status": "diagnostic_only" if diagnostic_only else "pass",
        "manifest_digest": manifest["manifest_digest"],
        "catalog_digest": catalog.get("catalog_digest"),
        "tasks": len(manifest["tasks"]),
        "non_retrieval_gap_tasks": len(manifest.get("excluded_tasks", [])),
        "non_retrieval_gap_reasons": {
            reason: sum(row.get("reason") == reason for row in manifest.get("excluded_tasks", []))
            for reason in sorted({row.get("reason") for row in manifest.get("excluded_tasks", [])
                                  if row.get("reason")})
        },
        "eligible_gold_locators": sum(len(row["gold"]) for row in manifest["tasks"]),
        "adapter_sources": len(pageindex_sources),
        "canonical_markdown_sources": sum(
            row.get("representation_kind") == "canonical_markdown" for row in pageindex_sources),
        "pdf_sources": sum(
            row.get("media_type") == "application/pdf" and not row.get("representation_kind")
            for row in pageindex_sources),
        "document_router": "bm25-document-router/v1",
        "max_routed_documents": min(ROUTED_DOCUMENT_LIMIT, len(pageindex_sources)),
        "route_preflight_digest": sha_text(json.dumps(route_preflight, sort_keys=True)),
        "routed_task_count": len(route_preflight),
        "gold_source_route_recall": (
            sum(row["gold_sources_routed"] for row in route_preflight) /
            max(1, sum(row["gold_source_count"] for row in route_preflight))),
        "gold_locator_route_reachability_ceiling": locator_ceiling,
        "route_preflight": route_preflight,
        "formal_eligible": not diagnostic_only,
        "unreachable_gold_scored_as_miss": bool(incomplete_route and not diagnostic_only),
        "diagnostic_only_override": diagnostic_only,
        "gateway_calls": 0,
    }
    (out / "qualification-report.json").write_text(
        json.dumps(qualification, indent=2, sort_keys=True) + "\n")
    if args.qualification_only:
        print(json.dumps(qualification, indent=2, sort_keys=True))
        return
    cache_dirs = require_fresh_cache_dirs(out)
    if not os.environ.get("AI_GATEWAY_API_KEY"):
        raise SystemExit("AI_GATEWAY_API_KEY unavailable")
    config = {"adapter": "proofpress.pageindex", "version": "1", "requested_model": MODEL,
              "provider": PROVIDER, "fallback": "forbidden", "max_sections": 20, "max_pages": 20,
              "toc_check_pages": 1, "max_pages_per_node": 1, "max_tokens_per_node": 2500,
              "document_router": "bm25-document-router/v1",
              "max_routed_documents": min(ROUTED_DOCUMENT_LIMIT, len(pageindex_sources)),
              "max_nodes_per_source": 3,
              "node_summary": False, "document_description": False,
              "timeout_seconds": args.timeout, "parallelism": args.parallelism}
    config["config_digest"] = sha_text(json.dumps(config, sort_keys=True))
    receipt_files = {build: out / f"gateway-private-receipts-build-{build}.jsonl" for build in (1, 2, 3)}
    raw, task_rows, latencies, call_costs = [], [], [], []
    bridges = {build: private_panel.bridge(args.gateway_server, receipt_files[build]) for build in (1, 2, 3)}
    try:
        for task in manifest["tasks"]:
            bm25 = bm25_receipts(index, task["query"])
            routed_sources, route_audit = route_pageindex_sources(
                index, task["query"], pageindex_sources,
                min(ROUTED_DOCUMENT_LIMIT, len(pageindex_sources)))
            if not routed_sources:
                raise ValueError("PageIndex document router produced no adapter-eligible sources")
            def run_build(build: int) -> tuple[int, list[dict[str, Any]], dict[str, Any]]:
                receipt_file = receipt_files[build]
                offset = len(receipt_file.read_text().splitlines()) if receipt_file.exists() else 0
                try:
                    rows, telemetry = private_panel.tree(task["query"], routed_sources, args.sidecar, config, 20, bridges[build][1],
                                                         cache_dirs[build - 1], args.timeout)
                    cost_summary = gateway_cost_summary(receipt_file, offset)
                    return build, rows, {"build": build, "status": "ok", "receipt_count": len(rows),
                                         "latency_ms": telemetry["latency_ms"], **cost_summary,
                                         "cache_hits": telemetry.get("index_cache_hits"),
                                         "cache_misses": telemetry.get("index_cache_misses"),
                                         "source_build_retries": telemetry.get("source_build_retries", 0)}
                except Exception as exc:
                    return build, [], {"build": build, "status": "inconclusive",
                                       "reason_type": type(exc).__name__, "reason_digest": sha_text(str(exc))}
            build_results = {}
            with ThreadPoolExecutor(max_workers=args.build_workers) as pool:
                futures = [pool.submit(run_build, build) for build in (1, 2, 3)]
                for future in as_completed(futures):
                    build, rows, meta = future.result(); build_results[build] = (rows, meta)
            builds = [build_results[build][0] for build in (1, 2, 3)]
            build_meta = [build_results[build][1] for build in (1, 2, 3)]
            for meta in build_meta:
                if meta["status"] == "ok":
                    latencies.append(float(meta["latency_ms"])); call_costs.append(float(meta["known_cost_usd"]))
            primary = builds[0]
            hybrid = hybrid_rrf(bm25, primary)
            hard_route = hard_route_bm25(index, task["query"], bm25, primary)
            prior = prior_bm25(index, task["query"], bm25, primary)
            systems = {"bm25-page/v1": bm25, "pageindex-tree/v1": primary,
                       "hybrid-rrf/v1": hybrid,
                       "pageindex-hard-route-bm25/v1": hard_route,
                       "pageindex-prior-bm25/v1": prior}
            primary_ok = build_meta[0]["status"] == "ok"
            metrics = {name: {f"k={k}": (
                score(rows[:k], task["gold"]) if name in {"bm25-page/v1", "pageindex-hard-route-bm25/v1", "pageindex-prior-bm25/v1"} or primary_ok else
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
                              "global_gold_miss_count_at_5": sum(not hit for hit in gold_hit_vector(bm25[:5], task["gold"])),
                              "global_gold_misses_recovered_by_prior_at_5": sum(
                                  not global_hit and prior_hit for global_hit, prior_hit in
                                  zip(gold_hit_vector(bm25[:5], task["gold"]),
                                      gold_hit_vector(prior[:5], task["gold"]))),
                              "pageindex_unique_gold_hits_at_5": sum(
                                  pageindex_hit and not global_hit for global_hit, pageindex_hit in
                                  zip(gold_hit_vector(bm25[:5], task["gold"]),
                                      gold_hit_vector(primary[:5], task["gold"]))),
                              "document_route": route_audit,
                              "pageindex_builds": build_meta,
                              "primary_to_rebuild_locator_jaccard": stability})
            raw.append({"task_id": task["task_id"], "document_route": route_audit, "systems": systems})
    finally:
        for gateway, _ in bridges.values():
            gateway.terminate()
            try: gateway.wait(timeout=5)
            except subprocess.TimeoutExpired: gateway.kill()
    systems_report = {}
    for name in ("bm25-page/v1", "pageindex-tree/v1", "hybrid-rrf/v1",
                 "pageindex-hard-route-bm25/v1", "pageindex-prior-bm25/v1"):
        systems_report[name] = {}
        for k in K_VALUES:
            rows = [task["systems"][name][f"k={k}"] for task in task_rows]
            systems_report[name][f"k={k}"] = {metric: mean(rows, metric) for metric in (
                "evidence_set_coverage", "complete_evidence_set_success", "citation_precision", "receipt_pass_rate")}
    paired = []
    paired_prior = []
    for row in task_rows:
        bm25 = row["systems"]["bm25-page/v1"]["k=5"]["evidence_set_coverage"]
        pageindex = row["systems"]["pageindex-tree/v1"]["k=5"]["evidence_set_coverage"]
        if bm25 is not None and pageindex is not None:
            paired.append(float(pageindex) - float(bm25))
        prior = row["systems"]["pageindex-prior-bm25/v1"]["k=5"]["evidence_set_coverage"]
        if bm25 is not None and prior is not None:
            paired_prior.append(float(prior) - float(bm25))
    all_builds = [meta for row in task_rows for meta in row["pageindex_builds"] if meta["status"] == "ok"]
    cold = [float(meta["latency_ms"]) for meta in all_builds if (meta.get("cache_misses") or 0) > 0]
    warm = [float(meta["latency_ms"]) for meta in all_builds if meta.get("cache_misses") == 0]
    warm_costs = [float(meta["cost_usd"]) for meta in all_builds
                  if meta.get("cache_misses") == 0 and isinstance(meta.get("cost_usd"), (int, float))]
    missing_cost_calls = sum(int(meta.get("missing_cost_call_count", 0)) for meta in all_builds)
    global_misses = sum(row["global_gold_miss_count_at_5"] for row in task_rows)
    recovered_misses = sum(row["global_gold_misses_recovered_by_prior_at_5"] for row in task_rows)
    unique_pageindex_hits = sum(row["pageindex_unique_gold_hits_at_5"] for row in task_rows)
    report = {"schema_version": "proofpress/private-gap-retrieval-report/v1",
              "manifest_digest": manifest["manifest_digest"], "catalog_digest": catalog.get("catalog_digest"),
              "model": MODEL, "provider": PROVIDER, "fallback": "forbidden",
              "qualification_status": qualification["status"],
              "diagnostic_only": diagnostic_only,
              "gold_locator_route_reachability_ceiling": locator_ceiling,
              "denominators": {"claim_tasks": len(claim_report.get("tasks", [])),
                               "tasks_with_frozen_gaps": len(manifest["tasks"]),
                               "scored_tasks": sum(bool(row["gold_locator_count"]) for row in task_rows),
                               "adapter_sources": len(pageindex_sources),
                               "canonical_markdown_sources": sum(row.get("representation_kind") == "canonical_markdown" for row in pageindex_sources),
                               "pdf_sources": sum(row.get("media_type") == "application/pdf" and not row.get("representation_kind") for row in pageindex_sources)},
              "systems": systems_report,
              "pageindex": {"fresh_cache_builds": 3, "primary_build": 1,
                            "latency_ms": {"all_p50": percentile(latencies, .5), "all_p95": percentile(latencies, .95),
                                           "cold_p50": percentile(cold, .5), "cold_p95": percentile(cold, .95),
                                           "warm_p50": percentile(warm, .5), "warm_p95": percentile(warm, .95)},
                            "cost_usd": sum(call_costs) if call_costs else None,
                            "cost_status": "complete" if not missing_cost_calls else "inconclusive_missing_cost",
                            "missing_cost_call_count": missing_cost_calls,
                            "mean_warm_query_cost_usd": statistics.mean(warm_costs) if warm_costs else None,
                            "mean_rebuild_locator_jaccard": statistics.mean(
                                value for row in task_rows for value in row["primary_to_rebuild_locator_jaccard"]
                                if isinstance(value, (int, float))
                            ) if any(isinstance(value, (int, float)) for row in task_rows
                                     for value in row["primary_to_rebuild_locator_jaccard"]) else None},
              "paired_pageindex_minus_bm25_at_5": {"denominator": len(paired),
                                                    "mean": statistics.mean(paired) if paired else None,
                                                    "bootstrap_95_ci": paired_bootstrap_ci(paired)},
              "paired_prior_minus_bm25_at_5": {"denominator": len(paired_prior),
                                                "mean": statistics.mean(paired_prior) if paired_prior else None,
                                                "bootstrap_95_ci": paired_bootstrap_ci(paired_prior)},
              "hierarchical_diagnostics": {
                  "global_gold_misses_at_5": global_misses,
                  "global_gold_misses_recovered_by_prior_at_5": recovered_misses,
                  "global_gold_miss_recovery_rate_at_5": (recovered_misses / global_misses
                                                           if global_misses else 1.0),
                  "pageindex_unique_gold_hits_at_5": unique_pageindex_hits,
                  "query_classes": {label: sum(classify_query(task["query"]) == label
                                                for task in manifest["tasks"])
                                    for label in ("exact", "thematic")},
              },
              "tasks": task_rows,
              "decision_boundary": "Private task-level frozen-gap panel; model-adjudicated silver is not human gold and cannot change admission policy."}
    report = enforce_inconclusive_build_semantics(report)
    (out / "raw-private-receipts.json").write_text(json.dumps(raw, indent=2) + "\n")
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"ok": True, "tasks": len(task_rows), "report": str(out / "sanitized-report.json")}))


if __name__ == "__main__":
    main()

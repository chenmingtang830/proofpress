#!/usr/bin/env python3
"""Freeze private model-adjudicated source/page silver before a scored run."""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from legal_pipeline_contract import MODEL_ROLES
from run_claim_construction_private import (
    Gateway,
    SectionIndex,
    _model_call,
    _write_private,
    digest,
    sha_text,
)

SCHEMA = "proofpress/private-model-adjudicated-silver/v1"


def _candidate_rows(index: SectionIndex, task: dict[str, Any]) -> list[dict[str, Any]]:
    rubric_text = " ".join(str(row.get("criteria", "")) for row in task.get("rubric", []) if isinstance(row, dict))
    query = " ".join((task.get("prompt", ""), task.get("gold_response", ""), rubric_text))
    rows = []
    for hit in index.search(query, max_documents=20, max_sections=20):
        section = hit["section"]
        candidate_id = "silver_" + sha_text(
            section["representation_digest"] + "\n" + section["id"]
        ).removeprefix("sha256:")[:20]
        rows.append({
            "candidate_id": candidate_id,
            "source_uri": section["source"]["uri"],
            "content_digest": section["source"]["content_digest"],
            "representation_digest": section["representation_digest"],
            "locator": {
                "kind": "section_span", "section_id": section["id"],
                "section_digest": section["text_digest"],
                "page_start": section["page_start"], "page_end": section["page_end"],
            },
            "quote": section.get("text", "")[:600],
            "rank": hit["rank"],
        })
    return rows


def _selected_ids(value: Any, allowed: set[str]) -> set[str]:
    if not isinstance(value, dict):
        raise ValueError("silver adjudication must be an object")
    selected = value.get("selected_candidate_ids", value.get("locators", []))
    ids = set()
    for row in selected if isinstance(selected, list) else []:
        candidate_id = row.get("candidate_id") if isinstance(row, dict) else row
        if isinstance(candidate_id, str):
            ids.add(candidate_id)
    if not ids.issubset(allowed):
        raise ValueError("silver adjudication referenced an unknown candidate")
    return ids


def _judge(task: dict[str, Any], candidates: list[dict[str, Any]], gateway: Gateway,
           pass_name: str) -> dict[str, Any]:
    payload = {
        "task": task["prompt"], "gold_response": task["gold_response"],
        "rubric_atoms": task.get("rubric", []), "candidate_sections": candidates,
        "pass": pass_name,
        "instruction": "Select the smallest source/page evidence set that supports the gold response and each rubric atom. Do not generate an answer. Return compact JSON with selected_candidate_ids, rubric_mapping, minimum_evidence_sets, exclusions.",
    }
    return _model_call(
        gateway,
        "You freeze model-adjudicated silver locators. Use only supplied candidates. Return JSON only.",
        json.dumps(payload, ensure_ascii=False),
        8000,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--tasks-json", required=True)
    parser.add_argument("--world-id", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--gateway-server", required=True)
    parser.add_argument("--provider", default="openai")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=float, default=300)
    parser.add_argument("--exclude-task-id", action="append", default=[])
    args = parser.parse_args()

    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    raw_tasks = json.loads(Path(args.tasks_json).read_text(encoding="utf-8"))
    raw_tasks = raw_tasks.get("tasks", raw_tasks) if isinstance(raw_tasks, dict) else raw_tasks
    excluded = set(args.exclude_task_id)
    tasks = [row for row in raw_tasks if row.get("world_id") == args.world_id
             and row.get("prompt") and row.get("gold_response") and row.get("task_id") not in excluded]
    tasks.sort(key=lambda row: row["task_id"])
    index = SectionIndex(catalog)
    gateway = None
    results: dict[str, dict[str, Any]] = {}
    private = out / "raw"
    try:
        gateway = Gateway(args.gateway_server, MODEL_ROLES["coverage_critic"], args.provider,
                          out, args.timeout, "low")

        def run(task: dict[str, Any]) -> tuple[str, dict[str, Any]]:
            candidates = _candidate_rows(index, task)
            allowed = {row["candidate_id"] for row in candidates}
            first = _judge(task, candidates, gateway, "independent_a")
            second = _judge(task, candidates, gateway, "independent_b")
            if not first["ok"] or not second["ok"]:
                reason = first["record"] if not first["ok"] else second["record"]
                result = {"task_id": task["task_id"], "status": "inconclusive",
                          "candidate_count": len(candidates), "reason": reason}
                _write_private(private / (task["task_id"] + ".json"), {
                    "task": task, "candidates": candidates,
                    "first": first.get("value"), "second": second.get("value"),
                })
                return task["task_id"], result
            try:
                left = _selected_ids(first["value"], allowed)
                right = _selected_ids(second["value"], allowed)
            except Exception as exc:
                result = {"task_id": task["task_id"], "status": "inconclusive",
                          "candidate_count": len(candidates),
                          "reason": {"type": type(exc).__name__, "digest": sha_text(str(exc))}}
                _write_private(private / (task["task_id"] + ".json"), {
                    "task": task, "candidates": candidates,
                    "first": first["value"], "second": second["value"],
                })
                return task["task_id"], result
            arbitration = None
            selected = left
            if left != right:
                arbitration_payload = {
                    "task": task["prompt"], "gold_response": task["gold_response"],
                    "rubric_atoms": task.get("rubric", []), "candidate_sections": candidates,
                    "judgment_a": first["value"], "judgment_b": second["value"],
                    "instruction": "Resolve only locator disagreements. Return compact JSON with selected_candidate_ids, rubric_mapping, minimum_evidence_sets, exclusions.",
                }
                arbitration = _model_call(
                    gateway,
                    "You arbitrate two independent silver-locator judgments. Return JSON only.",
                    json.dumps(arbitration_payload, ensure_ascii=False), 8000,
                )
                if not arbitration["ok"]:
                    result = {"task_id": task["task_id"], "status": "inconclusive",
                              "candidate_count": len(candidates), "reason": arbitration["record"]}
                    _write_private(private / (task["task_id"] + ".json"), {
                        "task": task, "candidates": candidates,
                        "first": first["value"], "second": second["value"],
                    })
                    return task["task_id"], result
                selected = _selected_ids(arbitration["value"], allowed)
            locators = [row for row in candidates if row["candidate_id"] in selected]
            frozen = {
                "schema_version": SCHEMA, "task_id": task["task_id"],
                "task_digest": sha_text(task["prompt"]),
                "gold_response_digest": sha_text(task["gold_response"]),
                "rubric_digest": digest(task.get("rubric", [])),
                "candidate_query_digest": digest([row["candidate_id"] for row in candidates]),
                "locators": locators,
                "judgments": {"a": first["value"], "b": second["value"],
                              "arbitration": arbitration["value"] if arbitration else None},
            }
            frozen["silver_digest"] = digest(frozen)
            _write_private(private / (task["task_id"] + ".json"), frozen)
            return task["task_id"], {
                "task_id": task["task_id"], "status": "ok",
                "candidate_count": len(candidates), "locator_count": len(locators),
                "independent_agreement": left == right,
                "arbitrated": left != right, "silver_digest": frozen["silver_digest"],
                "rubric_atom_count": len(task.get("rubric", [])),
            }

        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            futures = {pool.submit(run, task): task for task in tasks}
            for future in as_completed(futures):
                task = futures[future]
                try:
                    task_id, result = future.result()
                except Exception as exc:
                    task_id = task["task_id"]
                    result = {"task_id": task_id, "status": "inconclusive",
                              "reason": {"type": type(exc).__name__, "digest": sha_text(str(exc))}}
                results[task_id] = result
    finally:
        if gateway: gateway.stop()

    calls = gateway.calls if gateway else []
    receipts = gateway.receipt_rows() if gateway else []
    costs = [float(row["cost_usd"]) for row in receipts if isinstance(row.get("cost_usd"), (int, float))]
    report = {
        "schema_version": SCHEMA,
        "catalog_digest": catalog.get("catalog_digest"),
        "model": MODEL_ROLES["coverage_critic"], "provider": args.provider,
        "fallback": "forbidden", "excluded_development_task_ids": sorted(excluded),
        "tasks": [results[key] for key in sorted(results)],
        "denominators": {
            "tasks": len(tasks), "frozen": sum(row.get("status") == "ok" for row in results.values()),
            "inconclusive": sum(row.get("status") != "ok" for row in results.values()),
            "rubric_atoms": sum(len(task.get("rubric", [])) for task in tasks),
        },
        "telemetry": {
            "calls": len(calls), "gateway_receipts": len(receipts),
            "known_cost_usd": round(sum(costs), 8),
            "cost_status": "ok" if len(costs) == len(receipts) == len(calls) else "inconclusive",
        },
        "boundary": "Model-adjudicated silver, not human gold. Development-exposed tasks are excluded.",
        "raw_private_dir": str(private),
    }
    _write_private(out / "sanitized-report.json", report)
    print(json.dumps({"ok": True, "tasks": len(tasks),
                      "frozen": report["denominators"]["frozen"],
                      "inconclusive": report["denominators"]["inconclusive"],
                      "report": str(out / "sanitized-report.json")}))


if __name__ == "__main__":
    main()

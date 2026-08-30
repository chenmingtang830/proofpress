#!/usr/bin/env python3
"""Compare extractor attention/batching routes on one frozen private development block."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
from typing import Any

from governed_workflow_contract import digest
from run_claim_construction_private import Gateway
from run_model_routing_qualification_private import terminal_telemetry
from run_v10_role_matrix_private import MODELS, call_extractor

SCHEMA = "proofpress/v10-extractor-ablation/v1"
CONDITIONS = {
    "deepseek-b1": ("deepseek", 1),
    "deepseek-b4": ("deepseek", 4),
    "qwen-b4": ("qwen", 4),
    "ling-b4": ("ling", 4),
}


def score_atoms(atoms: list[dict[str, Any]], reference: list[dict[str, Any]]) -> dict[str, Any]:
    atom_requirements = {row["requirement_id"] for row in atoms}
    sufficient = {row["requirement_id"] for row in reference if row["evidence_sufficient"]}
    gaps = {row["requirement_id"] for row in reference if not row["evidence_sufficient"]}
    return {
        "atom_count": len(atoms),
        "expected_covered_count": len(sufficient),
        "expected_gap_count": len(gaps),
        "expected_covered_with_atom": len(sufficient & atom_requirements),
        "expected_gap_with_partial_atom": len(gaps & atom_requirements),
        "sufficient_atom_recall": len(sufficient & atom_requirements) / len(sufficient) if sufficient else None,
        # This is diagnostic, not a false-positive rate: a partial atom can honestly exist for a gap.
        "gap_partial_atom_rate": len(gaps & atom_requirements) / len(gaps) if gaps else None,
    }


def run_condition(label: str, model_label: str, batch_size: int, server: str,
                  output: Path, timeout: float, task_rows: list[dict[str, Any]]) -> dict[str, Any]:
    route = MODELS[model_label]
    gateway = Gateway(server, route["model"], route["provider"], output, timeout,
                      route["reasoning"], structured_output=True)
    tasks = []
    checkpoint_dir = output / "checkpoints" / label
    checkpoint_dir.mkdir(parents=True, exist_ok=True); checkpoint_dir.chmod(0o700)
    try:
        # Transport/schema preflight is deliberately discarded and never scored.
        first = task_rows[0]
        _, preflight = call_extractor(
            gateway, first["requirements"][:1], first["receipts"],
            first["retrieval_audit"][:1], batch_size=1,
        )
        if preflight["status"] != "ok":
            return {
                "condition": label, "route": route, "batch_size": batch_size,
                "tasks": [], "metrics": {}, "denominators": {"tasks": len(task_rows), "completed_tasks": 0},
                "telemetry": terminal_telemetry({label: gateway}), "status": "inconclusive",
                "failure": {"class": "route_preflight_failure", "stage": preflight},
            }
        for source in task_rows:
            atoms, stage = call_extractor(
                gateway, source["requirements"], source["receipts"],
                source["retrieval_audit"], batch_size=batch_size,
            )
            score = score_atoms(atoms, source["gap_reference"])
            tasks.append({
                "task_id": source["task_id"],
                "status": stage["status"],
                "stage": stage,
                "score": score,
                "artifact_digest": digest(atoms),
            })
            checkpoint = {"schema_version": SCHEMA, "condition": label, "task": tasks[-1]}
            (checkpoint_dir / f'{source["task_id"]}.json').write_text(
                json.dumps(checkpoint, indent=2, sort_keys=True) + "\n"
            )
    finally:
        gateway.stop()
    telemetry = terminal_telemetry({label: gateway})
    complete = [row for row in tasks if row["status"] == "ok"]
    expected = sum(row["score"]["expected_covered_count"] for row in complete)
    found = sum(row["score"]["expected_covered_with_atom"] for row in complete)
    gaps = sum(row["score"]["expected_gap_count"] for row in complete)
    partial = sum(row["score"]["expected_gap_with_partial_atom"] for row in complete)
    return {
        "condition": label,
        "route": route,
        "batch_size": batch_size,
        "tasks": tasks,
        "metrics": {
            "sufficient_atom_recall": found / expected if expected else None,
            "gap_partial_atom_rate": partial / gaps if gaps else None,
            "binding_pass_rate": 1.0 if complete else None,
        },
        "denominators": {"tasks": len(tasks), "completed_tasks": len(complete),
                         "expected_covered": expected, "expected_gaps": gaps},
        "telemetry": telemetry,
        "status": "pass" if len(complete) == len(task_rows) and not telemetry["missing_cost_calls"] else "inconclusive",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--construction-raw", required=True)
    parser.add_argument("--gateway-server", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--budget-usd", type=float, default=6.0)
    parser.add_argument("--timeout", type=float, default=300)
    parser.add_argument("--max-workers", type=int, default=2)
    args = parser.parse_args()
    raw_paths = sorted(Path(args.construction_raw).glob("*.json"))
    if len(raw_paths) != 4:
        raise SystemExit("extractor ablation requires exactly four frozen task artifacts")
    task_rows = [json.loads(path.read_text()) for path in raw_paths]
    output = Path(args.out); output.mkdir(parents=True, exist_ok=True); output.chmod(0o700)
    results = {}
    if args.max_workers < 1 or args.max_workers > len(CONDITIONS):
        raise SystemExit("max-workers must be between 1 and the condition count")
    with ThreadPoolExecutor(max_workers=args.max_workers) as pool:
        futures = {
            pool.submit(run_condition, label, model, batch, args.gateway_server,
                        output, args.timeout, task_rows): label
            for label, (model, batch) in CONDITIONS.items()
        }
        for future in as_completed(futures):
            label = futures[future]
            try:
                results[label] = future.result()
            except Exception as exc:
                results[label] = {
                    "condition": label, "status": "inconclusive", "tasks": [],
                    "metrics": {}, "telemetry": {"known_cost_usd": 0, "missing_cost_calls": 1},
                    "failure": {"class": type(exc).__name__, "digest": digest(str(exc))},
                }
    cost = sum(row["telemetry"]["known_cost_usd"] for row in results.values())
    if cost > args.budget_usd:
        raise RuntimeError("extractor ablation exceeded hard budget")
    report = {
        "schema_version": SCHEMA,
        "boundary": "Frozen four-task development ablation. The Sol evidence-sufficiency reference is model-adjudicated and used only for scoring, never as extractor input or admission authority. Route preflights are discarded and excluded from quality denominators.",
        "conditions": results,
        "telemetry": {"known_cost_usd": cost, "budget_usd": args.budget_usd,
                      "missing_cost_calls": sum(row["telemetry"]["missing_cost_calls"] for row in results.values()),
                      "fallback": "forbidden"},
        "status": "pass" if all(row["status"] == "pass" for row in results.values()) else "inconclusive",
    }
    (output / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "cost_usd": cost,
                      "conditions": {label: row["metrics"] for label, row in results.items()}}, sort_keys=True))


if __name__ == "__main__":
    main()

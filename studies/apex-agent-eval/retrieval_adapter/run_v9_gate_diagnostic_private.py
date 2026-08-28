#!/usr/bin/env python3
"""Run the frozen 4-task v9 atom/gate diagnostic matrix.

The runner reuses one frozen decomposition and deterministic catalog retrieval
for every cell. It varies only the evidence-atom extractor and the placement
of the claimability gate, while keeping the DeepSeek proposer and Sol verdict
gate fixed. Raw task/source/model artifacts remain in the private output.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from run_claim_construction_private import (
    Gateway, SectionIndex, _construct_v9, _write_private, digest,
)

SCHEMA = "proofpress/private-v9-gate-diagnostic/v1"
EXTRACTORS = {
    "ling": ("inclusionai/ling-3.0-flash-fin", "novita", "high"),
    "deepseek": ("deepseek/deepseek-v4-flash", "deepinfra", "none"),
    "sol": ("gpt-5.6-sol", "openai", "low"),
}
MODES = (
    "strict_atom_preproposal",
    "receipt_preproposal",
    "postproposal_binding",
)


def _cost(gateways: list[Gateway]) -> tuple[float | None, int]:
    """Use terminal Gateway receipts, not parsed-call success records, for cost."""
    calls = [row for gateway in gateways for row in gateway.calls]
    receipts = [row for gateway in gateways for row in gateway.receipt_rows()]
    costs = []
    missing = max(0, len(calls) - len(receipts))
    for row in receipts:
        usage = row.get("usage") if isinstance(row.get("usage"), dict) else {}
        cost = usage.get("cost_usd", row.get("cost_usd"))
        if isinstance(cost, (int, float)):
            costs.append(float(cost))
        else:
            missing += 1
    return sum(costs), missing


def _summary(task_id: str, extractor: str, mode: str,
             construction: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_id": task_id,
        "extractor": extractor,
        "claimability_mode": mode,
        "status": construction.get("status"),
        "critic_status": construction.get("critic_status"),
        "stage_counts": construction.get("stage_counts", {}),
        "claim_count": len(construction.get("claims", [])),
        "rejected_claim_count": construction.get("rejected_claim_count", 0),
        "evidence_atom_count": len(construction.get("evidence_atoms", [])),
        "requirement_status_counts": {
            state: sum(row.get("status") == state
                       for row in construction.get("requirements", []))
            for state in ("covered", "partial", "gap")
        },
        "artifact_digest": digest({
            "requirements": construction.get("requirements", []),
            "claims": construction.get("claims", []),
            "atoms": construction.get("evidence_atoms", []),
            "gates": construction.get("claimability_gates", []),
        }),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", required=True)
    ap.add_argument("--frozen-run-report", required=True,
                    help="Four-task v9 run whose decomposition is frozen for every cell")
    ap.add_argument("--gateway-server", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=float, default=300)
    ap.add_argument("--budget-usd", type=float, default=12.0)
    ap.add_argument("--prior-cost-usd", type=float, default=0.0,
                    help="Known terminal cost from an interrupted resumable attempt")
    args = ap.parse_args()

    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw_dir = out / "raw"; raw_dir.mkdir(exist_ok=True); raw_dir.chmod(0o700)
    catalog = json.loads(Path(args.catalog).read_text())
    frozen_report = json.loads(Path(args.frozen_run_report).read_text())
    frozen_rows = frozen_report.get("tasks", [])
    if len(frozen_rows) != 4 or not frozen_report.get("qualification", {}).get("requested"):
        raise SystemExit("diagnostic requires exactly four frozen qualification tasks")
    frozen_private = Path(frozen_report["raw_private_dir"])
    index = SectionIndex(catalog)

    proposer = Gateway(args.gateway_server, "deepseek/deepseek-v4-flash", "deepinfra",
                       out, args.timeout, "none", structured_output=True,
                       min_output_tokens=12000)
    sol = Gateway(args.gateway_server, "gpt-5.6-sol", "openai", out,
                  args.timeout, "low", structured_output=True)
    extractors = {
        label: Gateway(args.gateway_server, model, provider, out, args.timeout,
                       reasoning, structured_output=True, min_output_tokens=12000)
        for label, (model, provider, reasoning) in EXTRACTORS.items()
    }
    gateways = [proposer, sol, *extractors.values()]
    summaries: list[dict[str, Any]] = []
    try:
        for frozen_row in sorted(frozen_rows, key=lambda row: row["task_id"]):
            task_id = frozen_row["task_id"]
            frozen_artifact = json.loads((frozen_private / f"{task_id}.json").read_text())
            task = frozen_artifact["task"]
            decomposition = frozen_artifact["decomposition"]
            if decomposition.get("status") != "ok":
                raise SystemExit(f"frozen decomposition is not usable: {task_id}")
            for extractor_label, atom_gateway in extractors.items():
                existing = {
                    mode: raw_dir / extractor_label / mode / f"{task_id}.json"
                    for mode in MODES
                }
                if all(path.is_file() for path in existing.values()):
                    for mode, path in existing.items():
                        construction = json.loads(path.read_text())["construction"]
                        summaries.append(_summary(task_id, extractor_label, mode,
                                                  construction))
                    continue
                strict, strict_raw = _construct_v9(
                    task, decomposition, index, proposer, sol,
                    atom_gateway=atom_gateway,
                    claimability_mode="strict_atom_preproposal")
                atoms = strict.get("evidence_atoms", [])
                conflicts = {row["requirement_id"] for row in
                             strict.get("claimability_gates", [])
                             if row.get("state") == "conflict"}
                frozen_atoms = (atoms, conflicts, [{"status": "frozen_reuse",
                                                    "extractor": extractor_label}])
                cells = {"strict_atom_preproposal": (strict, strict_raw)}
                for mode in MODES[1:]:
                    cells[mode] = _construct_v9(
                        task, decomposition, index, proposer, sol,
                        atom_gateway=atom_gateway, claimability_mode=mode,
                        frozen_atom_bundle=frozen_atoms)
                for mode, (construction, raw) in cells.items():
                    summaries.append(_summary(task_id, extractor_label, mode, construction))
                    cell_dir = raw_dir / extractor_label / mode
                    _write_private(cell_dir / f"{task_id}.json", {
                        "schema_version": SCHEMA,
                        "task": task,
                        "decomposition": decomposition,
                        "construction": construction,
                        "raw": raw,
                    })
                known_cost, missing_cost = _cost(gateways)
                total_cost = args.prior_cost_usd + (known_cost or 0.0)
                if missing_cost or known_cost is None or total_cost > args.budget_usd:
                    raise RuntimeError("diagnostic budget telemetry is incomplete or over cap")
    finally:
        for gateway in gateways:
            gateway.stop()

    known_cost, missing_cost = _cost(gateways)
    cells = []
    for extractor in EXTRACTORS:
        for mode in MODES:
            rows = [row for row in summaries if row["extractor"] == extractor
                    and row["claimability_mode"] == mode]
            totals = {key: sum(row["stage_counts"].get(key, 0) for row in rows)
                      for key in ("frozen_requirements", "requirements_with_receipts",
                                  "requirements_with_valid_atoms",
                                  "requirements_with_explicit_atoms",
                                  "preproposal_eligible_requirements",
                                  "requirements_with_normalized_claims",
                                  "critic_supported_requirements")}
            cells.append({"extractor": extractor, "claimability_mode": mode,
                          "task_count": len(rows), "stage_counts": totals,
                          "supported_requirement_coverage": (
                              totals["critic_supported_requirements"] /
                              totals["frozen_requirements"]
                              if totals["frozen_requirements"] else None),
                          "artifact_digest": digest(rows)})
    report = {
        "schema_version": SCHEMA,
        "boundary": "Frozen four-task diagnostic only; rubric, gold, and silver never enter construction.",
        "frozen_run_digest": digest(frozen_report),
        "catalog_digest": digest(catalog),
        "fixed_proposer": {"model": "deepseek/deepseek-v4-flash",
                           "provider": "deepinfra", "reasoning": "none"},
        "fixed_critic": {"model": "gpt-5.6-sol", "provider": "openai",
                         "reasoning": "low"},
        "extractors": {label: {"model": model, "provider": provider,
                                "reasoning": reasoning}
                       for label, (model, provider, reasoning) in EXTRACTORS.items()},
        "claimability_modes": list(MODES),
        "denominators": {"tasks": 4, "cells": len(cells),
                         "task_cells": len(summaries)},
        "cells": cells,
        "tasks": summaries,
        "telemetry": {"calls": sum(len(gateway.calls) for gateway in gateways),
                      "known_cost_usd": args.prior_cost_usd + (known_cost or 0.0),
                      "prior_attempt_cost_usd": args.prior_cost_usd,
                      "missing_cost_calls": missing_cost,
                      "budget_usd": args.budget_usd,
                      "fallback": "forbidden"},
    }
    _write_private(out / "sanitized-report.json", report)
    print(json.dumps({"ok": True, "task_cells": len(summaries),
                      "cost_usd": known_cost,
                      "report": str(out / "sanitized-report.json")}))


if __name__ == "__main__":
    main()

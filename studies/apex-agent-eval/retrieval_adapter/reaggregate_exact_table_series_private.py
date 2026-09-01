#!/usr/bin/env python3
"""Reaggregate saved v18 artifacts through requirement-aware TSV series binding.

This is a bounded construction experiment, not an answer execution.  It reuses
the frozen v18 retrieval receipts and period domains, adds only table-series
selection plus derivation replanning calls, and keeps all resulting objects in
the not-governed candidate state.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
from typing import Any

from exact_knowledge_contract import (
    assess_requirement_readiness,
    bind_candidate_objects,
    bind_numeric_atom,
    digest,
)
from reaggregate_exact_knowledge_stage_a_private import summarize
from run_claim_construction_private import Gateway
from run_exact_knowledge_stage_a_private import (
    ROUTE,
    SCHEMA,
    TASK_IDS,
    _extract_period_numeric_atoms,
    _plan_derivations,
    _plan_period_derivations,
)
from run_model_routing_qualification_private import terminal_telemetry


def _replace_period_series(
        private: dict[str, Any], numeric_gateway: Gateway,
        derivation_gateway: Gateway) -> tuple[dict[str, Any], dict[str, Any]]:
    updated = deepcopy(private)
    plan = updated["plan"]
    slots = plan["slots"]
    objects = updated["objects"]
    period_domains = objects.get("period_domains", [])
    period_requirement_ids = {row["requirement_id"] for row in period_domains}

    raw_rows, table_status = _extract_period_numeric_atoms(
        numeric_gateway, slots, updated["receipts"], period_domains)
    if table_status["status"] != "ok":
        raise RuntimeError("table-series selection was inconclusive")
    built_rows = []
    validation_failures = []
    for row in raw_rows:
        try:
            built_rows.append(bind_numeric_atom(row, updated["receipts"]))
        except (KeyError, TypeError, ValueError) as exc:
            validation_failures.append(
                "table_numeric_atoms:" + type(exc).__name__ + ":" + digest(str(exc))[-12:])

    retained = [row for row in objects["numeric_atoms"]
                if row["requirement_id"] not in period_requirement_ids]
    objects["numeric_atoms"] = [*retained, *built_rows]
    period_derivations, period_status = _plan_period_derivations(
        derivation_gateway, slots, objects)
    period_requirement_ids = {row["slot_id"] for row in slots
                              if row["slot_type"] == "value_by_period"}
    general_derivations, general_status = _plan_derivations(
        derivation_gateway,
        [row for row in slots if row["slot_id"] not in period_requirement_ids], objects)
    if period_status["status"] != "ok" or general_status["status"] != "ok":
        raise RuntimeError("table-series derivation replanning was inconclusive")
    derivations = [*period_derivations, *general_derivations]
    derivation_status = {"status": "ok", "derivation_count": len(derivations),
                         "period": period_status, "general": general_status,
                         "invariant_failures": [*period_status.get("invariant_failures", []),
                                                *general_status.get("invariant_failures", [])]}
    updated["derivations"] = derivations
    updated["objects"] = objects
    authority_screens = updated.get("authority_screens", [])
    refreshed_plan = bind_candidate_objects(
        updated["plan"],
        evidence_atoms=[*objects["evidence_atoms"], *objects["numeric_atoms"]],
        authority_nodes=objects["authority_nodes"], derivations=derivations,
        authority_screens=authority_screens)
    updated["plan"] = refreshed_plan
    updated["readiness"] = assess_requirement_readiness(
        refreshed_plan,
        evidence_atoms=[*objects["evidence_atoms"], *objects["numeric_atoms"]],
        authority_nodes=objects["authority_nodes"], derivations=derivations,
        period_domains=objects.get("period_domains", []),
        authority_screens=authority_screens)
    prior_failures = list(updated.get("invariant_failures", []))
    new_failures = [*table_status.get("invariant_failures", []),
                    *validation_failures,
                    *derivation_status.get("invariant_failures", [])]
    updated["prior_invariant_failures"] = prior_failures
    updated["invariant_failures"] = new_failures
    updated.setdefault("stage_status", {})["table_series_reaggregation"] = table_status
    updated["stage_status"]["table_series_derivation"] = derivation_status
    updated["reaggregation"] = {
        "source_private_artifact_digest": digest(private),
        "retrieval_reused": True,
        "period_domains_reused": True,
        "prior_numeric_atoms_replaced_for_period_requirements": True,
        "answer_executor_ran": False,
        "automatic_admission": False,
        "admission_authority": False,
    }
    return updated, {
        "period_requirement_count": len(period_requirement_ids),
        "retained_numeric_atom_count": len(retained),
        "constructed_table_cell_count": len(built_rows),
        "table_series_candidate_count": table_status["table_series_candidate_count"],
        "complete_table_series_candidate_count":
            table_status["complete_table_series_candidate_count"],
        "selected_series_count": table_status["selected_series_count"],
        "missing_complete_table_count": table_status["missing_complete_table_count"],
        "new_invariant_failure_count": len(new_failures),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-report", required=True, type=Path)
    parser.add_argument("--gateway-server", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--budget-usd", type=float, default=2.0)
    parser.add_argument("--timeout", type=float, default=360)
    args = parser.parse_args()
    source = json.loads(args.source_report.read_text())
    if source.get("schema_version") != SCHEMA or tuple(source.get("task_ids", [])) != TASK_IDS:
        raise ValueError("source report is not the frozen five-task v18 panel")
    source_raw = Path(source["raw_private_dir"])
    args.out.mkdir(parents=True, exist_ok=True); args.out.chmod(0o700)
    raw_dir = args.out / "raw"; raw_dir.mkdir(exist_ok=True); raw_dir.chmod(0o700)
    gateways = {
        role: Gateway(args.gateway_server, ROUTE["model"], ROUTE["provider"],
                      args.out, args.timeout, ROUTE["reasoning"], structured_output=True)
        for role in ("numeric", "derivation")
    }
    prior_summaries = {row["task_id"]: row for row in source["tasks"]}
    summaries = []
    construction_rows = []
    prompts = []
    quotes = []
    try:
        for task_id in TASK_IDS:
            private = json.loads((source_raw / f"{task_id}.json").read_text())
            updated, construction = _replace_period_series(
                private, gateways["numeric"], gateways["derivation"])
            target = raw_dir / f"{task_id}.json"
            target.write_text(json.dumps(updated, ensure_ascii=False, indent=2,
                                         sort_keys=True) + "\n")
            target.chmod(0o600)
            summaries.append(summarize(updated, prior_summaries[task_id]))
            construction_rows.append({"task_id": task_id, **construction})
            prompts.append(updated["task"]["prompt"])
            quotes.extend(str(row.get("quote") or "")
                          for row in updated.get("receipts", {}).values())
            if terminal_telemetry(gateways)["known_cost_usd"] > args.budget_usd:
                raise RuntimeError("table-series reaggregation exceeded the hard model budget")
    finally:
        for gateway in gateways.values():
            gateway.stop()

    telemetry = terminal_telemetry(gateways)
    serialized = json.dumps({"tasks": summaries, "construction": construction_rows},
                            ensure_ascii=False, sort_keys=True)
    leaks = (["task_prompt"] if any(row and row in serialized for row in prompts) else [])
    if any(row and row in serialized for row in quotes):
        leaks.append("source_quote")
    invalid = sum(row["slot_states"].get("invalid_binding", 0) for row in summaries)
    output_slots_valid = all(
        sum(slot["slot_type"] == "output_structure" for slot in row["slots"]) == 1
        for row in summaries)
    complete_calls = (not telemetry["missing_cost_calls"]
                      and not telemetry["missing_token_calls"])
    qualification = ("pass" if len(summaries) == len(TASK_IDS) and not invalid
                     and not leaks and output_slots_valid and complete_calls else "inconclusive")
    states = Counter(slot["state"] for row in summaries for slot in row["slots"])
    report = {
        "schema_version": SCHEMA,
        "boundary": ("Saved-artifact table-series construction reaggregation without an answer executor. "
                     "All objects remain not_governed candidates; Human Approval is the only admission path."),
        "task_ids": list(TASK_IDS),
        "task_input_digest": source["task_input_digest"],
        "catalog_digest": source["catalog_digest"],
        "authority_catalog_digest": source.get("authority_catalog_digest"),
        "frozen_plan_dir_digest": source.get("frozen_plan_dir_digest"),
        "route": ROUTE,
        "tasks": summaries,
        "construction": construction_rows,
        "denominators": {
            "tasks": len(summaries), "completed_tasks": len(summaries),
            "slots": sum(row["slot_count"] for row in summaries),
            "candidate_covered_slots": sum(row["candidate_coverage"] for row in summaries),
            "governed_covered_slots": sum(row["governed_coverage"] for row in summaries),
            "gaps": states["gap"], "invalid_bindings": invalid,
            "proposed_claims": 0, "numeric_gate_failures": 0,
        },
        "telemetry": {**telemetry, "budget_usd": args.budget_usd,
                      "construction_only_no_executor": True},
        "privacy": {"sanitized_report_leak_types": sorted(set(leaks)),
                    "task_prompts_included": False, "source_quotes_included": False,
                    "numeric_values_included": False, "authority_text_included": False},
        "governance": {"automatic_admission": False, "admission_authority": False,
                       "human_approval_only": True,
                       "executor_ready_tasks": sum(row["executor_ready"] for row in summaries)},
        "qualification": {"status": qualification,
                          "output_structure_gate": output_slots_valid,
                          "invalid_binding_gate": invalid == 0,
                          "privacy_gate": not leaks,
                          "cost_completeness_gate": not telemetry["missing_cost_calls"],
                          "token_completeness_gate": not telemetry["missing_token_calls"],
                          "gaps_allowed_and_explicit": True},
        "reaggregation": {"artifact_reuse": True,
                          "source_execution_report_digest": digest(source),
                          "retrieval_model_calls": 0,
                          "answer_executor_calls": 0,
                          "change": ("requirement-aware TSV series selection with deterministic "
                                     "period-value cell binding and derivation replanning")},
        "raw_private_dir": str(raw_dir),
    }
    report["report_digest"] = digest(report)
    (args.out / "sanitized-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": qualification, "tasks": len(summaries),
                      "slots": report["denominators"]["slots"],
                      "candidate_covered": report["denominators"]["candidate_covered_slots"],
                      "gaps": report["denominators"]["gaps"],
                      "calls": telemetry["calls"],
                      "cost_usd": telemetry["known_cost_usd"]}, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Reaggregate Stage A private artifacts after deterministic contract changes."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any

from exact_knowledge_contract import assess_requirement_readiness, digest, screen_authority_applicability
from run_exact_knowledge_stage_a_private import SCHEMA, TASK_IDS


def summarize(private: dict[str, Any], prior: dict[str, Any]) -> dict[str, Any]:
    plan = private["plan"]; objects = private["objects"]
    slot_descriptions = {row["slot_id"]: row["description"] for row in plan["slots"]}
    authority_screens = private.get("authority_screens") or [
        screen_authority_applicability(slot_descriptions[row["requirement_id"]], row)
        for row in objects["authority_nodes"]]
    readiness = assess_requirement_readiness(
        plan, evidence_atoms=[*objects["evidence_atoms"], *objects["numeric_atoms"]],
        authority_nodes=objects["authority_nodes"], derivations=private["derivations"],
        period_domains=objects.get("period_domains", []),
        authority_screens=authority_screens)
    states = Counter(row["state"] for row in readiness["slots"])
    kinds: dict[str, str] = {}
    for row in [*objects["evidence_atoms"], *objects["numeric_atoms"]]:
        kinds[row["atom_id"]] = "evidence_atom"
    for row in objects["authority_nodes"]:
        kinds[row["authority_id"]] = "authority_node"
    for row in private["derivations"]:
        kinds[row["derivation_id"]] = "derivation_node"
    paths = Counter(kinds.get(object_id, "unknown") for row in readiness["slots"]
                    for object_id in row["object_ids"])
    slot_types = {row["slot_id"]: row["slot_type"] for row in plan["slots"]}
    failures = private.get("invariant_failures", [])
    return {"task_id": private["task"]["task_id"], "task_name": private["task"].get("task_name"),
            "status": "ok", "output_type": private["task"]["expected_output"],
            "plan_digest": plan["plan_digest"], "slot_count": len(plan["slots"]),
            "slot_states": dict(sorted(states.items())),
            "slots": [{"slot_id": row["slot_id"], "slot_type": slot_types[row["slot_id"]],
                       "state": row["state"], "object_count": len(row["object_ids"]),
                       "missing_period_count": len(row.get("missing_periods", []))}
                      for row in readiness["slots"]],
            "object_counts": {"evidence_atoms": len(objects["evidence_atoms"]),
                              "numeric_atoms": len(objects["numeric_atoms"]),
                              "task_parameters": len(objects["task_parameters"]),
                              "authority_nodes": len(objects["authority_nodes"]),
                              "period_domains": len(objects.get("period_domains", [])),
                              "authority_screens": len(authority_screens),
                              "derivations": len(private["derivations"])},
            "completion_paths": dict(sorted(paths.items())),
            "invariant_failure_count": len(failures),
            "invariant_failure_types": dict(sorted(Counter(row.split(":", 2)[0]
                                                             for row in failures).items())),
            "candidate_coverage": readiness["candidate_coverage"],
            "governed_coverage": readiness["governed_coverage"],
            "executor_ready": readiness["executor_ready"],
            "elapsed_ms": prior.get("elapsed_ms"),
            "private_artifact_digest": digest(private),
            "reaggregated_readiness_digest": readiness["readiness_digest"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-report", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    source = json.loads(args.source_report.read_text())
    if source.get("schema_version") != SCHEMA or tuple(source.get("task_ids", [])) != TASK_IDS:
        raise ValueError("source report is not the frozen Stage A panel")
    raw_dir = Path(source["raw_private_dir"])
    prior = {row["task_id"]: row for row in source["tasks"]}
    tasks = []
    prompts = []; quotes = []
    for task_id in TASK_IDS:
        private = json.loads((raw_dir / f"{task_id}.json").read_text())
        tasks.append(summarize(private, prior[task_id]))
        prompts.append(private["task"]["prompt"])
        quotes.extend(str(row.get("quote") or "") for row in private.get("receipts", {}).values())
    serialized = json.dumps(tasks, ensure_ascii=False, sort_keys=True)
    leaks = (["task_prompt"] if any(row and row in serialized for row in prompts) else [])
    if any(row and row in serialized for row in quotes):
        leaks.append("source_quote")
    invalid = sum(row["slot_states"].get("invalid_binding", 0) for row in tasks)
    output_slots_valid = all(sum(slot["slot_type"] == "output_structure" for slot in row["slots"]) == 1
                             for row in tasks)
    telemetry = dict(source["telemetry"])
    qualification = ("pass" if len(tasks) == len(TASK_IDS) and not invalid and not leaks
                     and output_slots_valid and not telemetry["missing_cost_calls"] else "inconclusive")
    report = {"schema_version": SCHEMA,
              "boundary": source["boundary"], "task_ids": list(TASK_IDS),
              "task_input_digest": source["task_input_digest"],
              "catalog_digest": source["catalog_digest"], "route": source["route"],
              "tasks": tasks,
              "denominators": {"tasks": len(tasks), "completed_tasks": len(tasks),
                               "slots": sum(row["slot_count"] for row in tasks),
                               "candidate_covered_slots": sum(row["candidate_coverage"] for row in tasks),
                               "governed_covered_slots": sum(row["governed_coverage"] for row in tasks),
                               "gaps": sum(row["slot_states"].get("gap", 0) for row in tasks),
                               "invalid_bindings": invalid, "proposed_claims": 0,
                               "numeric_gate_failures": 0},
              "telemetry": telemetry,
              "privacy": {"sanitized_report_leak_types": sorted(set(leaks)),
                          "task_prompts_included": False, "source_quotes_included": False,
                          "numeric_values_included": False, "authority_text_included": False},
              "governance": {"automatic_admission": False, "admission_authority": False,
                             "human_approval_only": True, "executor_ready_tasks": 0},
              "qualification": {"status": qualification,
                                "output_structure_gate": output_slots_valid,
                                "invalid_binding_gate": invalid == 0,
                                "privacy_gate": not leaks,
                                "cost_completeness_gate": not telemetry["missing_cost_calls"],
                                "gaps_allowed_and_explicit": True},
              "reaggregation": {"artifact_reuse": True,
                                "source_execution_report_digest": digest(source),
                                "new_model_calls": 0,
                                "change": ("value_by_period_requires_source_bound_period_domain; "
                                           "authority_coverage_requires_applicability_screen")},
              "raw_private_dir": str(raw_dir)}
    report["report_digest"] = digest(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": qualification, "tasks": len(tasks),
                      "slots": report["denominators"]["slots"],
                      "candidate_covered": report["denominators"]["candidate_covered_slots"],
                      "gaps": report["denominators"]["gaps"],
                      "new_model_calls": 0}, sort_keys=True))


if __name__ == "__main__":
    main()

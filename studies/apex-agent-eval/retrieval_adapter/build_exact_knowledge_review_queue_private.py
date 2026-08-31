#!/usr/bin/env python3
"""Build a private human-review queue from repeated Stage B readiness runs.

The queue preserves source excerpts and candidate objects only in the private
output.  Its sanitized manifest reports stability and review dispositions
without reproducing prompts, values, authority text, or source excerpts.  It
does not create an approval receipt or admit any object.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any

from exact_knowledge_contract import digest
from run_exact_knowledge_stage_a_private import SCHEMA as RUN_SCHEMA, TASK_IDS


PRIVATE_SCHEMA = "proofpress/exact-knowledge-human-review-queue/v1"
SANITIZED_SCHEMA = "proofpress/exact-knowledge-review-stability/v1"


def _object_index(private: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    objects = private["objects"]
    for label, id_key in (("evidence_atoms", "atom_id"), ("numeric_atoms", "atom_id"),
                          ("task_parameters", "parameter_id"),
                          ("authority_nodes", "authority_id"),
                          ("period_domains", "period_domain_id")):
        for row in objects.get(label, []):
            result[row[id_key]] = row
    for row in private.get("derivations", []):
        result[row["derivation_id"]] = row
    for row in private.get("authority_screens", []):
        result[row["screen_id"]] = row
    return result


def _receipt_ids(objects: list[dict[str, Any]]) -> set[str]:
    result = {str(row.get("evidence_id") or "") for row in objects if row.get("evidence_id")}
    return {row for row in result if row}


def build(reports: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    if len(reports) < 2 or any(row.get("schema_version") != RUN_SCHEMA for row in reports):
        raise ValueError("at least two exact-knowledge run reports are required")
    invariants = ("task_ids", "task_input_digest", "catalog_digest",
                  "authority_catalog_digest", "frozen_plan_dir_digest", "route")
    for key in invariants:
        if any(row.get(key) != reports[0].get(key) for row in reports[1:]):
            raise ValueError(f"review runs disagree on frozen {key}")
    if tuple(reports[0].get("task_ids", [])) != TASK_IDS:
        raise ValueError("review queue requires the frozen five-task panel")

    run_privates: list[dict[str, dict[str, Any]]] = []
    for report in reports:
        raw_dir = Path(report["raw_private_dir"])
        run_privates.append({task_id: json.loads((raw_dir / f"{task_id}.json").read_text())
                             for task_id in TASK_IDS})

    private_tasks = []
    sanitized_tasks = []
    dispositions = Counter()
    stable_slot_count = 0
    shared_object_count = 0
    for task_id in TASK_IDS:
        task_runs = [row[task_id] for row in run_privates]
        plan_digests = {row["stage_status"]["compiler"]["source_plan_digest"]
                        for row in task_runs}
        if len(plan_digests) != 1:
            raise ValueError("review runs disagree on task plan digest")
        plan_slots = {row["slot_id"]: row for row in task_runs[0]["plan"]["slots"]}
        slot_basis = [{key: row.get(key) for key in (
            "slot_id", "slot_type", "description", "exactness", "expected_periods",
            "required_object_kinds", "output_format")} for row in task_runs[0]["plan"]["slots"]]
        for private in task_runs[1:]:
            compared = [{key: row.get(key) for key in (
                "slot_id", "slot_type", "description", "exactness", "expected_periods",
                "required_object_kinds", "output_format")} for row in private["plan"]["slots"]]
            if compared != slot_basis:
                raise ValueError("review runs disagree on frozen slot definitions")
        readiness_by_run = [{row["slot_id"]: row for row in private["readiness"]["slots"]}
                            for private in task_runs]
        indexes = [_object_index(row) for row in task_runs]
        items = []
        sanitized_slots = []
        for slot_id, slot in plan_slots.items():
            rows = [run[slot_id] for run in readiness_by_run]
            states = [row["state"] for row in rows]
            stable = len(set(states)) == 1
            if stable:
                stable_slot_count += 1
            eligible_sets = [set(row.get("eligible_object_ids", row.get("object_ids", [])))
                             for row in rows]
            shared_ids = set.intersection(*eligible_sets) if eligible_sets else set()
            shared_object_count += len(shared_ids)
            if slot["slot_type"] == "output_structure":
                disposition = "mechanical_output_structure"
            elif not stable:
                disposition = "construction_stability_adjudication"
            elif states[0] == "gap":
                disposition = "source_or_construction_gap"
            elif shared_ids:
                disposition = "human_approval_candidate"
            else:
                disposition = "semantic_candidate_reconciliation"
            dispositions[disposition] += 1

            run_candidates = []
            all_objects = []
            all_receipts: dict[str, dict[str, Any]] = {}
            for run_index, (private, index, readiness) in enumerate(
                    zip(task_runs, indexes, rows), 1):
                ids = set(readiness.get("object_ids", []))
                ids.update(readiness.get("period_domain_ids", []))
                for authority_id in readiness.get("eligible_object_ids", []):
                    for screen in private.get("authority_screens", []):
                        if screen.get("authority_id") == authority_id:
                            ids.add(screen["screen_id"])
                candidates = [index[object_id] for object_id in sorted(ids) if object_id in index]
                for evidence_id in _receipt_ids(candidates):
                    if evidence_id in private["receipts"]:
                        all_receipts[evidence_id] = private["receipts"][evidence_id]
                all_objects.extend(candidates)
                run_candidates.append({"run_index": run_index, "state": readiness["state"],
                                       "candidate_objects": candidates})
            items.append({
                "slot": slot, "states": states, "stable": stable,
                "shared_candidate_object_ids": sorted(shared_ids),
                "disposition": disposition, "runs": run_candidates,
                "receipts": all_receipts,
                "human_decision": None, "admission_receipt": None,
            })
            sanitized_slots.append({
                "slot_id": slot_id, "slot_type": slot["slot_type"], "states": states,
                "stable": stable, "shared_candidate_object_count": len(shared_ids),
                "candidate_object_count": len({digest(row) for row in all_objects}),
                "disposition": disposition,
            })
        private_tasks.append({"task_id": task_id, "plan_digest": next(iter(plan_digests)),
                              "review_items": items})
        sanitized_tasks.append({"task_id": task_id, "plan_digest": next(iter(plan_digests)),
                                "slots": sanitized_slots})

    report_digests = [digest(row) for row in reports]
    private_queue = {
        "schema_version": PRIVATE_SCHEMA, "source_report_digests": report_digests,
        "frozen_basis": {key: reports[0].get(key) for key in invariants},
        "tasks": private_tasks,
        "governance": {"automatic_admission": False, "admission_authority": False,
                       "human_approval_receipts": 0, "executor_allowed": False},
    }
    private_queue["queue_digest"] = digest(private_queue)
    total_slots = sum(len(row["slots"]) for row in sanitized_tasks)
    sanitized = {
        "schema_version": SANITIZED_SCHEMA, "source_report_digests": report_digests,
        "run_count": len(reports), "task_count": len(TASK_IDS), "slot_count": total_slots,
        "stable_slot_count": stable_slot_count,
        "unstable_slot_count": total_slots - stable_slot_count,
        "slot_agreement_rate": stable_slot_count / total_slots if total_slots else 0,
        "shared_candidate_object_count": shared_object_count,
        "dispositions": dict(sorted(dispositions.items())),
        "tasks": sanitized_tasks,
        "private_queue_digest": private_queue["queue_digest"],
        "privacy": {"task_prompts_included": False, "source_quotes_included": False,
                    "numeric_values_included": False, "authority_text_included": False},
        "governance": {"automatic_admission": False, "admission_authority": False,
                       "human_approval_receipts": 0, "executor_allowed": False},
        "decision": "stop_before_executor_pending_stability_gap_closure_and_human_approval",
    }
    sanitized["report_digest"] = digest(sanitized)
    return private_queue, sanitized


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reports", nargs="+", required=True, type=Path)
    parser.add_argument("--private-out", required=True, type=Path)
    parser.add_argument("--sanitized-out", required=True, type=Path)
    args = parser.parse_args()
    reports = [json.loads(path.read_text()) for path in args.reports]
    private_queue, sanitized = build(reports)
    args.private_out.parent.mkdir(parents=True, exist_ok=True)
    args.private_out.write_text(json.dumps(private_queue, indent=2, sort_keys=True) + "\n")
    args.private_out.chmod(0o600)
    args.sanitized_out.parent.mkdir(parents=True, exist_ok=True)
    args.sanitized_out.write_text(json.dumps(sanitized, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"runs": sanitized["run_count"], "slots": sanitized["slot_count"],
                      "stable": sanitized["stable_slot_count"],
                      "unstable": sanitized["unstable_slot_count"],
                      "human_approval_receipts": 0,
                      "executor_allowed": False}, sort_keys=True))


if __name__ == "__main__":
    main()

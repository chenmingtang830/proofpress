#!/usr/bin/env python3
"""Build a sanitized candidate-readiness report from private exact-task inputs.

The input may contain task prompts and source excerpts and must remain outside
Git.  The output intentionally contains digests, IDs, slot states, and counts;
it does not reproduce prompts, excerpts, numeric values, or authority text.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from exact_knowledge_contract import (
    assess_requirement_readiness,
    bind_numeric_atom,
    bind_requirement_objects,
    build_exact_derivation,
    compile_requirement_plan,
    digest,
    validate_authority_node,
)


REPORT_SCHEMA = "proofpress/exact-knowledge-candidate-readiness-report/v1"


def _index(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = str(row.get(key) or "")
        if not value or value in result:
            raise ValueError(f"{key} values must be present and unique")
        result[value] = row
    return result


def build_candidate_readiness(bundle: dict[str, Any]) -> dict[str, Any]:
    """Construct typed candidates and report coverage without admitting them."""
    if not isinstance(bundle, dict):
        raise ValueError("readiness bundle must be an object")
    receipts = _index(list(bundle.get("receipts") or []), "evidence_id")
    plan = compile_requirement_plan(
        str(bundle.get("task_prompt") or ""),
        list(bundle.get("slots") or []),
        output_type=str(bundle.get("output_type") or ""),
    )
    atoms = [bind_numeric_atom(row, receipts)
             for row in list(bundle.get("numeric_atom_payloads") or [])]
    atom_index = _index(atoms, "atom_id")
    authorities = [validate_authority_node(row, receipts)
                   for row in list(bundle.get("authority_nodes") or [])]
    authority_index = _index(authorities, "authority_id")
    derivations: list[dict[str, Any]] = []
    for spec in list(bundle.get("derivations") or []):
        derivations.append(build_exact_derivation(
            requirement_id=str(spec.get("requirement_id") or ""),
            expression=str(spec.get("expression") or ""),
            variables=dict(spec.get("variables") or {}),
            input_bindings=dict(spec.get("input_bindings") or {}),
            numeric_atoms=atom_index,
            output_unit=str(spec.get("output_unit") or ""),
            entity=str(spec.get("entity") or ""),
            period=str(spec.get("period") or ""),
            round_places=spec.get("round_places", 2),
        ))
    derivation_index = _index(derivations, "derivation_id")
    plan = bind_requirement_objects(plan, dict(bundle.get("assignments") or {}))
    readiness = assess_requirement_readiness(
        plan,
        evidence_atoms=atoms,
        authority_nodes=authorities,
        derivations=derivations,
    )
    gaps = [row["slot_id"] for row in readiness["slots"] if row["state"] == "gap"]
    invalid = [row["slot_id"] for row in readiness["slots"]
               if row["state"] == "invalid_binding"]
    report = {
        "schema_version": REPORT_SCHEMA,
        "input_digest": digest(bundle),
        "task_prompt_digest": plan["task_prompt_digest"],
        "plan_digest": plan["plan_digest"],
        "readiness_digest": readiness["readiness_digest"],
        "slot_states": [{"slot_id": row["slot_id"], "state": row["state"]}
                        for row in readiness["slots"]],
        "candidate_coverage": readiness["candidate_coverage"],
        "governed_coverage": readiness["governed_coverage"],
        "executor_ready": readiness["executor_ready"],
        "gap_slot_ids": gaps,
        "invalid_slot_ids": invalid,
        "object_counts": {
            "numeric_atoms": len(atom_index),
            "authority_nodes": len(authority_index),
            "derivations": len(derivation_index),
        },
        "automatic_admission": False,
        "admission_authority": False,
    }
    report["report_digest"] = digest(report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    bundle = json.loads(args.input.read_text(encoding="utf-8"))
    report = build_candidate_readiness(bundle)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")


if __name__ == "__main__":
    main()

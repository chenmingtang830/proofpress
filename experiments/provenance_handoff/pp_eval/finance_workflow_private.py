"""Private Finance upstream task-quality qualification pipeline.

Raw prompts, evidence packets, and model outputs remain in the caller-selected
private run directory. The public report contains only counts, digests, gates,
and aggregate Gateway telemetry.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
import shutil
import hashlib
from pathlib import PurePosixPath
import re
import zipfile
from typing import Any

from pp_eval.finance_e2e_v2 import (
    ATOM_SCHEMA,
    MATERIAL_GAP_KINDS,
    construct_observed_facts,
    detect_material_conflicts,
    digest,
    execution_gate,
    extract_pdf_receipts,
    requirement_completeness,
    retrieve_receipts,
    validate_critic_verdicts,
    validate_finance_atom,
    validate_requirements,
    workbook_index_to_receipts,
)
from pp_eval.finance_gateway import FinanceGateway, ROUTES, audit_receipts
from pp_eval.storage import sha256_file
from pp_eval.apex_ib_pr36 import write_xlsx_evidence_index

_PATH_TOKEN = re.compile(r"[A-Za-z0-9]+")
_PATH_STOP = {"the", "and", "use", "using", "with", "from", "file", "files", "model",
              "analysis", "calculate", "assume", "task", "what", "would", "based"}


DECOMPOSITION_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["requirements"],
    "properties": {"requirements": {"type": "array", "minItems": 1, "maxItems": 20,
        "items": {"type": "object", "additionalProperties": False,
            "required": ["requirement_id", "kind", "requirement"],
            "properties": {
                "requirement_id": {"type": "string", "maxLength": 64},
                "kind": {"type": "string", "enum": ["deliverable", "calculation", "input", "output", "validation"]},
                "requirement": {"type": "string", "maxLength": 500},
            }}}},
}

ATOM_OUTPUT_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["atoms"],
    "properties": {"atoms": {"type": "array", "maxItems": 12,
        "items": {"type": "object", "additionalProperties": False,
            "required": ["atom_id", "requirement_id", "evidence_id", "receipt_digest",
                         "subject", "predicate", "value", "support_mode", "locator",
                         "exact_source_value", "unit", "currency", "period", "as_of_date",
                         "source_version", "qualification"],
            "properties": {
                "atom_id": {"type": "string", "maxLength": 80},
                "requirement_id": {"type": "string", "maxLength": 64},
                "evidence_id": {"type": "string", "maxLength": 80},
                "receipt_digest": {"type": "string", "maxLength": 80},
                "subject": {"type": "string", "maxLength": 240},
                "predicate": {"type": "string", "maxLength": 120},
                "value": {"type": "string", "maxLength": 300},
                "support_mode": {"type": "string", "enum": ["explicit", "inferred"]},
                "locator": {"type": "string", "maxLength": 500},
                "exact_source_value": {"anyOf": [{"type": "string"}, {"type": "number"},
                                                     {"type": "boolean"}, {"type": "null"}]},
                "unit": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                "currency": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                "period": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                "as_of_date": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                "source_version": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                "qualification": {"anyOf": [{"type": "string"}, {"type": "null"}]},
            }}}},
}

CRITIC_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["verdicts"],
    "properties": {"verdicts": {"type": "array", "maxItems": 40,
        "items": {"type": "object", "additionalProperties": False,
            "required": ["record_id", "verdict", "reason"],
            "properties": {
                "record_id": {"type": "string", "maxLength": 100},
                "verdict": {"type": "string", "enum": ["supported", "partially_supported", "unsupported", "conflicted", "misclassified"]},
                "reason": {"type": "string", "maxLength": 300},
            }}}},
}

COMPLETENESS_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["resolutions"],
    "properties": {"resolutions": {"type": "array", "minItems": 1, "maxItems": 20,
        "items": {"type": "object", "additionalProperties": False,
            "required": ["requirement_id", "status", "gap_kind", "reason"],
            "properties": {
                "requirement_id": {"type": "string", "maxLength": 64},
                "status": {"type": "string", "enum": ["covered", "material_gap"]},
                "gap_kind": {"anyOf": [{"type": "string", "enum": sorted(MATERIAL_GAP_KINDS)}, {"type": "null"}]},
                "reason": {"type": "string", "maxLength": 300},
            }}}},
}


def select_data_room_members(members: list[str], task_prompt: str,
                             *, pdf_limit: int = 32) -> list[str]:
    """Globally rank supported data-room sources without reading hidden task fields."""
    query = {token.casefold() for token in _PATH_TOKEN.findall(task_prompt)
             if len(token) >= 3 and token.casefold() not in _PATH_STOP}
    workbooks = sorted(path for path in members if path.startswith("filesystem/")
                       and path.lower().endswith(".xlsx"))
    scored = []
    for path in members:
        if not path.startswith("filesystem/") or not path.lower().endswith(".pdf"):
            continue
        tokens = {token.casefold() for token in _PATH_TOKEN.findall(path)
                  if len(token) >= 3}
        overlap = len(query & tokens)
        if overlap:
            scored.append((overlap, path))
    scored.sort(key=lambda row: (-row[0], row[1]))
    return workbooks + [path for _, path in scored[:pdf_limit]]


def materialize_compiler_data_room(*, world_zip: Path, destination: Path,
                                   public_task: dict[str, Any]) -> dict[str, Any]:
    """Inventory the full frozen world, then extract only deterministic sources."""
    destination.mkdir(parents=True, exist_ok=False)
    with zipfile.ZipFile(world_zip) as archive:
        members = sorted(name for name in archive.namelist()
                         if not name.endswith("/") and name.startswith("filesystem/"))
        selected = select_data_room_members(members, public_task["prompt"])
        inventory = []
        selected_records = []
        for member in members:
            path = PurePosixPath(member)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError("unsafe frozen world member")
            payload = archive.read(member)
            row = {"path": member, "bytes": len(payload),
                   "sha256": hashlib.sha256(payload).hexdigest(),
                   "selected": member in selected}
            inventory.append(row)
            if member in selected:
                target = destination / member
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(payload)
                selected_records.append({key: row[key] for key in ("path", "bytes", "sha256")})
    governed = destination / "filesystem" / "Governed"
    governed.mkdir(parents=True, exist_ok=True)
    (governed / "public_task.json").write_text(
        json.dumps(public_task, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    manifest = {
        "schema_version": "proofpress/finance-compiler-data-room/v2",
        "task_id": public_task["task_id"], "world_id": public_task["world_id"],
        "inventory_count": len(inventory), "selected_source_count": len(selected_records),
        "files": selected_records, "inventory_digest": digest(inventory),
        "selection_rule": "all_xlsx_plus_top32_prompt_path_overlap_pdfs",
    }
    manifest["manifest_digest"] = digest(manifest)
    (governed / "source_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    (destination / "package_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    write_xlsx_evidence_index(destination, selected_records)
    return manifest


def load_receipts(evidence_root: Path) -> list[dict[str, Any]]:
    governed = evidence_root / "filesystem" / "Governed"
    catalog = json.loads((governed / "evidence_index.json").read_text())
    receipts: list[dict[str, Any]] = []
    for row in catalog.get("sheets", []):
        sheet = json.loads((evidence_root / row["index_path"]).read_text())
        receipts.extend(workbook_index_to_receipts(
            artifact=sheet["artifact"], source_sha256="sha256:" + sheet["source_sha256"],
            sheets=[{"sheet": sheet["sheet"], "cells": sheet["cells"]}],
        ))
    manifest = json.loads((governed / "source_manifest.json").read_text())
    for row in manifest.get("files", []):
        artifact = row.get("path")
        if not isinstance(artifact, str) or not artifact.lower().endswith(".pdf"):
            continue
        receipts.extend(extract_pdf_receipts(
            path=str(evidence_root / artifact), artifact=artifact,
            source_sha256="sha256:" + row["sha256"]))
    if not receipts:
        raise ValueError("Finance evidence package has no workbook receipts")
    return receipts


def _receipt_packet(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fields = ("evidence_id", "receipt_digest", "locator", "source_value", "formula",
              "value_semantics", "local_context")
    return [{field: row.get(field) for field in fields} for row in rows]


def _formula_records(atoms: list[dict[str, Any]], receipts: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for atom in atoms:
        receipt = receipts[atom["evidence_id"]]
        formula = receipt.get("formula")
        if not formula or atom.get("support_mode") != "explicit":
            continue
        record = {
            "id": f"finance_formula_{len(records)+1:04d}_{atom['atom_id'][-8:]}",
            "requirement_id": atom["requirement_id"],
            "record_type": "calculation_choice",
            "statement": f"Source formula at {atom['locator']} is {formula}",
            "formula": formula, "status": "unresolved",
            "atom_ids": [atom["atom_id"]], "evidence_ids": [atom["evidence_id"]],
            "receipt_digests": [atom["receipt_digest"]],
        }
        record["construction_digest"] = digest(record)
        records.append(record)
    return records


def materialize_governed_overlay(*, evidence_root: Path, destination: Path,
                                 task: dict[str, Any], requirements: list[dict[str, Any]],
                                 records: list[dict[str, Any]], receipts: dict[str, dict[str, Any]],
                                 execution_receipt: dict[str, Any],
                                 target_artifacts: list[str]) -> dict[str, Any]:
    """Materialize only pristine targets, allowed records, and source extracts."""
    if execution_receipt.get("decision") != "allow":
        raise ValueError("blocked working set cannot be materialized")
    destination.mkdir(parents=True, exist_ok=False)
    copied = []
    for artifact in target_artifacts:
        source = evidence_root / artifact
        if not source.is_file():
            raise ValueError("pristine target artifact is missing")
        target = destination / artifact
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append({"path": artifact, "sha256": sha256_file(target),
                       "bytes": target.stat().st_size})
    governed = destination / "filesystem" / "Governed"
    governed.mkdir(parents=True, exist_ok=True)
    evidence_ids = {evidence_id for record in records
                    for evidence_id in record.get("evidence_ids", [])}
    extracts = [_receipt_packet([receipts[evidence_id]])[0]
                for evidence_id in sorted(evidence_ids)]
    working_set = {
        "schema_version": "proofpress/finance-governed-working-set/v2",
        "task_id": task["task_id"], "requirements": requirements,
        "records": records, "production_reliance": "prohibited",
        "admission": None,
    }
    working_set["working_set_digest"] = digest(working_set)
    files = {
        "public_task.json": task,
        "working_set.json": working_set,
        "permitted_source_extracts.json": {
            "schema_version": "proofpress/finance-source-extracts/v2",
            "extracts": extracts, "extract_digest": digest(extracts),
        },
        "execution_receipt.json": execution_receipt,
    }
    for name, value in files.items():
        (governed / name).write_text(json.dumps(value, ensure_ascii=False,
                                                indent=2, sort_keys=True) + "\n")
    manifest = {
        "schema_version": "proofpress/finance-governed-overlay/v2",
        "task_id": task["task_id"], "target_artifacts": copied,
        "working_set_digest": working_set["working_set_digest"],
        "permitted_extract_count": len(extracts),
        "full_data_room_present": False,
        "execution_gate": "allow",
    }
    manifest["overlay_digest"] = digest(manifest)
    (destination / "package_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def run_task_quality(*, repo: Path, evidence_root: Path, output: Path,
                     api_key: str, task_id: str,
                     target_artifacts: list[str]) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=False)
    raw = output / "raw_private"
    raw.mkdir(mode=0o700)
    public_task = json.loads((evidence_root / "filesystem/Governed/public_task.json").read_text())
    if public_task.get("task_id") != task_id:
        raise ValueError("public task does not match qualification task")
    gateways: dict[str, FinanceGateway] = {}
    call_counts: Counter[str] = Counter()

    def gateway(role: str) -> FinanceGateway:
        if role not in gateways:
            gateways[role] = FinanceGateway(repo=repo, route=ROUTES[role],
                                            output=raw / f"gateway-{role}", api_key=api_key)
        return gateways[role]

    status = "inconclusive"
    try:
        call_counts["decomposition"] += 1
        decomposition = gateway("decomposition").call(
            system="Decompose the public Investment Banking task. Do not answer it and do not use hidden evaluation material.",
            prompt=public_task["prompt"], schema=DECOMPOSITION_SCHEMA,
            schema_name="finance_requirements", max_tokens=4000)
        frozen_requirements = validate_requirements(decomposition["requirements"])
        requirements = frozen_requirements["requirements"]
        receipts = load_receipts(evidence_root)
        receipt_map = {row["evidence_id"]: row for row in receipts}
        retrieved = retrieve_receipts(requirements, receipts, limit_per_requirement=40)
        atoms = []
        extraction_failures = []
        for requirement in requirements:
            requirement_id = requirement["requirement_id"]
            # The governed set must equip the executor, never reveal a cached or
            # precomputed requested output. Output completeness is assessed from
            # its dependencies after extraction, not by extracting output cells.
            if requirement["kind"] == "output":
                continue
            packet = _receipt_packet(retrieved[requirement_id])
            if not packet:
                extraction_failures.append({"requirement_id": requirement_id, "reason": "no_lexical_receipts"})
                continue
            call_counts["atom_extraction"] += 1
            value = gateway("atom_extraction").call(
                system="Extract narrow evidence atoms only. Copy IDs, locator, digest, and exact_source_value exactly from supplied receipts. Do not calculate requested outputs or grant authority.",
                prompt=json.dumps({"requirement": requirement, "receipts": packet}, ensure_ascii=False),
                schema=ATOM_OUTPUT_SCHEMA, schema_name="finance_evidence_atoms", max_tokens=6000)
            for atom in value.get("atoms", []):
                try:
                    if atom.get("requirement_id") != requirement_id:
                        raise ValueError("atom requirement mismatch")
                    atoms.append(validate_finance_atom(atom, receipt_map))
                except ValueError as error:
                    extraction_failures.append({"requirement_id": requirement_id,
                                                "reason": type(error).__name__,
                                                "atom_digest": digest(atom)})
        records = construct_observed_facts(atoms) + _formula_records(atoms, receipt_map)
        by_requirement: dict[str, list[dict[str, Any]]] = {}
        for record in records:
            by_requirement.setdefault(record["requirement_id"], []).append(record)
        critic_verdicts: dict[str, dict[str, Any]] = {}
        for requirement in requirements:
            scoped = by_requirement.get(requirement["requirement_id"], [])
            if not scoped:
                continue
            call_counts["critic"] += 1
            value = gateway("critic").call(
                system="Independently audit every record against its source-bound fields. A record is supported only when the entire narrow statement and type are entailed. Do not repair or rewrite it.",
                prompt=json.dumps({"requirement": requirement, "records": scoped,
                                   "receipts": _receipt_packet([receipt_map[evidence_id]
                                       for record in scoped for evidence_id in record["evidence_ids"]])},
                                  ensure_ascii=False),
                schema=CRITIC_SCHEMA, schema_name="finance_critic_verdicts", max_tokens=6000)
            critic_verdicts.update(validate_critic_verdicts(scoped, value))
        supported = []
        for record in records:
            updated = dict(record)
            updated["status"] = ("supported" if critic_verdicts.get(record["id"], {}).get("verdict") == "supported"
                                 else "unsupported")
            if updated["status"] == "supported":
                supported.append(updated)
        call_counts["completeness"] += 1
        resolutions = gateway("completeness").call(
            system="Audit requirement completeness, not record truth. Declare a material gap whenever the supported records do not fully equip a downstream executor. Never invent missing evidence.",
            prompt=json.dumps({"requirements": requirements,
                               "supported_records": [{key: row.get(key) for key in
                                   ("id", "requirement_id", "record_type", "statement")}
                                  for row in supported]}, ensure_ascii=False),
            schema=COMPLETENESS_SCHEMA, schema_name="finance_requirement_completeness",
            max_tokens=5000)
        known_requirements = {row["requirement_id"] for row in requirements}
        resolution_by_id = {row.get("requirement_id"): row for row in resolutions.get("resolutions", [])
                            if row.get("requirement_id") in known_requirements}
        gaps = []
        covered_requirement_ids = set()
        for requirement in requirements:
            requirement_id = requirement["requirement_id"]
            row = resolution_by_id.get(requirement_id)
            if row and row.get("status") == "covered":
                covered_requirement_ids.add(requirement_id)
            else:
                gaps.append({"gap_id": f"gap_{len(gaps)+1:03d}", "requirement_id": requirement_id,
                             "kind": (row or {}).get("gap_kind") or "missing_input",
                             "material": True, "reason": (row or {}).get("reason") or "missing_completeness_resolution"})
        completeness = requirement_completeness(
            requirements, supported, gaps,
            covered_requirement_ids=covered_requirement_ids)
        conflicts = detect_material_conflicts(supported)
        route_audits = {role: audit_receipts(item.rows(), ROUTES[role], call_counts[role])
                        for role, item in gateways.items()}
        telemetry_complete = bool(route_audits) and all(row["decision"] == "allow" for row in route_audits.values())
        gate = execution_gate(
            records=supported,
            critic_verdicts={key: value for key, value in critic_verdicts.items() if key in {r["id"] for r in supported}},
            completeness=completeness, conflicts=conflicts,
            source_bindings_complete=not extraction_failures,
            telemetry_complete=telemetry_complete,
            requested_output_leakage=any(
                record.get("requirement_id") in {row["requirement_id"] for row in requirements
                                                  if row["kind"] == "output"}
                for record in supported))
        private = {"task": public_task, "requirements": requirements, "receipts": receipts,
                   "retrieved_receipt_ids": {key: [row["evidence_id"] for row in value]
                                              for key, value in retrieved.items()},
                   "atoms": atoms, "records": records, "critic_verdicts": critic_verdicts,
                   "supported_records": supported, "resolutions": resolutions,
                   "gaps": gaps, "completeness": completeness, "conflicts": conflicts,
                   "execution_gate": gate, "extraction_failures": extraction_failures}
        (raw / "task-quality-private.json").write_text(
            json.dumps(private, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        status = "allow" if gate["decision"] == "allow" else "block"
        report = {
            "schema_version": "proofpress/finance-upstream-task-quality/v1",
            "boundary": "Development qualification; zero executor, grader, calibration, or formal artifacts.",
            "task_id": task_id, "decision": status,
            "denominators": {"tasks": 1, "requirements": len(requirements),
                             "receipts": len(receipts), "atoms": len(atoms),
                             "records": len(records), "supported_records": len(supported),
                             "material_gaps": len(gaps), "extraction_failures": len(extraction_failures)},
            "execution_gate": gate, "route_audits": route_audits,
            "known_cost_usd": sum(row["known_cost_usd"] for row in route_audits.values()),
            "formal_denominator": 0, "calibration_denominator": 0,
            "private_artifact_digest": digest(private),
        }
        if gate["decision"] == "allow":
            overlay_manifest = materialize_governed_overlay(
                evidence_root=evidence_root, destination=output / "governed_overlay",
                task=public_task, requirements=requirements, records=supported,
                receipts=receipt_map, execution_receipt=gate,
                target_artifacts=target_artifacts)
            report["governed_overlay"] = overlay_manifest
        (output / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        return report
    finally:
        for item in gateways.values():
            item.stop()

"""Frozen PR36-style APEX Investment Banking experiment machinery.

This module is deliberately separate from :mod:`apex_ib`, whose completed run
is qualification evidence only.  Here, treatment construction happens before
a fresh executor is invoked.  Hidden benchmark rubric and gold fields never
enter builder or executor packages.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import shutil
import signal
import subprocess
import tarfile
import time
import uuid
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from .storage import sha256_file, write_json
from .apex_official import _environment, _git_commit, _image_id


SCHEMA = "proofpress/apex-ib-pr36/v1"
WORLD_ID = "world_f83f49b3776b4b5e870c36091f7e2b0b"
EXECUTOR_MODEL = "inclusionai/ling-3.0-flash-fin"
TREATMENT_PROPOSER_MODEL = "deepseek/deepseek-v4-flash"
JUDGE_MODEL = "google/gemini-3.1-pro-preview"
QUALIFICATION_TASK_ID = "task_9ba58a6197114140877a1df1754d2993"
FORMAL_TASK_IDS = (
    "task_9909f2ec2bbb4899ba7a956a475dfc01",
    "task_4f291b8b066e413f8cd0a99c593b89e8",
)
FINANCE_E2E_V2_FORMAL_TASK_IDS = (
    "task_9909f2ec2bbb4899ba7a956a475dfc01",
    "task_b2d58a02b48b4b5abd886aafac8b1c7e",
)
ALL_TASK_IDS = (QUALIFICATION_TASK_ID,) + FORMAL_TASK_IDS
EXECUTOR_ATTEMPTS = 3
GRADER_REPETITIONS = 3
DEFAULT_SEED = 20260828
AGENT_MAX_STEPS = 60
AGENT_TIMEOUT_SECONDS = 2_400
WATCHDOG_SECONDS = 2_700
MODEL_RESPONSE_TIMEOUT_SECONDS = 360
AI_GATEWAY_BASE = "https://ai-gateway.vercel.sh/v1"
ENVIRONMENT_IMAGE = "proofpress_ling_fin_apex_ckostp-environment:latest"
MIN_CALIBRATION_FREE_BYTES = 20 * 1024**3
# Formal cells are strictly serial and compact after every stage, so peak disk
# is bounded like calibration rather than accumulating across the 12 artifacts.
MIN_FORMAL_FREE_BYTES = 25 * 1024**3

MERGER_MODEL = "filesystem/04_Models/Merger-Acquisition Analysis/Merger Model - Barings BDC vF.xlsx"
VALUATION_MODEL = "filesystem/04_Models/BBDC Valuation Model/BBDC Valuation Model vF.xlsx"
COMPS_MODEL = "filesystem/02_Trading Comps Analysis/Comps Analysis vF.xlsx"
WHF_10K = "filesystem/02_Trading Comps Analysis/Comps Data/WHF/01a_SEC_Filings/WHF_10K_12.31.2024.pdf"


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    role: str
    evidence_allowlist: tuple[str, ...]
    final_artifact_allowlist: tuple[str, ...]


TASK_SPECS: dict[str, TaskSpec] = {
    QUALIFICATION_TASK_ID: TaskSpec(
        task_id=QUALIFICATION_TASK_ID,
        role="calibration",
        evidence_allowlist=(MERGER_MODEL,),
        final_artifact_allowlist=(MERGER_MODEL,),
    ),
    FORMAL_TASK_IDS[0]: TaskSpec(
        task_id=FORMAL_TASK_IDS[0],
        role="formal",
        evidence_allowlist=(MERGER_MODEL, WHF_10K),
        final_artifact_allowlist=(MERGER_MODEL,),
    ),
    FORMAL_TASK_IDS[1]: TaskSpec(
        task_id=FORMAL_TASK_IDS[1],
        role="formal",
        evidence_allowlist=(MERGER_MODEL, VALUATION_MODEL, COMPS_MODEL),
        final_artifact_allowlist=(MERGER_MODEL,),
    ),
    FINANCE_E2E_V2_FORMAL_TASK_IDS[1]: TaskSpec(
        task_id=FINANCE_E2E_V2_FORMAL_TASK_IDS[1],
        role="formal-v2",
        evidence_allowlist=(MERGER_MODEL,),
        final_artifact_allowlist=(MERGER_MODEL,),
    ),
}


def _canonical(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def trajectory_telemetry(trajectory: dict[str, Any], expected_model: str) -> dict[str, Any]:
    """Summarize terminal Gateway receipts and fail closed on missing routing/cost data."""
    usage = trajectory.get("usage") if isinstance(trajectory.get("usage"), dict) else {}
    call_log = usage.get("call_log") if isinstance(usage.get("call_log"), list) else []
    receipts: list[dict[str, Any]] = []
    for message in trajectory.get("messages", []):
        if not isinstance(message, dict):
            continue
        fields = message.get("provider_specific_fields")
        metadata = fields.get("provider_metadata") if isinstance(fields, dict) else None
        gateway = metadata.get("gateway") if isinstance(metadata, dict) else None
        if isinstance(gateway, dict):
            receipts.append(gateway)
    models = sorted({str(row.get("routing", {}).get("originalModelId")) for row in receipts})
    providers = sorted({str(row.get("routing", {}).get("finalProvider")) for row in receipts})
    costs: list[float] = []
    missing_cost = 0
    no_fallback = True
    provider_attempt_counts: list[int] = []
    for row in receipts:
        routing = row.get("routing") if isinstance(row.get("routing"), dict) else {}
        try:
            costs.append(float(row["cost"]))
        except (KeyError, TypeError, ValueError):
            missing_cost += 1
        provider_attempt_count = routing.get("totalProviderAttemptCount")
        if not isinstance(provider_attempt_count, int):
            provider_attempt_count = routing.get("providerAttemptCount")
        if not isinstance(provider_attempt_count, int):
            provider_attempt_count = 0
        provider_attempt_counts.append(provider_attempt_count)
        no_fallback = (
            no_fallback
            and routing.get("modelAttemptCount") == 1
            and provider_attempt_count == 1
        )
    complete = bool(call_log) and len(receipts) == len(call_log) and not missing_cost
    complete = complete and models == [expected_model] and bool(providers) and no_fallback
    return {
        "status": "complete" if complete else "incomplete",
        "model": expected_model,
        "providers": providers,
        "calls": len(call_log),
        "terminal_receipts": len(receipts),
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
        "reasoning_tokens": usage.get("reasoning_tokens"),
        "cached_tokens": usage.get("cached_tokens"),
        "known_cost_usd": round(sum(costs), 12),
        "missing_cost_calls": missing_cost + max(0, len(call_log) - len(receipts)),
        "fallback": "forbidden",
        "no_fallback_observed": no_fallback,
        "provider_attempt_counts": provider_attempt_counts,
        "provider_fallback_observed": any(count > 1 for count in provider_attempt_counts),
    }


def grader_telemetry(receipt_path: Path, expected_model: str) -> dict[str, Any]:
    """Summarize grading Gateway receipts and fail closed on incomplete calls."""
    rows: list[dict[str, Any]] = []
    if receipt_path.is_file():
        for line in receipt_path.read_text().splitlines():
            if line.strip():
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise ValueError("grader receipt must be a JSON object")
                rows.append(value)
    providers: set[str] = set()
    costs: list[float] = []
    prompt_tokens = completion_tokens = total_tokens = 0
    complete = bool(rows)
    no_fallback = True
    for row in rows:
        gateway = row.get("gateway") if isinstance(row.get("gateway"), dict) else {}
        routing = gateway.get("routing") if isinstance(gateway.get("routing"), dict) else {}
        usage = row.get("usage") if isinstance(row.get("usage"), dict) else {}
        provider = routing.get("finalProvider")
        if provider:
            providers.add(str(provider))
        try:
            costs.append(float(gateway["cost"]))
        except (KeyError, TypeError, ValueError):
            complete = False
        model_ok = routing.get("originalModelId") == expected_model
        provider_ok = bool(provider)
        token_values = (usage.get("prompt_tokens"), usage.get("completion_tokens"), usage.get("total_tokens"))
        tokens_ok = all(isinstance(value, int) and value >= 0 for value in token_values)
        no_fallback = no_fallback and routing.get("modelAttemptCount") == 1
        complete = complete and model_ok and provider_ok and tokens_ok
        if tokens_ok:
            prompt_tokens += token_values[0]
            completion_tokens += token_values[1]
            total_tokens += token_values[2]
    complete = complete and no_fallback
    return {
        "status": "complete" if complete else "incomplete", "model": expected_model,
        "providers": sorted(providers), "calls": len(rows), "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens, "total_tokens": total_tokens,
        "known_cost_usd": round(sum(costs), 12), "costed_calls": len(costs),
        "no_fallback_observed": no_fallback, "receipt_path": str(receipt_path),
    }


def derived_grading_llm_source(source: str) -> str:
    """Instrument the pinned grader's central LLM wrapper with terminal receipts."""
    import_anchor = "import time\n"
    return_anchor = """        response_obj = validated
        ok = True
        return validated
"""
    if source.count(import_anchor) != 1 or source.count(return_anchor) != 1:
        raise ValueError("pinned grading LLM wrapper changed; receipt hook cannot be applied")
    imports = "import json\nimport os\nfrom pathlib import Path\n" + import_anchor
    receipt = """        response_obj = validated
        receipt_path = os.environ.get("APEX_IB_GRADER_RECEIPTS")
        if receipt_path:
            response_dump = validated.model_dump(mode="json")
            choices = response_dump.get("choices") or []
            message = choices[0].get("message", {}) if choices else {}
            fields = message.get("provider_specific_fields") or {}
            metadata = fields.get("provider_metadata") or {}
            record = {"model": model, "usage": response_dump.get("usage") or {}, "gateway": metadata.get("gateway") or {}}
            with Path(receipt_path).open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, sort_keys=True) + "\\n")
        ok = True
        return validated
"""
    return source.replace(import_anchor, imports, 1).replace(return_anchor, receipt, 1)


def load_public_task(tasks_path: Path, task_id: str) -> dict[str, Any]:
    """Return only executor-public task fields; hidden fields are discarded."""
    if task_id not in TASK_SPECS:
        raise ValueError(f"task is not frozen for this study: {task_id}")
    tasks = json.loads(tasks_path.read_text(encoding="utf-8"))
    task = next((item for item in tasks if item.get("task_id") == task_id), None)
    if task is None:
        raise ValueError(f"task not found: {task_id}")
    if task.get("world_id") != WORLD_ID:
        raise ValueError("frozen task no longer maps to the frozen world")
    return {
        "task_id": task_id,
        "world_id": WORLD_ID,
        "domain": task.get("domain"),
        "task_name": task.get("task_name"),
        "prompt": task.get("prompt"),
        "expected_output": task.get("expected_output"),
    }


def source_manifest(world_zip: Path) -> dict[str, Any]:
    """Bind the immutable archive and every regular member without extraction."""
    members: list[dict[str, Any]] = []
    with zipfile.ZipFile(world_zip) as archive:
        for info in sorted(archive.infolist(), key=lambda item: item.filename):
            if info.is_dir():
                continue
            members.append({
                "path": info.filename,
                "size": info.file_size,
                "crc32": f"{info.CRC:08x}",
            })
    present = {item["path"] for item in members}
    required = {path for spec in TASK_SPECS.values() for path in spec.evidence_allowlist}
    missing = sorted(required - present)
    if missing:
        raise ValueError(f"frozen world is missing required files: {missing}")
    manifest = {
        "schema_version": f"{SCHEMA}/source-manifest",
        "world_id": WORLD_ID,
        "world_zip_sha256": sha256_file(world_zip),
        "file_count": len(members),
        "files": members,
    }
    manifest["manifest_sha256"] = _sha(_canonical(manifest))
    return manifest


def _safe_member(member: str) -> PurePosixPath:
    path = PurePosixPath(member)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError(f"unsafe archive member: {member}")
    return path


def materialize_evidence_overlay(
    world_zip: Path,
    task_id: str,
    root: Path,
    *,
    public_task: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Extract only the preregistered evidence files for a builder/executor."""
    spec = TASK_SPECS[task_id]
    root.mkdir(parents=True, exist_ok=False)
    records: list[dict[str, Any]] = []
    with zipfile.ZipFile(world_zip) as archive:
        names = set(archive.namelist())
        for member in spec.evidence_allowlist:
            _safe_member(member)
            if member not in names:
                raise ValueError(f"allowlisted member missing: {member}")
            payload = archive.read(member)
            destination = root / member
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(payload)
            records.append({"path": member, "size": len(payload), "sha256": _sha(payload)})
    if public_task is not None:
        public_task_path = root / "filesystem" / "Governed" / "public_task.json"
        write_json(public_task_path, public_task)
        records.append({
            "path": "filesystem/Governed/public_task.json",
            "size": public_task_path.stat().st_size,
            "sha256": sha256_file(public_task_path),
        })
    manifest = {
        "schema_version": f"{SCHEMA}/evidence-overlay",
        "task_id": task_id,
        "world_id": WORLD_ID,
        "files": records,
    }
    manifest["overlay_sha256"] = _sha(_canonical(manifest))
    write_json(root / "package_manifest.json", manifest)
    write_json(root / "filesystem" / "Governed" / "source_manifest.json", manifest)
    write_xlsx_evidence_index(root, records)
    validator = root / "filesystem" / "Governed" / "validate_candidate.py"
    validator.write_text("""#!/usr/bin/env python3
import json
import sys
from pathlib import Path

candidate = Path(sys.argv[1] if len(sys.argv) > 1 else "/filesystem/Governed/working_set.json")
value = json.loads(candidate.read_text())
claims = value.get("claims")
if not isinstance(claims, list) or not claims:
    raise SystemExit("INVALID: claims must be a non-empty list")
claim_ids = [claim.get("claim_id") for claim in claims]
if any(not isinstance(item, str) or not item for item in claim_ids) or len(claim_ids) != len(set(claim_ids)):
    raise SystemExit("INVALID: claim IDs must be unique non-empty strings")
allowed = {"derived_from", "depends_on", "qualifies", "supersedes", "conflicts_with", "deriv"}
for number, relation in enumerate(value.get("relations", []), start=1):
    if relation.get("type") not in allowed:
        raise SystemExit(f"INVALID: relation {number} has unknown type {relation.get('type')!r}")
    if relation.get("from") not in claim_ids or relation.get("to") not in claim_ids:
        raise SystemExit(f"INVALID: relation {number} references missing claim IDs: {relation}")
print("VALID: claim IDs and relation references are internally consistent")
""")
    return manifest


def _xlsx_cell_value(cell: ET.Element, shared_strings: list[str], namespace: str) -> Any:
    cell_type = cell.get("t")
    value = cell.find(f"{{{namespace}}}v")
    inline = cell.find(f"{{{namespace}}}is")
    if inline is not None:
        return "".join(part.text or "" for part in inline.iter(f"{{{namespace}}}t"))
    if value is None or value.text is None:
        return None
    if cell_type == "s":
        return shared_strings[int(value.text)]
    if cell_type in {"str", "e"}:
        return value.text
    if cell_type == "b":
        return value.text == "1"
    try:
        number = float(value.text)
        return int(number) if number.is_integer() else number
    except ValueError:
        return value.text


def extract_xlsx_index(path: Path) -> list[dict[str, Any]]:
    """Return compact, source-addressable non-empty XLSX cells without recalculation."""
    spreadsheet_ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    relationship_ns = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    package_ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        shared: list[str] = []
        if "xl/sharedStrings.xml" in names:
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared = ["".join(node.text or "" for node in item.iter(f"{{{spreadsheet_ns}}}t"))
                      for item in root.findall(f"{{{spreadsheet_ns}}}si")]
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {item.get("Id"): item.get("Target") for item in relationships.findall(f"{{{package_ns}}}Relationship")}
        sheets: list[dict[str, Any]] = []
        for sheet in workbook.findall(f".//{{{spreadsheet_ns}}}sheet"):
            target = targets[sheet.get(f"{{{relationship_ns}}}id")]
            member = target.lstrip("/") if target.startswith("/") else f"xl/{target.lstrip('./')}"
            xml = ET.fromstring(archive.read(member))
            cells: list[dict[str, Any]] = []
            for cell in xml.findall(f".//{{{spreadsheet_ns}}}c"):
                formula = cell.find(f"{{{spreadsheet_ns}}}f")
                value = _xlsx_cell_value(cell, shared, spreadsheet_ns)
                if value is None and (formula is None or not formula.text):
                    continue
                record: dict[str, Any] = {"cell": cell.get("r"), "value": value}
                if formula is not None and formula.text:
                    record["formula"] = formula.text
                cells.append(record)
            sheets.append({"sheet": sheet.get("name"), "cells": cells})
        return sheets


def build_xlsx_evidence_index(root: Path, records: list[dict[str, Any]]) -> dict[str, Any]:
    workbooks = []
    for record in records:
        if not record["path"].lower().endswith(".xlsx"):
            continue
        source_path = root / record["path"]
        if not zipfile.is_zipfile(source_path):
            continue
        workbooks.append({
            "artifact": record["path"], "source_sha256": record["sha256"],
            "sheets": extract_xlsx_index(source_path),
        })
    return {"schema_version": f"{SCHEMA}/xlsx-evidence-index", "workbooks": workbooks}


def write_xlsx_evidence_index(root: Path, records: list[dict[str, Any]]) -> dict[str, Any]:
    """Write a small catalog plus independently readable per-sheet indexes."""
    full = build_xlsx_evidence_index(root, records)
    governed = root / "filesystem" / "Governed"
    index_root = governed / "evidence_index"
    catalog: dict[str, Any] = {"schema_version": full["schema_version"], "sheets": []}
    for workbook_number, workbook in enumerate(full["workbooks"], start=1):
        for sheet_number, sheet in enumerate(workbook["sheets"], start=1):
            filename = f"workbook-{workbook_number:02d}-sheet-{sheet_number:02d}.json"
            relative = f"filesystem/Governed/evidence_index/{filename}"
            payload = {
                "schema_version": full["schema_version"],
                "artifact": workbook["artifact"],
                "source_sha256": workbook["source_sha256"],
                "sheet": sheet["sheet"],
                "cells": sheet["cells"],
            }
            write_json(index_root / filename, payload)
            catalog["sheets"].append({
                "artifact": workbook["artifact"], "source_sha256": workbook["source_sha256"],
                "sheet": sheet["sheet"], "cell_count": len(sheet["cells"]), "index_path": relative,
            })
    if catalog["sheets"]:
        write_json(governed / "evidence_index.json", catalog)
    return catalog


def builder_instruction(task: dict[str, Any]) -> str:
    """Prompt a builder to extract governance state, never solve the task."""
    return f"""You are the treatment-construction stage for a research-only APEX Investment Banking study.
Read only the bounded files mounted in this workspace and the public task below. Do not complete the requested
client task, do not edit the client workbook, and do not calculate or state the requested final answers.

Start with `Governed/evidence_index.json`, a small catalog whose `index_path` entries point to independently
readable per-sheet extractions of every non-empty workbook cell and formula. Read only the sheet indexes needed
for the public task. Do not scan or re-read whole workbooks when an indexed cell/formula is available; open an
original workbook only to resolve a named residual gap. The index is a navigation aid, while each claim must
still bind to the original workbook artifact, cell locator, and source digest recorded in the sheet index.

Create `Governed/working_set.json` containing: `schema_version` = `proofpress/apex-ib-working-set/v1`,
`task_id`, `requirements`, `claims`, `relations`, `coverage`, and `residual_gaps`. Each atomic claim must have
`claim_id`, `statement`, `value` (or null), `unit` (or null), `source` with relative `artifact`, `locator`,
and `source_sha256`, plus `state` = `proposed`. For every source, copy the exact `path` and `sha256` from
`Governed/source_manifest.json`; public-task assumptions must bind to `filesystem/Governed/public_task.json`.
Each relation must use exactly `from`, `to`, and `type`, where `from` and `to` are claim IDs. Relations may
use only `derived_from`, `depends_on`, `qualifies`, `supersedes`, or `conflicts_with`. Sensitivity scenarios
that intentionally replace base assumptions are not unresolved conflicts; represent them with `supersedes`
or `qualifies`. Interpretive ambiguity, an underspecified calculation method, or a choice the executor must
make is also not a source conflict: record it in `residual_gaps` and, when useful, use `qualifies`; never use
`conflicts_with` for it. Use `conflicts_with` only when two source-bound claims assert materially incompatible
facts about the same subject; such a relation will deliberately fail the execution gate. Bind task assumptions,
definitions, model inputs, formulas,
and dependencies needed by a fresh executor, but omit every requested final output value. This package is
staged research context, not an admission. You may bind an output formula as a dependency, but its `value`
must be null or the formula text only: never copy a cached, template, placeholder, standalone, or newly
calculated numeric value for any metric the public task asks the executor to return. Before finishing, run
`python /filesystem/Governed/validate_candidate.py /filesystem/Governed/working_set.json`. If it reports
`INVALID`, repair the candidate and rerun it; finish only after it prints `VALID`.

Public task:
{task['prompt']}"""


def validate_working_set(value: dict[str, Any], task_id: str, overlay_root: Path) -> dict[str, Any]:
    """Validate shape, source binding, graph references, and research-only state."""
    if value.get("schema_version") != "proofpress/apex-ib-working-set/v1":
        raise ValueError("unexpected working-set schema")
    if value.get("task_id") != task_id:
        raise ValueError("working-set task mismatch")
    claims = value.get("claims")
    if not isinstance(claims, list) or not claims:
        raise ValueError("working set has no claims")
    claim_ids: set[str] = set()
    prohibited_output_phrases = {
        FORMAL_TASK_IDS[0]: (
            "pro forma nav per share",
            "nii per share accretion",
            "net investment income per share accretion",
        ),
        FORMAL_TASK_IDS[1]: (
            "incremental change in value",
            "pro forma implied ev after dilution",
            "pro forma implied enterprise value after dilution",
            "total value creation vs standalone",
            "total value creation versus standalone",
        ),
    }.get(task_id, ())

    def contains_concrete_number(item: Any) -> bool:
        if isinstance(item, bool) or item is None:
            return False
        if isinstance(item, (int, float)):
            return True
        if isinstance(item, str):
            candidate = item.strip().replace(",", "").rstrip("%")
            try:
                float(candidate)
            except ValueError:
                return False
            return True
        if isinstance(item, dict):
            return any(contains_concrete_number(child) for child in item.values())
        if isinstance(item, list):
            return any(contains_concrete_number(child) for child in item)
        return False

    for claim in claims:
        if not isinstance(claim, dict) or claim.get("state") != "proposed":
            raise ValueError("every claim must remain proposed")
        claim_id = claim.get("claim_id")
        if not isinstance(claim_id, str) or not claim_id or claim_id in claim_ids:
            raise ValueError("claim IDs must be unique non-empty strings")
        claim_ids.add(claim_id)
        statement = str(claim.get("statement", "")).casefold()
        if any(phrase in statement for phrase in prohibited_output_phrases) and contains_concrete_number(
            claim.get("value")
        ):
            raise ValueError("working set leaks a requested final output value")
        source = claim.get("source")
        if not isinstance(source, dict):
            raise ValueError("claim source is required")
        artifact = source.get("artifact")
        locator = source.get("locator")
        if not isinstance(artifact, str) or not isinstance(locator, str) or not locator:
            raise ValueError("claim source requires artifact and locator")
        _safe_member(artifact)
        source_path = overlay_root / artifact
        if not source_path.is_file() or source.get("source_sha256") != sha256_file(source_path):
            raise ValueError("claim source digest does not bind to the overlay")
    allowed_relations = {"derived_from", "depends_on", "qualifies", "supersedes", "conflicts_with"}
    # Ling Fin occasionally shortens the unambiguous `derived_from` label to
    # `deriv` even when the prompt supplies the closed vocabulary. Normalize
    # that single spelling before hashing/admission; every other unknown label
    # remains a hard schema error.
    relation_aliases = {"deriv": "derived_from"}
    normalized_relations: list[dict[str, Any]] = []
    for relation in value.get("relations", []):
        normalized = dict(relation)
        normalized["type"] = relation_aliases.get(normalized.get("type"), normalized.get("type"))
        if normalized.get("type") not in allowed_relations:
            raise ValueError("unknown relation type")
        if normalized.get("from") not in claim_ids or normalized.get("to") not in claim_ids:
            raise ValueError("relation references unknown claim")
        normalized_relations.append(normalized)
    if value.get("admission") is not None:
        raise ValueError("builder cannot admit claims")
    frozen = dict(value)
    frozen["relations"] = normalized_relations
    frozen["working_set_sha256"] = _sha(_canonical(frozen))
    return frozen


def deterministic_gate(working_set: dict[str, Any], overlay_root: Path) -> dict[str, Any]:
    """Fail closed on digest drift or unresolved material conflict."""
    errors: list[dict[str, str]] = []
    for claim in working_set.get("claims", []):
        source = claim["source"]
        path = overlay_root / source["artifact"]
        actual = sha256_file(path) if path.is_file() else None
        if actual != source["source_sha256"]:
            errors.append({"kind": "source_digest_mismatch", "claim_id": claim["claim_id"]})
    for relation in working_set.get("relations", []):
        if relation.get("type") == "conflicts_with" and relation.get("material", True):
            errors.append({"kind": "material_unresolved_conflict", "claim_id": relation["from"]})
    return {
        "schema_version": f"{SCHEMA}/execution-gate",
        "decision": "block" if errors else "allow",
        "executor_invocation_allowed": not errors,
        "errors": errors,
    }


def materialize_proofpress_executor_overlay(
    evidence_overlay: Path, working_set: dict[str, Any], root: Path
) -> dict[str, Any]:
    """Copy bounded evidence and add verified graph/receipt sidecars."""
    if root.exists():
        raise FileExistsError(root)
    shutil.copytree(evidence_overlay, root)
    governed = root / "filesystem" / "Governed"
    governed.mkdir(parents=True, exist_ok=True)
    write_json(governed / "working_set.json", working_set)
    gate = deterministic_gate(working_set, root)
    write_json(governed / "execution_receipt.json", gate)
    manifest = {
        "schema_version": f"{SCHEMA}/executor-overlay",
        "task_id": working_set["task_id"],
        "working_set_sha256": working_set["working_set_sha256"],
        "gate_decision": gate["decision"],
        "production_reliance": "prohibited",
    }
    write_json(root / "package_manifest.json", manifest)
    return manifest


def filter_snapshot(source_zip: Path, destination_zip: Path, members: Iterable[str]) -> dict[str, Any]:
    """Create an arm-neutral grader package containing only declared client artifacts."""
    allowed = tuple(sorted(set(members)))
    with zipfile.ZipFile(source_zip) as source, zipfile.ZipFile(destination_zip, "w", zipfile.ZIP_DEFLATED) as target:
        source_names = set(source.namelist())
        for member in allowed:
            _safe_member(member)
            if member in source_names:
                target.writestr(member, source.read(member))
    return {"members": list(allowed), "sha256": sha256_file(destination_zip)}


def randomized_formal_schedule(seed: int = DEFAULT_SEED) -> list[dict[str, Any]]:
    randomizer = random.Random(seed)
    schedule: list[dict[str, Any]] = []
    for task_id in FORMAL_TASK_IDS:
        for attempt in range(1, EXECUTOR_ATTEMPTS + 1):
            arms = ["normal", "proofpress"]
            randomizer.shuffle(arms)
            schedule.append({"task_id": task_id, "attempt": attempt, "arm_order": arms})
    return schedule


def frozen_protocol(tasks_path: Path, world_zip: Path, seed: int = DEFAULT_SEED) -> dict[str, Any]:
    tasks = [load_public_task(tasks_path, task_id) for task_id in ALL_TASK_IDS]
    protocol = {
        "schema_version": f"{SCHEMA}/frozen-protocol",
        "world_id": WORLD_ID,
        "source_manifest": source_manifest(world_zip),
        "tasks": tasks,
        "executor_model": EXECUTOR_MODEL,
        "treatment_proposer_model": TREATMENT_PROPOSER_MODEL,
        "judge_model": JUDGE_MODEL,
        "runtime": {
            "agent_max_steps": AGENT_MAX_STEPS,
            "agent_timeout_seconds": AGENT_TIMEOUT_SECONDS,
            "watchdog_seconds": WATCHDOG_SECONDS,
            "model_response_timeout_seconds": MODEL_RESPONSE_TIMEOUT_SECONDS,
            "serial_executor_cells": True,
        },
        "executor_attempts_per_arm": EXECUTOR_ATTEMPTS,
        "grader_repetitions_per_artifact": GRADER_REPETITIONS,
        "formal_artifact_denominator": len(FORMAL_TASK_IDS) * 2 * EXECUTOR_ATTEMPTS,
        "seed": seed,
        "schedule": randomized_formal_schedule(seed),
        "official_score_claim": False,
    }
    protocol["protocol_sha256"] = _sha(_canonical(protocol))
    return protocol


def derived_agent_llm_source(source: str) -> str:
    """Preserve Gateway provider constraints through LiteLLM proxy transport."""
    old = '{"chat_template_kwargs", "include_server_side_tool_invocations"}'
    new = '{"chat_template_kwargs", "include_server_side_tool_invocations", "providerOptions"}'
    if source.count(old) != 1:
        raise ValueError("agent LLM extra-body passthrough anchor changed")
    return source.replace(old, new, 1)


def configure_runtime(
    checkout: Path,
    *,
    agent_model: str = EXECUTOR_MODEL,
    agent_provider: str | None = None,
) -> dict[str, str]:
    """Pin executor, judge, resource bounds, and cached Docker image."""
    example = checkout / "examples" / "hugging_face_task"
    orchestrator_path = example / "orchestrator_config.json"
    grading_path = example / "grading_settings.json"
    agent_path = example / "agent_config.json"
    compose_path = checkout / "environment" / "docker-compose.yml"
    agent_llm_path = checkout / "agents" / "runner" / "utils" / "llm.py"
    grading_llm_path = checkout / "grading" / "runner" / "utils" / "llm.py"
    orchestrator = json.loads(orchestrator_path.read_text())
    grading = json.loads(grading_path.read_text())
    agent = json.loads(agent_path.read_text())
    executor_extra_args: dict[str, Any] = {"custom_llm_provider": "openai"}
    if agent_provider is not None:
        executor_extra_args["providerOptions"] = {"gateway": {"only": [agent_provider]}}
    orchestrator.update({"model": agent_model, "extra_args": executor_extra_args})
    grading.update({"llm_judge_model": JUDGE_MODEL, "llm_judge_extra_args": {"custom_llm_provider": "openai"}})
    agent.setdefault("agent_config_values", {}).update({
        "llm_response_timeout": MODEL_RESPONSE_TIMEOUT_SECONDS,
        "timeout": AGENT_TIMEOUT_SECONDS,
        "max_steps": AGENT_MAX_STEPS,
    })
    write_json(orchestrator_path, orchestrator)
    write_json(grading_path, grading)
    write_json(agent_path, agent)
    compose = compose_path.read_text()
    anchor = "services:\n  environment:\n"
    image_line = f"    image: {ENVIRONMENT_IMAGE}\n"
    if image_line not in compose:
        if anchor not in compose:
            raise ValueError("pinned Docker compose anchor changed")
        compose = compose.replace(anchor, anchor + image_line, 1)
        compose_path.write_text(compose)
    grading_source = grading_llm_path.read_text()
    if "APEX_IB_GRADER_RECEIPTS" not in grading_source:
        grading_llm_path.write_text(derived_grading_llm_source(grading_source))
    agent_llm_source = agent_llm_path.read_text()
    if '"providerOptions"' not in agent_llm_source:
        agent_llm_path.write_text(derived_agent_llm_source(agent_llm_source))
    return {
        path.relative_to(checkout).as_posix(): sha256_file(path)
        for path in (
            orchestrator_path, grading_path, agent_path, compose_path,
            agent_llm_path, grading_llm_path,
        )
    }


def derived_launcher_source(source: str) -> str:
    """Add bounded-overlay, skip-grading, and neutral-grading hooks."""
    world_anchor = '''    # Populate world data, then overlay per-task files (order matters)
    log("Populating environment with world snapshot...")
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(world_zip, "r") as zf:
            zf.extractall(tmp)
        populate_subsystems(Path(tmp), output_dir, "world")

'''
    task_anchor = '''    if task.get("task_input_files"):
        task_prefix = f"task_files/{task['task_id']}"
        log(f"Downloading task input files: {task['task_id']}")
        snapshot_dir = snapshot_download(
            HF_DATASET, repo_type="dataset", allow_patterns=[f"{task_prefix}/**"]
        )
        task_dir = Path(snapshot_dir) / task_prefix
        if task_dir.exists():
            populate_subsystems(task_dir, output_dir, "task")
        else:
            log(f"  No task files found at {task_prefix}")

'''
    mcp_anchor = "    # Configure MCP servers using the all-servers config\n"
    prompt_anchor = '''    initial_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": task["prompt"]},
    ]
'''
    grading_anchor = "    # Run grading if agent completed\n"
    initial_arg = '            str(world_zip),\n'
    final_arg = '            str(final_zip),\n'
    anchors = (world_anchor, task_anchor, mcp_anchor, prompt_anchor, grading_anchor, initial_arg, final_arg)
    if any(source.count(anchor) != 1 for anchor in anchors):
        raise ValueError("pinned APEX launcher changed; PR36 hooks cannot be applied")
    world = '''    bounded_world = os.environ.get("APEX_IB_BOUNDED_WORLD") == "1"
    if bounded_world:
        log("PR36 bounded world: skipping full world population")
    else:
''' + "\n".join("    " + line if line else "" for line in world_anchor.rstrip().splitlines()) + "\n\n"
    task = '''    if not bounded_world:
''' + "\n".join("    " + line if line else "" for line in task_anchor.rstrip().splitlines()) + "\n\n"
    overlay = '''    overlay_dir = os.environ.get("APEX_IB_OVERLAY_DIR")
    if overlay_dir:
        overlay_root = Path(overlay_dir)
        if not overlay_root.is_dir():
            raise RuntimeError(f"PR36 overlay does not exist: {overlay_root}")
        log("Populating PR36 bounded overlay...")
        populate_subsystems(overlay_root, output_dir, "pr36_overlay")

'''
    prompt = '''    extra_instruction = ""
    instruction_path = os.environ.get("APEX_IB_INSTRUCTION_FILE")
    if instruction_path:
        extra_instruction = Path(instruction_path).read_text(encoding="utf-8").strip()
    user_prompt = task["prompt"] + ("\\n\\n" + extra_instruction if extra_instruction else "")
    initial_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
'''
    grading = '''    grading_initial_zip = world_zip
    grading_final_zip = final_zip
    neutral_members_path = os.environ.get("APEX_IB_NEUTRAL_GRADING_MEMBERS")
    if neutral_members_path:
        neutral_members = json.loads(Path(neutral_members_path).read_text(encoding="utf-8"))
        grading_initial_zip = output_dir / "neutral_initial.zip"
        grading_final_zip = output_dir / "neutral_final.zip"
        for source_path, target_path in ((world_zip, grading_initial_zip), (final_zip, grading_final_zip)):
            with zipfile.ZipFile(source_path, "r") as source_zip, zipfile.ZipFile(target_path, "w", zipfile.ZIP_DEFLATED) as target_zip:
                names = set(source_zip.namelist())
                for member in neutral_members:
                    if member in names:
                        target_zip.writestr(member, source_zip.read(member))
        log("PR36 grading: using arm-neutral declared artifact package")

'''
    rendered = source.replace(world_anchor, world).replace(task_anchor, task)
    rendered = rendered.replace(mcp_anchor, overlay + mcp_anchor).replace(prompt_anchor, prompt)
    rendered = rendered.replace(grading_anchor, grading + grading_anchor)
    rendered = rendered.replace("    if agent_status != \"completed\":\n", "    if agent_status != \"completed\" or os.environ.get(\"APEX_IB_SKIP_GRADING\") == \"1\":\n", 1)
    rendered = rendered.replace(initial_arg, '            str(grading_initial_zip),\n', 1)
    rendered = rendered.replace(final_arg, '            str(grading_final_zip),\n', 1)
    return rendered


def materialize_launcher(checkout: Path) -> Path:
    original = checkout / "examples" / "hugging_face_task" / "main.py"
    derived = original.with_name("main_proofpress_ib_pr36.py")
    source = derived_launcher_source(original.read_text())
    build = '["docker", "compose", "up", "-d", "--build"]'
    if source.count(build) != 1:
        raise ValueError("pinned Docker launch anchor changed")
    derived.write_text(source.replace(build, '["docker", "compose", "up", "-d", "--no-build"]'))
    return derived


def _runtime_environment(env_file: Path | None) -> dict[str, str]:
    env = _environment(env_file)
    key = env.get("AI_GATEWAY_API_KEY")
    if not key:
        raise RuntimeError("AI_GATEWAY_API_KEY is required")
    docker_bin = "/Applications/Docker.app/Contents/Resources/bin"
    env.update({
        "LITELLM_PROXY_API_BASE": AI_GATEWAY_BASE,
        "LITELLM_PROXY_API_KEY": key,
        "PATH": docker_bin + os.pathsep + env.get("PATH", os.environ.get("PATH", "")),
    })
    return env


def _stop(process: subprocess.Popen[str]) -> int:
    os.killpg(process.pid, signal.SIGTERM)
    try:
        return process.wait(timeout=30)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        return process.wait(timeout=30)


def run_apex_stage(
    checkout: Path,
    results_root: Path,
    task_id: str,
    stage: str,
    *,
    overlay: Path | None = None,
    instruction: str = "",
    bounded_world: bool = False,
    skip_grading: bool = False,
    env_file: Path | None = None,
    watchdog_seconds: int = WATCHDOG_SECONDS,
    agent_model: str = EXECUTOR_MODEL,
    agent_provider: str | None = None,
) -> dict[str, Any]:
    """Run one immutable builder or executor stage through Archipelago."""
    if task_id not in TASK_SPECS or watchdog_seconds < AGENT_TIMEOUT_SECONDS:
        raise ValueError("unfrozen task or insufficient watchdog")
    runtime_hashes = configure_runtime(
        checkout, agent_model=agent_model, agent_provider=agent_provider)
    launcher = materialize_launcher(checkout)
    runtime_hashes[launcher.relative_to(checkout).as_posix()] = sha256_file(launcher)
    env = _runtime_environment(env_file)
    run_id = f"{stage}-{task_id}-{uuid.uuid4().hex[:8]}"
    run_dir = results_root / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    instruction_path = run_dir / "instruction.txt"
    instruction_path.write_text(instruction + "\n")
    neutral_path = run_dir / "neutral_grading_members.json"
    write_json(neutral_path, list(TASK_SPECS[task_id].final_artifact_allowlist))
    example = checkout / "examples" / "hugging_face_task"
    output_dir = example / "output" / task_id
    if output_dir.exists():
        shutil.move(output_dir, run_dir / "preexisting_output")
    subprocess.run(["docker", "compose", "down", "-v"], cwd=checkout / "environment", env=env, capture_output=True)
    process_env = env | {
        "EXAMPLE_DIR": str(example), "ARCHIPELAGO_DIR": str(checkout),
        "ENVIRONMENT_DIR": str(checkout / "environment"), "AGENTS_DIR": str(checkout / "agents"),
        "GRADING_DIR": str(checkout / "grading"), "ENV_URL": "http://localhost:8080",
        "APEX_IB_INSTRUCTION_FILE": str(instruction_path),
        "APEX_IB_NEUTRAL_GRADING_MEMBERS": str(neutral_path),
        "APEX_IB_GRADER_RECEIPTS": str(run_dir / "grader_receipts.jsonl"),
    }
    if overlay is not None:
        process_env["APEX_IB_OVERLAY_DIR"] = str(overlay)
    if bounded_world:
        process_env["APEX_IB_BOUNDED_WORLD"] = "1"
    if skip_grading:
        process_env["APEX_IB_SKIP_GRADING"] = "1"
    started = time.monotonic()
    log_path = run_dir / "launcher.log"
    timed_out = False
    with log_path.open("w") as log:
        process = subprocess.Popen(
            ["uv", "run", "python", str(launcher), task_id], cwd=checkout / "agents",
            env=process_env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True,
        )
        try:
            returncode = process.wait(timeout=watchdog_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            returncode = _stop(process)
    captured = run_dir / "output"
    if output_dir.exists():
        shutil.move(output_dir, captured)
    trajectory_path = captured / "trajectory.json"
    grades_path = captured / "grades.json"
    trajectory = json.loads(trajectory_path.read_text()) if trajectory_path.exists() else {}
    grades = json.loads(grades_path.read_text()) if grades_path.exists() else {}
    telemetry = trajectory_telemetry(trajectory, agent_model)
    grading_telemetry = grader_telemetry(run_dir / "grader_receipts.jsonl", JUDGE_MODEL) if not skip_grading else None
    completed = not timed_out and returncode == 0 and trajectory.get("status") == "completed"
    completed = completed and telemetry["status"] == "complete"
    if not skip_grading:
        completed = completed and grades.get("grading_run_status") == "completed"
        completed = completed and grading_telemetry is not None and grading_telemetry["status"] == "complete"
    record = {
        "schema_version": f"{SCHEMA}/stage-run", "run_id": run_id, "stage": stage,
        "task_id": task_id, "world_id": WORLD_ID, "agent_model": agent_model,
        "executor_model": agent_model,
        "executor_provider_requested": agent_provider,
        "judge_model": JUDGE_MODEL, "official_score_claim": False,
        "bounded_world": bounded_world, "skip_grading": skip_grading,
        "elapsed_seconds": round(time.monotonic() - started, 3), "watchdog_timeout": timed_out,
        "launcher_returncode": returncode, "trajectory_status": trajectory.get("status"),
        "grading_status": grades.get("grading_run_status"),
        "native_score": grades.get("scoring_results", {}).get("final_score"),
        "status": "completed" if completed else "infrastructure_abort_or_incomplete",
        "archipelago_commit": _git_commit(checkout), "docker_image_id": _image_id(env),
        "runtime_hashes": runtime_hashes,
        "telemetry": telemetry,
        "grading_telemetry": grading_telemetry,
    }
    write_json(run_dir / "manifest.json", record)
    subprocess.run(["docker", "compose", "down", "-v"], cwd=checkout / "environment", env=env, capture_output=True)
    return record | {"run_dir": str(run_dir)}


def _snapshot_json(snapshot: Path, member: str) -> dict[str, Any]:
    with tarfile.open(snapshot, "r:gz") as archive:
        handle = archive.extractfile(member)
        if handle is None:
            raise ValueError(f"missing snapshot member: {member}")
        value = json.loads(handle.read().decode())
    if not isinstance(value, dict):
        raise ValueError(f"snapshot member is not an object: {member}")
    return value


def build_treatment(
    checkout: Path,
    results_root: Path,
    tasks_path: Path,
    world_zip: Path,
    task_id: str,
    *,
    env_file: Path | None = None,
) -> dict[str, Any]:
    """Build and deterministically validate one pre-executor working set."""
    task = load_public_task(tasks_path, task_id)
    treatment_root = results_root / f"treatment-{task_id}-{uuid.uuid4().hex[:8]}"
    treatment_root.mkdir(parents=True, exist_ok=False)
    evidence = treatment_root / "bounded_evidence"
    evidence_manifest = materialize_evidence_overlay(
        world_zip, task_id, evidence, public_task=task,
    )
    builder = run_apex_stage(
        checkout, treatment_root, task_id, "builder", overlay=evidence,
        instruction=builder_instruction(task), bounded_world=True, skip_grading=True, env_file=env_file,
        agent_model=TREATMENT_PROPOSER_MODEL,
    )
    record: dict[str, Any] = {
        "schema_version": f"{SCHEMA}/treatment-build", "task_id": task_id,
        "evidence_manifest": evidence_manifest, "builder": builder,
        "treatment_proposer_model": TREATMENT_PROPOSER_MODEL,
        "status": "builder_incomplete", "executor_invocation_allowed": False,
    }
    if builder["status"] == "completed":
        snapshot = Path(builder["run_dir"]) / "output" / "final_snapshot.tar.gz"
        try:
            proposed = _snapshot_json(snapshot, "filesystem/Governed/working_set.json")
            validated = validate_working_set(proposed, task_id, evidence)
            write_json(treatment_root / "validated_working_set.json", validated)
            executor_overlay = treatment_root / "executor_overlay"
            package = materialize_proofpress_executor_overlay(evidence, validated, executor_overlay)
            gate = deterministic_gate(validated, executor_overlay)
            record.update({
                "status": "ready" if gate["decision"] == "allow" else "blocked",
                "working_set_sha256": validated["working_set_sha256"],
                "executor_overlay": str(executor_overlay), "executor_package": package,
                "gate": gate, "executor_invocation_allowed": gate["executor_invocation_allowed"],
            })
        except (OSError, ValueError, json.JSONDecodeError, tarfile.TarError) as exc:
            record.update({"status": "working_set_invalid", "error": f"{type(exc).__name__}: {exc}"})
    write_json(treatment_root / "manifest.json", record)
    return record | {"treatment_root": str(treatment_root)}


PROOFPRESS_EXECUTOR_INSTRUCTION = """Complete the public task using only the mounted bounded evidence and
`Governed/working_set.json`. The claims are staged research context, not guaranteed truth. Verify source-bound
inputs against the mounted files, respect qualifications and conflicts, edit the requested client workbook,
and return the requested answer. Do not copy Proofpress sidecars into the client deliverable."""


def run_calibration_pair(
    checkout: Path,
    results_root: Path,
    tasks_path: Path,
    world_zip: Path,
    *,
    env_file: Path | None = None,
    seed: int = DEFAULT_SEED,
) -> dict[str, Any]:
    """Run one fresh, randomized Normal/Proofpress calibration pair."""
    results_root.mkdir(parents=True, exist_ok=False)
    protocol = frozen_protocol(tasks_path, world_zip, seed)
    write_json(results_root / "frozen_protocol.json", protocol)
    treatment = build_treatment(
        checkout, results_root, tasks_path, world_zip, QUALIFICATION_TASK_ID, env_file=env_file,
    )
    if treatment.get("builder", {}).get("status") == "completed":
        builder_output = Path(treatment["builder"]["run_dir"]) / "output"
        treatment["builder_compaction"] = compact_apex_output(builder_output, preserve_final_tar=False)
    report: dict[str, Any] = {
        "schema_version": f"{SCHEMA}/calibration", "formal_denominator": False,
        "protocol_sha256": protocol["protocol_sha256"], "treatment": treatment,
        "cells": [], "status": "treatment_not_ready",
    }
    if not treatment.get("executor_invocation_allowed"):
        write_json(results_root / "report.json", report)
        return report
    order = ["normal", "proofpress"]
    random.Random(seed).shuffle(order)
    for arm in order:
        if arm == "normal":
            cell = run_apex_stage(
                checkout, results_root, QUALIFICATION_TASK_ID, "calibration-cell",
                bounded_world=False, env_file=env_file,
            )
        else:
            cell = run_apex_stage(
                checkout, results_root, QUALIFICATION_TASK_ID, "calibration-cell",
                overlay=Path(treatment["executor_overlay"]), instruction=PROOFPRESS_EXECUTOR_INSTRUCTION,
                bounded_world=True, env_file=env_file,
            )
        cell_record: dict[str, Any] = {"arm": arm, "result": cell}
        if cell["status"] == "completed":
            cell_record["compaction"] = compact_apex_output(
                Path(cell["run_dir"]) / "output", preserve_final_tar=False,
            )
        report["cells"].append(cell_record)
    report["arm_order"] = order
    report["status"] = "completed" if all(item["result"]["status"] == "completed" for item in report["cells"]) else "incomplete"
    write_json(results_root / "report.json", report)
    return report


def host_preflight(checkout: Path, world_zip: Path, *, formal: bool = False) -> dict[str, Any]:
    """Check non-secret host requirements without starting a model call."""
    free = shutil.disk_usage(checkout).free
    required = MIN_FORMAL_FREE_BYTES if formal else MIN_CALIBRATION_FREE_BYTES
    docker_binary = shutil.which("docker")
    app_binary = Path("/Applications/Docker.app/Contents/Resources/bin/docker")
    if docker_binary is None and app_binary.is_file():
        docker_binary = str(app_binary)
    if docker_binary:
        docker = subprocess.run([docker_binary, "info"], capture_output=True, text=True, check=False)
        image = subprocess.run(
            [docker_binary, "image", "inspect", ENVIRONMENT_IMAGE, "--format", "{{.Id}}"],
            capture_output=True, text=True, check=False,
        )
    else:
        docker = subprocess.CompletedProcess([], 127, "", "docker CLI not found")
        image = subprocess.CompletedProcess([], 127, "", "docker CLI not found")
    return {
        "schema_version": f"{SCHEMA}/host-preflight", "mode": "formal" if formal else "calibration",
        "status": "passed" if free >= required and docker.returncode == 0 and image.returncode == 0 and world_zip.is_file() else "failed",
        "free_bytes": free, "required_free_bytes": required,
        "docker_healthy": docker.returncode == 0, "environment_image_present": image.returncode == 0,
        "docker_binary": docker_binary,
        "world_zip_present": world_zip.is_file(), "world_zip_sha256": sha256_file(world_zip) if world_zip.is_file() else None,
    }


def compact_apex_output(output_dir: Path, *, preserve_final_tar: bool = True) -> dict[str, Any]:
    """Remove reproducible launcher intermediates after recording their digests.

    Trajectory, grades, verifier definitions, neutral grader packages, and the
    final tar snapshot are retained. World copies and tar/zip conversion
    intermediates are recoverable from the frozen source manifest.
    """
    candidates = [
        path for path in output_dir.iterdir() if path.is_file() and (
            path.name.startswith("world_")
            or path.name == f"{WORLD_ID}.zip"
            or path.name == "final_snapshot.zip"
            or path.name.startswith("pr36_overlay_")
        )
    ] if output_dir.is_dir() else []
    if not preserve_final_tar and (output_dir / "final_snapshot.tar.gz").is_file():
        candidates.append(output_dir / "final_snapshot.tar.gz")
    records = [
        {"name": path.name, "size": path.stat().st_size, "sha256": sha256_file(path)}
        for path in sorted(set(candidates))
    ]
    manifest = {
        "schema_version": f"{SCHEMA}/output-compaction",
        "deleted_reconstructible_files": records,
        "bytes_reclaimed": sum(item["size"] for item in records),
        "retained_final_snapshot_tar": (output_dir / "final_snapshot.tar.gz").is_file() and preserve_final_tar,
    }
    write_json(output_dir / "compaction_manifest.json", manifest)
    for path in candidates:
        path.unlink()
    return manifest


def repeat_native_grading(
    checkout: Path,
    run_dir: Path,
    *,
    env_file: Path | None = None,
    repetitions: int = GRADER_REPETITIONS,
    agent_model: str = EXECUTOR_MODEL,
    agent_provider: str | None = None,
) -> dict[str, Any]:
    """Complete independent native judge repetitions on neutral packages."""
    if repetitions < 1:
        raise ValueError("grading repetitions must be positive")
    output = run_dir / "output"
    required = ("neutral_initial.zip", "neutral_final.zip", "trajectory.json", "verifiers.json", "grades.json")
    missing = [name for name in required if not (output / name).is_file()]
    if missing:
        raise ValueError(f"native grading inputs missing: {missing}")
    env = _runtime_environment(env_file)
    configure_runtime(
        checkout, agent_model=agent_model, agent_provider=agent_provider)
    grading_dir = run_dir / "grading_repetitions"
    grading_dir.mkdir(exist_ok=False)
    shutil.copy2(output / "grades.json", grading_dir / "repetition-01.json")
    first_telemetry = grader_telemetry(run_dir / "grader_receipts.jsonl", JUDGE_MODEL)
    records = [{"repetition": 1, "status": "completed" if first_telemetry["status"] == "complete" else "failed",
                "path": "repetition-01.json", "telemetry": first_telemetry}]
    for repetition in range(2, repetitions + 1):
        destination = grading_dir / f"repetition-{repetition:02d}.json"
        receipt_path = grading_dir / f"repetition-{repetition:02d}-receipts.jsonl"
        command = [
            "uv", "run", "python", "-m", "runner.main",
            "--grading-run-id", f"gr_{uuid.uuid4().hex[:8]}",
            "--trajectory-id", f"{run_dir.name}-grade-{repetition}",
            "--initial-snapshot", str(output / "neutral_initial.zip"),
            "--final-snapshot", str(output / "neutral_final.zip"),
            "--trajectory", str(output / "trajectory.json"),
            "--grading-settings", str(checkout / "examples" / "hugging_face_task" / "grading_settings.json"),
            "--verifiers", str(output / "verifiers.json"),
            "--eval-configs", str(checkout / "examples" / "hugging_face_task" / "eval_configs.json"),
            "--scoring-config", str(checkout / "examples" / "hugging_face_task" / "scoring_config.json"),
            "--output", str(destination),
        ]
        result = subprocess.run(command, cwd=checkout / "grading", env=env | {
            "APEX_IB_GRADER_RECEIPTS": str(receipt_path),
        }, capture_output=True, text=True, check=False)
        completed = result.returncode == 0 and destination.is_file()
        if completed:
            value = json.loads(destination.read_text())
            completed = value.get("grading_run_status") == "completed"
        telemetry = grader_telemetry(receipt_path, JUDGE_MODEL)
        completed = completed and telemetry["status"] == "complete"
        records.append({
            "repetition": repetition, "status": "completed" if completed else "failed",
            "path": destination.name, "returncode": result.returncode,
            "stderr_tail": result.stderr[-1000:] if not completed else "",
            "telemetry": telemetry,
        })
        if not completed:
            break
    report = {
        "schema_version": f"{SCHEMA}/grading-repetitions", "judge_model": JUDGE_MODEL,
        "required": repetitions, "records": records,
        "status": "completed" if len(records) == repetitions and all(item["status"] == "completed" for item in records) else "incomplete",
    }
    write_json(grading_dir / "manifest.json", report)
    return report


def majority_native_result(run_dir: Path) -> dict[str, Any]:
    grading_dir = run_dir / "grading_repetitions"
    files = sorted(grading_dir.glob("repetition-*.json"))
    if len(files) != GRADER_REPETITIONS:
        raise ValueError("complete grading repetitions are required")
    judgments: dict[str, list[float]] = {}
    for path in files:
        value = json.loads(path.read_text())
        if value.get("grading_run_status") != "completed":
            raise ValueError("incomplete grading repetition")
        for item in value.get("verifier_results", []):
            judgments.setdefault(item["verifier_id"], []).append(float(item.get("score", 0)))
    criteria = {
        verifier: {"scores": scores, "majority_pass": sum(score >= 0.5 for score in scores) >= 2}
        for verifier, scores in judgments.items()
    }
    passed = sum(item["majority_pass"] for item in criteria.values())
    return {
        "schema_version": f"{SCHEMA}/artifact-majority-result",
        "passed": passed, "total": len(criteria),
        "fraction": passed / len(criteria) if criteria else None,
        "exact_success": bool(criteria) and passed == len(criteria), "criteria": criteria,
    }


def run_formal_matrix(
    checkout: Path,
    results_root: Path,
    tasks_path: Path,
    world_zip: Path,
    *,
    env_file: Path | None = None,
    seed: int = DEFAULT_SEED,
) -> dict[str, Any]:
    """Execute the frozen 2-task × 2-arm × 3-attempt matrix serially."""
    results_root.mkdir(parents=True, exist_ok=False)
    protocol = frozen_protocol(tasks_path, world_zip, seed)
    write_json(results_root / "frozen_protocol.json", protocol)
    treatments: dict[str, dict[str, Any]] = {}
    for task_id in FORMAL_TASK_IDS:
        treatment = build_treatment(checkout, results_root, tasks_path, world_zip, task_id, env_file=env_file)
        treatments[task_id] = treatment
        if not treatment.get("executor_invocation_allowed"):
            report = {
                "schema_version": f"{SCHEMA}/formal-report", "status": "treatment_not_ready",
                "formal_artifact_denominator": 12, "treatments": treatments, "cells": [],
            }
            write_json(results_root / "report.json", report)
            return report
        builder_output = Path(treatment["builder"]["run_dir"]) / "output"
        compact_apex_output(builder_output, preserve_final_tar=False)
    cells: list[dict[str, Any]] = []
    for block in protocol["schedule"]:
        task_id = block["task_id"]
        for arm in block["arm_order"]:
            treatment = treatments[task_id]
            result = run_apex_stage(
                checkout, results_root, task_id, f"formal-a{block['attempt']}-{arm}",
                overlay=Path(treatment["executor_overlay"]) if arm == "proofpress" else None,
                instruction=PROOFPRESS_EXECUTOR_INSTRUCTION if arm == "proofpress" else "",
                bounded_world=arm == "proofpress", env_file=env_file,
            )
            cell: dict[str, Any] = {"task_id": task_id, "attempt": block["attempt"], "arm": arm, "result": result}
            if result["status"] == "completed":
                grading = repeat_native_grading(checkout, Path(result["run_dir"]), env_file=env_file)
                cell["grading_repetitions"] = grading
                if grading["status"] == "completed":
                    cell["majority_result"] = majority_native_result(Path(result["run_dir"]))
            # Every cell is compacted, including bounded failures.  Preserve the
            # failed cell's partial final tar for audit while removing its copied
            # world and reconstructible zip/tar intermediates.  Without this,
            # repeated 60-step outcomes can exhaust the host before later cells.
            cell["compaction"] = compact_apex_output(
                Path(result["run_dir"]) / "output",
                preserve_final_tar=result["status"] != "completed",
            )
            cells.append(cell)
            write_json(results_root / "cells.json", cells)
    valid = [cell for cell in cells if cell.get("majority_result")]
    stress = run_stress_cells(treatments, results_root / "stress")
    report = {
        "schema_version": f"{SCHEMA}/formal-report", "formal_artifact_denominator": 12,
        "valid_artifacts": len(valid), "treatments": treatments, "cells": cells, "stress": stress,
        "status": "completed" if len(valid) == 12 and stress["status"] == "passed" else "incomplete",
    }
    write_json(results_root / "report.json", report)
    return report


def run_stress_cells(treatments: dict[str, dict[str, Any]], root: Path) -> dict[str, Any]:
    """Execute the two frozen no-model fail-closed stress cells."""
    root.mkdir(parents=True, exist_ok=False)
    receipts: list[dict[str, Any]] = []

    digest_task = FORMAL_TASK_IDS[0]
    digest_treatment = treatments[digest_task]
    digest_overlay = root / "digest-drift-overlay"
    shutil.copytree(Path(digest_treatment["executor_overlay"]), digest_overlay)
    digest_working = json.loads((Path(digest_treatment["treatment_root"]) / "validated_working_set.json").read_text())
    source_path = digest_overlay / digest_working["claims"][0]["source"]["artifact"]
    with source_path.open("ab") as handle:
        handle.write(b"\nPROOFPRESS_FROZEN_STRESS_DRIFT\n")
    digest_gate = deterministic_gate(digest_working, digest_overlay)
    digest_receipt = {
        "stress": "material_source_digest_drift", "task_id": digest_task,
        "gate": digest_gate, "executor_invoked": False, "client_artifact_produced": False,
    }
    write_json(root / "digest_drift_receipt.json", digest_receipt)
    receipts.append(digest_receipt)

    conflict_task = FORMAL_TASK_IDS[1]
    conflict_treatment = treatments[conflict_task]
    conflict_overlay = Path(conflict_treatment["executor_overlay"])
    conflict_working = json.loads((Path(conflict_treatment["treatment_root"]) / "validated_working_set.json").read_text())
    original = conflict_working["claims"][0]
    conflicting = json.loads(json.dumps(original))
    conflicting["claim_id"] = f"{original['claim_id']}-stress-conflict"
    conflicting["statement"] = original["statement"] + " [frozen contradictory stress state]"
    conflict_working["claims"].append(conflicting)
    conflict_working.setdefault("relations", []).append({
        "from": original["claim_id"], "to": conflicting["claim_id"],
        "type": "conflicts_with", "material": True, "resolved": False,
    })
    conflict_gate = deterministic_gate(conflict_working, conflict_overlay)
    conflict_receipt = {
        "stress": "material_unresolved_claim_conflict", "task_id": conflict_task,
        "gate": conflict_gate, "executor_invoked": False, "client_artifact_produced": False,
    }
    write_json(root / "claim_conflict_receipt.json", conflict_receipt)
    receipts.append(conflict_receipt)
    passed = all(
        item["gate"]["decision"] == "block"
        and not item["gate"]["executor_invocation_allowed"]
        and not item["executor_invoked"] and not item["client_artifact_produced"]
        for item in receipts
    )
    report = {"schema_version": f"{SCHEMA}/stress-report", "status": "passed" if passed else "failed", "receipts": receipts}
    write_json(root / "report.json", report)
    return report

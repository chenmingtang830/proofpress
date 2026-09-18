"""Project bounded Baseten training exports into external experiment evidence."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from proofpress.integrations.external_experiment import normalize_manifest


SCHEMA = "proofpress.baseten_training.v0"
PRODUCTS = frozenset({"training_jobs", "loops"})
RECORD_TYPES = frozenset({
    "job", "metrics", "logs", "checkpoint", "evaluation",
    "trajectory_summary", "other",
})


def _object(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"Baseten training {field} must be an object")
    return value


def _allowed(raw: dict[str, Any], allowed: set[str], field: str) -> None:
    unknown = sorted(set(raw) - allowed)
    if unknown:
        raise ValueError(
            f"unknown Baseten training {field} fields: " + ", ".join(unknown))


def _string(value: Any, field: str, maximum: int = 2000) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Baseten training {field} must be a non-empty string")
    value = value.strip()
    if len(value) > maximum:
        raise ValueError(
            f"Baseten training {field} must be at most {maximum} characters")
    return value


def _canonical(value: Any, field: str) -> bytes:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Baseten training {field} must contain JSON values") from exc


def _sha256(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def _pointer(payload: Any, pointer: str, field: str) -> Any:
    if pointer == "":
        return payload
    if not pointer.startswith("/"):
        raise ValueError(f"Baseten training {field} must be an RFC 6901 JSON pointer")
    current = payload
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and token in current:
            current = current[token]
        elif isinstance(current, list) and token.isdigit() and int(token) < len(current):
            current = current[int(token)]
        else:
            raise ValueError(
                f"Baseten training {field} does not resolve in its record payload")
    return current


def _validate_identity(product: str, source: dict[str, Any],
                       records: list[dict[str, Any]]) -> None:
    run_id = source["run_id"]
    if product == "training_jobs":
        project_id = source["training_project_id"]
        matched = False
        for record in records:
            job = record["payload"].get("training_job")
            if not isinstance(job, dict):
                continue
            if job.get("id") != run_id:
                raise ValueError("Baseten training job id does not match source.run_id")
            observed_project = job.get("training_project_id")
            if observed_project is None and isinstance(job.get("training_project"), dict):
                observed_project = job["training_project"].get("id")
            if observed_project != project_id:
                raise ValueError(
                    "Baseten training project id does not match source.training_project_id")
            matched = True
        if not matched:
            raise ValueError(
                "Baseten training_jobs export requires a record containing training_job identity")
        return

    session_id = source["session_id"]
    matched = False
    for record in records:
        run = record["payload"].get("run")
        if not isinstance(run, dict):
            continue
        if run.get("id") != run_id or run.get("session_id") != session_id:
            raise ValueError("Baseten Loops run or session id does not match source")
        matched = True
    if not matched:
        raise ValueError(
            "Baseten Loops export requires a record containing run identity")


def to_external_experiment(payload: Any) -> dict[str, Any]:
    """Return a generic Proofpress manifest without retaining raw Baseten payloads."""
    raw = _object(payload, "bundle")
    if raw.get("schema_version") != SCHEMA:
        raise ValueError(f"Baseten training schema_version must be {SCHEMA}")
    _allowed(raw, {"schema_version", "source", "binding", "records"}, "bundle")
    if len(_canonical(raw, "bundle")) > 4 * 1024 * 1024:
        raise ValueError("Baseten training bundle must be at most 4194304 encoded bytes")

    source_raw = _object(raw.get("source"), "source")
    _allowed(source_raw, {
        "product", "run_id", "uri", "training_project_id", "session_id",
        "captured_at", "capture_mode", "provenance_status", "coverage",
        "known_omissions",
    }, "source")
    product = _string(source_raw.get("product"), "source.product", 64)
    if product not in PRODUCTS:
        raise ValueError(
            "Baseten training source.product must be one of: "
            + ", ".join(sorted(PRODUCTS)))
    source = {
        "product": product,
        "run_id": _string(source_raw.get("run_id"), "source.run_id", 512),
        "uri": _string(source_raw.get("uri"), "source.uri"),
        "capture_mode": _string(source_raw.get("capture_mode"),
                                "source.capture_mode", 128),
        "provenance_status": _string(source_raw.get("provenance_status"),
                                     "source.provenance_status", 128),
        "coverage": _string(source_raw.get("coverage"), "source.coverage", 64),
        "known_omissions": source_raw.get("known_omissions"),
    }
    if not isinstance(source["known_omissions"], list):
        raise ValueError("Baseten training source.known_omissions must be an array")
    if "captured_at" in source_raw:
        source["captured_at"] = _string(
            source_raw["captured_at"], "source.captured_at", 128)
    if product == "training_jobs":
        source["training_project_id"] = _string(
            source_raw.get("training_project_id"), "source.training_project_id", 512)
        if "session_id" in source_raw:
            raise ValueError("Baseten training_jobs source must not include session_id")
    else:
        source["session_id"] = _string(
            source_raw.get("session_id"), "source.session_id", 512)
        if "training_project_id" in source_raw:
            source["training_project_id"] = _string(
                source_raw["training_project_id"], "source.training_project_id", 512)

    binding_raw = _object(raw.get("binding"), "binding")
    _allowed(binding_raw, {"proofpress_run_id", "work_item_id", "code_revision",
                           "dataset_refs"}, "binding")
    dataset_refs = binding_raw.get("dataset_refs", [])
    if not isinstance(dataset_refs, list):
        raise ValueError("Baseten training binding.dataset_refs must be an array")
    binding = {
        "proofpress_run_id": _string(
            binding_raw.get("proofpress_run_id"), "binding.proofpress_run_id", 256),
        "dataset_refs": [
            _string(item, "binding.dataset_refs", 512) for item in dataset_refs
        ],
    }
    for field in ("work_item_id", "code_revision"):
        if field in binding_raw:
            binding[field] = _string(
                binding_raw[field], f"binding.{field}", 512)

    records_raw = raw.get("records")
    if not isinstance(records_raw, list) or not records_raw:
        raise ValueError("Baseten training records must be a non-empty array")
    records: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    selection_plan = []
    for index, item in enumerate(records_raw):
        item = _object(item, f"records[{index}]")
        _allowed(item, {"name", "record_type", "source_uri", "payload",
                        "selections"}, f"records[{index}]")
        name = _string(item.get("name"), f"records[{index}].name", 256)
        record_type = _string(
            item.get("record_type"), f"records[{index}].record_type", 64)
        if record_type not in RECORD_TYPES:
            raise ValueError(
                f"Baseten training records[{index}].record_type is unsupported")
        record_payload = _object(item.get("payload"), f"records[{index}].payload")
        source_uri = _string(
            item.get("source_uri"), f"records[{index}].source_uri")
        selections = item.get("selections")
        if not isinstance(selections, list) or not selections:
            raise ValueError(
                f"Baseten training records[{index}].selections must be a non-empty array")
        source_digest = _sha256(_canonical(
            record_payload, f"records[{index}].payload"))
        records.append({"payload": record_payload})
        for selection_index, selection in enumerate(selections):
            selection = _object(
                selection, f"records[{index}].selections[{selection_index}]")
            _allowed(selection, {"pointer", "observation", "artifact_type",
                                 "media_type", "selection_reason"},
                     f"records[{index}].selections[{selection_index}]")
            pointer = _string(
                selection.get("pointer"),
                f"records[{index}].selections[{selection_index}].pointer")
            _pointer(record_payload, pointer,
                     f"records[{index}].selections[{selection_index}].pointer")
            row = {
                "source_uri": source_uri,
                "source_digest": source_digest,
                "locator": {"kind": "json_pointer", "value": pointer},
                "observation": _string(
                    selection.get("observation"),
                    f"records[{index}].selections[{selection_index}].observation",
                    16000),
                "artifact_type": _string(
                    selection.get("artifact_type"),
                    f"records[{index}].selections[{selection_index}].artifact_type",
                    64),
            }
            for field, maximum in (("media_type", 512),
                                   ("selection_reason", 2000)):
                if field in selection:
                    row[field] = _string(
                        selection[field],
                        f"records[{index}].selections[{selection_index}].{field}",
                        maximum)
            evidence.append(row)
            selection_plan.append({
                "record": name, "record_type": record_type,
                "pointer": pointer, "artifact_type": row["artifact_type"],
            })

    _validate_identity(product, source, records)
    generic_source = {
        "system": f"baseten.{product}",
        "run_id": source["run_id"],
        "uri": source["uri"],
        "capture_mode": source["capture_mode"],
        "provenance_status": source["provenance_status"],
        "coverage": source["coverage"],
        "known_omissions": source["known_omissions"],
    }
    if "captured_at" in source:
        generic_source["captured_at"] = source["captured_at"]
    generic_binding = {
        **binding,
        "config_digest": _sha256(_canonical({
            "adapter": "baseten_training", "version": "0",
            "product": product, "selection_plan": selection_plan,
        }, "selection plan")),
    }
    return normalize_manifest({
        "schema_version": "proofpress.external_experiment.v0",
        "source": generic_source,
        "binding": generic_binding,
        "evidence": evidence,
        "adapter": {"name": "baseten_training", "version": "0"},
    })

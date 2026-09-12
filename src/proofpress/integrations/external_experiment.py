"""Strict, vendor-neutral external experiment manifest normalization.

The manifest is an ingestion contract, not an execution or trace contract.  It
binds selected observations to external source versions while making capture
method and known coverage limits explicit.  Provider credentials, raw source
bytes, and arbitrary trace payloads are deliberately outside the schema.
"""
from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import parse_qsl, urlsplit


SCHEMA = "proofpress.external_experiment.v0"
CAPTURE_MODES = frozenset({
    "instrumented_sdk", "provider_api", "webhook", "exported_bundle",
    "manual_submission",
})
PROVENANCE_STATUSES = frozenset({
    "directly_observed", "provider_attested", "importer_attested",
    "user_asserted",
})
COVERAGE_LEVELS = frozenset({"full", "partial", "unknown"})
ARTIFACT_TYPES = frozenset({
    "metric", "checkpoint", "evaluation", "trajectory_slice", "artifact",
    "other",
})
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_SECRET_KEY = re.compile(
    r"(?:^|[_-])(api[_-]?key|access[_-]?token|refresh[_-]?token|token|secret|"
    r"password|credential|authorization)(?:$|[_-])", re.IGNORECASE)
_JSON_POINTER = re.compile(r"^(?:/(?:[^~]|~[01])*)*$")


def _object(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"external experiment {field} must be an object")
    return value


def _allowed(raw: dict[str, Any], allowed: set[str], field: str) -> None:
    unknown = sorted(set(raw) - allowed)
    if unknown:
        raise ValueError(
            f"unknown external experiment {field} fields: " + ", ".join(unknown))


def _string(value: Any, field: str, maximum: int = 2000) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"external experiment {field} must be a non-empty string")
    value = value.strip()
    if len(value) > maximum:
        raise ValueError(
            f"external experiment {field} must be at most {maximum} characters")
    return value


def _digest(value: Any, field: str) -> str:
    value = _string(value, field, 71)
    if not _DIGEST.fullmatch(value):
        raise ValueError(f"external experiment {field} must be a sha256 digest")
    return value


def _enum(value: Any, allowed: frozenset[str], field: str) -> str:
    value = _string(value, field, 128)
    if value not in allowed:
        raise ValueError(
            f"external experiment {field} must be one of: "
            + ", ".join(sorted(allowed)))
    return value


def _strings(value: Any, field: str, *, required: bool = False) -> list[str]:
    if not isinstance(value, list) or (required and not value):
        suffix = "non-empty " if required else ""
        raise ValueError(f"external experiment {field} must be a {suffix}array")
    result = [_string(item, field, 512) for item in value]
    if len(result) != len(set(result)):
        raise ValueError(f"external experiment {field} must not contain duplicates")
    return result


def _uri(value: Any, field: str) -> str:
    value = _string(value, field)
    parsed = urlsplit(value)
    if not parsed.scheme:
        raise ValueError(f"external experiment {field} must be an absolute URI")
    if parsed.username or parsed.password:
        raise ValueError(f"external experiment {field} must not contain credentials")
    for key, _ in parse_qsl(parsed.query, keep_blank_values=True):
        if _SECRET_KEY.search(key):
            raise ValueError(f"external experiment {field} must not contain credential query parameters")
    return value


def _locator(value: Any) -> dict[str, Any]:
    raw = _object(value, "evidence.locator")
    kind = _string(raw.get("kind"), "evidence.locator.kind", 64)
    if kind == "json_pointer":
        _allowed(raw, {"kind", "value"}, "evidence.locator")
        pointer = _string(raw.get("value"), "evidence.locator.value")
        if not _JSON_POINTER.fullmatch(pointer):
            raise ValueError(
                "external experiment evidence.locator.value must be an RFC 6901 JSON pointer")
        return {"kind": kind, "value": pointer}
    # Other locator kinds are normalized by the existing retrieval-evidence
    # contract. Preserve only JSON values here; the kernel remains authoritative.
    try:
        return json.loads(json.dumps(raw, ensure_ascii=False))
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "external experiment evidence.locator must contain JSON values") from exc


def normalize_manifest(payload: Any) -> dict[str, Any]:
    """Validate and return the canonical v0 external experiment manifest."""
    raw = _object(payload, "manifest")
    if raw.get("schema_version") != SCHEMA:
        raise ValueError(
            f"external experiment schema_version must be {SCHEMA}")
    _allowed(raw, {"schema_version", "source", "binding", "evidence", "adapter"},
             "manifest")
    try:
        encoded_size = len(json.dumps(raw, ensure_ascii=False,
                                      separators=(",", ":")).encode("utf-8"))
    except (TypeError, ValueError) as exc:
        raise ValueError("external experiment manifest must contain JSON values") from exc
    if encoded_size > 512 * 1024:
        raise ValueError("external experiment manifest must be at most 524288 encoded bytes")

    source_raw = _object(raw.get("source"), "source")
    _allowed(source_raw, {"system", "run_id", "uri", "capture_mode",
                          "provenance_status", "coverage", "known_omissions",
                          "captured_at"}, "source")
    coverage = _enum(source_raw.get("coverage"), COVERAGE_LEVELS,
                     "source.coverage")
    omissions = _strings(source_raw.get("known_omissions"),
                         "source.known_omissions")
    if coverage == "full" and omissions:
        raise ValueError(
            "external experiment full coverage must not declare known omissions")
    if coverage == "partial" and not omissions:
        raise ValueError(
            "external experiment partial coverage requires known omissions")
    source = {
        "system": _string(source_raw.get("system"), "source.system", 256),
        "run_id": _string(source_raw.get("run_id"), "source.run_id", 512),
        "uri": _uri(source_raw.get("uri"), "source.uri"),
        "capture_mode": _enum(source_raw.get("capture_mode"), CAPTURE_MODES,
                              "source.capture_mode"),
        "provenance_status": _enum(source_raw.get("provenance_status"),
                                   PROVENANCE_STATUSES,
                                   "source.provenance_status"),
        "coverage": coverage,
        "known_omissions": omissions,
    }
    if "captured_at" in source_raw:
        source["captured_at"] = _string(source_raw["captured_at"],
                                        "source.captured_at", 128)

    binding_raw = _object(raw.get("binding"), "binding")
    _allowed(binding_raw, {"proofpress_run_id", "work_item_id", "code_revision",
                           "dataset_refs", "config_digest"}, "binding")
    binding = {
        "proofpress_run_id": _string(binding_raw.get("proofpress_run_id"),
                                     "binding.proofpress_run_id", 256),
        "dataset_refs": _strings(binding_raw.get("dataset_refs", []),
                                 "binding.dataset_refs"),
        "config_digest": _digest(binding_raw.get("config_digest"),
                                 "binding.config_digest"),
    }
    for field in ("work_item_id", "code_revision"):
        if field in binding_raw:
            binding[field] = _string(binding_raw[field], f"binding.{field}", 512)

    adapter_raw = _object(raw.get("adapter"), "adapter")
    _allowed(adapter_raw, {"name", "version"}, "adapter")
    adapter = {
        "name": _string(adapter_raw.get("name"), "adapter.name", 256),
        "version": _string(adapter_raw.get("version"), "adapter.version", 128),
    }

    evidence_raw = raw.get("evidence")
    if not isinstance(evidence_raw, list) or not evidence_raw:
        raise ValueError("external experiment evidence must be a non-empty array")
    evidence = []
    for index, item in enumerate(evidence_raw):
        item = _object(item, f"evidence[{index}]")
        _allowed(item, {"source_uri", "source_digest", "locator", "observation",
                        "artifact_type", "media_type", "selection_reason"},
                 f"evidence[{index}]")
        row = {
            "source_uri": _uri(item.get("source_uri"),
                               f"evidence[{index}].source_uri"),
            "source_digest": _digest(item.get("source_digest"),
                                     f"evidence[{index}].source_digest"),
            "locator": _locator(item.get("locator")),
            "observation": _string(item.get("observation"),
                                   f"evidence[{index}].observation", 16000),
            "artifact_type": _enum(item.get("artifact_type"), ARTIFACT_TYPES,
                                   f"evidence[{index}].artifact_type"),
        }
        for field in ("media_type", "selection_reason"):
            if field in item:
                row[field] = _string(item[field], f"evidence[{index}].{field}",
                                     512 if field == "media_type" else 2000)
        evidence.append(row)

    return {"schema_version": SCHEMA, "source": source, "binding": binding,
            "evidence": evidence, "adapter": adapter}

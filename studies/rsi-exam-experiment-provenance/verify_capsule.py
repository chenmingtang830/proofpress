#!/usr/bin/env python3
"""Offline integrity checks for the RSI-Exam experiment provenance profile."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "proofpress/rsi-exam-trajectory/v1"
DIGEST = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_KEYS = {
    "prompt",
    "prompts",
    "reasoning",
    "reasoning_summary",
    "transcript",
    "tool_input",
    "tool_inputs",
    "tool_output",
    "tool_outputs",
    "raw_input",
    "raw_output",
    "hidden_target",
    "hidden_targets",
}


def _add(errors: list[str], code: str) -> None:
    if code not in errors:
        errors.append(code)


def _digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _inside(root: Path, locator: str) -> Path | None:
    candidate = Path(locator)
    if candidate.is_absolute():
        return None
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        return None
    return resolved


def _walk_forbidden(value: Any, errors: list[str], path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_KEYS:
                _add(errors, f"forbidden_payload:{path}.{key}")
            _walk_forbidden(child, errors, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_forbidden(child, errors, f"{path}[{index}]")


def _require_mapping(parent: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        _add(errors, f"missing_or_invalid:{key}")
        return {}
    return value


def _require_digest(parent: dict[str, Any], key: str, errors: list[str]) -> str:
    value = parent.get(key)
    if not isinstance(value, str) or not DIGEST.fullmatch(value):
        _add(errors, f"invalid_digest:{key}")
        return ""
    return value


def _check_file(
    root: Path,
    locator: Any,
    expected: Any,
    errors: list[str],
    code_prefix: str,
) -> None:
    if not isinstance(locator, str) or not locator:
        _add(errors, f"{code_prefix}:invalid_locator")
        return
    path = _inside(root, locator)
    if path is None:
        _add(errors, f"{code_prefix}:locator_outside_root")
        return
    if not path.is_file():
        _add(errors, f"{code_prefix}:missing_file")
        return
    if not isinstance(expected, str) or not DIGEST.fullmatch(expected):
        _add(errors, f"{code_prefix}:invalid_digest")
        return
    if _digest(path) != expected:
        _add(errors, f"{code_prefix}:digest_mismatch")


def _check_receipt_bindings(
    root: Path,
    locator: Any,
    version_id: str,
    artifact_sha256: str,
    expected_score: Any,
    split: str,
    errors: list[str],
    code_prefix: str,
    evaluator_digest: str | None = None,
    verifier_digest: str | None = None,
    calibration_digest: str | None = None,
) -> None:
    if not isinstance(locator, str) or not locator:
        return
    path = _inside(root, locator)
    if path is None or not path.is_file():
        return
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        _add(errors, f"{code_prefix}:unreadable")
        return
    if not isinstance(receipt, dict):
        _add(errors, f"{code_prefix}:not_object")
        return
    if receipt.get("version_id") != version_id:
        _add(errors, f"{code_prefix}:version_mismatch")
    if receipt.get("artifact_sha256") != artifact_sha256:
        _add(errors, f"{code_prefix}:artifact_mismatch")
    if receipt.get("split") != split:
        _add(errors, f"{code_prefix}:split_mismatch")
    if receipt.get("score") != expected_score:
        _add(errors, f"{code_prefix}:score_mismatch")
    if evaluator_digest is not None and receipt.get("evaluator_digest") != evaluator_digest:
        _add(errors, f"{code_prefix}:evaluator_mismatch")
    if verifier_digest is not None and receipt.get("verifier_digest") != verifier_digest:
        _add(errors, f"{code_prefix}:verifier_mismatch")
    if calibration_digest is not None and receipt.get("calibration_digest") != calibration_digest:
        _add(errors, f"{code_prefix}:calibration_mismatch")


def verify_capsule(capsule_path: str | Path, artifact_root: str | Path | None = None) -> dict[str, Any]:
    capsule = Path(capsule_path).resolve()
    root = Path(artifact_root).resolve() if artifact_root else capsule.parent
    errors: list[str] = []
    checks: dict[str, bool] = {}

    try:
        with capsule.open(encoding="utf-8") as stream:
            data = json.load(stream)
    except (OSError, json.JSONDecodeError):
        return {
            "ok": False,
            "integrity": "fail",
            "coverage": "unverifiable",
            "errors": ["capsule_unreadable"],
            "checks": {"json": False},
        }

    if not isinstance(data, dict):
        return {
            "ok": False,
            "integrity": "fail",
            "coverage": "unverifiable",
            "errors": ["capsule_not_object"],
            "checks": {"json": True},
        }

    _walk_forbidden(data, errors)
    checks["json"] = True
    checks["schema_version"] = data.get("schema_version") == SCHEMA_VERSION
    if not checks["schema_version"]:
        _add(errors, "unsupported_schema_version")

    benchmark = _require_mapping(data, "benchmark", errors)
    rollout = _require_mapping(data, "rollout", errors)
    freeze = _require_mapping(data, "freeze", errors)
    source = _require_mapping(data, "source", errors)
    final = _require_mapping(data, "final_submission", errors)
    hidden = _require_mapping(data, "hidden_evaluation", errors)
    versions = data.get("versions")
    if not isinstance(versions, list) or not versions:
        _add(errors, "missing_or_invalid:versions")
        versions = []

    checks["benchmark"] = (
        benchmark.get("name") == "RSI-Exam"
        and all(isinstance(benchmark.get(key), str) and benchmark.get(key) for key in ("release", "task_id"))
    )
    if not checks["benchmark"]:
        _add(errors, "invalid_benchmark")

    checks["rollout"] = all(
        isinstance(rollout.get(key), str) and rollout.get(key)
        for key in ("id", "trace_session_id", "model", "harness")
    ) and isinstance(rollout.get("budget_hours"), (int, float)) and rollout.get("budget_hours", 0) > 0
    if not checks["rollout"]:
        _add(errors, "invalid_rollout")

    freeze_digests = {
        key: _require_digest(freeze, key, errors)
        for key in ("protocol_digest", "verifier_digest", "calibration_digest", "evaluator_digest")
    }
    checks["freeze"] = all(freeze_digests.values())

    trace_digest = _require_digest(source, "trace_digest", errors)
    checks["source"] = bool(trace_digest)
    source_manifest = source.get("manifest")
    manifest_ids: set[str] | None = None
    if source_manifest is not None:
        if not isinstance(source_manifest, dict):
            _add(errors, "invalid_manifest")
        else:
            manifest_path = _inside(root, source_manifest.get("locator", ""))
            expected_manifest_digest = source_manifest.get("sha256")
            if manifest_path is None:
                _add(errors, "manifest:locator_outside_root")
            elif not manifest_path.is_file():
                _add(errors, "manifest:missing_file")
            elif not isinstance(expected_manifest_digest, str) or not DIGEST.fullmatch(expected_manifest_digest):
                _add(errors, "manifest:invalid_digest")
            elif _digest(manifest_path) != expected_manifest_digest:
                _add(errors, "manifest:digest_mismatch")
            else:
                try:
                    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                    if manifest.get("session_id") != rollout.get("trace_session_id"):
                        _add(errors, "manifest:session_mismatch")
                    if manifest.get("rollout_id") != rollout.get("id"):
                        _add(errors, "manifest:rollout_mismatch")
                    if manifest.get("config_digest") != rollout.get("config_digest"):
                        _add(errors, "manifest:config_mismatch")
                    raw_ids = manifest.get("event_ids")
                    if not isinstance(raw_ids, list) or not raw_ids or not all(
                        isinstance(item, str) and item for item in raw_ids
                    ):
                        _add(errors, "manifest:invalid_event_ids")
                    else:
                        manifest_ids = set(raw_ids)
                except (OSError, json.JSONDecodeError):
                    _add(errors, "manifest:unreadable")

    version_by_id: dict[str, dict[str, Any]] = {}
    observed_event_ids: set[str] = set()
    ordinals: set[int] = set()
    for version in versions:
        if not isinstance(version, dict):
            _add(errors, "version:not_object")
            continue
        version_id = version.get("version_id")
        if not isinstance(version_id, str) or not version_id:
            _add(errors, "version:invalid_id")
            continue
        if version_id in version_by_id:
            _add(errors, "version:duplicate_id")
        version_by_id[version_id] = version
        ordinal = version.get("ordinal")
        if not isinstance(ordinal, int) or ordinal < 0:
            _add(errors, f"version:{version_id}:invalid_ordinal")
        elif ordinal in ordinals:
            _add(errors, "version:duplicate_ordinal")
        else:
            ordinals.add(ordinal)
        parents = version.get("parent_ids")
        if not isinstance(parents, list) or len(set(parents)) != len(parents):
            _add(errors, f"version:{version_id}:invalid_parents")
        elif any(not isinstance(parent, str) or not parent for parent in parents):
            _add(errors, f"version:{version_id}:invalid_parent_id")
        event_ids = version.get("trace_event_ids")
        if not isinstance(event_ids, list) or not event_ids or len(set(event_ids)) != len(event_ids):
            _add(errors, f"version:{version_id}:invalid_event_ids")
        else:
            observed_event_ids.update(event_ids)
        _check_file(
            root,
            version.get("artifact_locator"),
            version.get("artifact_sha256"),
            errors,
            f"artifact:{version_id}",
        )
        visible = version.get("visible_evaluation")
        if not isinstance(visible, dict):
            _add(errors, f"visible:{version_id}:missing")
        else:
            for key in ("receipt_sha256", "evaluator_digest", "calibration_digest"):
                _require_digest(visible, key, errors)
            _check_file(
                root,
                visible.get("receipt_locator"),
                visible.get("receipt_sha256"),
                errors,
                f"visible:{version_id}:receipt",
            )
            _check_receipt_bindings(
                root,
                visible.get("receipt_locator"),
                version_id,
                version.get("artifact_sha256"),
                visible.get("score"),
                "visible",
                errors,
                f"visible:{version_id}:receipt",
                evaluator_digest=visible.get("evaluator_digest"),
                calibration_digest=visible.get("calibration_digest"),
            )
            if visible.get("calibration_digest") != freeze_digests["calibration_digest"]:
                _add(errors, f"visible:{version_id}:calibration_drift")
            if visible.get("evaluator_digest") != freeze_digests["evaluator_digest"]:
                _add(errors, f"visible:{version_id}:evaluator_drift")
            visible_events = version.get("trace_event_ids", [])
            observed_event_ids.update(visible_events if isinstance(visible_events, list) else [])

    for version_id, version in version_by_id.items():
        parents = version.get("parent_ids", [])
        for parent in parents if isinstance(parents, list) else []:
            if parent not in version_by_id:
                _add(errors, f"version:{version_id}:missing_parent")
            elif isinstance(version.get("ordinal"), int) and isinstance(version_by_id[parent].get("ordinal"), int):
                if version_by_id[parent]["ordinal"] >= version["ordinal"]:
                    _add(errors, f"version:{version_id}:parent_order")

    final_id = final.get("version_id")
    hidden_id = hidden.get("version_id")
    checks["final_binding"] = (
        isinstance(final_id, str)
        and final_id in version_by_id
        and final.get("artifact_sha256") == version_by_id.get(final_id, {}).get("artifact_sha256")
        and hidden_id == final_id
        and hidden.get("artifact_sha256") == final.get("artifact_sha256")
    )
    if not checks["final_binding"]:
        _add(errors, "final_hidden_version_binding")
    final_events = final.get("trace_event_ids", [])
    hidden_events = hidden.get("trace_event_ids", [])
    if isinstance(final_events, list):
        observed_event_ids.update(final_events)
    if isinstance(hidden_events, list):
        observed_event_ids.update(hidden_events)

    _check_file(
        root,
        hidden.get("receipt_locator"),
        hidden.get("receipt_sha256"),
        errors,
        "hidden:receipt",
    )
    _check_receipt_bindings(
        root,
        hidden.get("receipt_locator"),
        hidden_id,
        hidden.get("artifact_sha256"),
        hidden.get("score"),
        "hidden",
        errors,
        "hidden:receipt",
        verifier_digest=hidden.get("verifier_digest"),
        calibration_digest=hidden.get("calibration_digest"),
    )
    for key in ("artifact_sha256", "receipt_sha256", "verifier_digest", "calibration_digest"):
        _require_digest(hidden, key, errors)
    checks["hidden_freeze_binding"] = (
        hidden.get("verifier_digest") == freeze_digests["verifier_digest"]
        and hidden.get("calibration_digest") == freeze_digests["calibration_digest"]
    )
    if not checks["hidden_freeze_binding"]:
        _add(errors, "hidden_evaluation_freeze_drift")

    if manifest_ids is None:
        coverage = "unverifiable"
    elif observed_event_ids == manifest_ids:
        coverage = "complete"
    elif observed_event_ids.issubset(manifest_ids):
        coverage = "partial"
    else:
        coverage = "partial"
        _add(errors, "manifest:unknown_observed_event")

    checks["no_forbidden_payload"] = not any(
        error.startswith("forbidden_payload:") for error in errors
    )
    checks["version_dag"] = not any(
        error.startswith("version:") and (
            "missing_parent" in error
            or "parent_order" in error
            or "duplicate" in error
            or "invalid_parent" in error
        )
        for error in errors
    )
    integrity = "pass" if not errors else "fail"
    return {
        "ok": integrity == "pass",
        "integrity": integrity,
        "coverage": coverage,
        "capsule_id": data.get("capsule_id"),
        "errors": errors,
        "checks": checks,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capsule")
    parser.add_argument("--artifact-root", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = verify_capsule(args.capsule, args.artifact_root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"integrity={result['integrity']} coverage={result['coverage']}")
        for error in result["errors"]:
            print(f"error: {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Deterministic validation for the additive experiment evidence profile."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
import hashlib
import json
import re
from typing import Any


PROFILE = "proofpress/profile/experiment/v1"
EVIDENCE_KINDS = frozenset({"metric_observation", "table_cell", "derivation"})
CONCLUSION_KINDS = frozenset({
    "finding", "regression", "no-change", "failed-attempt", "decision",
})
OPERATIONS = frozenset({"sum", "difference", "product", "ratio"})
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


def digest(value: Any) -> str:
    body = json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(body).hexdigest()


def _string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"experiment profile {field} must be a non-empty string")
    return value.strip()


def _digest(value: Any, field: str) -> str:
    value = _string(value, field)
    if not _DIGEST.fullmatch(value):
        raise ValueError(f"experiment profile {field} must be a sha256 digest")
    return value


def _decimal(value: Any, field: str) -> str:
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValueError(f"experiment profile {field} must be numeric")
    try:
        number = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"experiment profile {field} must be numeric") from exc
    if not number.is_finite():
        raise ValueError(f"experiment profile {field} must be finite")
    return format(number.normalize(), "f")


def normalize_identity(raw: Any) -> dict[str, str]:
    if not isinstance(raw, dict):
        raise ValueError("experiment profile experiment must be an object")
    allowed = {"experiment_id", "run_id", "model_revision", "dataset_revision",
               "environment_digest", "config_digest"}
    unknown = sorted(set(raw) - allowed)
    if unknown:
        raise ValueError("unknown experiment identity fields: " + ", ".join(unknown))
    return {
        "experiment_id": _string(raw.get("experiment_id"), "experiment.experiment_id"),
        "run_id": _string(raw.get("run_id"), "experiment.run_id"),
        "model_revision": _string(raw.get("model_revision"), "experiment.model_revision"),
        "dataset_revision": _string(raw.get("dataset_revision"), "experiment.dataset_revision"),
        "environment_digest": _digest(raw.get("environment_digest"), "experiment.environment_digest"),
        "config_digest": _digest(raw.get("config_digest"), "experiment.config_digest"),
    }


def _refs(raw: Any, field: str) -> list[str]:
    if not isinstance(raw, list) or not raw:
        raise ValueError(f"experiment profile {field} must be a non-empty array")
    refs = [_string(item, field) for item in raw]
    if len(set(refs)) != len(refs):
        raise ValueError(f"experiment profile {field} must not contain duplicates")
    return refs


def _strings(raw: Any, field: str) -> list[str]:
    if not isinstance(raw, list) or not raw:
        raise ValueError(f"experiment profile {field} must be a non-empty array")
    values = [_string(item, field) for item in raw]
    if len(set(values)) != len(values):
        raise ValueError(f"experiment profile {field} must not contain duplicates")
    return values


def _unit(value: Any, field: str = "unit") -> str:
    return _string(value, field)


def recomputation_payload(formula: dict[str, str], inputs: list[dict[str, str]],
                          output: dict[str, str]) -> dict[str, Any]:
    return {"formula": formula, "inputs": inputs, "output": output}


def _computed(operation: str, values: list[Decimal]) -> Decimal:
    if operation == "sum":
        return sum(values, Decimal(0))
    if operation == "difference":
        if len(values) != 2:
            raise ValueError("experiment derivation difference requires exactly two inputs")
        return values[0] - values[1]
    if operation == "product":
        result = Decimal(1)
        for value in values:
            result *= value
        return result
    if len(values) != 2:
        raise ValueError("experiment derivation ratio requires exactly two inputs")
    if values[1] == 0:
        raise ValueError("experiment derivation ratio denominator must not be zero")
    return values[0] / values[1]


def normalize_evidence(payload: Any, evidence_rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(payload, dict) or payload.get("schema_version") != PROFILE:
        raise ValueError(f"experiment evidence schema_version must be {PROFILE}")
    kind = payload.get("kind")
    if kind not in EVIDENCE_KINDS:
        raise ValueError("unknown experiment evidence kind")
    allowed = {"schema_version", "kind", "experiment", "observation", "cell",
               "derivation"}
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise ValueError("unknown experiment evidence fields: " + ", ".join(unknown))
    result: dict[str, Any] = {"schema_version": PROFILE, "kind": kind,
                              "experiment": normalize_identity(payload.get("experiment"))}
    if kind == "metric_observation":
        raw = payload.get("observation")
        if not isinstance(raw, dict):
            raise ValueError("experiment profile observation must be an object")
        allowed_observation = {"name", "version", "value", "unit", "population",
                               "slice", "source_evidence_ref"}
        unknown = sorted(set(raw) - allowed_observation)
        if unknown:
            raise ValueError("unknown experiment observation fields: " + ", ".join(unknown))
        if bool(raw.get("population")) == bool(raw.get("slice")):
            raise ValueError("experiment observation requires exactly one of population or slice")
        source_ref = _string(raw.get("source_evidence_ref"), "observation.source_evidence_ref")
        if source_ref not in evidence_rows:
            raise ValueError("unknown experiment source evidence: " + source_ref)
        normalized = {"name": _string(raw.get("name"), "observation.name"),
                      "version": _string(raw.get("version"), "observation.version"),
                      "value": _decimal(raw.get("value"), "observation.value"),
                      "unit": _unit(raw.get("unit"), "observation.unit"),
                      "source_evidence_ref": source_ref}
        key = "population" if raw.get("population") else "slice"
        normalized[key] = _string(raw.get(key), f"observation.{key}")
        result["observation"] = normalized
        return result
    if kind == "table_cell":
        raw = payload.get("cell")
        if not isinstance(raw, dict):
            raise ValueError("experiment profile cell must be an object")
        allowed_cell = {"table_id", "row", "column", "value", "unit",
                        "source_evidence_ref"}
        unknown = sorted(set(raw) - allowed_cell)
        if unknown:
            raise ValueError("unknown experiment cell fields: " + ", ".join(unknown))
        source_ref = _string(raw.get("source_evidence_ref"), "cell.source_evidence_ref")
        if source_ref not in evidence_rows:
            raise ValueError("unknown experiment source evidence: " + source_ref)
        result["cell"] = {
            "table_id": _string(raw.get("table_id"), "cell.table_id"),
            "row": _string(raw.get("row"), "cell.row"),
            "column": _string(raw.get("column"), "cell.column"),
            "value": _decimal(raw.get("value"), "cell.value"),
            "unit": _unit(raw.get("unit"), "cell.unit"),
            "source_evidence_ref": source_ref,
        }
        return result

    raw = payload.get("derivation")
    if not isinstance(raw, dict):
        raise ValueError("experiment profile derivation must be an object")
    allowed_derivation = {"formula", "input_evidence_refs", "output",
                          "recomputation_digest"}
    unknown = sorted(set(raw) - allowed_derivation)
    if unknown:
        raise ValueError("unknown experiment derivation fields: " + ", ".join(unknown))
    formula_raw = raw.get("formula")
    if not isinstance(formula_raw, dict):
        raise ValueError("experiment derivation formula must be an object")
    if set(formula_raw) != {"name", "version", "operation"}:
        raise ValueError("experiment derivation formula requires name, version, and operation")
    operation = formula_raw.get("operation")
    if operation not in OPERATIONS:
        raise ValueError("unknown experiment derivation operation")
    formula = {"name": _string(formula_raw.get("name"), "derivation.formula.name"),
               "version": _string(formula_raw.get("version"), "derivation.formula.version"),
               "operation": operation}
    refs = _refs(raw.get("input_evidence_refs"), "derivation.input_evidence_refs")
    missing = [ref for ref in refs if ref not in evidence_rows]
    if missing:
        raise ValueError("unknown experiment input evidence: " + ", ".join(missing))
    inputs = []
    for ref in refs:
        row = evidence_rows[ref]
        profile = row.get("experiment_profile", {})
        value_row = profile.get("observation") or profile.get("cell")
        if not value_row:
            raise ValueError("experiment derivation inputs must be metric or table evidence")
        inputs.append({"evidence_ref": ref, "value": value_row["value"],
                       "unit": value_row["unit"]})
    output_raw = raw.get("output")
    if not isinstance(output_raw, dict) or set(output_raw) != {"value", "unit"}:
        raise ValueError("experiment derivation output requires value and unit")
    output = {"value": _decimal(output_raw.get("value"), "derivation.output.value"),
              "unit": _unit(output_raw.get("unit"), "derivation.output.unit")}
    if operation in {"sum", "difference"}:
        units = {item["unit"] for item in inputs}
        if len(units) != 1 or output["unit"] not in units:
            raise ValueError("experiment additive derivation units must match")
    calculated = _computed(operation, [Decimal(item["value"]) for item in inputs])
    if Decimal(output["value"]) != calculated:
        raise ValueError("experiment derivation output does not recompute")
    recomputation = recomputation_payload(formula, inputs, output)
    expected = digest(recomputation)
    if _digest(raw.get("recomputation_digest"), "derivation.recomputation_digest") != expected:
        raise ValueError("experiment derivation recomputation digest mismatch")
    result["derivation"] = {"formula": formula, "input_evidence_refs": refs,
                            "output": output, "recomputation_digest": expected}
    return result


def normalize_conclusion(qualifiers: Any) -> dict[str, Any]:
    qualifiers = qualifiers or {}
    raw = qualifiers.get("experiment")
    if not isinstance(raw, dict):
        raise ValueError("experiment profile requires qualifiers.experiment")
    allowed = {"schema_version", "conclusion_kind", "experiment", "failure"}
    unknown = sorted(set(raw) - allowed)
    if unknown:
        raise ValueError("unknown experiment conclusion fields: " + ", ".join(unknown))
    if raw.get("schema_version") != PROFILE:
        raise ValueError(f"experiment conclusion schema_version must be {PROFILE}")
    kind = raw.get("conclusion_kind")
    if kind not in CONCLUSION_KINDS:
        raise ValueError("unknown experiment conclusion kind")
    normalized = {"schema_version": PROFILE, "conclusion_kind": kind,
                  "experiment": normalize_identity(raw.get("experiment"))}
    failure = raw.get("failure")
    if kind != "failed-attempt" and failure is not None:
        raise ValueError("experiment failure record is only valid for failed-attempt")
    if kind == "failed-attempt":
        if not isinstance(failure, dict):
            raise ValueError("failed-attempt requires an explicit failure record")
        allowed_failure = {"intervention", "expected_outcome", "observed_outcome",
                           "feedback_evidence_refs", "invalidated_hypotheses",
                           "repeat_policy", "changed_dimension_required", "next_action"}
        unknown = sorted(set(failure) - allowed_failure)
        if unknown:
            raise ValueError("unknown experiment failure fields: " + ", ".join(unknown))
        repeat_policy = failure.get("repeat_policy")
        if repeat_policy not in {"do-not-repeat", "retry-if-changed", "informational"}:
            raise ValueError("unknown experiment failure repeat_policy")
        changed = failure.get("changed_dimension_required")
        if repeat_policy == "retry-if-changed":
            changed = _string(changed, "failure.changed_dimension_required")
        elif changed is not None:
            raise ValueError("changed_dimension_required is only valid for retry-if-changed")
        normalized_failure = {
            "intervention": _string(failure.get("intervention"), "failure.intervention"),
            "expected_outcome": _string(failure.get("expected_outcome"), "failure.expected_outcome"),
            "observed_outcome": _string(failure.get("observed_outcome"), "failure.observed_outcome"),
            "feedback_evidence_refs": _refs(failure.get("feedback_evidence_refs"),
                                             "failure.feedback_evidence_refs"),
            "invalidated_hypotheses": _strings(failure.get("invalidated_hypotheses"),
                                                "failure.invalidated_hypotheses"),
            "repeat_policy": repeat_policy,
            "next_action": _string(failure.get("next_action"), "failure.next_action"),
        }
        if changed is not None:
            normalized_failure["changed_dimension_required"] = changed
        normalized["failure"] = normalized_failure
    return {**qualifiers, "experiment": normalized,
            "profile": PROFILE}

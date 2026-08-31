"""Fail-closed contract for the v25 exact-knowledge transfer experiment."""
from __future__ import annotations

import hashlib
import json
from typing import Any


SCHEMA = "proofpress/exact-knowledge-transfer-manifest/v1"
CONDITIONS = (
    "ordinary-claim",
    "claim-plus-table-cells",
    "claim-plus-table-cells-plus-derivation",
)
NONLEGAL_FAMILIES = (
    "financial_table_reconciliation",
    "operational_kpi",
    "contract_payment_schedule",
)


def _content_digest(value: Any) -> bool:
    return (isinstance(value, str) and len(value) == 71 and value.startswith("sha256:")
            and all(char in "0123456789abcdef" for char in value[7:]))


def digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def validate_transfer_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    """Validate experiment separation and return a content-addressed receipt."""
    failures: list[str] = []
    if manifest.get("schema_version") != SCHEMA:
        failures.append("schema_version mismatch")

    development = tuple(manifest.get("development_task_ids") or ())
    held_out = tuple(manifest.get("held_out_task_ids") or ())
    if len(development) != 5 or len(set(development)) != 5:
        failures.append("development panel must contain five unique tasks")
    if len(held_out) != 7 or len(set(held_out)) != 7:
        failures.append("held-out panel must contain seven unique tasks")
    if set(development) & set(held_out):
        failures.append("development and held-out panels overlap")
    if tuple(manifest.get("conditions") or ()) != CONDITIONS:
        failures.append("conditions or condition order changed")

    controls = manifest.get("frozen_controls") or {}
    for field in ("task_source_manifest_digest", "graph_digest", "executor",
                  "grader", "executor_gateway_canary", "grader_gateway_canary", "rubric_digest", "retry_policy",
                  "disclosure_budget", "executor_budget", "native_output_contract",
                  "primary_extraction_qualification"):
        if not _content_digest(controls.get(field)):
            failures.append(f"missing frozen control: {field}")

    extraction = manifest.get("stage_b5_extraction")
    if not isinstance(extraction, dict):
        failures.append("Stage B.5 extraction contract is missing")
    elif not isinstance(extraction.get("primary_route"), str) or not extraction["primary_route"]:
        failures.append("Stage B.5 primary extractor route is missing")

    families = manifest.get("nonlegal_families") or []
    family_names = tuple(row.get("family") for row in families
                         if isinstance(row, dict))
    if family_names != NONLEGAL_FAMILIES:
        failures.append("non-legal families or family order changed")
    for row in families:
        if not isinstance(row, dict):
            failures.append("non-legal family entry is not an object")
            continue
        if int(row.get("minimum_tasks", 0)) < 3:
            failures.append(f"non-legal family too small: {row.get('family')}")
        required = set(row.get("required_variants") or ())
        if not {"period_rows", "period_columns", "missing_or_conflicting_input"} <= required:
            failures.append(f"non-legal variants incomplete: {row.get('family')}")

    if manifest.get("outcome_access_before_freeze") is not False:
        failures.append("held-out outcomes must remain inaccessible before freeze")
    if manifest.get("human_approval_policy") != "required_for_admission_and_reuse":
        failures.append("Human Approval boundary changed")

    if failures:
        raise ValueError("; ".join(failures))
    return {
        "schema_version": "proofpress/exact-knowledge-transfer-freeze-receipt/v1",
        "status": "frozen",
        "development_task_count": len(development),
        "held_out_task_count": len(held_out),
        "condition_count": len(CONDITIONS),
        "nonlegal_family_count": len(families),
        "manifest_digest": digest(manifest),
        "outcome_access_before_freeze": False,
    }

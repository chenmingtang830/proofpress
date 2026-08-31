#!/usr/bin/env python3
"""Create a content-addressed, private Phase C pre-run freeze receipt.

This command deliberately creates no executor, model, or grading call.  It
only replaces the v25 placeholders with byte digests for the exact task/source
manifest, graph, rubric, route and budget contracts that a later run must use.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
CONTRACT_PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/transfer_validation_contract.py"
SPEC = importlib.util.spec_from_file_location("transfer_validation_contract", CONTRACT_PATH)
contract = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(contract)

CONTROL_ARGUMENTS = {
    "task_source_manifest_digest": "task_source_manifest",
    "graph_digest": "graph",
    "executor": "executor_config",
    "grader": "grader_config",
    "executor_gateway_canary": "executor_gateway_canary",
    "grader_gateway_canary": "grader_gateway_canary",
    "rubric_digest": "rubric_manifest",
    "retry_policy": "retry_policy",
    "disclosure_budget": "disclosure_budget",
    "executor_budget": "executor_budget",
    "native_output_contract": "native_output_contract",
    "primary_extraction_qualification": "primary_extraction_qualification",
}


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return "sha256:" + value.hexdigest()


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _metric(row: Any, *, name: str, minimum: float) -> None:
    """Require a published, threshold-meeting held-out metric.

    The development gate proves the frozen qualification route earned access to
    held-out documents.  Phase C additionally requires the held-out panel to
    have actually run; a mere ``heldout_authorized`` bit would otherwise allow
    a route to be frozen before its sensitivity evidence exists.
    """
    if not _number(row) or row < minimum:
        raise ValueError(f"extraction qualification held-out {name} did not meet the frozen minimum")


def _digest(value: Any, *, field: str) -> None:
    if not isinstance(value, str) or len(value) != 71 or not value.startswith("sha256:"):
        raise ValueError(f"{field} must be a sha256 digest")
    try:
        int(value[7:], 16)
    except ValueError as exc:
        raise ValueError(f"{field} must be a sha256 digest") from exc


def validate_extraction_qualification(report: dict[str, Any], *, route: str,
                                      key: str) -> None:
    """Validate an executed, source-safe Stage B.5 qualification summary.

    Reports keep document content private.  This intentionally checks only
    panel counts, published metrics, route identity, and the no-admission
    boundary before allowing their bytes into a Phase C freeze receipt.
    """
    if not isinstance(report, dict):
        raise ValueError("extraction qualification must be a JSON object")
    if report.get("automatic_admission") is not False or report.get("human_approval_required") is not True:
        raise ValueError("extraction qualification changed the Human Approval boundary")
    extractor = report.get(key)
    if not isinstance(extractor, dict) or extractor.get("route") != route:
        raise ValueError(f"extraction qualification route mismatch for {key}")
    gate = extractor.get("development_gate")
    if not isinstance(gate, dict) or gate.get("status") != "pass" or gate.get("heldout_authorized") is not True:
        raise ValueError(f"extraction qualification development gate did not pass for {key}")
    heldout = extractor.get("heldout_conformance")
    if not isinstance(heldout, dict) or not isinstance(heldout.get("documents_scored"), int) or heldout["documents_scored"] < 1:
        raise ValueError(f"extraction qualification held-out panel was not executed for {key}")
    for name, minimum in (("text_blocks_f1", .90), ("table_cells_f1", 1.0),
                          ("numeric_values_f1", 1.0), ("locator_rate", .90),
                          ("reading_order_rate", .80), ("cross_page_continuations_f1", 1.0)):
        _metric(heldout.get(name), name=name, minimum=minimum)
    ecological = extractor.get("ecological")
    if not isinstance(ecological, dict) or ecological.get("failed") != 0:
        raise ValueError(f"extraction qualification ecological panel did not complete for {key}")
    if not isinstance(ecological.get("documents"), int) or ecological.get("documents", 0) < 1:
        raise ValueError(f"extraction qualification ecological panel is absent for {key}")
    provenance = extractor.get("envelope_provenance")
    if not isinstance(provenance, dict):
        raise ValueError(f"extraction qualification envelope provenance is absent for {key}")
    if not all(isinstance(provenance.get(field), str) and provenance[field]
               for field in ("provider", "model", "version", "license", "model_revision")):
        raise ValueError(f"extraction qualification extractor identity is incomplete for {key}")
    _digest(provenance.get("config_digest"), field="extraction qualification config_digest")
    _digest(provenance.get("envelope_set_digest"), field="extraction qualification envelope_set_digest")
    if (not isinstance(provenance.get("envelope_count"), int)
            or provenance["envelope_count"] < ecological["documents"]):
        raise ValueError(f"extraction qualification envelope coverage is incomplete for {key}")
    if (provenance.get("status") != "not_governed_candidate"
            or provenance.get("admitted") is not False
            or provenance.get("human_approval_required") is not True):
        raise ValueError(f"extraction qualification envelope provenance changed the admission boundary for {key}")


def _canary_telemetry(value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError("Gateway canary telemetry is missing")
    cost = value.get("cost_usd")
    if cost is not None and (not _number(cost) or cost < 0):
        raise ValueError("Gateway canary cost telemetry is invalid")
    for name in ("input_tokens", "output_tokens"):
        count = value.get(name)
        if count is not None and (not isinstance(count, int) or isinstance(count, bool) or count < 0):
            raise ValueError("Gateway canary token telemetry is invalid")


def validate_gateway_canary(report: dict[str, Any], *, role: str,
                            config_path: Path, config: dict[str, Any]) -> None:
    """Bind a successful synthetic route check to exactly one frozen config."""
    if not isinstance(report, dict) or report.get("schema_version") != "proofpress/phase-c-gateway-canary/v1":
        raise ValueError(f"{role} Gateway canary schema is missing")
    if report.get("status") != "pass" or report.get("role") != role:
        raise ValueError(f"{role} Gateway canary did not pass")
    if report.get("automatic_admission") is not False or report.get("human_approval_required") is not True:
        raise ValueError(f"{role} Gateway canary changed the Human Approval boundary")
    if (report.get("config_digest") != file_digest(config_path)
            or report.get("model") != config.get("model") or report.get("provider") != config.get("provider")):
        raise ValueError(f"{role} Gateway canary does not match the frozen config")
    if any(field in report for field in ("artifact", "grade", "task", "prompt", "rubric", "candidate", "projection")):
        raise ValueError(f"{role} Gateway canary retained forbidden work-product content")
    _canary_telemetry(report.get("telemetry"))


def freeze(manifest: dict[str, Any], controls: dict[str, Path]) -> tuple[dict[str, Any], dict[str, Any]]:
    if set(controls) != set(CONTROL_ARGUMENTS):
        raise ValueError("every Phase C control file is required")
    if any(not path.is_file() for path in controls.values()):
        raise ValueError("every Phase C control must be a readable regular file")
    extraction = manifest.get("stage_b5_extraction")
    if not isinstance(extraction, dict):
        raise ValueError("Stage B.5 extraction contract is missing")
    primary = json.loads(controls["primary_extraction_qualification"].read_text())
    validate_extraction_qualification(primary, route=str(extraction.get("primary_route") or ""),
                                      key="paddleocr_vl_1_6_mlx")
    executor = json.loads(controls["executor"].read_text())
    grader = json.loads(controls["grader"].read_text())
    if not isinstance(executor, dict) or not isinstance(grader, dict):
        raise ValueError("Phase C Gateway configs must be JSON objects")
    validate_gateway_canary(json.loads(controls["executor_gateway_canary"].read_text()), role="executor",
                            config_path=controls["executor"], config=executor)
    validate_gateway_canary(json.loads(controls["grader_gateway_canary"].read_text()), role="grader",
                            config_path=controls["grader"], config=grader)
    frozen = json.loads(json.dumps(manifest))
    frozen["frozen_controls"] = {field: file_digest(controls[field]) for field in CONTROL_ARGUMENTS}
    frozen["execution_status"] = "frozen-pre-run-no-executor-called"
    receipt = contract.validate_transfer_manifest(frozen)
    receipt.update({"control_digests": frozen["frozen_controls"],
                    "automatic_admission": False, "human_approval_required": True,
                    "executor_called": False, "grader_called": False})
    return frozen, receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--v25-manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    for argument in CONTROL_ARGUMENTS.values():
        parser.add_argument("--" + argument.replace("_", "-"), type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.v25_manifest.read_text())
    controls = {field: getattr(args, argument) for field, argument in CONTROL_ARGUMENTS.items()}
    frozen, receipt = freeze(manifest, controls)
    args.out.mkdir(parents=True, exist_ok=True); args.out.chmod(0o700)
    manifest_path = args.out / "phase-c-frozen-manifest-private.json"
    receipt_path = args.out / "phase-c-freeze-receipt-sanitized.json"
    manifest_path.write_text(json.dumps(frozen, indent=2, sort_keys=True) + "\n"); manifest_path.chmod(0o600)
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n"); receipt_path.chmod(0o600)
    print(json.dumps({"status": receipt["status"], "manifest_digest": receipt["manifest_digest"],
                      "executor_called": False, "grader_called": False}, sort_keys=True))


if __name__ == "__main__":
    main()

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
    "rubric_digest": "rubric_manifest",
    "retry_policy": "retry_policy",
    "disclosure_budget": "disclosure_budget",
    "executor_budget": "executor_budget",
    "native_output_contract": "native_output_contract",
}


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return "sha256:" + value.hexdigest()


def freeze(manifest: dict[str, Any], controls: dict[str, Path]) -> tuple[dict[str, Any], dict[str, Any]]:
    if set(controls) != set(CONTROL_ARGUMENTS):
        raise ValueError("every Phase C control file is required")
    if any(not path.is_file() for path in controls.values()):
        raise ValueError("every Phase C control must be a readable regular file")
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

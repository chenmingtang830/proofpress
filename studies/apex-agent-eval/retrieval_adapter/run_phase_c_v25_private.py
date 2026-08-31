#!/usr/bin/env python3
"""One ordered private entry point for the frozen v25 Phase C experiment.

Without ``--execute`` this command only compiles private task controls and
content-addressed Gateway configs.  With ``--execute`` it follows the only
permitted order: synthetic executor/grader canaries, content-addressed freeze,
no-model preflight, then the 12-task × 3-condition panel.  It never prints or
stores API keys, prompts, source text, rubrics, candidates, or model output in
the repository.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = ROOT / "studies/apex-agent-eval/results/exact-knowledge-transfer-v25-manifest.json"
ADAPTER_PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/phase_c_gateway_adapter_private.py"


def _load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


task_controls = _load("studies/apex-agent-eval/retrieval_adapter/build_phase_c_task_controls_private.py", "phase_c_task_controls")
gateway_configs = _load("studies/apex-agent-eval/retrieval_adapter/build_phase_c_gateway_config_private.py", "phase_c_gateway_configs")
canary = _load("studies/apex-agent-eval/retrieval_adapter/run_phase_c_gateway_canary_private.py", "phase_c_gateway_canary")
freeze = _load("studies/apex-agent-eval/retrieval_adapter/freeze_v25_phase_c_inputs_private.py", "freeze_phase_c")
runner = _load("studies/apex-agent-eval/retrieval_adapter/run_frozen_phase_c_private.py", "run_frozen_phase_c")

SCHEMA = "proofpress/phase-c-v25-orchestration/v1"


def _read(path: Path, label: str) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def _write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.parent.chmod(0o700)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"); path.chmod(0o600)


def _fresh_out(out: Path) -> None:
    if out.exists() and not out.is_dir():
        raise ValueError("Phase C output path must be a directory")
    if out.exists() and any(out.iterdir()):
        raise ValueError("Phase C output directory must be empty for a fresh frozen run")
    out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)


def _config_args(role: str, values: dict[str, Any]) -> dict[str, Any]:
    return {"model": values[f"{role}_model"], "provider": values[f"{role}_provider"],
            "reasoning_effort": values[f"{role}_reasoning_effort"],
            "max_output_tokens": values[f"{role}_max_output_tokens"],
            "timeout_seconds": values[f"{role}_timeout_seconds"]}


def prepare(*, manifest_path: Path, task_root: Path, graph: Path, bridge: Path,
            primary_extraction_qualification: Path, retry_policy: Path, disclosure_budget: Path,
            executor_budget: Path, native_output_contract: Path, out: Path,
            settings: dict[str, Any]) -> tuple[dict[str, Path], dict[str, Any]]:
    """Build every non-model control into a fresh caller-owned private folder."""
    _fresh_out(out)
    manifest = _read(manifest_path, "v25 manifest")
    source, rubrics, task_receipt = task_controls.build(manifest=manifest, task_root=task_root)
    task_source = out / "phase-c-task-source-private.json"
    rubric_manifest = out / "phase-c-rubric-manifest-private.json"
    _write(task_source, source); _write(rubric_manifest, rubrics); _write(out / "phase-c-task-controls-sanitized.json", task_receipt)
    controls = {"task_source_manifest_digest": task_source, "rubric_digest": rubric_manifest,
                "graph_digest": graph, "primary_extraction_qualification": primary_extraction_qualification,
                "retry_policy": retry_policy, "disclosure_budget": disclosure_budget,
                "executor_budget": executor_budget, "native_output_contract": native_output_contract}
    for role in ("executor", "grader"):
        config = gateway_configs.build(role=role, adapter=ADAPTER_PATH, bridge=bridge, **_config_args(role, settings))
        path = out / f"phase-c-{role}-gateway-config-private.json"
        _write(path, config); controls[role] = path
    receipt = {"schema_version": SCHEMA, "status": "prepared-no-model-call", "automatic_admission": False,
               "human_approval_required": True, "task_count": len(source["tasks"]),
               "task_source_digest": task_controls.file_digest(task_source),
               "rubric_manifest_digest": task_controls.file_digest(rubric_manifest),
               "executor_config_digest": gateway_configs.file_digest(controls["executor"]),
               "grader_config_digest": gateway_configs.file_digest(controls["grader"]),
               "decision_boundary": "Preparation only; no Gateway, executor, grader, source claim, or candidate call occurred."}
    _write(out / "phase-c-orchestration-receipt-sanitized.json", receipt)
    return controls, receipt


def _canary_receipt(*, config_path: Path, role: str) -> dict[str, Any]:
    result = canary.run(config_path=config_path, role=role)
    _write(config_path.parent / f"phase-c-{role}-gateway-canary-sanitized.json", result)
    return result


def execute(*, manifest_path: Path, controls: dict[str, Path], out: Path) -> dict[str, Any]:
    """Run canaries, freeze, preflight, and Phase C in that exact order."""
    canaries = {role: _canary_receipt(config_path=controls[role], role=role)
                for role in ("executor", "grader")}
    if any(receipt.get("status") != "pass" for receipt in canaries.values()):
        receipt = {"schema_version": SCHEMA, "status": "inconclusive-route-canary", "automatic_admission": False,
                   "human_approval_required": True,
                   "executor_canary_status": canaries["executor"].get("status"),
                   "grader_canary_status": canaries["grader"].get("status")}
        _write(out / "phase-c-orchestration-receipt-sanitized.json", receipt)
        return receipt
    controls = {**controls,
                "executor_gateway_canary": out / "phase-c-executor-gateway-canary-sanitized.json",
                "grader_gateway_canary": out / "phase-c-grader-gateway-canary-sanitized.json"}
    frozen, freeze_receipt = freeze.freeze(_read(manifest_path, "v25 manifest"), controls)
    frozen_path = out / "phase-c-frozen-manifest-private.json"
    freeze_path = out / "phase-c-freeze-receipt-sanitized.json"
    _write(frozen_path, frozen); _write(freeze_path, freeze_receipt)
    preflight = runner.validate_preflight(frozen_manifest_path=frozen_path, freeze_receipt_path=freeze_path,
                                          control_paths=controls)
    result = runner.run(preflight, out=out)
    _write(out / "phase-c-result-sanitized.json", result)
    receipt = {"schema_version": SCHEMA, "status": result["status"], "automatic_admission": False,
               "human_approval_required": True, "frozen_manifest_digest": result["frozen_manifest_digest"],
               "planned_cells": result["planned_cells"], "scored_cells": result["scored_cells"],
               "inconclusive_cells": result["inconclusive_cells"],
               "decision_boundary": "Private Phase C evaluation only; no source, extraction, claim, or model output is admitted."}
    _write(out / "phase-c-orchestration-receipt-sanitized.json", receipt)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-root", required=True, type=Path)
    parser.add_argument("--graph", required=True, type=Path)
    parser.add_argument("--bridge", required=True, type=Path)
    parser.add_argument("--primary-extraction-qualification", required=True, type=Path)
    parser.add_argument("--retry-policy", required=True, type=Path)
    parser.add_argument("--disclosure-budget", required=True, type=Path)
    parser.add_argument("--executor-budget", required=True, type=Path)
    parser.add_argument("--native-output-contract", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--v25-manifest", default=MANIFEST_PATH, type=Path)
    parser.add_argument("--execute", action="store_true", help="Authorize synthetic canaries and the paid Phase C model panel.")
    for role in ("executor", "grader"):
        parser.add_argument(f"--{role}-model", required=True)
        parser.add_argument(f"--{role}-provider", required=True)
        parser.add_argument(f"--{role}-reasoning-effort", required=True)
        parser.add_argument(f"--{role}-max-output-tokens", required=True, type=int)
        parser.add_argument(f"--{role}-timeout-seconds", required=True, type=float)
    args = parser.parse_args(); settings = vars(args)
    try:
        controls, prepared = prepare(manifest_path=args.v25_manifest, task_root=args.task_root, graph=args.graph,
                                     bridge=args.bridge, primary_extraction_qualification=args.primary_extraction_qualification,
                                     retry_policy=args.retry_policy, disclosure_budget=args.disclosure_budget,
                                     executor_budget=args.executor_budget, native_output_contract=args.native_output_contract,
                                     out=args.out, settings=settings)
        result = execute(manifest_path=args.v25_manifest, controls=controls, out=args.out) if args.execute else prepared
        print(json.dumps({key: result.get(key) for key in ("status", "planned_cells", "scored_cells", "inconclusive_cells")}, sort_keys=True))
        if result.get("status") not in {"prepared-no-model-call", "complete"}:
            raise SystemExit(1)
    except Exception as exc:
        print(f"phase-c-v25-orchestration: {type(exc).__name__}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()

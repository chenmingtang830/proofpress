#!/usr/bin/env python3
"""Qualify one frozen Phase C Gateway configuration without private task data.

The canary invokes the exact frozen executor or grader command once with a
synthetic, non-APEX request.  Its output deliberately retains only config
identity, terminal status, and cost/token telemetry.  The underlying adapter
must still prove the one-provider routing receipt before any result is called
``pass``.  A full Phase C run therefore cannot be the first evidence that a
selected model route supports its required structured response.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
RUNNER_PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/run_frozen_phase_c_private.py"
RUNNER_SPEC = importlib.util.spec_from_file_location("run_frozen_phase_c", RUNNER_PATH)
runner = importlib.util.module_from_spec(RUNNER_SPEC); RUNNER_SPEC.loader.exec_module(runner)
SCHEMA = "proofpress/phase-c-gateway-canary/v1"


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return "sha256:" + value.hexdigest()


def request_for(role: str) -> dict[str, Any]:
    """Create a route-only probe; no APEX prompt, source, graph, or rubric."""
    if role == "executor":
        return {
            "schema_version": runner.SCHEMA,
            "kind": "executor",
            "task": {"task_id": "phase-c-gateway-canary", "prompt": "Return the requested structured artifact."},
            "projection": {"canary": True, "automatic_admission": False, "human_approval_required": True},
            "executor_budget": {"purpose": "route-canary-only"},
            "native_output_contract": {"canary": True},
            "instruction": "This is a route canary, not an APEX task. Return only the structured artifact.",
        }
    if role == "grader":
        return {
            "schema_version": runner.SCHEMA,
            "kind": "grader",
            "task": {"task_id": "phase-c-gateway-canary", "prompt": "Evaluate the synthetic candidate.",
                     "rubric": [{"id": "synthetic-structured-output"}]},
            "candidate": {"answer": "synthetic canary artifact"},
            "replica": 1,
            "instruction": "This is a route canary, not an APEX task. Return only the structured grade.",
        }
    raise ValueError("canary role must be executor or grader")


def validate_config(config: dict[str, Any], role: str) -> list[str]:
    runner._validate_command_config(config, role=role)
    command = config["command"]
    if command.count("--bridge") != 1 or not command[command.index("--bridge") + 1:command.index("--bridge") + 2]:
        raise ValueError("frozen Gateway config requires exactly one bridge path")
    return list(command)


def sanitize(*, config_path: Path, config: dict[str, Any], role: str,
             output: dict[str, Any], terminal: dict[str, Any]) -> dict[str, Any]:
    """Report route evidence without retaining an answer, grade, or prompt."""
    try:
        if terminal.get("status") != "ok":
            raise ValueError(str(terminal.get("reason") or "command_failure"))
        if role == "executor":
            _, telemetry = runner._executor_response(output)
        else:
            _, telemetry = runner._grader_response(output)
    except (ValueError, TypeError) as exc:
        return {"schema_version": SCHEMA, "status": "inconclusive", "role": role,
                "config_digest": file_digest(config_path), "model": config["model"], "provider": config["provider"],
                "reason": str(exc), "automatic_admission": False, "human_approval_required": True}
    return {"schema_version": SCHEMA, "status": "pass", "role": role,
            "config_digest": file_digest(config_path), "model": config["model"], "provider": config["provider"],
            "max_output_tokens": config["max_output_tokens"], "telemetry": telemetry,
            "automatic_admission": False, "human_approval_required": True,
            "decision_boundary": "Synthetic route check only; no APEX task, source, graph, artifact, or grade is admitted."}


def run(*, config_path: Path, role: str) -> dict[str, Any]:
    config = json.loads(config_path.read_text())
    if not isinstance(config, dict):
        raise ValueError("frozen Gateway config must be a JSON object")
    command = validate_config(config, role)
    output, terminal = runner._run_command(command, request_for(role), float(config["timeout_seconds"]))
    return sanitize(config_path=config_path, config=config, role=role, output=output, terminal=terminal)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--role", choices=("executor", "grader"), required=True)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = run(config_path=args.config, role=args.role)
        args.out.parent.mkdir(parents=True, exist_ok=True); args.out.parent.chmod(0o700)
        args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"); args.out.chmod(0o600)
        print(json.dumps({key: result.get(key) for key in ("status", "role", "model", "provider", "config_digest")}, sort_keys=True))
        if result["status"] != "pass":
            raise SystemExit(1)
    except Exception as exc:
        # Never write a bridge response, model response, or request payload to
        # stdout/stderr: those are caller-private even in a synthetic canary.
        print(f"phase-c-gateway-canary: {type(exc).__name__}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()

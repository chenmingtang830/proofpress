#!/usr/bin/env python3
"""Freeze-ready Phase C command configurations for the existing Gateway bridge.

The caller explicitly chooses each model/provider/budget pair.  This helper
does not contact a model and never reads or stores an API key; it content-
addresses the committed adapter plus the caller-owned Gateway bridge so the
Phase C runner can reject implementation drift before task data is opened.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "proofpress/phase-c-gateway-config/v1"


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return "sha256:" + value.hexdigest()


def _nonempty(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} is required")
    return value.strip()


def _positive(value: float | int, label: str) -> float | int:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        raise ValueError(f"{label} must be positive")
    return value


def build(*, role: str, adapter: Path, bridge: Path, model: str, provider: str,
          reasoning_effort: str, max_output_tokens: int, timeout_seconds: float) -> dict[str, Any]:
    """Produce one no-fallback, content-addressed command config."""
    if role not in {"executor", "grader"}:
        raise ValueError("role must be executor or grader")
    adapter, bridge = adapter.resolve(), bridge.resolve()
    if not adapter.is_file() or not bridge.is_file():
        raise ValueError("adapter and bridge must be readable regular files")
    model = _nonempty(model, "model")
    provider = _nonempty(provider, "provider")
    reasoning_effort = _nonempty(reasoning_effort, "reasoning effort")
    if not isinstance(max_output_tokens, int) or isinstance(max_output_tokens, bool):
        raise ValueError("max output tokens must be an integer")
    _positive(max_output_tokens, "max output tokens")
    _positive(timeout_seconds, "timeout seconds")
    command = [sys.executable, str(adapter), "--bridge", str(bridge), "--model", model,
               "--gateway-provider-only", provider, "--reasoning-effort", reasoning_effort,
               "--max-output-tokens", str(max_output_tokens), "--timeout-seconds", str(timeout_seconds)]
    config: dict[str, Any] = {
        "schema_version": SCHEMA,
        "role": role,
        "model": model,
        "provider": provider,
        "reasoning_effort": reasoning_effort,
        "max_output_tokens": max_output_tokens,
        "timeout_seconds": timeout_seconds,
        "gateway_policy": {
            "gateway_provider_only": provider,
            "retries": "forbidden",
            "fallback": "forbidden",
            "routing_receipt": "one-successful-attempt-required",
        },
        "command": command,
        "implementation_files": [
            {"path": str(adapter), "digest": file_digest(adapter)},
            {"path": str(bridge), "digest": file_digest(bridge)},
        ],
    }
    if role == "grader":
        config["blind_grades_per_artifact"] = 3
    return config


def _write_private(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    path.chmod(0o600)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", required=True, type=Path)
    parser.add_argument("--bridge", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    for role in ("executor", "grader"):
        parser.add_argument(f"--{role}-model", required=True)
        parser.add_argument(f"--{role}-provider", required=True)
        parser.add_argument(f"--{role}-reasoning-effort", required=True)
        parser.add_argument(f"--{role}-max-output-tokens", required=True, type=int)
        parser.add_argument(f"--{role}-timeout-seconds", required=True, type=float)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True); args.out.chmod(0o700)
    output = {}
    for role in ("executor", "grader"):
        config = build(role=role, adapter=args.adapter, bridge=args.bridge,
                       model=getattr(args, f"{role}_model"), provider=getattr(args, f"{role}_provider"),
                       reasoning_effort=getattr(args, f"{role}_reasoning_effort"),
                       max_output_tokens=getattr(args, f"{role}_max_output_tokens"),
                       timeout_seconds=getattr(args, f"{role}_timeout_seconds"))
        path = args.out / f"phase-c-{role}-gateway-config-private.json"
        _write_private(path, config)
        output[f"{role}_config_digest"] = file_digest(path)
    print(json.dumps({"status": "built-private-gateway-configs", **output}, sort_keys=True))


if __name__ == "__main__":
    main()

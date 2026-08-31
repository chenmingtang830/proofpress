#!/usr/bin/env python3
"""Private, no-fallback AI Gateway adapter for the frozen Phase C runner.

It deliberately lives beside the experiment rather than copying a credential or
Gateway client into the repository.  The caller supplies the already-installed
bridge in ``proofpress-dev``.  This adapter turns one Phase C executor/grader
request into one structured Gateway invocation, verifies the Gateway-issued
routing receipt, and returns only the native runner's artifact/grade plus
token-and-cost telemetry on stdout.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


SCHEMA = "proofpress/phase-c-gateway-adapter/v1"
ROLES = {"executor", "grader"}


def _executor_schema() -> dict[str, Any]:
    return {"type": "object", "additionalProperties": False,
            "required": ["artifact"], "properties": {
                "artifact": {"type": "object", "additionalProperties": False,
                             "required": ["answer"], "properties": {"answer": {"type": "string"}}}}}


def _grader_schema() -> dict[str, Any]:
    return {"type": "object", "additionalProperties": False,
            "required": ["grade"], "properties": {
                "grade": {"type": "object", "additionalProperties": False,
                          "required": ["rubric_fraction", "unsupported_claims", "citation_errors", "authority_errors"],
                          "properties": {"rubric_fraction": {"type": "number", "minimum": 0, "maximum": 1},
                                         "unsupported_claims": {"type": "integer", "minimum": 0},
                                         "citation_errors": {"type": "integer", "minimum": 0},
                                         "authority_errors": {"type": "integer", "minimum": 0}}}}}


def _model_messages(request: dict[str, Any]) -> list[dict[str, str]]:
    role = request.get("kind")
    if role == "executor":
        system = ("You are the frozen Phase C executor. Use only the supplied task and governed projection. "
                  "The task rubric and outcome are unavailable. Preserve the stated governance boundary. "
                  "Return only the requested structured artifact.")
        visible = {key: request[key] for key in ("task", "projection", "executor_budget",
                                                  "native_output_contract", "instruction") if key in request}
    elif role == "grader":
        system = ("You are the frozen Phase C blind grader. Grade only the supplied candidate against the supplied rubric. "
                  "Do not infer information from a projection or a different artifact. Return only the requested structured grade.")
        visible = {key: request[key] for key in ("task", "candidate", "instruction", "replica") if key in request}
    else:
        raise ValueError("Phase C Gateway adapter requires executor or grader kind")
    return [{"role": "system", "content": system},
            {"role": "user", "content": json.dumps(visible, ensure_ascii=False, sort_keys=True)}]


def build_gateway_request(request: dict[str, Any], *, model: str, provider: str,
                          max_output_tokens: int, timeout_seconds: float,
                          reasoning_effort: str) -> dict[str, Any]:
    if request.get("schema_version") != "proofpress/frozen-phase-c-run/v1":
        raise ValueError("unexpected Phase C request schema")
    role = request.get("kind")
    if role not in ROLES:
        raise ValueError("Phase C Gateway adapter requires executor or grader kind")
    if not all(isinstance(value, str) and value for value in (model, provider, reasoning_effort)):
        raise ValueError("model, provider, and reasoning effort are required")
    if max_output_tokens < 1 or timeout_seconds <= 0:
        raise ValueError("output-token and timeout limits must be positive")
    return {"model": model, "messages": _model_messages(request), "tools": [],
            "max_tokens": max_output_tokens, "reasoning_effort": reasoning_effort,
            "timeout_ms": int(timeout_seconds * 1000), "gateway_provider_only": provider,
            "response_format": {"type": "json_schema", "json_schema": {
                "name": f"phase_c_{role}_response", "schema": _executor_schema() if role == "executor" else _grader_schema()}}}


def _number_or_none(value: Any) -> float | int | None:
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0 else None


def _integer_or_none(value: Any) -> int | None:
    """Token counts must retain the frozen runner's integer receipt contract."""
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None


def validate_routing_receipt(receipt: Any, *, model: str, provider: str) -> None:
    """Reject a route that is incomplete, aliased, retried, or provider-failed over."""
    if not isinstance(receipt, dict):
        raise ValueError("Gateway routing receipt is missing")
    if (receipt.get("original_model_id") != model or receipt.get("canonical_slug") != model
            or receipt.get("resolved_provider") != provider or receipt.get("final_provider") != provider):
        raise ValueError("Gateway routing receipt did not preserve frozen model and provider")
    if receipt.get("model_attempt_count") != 1 or receipt.get("total_provider_attempt_count") != 1:
        raise ValueError("Gateway routing receipt records retry or fallback")
    attempts = receipt.get("model_attempts")
    if not isinstance(attempts, list) or len(attempts) != 1 or not isinstance(attempts[0], dict):
        raise ValueError("Gateway routing receipt has invalid model attempts")
    attempt = attempts[0]
    providers = attempt.get("provider_attempts")
    if (attempt.get("canonical_slug") != model or attempt.get("success") is not True
            or attempt.get("provider_attempt_count") != 1 or not isinstance(providers, list) or len(providers) != 1):
        raise ValueError("Gateway routing receipt does not prove one successful model attempt")
    provider_attempt = providers[0]
    if not isinstance(provider_attempt, dict) or provider_attempt.get("provider") != provider or provider_attempt.get("success") is not True:
        raise ValueError("Gateway routing receipt does not prove one successful provider attempt")


def normalize_response(response: dict[str, Any], *, role: str, model: str, provider: str) -> dict[str, Any]:
    validate_routing_receipt(response.get("gateway_routing_receipt"), model=model, provider=provider)
    choices = response.get("choices")
    if not isinstance(choices, list) or len(choices) != 1 or not isinstance(choices[0], dict):
        raise ValueError("Gateway response requires exactly one choice")
    message = choices[0].get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        raise ValueError("Gateway response has no structured message content")
    value = json.loads(message["content"])
    if not isinstance(value, dict):
        raise ValueError("Gateway structured response must be an object")
    usage = response.get("usage") if isinstance(response.get("usage"), dict) else {}
    telemetry = {"cost_usd": _number_or_none(usage.get("cost")),
                 "input_tokens": _integer_or_none(usage.get("prompt_tokens")),
                 "output_tokens": _integer_or_none(usage.get("completion_tokens"))}
    if role == "executor":
        artifact = value.get("artifact")
        if not isinstance(artifact, dict) or not isinstance(artifact.get("answer"), str):
            raise ValueError("Gateway executor response requires an answer artifact")
        return {"artifact": artifact, "telemetry": telemetry}
    grade = value.get("grade")
    if not isinstance(grade, dict):
        raise ValueError("Gateway grader response requires a grade")
    return {"grade": grade, "telemetry": telemetry}


def invoke(bridge: Path, bridge_request: dict[str, Any], *, timeout_seconds: float) -> dict[str, Any]:
    if not bridge.is_file():
        raise ValueError("Gateway bridge must be a readable regular file")
    if not os.environ.get("AI_GATEWAY_API_KEY"):
        raise ValueError("AI_GATEWAY_API_KEY is required in the local environment")
    environment = {"PATH": os.environ.get("PATH", ""), "AI_GATEWAY_API_KEY": os.environ["AI_GATEWAY_API_KEY"]}
    completed = subprocess.run(["node", str(bridge)], input=json.dumps(bridge_request), text=True,
                               capture_output=True, timeout=timeout_seconds + 15,
                               cwd=bridge.parent, env=environment, check=False)
    try:
        value = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Gateway bridge returned non-JSON output") from exc
    if completed.returncode or value.get("error"):
        error = value.get("error") if isinstance(value.get("error"), dict) else {}
        error_type = error.get("type") if isinstance(error.get("type"), str) else "gateway-bridge-failed"
        raise RuntimeError(f"Gateway bridge failed: {error_type}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bridge", required=True, type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--gateway-provider-only", required=True)
    parser.add_argument("--reasoning-effort", required=True)
    parser.add_argument("--max-output-tokens", required=True, type=int)
    parser.add_argument("--timeout-seconds", required=True, type=float)
    args = parser.parse_args()
    try:
        request = json.loads(sys.stdin.read())
        if not isinstance(request, dict):
            raise ValueError("Phase C request must be a JSON object")
        gateway_request = build_gateway_request(request, model=args.model, provider=args.gateway_provider_only,
                                                max_output_tokens=args.max_output_tokens,
                                                timeout_seconds=args.timeout_seconds,
                                                reasoning_effort=args.reasoning_effort)
        response = invoke(args.bridge, gateway_request, timeout_seconds=args.timeout_seconds)
        output = normalize_response(response, role=request["kind"], model=args.model,
                                    provider=args.gateway_provider_only)
        print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    except Exception as exc:
        # Do not print private prompts, rubrics, candidates, headers, or bridge
        # response text.  The frozen runner records this as an inconclusive cell.
        print(f"phase-c-gateway-adapter: {type(exc).__name__}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()

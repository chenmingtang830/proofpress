#!/usr/bin/env python3
"""Run fixed-route structured-output canaries before role-level evaluation."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
from typing import Any

from governed_workflow_contract import digest
from run_claim_construction_private import Gateway

SCHEMA = "proofpress/gateway-role-canary/v1"
ROLES = ("decomposition", "atom_extraction", "claim_proposal", "claim_critic")
MODELS = {
    "deepseek": ("deepseek/deepseek-v4-flash", "alibaba", "high"),
    "ling": ("inclusionai/ling-3.0-flash-fin", "novita", "high"),
    "qwen": ("alibaba/qwen3.8-27b", "alibaba", "high"),
    "muse": ("meta/muse-spark-1.2", "meta", "medium"),
    "glm": ("zai/glm-5.3-flash", "baseten", "high"),
    "sol": ("openai/gpt-5.6-sol", "openai", "high"),
    "gemini": ("google/gemini-3.1-pro-preview", "vertex", "low"),
}
OUTPUT_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["role", "items", "safe_to_continue"],
    "properties": {
        "role": {"type": "string", "enum": list(ROLES)},
        "items": {"type": "array", "minItems": 1, "maxItems": 2,
                  "items": {"type": "object", "additionalProperties": False,
                            "required": ["id", "label"],
                            "properties": {"id": {"type": "string", "maxLength": 24},
                                           "label": {"type": "string", "maxLength": 48}}}},
        "safe_to_continue": {"type": "boolean"},
    },
}


def run_model(label: str, route: tuple[str, str, str], server: str,
              output: Path, timeout: float) -> dict[str, Any]:
    model, provider, reasoning = route
    gateway = Gateway(server, model, provider, output, timeout, reasoning,
                      structured_output=True, min_output_tokens=256)
    cells = []
    try:
        for role in ROLES:
            result = gateway.call(
                "Follow the JSON schema exactly. Do not add prose.",
                f"Return one synthetic canary item for role {role}. Set role exactly to {role} and safe_to_continue true.",
                256, OUTPUT_SCHEMA, f"proofpress_{role}_canary")
            value = result.get("value") if result.get("ok") else None
            semantic_ok = bool(value and value.get("role") == role
                               and value.get("safe_to_continue") is True
                               and isinstance(value.get("items"), list) and value["items"])
            cells.append({"role": role,
                          "status": "pass" if result.get("ok") and semantic_ok else "inconclusive",
                          "transport_status": result["record"].get("status"),
                          "structured_output_mode": result["record"].get("structured_output_mode"),
                          "latency_ms": result["record"].get("latency_ms"),
                          "cost_usd": result["record"].get("cost_usd"),
                          "output_digest": result["record"].get("output_digest"),
                          "error_type": result["record"].get("error_type")})
    finally:
        gateway.stop()
    receipts = gateway.receipt_rows()
    receipt_ok = (len(receipts) == len(ROLES) and all(
        row.get("terminal") is True and row.get("model") == model
        and row.get("provider") == provider and row.get("fallback_used") is False
        and row.get("input_tokens") is not None and row.get("output_tokens") is not None
        and row.get("cost_usd") is not None for row in receipts))
    return {"label": label, "model": model, "provider": provider, "reasoning": reasoning,
            "cells": cells, "receipt_count": len(receipts), "terminal_telemetry_complete": receipt_ok,
            "status": "pass" if receipt_ok and all(row["status"] == "pass" for row in cells)
            else "inconclusive"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gateway-server", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--max-workers", type=int, default=4)
    parser.add_argument("--models", default=",".join(MODELS),
                        help="comma-separated frozen candidate labels")
    args = parser.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    selected = [row.strip() for row in args.models.split(",") if row.strip()]
    unknown = sorted(set(selected) - set(MODELS))
    if unknown:
        raise SystemExit("unknown frozen model labels: " + ",".join(unknown))
    rows = []
    with ThreadPoolExecutor(max_workers=max(1, min(args.max_workers, len(selected)))) as pool:
        futures = {pool.submit(run_model, label, route, args.gateway_server, out, args.timeout): label
                   for label, route in MODELS.items() if label in selected}
        for future in as_completed(futures):
            label = futures[future]
            try:
                rows.append(future.result())
            except Exception as exc:
                rows.append({"label": label, "model": MODELS[label][0],
                             "provider": MODELS[label][1], "reasoning": MODELS[label][2],
                             "status": "inconclusive", "error_type": type(exc).__name__,
                             "error_digest": digest(str(exc)), "cells": [],
                             "terminal_telemetry_complete": False})
    rows.sort(key=lambda row: row["label"])
    report = {"schema_version": SCHEMA,
              "boundary": "Transport/schema qualification only; not role quality evidence.",
              "models": rows,
              "denominators": {"models": len(rows), "roles_per_model": len(ROLES),
                               "passed_models": sum(row["status"] == "pass" for row in rows)},
              "fallback": "forbidden", "report_digest": digest(rows)}
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report["denominators"], sort_keys=True))


if __name__ == "__main__":
    main()

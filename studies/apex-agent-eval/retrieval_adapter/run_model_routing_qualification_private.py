#!/usr/bin/env python3
"""Qualify critic-routing policies over the frozen four-task legal panel.

The run reuses source-bound Sol atoms from the prior gate diagnostic. It does
not expose rubric, gold, silver, or task answers to any model. Observed-fact
claims are constructed deterministically; only their verdict routing varies.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import time
from typing import Any

from model_routing_contract import (
    SCHEMA, classification_metrics, construct_observed_claims, digest,
    route_verdicts, validate_verdicts,
)
from run_claim_construction_private import Gateway, V9_CRITIC_SCHEMA, _model_call

MODELS = {
    "deepseek": {"model": "deepseek/deepseek-v4-flash", "provider": "deepinfra", "reasoning": "none"},
    "luna": {"model": "gpt-5.6-luna", "provider": "openai", "reasoning": "low"},
    "sol": {"model": "gpt-5.6-sol", "provider": "openai", "reasoning": "low"},
}
POLICIES = {
    "deepseek_only": ("deepseek", "primary_only"),
    "luna_only": ("luna", "primary_only"),
    "sol_only": ("sol", "primary_only"),
    "deepseek_escalate_sol": ("deepseek", "non_supported_or_material_to_premium"),
    "luna_escalate_sol": ("luna", "non_supported_or_material_to_premium"),
}


def critic_payload(requirements: list[dict[str, Any]], claims: list[dict[str, Any]],
                   atoms: list[dict[str, Any]]) -> dict[str, Any]:
    atom_ids = {atom_id for claim in claims for atom_id in claim.get("atom_ids", [])}
    selected_atoms = [row for row in atoms if row.get("atom_id") in atom_ids]
    return {
        "requirements": [{key: row.get(key) for key in
                          ("requirement_id", "requirement", "type", "lifecycle_category")}
                         for row in requirements],
        "claims": claims,
        "evidence_atoms": selected_atoms,
        "instruction": (
            "Return exactly one verdict per claim. A supported verdict requires the "
            "claim statement to be no broader than its explicit atom; treat the separate "
            "qualification field as binding context. Do not repair, rewrite, or admit claims."
        ),
    }


def call_critic(gateway: Gateway, requirements: list[dict[str, Any]],
                claims: list[dict[str, Any]], atoms: list[dict[str, Any]],
                task_prompt: str | None = None) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    started = time.monotonic()
    payload = critic_payload(requirements, claims, atoms)
    if task_prompt:
        payload["task"] = task_prompt
        payload["instruction"] += " Also reject claims that are not responsive to the task and bound requirement."
    result = _model_call(
        gateway,
        "You are an independent evidence-fidelity verdict gate. Return structured verdicts only.",
        json.dumps(payload, ensure_ascii=False),
        10000, V9_CRITIC_SCHEMA, "proofpress_claim_verdicts", 2,
    )
    elapsed = time.monotonic() - started
    if not result["ok"]:
        return {}, {"status": "inconclusive", "elapsed_seconds": elapsed,
                    "failure": result["record"]}
    try:
        verdicts = validate_verdicts(claims, result["value"])
    except ValueError as exc:
        return {}, {"status": "schema_failure", "elapsed_seconds": elapsed,
                    "failure_digest": digest(str(exc))}
    return verdicts, {"status": "ok", "elapsed_seconds": elapsed,
                      "verdict_counts": dict(sorted(Counter(
                          row["verdict"] for row in verdicts.values()).items()))}


def terminal_telemetry(gateways: dict[str, Gateway]) -> dict[str, Any]:
    by_model: dict[str, Any] = {}
    missing = 0; missing_tokens = 0; total_cost = 0.0; calls = 0
    total_tokens = Counter()
    detail_fields = ("uncached_input_tokens", "cache_read_input_tokens",
                     "cache_write_input_tokens", "text_output_tokens",
                     "reasoning_output_tokens")
    missing_detail_tokens = Counter({field: 0 for field in detail_fields})
    for label, gateway in gateways.items():
        rows = gateway.receipt_rows(); calls += len(gateway.calls)
        costs = []; tokens = Counter(); latency = []
        for row in rows:
            usage = row.get("usage") if isinstance(row.get("usage"), dict) else {}
            cost = usage.get("cost_usd", row.get("cost_usd"))
            if isinstance(cost, (int, float)):
                costs.append(float(cost))
            else:
                missing += 1
            input_tokens = usage.get("prompt_tokens", row.get("input_tokens"))
            output_tokens = usage.get("completion_tokens", row.get("output_tokens"))
            if isinstance(input_tokens, int) and isinstance(output_tokens, int):
                tokens["input_tokens"] += input_tokens
                tokens["output_tokens"] += output_tokens
            else:
                missing_tokens += 1
            for source in detail_fields:
                value = row.get(source)
                if isinstance(value, int):
                    tokens[source] += value
                else:
                    missing_detail_tokens[source] += 1
            if isinstance(row.get("latency_ms"), (int, float)):
                latency.append(float(row["latency_ms"]))
        missing += max(0, len(gateway.calls) - len(rows))
        missing_tokens += max(0, len(gateway.calls) - len(rows))
        for field in detail_fields:
            missing_detail_tokens[field] += max(0, len(gateway.calls) - len(rows))
        total_cost += sum(costs)
        total_tokens.update(tokens)
        by_model[label] = {"calls": len(gateway.calls), "terminal_receipts": len(rows),
                           "known_cost_usd": sum(costs), **dict(tokens),
                           "latency_ms_total": sum(latency),
                           "latency_ms_mean": sum(latency) / len(latency) if latency else None}
    return {"calls": calls, "known_cost_usd": total_cost,
            "missing_cost_calls": missing, "missing_token_calls": missing_tokens,
            "missing_detailed_token_calls": dict(missing_detail_tokens),
            **dict(total_tokens), "by_model": by_model,
            "fallback": "forbidden"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--diagnostic", required=True)
    ap.add_argument("--gateway-server", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--budget-usd", type=float, default=8.0)
    ap.add_argument("--timeout", type=float, default=300)
    args = ap.parse_args()

    diagnostic_path = Path(args.diagnostic).resolve()
    diagnostic = json.loads(diagnostic_path.read_text())
    if diagnostic.get("schema_version") != "proofpress/private-v9-gate-diagnostic/v1":
        raise SystemExit("expected the frozen v9 gate diagnostic")
    raw_root = diagnostic_path.parent / "raw" / "sol" / "receipt_preproposal"
    paths = sorted(raw_root.glob("*.json"))
    if len(paths) != 4:
        raise SystemExit("qualification requires exactly four frozen Sol-atom tasks")

    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    private = out / "raw"; private.mkdir(exist_ok=True); private.chmod(0o700)
    gateways = {
        label: Gateway(args.gateway_server, row["model"], row["provider"], out,
                       args.timeout, row["reasoning"], structured_output=True)
        for label, row in MODELS.items()
    }
    tasks: list[dict[str, Any]] = []
    try:
        for path in paths:
            source = json.loads(path.read_text())
            construction = source["construction"]
            requirements = construction["requirements"]
            atoms = construction["evidence_atoms"]
            claims = construct_observed_claims(atoms, requirements)
            verdicts: dict[str, dict[str, dict[str, Any]]] = {}
            call_status: dict[str, Any] = {}
            for label, gateway in gateways.items():
                verdicts[label], call_status[label] = call_critic(
                    gateway, requirements, claims, atoms)
            if any(row["status"] != "ok" for row in call_status.values()):
                tasks.append({"task_id": path.stem, "status": "inconclusive",
                              "claim_count": len(claims), "calls": call_status})
                continue
            reference = verdicts["sol"]
            policies: dict[str, Any] = {}
            for policy, (primary_label, mode) in POLICIES.items():
                final, escalated = route_verdicts(
                    claims, verdicts[primary_label], reference, mode=mode)
                metrics = classification_metrics(final, reference)
                supported_requirements = {
                    claim["requirement_id"] for claim in claims
                    if final[claim["id"]]["verdict"] == "supported"
                }
                policies[policy] = {
                    **metrics,
                    "supported_requirement_count": len(supported_requirements),
                    "supported_requirement_coverage": (
                        len(supported_requirements) / len(requirements) if requirements else None),
                    "escalated_claim_count": len(escalated),
                    "escalation_rate": len(escalated) / len(claims) if claims else 0.0,
                }
            raw_value = {"schema_version": SCHEMA, "task_id": path.stem,
                         "claims": claims, "model_verdicts": verdicts,
                         "call_status": call_status}
            raw_path = private / f"{path.stem}.json"
            raw_path.write_text(json.dumps(raw_value, ensure_ascii=False,
                                           indent=2, sort_keys=True) + "\n")
            raw_path.chmod(0o600)
            tasks.append({"task_id": path.stem, "status": "ok",
                          "requirement_count": len(requirements),
                          "explicit_atom_count": sum(row.get("support_mode") == "explicit" for row in atoms),
                          "deterministic_claim_count": len(claims),
                          "calls": call_status, "policies": policies,
                          "artifact_digest": digest(raw_value)})
            telemetry = terminal_telemetry(gateways)
            if telemetry["missing_cost_calls"] or telemetry["known_cost_usd"] > args.budget_usd:
                raise RuntimeError("model-routing telemetry is incomplete or over budget")
    finally:
        for gateway in gateways.values(): gateway.stop()

    telemetry = terminal_telemetry(gateways)
    completed = [row for row in tasks if row["status"] == "ok"]
    policy_summary = []
    for policy in POLICIES:
        rows = [row["policies"][policy] for row in completed]
        claim_total = sum(row["claim_count"] for row in rows)
        requirement_total = sum(next(task["requirement_count"] for task in completed
                                     if task["policies"][policy] is row) for row in rows)
        policy_summary.append({
            "policy": policy,
            "task_count": len(rows),
            "claim_count": claim_total,
            "exact_verdict_agreement": (sum(row["exact_verdict_agreement"] * row["claim_count"] for row in rows) / claim_total if claim_total else None),
            "supported_precision": (sum(row["supported_precision"] * row["claim_count"] for row in rows) / claim_total if claim_total else None),
            "supported_recall": (sum(row["supported_recall"] * row["claim_count"] for row in rows) / claim_total if claim_total else None),
            "supported_requirement_coverage": (sum(row["supported_requirement_count"] for row in rows) / requirement_total if requirement_total else None),
            "escalation_rate": (sum(row["escalated_claim_count"] for row in rows) / claim_total if claim_total else 0.0),
        })
    old_best = max(diagnostic["cells"], key=lambda row: row.get("supported_requirement_coverage") or 0)
    report = {
        "schema_version": SCHEMA,
        "boundary": "Four-task development qualification; Sol verdicts are a model reference, not gold or admission.",
        "source_diagnostic_digest": digest(diagnostic),
        "models": MODELS,
        "policies": POLICIES,
        "denominators": {"tasks": len(tasks), "completed_tasks": len(completed),
                         "requirements": sum(row.get("requirement_count", 0) for row in completed),
                         "deterministic_claims": sum(row.get("deterministic_claim_count", 0) for row in completed)},
        "old_free_form_proposer_best": {
            "extractor": old_best["extractor"], "claimability_mode": old_best["claimability_mode"],
            "supported_requirement_coverage": old_best["supported_requirement_coverage"],
        },
        "policy_summary": policy_summary,
        "tasks": tasks,
        "telemetry": {**telemetry, "budget_usd": args.budget_usd},
        "qualification": {
            "status": "pass" if len(completed) == 4 and telemetry["missing_cost_calls"] == 0 else "inconclusive",
            "checks": {"four_tasks_complete": len(completed) == 4,
                       "terminal_cost_complete": telemetry["missing_cost_calls"] == 0,
                       "fallback_forbidden": True},
        },
        "raw_private_dir": str(private),
    }
    target = out / "sanitized-report.json"
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n"); target.chmod(0o600)
    print(json.dumps({"ok": report["qualification"]["status"] == "pass",
                      "report": str(target), "known_cost_usd": telemetry["known_cost_usd"]}))


if __name__ == "__main__": main()

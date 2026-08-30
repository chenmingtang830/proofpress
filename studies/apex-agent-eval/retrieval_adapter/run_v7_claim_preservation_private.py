#!/usr/bin/env python3
"""Preserve PR36-v7 recall while trimming claims to their bound evidence.

This is a staged candidate compiler.  It never admits claims and never sees a
rubric, gold response, or silver locator.  The model may keep a v7 claim,
rewrite it to the supported subset, or reject it; it may not add a claim.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
from typing import Any

from governed_workflow_contract import digest
from run_claim_construction_private import Gateway, _model_call
from run_model_routing_qualification_private import terminal_telemetry

SCHEMA = "proofpress/v7-claim-preservation/v1"
ROUTES = {
    "sol": {"model": "openai/gpt-5.6-sol", "provider": "openai", "reasoning": "low"},
    "glm": {"model": "zai/glm-5.3-flash", "provider": "baseten", "reasoning": "high"},
    "qwen": {"model": "alibaba/qwen3.8-27b", "provider": "alibaba", "reasoning": "high"},
}
OUTPUT_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["decisions"],
    "properties": {"decisions": {"type": "array", "maxItems": 8, "items": {
        "type": "object", "additionalProperties": False,
        "required": ["claim_id", "verdict", "supported_statement", "evidence_ids"],
        "properties": {
            "claim_id": {"type": "string", "maxLength": 96},
            "verdict": {"type": "string", "enum": ["keep", "repair", "reject"]},
            "supported_statement": {"type": ["string", "null"], "maxLength": 800},
            "evidence_ids": {"type": "array", "maxItems": 6,
                             "items": {"type": "string", "maxLength": 96}},
        },
    }}},
}


def compile_task(source: dict[str, Any], gateway: Gateway) -> tuple[dict[str, Any], dict[str, Any]]:
    construction = source["construction"]
    evidence = {row["evidence_id"]: row for row in construction.get("evidence", [])}
    claims = construction.get("claims", [])
    batches = [claims[index:index + 8] for index in range(0, len(claims), 8)]
    decisions: dict[str, dict[str, Any]] = {}
    statuses = []
    for batch in batches:
        allowed = {row["id"]: set(row.get("evidence_ids", [])) & set(evidence) for row in batch}
        payload = {"task": source["task"]["prompt"],
                   "requirements": construction.get("requirements", []),
                   "claims": [{key: row.get(key) for key in
                               ("id", "requirement_id", "claim_type", "statement", "evidence_ids")}
                              for row in batch],
                   "evidence_receipts": [{"evidence_id": evidence_id,
                                          "quote": evidence[evidence_id].get("quote", "")[:1600],
                                          "locator": evidence[evidence_id].get("locator")}
                                         for evidence_id in sorted(set().union(*allowed.values()))],
                   "instruction": ("Preserve each candidate's supported factual content. Keep it if every factual "
                                   "part is explicitly supported; repair it by removing only unsupported clauses; "
                                   "reject it only when no material supported factual statement remains. Do not add "
                                   "facts, legal conclusions, requirements, or claims. Return exactly one decision "
                                   "per claim and bind only evidence IDs already bound to that claim.")}
        rows = []; failure: Any = "claim-preservation attempts exhausted"
        for semantic_attempt in range(2):
            attempt_payload = {**payload, "semantic_attempt": semantic_attempt + 1,
                               "validation_reminder": ("Reject decisions require null supported_statement and empty evidence_ids. "
                                                       "Keep or repair decisions require a non-empty supported_statement. "
                                                       "Every returned evidence ID must already be bound to that claim.")}
            result = _model_call(gateway,
                                 "You are a source-bound claim preservation compiler, not an answer generator or admission authority.",
                                 json.dumps(attempt_payload, ensure_ascii=False), 10000, OUTPUT_SCHEMA,
                                 "proofpress_v7_claim_preservation", 2)
            if not result["ok"]:
                failure = result["record"]
                continue
            rows = result["value"].get("decisions", [])
            if {row.get("claim_id") for row in rows} != set(allowed):
                failure = "decision coverage mismatch"
                continue
            valid = True
            for row in rows:
                claim_id = row["claim_id"]
                if not set(row.get("evidence_ids", [])).issubset(allowed[claim_id]):
                    valid = False; break
                if row["verdict"] in {"keep", "repair"} and not str(row.get("supported_statement") or "").strip():
                    valid = False; break
                if row["verdict"] == "reject" and (row.get("supported_statement") is not None
                                                    or row.get("evidence_ids")):
                    valid = False; break
            if valid:
                failure = None
                break
            failure = "invalid claim-preservation binding"
        if failure is not None:
            statuses.append({"status": "inconclusive", "reason": failure})
            continue
        decisions.update({row["claim_id"]: row for row in rows})
        statuses.append({"status": "ok", "claim_count": len(rows)})

    compiled_claims = []
    for claim in claims:
        decision = decisions.get(claim["id"])
        if not decision or decision["verdict"] == "reject":
            continue
        compiled_claims.append({**claim, "statement": decision["supported_statement"],
                                "evidence_ids": decision["evidence_ids"],
                                "preservation_action": decision["verdict"]})
    surviving_by_requirement: dict[str, list[dict[str, Any]]] = {}
    for claim in compiled_claims:
        surviving_by_requirement.setdefault(claim["requirement_id"], []).append(claim)
    rejected_requirements = {claim["requirement_id"] for claim in claims
                             if decisions.get(claim["id"], {}).get("verdict") == "reject"}
    repaired_requirements = {claim["requirement_id"] for claim in compiled_claims
                             if claim.get("preservation_action") == "repair"}
    compiled_requirements = []
    for requirement in construction.get("requirements", []):
        requirement_id = requirement["requirement_id"]
        survivors = surviving_by_requirement.get(requirement_id, [])
        lost_content = requirement_id in rejected_requirements or requirement_id in repaired_requirements
        if not survivors:
            status = "gap"
        elif requirement.get("status") in {"gap", "partial"} or lost_content:
            status = "partial"
        else:
            status = "covered"
        is_open = status in {"gap", "partial"}
        compiled_requirements.append({**requirement, "status": status,
                                      "gap_reason": ("claim_preservation_removed_or_narrowed_content"
                                                     if is_open and lost_content else
                                                     "no_supported_claim_remained" if status == "gap" else
                                                     requirement.get("gap_reason")),
                                      "missing_evidence": ("Additional source-bound evidence is required to close the preserved claim set."
                                                           if is_open else None),
                                      "gap_queries": requirement.get("evidence_search_queries", []) if is_open else []})
    preserved_ids = {row["id"] for row in compiled_claims}
    compiled = {**construction, "requirements": compiled_requirements, "claims": compiled_claims,
                "relations": [row for row in construction.get("relations", [])
                              if row.get("from") in preserved_ids and row.get("to") in preserved_ids],
                "status": "staged-evaluation", "authority": "non-authoritative",
                "model_route": {"source": "pr36-v7-frozen", "compiler": gateway.model,
                                "provider": gateway.provider, "reasoning": gateway.reasoning}}
    output = {"task": source["task"], "decomposition": source.get("decomposition"),
              "construction": compiled}
    status = "ok" if len(decisions) == len(claims) and all(row["status"] == "ok" for row in statuses) else "inconclusive"
    return output, {"status": status, "input_claim_count": len(claims),
                    "preserved_claim_count": len(compiled_claims),
                    "repaired_claim_count": sum(row.get("preservation_action") == "repair" for row in compiled_claims),
                    "rejected_claim_count": len(claims) - len(compiled_claims),
                    "batch_status": statuses}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--v7-report", required=True)
    parser.add_argument("--gateway-server", required=True)
    parser.add_argument("--route", choices=tuple(ROUTES), default="sol")
    parser.add_argument("--out", required=True)
    parser.add_argument("--max-tasks", type=int, default=0)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--timeout", type=float, default=300)
    parser.add_argument("--budget-usd", type=float, default=20)
    args = parser.parse_args()
    report = json.loads(Path(args.v7_report).read_text())
    paths = sorted(Path(report["raw_private_dir"]).glob("*.json"))
    if args.max_tasks:
        paths = paths[:args.max_tasks]
    if not paths:
        raise SystemExit("v7 report contains no private task artifacts")
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw = out / "raw"; raw.mkdir(exist_ok=True); raw.chmod(0o700)
    route = ROUTES[args.route]
    gateways = [Gateway(args.gateway_server, route["model"], route["provider"], out,
                        args.timeout, route["reasoning"], structured_output=True)
                for _ in range(max(1, min(args.workers, len(paths))))]
    results = []
    try:
        def run(index_path: tuple[int, Path]) -> dict[str, Any]:
            index, path = index_path
            source = json.loads(path.read_text())
            value, task_result = compile_task(source, gateways[index % len(gateways)])
            target = raw / path.name
            target.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
            target.chmod(0o600)
            return {"task_id": path.stem, **task_result, "artifact_digest": digest(value)}
        with ThreadPoolExecutor(max_workers=len(gateways)) as pool:
            futures = [pool.submit(run, row) for row in enumerate(paths)]
            for future in as_completed(futures):
                results.append(future.result())
    finally:
        for gateway in gateways:
            gateway.stop()
    telemetry = terminal_telemetry({str(index): gateway for index, gateway in enumerate(gateways)})
    results.sort(key=lambda row: row["task_id"])
    complete = [row for row in results if row["status"] == "ok"]
    output = {"schema_version": SCHEMA,
              "boundary": "V7 claim-preservation candidate; no rubric, gold, or silver input and no admission authority.",
              "source_report_digest": digest(report), "route": route, "tasks": results,
              "denominators": {"tasks": len(results), "completed_tasks": len(complete),
                               "input_claims": sum(row["input_claim_count"] for row in complete),
                               "preserved_claims": sum(row["preserved_claim_count"] for row in complete)},
              "telemetry": {**telemetry, "budget_usd": args.budget_usd},
              "qualification": {"requested": bool(args.max_tasks),
                                "status": "pass" if len(complete) == len(results)
                                and not telemetry["missing_cost_calls"]
                                and telemetry["known_cost_usd"] <= args.budget_usd else "inconclusive"},
              "raw_private_dir": str(raw)}
    (out / "sanitized-report.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"qualification": output["qualification"],
                      "denominators": output["denominators"],
                      "cost_usd": telemetry["known_cost_usd"]}, sort_keys=True))


if __name__ == "__main__":
    main()

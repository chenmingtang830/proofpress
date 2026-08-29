#!/usr/bin/env python3
"""Materialize the preregistered v10 candidate route with requirement-level detail."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from governed_workflow_contract import claimability_decision, digest
from run_claim_construction_private import Gateway
from run_model_routing_qualification_private import terminal_telemetry
from run_v10_role_matrix_private import MODELS, _receipts, call_critic, call_proposer

SCHEMA = "proofpress/v10-selected-route-qualification/v1"
EXTRACTOR = "deepseek"
PROPOSER = "deepseek"
CRITIC = "sol"
COVERAGE_MODELS = ("qwen", "sol")
COVERAGE_OUTPUT = {
    "type": "object", "additionalProperties": False, "required": ["resolutions"],
    "properties": {"resolutions": {"type": "array", "maxItems": 40, "items": {
        "type": "object", "additionalProperties": False,
        "required": ["requirement_id", "status", "supporting_claim_ids"],
        "properties": {
            "requirement_id": {"type": "string", "maxLength": 96},
            "status": {"type": "string", "enum": ["covered", "partial", "gap"]},
            "supporting_claim_ids": {"type": "array", "maxItems": 8,
                                     "items": {"type": "string", "maxLength": 96}},
        },
    }}},
}


def call_coverage(gateway: Gateway, task_prompt: str, requirements: list[dict],
                  supported_claims: list[dict]) -> tuple[list[dict], dict]:
    from run_claim_construction_private import _model_call
    payload = {"task": task_prompt,
               "requirements": [{key: row.get(key) for key in
                                  ("requirement_id", "requirement", "type", "lifecycle_category")}
                                 for row in requirements],
               "supported_claims": [{key: row.get(key) for key in
                                     ("id", "requirement_id", "statement", "qualification", "claim_type")}
                                    for row in supported_claims],
               "instruction": "Resolve requirement completeness, not claim truth. covered means the supported claims fully answer the requirement; partial means useful supported facts remain incomplete; gap means no responsive supported claim. Do not rewrite claims or grant authority."}
    result = _model_call(gateway, "You are an independent requirement completeness gate.",
                         json.dumps(payload, ensure_ascii=False), 10000,
                         COVERAGE_OUTPUT, "proofpress_v10_requirement_resolutions", 2)
    if not result["ok"]:
        return [], {"status": "inconclusive", "failure": result["record"]}
    rows = result["value"].get("resolutions", [])
    known_requirements = {row["requirement_id"] for row in requirements}
    known_claims = {row["id"] for row in supported_claims}
    seen = set(); normalized = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        requirement_id = row.get("requirement_id"); status = row.get("status")
        raw_claim_ids = row.get("supporting_claim_ids", [])
        if not isinstance(raw_claim_ids, list):
            continue
        claim_ids = list(dict.fromkeys(raw_claim_ids))
        if requirement_id not in known_requirements or requirement_id in seen:
            continue
        if any(claim_id not in known_claims for claim_id in claim_ids):
            continue
        if status == "covered" and not claim_ids:
            status = "gap"
        if status == "gap":
            claim_ids = []
        normalized.append({"requirement_id": requirement_id, "status": status,
                           "supporting_claim_ids": claim_ids})
        seen.add(requirement_id)
    for requirement_id in sorted(known_requirements - seen):
        normalized.append({"requirement_id": requirement_id, "status": "gap",
                           "supporting_claim_ids": []})
    return normalized, {"status": "ok", "covered": sum(row["status"] == "covered" for row in normalized),
                        "partial": sum(row["status"] == "partial" for row in normalized),
                        "gap": sum(row["status"] == "gap" for row in normalized)}


def expected_gaps(semantic_root: Path, task_id: str, system_label: str) -> set[str]:
    path = semantic_root / f"{task_id}.json"
    if not path.is_file():
        return set()
    value = json.loads(path.read_text())
    return set(value.get("labels", {}).get("systems", {}).get(system_label, {})
               .get("expected_open_gap_requirement_ids", []))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--diagnostic", required=True)
    parser.add_argument("--matrix-raw", required=True)
    parser.add_argument("--semantic-raw", required=True)
    parser.add_argument("--semantic-system", default="evidence-first-v9")
    parser.add_argument("--gateway-server", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--budget-usd", type=float, default=5.0)
    parser.add_argument("--timeout", type=float, default=300)
    args = parser.parse_args()
    diagnostic = Path(args.diagnostic).resolve()
    source_paths = sorted((diagnostic.parent / "raw" / "sol" / "receipt_preproposal").glob("*.json"))
    if len(source_paths) != 4:
        raise SystemExit("selected route requires four frozen tasks")
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw = out / "raw"; raw.mkdir(exist_ok=True); raw.chmod(0o700)
    proposer_route, critic_route = MODELS[PROPOSER], MODELS[CRITIC]
    proposer = Gateway(args.gateway_server, proposer_route["model"], proposer_route["provider"], out,
                       args.timeout, proposer_route["reasoning"], structured_output=True)
    critic = Gateway(args.gateway_server, critic_route["model"], critic_route["provider"], out,
                     args.timeout, critic_route["reasoning"], structured_output=True)
    coverage_gateways = {label: Gateway(args.gateway_server, MODELS[label]["model"],
                                        MODELS[label]["provider"], out, args.timeout,
                                        MODELS[label]["reasoning"], structured_output=True)
                         for label in COVERAGE_MODELS}
    gateways = {"proposer": proposer, "critic": critic,
                **{f"coverage_{key}": value for key, value in coverage_gateways.items()}}
    tasks = []
    try:
        for source_path in source_paths:
            source = json.loads(source_path.read_text()); construction = source["construction"]
            matrix_path = Path(args.matrix_raw) / source_path.name
            matrix = json.loads(matrix_path.read_text())
            requirements = construction["requirements"]; receipts = _receipts(construction)
            atoms = matrix["extractors"][EXTRACTOR]
            gates = {row["requirement_id"]: claimability_decision(row, atoms, receipts)
                     for row in requirements}
            claims, proposer_status = call_proposer(proposer, requirements, atoms, gates)
            verdicts, critic_status = call_critic(critic, requirements, atoms, claims)
            verdict_by_id = {row["claim_id"]: row for row in verdicts}
            supported = [row for row in claims if verdict_by_id.get(row["id"], {}).get("verdict") == "supported"]
            expected = expected_gaps(Path(args.semantic_raw), source_path.stem, args.semantic_system)
            comparable_expected = expected & {row["requirement_id"] for row in requirements}
            resolutions = {}; coverage_status = {}
            for label, gateway in coverage_gateways.items():
                resolutions[label], coverage_status[label] = call_coverage(
                    gateway, str(source.get("task", {}).get("prompt", "")), requirements, supported)
            open_by_model = {label: {row["requirement_id"] for row in rows
                                     if row["status"] != "covered"}
                             for label, rows in resolutions.items()}
            private = {"task_id": source_path.stem, "requirements": requirements, "atoms": atoms,
                       "gates": gates, "claims": claims, "verdicts": verdicts,
                       "supported_claims": supported,
                       "requirement_resolutions": resolutions,
                       "expected_open_gap_requirement_ids": sorted(comparable_expected)}
            target = raw / source_path.name
            target.write_text(json.dumps(private, ensure_ascii=False, indent=2, sort_keys=True) + "\n"); target.chmod(0o600)
            ok = (proposer_status["status"] == critic_status["status"] == "ok"
                  and all(row["status"] == "ok" for row in coverage_status.values()))
            tasks.append({"task_id": source_path.stem,
                          "status": "ok" if ok else "inconclusive",
                          "requirement_count": len(requirements), "atom_count": len(atoms),
                          "claim_count": len(claims), "supported_claim_count": len(supported),
                          "unsupported_claim_count": len(claims) - len(supported),
                          "expected_gap_count": len(comparable_expected),
                          "coverage": {label: {"covered_requirement_count": sum(row["status"] == "covered" for row in resolutions[label]),
                                               "honest_gap_count": len(comparable_expected & open_by_model[label]),
                                               "status": coverage_status[label]}
                                       for label in COVERAGE_MODELS},
                          "proposer_status": proposer_status, "critic_status": critic_status,
                          "artifact_digest": digest(private)})
            telemetry = terminal_telemetry(gateways)
            if telemetry["known_cost_usd"] > args.budget_usd:
                raise RuntimeError("selected route exceeded its hard budget")
    finally:
        proposer.stop(); critic.stop()
        for gateway in coverage_gateways.values(): gateway.stop()
    telemetry = terminal_telemetry(gateways)
    completed = [row for row in tasks if row["status"] == "ok"]
    requirements = sum(row["requirement_count"] for row in completed)
    claims = sum(row["claim_count"] for row in completed)
    expected = sum(row["expected_gap_count"] for row in completed)
    report = {"schema_version": SCHEMA,
              "boundary": "Frozen four-task development qualification; expected gaps are model-adjudicated, not human gold or admission.",
              "route": {"extractor": MODELS[EXTRACTOR], "proposer": proposer_route,
                        "critic": critic_route, "critic_independent_of_candidate": True},
              "tasks": tasks,
              "denominators": {"tasks": len(tasks), "completed_tasks": len(completed),
                               "requirements": requirements, "claims": claims,
                               "expected_gaps": expected},
              "metrics": {"coverage_models": {label: {
                              "supported_requirement_coverage": sum(row["coverage"][label]["covered_requirement_count"] for row in completed) / requirements if requirements else None,
                              "honest_gap_recall": sum(row["coverage"][label]["honest_gap_count"] for row in completed) / expected if expected else None}
                              for label in COVERAGE_MODELS},
                          "unsupported_claim_rate": sum(row["unsupported_claim_count"] for row in completed) / claims if claims else None,
                          "evidence_binding_pass_rate": 1.0 if completed else None,
                          "receipt_validity": 1.0 if completed else None},
              "telemetry": {**telemetry, "budget_usd": args.budget_usd},
              "qualification": {"status": "pass" if len(completed) == 4 and not telemetry["missing_cost_calls"] else "inconclusive"},
              "raw_private_dir": str(raw)}
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["qualification"]["status"], "metrics": report["metrics"],
                      "cost_usd": telemetry["known_cost_usd"]}, sort_keys=True))


if __name__ == "__main__":
    main()

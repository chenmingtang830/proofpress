#!/usr/bin/env python3
"""Qualify deterministic observed-fact compilation from frozen v10 evidence atoms."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from governed_workflow_contract import digest, validate_compiled_claim
from run_claim_construction_private import Gateway, _model_call
from run_model_routing_qualification_private import terminal_telemetry
from run_v10_construction_qualification_private import score_requirement_opportunities
from run_v10_role_matrix_private import MODELS, call_critic
from run_v10_selected_route_private import COVERAGE_MODELS, call_coverage

SCHEMA = "proofpress/v10-deterministic-compiler-qualification/v1"
MAX_CLAIMS = 64
TYPE_CLASSIFIER_MODELS = {
    "deepseek": MODELS["deepseek"],
    "qwen": MODELS["qwen"],
    "luna": {"model": "openai/gpt-5.6-luna", "provider": "openai", "reasoning": "low"},
}
TYPE_OUTPUT = {"type": "object", "additionalProperties": False, "required": ["assignments"],
               "properties": {"assignments": {"type": "array", "maxItems": MAX_CLAIMS,
                   "items": {"type": "object", "additionalProperties": False,
                       "required": ["claim_id", "claim_type"],
                       "properties": {"claim_id": {"type": "string", "maxLength": 96},
                                      "claim_type": {"type": "string", "enum": [
                                          "observed_fact", "risk_signal", "domain_conclusion", "allocation"]}}}}}}


def compile_claims(atoms: list[dict[str, Any]], gates: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    claims = []
    seen = set()
    for atom in sorted(atoms, key=lambda row: (row["requirement_id"], row["evidence_id"], row["atom_id"])):
        gate = gates.get(atom["requirement_id"], {})
        if not gate.get("proposer_allowed"):
            continue
        bindings = atom["field_bindings"]
        start = min(bindings[field]["start"] for field in ("subject", "predicate", "value"))
        end = max(bindings[field]["end"] for field in ("subject", "predicate", "value"))
        statement = atom["exact_excerpt"][start:end].strip()
        key = (atom["requirement_id"], statement.casefold(), atom.get("qualification"))
        if not statement or key in seen:
            continue
        raw = {
            "requirement_id": atom["requirement_id"], "claim_type": "observed_fact",
            "statement": statement, "atom_ids": [atom["atom_id"]],
            "qualification": atom.get("qualification"), "status": "unresolved",
        }
        raw["id"] = "claim_det_" + digest(raw)[7:23]
        validate_compiled_claim(raw, {atom["atom_id"]: atom}, gate)
        claims.append(raw); seen.add(key)
        if len(claims) == MAX_CLAIMS:
            break
    return claims


def classify_types(gateway: Gateway, requirements: list[dict[str, Any]],
                   claims: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    requirement_by_id = {row["requirement_id"]: row for row in requirements}
    payload = {"claims": [{"claim_id": row["id"], "statement": row["statement"],
                            "qualification": row.get("qualification"),
                            "requirement": requirement_by_id[row["requirement_id"]].get("requirement"),
                            "requirement_type": requirement_by_id[row["requirement_id"]].get("type")}
                           for row in claims],
               "instruction": "Assign only the semantic type of each fixed source-bound proposition. Do not rewrite, infer, answer, or grant authority."}
    result = _model_call(gateway, "Classify fixed evidence-bound propositions by claim type only.",
                         json.dumps(payload, ensure_ascii=False), 6000, TYPE_OUTPUT,
                         "proofpress_v10_type_assignments", 2)
    if not result["ok"]:
        return [], {"status": "inconclusive", "failure": result["record"]}
    rows = result["value"].get("assignments", [])
    assignments = {row.get("claim_id"): row.get("claim_type") for row in rows}
    if len(rows) != len(assignments) or set(assignments) != {row["id"] for row in claims}:
        return [], {"status": "schema_failure", "failure_digest": digest(rows)}
    return [{**row, "claim_type": assignments[row["id"]]} for row in claims], {"status": "ok"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-raw", required=True)
    parser.add_argument("--reference-raw", required=True)
    parser.add_argument("--task-source-raw", required=True)
    parser.add_argument("--gateway-server", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--budget-usd", type=float, default=5.0)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--classifier", choices=["none", *TYPE_CLASSIFIER_MODELS], default="none")
    args = parser.parse_args()
    paths = sorted(Path(args.candidate_raw).glob("*.json"))
    if len(paths) != 4:
        raise SystemExit("deterministic compiler qualification requires four frozen tasks")
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw_out = out / "raw"; raw_out.mkdir(exist_ok=True); raw_out.chmod(0o700)
    routes = {"critic": MODELS["sol"], **{f"coverage_{label}": MODELS[label] for label in COVERAGE_MODELS}}
    if args.classifier != "none":
        routes["classifier"] = TYPE_CLASSIFIER_MODELS[args.classifier]
    gateways = {label: Gateway(args.gateway_server, route["model"], route["provider"], out,
                               args.timeout, route["reasoning"], structured_output=True)
                for label, route in routes.items()}
    tasks = []
    try:
        for path in paths:
            source = json.loads(path.read_text())
            task_source = json.loads((Path(args.task_source_raw) / path.name).read_text())
            reference = json.loads((Path(args.reference_raw) / path.name).read_text())["gap_reference"]
            claims = compile_claims(source["atoms"], source["gates"])
            classifier_status = {"status": "not_run", "classifier": "deterministic-observed-fact"}
            if args.classifier != "none":
                claims, classifier_status = classify_types(gateways["classifier"], source["requirements"], claims)
            verdicts, critic_status = call_critic(gateways["critic"], source["requirements"], source["atoms"], claims)
            verdict_by_id = {row["claim_id"]: row for row in verdicts}
            supported = [row for row in claims if verdict_by_id.get(row["id"], {}).get("verdict") == "supported"]
            resolutions = {}; coverage_status = {}; scores = {}
            for label in COVERAGE_MODELS:
                resolutions[label], coverage_status[label] = call_coverage(
                    gateways[f"coverage_{label}"], task_source["task"]["prompt"],
                    source["requirements"], supported,
                )
                scores[label] = score_requirement_opportunities(
                    reference, resolutions[label], source["atoms"], source["gates"], claims, supported,
                )
            private = {"task_id": source["task_id"], "requirements": source["requirements"],
                       "claims": claims, "verdicts": verdicts, "supported_claims": supported,
                       "requirement_resolutions": resolutions, "reference_digest": digest(reference)}
            target = raw_out / path.name
            target.write_text(json.dumps(private, indent=2, sort_keys=True) + "\n"); target.chmod(0o600)
            statuses = [critic_status, *coverage_status.values()]
            if args.classifier != "none":
                statuses.append(classifier_status)
            tasks.append({"task_id": source["task_id"],
                          "status": "ok" if all(row["status"] == "ok" for row in statuses) else "inconclusive",
                          "claim_count": len(claims), "supported_claim_count": len(supported),
                          "unsupported_claim_count": len(claims) - len(supported),
                          "coverage": scores, "stage_status": {"classifier": classifier_status,
                                                                 "critic": critic_status, "coverage": coverage_status},
                          "artifact_digest": digest(private)})
    finally:
        for gateway in gateways.values(): gateway.stop()
    telemetry = terminal_telemetry(gateways)
    completed = [row for row in tasks if row["status"] == "ok"]
    claims = sum(row["claim_count"] for row in completed)
    expected_gaps = sum(row["coverage"][COVERAGE_MODELS[0]]["expected_gap_count"] for row in completed) if completed else 0
    metrics = {"unsupported_claim_rate": sum(row["unsupported_claim_count"] for row in completed) / claims if claims else None,
               "coverage_models": {}}
    for label in COVERAGE_MODELS:
        expected_covered = sum(row["coverage"][label]["expected_covered_count"] for row in completed)
        true_covered = sum(row["coverage"][label]["true_covered_count"] for row in completed)
        false_covered = sum(row["coverage"][label]["false_covered_count"] for row in completed)
        honest = sum(row["coverage"][label]["honest_gap_count"] for row in completed)
        metrics["coverage_models"][label] = {
            "coverage_precision": true_covered / (true_covered + false_covered) if true_covered + false_covered else None,
            "coverage_recall": true_covered / expected_covered if expected_covered else None,
            "honest_gap_recall": honest / expected_gaps if expected_gaps else None,
            "loss_funnel": {stage: sum(row["coverage"][label]["loss_funnel"][stage] for row in completed)
                            for stage in ("extractor", "claimability", "proposer", "critic", "claim_shape")},
        }
    report = {"schema_version": SCHEMA, "status": "pass" if len(completed) == 4 and not telemetry["missing_cost_calls"] else "inconclusive",
              "boundary": "Four-task development qualification. Deterministic compilation creates unresolved observed-fact candidates only; it has no admission authority.",
              "route": {"compiler": "deterministic-minimum-bound-span/v1",
                        "classifier": args.classifier, **routes},
              "tasks": tasks, "metrics": metrics, "telemetry": {**telemetry, "budget_usd": args.budget_usd},
              "denominators": {"tasks": len(tasks), "completed_tasks": len(completed), "claims": claims,
                               "expected_gaps": expected_gaps}, "raw_private_dir": str(raw_out)}
    if telemetry["known_cost_usd"] > args.budget_usd:
        raise RuntimeError("deterministic compiler qualification exceeded hard budget")
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "metrics": metrics,
                      "cost_usd": telemetry["known_cost_usd"]}, sort_keys=True))


if __name__ == "__main__":
    main()

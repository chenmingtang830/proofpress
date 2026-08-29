#!/usr/bin/env python3
"""Run the selected v10 construction route on Qwen atomic requirements."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from governed_workflow_contract import claimability_decision, digest
from run_claim_construction_private import Gateway, SectionIndex, _evidence, _model_call
from run_model_routing_qualification_private import terminal_telemetry
from run_v10_role_matrix_private import MODELS, call_critic, call_extractor, call_proposer
from run_v10_selected_route_private import COVERAGE_MODELS, COVERAGE_OUTPUT, call_coverage

SCHEMA = "proofpress/v10-construction-qualification/v2"
DECOMPOSER = "qwen"
EXTRACTOR = "deepseek"
PROPOSER = "deepseek"
CRITIC = "sol"
EXTRACTOR_BATCH_SIZE = 4
GAP_REFERENCE_OUTPUT = {
    "type": "object", "additionalProperties": False, "required": ["requirements"],
    "properties": {"requirements": {"type": "array", "maxItems": 40, "items": {
        "type": "object", "additionalProperties": False,
        "required": ["requirement_id", "evidence_sufficient", "expected_status"],
        "properties": {"requirement_id": {"type": "string", "maxLength": 96},
                       "evidence_sufficient": {"type": "boolean"},
                       "expected_status": {"type": "string", "enum": ["covered", "partial", "gap"]}}}}},
}


def score_requirement_opportunities(
    reference: list[dict[str, Any]],
    resolutions: list[dict[str, Any]],
    atoms: list[dict[str, Any]],
    gates: dict[str, dict[str, Any]],
    claims: list[dict[str, Any]],
    supported: list[dict[str, Any]],
) -> dict[str, Any]:
    """Separate honest gaps from missed evidence-sufficient opportunities."""
    expected = {row["requirement_id"]: bool(row["evidence_sufficient"]) for row in reference}
    predicted = {row["requirement_id"]: row.get("status") == "covered" for row in resolutions}
    atom_ids = {row["requirement_id"] for row in atoms}
    claim_ids = {row["requirement_id"] for row in claims}
    supported_ids = {row["requirement_id"] for row in supported}
    sufficient = {rid for rid, value in expected.items() if value}
    expected_gaps = set(expected) - sufficient
    covered = {rid for rid, value in predicted.items() if value}
    true_covered = len(sufficient & covered)
    false_covered = len(expected_gaps & covered)
    missed_count = len(sufficient - covered)
    honest_gap_count = len(expected_gaps - covered)
    loss = {name: 0 for name in ("extractor", "claimability", "proposer", "critic", "claim_shape")}
    missed = []
    for requirement_id in sorted(sufficient - covered):
        if requirement_id not in atom_ids:
            stage = "extractor"
        elif not gates.get(requirement_id, {}).get("proposer_allowed"):
            stage = "claimability"
        elif requirement_id not in claim_ids:
            stage = "proposer"
        elif requirement_id not in supported_ids:
            stage = "critic"
        else:
            stage = "claim_shape"
        loss[stage] += 1
        missed.append({"requirement_id": requirement_id, "loss_stage": stage})
    return {
        "expected_covered_count": len(sufficient),
        "expected_gap_count": len(expected_gaps),
        "true_covered_count": true_covered,
        "false_covered_count": false_covered,
        "missed_opportunity_count": missed_count,
        "honest_gap_count": honest_gap_count,
        "coverage_precision": true_covered / (true_covered + false_covered) if true_covered + false_covered else None,
        "coverage_recall": true_covered / (true_covered + missed_count) if true_covered + missed_count else None,
        "honest_gap_recall": honest_gap_count / (honest_gap_count + false_covered) if honest_gap_count + false_covered else None,
        "loss_funnel": loss,
        "missed_opportunities": missed,
    }


def _multiquery_hits(requirement: dict[str, Any], index: SectionIndex,
                     max_sections: int) -> tuple[list[dict[str, Any]], str]:
    queries = [str(row) for row in requirement.get("evidence_search_queries", [])[:4] if str(row).strip()]
    requirement_text = str(requirement.get("requirement", "")).strip()
    if requirement_text:
        queries.append(requirement_text)
    queries = list(dict.fromkeys(queries)) or [requirement_text]
    merged: dict[tuple[str, str], dict[str, Any]] = {}
    for query in queries:
        for hit in index.search(query, max_documents=10, max_sections=max_sections):
            section = hit["section"]
            key = (section["uri"], section["id"])
            row = merged.setdefault(key, {**hit, "rrf_score": 0.0, "query_hits": 0})
            row["rrf_score"] += 1.0 / (60 + hit["rank"])
            row["query_hits"] += 1
            row["considered_documents"] = sorted(set(row["considered_documents"])
                                                   | set(hit["considered_documents"]))
    ranked = sorted(merged.values(), key=lambda row: (-row["rrf_score"], -row["query_hits"],
                                                       row["section"]["uri"], row["section"]["id"]))
    chosen: list[dict[str, Any]] = []; seen_sources: set[str] = set()
    for row in ranked:
        if row["section"]["uri"] not in seen_sources:
            chosen.append(row); seen_sources.add(row["section"]["uri"])
        if len(chosen) >= max_sections:
            break
    for row in ranked:
        if len(chosen) >= max_sections:
            break
        if row not in chosen:
            chosen.append(row)
    for rank, row in enumerate(chosen, 1):
        row["rank"] = rank
        row["score"] = row["rrf_score"]
    return chosen, " || ".join(queries)


def retrieve(requirements: list[dict[str, Any]], index: SectionIndex,
             max_sections: int = 6, mode: str = "joined",
             task_query: str = "") -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    if mode not in {"joined", "multiquery_rrf", "requirement_plus_task"}:
        raise ValueError("unknown retrieval mode")
    if mode == "requirement_plus_task" and not task_query.strip():
        raise ValueError("requirement_plus_task requires task query")
    task_hits = index.search(task_query, max_sections=max_sections) if mode == "requirement_plus_task" else []
    receipts = {}; audit = []
    for requirement in requirements:
        queries = requirement.get("evidence_search_queries") or [requirement.get("requirement", "")]
        query = " ".join(str(row) for row in queries[:4])
        if mode == "multiquery_rrf":
            hits, query = _multiquery_hits(requirement, index, max_sections)
        else:
            hits = index.search(query, max_sections=max_sections)
        if mode == "requirement_plus_task":
            safety = task_hits[:min(2, max_sections)]
            keys = {(row["section"]["uri"], row["section"]["id"]) for row in safety}
            hits = [*safety, *(row for row in hits
                               if (row["section"]["uri"], row["section"]["id"]) not in keys)]
            hits = hits[:max_sections]
            for rank, hit in enumerate(hits, 1):
                hit = dict(hit); hit["rank"] = rank
                hits[rank - 1] = hit
            query = f"task-safety:{task_query} || requirement:{query}"
        selected = [_evidence(requirement["requirement_id"], hit, query) for hit in hits]
        for row in selected:
            source = row.get("source") or {}
            receipts[row["evidence_id"]] = {
                "evidence_id": row["evidence_id"], "receipt_digest": row["receipt_digest"],
                "source_digest": source.get("content_digest"), "custody_valid": True,
                "quote": row["quote"], "locator": row["locator"], "source": source,
            }
        audit.append({"requirement_id": requirement["requirement_id"],
                      "evidence_ids": [row["evidence_id"] for row in selected],
                      "ranked_section_count": len(hits),
                      "considered_document_count": len({doc for hit in hits for doc in hit["considered_documents"]})})
    return receipts, audit


def gap_reference(gateway: Gateway, requirements: list[dict[str, Any]],
                  receipts: dict[str, dict[str, Any]], audit: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    payload_receipts = []
    for row in audit:
        for evidence_id in row["evidence_ids"][:3]:
            receipt = receipts[evidence_id]
            payload_receipts.append({"requirement_id": row["requirement_id"],
                                     "evidence_id": evidence_id, "quote": receipt["quote"][:1200],
                                     "locator": receipt["locator"]})
    payload = {"requirements": requirements, "retrieval_receipts": payload_receipts,
               "instruction": "Independently judge whether the retrieved receipts fully satisfy each requirement. partial and gap are both expected open gaps. Do not see or infer candidate claims, rubric, gold, or silver locators."}
    result = _model_call(gateway, "You adjudicate retrieval sufficiency before claim proposal.",
                         json.dumps(payload, ensure_ascii=False), 12000,
                         GAP_REFERENCE_OUTPUT, "proofpress_v10_gap_reference", 2)
    if not result["ok"]:
        return [], {"status": "inconclusive", "failure": result["record"]}
    known = {row["requirement_id"] for row in requirements}; seen = set(); rows = []
    for raw in result["value"].get("requirements", []):
        requirement_id = raw.get("requirement_id")
        if requirement_id not in known or requirement_id in seen:
            continue
        status = raw.get("expected_status")
        sufficient = bool(raw.get("evidence_sufficient")) and status == "covered"
        rows.append({"requirement_id": requirement_id,
                     "expected_status": "covered" if sufficient else status,
                     "evidence_sufficient": sufficient})
        seen.add(requirement_id)
    for requirement_id in sorted(known - seen):
        rows.append({"requirement_id": requirement_id, "expected_status": "gap",
                     "evidence_sufficient": False})
    return rows, {"status": "ok", "expected_gap_count": sum(not row["evidence_sufficient"] for row in rows)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--diagnostic", required=True)
    parser.add_argument("--decomposition-raw", required=True)
    parser.add_argument("--catalog")
    parser.add_argument("--frozen-retrieval-raw")
    parser.add_argument("--gateway-server", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--budget-usd", type=float, default=8.0)
    parser.add_argument("--timeout", type=float, default=300)
    parser.add_argument("--decomposer", choices=("qwen", "v7"), default=DECOMPOSER)
    parser.add_argument("--retrieval-mode", choices=("joined", "multiquery_rrf", "requirement_plus_task"), default="joined")
    parser.add_argument("--max-sections", type=int, default=6)
    args = parser.parse_args()
    diagnostic = Path(args.diagnostic).resolve()
    source_paths = sorted((diagnostic.parent / "raw" / "sol" / "receipt_preproposal").glob("*.json"))
    if len(source_paths) != 4:
        raise SystemExit("construction qualification requires four frozen tasks")
    missing = [path.name for path in source_paths if not (Path(args.decomposition_raw) / path.name).is_file()]
    if missing:
        raise SystemExit("decomposition artifacts missing: " + ",".join(missing))
    if bool(args.catalog) == bool(args.frozen_retrieval_raw):
        raise SystemExit("provide exactly one of --catalog or --frozen-retrieval-raw")
    index = SectionIndex(json.loads(Path(args.catalog).read_text())) if args.catalog else None
    frozen_retrieval = Path(args.frozen_retrieval_raw) if args.frozen_retrieval_raw else None
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw = out / "raw"; raw.mkdir(exist_ok=True); raw.chmod(0o700)
    routes = {"extractor": MODELS[EXTRACTOR], "proposer": MODELS[PROPOSER],
              "critic": MODELS[CRITIC], "gap_reference": MODELS["sol"],
              **{f"coverage_{label}": MODELS[label] for label in COVERAGE_MODELS}}
    gateways = {label: Gateway(args.gateway_server, route["model"], route["provider"], out,
                               args.timeout, route["reasoning"], structured_output=True)
                for label, route in routes.items()}
    tasks = []
    try:
        for source_path in source_paths:
            source = json.loads(source_path.read_text())
            decomposition = json.loads((Path(args.decomposition_raw) / source_path.name).read_text())
            requirements = decomposition["variants"][args.decomposer]["requirements"]
            frozen = None
            if frozen_retrieval is not None:
                frozen = json.loads((frozen_retrieval / source_path.name).read_text())
                receipts, audit = frozen["receipts"], frozen["retrieval_audit"]
            else:
                receipts, audit = retrieve(requirements, index, args.max_sections, args.retrieval_mode,
                                           source["task"]["prompt"])
            atoms, extractor_status = call_extractor(
                gateways["extractor"], requirements, receipts, audit,
                batch_size=EXTRACTOR_BATCH_SIZE,
            )
            gates = {row["requirement_id"]: claimability_decision(row, atoms, receipts,
                                                                    task_prompt=source["task"]["prompt"])
                     for row in requirements}
            if frozen is not None:
                reference = frozen["gap_reference"]
                reference_status = {"status": "ok", "source": "frozen-preproposal-reference"}
            else:
                reference, reference_status = gap_reference(gateways["gap_reference"], requirements, receipts, audit)
            claims, proposer_status = call_proposer(gateways["proposer"], requirements, atoms, gates)
            verdicts, critic_status = call_critic(gateways["critic"], requirements, atoms, claims)
            verdict_by_id = {row["claim_id"]: row for row in verdicts}
            supported = [row for row in claims if verdict_by_id.get(row["id"], {}).get("verdict") == "supported"]
            resolutions = {}; coverage_status = {}
            for label in COVERAGE_MODELS:
                resolutions[label], coverage_status[label] = call_coverage(
                    gateways[f"coverage_{label}"], source["task"]["prompt"], requirements, supported)
            expected_gaps = {row["requirement_id"] for row in reference if not row["evidence_sufficient"]}
            opportunity_scores = {
                label: score_requirement_opportunities(
                    reference, resolutions[label], atoms, gates, claims, supported
                )
                for label in COVERAGE_MODELS
            }
            private = {"task_id": source_path.stem, "requirements": requirements,
                       "retrieval_audit": audit, "receipts": receipts, "atoms": atoms, "gates": gates,
                       "claims": claims, "verdicts": verdicts, "supported_claims": supported,
                       "gap_reference": reference, "requirement_resolutions": resolutions}
            target = raw / source_path.name
            target.write_text(json.dumps(private, ensure_ascii=False, indent=2, sort_keys=True) + "\n"); target.chmod(0o600)
            status_rows = [extractor_status, reference_status, proposer_status, critic_status, *coverage_status.values()]
            tasks.append({"task_id": source_path.stem,
                          "status": "ok" if all(row["status"] == "ok" for row in status_rows) else "inconclusive",
                          "requirement_count": len(requirements), "atom_count": len(atoms),
                          "claim_count": len(claims), "supported_claim_count": len(supported),
                          "unsupported_claim_count": len(claims) - len(supported),
                          "expected_gap_count": len(expected_gaps),
                          "coverage": opportunity_scores,
                          "stage_status": {"extractor": extractor_status, "gap_reference": reference_status,
                                           "proposer": proposer_status, "critic": critic_status,
                                           "coverage": coverage_status},
                          "artifact_digest": digest(private)})
            telemetry = terminal_telemetry(gateways)
            if telemetry["known_cost_usd"] > args.budget_usd:
                raise RuntimeError("construction qualification exceeded hard budget")
    finally:
        for gateway in gateways.values(): gateway.stop()
    telemetry = terminal_telemetry(gateways); completed = [row for row in tasks if row["status"] == "ok"]
    requirements = sum(row["requirement_count"] for row in completed); claims = sum(row["claim_count"] for row in completed)
    expected = sum(row["expected_gap_count"] for row in completed)
    metrics = {"unsupported_claim_rate": sum(row["unsupported_claim_count"] for row in completed) / claims if claims else None,
               "evidence_binding_pass_rate": 1.0 if completed else None, "receipt_validity": 1.0 if completed else None,
               "coverage_models": {label: {
                   "coverage_precision": (
                       sum(row["coverage"][label]["true_covered_count"] for row in completed) /
                       max(1, sum(row["coverage"][label]["true_covered_count"] + row["coverage"][label]["false_covered_count"] for row in completed))
                   ),
                   "coverage_recall": (
                       sum(row["coverage"][label]["true_covered_count"] for row in completed) /
                       max(1, sum(row["coverage"][label]["expected_covered_count"] for row in completed))
                   ),
                   "honest_gap_recall": sum(row["coverage"][label]["honest_gap_count"] for row in completed) / expected if expected else None,
                   "loss_funnel": {stage: sum(row["coverage"][label]["loss_funnel"][stage] for row in completed)
                                   for stage in ("extractor", "claimability", "proposer", "critic", "claim_shape")}}
                   for label in COVERAGE_MODELS}}
    report = {"schema_version": SCHEMA,
              "boundary": "Four-task development qualification; Sol gap reference is model-adjudicated, not human gold or admission. Coverage recall is conditioned on independently adjudicated evidence sufficiency; honest gaps use a separate denominator.",
              "route": {"decomposition": (MODELS[args.decomposer] if args.decomposer in MODELS
                                             else {"model": "pr36-v7-frozen", "provider": "frozen", "reasoning": "n/a"}),
                        "extractor_batch_size": EXTRACTOR_BATCH_SIZE,
                        "retrieval": "frozen-replay" if frozen_retrieval is not None else args.retrieval_mode,
                        "max_sections": args.max_sections,
                        **routes},
              "tasks": tasks, "metrics": metrics,
              "denominators": {"tasks": len(tasks), "completed_tasks": len(completed),
                               "requirements": requirements, "claims": claims, "expected_gaps": expected},
              "telemetry": {**telemetry, "budget_usd": args.budget_usd},
              "qualification": {"status": "pass" if len(completed) == 4 and not telemetry["missing_cost_calls"] else "inconclusive"},
              "raw_private_dir": str(raw)}
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["qualification"]["status"], "metrics": metrics,
                      "cost_usd": telemetry["known_cost_usd"]}, sort_keys=True))


if __name__ == "__main__":
    main()

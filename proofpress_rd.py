"""Compile an evolving R&D blueprint into reviewable Proofpress records."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import proofpress_experiment as experiment
import proofpress_knowledge as knowledge
from proofpress_sdk import ProofpressClient


SCHEMA = "proofpress/rd-blueprint/v1"
STATUSES = frozenset({"active", "completed", "aborted", "deferred", "superseded"})
RELATIONS = frozenset({"depends_on", "qualifies", "supersedes"})


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical(value).encode()).hexdigest()


def _key(*parts: str) -> str:
    body = ":".join(parts)
    return "rd:" + hashlib.sha256(body.encode()).hexdigest()


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"R&D blueprint {field} must be a non-empty string")
    return value.strip()


def _texts(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"R&D blueprint {field} must be a non-empty array")
    result = [_text(item, field) for item in value]
    if len(result) != len(set(result)):
        raise ValueError(f"R&D blueprint {field} must not contain duplicates")
    return result


def validate(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict) or raw.get("schema_version") != SCHEMA:
        raise ValueError(f"R&D blueprint schema_version must be {SCHEMA}")
    allowed = {"schema_version", "lineage_id", "scope", "product_objective",
               "source_uri", "phases"}
    unknown = sorted(set(raw) - allowed)
    if unknown:
        raise ValueError("unknown R&D blueprint fields: " + ", ".join(unknown))
    phases = raw.get("phases")
    if not isinstance(phases, list) or not phases:
        raise ValueError("R&D blueprint phases must be a non-empty array")
    normalized = {"schema_version": SCHEMA,
                  "lineage_id": _text(raw.get("lineage_id"), "lineage_id"),
                  "scope": _text(raw.get("scope"), "scope"),
                  "product_objective": _text(raw.get("product_objective"), "product_objective"),
                  "source_uri": _text(raw.get("source_uri"), "source_uri"),
                  "phases": []}
    ids: set[str] = set()
    for index, phase in enumerate(phases):
        if not isinstance(phase, dict):
            raise ValueError("R&D blueprint phase must be an object")
        allowed_phase = {"phase_id", "status", "research_question", "product_connection",
                         "hypothesis", "protocol", "success_criteria", "stop_rules",
                         "observed_outcome", "decision", "next_action", "model_revision",
                         "dataset_revision", "relations", "failure"}
        unknown = sorted(set(phase) - allowed_phase)
        if unknown:
            raise ValueError("unknown R&D blueprint phase fields: " + ", ".join(unknown))
        phase_id = _text(phase.get("phase_id"), f"phases[{index}].phase_id")
        if phase_id in ids:
            raise ValueError("R&D blueprint phase_id must be unique")
        ids.add(phase_id)
        status = phase.get("status")
        if status not in STATUSES:
            raise ValueError("unknown R&D blueprint phase status")
        row = {"phase_id": phase_id, "status": status,
               "research_question": _text(phase.get("research_question"), "research_question"),
               "product_connection": _text(phase.get("product_connection"), "product_connection"),
               "hypothesis": _text(phase.get("hypothesis"), "hypothesis"),
               "protocol": _text(phase.get("protocol"), "protocol"),
               "success_criteria": _texts(phase.get("success_criteria"), "success_criteria"),
               "stop_rules": _texts(phase.get("stop_rules"), "stop_rules"),
               "observed_outcome": _text(phase.get("observed_outcome"), "observed_outcome"),
               "decision": _text(phase.get("decision"), "decision"),
               "next_action": _text(phase.get("next_action"), "next_action"),
               "model_revision": _text(phase.get("model_revision", "not-applicable:lineage"),
                                         "model_revision"),
               "dataset_revision": _text(phase.get("dataset_revision", "not-applicable:lineage"),
                                           "dataset_revision")}
        relations = phase.get("relations", [])
        if not isinstance(relations, list):
            raise ValueError("R&D blueprint relations must be an array")
        row["relations"] = []
        for relation in relations:
            if (not isinstance(relation, dict) or set(relation) != {"type", "target_phase_id"}
                    or relation.get("type") not in RELATIONS):
                raise ValueError("R&D blueprint relation is malformed")
            row["relations"].append({"type": relation["type"],
                                     "target_phase_id": _text(relation["target_phase_id"],
                                                               "target_phase_id")})
        failure = phase.get("failure")
        if status == "aborted":
            if not isinstance(failure, dict):
                raise ValueError("aborted R&D phase requires failure")
            required = {"intervention", "expected_outcome", "feedback",
                        "invalidated_hypotheses", "repeat_policy",
                        "changed_dimension_required"}
            if set(failure) != required:
                raise ValueError("R&D blueprint failure fields do not match the contract")
            row["failure"] = {"intervention": _text(failure["intervention"], "failure.intervention"),
                              "expected_outcome": _text(failure["expected_outcome"], "failure.expected_outcome"),
                              "feedback": _text(failure["feedback"], "failure.feedback"),
                              "invalidated_hypotheses": _texts(failure["invalidated_hypotheses"],
                                                               "failure.invalidated_hypotheses"),
                              "repeat_policy": _text(failure["repeat_policy"], "failure.repeat_policy"),
                              "changed_dimension_required": _text(
                                  failure["changed_dimension_required"],
                                  "failure.changed_dimension_required")}
            if row["failure"]["repeat_policy"] != "retry-if-changed":
                raise ValueError("aborted R&D phase currently requires retry-if-changed")
        elif failure is not None:
            raise ValueError("failure is only valid for an aborted R&D phase")
        normalized["phases"].append(row)
    for phase in normalized["phases"]:
        for relation in phase["relations"]:
            if relation["target_phase_id"] not in ids:
                raise ValueError("R&D blueprint relation target is unknown")
            if relation["target_phase_id"] == phase["phase_id"]:
                raise ValueError("R&D blueprint phase cannot relate to itself")
    return normalized


def compile_plan(raw: Any) -> dict[str, Any]:
    blueprint = validate(raw)
    records = []
    for phase in blueprint["phases"]:
        quote = _canonical({"lineage_id": blueprint["lineage_id"],
                            "product_objective": blueprint["product_objective"],
                            "phase": phase})
        source = {"schema_version": knowledge.RETRIEVAL_EVIDENCE_SCHEMA,
                  "source": {"uri": f'{blueprint["source_uri"]}#{phase["phase_id"]}',
                             "content_digest": "sha256:" + hashlib.sha256(quote.encode()).hexdigest(),
                             "media_type": "application/json"},
                  "evidence": {"quote": quote, "locator": {"kind": "text_span", "start": 0,
                              "end": len(quote), "text_digest": "sha256:" + hashlib.sha256(
                                  quote.encode()).hexdigest()}},
                  "retrieval": {"adapter": "proofpress.rd-blueprint", "version": "1",
                                "query": phase["phase_id"],
                                "config_digest": _digest({"schema": SCHEMA, "phase": phase["phase_id"]})}}
        identity = {"experiment_id": blueprint["lineage_id"], "run_id": phase["phase_id"],
                    "model_revision": phase["model_revision"],
                    "dataset_revision": phase["dataset_revision"],
                    "environment_digest": _digest({"scope": blueprint["scope"],
                                                   "product_connection": phase["product_connection"]}),
                    "config_digest": _digest({"protocol": phase["protocol"],
                                              "success_criteria": phase["success_criteria"],
                                              "stop_rules": phase["stop_rules"]})}
        kind = "failed-attempt" if phase["status"] == "aborted" else "decision"
        qualifier = {"schema_version": experiment.PROFILE, "conclusion_kind": kind,
                     "experiment": identity}
        if kind == "failed-attempt":
            failure = phase["failure"]
            qualifier["failure"] = {
                "intervention": failure["intervention"],
                "expected_outcome": failure["expected_outcome"],
                "observed_outcome": phase["observed_outcome"],
                "feedback_evidence_refs": ["$source_evidence"],
                "invalidated_hypotheses": failure["invalidated_hypotheses"],
                "repeat_policy": failure["repeat_policy"],
                "changed_dimension_required": failure["changed_dimension_required"],
                "next_action": phase["next_action"],
            }
        statement = (f'[{phase["status"]}] {phase["decision"]} '
                     f'Next action: {phase["next_action"]}')
        records.append({"phase_id": phase["phase_id"], "source_evidence": source,
                        "identity": identity, "statement": statement,
                        "qualifier": qualifier, "relations": phase["relations"]})
    return {"schema_version": SCHEMA, "lineage_id": blueprint["lineage_id"],
            "scope": blueprint["scope"], "records": records,
            "plan_digest": _digest(records)}


def sync(client: ProofpressClient, plan: dict[str, Any], proposer: str) -> dict[str, Any]:
    conclusions: dict[str, str] = {}
    evidence: dict[str, str] = {}
    for record in plan["records"]:
        phase_id = record["phase_id"]
        submitted = client.submit_evidence(record["source_evidence"],
                                           idempotency_key=_key(plan["plan_digest"], phase_id, "evidence"))
        evidence_ref = submitted["imported_evidence"][0]
        qualifier = json.loads(json.dumps(record["qualifier"]))
        if qualifier["conclusion_kind"] == "failed-attempt":
            qualifier["failure"]["feedback_evidence_refs"] = [evidence_ref]
        proposed = client.propose_conclusion(
            record["statement"], [evidence_ref], plan["scope"], proposer,
            qualifiers={"experiment": qualifier}, profile="experiment",
            idempotency_key=_key(plan["plan_digest"], phase_id, "conclusion"))
        conclusions[phase_id] = proposed["conclusion"]["id"]
        evidence[phase_id] = evidence_ref
    relations = []
    for record in plan["records"]:
        for relation in record["relations"]:
            proposed = client.propose_relation(
                conclusions[record["phase_id"]], conclusions[relation["target_phase_id"]],
                relation["type"], proposer,
                qualifiers={"rd_blueprint": {"schema_version": SCHEMA,
                                             "lineage_id": plan["lineage_id"]}},
                idempotency_key=_key(plan["plan_digest"], record["phase_id"],
                                     relation["type"], relation["target_phase_id"]))
            relations.append(proposed["relation"]["id"])
    return {"schema_version": SCHEMA, "plan_digest": plan["plan_digest"],
            "scope": plan["scope"], "evidence": evidence,
            "conclusions": conclusions, "relations": relations,
            "automatic_admission": False, "human_approval_required": True}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="proofpress-rd")
    parser.add_argument("blueprint", type=Path)
    parser.add_argument("--base-url")
    parser.add_argument("--token-env", default="PROOFPRESS_MCP_TOKEN")
    parser.add_argument("--proposer", default="agent:rd-blueprint")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    plan = compile_plan(json.loads(args.blueprint.read_text()))
    if not args.execute:
        print(json.dumps({"status": "dry-run", "plan_digest": plan["plan_digest"],
                          "scope": plan["scope"], "record_count": len(plan["records"])},
                         sort_keys=True))
        return
    if not args.base_url:
        raise SystemExit("--execute requires --base-url")
    token = os.environ.get(args.token_env)
    if not token:
        raise SystemExit(f"missing bearer token in {args.token_env}")
    result = sync(ProofpressClient.remote(args.base_url, token), plan, args.proposer)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Minimal verified-knowledge ledger for the long-horizon-agent MVP.

This module deliberately sits above raw telemetry.  It turns a small OTLP-ish
export into a portable, inspectable graph of source events, experiments,
candidate claims, reviews, and admitted knowledge.  It is a deterministic
prototype, not a truth oracle: admission means that the declared evidence and
review policy passed, not that a claim is universally true.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "proofpress/knowledge-ledger/v0"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def _hash(value: Any, prefix: str = "") -> str:
    return prefix + hashlib.sha256(_canonical(value)).hexdigest()[:16]


def _attr_value(value: Any) -> Any:
    if isinstance(value, dict) and "value" in value:
        value = value["value"]
    if isinstance(value, dict) and len(value) == 1:
        key = next(iter(value))
        if key in {"stringValue", "intValue", "doubleValue", "boolValue"}:
            value = value[key]
    if isinstance(value, (int, float, str)):
        return value
    return value


def _attributes(raw: Any) -> dict[str, Any]:
    if isinstance(raw, dict):
        return {str(k): _attr_value(v) for k, v in raw.items()}
    result: dict[str, Any] = {}
    for item in raw or []:
        if isinstance(item, dict) and item.get("key"):
            result[str(item["key"])] = _attr_value(item.get("value"))
    return result


def _spans(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Accept a compact fixture and the common OTLP JSON resourceSpans shape."""
    if isinstance(payload.get("spans"), list):
        return list(payload["spans"])
    found: list[dict[str, Any]] = []
    for resource in payload.get("resourceSpans", []):
        resource_attrs = _attributes(resource.get("resource", {}).get("attributes"))
        for scope in resource.get("scopeSpans", resource.get("instrumentationLibrarySpans", [])):
            for span in scope.get("spans", []):
                copy = dict(span)
                attrs = dict(resource_attrs)
                attrs.update(_attributes(span.get("attributes")))
                copy["attributes"] = attrs
                found.append(copy)
    return found


def _event_id(span: dict[str, Any]) -> str:
    raw = {"trace": span.get("traceId"), "span": span.get("spanId"),
           "name": span.get("name"), "start": span.get("startTimeUnixNano")}
    return _hash(raw, "src_")


def _experiment_id(attrs: dict[str, Any]) -> str | None:
    for key in ("experiment.id", "experiment_id", "experimentId"):
        if attrs.get(key):
            return str(attrs[key])
    return None


def _metric(attrs: dict[str, Any]) -> float | None:
    for key in ("metric.conversion_rate", "conversion_rate", "metric.value"):
        if key in attrs:
            try:
                return float(attrs[key])
            except (TypeError, ValueError):
                return None
    return None


def _source_event(span: dict[str, Any]) -> dict[str, Any]:
    attrs = _attributes(span.get("attributes"))
    events = []
    for event in span.get("events", []) or []:
        events.append({"name": event.get("name"),
                       "attributes": _attributes(event.get("attributes")),
                       "time": event.get("timeUnixNano")})
    record = {
        "id": _event_id(span),
        "kind": "trace",
        "trace_id": span.get("traceId"),
        "span_id": span.get("spanId"),
        "name": span.get("name", "unnamed"),
        "timestamp": span.get("startTimeUnixNano"),
        "status": span.get("status", {}).get("code", span.get("status")),
        "attributes": attrs,
        "events": events,
    }
    record["record_hash"] = _hash(record, "sha256:")
    return record


def _experiments(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for source in sources:
        exp_id = _experiment_id(source["attributes"])
        if exp_id:
            grouped.setdefault(exp_id, []).append(source)
    result = []
    for exp_id, records in sorted(grouped.items()):
        attrs = records[-1]["attributes"]
        metric = next((m for m in (_metric(r["attributes"]) for r in records) if m is not None), None)
        outcome = attrs.get("experiment.outcome", attrs.get("outcome", "unknown"))
        status = "complete" if any(str(r.get("status", "")).lower() in {"ok", "success", "unset", "0"}
                                    for r in records) else "unresolved"
        if any(str(r.get("status", "")).lower() in {"error", "failed", "2"} for r in records):
            status = "failed"
        result.append({
            "id": exp_id,
            "variant": attrs.get("experiment.variant", attrs.get("variant")),
            "metric": {"name": "conversion_rate", "value": metric},
            "outcome": outcome,
            "status": status,
            "source_refs": [r["id"] for r in records],
        })
    return result


def _claims(experiments: list[dict[str, Any]], old: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    old_by_id = {claim["id"]: claim for claim in (old or [])}
    result = []
    for exp in experiments:
        metric = exp["metric"]["value"]
        if metric is None:
            statement = f"Experiment {exp['id']} produced no measured conversion rate."
        else:
            variant = exp.get("variant") or "unknown variant"
            statement = f"Variant {variant} produced a conversion rate of {metric:.4f} in experiment {exp['id']}."
        claim_id = _hash({"experiment": exp["id"], "statement": statement}, "clm_")
        previous = old_by_id.get(claim_id, {})
        result.append({
            "id": claim_id,
            "kind": "candidate_claim",
            "statement": statement,
            "experiment_ref": exp["id"],
            "evidence_refs": exp["source_refs"],
            "support": {"metric": exp["metric"], "experiment_status": exp["status"]},
            "status": previous.get("status", "proposed"),
            "gate": _gate(exp),
            **({"admitted_by": previous["admitted_by"]} if previous.get("admitted_by") else {}),
        })
    return result


def _gate(experiment: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "has_source_evidence": bool(experiment["source_refs"]),
        "experiment_complete": experiment["status"] == "complete",
        "measured_metric": experiment["metric"]["value"] is not None,
        "no_error_status": experiment["status"] != "failed",
    }
    return {"eligible": all(checks.values()), "checks": checks,
            "policy": "mvp-evidence-and-completeness-v0"}


def _ledger_hash(ledger: dict[str, Any]) -> str:
    body = {k: v for k, v in ledger.items() if k not in {"ledger_hash", "updated_at"}}
    return "sha256:" + hashlib.sha256(_canonical(body)).hexdigest()


def _new_ledger() -> dict[str, Any]:
    return {"schema_version": SCHEMA, "ledger_id": _hash(_now(), "ldg_"),
            "created_at": _now(), "updated_at": _now(),
            "source_events": [], "experiments": [], "claims": [],
            "reviews": [], "admissions": [], "ledger_hash": ""}


def _read(path: str | os.PathLike[str]) -> dict[str, Any]:
    with open(path, encoding="utf-8") as handle:
        ledger = json.load(handle)
    if ledger.get("schema_version") != SCHEMA:
        raise ValueError(f"unsupported ledger schema: {ledger.get('schema_version')}")
    return ledger


def _write(path: str | os.PathLike[str], ledger: dict[str, Any]) -> None:
    ledger["updated_at"] = _now()
    ledger["ledger_hash"] = _ledger_hash(ledger)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{target.name}.", dir=str(target.parent), text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(ledger, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(tmp, target)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def ingest(input_path: str, output_path: str, propose: bool = True) -> dict[str, Any]:
    with open(input_path, encoding="utf-8") as handle:
        payload = json.load(handle)
    ledger = _read(output_path) if os.path.exists(output_path) else _new_ledger()
    existing = {event["id"] for event in ledger["source_events"]}
    for span in _spans(payload):
        source = _source_event(span)
        if source["id"] not in existing:
            ledger["source_events"].append(source)
    ledger["experiments"] = _experiments(ledger["source_events"])
    if propose:
        ledger["claims"] = _claims(ledger["experiments"], ledger["claims"])
    _write(output_path, ledger)
    return ledger


def review(path: str, claim_id: str, decision: str, reviewer: str, note: str | None = None) -> dict[str, Any]:
    ledger = _read(path)
    claim = next((c for c in ledger["claims"] if c["id"] == claim_id), None)
    if claim is None:
        raise ValueError(f"claim not found: {claim_id}")
    if decision == "accept" and not claim["gate"]["eligible"]:
        raise ValueError("claim is blocked by the deterministic admission gate")
    status = "admitted" if decision == "accept" else "rejected"
    claim["status"] = status
    claim["admitted_by"] = reviewer if status == "admitted" else None
    review_record = {"id": _hash({"claim": claim_id, "reviewer": reviewer, "time": _now()}, "rev_"),
                     "claim_ref": claim_id, "decision": decision, "reviewer": reviewer,
                     "note": note, "created_at": _now()}
    ledger["reviews"].append(review_record)
    ledger["admissions"].append({"claim_ref": claim_id, "status": status,
                                  "review_ref": review_record["id"],
                                  "evidence_refs": claim["evidence_refs"],
                                  "policy": claim["gate"]["policy"]})
    _write(path, ledger)
    return {"claim": claim, "review": review_record}


def context(path: str) -> dict[str, Any]:
    ledger = _read(path)
    admitted = [claim for claim in ledger["claims"] if claim.get("status") == "admitted"]
    return {"schema_version": "proofpress/agent-context/v0", "ledger_id": ledger["ledger_id"],
            "ledger_hash": ledger["ledger_hash"], "knowledge": admitted,
            "open_claims": [claim["id"] for claim in ledger["claims"]
                            if claim.get("status") in {"proposed", "rejected"}],
            "next_action": "continue from admitted knowledge; review open claims before use"}


def verify(path: str) -> dict[str, Any]:
    ledger = _read(path)
    checks = {
        "ledger_hash": ledger.get("ledger_hash") == _ledger_hash(ledger),
        "claim_evidence_refs": all(ref in {e["id"] for e in ledger["source_events"]}
                                    for claim in ledger["claims"] for ref in claim["evidence_refs"]),
        "admission_review_refs": all(admission["review_ref"] in {r["id"] for r in ledger["reviews"]}
                                     for admission in ledger["admissions"]),
    }
    return {"ok": all(checks.values()), "schema_version": SCHEMA, "ledger_id": ledger["ledger_id"],
            "ledger_hash": ledger["ledger_hash"], "checks": checks}


def add_cli(subparsers: Any) -> None:
    parser = subparsers.add_parser("knowledge", help="ingest traces and govern reusable agent knowledge")
    commands = parser.add_subparsers(dest="knowledge_cmd", required=True)
    ingest_parser = commands.add_parser("ingest", help="ingest OTLP JSON and propose claims")
    ingest_parser.add_argument("input")
    ingest_parser.add_argument("-o", "--output", required=True)
    ingest_parser.add_argument("--no-propose", action="store_true")
    ingest_parser.set_defaults(f=cmd)
    propose_parser = commands.add_parser("propose", help="recompute candidate claims from ingested traces")
    propose_parser.add_argument("ledger")
    propose_parser.set_defaults(f=cmd)
    review_parser = commands.add_parser("review", help="apply a human or policy review decision")
    review_parser.add_argument("ledger")
    review_parser.add_argument("--claim", required=True)
    review_parser.add_argument("--decision", choices=["accept", "reject"], required=True)
    review_parser.add_argument("--reviewer", required=True)
    review_parser.add_argument("--note")
    review_parser.set_defaults(f=cmd)
    for name in ("context", "verify"):
        p = commands.add_parser(name)
        p.add_argument("ledger")
        p.set_defaults(f=cmd)


def cmd(args: argparse.Namespace) -> None:
    if args.knowledge_cmd == "ingest":
        ledger = ingest(args.input, args.output, not args.no_propose)
        print(json.dumps({"ok": True, "ledger": args.output, "source_events": len(ledger["source_events"]),
                          "experiments": len(ledger["experiments"]), "claims": len(ledger["claims"]),
                          "ledger_hash": ledger["ledger_hash"]}, ensure_ascii=False, indent=2))
    elif args.knowledge_cmd == "propose":
        ledger = _read(args.ledger)
        ledger["claims"] = _claims(ledger["experiments"], ledger["claims"])
        _write(args.ledger, ledger)
        print(json.dumps({"ok": True, "claims": ledger["claims"]}, ensure_ascii=False, indent=2))
    elif args.knowledge_cmd == "review":
        print(json.dumps(review(args.ledger, args.claim, args.decision, args.reviewer, args.note),
                          ensure_ascii=False, indent=2))
    elif args.knowledge_cmd == "context":
        print(json.dumps(context(args.ledger), ensure_ascii=False, indent=2))
    elif args.knowledge_cmd == "verify":
        result = verify(args.ledger)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if not result["ok"]:
            raise SystemExit(1)

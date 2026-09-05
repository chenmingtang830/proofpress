#!/usr/bin/env python3
"""File-backed admission ledger: telemetry is input; admitted claims are context."""
from __future__ import annotations

import argparse, hashlib, json, math, os, re, secrets, subprocess, sys, tempfile, threading, webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from contextlib import contextmanager
from contextvars import ContextVar

from proofpress.integrations import repository as proofpress_repo
from proofpress.profiles import experiment as proofpress_experiment
from proofpress.kernel.events import current_event_store

SCHEMA = "proofpress/knowledge-ledger/v1"
ALLOWED = {"service.name","experiment.id","experiment_id","experimentId","experiment.variant","variant","metric.conversion_rate","conversion_rate","metric.value","experiment.outcome","outcome","sample.size","sample_size"}
DEFAULT_POLICY = {"id":"mvp-evidence-and-completeness","version":1,"min_sample_size":1,"require_guardrail_pass":False,"attribute_allowlist_version":"v1"}
TRACE_EVENT_TYPES = {"tool_call", "decision", "annotation", "state_change", "contribution"}
TRACE_SCHEMA_URL = "https://trace-protocol.org/schemas/trace-v0.5.json"
# TRACE wire versions this adapter accepts, each pinned to the upstream release commit that
# carries it and to the SHA-256 of that release's trace-v0.5.json. The digest records which
# schema bytes a version was reviewed against; the adapter validates the bounded fields it
# reads and never fetches, hashes, or applies the schema at import time.
TRACE_SUPPORTED_VERSIONS = {
    "0.5.0": {"commit": "6260cfe7089815763667d8cc869673a40ca570e0",
              "sha256": "sha256:10459fb5e334889b17f9abae36de175490558f300077ba5273d2764f2cb58463"},
    "0.5.1": {"commit": "a97d4e81fb3b4ec5134e992882d28a6cf97fac04",
              "sha256": "sha256:ce7b5bf03b31ab669d12018b0d64fa2421d03b7e7ab2da156f98581e4d62c544"},
}
TRACE_DIGEST_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")

def now(): return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def canon(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
def digest(v): return "sha256:"+hashlib.sha256(canon(v)).hexdigest()
def ident(v,prefix): return prefix+hashlib.sha256(canon(v)).hexdigest()[:16]
def number(d,*keys):
    for key in keys:
        if key in d:
            try: return float(d[key])
            except (TypeError,ValueError): return None
    return None
def val(v):
    if isinstance(v,dict) and "value" in v: v=v["value"]
    if isinstance(v,dict) and len(v)==1:
        key=next(iter(v))
        if key in {"stringValue","intValue","doubleValue","boolValue"}: v=v[key]
    return v if isinstance(v,(str,int,float,bool)) else None
def attrs(raw):
    if isinstance(raw,dict): items=raw.items()
    else: items=((x.get("key"),x.get("value")) for x in (raw or []) if isinstance(x,dict))
    out={str(k):val(v) for k,v in items if k}
    return {k:v for k,v in out.items() if v is not None and (k in ALLOWED or k.startswith("guardrail."))}
def spans(payload):
    if isinstance(payload.get("spans"),list): return list(payload["spans"])
    out=[]
    for resource in payload.get("resourceSpans",[]):
        base=attrs(resource.get("resource",{}).get("attributes"))
        for scope in resource.get("scopeSpans",resource.get("instrumentationLibrarySpans",[])):
            for span in scope.get("spans",[]):
                item=dict(span); item["attributes"]={**base,**attrs(span.get("attributes"))}; out.append(item)
    return out
def source(span):
    record={"id":ident({"trace":span.get("traceId"),"span":span.get("spanId"),"name":span.get("name"),"start":span.get("startTimeUnixNano")},"src_"),"kind":"source_event","trace_id":span.get("traceId"),"span_id":span.get("spanId"),"name":span.get("name","unnamed"),"timestamp":span.get("startTimeUnixNano"),"status":span.get("status",{}).get("code",span.get("status")),"attributes":attrs(span.get("attributes"))}
    record["record_hash"]=digest(record); return record
def trace_actor(actor):
    """Keep stable actor handles without importing arbitrary TRACE payloads."""
    actor = actor or {}
    return {key: actor.get(key) for key in ("type", "id", "role") if actor.get(key) is not None}
def trace_relation(session_id,event_id): return f"trace:{session_id}#{event_id}"
def _trace_number(value, field):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"TRACE decision confidence {field} must be a finite number")
    return value


def _trace_sha256(value, field):
    if not isinstance(value, str) or not TRACE_DIGEST_RE.fullmatch(value):
        raise ValueError(f"TRACE decision confidence {field} must be a sha256 digest")
    return value


def trace_decision_confidence(decision):
    """Project the bounded TRACE v0.5 decision-confidence extension.

    TRACE v0.5 deliberately permits additive decision fields. This adapter only
    preserves the numeric interval, method metadata, sample size, and content
    digests; it does not evaluate the result files or turn the disposition into
    a Proofpress admission decision.
    """
    if "confidence" not in decision or decision["confidence"] is None:
        return None
    raw = decision["confidence"]
    if not isinstance(raw, dict):
        raise ValueError("TRACE decision confidence must be an object")
    interval = raw.get("interval")
    if not isinstance(interval, dict):
        raise ValueError("TRACE decision confidence interval must be an object")
    lower = _trace_number(interval.get("lower"), "interval.lower")
    upper = _trace_number(interval.get("upper"), "interval.upper")
    if lower > upper:
        raise ValueError("TRACE decision confidence interval.lower must not exceed interval.upper")
    projected_interval = {"lower": lower, "upper": upper}
    if "level" in interval:
        level = _trace_number(interval["level"], "interval.level")
        if not 0 < level < 1:
            raise ValueError("TRACE decision confidence interval.level must be between 0 and 1")
        projected_interval["level"] = level
    method = raw.get("method")
    if not isinstance(method, dict) or not isinstance(method.get("name"), str) or not method["name"].strip():
        raise ValueError("TRACE decision confidence method.name must be a non-empty string")
    projected_method = {"name": method["name"]}
    if "resamples" in method:
        resamples = method["resamples"]
        if isinstance(resamples, bool) or not isinstance(resamples, int) or resamples < 1:
            raise ValueError("TRACE decision confidence method.resamples must be a positive integer")
        projected_method["resamples"] = resamples
    sample_size = raw.get("sample_size")
    if isinstance(sample_size, bool) or not isinstance(sample_size, int) or sample_size < 1:
        raise ValueError("TRACE decision confidence sample_size must be a positive integer")
    evidence_digests = raw.get("evidence_digests")
    if not isinstance(evidence_digests, dict) or not evidence_digests:
        raise ValueError("TRACE decision confidence evidence_digests must be a non-empty object")
    projected_digests = {}
    for label, value in evidence_digests.items():
        if not isinstance(label, str) or not label:
            raise ValueError("TRACE decision confidence evidence_digests keys must be non-empty strings")
        projected_digests[label] = _trace_sha256(value, f"evidence_digests.{label}")
    return {"interval": projected_interval, "method": projected_method,
            "sample_size": sample_size, "evidence_digests": projected_digests}


def trace_payload(event):
    """Project reviewable TRACE decision provenance, excluding raw tool I/O."""
    kind=event["type"]
    if kind=="tool_call":
        row=event.get("tool_call") or {}
        meta={key:row.get(key) for key in ("server","name","status","duration_ms","host","output_hash","output_truncated") if row.get(key) is not None}
        return meta | {key:trace_relation(event["session_id"],row[key]) for key in ("retries_event_id","parent_event_id") if row.get(key)}
    if kind=="decision":
        row=event.get("decision") or {}
        projected = {"description":row.get("description"),"rationale":row.get("rationale"),"disposition":row.get("disposition"),"suggestion_type":row.get("suggestion_type"),"proposed_by":trace_actor(row.get("proposed_by")),"resolved_by":trace_actor(row.get("resolved_by")),"revision_note":row.get("revision_note"),"revises":trace_relation(event["session_id"],row["revises_event_id"]) if row.get("revises_event_id") else None,"tags":row.get("tags") or [],"warnings":row.get("warnings") or []}
        if confidence := trace_decision_confidence(row):
            projected["confidence"] = confidence
        return projected
    if kind=="annotation":
        row=event.get("annotation") or {}
        return {"category":row.get("category"),"content":row.get("content"),"corrects":[trace_relation(event["session_id"],x) if ":" not in x else x for x in row.get("corrects_event_ids") or []],"related":[trace_relation(event["session_id"],x) for x in row.get("related_event_ids") or []],"tags":row.get("tags") or []}
    if kind=="contribution":
        row=event.get("contribution") or {}
        meta={key:row.get(key) for key in ("description","artifact","direction","execution") if row.get(key) is not None}
        return meta | {"related_decisions":[trace_relation(event["session_id"],x) for x in row.get("related_decision_ids") or []],"tags":row.get("tags") or []}
    row=event.get("state_change") or {}
    return {key:row.get(key) for key in ("description","field") if row.get(key) is not None}
def trace_source(session,event):
    if event.get("session_id") != session.get("id"): raise ValueError("TRACE event session_id does not match session id")
    if event.get("type") not in TRACE_EVENT_TYPES: raise ValueError("unsupported TRACE event type: "+str(event.get("type")))
    session_id=str(session["id"]); event_id=str(event.get("id") or "")
    if not event_id: raise ValueError("TRACE event has no id")
    metadata=session.get("metadata") or {}
    record={"id":ident({"protocol":"TRACE","session":session_id,"event":event_id},"src_"),"kind":"source_event","source_protocol":"TRACE","source_schema":session.get("trace_version"),"source_ref":trace_relation(session_id,event_id),"trace_id":session_id,"span_id":event_id,"name":"trace."+event["type"],"timestamp":event.get("timestamp"),"status":((event.get("tool_call") or {}).get("status") if event["type"]=="tool_call" else None),"attributes":{"project":metadata.get("project"),"project_key":metadata.get("project_key"),"event_type":event["type"],"actor":trace_actor(event.get("actor")),"event":trace_payload(event)}}
    record["record_hash"]=digest(record); return record
def evidence(src):
    item={"id":ident({"source":src["id"],"hash":src["record_hash"]},"evd_"),"kind":"evidence","source_ref":src["id"],"source_digest":src["record_hash"],"observation":{"name":src["name"],"timestamp":src["timestamp"],"status":src["status"],"attributes":src["attributes"]}}
    item["digest"]=digest(item); return item
def policy(raw=None):
    item={**DEFAULT_POLICY,**(raw or {})}; item.pop("digest",None); item["digest"]=digest(item); return item
def ledger_hash(ledger): return digest({k:v for k,v in ledger.items() if k not in {"ledger_hash","updated_at"}})
def new_ledger():
    item={"schema_version":SCHEMA,"ledger_id":ident(now(),"ldg_"),"created_at":now(),"updated_at":now(),"active_policy":policy(),"source_events":[],"evidence":[],"experiments":[],"claims":[],"reviews":[],"admissions":[],"supersessions":[],"ledger_hash":""}
    item["ledger_hash"]=ledger_hash(item); return item
def read(path):
    with open(path,encoding="utf-8") as h: item=json.load(h)
    if item.get("schema_version")!=SCHEMA: raise ValueError("unsupported ledger schema: "+str(item.get("schema_version")))
    return item
def load(path):
    p=Path(path); return new_ledger() if not p.exists() or p.stat().st_size==0 else read(path)
def write(path,item):
    item["updated_at"]=now(); item["ledger_hash"]=ledger_hash(item); target=Path(path); target.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix="."+target.name+".",dir=str(target.parent),text=True)
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as h: json.dump(item,h,ensure_ascii=False,indent=2); h.write("\n")
        os.replace(tmp,target)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
def experiment_id(a): return next((str(a[k]) for k in ("experiment.id","experiment_id","experimentId") if a.get(k)),None)
def experiments(sources,evidence_rows):
    ev={x["source_ref"]:x["id"] for x in evidence_rows}; groups={}
    for row in sources:
        if eid:=experiment_id(row["attributes"]): groups.setdefault(eid,[]).append(row)
    out=[]
    for eid,rows in sorted(groups.items()):
        a=rows[-1]["attributes"]; statuses={str(x.get("status","")).lower() for x in rows}
        status="failed" if statuses & {"error","failed","2"} else "complete" if statuses & {"ok","success","unset","0"} else "unresolved"
        metric=next((number(x["attributes"],"metric.conversion_rate","conversion_rate","metric.value") for x in rows if number(x["attributes"],"metric.conversion_rate","conversion_rate","metric.value") is not None),None)
        sample=next((number(x["attributes"],"sample.size","sample_size") for x in rows if number(x["attributes"],"sample.size","sample_size") is not None),None)
        out.append({"id":eid,"kind":"experiment","variant":a.get("experiment.variant",a.get("variant")),"metric":{"name":"conversion_rate","value":metric},"sample_size":sample,"outcome":a.get("experiment.outcome",a.get("outcome","unknown")),"status":status,"source_refs":[x["id"] for x in rows],"evidence_refs":[ev[x["id"]] for x in rows],"guardrails":{k:v for k,v in a.items() if k.startswith("guardrail.")}})
    return out
def gate(exp,p):
    guards=list(exp["guardrails"].values())
    checks={"has_evidence":bool(exp["evidence_refs"]),"experiment_complete":exp["status"]=="complete","measured_metric":exp["metric"]["value"] is not None,"sample_size_floor":(exp["sample_size"] or 0)>=p["min_sample_size"],"guardrails_pass":not p["require_guardrail_pass"] or (bool(guards) and all(x is True for x in guards)),"no_error_status":exp["status"]!="failed"}
    return {"eligible":all(checks.values()),"checks":checks,"policy_id":p["id"],"policy_digest":p["digest"]}
def add_claims(item,scope,proposer,expires):
    old={x["id"] for x in item["claims"]}
    for exp in item["experiments"]:
        metric=exp["metric"]["value"]; text=(f"Variant {exp.get('variant') or 'unknown variant'} produced a conversion rate of {metric:.4f} in experiment {exp['id']}." if metric is not None else f"Experiment {exp['id']} produced no measured conversion rate.")
        cid=ident({"experiment":exp["id"],"statement":text,"scope":scope,"evidence":exp["evidence_refs"]},"clm_")
        if cid in old: continue
        item["claims"].append({"id":cid,"kind":"claim","statement":text,"scope":scope,"proposer":proposer,"created_at":now(),"expires_at":expires,"experiment_ref":exp["id"],"evidence_refs":exp["evidence_refs"],"qualifiers":{"metric":exp["metric"],"sample_size":exp["sample_size"],"experiment_status":exp["status"],"guardrails":exp["guardrails"]},"gate":gate(exp,item["active_policy"]),"policy_snapshot":item["active_policy"]})
def ingest(input_path,output,propose=True,scope="default",proposer="agent:proposer",expires=None):
    with open(input_path,encoding="utf-8") as h: payload=json.load(h)
    item=load(output); existing={x["id"]:x for x in item["source_events"]}
    for span in spans(payload):
        row=source(span)
        if row["id"] in existing and existing[row["id"]]["record_hash"]!=row["record_hash"]: raise ValueError("source event conflict for "+row["id"])
        if row["id"] not in existing: item["source_events"].append(row)
    ev={x["id"] for x in item["evidence"]}
    for row in item["source_events"]:
        e=evidence(row)
        if e["id"] not in ev: item["evidence"].append(e)
    item["experiments"]=experiments(item["source_events"],item["evidence"])
    if propose: add_claims(item,scope,proposer,expires)
    write(output,item); return item
def claim(item,cid):
    found=next((x for x in item["claims"] if x["id"]==cid),None)
    if not found: raise ValueError("claim not found: "+cid)
    return found
def superseded(item,cid): return next((x["superseded_by"] for x in reversed(item["supersessions"]) if x["claim_ref"]==cid),None)
def state(item,row):
    if superseded(item,row["id"]): return "superseded"
    if row.get("expires_at") and row["expires_at"]<=now(): return "expired"
    events=[x for x in item["admissions"] if x["claim_ref"]==row["id"]]
    if not events: return "proposed"
    if events[-1]["policy_digest"]!=item["active_policy"]["digest"]: return "unresolved"
    return {"accept":"admitted","reject":"rejected","unresolved":"unresolved"}[events[-1]["decision"]]
def policy_review(path,cid,reviewer):
    item=read(path); row=claim(item,cid); g=row["gate"]; recommendation="accept" if g["eligible"] else ("reject" if not g["checks"]["no_error_status"] else "unresolved")
    review={"id":ident({"claim":cid,"reviewer":reviewer,"time":now()},"rev_"),"kind":"policy_recommendation","claim_ref":cid,"reviewer":reviewer,"identity_basis":"self_asserted","recommendation":recommendation,"rationale":"deterministic gate passed" if g["eligible"] else "deterministic gate did not pass","policy_digest":row["policy_snapshot"]["digest"],"created_at":now()}
    item["reviews"].append(review); write(path,item); return review
def review(path,cid,decision,reviewer,note=None):
    item=read(path); row=claim(item,cid)
    if decision=="accept" and not row["gate"]["eligible"]: raise ValueError("claim is blocked by the deterministic admission gate")
    if decision=="accept" and reviewer==row["proposer"]: raise ValueError("proposer may not self-approve a claim")
    r={"id":ident({"claim":cid,"reviewer":reviewer,"decision":decision,"time":now()},"rev_"),"kind":"human_review","claim_ref":cid,"decision":decision,"reviewer":reviewer,"identity_basis":"self_asserted","note":note,"created_at":now()}
    a={"id":ident({"review":r["id"],"claim":cid},"adm_"),"kind":"admission","claim_ref":cid,"decision":decision,"review_ref":r["id"],"evidence_refs":row["evidence_refs"],"policy_digest":row["policy_snapshot"]["digest"],"created_at":now()}
    item["reviews"].append(r); item["admissions"].append(a); write(path,item); return {"claim":row,"review":r,"admission":a}
def supersede(path,cid,by,reviewer,note=None):
    item=read(path); old,new=claim(item,cid),claim(item,by)
    if old["scope"]!=new["scope"]: raise ValueError("claims from different scopes cannot supersede each other")
    event={"id":ident({"claim":cid,"by":by,"time":now()},"sup_"),"kind":"supersession","claim_ref":cid,"superseded_by":by,"reviewer":reviewer,"identity_basis":"self_asserted","note":note,"created_at":now()}
    item["supersessions"].append(event); write(path,item); return event
def set_policy(path,min_sample_size,require_guardrail_pass=False):
    item=read(path); previous=item["active_policy"]
    item["active_policy"]=policy({**previous,"version":int(previous["version"])+1,"min_sample_size":min_sample_size,"require_guardrail_pass":require_guardrail_pass})
    write(path,item); return item["active_policy"]
def context(path,scope=None):
    item=read(path); rows=[x for x in item["claims"] if scope is None or x["scope"]==scope]; states={x["id"]:state(item,x) for x in rows}
    return {"schema_version":"proofpress/agent-context/v1","ledger_id":item["ledger_id"],"ledger_hash":item["ledger_hash"],"scope":scope,"policy":item["active_policy"],"knowledge":[x for x in rows if states[x["id"]]=="admitted"],"open_claims":[x["id"] for x in rows if states[x["id"]] in {"proposed","unresolved"}],"next_action":"continue from admitted knowledge; inspect provenance handles before relying on open claims"}
def view(path,scope=None):
    item=read(path); rows=[x for x in item["claims"] if scope is None or x["scope"]==scope]; cids={x["id"] for x in rows}; eids={r for x in rows for r in x["evidence_refs"]}; evid=[x for x in item["evidence"] if x["id"] in eids]; sids={x["source_ref"] for x in evid}; exids={x["experiment_ref"] for x in rows}
    nodes=[{**x,"node_type":"source_event"} for x in item["source_events"] if x["id"] in sids]+[{**x,"node_type":"evidence"} for x in evid]+[{**x,"node_type":"experiment"} for x in item["experiments"] if x["id"] in exids]+[{**x,"node_type":"claim","current_state":state(item,x)} for x in rows]+[{**x,"node_type":"admission"} for x in item["admissions"] if x["claim_ref"] in cids]
    edges=[{"type":"derived_from","from":x["id"],"to":x["source_ref"]} for x in evid]
    for x in rows: edges += [{"type":"supports","from":r,"to":x["id"]} for r in x["evidence_refs"]]
    for x in item["admissions"]:
        if x["claim_ref"] in cids: edges.append({"type":"admitted_by","from":x["claim_ref"],"to":x["id"]})
    return {"schema_version":"proofpress/ledger-view/v1","ledger_id":item["ledger_id"],"ledger_hash":item["ledger_hash"],"scope":scope,"nodes":nodes,"edges":edges}
def materialize(path,output,scope=None):
    projection=context(path,scope); lines=["# Governed knowledge","",f"Ledger: `{projection['ledger_id']}`",f"Digest: `{projection['ledger_hash']}`",""]
    for row in projection["knowledge"]: lines += [f"## {row['statement']}","",f"- Claim: `{row['id']}`",f"- Scope: `{row['scope']}`",f"- Evidence: {', '.join('`'+x+'`' for x in row['evidence_refs'])}",""]
    if not projection["knowledge"]: lines += ["No admitted knowledge for this scope.",""]
    Path(output).write_text("\n".join(lines),encoding="utf-8"); return {"ok":True,"output":output,"knowledge_count":len(projection["knowledge"]),"ledger_hash":projection["ledger_hash"]}
def verify(path):
    item=read(path); sources={x["id"]:x for x in item["source_events"]}; evid={x["id"]:x for x in item["evidence"]}; claims={x["id"]:x for x in item["claims"]}; reviews={x["id"]:x for x in item["reviews"]}
    checks={"ledger_hash":item["ledger_hash"]==ledger_hash(item),"source_records":all(x["record_hash"]==digest({k:v for k,v in x.items() if k!="record_hash"}) for x in sources.values()),"evidence_digests":all(x["source_ref"] in sources and x["source_digest"]==sources[x["source_ref"]]["record_hash"] and x["digest"]==digest({k:v for k,v in x.items() if k!="digest"}) for x in evid.values()),"claim_evidence_refs":all(r in evid for x in claims.values() for r in x["evidence_refs"]),"admission_review_refs":all(x["review_ref"] in reviews and x["claim_ref"] in claims for x in item["admissions"]),"policy_snapshot_integrity":all(x["policy_snapshot"]["digest"]==policy(x["policy_snapshot"])["digest"] for x in claims.values()),"no_self_approval":all(x["decision"]!="accept" or reviews[x["review_ref"]]["reviewer"]!=claims[x["claim_ref"]]["proposer"] for x in item["admissions"]),"admitted_gate":all(x["decision"]!="accept" or claims[x["claim_ref"]]["gate"]["eligible"] for x in item["admissions"])}
    return {"ok":all(checks.values()),"schema_version":SCHEMA,"ledger_id":item["ledger_id"],"ledger_hash":item["ledger_hash"],"checks":checks}
def add_cli(sub):
    parser=sub.add_parser("knowledge",help="ingest telemetry and govern reusable agent knowledge"); commands=parser.add_subparsers(dest="knowledge_cmd",required=True)
    def command(name,*args):
        p=commands.add_parser(name)
        for args_,kwargs in args: p.add_argument(*args_,**kwargs)
        p.set_defaults(f=cmd); return p
    common=[(("ledger",),{})]
    command("ingest",(("input",),{}),(("-o","--output"),{"required":True}),(("--no-propose",),{"action":"store_true"}),(("--scope",),{"default":"default"}),(("--proposer",),{"default":"agent:proposer"}),(("--expires-at",),{}))
    command("propose",*common,(("--scope",),{"default":"default"}),(("--proposer",),{"default":"agent:proposer"}),(("--expires-at",),{}))
    command("policy-review",*common,(("--claim",),{"required":True}),(("--reviewer",),{"default":"agent:policy-reviewer"}))
    command("review",*common,(("--claim",),{"required":True}),(("--decision",),{"choices":["accept","reject","unresolved"],"required":True}),(("--reviewer",),{"required":True}),(("--note",),{}))
    command("supersede",*common,(("--claim",),{"required":True}),(("--by",),{"required":True}),(("--reviewer",),{"required":True}),(("--note",),{}))
    command("policy-set",*common,(("--min-sample-size",),{"type":int,"required":True}),(("--require-guardrail-pass",),{"action":"store_true"}))
    for name in ("context","view","verify"): command(name,*common, *(((("--scope",),{}),) if name!="verify" else ()))
    command("materialize",*common,(("-o","--output"),{"required":True}),(("--scope",),{}))
def cmd(a):
    if a.knowledge_cmd=="ingest": item=ingest(a.input,a.output,not a.no_propose,a.scope,a.proposer,a.expires_at); out={"ok":True,"ledger":a.output,"source_events":len(item["source_events"]),"evidence":len(item["evidence"]),"experiments":len(item["experiments"]),"claims":len(item["claims"]),"ledger_hash":item["ledger_hash"]}
    elif a.knowledge_cmd=="propose": item=read(a.ledger); add_claims(item,a.scope,a.proposer,a.expires_at); write(a.ledger,item); out={"ok":True,"claims":item["claims"]}
    elif a.knowledge_cmd=="policy-review": out=policy_review(a.ledger,a.claim,a.reviewer)
    elif a.knowledge_cmd=="review": out=review(a.ledger,a.claim,a.decision,a.reviewer,a.note)
    elif a.knowledge_cmd=="supersede": out=supersede(a.ledger,a.claim,a.by,a.reviewer,a.note)
    elif a.knowledge_cmd=="policy-set": out=set_policy(a.ledger,a.min_sample_size,a.require_guardrail_pass)
    elif a.knowledge_cmd=="context": out=context(a.ledger,a.scope)
    elif a.knowledge_cmd=="view": out=view(a.ledger,a.scope)
    elif a.knowledge_cmd=="materialize": out=materialize(a.ledger,a.output,a.scope)
    else: out=verify(a.ledger)
    print(json.dumps(out,ensure_ascii=False,indent=2))
    if a.knowledge_cmd=="verify" and not out["ok"]: raise SystemExit(1)


# ---------------------------------------------------------------------------
# Local MVP v2: append-only knowledge events on a dedicated Git ref.
# The file-backed v1 functions above remain readable for one alpha migration
# window and for the published 0.4 compatibility command group.

KNOWLEDGE_REF = "refs/proofpress/knowledge"
EVENT_SCHEMA = "proofpress/knowledge-event/v2"
CONTEXT_SCHEMA = "proofpress/agent-context/v2"
LOCAL_OPERATION_SCHEMA = "proofpress/local-operation/v1alpha1"
LOCAL_OPERATION_RESULT_SCHEMA = "proofpress/local-operation-result/v1alpha1"
LOCAL_OPERATION_CONTRACT_STATUS = "internal_alpha"
LOCAL_IDEMPOTENCY_PATH = ".proofpress/runtime/idempotency.json"
LOCAL_OPERATION_SPECS = {
    "capabilities.get": {
        "required": (), "optional": (), "mutates": False,
        "replay_semantics": "read_only",
    },
    "configuration.get": {
        "required": (), "optional": (), "mutates": False,
        "replay_semantics": "read_only",
    },
    "evidence.import": {
        "required": ("path",), "optional": (), "mutates": True,
        "replay_semantics": "kernel_deduplicated",
    },
    "evidence.submit": {
        "required": ("payload",), "optional": ("profile",), "mutates": True,
        "replay_semantics": "kernel_deduplicated",
    },
    "conclusion.propose": {
        "required": ("statement", "evidence_refs", "proposer"),
        "optional": ("expires_at", "artifact_refs", "scope", "applicability",
                     "reproposal_of", "qualifiers", "profile"),
        "mutates": True, "replay_semantics": "kernel_deduplicated",
    },
    "conclusion.evaluate": {
        "required": ("conclusion_id",), "optional": ("actor",), "mutates": True,
        "replay_semantics": "kernel_deduplicated",
    },
    "conclusion.judge": {
        "required": ("conclusion_id",), "optional": ("actor",), "mutates": True,
        "replay_semantics": "kernel_deduplicated",
    },
    "conclusion.judge_batch": {
        "required": ("scope",), "optional": ("actor",), "mutates": True,
        "replay_semantics": "kernel_deduplicated",
    },
    "conclusion.review": {
        "required": ("conclusion_id", "decision", "reviewer"),
        "optional": ("note", "request_id", "expected_head"),
        "mutates": True, "replay_semantics": "parameter_request_id",
    },
    "conclusion.supersede": {
        "required": ("conclusion_id", "replacement_id", "reviewer"),
        "optional": ("note",), "mutates": True,
        "replay_semantics": "kernel_deduplicated",
    },
    "relation.propose": {
        "required": ("source_id", "target_id", "relation_type", "proposer"),
        "optional": ("confidence", "qualifiers", "actor"), "mutates": True,
        "replay_semantics": "kernel_deduplicated",
    },
    "relation.evaluate": {
        "required": ("relation_id",), "optional": ("actor",), "mutates": True,
        "replay_semantics": "kernel_deduplicated",
    },
    "relation.judge": {
        "required": ("relation_id",), "optional": ("actor",), "mutates": True,
        "replay_semantics": "kernel_deduplicated",
    },
    "relation.review": {
        "required": ("relation_id", "decision", "reviewer"),
        "optional": ("note", "request_id", "expected_head"),
        "mutates": True, "replay_semantics": "parameter_request_id",
    },
    "relation.resolve": {
        "required": ("relation_id", "disposition", "reviewer"),
        "optional": ("winner", "note", "expected_head"),
        "mutates": True, "replay_semantics": "kernel_deduplicated",
    },
    "graph.get": {
        "required": (), "optional": ("scope", "actor"), "mutates": False,
        "replay_semantics": "read_only",
    },
    "graph.traverse": {
        "required": ("seed_ids",),
        "optional": ("scope", "actor", "task", "max_depth", "max_claims",
                     "state"),
        "mutates": False, "replay_semantics": "read_only",
    },
    "context.get": {
        "required": (),
        "optional": ("scope", "actor", "task", "include_blocked_statements"),
        "mutates": False, "replay_semantics": "read_only",
    },
    "context.discover": {
        "required": (), "optional": ("actor", "task", "limit"),
        "mutates": False, "replay_semantics": "read_only",
    },
    "review.summary": {
        "required": (), "optional": ("scope", "actor"), "mutates": False,
        "replay_semantics": "read_only",
    },
    "review.receipt": {
        "required": ("conclusion_id",), "optional": ("actor",), "mutates": False,
        "replay_semantics": "read_only",
    },
}
TRAVERSAL_SCHEMA = "proofpress/graph-traversal/v1"
RETRIEVAL_EVIDENCE_SCHEMA = "proofpress/retrieval-evidence/v1"
DISCLOSURE_SCHEMA = "proofpress/governed-disclosure/v1"
ASSIMILATION_SCHEMA = "proofpress/assimilation-recommendation/v1"
PAGEINDEX_SIDECAR_SCHEMA = "proofpress/pageindex-sidecar/v1"
POLICY_PATH = ".proofpress/policy.json"
DEFAULT_POLICY_V2 = {
    "id": "proofpress-local-default",
    "version": 1,
    "min_evidence": 1,
    "require_judge": False,
    "allowed_actors": ["*"],
    "conflict_resolvers": ["*"],
    "verification": {
        "identity": "verifier:local-deterministic",
        "profile": "proofpress/default-verification/v1",
    },
    "judge": {
        "identity": "judge:local-advisory",
        "command": [],
        "timeout_seconds": 30,
    },
}
RELATION_TYPES = {"supports", "qualifies", "contradicts", "supersedes",
                  "depends_on", "same_as"}
SYMMETRIC_RELATIONS = {"contradicts", "same_as"}
LEGAL_PROFILE_SCHEMA = "proofpress/profile/legal/v1"


def _git(*args, input=None):
    result = subprocess.run(["git", *args], input=input, text=True,
                            capture_output=True)
    if result.returncode:
        raise ValueError("git " + " ".join(args) + ": " + result.stderr.strip())
    return result.stdout


def _event_payload(event):
    return {k: v for k, v in event.items() if k not in {"event_id", "commit"}}


def _event_id(event):
    return ident(_event_payload(event), "ppe_")


def v2_events():
    return current_event_store().list_events()


def append_v2(event, existing_rows=None):
    event = {"schema_version": EVENT_SCHEMA, **event}
    existing_rows = v2_events() if existing_rows is None else existing_rows
    immutable = {"source_recorded": "record", "evidence_bound": "evidence",
                 "conclusion_proposed": "conclusion", "relation_proposed": "relation"}
    if event.get("type") in immutable:
        prior = next((row for row in existing_rows
                      if row.get("type") == event["type"] and
                      row.get("subject_ref") == event.get("subject_ref")), None)
        if prior:
            field = immutable[event["type"]]
            if prior.get(field) != event.get(field):
                raise ValueError(f"immutable {event['type']} conflict for {event.get('subject_ref')}")
            return prior
    event.setdefault("created_at", now())
    event["event_id"] = _event_id(event)
    existing = {row["event_id"]: row for row in existing_rows}
    if event["event_id"] in existing:
        return existing[event["event_id"]]
    store = current_event_store()
    appended = store.append(
        event,
        message=f"{event['type']}: {event.get('subject_ref', event['event_id'])}",
        expected_head=store.head())
    existing_rows.append(appended)
    return appended


def v2_head():
    return current_event_store().head()


def _idempotent_review(projection, subject, request_id, review_key, final_keys):
    if not request_id: return None
    matches = [event for event in projection["events"]
               if event.get("type") == review_key and event.get("request_id") == request_id]
    if not matches: return None
    review = matches[-1]
    if review.get("subject_ref") != subject:
        raise ValueError("IDEMPOTENCY_KEY_CONFLICT")
    final = next((event for event in reversed(projection["events"])
                  if event.get("type") in final_keys and
                  event.get("review_ref") == review.get("event_id")), None)
    if not final: raise ValueError("IDEMPOTENT_REVIEW_INCOMPLETE")
    return {"ok": True, "review": review, "result": final, "idempotent": True}


def _require_expected_head(expected_head):
    if expected_head is not None and expected_head != v2_head():
        raise ValueError("STALE_LEDGER_HEAD")


_policy_override = ContextVar("proofpress_policy_override", default=None)
_judge_environment = ContextVar("proofpress_judge_environment", default=None)


@contextmanager
def using_policy(policy):
    """Request-local operator configuration; never mutate process environment."""
    token = _policy_override.set(policy)
    try:
        yield
    finally:
        _policy_override.reset(token)


@contextmanager
def using_judge_environment(environment):
    """Inject workspace-scoped provider credentials without mutating os.environ."""
    token = _judge_environment.set(dict(environment or {}))
    try:
        yield
    finally:
        _judge_environment.reset(token)


def load_v2_policy():
    override = _policy_override.get()
    if override is not None:
        return json.loads(json.dumps(override))
    raw = {}
    path = Path(POLICY_PATH)
    if path.exists():
        raw = json.loads(path.read_text(encoding="utf-8"))
    item = {**DEFAULT_POLICY_V2, **raw}
    item["verification"] = {
        **DEFAULT_POLICY_V2["verification"], **(raw.get("verification") or {})}
    item["judge"] = {**DEFAULT_POLICY_V2["judge"], **(raw.get("judge") or {})}
    # Explicit operator opt-in. Model and adapter are bound into the policy digest;
    # enabling/changing this requires revalidation of existing admissions.
    model = os.environ.get("PROOFPRESS_JUDGE_MODEL", "").strip()
    if model and not item["judge"]["command"]:
        item["judge"] = {"identity": "judge:openrouter-advisory",
                         "command": [sys.executable, "-m", "proofpress.hosted.judge", "--model", model],
                         "timeout_seconds": 60}
    for role in ("verification", "judge"):
        identity = item[role].get("identity")
        if not isinstance(identity, str) or not identity.strip():
            raise ValueError(f"policy {role}.identity must be a non-empty string")
    profile = item["verification"].get("profile")
    if not isinstance(profile, str) or not profile.strip():
        raise ValueError("policy verification.profile must be a non-empty string")
    command = item["judge"].get("command", [])
    if not isinstance(command, list) or not all(isinstance(x, str) for x in command):
        raise ValueError("policy judge.command must be an argv array")
    item["digest"] = digest({k: v for k, v in item.items() if k != "digest"})
    return item


def governance_configuration(policy=None):
    """Return the safe, digest-bound role configuration for local clients."""
    policy = policy or load_v2_policy()
    verification = policy["verification"]
    judge = policy["judge"]
    return {
        "schema_version": "proofpress/local-governance-config/v1alpha1",
        "policy_path": POLICY_PATH,
        "policy_digest": policy["digest"],
        "require_judge": bool(policy.get("require_judge")),
        "proposer": {"identity_source": "operation_parameter"},
        "verification": {
            "identity": verification["identity"],
            "profile": verification["profile"],
            "config_digest": digest(verification),
        },
        "judge": {
            "identity": judge["identity"],
            "configured": bool(judge["command"]),
            "timeout_seconds": judge["timeout_seconds"],
            "config_digest": digest(judge),
        },
        "authority_separation": {
            "proposer_may_verify_own_work": False,
            "proposer_may_judge_own_work": False,
            "judge_may_admit": False,
            "human_approval_required_for_admission": True,
        },
    }


def _judge_policy_payload(policy):
    """Keep executable judge configuration out of the model input packet."""
    return {
        **{key: value for key, value in policy.items()
           if key not in {"judge", "digest"}},
        "judge": {
            "identity": policy["judge"]["identity"],
            "config_digest": digest(policy["judge"]),
        },
        "digest": policy["digest"],
    }


def _require_configured_role_separation(row, policy, role):
    identity = policy[role]["identity"]
    if identity == row["proposer"]:
        raise ValueError(f"proposer may not act as configured {role} identity")
    return identity


def v2_projection(events=None):
    events = v2_events() if events is None else events
    result = {
        "sources": {}, "evidence": {}, "conclusions": {}, "evaluations": {},
        "recommendations": {}, "reviews": {}, "admissions": {},
        "rejections": {}, "revision_requests": {}, "supersessions": {}, "relations": {},
        "relation_evaluations": {}, "relation_reviews": {},
        "relation_recommendations": {}, "relation_admissions": {},
        "relation_rejections": {}, "relation_revision_requests": {},
        "conflict_resolutions": {}, "events": events,
    }
    for event in events:
        kind = event.get("type")
        subject = event.get("subject_ref")
        if kind == "source_recorded": result["sources"][subject] = event["record"]
        elif kind == "evidence_bound": result["evidence"][subject] = event["evidence"]
        elif kind == "conclusion_proposed": result["conclusions"][subject] = event["conclusion"]
        elif kind == "policy_evaluated": result["evaluations"][subject] = event
        elif kind == "judge_recommended": result["recommendations"][subject] = event
        elif kind == "human_reviewed": result["reviews"][subject] = event
        elif kind == "conclusion_admitted": result["admissions"][subject] = event
        elif kind == "conclusion_rejected": result["rejections"][subject] = event
        elif kind == "conclusion_revision_requested": result["revision_requests"][subject] = event
        elif kind == "conclusion_superseded": result["supersessions"][subject] = event
        elif kind == "relation_proposed": result["relations"][subject] = event["relation"]
        elif kind == "relation_evaluated": result["relation_evaluations"][subject] = event
        elif kind == "relation_judge_recommended": result["relation_recommendations"][subject] = event
        elif kind == "relation_reviewed": result["relation_reviews"][subject] = event
        elif kind == "relation_admitted": result["relation_admissions"][subject] = event
        elif kind == "relation_rejected": result["relation_rejections"][subject] = event
        elif kind == "relation_revision_requested": result["relation_revision_requests"][subject] = event
        elif kind == "contradiction_resolved": result["conflict_resolutions"][subject] = event
    return result


def _conclusion_digest(row):
    return digest({k: v for k, v in row.items() if k != "digest"})


def validate_profile(profile, qualifiers):
    qualifiers = qualifiers or {}
    if not profile: return qualifiers
    if profile == "repo":
        repo = qualifiers.get("repo")
        if not isinstance(repo, dict):
            raise ValueError("repo profile requires qualifiers.repo")
        required = {"schema_version", "claim_kind", "repository_id", "head_commit"}
        missing = sorted(required - set(repo))
        if missing: raise ValueError("repo profile missing: " + ", ".join(missing))
        if repo["schema_version"] != proofpress_repo.REPO_PROFILE_SCHEMA:
            raise ValueError("unsupported repo profile schema")
        if repo["claim_kind"] not in proofpress_repo.CLAIM_KINDS:
            raise ValueError("unknown repo claim kind")
        if not re.fullmatch(r"repo_[0-9a-f]{16}", str(repo["repository_id"])):
            raise ValueError("invalid repo repository_id")
        if not re.fullmatch(r"[0-9a-f]{40}", str(repo["head_commit"])):
            raise ValueError("invalid repo head_commit")
        unknown = set(repo) - (required | {"pull_request"})
        if unknown: raise ValueError("unknown repo profile fields: " + ", ".join(sorted(unknown)))
        return {**qualifiers, "profile": proofpress_repo.REPO_PROFILE_SCHEMA}
    if profile == "experiment":
        return proofpress_experiment.normalize_conclusion(qualifiers)
    if profile != "legal": raise ValueError("unknown claim profile: " + profile)
    legal = qualifiers.get("legal")
    if not isinstance(legal, dict):
        raise ValueError("legal profile requires qualifiers.legal")
    required = {"jurisdiction", "authority", "citation_locator"}
    missing = sorted(key for key in required if not isinstance(legal.get(key), str)
                     or not legal[key].strip())
    if missing: raise ValueError("legal profile missing: " + ", ".join(missing))
    allowed = required | {"effective_from", "effective_to", "document_type", "legal_status"}
    unknown = sorted(set(legal) - allowed)
    if unknown: raise ValueError("unknown legal profile fields: " + ", ".join(unknown))
    start, end = legal.get("effective_from"), legal.get("effective_to")
    if start and end and start > end:
        raise ValueError("legal effective_from must not be after effective_to")
    return {**qualifiers, "profile": LEGAL_PROFILE_SCHEMA}


def v2_state(projection, conclusion, policy=None):
    cid = conclusion["id"]
    policy = policy or load_v2_policy()
    if cid in projection["supersessions"]: return "superseded"
    if conclusion.get("expires_at") and conclusion["expires_at"] <= now(): return "expired"
    if cid in projection["rejections"]: return "rejected"
    if cid in projection["revision_requests"]: return "needs_revision"
    admitted = projection["admissions"].get(cid)
    if not admitted: return "needs_review"
    if admitted.get("policy_digest") != policy["digest"]: return "unresolved"
    if admitted.get("conclusion_digest") != conclusion["digest"]: return "unresolved"
    return "admitted"


def review_state_v2(projection, conclusion, policy=None):
    """Owner-facing state: failed current checks are blocked, not review work."""
    policy = policy or load_v2_policy()
    state = v2_state(projection, conclusion, policy)
    evaluation = projection["evaluations"].get(conclusion["id"])
    if (state in {"needs_review", "unresolved"} and evaluation and
            evaluation.get("conclusion_digest") == conclusion["digest"] and
            evaluation.get("policy_digest") == policy["digest"] and
            not evaluation.get("eligible")):
        return "blocked"
    return state


_SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")


def _required_string(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"retrieval evidence {field} must be a non-empty string")
    return value


def _required_digest(value, field):
    value = _required_string(value, field)
    if not _SHA256.fullmatch(value):
        raise ValueError(f"retrieval evidence {field} must be a sha256 digest")
    return value


def _required_positive_int(value, field, minimum=1):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"retrieval evidence {field} must be an integer >= {minimum}")
    return value


def _normalize_locator(raw, quote):
    if not isinstance(raw, dict):
        raise ValueError("retrieval evidence locator must be an object")
    kind = raw.get("kind")
    if kind == "text_span":
        start = _required_positive_int(raw.get("start"), "locator.start", 0)
        end = _required_positive_int(raw.get("end"), "locator.end", 0)
        if end <= start:
            raise ValueError("retrieval evidence locator.end must be greater than locator.start")
        if end - start != len(quote):
            raise ValueError("retrieval evidence text_span length must equal the quote length")
        return {"kind": kind, "start": start, "end": end,
                "text_digest": _required_digest(raw.get("text_digest"), "locator.text_digest")}
    if kind == "page_span":
        page_start = _required_positive_int(raw.get("page_start"), "locator.page_start")
        page_end = _required_positive_int(raw.get("page_end"), "locator.page_end")
        if page_end < page_start:
            raise ValueError("retrieval evidence locator.page_end must be >= locator.page_start")
        return {"kind": kind, "page_start": page_start, "page_end": page_end,
                "page_digest": _required_digest(raw.get("page_digest"), "locator.page_digest")}
    if kind == "section_span":
        page_start = _required_positive_int(raw.get("page_start"), "locator.page_start")
        page_end = _required_positive_int(raw.get("page_end"), "locator.page_end")
        if page_end < page_start:
            raise ValueError("retrieval evidence locator.page_end must be >= locator.page_start")
        return {"kind": kind,
                "section_id": _required_string(raw.get("section_id"), "locator.section_id"),
                "section_digest": _required_digest(raw.get("section_digest"), "locator.section_digest"),
                "page_start": page_start, "page_end": page_end}
    raise ValueError("retrieval evidence locator.kind must be text_span, page_span, or section_span")


def _retrieval_receipt(payload):
    """Validate the portable retrieval contract and return its canonical receipt.

    The receipt deliberately binds a locator to the source and the retrieval
    decision, but does not claim to rerun an external extractor, embedder, or
    PageIndex adapter. Those adapters can later provide the digests recorded
    here and be independently evaluated without changing admission semantics.
    """
    if not isinstance(payload, dict) or payload.get("schema_version") != RETRIEVAL_EVIDENCE_SCHEMA:
        raise ValueError(f"retrieval evidence schema_version must be {RETRIEVAL_EVIDENCE_SCHEMA}")
    source_row, evidence_row, retrieval_row = payload.get("source"), payload.get("evidence"), payload.get("retrieval")
    if not all(isinstance(row, dict) for row in (source_row, evidence_row, retrieval_row)):
        raise ValueError("retrieval evidence source, evidence, and retrieval must be objects")
    quote = _required_string(evidence_row.get("quote"), "evidence.quote")
    source = {"uri": _required_string(source_row.get("uri"), "source.uri"),
              "content_digest": _required_digest(source_row.get("content_digest"), "source.content_digest")}
    if "media_type" in source_row:
        source["media_type"] = _required_string(source_row["media_type"], "source.media_type")
    retrieval = {"adapter": _required_string(retrieval_row.get("adapter"), "retrieval.adapter"),
                 "version": _required_string(retrieval_row.get("version"), "retrieval.version"),
                 "query": _required_string(retrieval_row.get("query"), "retrieval.query"),
                 "config_digest": _required_digest(retrieval_row.get("config_digest"), "retrieval.config_digest")}
    if "selection_reason" in retrieval_row:
        retrieval["selection_reason"] = _required_string(retrieval_row["selection_reason"], "retrieval.selection_reason")
    return {"schema_version": RETRIEVAL_EVIDENCE_SCHEMA, "source": source,
            "quote": quote, "quote_digest": "sha256:" + hashlib.sha256(quote.encode("utf-8")).hexdigest(),
            "locator": _normalize_locator(evidence_row.get("locator"), quote),
            "retrieval": retrieval}


def _retrieval_receipt_valid(evidence_row):
    if evidence_row.get("kind") != "retrieval_evidence":
        return True
    receipt = evidence_row.get("retrieval_receipt")
    try:
        normalized = _retrieval_receipt({
            "schema_version": RETRIEVAL_EVIDENCE_SCHEMA,
            "source": receipt["source"],
            "evidence": {"quote": receipt["quote"], "locator": receipt["locator"]},
            "retrieval": receipt["retrieval"],
        })
    except (KeyError, TypeError, ValueError):
        return False
    return (receipt == normalized and
            evidence_row.get("source_content_digest") == normalized["source"]["content_digest"] and
            evidence_row.get("quote_digest") == normalized["quote_digest"] and
            evidence_row.get("retrieval_receipt_digest") == digest(normalized))


def _import_retrieval_evidence_v2(payload):
    receipt = _retrieval_receipt(payload)
    source = receipt["source"]
    src = {"id": ident({"uri": source["uri"], "digest": source["content_digest"]}, "src_"),
           "kind": "retrieval_source", "uri": source["uri"],
           "content_digest": source["content_digest"]}
    if "media_type" in source:
        src["media_type"] = source["media_type"]
    src["record_hash"] = digest(src)
    evidence = {"id": ident({"source": src["id"], "receipt": digest(receipt)}, "evd_"),
                "kind": "retrieval_evidence", "source_ref": src["id"],
                "source_digest": src["record_hash"],
                "source_content_digest": source["content_digest"],
                "quote_digest": receipt["quote_digest"],
                "retrieval_receipt": receipt,
                "retrieval_receipt_digest": digest(receipt)}
    evidence["digest"] = digest(evidence)
    created = [append_v2({"type": "source_recorded", "subject_ref": src["id"], "record": src}),
               append_v2({"type": "evidence_bound", "subject_ref": evidence["id"],
                          "source_ref": src["id"], "evidence": evidence})]
    return created


def _trace_session(payload):
    if not isinstance(payload, dict):
        return None
    if "trace_version" not in payload and "trace-protocol.org" not in str(payload.get("context", "")):
        return None
    if not payload.get("id") or not isinstance(payload.get("events"), list):
        raise ValueError("not a TRACE session document")
    version = str(payload.get("trace_version") or "")
    if version not in TRACE_SUPPORTED_VERSIONS:
        raise ValueError("unsupported TRACE trace_version: " + version
                         + "; accepted: " + ", ".join(sorted(TRACE_SUPPORTED_VERSIONS)))
    return payload


def _import_trace_evidence_v2(session):
    """Bind TRACE provenance as evidence only; it never creates a claim or admission."""
    created = []
    for raw in session["events"]:
        src = trace_source(session, raw)
        ev = evidence(src)
        created.append(append_v2({"type": "source_recorded", "subject_ref": src["id"], "record": src}))
        created.append(append_v2({"type": "evidence_bound", "subject_ref": ev["id"],
                                  "source_ref": src["id"], "evidence": ev}))
    return created


def import_evidence_v2(path):
    target = Path(path)
    if not target.exists(): raise ValueError(f"evidence input not found: {path}")
    created = []
    payload = None
    if target.suffix.lower() == ".json":
        payload = json.loads(target.read_text(encoding="utf-8"))
        trace = _trace_session(payload)
        span_rows = [] if trace or payload.get("schema_version") == RETRIEVAL_EVIDENCE_SCHEMA else spans(payload)
    else:
        trace = None
        span_rows = []
    if isinstance(payload, dict) and payload.get("schema_version") == proofpress_repo.REPO_EVIDENCE_SCHEMA:
        verification = proofpress_repo.verify_bundle(payload, Path.cwd())
        if not all(verification.values()):
            failed = sorted(key for key, value in verification.items() if not value)
            raise ValueError("repo evidence bundle failed verification: " + ", ".join(failed))
        repository = payload["repository"]
        src = {"id": ident({"repository": repository["id"],
                            "head": payload["change"]["head_commit"]}, "src_"),
               "kind": "repository_change", "repository": repository,
               "base_commit": payload["change"]["base_commit"],
               "head_commit": payload["change"]["head_commit"],
               "diff_digest": payload["change"]["diff_digest"],
               "changed_paths": payload["change"]["changed_paths"]}
        if payload.get("pull_request"):
            src["pull_request"] = payload["pull_request"]
        src["record_hash"] = digest(src)
        ev = {"id": ident({"source": src["id"], "bundle": payload["bundle_digest"]}, "evd_"),
              "kind": "repository_evidence", "source_ref": src["id"],
              "source_digest": src["record_hash"], "bundle": payload,
              "bundle_digest": payload["bundle_digest"],
              "verification": verification}
        ev["digest"] = digest(ev)
        created.extend([
            append_v2({"type": "source_recorded", "subject_ref": src["id"], "record": src}),
            append_v2({"type": "evidence_bound", "subject_ref": ev["id"],
                       "source_ref": src["id"], "evidence": ev}),
        ])
    elif isinstance(payload, dict) and payload.get("schema_version") == RETRIEVAL_EVIDENCE_SCHEMA:
        created.extend(_import_retrieval_evidence_v2(payload))
    elif trace:
        created.extend(_import_trace_evidence_v2(trace))
    elif span_rows:
        for raw in span_rows:
            src = source(raw)
            created.append(append_v2({"type": "source_recorded", "subject_ref": src["id"], "record": src}))
            ev = evidence(src)
            created.append(append_v2({"type": "evidence_bound", "subject_ref": ev["id"], "source_ref": src["id"], "evidence": ev}))
    else:
        body = target.read_bytes()
        sha = "sha256:" + hashlib.sha256(body).hexdigest()
        src = {
            "id": ident({"path": str(target), "digest": sha}, "src_"),
            "kind": "artifact", "path": str(target), "content_digest": sha,
            "size": len(body), "recorded_at": now(),
        }
        src["record_hash"] = digest(src)
        projection = v2_projection()
        prior = projection["sources"].get(src["id"])
        if prior:
            stable = ("kind", "path", "content_digest", "size")
            if any(prior.get(key) != src.get(key) for key in stable):
                raise ValueError("immutable artifact source conflict for " + src["id"])
            src = prior
        ev = {
            "id": ident({"source": src["id"], "digest": sha}, "evd_"),
            "kind": "artifact_evidence", "source_ref": src["id"],
            "source_digest": src["record_hash"], "artifact_digest": sha,
            "path": str(target),
        }
        ev["digest"] = digest(ev)
        created.append(append_v2({"type": "source_recorded", "subject_ref": src["id"], "record": src}))
        created.append(append_v2({"type": "evidence_bound", "subject_ref": ev["id"], "source_ref": src["id"], "evidence": ev}))
    projection = v2_projection()
    imported_evidence = sorted(row["subject_ref"] for row in created
                               if row.get("type") == "evidence_bound")
    return {"ok": True, "events_added": len(created),
            "imported_evidence": imported_evidence,
            "evidence": sorted(projection["evidence"]), "ref": KNOWLEDGE_REF}


def submit_evidence_v2(payload, profile=None):
    """Submit one bounded evidence envelope without a local path."""
    if profile is None:
        created = _import_retrieval_evidence_v2(payload)
    elif profile == "experiment":
        projection = v2_projection()
        normalized = proofpress_experiment.normalize_evidence(
            payload, projection["evidence"])
        evidence = {
            "id": ident({"profile": proofpress_experiment.PROFILE,
                         "payload": normalized}, "evd_"),
            "kind": "experiment_evidence",
            "experiment_profile": normalized,
            "source_evidence_refs": sorted(set(
                ([normalized.get("observation", {}).get("source_evidence_ref")]
                 if normalized.get("observation") else []) +
                ([normalized.get("cell", {}).get("source_evidence_ref")]
                 if normalized.get("cell") else []) +
                normalized.get("derivation", {}).get("input_evidence_refs", [])
            )),
        }
        evidence["source_evidence_refs"] = [x for x in evidence["source_evidence_refs"] if x]
        evidence["digest"] = digest(evidence)
        created = [append_v2({"type": "evidence_bound", "subject_ref": evidence["id"],
                              "source_ref": evidence["source_evidence_refs"][0],
                              "evidence": evidence})]
    else:
        raise ValueError("unknown evidence profile: " + str(profile))
    projection = v2_projection()
    imported_evidence = sorted(
        row["subject_ref"] for row in created
        if row.get("type") == "evidence_bound")
    return {"ok": True, "events_added": len(created),
            "imported_evidence": imported_evidence,
            "evidence": sorted(projection["evidence"]), "ref": KNOWLEDGE_REF}


def _repo_profile_checks(row, evidence_rows):
    repo = row.get("qualifiers", {}).get("repo")
    if not repo:
        return {}
    matching = [item for item in evidence_rows if item.get("kind") == "repository_evidence"]
    try:
        reverified = [proofpress_repo.verify_bundle(item["bundle"], Path.cwd())
                      for item in matching]
    except (KeyError, TypeError, ValueError):
        reverified = []
    return {
        "repo_evidence_present": bool(matching),
        "repo_evidence_verified": bool(matching) and all(
            all(item.get("verification", {}).values()) for item in matching),
        "repo_evidence_reverified": bool(reverified) and all(
            all(item.values()) for item in reverified),
        "repo_identity_bound": bool(matching) and all(
            item["bundle"]["repository"]["id"] == repo["repository_id"]
            for item in matching),
        "repo_commit_bound": bool(matching) and all(
            item["bundle"]["change"]["head_commit"] == repo["head_commit"]
            for item in matching),
        "repo_checks_passed": bool(matching) and all(
            all(receipt["status"] == "pass" for receipt in item["bundle"]["checks"])
            for item in matching),
        "repo_claim_is_current_fact": repo["claim_kind"] != "roadmap",
    }


def _experiment_profile_checks(row, evidence_rows, all_evidence):
    qualifier = row.get("qualifiers", {}).get("experiment")
    if not qualifier:
        return {}
    experiment_rows = [item for item in evidence_rows
                       if item.get("kind") == "experiment_evidence"]
    valid = []
    for item in experiment_rows:
        profile = item.get("experiment_profile")
        try:
            valid.append(proofpress_experiment.normalize_evidence(
                profile, all_evidence) == profile)
        except (KeyError, TypeError, ValueError):
            valid.append(False)
    identity = qualifier["experiment"]
    failure = qualifier.get("failure")
    failure_refs = set(failure.get("feedback_evidence_refs", [])) if failure else set()
    row_refs = set(row.get("evidence_refs", []))
    return {
        "experiment_evidence_present": bool(experiment_rows),
        "experiment_evidence_valid": bool(experiment_rows) and all(valid),
        "experiment_identity_bound": bool(experiment_rows) and all(
            item["experiment_profile"].get("experiment") == identity
            for item in experiment_rows),
        "experiment_conclusion_kind_valid": (
            qualifier.get("conclusion_kind") in proofpress_experiment.CONCLUSION_KINDS),
        "experiment_failure_feedback_bound": (
            qualifier.get("conclusion_kind") != "failed-attempt"
            or bool(failure_refs) and failure_refs <= row_refs),
    }


def _text_list(value, field):
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip()
                                          for item in value):
        raise ValueError(f"applicability.{field} must be an array of non-empty strings")
    return [item.strip() for item in value]


def _applicability(value):
    """Normalize the small, YAML-frontmatter-shaped discovery card.

    This is deliberately descriptive rather than an authorization mechanism.
    Visibility remains enforced by the workspace credential before a card is
    returned to an agent. Historical row-level restrictions remain readable as
    legacy data but cannot be created by new proposals.
    """
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError("applicability must be an object")
    allowed = {"title", "description", "when_relevant", "keywords",
               "validity_conditions"}
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ValueError("unknown applicability fields: " + ", ".join(unknown))
    card = {}
    for field in ("title", "description"):
        if field in value:
            text = value[field]
            if not isinstance(text, str) or not text.strip():
                raise ValueError(f"applicability.{field} must be a non-empty string")
            card[field] = text.strip()
    for field in ("when_relevant", "keywords", "validity_conditions"):
        items = _text_list(value.get(field), field)
        if items:
            card[field] = items
    if not card:
        raise ValueError("applicability must contain at least one discovery field")
    return card


def propose_v2(statement, evidence_refs, scope=None, proposer=None, expires_at=None,
               artifact_refs=None, applicability=None, qualifiers=None,
               profile=None, reproposal_of=None):
    projection = v2_projection()
    missing = [ref for ref in evidence_refs if ref not in projection["evidence"]]
    if missing: raise ValueError("unknown evidence: " + ", ".join(missing))
    if scope is not None and (not isinstance(scope, str) or not scope.strip()):
        raise ValueError("scope must be a non-empty string when provided")
    scope = scope.strip() if scope else None
    if not isinstance(proposer, str) or not proposer.strip():
        raise ValueError("proposer must be a non-empty string")
    applicability = _applicability(applicability)
    qualifiers = validate_profile(profile, qualifiers)
    if reproposal_of is not None:
        if not isinstance(reproposal_of, str) or not reproposal_of.strip():
            raise ValueError("reproposal_of must be a non-empty conclusion ID")
        reproposal_of = reproposal_of.strip()
        predecessor = projection["conclusions"].get(reproposal_of)
        if not predecessor:
            raise ValueError("re-proposal requires an existing rejected conclusion")
        if v2_state(projection, predecessor) != "rejected":
            raise ValueError("re-proposal predecessor must be rejected")
        if predecessor.get("scope") != scope:
            raise ValueError("re-proposal must preserve the predecessor scope")
    revision_of = (qualifiers or {}).get("revision_of")
    if revision_of and reproposal_of:
        raise ValueError("a proposal cannot be both a requested revision and a re-proposal")
    if revision_of:
        parent = projection["conclusions"].get(revision_of)
        request = projection["revision_requests"].get(revision_of)
        if not parent or not request:
            raise ValueError("revision requires an existing request for changes")
        if (qualifiers or {}).get("revision_request_ref") != request["event_id"]:
            raise ValueError("revision must reference the current revision request")
    identity = {"statement": statement, "evidence": sorted(evidence_refs),
                "scope": scope}
    if applicability is not None:
        identity["applicability"] = applicability
    if reproposal_of is not None:
        identity["reproposal_of"] = reproposal_of
    row = {
        "id": ident(identity, "knw_"),
        "kind": "conclusion", "statement": statement,
        "evidence_refs": sorted(set(evidence_refs)),
        "artifact_refs": sorted(set(artifact_refs or [])),
        "scope": scope, "proposer": proposer, "expires_at": expires_at,
        "applicability": applicability,
        "reproposal_of": reproposal_of,
        "qualifiers": qualifiers or {}, "created_at": now(),
    }
    if row["id"] == reproposal_of:
        raise ValueError("a conclusion cannot be a re-proposal of itself")
    prior = projection["conclusions"].get(row["id"])
    if prior:
        stable = set(row) - {"created_at", "digest"}
        if any(prior.get(key) != row.get(key) for key in stable):
            raise ValueError("immutable conclusion conflict for " + row["id"])
        row = prior
    row["digest"] = _conclusion_digest(row)
    event = append_v2({"type": "conclusion_proposed", "subject_ref": row["id"],
                       "conclusion": row})
    return {"ok": True, "conclusion": row, "event_id": event["event_id"]}


def _relation_digest(row):
    return digest({k: v for k, v in row.items() if k != "digest"})


def relation_state(projection, row):
    rid = row["id"]
    if rid in projection["relation_rejections"]: return "rejected"
    if rid in projection["relation_revision_requests"]: return "needs_revision"
    admitted = projection["relation_admissions"].get(rid)
    if not admitted: return "needs_review"
    if admitted.get("policy_digest") != load_v2_policy()["digest"]: return "unresolved"
    if admitted.get("relation_digest") != row["digest"]: return "unresolved"
    return "admitted"


def _relation_cycle(projection, source, target, relation_type):
    if relation_type not in {"depends_on", "supersedes"}: return False
    graph = {}
    for row in projection["relations"].values():
        if row["type"] == relation_type and relation_state(projection, row) != "rejected":
            graph.setdefault(row["from"], set()).add(row["to"])
    graph.setdefault(source, set()).add(target)
    stack, seen = [target], set()
    while stack:
        current = stack.pop()
        if current == source: return True
        if current in seen: continue
        seen.add(current); stack.extend(graph.get(current, ()))
    return False


def propose_relation_v2(source, target, relation_type, proposer,
                        confidence=None, qualifiers=None, actor=None):
    if relation_type not in RELATION_TYPES:
        raise ValueError("relation type must be one of: " + ", ".join(sorted(RELATION_TYPES)))
    projection = v2_projection()
    if source not in projection["conclusions"] or target not in projection["conclusions"]:
        raise ValueError("relation endpoints must reference existing conclusions")
    policy = load_v2_policy()
    actor = actor or proposer
    if actor and (not _actor_can_read(projection["conclusions"][source], policy, actor)
                  or not _actor_can_read(projection["conclusions"][target], policy, actor)):
        raise ValueError("relation endpoints must reference visible conclusions")
    if source == target: raise ValueError("relation endpoints must be distinct")
    if confidence is not None and not 0 <= confidence <= 1:
        raise ValueError("relation confidence must be between 0 and 1")
    left, right = (sorted((source, target)) if relation_type in SYMMETRIC_RELATIONS
                   else (source, target))
    row = {"id": ident({"from": left, "to": right, "type": relation_type}, "rel_"),
           "kind": "claim_relation", "from": left, "to": right,
           "type": relation_type, "proposer": proposer, "confidence": confidence,
           "qualifiers": qualifiers or {}, "created_at": now()}
    prior = projection["relations"].get(row["id"])
    if prior:
        stable = set(row) - {"created_at", "digest"}
        if any(prior.get(key) != row.get(key) for key in stable):
            raise ValueError("immutable relation conflict for " + row["id"])
        row = prior
    row["digest"] = _relation_digest(row)
    event = append_v2({"type": "relation_proposed", "subject_ref": row["id"],
                       "relation": row})
    return {"ok": True, "relation": row, "event_id": event["event_id"]}


def evaluate_relation_v2(rid, projection=None, events=None, policy=None, actor=None):
    events = v2_events() if events is None else events
    projection = v2_projection(events) if projection is None else projection
    row = projection["relations"].get(rid); policy = policy or load_v2_policy()
    if not row: raise ValueError("relation not found: " + rid)
    if (actor and (not _actor_can_read(projection["conclusions"].get(row["from"], {}), policy, actor)
                   or not _actor_can_read(projection["conclusions"].get(row["to"], {}), policy, actor))):
        raise ValueError("relation not found: " + rid)
    verifier = _require_configured_role_separation(row, policy, "verification")
    left, right = projection["conclusions"].get(row["from"]), projection["conclusions"].get(row["to"])
    duplicate = [candidate for candidate in projection["relations"].values()
                 if candidate["id"] != rid and candidate["from"] == row["from"]
                 and candidate["to"] == row["to"] and candidate["type"] == row["type"]]
    checks = {
        "endpoints_present": left is not None and right is not None,
        "distinct_endpoints": row["from"] != row["to"],
        "known_relation_type": row["type"] in RELATION_TYPES,
        "no_duplicate": not duplicate,
        "acyclic_when_directed": not _relation_cycle(projection, row["from"], row["to"], row["type"]),
    }
    event = append_v2({"type": "relation_evaluated", "subject_ref": rid,
                       "relation_digest": row["digest"], "checks": checks,
                       "policy_digest": policy["digest"],
                       "verifier": verifier,
                       "verification_profile": policy["verification"]["profile"],
                       "verification_config_digest": digest(policy["verification"]),
                       "eligible": all(checks.values()),
                       "semantic_boundary": "structural checks do not establish semantic correctness"},
                      existing_rows=events)
    return event


def judge_relation_v2(rid, actor=None):
    events = v2_events(); projection = v2_projection(events); policy = load_v2_policy()
    row = projection["relations"].get(rid)
    if not row: raise ValueError("relation not found: " + rid)
    if (actor and (not _actor_can_read(projection["conclusions"].get(row["from"], {}), policy, actor)
                   or not _actor_can_read(projection["conclusions"].get(row["to"], {}), policy, actor))):
        raise ValueError("relation not found: " + rid)
    judge_identity = _require_configured_role_separation(row, policy, "judge")
    current = projection["relation_evaluations"].get(rid)
    evaluation = (current if current and
                  current.get("relation_digest") == row["digest"] and
                  current.get("policy_digest") == policy["digest"] else
                  evaluate_relation_v2(rid, projection=projection, events=events, policy=policy,
                                       actor=actor))
    command = policy["judge"]["command"]
    if not command: raise ValueError("no judge.command configured in .proofpress/policy.json")
    packet = {"schema_version": "proofpress/relation-judge-request/v1",
              "relation": row,
              "from_claim": projection["conclusions"][row["from"]],
              "to_claim": projection["conclusions"][row["to"]],
              "evaluation": {k: v for k, v in evaluation.items() if k != "commit"},
              "policy": _judge_policy_payload(policy),
              "instruction": "Assess semantic relation correctness; deterministic checks establish structure only."}
    try:
        environment = os.environ.copy()
        environment.update(_judge_environment.get() or {})
        result = subprocess.run(command, input=json.dumps(packet), text=True,
                                capture_output=True, timeout=float(policy["judge"]["timeout_seconds"]),
                                env=environment)
    except subprocess.TimeoutExpired as exc:
        raise ValueError("relation judge command timed out") from exc
    if result.returncode: raise ValueError("relation judge command failed: " + result.stderr.strip())
    try: verdict = json.loads(result.stdout)
    except json.JSONDecodeError as exc: raise ValueError("relation judge returned invalid JSON") from exc
    if verdict.get("recommendation") not in {"accept", "reject", "escalate"}:
        raise ValueError("relation judge recommendation must be accept, reject, or escalate")
    if not isinstance(verdict.get("rationale"), str) or not verdict["rationale"].strip():
        raise ValueError("relation judge rationale is required")
    return append_v2({"type": "relation_judge_recommended", "subject_ref": rid,
                      "relation_digest": row["digest"],
                      "policy_digest": policy["digest"],
                      "judge": judge_identity,
                      "judge_config_digest": digest(policy["judge"]),
                      "recommendation": verdict["recommendation"],
                      "rationale": verdict["rationale"],
                      "adapter": verdict.get("adapter", command[0]),
                      "model": verdict.get("model")}, existing_rows=events)


def review_relation_v2(rid, decision, reviewer, note=None, request_id=None,
                       expected_head=None):
    if decision not in {"admit", "reject", "request_changes"}:
        raise ValueError("relation review decision must be admit, reject, or request_changes")
    projection = v2_projection()
    duplicate = _idempotent_review(
        projection, rid, request_id, "relation_reviewed",
        {"relation_admitted", "relation_rejected", "relation_revision_requested"})
    if duplicate: return duplicate
    _require_expected_head(expected_head)
    row = projection["relations"].get(rid)
    if not row: raise ValueError("relation not found: " + rid)
    if row["type"] == "contradicts" and relation_state(projection, row) == "admitted":
        raise ValueError("admitted contradiction may only transition through relation resolve")
    if decision == "admit" and reviewer == row["proposer"]:
        raise ValueError("proposer may not self-approve a relation")
    evaluation = evaluate_relation_v2(rid)
    if decision == "admit" and not evaluation["eligible"]:
        raise ValueError("relation is blocked by deterministic policy")
    projection = v2_projection(); recommendation = projection["relation_recommendations"].get(rid)
    policy = load_v2_policy()
    if decision == "admit" and policy["require_judge"]:
        if not recommendation or recommendation.get("relation_digest") != row["digest"] or recommendation.get("policy_digest") != policy["digest"] or recommendation.get("recommendation") != "accept":
            raise ValueError("current policy requires an accepting relation judge recommendation")
    review = append_v2({"type": "relation_reviewed", "subject_ref": rid,
                        "decision": decision, "reviewer": reviewer,
                        "identity_basis": "self_asserted", "note": note,
                        "request_id": request_id,
                        "relation_digest": row["digest"], "policy_digest": policy["digest"]})
    final_type = ("relation_admitted" if decision == "admit" else
                  "relation_revision_requested" if decision == "request_changes" else
                  "relation_rejected")
    final = append_v2({"type": final_type,
                       "subject_ref": rid, "review_ref": review["event_id"],
                       "reviewer": reviewer, "relation_digest": row["digest"],
                       "policy_digest": policy["digest"]})
    return {"ok": True, "review": review, "result": final}


def _matching_conflict_supersession(projection, relation, resolution):
    """Return the linked supersession only when a conflict resolution is complete."""
    if not resolution or resolution.get("disposition") != "supersede": return None
    if resolution.get("relation_digest") != relation.get("digest"): return None
    winner = resolution.get("winner")
    endpoints = {relation["from"], relation["to"]}
    if winner not in endpoints: return None
    loser = next(iter(endpoints - {winner}))
    supersession = projection["supersessions"].get(loser)
    if not supersession: return None
    if supersession.get("superseded_by") != winner: return None
    if supersession.get("resolution_ref") != resolution.get("event_id"): return None
    return supersession


def resolve_contradiction_v2(rid, disposition, reviewer, winner=None, note=None,
                             expected_head=None):
    """Resolve an admitted contradiction without inferring a winner automatically.

    Reviewer identity remains self-asserted in this local MVP. A policy allowlist
    restricts the declared resolver identity; it is not authentication.
    """
    if disposition not in {"supersede", "withhold"}:
        raise ValueError("contradiction resolution must be supersede or withhold")
    projection, policy = v2_projection(), load_v2_policy()
    _require_expected_head(expected_head)
    relation = projection["relations"].get(rid)
    if not relation or relation["type"] != "contradicts":
        raise ValueError("resolution requires an admitted contradicts relation")
    if relation_state(projection, relation) != "admitted":
        raise ValueError("contradiction relation is not admitted")
    if reviewer == relation["proposer"]:
        raise ValueError("proposer may not self-resolve a relation")
    allowed = policy.get("conflict_resolvers", ["*"])
    if "*" not in allowed and reviewer not in allowed:
        raise ValueError("reviewer is not allowed to resolve contradictions by policy")
    endpoints = {relation["from"], relation["to"]}
    if disposition == "supersede":
        if winner not in endpoints:
            raise ValueError("supersede resolution requires --winner to be a relation endpoint")
        loser = next(iter(endpoints - {winner}))
    elif winner:
        raise ValueError("withhold resolution must not name a winner")
    prior = projection["conflict_resolutions"].get(rid)
    if prior:
        stable = {"disposition": disposition, "winner": winner, "reviewer": reviewer, "note": note}
        prior_stable = {key: prior.get(key) for key in stable}
        if prior_stable != stable:
            raise ValueError("contradiction already has an immutable resolution")
        result = {"ok": True, "resolution": prior, "idempotent": True}
        if disposition == "supersede":
            supersession = _matching_conflict_supersession(projection, relation, prior)
            if not supersession:
                loser = next(iter(endpoints - {winner}))
                supersession = append_v2({"type": "conclusion_superseded", "subject_ref": loser,
                                          "superseded_by": winner, "reviewer": reviewer,
                                          "identity_basis": "self_asserted", "note": note,
                                          "resolution_ref": prior["event_id"]})
            result["supersession"] = supersession
        return result
    resolution = append_v2({"type": "contradiction_resolved", "subject_ref": rid,
                            "relation_digest": relation["digest"], "disposition": disposition,
                            "winner": winner, "reviewer": reviewer,
                            "identity_basis": "self_asserted", "note": note,
                            "policy_digest": policy["digest"]})
    result = {"ok": True, "resolution": resolution}
    if disposition == "supersede":
        supersession = append_v2({"type": "conclusion_superseded", "subject_ref": loser,
                                  "superseded_by": winner, "reviewer": reviewer,
                                  "identity_basis": "self_asserted", "note": note,
                                  "resolution_ref": resolution["event_id"]})
        result["supersession"] = supersession
    return result


def _active_contradictions(projection, policy, scope=None):
    """Map claims to admitted conflicts before actor visibility is considered."""
    current = {cid for cid, row in projection["conclusions"].items()
               if (not scope or row["scope"] == scope)
               and v2_state(projection, row, policy) == "admitted"}
    conflicts = {}
    for relation in projection["relations"].values():
        if (relation["type"] != "contradicts"
                or relation_state(projection, relation) != "admitted"
                or relation["from"] not in current or relation["to"] not in current):
            continue
        resolution = projection["conflict_resolutions"].get(relation["id"])
        if _matching_conflict_supersession(projection, relation, resolution):
            continue
        reason = ("contradiction_withheld"
                  if resolution and resolution.get("disposition") == "withhold"
                  else "contradiction_resolution_incomplete"
                  if resolution else "contradiction_unresolved")
        for cid, peer in ((relation["from"], relation["to"]),
                          (relation["to"], relation["from"])):
            conflicts.setdefault(cid, []).append({"relation_id": relation["id"],
                                                   "peer_id": peer, "reason": reason})
    return conflicts


def _conflict_resolution_receipts(projection, cid):
    """Project completed conflict decisions onto the surviving claim receipt."""
    receipts = []
    for rid, resolution in projection["conflict_resolutions"].items():
        relation = projection["relations"].get(rid)
        if not relation or resolution.get("winner") != cid: continue
        supersession = _matching_conflict_supersession(projection, relation, resolution)
        if not supersession: continue
        loser = next(iter({relation["from"], relation["to"]} - {cid}))
        receipts.append({"relation_id": rid, "relation_digest": relation["digest"],
                         "resolution_event": resolution["event_id"],
                         "supersession_event": supersession["event_id"],
                         "disposition": resolution["disposition"], "winner": cid,
                         "loser": loser, "reviewer": resolution["reviewer"],
                         "identity_basis": resolution["identity_basis"],
                         "policy_digest": resolution["policy_digest"]})
    return sorted(receipts, key=lambda row: row["relation_id"])


def evaluate_v2(cid, projection=None, events=None, policy=None, actor=None):
    events = v2_events() if events is None else events
    projection = v2_projection(events) if projection is None else projection
    row = projection["conclusions"].get(cid)
    if not row: raise ValueError("conclusion not found: " + cid)
    policy = policy or load_v2_policy()
    if actor and not _actor_can_read(row, policy, actor):
        raise ValueError("conclusion not found: " + cid)
    verifier = _require_configured_role_separation(row, policy, "verification")
    evidence_ok = [ref for ref in row["evidence_refs"] if ref in projection["evidence"]]
    checks = {
        "evidence_present": len(evidence_ok) >= int(policy["min_evidence"]),
        "evidence_integrity": all(projection["evidence"][ref].get("digest") ==
                                  digest({k: v for k, v in projection["evidence"][ref].items() if k != "digest"})
                                  for ref in evidence_ok),
        "retrieval_receipts": all(_retrieval_receipt_valid(projection["evidence"][ref])
                                 for ref in evidence_ok),
        "not_expired": not row.get("expires_at") or row["expires_at"] > now(),
        "not_superseded": cid not in projection["supersessions"],
        # A legacy scope remains valid, but new knowledge can state its reuse
        # conditions through the descriptive applicability card instead.
        "reuse_boundary_present": bool(row.get("scope") or row.get("applicability")),
    }
    checks.update(_repo_profile_checks(
        row, [projection["evidence"][ref] for ref in evidence_ok]))
    checks.update(_experiment_profile_checks(
        row, [projection["evidence"][ref] for ref in evidence_ok],
        projection["evidence"]))
    event = append_v2({"type": "policy_evaluated", "subject_ref": cid,
                       "conclusion_digest": row["digest"],
                       "policy_digest": policy["digest"], "checks": checks,
                       "verifier": verifier,
                       "verification_profile": policy["verification"]["profile"],
                       "verification_config_digest": digest(policy["verification"]),
                       "eligible": all(checks.values())}, existing_rows=events)
    return event


def judge_v2(cid, actor=None):
    events = v2_events(); projection = v2_projection(events); policy = load_v2_policy()
    row = projection["conclusions"].get(cid)
    if not row: raise ValueError("conclusion not found: " + cid)
    if actor and not _actor_can_read(row, policy, actor):
        raise ValueError("conclusion not found: " + cid)
    judge_identity = _require_configured_role_separation(row, policy, "judge")
    evaluation = evaluate_v2(
        cid, projection=projection, events=events, policy=policy, actor=actor)
    command = policy["judge"]["command"]
    if not command: raise ValueError("no judge.command configured in .proofpress/policy.json")
    reproposal_parent = _reproposal_parent(projection, row)
    packet = {"schema_version": "proofpress/judge-request/v1", "conclusion": row,
              "evidence": [projection["evidence"][x] for x in row["evidence_refs"]],
              "evaluation": {k: v for k, v in evaluation.items() if k != "commit"},
              "policy": _judge_policy_payload(policy)}
    if reproposal_parent:
        packet["reproposal_parent"] = reproposal_parent
    try:
        result = subprocess.run(command, input=json.dumps(packet), text=True,
                                capture_output=True, timeout=float(policy["judge"]["timeout_seconds"]))
    except subprocess.TimeoutExpired as exc:
        raise ValueError("judge command timed out") from exc
    if result.returncode:
        raise ValueError("judge command failed: " + result.stderr.strip())
    try: verdict = json.loads(result.stdout)
    except json.JSONDecodeError as exc: raise ValueError("judge returned invalid JSON") from exc
    if verdict.get("recommendation") not in {"accept", "reject", "escalate"}:
        raise ValueError("judge recommendation must be accept, reject, or escalate")
    if not isinstance(verdict.get("rationale"), str) or not verdict["rationale"].strip():
        raise ValueError("judge rationale is required")
    event = append_v2({"type": "judge_recommended", "subject_ref": cid,
                       "conclusion_digest": row["digest"],
                       "policy_digest": policy["digest"],
                       "judge": judge_identity,
                       "judge_config_digest": digest(policy["judge"]),
                       "recommendation": verdict["recommendation"],
                       "rationale": verdict["rationale"],
                       "adapter": verdict.get("adapter", command[0]),
                       "model": verdict.get("model")})
    return event


def judge_batch_v2(scope, actor=None):
    if not scope: raise ValueError("batch judge requires --scope")
    events = v2_events(); projection = v2_projection(events); policy = load_v2_policy()
    candidates = [row for row in projection["conclusions"].values()
                  if row.get("scope") == scope and
                  (not actor or _actor_can_read(row, policy, actor)) and
                  v2_state(projection, row, policy) in {"needs_review", "unresolved"}]
    for row in candidates:
        _require_configured_role_separation(row, policy, "judge")
    rows = [row for row in candidates if not _current_judge_recommendation(projection, row, policy)]
    if not rows:
        existing = [projection["recommendations"][row["id"]] for row in candidates
                    if _current_judge_recommendation(projection, row, policy)]
        if existing:
            receipts = sorted({row.get("batch_receipt") for row in existing
                               if row.get("batch_receipt")})
            return {"schema_version": "proofpress/judge-batch-result/v1", "scope": scope,
                    "batch_receipt": receipts[0] if len(receipts) == 1 else None,
                    "batch_receipts": receipts, "verdicts": existing, "idempotent": True}
        raise ValueError("no proposed conclusions require review in scope: " + scope)
    evaluations = {}
    for row in rows:
        current = projection["evaluations"].get(row["id"])
        evaluations[row["id"]] = (current if current and
            current.get("conclusion_digest") == row["digest"] and
            current.get("policy_digest") == policy["digest"] else
            evaluate_v2(row["id"], projection=projection, events=events, policy=policy,
                        actor=actor))
    command = policy["judge"]["command"]
    if not command: raise ValueError("no judge.command configured in .proofpress/policy.json")
    evidence_ids = sorted({ref for row in rows for ref in row["evidence_refs"]})
    packet = {
        "schema_version": "proofpress/judge-batch-request/v1",
        "transaction": {"scope": scope, "conclusion_ids": [row["id"] for row in rows]},
        "conclusions": [{"conclusion": row,
                         "evidence_refs": row["evidence_refs"],
                         "evaluation": {k: v for k, v in evaluations[row["id"]].items() if k != "commit"},
                         **({"reproposal_parent": _reproposal_parent(projection, row)}
                            if _reproposal_parent(projection, row) else {})}
                        for row in rows],
        "evidence_catalog": {ref: projection["evidence"][ref] for ref in evidence_ids},
        "policy": _judge_policy_payload(policy),
    }
    try:
        result = subprocess.run(command, input=json.dumps(packet), text=True,
                                capture_output=True, timeout=float(policy["judge"]["timeout_seconds"]))
    except subprocess.TimeoutExpired as exc:
        raise ValueError("batch judge command timed out") from exc
    if result.returncode: raise ValueError("batch judge command failed: " + result.stderr.strip())
    try: response = json.loads(result.stdout)
    except json.JSONDecodeError as exc: raise ValueError("batch judge returned invalid JSON") from exc
    verdicts = response.get("verdicts")
    if not isinstance(verdicts, list): raise ValueError("batch judge must return verdicts")
    expected = {row["id"] for row in rows}; seen = {}
    for verdict in verdicts:
        cid = verdict.get("conclusion_id")
        if cid not in expected or cid in seen: raise ValueError("batch judge returned unknown or duplicate conclusion_id")
        if verdict.get("recommendation") not in {"accept", "reject", "escalate"}:
            raise ValueError("batch judge recommendation must be accept, reject, or escalate")
        if verdict.get("risk_level") not in {"low", "medium", "high"}:
            raise ValueError("batch judge risk_level must be low, medium, or high")
        if not isinstance(verdict.get("rationale"), str) or not verdict["rationale"].strip():
            raise ValueError("batch judge rationale is required")
        seen[cid] = verdict
    if set(seen) != expected: raise ValueError("batch judge omitted one or more conclusions")
    transaction = append_v2({"type": "judge_batch_completed",
                             "subject_ref": ident({"scope": scope, "conclusions": sorted(expected),
                                                  "policy": policy["digest"], "at": now()}, "jbt_"),
                             "scope": scope, "conclusion_ids": sorted(expected),
                             "policy_digest": policy["digest"], "verdict_count": len(seen),
                             "judge": policy["judge"]["identity"],
                             "judge_config_digest": digest(policy["judge"]),
                             "adapter": response.get("adapter", command[0]), "model": response.get("model")},
                            existing_rows=events)
    recorded, individual = [], []
    for row in rows:
        verdict = seen[row["id"]]
        event = append_v2({"type": "judge_recommended", "subject_ref": row["id"],
                           "conclusion_digest": row["digest"], "policy_digest": policy["digest"],
                           "judge": policy["judge"]["identity"],
                           "judge_config_digest": digest(policy["judge"]),
                           "recommendation": verdict["recommendation"], "rationale": verdict["rationale"],
                           "risk_level": verdict["risk_level"], "batch_receipt": transaction["event_id"],
                           "adapter": response.get("adapter", command[0]), "model": response.get("model")},
                          existing_rows=events)
        recorded.append(event)
        if verdict["risk_level"] == "high" or verdict["recommendation"] == "escalate":
            individual.append({"conclusion_id": row["id"], "trigger": "high_risk" if verdict["risk_level"] == "high" else "escalated",
                               "receipt": judge_v2(row["id"])})
    return {"schema_version": "proofpress/judge-batch-result/v1", "scope": scope,
            "batch_receipt": transaction["event_id"], "verdicts": recorded,
            "individual_reviews": individual}


def _current_judge_recommendation(projection, row, policy):
    recommendation = projection["recommendations"].get(row["id"])
    return bool(recommendation and
                recommendation.get("conclusion_digest") == row["digest"] and
                recommendation.get("policy_digest") == policy["digest"])


def review_v2(cid, decision, reviewer, note=None, request_id=None,
              expected_head=None):
    if decision not in {"admit", "reject", "request_changes"}:
        raise ValueError("review decision must be admit, reject, or request_changes")
    projection = v2_projection()
    duplicate = _idempotent_review(
        projection, cid, request_id, "human_reviewed",
        {"conclusion_admitted", "conclusion_rejected", "conclusion_revision_requested"})
    if duplicate: return duplicate
    _require_expected_head(expected_head)
    row = projection["conclusions"].get(cid)
    if not row: raise ValueError("conclusion not found: " + cid)
    if decision != "admit":
        policy = load_v2_policy()
        conflicts = _active_contradictions(projection, policy)
        if cid in conflicts:
            raise ValueError("active contradiction endpoint may only transition through relation resolve")
    if decision == "admit" and reviewer == row["proposer"]:
        raise ValueError("proposer may not self-approve a conclusion")
    evaluation = evaluate_v2(cid)
    policy = load_v2_policy()
    if decision == "admit" and not evaluation["eligible"]:
        raise ValueError("conclusion is blocked by deterministic policy")
    projection = v2_projection()
    recommendation = projection["recommendations"].get(cid)
    if decision == "admit" and policy["require_judge"]:
        if not recommendation or recommendation.get("policy_digest") != policy["digest"] or recommendation.get("recommendation") != "accept":
            raise ValueError("current policy requires an accepting judge recommendation")
    review_event = append_v2({"type": "human_reviewed", "subject_ref": cid,
                              "decision": decision, "reviewer": reviewer,
                              "identity_basis": "self_asserted", "note": note,
                              "request_id": request_id,
                              "conclusion_digest": row["digest"],
                              "policy_digest": policy["digest"]})
    final_type = ("conclusion_admitted" if decision == "admit" else
                  "conclusion_revision_requested" if decision == "request_changes" else
                  "conclusion_rejected")
    final = append_v2({"type": final_type, "subject_ref": cid,
                       "review_ref": review_event["event_id"],
                       "reviewer": reviewer, "conclusion_digest": row["digest"],
                       "evidence_digests": {ref: projection["evidence"][ref]["digest"] for ref in row["evidence_refs"]},
                       "policy_digest": policy["digest"]})
    return {"ok": True, "review": review_event, "result": final}


def supersede_v2(cid, replacement, reviewer, note=None):
    projection = v2_projection()
    old, new = projection["conclusions"].get(cid), projection["conclusions"].get(replacement)
    if not old or not new: raise ValueError("both conclusions must exist")
    policy = load_v2_policy()
    conflicts = _active_contradictions(projection, policy)
    if cid in conflicts:
        raise ValueError("active contradiction must be superseded through relation resolve")
    return append_v2({"type": "conclusion_superseded", "subject_ref": cid,
                      "superseded_by": replacement, "reviewer": reviewer,
                      "identity_basis": "self_asserted", "note": note})


def _actor_can_read(row, policy, actor):
    return (not actor or "*" in row.get("allowed_actors", ["*"])
            or actor in row.get("allowed_actors", [])) and (
                not actor or "*" in policy["allowed_actors"]
                or actor in policy["allowed_actors"])


def _discovery_text(row):
    applicability = row.get("applicability") or {}
    values = [row.get("statement", ""), applicability.get("title", ""),
              applicability.get("description", "")]
    for field in ("when_relevant", "keywords", "validity_conditions"):
        values.extend(applicability.get(field, []))
    return " ".join(values).lower()


def _context_card(row, task=None):
    applicability = row.get("applicability") or {}
    tokens = set(re.findall(r"[\w-]+", (task or "").lower()))
    haystack = _discovery_text(row)
    matches = sorted(token for token in tokens if len(token) > 2 and token in haystack)
    return {
        "id": row["id"],
        "title": applicability.get("title") or row["statement"],
        "description": applicability.get("description"),
        "when_relevant": applicability.get("when_relevant", []),
        "keywords": applicability.get("keywords", []),
        "validity_conditions": applicability.get("validity_conditions", []),
        "legacy_scope": row.get("scope"),
        "match": {"task": task, "terms": matches, "score": len(matches)},
    }


def discover_context_v2(actor=None, task=None, limit=24):
    """List only visible, eligible context cards, ranked by task-word overlap.

    This is discovery, not semantic authorization: access filtering happens
    before cards are shaped or ranked, and callers still inspect the full
    admission receipt before relying on a selected conclusion.
    """
    if task is not None and (not isinstance(task, str) or not task.strip()):
        raise ValueError("task must be a non-empty string when provided")
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 100:
        raise ValueError("limit must be an integer from 1 to 100")
    projection, policy = v2_projection(), load_v2_policy()
    conflicts = _active_contradictions(projection, policy)
    cards = [_context_card(row, task) for cid, row in projection["conclusions"].items()
             if v2_state(projection, row, policy) == "admitted"
             and _actor_can_read(row, policy, actor) and cid not in conflicts]
    cards.sort(key=lambda card: (-card["match"]["score"], card["title"], card["id"]))
    return {"schema_version": "proofpress/context-discovery/v1",
            "actor": actor, "task": task, "cards": cards[:limit],
            "next_action": "select a card, then read its governed context and receipt before relying on it"}


def context_v2(scope=None, actor=None, task=None, include_blocked_statements=False):
    projection, policy = v2_projection(), load_v2_policy()
    knowledge, blocked, eligible = [], [], {}
    conflicts = _active_contradictions(projection, policy)
    for cid, row in projection["conclusions"].items():
        if scope and row["scope"] != scope: continue
        current = v2_state(projection, row, policy)
        actor_ok = _actor_can_read(row, policy, actor)
        if current == "admitted" and actor_ok and cid not in conflicts:
            eligible[cid] = row
        elif actor and not actor_ok:
            # A caller without disclosure rights must not learn that a
            # conclusion exists from a blocked id, state, or statement.
            continue
        else:
            conflict_rows = conflicts.get(cid, [])
            reason = (conflict_rows[0]["reason"] if conflict_rows else
                      current if current != "admitted" else "actor_not_allowed")
            item = {"id": cid, "reason": reason,
                    "required_action": ("human_conflict_review" if conflict_rows else
                                        "propose_revision" if reason == "needs_revision" else
                                        "reverify" if reason in {"expired", "unresolved", "superseded"} else
                                        "human_review")}
            if conflict_rows:
                item["relation_ids"] = sorted({row["relation_id"] for row in conflict_rows})
                item["peer_ids"] = sorted({row["peer_id"] for row in conflict_rows})
            if include_blocked_statements: item["statement"] = row["statement"]
            blocked.append(item)
    for cid, row in eligible.items():
        admitted = projection["admissions"][cid]
        knowledge.append({**row, "receipt": {"admission_event": admitted["event_id"],
                          "policy_digest": admitted["policy_digest"],
                          "evidence_digests": admitted["evidence_digests"],
                          "conflict_resolutions": _conflict_resolution_receipts(projection, cid)}})
    head = v2_head()
    admitted_ids = {row["id"] for row in knowledge}
    relations = [row for row in projection["relations"].values()
                 if relation_state(projection, row) == "admitted"
                 and row["from"] in admitted_ids and row["to"] in admitted_ids]
    return {"schema_version": CONTEXT_SCHEMA, "ledger_head": head, "scope": scope,
            "actor": actor, "task": task, "policy_digest": policy["digest"],
            "knowledge": knowledge, "relations": relations, "blocked": blocked,
            "next_action": "continue from admitted knowledge; reverify or review blocked conclusions"}


def graph_v2(scope=None, actor=None):
    projection, policy = v2_projection(), load_v2_policy(); nodes, edges = [], []
    wanted = {cid: row for cid, row in projection["conclusions"].items()
              if (not scope or row["scope"] == scope)
              and _actor_can_read(row, policy, actor)}
    evidence_ids = {ref for row in wanted.values() for ref in row["evidence_refs"]}
    pending = list(evidence_ids)
    while pending:
        eid = pending.pop()
        evidence = projection["evidence"].get(eid, {})
        for parent in evidence.get("source_evidence_refs", []):
            if parent not in evidence_ids:
                evidence_ids.add(parent)
                pending.append(parent)
    source_ids = {
        projection["evidence"][eid]["source_ref"]
        for eid in evidence_ids
        if eid in projection["evidence"] and projection["evidence"][eid].get("source_ref")
    }
    for sid in source_ids: nodes.append({"id": sid, "type": "raw", "label": projection["sources"][sid].get("name", Path(projection["sources"][sid].get("path", sid)).name)})
    for eid in evidence_ids:
        if eid in projection["evidence"]:
            evidence = projection["evidence"][eid]
            profile = evidence.get("experiment_profile", {})
            label = ("Experiment " + profile["kind"].replace("_", " ")
                     if profile.get("kind") else "Evidence receipt")
            nodes.append({"id": eid, "type": "evidence", "label": label})
            if evidence.get("source_ref"):
                edges.append({"from": evidence["source_ref"], "to": eid, "type": "bound_as"})
            edges += [{"from": parent, "to": eid, "type": "derived_from"}
                      for parent in evidence.get("source_evidence_refs", [])]
    for cid, row in wanted.items():
        nodes.append({"id": cid, "type": "conclusion", "state": review_state_v2(projection, row),
                      "scope": row["scope"],
                      "applicability": row.get("applicability"), "label": row["statement"],
                      "created_at": row.get("created_at")})
        edges += [{"from": eid, "to": cid, "type": "supports"} for eid in row["evidence_refs"]]
        if row.get("reproposal_of") in wanted:
            edges.append({"from": row["reproposal_of"], "to": cid,
                          "type": "re_proposed_as"})
        review = projection["reviews"].get(cid)
        if review:
            rid = review["event_id"]
            nodes.append({"id": rid, "type": "review", "state": v2_state(projection, row),
                          "label": f"{review['decision']} · {review['reviewer']}"})
            edges.append({"from": cid, "to": rid, "type": "reviewed_by"})
        if cid in projection["admissions"]:
            aid = projection["admissions"][cid]["event_id"]
            nodes.append({"id": aid, "type": "governed", "state": v2_state(projection, row), "label": "Governed knowledge"})
            edges.append({"from": review["event_id"] if review else cid, "to": aid, "type": "admitted_by"})
        if cid in projection["supersessions"]:
            edges.append({"from": cid, "to": projection["supersessions"][cid]["superseded_by"], "type": "superseded_by"})
    for row in projection["relations"].values():
        if row["from"] in wanted and row["to"] in wanted:
            edges.append({"id": row["id"], "from": row["from"], "to": row["to"],
                          "type": row["type"], "state": relation_state(projection, row)})
    return {"nodes": nodes, "edges": edges}


def traverse_graph_v2(seeds, scope=None, actor=None, task=None,
                      max_depth=2, max_claims=48, state="admitted"):
    """Expand admitted claim relations without disclosing ineligible claims."""
    if not seeds: raise ValueError("graph traversal requires at least one seed")
    if max_depth < 0: raise ValueError("max_depth must be non-negative")
    if max_claims < 1: raise ValueError("max_claims must be positive")
    if state not in {"admitted", "staged"}:
        raise ValueError("state must be admitted or staged")
    projection, policy = v2_projection(), load_v2_policy()
    conflicts = _active_contradictions(projection, policy)

    def staged_conclusion(cid, row):
        evaluation = projection["evaluations"].get(cid)
        recommendation = projection["recommendations"].get(cid)
        return bool(evaluation and evaluation.get("eligible")
                    and evaluation.get("conclusion_digest") == row["digest"]
                    and evaluation.get("policy_digest") == policy["digest"]
                    and recommendation and recommendation.get("recommendation") in {"accept", "escalate"}
                    and recommendation.get("conclusion_digest") == row["digest"]
                    and recommendation.get("policy_digest") == policy["digest"])

    def staged_relation(row):
        evaluation = projection["relation_evaluations"].get(row["id"])
        recommendation = projection["relation_recommendations"].get(row["id"])
        return bool(evaluation and evaluation.get("eligible")
                    and evaluation.get("relation_digest") == row["digest"]
                    and evaluation.get("policy_digest") == policy["digest"]
                    and recommendation and recommendation.get("recommendation") in {"accept", "escalate"}
                    and recommendation.get("relation_digest") == row["digest"]
                    and recommendation.get("policy_digest") == policy["digest"])

    def eligibility(cid):
        row = projection["conclusions"].get(cid)
        if not row: return "not_found"
        if scope and row["scope"] != scope: return "scope_mismatch"
        current = v2_state(projection, row, policy)
        if current in {"rejected", "expired", "superseded"}: return current
        if state == "admitted" and current != "admitted": return current
        if state == "staged" and current != "admitted" and not staged_conclusion(cid, row):
            return "not_staged"
        if cid in conflicts: return conflicts[cid][0]["reason"]
        return "eligible" if _actor_can_read(row, policy, actor) else "actor_not_allowed"

    ordered_seeds = list(dict.fromkeys(seeds))
    blocked = []
    eligible_seeds = []
    for cid in ordered_seeds:
        reason = eligibility(cid)
        if reason == "eligible": eligible_seeds.append(cid)
        else: blocked.append({"conclusion_id": cid, "reason": reason,
                              "required_action": ("human_conflict_review"
                                                  if reason.startswith("contradiction_")
                                                  else "human_review")})
    if not eligible_seeds:
        raise ValueError("graph traversal has no eligible seeds")

    eligible_relations = sorted(
        (row for row in projection["relations"].values()
         if (relation_state(projection, row) == "admitted"
             or state == "staged" and staged_relation(row))),
        key=lambda row: row["id"])
    adjacency = {}
    for row in eligible_relations:
        adjacency.setdefault(row["from"], []).append((row["to"], row))
        adjacency.setdefault(row["to"], []).append((row["from"], row))

    selected, selected_set = [], set()
    frontier = []
    for cid in eligible_seeds:
        if len(selected) >= max_claims: break
        selected.append(cid); selected_set.add(cid); frontier.append((cid, 0))
    included_relations, seen_relations, seen_blocked = [], set(), set()
    cursor = 0
    while cursor < len(frontier):
        current, depth = frontier[cursor]; cursor += 1
        if depth >= max_depth: continue
        for neighbor, relation in adjacency.get(current, []):
            reason = eligibility(neighbor)
            if reason != "eligible":
                key = (neighbor, relation["id"], reason)
                if key not in seen_blocked:
                    blocked.append({"conclusion_id": neighbor,
                                    "relation_id": relation["id"],
                                    "relation_type": relation["type"],
                                    "reason": reason,
                                    "required_action": ("human_conflict_review"
                                                        if reason.startswith("contradiction_")
                                                        else "human_review")})
                    seen_blocked.add(key)
                continue
            if relation["id"] not in seen_relations:
                included_relations.append({"id": relation["id"],
                                           "from": relation["from"],
                                           "to": relation["to"],
                                           "type": relation["type"]})
                seen_relations.add(relation["id"])
            if neighbor not in selected_set and len(selected) < max_claims:
                selected.append(neighbor); selected_set.add(neighbor)
                frontier.append((neighbor, depth + 1))

    head = v2_head()
    return {"schema_version": TRAVERSAL_SCHEMA, "ledger_head": head,
            "scope": scope, "actor": actor, "task": task, "state": state,
            "seed_conclusion_ids": ordered_seeds,
            "conclusion_ids": selected, "relations": included_relations,
            "blocked_neighbors": blocked,
            "limits": {"max_depth": max_depth, "max_claims": max_claims}}


def _query_terms(value):
    """Return stable, low-risk terms for deterministic claim selection."""
    return {term for term in re.findall(r"[a-z0-9][a-z0-9_-]{2,}", value.lower())
            if term not in {"about", "after", "before", "claim", "context", "evidence",
                            "from", "have", "into", "that", "the", "this", "what", "with"}}


def _read_corpus_manifest(path):
    """Read the caller-supplied custody boundary; never glob a data room."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = raw.get("sources") if isinstance(raw, dict) else raw
    if not isinstance(rows, list) or not rows:
        raise ValueError("corpus manifest must contain a non-empty sources array")
    out = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"corpus manifest source {index} must be an object")
        source_path = _required_string(row.get("path"), f"corpus.sources[{index}].path")
        uri = _required_string(row.get("uri"), f"corpus.sources[{index}].uri")
        content_digest = _required_digest(row.get("content_digest"), f"corpus.sources[{index}].content_digest")
        media_type = _required_string(row.get("media_type"), f"corpus.sources[{index}].media_type")
        target = Path(source_path)
        if not target.is_file():
            raise ValueError(f"corpus manifest source does not exist: {source_path}")
        actual = "sha256:" + hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != content_digest:
            raise ValueError(f"corpus manifest source digest mismatch: {uri}")
        out.append({"source_id": row.get("source_id") or ident({"uri": uri, "digest": content_digest}, "src_"),
                    "path": str(target.resolve()), "uri": uri,
                    "content_digest": content_digest, "media_type": media_type})
    return out


def _pageindex_discover(query, corpus_manifest, max_discovered, sidecar, config):
    """Call an explicit local sidecar and validate every returned receipt.

    The sidecar receives only the manifest-selected sources.  This function is
    intentionally read-only: a valid retrieval receipt is discovery material,
    not an evidence import or a conclusion proposal.
    """
    sources = _read_corpus_manifest(corpus_manifest)
    command = sidecar or os.environ.get("PROOFPRESS_PAGEINDEX_SIDECAR", "pageindex-sidecar")
    request = {"schema_version": PAGEINDEX_SIDECAR_SCHEMA, "query": query,
               "sources": sources, "config": config, "max_results": max_discovered}
    result = subprocess.run([command], input=json.dumps(request), text=True,
                            capture_output=True, timeout=60)
    if result.returncode:
        detail = result.stderr.strip() or "sidecar returned a non-zero exit status"
        raise ValueError("PageIndex sidecar failed closed: " + detail)
    try:
        response = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("PageIndex sidecar returned invalid JSON") from exc
    if response.get("schema_version") != PAGEINDEX_SIDECAR_SCHEMA:
        raise ValueError("PageIndex sidecar returned an unsupported schema")
    if response.get("fallback_used") is not False:
        raise ValueError("PageIndex sidecar must declare fallback_used=false")
    receipts = response.get("receipts")
    if not isinstance(receipts, list) or len(receipts) > max_discovered:
        raise ValueError("PageIndex sidecar returned an invalid receipt count")
    allowed = {(row["uri"], row["content_digest"]) for row in sources}
    discovered = []
    for raw in receipts:
        receipt = _retrieval_receipt(raw)
        if (receipt["source"]["uri"], receipt["source"]["content_digest"]) not in allowed:
            raise ValueError("PageIndex sidecar disclosed a source outside the corpus manifest")
        discovered.append({"status": "not_governed", "receipt": receipt,
                           "receipt_digest": digest(receipt),
                           "source_navigation": {"uri": receipt["source"]["uri"],
                                                 "locator": receipt["locator"]},
                           "required_action": "import_evidence_then_propose_evaluate_judge_review"})
    return discovered, {"sidecar": response.get("sidecar"),
                        "telemetry": response.get("telemetry", {}),
                        "corpus_manifest_digest": digest([{k: v for k, v in row.items() if k != "path"}
                                                          for row in sources])}


def disclose_v1(query, actor, scope=None, seeds=None, corpus_manifest=None,
                max_depth=2, max_claims=24, max_discovered=6, sidecar=None):
    """Return a bounded packet of governed claims and, only when needed, discovery.

    It is deliberately a read-only API for any caller profile.  Retrieval
    output is segregated from governed context and cannot mutate the ledger.
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("disclosure query must be a non-empty string")
    if not isinstance(actor, str) or not actor.strip():
        raise ValueError("disclosure actor must be a non-empty string")
    if max_discovered < 0 or max_claims < 1 or max_depth < 0:
        raise ValueError("disclosure limits must be non-negative and max_claims positive")
    policy = load_v2_policy()
    context = context_v2(scope, actor, query)
    terms = _query_terms(query)
    scored = []
    for row in context["knowledge"]:
        row_terms = _query_terms(row["statement"] + " " + row.get("scope", ""))
        overlap = len(terms & row_terms)
        if overlap:
            scored.append((-(overlap / max(1, len(terms))), row["id"]))
    selected_seeds = list(dict.fromkeys(seeds or []))
    if not selected_seeds:
        selected_seeds = [cid for _, cid in sorted(scored)[:max_claims]]
    traversal = None
    if selected_seeds:
        traversal = traverse_graph_v2(selected_seeds, scope, actor, query,
                                      max_depth, max_claims, "admitted")
        selected_ids = traversal["conclusion_ids"]
    else:
        selected_ids = []
    visible = {row["id"]: row for row in context["knowledge"]}
    governed = [visible[cid] for cid in selected_ids if cid in visible]
    # Existing context is sufficient only when every meaningful query term is
    # represented in its selected statements.  This keeps PageIndex out of a
    # normal executor path while enabling progressive disclosure for novelty.
    covered = set().union(*(_query_terms(row["statement"]) for row in governed)) if governed else set()
    unmet = bool(terms - covered)
    discovered, discovery_meta = [], None
    gap_terms = sorted(terms - covered)
    gap_id = ident({"query": query, "scope": scope, "terms": gap_terms}, "gap_") if gap_terms else None
    if unmet and corpus_manifest and max_discovered:
        config = {"adapter": "proofpress.pageindex", "version": "1",
                  "requested_model": "deepseek/deepseek-v4-flash",
                  "provider": "proofpress-dev-ai-gateway", "fallback": "forbidden",
                  "max_sections": max_discovered, "max_pages": max_discovered,
                  "toc_check_pages": 1, "max_pages_per_node": 1,
                  "max_tokens_per_node": 2500, "node_summary": False,
                  "document_description": False}
        config["config_digest"] = digest(config)
        discovered, discovery_meta = _pageindex_discover(query, corpus_manifest,
                                                          max_discovered, sidecar, config)
        for item in discovered:
            item["gap_refs"] = [gap_id] if gap_id else []
    lineage = [receipt_v2(cid) for cid in selected_ids]
    gaps = ([] if governed and not unmet else [{"id": gap_id, "kind": "unmet_question",
             "query_terms": gap_terms,
             "required_action": "inspect_discovered_evidence_or_propose_new_conclusion"}])
    blocked = list(context["blocked"])
    if traversal: blocked.extend(traversal["blocked_neighbors"])
    coverage = "covered" if not unmet else ("partial" if governed else "gap")
    return {"schema_version": DISCLOSURE_SCHEMA, "query": query, "actor": actor,
            "scope": scope, "governed_context": governed,
            "coverage": coverage, "lineage": lineage, "discovered_evidence": discovered, "gaps": gaps,
            "blocked": blocked, "actions": ["use_governed_context_for_reliance",
                "treat_discovered_evidence_as_not_governed",
                "use_existing_propose_evaluate_judge_review_path_for_new_claims"],
            "ledger_head": context["ledger_head"], "policy_digest": policy["digest"],
            "config_digest": digest({"max_depth": max_depth, "max_claims": max_claims,
                                      "max_discovered": max_discovered}),
            "traversal": traversal, "discovery": discovery_meta}


def _assimilation_recommendation(packet, candidates, duplicates, conflicts, actor, scope,
                                 recommender=None, config=None):
    """Return a model-shaped recommendation after deterministic gates pass.

    A caller may inject a recommender for a gateway-backed GLM run.  The CLI
    uses PROOFPRESS_ASSIMILATION_RECOMMENDER as an argv command and therefore
    never silently falls back to a hosted or alternate provider.  The small
    deterministic branch is intentionally available to conformance tests only.
    """
    if recommender is not None:
        result = recommender({"packet": packet, "candidates": candidates,
                              "duplicates": duplicates, "conflicts": conflicts,
                              "actor": actor, "scope": scope, "config": config or {}})
        if not isinstance(result, dict):
            raise ValueError("assimilation recommender must return an object")
        return result
    command = os.environ.get("PROOFPRESS_ASSIMILATION_RECOMMENDER")
    if command:
        argv = json.loads(command) if command.lstrip().startswith("[") else [command]
        result = subprocess.run(argv, input=json.dumps({
            "schema_version": "proofpress/assimilation-request/v1",
            "packet": packet, "candidates": candidates,
            "duplicates": duplicates, "conflicts": conflicts,
            "actor": actor, "scope": scope, "config": config or {},
            "model": "zai/glm-5.3-flash", "provider": "proofpress-dev-ai-gateway",
            "fallback": False}), text=True, capture_output=True, timeout=60)
        if result.returncode:
            raise ValueError("assimilation recommender failed closed: " + (result.stderr.strip() or "non-zero exit"))
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise ValueError("assimilation recommender returned invalid JSON") from exc
    raise ValueError("assimilation recommender unavailable; configure PROOFPRESS_ASSIMILATION_RECOMMENDER")


def assimilate_v1(packet, actor, scope=None, gap_ids=None, receipt_digests=None,
                  expected_head=None, submit=False, idempotency_key=None,
                  corpus_manifest=None, recommender=None, config=None):
    """Gate discovered receipts for explicit, non-admitting assimilation.

    The function is fail-closed and performs all validation before invoking a
    recommender.  Dry-run is the default.  Submit may import selected receipts
    or, when the recommendation supplies a candidate statement, create an
    unresolved conclusion and unresolved contradiction relations.  It never
    admits a conclusion or relation automatically.
    """
    if not isinstance(packet, dict) or packet.get("schema_version") != DISCLOSURE_SCHEMA:
        raise ValueError("assimilation packet must be a governed disclosure packet")
    if not isinstance(actor, str) or not actor.strip():
        raise ValueError("assimilation actor must be a non-empty string")
    if scope is not None and packet.get("scope") not in {None, scope}:
        raise ValueError("assimilation scope does not match disclosure packet")
    policy = load_v2_policy()
    if actor not in policy["allowed_actors"] and "*" not in policy["allowed_actors"]:
        raise ValueError("assimilation actor is not allowed by policy")
    packet_digest = digest(packet)
    if submit and idempotency_key:
        prior = next((event for event in v2_events()
                      if event.get("type") == "assimilation_submitted"
                      and event.get("idempotency_key") == idempotency_key), None)
        if prior:
            if prior.get("packet_digest") != packet_digest:
                raise ValueError("IDEMPOTENCY_KEY_CONFLICT")
            return {"schema_version": ASSIMILATION_SCHEMA, "packet_digest": packet_digest,
                    "ledger_head": v2_head(), "actor": actor,
                    "scope": scope or packet.get("scope"), "submitted": True,
                    "idempotent": True, "events_added": 0,
                    "transaction_event": prior.get("event_id")}
    if expected_head is not None and packet.get("ledger_head") != expected_head:
        raise ValueError("STALE_DISCLOSURE_LEDGER_HEAD")
    if packet.get("ledger_head") != v2_head():
        raise ValueError("STALE_LEDGER_HEAD")
    selected_gaps = set(gap_ids or [row.get("id") for row in packet.get("gaps", []) if row.get("id")])
    selected_receipts = set(receipt_digests or [row.get("receipt_digest") for row in packet.get("discovered_evidence", [])])
    if not selected_receipts:
        raise ValueError("assimilation requires at least one discovered receipt")
    packet_gaps = {row.get("id") for row in packet.get("gaps", []) if row.get("id")}
    if not selected_gaps.issubset(packet_gaps):
        raise ValueError("unknown assimilation gap id")
    discovered = {row.get("receipt_digest"): row for row in packet.get("discovered_evidence", [])}
    if any(key not in discovered for key in selected_receipts):
        raise ValueError("unknown assimilation receipt digest")
    if any(discovered[key].get("status") != "not_governed" for key in selected_receipts):
        raise ValueError("only not_governed receipts may be assimilated")
    for key in selected_receipts:
        item = discovered[key]
        if key != digest(item.get("receipt")):
            raise ValueError("discovered receipt digest mismatch")
        if not selected_gaps.intersection(item.get("gap_refs", [])):
            raise ValueError("receipt is not bound to a selected disclosure gap")
        receipt = item.get("receipt") or {}
        _retrieval_receipt({"schema_version": RETRIEVAL_EVIDENCE_SCHEMA,
                            "source": receipt.get("source"),
                            "evidence": {"quote": receipt.get("quote"),
                                         "locator": receipt.get("locator")},
                            "retrieval": receipt.get("retrieval")})
    if not corpus_manifest:
        raise ValueError("assimilation requires corpus manifest for source custody")
    if corpus_manifest:
        # Re-read the caller manifest at the custody boundary.  This catches
        # changed bytes between disclosure and assimilation.
        allowed = {(row["uri"], row["content_digest"]) for row in _read_corpus_manifest(corpus_manifest)}
        for key in selected_receipts:
            receipt = discovered[key]["receipt"]
            if (receipt["source"]["uri"], receipt["source"]["content_digest"]) not in allowed:
                raise ValueError("receipt source is outside the corpus manifest")
    projection = v2_projection()
    existing_receipts = {row.get("retrieval_receipt_digest") for row in projection["evidence"].values()
                         if row.get("kind") == "retrieval_evidence"}
    duplicates = sorted(key for key in selected_receipts if key in existing_receipts)
    candidates = sorted(selected_receipts - set(duplicates))
    conflicts = []
    for key in candidates:
        receipt = discovered[key]["receipt"]
        source_digest = receipt["source"]["content_digest"]
        for claim in projection["conclusions"].values():
            if claim.get("scope") == (scope or packet.get("scope")) and any(
                    projection["evidence"].get(ref, {}).get("source_content_digest") == source_digest
                    for ref in claim.get("evidence_refs", [])):
                conflicts.append({"receipt_digest": key, "conclusion_id": claim["id"],
                                  "reason": "existing claim uses the same source"})
    config = config or {"version": 1, "model": "zai/glm-5.3-flash",
                        "provider": "proofpress-dev-ai-gateway", "fallback": False}
    config_digest = digest(config)
    recommendation = _assimilation_recommendation(packet, candidates, duplicates, conflicts,
                                                   actor, scope or packet.get("scope"),
                                                   recommender, {**config, "config_digest": config_digest})
    allowed_actions = {"ephemeral_only", "recommend_evidence_import",
                       "recommend_claim_proposal", "recommend_conflict_proposal", "escalate"}
    if recommendation.get("action") not in allowed_actions:
        raise ValueError("assimilation recommendation action is invalid")
    candidate_statement = None
    if recommendation.get("action") in {"recommend_claim_proposal", "recommend_conflict_proposal"}:
        candidate_statement = _required_string(recommendation.get("candidate_statement"),
                                               "recommendation.candidate_statement")
        if not candidates:
            raise ValueError("candidate proposal requires non-duplicate discovered evidence")
    if recommendation.get("action") == "recommend_conflict_proposal" and not conflicts:
        raise ValueError("conflict proposal requires a deterministic conflict match")
    result = {"schema_version": ASSIMILATION_SCHEMA,
              "packet_digest": packet_digest, "ledger_head": v2_head(),
              "actor": actor, "scope": scope or packet.get("scope"),
              "gap_ids": sorted(selected_gaps),
              "receipt_digests": sorted(selected_receipts),
              "recommendation": recommendation,
              "duplicates": duplicates, "conflicts": conflicts,
              "gates": {"packet_valid": True, "receipt_binding": True,
                        "source_custody": True, "ledger_head_fresh": True,
                        "deduplication_checked": True, "conflict_checked": True},
              "policy_digest": policy["digest"], "config_digest": config_digest,
              "submitted": False}
    result["recommendation_digest"] = digest(result)
    if not submit:
        return result
    if not idempotency_key or not isinstance(idempotency_key, str) or not idempotency_key.strip():
        raise ValueError("--submit requires an idempotency key")
    expected_idempotency = digest({"packet_digest": result["packet_digest"],
                                   "ledger_head": result["ledger_head"], "actor": actor,
                                   "scope": result["scope"], "receipts": sorted(selected_receipts),
                                   "config_digest": config_digest})
    if idempotency_key != expected_idempotency:
        raise ValueError("idempotency key does not match packet, head, actor, scope, receipts, and config")
    for event in v2_events():
        if event.get("type") == "assimilation_submitted" and event.get("idempotency_key") == idempotency_key:
            if event.get("recommendation_digest") != result["recommendation_digest"]:
                raise ValueError("IDEMPOTENCY_KEY_CONFLICT")
            result["submitted"] = True; result["idempotent"] = True
            result["events_added"] = 0; return result
    submit_actions = {"recommend_evidence_import", "recommend_claim_proposal",
                      "recommend_conflict_proposal"}
    if recommendation.get("action") not in submit_actions:
        raise ValueError("recommendation does not authorize assimilation submit")
    _require_expected_head(result["ledger_head"])
    added = []
    for key in candidates:
        receipt = discovered[key]["receipt"]
        added.extend(_import_retrieval_evidence_v2({
            "schema_version": RETRIEVAL_EVIDENCE_SCHEMA,
            "source": receipt["source"],
            "evidence": {"quote": receipt["quote"], "locator": receipt["locator"]},
            "retrieval": receipt["retrieval"]}))
    proposal = None; proposed_relations = []
    if candidate_statement:
        projection = v2_projection()
        evidence_refs = sorted(row["id"] for row in projection["evidence"].values()
                               if row.get("retrieval_receipt_digest") in candidates)
        if not evidence_refs:
            raise ValueError("candidate proposal could not bind imported evidence")
        proposal = propose_v2(candidate_statement, evidence_refs, result["scope"], actor)
        if recommendation.get("action") == "recommend_conflict_proposal":
            for conclusion_id in sorted({row["conclusion_id"] for row in conflicts}):
                relation = propose_relation_v2(proposal["conclusion"]["id"], conclusion_id,
                                               "contradicts", actor)
                proposed_relations.append(relation["relation"])
    transaction = append_v2({"type": "assimilation_submitted",
                             "subject_ref": ident({"packet": result["packet_digest"], "key": idempotency_key}, "asm_"),
                             "packet_digest": result["packet_digest"],
                             "recommendation_digest": result["recommendation_digest"],
                             "idempotency_key": idempotency_key, "actor": actor,
                             "scope": result["scope"], "receipt_digests": sorted(selected_receipts),
                             "action": recommendation.get("action"), "policy_digest": policy["digest"],
                             "config_digest": config_digest})
    result["submitted"] = True
    result["events_added"] = len(added) + 1 + (1 if proposal else 0) + len(proposed_relations)
    result["transaction_event"] = transaction["event_id"]
    if proposal:
        result["candidate"] = {"id": proposal["conclusion"]["id"], "status": "unresolved"}
    if proposed_relations:
        result["relations"] = [{"id": row["id"], "type": row["type"], "status": "unresolved"}
                               for row in proposed_relations]
    return result


def summary_v2(scope=None, actor=None):
    projection, policy = v2_projection(), load_v2_policy()
    rows = [r for r in projection["conclusions"].values()
            if (not scope or r["scope"] == scope) and _actor_can_read(r, policy, actor)]
    counts = {key: 0 for key in ("needs_review", "needs_revision", "admitted",
                                  "rejected", "superseded", "expired", "unresolved")}
    for row in rows: counts[v2_state(projection, row)] += 1
    return {"total": len(rows), "counts": counts, "scope": scope}


def _reproposal_parent(projection, row):
    parent_id = row.get("reproposal_of")
    parent = projection["conclusions"].get(parent_id)
    if not parent:
        return None
    return {"id": parent_id, "statement": parent["statement"],
            "evidence_refs": parent["evidence_refs"],
            "rejection": projection["rejections"].get(parent_id),
            "review": projection["reviews"].get(parent_id),
            "rejection_reason": (projection["reviews"].get(parent_id) or {}).get("note")}


def receipt_v2(cid, actor=None):
    projection, policy = v2_projection(), load_v2_policy(); row = projection["conclusions"].get(cid)
    if not row or not _actor_can_read(row, policy, actor):
        raise ValueError("conclusion not found: " + cid)
    parent_id = row.get("qualifiers", {}).get("revision_of")
    parent = projection["conclusions"].get(parent_id)
    return {"conclusion": row, "state": review_state_v2(projection, row),
            "revision_request": projection["revision_requests"].get(cid),
            "revision_parent": ({"id": parent_id, "statement": parent["statement"],
                                  "evidence_refs": parent["evidence_refs"],
                                  "review": projection["reviews"].get(parent_id)} if parent else None),
            "revisions": [{"id": candidate["id"], "statement": candidate["statement"],
                           "state": v2_state(projection, candidate)}
                          for candidate in projection["conclusions"].values()
                          if candidate.get("qualifiers", {}).get("revision_of") == cid],
            "reproposal_parent": _reproposal_parent(projection, row),
            "reproposals": [{"id": candidate["id"], "statement": candidate["statement"],
                              "state": v2_state(projection, candidate)}
                             for candidate in projection["conclusions"].values()
                             if candidate.get("reproposal_of") == cid],
            "evidence": [projection["evidence"].get(x) for x in row["evidence_refs"]],
            "evaluation": projection["evaluations"].get(cid),
            "recommendation": projection["recommendations"].get(cid),
            "review": projection["reviews"].get(cid),
            "admission": projection["admissions"].get(cid),
            "rejection": projection["rejections"].get(cid),
            "supersession": projection["supersessions"].get(cid),
            "history": [{"event_id": e["event_id"], "type": e["type"],
                         "actor": e.get("reviewer") or e.get("verifier") or e.get("judge") or e.get("conclusion", {}).get("proposer"),
                         "model": e.get("model"), "note": e.get("note"),
                         "created_at": e["created_at"], "commit": e.get("commit")}
                        for e in projection["events"] if e.get("subject_ref") == cid]}


def relation_receipt_v2(rid):
    projection = v2_projection(); row = projection["relations"].get(rid)
    if not row: raise ValueError("relation not found: " + rid)
    return {"relation": row, "state": relation_state(projection, row),
            "evaluation": projection["relation_evaluations"].get(rid),
            "recommendation": projection["relation_recommendations"].get(rid),
            "review": projection["relation_reviews"].get(rid),
            "admission": projection["relation_admissions"].get(rid),
            "rejection": projection["relation_rejections"].get(rid),
            "resolution": projection["conflict_resolutions"].get(rid),
            "history": [{"event_id": e["event_id"], "type": e["type"],
                         "created_at": e["created_at"], "commit": e.get("commit")}
                        for e in projection["events"] if e.get("subject_ref") == rid]}


def import_v1(path):
    legacy = read(path)
    for row in legacy["source_events"]:
        append_v2({"type": "source_recorded", "subject_ref": row["id"], "record": row,
                   "created_at": row.get("created_at", legacy["created_at"])})
    for row in legacy["evidence"]:
        append_v2({"type": "evidence_bound", "subject_ref": row["id"],
                   "source_ref": row["source_ref"], "evidence": row,
                   "created_at": row.get("created_at", legacy["created_at"])})
    id_map = {}
    for row in legacy["claims"]:
        conclusion = {"id": "knw_" + row["id"].split("_", 1)[-1], "kind": "conclusion",
                      "statement": row["statement"], "evidence_refs": row["evidence_refs"],
                      "artifact_refs": [], "scope": row["scope"], "proposer": row["proposer"],
                      "expires_at": row.get("expires_at"), "allowed_actors": ["*"],
                      "qualifiers": row.get("qualifiers", {}), "created_at": row["created_at"]}
        conclusion["digest"] = _conclusion_digest(conclusion)
        id_map[row["id"]] = conclusion["id"]
        append_v2({"type": "conclusion_proposed", "subject_ref": conclusion["id"],
                   "conclusion": conclusion, "legacy_ref": row["id"], "created_at": row["created_at"]})
        append_v2({"type": "policy_evaluated", "subject_ref": conclusion["id"],
                   "conclusion_digest": conclusion["digest"],
                   "policy_digest": row["policy_snapshot"]["digest"],
                   "checks": row["gate"]["checks"], "eligible": row["gate"]["eligible"],
                   "legacy_ref": row["id"], "created_at": row["created_at"]})
    conclusions = v2_projection()["conclusions"]
    for row in legacy["reviews"]:
        cid = id_map.get(row["claim_ref"])
        if not cid: continue
        if row["kind"] == "policy_recommendation":
            append_v2({"type": "judge_recommended", "subject_ref": cid,
                       "conclusion_digest": conclusions[cid]["digest"],
                       "policy_digest": row["policy_digest"],
                       "recommendation": "escalate" if row["recommendation"] == "unresolved" else row["recommendation"],
                       "rationale": row["rationale"], "adapter": "proofpress-v1-policy-gate",
                       "legacy_ref": row["id"], "created_at": row["created_at"]})
        elif row["kind"] == "human_review":
            append_v2({"type": "human_reviewed", "subject_ref": cid,
                       "decision": {"accept": "admit", "reject": "reject"}.get(row["decision"], "escalate"),
                       "reviewer": row["reviewer"], "identity_basis": row.get("identity_basis", "self_asserted"),
                       "note": row.get("note"), "conclusion_digest": conclusions[cid]["digest"],
                       "policy_digest": next((a["policy_digest"] for a in legacy["admissions"] if a["review_ref"] == row["id"]), legacy["active_policy"]["digest"]),
                       "legacy_ref": row["id"], "created_at": row["created_at"]})
    review_events = {e.get("legacy_ref"): e for e in v2_events() if e["type"] == "human_reviewed"}
    evidence_by_id = v2_projection()["evidence"]
    for row in legacy["admissions"]:
        cid = id_map.get(row["claim_ref"])
        if not cid: continue
        review_event = review_events.get(row["review_ref"])
        final_type = "conclusion_admitted" if row["decision"] == "accept" else "conclusion_rejected"
        append_v2({"type": final_type, "subject_ref": cid,
                   "review_ref": review_event["event_id"] if review_event else row["review_ref"],
                   "reviewer": review_event.get("reviewer") if review_event else "unknown:v1",
                   "conclusion_digest": conclusions[cid]["digest"],
                   "evidence_digests": {ref: evidence_by_id[ref]["digest"] for ref in row["evidence_refs"] if ref in evidence_by_id},
                   "policy_digest": row["policy_digest"], "legacy_ref": row["id"],
                   "created_at": row["created_at"]})
    for row in legacy["supersessions"]:
        cid, replacement = id_map.get(row["claim_ref"]), id_map.get(row["superseded_by"])
        if cid and replacement:
            append_v2({"type": "conclusion_superseded", "subject_ref": cid,
                       "superseded_by": replacement, "reviewer": row["reviewer"],
                       "identity_basis": row.get("identity_basis", "self_asserted"),
                       "note": row.get("note"), "legacy_ref": row["id"],
                       "created_at": row["created_at"]})
    return {"ok": True, "source": path, "events": len(v2_events()), "ref": KNOWLEDGE_REF}


def _markdown_context(packet):
    lines = ["# Trusted context", "", f"Scope: `{packet.get('scope') or 'all'}`", ""]
    for row in packet["knowledge"]:
        lines += [f"## {row['statement']}", "", f"- Conclusion: `{row['id']}`", f"- Evidence: {', '.join(row['evidence_refs'])}", ""]
    if not packet["knowledge"]: lines += ["No admitted knowledge is eligible for this request.", ""]
    return "\n".join(lines)


def _ui_asset():
    return Path(__file__).resolve().parent.parent / "assets" / "local-ui" / "index.html"


class _UIHandler(BaseHTTPRequestHandler):
    token = None
    scope = None
    asset = None

    def log_message(self, fmt, *args): pass
    def _authorized(self):
        parsed = urlparse(self.path)
        query_token = parse_qs(parsed.query).get("token", [None])[0]
        return self.headers.get("X-Proofpress-Token") == self.token or query_token == self.token
    def _json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status); self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def _body(self):
        length = int(self.headers.get("Content-Length", "0")); return json.loads(self.rfile.read(length) or b"{}")
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            if not self._authorized(): return self._json(HTTPStatus.FORBIDDEN, {"error": "invalid session token"})
            html = self.asset.read_text(encoding="utf-8").replace("__PROOFPRESS_TOKEN__", self.token)
            body = html.encode(); self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body); return
        if not self._authorized(): return self._json(HTTPStatus.FORBIDDEN, {"error": "invalid session token"})
        try:
            if parsed.path == "/api/summary": payload = summary_v2(self.scope)
            elif parsed.path == "/api/conclusions":
                p = v2_projection(); payload = [{**r, "state": v2_state(p, r)} for r in p["conclusions"].values() if not self.scope or r["scope"] == self.scope]
            elif parsed.path.startswith("/api/conclusions/"): payload = receipt_v2(parsed.path.rsplit("/", 1)[-1])
            elif parsed.path == "/api/graph": payload = graph_v2(self.scope)
            else: return self._json(404, {"error": "not found"})
            self._json(200, payload)
        except Exception as exc: self._json(400, {"error": str(exc)})
    def do_POST(self):
        if not self._authorized(): return self._json(HTTPStatus.FORBIDDEN, {"error": "invalid session token"})
        try:
            data = self._body(); path = urlparse(self.path).path
            if path == "/api/evaluate": payload = evaluate_v2(data["conclusion"])
            elif path == "/api/judge":
                if data.get("confirmed") is not True: raise ValueError("judge command requires explicit confirmation")
                payload = judge_v2(data["conclusion"])
            elif path == "/api/judge-batch":
                if data.get("confirmed") is not True: raise ValueError("batch judge requires explicit confirmation")
                payload = judge_batch_v2(data.get("scope") or self.scope)
            elif path == "/api/reviews": payload = review_v2(data["conclusion"], data["decision"], data["reviewer"], data.get("note"))
            elif path == "/api/supersessions": payload = supersede_v2(data["conclusion"], data["by"], data["reviewer"], data.get("note"))
            elif path == "/api/context/preview": payload = context_v2(data.get("scope"), data.get("actor"), data.get("task"), True)
            else: return self._json(404, {"error": "not found"})
            self._json(200, payload)
        except Exception as exc: self._json(400, {"error": str(exc)})


def serve_ui(port=7331, scope=None, open_browser=True):
    asset = _ui_asset()
    if not asset.exists(): raise ValueError("local UI asset is missing")
    token = secrets.token_urlsafe(24)
    handler = type("ProofpressUIHandler", (_UIHandler,), {"token": token, "scope": scope, "asset": asset})
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    url = f"http://127.0.0.1:{server.server_port}/?token={token}"
    print("Proofpress local review UI: " + url, flush=True)
    if open_browser: threading.Timer(.2, lambda: webbrowser.open(url)).start()
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()


def seed_demo_v2():
    """Seed a new ledger with synthetic examples for the Local UI."""
    try:
        _git("show-ref", "--verify", "--quiet", KNOWLEDGE_REF)
    except ValueError:
        pass
    else:
        raise ValueError(
            f"{KNOWLEDGE_REF} already exists; run demo only in a new repository"
        )

    fixture = Path(__file__).resolve().parent.parent / "data" / "demo.otlp.json"
    if not fixture.exists():
        raise ValueError("packaged synthetic demo fixture is missing")
    imported = import_evidence_v2(str(fixture))
    baseline, candidate_b, timed_out = imported["evidence"]

    admitted = propose_v2(
        "Candidate B increased synthetic conversion from 12% to 18% "
        "in the recorded experiment.",
        [baseline, candidate_b], "demo", "agent:analyst",
    )["conclusion"]["id"]
    rejected = propose_v2(
        "Candidate C is ready for rollout despite the recorded timeout.",
        [timed_out], "demo", "agent:analyst",
    )["conclusion"]["id"]
    needs_review = propose_v2(
        "The observed Candidate B lift should be revalidated before a "
        "production rollout.",
        [candidate_b], "demo", "agent:analyst",
    )["conclusion"]["id"]

    for conclusion in (admitted, rejected, needs_review):
        evaluate_v2(conclusion)
    review_v2(
        admitted, "admit", "human:product-owner",
        "Synthetic demo admission: reuse only within the demo scope.",
    )
    review_v2(
        rejected, "reject", "human:product-owner",
        "Synthetic demo rejection: the source run timed out.",
    )
    context = context_v2("demo", "agent:successor", None, True)
    return {
        "synthetic": True,
        "scope": "demo",
        "states": {
            "admitted": admitted,
            "needs_review": needs_review,
            "rejected": rejected,
        },
        "eligible_context": [row["id"] for row in context["knowledge"]],
        "blocked": context["blocked"],
        "next": "proofpress ui --scope demo",
    }


def add_flat_cli(sub):
    demo_parser = sub.add_parser(
        "demo", help="seed a new ledger with clearly labeled synthetic UI data")
    demo_parser.set_defaults(f=cmd_flat, flat_cmd="demo")
    evidence_parser = sub.add_parser("evidence", help="bind local evidence to the trust ledger")
    evidence_sub = evidence_parser.add_subparsers(dest="evidence_cmd", required=True)
    evidence_import = evidence_sub.add_parser("import", help="import an artifact, OTLP JSON, retrieval receipt, or TRACE session")
    evidence_import.add_argument("input"); evidence_import.set_defaults(f=cmd_flat)
    propose_parser = sub.add_parser("propose", help="propose an evidence-bound reusable conclusion")
    propose_parser.add_argument("--statement", required=True); propose_parser.add_argument("--evidence", action="append", required=True)
    propose_parser.add_argument("--artifact", action="append", default=[]); propose_parser.add_argument("--scope", help="optional legacy exact-filter metadata")
    propose_parser.add_argument("--proposer", default="agent:proposer"); propose_parser.add_argument("--expires-at")
    propose_parser.add_argument("--applicability", help="JSON discovery card file")
    propose_parser.add_argument("--reproposal-of", help="rejected conclusion this candidate re-proposes")
    propose_parser.add_argument("--profile", choices=["legal", "repo", "experiment"]); propose_parser.add_argument("--qualifiers")
    propose_parser.set_defaults(f=cmd_flat, flat_cmd="propose")
    evaluate_parser = sub.add_parser("evaluate"); evaluate_parser.add_argument("conclusion")
    evaluate_parser.set_defaults(f=cmd_flat, flat_cmd="evaluate")
    judge_parser = sub.add_parser("judge", help="run an advisory policy judge for one conclusion or one scope batch")
    judge_parser.add_argument("conclusion", nargs="?"); judge_parser.add_argument("--scope")
    judge_parser.add_argument("--batch", action="store_true"); judge_parser.set_defaults(f=cmd_flat, flat_cmd="judge")
    review_parser = sub.add_parser("review", help="record the human admission decision")
    review_parser.add_argument("conclusion"); decision = review_parser.add_mutually_exclusive_group(required=True)
    decision.add_argument("--admit", action="store_true"); decision.add_argument("--reject", action="store_true")
    decision.add_argument("--request-changes", action="store_true")
    review_parser.add_argument("--reviewer", required=True); review_parser.add_argument("--note"); review_parser.set_defaults(f=cmd_flat, flat_cmd="review")
    review_parser.add_argument("--request-id"); review_parser.add_argument("--expected-head")
    supersede_parser = sub.add_parser("supersede"); supersede_parser.add_argument("conclusion"); supersede_parser.add_argument("--by", required=True)
    supersede_parser.add_argument("--reviewer", required=True); supersede_parser.add_argument("--note"); supersede_parser.set_defaults(f=cmd_flat, flat_cmd="supersede")
    relation_parser = sub.add_parser("relation", help="propose, evaluate, or review a typed claim relation")
    relation_sub = relation_parser.add_subparsers(dest="relation_cmd", required=True)
    relation_propose = relation_sub.add_parser("propose")
    relation_propose.add_argument("source"); relation_propose.add_argument("--to", required=True)
    relation_propose.add_argument("--type", required=True, choices=sorted(RELATION_TYPES))
    relation_propose.add_argument("--proposer", default="agent:proposer")
    relation_propose.add_argument("--confidence", type=float); relation_propose.add_argument("--qualifiers")
    relation_propose.set_defaults(f=cmd_flat, flat_cmd="relation-propose")
    relation_evaluate = relation_sub.add_parser("evaluate"); relation_evaluate.add_argument("relation")
    relation_evaluate.set_defaults(f=cmd_flat, flat_cmd="relation-evaluate")
    relation_judge = relation_sub.add_parser("judge"); relation_judge.add_argument("relation")
    relation_judge.set_defaults(f=cmd_flat, flat_cmd="relation-judge")
    relation_review = relation_sub.add_parser("review"); relation_review.add_argument("relation")
    relation_decision = relation_review.add_mutually_exclusive_group(required=True)
    relation_decision.add_argument("--admit", action="store_true"); relation_decision.add_argument("--reject", action="store_true")
    relation_decision.add_argument("--request-changes", action="store_true")
    relation_review.add_argument("--reviewer", required=True); relation_review.add_argument("--note")
    relation_review.add_argument("--request-id"); relation_review.add_argument("--expected-head")
    relation_review.set_defaults(f=cmd_flat, flat_cmd="relation-review")
    relation_resolve = relation_sub.add_parser("resolve", help="human-resolve an admitted contradiction")
    relation_resolve.add_argument("relation")
    relation_resolve.add_argument("--disposition", choices=["supersede", "withhold"], required=True)
    relation_resolve.add_argument("--winner")
    relation_resolve.add_argument("--reviewer", required=True); relation_resolve.add_argument("--note")
    relation_resolve.add_argument("--expected-head")
    relation_resolve.set_defaults(f=cmd_flat, flat_cmd="relation-resolve")
    context_parser = sub.add_parser("context", help="materialize only knowledge eligible for the next agent")
    context_parser.add_argument("--scope"); context_parser.add_argument("--actor"); context_parser.add_argument("--task")
    context_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    context_parser.add_argument("--include-blocked-statements", action="store_true"); context_parser.set_defaults(f=cmd_flat, flat_cmd="context")
    graph_parser = sub.add_parser("graph", help="project or traverse the governed claim graph")
    graph_parser.add_argument("--scope"); graph_parser.add_argument("--seed", action="append")
    graph_parser.add_argument("--actor"); graph_parser.add_argument("--task")
    graph_parser.add_argument("--max-depth", type=int, default=2)
    graph_parser.add_argument("--max-claims", type=int, default=48)
    graph_parser.add_argument("--state", choices=["admitted", "staged"], default="admitted")
    graph_parser.set_defaults(f=cmd_flat, flat_cmd="graph")
    disclose_parser = sub.add_parser("disclose", help="return bounded governed context and segregated novel evidence")
    disclose_parser.add_argument("--query", required=True); disclose_parser.add_argument("--actor", required=True)
    disclose_parser.add_argument("--scope"); disclose_parser.add_argument("--seed", action="append")
    disclose_parser.add_argument("--corpus-manifest")
    disclose_parser.add_argument("--sidecar", help="local PageIndex sidecar executable; no hosted fallback")
    disclose_parser.add_argument("--max-depth", type=int, default=2)
    disclose_parser.add_argument("--max-claims", type=int, default=24)
    disclose_parser.add_argument("--max-discovered", type=int, default=6)
    disclose_parser.set_defaults(f=cmd_flat, flat_cmd="disclose")
    assimilate_parser = sub.add_parser("assimilate", help="gate discovered disclosure evidence for explicit, non-admitting import")
    assimilate_parser.add_argument("--packet", required=True, help="JSON governed-disclosure packet")
    assimilate_parser.add_argument("--actor", required=True)
    assimilate_parser.add_argument("--scope")
    assimilate_parser.add_argument("--gap", action="append", dest="gaps")
    assimilate_parser.add_argument("--receipt", action="append", dest="receipts")
    assimilate_parser.add_argument("--corpus-manifest")
    assimilate_parser.add_argument("--expected-head")
    assimilate_parser.add_argument("--idempotency-key")
    assimilate_parser.add_argument("--submit", action="store_true")
    assimilate_parser.add_argument("--recommender", help="local JSON recommender argv; no hosted fallback")
    assimilate_parser.set_defaults(f=cmd_flat, flat_cmd="assimilate")
    catalog_parser = sub.add_parser("catalog", help="build a source-custody-only matter evidence catalog")
    catalog_parser.add_argument("manifest", help="JSON corpus manifest")
    catalog_parser.add_argument("-o", "--output", required=True)
    catalog_parser.add_argument("--cache-dir"); catalog_parser.add_argument("--libreoffice")
    catalog_parser.set_defaults(f=cmd_flat, flat_cmd="catalog")
    ui_parser = sub.add_parser("ui", help="open the local review and context UI")
    ui_parser.add_argument("--scope"); ui_parser.add_argument("--port", type=int, default=7331); ui_parser.add_argument("--no-open", action="store_true")
    ui_parser.set_defaults(f=cmd_flat, flat_cmd="ui")
    service_parser = sub.add_parser(
        "service", help="run the loopback-only local operation service")
    service_parser.add_argument("--workspace", required=True,
                                help="explicit Git repository root")
    service_parser.add_argument("--host", default="127.0.0.1")
    service_parser.add_argument("--port", type=int, default=7332)
    service_parser.add_argument("--token-env", default="PROOFPRESS_LOCAL_TOKEN")
    service_parser.set_defaults(f=cmd_flat, flat_cmd="service")
    migration = sub.add_parser("import-v1", help="one-way import of a 0.4 file-backed knowledge ledger")
    migration.add_argument("ledger"); migration.set_defaults(f=cmd_flat, flat_cmd="import-v1")


def local_operation_capabilities():
    """Describe only the operations implemented by this local contract."""
    return {
        "request_schema": LOCAL_OPERATION_SCHEMA,
        "result_schema": LOCAL_OPERATION_RESULT_SCHEMA,
        "contract_status": LOCAL_OPERATION_CONTRACT_STATUS,
        "transport": "in_process",
        "clients": ["python_sdk"],
        "profiles": {
            "conclusion": ["legal", "repo", "experiment"],
            "evidence": ["experiment"],
            "experiment_schema": proofpress_experiment.PROFILE,
        },
        "idempotency": {
            "field": "idempotency_key",
            "maximum_length": 128,
            "persistence": "workspace_local",
            "conflicting_reuse": "idempotency_conflict",
        },
        "operations": [
            {
                "name": name,
                "mutates": spec["mutates"],
                "required_parameters": list(spec["required"]),
                "optional_parameters": list(spec["optional"]),
                "replay_semantics": spec["replay_semantics"],
            }
            for name, spec in LOCAL_OPERATION_SPECS.items()
        ],
        "not_available": ["localhost_http", "mcp", "cloud"],
    }


def _local_operation_envelope(ok, operation=None, request_id=None, result=None,
                              error=None):
    envelope = {
        "schema_version": LOCAL_OPERATION_RESULT_SCHEMA,
        "contract_status": LOCAL_OPERATION_CONTRACT_STATUS,
        "ok": ok,
        "operation": operation,
    }
    if request_id is not None:
        envelope["request_id"] = request_id
    if ok:
        envelope["result"] = result
    else:
        envelope["error"] = error
    return envelope


def _local_operation_error(code, message, operation=None, request_id=None,
                           retryable=False, details=None):
    error = {"code": code, "message": message, "retryable": retryable}
    if details:
        error["details"] = details
    return _local_operation_envelope(
        False, operation=operation, request_id=request_id, error=error)


def _local_idempotency_records():
    store = current_event_store()
    if hasattr(store, "idempotency_records"):
        return store.idempotency_records()
    path = Path(LOCAL_IDEMPOTENCY_PATH)
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("local idempotency store is unreadable") from exc
    if not isinstance(value, dict):
        raise ValueError("local idempotency store must be an object")
    return value


def _store_local_idempotency(key, fingerprint, operation, result):
    store = current_event_store()
    if hasattr(store, "store_idempotency"):
        store.store_idempotency(key, fingerprint, operation, result, now())
        return
    path = Path(LOCAL_IDEMPOTENCY_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    records = _local_idempotency_records()
    records[key] = {
        "request_fingerprint": fingerprint,
        "operation": operation,
        "result": result,
        "recorded_at": now(),
    }
    handle, temporary = tempfile.mkstemp(prefix="idempotency-", suffix=".json",
                                         dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(records, stream, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))
            stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _execute_local_operation(request):
    """Execute one internal-alpha operation over the local governance kernel.

    This is the shared seam for the CLI and future local transports. It is not
    a public SDK or network API: callers must still run inside the selected Git
    workspace, and all writes retain the existing append-only ledger semantics.
    """
    if not isinstance(request, dict):
        return _local_operation_error(
            "invalid_request", "local operation request must be an object")
    operation = request.get("operation")
    request_id = request.get("request_id")
    idempotency_key = request.get("idempotency_key")
    if request.get("schema_version") != LOCAL_OPERATION_SCHEMA:
        return _local_operation_error(
            "unsupported_schema_version",
            f"local operation schema_version must be {LOCAL_OPERATION_SCHEMA}",
            operation=operation, request_id=request_id,
            details={"supported": [LOCAL_OPERATION_SCHEMA]})
    unknown = sorted(set(request) - {
        "schema_version", "operation", "parameters", "request_id",
        "idempotency_key"})
    if unknown:
        return _local_operation_error(
            "unknown_request_fields",
            "unknown local operation fields: " + ", ".join(unknown),
            operation=operation, request_id=request_id,
            details={"fields": unknown})
    if request_id is not None and (not isinstance(request_id, str) or
                                   not request_id or len(request_id) > 128):
        return _local_operation_error(
            "invalid_request_id",
            "local operation request_id must be a non-empty string of at most 128 characters",
            operation=operation)
    if idempotency_key is not None and (
            not isinstance(idempotency_key, str) or not idempotency_key or
            len(idempotency_key) > 128):
        return _local_operation_error(
            "invalid_idempotency_key",
            "idempotency_key must be a non-empty string of at most 128 characters",
            operation=operation, request_id=request_id)
    parameters = request.get("parameters")
    if not isinstance(operation, str) or not operation:
        return _local_operation_error(
            "missing_operation", "local operation name is required",
            request_id=request_id)
    if not isinstance(parameters, dict):
        return _local_operation_error(
            "invalid_parameters", "local operation parameters must be an object",
            operation=operation, request_id=request_id)
    spec = LOCAL_OPERATION_SPECS.get(operation)
    if spec is None:
        return _local_operation_error(
            "unsupported_operation", "unsupported local operation: " + operation,
            operation=operation, request_id=request_id)
    required = set(spec["required"])
    allowed = required | set(spec["optional"])
    missing = sorted(key for key in required if key not in parameters)
    extra = sorted(set(parameters) - allowed)
    if missing or extra:
        details = {}
        if missing:
            details["missing"] = missing
        if extra:
            details["unknown"] = extra
        return _local_operation_error(
            "invalid_parameters", f"invalid parameters for {operation}",
            operation=operation, request_id=request_id, details=details)

    fingerprint = digest({"operation": operation, "parameters": parameters})
    if idempotency_key is not None:
        try:
            prior = _local_idempotency_records().get(idempotency_key)
        except ValueError as exc:
            return _local_operation_error(
                "idempotency_store_invalid", str(exc), operation=operation,
                request_id=request_id)
        if prior:
            if prior.get("request_fingerprint") != fingerprint:
                return _local_operation_error(
                    "idempotency_conflict",
                    "idempotency_key was already used for a different request",
                    operation=operation, request_id=request_id,
                    details={"prior_operation": prior.get("operation")})
            envelope = _local_operation_envelope(
                True, operation=operation, request_id=request_id,
                result=prior.get("result"))
            envelope["idempotent_replay"] = True
            return envelope

    try:
        if operation == "capabilities.get":
            result = local_operation_capabilities()
        elif operation == "configuration.get":
            result = governance_configuration()
        elif operation == "evidence.import":
            result = import_evidence_v2(parameters["path"])
        elif operation == "evidence.submit":
            result = submit_evidence_v2(
                parameters["payload"], parameters.get("profile"))
        elif operation == "conclusion.propose":
            result = propose_v2(
                parameters["statement"], parameters["evidence_refs"],
                parameters.get("scope"), parameters["proposer"],
                parameters.get("expires_at"), parameters.get("artifact_refs"),
                parameters.get("applicability"), parameters.get("qualifiers"),
                parameters.get("profile"), parameters.get("reproposal_of"))
        elif operation == "conclusion.evaluate":
            result = evaluate_v2(parameters["conclusion_id"], actor=parameters.get("actor"))
        elif operation == "conclusion.judge":
            result = judge_v2(parameters["conclusion_id"], actor=parameters.get("actor"))
        elif operation == "conclusion.judge_batch":
            result = judge_batch_v2(parameters["scope"], actor=parameters.get("actor"))
        elif operation == "conclusion.review":
            result = review_v2(
                parameters["conclusion_id"], parameters["decision"],
                parameters["reviewer"], parameters.get("note"),
                parameters.get("request_id"), parameters.get("expected_head"))
        elif operation == "conclusion.supersede":
            result = supersede_v2(
                parameters["conclusion_id"], parameters["replacement_id"],
                parameters["reviewer"], parameters.get("note"))
        elif operation == "relation.propose":
            result = propose_relation_v2(
                parameters["source_id"], parameters["target_id"],
                parameters["relation_type"], parameters["proposer"],
                parameters.get("confidence"), parameters.get("qualifiers"),
                parameters.get("actor"))
        elif operation == "relation.evaluate":
            result = evaluate_relation_v2(parameters["relation_id"], actor=parameters.get("actor"))
        elif operation == "relation.judge":
            result = judge_relation_v2(parameters["relation_id"], actor=parameters.get("actor"))
        elif operation == "relation.review":
            result = review_relation_v2(
                parameters["relation_id"], parameters["decision"],
                parameters["reviewer"], parameters.get("note"),
                parameters.get("request_id"), parameters.get("expected_head"))
        elif operation == "relation.resolve":
            result = resolve_contradiction_v2(
                parameters["relation_id"], parameters["disposition"],
                parameters["reviewer"], parameters.get("winner"),
                parameters.get("note"), parameters.get("expected_head"))
        elif operation == "graph.get":
            result = graph_v2(parameters.get("scope"), parameters.get("actor"))
        elif operation == "graph.traverse":
            result = traverse_graph_v2(
                parameters["seed_ids"], parameters.get("scope"),
                parameters.get("actor"), parameters.get("task"),
                parameters.get("max_depth", 2),
                parameters.get("max_claims", 48),
                parameters.get("state", "admitted"))
        elif operation == "review.summary":
            result = summary_v2(parameters.get("scope"), parameters.get("actor"))
        elif operation == "review.receipt":
            result = receipt_v2(parameters["conclusion_id"], parameters.get("actor"))
        elif operation == "context.get":
            result = context_v2(
                parameters.get("scope"), parameters.get("actor"),
                parameters.get("task"),
                bool(parameters.get("include_blocked_statements", False)))
        elif operation == "context.discover":
            result = discover_context_v2(
                parameters.get("actor"), parameters.get("task"),
                parameters.get("limit", 24))
        else:
            raise ValueError("unsupported local operation: " + operation)
    except ValueError as exc:
        message = str(exc)
        if message == "STALE_LEDGER_HEAD":
            code = "ledger_head_conflict"
        elif message.startswith("evidence input not found:"):
            code = "resource_not_found"
        else:
            code = "operation_rejected"
        return _local_operation_error(
            code, message, operation=operation, request_id=request_id,
            retryable=code == "ledger_head_conflict")
    except OSError as exc:
        return _local_operation_error(
            "operation_io_error", str(exc), operation=operation,
            request_id=request_id)
    if idempotency_key is not None and spec["mutates"]:
        try:
            _store_local_idempotency(
                idempotency_key, fingerprint, operation, result)
        except (OSError, ValueError) as exc:
            return _local_operation_error(
                "idempotency_store_write_failed", str(exc),
                operation=operation, request_id=request_id)
    return _local_operation_envelope(
        True, operation=operation, request_id=request_id, result=result)


class _RollbackOperation(Exception):
    def __init__(self, envelope):
        self.envelope = envelope


def execute_local_operation(request):
    """Execute atomically when the selected backend provides transactions."""
    store = current_event_store()
    if not hasattr(store, "transaction"):
        return _execute_local_operation(request)
    try:
        with store.transaction():
            envelope = _execute_local_operation(request)
            if not envelope["ok"]:
                raise _RollbackOperation(envelope)
            return envelope
    except _RollbackOperation as rollback:
        return rollback.envelope


def _local_request(operation, parameters):
    envelope = execute_local_operation({
        "schema_version": LOCAL_OPERATION_SCHEMA,
        "operation": operation,
        "parameters": parameters,
    })
    if not envelope["ok"]:
        raise ValueError(envelope["error"]["message"])
    return envelope["result"]


def cmd_flat(a):
    command = getattr(a, "flat_cmd", None) or ("evidence-import" if getattr(a, "evidence_cmd", None) == "import" else None)
    if command == "demo": out = seed_demo_v2()
    elif command == "evidence-import":
        out = _local_request("evidence.import", {"path": a.input})
    elif command == "propose":
        qualifiers = json.loads(Path(a.qualifiers).read_text(encoding="utf-8")) if a.qualifiers else None
        applicability = json.loads(Path(a.applicability).read_text(encoding="utf-8")) if a.applicability else None
        out = _local_request("conclusion.propose", {
            "statement": a.statement, "evidence_refs": a.evidence,
            "scope": a.scope, "proposer": a.proposer,
            "expires_at": a.expires_at, "artifact_refs": a.artifact,
            "applicability": applicability, "reproposal_of": a.reproposal_of,
            "qualifiers": qualifiers,
            "profile": a.profile,
        })
    elif command == "evaluate":
        out = _local_request("conclusion.evaluate", {
            "conclusion_id": a.conclusion,
        })
    elif command == "judge":
        if a.batch or a.scope:
            out = _local_request("conclusion.judge_batch", {"scope": a.scope})
        elif a.conclusion:
            out = _local_request("conclusion.judge", {"conclusion_id": a.conclusion})
        else: raise ValueError("judge requires a conclusion or --batch --scope")
    elif command == "review":
        decision = "admit" if a.admit else "request_changes" if a.request_changes else "reject"
        out = _local_request("conclusion.review", {
            "conclusion_id": a.conclusion, "decision": decision,
            "reviewer": a.reviewer, "note": a.note,
            "request_id": a.request_id, "expected_head": a.expected_head,
        })
    elif command == "supersede":
        out = _local_request("conclusion.supersede", {
            "conclusion_id": a.conclusion, "replacement_id": a.by,
            "reviewer": a.reviewer, "note": a.note,
        })
    elif command == "relation-propose":
        qualifiers = json.loads(Path(a.qualifiers).read_text(encoding="utf-8")) if a.qualifiers else None
        out = _local_request("relation.propose", {
            "source_id": a.source, "target_id": a.to,
            "relation_type": a.type, "proposer": a.proposer,
            "confidence": a.confidence, "qualifiers": qualifiers,
        })
    elif command == "relation-evaluate":
        out = _local_request("relation.evaluate", {"relation_id": a.relation})
    elif command == "relation-judge":
        out = _local_request("relation.judge", {"relation_id": a.relation})
    elif command == "relation-review":
        decision = "admit" if a.admit else "request_changes" if a.request_changes else "reject"
        out = _local_request("relation.review", {
            "relation_id": a.relation, "decision": decision,
            "reviewer": a.reviewer, "note": a.note,
            "request_id": a.request_id, "expected_head": a.expected_head,
        })
    elif command == "relation-resolve":
        out = _local_request("relation.resolve", {
            "relation_id": a.relation, "disposition": a.disposition,
            "reviewer": a.reviewer, "winner": a.winner, "note": a.note,
            "expected_head": a.expected_head,
        })
    elif command == "graph":
        out = (_local_request("graph.traverse", {
                   "seed_ids": a.seed, "scope": a.scope, "actor": a.actor,
                   "task": a.task, "max_depth": a.max_depth,
                   "max_claims": a.max_claims, "state": a.state,
               }) if a.seed else
               _local_request("graph.get", {"scope": a.scope}))
    elif command == "context":
        out = _local_request("context.get", {
            "scope": a.scope, "actor": a.actor, "task": a.task,
            "include_blocked_statements": a.include_blocked_statements,
        })
        if a.format == "markdown": print(_markdown_context(out)); return
    elif command == "disclose":
        out = disclose_v1(a.query, a.actor, a.scope, a.seed, a.corpus_manifest,
                          a.max_depth, a.max_claims, a.max_discovered, a.sidecar)
    elif command == "assimilate":
        packet = json.loads(Path(a.packet).read_text(encoding="utf-8"))
        previous = os.environ.get("PROOFPRESS_ASSIMILATION_RECOMMENDER")
        if a.recommender:
            os.environ["PROOFPRESS_ASSIMILATION_RECOMMENDER"] = a.recommender
        try:
            out = assimilate_v1(packet, a.actor, a.scope, a.gaps, a.receipts,
                                a.expected_head, a.submit, a.idempotency_key,
                                a.corpus_manifest)
        finally:
            if a.recommender is not None:
                if previous is None: os.environ.pop("PROOFPRESS_ASSIMILATION_RECOMMENDER", None)
                else: os.environ["PROOFPRESS_ASSIMILATION_RECOMMENDER"] = previous
    elif command == "catalog":
        from proofpress_matter_catalog import build_catalog
        catalog = build_catalog(a.manifest, cache_dir=a.cache_dir, libreoffice=a.libreoffice)
        Path(a.output).write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        out = {"ok": True, "schema_version": "proofpress/matter-evidence-catalog/v1",
               "sources": len(catalog["sources"]), "representations": len(catalog["representations"]),
               "catalog_digest": catalog["catalog_digest"], "output": a.output}
    elif command == "ui": serve_ui(a.port, a.scope, not a.no_open); return
    elif command == "service":
        from proofpress.transports.http import run_from_args
        run_from_args(a); return
    elif command == "import-v1": out = import_v1(a.ledger)
    else: raise ValueError("unknown local MVP command")
    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))

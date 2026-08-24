#!/usr/bin/env python3
"""File-backed admission ledger: telemetry is input; admitted claims are context."""
from __future__ import annotations

import argparse, hashlib, json, os, secrets, subprocess, tempfile, threading, webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "proofpress/knowledge-ledger/v1"
ALLOWED = {"service.name","experiment.id","experiment_id","experimentId","experiment.variant","variant","metric.conversion_rate","conversion_rate","metric.value","experiment.outcome","outcome","sample.size","sample_size"}
DEFAULT_POLICY = {"id":"mvp-evidence-and-completeness","version":1,"min_sample_size":1,"require_guardrail_pass":False,"attribute_allowlist_version":"v1"}

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
POLICY_PATH = ".proofpress/policy.json"
DEFAULT_POLICY_V2 = {
    "id": "proofpress-local-default",
    "version": 1,
    "min_evidence": 1,
    "require_judge": False,
    "allowed_actors": ["*"],
    "judge": {"command": [], "timeout_seconds": 30},
}


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
    try:
        commits = _git("rev-list", "--reverse", KNOWLEDGE_REF).split()
    except ValueError:
        return []
    rows = []
    for commit in commits:
        row = json.loads(_git("show", f"{commit}:event.json"))
        row["commit"] = commit
        rows.append(row)
    return rows


def append_v2(event):
    event = {"schema_version": EVENT_SCHEMA, **event}
    existing_rows = v2_events()
    immutable = {"source_recorded": "record", "evidence_bound": "evidence",
                 "conclusion_proposed": "conclusion"}
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
    blob = _git("hash-object", "-w", "--stdin",
                input=json.dumps(event, ensure_ascii=False, sort_keys=True,
                                 indent=2) + "\n").strip()
    tree = _git("mktree", input=f"100644 blob {blob}\tevent.json\n").strip()
    parent = []
    try:
        parent = ["-p", _git("rev-parse", KNOWLEDGE_REF).strip()]
    except ValueError:
        pass
    commit = _git("commit-tree", tree, *parent, "-m",
                  f"{event['type']}: {event.get('subject_ref', event['event_id'])}").strip()
    _git("update-ref", KNOWLEDGE_REF, commit)
    return {**event, "commit": commit}


def load_v2_policy():
    raw = {}
    path = Path(POLICY_PATH)
    if path.exists():
        raw = json.loads(path.read_text(encoding="utf-8"))
    item = {**DEFAULT_POLICY_V2, **raw}
    item["judge"] = {**DEFAULT_POLICY_V2["judge"], **(raw.get("judge") or {})}
    command = item["judge"].get("command", [])
    if not isinstance(command, list) or not all(isinstance(x, str) for x in command):
        raise ValueError("policy judge.command must be an argv array")
    item["digest"] = digest({k: v for k, v in item.items() if k != "digest"})
    return item


def v2_projection(events=None):
    events = v2_events() if events is None else events
    result = {
        "sources": {}, "evidence": {}, "conclusions": {}, "evaluations": {},
        "recommendations": {}, "reviews": {}, "admissions": {},
        "rejections": {}, "supersessions": {}, "events": events,
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
        elif kind == "conclusion_superseded": result["supersessions"][subject] = event
    return result


def _conclusion_digest(row):
    return digest({k: v for k, v in row.items() if k != "digest"})


def v2_state(projection, conclusion, policy=None):
    cid = conclusion["id"]
    policy = policy or load_v2_policy()
    if cid in projection["supersessions"]: return "superseded"
    if conclusion.get("expires_at") and conclusion["expires_at"] <= now(): return "expired"
    if cid in projection["rejections"]: return "rejected"
    admitted = projection["admissions"].get(cid)
    if not admitted: return "needs_review"
    if admitted.get("policy_digest") != policy["digest"]: return "unresolved"
    if admitted.get("conclusion_digest") != conclusion["digest"]: return "unresolved"
    return "admitted"


def import_evidence_v2(path):
    target = Path(path)
    if not target.exists(): raise ValueError(f"evidence input not found: {path}")
    created = []
    if target.suffix.lower() == ".json":
        payload = json.loads(target.read_text(encoding="utf-8"))
        span_rows = spans(payload)
    else:
        span_rows = []
    if span_rows:
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
    return {"ok": True, "events_added": len(created),
            "evidence": sorted(projection["evidence"]), "ref": KNOWLEDGE_REF}


def propose_v2(statement, evidence_refs, scope, proposer, expires_at=None,
               artifact_refs=None, allowed_actors=None, qualifiers=None):
    projection = v2_projection()
    missing = [ref for ref in evidence_refs if ref not in projection["evidence"]]
    if missing: raise ValueError("unknown evidence: " + ", ".join(missing))
    row = {
        "id": ident({"statement": statement, "evidence": sorted(evidence_refs),
                    "scope": scope}, "knw_"),
        "kind": "conclusion", "statement": statement,
        "evidence_refs": sorted(set(evidence_refs)),
        "artifact_refs": sorted(set(artifact_refs or [])),
        "scope": scope, "proposer": proposer, "expires_at": expires_at,
        "allowed_actors": allowed_actors or ["*"],
        "qualifiers": qualifiers or {}, "created_at": now(),
    }
    row["digest"] = _conclusion_digest(row)
    event = append_v2({"type": "conclusion_proposed", "subject_ref": row["id"],
                       "conclusion": row})
    return {"ok": True, "conclusion": row, "event_id": event["event_id"]}


def evaluate_v2(cid):
    projection = v2_projection()
    row = projection["conclusions"].get(cid)
    if not row: raise ValueError("conclusion not found: " + cid)
    policy = load_v2_policy()
    evidence_ok = [ref for ref in row["evidence_refs"] if ref in projection["evidence"]]
    checks = {
        "evidence_present": len(evidence_ok) >= int(policy["min_evidence"]),
        "evidence_integrity": all(projection["evidence"][ref].get("digest") ==
                                  digest({k: v for k, v in projection["evidence"][ref].items() if k != "digest"})
                                  for ref in evidence_ok),
        "not_expired": not row.get("expires_at") or row["expires_at"] > now(),
        "not_superseded": cid not in projection["supersessions"],
        "scope_present": bool(row.get("scope")),
    }
    event = append_v2({"type": "policy_evaluated", "subject_ref": cid,
                       "conclusion_digest": row["digest"],
                       "policy_digest": policy["digest"], "checks": checks,
                       "eligible": all(checks.values())})
    return event


def judge_v2(cid):
    evaluation = evaluate_v2(cid)
    policy = load_v2_policy()
    command = policy["judge"]["command"]
    if not command: raise ValueError("no judge.command configured in .proofpress/policy.json")
    projection = v2_projection()
    row = projection["conclusions"][cid]
    packet = {"schema_version": "proofpress/judge-request/v1", "conclusion": row,
              "evidence": [projection["evidence"][x] for x in row["evidence_refs"]],
              "evaluation": {k: v for k, v in evaluation.items() if k != "commit"},
              "policy": policy}
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
                       "recommendation": verdict["recommendation"],
                       "rationale": verdict["rationale"],
                       "adapter": verdict.get("adapter", command[0]),
                       "model": verdict.get("model")})
    return event


def judge_batch_v2(scope):
    if not scope: raise ValueError("batch judge requires --scope")
    projection = v2_projection()
    rows = [row for row in projection["conclusions"].values()
            if row.get("scope") == scope and v2_state(projection, row) in {"needs_review", "unresolved"}]
    if not rows: raise ValueError("no proposed conclusions require review in scope: " + scope)
    evaluations = {row["id"]: evaluate_v2(row["id"]) for row in rows}
    projection = v2_projection(); policy = load_v2_policy(); command = policy["judge"]["command"]
    if not command: raise ValueError("no judge.command configured in .proofpress/policy.json")
    evidence_ids = sorted({ref for row in rows for ref in row["evidence_refs"]})
    packet = {
        "schema_version": "proofpress/judge-batch-request/v1",
        "transaction": {"scope": scope, "conclusion_ids": [row["id"] for row in rows]},
        "conclusions": [{"conclusion": row,
                         "evidence_refs": row["evidence_refs"],
                         "evaluation": {k: v for k, v in evaluations[row["id"]].items() if k != "commit"}}
                        for row in rows],
        "evidence_catalog": {ref: projection["evidence"][ref] for ref in evidence_ids},
        "policy": policy,
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
    transaction = append_v2({"type": "judge_batch_completed", "subject_ref": ident({"scope": scope,
                            "conclusions": sorted(expected), "policy": policy["digest"], "at": now()}, "jbt_"),
                            "scope": scope, "conclusion_ids": sorted(expected),
                            "policy_digest": policy["digest"], "verdict_count": len(seen),
                            "adapter": response.get("adapter", command[0]), "model": response.get("model")})
    recorded, individual = [], []
    for row in rows:
        verdict = seen[row["id"]]
        event = append_v2({"type": "judge_recommended", "subject_ref": row["id"],
                           "conclusion_digest": row["digest"], "policy_digest": policy["digest"],
                           "recommendation": verdict["recommendation"], "rationale": verdict["rationale"],
                           "risk_level": verdict["risk_level"], "batch_receipt": transaction["event_id"],
                           "adapter": response.get("adapter", command[0]), "model": response.get("model")})
        recorded.append(event)
        if verdict["risk_level"] == "high" or verdict["recommendation"] == "escalate":
            individual.append({"conclusion_id": row["id"], "trigger": "high_risk" if verdict["risk_level"] == "high" else "escalated",
                               "receipt": judge_v2(row["id"])})
    return {"schema_version": "proofpress/judge-batch-result/v1", "scope": scope,
            "batch_receipt": transaction["event_id"], "verdicts": recorded,
            "individual_reviews": individual}


def review_v2(cid, decision, reviewer, note=None):
    projection = v2_projection()
    row = projection["conclusions"].get(cid)
    if not row: raise ValueError("conclusion not found: " + cid)
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
                              "conclusion_digest": row["digest"],
                              "policy_digest": policy["digest"]})
    final_type = "conclusion_admitted" if decision == "admit" else "conclusion_rejected"
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
    if old["scope"] != new["scope"]: raise ValueError("conclusions from different scopes cannot supersede each other")
    return append_v2({"type": "conclusion_superseded", "subject_ref": cid,
                      "superseded_by": replacement, "reviewer": reviewer,
                      "identity_basis": "self_asserted", "note": note})


def context_v2(scope=None, actor=None, task=None, include_blocked_statements=False):
    projection, policy = v2_projection(), load_v2_policy()
    knowledge, blocked = [], []
    for cid, row in projection["conclusions"].items():
        if scope and row["scope"] != scope: continue
        current = v2_state(projection, row, policy)
        actor_ok = not actor or "*" in row.get("allowed_actors", ["*"]) or actor in row.get("allowed_actors", [])
        policy_actor_ok = not actor or "*" in policy["allowed_actors"] or actor in policy["allowed_actors"]
        if current == "admitted" and actor_ok and policy_actor_ok:
            admitted = projection["admissions"][cid]
            knowledge.append({**row, "receipt": {"admission_event": admitted["event_id"],
                              "policy_digest": admitted["policy_digest"],
                              "evidence_digests": admitted["evidence_digests"]}})
        else:
            reason = current if current != "admitted" else "actor_not_allowed"
            item = {"id": cid, "reason": reason,
                    "required_action": "reverify" if reason in {"expired", "unresolved", "superseded"} else "human_review"}
            if include_blocked_statements: item["statement"] = row["statement"]
            blocked.append(item)
    head = None
    try: head = _git("rev-parse", KNOWLEDGE_REF).strip()
    except ValueError: pass
    return {"schema_version": CONTEXT_SCHEMA, "ledger_head": head, "scope": scope,
            "actor": actor, "task": task, "policy_digest": policy["digest"],
            "knowledge": knowledge, "blocked": blocked,
            "next_action": "continue from admitted knowledge; reverify or review blocked conclusions"}


def graph_v2(scope=None):
    projection = v2_projection(); nodes, edges = [], []
    wanted = {cid: row for cid, row in projection["conclusions"].items() if not scope or row["scope"] == scope}
    evidence_ids = {ref for row in wanted.values() for ref in row["evidence_refs"]}
    source_ids = {projection["evidence"][eid]["source_ref"] for eid in evidence_ids if eid in projection["evidence"]}
    for sid in source_ids: nodes.append({"id": sid, "type": "raw", "label": projection["sources"][sid].get("name", Path(projection["sources"][sid].get("path", sid)).name)})
    for eid in evidence_ids:
        if eid in projection["evidence"]:
            nodes.append({"id": eid, "type": "evidence", "label": "Evidence receipt"})
            edges.append({"from": projection["evidence"][eid]["source_ref"], "to": eid, "type": "bound_as"})
    for cid, row in wanted.items():
        nodes.append({"id": cid, "type": "conclusion", "state": v2_state(projection, row), "label": row["statement"]})
        edges += [{"from": eid, "to": cid, "type": "supports"} for eid in row["evidence_refs"]]
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
    return {"nodes": nodes, "edges": edges}


def summary_v2(scope=None):
    projection = v2_projection(); rows = [r for r in projection["conclusions"].values() if not scope or r["scope"] == scope]
    counts = {key: 0 for key in ("needs_review", "admitted", "rejected", "superseded", "expired", "unresolved")}
    for row in rows: counts[v2_state(projection, row)] += 1
    return {"total": len(rows), "counts": counts, "scope": scope}


def receipt_v2(cid):
    projection = v2_projection(); row = projection["conclusions"].get(cid)
    if not row: raise ValueError("conclusion not found: " + cid)
    return {"conclusion": row, "state": v2_state(projection, row),
            "evidence": [projection["evidence"].get(x) for x in row["evidence_refs"]],
            "evaluation": projection["evaluations"].get(cid),
            "recommendation": projection["recommendations"].get(cid),
            "review": projection["reviews"].get(cid),
            "admission": projection["admissions"].get(cid),
            "rejection": projection["rejections"].get(cid),
            "supersession": projection["supersessions"].get(cid),
            "history": [{"event_id": e["event_id"], "type": e["type"],
                         "created_at": e["created_at"], "commit": e.get("commit")}
                        for e in projection["events"] if e.get("subject_ref") == cid]}


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
    return Path(__file__).resolve().parent / "assets" / "local-ui" / "index.html"


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


def add_flat_cli(sub):
    evidence_parser = sub.add_parser("evidence", help="bind local evidence to the trust ledger")
    evidence_sub = evidence_parser.add_subparsers(dest="evidence_cmd", required=True)
    evidence_import = evidence_sub.add_parser("import", help="import an artifact or OTLP JSON as evidence")
    evidence_import.add_argument("input"); evidence_import.set_defaults(f=cmd_flat)
    propose_parser = sub.add_parser("propose", help="propose an evidence-bound reusable conclusion")
    propose_parser.add_argument("--statement", required=True); propose_parser.add_argument("--evidence", action="append", required=True)
    propose_parser.add_argument("--artifact", action="append", default=[]); propose_parser.add_argument("--scope", required=True)
    propose_parser.add_argument("--proposer", default="agent:proposer"); propose_parser.add_argument("--expires-at")
    propose_parser.add_argument("--allow-actor", action="append", default=[]); propose_parser.set_defaults(f=cmd_flat, flat_cmd="propose")
    evaluate_parser = sub.add_parser("evaluate"); evaluate_parser.add_argument("conclusion")
    evaluate_parser.set_defaults(f=cmd_flat, flat_cmd="evaluate")
    judge_parser = sub.add_parser("judge", help="run an advisory policy judge for one conclusion or one scope batch")
    judge_parser.add_argument("conclusion", nargs="?"); judge_parser.add_argument("--scope")
    judge_parser.add_argument("--batch", action="store_true"); judge_parser.set_defaults(f=cmd_flat, flat_cmd="judge")
    review_parser = sub.add_parser("review", help="record the human admission decision")
    review_parser.add_argument("conclusion"); decision = review_parser.add_mutually_exclusive_group(required=True)
    decision.add_argument("--admit", action="store_true"); decision.add_argument("--reject", action="store_true")
    review_parser.add_argument("--reviewer", required=True); review_parser.add_argument("--note"); review_parser.set_defaults(f=cmd_flat, flat_cmd="review")
    supersede_parser = sub.add_parser("supersede"); supersede_parser.add_argument("conclusion"); supersede_parser.add_argument("--by", required=True)
    supersede_parser.add_argument("--reviewer", required=True); supersede_parser.add_argument("--note"); supersede_parser.set_defaults(f=cmd_flat, flat_cmd="supersede")
    context_parser = sub.add_parser("context", help="materialize only knowledge eligible for the next agent")
    context_parser.add_argument("--scope"); context_parser.add_argument("--actor"); context_parser.add_argument("--task")
    context_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    context_parser.add_argument("--include-blocked-statements", action="store_true"); context_parser.set_defaults(f=cmd_flat, flat_cmd="context")
    ui_parser = sub.add_parser("ui", help="open the local review and context UI")
    ui_parser.add_argument("--scope"); ui_parser.add_argument("--port", type=int, default=7331); ui_parser.add_argument("--no-open", action="store_true")
    ui_parser.set_defaults(f=cmd_flat, flat_cmd="ui")
    migration = sub.add_parser("import-v1", help="one-way import of a 0.4 file-backed knowledge ledger")
    migration.add_argument("ledger"); migration.set_defaults(f=cmd_flat, flat_cmd="import-v1")


def cmd_flat(a):
    command = getattr(a, "flat_cmd", None) or ("evidence-import" if getattr(a, "evidence_cmd", None) == "import" else None)
    if command == "evidence-import": out = import_evidence_v2(a.input)
    elif command == "propose": out = propose_v2(a.statement, a.evidence, a.scope, a.proposer, a.expires_at, a.artifact, a.allow_actor or None)
    elif command == "evaluate": out = evaluate_v2(a.conclusion)
    elif command == "judge":
        if a.batch or a.scope: out = judge_batch_v2(a.scope)
        elif a.conclusion: out = judge_v2(a.conclusion)
        else: raise ValueError("judge requires a conclusion or --batch --scope")
    elif command == "review": out = review_v2(a.conclusion, "admit" if a.admit else "reject", a.reviewer, a.note)
    elif command == "supersede": out = supersede_v2(a.conclusion, a.by, a.reviewer, a.note)
    elif command == "context":
        out = context_v2(a.scope, a.actor, a.task, a.include_blocked_statements)
        if a.format == "markdown": print(_markdown_context(out)); return
    elif command == "ui": serve_ui(a.port, a.scope, not a.no_open); return
    elif command == "import-v1": out = import_v1(a.ledger)
    else: raise ValueError("unknown local MVP command")
    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))

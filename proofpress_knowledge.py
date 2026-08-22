#!/usr/bin/env python3
"""File-backed admission ledger: telemetry is input; admitted claims are context."""
from __future__ import annotations

import argparse, hashlib, json, os, tempfile
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

#!/usr/bin/env python3
"""Qualify a separate requirement-completeness gate over fixed claims."""
from __future__ import annotations

import argparse, json, time
from pathlib import Path

from model_routing_contract import digest
from run_claim_construction_private import Gateway, _model_call
from run_model_routing_qualification_private import MODELS, terminal_telemetry

STATES=("covered","partial","gap","conflict","needs_legal_analysis")
SCHEMA={"type":"object","additionalProperties":False,"required":["requirements"],"properties":{"requirements":{"type":"array","maxItems":40,"items":{"type":"object","additionalProperties":False,"required":["requirement_id","state","claim_ids"],"properties":{"requirement_id":{"type":"string"},"state":{"type":"string","enum":list(STATES)},"claim_ids":{"type":"array","maxItems":16,"items":{"type":"string"}}}}}}}


def validate(requirements,claims,value):
    req_ids={x["requirement_id"] for x in requirements}; claim_ids={x["id"] for x in claims}; rows=value.get("requirements") if isinstance(value,dict) else None
    if not isinstance(rows,list) or len(rows)!=len(requirements): raise ValueError("exactly one coverage state per requirement is required")
    result={}
    for row in rows:
      rid=row.get("requirement_id"); refs=set(row.get("claim_ids",[]))
      if rid not in req_ids or rid in result or row.get("state") not in STATES or not refs.issubset(claim_ids): raise ValueError("invalid coverage assignment")
      if row["state"]=="covered" and not refs: raise ValueError("covered requires claim binding")
      result[rid]={"requirement_id":rid,"state":row["state"],"claim_ids":sorted(refs)}
    if set(result)!=req_ids: raise ValueError("coverage assignment is incomplete")
    return result


def call(gateway,requirements,claims):
    by_req={r["requirement_id"]:[] for r in requirements}
    for c in claims: by_req.get(c["requirement_id"],[]).append({k:c.get(k) for k in ("id","claim_type","statement","qualification")})
    payload={"requirements":[{"requirement_id":r["requirement_id"],"requirement":r.get("requirement"),"applicability":r.get("applicability"),"claims":by_req[r["requirement_id"]]} for r in requirements],"instruction":"Classify whether the supplied claims fully answer each requirement. covered means all material elements are supported; partial means some but not all; gap means none; preserve conflicts and legal-analysis needs. Do not add claims or answer the task."}
    started=time.monotonic(); result=_model_call(gateway,"You are an independent legal requirement-completeness gate. Return states and claim IDs only.",json.dumps(payload,ensure_ascii=False),7000,SCHEMA,"proofpress_requirement_coverage",2)
    if not result["ok"]: return {},{"status":"inconclusive","elapsed_seconds":time.monotonic()-started,"failure":result["record"]}
    try: states=validate(requirements,claims,result["value"])
    except ValueError as exc: return {},{"status":"schema_failure","elapsed_seconds":time.monotonic()-started,"failure_digest":digest(str(exc))}
    return states,{"status":"ok","elapsed_seconds":time.monotonic()-started}


def metrics(candidate,reference):
    ids=sorted(reference); exact=sum(candidate[x]["state"]==reference[x]["state"] for x in ids); cand_open={x for x in ids if candidate[x]["state"]!="covered"}; ref_open={x for x in ids if reference[x]["state"]!="covered"}; tp=len(cand_open&ref_open); precision=tp/len(cand_open) if cand_open else 1.; recall=tp/len(ref_open) if ref_open else 1.
    return {"requirements":len(ids),"exact_state_agreement":exact/len(ids),"open_gap_precision":precision,"open_gap_recall":recall,"candidate_open":len(cand_open),"reference_open":len(ref_open)}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--candidate-report",required=True); ap.add_argument("--gateway-server",required=True); ap.add_argument("--out",required=True); ap.add_argument("--budget-usd",type=float,default=6); ap.add_argument("--timeout",type=float,default=300); args=ap.parse_args()
    candidate=json.loads(Path(args.candidate_report).read_text()); raw_in=Path(candidate["raw_private_dir"]); out=Path(args.out);out.mkdir(parents=True,exist_ok=True);out.chmod(0o700);raw=out/"raw";raw.mkdir(exist_ok=True);raw.chmod(0o700)
    gateways={label:Gateway(args.gateway_server,row["model"],row["provider"],out,args.timeout,row["reasoning"],structured_output=True) for label,row in MODELS.items()}; tasks=[]
    try:
      for task in candidate["tasks"]:
        task_id=task["task_id"]; source=json.loads((raw_in/f"{task_id}.json").read_text()); reqs=source["construction"]["requirements"]; claims=source["construction"]["claims"]; states={}; statuses={}
        for label,gateway in gateways.items(): states[label],statuses[label]=call(gateway,reqs,claims)
        ok=all(statuses[x]["status"]=="ok" for x in MODELS); comparisons={label:metrics(states[label],states["sol"]) for label in MODELS if states.get(label) and states.get("sol")}
        private={"task_id":task_id,"states":states,"statuses":statuses}; p=raw/f"{task_id}.json";p.write_text(json.dumps(private,indent=2,sort_keys=True)+"\n");p.chmod(0o600)
        tasks.append({"task_id":task_id,"status":"ok" if ok else "inconclusive","comparisons":comparisons,"statuses":statuses,"artifact_digest":digest(private)})
    finally:
      for g in gateways.values():g.stop()
    tele=terminal_telemetry(gateways); complete=[x for x in tasks if x["status"]=="ok"]; summary=[]
    for label in MODELS:
      rows=[x["comparisons"][label] for x in complete]; denom=sum(x["requirements"] for x in rows)
      summary.append({"model":label,"requirements":denom,"exact_state_agreement":sum(x["exact_state_agreement"]*x["requirements"] for x in rows)/denom if denom else None,"open_gap_precision":sum(x["open_gap_precision"]*x["requirements"] for x in rows)/denom if denom else None,"open_gap_recall":sum(x["open_gap_recall"]*x["requirements"] for x in rows)/denom if denom else None,"candidate_open":sum(x["candidate_open"] for x in rows),"reference_open":sum(x["reference_open"] for x in rows)})
    report={"schema_version":"proofpress/requirement-coverage-qualification/v1","boundary":"Four-task development tuning; fixed claims; Sol states are model reference, not gold/admission.","candidate_report_digest":digest(candidate),"models":MODELS,"summary":summary,"tasks":tasks,"telemetry":{**tele,"budget_usd":args.budget_usd},"qualification":{"status":"pass" if len(complete)==4 and not tele["missing_cost_calls"] else "inconclusive"},"raw_private_dir":str(raw)}
    target=out/"sanitized-report.json";target.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n");target.chmod(0o600);print(json.dumps({"ok":report["qualification"]["status"]=="pass","report":str(target),"known_cost_usd":tele["known_cost_usd"]}))

if __name__=="__main__":main()

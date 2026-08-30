#!/usr/bin/env python3
"""Compare type-only classifiers without permitting claim prose rewrites."""
from __future__ import annotations

import argparse, json, time
from pathlib import Path

from model_routing_contract import apply_type_assignments, construct_observed_claims, digest, validate_verdicts
from run_claim_construction_private import Gateway, V9_CRITIC_SCHEMA, _model_call
from run_model_routing_qualification_private import MODELS, call_critic, terminal_telemetry

TYPE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["assignments"],
    "properties": {
        "assignments": {
            "type": "array",
            "maxItems": 64,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["claim_id", "claim_type"],
                "properties": {
                    "claim_id": {"type": "string"},
                    "claim_type": {"type": "string", "enum": [
                        "observed_fact", "risk_signal", "legal_conclusion",
                        "contract_allocation",
                    ]},
                },
            },
        },
    },
}


def classify(gateway, requirements, claims, atoms):
    req = {row["requirement_id"]: row for row in requirements}
    payload = {"claims": [{"claim_id": row["id"], "statement": row["statement"],
                            "qualification": row.get("qualification"),
                            "requirement": req[row["requirement_id"]].get("requirement"),
                            "requirement_type": req[row["requirement_id"]].get("type"),
                            "lifecycle_category": req[row["requirement_id"]].get("lifecycle_category")}
                           for row in claims],
               "instruction": "Assign only a claim_type. Do not rewrite, infer, answer, or grant authority."}
    started=time.monotonic()
    result=_model_call(gateway, "Classify source-bound propositions by legal claim type. Return assignments only.",
                       json.dumps(payload,ensure_ascii=False),6000,TYPE_SCHEMA,
                       "proofpress_claim_type_assignments",2)
    if not result["ok"]: return [],{"status":"inconclusive","elapsed_seconds":time.monotonic()-started,"failure":result["record"]}
    try: typed=apply_type_assignments(claims,result["value"])
    except ValueError as exc: return [],{"status":"schema_failure","elapsed_seconds":time.monotonic()-started,"failure_digest":digest(str(exc))}
    return typed,{"status":"ok","elapsed_seconds":time.monotonic()-started}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--diagnostic",required=True); ap.add_argument("--gateway-server",required=True); ap.add_argument("--out",required=True); ap.add_argument("--budget-usd",type=float,default=8); ap.add_argument("--timeout",type=float,default=300); args=ap.parse_args()
    diag_path=Path(args.diagnostic).resolve(); diagnostic=json.loads(diag_path.read_text())
    paths=sorted((diag_path.parent/"raw"/"sol"/"receipt_preproposal").glob("*.json"))
    if len(paths)!=4: raise SystemExit("four frozen tasks required")
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True); out.chmod(0o700); raw=out/"raw"; raw.mkdir(exist_ok=True); raw.chmod(0o700)
    classifiers={label:Gateway(args.gateway_server,row["model"],row["provider"],out,args.timeout,row["reasoning"],structured_output=True) for label,row in MODELS.items()}
    critics={label:Gateway(args.gateway_server,"gpt-5.6-sol","openai",out,args.timeout,"low",structured_output=True) for label in MODELS}
    gateways={**{f"classifier_{k}":v for k,v in classifiers.items()},**{f"critic_{k}":v for k,v in critics.items()}}
    tasks=[]
    try:
      for path in paths:
        existing=raw/f"{path.stem}.json"
        if existing.is_file():
          saved=json.loads(existing.read_text())
          if set(saved.get("variants",{}))==set(MODELS):
            tasks.append({"task_id":path.stem,"status":"ok","requirement_count":len(json.loads(path.read_text())["construction"]["requirements"]),"variants":saved["variants"],"statuses":saved["statuses"],"artifact_digest":digest(saved)})
            continue
        source=json.loads(path.read_text()); c=source["construction"]; reqs=c["requirements"]; atoms=c["evidence_atoms"]; claims=construct_observed_claims(atoms,reqs)
        variants={}; status={}
        for label in MODELS:
          typed,cs=classify(classifiers[label],reqs,claims,atoms); status[f"classifier_{label}"]=cs
          if not typed: continue
          verdicts,vs=call_critic(critics[label],reqs,typed,atoms); status[f"critic_{label}"]=vs
          if not verdicts: continue
          supported={x["requirement_id"] for x in typed if verdicts[x["id"]]["verdict"]=="supported"}
          variants[label]={"claim_count":len(typed),"supported_claim_count":sum(x["verdict"]=="supported" for x in verdicts.values()),"supported_requirement_count":len(supported),"supported_requirement_coverage":len(supported)/len(reqs),"verdict_counts":vs["verdict_counts"]}
        ok=len(variants)==len(MODELS)
        private={"task_id":path.stem,"variants":variants,"statuses":status}; rp=raw/f"{path.stem}.json"; rp.write_text(json.dumps(private,indent=2,sort_keys=True)+"\n"); rp.chmod(0o600)
        tasks.append({"task_id":path.stem,"status":"ok" if ok else "inconclusive","requirement_count":len(reqs),"variants":variants,"statuses":status,"artifact_digest":digest(private)})
        tele=terminal_telemetry(gateways)
        # Development tuning may finish quality cells when a provider omits
        # terminal cost, but the route remains cost-inconclusive and cannot be
        # promoted. The known-cost hard cap still stops execution immediately.
        if tele["known_cost_usd"]>args.budget_usd: raise RuntimeError("budget exceeded")
    finally:
      for g in gateways.values(): g.stop()
    tele=terminal_telemetry(gateways); completed=[x for x in tasks if x["status"]=="ok"]
    summary=[]
    for label in MODELS:
      rows=[x["variants"][label] for x in completed]; denom=sum(x["requirement_count"] for x in completed)
      summary.append({"classifier":label,"tasks":len(rows),"claims":sum(x["claim_count"] for x in rows),"supported_claims":sum(x["supported_claim_count"] for x in rows),"supported_requirement_coverage":sum(x["supported_requirement_count"] for x in rows)/denom if denom else None})
    report={"schema_version":"proofpress/claim-type-qualification/v1","boundary":"Four-task development tuning; fixed statements and receipts; Sol verdict is model reference, not gold/admission.","models":MODELS,"denominators":{"tasks":len(tasks),"requirements":sum(x.get("requirement_count",0) for x in completed)},"summary":summary,"tasks":tasks,"telemetry":{**tele,"budget_usd":args.budget_usd,"cost_status":"complete" if not tele["missing_cost_calls"] else "inconclusive"},"qualification":{"status":"pass" if len(completed)==4 and not tele["missing_cost_calls"] else ("quality_complete_cost_inconclusive" if len(completed)==4 else "inconclusive")},"raw_private_dir":str(raw)}
    target=out/"sanitized-report.json"; target.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n"); target.chmod(0o600); print(json.dumps({"ok":report["qualification"]["status"]=="pass","report":str(target),"known_cost_usd":tele["known_cost_usd"]}))

if __name__=="__main__": main()

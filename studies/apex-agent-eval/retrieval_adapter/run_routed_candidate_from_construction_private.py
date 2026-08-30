#!/usr/bin/env python3
"""Apply the frozen routed claim policy to an existing construction run."""
from __future__ import annotations

import argparse, json
from pathlib import Path

from model_routing_contract import construct_observed_claims, digest
from run_claim_construction_private import Gateway
from run_claim_type_qualification_private import classify
from run_model_routing_qualification_private import call_critic, terminal_telemetry
from run_requirement_coverage_qualification_private import call as coverage_call


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--source-report",required=True);ap.add_argument("--gateway-server",required=True);ap.add_argument("--out",required=True);ap.add_argument("--budget-usd",type=float,default=6);ap.add_argument("--timeout",type=float,default=300);args=ap.parse_args()
    source_report=json.loads(Path(args.source_report).read_text()); source_raw=Path(source_report["raw_private_dir"]);out=Path(args.out);out.mkdir(parents=True,exist_ok=True);out.chmod(0o700);raw=out/"raw";raw.mkdir(exist_ok=True);raw.chmod(0o700)
    type_gateway=Gateway(args.gateway_server,"gpt-5.6-luna","openai",out,args.timeout,"low",structured_output=True);critic_gateway=Gateway(args.gateway_server,"gpt-5.6-sol","openai",out,args.timeout,"low",structured_output=True);coverage_gateway=Gateway(args.gateway_server,"gpt-5.6-luna","openai",out,args.timeout,"low",structured_output=True);gateways={"luna_type":type_gateway,"sol_critic":critic_gateway,"luna_coverage":coverage_gateway};tasks=[]
    try:
      for task in source_report["tasks"]:
        task_id=task["task_id"];source=json.loads((source_raw/f"{task_id}.json").read_text());c=source["construction"];reqs=c["requirements"];atoms=c.get("evidence_atoms",[]);claims=construct_observed_claims(atoms,reqs);typed,ts=classify(type_gateway,reqs,claims,atoms);verdicts,vs=call_critic(critic_gateway,reqs,typed,atoms,source.get("task",{}).get("prompt"));supported=[x for x in typed if verdicts.get(x["id"],{}).get("verdict")=="supported"];coverage,cs=coverage_call(coverage_gateway,reqs,supported)
        ok=all(x["status"]=="ok" for x in (ts,vs,cs));requirements=[]
        for req in reqs:
          row=dict(req);state=coverage.get(row["requirement_id"],{}).get("state","gap");row["coverage_gate_state"]=state;row["status"]="covered" if state=="covered" else "gap" if state in {"gap","conflict"} else "partial";requirements.append(row)
        construction={**c,"status":"ok" if ok else "inconclusive","requirements":requirements,"claims":supported,"relations":[],"critic_status":"ok" if vs["status"]=="ok" else "inconclusive","critic_verdicts":list(verdicts.values()),"model_route":{"claim_constructor":"deterministic-atom-to-statement/v1","type_classifier":"gpt-5.6-luna/openai/low","claim_critic":"gpt-5.6-sol/openai/low/task-aware","coverage_gate":"gpt-5.6-luna/openai/low"}}
        private={"task":source["task"],"decomposition":source["decomposition"],"construction":construction};p=raw/f"{task_id}.json";p.write_text(json.dumps(private,ensure_ascii=False,indent=2,sort_keys=True)+"\n");p.chmod(0o600)
        tasks.append({"task_id":task_id,"status":"ok" if ok else "inconclusive","requirement_count":len(reqs),"atom_count":len(atoms),"deterministic_claim_count":len(typed),"supported_claim_count":len(supported),"open_requirement_count":sum(x["status"]!="covered" for x in requirements),"artifact_digest":digest(private)})
    finally:
      for g in gateways.values():g.stop()
    tele=terminal_telemetry(gateways);complete=[x for x in tasks if x["status"]=="ok"]
    report={"schema_version":"proofpress/routed-claim-construction/v1","system":"evidence-first-routed-luna-decomposition","catalog_digest":source_report.get("catalog_digest"),"source_count":source_report.get("source_count"),"unique_source_uri_count":source_report.get("unique_source_uri_count"),"section_count":source_report.get("section_count"),"source_report_digest":digest(source_report),"tasks":tasks,"denominators":{"tasks":len(tasks),"requirements":sum(x["requirement_count"] for x in complete),"atoms":sum(x["atom_count"] for x in complete),"claims":sum(x["supported_claim_count"] for x in complete)},"telemetry":{**tele,"budget_usd":args.budget_usd},"qualification":{"requested":True,"status":"pass" if len(complete)==4 and not tele["missing_cost_calls"] else "inconclusive"},"raw_private_dir":str(raw)}
    target=out/"sanitized-report.json";target.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n");target.chmod(0o600);print(json.dumps({"ok":report["qualification"]["status"]=="pass","report":str(target),"known_cost_usd":tele["known_cost_usd"]}))

if __name__=="__main__":main()

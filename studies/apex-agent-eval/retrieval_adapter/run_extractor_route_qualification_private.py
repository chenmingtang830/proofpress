#!/usr/bin/env python3
"""Compare frozen atom extractors under one fixed claim-shaping route."""
from __future__ import annotations

import argparse, json
from pathlib import Path

from model_routing_contract import construct_observed_claims, digest
from run_claim_construction_private import Gateway
from run_claim_type_qualification_private import classify
from run_model_routing_qualification_private import call_critic, terminal_telemetry

EXTRACTORS = ("ling", "deepseek", "sol")


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--diagnostic",required=True); ap.add_argument("--gateway-server",required=True); ap.add_argument("--out",required=True); ap.add_argument("--budget-usd",type=float,default=8); ap.add_argument("--timeout",type=float,default=300); args=ap.parse_args()
    diag=Path(args.diagnostic).resolve(); root=diag.parent/"raw"; out=Path(args.out); out.mkdir(parents=True,exist_ok=True); out.chmod(0o700); raw=out/"raw"; raw.mkdir(exist_ok=True); raw.chmod(0o700)
    task_ids=sorted(p.stem for p in (root/"sol"/"receipt_preproposal").glob("*.json"))
    if len(task_ids)!=4: raise SystemExit("four frozen tasks required")
    classifier=Gateway(args.gateway_server,"gpt-5.6-luna","openai",out,args.timeout,"low",structured_output=True)
    critic=Gateway(args.gateway_server,"gpt-5.6-sol","openai",out,args.timeout,"low",structured_output=True)
    gateways={"luna_type_classifier":classifier,"sol_critic":critic}; cells=[]
    try:
      for extractor in EXTRACTORS:
       for task_id in task_ids:
        saved_path=raw/f"{extractor}-{task_id}.json"
        if saved_path.is_file():
          saved=json.loads(saved_path.read_text()); cells.append(saved["summary"]); continue
        source=json.loads((root/extractor/"receipt_preproposal"/f"{task_id}.json").read_text()); c=source["construction"]; reqs=c["requirements"]; atoms=c["evidence_atoms"]
        claims=construct_observed_claims(atoms,reqs); typed,cs=classify(classifier,reqs,claims,atoms)
        verdicts,vs=call_critic(critic,reqs,typed,atoms) if typed else ({},{"status":"not_run"})
        ok=cs["status"]=="ok" and vs["status"]=="ok"
        supported={x["requirement_id"] for x in typed if verdicts.get(x["id"],{}).get("verdict")=="supported"}
        summary={"extractor":extractor,"task_id":task_id,"status":"ok" if ok else "inconclusive","requirement_count":len(reqs),"valid_atom_count":len(atoms),"atom_requirement_count":len({x["requirement_id"] for x in atoms}),"claim_count":len(typed),"supported_claim_count":sum(x.get("verdict")=="supported" for x in verdicts.values()),"supported_requirement_count":len(supported),"supported_requirement_coverage":len(supported)/len(reqs) if reqs else None,"classifier_status":cs,"critic_status":vs}
        private={"summary":summary,"typed_claims":typed,"verdicts":verdicts}; saved_path.write_text(json.dumps(private,indent=2,sort_keys=True)+"\n"); saved_path.chmod(0o600); cells.append(summary)
        tele=terminal_telemetry(gateways)
        if tele["known_cost_usd"]>args.budget_usd: raise RuntimeError("budget exceeded")
    finally:
      classifier.stop(); critic.stop()
    tele=terminal_telemetry(gateways); complete=[x for x in cells if x["status"]=="ok"]; summary=[]
    for extractor in EXTRACTORS:
      rows=[x for x in complete if x["extractor"]==extractor]; denom=sum(x["requirement_count"] for x in rows)
      summary.append({"extractor":extractor,"tasks":len(rows),"requirements":denom,"valid_atoms":sum(x["valid_atom_count"] for x in rows),"atom_requirement_coverage":sum(x["atom_requirement_count"] for x in rows)/denom if denom else None,"claims":sum(x["claim_count"] for x in rows),"supported_claims":sum(x["supported_claim_count"] for x in rows),"supported_requirement_coverage":sum(x["supported_requirement_count"] for x in rows)/denom if denom else None})
    report={"schema_version":"proofpress/extractor-route-qualification/v1","boundary":"Four-task development tuning; frozen atoms per extractor; fixed Luna type-only classifier and Sol model-reference critic.","fixed_route":{"type_classifier":"gpt-5.6-luna/openai/low","critic":"gpt-5.6-sol/openai/low"},"summary":summary,"cells":cells,"telemetry":{**tele,"budget_usd":args.budget_usd,"cost_status":"complete" if not tele["missing_cost_calls"] else "inconclusive"},"qualification":{"status":"pass" if len(complete)==12 and not tele["missing_cost_calls"] else "inconclusive"},"raw_private_dir":str(raw)}
    target=out/"sanitized-report.json"; target.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n"); target.chmod(0o600); print(json.dumps({"ok":report["qualification"]["status"]=="pass","report":str(target),"known_cost_usd":tele["known_cost_usd"]}))

if __name__=="__main__": main()

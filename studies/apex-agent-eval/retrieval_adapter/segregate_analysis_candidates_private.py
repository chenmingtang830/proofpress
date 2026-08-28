#!/usr/bin/env python3
"""Segregate risk/legal-analysis records from evidence-bound graph claims."""
from __future__ import annotations

import argparse, json
from pathlib import Path
from model_routing_contract import digest

ANALYSIS_TYPES={"risk_signal","legal_conclusion"}


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--source-report",required=True);ap.add_argument("--out",required=True);args=ap.parse_args();source_report=json.loads(Path(args.source_report).read_text());source_raw=Path(source_report["raw_private_dir"]);out=Path(args.out);out.mkdir(parents=True,exist_ok=True);out.chmod(0o700);raw=out/"raw";raw.mkdir(exist_ok=True);raw.chmod(0o700);tasks=[]
    for task in source_report["tasks"]:
      task_id=task["task_id"];value=json.loads((source_raw/f"{task_id}.json").read_text());construction=value["construction"];claims=[];analysis=[]
      for claim in construction.get("claims",[]):
        if claim.get("claim_type") in ANALYSIS_TYPES:
          row=dict(claim);row["status"]="analysis_only";row["admission_eligible"]=False;analysis.append(row)
        else: claims.append(claim)
      construction={**construction,"claims":claims,"analysis_candidates":analysis,"analysis_segregation":"risk-and-legal-analysis/v1"};private={**value,"construction":construction};p=raw/f"{task_id}.json";p.write_text(json.dumps(private,ensure_ascii=False,indent=2,sort_keys=True)+"\n");p.chmod(0o600);tasks.append({"task_id":task_id,"status":"ok","requirement_count":len(construction.get("requirements",[])),"claim_count":len(claims),"analysis_candidate_count":len(analysis),"artifact_digest":digest(private)})
    report={**source_report,"schema_version":"proofpress/routed-claim-construction/v1","system":"evidence-first-routed-luna-decomposition-segregated","source_report_digest":digest(source_report),"tasks":tasks,"denominators":{"tasks":len(tasks),"requirements":sum(x["requirement_count"] for x in tasks),"claims":sum(x["claim_count"] for x in tasks),"analysis_candidates":sum(x["analysis_candidate_count"] for x in tasks)},"raw_private_dir":str(raw)}
    target=out/"sanitized-report.json";target.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n");target.chmod(0o600);print(target)

if __name__=="__main__":main()

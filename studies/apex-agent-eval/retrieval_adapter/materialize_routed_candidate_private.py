#!/usr/bin/env python3
"""Materialize one routed development candidate for existing paired scorers."""
from __future__ import annotations

import argparse, json
from pathlib import Path

from model_routing_contract import digest


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--diagnostic",required=True); ap.add_argument("--frozen-run-report",required=True); ap.add_argument("--route-report",required=True); ap.add_argument("--coverage-report"); ap.add_argument("--coverage-model",choices=("deepseek","luna","sol")); ap.add_argument("--extractor",choices=("ling","deepseek","sol"),required=True); ap.add_argument("--out",required=True); args=ap.parse_args()
    diagnostic=Path(args.diagnostic).resolve(); diagnostic_report=json.loads(diagnostic.read_text()); frozen_report=json.loads(Path(args.frozen_run_report).read_text()); route_path=Path(args.route_report).resolve(); route=json.loads(route_path.read_text()); out=Path(args.out); out.mkdir(parents=True,exist_ok=True); out.chmod(0o700); raw=out/"raw"; raw.mkdir(exist_ok=True); raw.chmod(0o700)
    if digest(frozen_report) != diagnostic_report.get("frozen_run_digest"):
        raise SystemExit("frozen run report does not match the gate diagnostic")
    coverage_report=json.loads(Path(args.coverage_report).read_text()) if args.coverage_report else None
    if bool(coverage_report) != bool(args.coverage_model):
        raise SystemExit("coverage report and model must be supplied together")
    coverage_raw=Path(coverage_report["raw_private_dir"]) if coverage_report else None
    rows=[]
    for cell in route["cells"]:
      if cell["extractor"]!=args.extractor or cell["status"]!="ok": continue
      task_id=cell["task_id"]
      source=json.loads((diagnostic.parent/"raw"/args.extractor/"receipt_preproposal"/f"{task_id}.json").read_text())
      routed=json.loads((route_path.parent/"raw"/f"{args.extractor}-{task_id}.json").read_text())
      verdicts=routed["verdicts"]; claims=[x for x in routed["typed_claims"] if verdicts.get(x["id"],{}).get("verdict")=="supported"]
      supported={x["requirement_id"] for x in claims}; atom_req={x["requirement_id"] for x in source["construction"]["evidence_atoms"]}
      coverage_states={}
      if coverage_raw:
        coverage_private=json.loads((coverage_raw/f"{task_id}.json").read_text())
        coverage_states=coverage_private["states"][args.coverage_model]
      requirements=[]
      for req in source["construction"]["requirements"]:
        row=dict(req); rid=row["requirement_id"]
        model_state=coverage_states.get(rid,{}).get("state")
        row["status"]=("covered" if model_state=="covered" else
                       "gap" if model_state in {"gap","conflict"} else
                       "partial" if model_state else
                       ("covered" if rid in supported else ("partial" if rid in atom_req else "gap")))
        if model_state:
          row["coverage_gate_state"]=model_state
        requirements.append(row)
      construction={**source["construction"],"requirements":requirements,"claims":claims,"relations":[],"critic_status":"ok","critic_verdicts":list(verdicts.values()),"status":"ok","model_route":{"extractor":args.extractor,"claim_constructor":"deterministic-atom-to-statement/v1","type_classifier":"gpt-5.6-luna","critic":"gpt-5.6-sol","coverage_gate":args.coverage_model}}
      private={"task":source["task"],"decomposition":source["decomposition"],"construction":construction}; target=raw/f"{task_id}.json"; target.write_text(json.dumps(private,ensure_ascii=False,indent=2,sort_keys=True)+"\n"); target.chmod(0o600)
      rows.append({"task_id":task_id,"status":"ok","requirement_count":len(requirements),"claim_count":len(claims),"artifact_digest":digest(private)})
    report={"schema_version":"proofpress/routed-claim-construction/v1","system":f"evidence-first-routed-{args.extractor}","catalog_digest":frozen_report.get("catalog_digest"),"source_count":frozen_report.get("source_count"),"unique_source_uri_count":frozen_report.get("unique_source_uri_count"),"section_count":frozen_report.get("section_count"),"tasks":rows,"denominators":{"tasks":len(rows),"requirements":sum(x["requirement_count"] for x in rows),"claims":sum(x["claim_count"] for x in rows)},"qualification":{"requested":True,"status":"pass" if len(rows)==4 else "inconclusive"},"frozen_run_report_digest":digest(frozen_report),"route_report_digest":digest(route),"coverage_report_digest":digest(coverage_report) if coverage_report else None,"coverage_model":args.coverage_model,"raw_private_dir":str(raw)}
    target=out/"sanitized-report.json"; target.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n"); target.chmod(0o600); print(target)

if __name__=="__main__": main()

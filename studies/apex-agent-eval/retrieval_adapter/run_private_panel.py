#!/usr/bin/env python3
"""Private PageIndex panel. Raw APEX data and HF gold never enter public output."""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, time
from pathlib import Path

SCHEMA="proofpress/private-retrieval-panel/v2"
MODEL="deepseek/deepseek-v4-flash-0731"
PROVIDER="fireworks"
SYSTEMS=("lexical-chunk/v1","pageindex-tree/v1","hybrid/v1")
def sha(v): return "sha256:"+hashlib.sha256(v.encode() if isinstance(v,str) else v).hexdigest()
def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def validate(path):
    data=load(path)
    if data.get("schema_version")!=SCHEMA or not isinstance(data.get("sources"),list) or not isinstance(data.get("tasks"),list): raise ValueError("unsupported private panel manifest")
    for row in data["sources"]:
        if any(not row.get(k) for k in ("uri","path","content_digest","media_type","extracted_text_path")): raise ValueError("source is missing a custody field")
        if sha(Path(row["path"]).read_bytes())!=row["content_digest"]: raise ValueError("source custody check failed")
    for row in data["tasks"]:
        # gold_response is the frozen Hugging Face ground truth; gold locators
        # are separately adjudicated before any system output is inspected.
        if not row.get("task_id") or not row.get("query") or not isinstance(row.get("gold"),list) or not isinstance(row.get("gold_response"),str): raise ValueError("task needs query, HF gold response, and a locator array")
    return data
def lexical(query,sources,limit):
    terms={x.lower() for x in query.split() if len(x)>2}; rows=[]
    for src in sources:
        text=Path(src["extracted_text_path"]).read_text(encoding="utf-8")
        for start in range(0,len(text),700):
            quote=text[start:start+900]; score=sum(term in quote.lower() for term in terms)
            if score: rows.append((-score,src["uri"],start,quote,src))
    rows.sort(key=lambda x:x[:3])
    return [{"schema_version":"proofpress/retrieval-evidence/v1","source":{"uri":x[4]["uri"],"content_digest":x[4]["content_digest"],"media_type":x[4]["media_type"]},"evidence":{"quote":x[3],"locator":{"kind":"text_span","start":x[2],"end":x[2]+len(x[3]),"text_digest":sha(Path(x[4]["extracted_text_path"]).read_bytes())}},"retrieval":{"adapter":"lexical-chunk/v1","version":"1","query":query,"config_digest":sha("lexical-900-overlap-200-v1")}} for x in rows[:limit]]
def hit(receipt,gold):
    loc=receipt.get("evidence",{}).get("locator",{}); uri=receipt.get("source",{}).get("uri")
    for target in gold:
        if uri!=target.get("source_uri"): continue
        if loc.get("kind") in {"page_span","section_span"} and loc.get("page_start",0)<=target.get("page_end",-1) and loc.get("page_end",-1)>=target.get("page_start",0): return True
        if loc.get("kind")=="text_span" and target.get("kind")=="text_span" and loc.get("start",-1)<target.get("end",-1) and loc.get("end",-1)>target.get("start",-1): return True
    return False
def score(receipts,gold):
    if not gold:
        # A golden answer alone is not a source-location judgment.  Preserve
        # the completed retrieval run, but do not invent a recall denominator.
        return {"document_locator_recall_at_k":None,"quote_binding_rate":None,"citation_precision":None,"receipt_pass_rate":None}
    bound=[r for r in receipts if r.get("source",{}).get("content_digest") and r.get("evidence",{}).get("locator")]; hits=sum(hit(r,gold) for r in receipts)
    return {"document_locator_recall_at_k":bool(hits),"quote_binding_rate":len(bound)/len(receipts) if receipts else 0,"citation_precision":hits/len(receipts) if receipts else 0,"receipt_pass_rate":len(bound)/len(receipts) if receipts else 0}
def bridge(script,receipt_file):
    env=os.environ.copy(); env.update({"PROOFPRESS_PAGEINDEX_MODEL":MODEL,"PROOFPRESS_PAGEINDEX_PROVIDER":PROVIDER,"PROOFPRESS_PAGEINDEX_PORT":"0","PROOFPRESS_PAGEINDEX_RECEIPTS":str(receipt_file)})
    process=subprocess.Popen(["node",script],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=env); line=process.stdout.readline().strip()
    try: port=int(json.loads(line)["port"])
    except Exception: process.kill(); raise RuntimeError("Gateway bridge did not become ready")
    return process,"http://127.0.0.1:%s/v1"%port
def tree(query,sources,sidecar,config,limit,base_url):
    request={"schema_version":"proofpress/pageindex-sidecar/v1","query":query,"sources":[{k:v for k,v in s.items() if k in {"source_id","path","uri","content_digest","media_type"}} for s in sources],"config":config,"max_results":limit}
    env=os.environ.copy(); env.update({"OPENAI_BASE_URL":base_url,"OPENAI_API_KEY":"local-gateway-bridge"})
    result=subprocess.run([sidecar],input=json.dumps(request),text=True,capture_output=True,timeout=300,env=env)
    if result.returncode: raise RuntimeError("sidecar failed closed")
    out=json.loads(result.stdout)
    if out.get("schema_version")!="proofpress/pageindex-sidecar/v1" or out.get("fallback_used") is not False: raise RuntimeError("sidecar no-fallback protocol failed")
    if not isinstance(out.get("telemetry",{}).get("latency_ms"),(int,float)): raise RuntimeError("sidecar latency missing")
    return out.get("receipts",[]),out["telemetry"]
def costs(receipt_file,offset):
    rows=[json.loads(x) for x in receipt_file.read_text(encoding="utf-8").splitlines()[offset:]] if receipt_file.exists() else []
    if not rows or any(r.get("model")!=MODEL or r.get("provider")!=PROVIDER or r.get("fallback_used") is not False or not isinstance(r.get("cost_usd"),(int,float)) for r in rows): raise RuntimeError("Gateway telemetry incomplete")
    return sum(r["cost_usd"] for r in rows)
def quantile(values,q):
    rows=sorted(values); return rows[min(len(rows)-1,round((len(rows)-1)*q))] if rows else None
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--manifest",required=True); ap.add_argument("--out",required=True); ap.add_argument("--sidecar",required=True); ap.add_argument("--gateway-server",required=True); ap.add_argument("--limit",type=int,default=6); a=ap.parse_args()
    if not os.environ.get("AI_GATEWAY_API_KEY"): raise SystemExit("scored panel fails closed: AI_GATEWAY_API_KEY unavailable")
    data=validate(a.manifest); out=Path(a.out); out.mkdir(parents=True,exist_ok=True); private_gateway=out/"gateway-private-receipts.jsonl"
    config={"adapter":"proofpress.pageindex","version":"1","requested_model":MODEL,"provider":PROVIDER,"fallback":"forbidden","max_sections":a.limit,"max_pages":a.limit}; config["config_digest"]=sha(json.dumps(config,sort_keys=True))
    runs={n:{"completed":0,"inconclusive":0,"receipt_count":0,"latencies":[],"costs":[],"metric_rows":[]} for n in SYSTEMS}; raw=[]; gateway,base=bridge(a.gateway_server,private_gateway)
    try:
      for task in data["tasks"]:
        started=time.monotonic(); lex=lexical(task["query"],data["sources"],a.limit); latency=(time.monotonic()-started)*1000
        raw.append({"task_id":task["task_id"],"system":SYSTEMS[0],"receipts":lex}); r=runs[SYSTEMS[0]]; r["completed"]+=1; r["receipt_count"]+=len(lex); r["latencies"].append(latency); r["costs"].append(0); r["metric_rows"].append(score(lex,task["gold"]))
        offset=len(private_gateway.read_text().splitlines()) if private_gateway.exists() else 0
        try:
          indexed,telemetry=tree(task["query"],data["sources"],a.sidecar,config,a.limit,base); cost=costs(private_gateway,offset); hybrid=(lex+indexed)[:a.limit]
          for name,receipts in ((SYSTEMS[1],indexed),(SYSTEMS[2],hybrid)):
            raw.append({"task_id":task["task_id"],"system":name,"receipts":receipts}); r=runs[name]; r["completed"]+=1; r["receipt_count"]+=len(receipts); r["latencies"].append(telemetry["latency_ms"]); r["costs"].append(cost); r["metric_rows"].append(score(receipts,task["gold"]))
        except RuntimeError as exc:
          for name in SYSTEMS[1:]: runs[name]["inconclusive"]+=1
          raw.append({"task_id":task["task_id"],"system":"pageindex-and-hybrid","status":"inconclusive","reason":str(exc)})
    finally: gateway.terminate(); gateway.wait(timeout=5)
    for r in runs.values():
      metrics=r.pop("metric_rows"); latencies=r.pop("latencies"); costs_=r.pop("costs"); r["latency_ms"]={"p50":quantile(latencies,.5),"p95":quantile(latencies,.95)}; r["cost_usd"]=sum(costs_) if costs_ else None
      scored=[x for x in metrics if x["document_locator_recall_at_k"] is not None]
      r["metric_denominator"]={"locator_scored_tasks":len(scored),"answer_only_tasks":len(metrics)-len(scored)}
      r["metrics"]={k:sum(float(x[k]) for x in scored)/len(scored) if scored else None for k in ("document_locator_recall_at_k","quote_binding_rate","citation_precision","receipt_pass_rate")}
    tasks=[{"task_id":t["task_id"],"query_digest":sha(t["query"]),"gold_response_digest":sha(t["gold_response"]),"gold_locator_digest":sha(json.dumps(t["gold"],sort_keys=True))} for t in data["tasks"]]
    report={"schema_version":"proofpress/retrieval-panel-sanitized/v2","manifest_digest":sha(json.dumps({"sources":[{"uri":s["uri"],"content_digest":s["content_digest"],"media_type":s["media_type"]} for s in data["sources"]],"tasks":tasks},sort_keys=True)),"model":{"requested":MODEL,"provider":PROVIDER,"fallback":"forbidden"},"tasks":tasks,"systems":runs,"scoring_boundary":"answer-only tasks have no locator metric denominator and are reported as unscored"}
    (out/"raw-private-receipts.json").write_text(json.dumps(raw,indent=2),encoding="utf-8"); (out/"sanitized-report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"sanitized_report":str(out/"sanitized-report.json"),"systems":runs},indent=2))
if __name__=="__main__": main()

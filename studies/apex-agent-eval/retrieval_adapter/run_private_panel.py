#!/usr/bin/env python3
"""Private PageIndex panel. Raw APEX data and HF gold never enter public output."""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, time
from pathlib import Path

SCHEMA="proofpress/private-retrieval-panel/v2"
MODEL=os.environ.get("PROOFPRESS_EXECUTOR_MODEL", "deepseek/deepseek-v4-flash")
PROVIDER=os.environ.get("PROOFPRESS_AI_GATEWAY_PROVIDER", "proofpress-dev-ai-gateway")
DECOMPOSITION_MODEL=os.environ.get("PROOFPRESS_DECOMPOSITION_MODEL", "zai/glm-5.3-flash")
PROPOSER_MODEL=os.environ.get("PROOFPRESS_PROPOSER_MODEL", "zai/glm-5.3-flash")
CRITIC_MODEL=os.environ.get("PROOFPRESS_CRITIC_MODEL", "gpt-5.6-sol")
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
        return {"document_locator_recall_at_k":None,"evidence_set_coverage":None,"complete_evidence_set_success":None,"quote_binding_rate":None,"citation_precision":None,"receipt_pass_rate":None}
    bound=[r for r in receipts if r.get("source",{}).get("content_digest") and r.get("evidence",{}).get("locator")]; hits=sum(hit(r,gold) for r in receipts)
    coverage=hits/len(gold) if gold else None
    return {"document_locator_recall_at_k":coverage,"evidence_set_coverage":coverage,
            "complete_evidence_set_success":coverage == 1 if coverage is not None else None,
            "quote_binding_rate":len(bound)/len(receipts) if receipts else 0,
            "citation_precision":hits/len(receipts) if receipts else 0,
            "receipt_pass_rate":len(bound)/len(receipts) if receipts else 0}

def hybrid_rrf(lexical_rows, pageindex_rows, limit, k0=60):
    """Fixed reciprocal-rank fusion over a single top-20 union.

    Source/overlapping locator duplicates are collapsed before scoring; ties
    are stable on source URI and locator digest, so repeated runs are replayable.
    """
    def key(row):
        source=row.get("source", {})
        locator=row.get("evidence", {}).get("locator", {})
        return (source.get("uri"), source.get("content_digest"), json.dumps(locator, sort_keys=True))
    fused={}
    for rank, row in enumerate(lexical_rows, 1):
        fused.setdefault(key(row), {"row": row, "score": 0.0})["score"] += 1/(k0+rank)
    for rank, row in enumerate(pageindex_rows, 1):
        fused.setdefault(key(row), {"row": row, "score": 0.0})["score"] += 1/(k0+rank)
    ordered=sorted(fused.values(), key=lambda item: (-item["score"], key(item["row"])))
    return [item["row"] for item in ordered[:limit]]
def bridge(script,receipt_file):
    env=os.environ.copy(); env.update({"PROOFPRESS_PAGEINDEX_MODEL":MODEL,"PROOFPRESS_PAGEINDEX_PROVIDER":PROVIDER,"PROOFPRESS_PAGEINDEX_PORT":"0","PROOFPRESS_PAGEINDEX_RECEIPTS":str(receipt_file)})
    # The bridge emits compatibility warnings on stderr for each Gateway call.
    # Never leave a piped stderr unread: after enough PageIndex requests its
    # OS pipe can fill and falsely stall the otherwise healthy server.
    process=subprocess.Popen(["node",script],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,env=env); line=process.stdout.readline().strip()
    try: port=int(json.loads(line)["port"])
    except Exception: process.kill(); raise RuntimeError("Gateway bridge did not become ready")
    return process,"http://127.0.0.1:%s/v1"%port
def tree_request(query,sources,config,limit,cache_dir):
    # The source digest binds original custody/navigation while path_digest
    # binds the canonical bytes PageIndex actually reads.  Keep locator_map and
    # representation_kind so the sidecar can map canonical line hits back to
    # stable source section/page locators.  Dropping these fields silently
    # collapses the two custody domains and makes every converted Office/text
    # source fail closed.
    allowed={"source_id","path","uri","content_digest","media_type",
             "representation_digest","transform_digest","page_count",
             "path_digest","representation_kind","locator_map"}
    return {"schema_version":"proofpress/pageindex-sidecar/v1","query":query,"sources":[{k:v for k,v in s.items() if k in allowed} for s in sources],"config":config,"max_results":limit,"cache_dir":str(cache_dir)}
def tree(query,sources,sidecar,config,limit,base_url,cache_dir,timeout_seconds):
    request=tree_request(query,sources,config,limit,cache_dir)
    env=os.environ.copy(); env.update({"OPENAI_BASE_URL":base_url,"OPENAI_API_KEY":"local-gateway-bridge"})
    result=subprocess.run([sidecar],input=json.dumps(request),text=True,capture_output=True,timeout=timeout_seconds,env=env)
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
    ap=argparse.ArgumentParser(); ap.add_argument("--manifest",required=True); ap.add_argument("--out",required=True); ap.add_argument("--sidecar",required=True); ap.add_argument("--gateway-server",required=True); ap.add_argument("--limit",type=int,default=6); ap.add_argument("--pageindex-timeout-seconds",type=int,default=int(os.environ.get("PROOFPRESS_PAGEINDEX_TIMEOUT_SECONDS","1800"))); ap.add_argument("--pageindex-parallelism",type=int,default=int(os.environ.get("PROOFPRESS_PAGEINDEX_PARALLELISM","4"))); a=ap.parse_args()
    if not os.environ.get("AI_GATEWAY_API_KEY"): raise SystemExit("scored panel fails closed: AI_GATEWAY_API_KEY unavailable")
    data=validate(a.manifest); out=Path(a.out); out.mkdir(parents=True,exist_ok=True); private_gateway=out/"gateway-private-receipts.jsonl"
    if a.pageindex_timeout_seconds < 1: raise SystemExit("PageIndex timeout must be positive")
    if a.pageindex_parallelism < 1: raise SystemExit("PageIndex parallelism must be positive")
    config={"adapter":"proofpress.pageindex","version":"1","requested_model":MODEL,"provider":PROVIDER,"fallback":"forbidden","max_sections":20,"max_pages":20,"toc_check_pages":1,"max_pages_per_node":1,"max_tokens_per_node":2500,"node_summary":False,"document_description":False,"timeout_seconds":a.pageindex_timeout_seconds,"parallelism":a.pageindex_parallelism}; config["config_digest"]=sha(json.dumps(config,sort_keys=True))
    runs={n:{"completed":0,"inconclusive":0,"receipt_count":0,"latencies":[],"costs":[],"metric_rows":[]} for n in SYSTEMS}; raw=[]; gateway,base=bridge(a.gateway_server,private_gateway)
    try:
      for task in data["tasks"]:
        started=time.monotonic(); lex=lexical(task["query"],data["sources"],a.limit); latency=(time.monotonic()-started)*1000
        raw.append({"task_id":task["task_id"],"system":SYSTEMS[0],"receipts":lex}); r=runs[SYSTEMS[0]]; r["completed"]+=1; r["receipt_count"]+=len(lex); r["latencies"].append(latency); r["costs"].append(0); r["metric_rows"].append(score(lex,task["gold"]))
        offset=len(private_gateway.read_text().splitlines()) if private_gateway.exists() else 0
        try:
          indexed,telemetry=tree(task["query"],data["sources"],a.sidecar,config,20,base,out/"pageindex-cache",a.pageindex_timeout_seconds); cost=costs(private_gateway,offset); hybrid=hybrid_rrf(lex,indexed,a.limit)
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
      r["metrics"]={k:sum(float(x[k]) for x in scored)/len(scored) if scored else None for k in ("document_locator_recall_at_k","evidence_set_coverage","complete_evidence_set_success","quote_binding_rate","citation_precision","receipt_pass_rate")}
    tasks=[{"task_id":t["task_id"],"query_digest":sha(t["query"]),"gold_response_digest":sha(t["gold_response"]),"gold_locator_digest":sha(json.dumps(t["gold"],sort_keys=True))} for t in data["tasks"]]
    report={"schema_version":"proofpress/retrieval-panel-sanitized/v3","manifest_digest":sha(json.dumps({"sources":[{"uri":s["uri"],"content_digest":s["content_digest"],"media_type":s["media_type"]} for s in data["sources"]],"tasks":tasks},sort_keys=True)),"models":{"decomposition":DECOMPOSITION_MODEL,"proposer":PROPOSER_MODEL,"critic":CRITIC_MODEL,"executor":MODEL},"provider":PROVIDER,"fallback":"forbidden","tasks":tasks,"systems":runs,"scoring_boundary":"answer-only tasks have no locator metric denominator and are reported as unscored","decision_boundary":"private operating decision; not evidence that PageIndex is generally supported"}
    (out/"raw-private-receipts.json").write_text(json.dumps(raw,indent=2),encoding="utf-8"); (out/"sanitized-report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"sanitized_report":str(out/"sanitized-report.json"),"systems":runs},indent=2))
if __name__=="__main__": main()

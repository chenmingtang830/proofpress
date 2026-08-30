#!/usr/bin/env python3
"""Freeze a caller-downloaded Hugging Face APEX golden response privately.

This deliberately accepts an already authorized local download. It neither
downloads corpus material nor prints a prompt, answer, locator, or local path.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

SCHEMA="proofpress/private-retrieval-panel/v2"
def sha(text): return "sha256:"+hashlib.sha256(text.encode()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--tasks-json",required=True); ap.add_argument("--task-id",required=True); ap.add_argument("--sources-json",required=True); ap.add_argument("--gold-locators-json",required=True); ap.add_argument("--out",required=True); a=ap.parse_args()
    raw=json.loads(Path(a.tasks_json).read_text(encoding="utf-8")); rows=raw.get("tasks",raw) if isinstance(raw,dict) else raw
    task=next((x for x in rows if x.get("task_id")==a.task_id),None)
    if not task or not isinstance(task.get("gold_response"),str): raise SystemExit("requested task has no golden response")
    sources=json.loads(Path(a.sources_json).read_text(encoding="utf-8")); gold=json.loads(Path(a.gold_locators_json).read_text(encoding="utf-8"))
    if not isinstance(sources,list) or not isinstance(gold,list): raise SystemExit("sources and locators must be arrays")
    record={"schema_version":SCHEMA,"sources":sources,"tasks":[{"task_id":a.task_id,"query":task.get("prompt",task.get("task_name","")),"gold_response":task["gold_response"],"gold":gold}]}
    Path(a.out).write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"ok":True,"task_id":a.task_id,"gold_response_digest":sha(task["gold_response"]),"source_count":len(sources),"gold_locator_count":len(gold)}))
if __name__=="__main__": main()

#!/usr/bin/env python3
"""Create a private answer-only panel manifest from an authorized HF download.

The public repository never receives corpus bytes, filenames, prompts, or the
golden answer.  Since APEX task records do not contain source/page ground
truth, this prepares an explicitly unscored locator mode rather than fabricating
gold locators from a retrieval system's output.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path

SCHEMA = "proofpress/private-retrieval-panel/v2"

def sha_bytes(value): return "sha256:" + hashlib.sha256(value).hexdigest()
def sha_text(value): return sha_bytes(value.encode())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks-json", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--workspace", required=True, help="authorized private output directory")
    parser.add_argument("--out", required=True, help="private manifest path")
    parser.add_argument("--max-sources", type=int, default=0)
    parser.add_argument("--smallest-first", action="store_true")
    args = parser.parse_args()
    rows = json.loads(Path(args.tasks_json).read_text(encoding="utf-8"))
    rows = rows.get("tasks", rows) if isinstance(rows, dict) else rows
    task = next((row for row in rows if row.get("task_id") == args.task_id), None)
    if not task or not isinstance(task.get("gold_response"), str) or not task.get("prompt"):
        raise SystemExit("requested HF task is not usable")
    workspace = Path(args.workspace); text_dir = workspace / "extracted-text"; text_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(Path(args.corpus).rglob("*.pdf"))
    if args.smallest_first: files.sort(key=lambda path: (path.stat().st_size, str(path)))
    if args.max_sources: files = files[:args.max_sources]
    if not files: raise SystemExit("no PDF sources found in authorized corpus")
    sources = []
    for path in files:
        payload = path.read_bytes(); digest = sha_bytes(payload); source_id = digest.removeprefix("sha256:")[:24]
        text_path = text_dir / (source_id + ".txt")
        if not text_path.exists():
            run = subprocess.run(["pdftotext", str(path), str(text_path)], capture_output=True, text=True)
            if run.returncode: raise SystemExit("PDF extraction failed for a custody-verified source")
        sources.append({"source_id": source_id, "uri": "private://apex/" + source_id,
                        "path": str(path), "content_digest": digest,
                        "media_type": "application/pdf", "extracted_text_path": str(text_path)})
    output = {"schema_version": SCHEMA, "sources": sources,
              "tasks": [{"task_id": args.task_id, "query": task["prompt"],
                         "gold_response": task["gold_response"], "gold": []}]}
    Path(args.out).write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "task_id": args.task_id,
                      "gold_response_digest": sha_text(task["gold_response"]),
                      "source_count": len(sources), "scoring_mode": "answer_only_unscored"}))

if __name__ == "__main__": main()

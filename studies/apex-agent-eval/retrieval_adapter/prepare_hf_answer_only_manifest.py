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
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--task-id", action="append", dest="task_ids")
    selection.add_argument("--world-id")
    parser.add_argument("--max-tasks", type=int, default=0)
    parser.add_argument("--min-gold-chars", type=int, default=1)
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--workspace", required=True, help="authorized private output directory")
    parser.add_argument("--out", required=True, help="private manifest path")
    parser.add_argument("--max-sources", type=int, default=0)
    parser.add_argument("--smallest-first", action="store_true")
    parser.add_argument("--all-sources", action="store_true",
                        help="include every readable corpus file for the full evidence substrate (PageIndex still requires PDF sources)")
    parser.add_argument("--include-hidden", action="store_true",
                        help="include hidden app-data files under a world root; .apex-data metadata is always excluded")
    args = parser.parse_args()
    rows = json.loads(Path(args.tasks_json).read_text(encoding="utf-8"))
    rows = rows.get("tasks", rows) if isinstance(rows, dict) else rows
    requested = set(args.task_ids or [])
    tasks = [row for row in rows
             if ((row.get("task_id") in requested) if requested else (row.get("world_id") == args.world_id))
             and isinstance(row.get("gold_response"), str) and row.get("prompt")
             and len(row["gold_response"]) >= args.min_gold_chars]
    tasks.sort(key=lambda row: row["task_id"])
    if args.max_tasks: tasks = tasks[:args.max_tasks]
    if not tasks or (requested and {row["task_id"] for row in tasks} != requested):
        raise SystemExit("requested HF task selection is incomplete or unusable")
    workspace = Path(args.workspace); text_dir = workspace / "extracted-text"; text_dir.mkdir(parents=True, exist_ok=True)
    corpus_root = Path(args.corpus).resolve()
    files = sorted(path for path in corpus_root.rglob("*")
                   if path.is_file()
                   and ".apex-data" not in path.relative_to(corpus_root).parts
                   and (args.include_hidden or not any(part.startswith(".") for part in path.relative_to(corpus_root).parts))
                   and (args.all_sources or path.suffix.lower() == ".pdf"))
    if args.smallest_first: files.sort(key=lambda path: (path.stat().st_size, str(path)))
    if args.max_sources: files = files[:args.max_sources]
    if not files: raise SystemExit("no PDF sources found in authorized corpus")
    sources = []
    for path in files:
        payload = path.read_bytes(); digest = sha_bytes(payload); source_id = digest.removeprefix("sha256:")[:24]
        text_path = text_dir / (source_id + ".txt")
        if not text_path.exists():
            if path.suffix.lower() == ".pdf":
                run = subprocess.run(["pdftotext", str(path), str(text_path)], capture_output=True, text=True)
                if run.returncode: raise SystemExit("PDF extraction failed for a custody-verified source")
            else:
                text_path.write_text(path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        media_type = "application/pdf" if path.suffix.lower() == ".pdf" else "text/plain"
        sources.append({"source_id": source_id, "uri": "private://apex/" + source_id,
                        "path": str(path), "content_digest": digest,
                        "media_type": media_type, "extracted_text_path": str(text_path)})
    task_rows = [{"task_id": task["task_id"], "query": task["prompt"],
                  "gold_response": task["gold_response"], "gold": []}
                 for task in tasks]
    output = {"schema_version": SCHEMA, "sources": sources, "tasks": task_rows}
    Path(args.out).write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "task_count": len(tasks),
                      "task_set_digest": sha_text("\n".join(row["task_id"] for row in tasks)),
                      "gold_response_digests": [sha_text(row["gold_response"]) for row in tasks],
                      "source_count": len(sources), "scoring_mode": "answer_only_unscored"}))

if __name__ == "__main__": main()

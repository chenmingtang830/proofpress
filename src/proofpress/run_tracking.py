"""Thin CLI for the task-run operation contract; separate from portable history."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from proofpress.client import ProofpressClient


def _client(args):
    if args.base_url:
        token = os.environ.get(args.token_env)
        if not token: raise SystemExit(f"missing bearer token in {args.token_env}")
        return (ProofpressClient.remote(args.base_url, token)
                if args.base_url.startswith("https://")
                else ProofpressClient.localhost(args.base_url, token))
    workspace = Path(args.workspace).resolve()
    os.chdir(workspace)
    return ProofpressClient.in_process(workspace)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="proofpress run")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--base-url")
    parser.add_argument("--token-env", default="PROOFPRESS_TOKEN")
    parser.add_argument("--actor", default=os.environ.get("PROOFPRESS_PRINCIPAL"))
    sub = parser.add_subparsers(dest="command", required=True)
    start = sub.add_parser("start"); start.add_argument("purpose"); start.add_argument("--idempotency-key")
    finish = sub.add_parser("finish"); finish.add_argument("run_id"); finish.add_argument("status", choices=("completed", "failed", "aborted")); finish.add_argument("--summary"); finish.add_argument("--idempotency-key")
    get = sub.add_parser("get"); get.add_argument("run_id")
    listing = sub.add_parser("list"); listing.add_argument("--status", choices=("running", "completed", "failed", "aborted")); listing.add_argument("--limit", type=int, default=50)
    capture = sub.add_parser("capture"); capture.add_argument("run_id"); capture.add_argument("--scope"); capture.add_argument("--task"); capture.add_argument("--idempotency-key")
    rely = sub.add_parser("rely"); rely.add_argument("run_id"); rely.add_argument("receipt_id"); rely.add_argument("claim_id"); rely.add_argument("claim_digest"); rely.add_argument("purpose"); rely.add_argument("--idempotency-key")
    output = sub.add_parser("output"); output.add_argument("run_id"); output.add_argument("reference"); output.add_argument("content_digest"); output.add_argument("--summary"); output.add_argument("--reliance", action="append", default=[]); output.add_argument("--media-type"); output.add_argument("--idempotency-key")
    observe = sub.add_parser("observe"); observe.add_argument("run_id"); observe.add_argument("kind", choices=("test", "human", "external_evaluation", "outcome")); observe.add_argument("source"); observe.add_argument("meaning"); observe.add_argument("--evidence", action="append", default=[]); observe.add_argument("--output", action="append", default=[]); observe.add_argument("--observed-at"); observe.add_argument("--idempotency-key")
    args = parser.parse_args(argv)
    if not args.actor: raise SystemExit("--actor or PROOFPRESS_PRINCIPAL is required for run tracking")
    client = _client(args); c = args.command
    if c == "start": result = client.start_run(args.purpose, actor=args.actor, idempotency_key=args.idempotency_key)
    elif c == "finish": result = client.finish_run(args.run_id, args.status, actor=args.actor, summary=args.summary, idempotency_key=args.idempotency_key)
    elif c == "get": result = client.get_run(args.run_id, actor=args.actor)
    elif c == "list": result = client.list_runs(actor=args.actor, status=args.status, limit=args.limit)
    elif c == "capture": result = client.capture_context(args.run_id, actor=args.actor, scope=args.scope, task=args.task, idempotency_key=args.idempotency_key)
    elif c == "rely": result = client.record_reliance(args.run_id, args.receipt_id, args.claim_id, args.claim_digest, args.purpose, actor=args.actor, idempotency_key=args.idempotency_key)
    elif c == "output": result = client.record_output(args.run_id, args.reference, args.content_digest, actor=args.actor, summary=args.summary, reliance_ids=args.reliance, media_type=args.media_type, idempotency_key=args.idempotency_key)
    else: result = client.record_observation(args.run_id, args.kind, args.source, args.meaning, actor=args.actor, evidence_refs=args.evidence, output_ids=args.output, observed_at=args.observed_at, idempotency_key=args.idempotency_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))

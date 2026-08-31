#!/usr/bin/env python3
"""Small owner/agent CLI for a personal hosted Proofpress workspace."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from proofpress_sdk import ProofpressClient, ProofpressError


def _client(args):
    token = os.environ.get(args.token_env)
    if not token:
        raise SystemExit(f"missing hosted credential in {args.token_env}")
    if args.base_url.startswith("https://"):
        return ProofpressClient.remote(args.base_url, token, args.timeout)
    return ProofpressClient.localhost(args.base_url, token, args.timeout)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="proofpress-remote")
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--token-env", default="PROOFPRESS_TOKEN")
    parser.add_argument("--timeout", type=float, default=30.0)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("capabilities")
    submit = subparsers.add_parser("submit-evidence")
    submit.add_argument("file")
    submit.add_argument("--idempotency-key")
    propose = subparsers.add_parser("propose")
    propose.add_argument("--statement", required=True)
    propose.add_argument("--evidence", action="append", required=True)
    propose.add_argument("--scope", required=True)
    propose.add_argument("--idempotency-key")
    evaluate = subparsers.add_parser("evaluate")
    evaluate.add_argument("conclusion_id")
    review = subparsers.add_parser("review")
    review.add_argument("conclusion_id")
    decisions = review.add_mutually_exclusive_group(required=True)
    decisions.add_argument("--admit", action="store_true")
    decisions.add_argument("--reject", action="store_true")
    decisions.add_argument("--request-changes", action="store_true")
    review.add_argument("--note")
    review.add_argument("--request-id", required=True)
    review.add_argument("--expected-head")
    context = subparsers.add_parser("context")
    context.add_argument("--scope")
    context.add_argument("--task")
    summary = subparsers.add_parser("review-summary")
    summary.add_argument("--scope")
    receipt = subparsers.add_parser("review-receipt")
    receipt.add_argument("conclusion_id")
    args = parser.parse_args(argv)
    client = _client(args)
    try:
        if args.command == "capabilities":
            result = client.capabilities()
        elif args.command == "submit-evidence":
            payload = json.loads(Path(args.file).read_text(encoding="utf-8"))
            result = client.submit_evidence(
                payload, idempotency_key=args.idempotency_key)
        elif args.command == "propose":
            result = client.propose_conclusion(
                args.statement, args.evidence, args.scope, "server-derived",
                idempotency_key=args.idempotency_key)
        elif args.command == "evaluate":
            result = client.evaluate_conclusion(args.conclusion_id)
        elif args.command == "review":
            decision = "admit" if args.admit else "reject" if args.reject \
                else "request_changes"
            result = client.review_conclusion(
                args.conclusion_id, decision, "server-derived", note=args.note,
                review_request_id=args.request_id,
                expected_head=args.expected_head)
        elif args.command == "context":
            result = client.context(
                scope=args.scope, actor="server-derived", task=args.task)
        elif args.command == "review-summary":
            result = client.review_summary(args.scope)
        else:
            result = client.review_receipt(args.conclusion_id)
    except (ProofpressError, OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

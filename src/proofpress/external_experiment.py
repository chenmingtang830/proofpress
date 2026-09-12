"""CLI for vendor-neutral external experiment evidence ingestion."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from proofpress.client import ProofpressClient


def _client(args):
    if args.base_url:
        token = os.environ.get(args.token_env)
        if not token:
            raise SystemExit(f"missing bearer token in {args.token_env}")
        return (ProofpressClient.remote(args.base_url, token)
                if args.base_url.startswith("https://")
                else ProofpressClient.localhost(args.base_url, token))
    workspace = Path(args.workspace).resolve()
    os.chdir(workspace)
    return ProofpressClient.in_process(workspace)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="proofpress experiment")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--base-url")
    parser.add_argument("--token-env", default="PROOFPRESS_TOKEN")
    parser.add_argument("--actor", default=os.environ.get("PROOFPRESS_PRINCIPAL"))
    sub = parser.add_subparsers(dest="command", required=True)
    ingest = sub.add_parser(
        "ingest", help="ingest a bounded external experiment manifest")
    ingest.add_argument("manifest", type=Path)
    ingest.add_argument("--idempotency-key")
    args = parser.parse_args(argv)
    if not args.actor:
        raise SystemExit(
            "--actor or PROOFPRESS_PRINCIPAL is required for experiment ingestion")
    try:
        payload = json.loads(args.manifest.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"manifest not found: {args.manifest}") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"manifest must be valid UTF-8 JSON: {exc}") from exc
    result = _client(args).ingest_external_experiment(
        payload, actor=args.actor, idempotency_key=args.idempotency_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

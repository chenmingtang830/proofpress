"""Single-repository evidence bundle adapter and self-dogfood workflow."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

from proofpress.profiles.repository import (
    REPO_EVIDENCE_SCHEMA, REPO_PROFILE_SCHEMA as REPO_PROFILE_SCHEMA,
    CLAIM_KINDS as CLAIM_KINDS, CHECK_STATUSES as CHECK_STATUSES,
    digest, repository_identity, verify_bundle as verify_bundle, repo_qualifiers,
    _git, _workspace_root, _canonical_remote, _commit, _read_check,
)


def build_bundle(workspace: str | Path, *, base_ref: str, head_ref: str = "HEAD",
                 check_receipts: Iterable[str | Path], pr_number: int | None = None,
                 pr_url: str | None = None) -> dict[str, Any]:
    """Build one bounded, secret-minimized evidence projection for a Git change."""
    root = _workspace_root(workspace)
    remote = _canonical_remote(_git(root, "remote", "get-url", "origin"))
    base, head = _commit(root, base_ref), _commit(root, head_ref)
    if base == head:
        raise ValueError("repo evidence requires distinct base and head commits")
    merge_base = _git(root, "merge-base", base, head).strip()
    if merge_base != base:
        raise ValueError("base commit must be an ancestor of head commit")
    diff = _git(root, "diff", "--binary", "--full-index", base, head, text=False)
    paths_raw = _git(root, "diff", "--name-only", "-z", base, head, text=False)
    paths = sorted({value.decode("utf-8") for value in paths_raw.split(b"\0") if value})
    if not paths:
        raise ValueError("repo evidence change has no changed paths")
    checks = [_read_check(path, head) for path in check_receipts]
    if not checks:
        raise ValueError("repo evidence requires at least one check receipt")
    if pr_number is not None and (isinstance(pr_number, bool) or pr_number < 1):
        raise ValueError("pull request number must be a positive integer")
    pull_request = {"number": pr_number, "url": pr_url} if pr_number else None
    bundle = {
        "schema_version": REPO_EVIDENCE_SCHEMA,
        "repository": {"id": repository_identity(remote), "remote": remote},
        "change": {"base_commit": base, "head_commit": head,
                   "diff_digest": "sha256:" + hashlib.sha256(diff).hexdigest(),
                   "changed_paths": paths},
        "checks": checks,
    }
    if pull_request:
        bundle["pull_request"] = pull_request
    bundle["bundle_digest"] = digest(bundle)
    return bundle


def write_bundle(path: str | Path, bundle: dict[str, Any]) -> Path:
    target = Path(path)
    target.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    return target


def propose_candidate(client, bundle_path: str | Path, *, title: str, statement: str,
                      claim_kind: str, scope: str, proposer: str,
                      idempotency_prefix: str) -> dict[str, Any]:
    """Import, propose, and evaluate; deliberately stop before Human Approval."""
    bundle = json.loads(Path(bundle_path).read_text(encoding="utf-8"))
    imported = client.import_evidence(
        bundle_path, idempotency_key=idempotency_prefix + ":evidence")
    evidence_refs = imported.get("imported_evidence")
    if not evidence_refs:
        raise ValueError("repo evidence import returned no imported_evidence")
    proposal = client.propose_claim(
        statement, evidence_refs, scope, proposer, profile="repo", title=title,
        qualifiers=repo_qualifiers(bundle, claim_kind),
        idempotency_key=idempotency_prefix + ":proposal")
    claim_id = proposal["claim"]["id"]
    evaluation = client.evaluate_claim(
        claim_id, idempotency_key=idempotency_prefix + ":evaluation")
    return {"candidate": proposal["claim"], "evaluation": evaluation,
            "next": "independent Human Approval is required for admission"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="proofpress repo",
        description="Proofpress single-repo dogfood helper")
    sub = parser.add_subparsers(dest="command", required=True)
    bundle = sub.add_parser("bundle", help="create a bounded repository evidence bundle")
    bundle.add_argument("--workspace", default=".")
    bundle.add_argument("--base-ref", required=True); bundle.add_argument("--head-ref", default="HEAD")
    bundle.add_argument("--check", action="append", required=True, dest="checks")
    bundle.add_argument("--pr-number", type=int); bundle.add_argument("--pr-url")
    bundle.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    if args.command == "bundle":
        result = build_bundle(args.workspace, base_ref=args.base_ref,
                              head_ref=args.head_ref, check_receipts=args.checks,
                              pr_number=args.pr_number, pr_url=args.pr_url)
        write_bundle(args.output, result)
        print(json.dumps({"ok": True, "output": str(Path(args.output).resolve()),
                          "bundle_digest": result["bundle_digest"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

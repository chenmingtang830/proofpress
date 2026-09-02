"""Single-repository evidence bundles and self-dogfood workflow helpers."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Iterable
from urllib.parse import urlparse


REPO_EVIDENCE_SCHEMA = "proofpress/repo-evidence-bundle/v1"
REPO_PROFILE_SCHEMA = "proofpress/profile/repository/v1"
CLAIM_KINDS = {"capability", "boundary", "limitation", "roadmap"}
CHECK_STATUSES = {"pass", "fail"}
_SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")


def _canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canon(value)).hexdigest()


def _git(workspace: Path, *args: str, text: bool = True):
    result = subprocess.run(["git", *args], cwd=workspace, capture_output=True,
                            text=text)
    if result.returncode:
        detail = result.stderr.strip() if text else result.stderr.decode().strip()
        raise ValueError(f"git {' '.join(args)}: {detail}")
    return result.stdout


def _workspace_root(workspace: str | Path) -> Path:
    requested = Path(workspace).resolve()
    root = Path(_git(requested, "rev-parse", "--show-toplevel").strip()).resolve()
    if requested != root:
        raise ValueError("repo dogfood workspace must be the Git repository root")
    return root


def _canonical_remote(raw: str) -> str:
    value = raw.strip()
    if not value:
        raise ValueError("repository remote is required")
    if value.startswith("git@"):
        host, path = value[4:].split(":", 1)
        value = f"https://{host}/{path}"
    elif value.startswith("ssh://"):
        parsed = urlparse(value)
        value = f"https://{parsed.hostname}{parsed.path}"
    parsed = urlparse(value)
    if parsed.username or parsed.password:
        raise ValueError("repository remote must not contain credentials")
    if parsed.scheme not in {"https", "http"} or not parsed.hostname:
        raise ValueError("repository remote must be an HTTP(S) or Git SSH remote")
    normalized = value[:-4] if value.endswith(".git") else value
    return normalized.rstrip("/")


def repository_identity(remote: str) -> str:
    return "repo_" + hashlib.sha256(remote.encode()).hexdigest()[:16]


def _commit(workspace: Path, ref: str) -> str:
    value = _git(workspace, "rev-parse", "--verify", f"{ref}^{{commit}}").strip()
    if not re.fullmatch(r"[0-9a-f]{40}", value):
        raise ValueError(f"invalid commit resolved from {ref}")
    return value


def _read_check(path: str | Path, head_commit: str) -> dict[str, Any]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("check receipt must be a JSON object")
    allowed = {"name", "status", "commit", "url", "workflow", "run_id",
               "command", "output_digest"}
    unknown = set(raw) - allowed
    if unknown:
        raise ValueError("unsupported check receipt fields: " + ", ".join(sorted(unknown)))
    name, status, commit = raw.get("name"), raw.get("status"), raw.get("commit")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("check receipt name is required")
    if status not in CHECK_STATUSES:
        raise ValueError("check receipt status must be pass or fail")
    if commit != head_commit:
        raise ValueError("check receipt commit must equal the bundle head commit")
    if "output_digest" in raw and not _SHA256.fullmatch(str(raw["output_digest"])):
        raise ValueError("check receipt output_digest must be a sha256 digest")
    projected = {key: raw[key] for key in sorted(raw) if raw[key] is not None}
    projected["receipt_digest"] = digest(projected)
    return projected


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


def verify_bundle(payload: Any, workspace: str | Path) -> dict[str, bool]:
    """Recompute repository bindings; a pass is evidence, never admission."""
    checks = {"schema": False, "bundle_digest": False, "repository": False,
              "commits": False, "diff_digest": False, "changed_paths": False,
              "check_receipts": False, "checks_passed": False}
    if not isinstance(payload, dict) or payload.get("schema_version") != REPO_EVIDENCE_SCHEMA:
        return checks
    checks["schema"] = True
    body = {key: value for key, value in payload.items() if key != "bundle_digest"}
    checks["bundle_digest"] = payload.get("bundle_digest") == digest(body)
    try:
        root = _workspace_root(workspace)
        remote = _canonical_remote(_git(root, "remote", "get-url", "origin"))
        repository = payload["repository"]
        checks["repository"] = (repository == {
            "id": repository_identity(remote), "remote": remote})
        change = payload["change"]
        base = _commit(root, change["base_commit"])
        head = _commit(root, change["head_commit"])
        checks["commits"] = (_git(root, "merge-base", base, head).strip() == base)
        diff = _git(root, "diff", "--binary", "--full-index", base, head, text=False)
        checks["diff_digest"] = change.get("diff_digest") == (
            "sha256:" + hashlib.sha256(diff).hexdigest())
        raw_paths = _git(root, "diff", "--name-only", "-z", base, head, text=False)
        actual_paths = sorted({item.decode("utf-8") for item in raw_paths.split(b"\0") if item})
        checks["changed_paths"] = change.get("changed_paths") == actual_paths and bool(actual_paths)
        receipts = payload.get("checks")
        valid_receipts = isinstance(receipts, list) and bool(receipts)
        for receipt in receipts if isinstance(receipts, list) else []:
            projected = {key: value for key, value in receipt.items()
                         if key != "receipt_digest"}
            valid_receipts = bool(valid_receipts and
                                  receipt.get("commit") == head and
                                  receipt.get("status") in CHECK_STATUSES and
                                  receipt.get("receipt_digest") == digest(projected))
        checks["check_receipts"] = valid_receipts
        checks["checks_passed"] = bool(valid_receipts and
                                       all(row["status"] == "pass" for row in receipts))
    except (KeyError, TypeError, ValueError):
        pass
    return checks


def write_bundle(path: str | Path, bundle: dict[str, Any]) -> Path:
    target = Path(path)
    target.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    return target


def repo_qualifiers(bundle: dict[str, Any], claim_kind: str) -> dict[str, Any]:
    if claim_kind not in CLAIM_KINDS:
        raise ValueError("repo claim kind must be capability, boundary, limitation, or roadmap")
    return {"repo": {"schema_version": REPO_PROFILE_SCHEMA,
                     "claim_kind": claim_kind,
                     "repository_id": bundle["repository"]["id"],
                     "head_commit": bundle["change"]["head_commit"],
                     "pull_request": bundle.get("pull_request")}}


def propose_candidate(client, bundle_path: str | Path, *, statement: str,
                      claim_kind: str, scope: str, proposer: str,
                      idempotency_prefix: str) -> dict[str, Any]:
    """Import, propose, and evaluate; deliberately stop before Human Approval."""
    bundle = json.loads(Path(bundle_path).read_text(encoding="utf-8"))
    imported = client.import_evidence(
        bundle_path, idempotency_key=idempotency_prefix + ":evidence")
    evidence_refs = imported.get("imported_evidence")
    if not evidence_refs:
        raise ValueError("repo evidence import returned no imported_evidence")
    proposal = client.propose_conclusion(
        statement, evidence_refs, scope, proposer, profile="repo",
        qualifiers=repo_qualifiers(bundle, claim_kind),
        idempotency_key=idempotency_prefix + ":proposal")
    conclusion_id = proposal["conclusion"]["id"]
    evaluation = client.evaluate_conclusion(
        conclusion_id, idempotency_key=idempotency_prefix + ":evaluation")
    return {"candidate": proposal["conclusion"], "evaluation": evaluation,
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

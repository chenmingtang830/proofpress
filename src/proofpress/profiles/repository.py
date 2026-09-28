"""Repository evidence profile validation; a passing check is never admission."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any
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


def repo_qualifiers(bundle: dict[str, Any], claim_kind: str) -> dict[str, Any]:
    if claim_kind not in CLAIM_KINDS:
        raise ValueError("repo claim kind must be capability, boundary, limitation, or roadmap")
    return {"repo": {"schema_version": REPO_PROFILE_SCHEMA,
                     "claim_kind": claim_kind,
                     "repository_id": bundle["repository"]["id"],
                     "head_commit": bundle["change"]["head_commit"],
                     "pull_request": bundle.get("pull_request")}}

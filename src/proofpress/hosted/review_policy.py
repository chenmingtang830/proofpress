"""Versioned owner settings. Secrets and executable configuration never enter UI data."""
from __future__ import annotations

import json
import os
import re
import sys

from proofpress.kernel import operations as kernel

RUBRICS = {"evidence-support/v1": "Evidence support, source binding, missing evidence and limitations"}


def migrate(connection):
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS hosted_review_policies (
            workspace_id TEXT NOT NULL, version INTEGER NOT NULL,
            settings_json TEXT NOT NULL, policy_json TEXT NOT NULL,
            actor TEXT NOT NULL, created_at TEXT NOT NULL,
            PRIMARY KEY(workspace_id, version)
        );
        CREATE TABLE IF NOT EXISTS hosted_judge_jobs (
            job_id TEXT PRIMARY KEY, workspace_id TEXT NOT NULL,
            conclusion_id TEXT NOT NULL, policy_digest TEXT NOT NULL,
            requested_by TEXT NOT NULL, state TEXT NOT NULL,
            created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
            detail TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS hosted_context_reads (
            read_id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace_id TEXT NOT NULL, actor TEXT NOT NULL,
            scope TEXT, conclusion_ids_json TEXT NOT NULL, created_at TEXT NOT NULL
        );
    """)


def current(connection, workspace_id):
    row = connection.execute(
        "SELECT * FROM hosted_review_policies WHERE workspace_id=? ORDER BY version DESC LIMIT 1",
        (workspace_id,)).fetchone()
    if row:
        return {"version": row["version"], "settings": json.loads(row["settings_json"]),
                "policy": json.loads(row["policy_json"]), "actor": row["actor"],
                "updated_at": row["created_at"]}
    policy = kernel.load_v2_policy()
    command = policy["judge"]["command"]
    model = command[command.index("--model") + 1] if "--model" in command else ""
    return {"version": 0, "policy": policy, "actor": "deployment configuration",
            "updated_at": None, "settings": {
                "mode": "manual" if command else "off", "model": model,
                "rubric": "evidence-support/v1", "require_judge": bool(policy.get("require_judge")),
                "external_consent": False}}


def public(record):
    return {key: record[key] for key in ("version", "settings", "actor", "updated_at")} | {
        "policy_digest": record["policy"]["digest"], "rubrics": RUBRICS,
        "provider_ready": bool(os.environ.get("OPENROUTER_API_KEY"))}


def validate(settings, prior):
    if not isinstance(settings, dict) or set(settings) != {
        "mode", "model", "rubric", "require_judge", "external_consent"
    }:
        raise ValueError("Provide mode, model, rubric, require_judge and external_consent.")
    if settings["mode"] not in {"off", "manual", "automatic"}:
        raise ValueError("Select off, manual or automatic.")
    if settings["rubric"] not in RUBRICS:
        raise ValueError("Unsupported review rubric version.")
    if any(type(settings[k]) is not bool for k in ("require_judge", "external_consent")):
        raise ValueError("Consent and approval requirements must be boolean.")
    model = settings["model"]
    if not isinstance(model, str) or (model and not re.fullmatch(r"[A-Za-z0-9_.:/-]{1,160}", model)):
        raise ValueError("Use a provider/model identifier.")
    enabled = settings["mode"] != "off"
    if enabled and (not model or not settings["external_consent"]):
        raise ValueError("Choose a model and consent to sending bounded evidence to OpenRouter.")
    if not enabled and settings["require_judge"]:
        raise ValueError("Enable LM advice before making it an approval requirement.")
    if enabled and not os.environ.get("OPENROUTER_API_KEY"):
        raise ValueError("Configure OPENROUTER_API_KEY in the server environment first.")
    policy = json.loads(json.dumps(prior))
    policy["require_judge"] = settings["require_judge"]
    policy["judge"] = {"identity": "judge:openrouter-advisory", "timeout_seconds": 60,
                       "command": [sys.executable, "-m", "proofpress.hosted.judge", "--model", model] if enabled else []}
    # The rubric is part of the model packet and policy digest, not arbitrary executable code.
    policy["review_rubric"] = settings["rubric"]
    policy["digest"] = kernel.digest({k: v for k, v in policy.items() if k != "digest"})
    return policy


def semantic_event(event, initiator):
    kind = event.get("type")
    labels = {"conclusion_proposed": "Proposed a conclusion", "evidence_bound": "Submitted evidence",
              "policy_evaluated": "Checked evidence", "judge_recommended": "Reviewed evidence with LM",
              "conclusion_admitted": "Approved for reuse", "conclusion_rejected": "Rejected a conclusion",
              "conclusion_revision_requested": "Requested changes", "conclusion_superseded": "Replaced a conclusion",
              "relation_proposed": "Proposed a relationship", "relation_admitted": "Approved a relationship"}
    if kind not in labels:
        return None
    actor = event.get("verifier") or event.get("judge") or event.get("reviewer") or event.get("conclusion", {}).get("proposer") or initiator
    outcome = {"conclusion_admitted": "admitted", "conclusion_rejected": "rejected",
               "conclusion_revision_requested": "needs_revision"}.get(kind, "recorded")
    detail = event.get("note") or ""
    if kind == "policy_evaluated":
        failed = [name.replace("_", " ") for name, passed in event.get("checks", {}).items() if not passed]
        outcome = "checks_passed" if event.get("eligible") else "blocked"
        detail = ", ".join(failed) if failed else "All deterministic checks passed"
    if kind == "judge_recommended":
        outcome = {"accept": "evidence_supported", "reject": "evidence_not_supported", "escalate": "needs_attention"}.get(event.get("recommendation"), "recorded")
        detail = event.get("rationale", "")
    return {"id": event["event_id"], "occurred_at": event["created_at"],
            "actor": actor, "initiator": initiator, "action": labels[kind], "outcome": outcome,
            "subject_id": event.get("subject_ref"), "detail": detail,
            "model": event.get("model"), "kind": kind}

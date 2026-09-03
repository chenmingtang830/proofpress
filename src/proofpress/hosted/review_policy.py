"""Versioned owner settings. Secrets and executable configuration never enter UI data."""
from __future__ import annotations

import json
import ipaddress
import os
import re
import sys
from urllib.parse import urlparse

from proofpress.kernel import operations as kernel

RUBRICS = {"evidence-support/v1": "Evidence support, source binding, missing evidence and limitations"}
PROVIDERS = {
    "openrouter": {"label": "OpenRouter", "endpoint": "https://openrouter.ai/api/v1/chat/completions", "zdr": True},
    "openai": {"label": "OpenAI", "endpoint": "https://api.openai.com/v1/chat/completions", "zdr": False},
    "anthropic": {"label": "Anthropic", "endpoint": "https://api.anthropic.com/v1/messages", "zdr": False},
    "custom": {"label": "Custom OpenAI-compatible", "endpoint": "", "zdr": False},
}
POLICY_AUTHORING_PROMPT = """Help me author a Proofpress workspace review policy. Ask me concise questions about the knowledge being reviewed, evidence requirements, sensitive data, acceptable external model providers, escalation conditions, and when a human must decide. Then return only JSON with these fields: provider, endpoint, model, criteria, zdr, mode, require_judge, external_consent. mode must be off, manual, or automatic. require_judge controls whether current supporting LM advice is required before human approval; the judge never approves knowledge. Do not request or include API keys, secrets, raw private traces, or credentials."""


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
        CREATE TABLE IF NOT EXISTS hosted_provider_secrets (
            workspace_id TEXT PRIMARY KEY, ciphertext BLOB NOT NULL,
            last_four TEXT NOT NULL, updated_at TEXT NOT NULL
        );
    """)


def current(connection, workspace_id):
    row = connection.execute(
        "SELECT * FROM hosted_review_policies WHERE workspace_id=? ORDER BY version DESC LIMIT 1",
        (workspace_id,)).fetchone()
    if row:
        settings = normalize(json.loads(row["settings_json"]))
        return {"version": row["version"], "settings": settings,
                "policy": json.loads(row["policy_json"]), "actor": row["actor"],
                "updated_at": row["created_at"]}
    policy = kernel.load_v2_policy()
    command = policy["judge"]["command"]
    model = command[command.index("--model") + 1] if "--model" in command else ""
    return {"version": 0, "policy": policy, "actor": "deployment configuration",
            "updated_at": None, "settings": normalize({
                "mode": "manual" if command else "off", "model": model,
                "rubric": "evidence-support/v1", "require_judge": bool(policy.get("require_judge")),
                "external_consent": False})}


def normalize(settings):
    return {"provider": "openrouter", "endpoint": "", "criteria": "", "zdr": True,
            "mode": "off", "model": "", "rubric": "evidence-support/v1",
            "require_judge": False, "external_consent": False, **settings}


def _cipher():
    from cryptography.fernet import Fernet
    key = os.environ.get("PROOFPRESS_SECRET_ENCRYPTION_KEY", "").strip().encode()
    if not key:
        raise ValueError("Secure credential storage is not configured for this deployment.")
    try:
        return Fernet(key)
    except ValueError as exc:
        raise ValueError("Secure credential storage is misconfigured.") from exc


def credential_status(connection, workspace_id):
    row = connection.execute("SELECT last_four, updated_at FROM hosted_provider_secrets WHERE workspace_id=?", (workspace_id,)).fetchone()
    return {"configured": bool(row), "last_four": row["last_four"] if row else None,
            "updated_at": row["updated_at"] if row else None,
            "storage_ready": bool(os.environ.get("PROOFPRESS_SECRET_ENCRYPTION_KEY"))}


def save_credential(connection, workspace_id, secret, updated_at):
    if not isinstance(secret, str) or not 8 <= len(secret) <= 8192:
        raise ValueError("Enter a valid provider API key.")
    encrypted = _cipher().encrypt(secret.encode())
    connection.execute("INSERT INTO hosted_provider_secrets VALUES (?, ?, ?, ?) ON CONFLICT(workspace_id) DO UPDATE SET ciphertext=excluded.ciphertext,last_four=excluded.last_four,updated_at=excluded.updated_at",
                       (workspace_id, encrypted, secret[-4:], updated_at))


def delete_credential(connection, workspace_id):
    connection.execute("DELETE FROM hosted_provider_secrets WHERE workspace_id=?", (workspace_id,))


def credential(connection, workspace_id):
    row = connection.execute("SELECT ciphertext FROM hosted_provider_secrets WHERE workspace_id=?", (workspace_id,)).fetchone()
    if not row:
        legacy = os.environ.get("OPENROUTER_API_KEY", "").strip()
        return legacy or None
    from cryptography.fernet import InvalidToken
    try:
        return _cipher().decrypt(row["ciphertext"]).decode()
    except InvalidToken as exc:
        raise ValueError("Stored provider credential cannot be decrypted.") from exc


def public(record, credential=None):
    return {key: record[key] for key in ("version", "settings", "actor", "updated_at")} | {
        "policy_digest": record["policy"]["digest"], "rubrics": RUBRICS,
        "providers": PROVIDERS, "credential": credential or {"configured": bool(os.environ.get("OPENROUTER_API_KEY")), "last_four": None, "updated_at": None, "storage_ready": bool(os.environ.get("PROOFPRESS_SECRET_ENCRYPTION_KEY"))},
        "authoring_prompt": POLICY_AUTHORING_PROMPT}


def _endpoint(settings):
    provider = settings["provider"]
    if provider != "custom":
        return PROVIDERS[provider]["endpoint"]
    value = settings["endpoint"].strip()
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Custom endpoints must use a public HTTPS URL.")
    if parsed.hostname in {"localhost", "localhost.localdomain"}:
        raise ValueError("Custom endpoints must use a public HTTPS URL.")
    try:
        if ipaddress.ip_address(parsed.hostname).is_private:
            raise ValueError("Custom endpoints must use a public HTTPS URL.")
    except ValueError as exc:
        if "public HTTPS" in str(exc):
            raise
    return value


def validate(settings, prior):
    if not isinstance(settings, dict) or set(settings) != {
        "provider", "endpoint", "model", "rubric", "criteria", "zdr",
        "mode", "require_judge", "external_consent"
    }:
        raise ValueError("Provide mode, model, rubric, require_judge and external_consent.")
    if settings["mode"] not in {"off", "manual", "automatic"}:
        raise ValueError("Select off, manual or automatic.")
    if settings["rubric"] not in RUBRICS:
        raise ValueError("Unsupported review rubric version.")
    if settings["provider"] not in PROVIDERS:
        raise ValueError("Select a supported model provider.")
    if any(type(settings[k]) is not bool for k in ("require_judge", "external_consent", "zdr")):
        raise ValueError("Consent and approval requirements must be boolean.")
    model = settings["model"]
    if not isinstance(model, str) or (model and not re.fullmatch(r"[A-Za-z0-9_.:/-]{1,160}", model)):
        raise ValueError("Use a provider/model identifier.")
    criteria = settings["criteria"]
    if not isinstance(criteria, str) or len(criteria) > 8000:
        raise ValueError("Evaluation criteria must be 8,000 characters or fewer.")
    endpoint = _endpoint(settings) if settings["mode"] != "off" else (settings["endpoint"].strip() if isinstance(settings["endpoint"], str) else "")
    enabled = settings["mode"] != "off"
    if enabled and (not model or not settings["external_consent"]):
        raise ValueError("Choose a model and consent to external processing.")
    if not enabled and settings["require_judge"]:
        raise ValueError("Enable LM advice before making it an approval requirement.")
    policy = json.loads(json.dumps(prior))
    policy["require_judge"] = settings["require_judge"]
    command = [sys.executable, "-m", "proofpress.hosted.judge", "--provider", settings["provider"],
               "--endpoint", endpoint, "--model", model, "--criteria", criteria]
    if settings["provider"] == "openrouter" and settings["zdr"]:
        command.append("--zdr")
    policy["judge"] = {"identity": f"judge:{settings['provider']}-advisory", "timeout_seconds": 60,
                       "command": command if enabled else []}
    # The rubric is part of the model packet and policy digest, not arbitrary executable code.
    policy["review_rubric"] = settings["rubric"]
    policy["data_handling"] = {"external_processing": settings["external_consent"],
                               "zero_data_retention": settings["provider"] == "openrouter" and settings["zdr"]}
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

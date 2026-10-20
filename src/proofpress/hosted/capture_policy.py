"""Versioned workspace capture guidance, separate from admission authority."""
from copy import deepcopy
import json
import hashlib

SCHEMA = "proofpress/capture-policy/v1alpha1"
DEFAULT_SETTINGS = {
    "purpose": "Preserve bounded findings that future work can reuse.",
    "capture": ["Evidence-backed conclusions", "Durable decisions", "Reproducible results"],
    "exclude": ["Unvalidated hypotheses", "Duplicate findings", "Routine progress updates"],
}
LIMITS = {
    "bounded_evidence_required": True,
    "secrets_and_raw_private_traces_excluded": True,
    "agent_cannot_approve_or_change_policy": True,
    "staged_context_is_draft_only": True,
}


def migrate(connection):
    connection.execute("""CREATE TABLE IF NOT EXISTS hosted_capture_policies (
        workspace_id TEXT NOT NULL REFERENCES hosted_workspaces(workspace_id),
        version INTEGER NOT NULL, settings_json TEXT NOT NULL,
        actor TEXT NOT NULL, created_at TEXT NOT NULL,
        PRIMARY KEY (workspace_id, version))""")


def current(connection, workspace_id):
    row = connection.execute(
        "SELECT * FROM hosted_capture_policies WHERE workspace_id=? ORDER BY version DESC LIMIT 1",
        (workspace_id,)).fetchone()
    settings = json.loads(row["settings_json"]) if row else deepcopy(DEFAULT_SETTINGS)
    policy_digest = "sha256:" + hashlib.sha256(json.dumps(
        {"schema_version": SCHEMA, "settings": settings, "limits": LIMITS},
        sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"schema_version": SCHEMA, "workspace_id": workspace_id,
            "policy_digest": policy_digest,
            "version": row["version"] if row else 0,
            "settings": settings,
            "actor": row["actor"] if row else None,
            "updated_at": row["created_at"] if row else None,
            "limits": deepcopy(LIMITS),
            "authority": "Proposal-selection guidance only; server checks and owner admission remain authoritative."}


def validate(settings):
    if not isinstance(settings, dict) or set(settings) != set(DEFAULT_SETTINGS):
        raise ValueError("Provide purpose, capture and exclude fields.")
    purpose = settings["purpose"]
    if not isinstance(purpose, str) or not purpose.strip() or len(purpose) > 1000:
        raise ValueError("Purpose must be 1–1,000 characters.")
    result = {"purpose": purpose.strip()}
    for key in ("capture", "exclude"):
        rows = settings[key]
        if (not isinstance(rows, list) or len(rows) > 30 or
                any(not isinstance(item, str) or not item.strip() or len(item) > 500 for item in rows)):
            raise ValueError("Use up to 30 non-empty rules of at most 500 characters each.")
        result[key] = list(dict.fromkeys(item.strip() for item in rows))
    if not result["capture"]:
        raise ValueError("Include at least one capture rule.")
    return result

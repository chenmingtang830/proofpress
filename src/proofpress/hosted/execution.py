"""Durable, content-minimizing records for keyed pilot operations.

The kernel event and idempotency transaction remains the write authority. These
rows describe attempts; they never authorize a claim or replay source content.
"""
from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timezone
from typing import Any

from proofpress.kernel import operations as kernel


TRACKED_OPERATIONS = frozenset({"evidence.submit", "experiment.ingest", "claim.evaluate"})
SCHEMA_VERSION = "proofpress/hosted-execution/v1"
RETRYABLE_ERRORS = frozenset({
    "ledger_head_conflict", "operation_io_error", "idempotency_store_write_failed",
})


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _bounded(value: Any) -> str | None:
    return (value if isinstance(value, str) and
            re.fullmatch(r"[A-Za-z0-9._:/-]{1,128}", value) else None)


def migrate(connection: sqlite3.Connection) -> None:
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS hosted_executions (
            execution_id TEXT PRIMARY KEY,
            workspace_id TEXT NOT NULL,
            principal_id TEXT NOT NULL,
            idempotency_key TEXT NOT NULL,
            operation TEXT NOT NULL,
            request_fingerprint TEXT NOT NULL,
            versions_json TEXT NOT NULL,
            input_refs_json TEXT NOT NULL,
            output_refs_json TEXT NOT NULL DEFAULT '{}',
            state TEXT NOT NULL CHECK(state IN ('running','succeeded',
                'retryable_failed','terminal_failed','interrupted')),
            error_code TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(workspace_id, principal_id, idempotency_key)
        );
        CREATE TABLE IF NOT EXISTS hosted_execution_attempts (
            attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            execution_id TEXT NOT NULL,
            started_at TEXT NOT NULL,
            finished_at TEXT,
            state TEXT NOT NULL CHECK(state IN ('running','succeeded',
                'retryable_failed','terminal_failed','interrupted')),
            error_code TEXT,
            idempotent_replay INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(execution_id) REFERENCES hosted_executions(execution_id)
        );
        CREATE INDEX IF NOT EXISTS hosted_executions_workspace_updated
            ON hosted_executions(workspace_id, updated_at);
    """)


def metadata(operation: str, parameters: dict[str, Any], policy: dict[str, Any]) -> tuple[dict, dict]:
    """Project only version identifiers and opaque links, never request content."""
    if operation == "claim.evaluate":
        verifier = policy.get("verification") or {}
        return ({"policy_digest": _bounded(policy.get("digest")),
                 "verification_profile": _bounded(verifier.get("profile")),
                 "verification_config_digest": kernel.digest(verifier)},
                {"claim_id": _bounded(parameters.get("claim_id"))})
    payload = parameters.get("payload")
    payload = payload if isinstance(payload, dict) else {}
    if operation == "experiment.ingest":
        adapter = payload.get("adapter")
        adapter = adapter if isinstance(adapter, dict) else {}
        binding = payload.get("binding")
        binding = binding if isinstance(binding, dict) else {}
        source = payload.get("source")
        source = source if isinstance(source, dict) else {}
        return ({"schema_version": _bounded(payload.get("schema_version")),
                 "adapter": _bounded(adapter.get("name")),
                 "adapter_version": _bounded(adapter.get("version")),
                 "config_digest": _bounded(binding.get("config_digest"))},
                {"run_id": _bounded(binding.get("proofpress_run_id")),
                 "external_run_id": _bounded(source.get("run_id"))})
    retrieval = payload.get("retrieval")
    retrieval = retrieval if isinstance(retrieval, dict) else {}
    return ({"schema_version": _bounded(payload.get("schema_version")),
             "profile": _bounded(parameters.get("profile")),
             "adapter": _bounded(retrieval.get("adapter")),
             "adapter_version": _bounded(retrieval.get("version")),
             "config_digest": _bounded(retrieval.get("config_digest"))}, {})


def begin(connection: sqlite3.Connection, *, workspace_id: str, principal_id: str,
          idempotency_key: str, operation: str, fingerprint: str,
          versions: dict, input_refs: dict) -> tuple[int | None, str | None]:
    """Reserve one attempt before execution; identical keys never run concurrently."""
    execution_id = kernel.digest([workspace_id, principal_id, idempotency_key])
    versions_json = json.dumps(versions, sort_keys=True)
    connection.execute("BEGIN IMMEDIATE")
    prior = connection.execute(
        "SELECT * FROM hosted_executions WHERE execution_id=?", (execution_id,)).fetchone()
    if prior:
        if (prior["operation"] != operation or
                prior["request_fingerprint"] != fingerprint):
            return None, "idempotency_conflict"
        if prior["versions_json"] != versions_json:
            return None, "execution_version_conflict"
        if prior["state"] == "running":
            return None, "execution_in_progress"
        if prior["state"] == "terminal_failed":
            return None, "execution_terminal"
        connection.execute(
            "UPDATE hosted_executions SET state='running', error_code=NULL, updated_at=? "
            "WHERE execution_id=?", (_now(), execution_id))
    else:
        at = _now()
        connection.execute(
            "INSERT INTO hosted_executions(execution_id,workspace_id,principal_id,"
            "idempotency_key,operation,request_fingerprint,versions_json,input_refs_json,"
            "state,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (execution_id, workspace_id, principal_id, idempotency_key, operation,
             fingerprint, versions_json, json.dumps(input_refs, sort_keys=True),
             "running", at, at))
    cursor = connection.execute(
        "INSERT INTO hosted_execution_attempts(execution_id,started_at,state) "
        "VALUES(?,?,'running')", (execution_id, _now()))
    return cursor.lastrowid, None


def finish(connection: sqlite3.Connection, attempt_id: int,
           envelope: dict[str, Any], *, workspace_id: str,
           principal_id: str) -> None:
    parent = connection.execute(
        "SELECT e.execution_id FROM hosted_execution_attempts a "
        "JOIN hosted_executions e ON e.execution_id=a.execution_id "
        "WHERE a.attempt_id=? AND e.workspace_id=? AND e.principal_id=?",
        (attempt_id, workspace_id, principal_id)).fetchone()
    if not parent:
        raise ValueError("execution_attempt_not_found")
    error_code = envelope.get("error", {}).get("code") if not envelope.get("ok") else None
    state = ("succeeded" if envelope.get("ok") else
             "retryable_failed" if error_code in RETRYABLE_ERRORS else "terminal_failed")
    result = envelope.get("result") or {}
    refs = {}
    if envelope.get("ok"):
        refs = {"evidence_ids": result.get("imported_evidence", [])}
        if not refs["evidence_ids"]:
            refs["evidence_ids"] = result.get("evidence", []) if isinstance(result.get("evidence"), list) else []
        if isinstance(result.get("event_id"), str):
            refs["evaluation_event_id"] = result["event_id"]
    connection.execute(
        "UPDATE hosted_execution_attempts SET state=?,error_code=?,finished_at=?,"
        "idempotent_replay=? WHERE attempt_id=? AND execution_id=?",
        (state, error_code, _now(), int(bool(envelope.get("idempotent_replay"))),
         attempt_id, parent["execution_id"]))
    connection.execute(
        "UPDATE hosted_executions SET state=?,error_code=?,output_refs_json=?,updated_at=? "
        "WHERE execution_id=? AND workspace_id=? AND principal_id=?",
        (state, error_code, json.dumps(refs, sort_keys=True), _now(),
         parent["execution_id"], workspace_id, principal_id))


def resume(connection: sqlite3.Connection, *, workspace_id: str) -> None:
    """An interrupted request waits for explicit resubmission with the same key."""
    at = _now()
    connection.execute(
        "UPDATE hosted_execution_attempts SET state='interrupted', finished_at=? "
        "WHERE state='running' AND execution_id IN "
        "(SELECT execution_id FROM hosted_executions WHERE workspace_id=?)",
        (at, workspace_id))
    connection.execute(
        "UPDATE hosted_executions SET state='interrupted', updated_at=? "
        "WHERE state='running' AND workspace_id=?", (at, workspace_id))

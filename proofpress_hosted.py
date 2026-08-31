"""Personal hosted workspace identity and authority boundary."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import hmac
import json
from pathlib import Path
import secrets
import sqlite3
from typing import Any

import proofpress_knowledge as knowledge
from proofpress_event_store import SQLiteEventStore, using_event_store


OWNER_ONLY_OPERATIONS = frozenset({
    "conclusion.review", "conclusion.supersede",
    "relation.review", "relation.resolve",
})
AGENT_OPERATIONS = frozenset({
    "capabilities.get", "configuration.get", "evidence.submit",
    "conclusion.propose", "conclusion.evaluate", "conclusion.judge",
    "conclusion.judge_batch", "relation.propose", "relation.evaluate",
    "relation.judge", "graph.get", "graph.traverse", "context.get",
    "review.summary", "review.receipt",
})
IDENTITY_PARAMETERS = {
    "conclusion.propose": "proposer",
    "relation.propose": "proposer",
    "conclusion.review": "reviewer",
    "conclusion.supersede": "reviewer",
    "relation.review": "reviewer",
    "relation.resolve": "reviewer",
    "context.get": "actor",
    "graph.traverse": "actor",
}


class HostedAuthError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class PrincipalContext:
    workspace_id: str
    principal_id: str
    role: str
    credential_id: str
    permissions: frozenset[str]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _secret_hash(secret: str, salt: bytes) -> bytes:
    return hashlib.scrypt(secret.encode("utf-8"), salt=salt,
                          n=2 ** 14, r=8, p=1, dklen=32)


class HostedControlPlane:
    """One-owner authority service over workspace-scoped SQLite history."""

    def __init__(self, database: str | Path):
        self.database = Path(database)
        self.database.parent.mkdir(parents=True, exist_ok=True)
        self._migrate()
        SQLiteEventStore(self.database, "__schema__", "system:migration")

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database, timeout=30)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 30000")
        return connection

    def _migrate(self) -> None:
        connection = self._connect()
        try:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS hosted_workspaces (
                    workspace_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS hosted_principals (
                    workspace_id TEXT NOT NULL,
                    principal_id TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('owner', 'agent')),
                    display_name TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, principal_id),
                    FOREIGN KEY (workspace_id) REFERENCES hosted_workspaces(workspace_id)
                );
                CREATE TABLE IF NOT EXISTS hosted_credentials (
                    credential_id TEXT PRIMARY KEY,
                    workspace_id TEXT NOT NULL,
                    principal_id TEXT NOT NULL,
                    label TEXT NOT NULL,
                    secret_salt BLOB NOT NULL,
                    secret_hash BLOB NOT NULL,
                    permissions_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_used_at TEXT,
                    revoked_at TEXT,
                    FOREIGN KEY (workspace_id, principal_id)
                        REFERENCES hosted_principals(workspace_id, principal_id)
                );
                CREATE TABLE IF NOT EXISTS hosted_audit (
                    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    occurred_at TEXT NOT NULL,
                    workspace_id TEXT,
                    principal_id TEXT,
                    credential_id TEXT,
                    operation TEXT,
                    request_id TEXT,
                    idempotency_key TEXT,
                    outcome TEXT NOT NULL,
                    event_head TEXT
                );
                CREATE TABLE IF NOT EXISTS hosted_recovery (
                    workspace_id TEXT PRIMARY KEY,
                    secret_salt BLOB NOT NULL,
                    secret_hash BLOB NOT NULL,
                    rotated_at TEXT NOT NULL,
                    FOREIGN KEY (workspace_id) REFERENCES hosted_workspaces(workspace_id)
                );
            """)
            connection.commit()
        finally:
            connection.close()

    @staticmethod
    def _new_credential_values() -> tuple[str, str, bytes, bytes]:
        credential_id = "cred_" + secrets.token_hex(8)
        secret = secrets.token_urlsafe(32)
        salt = secrets.token_bytes(16)
        return credential_id, f"pph_{credential_id}_{secret}", salt, _secret_hash(secret, salt)

    def bootstrap(self, workspace_id: str, owner_principal_id: str,
                  display_name: str = "Owner") -> dict[str, str]:
        if not workspace_id or not owner_principal_id:
            raise ValueError("workspace_id and owner_principal_id are required")
        credential_id, token, salt, secret_hash = self._new_credential_values()
        recovery_secret = secrets.token_urlsafe(40)
        recovery_salt = secrets.token_bytes(16)
        created_at = _now()
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            if connection.execute("SELECT 1 FROM hosted_workspaces LIMIT 1").fetchone():
                raise ValueError("personal hosted control plane is already bootstrapped")
            connection.execute("INSERT INTO hosted_workspaces VALUES (?, ?)",
                               (workspace_id, created_at))
            connection.execute(
                "INSERT INTO hosted_principals VALUES (?, ?, 'owner', ?, ?)",
                (workspace_id, owner_principal_id, display_name, created_at))
            connection.execute(
                "INSERT INTO hosted_credentials VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL)",
                (credential_id, workspace_id, owner_principal_id, "owner-bootstrap",
                 salt, secret_hash, json.dumps(["*"]), created_at))
            connection.execute(
                "INSERT INTO hosted_recovery VALUES (?, ?, ?, ?)",
                (workspace_id, recovery_salt,
                 _secret_hash(recovery_secret, recovery_salt), created_at))
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()
        return {"workspace_id": workspace_id, "principal_id": owner_principal_id,
                "credential_id": credential_id, "token": token,
                "recovery_secret": recovery_secret}

    @staticmethod
    def _split_token(token: str) -> tuple[str, str]:
        if not isinstance(token, str) or not token.startswith("pph_cred_"):
            raise HostedAuthError("invalid_credential", "invalid hosted bearer credential")
        parts = token.split("_", 3)
        if len(parts) != 4 or not parts[2] or not parts[3]:
            raise HostedAuthError("invalid_credential", "invalid hosted bearer credential")
        return "cred_" + parts[2], parts[3]

    def authenticate(self, token: str) -> PrincipalContext:
        credential_id, secret = self._split_token(token)
        connection = self._connect()
        try:
            row = connection.execute(
                "SELECT c.*, p.role FROM hosted_credentials c JOIN hosted_principals p "
                "USING(workspace_id, principal_id) WHERE credential_id = ?",
                (credential_id,)).fetchone()
            if not row or row["revoked_at"] is not None:
                raise HostedAuthError("invalid_credential", "invalid hosted bearer credential")
            actual = _secret_hash(secret, row["secret_salt"])
            if not hmac.compare_digest(actual, row["secret_hash"]):
                raise HostedAuthError("invalid_credential", "invalid hosted bearer credential")
            connection.execute(
                "UPDATE hosted_credentials SET last_used_at = ? WHERE credential_id = ?",
                (_now(), credential_id))
            connection.commit()
            return PrincipalContext(
                row["workspace_id"], row["principal_id"], row["role"],
                credential_id, frozenset(json.loads(row["permissions_json"])))
        finally:
            connection.close()

    def issue_agent_credential(self, owner_token: str, principal_id: str,
                               label: str, display_name: str | None = None,
                               permissions: set[str] | None = None) -> dict[str, str]:
        owner = self.authenticate(owner_token)
        if owner.role != "owner":
            raise HostedAuthError("owner_required", "owner credential required")
        granted = frozenset(permissions or AGENT_OPERATIONS)
        if not granted or not granted <= AGENT_OPERATIONS:
            raise ValueError("agent permissions must be a non-empty safe-operation subset")
        credential_id, token, salt, secret_hash = self._new_credential_values()
        created_at = _now()
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "INSERT OR IGNORE INTO hosted_principals VALUES (?, ?, 'agent', ?, ?)",
                (owner.workspace_id, principal_id, display_name or principal_id, created_at))
            row = connection.execute(
                "SELECT role FROM hosted_principals WHERE workspace_id = ? AND principal_id = ?",
                (owner.workspace_id, principal_id)).fetchone()
            if not row or row["role"] != "agent":
                raise ValueError("principal_id is not an agent principal")
            connection.execute(
                "INSERT INTO hosted_credentials VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL)",
                (credential_id, owner.workspace_id, principal_id, label, salt,
                 secret_hash, json.dumps(sorted(granted)), created_at))
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()
        return {"workspace_id": owner.workspace_id, "principal_id": principal_id,
                "credential_id": credential_id, "token": token}

    def revoke_credential(self, owner_token: str, credential_id: str) -> None:
        owner = self.authenticate(owner_token)
        if owner.role != "owner":
            raise HostedAuthError("owner_required", "owner credential required")
        if credential_id == owner.credential_id:
            raise ValueError("rotate the owner credential before revoking the active credential")
        connection = self._connect()
        try:
            cursor = connection.execute(
                "UPDATE hosted_credentials SET revoked_at = ? "
                "WHERE credential_id = ? AND workspace_id = ? AND revoked_at IS NULL",
                (_now(), credential_id, owner.workspace_id))
            if cursor.rowcount != 1:
                raise ValueError("active credential not found")
            connection.commit()
        finally:
            connection.close()

    def rotate_agent_credential(self, owner_token: str, credential_id: str,
                                label: str | None = None) -> dict[str, str]:
        owner = self.authenticate(owner_token)
        if owner.role != "owner":
            raise HostedAuthError("owner_required", "owner credential required")
        new_id, token, salt, secret_hash = self._new_credential_values()
        created_at = _now()
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT c.*, p.role FROM hosted_credentials c JOIN hosted_principals p "
                "USING(workspace_id, principal_id) WHERE credential_id = ? "
                "AND c.workspace_id = ? AND revoked_at IS NULL",
                (credential_id, owner.workspace_id)).fetchone()
            if not row or row["role"] != "agent":
                raise ValueError("active agent credential not found")
            connection.execute(
                "INSERT INTO hosted_credentials VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL)",
                (new_id, owner.workspace_id, row["principal_id"], label or row["label"],
                 salt, secret_hash, row["permissions_json"], created_at))
            connection.execute(
                "UPDATE hosted_credentials SET revoked_at = ? WHERE credential_id = ?",
                (created_at, credential_id))
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()
        return {"workspace_id": owner.workspace_id,
                "principal_id": row["principal_id"], "credential_id": new_id,
                "token": token}

    def recover_owner(self, workspace_id: str,
                      recovery_secret: str) -> dict[str, str]:
        connection = self._connect()
        try:
            row = connection.execute(
                "SELECT r.*, p.principal_id FROM hosted_recovery r "
                "JOIN hosted_principals p USING(workspace_id) "
                "WHERE r.workspace_id = ? AND p.role = 'owner'",
                (workspace_id,)).fetchone()
            if not row or not hmac.compare_digest(
                    _secret_hash(recovery_secret, row["secret_salt"]),
                    row["secret_hash"]):
                raise HostedAuthError("invalid_recovery_secret",
                                      "invalid owner recovery secret")
            credential_id, token, salt, secret_hash = self._new_credential_values()
            next_recovery = secrets.token_urlsafe(40)
            next_salt = secrets.token_bytes(16)
            rotated_at = _now()
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "UPDATE hosted_credentials SET revoked_at = ? WHERE workspace_id = ? "
                "AND principal_id = ? AND revoked_at IS NULL",
                (rotated_at, workspace_id, row["principal_id"]))
            connection.execute(
                "INSERT INTO hosted_credentials VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL)",
                (credential_id, workspace_id, row["principal_id"], "owner-recovery",
                 salt, secret_hash, json.dumps(["*"]), rotated_at))
            connection.execute(
                "UPDATE hosted_recovery SET secret_salt = ?, secret_hash = ?, rotated_at = ? "
                "WHERE workspace_id = ?",
                (next_salt, _secret_hash(next_recovery, next_salt),
                 rotated_at, workspace_id))
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()
        return {"workspace_id": workspace_id, "principal_id": row["principal_id"],
                "credential_id": credential_id, "token": token,
                "recovery_secret": next_recovery}

    @staticmethod
    def _error_envelope(request: Any, code: str, message: str) -> dict[str, Any]:
        operation = request.get("operation") if isinstance(request, dict) else None
        return {"schema_version": knowledge.LOCAL_OPERATION_RESULT_SCHEMA,
                "contract_status": knowledge.LOCAL_OPERATION_CONTRACT_STATUS,
                "ok": False, "operation": operation,
                "error": {"code": code, "message": message, "retryable": False}}

    def execute(self, token: str, request: dict[str, Any]) -> dict[str, Any]:
        try:
            context = self.authenticate(token)
        except HostedAuthError as exc:
            return self._error_envelope(request, exc.code, str(exc))
        operation = request.get("operation") if isinstance(request, dict) else None
        allowed = (operation in AGENT_OPERATIONS and
                   (context.role == "owner" or operation in context.permissions))
        if operation in OWNER_ONLY_OPERATIONS:
            allowed = context.role == "owner"
        if not allowed:
            envelope = self._error_envelope(
                request, "operation_forbidden", "operation is not permitted for this principal")
            self._audit(context, request, envelope, None)
            return envelope
        normalized = json.loads(json.dumps(request))
        parameters = normalized.get("parameters")
        if isinstance(parameters, dict) and operation in IDENTITY_PARAMETERS:
            parameters[IDENTITY_PARAMETERS[operation]] = context.principal_id
        store = SQLiteEventStore(
            self.database, context.workspace_id, context.principal_id)
        with using_event_store(store):
            envelope = knowledge.execute_local_operation(normalized)
            head = store.head()
        if envelope.get("ok") and operation == "capabilities.get":
            result = dict(envelope["result"])
            result["transport"] = "hosted_https"
            result["clients"] = sorted(set(result.get("clients", [])) |
                                       {"python_sdk", "mcp_stdio_bridge"})
            result["not_available"] = [
                item for item in result.get("not_available", [])
                if item not in {"localhost_http", "mcp", "cloud"}]
            result["hosted"] = {
                "deployment": "personal_single_instance_alpha",
                "workspace_id": context.workspace_id,
                "principal_id": context.principal_id,
                "role": context.role,
                "owner_approval_available": context.role == "owner",
            }
            envelope = {**envelope, "result": result}
        self._audit(context, request, envelope, head)
        return envelope

    def _audit(self, context: PrincipalContext, request: Any,
               envelope: dict[str, Any], event_head: str | None) -> None:
        request = request if isinstance(request, dict) else {}
        connection = self._connect()
        try:
            connection.execute(
                "INSERT INTO hosted_audit(occurred_at, workspace_id, principal_id, "
                "credential_id, operation, request_id, idempotency_key, outcome, event_head) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (_now(), context.workspace_id, context.principal_id,
                 context.credential_id, request.get("operation"), request.get("request_id"),
                 request.get("idempotency_key"), "ok" if envelope["ok"] else
                 envelope["error"]["code"], event_head))
            connection.commit()
        finally:
            connection.close()

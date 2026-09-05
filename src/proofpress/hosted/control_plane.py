"""Self-hosted workspace identity and authority boundary."""
from __future__ import annotations

from dataclasses import dataclass
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import hmac
import json
from pathlib import Path
import secrets
import sqlite3
import threading
from typing import Any

from proofpress.kernel import operations as knowledge
from proofpress.kernel.events import SQLiteEventStore, using_event_store
from proofpress.hosted import review_policy


OWNER_ONLY_OPERATIONS = frozenset({
    "conclusion.review", "conclusion.supersede",
    "relation.review", "relation.resolve",
})
AGENT_OPERATIONS = frozenset({
    "capabilities.get", "configuration.get", "evidence.submit",
    "conclusion.propose", "conclusion.evaluate", "conclusion.judge",
    "conclusion.judge_batch", "relation.propose", "relation.evaluate",
    "relation.judge", "graph.get", "graph.traverse", "context.get", "context.discover",
    "review.summary", "review.receipt",
})
IDENTITY_PARAMETERS = {
    "conclusion.propose": "proposer",
    "conclusion.evaluate": "actor",
    "conclusion.judge": "actor",
    "conclusion.judge_batch": "actor",
    "relation.propose": "proposer",
    "relation.evaluate": "actor",
    "relation.judge": "actor",
    "conclusion.review": "reviewer",
    "conclusion.supersede": "reviewer",
    "relation.review": "reviewer",
    "relation.resolve": "reviewer",
    "context.get": "actor",
    "context.discover": "actor",
    "graph.traverse": "actor",
    "graph.get": "actor",
    "review.summary": "actor",
    "review.receipt": "actor",
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
        self._judge_worker_lock = threading.Lock()
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
                CREATE TABLE IF NOT EXISTS hosted_oauth_clients (
                    client_id TEXT PRIMARY KEY,
                    client_name TEXT NOT NULL,
                    redirect_uris_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS hosted_oauth_codes (
                    code_hash TEXT PRIMARY KEY,
                    credential_id TEXT NOT NULL,
                    client_id TEXT NOT NULL,
                    redirect_uri TEXT NOT NULL,
                    resource TEXT NOT NULL,
                    code_challenge TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    used_at TEXT,
                    FOREIGN KEY (credential_id) REFERENCES hosted_credentials(credential_id),
                    FOREIGN KEY (client_id) REFERENCES hosted_oauth_clients(client_id)
                );
                CREATE TABLE IF NOT EXISTS hosted_oauth_tokens (
                    token_hash TEXT PRIMARY KEY,
                    credential_id TEXT NOT NULL,
                    client_id TEXT NOT NULL,
                    kind TEXT NOT NULL CHECK(kind IN ('access', 'refresh')),
                    family_id TEXT NOT NULL,
                    resource TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    revoked_at TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (credential_id) REFERENCES hosted_credentials(credential_id)
                );
            """)
            review_policy.migrate(connection)
            connection.commit()
        finally:
            connection.close()

    @staticmethod
    def _oauth_hash(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def register_oauth_client(self, client_name: str,
                              redirect_uris: list[str]) -> dict[str, Any]:
        if (not isinstance(client_name, str) or not client_name.strip()
                or not isinstance(redirect_uris, list) or not redirect_uris):
            raise ValueError("client_name and redirect_uris are required")
        from urllib.parse import urlparse
        clean = []
        for value in redirect_uris:
            if not isinstance(value, str):
                raise ValueError("redirect URIs must be strings")
            parsed = urlparse(value)
            loopback = parsed.scheme == "http" and parsed.hostname in {
                "127.0.0.1", "::1", "localhost"}
            if parsed.fragment or not (parsed.scheme == "https" or loopback):
                raise ValueError("redirect URIs must use HTTPS or loopback HTTP")
            clean.append(value)
        client_id = "ppoc_" + secrets.token_urlsafe(18)
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO hosted_oauth_clients VALUES (?, ?, ?, ?)",
                (client_id, client_name.strip(), json.dumps(clean), _now()))
        return {"client_id": client_id, "client_name": client_name.strip(),
                "redirect_uris": clean, "token_endpoint_auth_method": "none"}

    def validate_oauth_client(self, client_id: str, redirect_uri: str) -> None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT redirect_uris_json FROM hosted_oauth_clients WHERE client_id=?",
                (client_id,)).fetchone()
        if not row or redirect_uri not in json.loads(row["redirect_uris_json"]):
            raise HostedAuthError("invalid_client", "unknown client or redirect URI")

    def create_oauth_code(self, agent_token: str, client_id: str,
                          redirect_uri: str, resource: str,
                          code_challenge: str) -> str:
        context = self.authenticate(agent_token)
        if context.role != "agent":
            raise HostedAuthError(
                "agent_required", "owner credentials cannot authorize MCP clients")
        self.validate_oauth_client(client_id, redirect_uri)
        if (not isinstance(code_challenge, str)
                or not 43 <= len(code_challenge) <= 128):
            raise HostedAuthError("invalid_request", "PKCE S256 challenge is required")
        code = "ppocd_" + secrets.token_urlsafe(32)
        from datetime import timedelta
        expires = (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO hosted_oauth_codes VALUES (?, ?, ?, ?, ?, ?, ?, NULL)",
                (self._oauth_hash(code), context.credential_id, client_id,
                 redirect_uri, resource, code_challenge, expires))
        return code

    def _issue_oauth_pair(self, connection, credential_id: str,
                          client_id: str, resource: str,
                          family_id: str | None = None):
        from datetime import timedelta
        created = datetime.now(timezone.utc)
        family = family_id or "ppof_" + secrets.token_urlsafe(18)
        access = "ppoa_" + secrets.token_urlsafe(32)
        refresh = "ppor_" + secrets.token_urlsafe(40)
        for value, kind, expiry in (
            (access, "access", created + timedelta(minutes=30)),
            (refresh, "refresh", created + timedelta(days=30)),
        ):
            connection.execute(
                "INSERT INTO hosted_oauth_tokens VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?)",
                (self._oauth_hash(value), credential_id, client_id, kind, family, resource,
                 expiry.isoformat(), created.isoformat()))
        return {"access_token": access, "token_type": "Bearer",
                "expires_in": 1800, "refresh_token": refresh,
                "scope": "proofpress:agent"}

    def exchange_oauth_code(self, code: str, client_id: str,
                            redirect_uri: str, resource: str,
                            code_verifier: str) -> dict[str, Any]:
        import base64
        if not isinstance(code_verifier, str) or not 43 <= len(code_verifier) <= 128:
            raise HostedAuthError("invalid_grant", "PKCE verifier is invalid")
        challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode()).digest()).rstrip(b"=").decode()
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT * FROM hosted_oauth_codes WHERE code_hash=?",
                (self._oauth_hash(code),)).fetchone()
            now = datetime.now(timezone.utc)
            if (not row or row["used_at"] or datetime.fromisoformat(row["expires_at"]) <= now
                    or row["client_id"] != client_id
                    or row["redirect_uri"] != redirect_uri
                    or row["resource"] != resource
                    or not hmac.compare_digest(row["code_challenge"], challenge)):
                raise HostedAuthError("invalid_grant", "authorization code is invalid")
            connection.execute(
                "UPDATE hosted_oauth_codes SET used_at=? WHERE code_hash=?",
                (_now(), self._oauth_hash(code)))
            result = self._issue_oauth_pair(
                connection, row["credential_id"], client_id, resource)
            connection.commit()
            return result
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    def refresh_oauth_token(self, refresh_token: str, client_id: str,
                            resource: str) -> dict[str, Any]:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT t.*, c.revoked_at AS credential_revoked FROM hosted_oauth_tokens t "
                "JOIN hosted_credentials c USING(credential_id) WHERE token_hash=? AND kind='refresh'",
                (self._oauth_hash(refresh_token),)).fetchone()
            now = datetime.now(timezone.utc)
            if row and row["revoked_at"]:
                connection.execute(
                    "UPDATE hosted_oauth_tokens SET revoked_at=? "
                    "WHERE family_id=? AND revoked_at IS NULL",
                    (_now(), row["family_id"]))
                connection.commit()
                raise HostedAuthError(
                    "invalid_grant", "refresh token reuse revoked this session")
            if (not row or row["revoked_at"] or row["credential_revoked"]
                    or datetime.fromisoformat(row["expires_at"]) <= now
                    or row["client_id"] != client_id
                    or row["resource"] != resource):
                raise HostedAuthError("invalid_grant", "refresh token is invalid")
            connection.execute(
                "UPDATE hosted_oauth_tokens SET revoked_at=? WHERE family_id=? AND revoked_at IS NULL",
                (_now(), row["family_id"]))
            result = self._issue_oauth_pair(
                connection, row["credential_id"], client_id, resource,
                row["family_id"])
            connection.commit()
            return result
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    def authenticate_oauth_access(self, token: str,
                                  resource: str) -> PrincipalContext:
        if not token.startswith("ppoa_"):
            raise HostedAuthError("invalid_token", "invalid MCP access token")
        connection = self._connect()
        try:
            row = connection.execute(
                "SELECT t.*, c.workspace_id, c.principal_id, c.permissions_json, "
                "c.revoked_at AS credential_revoked, p.role FROM hosted_oauth_tokens t "
                "JOIN hosted_credentials c USING(credential_id) "
                "JOIN hosted_principals p USING(workspace_id, principal_id) "
                "WHERE token_hash=? AND kind='access'",
                (self._oauth_hash(token),)).fetchone()
            now = datetime.now(timezone.utc)
            if (not row or row["revoked_at"] or row["credential_revoked"]
                    or datetime.fromisoformat(row["expires_at"]) <= now
                    or row["resource"] != resource or row["role"] != "agent"):
                raise HostedAuthError("invalid_token", "invalid MCP access token")
            return PrincipalContext(
                row["workspace_id"], row["principal_id"], row["role"],
                row["credential_id"], frozenset(json.loads(row["permissions_json"])))
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

    def list_credentials(self, owner_token: str) -> list[dict[str, Any]]:
        owner = self.authenticate(owner_token)
        if owner.role != "owner":
            raise HostedAuthError("owner_required", "owner credential required")
        connection = self._connect()
        try:
            rows = connection.execute(
                "SELECT c.credential_id, c.principal_id, p.role, c.label, "
                "c.permissions_json, c.created_at, c.last_used_at, c.revoked_at "
                "FROM hosted_credentials c JOIN hosted_principals p "
                "USING(workspace_id, principal_id) WHERE c.workspace_id = ? "
                "ORDER BY c.created_at, c.credential_id",
                (owner.workspace_id,)).fetchall()
            return [{key: row[key] for key in row.keys()
                     if key != "permissions_json"} | {
                         "permissions": json.loads(row["permissions_json"])}
                    for row in rows]
        finally:
            connection.close()

    def list_audit(self, owner_token: str, limit: int = 100) -> list[dict[str, Any]]:
        owner = self.authenticate(owner_token)
        if owner.role != "owner":
            raise HostedAuthError("owner_required", "owner credential required")
        safe_limit = max(1, min(int(limit), 250))
        connection = self._connect()
        try:
            rows = connection.execute(
                "SELECT audit_id, occurred_at, principal_id, operation, outcome, event_head "
                "FROM hosted_audit WHERE workspace_id = ? ORDER BY audit_id DESC LIMIT ?",
                (owner.workspace_id, safe_limit)).fetchall()
            return [{key: row[key] for key in row.keys()} for row in rows]
        finally:
            connection.close()

    def _owner(self, token):
        context = self.authenticate(token)
        if context.role != "owner":
            raise HostedAuthError("owner_required", "owner credential required")
        return context

    @contextmanager
    def _db(self):
        connection = self._connect()
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def _policy(self, workspace_id):
        with self._db() as connection:
            return review_policy.current(connection, workspace_id)

    def get_review_policy(self, token):
        owner = self._owner(token)
        with self._db() as connection:
            return review_policy.public(review_policy.current(connection, owner.workspace_id),
                                        review_policy.credential_status(connection, owner.workspace_id))

    def save_review_policy(self, token, settings, expected_version, api_key=None, delete_key=False):
        owner = self._owner(token)
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            prior = review_policy.current(connection, owner.workspace_id)
            if type(expected_version) is not int or expected_version != prior["version"]:
                raise HostedAuthError("stale_policy", "Review policy changed. Reload before saving.")
            policy = review_policy.validate(settings, prior["policy"])
            changed_at = _now()
            if delete_key:
                review_policy.delete_credential(connection, owner.workspace_id)
            elif api_key:
                review_policy.save_credential(connection, owner.workspace_id, api_key, changed_at)
            elif settings["provider"] != prior["settings"].get("provider"):
                raise ValueError("Add the API key for the selected provider.")
            if settings["mode"] != "off" and not review_policy.credential(connection, owner.workspace_id):
                raise ValueError("Add a provider API key before enabling LM review.")
            if settings == prior["settings"] and not api_key and not delete_key:
                return review_policy.public(prior, review_policy.credential_status(connection, owner.workspace_id))
            record = {"version": prior["version"] + 1, "settings": settings, "policy": policy,
                      "actor": owner.principal_id, "updated_at": changed_at}
            connection.execute("INSERT INTO hosted_review_policies VALUES (?, ?, ?, ?, ?, ?)",
                               (owner.workspace_id, record["version"], json.dumps(settings),
                                json.dumps(policy), owner.principal_id, record["updated_at"]))
            connection.commit()
            if settings["mode"] == "automatic":
                store = SQLiteEventStore(self.database, owner.workspace_id, owner.principal_id)
                with using_event_store(store), knowledge.using_policy(policy):
                    projection = knowledge.v2_projection()
                    candidates = [row for row in projection["conclusions"].values()
                                  if knowledge.v2_state(projection, row, policy) in {"needs_review", "unresolved"}]
                for conclusion in candidates:
                    self._schedule_judge(owner, conclusion, record, start=False)
                if candidates:
                    threading.Thread(target=self.run_judge_jobs, daemon=True).start()
            return review_policy.public(record, review_policy.credential_status(connection, owner.workspace_id))
        finally:
            connection.close()

    def list_activity(self, token, limit=100):
        owner = self._owner(token)
        limit = max(1, min(int(limit), 250))
        connection = self._connect()
        try:
            events = connection.execute("SELECT payload_json, principal_id FROM events WHERE workspace_id=? ORDER BY sequence",
                                        (owner.workspace_id,)).fetchall()
            subjects = {}
            reviews = {}
            rows = []
            for raw in events:
                event = json.loads(raw["payload_json"])
                if event.get("type") == "human_reviewed":
                    reviews[event["event_id"]] = event
                conclusion = event.get("conclusion")
                if conclusion:
                    subjects[conclusion["id"]] = conclusion
                row = review_policy.semantic_event(event, raw["principal_id"])
                if row:
                    if event.get("review_ref") in reviews:
                        row["detail"] = reviews[event["review_ref"]].get("note") or row["detail"]
                    if event.get("type") == "evidence_bound":
                        evidence = event.get("evidence", {})
                        row["detail"] = evidence.get("retrieval_receipt", {}).get("source", {}).get("uri") or evidence.get("path") or row["subject_id"]
                    rows.append(row)
            for row in rows:
                subject = subjects.get(row["subject_id"], {})
                row["statement"] = subject.get("statement", "")
                row["scope"] = subject.get("scope", "")
            for raw in connection.execute("SELECT * FROM hosted_context_reads WHERE workspace_id=? ORDER BY read_id DESC LIMIT ?", (owner.workspace_id, limit)):
                ids = json.loads(raw["conclusion_ids_json"])
                rows.append({"id": f"read-{raw['read_id']}", "occurred_at": raw["created_at"],
                             "actor": raw["actor"], "action": "Retrieved governed context", "kind": "context_retrieved",
                             "outcome": "retrieved", "scope": raw["scope"], "conclusion_ids": ids,
                             "detail": f"{len(ids)} conclusions returned. Retrieval does not prove use."})
            for raw in connection.execute("SELECT * FROM hosted_review_policies WHERE workspace_id=?", (owner.workspace_id,)):
                rows.append({"id": f"policy-{raw['version']}", "occurred_at": raw["created_at"],
                             "actor": raw["actor"], "action": "Updated review policy", "outcome": "recorded",
                             "detail": f"Version {raw['version']}", "kind": "policy_updated"})
            return sorted(rows, key=lambda row: (row["occurred_at"], row["id"]), reverse=True)[:limit]
        finally:
            connection.close()

    def _schedule_judge(self, context, conclusion, record, start=True):
        if record["settings"]["mode"] != "automatic":
            return
        job_id = knowledge.digest([context.workspace_id, conclusion["id"], conclusion["digest"], record["policy"]["digest"]])
        with self._db() as connection:
            connection.execute("INSERT OR IGNORE INTO hosted_judge_jobs VALUES (?, ?, ?, ?, ?, 'queued', ?, ?, '')",
                               (job_id, context.workspace_id, conclusion["id"], record["policy"]["digest"], context.principal_id, _now(), _now()))
        if start:
            threading.Thread(target=self.run_judge_jobs, daemon=True).start()

    def run_judge_jobs(self):
        """Durable queue, one claim per job; interrupted calls require explicit manual retry."""
        with self._judge_worker_lock:
            self._drain_judge_jobs()

    def _drain_judge_jobs(self):
        while True:
            connection = self._connect()
            try:
                connection.execute("BEGIN IMMEDIATE")
                job = connection.execute("SELECT * FROM hosted_judge_jobs WHERE state='queued' ORDER BY created_at LIMIT 1").fetchone()
                if not job:
                    return
                connection.execute("UPDATE hosted_judge_jobs SET state='running', updated_at=? WHERE job_id=?", (_now(), job["job_id"]))
                connection.commit()
            finally:
                connection.close()
            state, detail = "failed", "LM advice failed. Retry from the review page."
            try:
                record = self._policy(job["workspace_id"])
                store = SQLiteEventStore(self.database, job["workspace_id"], "system:auto-review")
                with self._db() as secret_connection:
                    provider_secret = review_policy.credential(secret_connection, job["workspace_id"])
                with using_event_store(store), knowledge.using_policy(record["policy"]), knowledge.using_judge_environment({"PROOFPRESS_JUDGE_API_KEY": provider_secret or ""}):
                    if record["settings"]["mode"] != "automatic" or record["policy"]["digest"] != job["policy_digest"]:
                        state, detail = "skipped", "Review policy changed."
                    elif knowledge.receipt_v2(job["conclusion_id"])["state"] not in {"needs_review", "unresolved"}:
                        state, detail = "skipped", "Conclusion no longer needs review."
                    elif not knowledge.evaluate_v2(job["conclusion_id"])["eligible"]:
                        state, detail = "blocked", "Fix deterministic checks before requesting LM advice."
                    else:
                        receipt = knowledge.receipt_v2(job["conclusion_id"])
                        recommendation = receipt.get("recommendation")
                        if not (recommendation and
                                recommendation.get("conclusion_digest") == receipt["conclusion"]["digest"] and
                                recommendation.get("policy_digest") == record["policy"]["digest"]):
                            knowledge.judge_v2(job["conclusion_id"])
                        state, detail = "completed", "LM advice recorded."
            except Exception:
                # Do not persist provider responses or executable diagnostics in owner-facing data.
                try:
                    store = SQLiteEventStore(self.database, job["workspace_id"], "system:auto-review")
                    with using_event_store(store), knowledge.using_policy(self._policy(job["workspace_id"])["policy"]):
                        receipt = knowledge.receipt_v2(job["conclusion_id"])
                        if receipt.get("recommendation"):
                            state, detail = "completed", "LM advice recorded."
                except Exception:
                    pass
            with self._db() as connection:
                connection.execute("UPDATE hosted_judge_jobs SET state=?, detail=?, updated_at=? WHERE job_id=?", (state, detail, _now(), job["job_id"]))

    def resume_judge_jobs(self):
        with self._db() as connection:
            connection.execute("UPDATE hosted_judge_jobs SET state='interrupted', detail='Server restarted during LM review. Retry explicitly.', updated_at=? WHERE state='running'", (_now(),))
            # Repair a crash between committing a new proposal and enqueueing its review.
            workspaces = connection.execute("SELECT workspace_id FROM hosted_workspaces").fetchall()
            for workspace in workspaces:
                record = review_policy.current(connection, workspace["workspace_id"])
                if record["settings"]["mode"] != "automatic" or not record["updated_at"]:
                    continue
                for raw in connection.execute("SELECT payload_json, principal_id FROM events WHERE workspace_id=?", (workspace["workspace_id"],)).fetchall():
                    event = json.loads(raw["payload_json"])
                    if event.get("type") == "conclusion_proposed" and event["created_at"] >= record["updated_at"]:
                        conclusion = event["conclusion"]
                        job_id = knowledge.digest([workspace["workspace_id"], conclusion["id"], conclusion["digest"], record["policy"]["digest"]])
                        connection.execute("INSERT OR IGNORE INTO hosted_judge_jobs VALUES (?, ?, ?, ?, ?, 'queued', ?, ?, '')", (job_id, workspace["workspace_id"], conclusion["id"], record["policy"]["digest"], raw["principal_id"], _now(), _now()))
        threading.Thread(target=self.run_judge_jobs, daemon=True).start()

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
        return self.execute_as(context, request)

    def execute_as(self, context: PrincipalContext,
                   request: dict[str, Any]) -> dict[str, Any]:
        """Execute with an already authenticated server-side principal context."""
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
            # Owners inspect the whole workspace in their review surface. An
            # agent's actor identity is always server-derived for reads, so a
            # supplied actor cannot bypass row-level access controls.
            if (context.role == "owner" and operation in
                    {"graph.get", "review.summary", "review.receipt"}):
                parameters.pop("actor", None)
            else:
                parameters[IDENTITY_PARAMETERS[operation]] = context.principal_id
        store = SQLiteEventStore(
            self.database, context.workspace_id, context.principal_id)
        record = self._policy(context.workspace_id)
        prior_conclusions = {e.get("subject_ref") for e in store.list_events() if e.get("type") == "conclusion_proposed"} if operation == "conclusion.propose" else set()
        judge_environment = {}
        if operation in {"conclusion.judge", "conclusion.judge_batch", "relation.judge"}:
            with self._db() as connection:
                provider_secret = review_policy.credential(connection, context.workspace_id)
            judge_environment["PROOFPRESS_JUDGE_API_KEY"] = provider_secret or ""
        with using_event_store(store), knowledge.using_policy(record["policy"]), knowledge.using_judge_environment(judge_environment):
            envelope = knowledge.execute_local_operation(normalized)
            head = store.head()
            if envelope.get("ok") and operation == "review.receipt":
                result = envelope["result"]
                evaluation = result.get("evaluation") or {}
                advice = result.get("recommendation") or {}
                result["review_policy"] = {
                    "require_judge": record["policy"].get("require_judge", False),
                    "mode": record["settings"]["mode"], "model": record["settings"]["model"],
                    "provider": record["settings"].get("provider", "openrouter"),
                    "rubric": record["settings"]["rubric"],
                    "zdr": record["settings"].get("zdr", False),
                    "policy_digest": record["policy"]["digest"],
                    "checks_current": evaluation.get("policy_digest") == record["policy"]["digest"],
                    "advice_current": advice.get("policy_digest") == record["policy"]["digest"],
                }
                with self._db() as connection:
                    job = connection.execute("SELECT state, detail FROM hosted_judge_jobs WHERE workspace_id=? AND conclusion_id=? ORDER BY created_at DESC LIMIT 1", (context.workspace_id, result["conclusion"]["id"])).fetchone()
                    result["judge_job"] = dict(job) if job else None
        if envelope.get("ok") and operation == "capabilities.get":
            result = dict(envelope["result"])
            result["transport"] = "hosted_https"
            result["clients"] = sorted(set(result.get("clients", [])) |
                                       {"python_sdk", "mcp_stdio_bridge",
                                        "mcp_streamable_http"})
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
        if envelope.get("ok") and operation == "conclusion.propose":
            conclusion = envelope["result"]["conclusion"]
            if conclusion["id"] not in prior_conclusions:
                self._schedule_judge(context, conclusion, record)
        if envelope.get("ok") and operation == "context.get" and context.role == "agent":
            ids = [row["id"] for row in envelope["result"].get("knowledge", [])]
            with self._db() as connection:
                connection.execute("INSERT INTO hosted_context_reads(workspace_id,actor,scope,conclusion_ids_json,created_at) VALUES(?,?,?,?,?)",
                                   (context.workspace_id, context.principal_id, (parameters or {}).get("scope"), json.dumps(ids), _now()))
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

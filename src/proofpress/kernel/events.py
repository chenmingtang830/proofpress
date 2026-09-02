"""Backend-neutral append-only history contract for Proofpress knowledge events."""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import threading
from typing import Any, Iterator, Mapping, Protocol


JsonObject = dict[str, Any]


class EventStore(Protocol):
    """Minimal persistence seam used by the governance kernel."""

    def list_events(self) -> list[JsonObject]: ...
    def head(self) -> str | None: ...
    def append(self, event: Mapping[str, Any], *, message: str,
               expected_head: str | None) -> JsonObject: ...


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def content_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value)).hexdigest()


def history_envelopes(events: list[Mapping[str, Any]]) -> list[JsonObject]:
    """Build backend-independent, hash-linked envelopes from ordered events."""
    rows: list[JsonObject] = []
    prior_digest = None
    for sequence, event in enumerate(events, start=1):
        payload = {key: value for key, value in event.items() if key != "commit"}
        envelope = {
            "schema_version": "proofpress/history-envelope/v1alpha1",
            "sequence": sequence,
            "prior_event_digest": prior_digest,
            "payload_digest": content_digest(payload),
            "payload": payload,
        }
        envelope["event_digest"] = content_digest(envelope)
        rows.append(envelope)
        prior_digest = envelope["event_digest"]
    return rows


def verify_history_envelopes(envelopes: list[Mapping[str, Any]]) -> JsonObject:
    prior_digest = None
    for sequence, envelope in enumerate(envelopes, start=1):
        if envelope.get("schema_version") != "proofpress/history-envelope/v1alpha1":
            return {"ok": False, "sequence": sequence,
                    "error": "unsupported_history_envelope"}
        if envelope.get("sequence") != sequence:
            return {"ok": False, "sequence": sequence, "error": "invalid_sequence"}
        if envelope.get("prior_event_digest") != prior_digest:
            return {"ok": False, "sequence": sequence,
                    "error": "invalid_prior_event_digest"}
        if envelope.get("payload_digest") != content_digest(envelope.get("payload")):
            return {"ok": False, "sequence": sequence,
                    "error": "invalid_payload_digest"}
        unsigned = {key: value for key, value in envelope.items()
                    if key != "event_digest"}
        if envelope.get("event_digest") != content_digest(unsigned):
            return {"ok": False, "sequence": sequence,
                    "error": "invalid_event_digest"}
        prior_digest = envelope["event_digest"]
    return {"ok": True, "events": len(envelopes), "head": prior_digest}


class GitEventStore:
    """Adapter preserving the existing dedicated-ref Git ledger format."""

    def __init__(self, ref: str = "refs/proofpress/knowledge"):
        self.ref = ref

    @staticmethod
    def _git(*args: str, input: str | None = None) -> str:
        result = subprocess.run(["git", *args], input=input, text=True,
                                capture_output=True)
        if result.returncode:
            raise ValueError("git " + " ".join(args) + ": " + result.stderr.strip())
        return result.stdout

    def list_events(self) -> list[JsonObject]:
        try:
            commits = self._git("rev-list", "--reverse", self.ref).split()
        except ValueError:
            return []
        if not commits:
            return []
        specs = [f"{commit}:event.json" for commit in commits]
        result = subprocess.run(["git", "cat-file", "--batch"],
                                input=("\n".join(specs) + "\n").encode(),
                                capture_output=True)
        if result.returncode:
            raise ValueError("git cat-file --batch: " +
                             result.stderr.decode(errors="replace").strip())
        rows: list[JsonObject] = []
        output = io.BytesIO(result.stdout)
        for commit, spec in zip(commits, specs):
            header_line = output.readline()
            if not header_line:
                raise ValueError("git cat-file --batch returned a truncated header")
            header = header_line.decode().split()
            if len(header) != 3 or header[1] != "blob":
                raise ValueError("git cat-file --batch: missing event blob for " + spec)
            size = int(header[2])
            blob = output.read(size)
            if len(blob) != size or output.read(1) != b"\n":
                raise ValueError("git cat-file --batch returned a truncated event blob")
            row = json.loads(blob.decode("utf-8"))
            row["commit"] = commit
            rows.append(row)
        return rows

    def head(self) -> str | None:
        try:
            return self._git("rev-parse", self.ref).strip()
        except ValueError:
            return None

    def append(self, event: Mapping[str, Any], *, message: str,
               expected_head: str | None) -> JsonObject:
        blob = self._git("hash-object", "-w", "--stdin",
                         input=json.dumps(dict(event), ensure_ascii=False,
                                          sort_keys=True, indent=2) + "\n").strip()
        tree = self._git("mktree", input=f"100644 blob {blob}\tevent.json\n").strip()
        parent = ["-p", expected_head] if expected_head else []
        commit = self._git("commit-tree", tree, *parent, "-m", message).strip()
        self._git("update-ref", self.ref, commit, expected_head or "0" * 40)
        return {**event, "commit": commit}


class MemoryEventStore:
    """Deterministic store for parity tests and embedded integrations."""

    def __init__(self):
        self.events: list[JsonObject] = []

    def list_events(self) -> list[JsonObject]:
        return [dict(row) for row in self.events]

    def head(self) -> str | None:
        return self.events[-1]["commit"] if self.events else None

    def append(self, event: Mapping[str, Any], *, message: str,
               expected_head: str | None) -> JsonObject:
        del message
        if expected_head != self.head():
            raise ValueError("STALE_EVENT_STORE_HEAD")
        commit = content_digest({"prior": expected_head, "event": event})
        appended = {**event, "commit": commit}
        self.events.append(appended)
        return dict(appended)


class SQLiteEventStore:
    """Transactional single-instance store for one personal hosted workspace."""

    def __init__(self, path: str | Path, workspace_id: str,
                 principal_id: str = "system:kernel"):
        if not workspace_id or not principal_id:
            raise ValueError("workspace_id and principal_id are required")
        self.path = Path(path)
        self.workspace_id = workspace_id
        self.principal_id = principal_id
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._connection: ContextVar[sqlite3.Connection | None] = ContextVar(
            f"proofpress_sqlite_connection_{id(self)}", default=None)
        self._migration_lock = threading.Lock()
        self._migrate()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 30000")
        return connection

    def _migrate(self) -> None:
        with self._migration_lock:
            connection = self._connect()
            try:
                connection.execute("PRAGMA journal_mode = WAL")
                connection.executescript("""
                    CREATE TABLE IF NOT EXISTS schema_migrations (
                        version INTEGER PRIMARY KEY,
                        applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                    );
                    CREATE TABLE IF NOT EXISTS events (
                        workspace_id TEXT NOT NULL,
                        sequence INTEGER NOT NULL,
                        event_id TEXT NOT NULL,
                        prior_head TEXT,
                        event_head TEXT NOT NULL,
                        principal_id TEXT NOT NULL,
                        payload_json TEXT NOT NULL,
                        PRIMARY KEY (workspace_id, sequence),
                        UNIQUE (workspace_id, event_id),
                        UNIQUE (workspace_id, event_head)
                    );
                    CREATE TABLE IF NOT EXISTS idempotency (
                        workspace_id TEXT NOT NULL,
                        principal_id TEXT NOT NULL,
                        idempotency_key TEXT NOT NULL,
                        request_fingerprint TEXT NOT NULL,
                        operation TEXT NOT NULL,
                        result_json TEXT NOT NULL,
                        recorded_at TEXT NOT NULL,
                        PRIMARY KEY (workspace_id, principal_id, idempotency_key)
                    );
                    INSERT OR IGNORE INTO schema_migrations(version) VALUES (1);
                """)
            finally:
                connection.close()

    @contextmanager
    def transaction(self) -> Iterator[None]:
        if self._connection.get() is not None:
            yield
            return
        connection = self._connect()
        token = self._connection.set(connection)
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield
            connection.execute("COMMIT")
        except BaseException:
            connection.execute("ROLLBACK")
            raise
        finally:
            self._connection.reset(token)
            connection.close()

    @contextmanager
    def _access(self) -> Iterator[sqlite3.Connection]:
        existing = self._connection.get()
        if existing is not None:
            yield existing
            return
        connection = self._connect()
        try:
            yield connection
        finally:
            connection.close()

    def list_events(self) -> list[JsonObject]:
        with self._access() as connection:
            rows = connection.execute(
                "SELECT payload_json, event_head FROM events "
                "WHERE workspace_id = ? ORDER BY sequence", (self.workspace_id,))
            return [{**json.loads(row["payload_json"]), "commit": row["event_head"]}
                    for row in rows]

    def head(self) -> str | None:
        with self._access() as connection:
            row = connection.execute(
                "SELECT event_head FROM events WHERE workspace_id = ? "
                "ORDER BY sequence DESC LIMIT 1", (self.workspace_id,)).fetchone()
            return row["event_head"] if row else None

    def append(self, event: Mapping[str, Any], *, message: str,
               expected_head: str | None) -> JsonObject:
        del message
        with self.transaction():
            connection = self._connection.get()
            assert connection is not None
            row = connection.execute(
                "SELECT sequence, event_head FROM events WHERE workspace_id = ? "
                "ORDER BY sequence DESC LIMIT 1", (self.workspace_id,)).fetchone()
            actual_head = row["event_head"] if row else None
            if actual_head != expected_head:
                raise ValueError("STALE_EVENT_STORE_HEAD")
            sequence = (row["sequence"] if row else 0) + 1
            event_head = content_digest({
                "workspace_id": self.workspace_id, "sequence": sequence,
                "prior_head": actual_head, "principal_id": self.principal_id,
                "event": event,
            })
            connection.execute(
                "INSERT INTO events(workspace_id, sequence, event_id, prior_head, "
                "event_head, principal_id, payload_json) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (self.workspace_id, sequence, event["event_id"], actual_head,
                 event_head, self.principal_id,
                 canonical_json(dict(event)).decode("utf-8")))
            return {**event, "commit": event_head}

    def idempotency_records(self) -> dict[str, JsonObject]:
        with self._access() as connection:
            rows = connection.execute(
                "SELECT idempotency_key, request_fingerprint, operation, result_json, "
                "recorded_at FROM idempotency WHERE workspace_id = ? AND principal_id = ?",
                (self.workspace_id, self.principal_id))
            return {row["idempotency_key"]: {
                "request_fingerprint": row["request_fingerprint"],
                "operation": row["operation"],
                "result": json.loads(row["result_json"]),
                "recorded_at": row["recorded_at"],
            } for row in rows}

    def store_idempotency(self, key: str, fingerprint: str, operation: str,
                          result: Any, recorded_at: str) -> None:
        with self._access() as connection:
            connection.execute(
                "INSERT INTO idempotency(workspace_id, principal_id, idempotency_key, "
                "request_fingerprint, operation, result_json, recorded_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (self.workspace_id, self.principal_id, key, fingerprint, operation,
                 canonical_json(result).decode("utf-8"), recorded_at))

    def export_bundle(self) -> JsonObject:
        envelopes = history_envelopes(self.list_events())
        verification = verify_history_envelopes(envelopes)
        return {
            "schema_version": "proofpress/history-export/v1alpha1",
            "workspace_id": self.workspace_id,
            "events": envelopes,
            "verification": verification,
        }

    def backup_to(self, target: str | Path) -> Path:
        target_path = Path(target)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        source = self._connect()
        destination = sqlite3.connect(target_path)
        try:
            source.backup(destination)
        finally:
            destination.close()
            source.close()
        return target_path


_ACTIVE_EVENT_STORE: ContextVar[EventStore | None] = ContextVar(
    "proofpress_active_event_store", default=None)


def current_event_store() -> EventStore:
    return _ACTIVE_EVENT_STORE.get() or GitEventStore()


@contextmanager
def using_event_store(store: EventStore) -> Iterator[EventStore]:
    token = _ACTIVE_EVENT_STORE.set(store)
    try:
        yield store
    finally:
        _ACTIVE_EVENT_STORE.reset(token)

"""Backend-neutral append-only history contract for Proofpress knowledge events."""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
import hashlib
import io
import json
import subprocess
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

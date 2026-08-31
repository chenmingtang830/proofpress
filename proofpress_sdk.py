"""Typed thin client for the Proofpress local operation contract."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import proofpress_knowledge as knowledge


JsonObject = dict[str, Any]


class ProofpressError(Exception):
    """Stable operation error returned by any Proofpress transport."""

    def __init__(self, code: str, message: str, *, retryable: bool = False,
                 details: Mapping[str, Any] | None = None, status: int | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable
        self.details = dict(details or {})
        self.status = status


class ProofpressTransportError(ProofpressError):
    pass


class Transport(Protocol):
    def execute(self, request: Mapping[str, Any]) -> JsonObject: ...


@dataclass(frozen=True)
class InProcessTransport:
    workspace: Path

    def __init__(self, workspace: str | Path = "."):
        object.__setattr__(self, "workspace", Path(workspace).resolve())

    def execute(self, request: Mapping[str, Any]) -> JsonObject:
        if Path.cwd().resolve() != self.workspace:
            raise ProofpressTransportError(
                "workspace_mismatch",
                "in-process transport requires the process working directory to equal workspace")
        return knowledge.execute_local_operation(dict(request))


@dataclass(frozen=True)
class LocalHttpTransport:
    base_url: str
    token: str
    timeout: float = 30.0

    def __post_init__(self):
        parsed = urlparse(self.base_url)
        if parsed.scheme != "http" or parsed.hostname not in {
                "127.0.0.1", "::1", "localhost"}:
            raise ValueError("local HTTP transport requires a loopback http URL")
        if not self.token:
            raise ValueError("local HTTP transport requires a bearer token")

    def execute(self, request: Mapping[str, Any]) -> JsonObject:
        return _execute_http(self.base_url, self.token, self.timeout, request)


@dataclass(frozen=True)
class RemoteHttpTransport:
    base_url: str
    token: str
    timeout: float = 30.0

    def __post_init__(self):
        parsed = urlparse(self.base_url)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("remote HTTP transport requires an https URL")
        if parsed.username or parsed.password or parsed.fragment:
            raise ValueError("remote HTTP transport URL must not contain credentials or a fragment")
        if not self.token:
            raise ValueError("remote HTTP transport requires a bearer token")

    def execute(self, request: Mapping[str, Any]) -> JsonObject:
        return _execute_http(self.base_url, self.token, self.timeout, request)


def _execute_http(base_url: str, token: str, timeout: float,
                  request: Mapping[str, Any]) -> JsonObject:
    body = json.dumps(dict(request), ensure_ascii=False,
                      separators=(",", ":")).encode()
    target = base_url.rstrip("/") + "/v1/operations"
    http_request = Request(
        target, data=body, method="POST",
        headers={"Authorization": "Bearer " + token,
                 "Content-Type": "application/json"})
    try:
        with urlopen(http_request, timeout=timeout) as response:
            return json.loads(response.read())
    except HTTPError as exc:
        try:
            payload = json.loads(exc.read())
        except (UnicodeDecodeError, json.JSONDecodeError):
            payload = {}
        finally:
            exc.close()
        if isinstance(payload, dict) and "ok" in payload:
            return payload
        raise ProofpressTransportError(
            "http_error", str(payload.get("error", exc.reason)),
            retryable=exc.code >= 500, status=exc.code) from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise ProofpressTransportError(
            "transport_unavailable", str(exc), retryable=True) from exc


class ProofpressClient:
    """One client surface for in-process, localhost, and remote transports."""

    def __init__(self, transport: Transport):
        self.transport = transport

    @classmethod
    def in_process(cls, workspace: str | Path = ".") -> "ProofpressClient":
        return cls(InProcessTransport(workspace))

    @classmethod
    def localhost(cls, base_url: str, token: str,
                  timeout: float = 30.0) -> "ProofpressClient":
        return cls(LocalHttpTransport(base_url, token, timeout))

    @classmethod
    def remote(cls, base_url: str, token: str,
               timeout: float = 30.0) -> "ProofpressClient":
        return cls(RemoteHttpTransport(base_url, token, timeout))

    def execute_raw(self, operation: str, parameters: Mapping[str, Any] | None = None,
                    *, request_id: str | None = None,
                    idempotency_key: str | None = None) -> JsonObject:
        request: JsonObject = {
            "schema_version": knowledge.LOCAL_OPERATION_SCHEMA,
            "operation": operation,
            "parameters": dict(parameters or {}),
        }
        if request_id is not None:
            request["request_id"] = request_id
        if idempotency_key is not None:
            request["idempotency_key"] = idempotency_key
        envelope = self.transport.execute(request)
        if not isinstance(envelope, dict) or "ok" not in envelope:
            raise ProofpressTransportError(
                "invalid_transport_response",
                "transport returned an invalid operation envelope")
        return envelope

    def execute(self, operation: str, parameters: Mapping[str, Any] | None = None,
                *, request_id: str | None = None,
                idempotency_key: str | None = None) -> Any:
        envelope = self.execute_raw(
            operation, parameters, request_id=request_id,
            idempotency_key=idempotency_key)
        if not envelope["ok"]:
            error = envelope.get("error") or {}
            raise ProofpressError(
                error.get("code", "unknown_error"),
                error.get("message", "Proofpress operation failed"),
                retryable=bool(error.get("retryable")),
                details=error.get("details"))
        return envelope.get("result")

    def capabilities(self):
        return self.execute("capabilities.get")

    def configuration(self):
        return self.execute("configuration.get")

    def import_evidence(self, path, **meta):
        return self.execute("evidence.import", {"path": str(path)}, **meta)

    def submit_evidence(self, payload, *, profile=None, **meta):
        parameters = {"payload": dict(payload)}
        if profile is not None:
            parameters["profile"] = profile
        return self.execute("evidence.submit", parameters, **meta)

    def propose_conclusion(self, statement, evidence_refs, scope, proposer,
                           *, expires_at=None, artifact_refs=None,
                           allowed_actors=None, qualifiers=None, profile=None, **meta):
        return self.execute("conclusion.propose", {
            "statement": statement, "evidence_refs": list(evidence_refs),
            "scope": scope, "proposer": proposer, "expires_at": expires_at,
            "artifact_refs": list(artifact_refs or []),
            "allowed_actors": allowed_actors, "qualifiers": qualifiers,
            "profile": profile}, **meta)
    def evaluate_conclusion(self, conclusion_id, **meta):
        return self.execute("conclusion.evaluate", {"conclusion_id": conclusion_id}, **meta)
    def judge_conclusion(self, conclusion_id, **meta):
        return self.execute("conclusion.judge", {"conclusion_id": conclusion_id}, **meta)
    def judge_scope(self, scope, **meta):
        return self.execute("conclusion.judge_batch", {"scope": scope}, **meta)
    def review_conclusion(self, conclusion_id, decision, reviewer, *, note=None,
                          review_request_id=None, expected_head=None, **meta):
        return self.execute("conclusion.review", {
            "conclusion_id": conclusion_id, "decision": decision,
            "reviewer": reviewer, "note": note,
            "request_id": review_request_id, "expected_head": expected_head}, **meta)
    def supersede_conclusion(self, conclusion_id, replacement_id, reviewer,
                             *, note=None, **meta):
        return self.execute("conclusion.supersede", {
            "conclusion_id": conclusion_id, "replacement_id": replacement_id,
            "reviewer": reviewer, "note": note}, **meta)
    def propose_relation(self, source_id, target_id, relation_type, proposer,
                         *, confidence=None, qualifiers=None, **meta):
        return self.execute("relation.propose", {
            "source_id": source_id, "target_id": target_id,
            "relation_type": relation_type, "proposer": proposer,
            "confidence": confidence, "qualifiers": qualifiers}, **meta)
    def evaluate_relation(self, relation_id, **meta):
        return self.execute("relation.evaluate", {"relation_id": relation_id}, **meta)
    def judge_relation(self, relation_id, **meta):
        return self.execute("relation.judge", {"relation_id": relation_id}, **meta)
    def review_relation(self, relation_id, decision, reviewer, *, note=None,
                        review_request_id=None, expected_head=None, **meta):
        return self.execute("relation.review", {
            "relation_id": relation_id, "decision": decision,
            "reviewer": reviewer, "note": note,
            "request_id": review_request_id, "expected_head": expected_head}, **meta)
    def resolve_relation(self, relation_id, disposition, reviewer, *, winner=None,
                         note=None, expected_head=None, **meta):
        return self.execute("relation.resolve", {
            "relation_id": relation_id, "disposition": disposition,
            "reviewer": reviewer, "winner": winner, "note": note,
            "expected_head": expected_head}, **meta)
    def graph(self, scope=None):
        return self.execute("graph.get", {"scope": scope})
    def traverse_graph(self, seed_ids, *, scope=None, actor=None, task=None,
                       max_depth=2, max_claims=48, state="admitted"):
        return self.execute("graph.traverse", {
            "seed_ids": list(seed_ids), "scope": scope, "actor": actor,
            "task": task, "max_depth": max_depth,
            "max_claims": max_claims, "state": state})
    def context(self, *, scope=None, actor=None, task=None,
                include_blocked_statements=False):
        return self.execute("context.get", {
            "scope": scope, "actor": actor, "task": task,
            "include_blocked_statements": include_blocked_statements})
    def review_summary(self, scope=None):
        return self.execute("review.summary", {"scope": scope})

    def review_receipt(self, conclusion_id):
        return self.execute("review.receipt", {"conclusion_id": conclusion_id})

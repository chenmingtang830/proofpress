"""Thin MCP adapter over the canonical Proofpress operation contract."""
from __future__ import annotations

import argparse
import functools
import json
import logging
import os
from pathlib import Path
import re
from typing import TYPE_CHECKING, Annotated, Any, TypeAlias
from urllib.parse import urlencode, urlparse

try:  # both ship with pydantic, an mcp dependency; without the extra pydantic never sees this module
    from annotated_types import MinLen
    from typing_extensions import TypedDict  # pydantic reads TypedDict metadata only from this on 3.11
except ImportError:  # pragma: no cover - only without the mcp extra
    MinLen = None
    from typing import TypedDict

from proofpress.client import ProofpressClient, ProofpressError, ProofpressTransportError

# The kernel's non-empty rule, published and enforced at argument validation.
if TYPE_CHECKING:
    from annotated_types import MinLen as _MinLen
    NonEmptyText: TypeAlias = Annotated[str, _MinLen(1)]
elif MinLen is not None:
    NonEmptyText = Annotated[str, MinLen(1)]
else:
    NonEmptyText = str


logger = logging.getLogger(__name__)

MCP_SERVER_NAME = "Proofpress"
MCP_INSTRUCTIONS = (
    "Proofpress governs agent-produced knowledge. Submit only bounded evidence; "
    "propose claims with evidence references; use governed_context for approved reliance. "
    "If staged_context is returned, keep it separate and use it only for drafts "
    "marked unapproved; never record it as governed reliance. "
    "This server intentionally exposes no Human Approval, rejection, supersession, "
    "policy, credential, or owner-recovery tool. Ask the human owner to use the "
    "separate review surface for authority-bearing decisions."
)
MCP_SAFE_TOOLS = (
    "proofpress_capabilities",
    "proofpress_submit_evidence",
    "proofpress_propose_claim",
    "proofpress_discover_context",
    "proofpress_get_context",
    "proofpress_get_graph",
    "proofpress_traverse_graph",
    "proofpress_get_lineage",
    "proofpress_get_review_summary",
    "proofpress_get_review_receipt",
    "proofpress_get_review_link",
    "proofpress_start_run",
    "proofpress_finish_run",
    "proofpress_get_run",
    "proofpress_list_runs",
    "proofpress_capture_context",
    "proofpress_record_reliance",
    "proofpress_record_output",
    "proofpress_record_observation",
)
EVIDENCE_ID_RE = re.compile(r"evd_[0-9a-f]{16}\Z")


class McpRequestError(ValueError):
    """A call the MCP layer rejects before it reaches the kernel; the message is for the agent."""


class ProofpressMcpGateway:
    """Safe agent-facing methods backed by one Proofpress client."""

    def __init__(self, client: ProofpressClient, principal: str,
                 review_base_url: str | None = None):
        if not isinstance(principal, str) or not principal.strip():
            raise ValueError("MCP principal must be a non-empty server configuration value")
        if review_base_url is not None:
            parsed = urlparse(review_base_url)
            if parsed.scheme not in {"http", "https"} or not parsed.hostname:
                raise ValueError("review base URL must be an http or https URL")
        self.client = client
        self.principal = principal.strip()
        self.review_base_url = review_base_url.rstrip("/") if review_base_url else None

    def capabilities(self) -> dict[str, Any]:
        result = dict(self.client.capabilities())
        result["not_available"] = [
            item for item in result.get("not_available", []) if item != "mcp"
        ]
        result["clients"] = sorted(set(result.get("clients", [])) | {"mcp"})
        result["mcp"] = {
            "server": MCP_SERVER_NAME,
            "principal": result.get("hosted", {}).get(
                "principal_id", self.principal),
            "tools": list(MCP_SAFE_TOOLS),
            "human_approval_available": False,
        }
        return result

    def submit_evidence(self, payload: dict[str, Any],
                        idempotency_key: str | None = None, *,
                        profile: str | None = None) -> dict[str, Any]:
        if profile not in {None, "experiment"}:
            raise McpRequestError(
                "unsupported evidence profile: " + str(profile) +
                "; omit profile for proofpress/retrieval-evidence/v1 or use experiment")
        return self.client.submit_evidence(
            payload, profile=profile, idempotency_key=idempotency_key)

    def propose_claim(
            self, statement: str, evidence_refs: list[str], scope: str | None = None,
            expires_at: str | None = None,
            artifact_refs: list[str] | None = None,
            applicability: dict[str, Any] | None = None,
            reproposal_of: str | None = None,
            qualifiers: dict[str, Any] | None = None,
            profile: str | None = None,
            idempotency_key: str | None = None, *, title: str) -> dict[str, Any]:
        if (not evidence_refs or
                any(not isinstance(ref, str) or EVIDENCE_ID_RE.fullmatch(ref) is None
                    for ref in evidence_refs)):
            raise McpRequestError(
                "evidence_refs must contain evd_ IDs returned by "
                "proofpress_submit_evidence; source and artifact URLs are not evidence IDs")
        return self.client.propose_claim(
            statement, evidence_refs, scope, self.principal,
            expires_at=expires_at, artifact_refs=artifact_refs,
            applicability=applicability,
            reproposal_of=reproposal_of,
            qualifiers=qualifiers,
            profile=profile, idempotency_key=idempotency_key, title=title)

    def discover_context(self, task: str | None = None,
                         limit: int = 24) -> dict[str, Any]:
        return self.client.discover_context(
            actor=self.principal, task=task, limit=limit)

    def get_context(self, scope: str | None = None,
                    task: str | None = None) -> dict[str, Any]:
        return self.client.context(
            scope=scope, actor=self.principal, task=task,
            include_blocked_statements=False)

    def start_run(self, purpose: str, metadata: dict[str, Any] | None = None,
                  idempotency_key: str | None = None) -> dict[str, Any]:
        return self.client.start_run(purpose, actor=self.principal, metadata=metadata,
                                     idempotency_key=idempotency_key)

    def finish_run(self, run_id: str, status: str, summary: str | None = None,
                   idempotency_key: str | None = None) -> dict[str, Any]:
        return self.client.finish_run(run_id, status, actor=self.principal,
                                      summary=summary, idempotency_key=idempotency_key)

    def get_run(self, run_id: str) -> dict[str, Any]:
        return self.client.get_run(run_id, actor=self.principal)

    def list_runs(self, status: str | None = None, limit: int = 50) -> dict[str, Any]:
        return self.client.list_runs(actor=self.principal, status=status, limit=limit)

    def capture_context(self, run_id: str, scope: str | None = None,
                        task: str | None = None,
                        idempotency_key: str | None = None) -> dict[str, Any]:
        return self.client.capture_context(run_id, actor=self.principal, scope=scope,
                                           task=task, idempotency_key=idempotency_key)

    def record_reliance(self, run_id: str, receipt_id: str, claim_id: str,
                        claim_digest: str, purpose: str,
                        idempotency_key: str | None = None) -> dict[str, Any]:
        return self.client.record_reliance(
            run_id, receipt_id, claim_id, claim_digest, purpose,
            actor=self.principal, idempotency_key=idempotency_key)

    def record_output(self, run_id: str, reference: str, content_digest: str,
                      summary: str | None = None,
                      reliance_ids: list[str] | None = None,
                      media_type: str | None = None,
                      idempotency_key: str | None = None) -> dict[str, Any]:
        return self.client.record_output(
            run_id, reference, content_digest, actor=self.principal, summary=summary,
            reliance_ids=reliance_ids, media_type=media_type,
            idempotency_key=idempotency_key)

    def record_observation(self, run_id: str, kind: str, source: str, meaning: str,
                           evidence_refs: list[str] | None = None,
                           output_ids: list[str] | None = None,
                           observed_at: str | None = None,
                           idempotency_key: str | None = None) -> dict[str, Any]:
        return self.client.record_observation(
            run_id, kind, source, meaning, actor=self.principal,
            evidence_refs=evidence_refs, output_ids=output_ids,
            observed_at=observed_at, idempotency_key=idempotency_key)

    def evaluate_claim(self, claim_id: str) -> dict[str, Any]:
        return self.client.evaluate_claim(claim_id, actor=self.principal)

    def judge_claim(self, claim_id: str) -> dict[str, Any]:
        return self.client.judge_claim(claim_id, actor=self.principal)

    def get_graph(self, scope: str | None = None) -> dict[str, Any]:
        return self.client.graph(scope, actor=self.principal)

    def traverse_graph(self, seed_ids: list[str], scope: str | None = None,
                       task: str | None = None, max_depth: int = 2,
                       max_claims: int = 48) -> dict[str, Any]:
        return self.client.traverse_graph(
            seed_ids, scope=scope, actor=self.principal, task=task,
            max_depth=max_depth, max_claims=max_claims, state="admitted")

    def get_lineage(self, claim_id: str) -> dict[str, Any]:
        receipt = self.get_review_receipt(claim_id)
        graph = self.get_graph(receipt["claim"].get("scope"))
        incoming: dict[str, list[dict[str, Any]]] = {}
        for edge in graph.get("edges", []):
            incoming.setdefault(edge["to"], []).append(edge)
        wanted, pending, edges = {claim_id}, [claim_id], []
        while pending:
            current = pending.pop()
            for edge in incoming.get(current, []):
                if edge.get("type") not in {"supports", "derived_from", "bound_as"}:
                    continue
                edges.append(edge)
                if edge["from"] not in wanted:
                    wanted.add(edge["from"])
                    pending.append(edge["from"])
        return {"claim_id": claim_id, "state": receipt["state"],
                "scope": receipt["claim"].get("scope"),
                "nodes": [row for row in graph.get("nodes", [])
                          if row["id"] in wanted], "edges": edges,
                "evidence": receipt.get("evidence", []),
                "ledger_head": receipt.get("ledger_head")}

    def get_review_summary(self, scope: str | None = None) -> dict[str, Any]:
        return self.client.review_summary(scope, actor=self.principal)

    def get_review_receipt(self, claim_id: str) -> dict[str, Any]:
        return self.client.review_receipt(claim_id, actor=self.principal)

    def get_review_link(self, claim_id: str) -> dict[str, Any]:
        receipt = self.get_review_receipt(claim_id)
        result: dict[str, Any] = {
            "claim_id": claim_id,
            "state": receipt["state"],
            "requires_human_owner": True,
        }
        if self.review_base_url:
            result["url"] = self.review_base_url + "/review?" + urlencode(
                {"claim_id": claim_id})
        else:
            result["url"] = None
            result["configuration_required"] = "PROOFPRESS_REVIEW_BASE_URL"
        return result


class ApplicabilityCard(TypedDict, total=False):
    """Discovery card for a proposed claim; give at least one field.

    title and description are strings. when_relevant, keywords, and
    validity_conditions are arrays of non-empty strings, never one sentence.
    No other keys are accepted.
    """

    # Unknown keys then fail argument validation by name instead of being dropped;
    # the schema also states the kernel's at-least-one-field rule and this docstring.
    __pydantic_config__ = {"extra": "forbid",  # type: ignore[misc]
                           "json_schema_extra": {"minProperties": 1}}

    title: NonEmptyText
    description: NonEmptyText
    when_relevant: list[NonEmptyText] | None
    keywords: list[NonEmptyText] | None
    validity_conditions: list[NonEmptyText] | None


SERVER_SIDE_ERROR_TEXT = (
    "the Proofpress server could not complete the operation; see the server log")
# The kernel's envelope code for an OSError; its text can name a file on the server.
_SERVER_SIDE_CODES = frozenset({"operation_io_error"})


def _is_server_side(exc: ProofpressError) -> bool:
    """A failure of the server's own environment rather than of the request."""
    return isinstance(exc, ProofpressTransportError) or exc.code in _SERVER_SIDE_CODES


def _tool_error_text(exc: Exception) -> str:
    """Text an agent reads for an anticipated failure: always "code: message".

    A ProofpressError carries the stable code of the operation envelope (for
    example operation_rejected), its details when there are any, and says
    when a retry may succeed. For a transport or I/O failure only the code and
    a fixed phrase are forwarded; the message belongs in the server log. An
    McpRequestError comes from a check in this MCP layer and gets the same
    code the hosted MCP transport uses for those checks, invalid_tool_request.
    """
    if isinstance(exc, ProofpressError):
        if _is_server_side(exc):
            text = f"{exc.code}: {SERVER_SIDE_ERROR_TEXT}"
        else:
            text = f"{exc.code}: {exc.message}"
            if exc.details:
                text += " " + json.dumps(exc.details, sort_keys=True)
        return text + " (retryable)" if exc.retryable else text
    return f"invalid_tool_request: {exc}"


def _agent_facing(fn):
    """Forward anticipated failures to the agent; leave genuine crashes to the SDK.

    The official SDK forwards only the text of its own ToolError to the client.
    Every other exception is treated as a crash: the client reads just
    "Error executing tool <name>" and the reason stays in the server log.
    Proofpress reports contract violations as McpRequestError (the gateway's
    own checks) and ProofpressError (the operation envelope any transport
    returns, raised by the client), so both are re-raised as ToolError. A
    request-level error keeps its message so the agent can correct the call.
    A failure of the server's own environment (a transport error, an I/O
    error) forwards its code only, so the agent can tell a broken server from
    a bad request while the message, which can name files or upstream
    services, is logged here. Anything else, a plain ValueError included, is
    left alone and stays generic.
    """
    from mcp.server.mcpserver.exceptions import ToolError

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except (McpRequestError, ProofpressError) as exc:
            if isinstance(exc, ProofpressError) and _is_server_side(exc):
                logger.error("%s: %s", exc.code, exc.message)
            raise ToolError(_tool_error_text(exc)) from exc

    return wrapper


def build_mcp_server(gateway: ProofpressMcpGateway):
    """Build the optional official-SDK server without making MCP a core dependency."""
    try:
        from mcp.server import MCPServer
    except ImportError as exc:  # pragma: no cover - exercised in CLI packaging checks
        raise RuntimeError(
            "MCP support requires the optional dependency: pip install 'proofpress-local[mcp]'"
        ) from exc

    server = MCPServer(MCP_SERVER_NAME, instructions=MCP_INSTRUCTIONS)

    def tool(name: str):
        """Register one agent-facing tool; every tool goes through _agent_facing."""
        def register(fn):
            return server.tool(name=name)(_agent_facing(fn))
        return register

    @tool(name="proofpress_capabilities")
    def proofpress_capabilities() -> dict[str, Any]:
        """Describe the safe MCP surface and underlying Proofpress contract."""
        return gateway.capabilities()

    @tool(name="proofpress_submit_evidence")
    def proofpress_submit_evidence(
            payload: dict[str, Any],
            profile: str | None = None,
            idempotency_key: str | None = None) -> dict[str, Any]:
        """Submit bounded evidence.

        Omit profile for a proofpress/retrieval-evidence/v1 envelope. The only
        supported evidence profile is experiment.
        """
        return gateway.submit_evidence(
            payload, idempotency_key=idempotency_key, profile=profile)

    @tool(name="proofpress_propose_claim")
    def proofpress_propose_claim(
            statement: str, evidence_refs: list[str], scope: str | None = None,
            expires_at: str | None = None,
            artifact_refs: list[str] | None = None,
            applicability: ApplicabilityCard | None = None,
            reproposal_of: str | None = None,
            qualifiers: dict[str, Any] | None = None,
            profile: str | None = None,
            idempotency_key: str | None = None, *, title: str) -> dict[str, Any]:
        """Propose an evidence-bound claim as the configured agent principal.

        Required title is a short claim heading (at most 120 characters).
        Statement is the complete claim; title does not replace its limits.

        evidence_refs must be evd_ IDs returned by
        proofpress_submit_evidence, not source or artifact URLs.

        Scope is optional legacy exact-filter metadata. Applicability is a
        small discoverable card with at least one field: title and
        description are strings; when_relevant, keywords, and
        validity_conditions are arrays of non-empty strings, never a single
        sentence. To answer request_changes, read the original review receipt and pass
        qualifiers.revision_of (original claim ID) and
        qualifiers.revision_request_ref (revision_request.event_id). Preserve
        any required profile qualifiers and state the revised applicability.
        The revised candidate
        still needs human approval; proposing never replaces or admits it.

        To propose a corrected successor after a rejection, pass
        reproposal_of with the rejected claim ID. The old rejection remains
        immutable and the new candidate requires a new human decision.
        """
        return gateway.propose_claim(
            statement, evidence_refs, scope, expires_at, artifact_refs,
            None if applicability is None else dict(applicability),
            reproposal_of, qualifiers, profile, idempotency_key, title=title)

    @tool(name="proofpress_discover_context")
    def proofpress_discover_context(
            task: str | None = None, limit: int = 24) -> dict[str, Any]:
        """Discover only admitted, current context visible to this agent.

        Task words rank the frontmatter-style applicability cards. This does
        not weaken credential or actor visibility checks.
        """
        return gateway.discover_context(task, limit)

    @tool(name="proofpress_get_context")
    def proofpress_get_context(
            scope: str | None = None,
            task: str | None = None) -> dict[str, Any]:
        """Return admitted, current context eligible for this agent.

        Scope remains an optional legacy exact filter; discover_context is the
        normal starting point when an agent does not know a scope name.
        """
        return gateway.get_context(scope, task)

    @tool(name="proofpress_get_graph")
    def proofpress_get_graph(scope: str | None = None) -> dict[str, Any]:
        """Read the governed claim graph for an optional scope."""
        return gateway.get_graph(scope)

    @tool(name="proofpress_start_run")
    def proofpress_start_run(purpose: str, metadata: dict[str, Any] | None = None,
                             idempotency_key: str | None = None) -> dict[str, Any]:
        """Start a task run. The configured principal is recorded by the server."""
        return gateway.start_run(purpose, metadata, idempotency_key)

    @tool(name="proofpress_finish_run")
    def proofpress_finish_run(run_id: str, status: str, summary: str | None = None,
                              idempotency_key: str | None = None) -> dict[str, Any]:
        """Finish a run as completed, failed, or aborted."""
        return gateway.finish_run(run_id, status, summary, idempotency_key)

    @tool(name="proofpress_get_run")
    def proofpress_get_run(run_id: str) -> dict[str, Any]:
        """Read one run and its frozen receipts, declared reliance, outputs, and observations."""
        return gateway.get_run(run_id)

    @tool(name="proofpress_list_runs")
    def proofpress_list_runs(status: str | None = None,
                             limit: int = 50) -> dict[str, Any]:
        """List task runs without changing governance state."""
        return gateway.list_runs(status, limit)

    @tool(name="proofpress_capture_context")
    def proofpress_capture_context(run_id: str, scope: str | None = None,
                                   task: str | None = None,
                                   idempotency_key: str | None = None) -> dict[str, Any]:
        """Retrieve authorized governed context and freeze the exact returned versions for a run."""
        return gateway.capture_context(run_id, scope, task, idempotency_key)

    @tool(name="proofpress_record_reliance")
    def proofpress_record_reliance(run_id: str, receipt_id: str, claim_id: str,
                                   claim_digest: str, purpose: str,
                                   idempotency_key: str | None = None) -> dict[str, Any]:
        """Explicitly declare reliance on one exact claim version from a run receipt."""
        return gateway.record_reliance(run_id, receipt_id, claim_id, claim_digest,
                                       purpose, idempotency_key)

    @tool(name="proofpress_record_output")
    def proofpress_record_output(run_id: str, reference: str, content_digest: str,
                                 summary: str | None = None,
                                 reliance_ids: list[str] | None = None,
                                 media_type: str | None = None,
                                 idempotency_key: str | None = None) -> dict[str, Any]:
        """Record an external artifact reference and content hash; content stays in its source system."""
        return gateway.record_output(run_id, reference, content_digest, summary,
                                     reliance_ids, media_type, idempotency_key)

    @tool(name="proofpress_record_observation")
    def proofpress_record_observation(run_id: str, kind: str, source: str,
                                      meaning: str,
                                      evidence_refs: list[str] | None = None,
                                      output_ids: list[str] | None = None,
                                      observed_at: str | None = None,
                                      idempotency_key: str | None = None) -> dict[str, Any]:
        """Append a sourced test, human, external-evaluation, or outcome observation; no score is inferred."""
        return gateway.record_observation(run_id, kind, source, meaning,
                                          evidence_refs, output_ids, observed_at,
                                          idempotency_key)

    @tool(name="proofpress_traverse_graph")
    def proofpress_traverse_graph(
            seed_ids: list[str], scope: str | None = None,
            task: str | None = None, max_depth: int = 2,
            max_claims: int = 48) -> dict[str, Any]:
        """Traverse eligible admitted relations from one or more claims."""
        return gateway.traverse_graph(
            seed_ids, scope, task, max_depth, max_claims)

    @tool(name="proofpress_get_lineage")
    def proofpress_get_lineage(claim_id: str) -> dict[str, Any]:
        """Trace a claim through evidence derivations to source records."""
        return gateway.get_lineage(claim_id)

    @tool(name="proofpress_get_review_summary")
    def proofpress_get_review_summary(
            scope: str | None = None) -> dict[str, Any]:
        """Read review-state counts without making an authority decision."""
        return gateway.get_review_summary(scope)

    @tool(name="proofpress_get_review_receipt")
    def proofpress_get_review_receipt(
            claim_id: str) -> dict[str, Any]:
        """Read the evidence, checks, state, and authority receipt for a claim."""
        return gateway.get_review_receipt(claim_id)

    @tool(name="proofpress_get_review_link")
    def proofpress_get_review_link(claim_id: str) -> dict[str, Any]:
        """Create a link for the human owner; this tool cannot approve the claim."""
        return gateway.get_review_link(claim_id)

    return server


def _configured_client(args) -> ProofpressClient:
    if args.base_url:
        token = os.environ.get(args.token_env)
        if not token:
            raise SystemExit(f"missing bearer token in {args.token_env}")
        if args.base_url.startswith("https://"):
            return ProofpressClient.remote(args.base_url, token, args.timeout)
        return ProofpressClient.localhost(args.base_url, token, args.timeout)
    workspace = Path(args.workspace).resolve()
    os.chdir(workspace)
    return ProofpressClient.in_process(workspace)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="proofpress mcp",
        description="Safe MCP adapter over the Proofpress operation contract")
    parser.add_argument("--transport", choices=("stdio", "streamable-http"),
                        default="stdio")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--base-url")
    parser.add_argument("--token-env", default="PROOFPRESS_MCP_TOKEN")
    parser.add_argument("--principal-env", default="PROOFPRESS_MCP_PRINCIPAL")
    parser.add_argument("--review-base-url",
                        default=os.environ.get("PROOFPRESS_REVIEW_BASE_URL"))
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7333)
    args = parser.parse_args(argv)

    principal = os.environ.get(args.principal_env)
    if not principal and args.base_url:
        principal = "server-derived"
    if not principal:
        raise SystemExit(f"missing configured agent principal in {args.principal_env}")
    if args.transport == "streamable-http" and args.host not in {
            "127.0.0.1", "::1", "localhost"}:
        raise SystemExit(
            "reference MCP HTTP transport is loopback-only until hosted MCP authentication is configured")

    gateway = ProofpressMcpGateway(
        _configured_client(args), principal, args.review_base_url)
    server = build_mcp_server(gateway)
    if args.transport == "stdio":
        server.run(transport="stdio")
    else:
        server.run(transport="streamable-http", host=args.host, port=args.port)


if __name__ == "__main__":
    main()

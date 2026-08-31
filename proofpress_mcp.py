"""Thin MCP adapter over the canonical Proofpress operation contract."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urlparse

from proofpress_sdk import ProofpressClient


MCP_SERVER_NAME = "Proofpress"
MCP_INSTRUCTIONS = (
    "Proofpress governs agent-produced knowledge. Submit only bounded evidence; "
    "propose conclusions with evidence references; retrieve only governed context. "
    "This server intentionally exposes no Human Approval, rejection, supersession, "
    "policy, credential, or owner-recovery tool. Ask the human owner to use the "
    "separate review surface for authority-bearing decisions."
)
MCP_SAFE_TOOLS = (
    "proofpress_capabilities",
    "proofpress_submit_evidence",
    "proofpress_propose_conclusion",
    "proofpress_get_context",
    "proofpress_get_graph",
    "proofpress_get_review_summary",
    "proofpress_get_review_receipt",
    "proofpress_get_review_link",
)


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
            "principal": self.principal,
            "tools": list(MCP_SAFE_TOOLS),
            "human_approval_available": False,
        }
        return result

    def submit_evidence(self, payload: dict[str, Any],
                        idempotency_key: str | None = None) -> dict[str, Any]:
        return self.client.submit_evidence(
            payload, idempotency_key=idempotency_key)

    def propose_conclusion(
            self, statement: str, evidence_refs: list[str], scope: str,
            expires_at: str | None = None,
            artifact_refs: list[str] | None = None,
            allowed_actors: list[str] | None = None,
            qualifiers: dict[str, Any] | None = None,
            profile: str | None = None,
            idempotency_key: str | None = None) -> dict[str, Any]:
        return self.client.propose_conclusion(
            statement, evidence_refs, scope, self.principal,
            expires_at=expires_at, artifact_refs=artifact_refs,
            allowed_actors=allowed_actors, qualifiers=qualifiers,
            profile=profile, idempotency_key=idempotency_key)

    def get_context(self, scope: str | None = None,
                    task: str | None = None) -> dict[str, Any]:
        return self.client.context(
            scope=scope, actor=self.principal, task=task,
            include_blocked_statements=False)

    def get_graph(self, scope: str | None = None) -> dict[str, Any]:
        return self.client.graph(scope)

    def get_review_summary(self, scope: str | None = None) -> dict[str, Any]:
        return self.client.review_summary(scope)

    def get_review_receipt(self, conclusion_id: str) -> dict[str, Any]:
        return self.client.review_receipt(conclusion_id)

    def get_review_link(self, conclusion_id: str) -> dict[str, Any]:
        receipt = self.get_review_receipt(conclusion_id)
        result: dict[str, Any] = {
            "conclusion_id": conclusion_id,
            "state": receipt["state"],
            "requires_human_owner": True,
        }
        if self.review_base_url:
            result["url"] = self.review_base_url + "/review?" + urlencode(
                {"conclusion_id": conclusion_id})
        else:
            result["url"] = None
            result["configuration_required"] = "PROOFPRESS_REVIEW_BASE_URL"
        return result


def build_mcp_server(gateway: ProofpressMcpGateway):
    """Build the optional official-SDK server without making MCP a core dependency."""
    try:
        from mcp.server import MCPServer
    except ImportError as exc:  # pragma: no cover - exercised in CLI packaging checks
        raise RuntimeError(
            "MCP support requires the optional dependency: pip install 'proofpress-local[mcp]'"
        ) from exc

    server = MCPServer(MCP_SERVER_NAME, instructions=MCP_INSTRUCTIONS)

    @server.tool(name="proofpress_capabilities")
    def proofpress_capabilities() -> dict[str, Any]:
        """Describe the safe MCP surface and underlying Proofpress contract."""
        return gateway.capabilities()

    @server.tool(name="proofpress_submit_evidence")
    def proofpress_submit_evidence(
            payload: dict[str, Any],
            idempotency_key: str | None = None) -> dict[str, Any]:
        """Submit one bounded proofpress/retrieval-evidence/v1 envelope."""
        return gateway.submit_evidence(payload, idempotency_key)

    @server.tool(name="proofpress_propose_conclusion")
    def proofpress_propose_conclusion(
            statement: str, evidence_refs: list[str], scope: str,
            expires_at: str | None = None,
            artifact_refs: list[str] | None = None,
            allowed_actors: list[str] | None = None,
            qualifiers: dict[str, Any] | None = None,
            profile: str | None = None,
            idempotency_key: str | None = None) -> dict[str, Any]:
        """Propose an evidence-bound conclusion as the configured agent principal."""
        return gateway.propose_conclusion(
            statement, evidence_refs, scope, expires_at, artifact_refs,
            allowed_actors, qualifiers, profile, idempotency_key)

    @server.tool(name="proofpress_get_context")
    def proofpress_get_context(
            scope: str | None = None,
            task: str | None = None) -> dict[str, Any]:
        """Return only admitted, current, in-scope context eligible for this agent."""
        return gateway.get_context(scope, task)

    @server.tool(name="proofpress_get_graph")
    def proofpress_get_graph(scope: str | None = None) -> dict[str, Any]:
        """Read the governed claim graph for an optional scope."""
        return gateway.get_graph(scope)

    @server.tool(name="proofpress_get_review_summary")
    def proofpress_get_review_summary(
            scope: str | None = None) -> dict[str, Any]:
        """Read review-state counts without making an authority decision."""
        return gateway.get_review_summary(scope)

    @server.tool(name="proofpress_get_review_receipt")
    def proofpress_get_review_receipt(
            conclusion_id: str) -> dict[str, Any]:
        """Read the evidence, checks, state, and authority receipt for a conclusion."""
        return gateway.get_review_receipt(conclusion_id)

    @server.tool(name="proofpress_get_review_link")
    def proofpress_get_review_link(conclusion_id: str) -> dict[str, Any]:
        """Create a link for the human owner; this tool cannot approve the conclusion."""
        return gateway.get_review_link(conclusion_id)

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
        prog="proofpress-mcp",
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

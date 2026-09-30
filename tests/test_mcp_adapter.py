import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any
import unittest


ROOT = Path(__file__).resolve().parents[1]
HAS_MCP_SDK = importlib.util.find_spec("mcp") is not None


class GatewayFixture(unittest.TestCase):
    """A gateway over an in-process client on a fresh temporary repository."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"],
                       cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"],
                       cwd=self.repo, check=True)
        sys.path.insert(0, str(ROOT))
        import proofpress_mcp
        from proofpress import client as proofpress_sdk
        self.mcp = proofpress_mcp
        self.previous = Path.cwd()
        os.chdir(self.repo)
        client = proofpress_sdk.ProofpressClient.in_process(self.repo)
        self.gateway = proofpress_mcp.ProofpressMcpGateway(
            client, "agent:example-client", "https://review.example.test")

    def tearDown(self):
        os.chdir(self.previous)
        self.tmp.cleanup()

    @staticmethod
    def evidence_payload():
        quote = "The liability cap is one year of fees."
        return {
            "schema_version": "proofpress/retrieval-evidence/v1",
            "source": {
                "uri": "workspace://contracts/msa.pdf",
                "content_digest": "sha256:" + "a" * 64,
                "media_type": "application/pdf",
            },
            "evidence": {
                "quote": quote,
                "locator": {
                    "kind": "text_span", "start": 0, "end": len(quote),
                    "text_digest": "sha256:" + hashlib.sha256(
                        quote.encode()).hexdigest(),
                },
            },
            "retrieval": {
                "adapter": "partner.runtime", "version": "1",
                "query": "What is the liability cap?",
                "config_digest": "sha256:" + "b" * 64,
                "selection_reason": "direct clause match",
            },
        }

    @staticmethod
    def spreadsheet_evidence_payload():
        quote = "Revenue!F12 changed from 1180000 to 1050000."
        return {
            "schema_version": "proofpress/retrieval-evidence/v1",
            "source": {
                "uri": "workspace://finance/annual-plan.xlsx?revision=v18",
                "content_digest": "sha256:" + "c" * 64,
                "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            },
            "evidence": {"quote": quote, "locator": {
                "kind": "spreadsheet_cell", "sheet": "Revenue", "cell": "F12",
                "cell_digest": "sha256:" + "d" * 64,
                "previous_source_content_digest": "sha256:" + "e" * 64,
                "previous_cell_digest": "sha256:" + "f" * 64,
            }},
            "retrieval": {
                "adapter": "company.workbook-diff", "version": "1.0.0",
                "query": "Annual Plan Revenue!F12 revision",
                "config_digest": "sha256:" + "b" * 64,
            },
        }


class McpAdapterTests(GatewayFixture):
    def test_safe_surface_has_no_authority_bearing_tools(self):
        tools = set(self.mcp.MCP_SAFE_TOOLS)
        self.assertIn("proofpress_propose_claim", tools)
        self.assertIn("proofpress_get_review_link", tools)
        self.assertIn("proofpress_traverse_graph", tools)
        self.assertIn("proofpress_get_lineage", tools)
        for forbidden in ("approve", "admit", "reject", "supersede", "policy",
                          "credential", "owner"):
            self.assertFalse(any(forbidden in tool for tool in tools), forbidden)
        capabilities = self.gateway.capabilities()
        self.assertIn("mcp", capabilities["clients"])
        self.assertNotIn("mcp", capabilities["not_available"])
        self.assertFalse(capabilities["mcp"]["human_approval_available"])

    def test_mcp_submits_a_source_bound_spreadsheet_cell(self):
        imported = self.gateway.submit_evidence(
            self.spreadsheet_evidence_payload(), "mcp-spreadsheet-evidence-001")
        evidence_id = imported["evidence"][0]
        receipt = self.gateway.get_review_receipt(
            self.gateway.propose_claim(
                "Revenue!F12 was revised for the FY2026 base case.", [evidence_id],
                "finance:annual-plan:fy2026",
                idempotency_key="mcp-spreadsheet-proposal-001",
                title="FY2026 revenue revision")["claim"]["id"])
        locator = receipt["evidence"][0]["retrieval_receipt"]["locator"]
        self.assertEqual(locator["kind"], "spreadsheet_cell")
        self.assertEqual(locator["sheet"], "Revenue")
        self.assertEqual(locator["cell"], "F12")

    def test_bounded_evidence_proposal_and_context_close_the_loop(self):
        imported = self.gateway.submit_evidence(
            self.evidence_payload(), "mcp-evidence-001")
        evidence_id = imported["evidence"][0]
        replay = self.gateway.submit_evidence(
            self.evidence_payload(), "mcp-evidence-001")
        self.assertEqual(replay, imported)

        proposed = self.gateway.propose_claim(
            "The liability cap is one year of fees.", [evidence_id],
            "contract-review", idempotency_key="mcp-proposal-001", title="Test claim")
        claim = proposed["claim"]
        self.assertEqual(claim["proposer"], "agent:example-client")
        self.assertEqual(self.gateway.get_context("contract-review")["governed_context"], [])

        receipt = self.gateway.get_review_receipt(claim["id"])
        self.assertEqual(receipt["state"], "needs_review")
        lineage = self.gateway.get_lineage(claim["id"])
        self.assertEqual(lineage["claim_id"], claim["id"])
        self.assertEqual(
            {node["type"] for node in lineage["nodes"]},
            {"raw", "evidence", "claim"})
        self.assertEqual(
            {edge["type"] for edge in lineage["edges"]},
            {"bound_as", "supports"})
        link = self.gateway.get_review_link(claim["id"])
        self.assertTrue(link["requires_human_owner"])
        self.assertIn(claim["id"], link["url"])

        self.gateway.client.review_claim(
            claim["id"], "admit", "human:owner",
            review_request_id="human-review-001")
        context = self.gateway.get_context("contract-review")
        self.assertEqual(context["governed_context"][0]["id"], claim["id"])

    def test_principal_is_configuration_not_tool_input(self):
        parameters = self.gateway.propose_claim.__annotations__
        self.assertNotIn("proposer", parameters)
        with self.assertRaisesRegex(ValueError, "principal"):
            self.mcp.ProofpressMcpGateway(self.gateway.client, "")

    def test_mutation_contract_errors_are_actionable(self):
        with self.assertRaisesRegex(
                ValueError, "unsupported evidence profile: repository_change"):
            self.gateway.submit_evidence(
                {"repository": "example/repo"}, profile="repository_change")
        with self.assertRaisesRegex(
                ValueError, "evd_ IDs returned by proofpress_submit_evidence"):
            self.gateway.propose_claim(
                "A candidate", ["https://example.test/source"], "test", title="Test claim")

    def test_transport_module_imports_without_the_mcp_extra(self):
        # CI installs the extra, so block it and its dependencies here: the CLI
        # imports this module before it knows whether the optional SDK exists.
        blocked = ["mcp", "pydantic", "pydantic_core", "annotated_types", "typing_extensions"]
        completed = subprocess.run(
            [sys.executable, "-c",
             "import sys; sys.modules.update({name: None for name in %r}); "
             "import proofpress.transports.mcp as m; print(m.MCP_SERVER_NAME)" % blocked],
            capture_output=True, text=True, cwd=self.repo)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), "Proofpress")


EXPECTED_CARD_SHAPES = {
    "title": "string(minLength 1)", "description": "string(minLength 1)",
    "when_relevant": "array of string(minLength 1) or null",
    "keywords": "array of string(minLength 1) or null",
    "validity_conditions": "array of string(minLength 1) or null",
}


def _client_view(server, name, arguments) -> tuple[bool, Any]:
    """Call one tool in process and return (is_error, text_or_result).

    The SDK's request handler turns a ToolError raised by MCPServer.call_tool
    into an is_error result whose only content is the exception text, so this
    is exactly what a connected agent reads.
    """
    import anyio
    from mcp.server.mcpserver.exceptions import ToolError

    async def run() -> tuple[bool, Any]:
        try:
            result = await server.call_tool(name, arguments)
        except ToolError as exc:
            return True, str(exc)
        return False, result.structured_content

    return anyio.run(run)


def _arguments_from_schema(schema):
    """Build the smallest argument set a published input schema requires."""
    placeholders = {"string": "x", "array": [], "object": {}, "integer": 1,
                    "number": 1, "boolean": False}
    arguments = {}
    for name in schema.get("required", []):
        prop = schema["properties"][name]
        options = prop.get("anyOf", [prop])
        kind = next(option.get("type") for option in options
                    if option.get("type") not in {None, "null"})
        arguments[name] = placeholders[kind]
    return arguments


def _object_schema(root, node):
    """Follow anyOf and $ref to the object schema an optional parameter allows."""
    for option in node.get("anyOf", [node]):
        if "$ref" in option:
            return root["$defs"][option["$ref"].rsplit("/", 1)[1]]
        if option.get("type") == "object":
            return option
    raise AssertionError("no object schema in %r" % (node,))


def _shape(prop):
    """Render one property schema as text, constraints and nullability included."""
    kinds = []
    for option in prop.get("anyOf", [prop]):
        kind = option.get("type", "?")
        if kind == "array":
            kind = "array of " + _shape(option.get("items", {}))
        elif "minLength" in option:
            kind += "(minLength %d)" % option["minLength"]
        kinds.append(kind)
    return " or ".join(kinds)


def _field_shapes(card):
    return {name: _shape(prop) for name, prop in card.get("properties", {}).items()}


@unittest.skipUnless(HAS_MCP_SDK, "needs the mcp extra: pip install 'proofpress-local[mcp]'")
class McpServerErrorTests(GatewayFixture):
    """What an agent reads when a call fails through the official SDK server."""

    def setUp(self):
        super().setUp()
        self.server = self.mcp.build_mcp_server(self.gateway)
        self.evidence_id = self.gateway.submit_evidence(
            self.evidence_payload(), "mcp-server-evidence-001")["evidence"][0]

    def propose(self, **overrides):
        arguments = {"statement": "The liability cap is one year of fees.",
                     "evidence_refs": [self.evidence_id], "scope": "contract-review",
                     "title": "Test claim"}
        arguments.update(overrides)
        return _client_view(self.server, "proofpress_propose_claim", arguments)

    def test_a_string_for_a_list_field_is_named_in_the_error(self):
        for field in ("when_relevant", "keywords", "validity_conditions"):
            is_error, text = self.propose(applicability={field: "one sentence"})
            self.assertTrue(is_error, field)
            self.assertIn(field, text)
            self.assertIn("Input should be a valid list", text)

    def test_an_unknown_applicability_field_is_named_in_the_error(self):
        is_error, text = self.propose(applicability={"foo": "bar"})
        self.assertTrue(is_error)
        self.assertIn("foo", text)

    def test_gateway_validation_reaches_the_agent_as_an_invalid_request(self):
        is_error, text = self.propose(evidence_refs=["https://example.test/source"])
        self.assertTrue(is_error)
        self.assertEqual(text, (
            "Error executing tool proofpress_propose_claim: invalid_tool_request: "
            "evidence_refs must contain evd_ IDs returned by proofpress_submit_evidence; "
            "source and artifact URLs are not evidence IDs"))

    def test_kernel_validation_reaches_the_agent_with_its_code(self):
        is_error, text = self.propose(applicability={})
        self.assertTrue(is_error)
        self.assertEqual(text, (
            "Error executing tool proofpress_propose_claim: operation_rejected: "
            "applicability must contain at least one discovery field"))

    def test_error_text_carries_the_code_details_and_retryable_flag(self):
        from proofpress.client import ProofpressError, ProofpressTransportError
        from proofpress.transports.mcp import _tool_error_text

        self.assertEqual(
            _tool_error_text(ProofpressError("ledger_head_conflict", "STALE_LEDGER_HEAD",
                                             retryable=True)),
            "ledger_head_conflict: STALE_LEDGER_HEAD (retryable)")
        self.assertEqual(
            _tool_error_text(ProofpressError(
                "invalid_parameters", "invalid parameters for claim.propose",
                details={"missing": ["title"], "unknown": ["proposer"]})),
            'invalid_parameters: invalid parameters for claim.propose '
            '{"missing": ["title"], "unknown": ["proposer"]}')
        self.assertEqual(
            _tool_error_text(self.mcp.McpRequestError("scope must be a non-empty string")),
            "invalid_tool_request: scope must be a non-empty string")
        # Failures of the server's own environment keep their text in the server log.
        self.assertEqual(
            _tool_error_text(ProofpressError(
                "operation_io_error",
                "[Errno 28] No space left on device: '/workspace/.proofpress/ledger.jsonl'")),
            "operation_io_error: the Proofpress server could not complete the operation; "
            "see the server log")
        self.assertEqual(
            _tool_error_text(ProofpressTransportError(
                "transport_unavailable", "<urlopen error [Errno 61] Connection refused>",
                retryable=True)),
            "transport_unavailable: the Proofpress server could not complete the operation; "
            "see the server log (retryable)")

    def test_a_null_list_field_is_treated_as_absent(self):
        is_error, result = self.propose(applicability={"title": "Cap", "keywords": None})
        self.assertFalse(is_error, result)
        self.assertEqual(result["claim"]["applicability"], {"title": "Cap"})

    def test_an_empty_string_is_rejected_at_argument_validation(self):
        is_error, text = self.propose(applicability={"keywords": ["cap", ""]})
        self.assertTrue(is_error)
        self.assertIn("applicability.keywords.1", text)
        self.assertIn("at least 1 character", text)
        is_error, text = self.propose(applicability={"title": ""})
        self.assertTrue(is_error)
        self.assertIn("applicability.title", text)
        self.assertIn("at least 1 character", text)

    def test_card_fields_match_the_kernel_contract(self):
        from proofpress.hosted import mcp_http
        from proofpress.kernel import operations

        kernel_fields = set(operations.APPLICABILITY_TEXT_FIELDS +
                            operations.APPLICABILITY_LIST_FIELDS)
        self.assertEqual(set(self.mcp.ApplicabilityCard.__annotations__), kernel_fields)
        self.assertEqual(set(mcp_http.APPLICABILITY_SCHEMA["properties"]), kernel_fields)

    def test_a_valid_card_still_proposes(self):
        card = {"title": "Liability cap", "description": "Cap on liability in the MSA",
                "when_relevant": ["one sentence"], "keywords": ["cap", "liability"],
                "validity_conditions": ["MSA revision 4 in force"]}
        is_error, result = self.propose(applicability=card)
        self.assertFalse(is_error)
        self.assertEqual(result["claim"]["applicability"], card)

    def test_operation_errors_reach_the_agent_with_their_code(self):
        from proofpress.client import ProofpressError, ProofpressTransportError

        def io_failure(*args, **kwargs):
            raise ProofpressError(
                "operation_io_error",
                "[Errno 28] No space left on device: '/workspace/.proofpress/ledger.jsonl'")

        def stale_head(*args, **kwargs):
            raise ProofpressError("ledger_head_conflict", "STALE_LEDGER_HEAD", retryable=True)

        def proxy_down(*args, **kwargs):
            raise ProofpressTransportError("http_error", "Bad Gateway", retryable=True,
                                           status=502)

        def decode_failure(*args, **kwargs):
            return json.loads("<html>not json</html>")

        self.gateway.get_review_summary = io_failure
        self.gateway.get_graph = stale_head
        self.gateway.list_runs = proxy_down
        self.gateway.capabilities = decode_failure
        with self.assertLogs("proofpress.transports.mcp", level="ERROR") as logs:
            self.assertEqual(
                _client_view(self.server, "proofpress_get_review_summary", {}),
                (True, "Error executing tool proofpress_get_review_summary: "
                       "operation_io_error: the Proofpress server could not complete the "
                       "operation; see the server log"))
        self.assertIn("/workspace/.proofpress/ledger.jsonl", "\n".join(logs.output))
        self.assertEqual(
            _client_view(self.server, "proofpress_get_graph", {}),
            (True, "Error executing tool proofpress_get_graph: ledger_head_conflict: "
                   "STALE_LEDGER_HEAD (retryable)"))
        self.assertEqual(
            _client_view(self.server, "proofpress_list_runs", {}),
            (True, "Error executing tool proofpress_list_runs: http_error: the Proofpress "
                   "server could not complete the operation; see the server log (retryable)"))
        # A decode failure is a ValueError, but never the agent's request: it stays a crash.
        self.assertEqual(
            _client_view(self.server, "proofpress_capabilities", {}),
            (True, "Error executing tool proofpress_capabilities"))

    def test_a_crash_stays_generic(self):
        def explode(*args, **kwargs):
            raise RuntimeError("ledger file is corrupt at /private/workspace")

        def unplanned_value_error(*args, **kwargs):
            raise ValueError("could not parse /private/workspace/.proofpress/config")

        self.gateway.get_review_summary = explode
        self.gateway.get_graph = unplanned_value_error
        # Only the MCP layer's own request checks are agent-facing; any other
        # ValueError is a crash and keeps its text on the server.
        self.assertEqual(
            _client_view(self.server, "proofpress_get_review_summary", {}),
            (True, "Error executing tool proofpress_get_review_summary"))
        self.assertEqual(
            _client_view(self.server, "proofpress_get_graph", {}),
            (True, "Error executing tool proofpress_get_graph"))

    def test_every_tool_forwards_anticipated_failures_from_its_gateway_method(self):
        import anyio

        def anticipated(method):
            def raise_probe(*args, **kwargs):
                raise self.mcp.McpRequestError("probe: " + method)
            return raise_probe

        tools = anyio.run(self.server.list_tools)
        self.assertEqual({tool.name for tool in tools}, set(self.mcp.MCP_SAFE_TOOLS))
        for name in dir(self.gateway):
            if not name.startswith("_") and callable(getattr(self.gateway, name)):
                setattr(self.gateway, name, anticipated(name))
        for tool in tools:
            # proofpress_<method> calls gateway.<method>; the probe names which one ran.
            method = tool.name.removeprefix("proofpress_")
            is_error, text = _client_view(
                self.server, tool.name, _arguments_from_schema(tool.input_schema))
            self.assertEqual(
                (is_error, text),
                (True, f"Error executing tool {tool.name}: invalid_tool_request: probe: {method}"))

    def test_published_schema_states_the_applicability_shape(self):
        import anyio
        from proofpress.hosted import mcp_http

        tools = {tool.name: tool for tool in anyio.run(self.server.list_tools)}
        schema = tools["proofpress_propose_claim"].input_schema
        self.assertLessEqual({"title", "statement", "evidence_refs"}, set(schema["required"]))
        card = _object_schema(schema, schema["properties"]["applicability"])
        hosted = next(tool for tool in mcp_http.TOOLS
                      if tool["name"] == "proofpress_propose_claim")
        hosted_card = hosted["inputSchema"]["properties"]["applicability"]
        for published in (card, hosted_card):
            self.assertEqual(_field_shapes(published), EXPECTED_CARD_SHAPES)
            self.assertIs(published.get("additionalProperties"), False)
            self.assertEqual(published.get("minProperties"), 1)
            self.assertIn("arrays of non-empty strings", published.get("description", ""))

    def test_stdio_server_reports_the_reason_to_a_real_client(self):
        import anyio
        from mcp.client.session import ClientSession
        from mcp.client.stdio import StdioServerParameters, stdio_client

        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "proofpress.transports.mcp", "--workspace", str(self.repo)],
            env={**os.environ, "PROOFPRESS_MCP_PRINCIPAL": "agent:example-client"})

        cases = {
            "argument validation": {"applicability": {"when_relevant": "one sentence"}},
            "gateway check": {"evidence_refs": ["https://example.test/source"]},
            "kernel rejection": {"applicability": {}},
        }

        async def run():
            seen = {}
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    for label, overrides in cases.items():
                        arguments = {"statement": "The liability cap is one year of fees.",
                                     "evidence_refs": [self.evidence_id],
                                     "title": "Test claim", **overrides}
                        result = await session.call_tool("proofpress_propose_claim", arguments)
                        seen[label] = (result.is_error, " ".join(
                            getattr(block, "text", "") for block in result.content))
            return seen

        seen = anyio.run(run)
        self.assertTrue(all(is_error for is_error, _ in seen.values()), seen)
        self.assertIn("when_relevant", seen["argument validation"][1])
        self.assertIn("invalid_tool_request: evidence_refs must contain evd_ IDs",
                      seen["gateway check"][1])
        self.assertIn("operation_rejected: applicability must contain at least one",
                      seen["kernel rejection"][1])


if __name__ == "__main__":
    unittest.main()

import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class McpAdapterTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()

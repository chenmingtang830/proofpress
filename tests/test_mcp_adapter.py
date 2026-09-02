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
            client, "agent:kelton-codex", "https://review.example.test")

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

    def test_safe_surface_has_no_authority_bearing_tools(self):
        tools = set(self.mcp.MCP_SAFE_TOOLS)
        self.assertIn("proofpress_propose_conclusion", tools)
        self.assertIn("proofpress_get_review_link", tools)
        for forbidden in ("approve", "admit", "reject", "supersede", "policy",
                          "credential", "owner"):
            self.assertFalse(any(forbidden in tool for tool in tools), forbidden)
        capabilities = self.gateway.capabilities()
        self.assertIn("mcp", capabilities["clients"])
        self.assertNotIn("mcp", capabilities["not_available"])
        self.assertFalse(capabilities["mcp"]["human_approval_available"])

    def test_bounded_evidence_proposal_and_context_close_the_loop(self):
        imported = self.gateway.submit_evidence(
            self.evidence_payload(), "mcp-evidence-001")
        evidence_id = imported["evidence"][0]
        replay = self.gateway.submit_evidence(
            self.evidence_payload(), "mcp-evidence-001")
        self.assertEqual(replay, imported)

        proposed = self.gateway.propose_conclusion(
            "The liability cap is one year of fees.", [evidence_id],
            "partner-poc", idempotency_key="mcp-proposal-001")
        conclusion = proposed["conclusion"]
        self.assertEqual(conclusion["proposer"], "agent:kelton-codex")
        self.assertEqual(self.gateway.get_context("partner-poc")["knowledge"], [])

        receipt = self.gateway.get_review_receipt(conclusion["id"])
        self.assertEqual(receipt["state"], "needs_review")
        link = self.gateway.get_review_link(conclusion["id"])
        self.assertTrue(link["requires_human_owner"])
        self.assertIn(conclusion["id"], link["url"])

        self.gateway.client.review_conclusion(
            conclusion["id"], "admit", "human:kelton",
            review_request_id="human-review-001")
        context = self.gateway.get_context("partner-poc")
        self.assertEqual(context["knowledge"][0]["id"], conclusion["id"])

    def test_principal_is_configuration_not_tool_input(self):
        parameters = self.gateway.propose_conclusion.__annotations__
        self.assertNotIn("proposer", parameters)
        with self.assertRaisesRegex(ValueError, "principal"):
            self.mcp.ProofpressMcpGateway(self.gateway.client, "")


if __name__ == "__main__":
    unittest.main()

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]


def evidence_payload():
    quote = "The liability cap is one year of fees."
    return {
        "schema_version": "proofpress/retrieval-evidence/v1",
        "source": {"uri": "workspace://msa.pdf",
                   "content_digest": "sha256:" + "a" * 64},
        "evidence": {"quote": quote, "locator": {
            "kind": "text_span", "start": 0, "end": len(quote),
            "text_digest": "sha256:" + hashlib.sha256(quote.encode()).hexdigest()}},
        "retrieval": {"adapter": "partner", "version": "1", "query": "cap?",
                      "config_digest": "sha256:" + "b" * 64},
    }


class HostedServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        sys.path.insert(0, str(ROOT))
        import proofpress_hosted_service
        import proofpress_mcp
        import proofpress_sdk
        self.service = proofpress_hosted_service
        self.mcp = proofpress_mcp
        self.sdk = proofpress_sdk
        self.server = proofpress_hosted_service.create_hosted_server(
            Path(self.tmp.name) / "hosted.db", port=0, max_request_bytes=2048)
        self.owner = self.server.proofpress_control.bootstrap(
            "workspace:kelton", "human:kelton")
        self.agent = self.server.proofpress_control.issue_agent_credential(
            self.owner["token"], "agent:codex-laptop", "Codex laptop")
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.tmp.cleanup()

    def get(self, path, token=None):
        headers = {"Authorization": "Bearer " + token} if token else {}
        request = Request(self.base_url + path, headers=headers)
        try:
            with urlopen(request) as response:
                return response.status, json.loads(response.read())
        except HTTPError as exc:
            try:
                return exc.code, json.loads(exc.read())
            finally:
                exc.close()

    def test_health_readiness_auth_and_capability_boundary(self):
        self.assertEqual(self.get("/healthz")[0], 200)
        status, ready = self.get("/readyz")
        self.assertEqual(status, 200)
        self.assertEqual(ready["database_integrity"], "ok")
        self.assertEqual(self.get("/v1/capabilities")[0], 401)
        status, envelope = self.get("/v1/capabilities", self.agent["token"])
        self.assertEqual(status, 200)
        hosted = envelope["result"]["hosted"]
        self.assertEqual(hosted["principal_id"], "agent:codex-laptop")
        self.assertFalse(hosted["owner_approval_available"])
        self.assertEqual(envelope["result"]["transport"], "hosted_https")

    def test_two_clients_close_proposal_review_context_loop(self):
        agent = self.sdk.ProofpressClient.localhost(
            self.base_url, self.agent["token"])
        owner = self.sdk.ProofpressClient.localhost(
            self.base_url, self.owner["token"])
        imported = agent.submit_evidence(evidence_payload())
        proposed = agent.propose_conclusion(
            "The liability cap is one year of fees.", imported["evidence"],
            "partner-poc", "spoofed:owner")
        conclusion = proposed["conclusion"]
        self.assertEqual(conclusion["proposer"], "agent:codex-laptop")
        agent.evaluate_conclusion(conclusion["id"])
        owner.review_conclusion(
            conclusion["id"], "admit", "spoofed:agent",
            review_request_id="owner-review-1")
        context = agent.context(scope="partner-poc", actor="spoofed:owner")
        self.assertEqual(context["actor"], "agent:codex-laptop")
        self.assertEqual(context["knowledge"][0]["id"], conclusion["id"])

    def test_stdio_mcp_bridge_uses_hosted_credential_identity(self):
        client = self.sdk.ProofpressClient.localhost(
            self.base_url, self.agent["token"])
        gateway = self.mcp.ProofpressMcpGateway(client, "server-derived")
        capabilities = gateway.capabilities()
        self.assertEqual(capabilities["mcp"]["principal"], "agent:codex-laptop")
        imported = gateway.submit_evidence(evidence_payload())
        proposed = gateway.propose_conclusion(
            "The liability cap is one year of fees.", imported["evidence"],
            "mcp-poc")
        self.assertEqual(
            proposed["conclusion"]["proposer"], "agent:codex-laptop")

    def test_origin_refuses_public_bind_and_limits_request_bodies(self):
        with self.assertRaisesRegex(ValueError, "loopback"):
            self.service.create_hosted_server(
                Path(self.tmp.name) / "unsafe.db", host="0.0.0.0")
        request = Request(
            self.base_url + "/v1/operations", data=b"{" + b"x" * 3000,
            method="POST", headers={"Content-Type": "application/json",
                                     "Authorization": "Bearer " + self.agent["token"]})
        with self.assertRaises(HTTPError) as raised:
            urlopen(request)
        self.assertEqual(raised.exception.code, 413)
        raised.exception.close()


if __name__ == "__main__":
    unittest.main()

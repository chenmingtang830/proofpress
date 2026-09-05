import base64
import hashlib
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen

from proofpress.hosted.service import create_hosted_server


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class HostedMcpOAuthTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.server = create_hosted_server(
            Path(self.tmp.name) / "hosted.db", port=0)
        self.owner = self.server.proofpress_control.bootstrap(
            "workspace:test", "human:owner")
        self.agent = self.server.proofpress_control.issue_agent_credential(
            self.owner["token"], "agent:cursor", "Cursor")
        self.thread = threading.Thread(
            target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"
        self.resource = self.base + "/mcp"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.tmp.cleanup()

    def json_request(self, path, body=None, token=None):
        headers = {}
        data = None
        if body is not None:
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
        if token:
            headers["Authorization"] = "Bearer " + token
        request = Request(self.base + path, data=data, headers=headers,
                          method="POST" if body is not None else "GET")
        try:
            with urlopen(request) as response:
                raw = response.read()
                return response.status, response.headers, json.loads(raw) if raw else None
        except HTTPError as exc:
            try:
                raw = exc.read()
                return exc.code, exc.headers, json.loads(raw) if raw else None
            finally:
                exc.close()

    def form_request(self, path, values):
        request = Request(
            self.base + path, data=urlencode(values).encode(), method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"})
        try:
            with build_opener(NoRedirect()).open(request) as response:
                return response.status, response.headers, response.read()
        except HTTPError as exc:
            try:
                return exc.code, exc.headers, exc.read()
            finally:
                exc.close()

    def register(self):
        status, _, client = self.json_request("/register", {
            "client_name": "Test MCP client",
            "redirect_uris": ["http://127.0.0.1:9876/callback"],
            "token_endpoint_auth_method": "none",
        })
        self.assertEqual(status, 201)
        return client

    def authorize(self, credential):
        client = self.register()
        self.client_id = client["client_id"]
        verifier = "v" * 64
        challenge = base64.urlsafe_b64encode(
            hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
        values = {
            "response_type": "code", "client_id": client["client_id"],
            "redirect_uri": client["redirect_uris"][0], "state": "state-1",
            "code_challenge": challenge, "code_challenge_method": "S256",
            "resource": self.resource, "scope": "proofpress:agent",
            "agent_token": credential,
        }
        status, headers, _ = self.form_request("/authorize", values)
        if status != 303:
            return status, None, client, verifier
        query = parse_qs(urlparse(headers["Location"]).query)
        self.assertEqual(query["state"], ["state-1"])
        return status, query["code"][0], client, verifier

    def exchange(self):
        status, code, client, verifier = self.authorize(self.agent["token"])
        self.assertEqual(status, 303)
        status, _, tokens = self.form_request("/token", {
            "grant_type": "authorization_code", "code": code,
            "client_id": client["client_id"],
            "redirect_uri": client["redirect_uris"][0],
            "resource": self.resource, "code_verifier": verifier,
        })
        self.assertEqual(status, 200)
        return json.loads(tokens)

    def test_discovery_challenge_and_owner_rejection(self):
        status, _, metadata = self.json_request(
            "/.well-known/oauth-protected-resource")
        self.assertEqual(status, 200)
        self.assertEqual(metadata["resource"], self.resource)
        status, headers, _ = self.json_request("/mcp", {
            "jsonrpc": "2.0", "id": 1, "method": "initialize"})
        self.assertEqual(status, 401)
        self.assertIn("resource_metadata=", headers["WWW-Authenticate"])
        status, _, _, _ = self.authorize(self.owner["token"])
        self.assertEqual(status, 401)

    def test_pkce_token_remote_mcp_and_revocation(self):
        tokens = self.exchange()
        self.assertTrue(tokens["access_token"].startswith("ppoa_"))
        request = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                   "params": {"protocolVersion": "2025-06-18",
                              "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}}
        status, _, response = self.json_request(
            "/mcp", request, tokens["access_token"])
        self.assertEqual(status, 200)
        self.assertEqual(response["result"]["serverInfo"]["name"], "Proofpress")
        status, _, response = self.json_request("/mcp", {
            "jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            tokens["access_token"])
        tools = {row["name"]: row for row in response["result"]["tools"]}
        names = set(tools)
        self.assertIn("proofpress_discover_context", names)
        self.assertIn("proofpress_traverse_graph", names)
        self.assertIn("proofpress_get_lineage", names)
        self.assertNotIn("proofpress_approve", names)
        submit_schema = tools["proofpress_submit_evidence"]["inputSchema"]
        self.assertEqual(
            submit_schema["properties"]["profile"]["enum"], ["experiment"])
        retrieval = submit_schema["allOf"][0]["then"]["properties"]["payload"]
        self.assertEqual(
            retrieval["properties"]["schema_version"]["const"],
            "proofpress/retrieval-evidence/v1")
        proposal_refs = tools["proofpress_propose_conclusion"]["inputSchema"]["properties"]["evidence_refs"]
        self.assertEqual(proposal_refs["minItems"], 1)
        self.assertEqual(proposal_refs["items"]["pattern"], r"^evd_[0-9a-f]{16}$")
        proposal_properties = tools["proofpress_propose_conclusion"][
            "inputSchema"]["properties"]
        self.assertEqual(proposal_properties["reproposal_of"]["pattern"],
                         r"^knw_[A-Za-z0-9]+$")
        self.assertNotIn("allowed_actors", proposal_properties)
        self.server.proofpress_control.revoke_credential(
            self.owner["token"], self.agent["credential_id"])
        self.assertEqual(self.json_request(
            "/mcp", request, tokens["access_token"])[0], 401)

    def test_authorization_code_is_single_use_and_refresh_rotates(self):
        tokens = self.exchange()
        status, _, replacement_raw = self.form_request("/token", {
            "grant_type": "refresh_token",
            "refresh_token": tokens["refresh_token"],
            "client_id": self.client_id,
            "resource": self.resource,
        })
        self.assertEqual(status, 200)
        replacement = json.loads(replacement_raw)
        self.assertNotEqual(replacement["access_token"], tokens["access_token"])
        status, _, body = self.form_request("/token", {
            "grant_type": "refresh_token",
            "refresh_token": tokens["refresh_token"],
            "client_id": self.client_id,
            "resource": self.resource,
        })
        self.assertEqual(status, 400)
        self.assertEqual(json.loads(body)["error"], "invalid_grant")
        initialize = {"jsonrpc": "2.0", "id": 9, "method": "initialize"}
        self.assertEqual(self.json_request(
            "/mcp", initialize, replacement["access_token"])[0], 401)

    def test_remote_mcp_returns_actionable_mutation_errors(self):
        tokens = self.exchange()
        status, _, response = self.json_request("/mcp", {
            "jsonrpc": "2.0", "id": 20, "method": "tools/call",
            "params": {"name": "proofpress_submit_evidence", "arguments": {
                "payload": {"repository": "example/repo"},
                "profile": "repository_change",
            }}}, tokens["access_token"])
        self.assertEqual(status, 200)
        result = response["result"]
        self.assertTrue(result["isError"])
        self.assertEqual(
            result["structuredContent"]["error"]["code"],
            "invalid_tool_request")
        self.assertIn(
            "unsupported evidence profile: repository_change",
            result["structuredContent"]["error"]["message"])

        status, _, response = self.json_request("/mcp", {
            "jsonrpc": "2.0", "id": 21, "method": "tools/call",
            "params": {"name": "proofpress_propose_conclusion", "arguments": {
                "statement": "A candidate", "scope": "test",
                "evidence_refs": ["https://example.test/source"],
            }}}, tokens["access_token"])
        self.assertEqual(status, 200)
        result = response["result"]
        self.assertTrue(result["isError"])
        self.assertIn(
            "evd_ IDs returned by proofpress_submit_evidence",
            result["structuredContent"]["error"]["message"])


if __name__ == "__main__":
    unittest.main()

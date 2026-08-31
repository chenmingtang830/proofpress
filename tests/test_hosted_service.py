import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.parse import urlencode
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

    def owner_admin(self, token, body):
        request = Request(
            self.base_url + "/v1/owner/credentials",
            data=json.dumps(body).encode(), method="POST",
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer " + token})
        try:
            with urlopen(request) as response:
                return response.status, json.loads(response.read())
        except HTTPError as exc:
            try:
                return exc.code, json.loads(exc.read())
            finally:
                exc.close()

    def form(self, path, values, cookie=None):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if cookie:
            headers["Cookie"] = cookie
        request = Request(
            self.base_url + path, data=urlencode(values).encode(), method="POST",
            headers=headers)
        opener = __import__("urllib.request", fromlist=["build_opener"]).build_opener(
            __import__("urllib.request", fromlist=["HTTPRedirectHandler"]).HTTPRedirectHandler())
        try:
            with opener.open(request) as response:
                return response.status, response.headers, response.read().decode()
        except HTTPError as exc:
            try:
                return exc.code, exc.headers, exc.read().decode()
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

    def test_owner_web_login_review_and_successor_context(self):
        agent = self.sdk.ProofpressClient.localhost(
            self.base_url, self.agent["token"])
        imported = agent.submit_evidence(evidence_payload())
        proposed = agent.propose_conclusion(
            "The liability cap is one year of fees.", imported["evidence"],
            "web-review-poc", "spoofed")
        conclusion_id = proposed["conclusion"]["id"]
        agent.evaluate_conclusion(conclusion_id)

        status, _, login = self.form("/owner/login", {"token": "wrong"})
        self.assertEqual(status, 401)
        self.assertNotIn(self.owner["token"], login)

        request = Request(
            self.base_url + "/owner/login",
            data=urlencode({"token": self.owner["token"]}).encode(),
            method="POST", headers={"Content-Type": "application/x-www-form-urlencoded"})
        class NoRedirect(__import__("urllib.request", fromlist=["HTTPRedirectHandler"]).HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None
        opener = __import__("urllib.request", fromlist=["build_opener"]).build_opener(NoRedirect())
        with self.assertRaises(HTTPError) as raised:
            opener.open(request)
        self.assertEqual(raised.exception.code, 303)
        cookie = raised.exception.headers["Set-Cookie"].split(";", 1)[0]
        raised.exception.close()

        review_request = Request(
            self.base_url + "/review?" + urlencode({"conclusion_id": conclusion_id}),
            headers={"Cookie": cookie})
        with urlopen(review_request) as response:
            page = response.read().decode()
        self.assertIn("Evidence and receipts", page)
        self.assertNotIn(self.owner["token"], page)
        session_id = cookie.split("=", 1)[1]
        csrf = self.server.proofpress_owner_sessions[session_id]["csrf"]
        status, _, _ = self.form("/owner/review", {
            "csrf": csrf, "conclusion_id": conclusion_id,
            "decision": "admit", "note": "Richard dogfood",
        }, cookie)
        self.assertEqual(status, 200)
        successor = self.sdk.ProofpressClient.localhost(
            self.base_url, self.agent["token"])
        context = successor.context(scope="web-review-poc", actor="spoofed")
        self.assertEqual([row["id"] for row in context["knowledge"]], [conclusion_id])

    def test_owner_review_rejects_csrf_failure(self):
        request = Request(
            self.base_url + "/owner/login",
            data=urlencode({"token": self.owner["token"]}).encode(), method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"})
        class NoRedirect(__import__("urllib.request", fromlist=["HTTPRedirectHandler"]).HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None
        opener = __import__("urllib.request", fromlist=["build_opener"]).build_opener(NoRedirect())
        with self.assertRaises(HTTPError) as raised:
            opener.open(request)
        cookie = raised.exception.headers["Set-Cookie"].split(";", 1)[0]
        raised.exception.close()
        status, _, body = self.form("/owner/review", {
            "csrf": "wrong", "conclusion_id": "missing", "decision": "admit",
        }, cookie)
        self.assertEqual(status, 403)
        self.assertIn("csrf_failed", body)

    def test_owner_https_credential_lifecycle_is_separate_from_mcp(self):
        status, issued = self.owner_admin(self.owner["token"], {
            "action": "issue", "principal_id": "agent:claude-code",
            "label": "Claude Code laptop"})
        self.assertEqual(status, 200)
        token = issued["result"]["token"]
        credential_id = issued["result"]["credential_id"]
        self.assertNotEqual(token, self.agent["token"])
        status, listing = self.get(
            "/v1/owner/credentials", self.owner["token"])
        self.assertEqual(status, 200)
        row = next(item for item in listing["credentials"]
                   if item["credential_id"] == credential_id)
        self.assertEqual(row["principal_id"], "agent:claude-code")
        self.assertNotIn("token", row)
        self.assertNotIn("secret_hash", row)

        status, rotated = self.owner_admin(self.owner["token"], {
            "action": "rotate", "credential_id": credential_id})
        self.assertEqual(status, 200)
        self.assertEqual(self.get("/v1/capabilities", token)[0], 401)
        replacement = rotated["result"]
        self.assertEqual(self.get(
            "/v1/capabilities", replacement["token"])[0], 200)
        status, revoked = self.owner_admin(self.owner["token"], {
            "action": "revoke", "credential_id": replacement["credential_id"]})
        self.assertEqual(status, 200)
        self.assertEqual(revoked["result"]["revoked"],
                         replacement["credential_id"])
        self.assertEqual(self.get(
            "/v1/capabilities", replacement["token"])[0], 401)

        status, denied = self.owner_admin(self.agent["token"], {
            "action": "issue", "principal_id": "agent:forbidden",
            "label": "Forbidden"})
        self.assertEqual(status, 401)
        self.assertEqual(denied["error"]["code"], "owner_required")

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

    def test_managed_platform_can_explicitly_bind_public_interface(self):
        server = self.service.create_hosted_server(
            Path(self.tmp.name) / "render.db", host="0.0.0.0", port=0,
            allow_public_bind=True)
        try:
            self.assertGreater(server.server_port, 0)
        finally:
            server.server_close()

    def test_remote_cli_and_offline_export_verifier(self):
        evidence_file = Path(self.tmp.name) / "evidence.json"
        evidence_file.write_text(json.dumps(evidence_payload()), encoding="utf-8")
        environment = {**os.environ, "PROOFPRESS_TOKEN": self.agent["token"]}
        submitted = subprocess.run([
            sys.executable, str(ROOT / "proofpress_remote.py"),
            "--base-url", self.base_url, "submit-evidence", str(evidence_file),
            "--idempotency-key", "cli-evidence-1"],
            text=True, capture_output=True, env=environment, check=True)
        self.assertTrue(json.loads(submitted.stdout)["evidence"])

        from proofpress_event_store import SQLiteEventStore
        bundle = SQLiteEventStore(
            self.server.proofpress_control.database,
            self.owner["workspace_id"]).export_bundle()
        export_file = Path(self.tmp.name) / "export.json"
        export_file.write_text(json.dumps(bundle), encoding="utf-8")
        verified = subprocess.run([
            sys.executable, str(ROOT / "proofpress_hosted_service.py"),
            "verify-export", str(export_file)], text=True, capture_output=True,
            check=True)
        self.assertTrue(json.loads(verified.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()

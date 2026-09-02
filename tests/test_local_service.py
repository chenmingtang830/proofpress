import http.client
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "verified-knowledge-ledger" / "demo.otlp.json"


class LocalServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"],
                       cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"],
                       cwd=self.repo, check=True)
        sys.path.insert(0, str(ROOT))
        from proofpress.transports import http as proofpress_service
        self.service = proofpress_service
        self.previous = Path.cwd()
        os.chdir(self.repo)
        self.token = "test-local-token-0001"
        self.server = self.service.create_local_server(
            self.repo, self.token, port=0, max_request_bytes=512)
        self.thread = threading.Thread(target=self.server.serve_forever,
                                       daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join()
        os.chdir(self.previous)
        self.tmp.cleanup()

    def request(self, method, path, value=None, token=None, headers=None):
        connection = http.client.HTTPConnection(
            "127.0.0.1", self.server.server_port, timeout=5)
        body = None if value is None else json.dumps(value)
        request_headers = dict(headers or {})
        if value is not None:
            request_headers.setdefault("Content-Type", "application/json")
        if token is not None:
            request_headers["Authorization"] = "Bearer " + token
        connection.request(method, path, body=body, headers=request_headers)
        response = connection.getresponse()
        payload = json.loads(response.read())
        connection.close()
        return response.status, payload

    def test_health_readiness_auth_and_capabilities(self):
        status, health = self.request("GET", "/healthz")
        self.assertEqual(status, 200); self.assertEqual(health["status"], "ok")
        status, ready = self.request("GET", "/readyz")
        self.assertEqual(status, 200); self.assertEqual(ready["status"], "ready")
        self.assertEqual(Path(ready["workspace"]).resolve(), self.repo.resolve())

        status, unauthorized = self.request("GET", "/v1/capabilities")
        self.assertEqual(status, 401); self.assertEqual(unauthorized["error"], "unauthorized")
        status, envelope = self.request(
            "GET", "/v1/capabilities", token=self.token)
        self.assertEqual(status, 200); self.assertTrue(envelope["ok"])
        self.assertEqual(envelope["result"]["request_schema"],
                         "proofpress/local-operation/v1alpha1")
        self.assertEqual(envelope["result"]["transport"], "localhost_http")
        self.assertNotIn("localhost_http", envelope["result"]["not_available"])

    def test_operation_endpoint_preserves_contract_and_replay(self):
        request = {
            "schema_version": "proofpress/local-operation/v1alpha1",
            "operation": "evidence.import",
            "parameters": {"path": str(FIXTURE)},
            "idempotency_key": "service-import-001",
        }
        status, first = self.request(
            "POST", "/v1/operations", request, self.token)
        self.assertEqual(status, 200); self.assertTrue(first["ok"])
        status, replay = self.request(
            "POST", "/v1/operations", request, self.token)
        self.assertEqual(status, 200); self.assertTrue(replay["idempotent_replay"])
        self.assertEqual(first["result"], replay["result"])

        conflict_request = dict(request)
        conflict_request["parameters"] = {"path": str(self.repo / "other.json")}
        status, conflict = self.request(
            "POST", "/v1/operations", conflict_request, self.token)
        self.assertEqual(status, 409)
        self.assertEqual(conflict["error"]["code"], "idempotency_conflict")

    def test_request_limits_content_type_and_loopback_boundary(self):
        status, response = self.request(
            "POST", "/v1/operations", {"padding": "x" * 600}, self.token)
        self.assertEqual(status, 413); self.assertEqual(response["error"], "request_too_large")
        status, response = self.request(
            "POST", "/v1/operations", None, self.token,
            {"Content-Type": "text/plain", "Content-Length": "0"})
        self.assertEqual(status, 415)
        with self.assertRaisesRegex(ValueError, "only supports loopback"):
            self.service.create_local_server(
                self.repo, self.token, host="0.0.0.0", port=0)


if __name__ == "__main__":
    unittest.main()

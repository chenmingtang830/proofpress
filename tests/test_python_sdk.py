import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "verified-knowledge-ledger" / "demo.otlp.json"
CONFORMANCE = ROOT / "tests" / "fixtures" / "local_operation_conformance_v1alpha1.json"


class PythonSDKTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"],
                       cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"],
                       cwd=self.repo, check=True)
        sys.path.insert(0, str(ROOT))
        import proofpress_sdk
        import proofpress_service
        self.sdk = proofpress_sdk
        self.previous = Path.cwd()
        os.chdir(self.repo)
        self.token = "sdk-local-token-0001"
        self.server = proofpress_service.create_local_server(
            self.repo, self.token, port=0)
        self.thread = threading.Thread(target=self.server.serve_forever,
                                       daemon=True)
        self.thread.start()
        self.direct = self.sdk.ProofpressClient.in_process(self.repo)
        self.http = self.sdk.ProofpressClient.localhost(
            f"http://127.0.0.1:{self.server.server_port}", self.token)

    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join()
        os.chdir(self.previous)
        self.tmp.cleanup()

    def test_in_process_and_http_share_one_typed_lifecycle(self):
        self.assertEqual(self.direct.capabilities()["transport"], "in_process")
        self.assertEqual(self.http.capabilities()["transport"], "localhost_http")

        imported = self.direct.import_evidence(
            FIXTURE, idempotency_key="sdk-import-001")
        proposed = self.http.propose_conclusion(
            "The SDK proposal remains governed until Human Approval",
            [imported["evidence"][0]], "sdk-test", "agent:sdk",
            idempotency_key="sdk-propose-001")
        conclusion_id = proposed["conclusion"]["id"]
        evaluation = self.direct.evaluate_conclusion(conclusion_id)
        self.assertTrue(evaluation["eligible"])
        reviewed = self.http.review_conclusion(
            conclusion_id, "admit", "human:reviewer",
            review_request_id="sdk-review-001",
            idempotency_key="sdk-review-envelope-001")
        self.assertEqual(reviewed["result"]["type"], "conclusion_admitted")

        direct_context = self.direct.context(scope="sdk-test", actor="agent:next")
        http_context = self.http.context(scope="sdk-test", actor="agent:next")
        self.assertEqual(http_context, direct_context)
        self.assertEqual(direct_context["knowledge"][0]["id"], conclusion_id)

    def test_sdk_exposes_stable_errors_and_replay_metadata(self):
        first = self.http.import_evidence(
            FIXTURE, idempotency_key="sdk-replay-001")
        replay = self.http.execute_raw(
            "evidence.import", {"path": str(FIXTURE)},
            idempotency_key="sdk-replay-001")
        self.assertTrue(replay["idempotent_replay"])
        self.assertEqual(replay["result"], first)

        with self.assertRaises(self.sdk.ProofpressError) as raised:
            self.http.execute(
                "evidence.import", {"path": str(self.repo / "different.json")},
                idempotency_key="sdk-replay-001")
        self.assertEqual(raised.exception.code, "idempotency_conflict")
        self.assertFalse(raised.exception.retryable)

        with self.assertRaises(self.sdk.ProofpressError) as missing:
            self.direct.evaluate_conclusion("missing")
        self.assertEqual(missing.exception.code, "operation_rejected")

    def test_sdk_rejects_unsafe_transport_and_workspace_ambiguity(self):
        with self.assertRaisesRegex(ValueError, "loopback"):
            self.sdk.ProofpressClient.localhost(
                "http://0.0.0.0:7332", self.token)
        os.chdir(self.previous)
        try:
            with self.assertRaises(self.sdk.ProofpressTransportError) as raised:
                self.direct.capabilities()
            self.assertEqual(raised.exception.code, "workspace_mismatch")
        finally:
            os.chdir(self.repo)

        for url in ("http://api.example.test", "https://", "https://u:p@example.test"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                self.sdk.ProofpressClient.remote(url, self.token)
        remote = self.sdk.ProofpressClient.remote(
            "https://proofpress.example.test", self.token)
        self.assertIsInstance(remote.transport, self.sdk.RemoteHttpTransport)

    def test_both_sdk_transports_pass_frozen_validation_vectors(self):
        fixture = __import__("json").loads(CONFORMANCE.read_text(encoding="utf-8"))
        for client in (self.direct, self.http):
            for vector in fixture["vectors"]:
                with self.subTest(transport=type(client.transport).__name__,
                                  vector=vector["name"]):
                    envelope = client.transport.execute(vector["request"])
                    self.assertEqual(envelope["ok"], vector["expect"]["ok"])
                    if not envelope["ok"]:
                        self.assertEqual(envelope["error"]["code"],
                                         vector["expect"]["error_code"])

    def test_python_project_declares_the_sdk_and_supported_runtime(self):
        import tomllib
        project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(project["project"]["name"], "proofpress-local")
        self.assertEqual(project["project"]["requires-python"], ">=3.11")
        self.assertIn("proofpress_sdk", project["tool"]["setuptools"]["py-modules"])
        self.assertIn("proofpress_service", project["tool"]["setuptools"]["py-modules"])
        self.assertIn("proofpress_mcp", project["tool"]["setuptools"]["py-modules"])
        self.assertIn("proofpress_experiment", project["tool"]["setuptools"]["py-modules"])
        self.assertIn("*.html", project["tool"]["setuptools"]["package-data"]["proofpress_self_hosted"])
        self.assertEqual(project["project"]["scripts"]["proofpress-mcp"],
                         "proofpress_mcp:main")
        self.assertIn("mcp>=2,<3", project["project"]["optional-dependencies"]["mcp"])


if __name__ == "__main__":
    unittest.main()

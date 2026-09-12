import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "external_experiment_v0.json"
sys.path.insert(0, str(ROOT / "src"))

from proofpress import ProofpressClient, ProofpressError
from proofpress.hosted import HostedControlPlane
from proofpress.kernel import operations as kernel_ops
from proofpress.transports import http as local_http


class ExternalExperimentIngestionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"],
                       cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"],
                       cwd=self.repo, check=True)
        self.previous = Path.cwd()
        os.chdir(self.repo)
        self.client = ProofpressClient.in_process(self.repo)
        self.run = self.client.start_run(
            "Evaluate an external RL run", actor="agent:researcher")

    def tearDown(self):
        os.chdir(self.previous)
        self.tmp.cleanup()

    def manifest(self):
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        payload["binding"]["proofpress_run_id"] = self.run["id"]
        return payload

    def test_ingests_bounded_evidence_and_preserves_capture_limits(self):
        result = self.client.ingest_external_experiment(
            self.manifest(), actor="agent:researcher")
        self.assertEqual(result["schema_version"],
                         "proofpress/external-experiment-ingestion/v0")
        self.assertEqual(result["coverage"], "partial")
        self.assertEqual(result["known_omissions"], ["raw_trajectories"])
        self.assertEqual(result["authority"],
                         "evidence_only_human_approval_required")
        evidence_id = result["imported_evidence"][0]
        row = kernel_ops.v2_projection()["evidence"][evidence_id]
        self.assertEqual(row["run_id"], self.run["id"])
        self.assertEqual(row["retrieval_receipt"]["locator"], {
            "kind": "json_pointer", "value": "/metrics/pass_rate"})
        external = row["external_experiment"]
        self.assertEqual(external["source"]["system"], "example-rl-vendor")
        self.assertEqual(external["source"]["provenance_status"],
                         "importer_attested")
        self.assertEqual(external["ingested_by"], "agent:researcher")
        self.assertNotIn("source_content", row)
        self.assertNotIn("source_content", row["retrieval_receipt"]["source"])
        detail = self.client.get_run(self.run["id"], actor="agent:researcher")
        self.assertEqual(detail["external_evidence"][0]["id"], evidence_id)

        proposed = self.client.propose_claim(
            "Pass rate was 0.74 on evaluation set v4.", [evidence_id],
            "research-program-7", "agent:researcher", title="External pass rate")
        self.client.evaluate_claim(proposed["claim"]["id"])
        self.assertEqual(
            self.client.context(scope="research-program-7")["governed_context"], [])

    def test_same_manifest_is_idempotent_and_changed_content_is_new_history(self):
        first = self.client.ingest_external_experiment(
            self.manifest(), actor="agent:researcher")
        event_count = len(kernel_ops.v2_events())
        replay = self.client.ingest_external_experiment(
            self.manifest(), actor="agent:researcher")
        self.assertTrue(replay["idempotent"])
        self.assertEqual(replay["events_added"], 0)
        self.assertEqual(replay["imported_evidence"], first["imported_evidence"])
        self.assertEqual(len(kernel_ops.v2_events()), event_count)

        changed = self.manifest()
        changed["evidence"][0]["source_digest"] = "sha256:" + "d" * 64
        revision = self.client.ingest_external_experiment(
            changed, actor="agent:researcher")
        self.assertNotEqual(revision["imported_evidence"],
                            first["imported_evidence"])
        self.assertGreater(revision["events_added"], 0)

    def test_validation_fails_closed_before_any_partial_append(self):
        payload = self.manifest()
        payload["evidence"].append(copy.deepcopy(payload["evidence"][0]))
        payload["evidence"][1]["source_digest"] = "not-a-digest"
        before = len(kernel_ops.v2_events())
        with self.assertRaisesRegex(ProofpressError, "sha256 digest"):
            self.client.ingest_external_experiment(
                payload, actor="agent:researcher")
        self.assertEqual(len(kernel_ops.v2_events()), before)

        partial_without_omissions = self.manifest()
        partial_without_omissions["source"]["known_omissions"] = []
        with self.assertRaisesRegex(ProofpressError, "requires known omissions"):
            self.client.ingest_external_experiment(
                partial_without_omissions, actor="agent:researcher")

        bad_pointer = self.manifest()
        bad_pointer["evidence"][0]["locator"]["value"] = "/metrics/~bad"
        with self.assertRaisesRegex(ProofpressError, "RFC 6901"):
            self.client.ingest_external_experiment(
                bad_pointer, actor="agent:researcher")

    def test_wrong_actor_cross_run_and_secret_shaped_fields_are_rejected(self):
        with self.assertRaisesRegex(ProofpressError, "only the run actor"):
            self.client.ingest_external_experiment(
                self.manifest(), actor="agent:other")

        missing_run = self.manifest()
        missing_run["binding"]["proofpress_run_id"] = "run_other_workspace"
        with self.assertRaisesRegex(ProofpressError, "run not found"):
            self.client.ingest_external_experiment(
                missing_run, actor="agent:researcher")

        secret_field = self.manifest()
        secret_field["source"]["api_key"] = "must-not-be-stored"
        with self.assertRaisesRegex(ProofpressError, "unknown.*api_key"):
            self.client.ingest_external_experiment(
                secret_field, actor="agent:researcher")
        self.assertNotIn("must-not-be-stored", json.dumps(kernel_ops.v2_events()))

        credential_uri = self.manifest()
        credential_uri["evidence"][0]["source_uri"] = (
            "https://provider.example/result?access_token=must-not-be-stored")
        with self.assertRaisesRegex(ProofpressError, "credential query"):
            self.client.ingest_external_experiment(
                credential_uri, actor="agent:researcher")
        self.assertNotIn("must-not-be-stored", json.dumps(kernel_ops.v2_events()))

    def test_cli_uses_the_same_operation_contract(self):
        manifest = self.repo / "external-run.json"
        manifest.write_text(json.dumps(self.manifest()), encoding="utf-8")
        env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
        result = subprocess.run([
            sys.executable, "-m", "proofpress.cli", "experiment", "--actor",
            "agent:researcher", "ingest", str(manifest),
            "--idempotency-key", "external-cli-1",
        ], cwd=self.repo, env=env, text=True, capture_output=True, check=True)
        output = json.loads(result.stdout)
        self.assertEqual(output["external_run_id"], "vendor-run-42")
        self.assertEqual(len(output["imported_evidence"]), 1)


class HostedExternalExperimentIngestionTests(unittest.TestCase):
    def test_hosted_identity_is_server_derived_and_workspace_isolated(self):
        with tempfile.TemporaryDirectory() as tmp:
            control = HostedControlPlane(Path(tmp) / "hosted.db")
            owner = control.bootstrap("workspace-a", "human:owner", "Owner")
            agent = control.issue_agent_credential(
                owner["token"], "agent:researcher", "research agent")

            def operation(name, parameters, key=None):
                row = {"schema_version": kernel_ops.LOCAL_OPERATION_SCHEMA,
                       "operation": name, "parameters": parameters}
                if key:
                    row["idempotency_key"] = key
                return row

            started = control.execute(agent["token"], operation(
                "run.start", {"purpose": "Hosted external run",
                              "actor": "agent:spoofed", "metadata": None},
                "external-start"))
            self.assertTrue(started["ok"])
            payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
            payload["binding"]["proofpress_run_id"] = started["result"]["id"]
            ingested = control.execute(agent["token"], operation(
                "experiment.ingest", {"payload": payload,
                                      "actor": "agent:spoofed"},
                "external-ingest"))
            self.assertTrue(ingested["ok"])
            evidence_id = ingested["result"]["imported_evidence"][0]
            detail = control.execute(agent["token"], operation(
                "run.get", {"run_id": started["result"]["id"],
                            "actor": "agent:spoofed"}))
            evidence = next(row for row in detail["result"]["external_evidence"]
                            if row["id"] == evidence_id)
            self.assertEqual(evidence["external_experiment"]["ingested_by"],
                             "agent:researcher")

    def test_local_http_uses_the_same_external_ingestion_operation(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"],
                           cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"],
                           cwd=repo, check=True)
            previous = Path.cwd()
            server = None
            thread = None
            try:
                os.chdir(repo)
                token = "local-experiment-token-0001"
                server = local_http.create_local_server(repo, token, port=0)
                thread = threading.Thread(target=server.serve_forever,
                                          daemon=True)
                thread.start()
                client = ProofpressClient.localhost(
                    f"http://127.0.0.1:{server.server_port}", token)
                run = client.start_run("HTTP external run",
                                       actor="agent:researcher")
                payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
                payload["binding"]["proofpress_run_id"] = run["id"]
                result = client.ingest_external_experiment(
                    payload, actor="agent:researcher",
                    idempotency_key="http-external-ingest")
                self.assertEqual(result["external_run_id"], "vendor-run-42")
                self.assertEqual(len(result["imported_evidence"]), 1)
            finally:
                if server is not None:
                    server.shutdown()
                    server.server_close()
                if thread is not None:
                    thread.join()
                os.chdir(previous)


if __name__ == "__main__":
    unittest.main()

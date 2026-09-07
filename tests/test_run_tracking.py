import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import unittest

from proofpress import client as sdk
from proofpress.hosted.control_plane import HostedControlPlane


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "verified-knowledge-ledger" / "demo.otlp.json"


class RunTrackingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.repo, check=True)
        self.previous = Path.cwd(); os.chdir(self.repo)
        self.client = sdk.ProofpressClient.in_process(self.repo)
        imported = self.client.import_evidence(FIXTURE)
        self.evidence = imported["evidence"][0]
        proposed = self.client.propose_claim(
            "This synthetic fixture is safe for task-run contract tests.",
            [self.evidence], "run-tests", "agent:proposer", title="Synthetic fixture boundary")
        self.claim = proposed["claim"]
        self.client.evaluate_claim(self.claim["id"])
        self.client.review_claim(self.claim["id"], "admit", "human:test-owner")

    def tearDown(self):
        os.chdir(self.previous); self.tmp.cleanup()

    def test_complete_chain_freezes_context_and_requires_declared_reliance(self):
        run = self.client.start_run("Implement a safe fixture", actor="agent:runner",
                                    idempotency_key="run-start-1")
        receipt = self.client.capture_context(
            run["id"], actor="agent:runner", scope="run-tests",
            task="safe fixture", idempotency_key="capture-1")
        self.assertEqual(receipt["claims"][0]["claim_id"], self.claim["id"])
        self.assertEqual(receipt["claims"][0]["claim_digest"], self.claim["digest"])
        self.assertIn("admission", receipt["claims"][0])
        self.assertEqual(self.client.get_run(run["id"], actor="agent:runner")["reliances"], [])

        with self.assertRaisesRegex(sdk.ProofpressError, "not returned"):
            self.client.record_reliance(run["id"], receipt["id"], self.claim["id"],
                                        "sha256:" + "0" * 64, "invalid version",
                                        actor="agent:runner")
        reliance = self.client.record_reliance(
            run["id"], receipt["id"], self.claim["id"], self.claim["digest"],
            "Use only the recorded fixture boundary", actor="agent:runner",
            idempotency_key="rely-1")
        output = self.client.record_output(
            run["id"], "repo://proofpress/tests/test_run_tracking.py",
            "sha256:" + hashlib.sha256(b"synthetic output v1").hexdigest(),
            actor="agent:runner", summary="Synthetic contract output",
            reliance_ids=[reliance["id"]], idempotency_key="output-1")
        self.client.finish_run(run["id"], "completed", actor="agent:runner",
                               summary="Contract path completed", idempotency_key="finish-1")
        observation = self.client.record_observation(
            run["id"], "test", "python unittest",
            "The synthetic end-to-end assertions passed.", actor="agent:observer",
            output_ids=[output["id"]], idempotency_key="observe-1")
        detail = self.client.get_run(run["id"], actor="human:owner")
        self.assertEqual(detail["status"], "completed")
        self.assertEqual(detail["observations"][0]["id"], observation["id"])
        self.assertNotIn("score", json.dumps(detail))

        replay = self.client.start_run("Implement a safe fixture", actor="agent:runner",
                                       idempotency_key="run-start-1")
        self.assertEqual(replay["id"], run["id"])
        listing = self.client.list_runs(actor="human:owner")
        self.assertEqual(listing["runs"][0]["counts"], {
            "retrieved": 1, "relied_on": 1, "outputs": 1, "observations": 1})

    def test_receipts_and_output_hashes_remain_distinct_across_runs(self):
        first = self.client.start_run("First safe run", actor="agent:runner")
        first_receipt = self.client.capture_context(first["id"], actor="agent:runner", scope="run-tests")
        first_output = self.client.record_output(first["id"], "repo://result.txt",
                                                  "sha256:" + "1" * 64,
                                                  actor="agent:runner")
        second = self.client.start_run("Second safe run", actor="agent:runner")
        second_receipt = self.client.capture_context(second["id"], actor="agent:runner", scope="run-tests")
        second_output = self.client.record_output(second["id"], "repo://result.txt",
                                                   "sha256:" + "2" * 64,
                                                   actor="agent:runner")
        self.assertNotEqual(first_receipt["id"], second_receipt["id"])
        self.assertEqual(first_receipt["claims"], second_receipt["claims"])
        self.assertNotEqual(first_output["content_digest"], second_output["content_digest"])
        self.assertEqual(self.client.get_run(first["id"])["outputs"][0]["content_digest"],
                         "sha256:" + "1" * 64)

    def test_cross_run_references_and_wrong_actor_fail_closed(self):
        first = self.client.start_run("First", actor="agent:a")
        second = self.client.start_run("Second", actor="agent:b")
        receipt = self.client.capture_context(first["id"], actor="agent:a", scope="run-tests")
        with self.assertRaisesRegex(sdk.ProofpressError, "does not belong"):
            self.client.record_reliance(second["id"], receipt["id"], self.claim["id"],
                                        self.claim["digest"], "cross-run", actor="agent:b")
        with self.assertRaisesRegex(sdk.ProofpressError, "only the run actor"):
            self.client.finish_run(first["id"], "aborted", actor="agent:b")


class HostedRunPermissionTests(unittest.TestCase):
    @staticmethod
    def request(operation, parameters, key=None):
        row = {"schema_version": "proofpress/local-operation/v1alpha1",
               "operation": operation, "parameters": parameters}
        if key: row["idempotency_key"] = key
        return row

    def test_hosted_actor_is_server_derived_for_run_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            control = HostedControlPlane(Path(tmp) / "hosted.db")
            owner = control.bootstrap("workspace-a", "human:owner", "Owner")["token"]
            agent = control.issue_agent_credential(owner, "agent:bound", "run agent")["token"]
            started = control.execute(agent, self.request(
                "run.start", {"purpose": "Hosted run", "actor": "agent:spoofed",
                              "metadata": None}, "hosted-run-1"))
            self.assertTrue(started["ok"])
            self.assertEqual(started["result"]["actor"], "agent:bound")
            listed = control.execute(agent, self.request(
                "run.list", {"actor": "agent:spoofed", "status": None, "limit": 50}))
            self.assertEqual(listed["result"]["runs"][0]["actor"], "agent:bound")

    def test_existing_restricted_credential_is_not_expanded_by_migration(self):
        with tempfile.TemporaryDirectory() as tmp:
            control = HostedControlPlane(Path(tmp) / "hosted.db")
            bootstrap = control.bootstrap("workspace-a", "human:owner", "Owner")
            owner = bootstrap["token"]
            issued = control.issue_agent_credential(
                owner, "agent:legacy", "restricted", permissions={"context.get"})
            control = HostedControlPlane(Path(tmp) / "hosted.db")
            forbidden = control.execute(issued["token"], self.request("run.list", {}))
            self.assertFalse(forbidden["ok"])
            self.assertEqual(forbidden["error"]["code"], "operation_forbidden")
            with sqlite3.connect(Path(tmp) / "hosted.db") as connection:
                permissions = json.loads(connection.execute(
                    "SELECT permissions_json FROM hosted_credentials WHERE credential_id=?",
                    (issued["credential_id"],)).fetchone()[0])
            self.assertEqual(permissions, ["context.get"])


if __name__ == "__main__":
    unittest.main()

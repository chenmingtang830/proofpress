"""Durable pilot execution records preserve retry and admission boundaries."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from proofpress.hosted import execution
from proofpress.execution import external_trigger_key
from proofpress.hosted.control_plane import HostedControlPlane, HostedAuthError
from proofpress.kernel.events import SQLiteEventStore
from test_hosted_authority import evidence_payload, operation


class HostedExecutionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.database = Path(self.temp.name) / "hosted.db"
        self.control = HostedControlPlane(self.database)
        self.owner = self.control.bootstrap("workspace:one", "human:owner")["token"]
        self.agent = self.control.issue_agent_credential(
            self.owner, "agent:pilot", "Pilot agent")["token"]

    def test_external_trigger_key_is_stable_and_versions_corrections(self):
        first = external_trigger_key("experiment.ingest", "tracker", "event-7", "v1")
        self.assertEqual(first, external_trigger_key(
            "experiment.ingest", "tracker", "event-7", "v1"))
        self.assertNotEqual(first, external_trigger_key(
            "experiment.ingest", "tracker", "event-7", "v2"))
        self.assertLessEqual(len(first), 128)
        self.assertNotIn("event-7", first)

    def test_crash_after_governed_write_retries_without_duplicate(self):
        request = operation("evidence.submit", {"payload": evidence_payload()}, "trigger-1")
        with patch("proofpress.hosted.control_plane.execution.finish",
                   side_effect=SystemExit("simulated crash after kernel commit")):
            with self.assertRaises(SystemExit):
                self.control.execute(self.agent, request)
        store = SQLiteEventStore(self.database, "workspace:one", "agent:pilot")
        prior_events = store.list_events()
        self.assertTrue(prior_events)
        with self.control._db() as connection:
            row = connection.execute("SELECT state FROM hosted_executions").fetchone()
            self.assertEqual(row["state"], "running")
            execution.resume(connection)
        self.assertEqual(self.control.list_executions(self.owner)[0]["state"], "interrupted")

        restarted = HostedControlPlane(self.database)
        repeated = restarted.execute(self.agent, request)
        self.assertTrue(repeated["ok"])
        self.assertTrue(repeated["idempotent_replay"])
        self.assertEqual(store.list_events(), prior_events)
        record = restarted.list_executions(self.owner)[0]
        self.assertEqual(record["state"], "succeeded")
        self.assertEqual([row["state"] for row in record["attempts"]],
                         ["interrupted", "succeeded"])
        self.assertTrue(record["attempts"][-1]["idempotent_replay"])
        self.assertEqual(record["output_refs"]["evidence_ids"],
                         repeated["result"]["imported_evidence"])

    def test_terminal_failure_is_inspectable_and_requires_new_key(self):
        payload = {**evidence_payload(), "schema_version": "unsupported",
                   "private_note": "do-not-store-this"}
        request = operation("evidence.submit", {"payload": payload}, "bad-trigger")
        failed = self.control.execute(self.agent, request)
        self.assertFalse(failed["ok"])
        record = self.control.list_executions(self.owner)[0]
        self.assertEqual(record["state"], "terminal_failed")
        self.assertEqual(record["attempts"][0]["state"], "terminal_failed")
        self.assertNotIn("do-not-store-this", json.dumps(record))
        self.assertEqual(self.control.execute(self.agent, request)["error"]["code"],
                         "execution_terminal")
        corrected = self.control.execute(
            self.agent, operation("evidence.submit", {"payload": evidence_payload()},
                                  "corrected-trigger"))
        self.assertTrue(corrected["ok"])
        activity = self.control.list_activity(self.owner)
        self.assertTrue(any(row.get("kind") == "workflow_execution" for row in activity))

    def test_transient_failure_is_explicitly_retryable_with_same_key(self):
        request = operation("evidence.submit", {"payload": evidence_payload()}, "transient-1")
        with patch("proofpress.hosted.control_plane.kernel_ops.execute_local_operation",
                   return_value={"ok": False, "error": {"code": "operation_io_error"}}):
            failed = self.control.execute(self.agent, request)
        self.assertFalse(failed["ok"])
        self.assertEqual(self.control.list_executions(self.owner)[0]["state"],
                         "retryable_failed")
        succeeded = self.control.execute(self.agent, request)
        self.assertTrue(succeeded["ok"])
        self.assertEqual([row["state"] for row in
                          self.control.list_executions(self.owner)[0]["attempts"]],
                         ["retryable_failed", "succeeded"])

    def test_evidence_and_verification_link_to_owner_admission(self):
        submitted = self.control.execute(
            self.agent, operation("evidence.submit", {"payload": evidence_payload()},
                                  "source-v1"))
        evidence_id = submitted["result"]["imported_evidence"][0]
        proposed = self.control.execute(self.agent, operation("claim.propose", {
            "title": "Bounded pilot claim", "statement": "The liability cap is one year of fees.",
            "evidence_refs": [evidence_id], "scope": "pilot", "proposer": "spoofed",
        }, "proposal-v1"))
        claim_id = proposed["result"]["claim"]["id"]
        checked = self.control.execute(self.agent, operation(
            "claim.evaluate", {"claim_id": claim_id}, "verify-v1"))
        self.assertTrue(checked["ok"])
        reviewed = self.control.execute(self.owner, operation("claim.review", {
            "claim_id": claim_id, "decision": "admit", "reviewer": "spoofed",
            "request_id": "human-review-v1",
        }))
        self.assertTrue(reviewed["ok"])
        records = self.control.list_executions(self.owner)
        self.assertEqual({row["operation"] for row in records},
                         {"evidence.submit", "claim.evaluate"})
        for row in records:
            self.assertEqual(row["linked_claims"][0]["claim_id"], claim_id)
            self.assertEqual(row["linked_claims"][0]["state"], "admitted")
            self.assertEqual(row["linked_claims"][0]["authority_basis"], "human_review")
        self.assertEqual(next(row for row in records if row["operation"] == "claim.evaluate")
                         ["output_refs"]["evaluation_event_id"],
                         checked["result"]["event_id"])
        with self.assertRaises(HostedAuthError):
            self.control.list_executions(self.agent)

    def test_external_experiment_records_adapter_and_run_binding(self):
        started = self.control.execute(self.agent, operation("run.start", {
            "purpose": "Pilot experiment", "actor": "spoofed", "metadata": None,
        }, "run-start-1"))
        self.assertTrue(started["ok"])
        fixture = Path(__file__).parent / "fixtures/external_experiment_v0.json"
        payload = json.loads(fixture.read_text(encoding="utf-8"))
        payload["binding"]["proofpress_run_id"] = started["result"]["id"]
        ingested = self.control.execute(self.agent, operation(
            "experiment.ingest", {"payload": payload, "actor": "spoofed"},
            "external-event-v1"))
        self.assertTrue(ingested["ok"])
        record = self.control.list_executions(self.owner)[0]
        self.assertEqual(record["operation"], "experiment.ingest")
        self.assertEqual(record["versions"]["adapter"], payload["adapter"]["name"])
        self.assertEqual(record["versions"]["adapter_version"],
                         payload["adapter"]["version"])
        self.assertEqual(record["input_refs"]["run_id"], started["result"]["id"])
        self.assertEqual(record["output_refs"]["evidence_ids"],
                         ingested["result"]["imported_evidence"])

    def test_execution_keys_are_principal_and_deployment_scoped(self):
        request = operation("evidence.submit", {"payload": evidence_payload()}, "same-key")
        self.assertTrue(self.control.execute(self.agent, request)["ok"])
        other = self.control.issue_agent_credential(
            self.owner, "agent:other", "Other agent")["token"]
        self.assertTrue(self.control.execute(other, request)["ok"])
        second = HostedControlPlane(Path(self.temp.name) / "second.db")
        second_owner = second.bootstrap("workspace:two", "human:second")["token"]
        second_agent = second.issue_agent_credential(
            second_owner, "agent:pilot", "Second pilot")["token"]
        self.assertTrue(second.execute(second_agent, request)["ok"])
        self.assertEqual(len(self.control.list_executions(self.owner)), 2)
        self.assertEqual(len(second.list_executions(second_owner)), 1)

    def test_same_key_rejects_changed_payload_or_version(self):
        request = operation("evidence.submit", {"payload": evidence_payload()}, "stable-1")
        self.assertTrue(self.control.execute(self.agent, request)["ok"])
        changed = operation("evidence.submit", {
            "payload": {**evidence_payload(), "extra": "changed"}}, "stable-1")
        self.assertEqual(self.control.execute(self.agent, changed)["error"]["code"],
                         "idempotency_conflict")
        with self.control._db() as connection:
            record = connection.execute("SELECT * FROM hosted_executions").fetchone()
            attempt, problem = execution.begin(
                connection, workspace_id=record["workspace_id"],
                principal_id=record["principal_id"],
                idempotency_key=record["idempotency_key"],
                operation=record["operation"],
                fingerprint=record["request_fingerprint"],
                versions={"schema_version": "changed"}, input_refs={})
        self.assertIsNone(attempt)
        self.assertEqual(problem, "execution_version_conflict")


if __name__ == "__main__":
    unittest.main()

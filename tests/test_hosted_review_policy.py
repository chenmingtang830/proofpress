import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from cryptography.fernet import Fernet

from proofpress.hosted.control_plane import HostedControlPlane, HostedAuthError
from proofpress.kernel import operations as kernel
from proofpress.kernel.events import SQLiteEventStore, using_event_store
from test_hosted_authority import evidence_payload, operation


class ReviewPolicyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.control = HostedControlPlane(Path(self.tmp.name) / "test.db")
        self.owner = self.control.bootstrap("workspace:test", "human:owner")["token"]
        self.agent = self.control.issue_agent_credential(self.owner, "agent:codex", "Codex")["token"]
        self.settings = {"mode": "manual", "model": "deepseek/deepseek-v4-flash",
                         "provider": "openrouter", "endpoint": "", "criteria": "Escalate unsupported claims.",
                         "zdr": True, "rubric": "evidence-support/v1",
                         "external_consent": True, "require_judge": True}

    def proposal(self, label="A"):
        evidence = self.control.execute(self.agent, operation("evidence.submit", {"payload": evidence_payload()}))
        return self.control.execute(self.agent, operation("conclusion.propose", {
            "statement": label, "evidence_refs": evidence["result"]["evidence"], "scope": "test",
            "proposer": "agent:codex"}, "proposal-" + label))

    def test_owner_only_versioned_persistence_and_safe_public_config(self):
        with self.assertRaises(HostedAuthError):
            self.control.get_review_policy(self.agent)
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-not-a-real-key"}):
            with self.assertRaises(ValueError):
                self.control.save_review_policy(self.owner, {**self.settings, "external_consent": False}, 0)
            record = self.control.save_review_policy(self.owner, self.settings, 0)
        self.assertEqual(record["version"], 1)
        self.assertNotIn("command", json.dumps(record))
        self.assertNotIn("test-not-a-real-key", json.dumps(record))
        fresh = HostedControlPlane(self.control.database)
        self.assertEqual(fresh.get_review_policy(self.owner)["version"], 1)
        with self.assertRaises(HostedAuthError):
            fresh.save_review_policy(self.owner, self.settings, 0)
        other = HostedControlPlane(Path(self.tmp.name)/"other.db")
        owner = other.bootstrap("workspace:other", "human:other")["token"]
        self.assertEqual(other.get_review_policy(owner)["version"], 0)

    def test_workspace_api_key_is_encrypted_write_only_and_provider_bound(self):
        master = Fernet.generate_key().decode()
        provider_key = "sk-customer-private-1234"
        with patch.dict(os.environ, {"PROOFPRESS_SECRET_ENCRYPTION_KEY": master}, clear=False):
            record = self.control.save_review_policy(self.owner, self.settings, 0, provider_key)
            self.assertTrue(record["credential"]["configured"])
            self.assertEqual(record["credential"]["last_four"], "1234")
            self.assertNotIn(provider_key, json.dumps(record))
            with self.control._db() as connection:
                stored = connection.execute("SELECT ciphertext FROM hosted_provider_secrets").fetchone()[0]
            self.assertNotIn(provider_key.encode(), stored)
            self.assertEqual(self.control.get_review_policy(self.owner)["credential"]["last_four"], "1234")
            with self.assertRaisesRegex(ValueError, "API key for the selected provider"):
                self.control.save_review_policy(self.owner, {**self.settings, "provider": "openai", "model": "gpt-5"}, 1)

    def test_required_advice_cannot_be_bypassed_and_receipt_explains_it(self):
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test"}):
            self.control.save_review_policy(self.owner, self.settings, 0)
        cid = self.proposal()["result"]["conclusion"]["id"]
        self.control.execute(self.agent, operation("conclusion.evaluate", {"conclusion_id": cid}))
        denied = self.control.execute(self.owner, operation("conclusion.review", {"conclusion_id": cid, "decision": "admit", "reviewer": "human:owner"}))
        self.assertFalse(denied["ok"])
        receipt = self.control.execute(self.owner, operation("review.receipt", {"conclusion_id": cid}))["result"]
        self.assertTrue(receipt["review_policy"]["require_judge"])
        self.assertTrue(receipt["review_policy"]["checks_current"])
        self.assertFalse(receipt["review_policy"]["advice_current"])

    def test_semantic_feed_has_real_actors_and_reads_do_not_claim_use(self):
        cid = self.proposal()["result"]["conclusion"]["id"]
        self.control.execute(self.agent, operation("conclusion.evaluate", {"conclusion_id": cid}))
        self.control.execute(self.agent, operation("context.get", {"scope": "test"}))
        self.control.execute(self.owner, operation("context.get", {"scope": "test"}))
        rows = self.control.list_activity(self.owner)
        proposal = next(row for row in rows if row["kind"] == "conclusion_proposed")
        self.assertEqual(proposal["actor"], "agent:codex")
        evaluation = next(row for row in rows if row["kind"] == "policy_evaluated")
        self.assertEqual(evaluation["actor"], kernel.load_v2_policy()["verification"]["identity"])
        self.assertEqual(evaluation["initiator"], "agent:codex")
        reads = [row for row in rows if row["kind"] == "context_retrieved"]
        self.assertEqual(len(reads), 1)
        self.assertEqual(reads[0]["conclusion_ids"], [])
        self.assertIn("does not prove use", reads[0]["detail"])
        self.assertTrue(any(row["operation"] == "context.get" for row in self.control.list_audit(self.owner)))

    def test_automatic_jobs_deduplicate_and_never_admit(self):
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test"}):
            self.control.save_review_policy(self.owner, {**self.settings, "mode":"automatic"}, 0)
        with patch("proofpress.hosted.control_plane.threading.Thread"):
            first = self.proposal()
            self.proposal()
        with patch.object(kernel, "judge_v2", return_value={"recommendation":"accept"}) as judge:
            self.control.run_judge_jobs()
            self.control.run_judge_jobs()
            self.assertEqual(judge.call_count, 1)
        cid = first["result"]["conclusion"]["id"]
        receipt = self.control.execute(self.owner, operation("review.receipt", {"conclusion_id":cid}))["result"]
        self.assertEqual(receipt["state"], "needs_review")
        self.assertEqual(receipt["judge_job"]["state"], "completed")

    def test_activating_automatic_policy_enqueues_existing_candidates(self):
        cid = self.proposal("existing")["result"]["conclusion"]["id"]
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test"}), \
             patch("proofpress.hosted.control_plane.threading.Thread"):
            self.control.save_review_policy(self.owner, {**self.settings, "mode":"automatic"}, 0)
        with self.control._db() as connection:
            job = connection.execute("SELECT conclusion_id, state FROM hosted_judge_jobs").fetchone()
        self.assertEqual((job["conclusion_id"], job["state"]), (cid, "queued"))

    def test_failed_current_checks_are_blocked_out_of_owner_review(self):
        proposal = self.control.execute(self.agent, operation("conclusion.propose", {
            "statement": "Unsupported candidate", "evidence_refs": [], "scope": "test",
            "proposer": "agent:codex"}, "unsupported"))
        cid = proposal["result"]["conclusion"]["id"]
        self.control.execute(self.agent, operation("conclusion.evaluate", {"conclusion_id": cid}))
        receipt = self.control.execute(self.owner, operation("review.receipt", {"conclusion_id": cid}))["result"]
        graph = self.control.execute(self.owner, operation("graph.get", {}))["result"]
        self.assertEqual(receipt["state"], "blocked")
        self.assertEqual(next(row for row in graph["nodes"] if row["id"] == cid)["state"], "blocked")

    def test_failed_checks_skip_provider_and_restart_does_not_retry_running_job(self):
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test"}):
            self.control.save_review_policy(self.owner, {**self.settings, "mode":"automatic"}, 0)
        with patch("proofpress.hosted.control_plane.threading.Thread"):
            self.proposal()
        with patch.object(kernel, "evaluate_v2", return_value={"eligible":False}), patch.object(kernel,"judge_v2") as judge:
            self.control.run_judge_jobs()
            judge.assert_not_called()
        with self.control._db() as connection:
            self.assertEqual(connection.execute("SELECT state FROM hosted_judge_jobs").fetchone()[0], "blocked")
            connection.execute("UPDATE hosted_judge_jobs SET state='running'")
        with patch("proofpress.hosted.control_plane.threading.Thread"):
            self.control.resume_judge_jobs()
        with patch.object(kernel,"judge_v2") as judge:
            self.control.run_judge_jobs()
            judge.assert_not_called()

    def test_policy_override_is_scoped(self):
        before = kernel.load_v2_policy()
        changed = {**before, "id":"isolated"}
        with kernel.using_policy(changed):
            self.assertEqual(kernel.load_v2_policy()["id"], "isolated")
        self.assertEqual(kernel.load_v2_policy(), before)

import json
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from cryptography.fernet import Fernet

from proofpress.hosted import review_policy
from proofpress.hosted.control_plane import HostedControlPlane, HostedAuthError
from proofpress.hosted.review_policy import POLICY_AUTHORING_PROMPT, PROVIDERS
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
        return self.control.execute(self.agent, operation("claim.propose", {
            "title": label, "statement": label,
            "evidence_refs": evidence["result"]["evidence"], "scope": "test",
            "proposer": "agent:codex"}, "proposal-" + label))

    def test_agent_prompt_only_authors_criteria(self):
        self.assertIn('{"criteria":', POLICY_AUTHORING_PROMPT)
        self.assertIn("Do not choose a model or provider", POLICY_AUTHORING_PROMPT)
        self.assertNotIn("return only JSON with these fields: provider", POLICY_AUTHORING_PROMPT)

    def test_common_model_providers_are_available_individually(self):
        self.assertEqual(
            [PROVIDERS[key]["label"] for key in (
                "azure_openai", "amazon_bedrock", "google_gemini", "xai", "groq", "mistral")],
            ["Azure OpenAI", "Amazon Bedrock", "Google Gemini", "xAI", "Groq", "Mistral AI"],
        )
        self.assertTrue(PROVIDERS["azure_openai"]["endpoint_required"])
        self.assertTrue(PROVIDERS["azure_openai"]["editable_model"])
        self.assertTrue(PROVIDERS["amazon_bedrock"]["endpoint_required"])
        for key, provider in PROVIDERS.items():
            if key != "custom":
                self.assertIn(provider["default_model"], provider["models"])

    def test_tenant_specific_provider_endpoint_is_validated(self):
        azure = {**self.settings, "provider": "azure_openai", "model": "gpt-5", "endpoint": ""}
        with self.assertRaisesRegex(ValueError, "public HTTPS URL"):
            self.control.save_review_policy(self.owner, azure, 0, "azure-provider-key")
        bedrock = {**self.settings, "provider": "amazon_bedrock", "model": "openai.gpt-oss-120b-1:0",
                   "endpoint": "https://bedrock-runtime.us-east-1.amazonaws.com/openai/v1/chat/completions"}
        with patch.dict(os.environ, {"PROOFPRESS_SECRET_ENCRYPTION_KEY": Fernet.generate_key().decode()}, clear=False):
            record = self.control.save_review_policy(self.owner, bedrock, 0, "bedrock-provider-key")
        self.assertEqual(record["settings"]["provider"], "amazon_bedrock")

    def test_legacy_judge_job_column_migrates_without_losing_jobs(self):
        legacy_path = Path(self.tmp.name) / "legacy-judge-jobs.db"
        connection = sqlite3.connect(legacy_path)
        try:
            connection.execute("""
                CREATE TABLE hosted_judge_jobs (
                    job_id TEXT PRIMARY KEY, workspace_id TEXT NOT NULL,
                    conclusion_id TEXT NOT NULL, policy_digest TEXT NOT NULL,
                    requested_by TEXT NOT NULL, state TEXT NOT NULL,
                    created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
                    detail TEXT NOT NULL DEFAULT ''
                )
            """)
            connection.execute(
                "INSERT INTO hosted_judge_jobs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                ("job-1", "workspace:legacy", "clm-legacy", "policy", "agent:legacy",
                 "queued", "2026-09-06T00:00:00Z", "2026-09-06T00:00:00Z", ""),
            )
            connection.commit()
        finally:
            connection.close()

        migrated = HostedControlPlane(legacy_path)
        with migrated._db() as connection:
            columns = {row["name"] for row in connection.execute(
                "PRAGMA table_info(hosted_judge_jobs)")}
            job = connection.execute(
                "SELECT claim_id, state FROM hosted_judge_jobs WHERE job_id='job-1'").fetchone()
        self.assertIn("claim_id", columns)
        self.assertNotIn("conclusion_id", columns)
        self.assertEqual((job["claim_id"], job["state"]), ("clm-legacy", "queued"))
        owner = migrated.bootstrap("workspace:legacy", "human:owner")["token"]
        agent = migrated.issue_agent_credential(owner, "agent:codex", "Codex")["token"]
        proposal = migrated.execute(agent, operation("claim.propose", {
            "title": "Migration receipt compatibility",
            "statement": "Migration preserves receipt reads", "evidence_refs": [],
            "scope": "test", "proposer": "agent:codex"}, "legacy-migration"))
        self.assertTrue(proposal["ok"])
        receipt = migrated.execute(owner, operation("review.receipt", {
            "claim_id": proposal["result"]["claim"]["id"]}))
        self.assertTrue(receipt["ok"])

    def test_legacy_context_read_column_migrates_without_losing_activity(self):
        legacy_path = Path(self.tmp.name) / "legacy-context-reads.db"
        connection = sqlite3.connect(legacy_path)
        try:
            connection.execute("""
                CREATE TABLE hosted_context_reads (
                    read_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workspace_id TEXT NOT NULL, actor TEXT NOT NULL,
                    scope TEXT, conclusion_ids_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            connection.execute(
                "INSERT INTO hosted_context_reads(workspace_id,actor,scope,conclusion_ids_json,created_at) "
                "VALUES(?,?,?,?,?)",
                ("workspace:legacy", "agent:legacy", "legacy:scope",
                 json.dumps(["knw-legacy"]), "2026-09-06T00:00:00Z"),
            )
            connection.commit()
        finally:
            connection.close()

        migrated = HostedControlPlane(legacy_path)
        owner = migrated.bootstrap("workspace:legacy", "human:owner")["token"]
        with migrated._db() as connection:
            columns = {row["name"] for row in connection.execute(
                "PRAGMA table_info(hosted_context_reads)")}
        self.assertIn("claim_ids_json", columns)
        self.assertNotIn("conclusion_ids_json", columns)
        activity = migrated.list_activity(owner)
        read = next(row for row in activity if row["kind"] == "context_retrieved")
        self.assertEqual(read["claim_ids"], ["knw-legacy"])
        self.assertEqual(read["scope"], "legacy:scope")

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

    def test_deployment_key_is_reported_as_configured_without_exposing_it(self):
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "deployment-only-secret"}):
            record = self.control.get_review_policy(self.owner)
        self.assertTrue(record["credential"]["configured"])
        self.assertIsNone(record["credential"]["last_four"])
        self.assertNotIn("deployment-only-secret", json.dumps(record))

    def test_openrouter_deployment_key_cannot_cross_provider_boundary(self):
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "deployment-only-secret"}):
            switched = {**self.settings, "provider": "openai", "model": "gpt-5.4"}
            with self.assertRaisesRegex(ValueError, "API key for the selected provider"):
                self.control.save_review_policy(self.owner, switched, 0, delete_key=True)
            with self.control._db() as connection:
                self.assertIsNone(review_policy.credential(connection, "workspace:test", "openai"))
                self.assertFalse(review_policy.credential_status(
                    connection, "workspace:test", "openai")["configured"])

    def test_required_advice_cannot_be_bypassed_and_receipt_explains_it(self):
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test"}):
            self.control.save_review_policy(self.owner, self.settings, 0)
        cid = self.proposal()["result"]["claim"]["id"]
        self.control.execute(self.agent, operation("claim.evaluate", {"claim_id": cid}))
        denied = self.control.execute(self.owner, operation("claim.review", {"claim_id": cid, "decision": "admit", "reviewer": "human:owner"}))
        self.assertFalse(denied["ok"])
        receipt = self.control.execute(self.owner, operation("review.receipt", {"claim_id": cid}))["result"]
        self.assertTrue(receipt["review_policy"]["require_judge"])
        self.assertTrue(receipt["review_policy"]["checks_current"])
        self.assertFalse(receipt["review_policy"]["advice_current"])

    def test_semantic_feed_has_real_actors_and_reads_do_not_claim_use(self):
        cid = self.proposal()["result"]["claim"]["id"]
        self.control.execute(self.agent, operation("claim.evaluate", {"claim_id": cid}))
        self.control.execute(self.agent, operation("context.get", {"scope": "test"}))
        self.control.execute(self.owner, operation("context.get", {"scope": "test"}))
        rows = self.control.list_activity(self.owner)
        proposal = next(row for row in rows if row["kind"] == "claim_proposed")
        self.assertEqual(proposal["actor"], "agent:codex")
        evaluation = next(row for row in rows if row["kind"] == "policy_evaluated")
        self.assertEqual(evaluation["actor"], kernel.load_v2_policy()["verification"]["identity"])
        self.assertEqual(evaluation["initiator"], "agent:codex")
        reads = [row for row in rows if row["kind"] == "context_retrieved"]
        self.assertEqual(len(reads), 1)
        self.assertEqual(reads[0]["claim_ids"], [])
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
        cid = first["result"]["claim"]["id"]
        receipt = self.control.execute(self.owner, operation("review.receipt", {"claim_id":cid}))["result"]
        self.assertEqual(receipt["state"], "needs_review")
        self.assertEqual(receipt["judge_job"]["state"], "completed")

    def test_activating_automatic_policy_enqueues_existing_candidates(self):
        cid = self.proposal("existing")["result"]["claim"]["id"]
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test"}), \
             patch("proofpress.hosted.control_plane.threading.Thread"):
            self.control.save_review_policy(self.owner, {**self.settings, "mode":"automatic"}, 0)
        with self.control._db() as connection:
            job = connection.execute("SELECT claim_id, state FROM hosted_judge_jobs").fetchone()
        self.assertEqual((job["claim_id"], job["state"]), (cid, "queued"))

    def test_failed_current_checks_are_blocked_out_of_owner_review(self):
        proposal = self.control.execute(self.agent, operation("claim.propose", {
            "title": "Unsupported candidate",
            "statement": "Unsupported candidate", "evidence_refs": [], "scope": "test",
            "proposer": "agent:codex"}, "unsupported"))
        cid = proposal["result"]["claim"]["id"]
        self.control.execute(self.agent, operation("claim.evaluate", {"claim_id": cid}))
        receipt = self.control.execute(self.owner, operation("review.receipt", {"claim_id": cid}))["result"]
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

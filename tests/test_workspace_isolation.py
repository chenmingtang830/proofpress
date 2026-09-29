"""Shared-database isolation at the hosted service and mutation boundaries."""
from dataclasses import replace
import base64
import hashlib
import json
import os
from pathlib import Path
import tempfile
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from proofpress.hosted import execution, review_policy
from cryptography.fernet import Fernet
from proofpress.hosted.control_plane import HostedAuthError, HostedControlPlane
from proofpress.hosted import mcp_http
from proofpress.hosted.service import create_hosted_server
from proofpress.kernel import operations as kernel
from proofpress.kernel.contracts import AGENT_OPERATIONS
from proofpress.kernel.events import SQLiteEventStore
from test_hosted_authority import evidence_payload, operation


class WorkspaceIsolationTests(unittest.TestCase):
    def configure_workspace(self, owner, *, criteria=""):
        return self.control.save_review_policy(owner, {
            "mode": "off", "provider": "openrouter", "endpoint": "",
            "model": "", "criteria": criteria, "zdr": True,
            "rubric": "evidence-support/v1", "external_consent": False,
            "require_judge": False}, 0)

    def configure_b(self):
        return self.configure_workspace(self.b_owner, criteria="B-only criteria")

    def seed_claim(self, agent, owner, marker, *, state="admit", scope="shared-topic"):
        payload = evidence_payload()
        payload["source"]["uri"] = f"workspace://{marker}.pdf"
        payload["source"]["content_digest"] = "sha256:" + (
            "c" if marker.startswith("B") else "d") * 64
        submitted = self.control.execute(agent, operation(
            "evidence.submit", {"payload": payload}, marker + "-evidence"))
        self.assertTrue(submitted["ok"], submitted)
        evidence_id = submitted["result"]["evidence"][0]
        proposed = self.control.execute(agent, operation("claim.propose", {
            "title": marker, "statement": marker + " private content",
            "evidence_refs": [evidence_id], "proposer": "spoofed", "scope": scope,
        }, marker + "-claim"))
        self.assertTrue(proposed["ok"], proposed)
        claim = proposed["result"]["claim"]
        if state in {"admit", "reject"}:
            checked = self.control.execute(agent, operation(
                "claim.evaluate", {"claim_id": claim["id"]}))
            self.assertTrue(checked["ok"], checked)
            reviewed = self.control.execute(owner, operation("claim.review", {
                "claim_id": claim["id"], "decision": state,
                "reviewer": "spoofed", "request_id": marker + "-review",
                "note": "Synthetic rejection" if state == "reject" else "",
            }))
            self.assertTrue(reviewed["ok"], reviewed)
        return claim, evidence_id

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.database = Path(self.temp.name) / "shared.db"
        self.control = HostedControlPlane(self.database)
        self.a_bootstrap = self.control.bootstrap("workspace:A", "human:owner")
        self.a_owner = self.a_bootstrap["token"]
        self.a_agent = self.control.issue_agent_credential(
            self.a_owner, "agent:same", "A agent")["token"]
        # A test fixture may add B to the same database; production bootstrap
        # must still refuse a second workspace.
        with self.control._db() as connection:
            connection.execute("INSERT INTO hosted_workspaces VALUES (?, ?)",
                               ("workspace:B", "2026-01-01T00:00:00Z"))
            for principal, role in (("human:owner", "owner"), ("agent:same", "agent")):
                connection.execute("INSERT INTO hosted_principals VALUES (?, ?, ?, ?, ?)",
                    ("workspace:B", principal, role, principal, "2026-01-01T00:00:00Z"))
                cred_id, token, salt, secret_hash = self.control._new_credential_values()
                connection.execute("INSERT INTO hosted_credentials VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL)",
                    (cred_id, "workspace:B", principal, principal, salt, secret_hash,
                     json.dumps(["*"] if role == "owner" else sorted(AGENT_OPERATIONS)),
                     "2026-01-01T00:00:00Z"))
                if role == "owner":
                    self.b_owner = token
                else:
                    self.b_agent = token

    def test_context_identity_is_revalidated_before_read_or_audit(self):
        self.configure_b()
        submitted = self.control.execute(self.b_agent, operation(
            "evidence.submit", {"payload": evidence_payload()}))
        self.assertTrue(submitted["ok"])
        b_context = self.control.authenticate(self.b_agent)
        a_context = self.control.authenticate(self.a_agent)
        with self.control._db() as connection:
            before = connection.execute("SELECT COUNT(*) FROM hosted_audit WHERE workspace_id='workspace:B'").fetchone()[0]
        for forged in (replace(a_context, workspace_id="workspace:B"),
                       replace(a_context, role="owner", permissions=frozenset({"*"})),
                       replace(a_context, credential_id=b_context.credential_id)):
            denied = self.control.execute_as(forged, operation(
                "claim.review", {"claim_id": "foreign", "decision": "admit",
                                 "reviewer": "human:owner", "request_id": "forged"}))
            self.assertFalse(denied["ok"])
            self.assertIn(denied["error"]["code"], {"invalid_credential", "operation_forbidden"})
        with self.control._db() as connection:
            after = connection.execute("SELECT COUNT(*) FROM hosted_audit WHERE workspace_id='workspace:B'").fetchone()[0]
        self.assertEqual(before, after)
        with self.assertRaisesRegex(ValueError, "already bootstrapped"):
            self.control.bootstrap("workspace:C", "human:owner")

    def test_policy_and_deployment_key_do_not_cross_workspace(self):
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "synthetic-a-only",
                                  "PROOFPRESS_JUDGE_MODEL": "synthetic-model"}):
            with self.control._db() as connection:
                a = self.control._current_policy(connection, "workspace:A")
                self.assertEqual(a["version"], 0)
                self.assertEqual(self.control._provider_credential(
                    connection, "workspace:A", "openrouter"), "synthetic-a-only")
                self.assertIsNone(self.control._provider_credential(
                    connection, "workspace:B", "openrouter"))
                self.assertFalse(self.control._credential_status(
                    connection, "workspace:B", "openrouter")["configured"])
                with kernel.using_policy({"digest": "ambient-other-workspace"}):
                    self.assertEqual(self.control._current_policy(
                        connection, "workspace:A")["policy"]["digest"], a["policy"]["digest"])
                    with self.assertRaisesRegex(ValueError, "workspace_policy_missing"):
                        self.control._current_policy(connection, "workspace:B")
                    with self.assertRaisesRegex(ValueError, "workspace_policy_missing"):
                        self.control._current_policy(connection, "workspace:missing")
                self.assertFalse(review_policy.public(a, {"configured": False})
                                 ["credential"]["configured"])
        self.assertEqual(self.control.execute(self.b_agent, operation(
            "capabilities.get", {}))["error"]["code"], "workspace_policy_missing")
        restarted = HostedControlPlane(self.database)
        self.assertIsNone(restarted.legacy_default_workspace_id)
        with self.assertRaisesRegex(ValueError, "workspace_policy_missing"):
            restarted._policy("workspace:A")
        explicit = HostedControlPlane(self.database, legacy_default_workspace_id="workspace:A")
        self.assertEqual(explicit._policy("workspace:A")["version"], 0)

    def test_identical_ids_and_retry_keys_remain_workspace_local(self):
        request = operation("evidence.submit", {"payload": evidence_payload()}, "shared-key")
        a = self.control.execute(self.a_agent, request)
        b = self.control.execute(self.b_agent, request)
        self.assertTrue(a["ok"])
        # B must first receive its own explicit policy; never copy A's defaults.
        self.assertFalse(b["ok"])
        self.configure_b()
        b = self.control.execute(self.b_agent, request)
        self.assertTrue(b["ok"])
        self.assertEqual(a["result"]["evidence"], b["result"]["evidence"])
        self.assertEqual(len(self.control.list_executions(self.a_owner)), 1)
        self.assertEqual(len(self.control.list_executions(self.b_owner)), 1)
        self.assertEqual(len(SQLiteEventStore(self.database, "workspace:A", "agent:same").list_events()),
                         len(SQLiteEventStore(self.database, "workspace:B", "agent:same").list_events()))

    def test_foreign_claim_reads_writes_and_context_are_isolated(self):
        self.configure_b()
        payload = evidence_payload()
        payload["source"]["uri"] = "workspace://b-private.pdf"
        payload["source"]["content_digest"] = "sha256:" + "c" * 64
        evidence = self.control.execute(self.b_agent, operation(
            "evidence.submit", {"payload": payload}))["result"]["evidence"][0]
        proposed = self.control.execute(self.b_agent, operation("claim.propose", {
            "title": "B private", "statement": "B-only governed content marker",
            "evidence_refs": [evidence], "proposer": "agent:same", "scope": "shared-topic",
        }))
        self.assertTrue(proposed["ok"])
        claim_id = proposed["result"]["claim"]["id"]
        self.assertTrue(self.control.execute(self.b_agent, operation(
            "claim.evaluate", {"claim_id": claim_id}))["ok"])
        self.assertTrue(self.control.execute(self.b_owner, operation(
            "claim.review", {"claim_id": claim_id, "decision": "admit",
                              "reviewer": "human:owner", "request_id": "b-review"}))["ok"])
        b_store = SQLiteEventStore(self.database, "workspace:B", "agent:same")
        b_head = b_store.head()
        for token, name, parameters in (
            (self.a_owner, "review.receipt", {"claim_id": claim_id}),
            (self.a_agent, "claim.evaluate", {"claim_id": claim_id}),
            (self.a_owner, "claim.review", {"claim_id": claim_id,
                                              "decision": "admit", "request_id": "a-foreign"}),
        ):
            result = self.control.execute(token, operation(name, parameters))
            self.assertFalse(result["ok"], (name, result))
            self.assertNotIn("B-only governed content marker", json.dumps(result))
        context = self.control.execute(self.a_agent, operation(
            "context.get", {"scope": "shared-topic"}))
        self.assertTrue(context["ok"])
        self.assertNotIn("B-only governed content marker", json.dumps(context))
        self.assertEqual(b_store.head(), b_head)

    def test_foreign_context_surfaces_and_evidence_bindings_are_excluded(self):
        self.configure_b()
        b_claim, b_evidence = self.seed_claim(
            self.b_agent, self.b_owner, "B-private-admitted")
        b_store = SQLiteEventStore(self.database, "workspace:B", "agent:same")
        before = b_store.head()
        for name, params in (
            ("context.get", {"scope": "shared-topic"}),
            ("context.discover", {"task": "B-private-admitted"}),
            ("graph.get", {"scope": "shared-topic"}),
            ("graph.traverse", {"seed_ids": [b_claim["id"]],
                                "scope": "shared-topic"}),
            ("review.summary", {"scope": "shared-topic"}),
        ):
            for token in (self.a_agent, self.a_owner):
                result = self.control.execute(token, operation(name, params))
                if name != "graph.traverse":
                    self.assertTrue(result["ok"], (name, result))
                else:
                    self.assertFalse(result["ok"], result)
                    self.assertEqual(result["error"]["code"], "operation_rejected")
                visible = dict(result.get("result") or result.get("error") or {})
                visible.pop("task", None)  # Caller-supplied text may be echoed.
                self.assertNotIn("B-private-admitted", json.dumps(visible))
        proposed = self.control.execute(self.a_agent, operation("claim.propose", {
            "title": "foreign evidence", "statement": "Cannot bind B evidence",
            "evidence_refs": [b_evidence], "proposer": "spoofed",
        }))
        self.assertFalse(proposed["ok"], proposed)
        self.assertEqual(b_store.head(), before)

    def test_foreign_claim_lifecycle_and_relation_endpoints_are_rejected(self):
        self.configure_b()
        b_claim, _ = self.seed_claim(self.b_agent, self.b_owner, "B-lifecycle")
        a_claim, _ = self.seed_claim(self.a_agent, self.a_owner, "A-lifecycle")
        b_store = SQLiteEventStore(self.database, "workspace:B", "agent:same")
        b_head = b_store.head()
        a_head = SQLiteEventStore(self.database, "workspace:A", "agent:same").head()
        attempts = (
            (self.a_owner, "claim.supersede", {"claim_id": b_claim["id"],
                "replacement_id": a_claim["id"], "reviewer": "spoofed"}),
            (self.a_owner, "claim.withdraw", {"claim_id": b_claim["id"],
                "reviewer": "spoofed", "note": "x", "request_id": "foreign-withdraw",
                "expected_head": a_head}),
            (self.a_owner, "claim.reassess", {"claim_id": b_claim["id"],
                "decision": "retain", "reviewer": "spoofed", "note": "x",
                "request_id": "foreign-reassess", "expected_head": a_head}),
            (self.a_agent, "relation.propose", {"source_id": a_claim["id"],
                "target_id": b_claim["id"], "relation_type": "supports",
                "proposer": "spoofed"}),
            (self.a_agent, "claim.propose", {"title": "foreign predecessor",
                "statement": "invalid", "evidence_refs": [], "proposer": "spoofed",
                "reproposal_of": b_claim["id"]}),
        )
        for token, name, params in attempts:
            result = self.control.execute(token, operation(name, params))
            self.assertFalse(result["ok"], (name, result))
            self.assertNotIn("B-lifecycle private content", json.dumps(result))
            self.assertEqual(b_store.head(), b_head)

    def test_foreign_relation_operations_are_rejected(self):
        self.configure_b()
        first, _ = self.seed_claim(self.b_agent, self.b_owner, "B-relation-source")
        second, _ = self.seed_claim(self.b_agent, self.b_owner, "B-relation-target")
        proposed = self.control.execute(self.b_agent, operation("relation.propose", {
            "source_id": first["id"], "target_id": second["id"],
            "relation_type": "qualifies", "proposer": "spoofed"}))
        self.assertTrue(proposed["ok"], proposed)
        relation_id = proposed["result"]["relation"]["id"]
        b_store = SQLiteEventStore(self.database, "workspace:B", "agent:same")
        before = b_store.head()
        for token, name, params in (
            (self.a_agent, "relation.evaluate", {"relation_id": relation_id}),
            (self.a_agent, "relation.judge", {"relation_id": relation_id}),
            (self.a_owner, "relation.review", {"relation_id": relation_id,
                "decision": "admit", "reviewer": "spoofed"}),
            (self.a_owner, "relation.resolve", {"relation_id": relation_id,
                "disposition": "retire", "reviewer": "spoofed"}),
        ):
            result = self.control.execute(token, operation(name, params))
            self.assertFalse(result["ok"], (name, result))
            self.assertNotIn("B-relation", json.dumps(result))
            self.assertEqual(b_store.head(), before)

    def test_mcp_receipt_lineage_and_review_link_reject_foreign_claim(self):
        self.configure_b()
        b_claim, _ = self.seed_claim(self.b_agent, self.b_owner, "B-mcp")
        context = self.control.authenticate(self.a_agent)
        for name, args in (
            ("proofpress_get_review_receipt", {"claim_id": b_claim["id"]}),
            ("proofpress_get_lineage", {"claim_id": b_claim["id"]}),
            ("proofpress_get_review_link", {"claim_id": b_claim["id"]}),
        ):
            with self.assertRaises(ValueError, msg=name):
                mcp_http.call_tool(self.control, context, name, args,
                                   "https://proofpress.example")

    def test_oauth_token_family_keeps_credential_workspace(self):
        self.configure_b()
        client = self.control.register_oauth_client(
            "synthetic", ["http://127.0.0.1:9876/callback"])
        client_id = client["client_id"]
        redirect = client["redirect_uris"][0]
        resource = "https://proofpress.example/mcp"
        verifier = "v" * 64
        challenge = base64.urlsafe_b64encode(
            hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
        pairs = {}
        for workspace, token in (("A", self.a_agent), ("B", self.b_agent)):
            code = self.control.create_oauth_code(
                token, client_id, redirect, resource, challenge)
            pair = self.control.exchange_oauth_code(
                code, client_id, redirect, resource, verifier)
            self.assertEqual(self.control.authenticate_oauth_access(
                pair["access_token"], resource).workspace_id, "workspace:" + workspace)
            pairs[workspace] = pair
        with self.assertRaises(HostedAuthError):
            self.control.refresh_oauth_token(pairs["A"]["refresh_token"],
                                             client_id, "https://other.example/mcp")
        refreshed = self.control.refresh_oauth_token(
            pairs["A"]["refresh_token"], client_id, resource)
        self.assertEqual(self.control.authenticate_oauth_access(
            refreshed["access_token"], resource).workspace_id, "workspace:A")
        with self.assertRaises(HostedAuthError):
            self.control.refresh_oauth_token(pairs["A"]["refresh_token"], client_id, resource)
        self.assertEqual(self.control.authenticate_oauth_access(
            pairs["B"]["access_token"], resource).workspace_id, "workspace:B")

    def test_run_and_external_ingest_cannot_bind_foreign_run(self):
        self.configure_b()
        started = self.control.execute(self.b_agent, operation("run.start", {
            "purpose": "B private run", "actor": "spoofed", "metadata": None},
            "same-run-key"))
        self.assertTrue(started["ok"], started)
        run_id = started["result"]["id"]
        b_store = SQLiteEventStore(self.database, "workspace:B", "agent:same")
        before = b_store.head()
        for name, params in (
            ("run.get", {"run_id": run_id}),
            ("run.finish", {"run_id": run_id, "status": "completed", "actor": "spoofed"}),
            ("context.capture", {"run_id": run_id, "actor": "spoofed"}),
            ("reliance.record", {"run_id": run_id, "receipt_id": "receipt",
                "claim_id": "claim", "claim_digest": "sha256:" + "a" * 64,
                "purpose": "foreign", "actor": "spoofed"}),
            ("output.record", {"run_id": run_id, "reference": "repo://output",
                "content_digest": "sha256:" + "b" * 64, "actor": "spoofed"}),
            ("observation.record", {"run_id": run_id, "kind": "test",
                "source": "synthetic", "meaning": "foreign", "actor": "spoofed"}),
        ):
            result = self.control.execute(self.a_agent, operation(name, params))
            self.assertFalse(result["ok"], (name, result))
            self.assertNotIn("B private run", json.dumps(result))
        fixture = Path(__file__).parent / "fixtures/external_experiment_v0.json"
        payload = json.loads(fixture.read_text(encoding="utf-8"))
        payload["binding"]["proofpress_run_id"] = run_id
        ingested = self.control.execute(self.a_agent, operation(
            "experiment.ingest", {"payload": payload, "actor": "spoofed"},
            "foreign-experiment"))
        self.assertFalse(ingested["ok"], ingested)
        self.assertEqual(b_store.head(), before)
        listed = self.control.execute(self.a_agent, operation("run.list", {}))
        self.assertTrue(listed["ok"])
        self.assertNotIn("B private run", json.dumps(listed))

    def test_foreign_receipt_reliance_and_output_links_fail_closed(self):
        self.configure_b()
        b_claim, b_evidence = self.seed_claim(
            self.b_agent, self.b_owner, "B-reliance")
        b_run = self.control.execute(self.b_agent, operation("run.start", {
            "purpose": "B run", "actor": "spoofed"}, "b-start"))["result"]["id"]
        b_capture = self.control.execute(self.b_agent, operation("context.capture", {
            "run_id": b_run, "actor": "spoofed", "scope": "shared-topic"}, "b-capture"))
        self.assertTrue(b_capture["ok"], b_capture)
        b_receipt = b_capture["result"]["id"]
        b_claim_digest = b_claim["digest"]
        a_run = self.control.execute(self.a_agent, operation("run.start", {
            "purpose": "A run", "actor": "spoofed"}, "a-start"))["result"]["id"]
        b_store = SQLiteEventStore(self.database, "workspace:B", "agent:same")
        b_head = b_store.head()
        a_head = SQLiteEventStore(self.database, "workspace:A", "agent:same").head()
        attempts = (
            ("reliance.record", {"run_id": a_run, "receipt_id": b_receipt,
                "claim_id": b_claim["id"], "claim_digest": b_claim_digest,
                "purpose": "foreign", "actor": "spoofed"}),
            ("output.record", {"run_id": a_run, "reference": "repo://a-output",
                "content_digest": "sha256:" + "e" * 64, "actor": "spoofed",
                "reliance_ids": ["rel_foreign"]}),
            ("observation.record", {"run_id": a_run, "kind": "test",
                "source": "synthetic", "meaning": "foreign", "actor": "spoofed",
                "evidence_refs": [b_evidence]}),
        )
        for name, params in attempts:
            result = self.control.execute(self.a_agent, operation(name, params))
            self.assertFalse(result["ok"], (name, result))
            self.assertNotIn("B-reliance private content", json.dumps(result))
            self.assertEqual(b_store.head(), b_head)
        self.assertEqual(SQLiteEventStore(
            self.database, "workspace:A", "agent:same").head(), a_head)

    def test_request_cannot_select_workspace(self):
        self.configure_b()
        before = SQLiteEventStore(self.database, "workspace:B", "agent:same").head()
        for selector in ("workspace_id", "organization_id"):
            request = operation("context.get", {"scope": "shared-topic",
                                               selector: "workspace:B"})
            result = self.control.execute(self.a_agent, request)
            self.assertFalse(result["ok"], result)
            request = operation("context.get", {"scope": "shared-topic"})
            request[selector] = "workspace:B"
            result = self.control.execute(self.a_agent, request)
            self.assertFalse(result["ok"], result)
        self.assertEqual(SQLiteEventStore(
            self.database, "workspace:B", "agent:same").head(), before)

    def test_content_ids_collide_without_sharing_lifecycle_or_history(self):
        self.configure_b()
        request = operation("evidence.submit", {"payload": evidence_payload()}, "same-key")
        a_evidence = self.control.execute(self.a_agent, request)
        b_evidence = self.control.execute(self.b_agent, request)
        self.assertTrue(a_evidence["ok"] and b_evidence["ok"])
        self.assertEqual(a_evidence["result"]["evidence"], b_evidence["result"]["evidence"])
        propose = operation("claim.propose", {"title": "Same content",
            "statement": "A bounded identical claim", "evidence_refs": a_evidence["result"]["evidence"],
            "scope": "shared-topic", "proposer": "spoofed"}, "same-claim-key")
        a = self.control.execute(self.a_agent, propose)
        b = self.control.execute(self.b_agent, propose)
        self.assertTrue(a["ok"] and b["ok"])
        claim_id = a["result"]["claim"]["id"]
        self.assertEqual(claim_id, b["result"]["claim"]["id"])
        self.assertTrue(self.control.execute(self.b_agent, operation(
            "claim.evaluate", {"claim_id": claim_id}))["ok"])
        self.assertTrue(self.control.execute(self.b_owner, operation("claim.review", {
            "claim_id": claim_id, "decision": "admit", "reviewer": "spoofed",
            "request_id": "b-admit"}))["ok"])
        a_receipt = self.control.execute(self.a_owner, operation(
            "review.receipt", {"claim_id": claim_id}))
        b_receipt = self.control.execute(self.b_owner, operation(
            "review.receipt", {"claim_id": claim_id}))
        self.assertTrue(a_receipt["ok"] and b_receipt["ok"])
        self.assertNotEqual(a_receipt["result"]["state"], b_receipt["result"]["state"])
        self.assertNotIn("b-admit", json.dumps(a_receipt))

    def test_foreign_rejected_revised_withdrawn_and_related_states_are_hidden(self):
        self.configure_b()
        rejected, _ = self.seed_claim(self.b_agent, self.b_owner,
                                      "B-rejected", state="reject")
        revised, _ = self.seed_claim(self.b_agent, self.b_owner,
                                     "B-revised", state="candidate")
        self.assertTrue(self.control.execute(self.b_agent, operation(
            "claim.evaluate", {"claim_id": revised["id"]}))["ok"])
        changed = self.control.execute(self.b_owner, operation("claim.review", {
            "claim_id": revised["id"], "decision": "request_changes",
            "reviewer": "spoofed", "request_id": "b-changes",
            "note": "Synthetic revision"}))
        self.assertTrue(changed["ok"], changed)
        withdrawn, _ = self.seed_claim(self.b_agent, self.b_owner,
                                       "B-withdrawn")
        b_head = SQLiteEventStore(self.database, "workspace:B", "agent:same").head()
        withdrawn_result = self.control.execute(self.b_owner, operation("claim.withdraw", {
            "claim_id": withdrawn["id"], "reviewer": "spoofed",
            "note": "synthetic withdrawal", "request_id": "b-withdraw",
            "expected_head": b_head}))
        self.assertTrue(withdrawn_result["ok"], withdrawn_result)
        related, _ = self.seed_claim(self.b_agent, self.b_owner, "B-related")
        relation = self.control.execute(self.b_agent, operation("relation.propose", {
            "source_id": rejected["id"], "target_id": related["id"],
            "relation_type": "qualifies", "proposer": "spoofed"}))
        self.assertTrue(relation["ok"], relation)
        b_store = SQLiteEventStore(self.database, "workspace:B", "agent:same")
        before = b_store.head()
        for row in (rejected, revised, withdrawn, related):
            foreign = self.control.execute(self.a_owner, operation(
                "review.receipt", {"claim_id": row["id"]}))
            self.assertFalse(foreign["ok"], foreign)
            self.assertNotIn(row["statement"], json.dumps(foreign))
        for name, params in (
            ("review.summary", {"scope": "shared-topic"}),
            ("graph.get", {"scope": "shared-topic"}),
            ("context.get", {"scope": "shared-topic"}),
        ):
            result = self.control.execute(self.a_owner, operation(name, params))
            self.assertTrue(result["ok"], (name, result))
            for marker in ("B-rejected", "B-revised", "B-withdrawn", "B-related"):
                self.assertNotIn(marker, json.dumps(result))
        self.assertEqual(b_store.head(), before)

    def test_policy_cas_and_owner_inspection_remain_local(self):
        b_policy = self.configure_b()
        b_claim, _ = self.seed_claim(self.b_agent, self.b_owner, "B-inspection")
        self.control.execute(self.b_agent, operation("context.get", {"scope": "shared-topic"}))
        b_before = self.control._policy("workspace:B")
        self.assertEqual(b_before["policy"]["digest"], b_policy["policy_digest"])
        a_policy = self.control.save_review_policy(self.a_owner, {
            "mode": "off", "provider": "openrouter", "endpoint": "",
            "model": "", "criteria": "A-only criteria", "zdr": True,
            "rubric": "evidence-support/v1", "external_consent": False,
            "require_judge": False}, 0)
        self.assertNotEqual(a_policy["policy_digest"], b_policy["policy_digest"])
        with self.assertRaisesRegex(ValueError, "Review policy changed"):
            self.control.save_review_policy(self.a_owner, a_policy["settings"], 0)
        self.assertEqual(self.control._policy("workspace:B")["policy"]["digest"],
                         b_policy["policy_digest"])
        for owner in (self.a_owner, self.b_owner):
            snapshot = {
                "credentials": self.control.list_credentials(owner),
                "activity": self.control.list_activity(owner),
                "audit": self.control.list_audit(owner),
                "executions": self.control.list_executions(owner),
                "dashboard": self.control.home_dashboard(owner),
                "policy": self.control.get_review_policy(owner),
            }
            if owner == self.a_owner:
                self.assertNotIn("B-inspection", json.dumps(snapshot))
                self.assertNotIn(b_claim["id"], json.dumps(snapshot))
                self.assertNotIn("B-only criteria", json.dumps(snapshot))
            else:
                self.assertNotIn("A-only criteria", json.dumps(snapshot))

    def test_provider_secrets_and_judge_environment_are_workspace_local(self):
        self.configure_b()
        with patch.dict(os.environ, {
                "PROOFPRESS_SECRET_ENCRYPTION_KEY": Fernet.generate_key().decode(),
                "OPENROUTER_API_KEY": "deployment-a-key"}):
            with self.control._db() as connection:
                review_policy.save_credential(connection, "workspace:B",
                                              "synthetic-b-provider-key", "2026-01-01")
                self.assertEqual(self.control._provider_credential(
                    connection, "workspace:A", "openrouter"), "deployment-a-key")
                self.assertEqual(self.control._provider_credential(
                    connection, "workspace:B", "openrouter"), "synthetic-b-provider-key")
            seen = []
            def capture(_request):
                seen.append(kernel._judge_environment.get()["PROOFPRESS_JUDGE_API_KEY"])
                return {"ok": False, "error": {"code": "operation_rejected",
                                               "message": "synthetic no-provider-call"}}
            with patch("proofpress.hosted.control_plane.kernel_ops.execute_local_operation",
                       side_effect=capture):
                self.control.execute(self.a_agent, operation(
                    "claim.judge", {"claim_id": "missing"}))
                self.control.execute(self.b_agent, operation(
                    "claim.judge", {"claim_id": "missing"}))
            self.assertEqual(seen, ["deployment-a-key", "synthetic-b-provider-key"])
            self.assertIsNone(kernel._judge_environment.get())
            with self.control._db() as connection:
                review_policy.delete_credential(connection, "workspace:B")
                self.assertIsNone(self.control._provider_credential(
                    connection, "workspace:B", "openrouter"))
                self.assertEqual(self.control._provider_credential(
                    connection, "workspace:A", "openrouter"), "deployment-a-key")
            self.assertEqual(os.environ["OPENROUTER_API_KEY"], "deployment-a-key")

    def test_reverse_access_and_denial_audit_stay_with_caller(self):
        self.configure_b()
        a_claim, _ = self.seed_claim(self.a_agent, self.a_owner, "A-reverse")
        a_store = SQLiteEventStore(self.database, "workspace:A", "agent:same")
        a_head = a_store.head()
        with self.control._db() as connection:
            a_audits = connection.execute(
                "SELECT COUNT(*) FROM hosted_audit WHERE workspace_id='workspace:A'").fetchone()[0]
        for token, name, params in (
            (self.b_owner, "review.receipt", {"claim_id": a_claim["id"]}),
            (self.b_agent, "claim.evaluate", {"claim_id": a_claim["id"]}),
            (self.b_owner, "claim.withdraw", {"claim_id": a_claim["id"],
                "reviewer": "spoofed", "note": "foreign", "request_id": "b-foreign",
                "expected_head": a_head}),
        ):
            result = self.control.execute(token, operation(name, params))
            self.assertFalse(result["ok"], (name, result))
            self.assertNotIn("A-reverse private content", json.dumps(result))
        self.assertEqual(a_store.head(), a_head)
        with self.control._db() as connection:
            self.assertEqual(connection.execute(
                "SELECT COUNT(*) FROM hosted_audit WHERE workspace_id='workspace:A'").fetchone()[0],
                a_audits)

    def test_store_and_policy_context_reset_after_exception_and_threads(self):
        self.configure_b()
        from proofpress.kernel.events import current_event_store
        def inspect(token):
            context = self.control.authenticate(token)
            result = self.control.execute(token, operation("context.get", {
                "scope": "shared-topic"}))
            return context.workspace_id, result["ok"], result["result"]["actor"]
        with ThreadPoolExecutor(max_workers=2) as pool:
            observations = list(pool.map(inspect, (self.a_agent, self.b_agent)))
        self.assertEqual({row[0] for row in observations},
                         {"workspace:A", "workspace:B"})
        self.assertTrue(all(row[1] and row[2] == "agent:same" for row in observations))
        with patch("proofpress.hosted.control_plane.kernel_ops.execute_local_operation",
                   side_effect=RuntimeError("synthetic failure")):
            with self.assertRaisesRegex(RuntimeError, "synthetic failure"):
                self.control.execute(self.b_agent, operation("context.get", {}))
        self.assertIsNone(kernel._policy_override.get())
        self.assertIsNone(kernel._judge_environment.get())
        # Outside the hosted call, the ambient store is the local default,
        # never the previous customer's SQLite store.
        self.assertNotIsInstance(current_event_store(), SQLiteEventStore)

    def test_single_workspace_restart_preserves_heads_and_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "prior.db"
            original = HostedControlPlane(database)
            owner = original.bootstrap("workspace:legacy", "human:owner")["token"]
            agent = original.issue_agent_credential(owner, "agent:same", "legacy")["token"]
            request = operation("evidence.submit", {"payload": evidence_payload()},
                                "stable-before-upgrade")
            first = original.execute(agent, request)
            self.assertTrue(first["ok"], first)
            store = SQLiteEventStore(database, "workspace:legacy", "agent:same")
            before_head = store.head()
            before_policy = original._policy("workspace:legacy")["policy"]["digest"]
            restarted = HostedControlPlane(database)
            self.assertEqual(restarted.legacy_default_workspace_id, "workspace:legacy")
            self.assertEqual(restarted._policy("workspace:legacy")["policy"]["digest"],
                             before_policy)
            self.assertEqual(restarted.authenticate(agent).workspace_id,
                             "workspace:legacy")
            replay = restarted.execute(agent, request)
            self.assertTrue(replay["ok"] and replay.get("idempotent_replay"), replay)
            self.assertEqual(store.head(), before_head)
            self.assertEqual(restarted.list_executions(owner)[0]["state"], "succeeded")

    def test_export_is_workspace_scoped_and_backup_is_not_an_operation(self):
        self.configure_b()
        self.seed_claim(self.b_agent, self.b_owner, "B-export")
        bundle = SQLiteEventStore(self.database, "workspace:A", "agent:same").export_bundle()
        self.assertEqual(bundle["workspace_id"], "workspace:A")
        self.assertNotIn("B-export", json.dumps(bundle))
        for name in ("backup", "restore", "database.backup", "database.restore"):
            self.assertFalse(self.control.execute(self.a_agent,
                operation(name, {}))["ok"])

    def test_credential_administration_stays_with_owner_workspace(self):
        b_id = self.control.authenticate(self.b_agent).credential_id
        self.assertNotIn(b_id, [row["credential_id"] for row in
                           self.control.list_credentials(self.a_owner)])
        with self.assertRaisesRegex(ValueError, "active credential not found"):
            self.control.revoke_credential(self.a_owner, b_id)
        with self.assertRaisesRegex(ValueError, "active agent credential not found"):
            self.control.rotate_agent_credential(self.a_owner, b_id)
        self.assertEqual(self.control.authenticate(self.b_agent).credential_id, b_id)

    def test_owner_session_and_assistant_default_are_workspace_bound(self):
        self.configure_b()
        b_claim, _ = self.seed_claim(self.b_agent, self.b_owner, "B-owner-page")
        server = create_hosted_server(
            self.database, port=0, legacy_default_workspace_id="workspace:A")
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            for name, token in (("a", self.a_owner), ("b", self.b_owner)):
                server.proofpress_owner_sessions[name] = {
                    "context": server.proofpress_control.authenticate(token),
                    "csrf": "synthetic-csrf", "expires_at": time.time() + 60}
            with patch.dict(os.environ, {"OPENROUTER_API_KEY": "synthetic-key",
                                      "PROOFPRESS_WORKSPACE_LABEL": "A label"}):
                base = f"http://127.0.0.1:{server.server_port}"
                def session(name):
                    with urlopen(Request(base + "/owner/api/session",
                                         headers={"Cookie": "pp_owner=" + name})) as response:
                        return json.loads(response.read())["result"]
                a, b = session("a"), session("b")
                self.assertEqual(a["workspace_id"], "workspace:A")
                self.assertEqual(a["workspace"], "A label")
                self.assertTrue(a["capabilities"]["assistant"])
                self.assertEqual(b["workspace_id"], "workspace:B")
                self.assertEqual(b["workspace"], "workspace:B")
                self.assertFalse(b["capabilities"]["assistant"])
                with urlopen(Request(base + "/owner/api/review-policy",
                                     headers={"Cookie": "pp_owner=b"})) as response:
                    b_policy = json.loads(response.read())["result"]
                self.assertEqual(b_policy["version"], 1)
                self.assertFalse(b_policy["credential"]["configured"])
                for path in ("/owner/api/claims/" + b_claim["id"],
                             "/owner/api/summary?scope=shared-topic",
                             "/owner/api/context?scope=shared-topic",
                             "/owner/api/graph?scope=shared-topic",
                             "/owner/api/activity", "/owner/api/technical-logs",
                             "/owner/api/executions", "/owner/api/dashboard"):
                    request = Request(base + path, headers={"Cookie": "pp_owner=a"})
                    try:
                        with urlopen(request) as response:
                            body = response.read().decode()
                    except HTTPError as exc:
                        body = exc.read().decode()
                        exc.close()
                    self.assertNotIn("B-owner-page", body, path)
                    self.assertNotIn("B-only criteria", body, path)
                request = Request(base + "/owner/api/ask",
                    data=json.dumps({"csrf": "synthetic-csrf", "question": "test",
                                     "snapshot": {"private": "B"}}).encode(),
                    headers={"Cookie": "pp_owner=b", "Content-Type": "application/json"},
                    method="POST")
                with self.assertRaises(HTTPError) as failed:
                    urlopen(request)
                self.assertEqual(failed.exception.code, 503)
                self.assertEqual(json.loads(failed.exception.read())["error"]["code"],
                                 "assistant_unconfigured")
                failed.exception.close()
            self.control.revoke_credential(
                self.a_owner, self.control.authenticate(self.a_agent).credential_id)
            with urlopen(Request(base + "/owner/api/session",
                                 headers={"Cookie": "pp_owner=b"})) as response:
                self.assertEqual(json.loads(response.read())["result"]["workspace_id"],
                                 "workspace:B")
            recovered = self.control.recover_owner(
                "workspace:A", self.a_bootstrap["recovery_secret"])
            with self.assertRaises(HTTPError) as stale:
                urlopen(Request(base + "/owner/api/session",
                                headers={"Cookie": "pp_owner=a"}))
            self.assertEqual(stale.exception.code, 401)
            stale.exception.close()
            self.assertEqual(self.control.authenticate(recovered["token"]).workspace_id,
                             "workspace:A")
            with urlopen(Request(base + "/owner/api/session",
                                 headers={"Cookie": "pp_owner=b"})) as response:
                self.assertEqual(json.loads(response.read())["result"]["workspace_id"],
                                 "workspace:B")
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_finish_and_recovery_reject_foreign_attempt(self):
        with self.control._db() as connection:
            a_id, error = execution.begin(connection, workspace_id="workspace:A",
                principal_id="agent:same", idempotency_key="same", operation="claim.evaluate",
                fingerprint="fingerprint", versions={}, input_refs={})
            self.assertIsNone(error)
            connection.commit()
            b_id, error = execution.begin(connection, workspace_id="workspace:B",
                principal_id="agent:same", idempotency_key="same", operation="claim.evaluate",
                fingerprint="fingerprint", versions={}, input_refs={})
            self.assertIsNone(error)
            before = connection.execute(
                "SELECT state,output_refs_json FROM hosted_executions WHERE workspace_id='workspace:B'").fetchone()
            with self.assertRaisesRegex(ValueError, "execution_attempt_not_found"):
                execution.finish(connection, b_id, {"ok": True},
                                 workspace_id="workspace:A", principal_id="agent:same")
            with self.assertRaisesRegex(ValueError, "execution_attempt_not_found"):
                execution.finish(connection, b_id, {"ok": True},
                                 workspace_id="workspace:B", principal_id="agent:other")
            after = connection.execute(
                "SELECT state,output_refs_json FROM hosted_executions WHERE workspace_id='workspace:B'").fetchone()
            self.assertEqual(tuple(before), tuple(after))
            execution.resume(connection, workspace_id="workspace:A")
            states = connection.execute("SELECT workspace_id,state FROM hosted_executions").fetchall()
            self.assertEqual({row["workspace_id"]: row["state"] for row in states},
                             {"workspace:A": "interrupted", "workspace:B": "running"})
            execution.finish(connection, b_id, {"ok": True},
                             workspace_id="workspace:B", principal_id="agent:same")
            self.assertEqual(connection.execute(
                "SELECT state FROM hosted_execution_attempts WHERE attempt_id=?", (a_id,)).fetchone()[0],
                "interrupted")
        with self.control._db() as connection:
            execution.resume(connection, workspace_id="workspace:B")
            self.assertEqual(connection.execute(
                "SELECT state FROM hosted_executions WHERE workspace_id='workspace:A'").fetchone()[0],
                "interrupted")

    def test_judge_queue_and_recovery_are_scoped(self):
        with self.control._db() as connection:
            for workspace in ("workspace:A", "workspace:B"):
                connection.execute("INSERT INTO hosted_judge_jobs VALUES (?, ?, ?, ?, ?, 'running', ?, ?, '')",
                    (workspace, workspace, "claim", "digest", "agent:same", "2026-01-01", "2026-01-01"))
        with patch("proofpress.hosted.control_plane.threading.Thread"):
            self.control.resume_judge_jobs(workspace_id="workspace:A")
        with self.control._db() as connection:
            rows = connection.execute("SELECT workspace_id,state FROM hosted_judge_jobs").fetchall()
        self.assertEqual({row["workspace_id"]: row["state"] for row in rows},
                         {"workspace:A": "interrupted", "workspace:B": "running"})
        with self.control._db() as connection:
            connection.execute("UPDATE hosted_judge_jobs SET state='queued' WHERE workspace_id='workspace:B'")
        self.control.run_judge_jobs(workspace_id="workspace:A")
        with self.control._db() as connection:
            self.assertEqual(connection.execute(
                "SELECT state FROM hosted_judge_jobs WHERE workspace_id='workspace:B'").fetchone()[0],
                "queued")
        with self.assertRaisesRegex(ValueError, "workspace_id required"):
            self.control.run_judge_jobs()


if __name__ == "__main__":
    unittest.main()

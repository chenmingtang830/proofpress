"""Network-free TypeSafe transport, credential isolation and governance regression tests."""
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from cryptography.fernet import Fernet
from proofpress.hosted import jev, review_policy
from proofpress.hosted.judge import judge
from proofpress.hosted.control_plane import HostedControlPlane
from proofpress.kernel import operations as kernel
from test_hosted_authority import evidence_payload, operation


def typed_response(request, choice="accept", support=.99, confidence=.95):
    body = json.loads(request.data)
    answers = {}
    for key, question in body["questions"].items():
        if question["type"] == "choice":
            answers[key] = {"type": "choice", "choice": choice,
                            "probabilities": {v: .98 if v == choice else .01 for v in question["criteria"]},
                            "confidence": confidence}
        else:
            answers[key] = {"type": "noul", "noul": support}
    return {"model": "jev-test-revision", "answers": answers,
            "usage": {"input_tokens": 125, "output_tokens": 12}}


def opener(request, timeout):
    return io.BytesIO(json.dumps(typed_response(request)).encode())


class JevAdapterTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {"TYPESAFE_API_KEY": "typesafe-test-key"}, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)
        self.packet = {"schema_version": "proofpress/judge-request/v1", "claim": {"id": "c1"},
                       "evidence": [], "evaluation": {"eligible": True}}

    def test_request_and_bounded_audit(self):
        requests = []
        def capture(request, timeout):
            requests.append(request)
            return opener(request, timeout)
        result = judge(self.packet, provider="typesafe", opener=capture)
        request = requests[0]
        self.assertEqual(request.full_url, jev.ENDPOINT)
        self.assertEqual(request.get_header("Authorization"), "Bearer typesafe-test-key")
        body = json.loads(request.data)
        self.assertEqual(body["model"], "jev-latest")
        self.assertNotIn("messages", body)
        self.assertEqual(result["recommendation"], "accept")
        self.assertIn("Template summary", result["rationale"])
        audit = jev.validate_audit(result["decision_audit"], "accept")
        self.assertEqual(audit["usage"]["input_tokens"], 125)
        self.assertNotIn("typesafe-test-key", json.dumps(audit))
        self.assertNotIn("state", audit)

    def test_uncertainty_and_criteria_are_not_acceptance(self):
        for choice, support, confidence, expected in [
            ("accept", .5, .95, "escalate"), ("accept", .99, .2, "escalate"),
            ("reject", .01, .95, "reject"), ("escalate", .99, .95, "escalate")]:
            with self.subTest(choice=choice, support=support):
                result = jev.judge(self.packet, opener=lambda r, timeout: io.BytesIO(
                    json.dumps(typed_response(r, choice, support, confidence)).encode()))
                self.assertEqual(result["recommendation"], expected)

    def test_invalid_response_never_records_advice(self):
        def invalid_kind(p): p["answers"]["item_0_recommendation"]["choice"] = "admit"
        def missing(p): p["answers"].pop("item_0_scope_valid")
        def nan(p): p["answers"]["item_0_scope_valid"]["noul"] = float("nan")
        def boolean(p): p["answers"]["item_0_scope_valid"]["noul"] = True
        def bad_sum(p): p["answers"]["item_0_recommendation"]["probabilities"]["reject"] = .9
        def wrong_type(p): p["answers"]["item_0_scope_valid"]["type"] = "choice"
        for mutate in (invalid_kind, missing, nan, boolean, bad_sum, wrong_type):
            def fake(request, timeout):
                payload = typed_response(request); mutate(payload)
                return io.BytesIO(json.dumps(payload).encode())
            with self.subTest(mutate=mutate.__name__), self.assertRaisesRegex(ValueError, "no recommendation recorded"):
                jev.judge(self.packet, opener=fake)

    def test_failed_checks_missing_key_and_oversize_make_no_call(self):
        no_call = lambda *a, **kw: self.fail("Network must not be used")
        with patch.dict(os.environ, {"PROOFPRESS_JUDGE_API_KEY": ""}):
            with self.assertRaisesRegex(ValueError, "API key"):
                jev.judge(self.packet, opener=no_call)
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "API key"):
                jev.judge(self.packet, opener=no_call)
        for packet in ({**self.packet, "evaluation": {"eligible": False}},
                       {**self.packet, "evidence": ["x" * 128_001]}):
            with self.assertRaises(ValueError):
                jev.judge(packet, opener=no_call)

    def test_upstream_errors_are_sanitized(self):
        for exc in (TimeoutError("secret private evidence"), RuntimeError("secret provider body")):
            with self.assertRaises(ValueError) as error:
                jev.judge(self.packet, opener=lambda *a, **kw: (_ for _ in ()).throw(exc))
            self.assertNotIn("secret", str(error.exception))
            self.assertTrue(error.exception.__suppress_context__)

    def test_workspace_key_wins_and_other_provider_keys_are_not_used(self):
        with patch.dict(os.environ, {"PROOFPRESS_JUDGE_API_KEY": "workspace-key"}):
            def check(request, timeout):
                self.assertEqual(request.get_header("Authorization"), "Bearer workspace-key")
                return opener(request, timeout)
            jev.judge(self.packet, opener=check)
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "wrong-provider"}, clear=True):
            with self.assertRaisesRegex(ValueError, "API key"):
                jev.judge(self.packet)

    def test_metadata_cannot_override_mapped_recommendation(self):
        result = jev.judge(self.packet, opener=opener)
        audit = copy.deepcopy(result["decision_audit"])
        audit["answers"]["scope_valid"]["noul"] = .2
        with self.assertRaisesRegex(ValueError, "Invalid typed judge audit"):
            kernel._decision_audit_fields({**result, "decision_audit": audit})

    def test_batch_is_one_request_with_complete_per_claim_audit(self):
        packet = {"schema_version": "proofpress/judge-batch-request/v1", "evidence_catalog": {},
                  "claims": [{"claim": {"id": str(i)}, "evidence_refs": [], "evaluation": {"eligible": True}}
                             for i in range(3)]}
        calls = []
        def capture(request, timeout):
            calls.append(request)
            return opener(request, timeout)
        result = jev.judge(packet, opener=capture)
        self.assertEqual(len(calls), 1)
        self.assertEqual([v["claim_id"] for v in result["verdicts"]], ["0", "1", "2"])
        for index, verdict in enumerate(result["verdicts"]):
            self.assertEqual(jev.validate_audit(verdict["decision_audit"], "accept")["item_index"], index)
        packet["claims"] *= 12
        with self.assertRaisesRegex(ValueError, "1 to 32"):
            jev.judge(packet, opener=lambda *a, **kw: self.fail("No provider call"))

    def test_cli_env_opt_in_is_explicit_and_bound(self):
        with patch.object(kernel, "POLICY_PATH", "/nonexistent-jev-test-policy"):
            initial = kernel.load_v2_policy()
            with patch.dict(os.environ, {"PROOFPRESS_JUDGE_PROVIDER": "typesafe", "PROOFPRESS_JUDGE_MODEL": "jev-latest"}):
                enabled = kernel.load_v2_policy()
        self.assertEqual(initial["judge"]["command"], [])
        self.assertIn("typesafe", enabled["judge"]["command"])
        self.assertNotEqual(initial["digest"], enabled["digest"])
        self.assertFalse(enabled["require_judge"])


class JevHostedTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.env = patch.dict(os.environ, {"PROOFPRESS_SECRET_ENCRYPTION_KEY": Fernet.generate_key().decode()}, clear=True)
        self.env.start(); self.addCleanup(self.env.stop)
        self.control = HostedControlPlane(Path(self.tmp.name) / "test.db")
        self.owner = self.control.bootstrap("workspace:jev-test", "human:test")["token"]
        self.agent = self.control.issue_agent_credential(self.owner, "agent:test", "Test")["token"]
        self.settings = {"provider": "typesafe", "model": "jev-latest", "endpoint": "", "criteria": "Require evidence.",
                         "zdr": False, "rubric": "evidence-support/v1", "mode": "manual",
                         "external_consent": True, "require_judge": False}
        self.control.save_review_policy(self.owner, self.settings, 0, "workspace-jev-key")
        self.calls = []

    def proposal(self, title="A"):
        evidence = self.control.execute(self.agent, operation("evidence.submit", {"payload": evidence_payload()}))
        result = self.control.execute(self.agent, operation("claim.propose", {
            "title": title, "statement": title, "scope": "jev-test", "proposer": "agent:test",
            "evidence_refs": evidence["result"]["evidence"]}))
        self.assertTrue(result["ok"], result)
        return result["result"]["claim"]["id"]

    def run_adapter(self, command, *, input, env, **kwargs):
        self.calls.append(json.loads(input))
        self.assertEqual(env["PROOFPRESS_JUDGE_API_KEY"], "workspace-jev-key")
        with patch.dict(os.environ, env, clear=True):
            result = judge(json.loads(input), provider="typesafe", model="jev-latest", opener=opener)
        return subprocess.CompletedProcess(command, 0, json.dumps(result), "")

    def execute(self, name, parameters):
        result = self.control.execute(self.agent, operation(name, parameters))
        self.assertTrue(result["ok"], result)
        return result["result"]

    def test_claim_advice_receipt_and_no_context_admission(self):
        cid = self.proposal()
        with patch.object(kernel.subprocess, "run", side_effect=self.run_adapter):
            self.execute("claim.judge", {"claim_id": cid})
        receipt = self.execute("review.receipt", {"claim_id": cid})
        self.assertEqual(receipt["state"], "needs_review")
        self.assertEqual(receipt["recommendation"]["decision_audit"]["backend"], "jev")
        context = self.execute("context.get", {"scope": "jev-test"})
        self.assertEqual(context["governed_context"], [])
        forbidden = self.control.execute(self.agent, operation("claim.review", {
            "claim_id": cid, "decision": "admit", "reviewer": "agent:test"}))
        self.assertFalse(forbidden["ok"])

    def test_relation_judge_includes_bound_evidence_without_quarantine(self):
        a, b = self.proposal("A"), self.proposal("B")
        # Synthetic owner admission in this temporary test database only.
        for cid in (a, b):
            self.control.execute(self.owner, operation("claim.review", {
                "claim_id": cid, "decision": "admit", "reviewer": "human:test"}))
        relation = self.execute("relation.propose", {"source_id": a, "target_id": b,
                                "relation_type": "contradicts", "proposer": "agent:test"})
        rid = relation["relation"]["id"]
        with patch.object(kernel.subprocess, "run", side_effect=self.run_adapter):
            verdict = self.execute("relation.judge", {"relation_id": rid})
        self.assertEqual(verdict["recommendation"], "accept")
        self.assertTrue(self.calls[-1]["evidence"])
        context = self.execute("context.get", {"scope": "jev-test"})
        self.assertEqual(len(context["governed_context"]), 2)
        self.assertEqual(context["relations"], [])
        admitted = self.control.execute(self.owner, operation("relation.review", {
            "relation_id": rid, "decision": "admit", "reviewer": "human:test"}))
        self.assertTrue(admitted["ok"], admitted)
        self.assertEqual(self.execute("context.get", {"scope": "jev-test"})["governed_context"], [])

    def test_batch_persists_audit_and_policy_changes_invalidate_advice(self):
        cid = self.proposal()
        self.proposal("B")
        with patch.object(kernel.subprocess, "run", side_effect=self.run_adapter):
            result = self.execute("claim.judge_batch", {"scope": "jev-test"})
        self.assertEqual(len(result["verdicts"]), 2)
        self.assertTrue(all(v["decision_audit"] for v in result["verdicts"]))
        self.control.save_review_policy(self.owner, {**self.settings, "criteria": "New criteria."}, 1)
        receipt = self.execute("review.receipt", {"claim_id": cid})
        self.assertFalse(receipt["review_policy"]["advice_current"])

    def test_automatic_queue_receives_workspace_key(self):
        self.control.save_review_policy(self.owner, {**self.settings, "mode": "automatic"}, 1)
        with patch("threading.Thread.start"):
            cid = self.proposal()
        with patch.object(kernel.subprocess, "run", side_effect=self.run_adapter):
            self.control.run_judge_jobs()
        receipt = self.execute("review.receipt", {"claim_id": cid})
        self.assertEqual(receipt["judge_job"]["state"], "completed")
        self.assertEqual(receipt["state"], "needs_review")

    def test_hosted_requires_consent_and_does_not_fall_back_to_local_key(self):
        with self.assertRaises(ValueError):
            self.control.save_review_policy(self.owner, {**self.settings, "external_consent": False}, 1)
        with self.control._db() as connection:
            review_policy.delete_credential(connection, "workspace:jev-test")
        cid = self.proposal()
        def missing(command, *, input, env, **kw):
            self.assertEqual(env["PROOFPRESS_JUDGE_API_KEY"], "")
            with patch.dict(os.environ, {**env, "TYPESAFE_API_KEY": "wrong-host-key"}, clear=True):
                with self.assertRaisesRegex(ValueError, "API key"):
                    jev.judge(json.loads(input), opener=lambda *a, **kw: self.fail("No host fallback"))
            return subprocess.CompletedProcess(command, 1, "", "Advisory judge failed")
        with patch.object(kernel.subprocess, "run", side_effect=missing):
            result = self.control.execute(self.agent, operation("claim.judge", {"claim_id": cid}))
        self.assertFalse(result["ok"])
        receipt = self.execute("review.receipt", {"claim_id": cid})
        self.assertFalse(receipt.get("recommendation"))

    def test_cycles_remain_blocked_and_duplicate_proposals_do_not_add_edges(self):
        a, b = self.proposal("A"), self.proposal("B")
        params = {"source_id": a, "target_id": b, "relation_type": "depends_on", "proposer": "agent:test"}
        first = self.execute("relation.propose", params)
        repeated = self.execute("relation.propose", params)
        self.assertEqual(first["relation"]["id"], repeated["relation"]["id"])
        reverse = self.execute("relation.propose", {**params, "source_id": b, "target_id": a})
        rid = reverse["relation"]["id"]
        evaluation = self.execute("relation.evaluate", {"relation_id": rid})
        self.assertFalse(evaluation["checks"]["acyclic_when_directed"])
        with patch.object(kernel.subprocess, "run", side_effect=self.run_adapter):
            result = self.control.execute(self.agent, operation("relation.judge", {"relation_id": rid}))
        self.assertFalse(result["ok"])
        self.assertFalse(self.control.execute(self.owner, operation("relation.review", {
            "relation_id": rid, "decision": "admit", "reviewer": "human:test"}))["ok"])
        with patch.object(kernel.subprocess, "run") as run:
            result = self.control.execute(self.agent, operation("relation.propose", {**params, "relation_type": "none"}))
        self.assertFalse(result["ok"])
        run.assert_not_called()

"""Network-free TypeSafe transport, credential isolation and governance regression tests."""
import copy
import hashlib
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


def typed_response(request, choice="accept", support=.99, confidence=.95, relation_choice=None,
                   relation_confidence=None):
    body = json.loads(request.data)
    answers = {}
    for key, question in body["questions"].items():
        if question["type"] == "choice":
            selected = (relation_choice if relation_choice is not None else next(iter(question["criteria"]))) \
                if key.endswith("_relation_type") else choice
            selected_confidence = (relation_confidence if relation_confidence is not None else confidence) \
                if key.endswith("_relation_type") else confidence
            probabilities = {v: .02 / (len(question["criteria"]) - 1)
                             for v in question["criteria"]}
            probabilities[selected] = .98
            answers[key] = {"type": "choice", "choice": selected,
                            "probabilities": probabilities,
                            "confidence": selected_confidence}
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

    def test_relation_citation_limits_the_evidence_support_question(self):
        quote = "The limitation does not apply to fraud."
        citation = {"quote": quote, "locator": {"kind": "text_span", "start": 0,
                    "end": len(quote)}, "quote_digest": "sha256:" + hashlib.sha256(
                        quote.encode("utf-8")).hexdigest()}
        questions = jev.questions_for({"relation": {"type": "qualifies"}, "relation_citation": citation})
        self.assertIn("named relation citation quote", questions["evidence_support"]["instructions"])
        self.assertIn("rather than any other supplied evidence", questions["evidence_support"]["instructions"])
        self.assertEqual(questions["relation_type"]["type"], "choice")
        self.assertEqual(questions["relation_type"]["criteria"], jev.RELATION_TYPE_CRITERIA)
        with self.assertRaisesRegex(ValueError, "invalid relation citation packet"):
            jev.questions_for({"relation": {"type": "qualifies"},
                               "relation_citation": {**citation, "quote_digest": "sha256:bad"}})

    def test_relation_citation_choice_never_rewrites_a_relation(self):
        quote = "The exclusion narrows the general liability cap."
        citation = {"quote": quote, "locator": {"kind": "text_span", "start": 0, "end": len(quote)},
                    "quote_digest": "sha256:" + hashlib.sha256(quote.encode("utf-8")).hexdigest()}
        packet = {"schema_version": "proofpress/relation-judge-request/v1",
                  "relation": {"id": "r1", "from": "c1", "to": "c2", "type": "qualifies"},
                  "from_claim": {"id": "c1"}, "to_claim": {"id": "c2"}, "evidence": [],
                  "relation_citation": citation, "evaluation": {"eligible": True}}

        def response(*, generic="accept", relation_choice="qualifies", relation_confidence=.95):
            return lambda request, timeout: io.BytesIO(json.dumps(typed_response(
                request, generic, relation_choice=relation_choice,
                relation_confidence=relation_confidence)).encode())

        accepted = jev.judge(packet, opener=response())
        audit = jev.validate_audit(accepted["decision_audit"], "accept")
        self.assertEqual(audit["question_set_version"], jev.RELATION_TYPE_QUESTION_VERSION)
        self.assertEqual(audit["mapping_version"], jev.RELATION_TYPE_MAPPING_VERSION)
        self.assertEqual(audit["declared_relation_type"], "qualifies")
        with self.assertRaisesRegex(ValueError, "Invalid typed judge audit"):
            jev.validate_audit(accepted["decision_audit"], "accept", "supports")

        different_type = jev.judge(packet, opener=response(relation_choice="supports"))
        self.assertEqual(different_type["recommendation"], "escalate")
        self.assertEqual(different_type["decision_audit"]["declared_relation_type"], "qualifies")

        no_relation = jev.judge(packet, opener=response(generic="reject", relation_choice="no_relation"))
        self.assertEqual(no_relation["recommendation"], "reject")
        self.assertEqual(jev.judge(packet, opener=response(relation_choice="insufficient"))["recommendation"],
                         "escalate")
        self.assertEqual(jev.judge(packet, opener=response(relation_confidence=.2))["recommendation"],
                         "escalate")

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
    provider = "typesafe"
    model = "jev-latest"
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.env = patch.dict(os.environ, {"PROOFPRESS_SECRET_ENCRYPTION_KEY": Fernet.generate_key().decode()}, clear=True)
        self.env.start(); self.addCleanup(self.env.stop)
        self.control = HostedControlPlane(Path(self.tmp.name) / "test.db")
        self.owner = self.control.bootstrap("workspace:jev-test", "human:test")["token"]
        self.agent = self.control.issue_agent_credential(self.owner, "agent:test", "Test")["token"]
        self.settings = {"provider": self.provider, "model": self.model, "endpoint": "", "criteria": "Require evidence.",
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
        if command[0] == "node":
            from urllib.request import Request
            response = typed_response(Request(jev.ENDPOINT, data=input))
            response["model"] = self.model
            return subprocess.CompletedProcess(command, 0, json.dumps(response).encode(), b"")
        self.calls.append(json.loads(input))
        self.assertEqual(env["PROOFPRESS_JUDGE_API_KEY"], "workspace-jev-key")
        with patch.dict(os.environ, env, clear=True):
            result = judge(json.loads(input), provider=self.provider, model=self.model, opener=opener)
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
            with patch.dict(os.environ, {**env, "TYPESAFE_API_KEY": "wrong-host-key", "AI_GATEWAY_API_KEY": "wrong-host-key"}, clear=True):
                with self.assertRaisesRegex(ValueError, "API key"):
                    jev.judge(json.loads(input), gateway=self.provider == "vercel_jev", opener=lambda *a, **kw: self.fail("No host fallback"))
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

class JevGatewayTests(unittest.TestCase):
    def setUp(self):
        self.packet = {"schema_version": "proofpress/judge-request/v1", "claim": {"id": "c1"},
                       "evidence": [], "evaluation": {"eligible": True}}

    def test_gateway_transport_and_audit(self):
        def bridge(args, **kwargs):
            self.assertEqual(args[0], "node")
            self.assertEqual(kwargs["env"]["PROOFPRESS_JUDGE_API_KEY"], "workspace-key")
            self.assertEqual(kwargs["timeout"], 50)
            wire = json.loads(kwargs["input"])
            self.assertEqual(wire["model"], "typesafe-ai/jev")
            self.assertEqual(wire["questions"]["item_0_scope_valid"]["type"], "boolean")
            self.assertEqual(wire["providerOptions"], {"gateway": {"zeroDataRetention": True}})
            from urllib.request import Request
            response = typed_response(Request(jev.ENDPOINT, data=kwargs["input"]))
            response["model"] = "typesafe-ai/jev"
            return subprocess.CompletedProcess(args, 0, stdout=json.dumps(response).encode())
        with patch.dict(os.environ, {"PROOFPRESS_JUDGE_API_KEY": "workspace-key", "AI_GATEWAY_API_KEY": "host-key"}), patch.object(jev.subprocess, "run", side_effect=bridge):
            result = judge(self.packet, provider="vercel_jev", zdr=True)
        audit = jev.validate_audit(result["decision_audit"], result["recommendation"])
        self.assertEqual(audit["transport"]["response_model_source"], "gateway-route")
        self.assertEqual(audit["schema_version"], "proofpress/decision-audit/v2")
        tampered = copy.deepcopy(audit); tampered["transport"]["sdk"] = "unknown"
        with self.assertRaises(ValueError): jev.validate_audit(tampered, result["recommendation"])

    def test_no_workspace_key_never_uses_host_gateway_key(self):
        with patch.dict(os.environ, {"PROOFPRESS_JUDGE_API_KEY": "", "AI_GATEWAY_API_KEY": "host-key"}), patch.object(jev.subprocess, "run") as run:
            with self.assertRaisesRegex(ValueError, "API key"):
                judge(self.packet, provider="vercel_jev")
            run.assert_not_called()

    def test_transport_failure_is_sanitized_and_does_not_fallback(self):
        for error in (FileNotFoundError("node"), subprocess.TimeoutExpired("node", 50),
                      subprocess.CalledProcessError(1, "node", stderr=b"secret provider response")):
            with patch.dict(os.environ, {"AI_GATEWAY_API_KEY": "test"}, clear=True), patch.object(jev.subprocess, "run", side_effect=error) as run:
                with self.assertRaisesRegex(ValueError, "no recommendation recorded") as caught:
                    judge(self.packet, provider="vercel_jev")
                self.assertNotIn("secret", str(caught.exception)); self.assertEqual(run.call_count, 1)


class JevGatewayHostedTests(JevHostedTests):
    provider = "vercel_jev"
    model = "typesafe-ai/jev"

    def test_gateway_policy_binds_zdr_and_rejects_other_models(self):
        with self.control._db() as connection:
            prior = review_policy.current(connection, "workspace:jev-test")["policy"]
        enabled = review_policy.validate({**self.settings, "zdr": True}, prior)
        self.assertIn("--zdr", enabled["judge"]["command"])
        self.assertTrue(enabled["data_handling"]["zero_data_retention"])
        self.assertNotEqual(enabled["digest"], prior["digest"])
        with self.assertRaisesRegex(ValueError, "typesafe-ai/jev"):
            review_policy.validate({**self.settings, "model": "other/model"}, prior)

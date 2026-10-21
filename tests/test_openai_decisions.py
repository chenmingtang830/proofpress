import copy
import io
import json
import os
import unittest
from unittest.mock import patch

from proofpress.hosted import decisions, review_policy
from proofpress.hosted.judge import judge, JudgeFailure
import test_hosted_review_policy as policy_tests


class DecisionsTests(unittest.TestCase):
    def setUp(self):
        self.packet = {"schema_version": "proofpress/judge-request/v1", "evaluation": {"eligible": True}, "claim": {"statement": "Synthetic claim"}}
        self.payload = {"answers": [{"name": name, "type": "predicate", "probability": .95} for name in decisions.QUESTIONS]}

    def test_typed_endpoint_and_advisory_mapping(self):
        def opener(request, timeout):
            self.assertEqual(request.full_url, decisions.ENDPOINT)
            body = json.loads(request.data)
            self.assertEqual(body["model"], "gpt-6-luna")
            self.assertNotIn("messages", body)
            self.assertEqual(len(body["questions"]), 3)
            self.assertEqual(timeout, 45)
            return io.BytesIO(json.dumps(self.payload).encode())
        with patch.dict(os.environ, {"PROOFPRESS_JUDGE_API_KEY": "synthetic-openai-key"}):
            result = judge(self.packet, provider="openai_decisions", opener=opener)
        self.assertEqual(result["recommendation"], "accept")
        self.assertIn("uncalibrated", result["rationale"])
        self.assertNotIn("decision_audit", result)  # Never mislabel these as Jev answers.

    def test_refusal_and_uncertainty_escalate(self):
        self.payload["answers"][0]["probability"] = .5
        self.assertEqual(decisions.interpret(self.payload)["recommendation"], "escalate")
        self.payload["answers"][0] = {"name": "evidence_support", "type": "refusal"}
        self.assertEqual(decisions.interpret(self.payload)["recommendation"], "escalate")

    def test_malformed_answers_fail_closed(self):
        variants = [{}, {"answers": []}]
        for value in [True, None, -1, 1.1, float("nan"), float("inf"), "0.99"]:
            bad = copy.deepcopy(self.payload)
            bad["answers"][0]["probability"] = value
            variants.append(bad)
        for field, value in [("name", "unknown"), ("name", "scope_valid"), ("name", []), ("type", "choice")]:
            bad = copy.deepcopy(self.payload)
            bad["answers"][0][field] = value
            variants.append(bad)
        for payload in variants:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                decisions.interpret(payload)

    def test_no_key_fallback_or_wrong_endpoint_or_ineligible_call(self):
        with patch.dict(os.environ, {"PROOFPRESS_JUDGE_API_KEY": "", "OPENAI_API_KEY": "do-not-use", "GMI_API_KEY": "do-not-use"}):
            with self.assertRaises(JudgeFailure):
                judge(self.packet, provider="openai_decisions")
        with self.assertRaises(JudgeFailure):
            decisions.judge(self.packet, endpoint="https://elsewhere.example/v1/decisions")
        with self.assertRaises(JudgeFailure):
            decisions.judge({**self.packet, "evaluation": {"eligible": False}})


class ManagedPolicyTests(unittest.TestCase):
    setUp = policy_tests.ReviewPolicyTests.setUp

    def managed(self, **overrides):
        return {**self.settings, "provider": "managed_openai_decisions", "model": "gpt-6-luna", "require_judge": False, **overrides}

    def test_hosted_opt_in_requires_separate_operator_key(self):
        with patch.dict(os.environ, {"PROOFPRESS_MANAGED_OPENAI_API_KEY": "", "GMI_API_KEY": "not-openai"}):
            with self.assertRaisesRegex(ValueError, "not configured yet"):
                self.control.save_review_policy(self.owner, self.managed(), 0)
        with patch.dict(os.environ, {"PROOFPRESS_MANAGED_OPENAI_API_KEY": "synthetic-platform-key"}):
            with self.assertRaisesRegex(ValueError, "consent"):
                self.control.save_review_policy(self.owner, self.managed(external_consent=False), 0)
            saved = self.control.save_review_policy(self.owner, self.managed(), 0)
            self.assertTrue(saved["credential"]["configured"])
            self.assertIsNone(saved["credential"]["last_four"])
            self.assertNotIn("synthetic-platform-key", json.dumps(saved))
            self.assertFalse(saved["settings"]["auto_admit_new_claims"])
            with self.assertRaisesRegex(ValueError, "API key"):
                self.control.save_review_policy(self.owner, {**self.settings, "provider": "openai_decisions", "model": "gpt-6-luna"}, 1)

    def test_managed_is_not_a_byok_fallback_and_cannot_auto_approve(self):
        with patch.dict(os.environ, {"PROOFPRESS_MANAGED_OPENAI_API_KEY": "synthetic-platform-key"}):
            with self.control._db() as connection:
                self.assertIsNone(review_policy.credential(connection, "workspace:test", "openai_decisions"))
            with self.assertRaisesRegex(ValueError, "human approval"):
                self.control.save_review_policy(self.owner, self.managed(mode="automatic", require_judge=True, auto_admit_new_claims=True), 0)
            with self.assertRaisesRegex(ValueError, "operator's key"):
                self.control.save_review_policy(self.owner, self.managed(), 0, api_key="wrong-provider-key")

    def test_default_does_not_enable_processing(self):
        settings = review_policy.initial_workspace_policy()["settings"]
        self.assertEqual(settings["provider"], "managed_openai_decisions")
        self.assertEqual(settings["mode"], "off")
        self.assertFalse(settings["external_consent"])

    def test_new_manual_workspace_does_not_require_unused_provider_key(self):
        self.control.legacy_default_workspace_id = None
        saved = self.control.save_review_policy(self.owner, {
            **self.settings, "mode": "off", "external_consent": False, "require_judge": False}, 0)
        self.assertEqual(saved["settings"]["mode"], "off")
        self.assertFalse(saved["credential"]["configured"])

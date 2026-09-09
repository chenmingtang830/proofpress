import io
import json
import os
import unittest
from unittest.mock import patch

from proofpress.hosted.judge import DEFAULT_MODEL, judge
from proofpress.kernel import operations


class OpenRouterJudgeTests(unittest.TestCase):
    def response(self, verdict):
        return io.BytesIO(json.dumps({"choices": [{"message": {"content": json.dumps(verdict)}}]}).encode())

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-only"})
    def test_model_and_advisory_verdict(self):
        requests = []
        def opener(request, timeout):
            requests.append(json.loads(request.data))
            return self.response({"recommendation": "accept", "rationale": "Evidence ev_1 supports this bound assertion."})
        result = judge({"claim": {"id": "c1"}, "evidence": []}, opener=opener)
        self.assertEqual(requests[0]["model"], "deepseek/deepseek-v4-flash")
        self.assertEqual(result["model"], DEFAULT_MODEL)
        self.assertEqual(set(result), {"recommendation", "rationale", "adapter", "model"})

    @patch.dict(os.environ, {"PROOFPRESS_JUDGE_API_KEY": "azure-test-only"})
    def test_azure_openai_uses_tenant_endpoint_and_api_key_header(self):
        requests = []
        def opener(request, timeout):
            requests.append(request)
            return self.response({"recommendation": "escalate", "rationale": "Evidence is incomplete."})
        endpoint = "https://customer.openai.azure.com/openai/v1/chat/completions"
        result = judge({}, model="gpt-5.4", provider="azure_openai", endpoint=endpoint, opener=opener)
        self.assertEqual(requests[0].full_url, endpoint)
        self.assertEqual(requests[0].get_header("Api-key"), "azure-test-only")
        self.assertIsNone(requests[0].get_header("Authorization"))
        payload = json.loads(requests[0].data)
        self.assertEqual(payload["max_completion_tokens"], 1800)
        self.assertNotIn("max_tokens", payload)
        self.assertEqual(result["adapter"], "proofpress-azure_openai-judge/v1")

    @patch.dict(os.environ, {"PROOFPRESS_JUDGE_API_KEY": "openai-test-only"})
    def test_openai_gpt5_uses_completion_token_limit(self):
        requests = []
        def opener(request, timeout):
            requests.append(request)
            return self.response({"recommendation": "accept", "rationale": "Evidence ev_1 supports the claim."})
        judge({}, model="gpt-5.4", provider="openai", opener=opener)
        payload = json.loads(requests[0].data)
        self.assertEqual(payload["max_completion_tokens"], 1800)
        self.assertNotIn("max_tokens", payload)
        self.assertEqual(requests[0].get_header("Authorization"), "Bearer openai-test-only")

    @patch.dict(os.environ, {"PROOFPRESS_JUDGE_API_KEY": "gemini-test-only"})
    def test_openai_compatible_provider_uses_registered_endpoint(self):
        requests = []
        def opener(request, timeout):
            requests.append(request)
            return self.response({"recommendation": "accept", "rationale": "Evidence ev_1 supports the claim."})
        judge({}, model="gemini-3.8-flash", provider="google_gemini", opener=opener)
        self.assertEqual(requests[0].full_url, "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions")
        self.assertEqual(requests[0].get_header("Authorization"), "Bearer gemini-test-only")

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-only"})
    def test_invalid_verdict_fails_closed(self):
        for verdict in [{"recommendation": "admit", "rationale": "approve"}, {}, [],
                        {"recommendation": "accept", "rationale": ""}]:
            with self.subTest(verdict=verdict), self.assertRaisesRegex(ValueError, "no recommendation recorded"):
                judge({}, opener=lambda *a, **kw: self.response(verdict))

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-only"})
    def test_upstream_error_does_not_expose_provider_body(self):
        def failed(*a, **kw):
            raise RuntimeError("test-only private provider body")
        with self.assertRaises(ValueError) as error:
            judge({}, opener=failed)
        self.assertNotIn("test-only", str(error.exception))

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-only"})
    def test_no_silent_input_truncation(self):
        with self.assertRaisesRegex(ValueError, "bounded input limit"):
            judge({"evidence": "x" * 128_001}, opener=lambda *a, **kw: self.fail("No provider call allowed"))

    @patch.dict(os.environ, {"PROOFPRESS_JUDGE_MODEL": ""})
    @patch.object(operations, "POLICY_PATH", "/nonexistent-proofpress-test-policy")
    def test_opt_in_is_digest_bound_and_not_required(self):
        initial = operations.load_v2_policy()
        with patch.dict(os.environ, {"PROOFPRESS_JUDGE_MODEL": DEFAULT_MODEL}):
            configured = operations.load_v2_policy()
        self.assertEqual(initial["judge"]["command"], [])
        self.assertNotEqual(initial["digest"], configured["digest"])
        self.assertFalse(configured["require_judge"])
        self.assertEqual(configured["judge"]["command"][-1], DEFAULT_MODEL)


if __name__ == "__main__":
    unittest.main()

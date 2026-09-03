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
        result = judge({"conclusion": {"id": "c1"}, "evidence": []}, opener=opener)
        self.assertEqual(requests[0]["model"], "deepseek/deepseek-v4-flash")
        self.assertEqual(result["model"], DEFAULT_MODEL)
        self.assertEqual(set(result), {"recommendation", "rationale", "adapter", "model"})

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

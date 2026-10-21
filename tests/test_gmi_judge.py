import io
import json
import os
import unittest
from unittest.mock import patch

from proofpress.hosted.judge import JudgeFailure, judge


class GmiJudgeTests(unittest.TestCase):
    def test_chat_request_contract_uses_json_and_never_truncates(self):
        def opener(request, timeout):
            self.assertEqual(request.full_url, "https://api.gmi-serving.com/v1/chat/completions")
            self.assertEqual(request.get_header("Authorization"), "Bearer synthetic-gmi-key")
            self.assertEqual(request.get_header("User-agent"), "Proofpress/1.0")
            body = json.loads(request.data)
            self.assertEqual(body["model"], "openai/gpt-6-luna")
            self.assertEqual(body["context_length_exceeded_behavior"], "error")
            self.assertEqual(body["response_format"], {"type": "json_object"})
            self.assertEqual(body["max_completion_tokens"], 1800)
            self.assertNotIn("questions", body)
            return io.BytesIO(json.dumps({"choices": [{"message": {"content": json.dumps({
                "recommendation": "escalate", "rationale": "Synthetic sample lacks evidence."})}}]}).encode())

        with patch.dict(os.environ, {"PROOFPRESS_JUDGE_API_KEY": "synthetic-gmi-key"}):
            result = judge({"claim": {"statement": "Synthetic sample"}}, provider="managed_gmi", opener=opener)
        self.assertEqual(result["recommendation"], "escalate")
        self.assertNotIn("decision_audit", result)

    def test_cannot_redirect_operator_key_or_silently_change_model(self):
        for kwargs in [{"endpoint": "https://elsewhere.example/chat"}, {"model": "another-model"}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(JudgeFailure):
                judge({}, provider="managed_gmi", **kwargs)

    def test_does_not_borrow_another_provider_key(self):
        with patch.dict(os.environ, {"PROOFPRESS_JUDGE_API_KEY": "", "OPENROUTER_API_KEY": "not-gmi", "OPENAI_API_KEY": "not-gmi"}):
            with self.assertRaises(JudgeFailure):
                judge({}, provider="managed_gmi")

    def test_invalid_json_does_not_record_advice(self):
        with patch.dict(os.environ, {"PROOFPRESS_JUDGE_API_KEY": "synthetic-gmi-key"}):
            with self.assertRaises(JudgeFailure):
                judge({}, provider="managed_gmi", opener=lambda *a, **kw: io.BytesIO(b'{"choices": []}'))

import json
import os
import unittest

from proofpress.hosted import assistant


class OwnerAssistantTests(unittest.TestCase):
    def setUp(self):
        os.environ.pop("OPENROUTER_API_KEY", None)
        os.environ.pop("OPENROUTER_MODEL", None)

    def test_refuses_to_call_upstream_without_a_key(self):
        result = assistant.ask("What needs review?", {"page": "review"})
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "assistant_unconfigured")

    def test_rejects_an_empty_question(self):
        os.environ["OPENROUTER_API_KEY"] = "sk-or-test"
        result = assistant.ask("   ", {"page": "review"})
        self.assertEqual(result["error"]["code"], "invalid_request")

    def test_uses_explicit_production_default_and_allows_override(self):
        self.assertEqual(assistant.model_name(), "openai/gpt-5.4-mini")
        os.environ["OPENROUTER_MODEL"] = "openai/gpt-5.4"
        self.assertEqual(assistant.model_name(), "openai/gpt-5.4")

    def test_sends_snapshot_and_returns_model_text(self):
        os.environ["OPENROUTER_API_KEY"] = "sk-or-test"
        captured = {}

        class FakeResponse:
            def read(self):
                return b'{"model":"openai/gpt-4o-mini","choices":[{"message":{"content":"3 items need review. I cannot admit them."}}]}'

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        def fake_open(request, timeout=0):
            captured["auth"] = request.headers["Authorization"]
            captured["body"] = request.data.decode()
            return FakeResponse()

        result = assistant.ask(
            "What should I worry about before approving?",
            {"page": "review", "pending": [{"id": "c1"}]},
            opener=fake_open,
        )
        self.assertTrue(result["ok"])
        self.assertFalse(result["result"]["can_admit"])
        self.assertIn("cannot admit", result["result"]["answer"])
        self.assertTrue(captured["auth"].startswith("Bearer sk-or-test"))
        payload = json.loads(captured["body"])
        user = payload["messages"][1]["content"]
        self.assertIn("What should I worry about before approving?", user)
        snapshot = json.loads(
            user.split("Workspace snapshot:\n", 1)[1].split("\n\nOwner question:", 1)[0]
        )
        self.assertEqual(snapshot["pending"][0]["id"], "c1")


if __name__ == "__main__":
    unittest.main()

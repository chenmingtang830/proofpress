import copy
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def retrieval_payload():
    quote = "The liability cap is one year of fees."
    return {
        "schema_version": "proofpress/retrieval-evidence/v1",
        "source": {"uri": "workspace://msa.pdf",
                   "content_digest": "sha256:" + "a" * 64},
        "evidence": {"quote": quote, "locator": {
            "kind": "text_span", "start": 0, "end": len(quote),
            "text_digest": "sha256:" + hashlib.sha256(quote.encode()).hexdigest()}},
        "retrieval": {"adapter": "test", "version": "1", "query": "cap?",
                      "config_digest": "sha256:" + "b" * 64},
    }


class EventStoreTests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"],
                       cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"],
                       cwd=self.repo, check=True)
        sys.path.insert(0, str(ROOT))
        from proofpress.kernel import events as proofpress_event_store
        from proofpress.kernel import operations as proofpress_knowledge
        self.store = proofpress_event_store
        self.knowledge = proofpress_knowledge
        self.original_now = self.knowledge.now
        self.knowledge.now = lambda: "2026-08-31T00:00:00Z"
        self.previous = Path.cwd()
        os.chdir(self.repo)

    def tearDown(self):
        self.knowledge.now = self.original_now
        os.chdir(self.previous)
        self.tmp.cleanup()

    def lifecycle(self):
        imported = self.knowledge.submit_evidence_v2(retrieval_payload())
        proposed = self.knowledge.propose_v2(
            "The liability cap is one year of fees.",
            [imported["evidence"][0]], "store-parity", "agent:test")
        self.knowledge.evaluate_v2(proposed["conclusion"]["id"])
        self.knowledge.review_v2(
            proposed["conclusion"]["id"], "admit", "human:owner")
        return self.knowledge.context_v2("store-parity", "agent:next")

    def test_memory_and_git_backends_preserve_lifecycle_results(self):
        git_context = self.lifecycle()
        git_events = self.knowledge.v2_events()
        memory = self.store.MemoryEventStore()
        with self.store.using_event_store(memory):
            memory_context = self.lifecycle()
            memory_events = self.knowledge.v2_events()
        memory_context.pop("ledger_head")
        git_context.pop("ledger_head")
        self.assertEqual(memory_context, git_context)
        without_commit = lambda rows: [
            {key: value for key, value in row.items() if key != "commit"}
            for row in rows]
        self.assertEqual(without_commit(memory_events), without_commit(git_events))

    def test_history_envelope_is_portable_and_tamper_evident(self):
        self.lifecycle()
        envelopes = self.store.history_envelopes(self.knowledge.v2_events())
        verified = self.store.verify_history_envelopes(envelopes)
        self.assertTrue(verified["ok"])
        self.assertEqual(verified["events"], len(envelopes))
        tampered = copy.deepcopy(envelopes)
        tampered[0]["payload"]["type"] = "tampered"
        result = self.store.verify_history_envelopes(tampered)
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "invalid_payload_digest")

    def test_memory_store_rejects_a_stale_append(self):
        memory = self.store.MemoryEventStore()
        memory.append({"event_id": "one"}, message="one", expected_head=None)
        with self.assertRaisesRegex(ValueError, "STALE_EVENT_STORE_HEAD"):
            memory.append({"event_id": "two"}, message="two", expected_head=None)


if __name__ == "__main__":
    unittest.main()

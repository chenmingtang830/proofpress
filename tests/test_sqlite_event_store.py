import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest


ROOT = Path(__file__).resolve().parents[1]


def evidence_payload():
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


class SQLiteEventStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        sys.path.insert(0, str(ROOT))
        from proofpress.kernel import events as proofpress_event_store
        from proofpress.kernel import operations as proofpress_knowledge
        self.event_store = proofpress_event_store
        self.knowledge = proofpress_knowledge
        self.store = proofpress_event_store.SQLiteEventStore(
            self.root / "hosted.db", "workspace:personal", "agent:device-a")

    def tearDown(self):
        self.tmp.cleanup()

    def request(self, operation, parameters, key=None):
        request = {"schema_version": self.knowledge.LOCAL_OPERATION_SCHEMA,
                   "operation": operation, "parameters": parameters}
        if key:
            request["idempotency_key"] = key
        with self.event_store.using_event_store(self.store):
            return self.knowledge.execute_local_operation(request)

    def test_operation_events_and_idempotency_commit_together(self):
        first = self.request("evidence.submit", {"payload": evidence_payload()},
                             "evidence-001")
        self.assertTrue(first["ok"])
        event_count = len(self.store.list_events())
        replay = self.request("evidence.submit", {"payload": evidence_payload()},
                              "evidence-001")
        self.assertTrue(replay["ok"])
        self.assertTrue(replay["idempotent_replay"])
        self.assertEqual(len(self.store.list_events()), event_count)

        changed = evidence_payload()
        changed["retrieval"]["query"] = "different"
        conflict = self.request("evidence.submit", {"payload": changed},
                                "evidence-001")
        self.assertFalse(conflict["ok"])
        self.assertEqual(conflict["error"]["code"], "idempotency_conflict")
        self.assertEqual(len(self.store.list_events()), event_count)

    def test_transaction_rolls_back_partial_history(self):
        event = {"schema_version": "proofpress/knowledge-event/v2",
                 "type": "test", "event_id": "ppe_test"}
        with self.assertRaisesRegex(RuntimeError, "fault after append"):
            with self.store.transaction():
                self.store.append(event, message="test", expected_head=None)
                raise RuntimeError("fault after append")
        self.assertEqual(self.store.list_events(), [])
        self.assertIsNone(self.store.head())

    def test_competing_expected_heads_allow_one_append(self):
        barrier = threading.Barrier(2)
        outcomes = []

        def append(index):
            barrier.wait()
            try:
                outcomes.append(self.store.append(
                    {"event_id": f"event-{index}", "type": "test"},
                    message="test", expected_head=None)["event_id"])
            except ValueError as exc:
                outcomes.append(str(exc))

        threads = [threading.Thread(target=append, args=(index,)) for index in (1, 2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(len(self.store.list_events()), 1)
        self.assertEqual(outcomes.count("STALE_EVENT_STORE_HEAD"), 1)

    def test_workspace_and_principal_scope_are_isolated(self):
        other_principal = self.event_store.SQLiteEventStore(
            self.store.path, self.store.workspace_id, "agent:device-b")
        other_workspace = self.event_store.SQLiteEventStore(
            self.store.path, "workspace:other", "agent:device-a")
        self.request("evidence.submit", {"payload": evidence_payload()}, "same-key")
        with self.event_store.using_event_store(other_principal):
            result = self.knowledge.execute_local_operation({
                "schema_version": self.knowledge.LOCAL_OPERATION_SCHEMA,
                "operation": "evidence.submit",
                "parameters": {"payload": evidence_payload()},
                "idempotency_key": "same-key"})
        self.assertTrue(result["ok"])
        self.assertEqual(len(other_workspace.list_events()), 0)

    def test_export_and_backup_are_self_consistent(self):
        self.request("evidence.submit", {"payload": evidence_payload()}, "export-1")
        bundle = self.store.export_bundle()
        self.assertTrue(bundle["verification"]["ok"])
        backup = self.store.backup_to(self.root / "backup.db")
        connection = sqlite3.connect(backup)
        try:
            count = connection.execute(
                "SELECT COUNT(*) FROM events WHERE workspace_id = ?",
                (self.store.workspace_id,)).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(count, len(self.store.list_events()))


if __name__ == "__main__":
    unittest.main()

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/run_claim_construction_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("claim_construction_runner", PATH)
runner = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(runner)


class GatewayStartupTimeoutTests(unittest.TestCase):
    def test_readiness_read_is_bounded(self):
        proc = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(2)"],
            stdout=subprocess.PIPE,
            text=True,
        )
        try:
            with self.assertRaisesRegex(TimeoutError, "readiness"):
                runner._read_ready_line(proc.stdout, 0.01)
        finally:
            proc.terminate()
            proc.wait(timeout=2)
            proc.stdout.close()

    def test_durable_receipts_and_attempt_journal_survive_a_new_gateway_instance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            receipt_path = root / "terminal-receipts" / "compiler.jsonl"
            first = object.__new__(runner.Gateway)
            first._durable_receipt_path = receipt_path
            first._attempt_journal_path = receipt_path.with_name("compiler-attempts.jsonl")
            first._lock = __import__("threading").Lock()
            first._receipt_path = receipt_path
            first._append_attempt_event({"event": "attempt_started", "attempt_id": "attempt-000001",
                                         "request_digest": "sha256:request"})
            receipt_path.parent.mkdir(parents=True, exist_ok=True)
            receipt_path.write_text('{"terminal":true,"attempt_id":"attempt-000001","cost_usd":0.1}\n')
            self.assertEqual(first.attempt_count(), 1)
            self.assertEqual(first.receipt_rows()[0]["attempt_id"], "attempt-000001")

            resumed = object.__new__(runner.Gateway)
            resumed._durable_receipt_path = receipt_path
            resumed._attempt_journal_path = first._attempt_journal_path
            resumed._lock = __import__("threading").Lock()
            resumed._receipt_path = receipt_path
            self.assertEqual(resumed.attempt_count(), 1)
            self.assertEqual(resumed.receipt_rows()[0]["terminal"], True)


if __name__ == "__main__":
    unittest.main()

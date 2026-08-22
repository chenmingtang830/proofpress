import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "proofpress.py"
FIXTURE = ROOT / "examples" / "verified-knowledge-ledger" / "demo.otlp.json"


class KnowledgeLedgerTests(unittest.TestCase):
    def run_cli(self, *args, check=True):
        result = subprocess.run(["python3", str(CLI), *args], cwd=ROOT,
                                text=True, capture_output=True)
        if check and result.returncode:
            self.fail(f"command failed: {result.args}\n{result.stdout}\n{result.stderr}")
        return result

    def test_otlp_to_reviewed_context_flow(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "ledger.json"
            result = self.run_cli("knowledge", "ingest", str(FIXTURE), "-o", str(ledger))
            summary = json.loads(result.stdout)
            self.assertEqual(summary["source_events"], 3)
            self.assertEqual(summary["experiments"], 3)
            self.assertEqual(summary["claims"], 3)

            data = json.loads(ledger.read_text())
            claims = {claim["support"]["experiment_status"]: claim for claim in data["claims"]}
            self.assertTrue(claims["complete"]["gate"]["eligible"])
            self.assertFalse(claims["failed"]["gate"]["eligible"])

            accepted = claims["complete"]["id"]
            self.run_cli("knowledge", "review", str(ledger), "--claim", accepted,
                         "--decision", "accept", "--reviewer", "human:demo")
            context = json.loads(self.run_cli("knowledge", "context", str(ledger)).stdout)
            self.assertEqual([claim["id"] for claim in context["knowledge"]], [accepted])
            self.assertEqual(len(context["open_claims"]), 2)

            verified = json.loads(self.run_cli("knowledge", "verify", str(ledger)).stdout)
            self.assertTrue(verified["ok"], verified)

    def test_accepting_blocked_claim_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "ledger.json"
            self.run_cli("knowledge", "ingest", str(FIXTURE), "-o", str(ledger))
            data = json.loads(ledger.read_text())
            blocked = next(c["id"] for c in data["claims"] if c["support"]["experiment_status"] == "failed")
            result = self.run_cli("knowledge", "review", str(ledger), "--claim", blocked,
                                  "--decision", "accept", "--reviewer", "human:demo", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("blocked", result.stderr)


if __name__ == "__main__":
    unittest.main()

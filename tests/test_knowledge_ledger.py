import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from proofpress.kernel import operations as knowledge


ROOT = Path(__file__).resolve().parents[1]
CLI = (sys.executable, "-m", "proofpress.cli")
FIXTURE = ROOT / "examples" / "verified-knowledge-ledger" / "demo.otlp.json"


class KnowledgeLedgerTests(unittest.TestCase):
    def run_cli(self, *args, check=True):
        result = subprocess.run([*CLI, *args], cwd=ROOT, text=True, capture_output=True)
        if check and result.returncode:
            self.fail(f"command failed: {result.args}\n{result.stdout}\n{result.stderr}")
        return result

    def new_ledger(self, directory, *extra):
        ledger = Path(directory) / "ledger.json"
        result = self.run_cli("knowledge", "ingest", str(FIXTURE), "-o", str(ledger), "--scope", "coframe-demo", *extra)
        return ledger, json.loads(result.stdout)

    def test_otlp_creates_immutable_evidence_and_view(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger, summary = self.new_ledger(directory)
            self.assertEqual((summary["source_events"], summary["evidence"], summary["claims"]), (3, 3, 3))
            data = json.loads(ledger.read_text())
            self.assertEqual(data["schema_version"], "proofpress/knowledge-ledger/v1")
            self.assertTrue(all("digest" in item and "source_ref" in item for item in data["evidence"]))
            second, _ = self.new_ledger(Path(directory) / "repeat")
            repeated = knowledge.read(second)
            self.assertEqual([item["id"] for item in data["evidence"]], [item["id"] for item in repeated["evidence"]])
            self.assertEqual([item["id"] for item in data["claims"]], [item["id"] for item in repeated["claims"]])
            view = json.loads(self.run_cli("knowledge", "view", str(ledger), "--scope", "coframe-demo").stdout)
            self.assertEqual(view["schema_version"], "proofpress/ledger-view/v1")
            self.assertTrue(any(edge["type"] == "supports" for edge in view["edges"]))

    def test_empty_existing_output_is_initialized(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "ledger.json"
            ledger.touch()
            self.run_cli("knowledge", "ingest", str(FIXTURE), "-o", str(ledger))
            self.assertEqual(json.loads(ledger.read_text())["schema_version"], "proofpress/knowledge-ledger/v1")

    def test_policy_then_human_admission_projects_only_admitted_claims(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger, _ = self.new_ledger(Path(directory) / "active", "--proposer", "agent:runner")
            data = json.loads(ledger.read_text())
            accepted = next(c["id"] for c in data["claims"] if c["gate"]["eligible"])
            self.assertEqual(json.loads(self.run_cli("knowledge", "policy-review", str(ledger), "--claim", accepted).stdout)["recommendation"], "accept")
            self.run_cli("knowledge", "review", str(ledger), "--claim", accepted, "--decision", "accept", "--reviewer", "human:demo")
            context = json.loads(self.run_cli("knowledge", "context", str(ledger), "--scope", "coframe-demo").stdout)
            self.assertEqual([claim["id"] for claim in context["knowledge"]], [accepted])
            self.assertNotIn(accepted, context["open_claims"])
            verified = json.loads(self.run_cli("knowledge", "verify", str(ledger)).stdout)
            self.assertTrue(verified["ok"], verified)

    def test_blocked_and_self_approved_claims_are_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger, _ = self.new_ledger(Path(directory) / "active", "--proposer", "agent:runner")
            data = json.loads(ledger.read_text())
            blocked = next(c["id"] for c in data["claims"] if not c["gate"]["eligible"])
            eligible = next(c["id"] for c in data["claims"] if c["gate"]["eligible"])
            result = self.run_cli("knowledge", "review", str(ledger), "--claim", blocked, "--decision", "accept", "--reviewer", "human:demo", check=False)
            self.assertIn("blocked", result.stderr)
            result = self.run_cli("knowledge", "review", str(ledger), "--claim", eligible, "--decision", "accept", "--reviewer", "agent:runner", check=False)
            self.assertIn("self-approve", result.stderr)

    def test_rejected_expired_and_policy_drift_do_not_enter_context(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger, _ = self.new_ledger(directory, "--proposer", "agent:runner")
            data = json.loads(ledger.read_text())
            eligible = [c for c in data["claims"] if c["gate"]["eligible"]]
            self.run_cli("knowledge", "review", str(ledger), "--claim", eligible[0]["id"], "--decision", "reject", "--reviewer", "human:demo")
            self.run_cli("knowledge", "review", str(ledger), "--claim", eligible[1]["id"], "--decision", "accept", "--reviewer", "human:demo")
            data = knowledge.read(ledger)
            data["active_policy"] = knowledge.policy({"version": 2, "min_sample_size": 500})
            knowledge.write(ledger, data)
            context = knowledge.context(ledger, "coframe-demo")
            self.assertEqual(context["knowledge"], [])
            self.assertIn(eligible[1]["id"], context["open_claims"])

    def test_expiry_and_supersession_are_excluded_from_current_context(self):
        with tempfile.TemporaryDirectory() as directory:
            expired, _ = self.new_ledger(directory, "--expires-at", "2000-01-01T00:00:00Z")
            self.assertEqual(knowledge.context(expired, "coframe-demo")["knowledge"], [])
            ledger, _ = self.new_ledger(Path(directory) / "active", "--proposer", "agent:runner")
            data = knowledge.read(ledger)
            eligible = [c["id"] for c in data["claims"] if c["gate"]["eligible"]]
            for claim_id in eligible:
                self.run_cli("knowledge", "review", str(ledger), "--claim", claim_id,
                             "--decision", "accept", "--reviewer", "human:demo")
            self.run_cli("knowledge", "supersede", str(ledger), "--claim", eligible[0],
                         "--by", eligible[1], "--reviewer", "human:demo")
            context = knowledge.context(ledger, "coframe-demo")
            self.assertEqual([c["id"] for c in context["knowledge"]], [eligible[1]])

    def test_materialize_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger, _ = self.new_ledger(directory, "--proposer", "agent:runner")
            data = json.loads(ledger.read_text())
            eligible = next(c["id"] for c in data["claims"] if c["gate"]["eligible"])
            self.run_cli("knowledge", "review", str(ledger), "--claim", eligible, "--decision", "accept", "--reviewer", "human:demo")
            output = Path(directory) / "context.md"
            result = json.loads(self.run_cli("knowledge", "materialize", str(ledger), "-o", str(output), "--scope", "coframe-demo").stdout)
            self.assertEqual(result["knowledge_count"], 1)
            self.assertIn(eligible, output.read_text())
            data = knowledge.read(ledger)
            data["evidence"][0]["observation"]["name"] = "tampered"
            knowledge.write(ledger, data)
            verified = knowledge.verify(ledger)
            self.assertFalse(verified["ok"])
            self.assertFalse(verified["checks"]["evidence_digests"])


if __name__ == "__main__":
    unittest.main()

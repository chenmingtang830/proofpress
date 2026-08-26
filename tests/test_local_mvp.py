import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "proofpress.py"
FIXTURE = ROOT / "examples" / "verified-knowledge-ledger" / "demo.otlp.json"


class LocalMVPTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.repo, check=True)

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *args, check=True):
        result = subprocess.run([sys.executable, str(CLI), *args], cwd=self.repo,
                                text=True, capture_output=True)
        if check and result.returncode:
            self.fail(f"failed: {result.args}\n{result.stdout}\n{result.stderr}")
        return result

    def data(self, *args):
        return json.loads(self.cli(*args).stdout)

    def seed(self, proposer="agent:runner"):
        imported = self.data("evidence", "import", str(FIXTURE))
        evidence = imported["evidence"][0]
        proposed = self.data("propose", "--statement", "The liability cap is 1x annual fees",
                             "--evidence", evidence, "--scope", "msa-negotiation",
                             "--proposer", proposer)
        return evidence, proposed["conclusion"]["id"]

    def count_events(self):
        return int(subprocess.run(["git", "rev-list", "--count", "refs/proofpress/knowledge"],
                                  cwd=self.repo, text=True, capture_output=True, check=True).stdout)

    def test_import_is_idempotent_and_events_are_git_backed(self):
        first = self.data("evidence", "import", str(FIXTURE))
        count = self.count_events()
        second = self.data("evidence", "import", str(FIXTURE))
        self.assertEqual(first["evidence"], second["evidence"])
        self.assertEqual(self.count_events(), count)
        self.assertTrue(subprocess.run(["git", "show-ref", "--verify", "refs/proofpress/knowledge"],
                                       cwd=self.repo, capture_output=True).returncode == 0)

    def test_admission_and_context_gate(self):
        _, cid = self.seed()
        evaluation = self.data("evaluate", cid)
        self.assertTrue(evaluation["eligible"])
        self.data("review", cid, "--admit", "--reviewer", "human:alice")
        context = self.data("context", "--scope", "msa-negotiation",
                            "--actor", "agent:successor")
        self.assertEqual([row["id"] for row in context["knowledge"]], [cid])
        self.assertEqual(context["blocked"], [])
        self.assertIn("admission_event", context["knowledge"][0]["receipt"])
        sys.path.insert(0, str(ROOT))
        import proofpress_knowledge as knowledge
        previous = Path.cwd()
        try:
            os.chdir(self.repo)
            graph = knowledge.graph_v2("msa-negotiation")
        finally:
            os.chdir(previous)
        self.assertTrue({"raw", "evidence", "conclusion", "review", "governed"}
                        <= {node["type"] for node in graph["nodes"]})

    def test_self_approval_rejection_and_supersession_fail_closed(self):
        evidence, old = self.seed()
        blocked = self.cli("review", old, "--admit", "--reviewer", "agent:runner", check=False)
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("self-approve", blocked.stderr)
        new = self.data("propose", "--statement", "The liability cap requires escalation",
                        "--evidence", evidence, "--scope", "msa-negotiation",
                        "--proposer", "agent:runner")["conclusion"]["id"]
        self.data("supersede", old, "--by", new, "--reviewer", "human:alice")
        packet = self.data("context", "--scope", "msa-negotiation")
        reasons = {row["id"]: row["reason"] for row in packet["blocked"]}
        self.assertEqual(reasons[old], "superseded")
        self.data("review", new, "--reject", "--reviewer", "human:alice")
        packet = self.data("context", "--scope", "msa-negotiation")
        reasons = {row["id"]: row["reason"] for row in packet["blocked"]}
        self.assertEqual(reasons[new], "rejected")
        self.assertTrue(all("statement" not in row for row in packet["blocked"]))

    def test_external_judge_is_advisory_and_required_policy_is_enforced(self):
        _, cid = self.seed()
        policy_dir = self.repo / ".proofpress"
        policy_dir.mkdir()
        judge_code = "import json,sys; json.load(sys.stdin); print(json.dumps({'recommendation':'accept','rationale':'policy requirements satisfied','adapter':'fixture'}))"
        (policy_dir / "policy.json").write_text(json.dumps({
            "require_judge": True,
            "judge": {"command": [sys.executable, "-c", judge_code], "timeout_seconds": 5},
        }))
        missing = self.cli("review", cid, "--admit", "--reviewer", "human:alice", check=False)
        self.assertIn("requires an accepting judge", missing.stderr)
        recommendation = self.data("judge", cid)
        self.assertEqual(recommendation["recommendation"], "accept")
        self.data("review", cid, "--admit", "--reviewer", "human:alice")
        self.assertEqual(len(self.data("context", "--scope", "msa-negotiation")["knowledge"]), 1)

    def test_transaction_level_batch_judge_records_individual_receipts(self):
        evidence, first = self.seed()
        second = self.data("propose", "--statement", "The indemnity requires escalation",
                           "--evidence", evidence, "--scope", "msa-negotiation",
                           "--proposer", "agent:runner")["conclusion"]["id"]
        policy_dir = self.repo / ".proofpress"; policy_dir.mkdir()
        judge_code = (
            "import json,sys; p=json.load(sys.stdin); "
            "vs=[{'conclusion_id':x['conclusion']['id'],'recommendation':'accept','risk_level':'low','rationale':'supported'} for x in p['conclusions']]; "
            "print(json.dumps({'verdicts':vs,'adapter':'fixture-batch'}))"
        )
        (policy_dir / "policy.json").write_text(json.dumps({
            "judge": {"command": [sys.executable, "-c", judge_code], "timeout_seconds": 5},
        }))
        result = self.data("judge", "--batch", "--scope", "msa-negotiation")
        self.assertEqual(len(result["verdicts"]), 2)
        self.assertEqual(result["individual_reviews"], [])
        self.assertTrue(all(row["batch_receipt"] == result["batch_receipt"] for row in result["verdicts"]))
        self.assertEqual({row["subject_ref"] for row in result["verdicts"]}, {first, second})

    def test_v1_migration_is_one_way_and_idempotent(self):
        legacy = self.repo / "legacy.json"
        self.cli("knowledge", "ingest", str(FIXTURE), "-o", str(legacy),
                 "--scope", "legacy")
        legacy_data = json.loads(legacy.read_text())
        claim = legacy_data["claims"][0]
        self.cli("knowledge", "review", str(legacy), "--claim", claim["id"],
                 "--decision", "accept", "--reviewer", "human:alice")
        original = legacy.read_bytes()
        self.data("import-v1", str(legacy))
        migrated = self.cli("context", "--scope", "legacy").stdout
        self.assertIn("unresolved", migrated)
        event_types = [json.loads(line)["type"] for line in subprocess.run(
            ["git", "log", "--format=%H", "refs/proofpress/knowledge"], cwd=self.repo,
            text=True, capture_output=True, check=True).stdout.splitlines()
            for line in [subprocess.run(["git", "show", f"{line}:event.json"], cwd=self.repo,
                                        text=True, capture_output=True, check=True).stdout]]
        self.assertIn("conclusion_admitted", event_types)
        self.assertIn("human_reviewed", event_types)
        count = self.count_events()
        self.data("import-v1", str(legacy))
        self.assertEqual(self.count_events(), count)
        self.assertEqual(legacy.read_bytes(), original)

    def test_local_ui_reads_real_ledger_and_rejects_missing_token(self):
        self.seed()
        process = subprocess.Popen([sys.executable, str(CLI), "ui", "--no-open", "--port", "0"],
                                   cwd=self.repo, text=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        try:
            line = process.stdout.readline().strip()
            url = line.split(": ", 1)[1]
            body = urlopen(url, timeout=5).read().decode()
            self.assertIn("REVIEW QUEUE", body)
            base, token = url.split("/?token=")
            request = Request(base + "/api/summary", headers={"X-Proofpress-Token": token})
            summary = json.loads(urlopen(request, timeout=5).read())
            self.assertEqual(summary["total"], 1)
            with self.assertRaises(HTTPError) as caught:
                urlopen(base + "/api/summary", timeout=2)
            caught.exception.close()
        finally:
            process.terminate()
            process.communicate(timeout=5)


if __name__ == "__main__":
    unittest.main()

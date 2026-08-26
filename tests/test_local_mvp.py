import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
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

    def test_artifact_evidence_import_is_idempotent(self):
        artifact = self.repo / "task-evidence.json"
        artifact.write_text('{"task":"protect the buyer"}\n')
        first = self.data("evidence", "import", str(artifact))
        count = self.count_events()
        second = self.data("evidence", "import", str(artifact))
        self.assertEqual(first["evidence"], second["evidence"])
        self.assertEqual(self.count_events(), count)

    def test_claim_and_relation_proposals_are_resumable(self):
        evidence, first = self.seed()
        second = self.data("propose", "--statement", "The exception narrows the cap",
                           "--evidence", evidence, "--scope", "msa-negotiation",
                           "--proposer", "agent:runner")["conclusion"]["id"]
        relation_args = ("relation", "propose", second, "--to", first,
                         "--type", "qualifies", "--proposer", "agent:runner")
        relation = self.data(*relation_args)["relation"]["id"]
        count = self.count_events()
        repeated_first = self.seed()[1]
        repeated_relation = self.data(*relation_args)["relation"]["id"]
        self.assertEqual((repeated_first, repeated_relation), (first, relation))
        self.assertEqual(self.count_events(), count)

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

    def test_request_changes_is_append_only_and_excluded_from_context(self):
        evidence, cid = self.seed()
        head = subprocess.run(["git", "rev-parse", "refs/proofpress/knowledge"], cwd=self.repo,
                              text=True, capture_output=True, check=True).stdout.strip()
        request_id = "review-request-001"
        result = self.data("review", cid, "--request-changes", "--reviewer", "human:alice",
                           "--note", "Bind the conclusion to the operative schedule.",
                           "--request-id", request_id, "--expected-head", head)
        count_after_review = self.count_events()
        self.assertEqual(result["review"]["decision"], "request_changes")
        self.assertEqual(result["result"]["type"], "conclusion_revision_requested")
        packet = self.data("context", "--scope", "msa-negotiation")
        blocked = next(row for row in packet["blocked"] if row["id"] == cid)
        self.assertEqual((blocked["reason"], blocked["required_action"]),
                         ("needs_revision", "propose_revision"))
        graph = self.data("graph", "--scope", "msa-negotiation")
        conclusion = next(row for row in graph["nodes"] if row["id"] == cid)
        self.assertEqual(conclusion["state"], "needs_revision")
        self.assertEqual(self.count_events(), count_after_review)
        repeated = self.data("review", cid, "--request-changes", "--reviewer", "human:alice",
                             "--note", "Bind the conclusion to the operative schedule.",
                             "--request-id", request_id, "--expected-head", head)
        self.assertTrue(repeated["idempotent"])
        self.assertEqual(self.count_events(), count_after_review)
        stale = self.cli("review", cid, "--reject", "--reviewer", "human:alice",
                         "--request-id", "review-request-002", "--expected-head", head,
                         check=False)
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn("STALE_LEDGER_HEAD", stale.stderr)
        revised = self.data("propose", "--statement", "The operative schedule sets a 1x cap",
                            "--evidence", evidence, "--scope", "msa-negotiation",
                            "--proposer", "agent:runner")["conclusion"]["id"]
        self.assertNotEqual(revised, cid)
        self.assertEqual(next(row for row in self.data("graph", "--scope", "msa-negotiation")["nodes"]
                              if row["id"] == revised)["state"], "needs_review")

    def test_relation_request_changes_uses_the_same_general_review_state(self):
        evidence, first = self.seed()
        second = self.data("propose", "--statement", "The exception narrows the cap",
                           "--evidence", evidence, "--scope", "msa-negotiation",
                           "--proposer", "agent:runner")["conclusion"]["id"]
        relation = self.data("relation", "propose", second, "--to", first,
                             "--type", "qualifies")["relation"]["id"]
        result = self.data("relation", "review", relation, "--request-changes",
                           "--reviewer", "human:alice", "--note", "Clarify directionality.")
        self.assertEqual(result["result"]["type"], "relation_revision_requested")
        graph = self.data("graph", "--scope", "msa-negotiation")
        edge = next(row for row in graph["edges"] if row.get("id") == relation)
        self.assertEqual(edge["state"], "needs_revision")

    def test_general_claim_relations_require_structural_checks_and_human_admission(self):
        evidence, first = self.seed()
        second = self.data("propose", "--statement", "The liability cap excludes fraud",
                           "--evidence", evidence, "--scope", "msa-negotiation",
                           "--proposer", "agent:runner")["conclusion"]["id"]
        relation = self.data("relation", "propose", second, "--to", first,
                             "--type", "qualifies", "--proposer", "agent:runner",
                             "--confidence", "0.82")["relation"]
        evaluation = self.data("relation", "evaluate", relation["id"])
        self.assertTrue(evaluation["eligible"])
        self.assertIn("do not establish semantic correctness", evaluation["semantic_boundary"])
        blocked = self.cli("relation", "review", relation["id"], "--admit",
                           "--reviewer", "agent:runner", check=False)
        self.assertIn("self-approve", blocked.stderr)
        self.data("review", first, "--admit", "--reviewer", "human:alice")
        self.data("review", second, "--admit", "--reviewer", "human:alice")
        self.data("relation", "review", relation["id"], "--admit",
                  "--reviewer", "human:alice")
        packet = self.data("context", "--scope", "msa-negotiation")
        self.assertEqual([row["id"] for row in packet["relations"]], [relation["id"]])
        graph = self.data("graph", "--scope", "msa-negotiation")
        edge = next(row for row in graph["edges"] if row.get("id") == relation["id"])
        self.assertEqual((edge["type"], edge["state"]), ("qualifies", "admitted"))
        policy_dir = self.repo / ".proofpress"; policy_dir.mkdir()
        (policy_dir / "policy.json").write_text(json.dumps({"min_evidence": 2}))
        graph = self.data("graph", "--scope", "msa-negotiation")
        edge = next(row for row in graph["edges"] if row.get("id") == relation["id"])
        self.assertEqual(edge["state"], "unresolved")

    def test_relation_semantic_judge_is_advisory_and_policy_enforced(self):
        evidence, first = self.seed()
        second = self.data("propose", "--statement", "The exception narrows the cap",
                           "--evidence", evidence, "--scope", "msa-negotiation",
                           "--proposer", "agent:runner")["conclusion"]["id"]
        relation = self.data("relation", "propose", second, "--to", first,
                             "--type", "qualifies", "--proposer", "agent:runner")["relation"]["id"]
        policy_dir = self.repo / ".proofpress"; policy_dir.mkdir()
        judge_code = ("import json,sys; p=json.load(sys.stdin); "
                      "assert p['schema_version']=='proofpress/relation-judge-request/v1'; "
                      "print(json.dumps({'recommendation':'accept','rationale':'the exception narrows the target claim','adapter':'fixture'}))")
        (policy_dir / "policy.json").write_text(json.dumps({
            "require_judge": True,
            "judge": {"command": [sys.executable, "-c", judge_code], "timeout_seconds": 5},
        }))
        missing = self.cli("relation", "review", relation, "--admit",
                           "--reviewer", "human:alice", check=False)
        self.assertIn("accepting relation judge", missing.stderr)
        recommendation = self.data("relation", "judge", relation)
        self.assertEqual(recommendation["recommendation"], "accept")
        self.data("relation", "review", relation, "--admit", "--reviewer", "human:alice")

    def test_directed_relation_cycles_fail_closed(self):
        evidence, first = self.seed()
        second = self.data("propose", "--statement", "Second conclusion",
                           "--evidence", evidence, "--scope", "msa-negotiation",
                           "--proposer", "agent:runner")["conclusion"]["id"]
        forward = self.data("relation", "propose", first, "--to", second,
                            "--type", "depends_on")["relation"]["id"]
        self.data("relation", "review", forward, "--admit", "--reviewer", "human:alice")
        reverse = self.data("relation", "propose", second, "--to", first,
                            "--type", "depends_on")["relation"]["id"]
        evaluation = self.data("relation", "evaluate", reverse)
        self.assertFalse(evaluation["eligible"])
        self.assertFalse(evaluation["checks"]["acyclic_when_directed"])

    def test_legal_profile_is_optional_and_validated(self):
        evidence = self.data("evidence", "import", str(FIXTURE))["evidence"][0]
        qualifiers = self.repo / "legal.json"
        qualifiers.write_text(json.dumps({"legal": {
            "jurisdiction": "US-DE", "authority": "agreement",
            "citation_locator": "Section 8.1", "effective_from": "2026-01-01",
            "document_type": "stock_purchase_agreement"
        }}))
        row = self.data("propose", "--statement", "The closing condition applies",
                        "--evidence", evidence, "--scope", "deal", "--profile", "legal",
                        "--qualifiers", str(qualifiers))["conclusion"]
        self.assertEqual(row["qualifiers"]["profile"], "proofpress/profile/legal/v1")
        qualifiers.write_text(json.dumps({"legal": {"jurisdiction": "US-DE"}}))
        failed = self.cli("propose", "--statement", "Incomplete legal metadata",
                          "--evidence", evidence, "--scope", "deal", "--profile", "legal",
                          "--qualifiers", str(qualifiers), check=False)
        self.assertIn("legal profile missing", failed.stderr)

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

    def test_batch_judge_loads_history_once_and_resumes_without_duplicates(self):
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
        self.data("evaluate", first)
        self.data("evaluate", second)
        sys.path.insert(0, str(ROOT))
        import proofpress_knowledge as knowledge
        original_run = subprocess.run
        git_commands = []

        def counted_run(args, *positional, **kwargs):
            if args and args[0] == "git": git_commands.append(tuple(args[1:3]))
            return original_run(args, *positional, **kwargs)

        previous = Path.cwd(); os.chdir(self.repo)
        try:
            evaluations_before = len([row for row in knowledge.v2_events()
                                      if row.get("type") == "policy_evaluated"])
            with patch.object(knowledge.subprocess, "run", side_effect=counted_run):
                result = knowledge.judge_batch_v2("msa-negotiation")
            traversals = [command for command in git_commands
                          if command[0] in {"rev-list", "cat-file", "show"}]
            self.assertEqual(traversals.count(("rev-list", "--reverse")), 1)
            self.assertEqual(traversals.count(("cat-file", "--batch")), 1)
            self.assertFalse(any(command[0] == "show" for command in traversals))
            self.assertEqual({row["subject_ref"] for row in result["verdicts"]}, {first, second})
            evaluations_after = len([row for row in knowledge.v2_events()
                                     if row.get("type") == "policy_evaluated"])
            self.assertEqual(evaluations_after, evaluations_before)

            third = knowledge.propose_v2("第三项有界结论 — Unicode survives event loading", [evidence],
                                         "msa-negotiation", "agent:runner")["conclusion"]["id"]
            resumed = knowledge.judge_batch_v2("msa-negotiation")
            self.assertEqual([row["subject_ref"] for row in resumed["verdicts"]], [third])
            idempotent = knowledge.judge_batch_v2("msa-negotiation")
            self.assertTrue(idempotent["idempotent"])
            self.assertIsNone(idempotent["batch_receipt"])
            self.assertEqual(len(idempotent["batch_receipts"]), 2)
            self.assertIn("第三项有界结论", knowledge.v2_projection()["conclusions"][third]["statement"])
            recommendations = [row for row in knowledge.v2_events()
                               if row.get("type") == "judge_recommended"]
            self.assertEqual({row["subject_ref"] for row in recommendations}, {first, second, third})
            self.assertEqual(len(recommendations), 3)
        finally:
            os.chdir(previous)
            sys.path.remove(str(ROOT))

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

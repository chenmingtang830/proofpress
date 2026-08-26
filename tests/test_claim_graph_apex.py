import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "verified-knowledge-ledger" / "legal" / "apex-claim-graph.json"
sys.path.insert(0, str(ROOT))
import proofpress_knowledge as knowledge


class ApexClaimGraphAcceptanceTests(unittest.TestCase):
    def _repo(self, directory):
        repo = Path(directory)
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
        return repo

    def test_thirteen_claims_and_seven_relations_reach_governed_context(self):
        fixture = json.loads(FIXTURE.read_text())
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
            previous = Path.cwd()
            try:
                os.chdir(repo)
                evidence = []
                for index in range(7):
                    source = repo / f"source-{index}.txt"
                    source.write_text(f"Public APEX acceptance evidence {index}\n")
                    evidence.append(knowledge.import_evidence_v2(str(source))["evidence"][-1])
                claims = {}
                for row in fixture["claims"]:
                    qualifiers = {"legal": {"jurisdiction": "US-Federal/Delaware",
                                  "authority": row["authority"],
                                  "citation_locator": row["citation_locator"]}}
                    result = knowledge.propose_v2(row["statement"], [evidence[row["evidence"]]],
                              fixture["scope"], "agent:luna-proposer",
                              qualifiers=qualifiers, profile="legal")
                    claims[row["key"]] = result["conclusion"]["id"]
                    knowledge.review_v2(claims[row["key"]], "admit", "human:lawyer")
                relations = []
                for row in fixture["relations"]:
                    result = knowledge.propose_relation_v2(claims[row["from"]], claims[row["to"]],
                              row["type"], "agent:luna-relation-proposer", .8)
                    rid = result["relation"]["id"]
                    self.assertTrue(knowledge.evaluate_relation_v2(rid)["eligible"])
                    knowledge.review_relation_v2(rid, "admit", "human:lawyer")
                    relations.append(rid)
                context = knowledge.context_v2(fixture["scope"], "agent:apex-executor")
                self.assertEqual(len(context["knowledge"]), 13)
                self.assertEqual(len(context["relations"]), 7)
                graph = knowledge.graph_v2(fixture["scope"])
                self.assertEqual(len([edge for edge in graph["edges"] if edge.get("id") in relations]), 7)
                self.assertTrue(knowledge.v2_events())
            finally:
                os.chdir(previous)

    def test_bounded_traversal_expands_only_eligible_claims(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self._repo(directory); previous = Path.cwd()
            try:
                os.chdir(repo)
                source = repo / "source.txt"; source.write_text("Bound evidence\n")
                evidence = knowledge.import_evidence_v2(str(source))["evidence"][0]
                claims = []
                for index in range(3):
                    result = knowledge.propose_v2(
                        f"Admitted conclusion {index}", [evidence], "matter-1",
                        "agent:proposer", allowed_actors=["agent:executor"])
                    cid = result["conclusion"]["id"]
                    knowledge.review_v2(cid, "admit", "human:lawyer")
                    claims.append(cid)
                relations = []
                for left, right in zip(claims, claims[1:]):
                    relation = knowledge.propose_relation_v2(
                        left, right, "depends_on", "agent:proposer")["relation"]["id"]
                    knowledge.review_relation_v2(relation, "admit", "human:lawyer")
                    relations.append(relation)

                depth_one = knowledge.traverse_graph_v2(
                    [claims[0]], "matter-1", "agent:executor", max_depth=1)
                self.assertEqual(depth_one["conclusion_ids"], claims[:2])
                self.assertEqual(len(depth_one["relations"]), 1)
                bounded = knowledge.traverse_graph_v2(
                    [claims[0]], "matter-1", "agent:executor",
                    max_depth=2, max_claims=2)
                self.assertEqual(bounded["conclusion_ids"], claims[:2])
                self.assertEqual(bounded["schema_version"], knowledge.TRAVERSAL_SCHEMA)
            finally:
                os.chdir(previous)

    def test_traversal_records_blocked_neighbor_without_statement(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self._repo(directory); previous = Path.cwd()
            try:
                os.chdir(repo)
                source = repo / "source.txt"; source.write_text("Bound evidence\n")
                evidence = knowledge.import_evidence_v2(str(source))["evidence"][0]
                visible = knowledge.propose_v2(
                    "Visible conclusion", [evidence], "matter-1", "agent:proposer")["conclusion"]["id"]
                blocked = knowledge.propose_v2(
                    "Secret blocked statement", [evidence], "matter-1", "agent:proposer",
                    allowed_actors=["agent:other"])["conclusion"]["id"]
                knowledge.review_v2(visible, "admit", "human:lawyer")
                knowledge.review_v2(blocked, "admit", "human:lawyer")
                relation = knowledge.propose_relation_v2(
                    visible, blocked, "qualifies", "agent:proposer")["relation"]["id"]
                knowledge.review_relation_v2(relation, "admit", "human:lawyer")

                result = knowledge.traverse_graph_v2(
                    [visible], "matter-1", "agent:executor")
                self.assertEqual(result["conclusion_ids"], [visible])
                self.assertEqual(result["blocked_neighbors"][0]["conclusion_id"], blocked)
                self.assertNotIn("statement", result["blocked_neighbors"][0])
                self.assertNotIn("Secret blocked statement", json.dumps(result))
            finally:
                os.chdir(previous)

    def test_staged_traversal_uses_non_rejected_recommendations_without_admission(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self._repo(directory); previous = Path.cwd()
            try:
                os.chdir(repo)
                source = repo / "source.txt"; source.write_text("Bound evidence\n")
                evidence = knowledge.import_evidence_v2(str(source))["evidence"][0]
                claims = []
                for index, statement in enumerate(("Staged seed", "Staged neighbor")):
                    cid = knowledge.propose_v2(
                        statement, [evidence], "matter-1", "agent:proposer")["conclusion"]["id"]
                    evaluation = knowledge.evaluate_v2(cid)
                    row = knowledge.v2_projection()["conclusions"][cid]
                    knowledge.append_v2({"type": "judge_recommended", "subject_ref": cid,
                        "conclusion_digest": row["digest"], "policy_digest": evaluation["policy_digest"],
                        "recommendation": "accept" if index == 0 else "escalate",
                        "rationale": "Non-rejected recommendation for test staging."})
                    claims.append(cid)
                rid = knowledge.propose_relation_v2(
                    claims[0], claims[1], "supports", "agent:proposer")["relation"]["id"]
                evaluation = knowledge.evaluate_relation_v2(rid)
                row = knowledge.v2_projection()["relations"][rid]
                knowledge.append_v2({"type": "relation_judge_recommended", "subject_ref": rid,
                    "relation_digest": row["digest"], "policy_digest": evaluation["policy_digest"],
                    "recommendation": "escalate", "rationale": "Escalated relation for test staging."})

                with self.assertRaisesRegex(ValueError, "no eligible seeds"):
                    knowledge.traverse_graph_v2([claims[0]], "matter-1")
                result = knowledge.traverse_graph_v2(
                    [claims[0]], "matter-1", state="staged")
                self.assertEqual(result["conclusion_ids"], claims)
                self.assertEqual(result["state"], "staged")
                self.assertEqual(len(result["relations"]), 1)
                self.assertFalse(knowledge.v2_projection()["admissions"])
            finally:
                os.chdir(previous)


if __name__ == "__main__":
    unittest.main()

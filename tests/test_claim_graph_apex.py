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
from proofpress.kernel import operations as kernel_ops


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
                    evidence.append(kernel_ops.import_evidence_v2(str(source))["evidence"][-1])
                claims = {}
                for row in fixture["claims"]:
                    qualifiers = {"legal": {"jurisdiction": "US-Federal/Delaware",
                                  "authority": row["authority"],
                                  "citation_locator": row["citation_locator"]}}
                    result = kernel_ops.propose_v2(row["statement"], [evidence[row["evidence"]]],
                              fixture["scope"], "agent:luna-proposer",
                              qualifiers=qualifiers, profile="legal")
                    claims[row["key"]] = result["claim"]["id"]
                    kernel_ops.review_v2(claims[row["key"]], "admit", "human:lawyer")
                relations = []
                for row in fixture["relations"]:
                    result = kernel_ops.propose_relation_v2(claims[row["from"]], claims[row["to"]],
                              row["type"], "agent:luna-relation-proposer", .8)
                    rid = result["relation"]["id"]
                    self.assertTrue(kernel_ops.evaluate_relation_v2(rid)["eligible"])
                    kernel_ops.review_relation_v2(rid, "admit", "human:lawyer")
                    relations.append(rid)
                context = kernel_ops.context_v2(fixture["scope"], "agent:apex-executor")
                self.assertEqual(len(context["governed_context"]), 13)
                self.assertEqual(len(context["relations"]), 7)
                graph = kernel_ops.graph_v2(fixture["scope"])
                self.assertEqual(len([edge for edge in graph["edges"] if edge.get("id") in relations]), 7)
                self.assertTrue(kernel_ops.v2_events())
            finally:
                os.chdir(previous)

    def test_bounded_traversal_expands_only_eligible_claims(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self._repo(directory); previous = Path.cwd()
            try:
                os.chdir(repo)
                source = repo / "source.txt"; source.write_text("Bound evidence\n")
                evidence = kernel_ops.import_evidence_v2(str(source))["evidence"][0]
                claims = []
                for index in range(3):
                    result = kernel_ops.propose_v2(
                        f"Admitted claim {index}", [evidence], "matter-1",
                        "agent:proposer")
                    cid = result["claim"]["id"]
                    kernel_ops.review_v2(cid, "admit", "human:lawyer")
                    claims.append(cid)
                relations = []
                for left, right in zip(claims, claims[1:]):
                    relation = kernel_ops.propose_relation_v2(
                        left, right, "depends_on", "agent:proposer")["relation"]["id"]
                    kernel_ops.review_relation_v2(relation, "admit", "human:lawyer")
                    relations.append(relation)

                depth_one = kernel_ops.traverse_graph_v2(
                    [claims[0]], "matter-1", "agent:executor", max_depth=1)
                self.assertEqual(depth_one["claim_ids"], claims[:2])
                self.assertEqual(len(depth_one["relations"]), 1)
                bounded = kernel_ops.traverse_graph_v2(
                    [claims[0]], "matter-1", "agent:executor",
                    max_depth=2, max_claims=2)
                self.assertEqual(bounded["claim_ids"], claims[:2])
                self.assertEqual(bounded["schema_version"], kernel_ops.TRAVERSAL_SCHEMA)
            finally:
                os.chdir(previous)

    def test_staged_traversal_uses_non_rejected_recommendations_without_admission(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self._repo(directory); previous = Path.cwd()
            try:
                os.chdir(repo)
                source = repo / "source.txt"; source.write_text("Bound evidence\n")
                evidence = kernel_ops.import_evidence_v2(str(source))["evidence"][0]
                claims = []
                for index, statement in enumerate(("Staged seed", "Staged neighbor")):
                    cid = kernel_ops.propose_v2(
                        statement, [evidence], "matter-1", "agent:proposer")["claim"]["id"]
                    evaluation = kernel_ops.evaluate_v2(cid)
                    row = kernel_ops.v2_projection()["claims"][cid]
                    kernel_ops.append_v2({"type": "judge_recommended", "subject_ref": cid,
                        "claim_digest": row["digest"], "policy_digest": evaluation["policy_digest"],
                        "recommendation": "accept" if index == 0 else "escalate",
                        "rationale": "Non-rejected recommendation for test staging."})
                    claims.append(cid)
                rid = kernel_ops.propose_relation_v2(
                    claims[0], claims[1], "supports", "agent:proposer")["relation"]["id"]
                evaluation = kernel_ops.evaluate_relation_v2(rid)
                row = kernel_ops.v2_projection()["relations"][rid]
                kernel_ops.append_v2({"type": "relation_judge_recommended", "subject_ref": rid,
                    "relation_digest": row["digest"], "policy_digest": evaluation["policy_digest"],
                    "recommendation": "escalate", "rationale": "Escalated relation for test staging."})

                with self.assertRaisesRegex(ValueError, "no eligible seeds"):
                    kernel_ops.traverse_graph_v2([claims[0]], "matter-1")
                result = kernel_ops.traverse_graph_v2(
                    [claims[0]], "matter-1", state="staged")
                self.assertEqual(result["claim_ids"], claims)
                self.assertEqual(result["state"], "staged")
                self.assertEqual(len(result["relations"]), 1)
                self.assertFalse(kernel_ops.v2_projection()["admissions"])
            finally:
                os.chdir(previous)


if __name__ == "__main__":
    unittest.main()

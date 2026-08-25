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


if __name__ == "__main__":
    unittest.main()

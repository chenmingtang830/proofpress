"""Bounded citation checks for claim-to-claim relations."""
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proofpress.kernel import operations as kernel_ops
from proofpress.hosted import jev


def digest(value):
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


class RelationCitationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.repo, check=True)
        self.previous = Path.cwd()
        os.chdir(self.repo)

    def tearDown(self):
        os.chdir(self.previous)
        self.tmp.cleanup()

    def submit(self, quote, source="workspace://matter/msa.pdf?revision=7"):
        payload = {
            "schema_version": kernel_ops.RETRIEVAL_EVIDENCE_SCHEMA,
            "source": {"uri": source, "content_digest": digest(source)},
            "evidence": {"quote": quote, "locator": {
                "kind": "text_span", "start": 0, "end": len(quote),
                "text_digest": digest(source + ":text"),
            }},
            "retrieval": {"adapter": "test.contract-index", "version": "1",
                          "query": "liability cap", "config_digest": digest("config")},
        }
        return kernel_ops.submit_evidence_v2(payload)["imported_evidence"][0]

    def claims(self, evidence):
        first = kernel_ops.propose_v2(
            "The liability cap is one year of fees.", [evidence], "matter-7", "agent:proposer")["claim"]["id"]
        second = kernel_ops.propose_v2(
            "The liability cap excludes fraud.", [evidence], "matter-7", "agent:proposer")["claim"]["id"]
        return first, second

    def test_citation_is_bound_to_endpoint_evidence_and_materialized_for_judge(self):
        quote = "The limitation does not apply to fraud."
        evidence = self.submit(quote)
        first, second = self.claims(evidence)
        citation = {"schema_version": kernel_ops.RELATION_CITATION_SCHEMA,
                    "evidence_ref": evidence, "quote_digest": digest(quote)}
        relation = kernel_ops.propose_relation_v2(
            second, first, "qualifies", "agent:relation", qualifiers={"citation": citation})["relation"]
        self.assertEqual(relation["qualifiers"]["citation"], citation)
        evaluation = kernel_ops.evaluate_relation_v2(relation["id"])
        self.assertTrue(evaluation["checks"]["citation_binding_valid"])
        self.assertIn("does not re-read source text", evaluation["semantic_boundary"])

        policy_dir = self.repo / ".proofpress"
        policy_dir.mkdir()
        (policy_dir / "policy.json").write_text(json.dumps({
            "judge": {"command": [sys.executable, "-c", "unused"], "timeout_seconds": 5},
        }))
        packets = []
        original_run = subprocess.run

        def jev_response(request, timeout):
            body = json.loads(request.data)
            answers = {}
            for key, question in body["questions"].items():
                if question["type"] == "choice":
                    selected = "qualifies" if key.endswith("_relation_type") else "accept"
                    probabilities = {value: .02 / (len(question["criteria"]) - 1)
                                     for value in question["criteria"]}
                    probabilities[selected] = .98
                    answers[key] = {"type": "choice", "choice": selected,
                                    "probabilities": probabilities, "confidence": .95}
                else:
                    answers[key] = {"type": "noul", "noul": .99}
            return io.BytesIO(json.dumps({"model": "jev-test-revision", "answers": answers}).encode())

        def run(command, *, input, **kwargs):
            if command[0] == "git":
                return original_run(command, input=input, **kwargs)
            packets.append(json.loads(input))
            with patch.dict(os.environ, {"TYPESAFE_API_KEY": "test-key"}):
                verdict = jev.judge(packets[-1], opener=jev_response)
            return subprocess.CompletedProcess(command, 0, json.dumps(verdict), "")

        with patch.object(kernel_ops.subprocess, "run", side_effect=run):
            event = kernel_ops.judge_relation_v2(relation["id"])
        self.assertEqual(len(packets[0]["evidence"]), 1)
        self.assertEqual(packets[0]["evidence"][0]["id"], evidence)
        self.assertEqual(packets[0]["relation_citation"], {
            **citation, "quote": quote,
            "source_content_digest": digest("workspace://matter/msa.pdf?revision=7"),
            "locator": {"kind": "text_span", "start": 0, "end": len(quote),
                        "text_digest": digest("workspace://matter/msa.pdf?revision=7:text")},
        })
        audit = event["decision_audit"]
        self.assertEqual(audit["question_set_version"], jev.RELATION_TYPE_QUESTION_VERSION)
        self.assertEqual(audit["declared_relation_type"], "qualifies")
        receipt = kernel_ops.receipt_v2(first)
        self.assertEqual(len(receipt["relation_advice"]), 1)
        self.assertEqual(receipt["relation_advice"][0]["relation"]["id"], relation["id"])
        self.assertEqual(receipt["relation_advice"][0]["recommendation"]["decision_audit"],
                         audit)
        graph_edge = next(edge for edge in kernel_ops.graph_v2(scope="matter-7")["edges"]
                          if edge.get("id") == relation["id"])
        self.assertEqual(graph_edge["citation"], citation)
        self.assertEqual(graph_edge["advice"]["recommendation"], "accept")
        self.assertEqual(graph_edge["advice"]["decision_audit"], audit)

    def test_missing_citation_endpoints_fail_closed_without_key_error(self):
        quote = "The limitation does not apply to fraud."
        evidence = self.submit(quote)
        first, second = self.claims(evidence)
        citation = {"schema_version": kernel_ops.RELATION_CITATION_SCHEMA,
                    "evidence_ref": evidence, "quote_digest": digest(quote)}
        row = {"from": "missing-source", "to": second, "qualifiers": {"citation": citation}}
        self.assertFalse(kernel_ops._relation_citation_valid({"claims": {}, "evidence": {}}, row))

    def test_citation_rejects_an_unbound_or_tampered_quote_digest(self):
        evidence = self.submit("The cap excludes fraud.")
        other = self.submit("A different source excerpt.", "workspace://matter/other.pdf?revision=1")
        first, second = self.claims(evidence)
        base = {"schema_version": kernel_ops.RELATION_CITATION_SCHEMA,
                "evidence_ref": other, "quote_digest": digest("A different source excerpt.")}
        with self.assertRaisesRegex(ValueError, "bound to a relation endpoint"):
            kernel_ops.propose_relation_v2(second, first, "qualifies", "agent:relation",
                                            qualifiers={"citation": base})
        with self.assertRaisesRegex(ValueError, "does not match bound evidence"):
            kernel_ops.propose_relation_v2(second, first, "qualifies", "agent:relation",
                                            qualifiers={"citation": {**base, "evidence_ref": evidence,
                                                                      "quote_digest": digest("wrong")}})

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "proofpress.py"
FIXTURE = ROOT / "examples" / "verified-knowledge-ledger" / "demo.otlp.json"


class LocalOperationContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"],
                       cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"],
                       cwd=self.repo, check=True)
        sys.path.insert(0, str(ROOT))
        import proofpress_knowledge
        self.knowledge = proofpress_knowledge
        self.previous = Path.cwd()
        os.chdir(self.repo)

    def tearDown(self):
        os.chdir(self.previous)
        self.tmp.cleanup()

    def execute(self, operation, **parameters):
        return self.knowledge.execute_local_operation({
            "schema_version": self.knowledge.LOCAL_OPERATION_SCHEMA,
            "operation": operation,
            "parameters": parameters,
        })

    def cli(self, *args):
        result = subprocess.run([sys.executable, str(CLI), *args], cwd=self.repo,
                                text=True, capture_output=True, check=True)
        return json.loads(result.stdout)

    def test_contract_rejects_unknown_schema_operation_and_parameters(self):
        with self.assertRaisesRegex(ValueError, "schema_version"):
            self.knowledge.execute_local_operation({
                "schema_version": "proofpress/local-operation/future",
                "operation": "context.get", "parameters": {},
            })
        with self.assertRaisesRegex(ValueError, "unsupported local operation"):
            self.execute("cloud.admit")
        with self.assertRaisesRegex(ValueError, "unknown parameters"):
            self.execute("context.get", cloud_tenant="not-supported")

    def test_direct_contract_and_cli_share_one_governance_lifecycle(self):
        imported = self.execute("evidence.import", path=str(FIXTURE))
        self.assertEqual(imported["contract_status"], "internal_alpha")
        evidence_id = imported["result"]["evidence"][0]

        proposed = self.execute(
            "conclusion.propose",
            statement="The liability cap is 1x annual fees",
            evidence_refs=[evidence_id], scope="msa-negotiation",
            proposer="agent:runner", expires_at=None, artifact_refs=[],
            allowed_actors=["agent:successor"], qualifiers=None, profile=None,
        )
        conclusion_id = proposed["result"]["conclusion"]["id"]

        cli_evaluation = self.cli("evaluate", conclusion_id)
        direct_evaluation = self.execute(
            "conclusion.evaluate", conclusion_id=conclusion_id)["result"]
        self.assertEqual(cli_evaluation["checks"], direct_evaluation["checks"])
        self.assertEqual(cli_evaluation["eligible"], direct_evaluation["eligible"])

        cli_review = self.cli(
            "review", conclusion_id, "--admit", "--reviewer", "human:alice",
            "--request-id", "review-001")
        self.assertEqual(cli_review["result"]["type"], "conclusion_admitted")

        direct_context = self.execute(
            "context.get", scope="msa-negotiation", actor="agent:successor",
            task=None, include_blocked_statements=False)["result"]
        cli_context = self.cli(
            "context", "--scope", "msa-negotiation",
            "--actor", "agent:successor")
        self.assertEqual(cli_context, direct_context)
        self.assertEqual([row["id"] for row in direct_context["knowledge"]],
                         [conclusion_id])

    def test_cli_proposal_is_visible_through_direct_contract(self):
        evidence_id = self.cli("evidence", "import", str(FIXTURE))["evidence"][0]
        proposed = self.cli(
            "propose", "--statement", "The indemnity requires escalation",
            "--evidence", evidence_id, "--scope", "msa-negotiation",
            "--proposer", "agent:runner")
        conclusion_id = proposed["conclusion"]["id"]
        context = self.execute(
            "context.get", scope="msa-negotiation", actor=None, task=None,
            include_blocked_statements=False)["result"]
        self.assertEqual(context["knowledge"], [])
        self.assertEqual(context["blocked"][0]["id"], conclusion_id)
        self.assertEqual(context["blocked"][0]["reason"], "needs_review")


if __name__ == "__main__":
    unittest.main()

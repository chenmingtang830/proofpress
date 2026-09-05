import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CLI = (sys.executable, "-m", "proofpress.cli")
FIXTURE = ROOT / "examples" / "verified-knowledge-ledger" / "demo.otlp.json"
CONFORMANCE = ROOT / "tests" / "fixtures" / "local_operation_conformance_v1alpha1.json"


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
        from proofpress.kernel import operations as proofpress_knowledge
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
        result = subprocess.run([*CLI, *args], cwd=self.repo,
                                text=True, capture_output=True, check=True)
        return json.loads(result.stdout)

    def test_contract_returns_stable_validation_errors(self):
        unsupported_schema = self.knowledge.execute_local_operation({
            "schema_version": "proofpress/local-operation/future",
            "operation": "context.get", "parameters": {},
            "request_id": "request-001",
        })
        self.assertFalse(unsupported_schema["ok"])
        self.assertEqual(unsupported_schema["request_id"], "request-001")
        self.assertEqual(unsupported_schema["error"]["code"],
                         "unsupported_schema_version")
        self.assertFalse(unsupported_schema["error"]["retryable"])

        unsupported_operation = self.execute("cloud.admit")
        self.assertEqual(unsupported_operation["error"]["code"],
                         "unsupported_operation")

        invalid_parameters = self.execute(
            "context.get", cloud_tenant="not-supported")
        self.assertEqual(invalid_parameters["error"]["code"],
                         "invalid_parameters")
        self.assertEqual(invalid_parameters["error"]["details"]["unknown"],
                         ["cloud_tenant"])

        retired_reader_acl = self.execute(
            "conclusion.propose", statement="A bounded conclusion",
            evidence_refs=[], proposer="agent:test",
            allowed_actors=["agent:legal"])
        self.assertEqual(retired_reader_acl["error"]["code"],
                         "invalid_parameters")
        self.assertEqual(retired_reader_acl["error"]["details"]["unknown"],
                         ["allowed_actors"])

    def test_frozen_conformance_vectors(self):
        fixture = json.loads(CONFORMANCE.read_text(encoding="utf-8"))
        self.assertEqual(fixture["schema_version"],
                         "proofpress/local-operation-conformance/v1alpha1")
        for vector in fixture["vectors"]:
            with self.subTest(vector=vector["name"]):
                response = self.knowledge.execute_local_operation(vector["request"])
                expected = vector["expect"]
                self.assertEqual(response["ok"], expected["ok"])
                if expected["ok"]:
                    self.assertEqual(response["result"]["request_schema"],
                                     expected["result_schema_version"])
                else:
                    self.assertEqual(response["error"]["code"],
                                     expected["error_code"])

    def test_mutating_request_replay_is_persistent_and_conflicts_fail_closed(self):
        first = self.knowledge.execute_local_operation({
            "schema_version": self.knowledge.LOCAL_OPERATION_SCHEMA,
            "operation": "evidence.import",
            "parameters": {"path": str(FIXTURE)},
            "request_id": "request-first",
            "idempotency_key": "evidence-import-001",
        })
        self.assertTrue(first["ok"])
        event_count = len(self.knowledge.v2_events())

        replay = self.knowledge.execute_local_operation({
            "schema_version": self.knowledge.LOCAL_OPERATION_SCHEMA,
            "operation": "evidence.import",
            "parameters": {"path": str(FIXTURE)},
            "request_id": "request-retry",
            "idempotency_key": "evidence-import-001",
        })
        self.assertTrue(replay["ok"])
        self.assertTrue(replay["idempotent_replay"])
        self.assertEqual(replay["request_id"], "request-retry")
        self.assertEqual(replay["result"], first["result"])
        self.assertEqual(len(self.knowledge.v2_events()), event_count)
        self.assertTrue((self.repo / self.knowledge.LOCAL_IDEMPOTENCY_PATH).is_file())

        conflict = self.knowledge.execute_local_operation({
            "schema_version": self.knowledge.LOCAL_OPERATION_SCHEMA,
            "operation": "evidence.import",
            "parameters": {"path": str(self.repo / "different.json")},
            "idempotency_key": "evidence-import-001",
        })
        self.assertFalse(conflict["ok"])
        self.assertEqual(conflict["error"]["code"], "idempotency_conflict")

    def test_capabilities_are_negotiable_and_do_not_claim_future_surfaces(self):
        capabilities = self.knowledge.execute_local_operation({
            "schema_version": self.knowledge.LOCAL_OPERATION_SCHEMA,
            "operation": "capabilities.get", "parameters": {},
            "request_id": "capabilities-001",
        })
        self.assertTrue(capabilities["ok"])
        self.assertEqual(capabilities["request_id"], "capabilities-001")
        result = capabilities["result"]
        self.assertEqual(result["request_schema"],
                         self.knowledge.LOCAL_OPERATION_SCHEMA)
        operations = {item["name"]: item for item in result["operations"]}
        self.assertIn("configuration.get", operations)
        self.assertIn("conclusion.review", operations)
        self.assertIn("conclusion.judge", operations)
        self.assertIn("relation.resolve", operations)
        self.assertIn("graph.get", operations)
        self.assertIn("graph.traverse", operations)
        self.assertFalse(operations["graph.traverse"]["mutates"])
        self.assertEqual(operations["conclusion.review"]["replay_semantics"],
                         "parameter_request_id")
        self.assertEqual(result["not_available"],
                         ["localhost_http", "mcp", "cloud"])

    def test_governance_configuration_separates_roles_and_hides_command(self):
        policy_dir = self.repo / ".proofpress"
        policy_dir.mkdir()
        (policy_dir / "policy.json").write_text(json.dumps({
            "verification": {
                "identity": "verifier:customer-policy",
                "profile": "customer/legal-verification/v1",
            },
            "judge": {
                "identity": "judge:customer-advisory",
                "command": ["judge-adapter", "--token", "must-not-leak"],
                "timeout_seconds": 12,
            },
        }))
        configured = self.execute("configuration.get")
        self.assertTrue(configured["ok"])
        result = configured["result"]
        self.assertEqual(result["proposer"]["identity_source"],
                         "operation_parameter")
        self.assertEqual(result["verification"]["identity"],
                         "verifier:customer-policy")
        self.assertEqual(result["judge"]["identity"],
                         "judge:customer-advisory")
        self.assertTrue(result["judge"]["configured"])
        self.assertNotIn("command", result["judge"])
        self.assertNotIn("must-not-leak", json.dumps(result))
        self.assertFalse(result["authority_separation"]
                         ["proposer_may_verify_own_work"])
        self.assertFalse(result["authority_separation"]
                         ["proposer_may_judge_own_work"])
        self.assertFalse(result["authority_separation"]["judge_may_admit"])

    def test_configured_verifier_is_bound_and_cannot_be_the_proposer(self):
        imported = self.execute("evidence.import", path=str(FIXTURE))
        evidence_id = imported["result"]["evidence"][0]
        proposed = self.execute(
            "conclusion.propose", statement="The cap is one times fees",
            evidence_refs=[evidence_id], scope="matter-1",
            proposer="agent:runner")
        conclusion_id = proposed["result"]["conclusion"]["id"]
        evaluated = self.execute(
            "conclusion.evaluate", conclusion_id=conclusion_id)
        self.assertEqual(evaluated["result"]["verifier"],
                         "verifier:local-deterministic")
        self.assertEqual(evaluated["result"]["verification_profile"],
                         "proofpress/default-verification/v1")
        self.assertIn("verification_config_digest", evaluated["result"])

        self_proposed = self.execute(
            "conclusion.propose", statement="A separate candidate",
            evidence_refs=[evidence_id], scope="matter-1",
            proposer="verifier:local-deterministic")
        rejected = self.execute(
            "conclusion.evaluate",
            conclusion_id=self_proposed["result"]["conclusion"]["id"])
        self.assertEqual(rejected["error"]["code"], "operation_rejected")
        self.assertIn("may not act as configured verification identity",
                      rejected["error"]["message"])

    def test_configured_judge_cannot_be_the_proposer(self):
        imported = self.execute("evidence.import", path=str(FIXTURE))
        proposed = self.execute(
            "conclusion.propose", statement="The judge cannot self-assess",
            evidence_refs=[imported["result"]["evidence"][0]], scope="matter-1",
            proposer="judge:local-advisory")
        conclusion_id = proposed["result"]["conclusion"]["id"]
        with self.assertRaisesRegex(
                ValueError, "may not act as configured judge identity"):
            self.knowledge.judge_v2(conclusion_id)

    def test_kernel_rejections_use_the_operation_error_envelope(self):
        rejected = self.execute(
            "conclusion.evaluate", conclusion_id="conclusion-does-not-exist")
        self.assertFalse(rejected["ok"])
        self.assertEqual(rejected["error"]["code"], "operation_rejected")
        self.assertFalse(rejected["error"]["retryable"])

        missing_file = self.execute(
            "evidence.import", path=str(self.repo / "missing-evidence.json"))
        self.assertEqual(missing_file["error"]["code"], "resource_not_found")
        self.assertFalse(missing_file["error"]["retryable"])

    def test_direct_contract_and_cli_share_one_governance_lifecycle(self):
        imported = self.execute("evidence.import", path=str(FIXTURE))
        self.assertTrue(imported["ok"])
        self.assertEqual(imported["contract_status"], "internal_alpha")
        evidence_id = imported["result"]["evidence"][0]

        proposed = self.execute(
            "conclusion.propose",
            statement="The liability cap is 1x annual fees",
            evidence_refs=[evidence_id], scope="msa-negotiation",
            proposer="agent:runner", expires_at=None, artifact_refs=[],
            applicability=None, qualifiers=None, profile=None,
        )
        conclusion_id = proposed["result"]["conclusion"]["id"]

        cli_evaluation = self.cli("evaluate", conclusion_id)
        direct_evaluation = self.execute(
            "conclusion.evaluate", conclusion_id=conclusion_id)["result"]
        self.assertEqual(cli_evaluation["checks"], direct_evaluation["checks"])
        self.assertEqual(cli_evaluation["eligible"], direct_evaluation["eligible"])

        stale_review = self.execute(
            "conclusion.review", conclusion_id=conclusion_id,
            decision="admit", reviewer="human:alice",
            expected_head="stale-ledger-head")
        self.assertEqual(stale_review["error"]["code"],
                         "ledger_head_conflict")
        self.assertTrue(stale_review["error"]["retryable"])

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

    def test_relation_lifecycle_uses_the_shared_contract(self):
        evidence_id = self.execute(
            "evidence.import", path=str(FIXTURE))["result"]["evidence"][0]
        first = self.execute(
            "conclusion.propose", statement="The agreement limits liability",
            evidence_refs=[evidence_id], scope="matter-1", proposer="agent:one")
        second = self.execute(
            "conclusion.propose", statement="The cap excludes misconduct",
            evidence_refs=[evidence_id], scope="matter-1", proposer="agent:two")
        source_id = first["result"]["conclusion"]["id"]
        target_id = second["result"]["conclusion"]["id"]

        proposed = self.execute(
            "relation.propose", source_id=source_id, target_id=target_id,
            relation_type="qualifies", proposer="agent:relation")
        relation_id = proposed["result"]["relation"]["id"]
        cli_evaluation = self.cli("relation", "evaluate", relation_id)
        self.assertTrue(cli_evaluation["eligible"])

        for conclusion_id in (source_id, target_id):
            admitted = self.execute(
                "conclusion.review", conclusion_id=conclusion_id,
                decision="admit", reviewer="human:alice",
                request_id="admit-" + conclusion_id)
            self.assertTrue(admitted["ok"])

        reviewed = self.execute(
            "relation.review", relation_id=relation_id, decision="admit",
            reviewer="human:alice", request_id="relation-review-001")
        self.assertTrue(reviewed["ok"])
        self.assertEqual(reviewed["result"]["result"]["type"],
                         "relation_admitted")

        duplicate = self.execute(
            "relation.review", relation_id=relation_id, decision="admit",
            reviewer="human:alice", request_id="relation-review-001")
        self.assertTrue(duplicate["ok"])
        self.assertTrue(duplicate["result"]["idempotent"])

        graph = self.execute("graph.get", scope="matter-1")["result"]
        cli_graph = self.cli("graph", "--scope", "matter-1")
        self.assertEqual(cli_graph, graph)
        traversal = self.execute(
            "graph.traverse", seed_ids=[source_id], scope="matter-1",
            actor=None, task=None, max_depth=1, max_claims=2,
            state="admitted")
        self.assertTrue(traversal["ok"])
        self.assertEqual(set(traversal["result"]["conclusion_ids"]),
                         {source_id, target_id})
        self.assertEqual(traversal["result"]["relations"][0]["id"], relation_id)

    def test_cli_supersede_is_visible_through_contract_context(self):
        evidence_id = self.execute(
            "evidence.import", path=str(FIXTURE))["result"]["evidence"][0]
        old = self.execute(
            "conclusion.propose", statement="The old position",
            evidence_refs=[evidence_id], scope="matter-1", proposer="agent:one")
        new = self.execute(
            "conclusion.propose", statement="The replacement position",
            evidence_refs=[evidence_id], scope="matter-1", proposer="agent:two")
        old_id = old["result"]["conclusion"]["id"]
        new_id = new["result"]["conclusion"]["id"]
        superseded = self.cli(
            "supersede", old_id, "--by", new_id,
            "--reviewer", "human:alice")
        self.assertEqual(superseded["subject_ref"], old_id)
        self.assertEqual(superseded["superseded_by"], new_id)

        context = self.execute(
            "context.get", scope="matter-1",
            include_blocked_statements=True)["result"]
        blocked = {row["id"]: row for row in context["blocked"]}
        self.assertEqual(blocked[old_id]["reason"], "superseded")


if __name__ == "__main__":
    unittest.main()

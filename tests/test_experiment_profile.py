import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proofpress.profiles import experiment
from proofpress.kernel import operations as knowledge
from proofpress import ProofpressClient
from proofpress_mcp import ProofpressMcpGateway
from proofpress.hosted import HostedControlPlane


class ExperimentProfileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"],
                       cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"],
                       cwd=self.repo, check=True)
        self.previous = Path.cwd()
        os.chdir(self.repo)
        self.client = ProofpressClient.in_process(self.repo)

    def tearDown(self):
        os.chdir(self.previous)
        self.tmp.cleanup()

    @staticmethod
    def identity():
        return {"experiment_id": "exp-training-42", "run_id": "run-003",
                "model_revision": "model:abc123", "dataset_revision": "data:def456",
                "environment_digest": "sha256:" + "a" * 64,
                "config_digest": "sha256:" + "b" * 64}

    @staticmethod
    def retrieval_payload():
        quote = "accuracy,0.82"
        return {"schema_version": knowledge.RETRIEVAL_EVIDENCE_SCHEMA,
                "source": {"uri": "workspace://runs/003/metrics.csv",
                           "content_digest": "sha256:" + "c" * 64,
                           "media_type": "text/csv"},
                "evidence": {"quote": quote,
                             "locator": {"kind": "text_span", "start": 0,
                                         "end": len(quote),
                                         "text_digest": "sha256:" + hashlib.sha256(
                                             quote.encode()).hexdigest()}},
                "retrieval": {"adapter": "pioneer.metrics", "version": "1",
                              "query": "accuracy", "config_digest": "sha256:" + "d" * 64}}

    def submit_metric(self, value="0.82", unit="ratio"):
        source = self.client.submit_evidence(self.retrieval_payload())["imported_evidence"][0]
        payload = {"schema_version": experiment.PROFILE, "kind": "metric_observation",
                   "experiment": self.identity(),
                   "observation": {"name": "accuracy", "version": "v1",
                                   "value": value, "unit": unit,
                                   "population": "validation", "source_evidence_ref": source}}
        result = self.client.submit_evidence(payload, profile="experiment")
        return result["imported_evidence"][0], payload

    def test_sdk_mcp_transport_parity_and_human_admission_boundary(self):
        metric, _ = self.submit_metric()
        qualifiers = {"experiment": {"schema_version": experiment.PROFILE,
                     "conclusion_kind": "finding", "experiment": self.identity()}}
        sdk = self.client.propose_conclusion(
            "Validation accuracy was 0.82.", [metric], "pioneer", "agent:sdk",
            qualifiers=qualifiers, profile="experiment")
        self.assertEqual(sdk["conclusion"]["qualifiers"]["profile"], experiment.PROFILE)
        evaluated = self.client.evaluate_conclusion(sdk["conclusion"]["id"])
        self.assertTrue(evaluated["eligible"])
        self.assertTrue(all(evaluated["checks"].values()))
        self.assertEqual(self.client.context(scope="pioneer")["knowledge"], [])

        other = Path(self.tmp.name) / "mcp"
        other.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=other, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=other, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=other, check=True)
        mcp_client = ProofpressClient.in_process(other)
        gateway = ProofpressMcpGateway(mcp_client, "agent:mcp")
        os.chdir(other)
        source = gateway.submit_evidence(self.retrieval_payload())["imported_evidence"][0]
        payload = {"schema_version": experiment.PROFILE, "kind": "metric_observation",
                   "experiment": self.identity(), "observation": {"name": "accuracy",
                   "version": "v1", "value": "0.82", "unit": "ratio",
                   "population": "validation", "source_evidence_ref": source}}
        mcp = gateway.submit_evidence(payload, profile="experiment")
        projected = knowledge.v2_projection()["evidence"][mcp["imported_evidence"][0]]
        self.assertEqual(projected["experiment_profile"],
                         sdk_metric := knowledge.proofpress_experiment.normalize_evidence(
                             payload, knowledge.v2_projection()["evidence"]))
        self.assertEqual(sdk_metric["schema_version"], experiment.PROFILE)

    def test_hosted_transport_accepts_same_profile_without_granting_authority(self):
        control = HostedControlPlane(Path(self.tmp.name) / "hosted.db")
        owner = control.bootstrap("workspace:pioneer", "human:kelton", "Kelton")
        agent = control.issue_agent_credential(
            owner["token"], "agent:pioneer", "Pioneer agent")

        def operation(name, parameters, key):
            return {"schema_version": knowledge.LOCAL_OPERATION_SCHEMA,
                    "operation": name, "parameters": parameters,
                    "idempotency_key": key}

        source = control.execute(agent["token"], operation(
            "evidence.submit", {"payload": self.retrieval_payload()}, "source"))
        source_ref = source["result"]["imported_evidence"][0]
        payload = {"schema_version": experiment.PROFILE, "kind": "metric_observation",
                   "experiment": self.identity(), "observation": {"name": "accuracy",
                   "version": "v1", "value": "0.82", "unit": "ratio",
                   "population": "validation", "source_evidence_ref": source_ref}}
        submitted = control.execute(agent["token"], operation(
            "evidence.submit", {"payload": payload, "profile": "experiment"},
            "metric"))
        self.assertTrue(submitted["ok"])
        metric = submitted["result"]["imported_evidence"][0]
        qualifiers = {"experiment": {"schema_version": experiment.PROFILE,
                     "conclusion_kind": "finding", "experiment": self.identity()}}
        proposed = control.execute(agent["token"], operation(
            "conclusion.propose", {"statement": "Accuracy was 0.82.",
            "evidence_refs": [metric], "scope": "pioneer",
            "qualifiers": qualifiers, "profile": "experiment"}, "proposal"))
        self.assertTrue(proposed["ok"])
        context = control.execute(agent["token"], {
            "schema_version": knowledge.LOCAL_OPERATION_SCHEMA,
            "operation": "context.get", "parameters": {"scope": "pioneer"}})
        self.assertEqual(context["result"]["knowledge"], [])

    def test_capability_negotiation_advertises_additive_profile(self):
        capabilities = self.client.capabilities()
        self.assertEqual(capabilities["profiles"]["experiment_schema"], experiment.PROFILE)
        self.assertIn("experiment", capabilities["profiles"]["evidence"])

    def test_table_cell_and_derivation_recompute(self):
        metric, _ = self.submit_metric(value="82", unit="count")
        formula = {"name": "double", "version": "1", "operation": "sum"}
        inputs = [{"evidence_ref": metric, "value": "82", "unit": "count"},
                  {"evidence_ref": metric, "value": "82", "unit": "count"}]
        # Duplicate refs are rejected: create a source-bound table cell as input two.
        source = self.client.submit_evidence(self.retrieval_payload())["imported_evidence"][0]
        cell_payload = {"schema_version": experiment.PROFILE, "kind": "table_cell",
                        "experiment": self.identity(), "cell": {"table_id": "metrics",
                        "row": "accuracy", "column": "count", "value": "82",
                        "unit": "count", "source_evidence_ref": source}}
        cell = self.client.submit_evidence(
            cell_payload, profile="experiment")["imported_evidence"][0]
        inputs[1]["evidence_ref"] = cell
        output = {"value": "164", "unit": "count"}
        derivation = {"schema_version": experiment.PROFILE, "kind": "derivation",
                      "experiment": self.identity(), "derivation": {"formula": formula,
                      "input_evidence_refs": [metric, cell], "output": output,
                      "recomputation_digest": experiment.digest(
                          experiment.recomputation_payload(formula, inputs, output))}}
        result = self.client.submit_evidence(derivation, profile="experiment")
        self.assertEqual(len(result["imported_evidence"]), 1)
        derivation_ref = result["imported_evidence"][0]
        proposed = self.client.propose_conclusion(
            "The two exact counts sum to 164.", [derivation_ref], "pioneer",
            "agent:test", qualifiers={"experiment": {
                "schema_version": experiment.PROFILE,
                "conclusion_kind": "finding", "experiment": self.identity()}},
            profile="experiment")
        graph = knowledge.graph_v2(scope="pioneer")
        node_ids = {node["id"] for node in graph["nodes"]}
        self.assertTrue({metric, cell, derivation_ref,
                         proposed["conclusion"]["id"]}.issubset(node_ids))
        self.assertIn({"from": metric, "to": derivation_ref,
                       "type": "derived_from"}, graph["edges"])
        self.assertIn({"from": cell, "to": derivation_ref,
                       "type": "derived_from"}, graph["edges"])
        bad = {**derivation, "derivation": {**derivation["derivation"],
                                             "output": {"value": "165", "unit": "count"}}}
        with self.assertRaisesRegex(Exception, "does not recompute"):
            self.client.submit_evidence(bad, profile="experiment")

    def test_invalid_refs_digests_units_and_kinds_fail_closed(self):
        _, payload = self.submit_metric()
        payload["observation"]["source_evidence_ref"] = "evd_missing"
        with self.assertRaisesRegex(Exception, "unknown experiment source evidence"):
            self.client.submit_evidence(payload, profile="experiment")
        qualifiers = {"experiment": {"schema_version": experiment.PROFILE,
                     "conclusion_kind": "scientifically-proven", "experiment": self.identity()}}
        with self.assertRaisesRegex(Exception, "unknown experiment conclusion kind"):
            self.client.propose_conclusion("Invalid", [], "pioneer", "agent:test",
                                           qualifiers=qualifiers, profile="experiment")

    def test_failed_attempt_is_a_first_class_reusable_failure_record(self):
        metric, _ = self.submit_metric(value="0.61")
        failure = {"intervention": "Use retrieval configuration cfg-b.",
                   "expected_outcome": "Accuracy exceeds 0.80.",
                   "observed_outcome": "Accuracy was 0.61.",
                   "feedback_evidence_refs": [metric],
                   "invalidated_hypotheses": ["cfg-b improves this dataset revision"],
                   "repeat_policy": "retry-if-changed",
                   "changed_dimension_required": "dataset or retrieval configuration",
                   "next_action": "Try cfg-c and preserve cfg-b as the control."}
        qualifiers = {"experiment": {"schema_version": experiment.PROFILE,
                     "conclusion_kind": "failed-attempt", "experiment": self.identity(),
                     "failure": failure}}
        result = self.client.propose_conclusion(
            "Configuration cfg-b did not meet the accuracy target.", [metric],
            "pioneer", "agent:test", qualifiers=qualifiers, profile="experiment")
        self.assertEqual(result["conclusion"]["qualifiers"]["experiment"]["failure"], failure)
        evaluated = self.client.evaluate_conclusion(result["conclusion"]["id"])
        self.assertTrue(evaluated["checks"]["experiment_failure_feedback_bound"])

        missing = {"experiment": {"schema_version": experiment.PROFILE,
                   "conclusion_kind": "failed-attempt", "experiment": self.identity()}}
        with self.assertRaisesRegex(Exception, "explicit failure record"):
            self.client.propose_conclusion("Opaque failure.", [metric], "pioneer",
                                           "agent:test", qualifiers=missing,
                                           profile="experiment")


if __name__ == "__main__":
    unittest.main()

"""Reproduce capture format failures with synthetic selected-file inputs."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import Mock

from proofpress.capture_input import validate_claim_input
from proofpress.hosted.control_plane import HostedControlPlane
from proofpress.hosted import mcp_http
from proofpress.kernel.operations import normalize_retrieval_evidence_v1
from proofpress.mcp_schemas import capture_schema, EXPERIMENT_PROFILE
from proofpress.profiles.experiment import normalize_claim
from proofpress.transports.mcp import ProofpressMcpGateway, McpRequestError

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("prepare_evidence", ROOT / ".agents/skills/proofpress-governed-context/scripts/prepare_evidence.py")
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class CaptureInputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "synthetic-slides.bin"
        self.source.write_bytes(b"synthetic source bytes, not the text projection")
        self.text = self.root / "slide-3.txt"
        self.text.write_bytes("Slide 3\nAn observed result: β = 0.2.\n".encode())
        self.quote = self.root / "quote.txt"
        self.quote.write_bytes("An observed result: β = 0.2.".encode())
        self.config = self.root / "extraction.json"
        self.config.write_text('{"reader":"synthetic-test","version":"1","slide":3}')
        self.payload = helper.prepare(self.source, self.text, self.quote, self.config, "observed result", "synthetic-test", "1", 3)

    def test_selected_slide_hashes_are_real_and_payload_is_kernel_valid(self):
        receipt = normalize_retrieval_evidence_v1(self.payload)
        self.assertEqual(receipt["quote"], self.quote.read_text())
        self.assertEqual(receipt["locator"]["page_start"], 3)
        self.assertEqual(receipt["source"]["content_digest"], helper.digest(self.source.read_bytes()))
        self.assertEqual(receipt["locator"]["page_digest"], helper.digest(self.text.read_bytes()))
        config = json.dumps(json.loads(self.config.read_text()), sort_keys=True, separators=(",", ":")).encode()
        self.assertEqual(receipt["retrieval"]["config_digest"], "sha256:" + hashlib.sha256(config).hexdigest())
        self.assertNotEqual(receipt["source"]["content_digest"], receipt["locator"]["page_digest"])
        text_payload = helper.prepare(self.source, self.text, self.quote, self.config, "observed result", "synthetic-test", "1")
        self.assertEqual(normalize_retrieval_evidence_v1(text_payload)["locator"]["start"], len("Slide 3\n"))

    def test_helper_refuses_inexact_quote_empty_config_and_invalid_page(self):
        for page in (0, -1):
            with self.assertRaisesRegex(ValueError, "1-based"):
                helper.prepare(self.source, self.text, self.quote, self.config, "q", "a", "1", page)
        self.quote.write_text("Paraphrased result")
        with self.assertRaisesRegex(ValueError, "verbatim"):
            helper.prepare(self.source, self.text, self.quote, self.config, "q", "a", "1")
        self.config.write_text("{}")
        with self.assertRaisesRegex(ValueError, "non-empty JSON object"):
            helper.prepare(self.source, self.text, self.quote, self.config, "q", "a", "1")

    def malformed(self):
        quote = copy.deepcopy(self.payload)
        quote["evidence"]["quote"] = [quote["evidence"]["quote"]]
        config = copy.deepcopy(self.payload)
        config["retrieval"]["config_digest"] = ""
        section = copy.deepcopy(self.payload)
        section["evidence"]["locator"] = {"kind": "section_span", "section_id": "slide-3", "section_digest": helper.digest(self.text.read_bytes())}
        flat = copy.deepcopy(self.payload)
        flat.update(flat.pop("evidence"))
        return [quote, config, section, flat]

    def test_http_rejects_format_before_reserving_then_accepts_same_key(self):
        database = self.root / "hosted.db"
        control = HostedControlPlane(database)
        owner = control.bootstrap("workspace:synthetic", "human:test")
        agent = control.issue_agent_credential(owner["token"], "agent:test", "Test")
        context = control.authenticate(agent["token"])
        for payload in self.malformed():
            with self.assertRaisesRegex(ValueError, "before submission.*did not consume"):
                mcp_http.call_tool(control, context, "proofpress_submit_evidence", {"payload": payload, "idempotency_key": "same-key"}, "http://localhost")
        with sqlite3.connect(database) as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM hosted_executions").fetchone()[0], 0)
        args = {"payload": self.payload, "idempotency_key": "same-key"}
        result = mcp_http.call_tool(control, context, "proofpress_submit_evidence", args, "http://localhost")
        self.assertTrue(result["evidence"][0].startswith("evd_"))
        replay = mcp_http.call_tool(control, context, "proofpress_submit_evidence", args, "http://localhost")
        self.assertEqual(replay["evidence"], result["evidence"])

    def test_stdio_checks_before_client_and_discovery_is_read_only(self):
        client = Mock()
        gateway = ProofpressMcpGateway(client, "agent:test")
        for payload in self.malformed():
            with self.assertRaisesRegex(McpRequestError, "before submission"):
                gateway.submit_evidence(payload, idempotency_key="same-key")
        client.submit_evidence.assert_not_called()
        self.assertEqual(gateway.get_capture_schema(), mcp_http.call_tool(None, None, "proofpress_get_capture_schema", {}, ""))
        self.assertEqual(client.mock_calls, [])
        with self.assertRaisesRegex(McpRequestError, "qualifiers.experiment"):
            gateway.propose_claim("A result", ["evd_" + "a" * 16], profile="experiment", title="Result")
        client.propose_claim.assert_not_called()

    def test_experiment_closed_contract_matches_kernel_and_both_transports(self):
        from jsonschema import Draft202012Validator
        schema = capture_schema()
        identity = {"experiment_id": "synthetic", "run_id": "run-1", "model_revision": "model-1", "dataset_revision": "data-1",
                    "environment_digest": helper.digest(b"env"), "config_digest": helper.digest(b"config")}
        qualifiers = {"experiment": {"schema_version": EXPERIMENT_PROFILE, "claim_kind": "finding", "experiment": identity}}
        Draft202012Validator(schema["claim_qualifiers"]).validate(qualifiers)
        self.assertEqual(normalize_claim(qualifiers)["experiment"], qualifiers["experiment"])
        validate_claim_input(qualifiers, "experiment")
        for invalid in (None, {}, [], {"experiment": {**qualifiers["experiment"], "unknown": True}}):
            with self.assertRaises(ValueError):
                validate_claim_input(invalid, "experiment")
        evidence = {"schema_version": EXPERIMENT_PROFILE, "kind": "metric_observation", "experiment": identity,
                    "observation": {"name": "metric", "version": "1", "unit": "count", "value": 2,
                                    "population": "synthetic", "source_evidence_ref": "evd_" + "a" * 16}}
        Draft202012Validator(schema["experiment_evidence"]).validate(evidence)
        submitted = next(tool for tool in mcp_http.TOOLS if tool["name"] == "proofpress_submit_evidence")
        Draft202012Validator(submitted["inputSchema"]).validate({"payload": evidence, "profile": "experiment"})
        discovery = capture_schema()
        discovery["claim_qualifiers"]["properties"].clear()
        self.assertTrue(capture_schema()["claim_qualifiers"]["properties"])

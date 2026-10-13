"""The published MCP evidence schemas, checked against the kernel with a JSON Schema validator: what the kernel accepts
the schema accepts, what the schema refuses the kernel refuses, and every rule deliberately left to the kernel is named
here and in the schema's descriptions."""
from __future__ import annotations

import copy
import unittest

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - jsonschema comes with the mcp extra
    Draft202012Validator = None

from proofpress.kernel.operations import normalize_retrieval_evidence_v1
from proofpress.mcp_schemas import (EXPERIMENT_PROFILE, LOCATOR_SCHEMA, RETRIEVAL_EVIDENCE_INPUT_SCHEMA, retrieval_evidence_schema,
                                    stdio_evidence_payload_schema)
from proofpress.profiles.experiment import PROFILE

DIGEST = "sha256:" + "a" * 64
QUOTE = "Scope 1 emissions were 8,420 tCO2e."
LOCATORS = {
    "text_span": {"kind": "text_span", "start": 0, "end": len(QUOTE), "text_digest": DIGEST},
    "page_span": {"kind": "page_span", "page_start": 2, "page_end": 2, "page_digest": DIGEST},
    "section_span": {"kind": "section_span", "section_id": "s-1", "section_digest": DIGEST, "page_start": 2, "page_end": 3},
    "spreadsheet_cell": {"kind": "spreadsheet_cell", "sheet": "Data", "cell": "B7", "cell_digest": DIGEST},
    "json_pointer": {"kind": "json_pointer", "value": "/a/0"},
}


def envelope(locator: dict) -> dict:
    return {"schema_version": "proofpress/retrieval-evidence/v1",
            "source": {"uri": "reports/x.pdf", "content_digest": DIGEST},
            "evidence": {"quote": QUOTE, "locator": locator},
            "retrieval": {"adapter": "agent", "version": "1", "query": "scope 1", "config_digest": DIGEST}}


def kernel_accepts(payload: dict) -> bool:
    try:
        normalize_retrieval_evidence_v1(copy.deepcopy(payload))
    except ValueError:
        return False
    return True


@unittest.skipIf(Draft202012Validator is None, "jsonschema is not installed")
class EvidenceSchemaAgainstKernel(unittest.TestCase):
    def setUp(self):
        self.envelope = Draft202012Validator(retrieval_evidence_schema())
        self.stdio = Draft202012Validator(stdio_evidence_payload_schema())

    def test_the_schemas_are_valid_json_schema(self):
        Draft202012Validator.check_schema(retrieval_evidence_schema())
        Draft202012Validator.check_schema(stdio_evidence_payload_schema())

    def test_each_locator_kind_kernel_accepted_is_schema_valid(self):
        self.assertEqual([k["properties"]["kind"]["const"] for k in LOCATOR_SCHEMA["oneOf"]], list(LOCATORS))
        accepted = {**LOCATORS, "spreadsheet_cell (history null)": {**LOCATORS["spreadsheet_cell"], "previous_source_content_digest": None, "previous_cell_digest": None},
                    "spreadsheet_cell (history given)": {**LOCATORS["spreadsheet_cell"], "previous_source_content_digest": DIGEST, "previous_cell_digest": DIGEST},
                    "json_pointer (whole document)": {"kind": "json_pointer", "value": ""}}
        for name, loc in accepted.items():
            with self.subTest(name):
                self.assertTrue(kernel_accepts(envelope(loc)))
                self.assertTrue(self.envelope.is_valid(envelope(loc)), list(self.envelope.iter_errors(envelope(loc))))

    def test_what_the_schema_refuses_the_kernel_refuses(self):
        refused = {
            "unknown kind": {"kind": "line_span", "line": 3},
            "page_start missing": {k: v for k, v in LOCATORS["page_span"].items() if k != "page_start"},
            "page zero": {**LOCATORS["page_span"], "page_start": 0},
            "page as text": {**LOCATORS["page_span"], "page_start": "2"},
            "digest malformed": {**LOCATORS["page_span"], "page_digest": "abc"},
            "blank sheet": {**LOCATORS["spreadsheet_cell"], "sheet": " "},
            "blank section": {**LOCATORS["section_span"], "section_id": " "},
            "cell not A1": {**LOCATORS["spreadsheet_cell"], "cell": "b7"},
            "pointer without slash": {"kind": "json_pointer", "value": "a"},
            "pointer bad escape": {"kind": "json_pointer", "value": "/a~2b"},
            "pointer extra field": {"kind": "json_pointer", "value": "/a", "x": 1},
        }
        for name, loc in refused.items():
            with self.subTest(name):
                self.assertFalse(self.envelope.is_valid(envelope(loc)))
                self.assertFalse(kernel_accepts(envelope(loc)))
        self.assertFalse(self.envelope.is_valid({k: v for k, v in envelope(LOCATORS["page_span"]).items() if k != "retrieval"}))
        for name, loc in {"digest with a final newline": {**LOCATORS["page_span"], "page_digest": DIGEST + "\n"},
                          "pointer of one newline": {"kind": "json_pointer", "value": "\n"},
                          "cell with a final newline": {**LOCATORS["spreadsheet_cell"], "cell": "B7\n"}}.items():
            with self.subTest(name):
                self.assertFalse(self.envelope.is_valid(envelope(loc)))
                self.assertFalse(kernel_accepts(envelope(loc)))

    def test_each_published_required_field_is_one_the_kernel_requires(self):
        for kind_schema in LOCATOR_SCHEMA["oneOf"]:
            locator = LOCATORS[kind_schema["properties"]["kind"]["const"]]
            for field in kind_schema["required"]:
                with self.subTest(kind=locator["kind"], missing=field):
                    smaller = envelope({k: v for k, v in locator.items() if k != field})
                    self.assertFalse(self.envelope.is_valid(smaller))
                    self.assertFalse(kernel_accepts(smaller))

    def test_rules_left_to_the_kernel_are_named_here(self):
        """Rules deliberately left to the kernel: the schema accepts these, the kernel refuses them, and the schema's
        descriptions say so."""
        kernel_only = {
            "reversed page range": {**LOCATORS["page_span"], "page_start": 3, "page_end": 2},
            "text span length differs from the quote": {**LOCATORS["text_span"], "end": len(QUOTE) + 1},
            "cell past row 1048576": {**LOCATORS["spreadsheet_cell"], "cell": "A1048577"},
            "one history digest only": {**LOCATORS["spreadsheet_cell"], "previous_cell_digest": DIGEST},
            "column past XFD": {**LOCATORS["spreadsheet_cell"], "cell": "XFE1"},
            "page as 2.0": {**LOCATORS["page_span"], "page_start": 2.0, "page_end": 2.0},
        }
        for name, loc in kernel_only.items():
            with self.subTest(name):
                self.assertTrue(self.envelope.is_valid(envelope(loc)))
                self.assertFalse(kernel_accepts(envelope(loc)))
        described = " ".join(k["description"] for k in LOCATOR_SCHEMA["oneOf"])
        for phrase in ("page_end >= page_start", "end - start equals the quote's length", "row 1048576", "given together or not at all"):
            self.assertIn(phrase, described)
        self.assertIn("refuses 2.0", LOCATOR_SCHEMA["oneOf"][1]["properties"]["page_start"]["description"])

    def test_the_hosted_server_keeps_its_published_names(self):
        from proofpress.hosted import mcp_http
        from proofpress.mcp_schemas import SHA256_PATTERN

        self.assertEqual(mcp_http.RETRIEVAL_EVIDENCE_SCHEMA, retrieval_evidence_schema())
        self.assertEqual(mcp_http.SHA256_PATTERN, SHA256_PATTERN)

    def test_the_stdio_payload_is_an_envelope_or_an_experiment_payload_by_its_version(self):
        self.assertEqual(EXPERIMENT_PROFILE, PROFILE)
        self.assertTrue(self.stdio.is_valid(envelope(LOCATORS["page_span"])))
        self.assertFalse(self.stdio.is_valid(envelope({"kind": "line_span"})))  # a retrieval envelope must be one
        self.assertTrue(self.stdio.is_valid({"schema_version": PROFILE, "kind": "observation"}))
        self.assertFalse(self.stdio.is_valid({}))
        self.assertFalse(self.stdio.is_valid({"schema_version": "something/else"}))

    def test_each_transport_publishes_its_own_copy(self):
        a, b = retrieval_evidence_schema(), retrieval_evidence_schema()
        a["properties"]["evidence"]["properties"]["locator"]["oneOf"].clear()
        self.assertTrue(b["properties"]["evidence"]["properties"]["locator"]["oneOf"])
        self.assertTrue(RETRIEVAL_EVIDENCE_INPUT_SCHEMA["properties"]["evidence"]["properties"]["locator"]["oneOf"])


if __name__ == "__main__":
    unittest.main()

import hashlib
import unittest

from proofpress.integrations import (
    ContentAddressedReceiptAdapter,
    ContentAddressedReceiptError,
    build_retrieval_evidence,
)
from proofpress.kernel import operations as knowledge


def digest(value):
    return "sha256:" + hashlib.sha256(value.encode()).hexdigest()


class ContentAddressedAdapterTests(unittest.TestCase):
    def test_emits_normalized_receipt_without_retaining_adapter_configuration(self):
        adapter = ContentAddressedReceiptAdapter(
            adapter="company.document-index", version="2.1.0",
            config={"chunker": "paragraph-v2", "max_quote_chars": 500},
        )
        quote = "The approved Q4 budget is $1,050,000."
        receipt = adapter.evidence(
            source_uri="drive://finance/budget-q4.docx?revision=27",
            source_content_digest=digest("budget-q4-r27"), quote=quote,
            locator={"kind": "text_span", "start": 812, "end": 812 + len(quote),
                     "text_digest": digest("budget-q4-extracted-text-r27")},
            query="approved Q4 budget", media_type=(
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        )
        self.assertEqual(receipt["schema_version"], knowledge.RETRIEVAL_EVIDENCE_SCHEMA)
        self.assertEqual(receipt["retrieval"]["config_digest"], adapter.bound_config_digest)
        self.assertNotIn("config", receipt["retrieval"])
        self.assertNotIn("source_content", receipt["source"])
        self.assertEqual(knowledge.normalize_retrieval_evidence_v1({
            "schema_version": receipt["schema_version"],
            "source": receipt["source"],
            "evidence": {"quote": receipt["quote"], "locator": receipt["locator"]},
            "retrieval": receipt["retrieval"],
        }), receipt)

    def test_reuses_the_same_seam_for_a_spreadsheet_locator(self):
        quote = "Revenue!F12 changed from 1180000 to 1050000."
        receipt = build_retrieval_evidence(
            adapter="company.workbook-diff", version="1.0.0",
            config_digest=digest("workbook-diff-config-v1"),
            source_uri="workspace://finance/annual-plan.xlsx?revision=v18",
            source_content_digest=digest("annual-plan-v18"), quote=quote,
            locator={
                "kind": "spreadsheet_cell", "sheet": "Revenue", "cell": "F12",
                "cell_digest": digest("v18:Revenue!F12:1050000"),
                "previous_source_content_digest": digest("annual-plan-v17"),
                "previous_cell_digest": digest("v17:Revenue!F12:1180000"),
            }, query="Annual Plan Revenue!F12 revision",
        )
        self.assertEqual(receipt["locator"]["kind"], "spreadsheet_cell")
        self.assertEqual(receipt["source"]["content_digest"], digest("annual-plan-v18"))

    def test_requires_one_non_secret_configuration_binding(self):
        with self.assertRaisesRegex(ContentAddressedReceiptError, "exactly one"):
            ContentAddressedReceiptAdapter("company.index", "1", config={},
                                           config_digest=digest("also-bound"))
        with self.assertRaisesRegex(ContentAddressedReceiptError, "sha256"):
            build_retrieval_evidence(
                adapter="company.index", version="1", config={"mode": "safe"},
                source_uri="source://item/1", source_content_digest="not-a-digest",
                quote="A bounded quote.",
                locator={"kind": "text_span", "start": 0, "end": 16,
                         "text_digest": digest("source-text")}, query="item 1",
            )

import hashlib
import unittest

from proofpress.kernel import operations as knowledge


def digest(value):
    return "sha256:" + hashlib.sha256(value.encode()).hexdigest()


def payload(locator):
    quote = "Revenue!F12 changed from 1180000 to 1050000."
    return {
        "schema_version": knowledge.RETRIEVAL_EVIDENCE_SCHEMA,
        "source": {
            "uri": "workspace://finance/annual-plan.xlsx?revision=v18",
            "content_digest": digest("annual-plan-v18"),
            "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        },
        "evidence": {"quote": quote, "locator": locator},
        "retrieval": {
            "adapter": "company.workbook-diff", "version": "1.0.0",
            "query": "Annual Plan Revenue!F12 revision",
            "config_digest": digest("company.workbook-diff/1.0.0"),
        },
    }


class SpreadsheetEvidenceTests(unittest.TestCase):
    def test_cell_change_binds_current_and_previous_revisions(self):
        receipt = knowledge._retrieval_receipt(payload({
            "kind": "spreadsheet_cell", "sheet": "Revenue", "cell": "F12",
            "cell_digest": digest("v18:Revenue!F12:1050000"),
            "previous_source_content_digest": digest("annual-plan-v17"),
            "previous_cell_digest": digest("v17:Revenue!F12:1180000"),
        }))
        self.assertEqual(receipt["locator"], {
            "kind": "spreadsheet_cell", "sheet": "Revenue", "cell": "F12",
            "cell_digest": digest("v18:Revenue!F12:1050000"),
            "previous_source_content_digest": digest("annual-plan-v17"),
            "previous_cell_digest": digest("v17:Revenue!F12:1180000"),
        })

    def test_cell_locator_requires_a_canonical_address_and_paired_history(self):
        bad_address = {"kind": "spreadsheet_cell", "sheet": "Revenue", "cell": "$F$12",
                       "cell_digest": digest("current")}
        with self.assertRaisesRegex(ValueError, "canonical A1"):
            knowledge._retrieval_receipt(payload(bad_address))
        missing_prior_cell = {"kind": "spreadsheet_cell", "sheet": "Revenue", "cell": "F12",
                              "cell_digest": digest("current"),
                              "previous_source_content_digest": digest("previous")}
        with self.assertRaisesRegex(ValueError, "must be paired"):
            knowledge._retrieval_receipt(payload(missing_prior_cell))

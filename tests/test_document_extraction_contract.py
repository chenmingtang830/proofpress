import unittest

from document_extraction_contract import build_envelope, compare_envelopes, digest, validate_envelope


def fixture(value="18,486"):
    source = {"uri": "fixture/schedule.pdf", "content_digest": "sha256:" + "1" * 64,
              "media_type": "application/pdf"}
    extractor = {"provider": "fixture", "model": "canonical-control", "version": "1",
                 "license": "test-only", "config_digest": digest({"dpi": 144})}
    locator = {"page": 1, "bbox": [10, 10, 20, 20]}
    return build_envelope(source=source, extractor=extractor,
                          pages=[{"page": 1, "render_digest": "sha256:" + "2" * 64}],
                          blocks=[{"id": "block-1", "text": "Tax", "locator": locator}],
                          tables=[{"id": "table-1", "locator": locator,
                                   "cells": [{"row": 0, "column": 0, "raw_text": value,
                                              "locator": locator}]}])


class DocumentExtractionContractTests(unittest.TestCase):
    def test_valid_envelope_is_unadmitted_and_content_addressed(self):
        value = fixture()
        validate_envelope(value)
        self.assertFalse(value["admitted"])
        self.assertEqual(value["status"], "not_governed_candidate")

    def test_missing_cell_locator_fails_closed(self):
        value = fixture()
        del value["tables"][0]["cells"][0]["locator"]
        with self.assertRaisesRegex(ValueError, "locator"):
            validate_envelope(value)

    def test_digest_tamper_fails_closed(self):
        value = fixture()
        value["blocks"][0]["text"] = "changed"
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            validate_envelope(value)

    def test_provider_disagreement_becomes_review_conflict(self):
        receipt = compare_envelopes(fixture("18,486"), fixture("18,468"))
        self.assertEqual(receipt["resolution"], "human_review_required")
        self.assertEqual(len(receipt["conflicts"]), 1)


if __name__ == "__main__":
    unittest.main()

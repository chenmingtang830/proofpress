import unittest

from proofpress.integrations.document_extraction.contract import build_envelope, digest
from proofpress.integrations.document_extraction.qualification import GOLD_SCHEMA, score_envelope


class DocumentExtractionQualificationTests(unittest.TestCase):
    def test_scores_source_bound_structure_and_repeatability(self):
        source = {"uri": "fixture.pdf", "content_digest": "sha256:" + "1" * 64,
                  "media_type": "application/pdf"}
        locator = {"page": 1, "bbox": [0, 0, 50, 10]}
        envelope = build_envelope(
            source=source,
            extractor={"provider": "fixture", "model": "exact", "version": "1",
                       "license": "test", "config_digest": digest({})},
            pages=[{"page": 1, "render_digest": "sha256:" + "2" * 64}],
            blocks=[{"id": "a", "text": "Revenue 2024", "locator": locator}],
            tables=[{"id": "t1", "locator": locator, "cells": [
                {"row": 0, "column": 0, "raw_text": "Year", "locator": locator},
                {"row": 1, "column": 0, "raw_text": "2024", "locator": locator},
            ]}],
        )
        gold = {
            "schema_version": GOLD_SCHEMA,
            "source_content_digest": source["content_digest"],
            "blocks": [{"text": "Revenue 2024", "page": 1,
                        "bbox": locator["bbox"], "order": 1}],
            "tables": [{"page": 1, "cells": [
                [{"raw_text": "Year"}], [{"raw_text": "2024"}],
            ]}],
        }
        score = score_envelope(
            envelope, gold, repeat_extraction_digest=envelope["extraction_digest"])
        self.assertEqual(score["text_blocks"]["f1"], 1)
        self.assertEqual(score["table_cells"]["f1"], 1)
        self.assertTrue(score["repeatability"]["identical"])

    def test_source_mismatch_fails_closed(self):
        source = {"uri": "fixture.pdf", "content_digest": "sha256:" + "1" * 64,
                  "media_type": "application/pdf"}
        envelope = build_envelope(
            source=source,
            extractor={"provider": "x", "model": "x", "version": "1",
                       "license": "x", "config_digest": digest({})},
            pages=[{"page": 1, "render_digest": "sha256:" + "2" * 64}],
            blocks=[], tables=[])
        gold = {"schema_version": GOLD_SCHEMA,
                "source_content_digest": "sha256:" + "9" * 64,
                "blocks": [], "tables": []}
        with self.assertRaisesRegex(ValueError, "source digests differ"):
            score_envelope(envelope, gold)


if __name__ == "__main__":
    unittest.main()

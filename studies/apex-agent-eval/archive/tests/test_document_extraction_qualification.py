import unittest

from proofpress.integrations.document_extraction.contract import build_envelope, digest
from proofpress.integrations.document_extraction.qualification import GOLD_SCHEMA, score_envelope
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "studies/apex-agent-eval/retrieval_adapter"))
from score_document_extraction_panel_private import aggregate_fraction


class DocumentExtractionQualificationTests(unittest.TestCase):
    def test_scores_text_cells_numbers_locators_order_cross_page_and_repeatability(self):
        source = {"uri": "fixture.pdf", "content_digest": "sha256:" + "1" * 64,
                  "media_type": "application/pdf"}
        extractor = {"provider": "fixture", "model": "exact", "version": "1",
                     "license": "test", "config_digest": digest({})}
        left = {"page": 1, "bbox": [0, 0, 50, 10]}; right = {"page": 1, "bbox": [0, 20, 50, 30]}
        envelope = build_envelope(source=source, extractor=extractor,
            pages=[{"page": 1, "render_digest": "sha256:" + "2" * 64},
                   {"page": 2, "render_digest": "sha256:" + "3" * 64}],
            blocks=[{"id": "a", "text": "Revenue 2024", "locator": left},
                    {"id": "b", "text": "Total $18,486", "locator": right}],
            tables=[{"id": "t1", "locator": left, "continuation_id": "schedule",
                     "cells": [{"row": 0, "column": 0, "raw_text": "Year", "locator": left},
                               {"row": 0, "column": 1, "raw_text": "Tax", "locator": left},
                               {"row": 1, "column": 0, "raw_text": "2024", "locator": left},
                               {"row": 1, "column": 1, "raw_text": "$18,486", "locator": left}]}])
        gold = {"schema_version": GOLD_SCHEMA, "source_content_digest": source["content_digest"],
                "blocks": [{"text": "Revenue 2024", "page": 1, "bbox": left["bbox"], "order": 1},
                           {"text": "Total $18,486", "page": 1, "bbox": right["bbox"], "order": 2}],
                "tables": [{"page": 1, "continuation_id": "schedule", "cells": [
                    [{"raw_text": "Year"}, {"raw_text": "Tax"}],
                    [{"raw_text": "2024"}, {"raw_text": "$18,486"}]]}]}
        score = score_envelope(envelope, gold, repeat_extraction_digest=envelope["extraction_digest"])
        self.assertEqual(score["text_blocks"]["f1"], 1)
        self.assertEqual(score["table_cells"]["f1"], 1)
        self.assertEqual(score["numeric_values"]["f1"], 1)
        self.assertEqual(score["locators"]["rate"], 1)
        self.assertEqual(score["reading_order"]["rate"], 1)
        self.assertEqual(score["cross_page_continuations"]["f1"], 1)
        self.assertTrue(score["repeatability"]["identical"])

    def test_source_mismatch_fails_closed(self):
        source = {"uri": "fixture.pdf", "content_digest": "sha256:" + "1" * 64,
                  "media_type": "application/pdf"}
        envelope = build_envelope(source=source,
            extractor={"provider": "x", "model": "x", "version": "1", "license": "x",
                       "config_digest": digest({})},
            pages=[{"page": 1, "render_digest": "sha256:" + "2" * 64}], blocks=[], tables=[])
        gold = {"schema_version": GOLD_SCHEMA, "source_content_digest": "sha256:" + "9" * 64,
                "blocks": [], "tables": []}
        with self.assertRaisesRegex(ValueError, "source digests differ"):
            score_envelope(envelope, gold)

    def test_panel_aggregate_uses_micro_denominators(self):
        rows = [{"table_cells": {"matched": 2, "expected": 4, "observed": 2}},
                {"table_cells": {"matched": 1, "expected": 1, "observed": 3}}]
        result = aggregate_fraction(rows, "table_cells")
        self.assertEqual((result["matched"], result["expected"], result["observed"]), (3, 5, 5))
        self.assertEqual(result["f1"], 0.6)


if __name__ == "__main__":
    unittest.main()

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from proofpress.integrations.matter_catalog import SCHEMA, build_catalog
from proofpress.integrations.document_extraction.contract import build_envelope, digest


class MatterCatalogTests(unittest.TestCase):
    def test_all_sources_are_catalogued_and_cache_invalidates_on_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            text = root / "agreement.txt"; text.write_text("# Parties\nSeller and Buyer\n\f# Economics\nFees are fixed\n")
            data = root / "schedule.json"; data.write_text('{"z": 1, "a": 2}')
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"sources": [
                {"path": str(text), "uri": "matter/agreement.txt", "media_type": "text/plain"},
                {"path": str(data), "uri": "matter/schedule.json", "media_type": "application/json"},
            ]}))
            cache = root / "cache"
            first = build_catalog(manifest, cache_dir=cache)
            self.assertEqual(first["schema_version"], SCHEMA)
            self.assertEqual(len(first["sources"]), 2)
            self.assertEqual([r["page_count"] for r in first["representations"]], [2, 1])
            before = first["catalog_digest"]
            text.write_text("# Parties\nSeller, Buyer, and Guarantor\n\f# Economics\nFees are fixed\n")
            second = build_catalog(manifest, cache_dir=cache)
            self.assertNotEqual(before, second["catalog_digest"])
            self.assertNotEqual(first["representations"][0]["representation_digest"],
                                second["representations"][0]["representation_digest"])

    def test_manifest_digest_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / "memo.txt"; source.write_text("memo")
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"sources": [{"path": str(source), "uri": "memo.txt",
                "media_type": "text/plain", "content_digest": "sha256:" + "0" * 64}]}))
            with self.assertRaisesRegex(ValueError, "digest mismatch"):
                build_catalog(manifest)

    def test_identical_bytes_keep_distinct_source_custody_when_cached(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            left = root / "left.txt"; left.write_text("same bytes")
            right = root / "right.txt"; right.write_text("same bytes")
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"sources": [
                {"path": str(left), "uri": "matter/left.txt", "media_type": "text/plain"},
                {"path": str(right), "uri": "matter/right.txt", "media_type": "text/plain"},
            ]}))
            catalog = build_catalog(manifest, cache_dir=root / "cache")
            self.assertEqual(
                [row["source"]["uri"] for row in catalog["representations"]],
                ["matter/left.txt", "matter/right.txt"],
            )
            self.assertEqual(len({row["source"]["source_digest"] for row in catalog["representations"]}), 2)

    def test_validated_extraction_envelope_preserves_table_cells_as_tsv(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / "schedule.pdf"; source.write_bytes(b"fixture-pdf")
            source_digest = "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()
            locator = {"page": 1, "bbox": [1, 2, 3, 4]}
            envelope = build_envelope(
                source={"uri": "matter/schedule.pdf", "content_digest": source_digest,
                        "media_type": "application/pdf"},
                extractor={"provider": "fixture", "model": "table", "version": "1",
                           "license": "test-only", "config_digest": digest({"fixed": True})},
                pages=[{"page": 1, "render_digest": "sha256:" + "2" * 64}],
                blocks=[], tables=[{"id": "table-1", "locator": locator, "cells": [
                    {"row": 0, "column": 0, "raw_text": "Year", "locator": locator},
                    {"row": 0, "column": 1, "raw_text": "Tax", "locator": locator},
                    {"row": 1, "column": 0, "raw_text": "2024", "locator": locator},
                    {"row": 1, "column": 1, "raw_text": "$18,486", "locator": locator},
                ]}])
            envelope_path = root / "envelope.json"; envelope_path.write_text(json.dumps(envelope))
            catalog = build_catalog({"sources": [{"path": str(source), "uri": "matter/schedule.pdf",
                "media_type": "application/pdf", "extraction_envelope_path": str(envelope_path)}]})
            representation = catalog["representations"][0]
            self.assertEqual(representation["transform"]["mode"], "document-extraction-envelope")
            self.assertEqual(representation["sections"][0]["text"], "Year\tTax\n2024\t$18,486")

    def test_extraction_envelope_for_other_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / "schedule.pdf"; source.write_bytes(b"fixture-pdf")
            locator = {"page": 1}
            envelope = build_envelope(
                source={"uri": "other.pdf", "content_digest": "sha256:" + "1" * 64,
                        "media_type": "application/pdf"},
                extractor={"provider": "fixture", "model": "table", "version": "1",
                           "license": "test-only", "config_digest": digest({})},
                pages=[{"page": 1, "render_digest": "sha256:" + "2" * 64}], blocks=[],
                tables=[{"id": "t", "locator": locator,
                         "cells": [{"row": 0, "column": 0, "raw_text": "x", "locator": locator}]}])
            envelope_path = root / "envelope.json"; envelope_path.write_text(json.dumps(envelope))
            with self.assertRaisesRegex(ValueError, "source digest mismatch"):
                build_catalog({"sources": [{"path": str(source), "uri": "matter/schedule.pdf",
                    "media_type": "application/pdf", "extraction_envelope_path": str(envelope_path)}]})


if __name__ == "__main__":
    unittest.main()

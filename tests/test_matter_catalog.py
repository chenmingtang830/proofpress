import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from proofpress_matter_catalog import SCHEMA, build_catalog


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


if __name__ == "__main__":
    unittest.main()

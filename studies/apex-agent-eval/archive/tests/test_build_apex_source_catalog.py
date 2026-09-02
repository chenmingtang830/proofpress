import importlib.util
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/build_apex_source_catalog_private.py"
SPEC = importlib.util.spec_from_file_location("apex_source_catalog", PATH)
catalog_builder = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = catalog_builder
SPEC.loader.exec_module(catalog_builder)


WORD_DOCUMENT = """<?xml version="1.0" encoding="UTF-8"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>
<w:p><w:r><w:t>Tax schedule</w:t></w:r></w:p>
<w:tbl><w:tr><w:tc><w:p><w:r><w:t>Year</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Federal tax</w:t></w:r></w:p></w:tc></w:tr>
<w:tr><w:tc><w:p><w:r><w:t>2024</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>$18,486</w:t></w:r></w:p></w:tc></w:tr></w:tbl>
</w:body></w:document>"""


class ApexSourceCatalogTests(unittest.TestCase):
    def write_docx(self, path: Path) -> None:
        with zipfile.ZipFile(path, "w") as document:
            document.writestr("word/document.xml", WORD_DOCUMENT)

    def test_compiles_native_docx_table_and_non_office_sources(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "world"; root.mkdir()
            self.write_docx(root / "schedule.docx")
            (root / "calendar.ics").write_text("BEGIN:VCALENDAR\nSUMMARY:Tax deadline\nEND:VCALENDAR\n")
            (root / "state.json").write_text(json.dumps({"status": "open"}))
            (root / "ignored.bin").write_bytes(b"ignored")
            catalog, receipt = catalog_builder.build([root], max_section_chars=256)
        self.assertEqual(receipt["source_count"], 3)
        self.assertEqual(receipt["table_section_count"], 1)
        self.assertEqual(receipt["native_extraction_gap_count"], 0)
        docx = next(item for item in catalog["representations"]
                    if item["source"]["media_type"].endswith("wordprocessingml.document"))
        table = next(item for item in docx["sections"] if item["heading"] == "table-1")
        self.assertEqual(table["text"], "Year\tFederal tax\n2024\t$18,486")
        self.assertTrue(docx["source"]["uri"].startswith("apex://world/"))
        self.assertNotIn(str(root), json.dumps(catalog))
        self.assertFalse(catalog["automatic_admission"])
        self.assertTrue(catalog["human_approval_required"])

    def test_explicit_gap_keeps_an_unreadable_doc_source_visible(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "world"; root.mkdir()
            (root / "broken.docx").write_bytes(b"not a zip")
            catalog, receipt = catalog_builder.build([root])
            source_digest = catalog_builder.file_digest(root / "broken.docx")
        self.assertEqual(receipt["source_count"], 1)
        self.assertEqual(receipt["native_extraction_gap_count"], 1)
        self.assertEqual(catalog["representations"][0]["sections"][0]["heading"], "native-extraction-gap")
        self.assertEqual(catalog["representations"][0]["source"]["content_digest"],
                         source_digest)

    def test_empty_native_pdf_text_is_an_explicit_candidate_gap(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "world"; root.mkdir()
            source = root / "scan.pdf"; source.write_bytes(b"fixture")
            with patch.object(catalog_builder, "extract_units",
                              return_value=[("page-1-native-text-unavailable", 1, "")]):
                catalog, receipt = catalog_builder.build([root])
        self.assertEqual(receipt["native_extraction_gap_count"], 1)
        self.assertEqual(catalog["representations"][0]["extraction_gap"], "native_text_unavailable")


if __name__ == "__main__":
    unittest.main()

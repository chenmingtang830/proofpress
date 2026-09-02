import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

import proofpress_evidence as evidence


ROOT = Path(__file__).resolve().parents[1]
CLI = (sys.executable, "-m", "proofpress.cli")


def write_docx(
    path, text, *, reverse=False, compact=False,
    compression=zipfile.ZIP_DEFLATED,
):
    if compact:
        content_types = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '</Types>'
        )
        relationships = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
            'Target="word/document.xml"/>'
            '</Relationships>'
        )
        document_xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f'<w:body><w:p><w:r><w:t>{text}</w:t></w:r></w:p></w:body>'
            '</w:document>'
        )
    else:
        content_types = """<?xml version="1.0" encoding="UTF-8"?>
            <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
              <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
              <Default Extension="xml" ContentType="application/xml"/>
              <Override PartName="/word/document.xml"
                ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
            </Types>"""
        relationships = """<?xml version="1.0" encoding="UTF-8"?>
            <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
              <Relationship Id="rId1"
                Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
                Target="word/document.xml"/>
            </Relationships>"""
        document_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
            <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
              <w:body><w:p><w:r><w:t>{text}</w:t></w:r></w:p></w:body>
            </w:document>"""
    parts = [
        ("[Content_Types].xml", content_types),
        ("_rels/.rels", relationships),
        ("word/document.xml", document_xml),
    ]
    if reverse:
        parts.reverse()
    with zipfile.ZipFile(path, "w", compression=compression) as archive:
        for name, value in parts:
            archive.writestr(name, value)


def write_ooxml_fixture(path, main_part):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8"?>
            <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
              <Default Extension="xml" ContentType="application/xml"/>
            </Types>""",
        )
        archive.writestr(main_part, "<fixture/>")


class ArtifactProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.artifact = self.root / "report.pdf"
        self.artifact.write_bytes(b"%PDF-not-a-parser-test\x00\xff")

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *args, check=True):
        return subprocess.run(
            [*CLI, *args],
            cwd=self.root,
            text=True,
            capture_output=True,
            check=check,
        )

    def test_generic_artifact_creates_byte_evidence_only(self):
        envelope = evidence.create_evidence(self.artifact)

        self.assertEqual(envelope["protocol"], "proofpress.artifact-provenance")
        self.assertEqual(envelope["verification"]["level"], "byte")
        self.assertEqual(
            envelope["verification"]["adapter"], "proofpress.generic-binary")
        self.assertEqual(
            envelope["verification"]["provider"], "proofpress.digest")
        self.assertEqual(envelope["subject"]["media_type"], "application/pdf")
        self.assertTrue(evidence.verify_evidence(self.artifact, envelope).ok)

    def test_mutated_artifact_fails_byte_verification(self):
        envelope = evidence.create_evidence(self.artifact)
        self.artifact.write_bytes(self.artifact.read_bytes() + b"changed")

        result = evidence.verify_evidence(self.artifact, envelope)

        self.assertFalse(result.ok)
        self.assertEqual(result.status, "failed")
        self.assertTrue(all(check["status"] == "failed"
                            for check in result.checks))

    def test_generic_adapter_cannot_claim_semantic_verification(self):
        with self.assertRaisesRegex(
                evidence.EvidenceError, "cannot claim semantic"):
            evidence.create_evidence(self.artifact, level="semantic")

    def test_tampered_level_or_context_invalidates_envelope_id(self):
        envelope = evidence.create_evidence(
            self.artifact, context={"work_item": "work_123"})
        envelope["context"]["work_item"] = "work_other"

        with self.assertRaisesRegex(
                evidence.EvidenceError, "evidence_id does not match"):
            evidence.verify_evidence(self.artifact, envelope)

    def test_specific_adapter_can_be_registered_after_generic_fallback(self):
        class PdfAdapter:
            adapter_id = "example.pdf"
            max_level = "byte"

            def supports(self, path, media_type):
                return media_type == "application/pdf"

            def describe(self, path, media_type):
                return {
                    "name": path.name,
                    "media_type": media_type,
                    "byte_length": path.stat().st_size,
                    "format": "pdf",
                }

        registry = evidence.default_registry()
        registry.register_adapter(PdfAdapter())

        envelope = registry.create(self.artifact)

        self.assertEqual(envelope["verification"]["adapter"], "example.pdf")
        self.assertEqual(envelope["subject"]["format"], "pdf")

    def test_valid_pdf_uses_format_adapter_without_claiming_render(self):
        self.artifact.write_bytes(
            b"%PDF-1.7\n1 0 obj<</Type /Page>>endobj\n%%EOF\n")

        envelope = evidence.create_evidence(self.artifact)

        self.assertEqual(envelope["verification"]["level"], "byte")
        self.assertEqual(envelope["verification"]["adapter"], "proofpress.pdf")
        self.assertEqual(envelope["subject"]["format"], "pdf")
        self.assertEqual(envelope["subject"]["pdf"]["page_count_hint"], 1)

        self.artifact.write_bytes(self.artifact.read_bytes() + b"mutated")
        self.assertFalse(evidence.verify_evidence(self.artifact, envelope).ok)

    def test_other_ooxml_formats_remain_conservative_byte_evidence(self):
        fixtures = (
            ("review.pptx", "ppt/presentation.xml"),
            ("forecast.xlsx", "xl/workbook.xml"),
        )
        for filename, main_part in fixtures:
            with self.subTest(filename=filename):
                artifact = self.root / filename
                write_ooxml_fixture(artifact, main_part)

                envelope = evidence.create_evidence(artifact)

                self.assertEqual(envelope["verification"]["level"], "byte")
                self.assertEqual(
                    envelope["verification"]["adapter"],
                    "proofpress.generic-binary",
                )
                self.assertTrue(evidence.verify_evidence(artifact, envelope).ok)
                with self.assertRaisesRegex(
                        evidence.EvidenceError, "cannot claim semantic"):
                    evidence.create_evidence(artifact, level="semantic")

    def test_docx_defaults_to_semantic_evidence(self):
        document = self.root / "proposal.docx"
        write_docx(document, "Approve the launch")

        envelope = evidence.create_evidence(document)

        self.assertEqual(envelope["verification"]["level"], "semantic")
        self.assertEqual(
            envelope["verification"]["adapter"], "proofpress.ooxml-word")
        self.assertEqual(
            envelope["verification"]["provider"],
            "proofpress.ooxml-semantic",
        )
        self.assertEqual(envelope["subject"]["document"]["metrics"]["paragraphs"], 1)
        self.assertTrue(evidence.verify_evidence(document, envelope).ok)

    def test_docx_repackaging_preserves_semantic_verification(self):
        document = self.root / "proposal.docx"
        write_docx(document, "Same logical content")
        envelope = evidence.create_evidence(document)
        original_byte_digest = envelope["subject"]["digest"]["value"]

        write_docx(
            document, "Same logical content", reverse=True, compact=True,
            compression=zipfile.ZIP_STORED,
        )
        result = evidence.verify_evidence(document, envelope)

        self.assertNotEqual(evidence._sha256(document), original_byte_digest)
        self.assertTrue(result.ok)
        self.assertEqual(result.level, "semantic")

    def test_docx_content_change_fails_semantic_verification(self):
        document = self.root / "proposal.docx"
        write_docx(document, "Approved")
        envelope = evidence.create_evidence(document)

        write_docx(document, "Rejected")
        result = evidence.verify_evidence(document, envelope)

        self.assertFalse(result.ok)
        self.assertEqual(result.status, "failed")
        self.assertEqual(result.checks[0]["type"], "semantic_digest")
        self.assertEqual(result.checks[0]["status"], "failed")

    def test_docx_can_still_request_exact_byte_evidence(self):
        document = self.root / "proposal.docx"
        write_docx(document, "Exact package")

        envelope = evidence.create_evidence(document, level="byte")

        self.assertEqual(envelope["verification"]["level"], "byte")
        self.assertEqual(envelope["verification"]["provider"], "proofpress.digest")
        self.assertEqual(
            envelope["verification"]["adapter"], "proofpress.ooxml-word")

    def test_cli_auto_selects_docx_semantic_verification(self):
        document = self.root / "proposal.docx"
        evidence_path = self.root / "proposal.provenance.json"
        write_docx(document, "CLI semantic evidence")

        self.cli(
            "provenance", "create", str(document),
            "--output", str(evidence_path),
        )
        envelope = json.loads(evidence_path.read_text())
        self.assertEqual(envelope["verification"]["level"], "semantic")

        verified = self.cli(
            "provenance", "verify", str(document),
            "--evidence", str(evidence_path), "--json",
        )
        self.assertEqual(json.loads(verified.stdout)["status"], "verified")

    def test_cli_create_and_verify_arbitrary_binary(self):
        evidence_path = self.root / "report.provenance.json"
        created = self.cli(
            "provenance", "create", str(self.artifact),
            "--output", str(evidence_path),
        )
        self.assertIn("provenance evidence written", created.stdout)
        envelope = json.loads(evidence_path.read_text())
        self.assertEqual(envelope["verification"]["level"], "byte")

        verified = self.cli(
            "provenance", "verify", str(self.artifact),
            "--evidence", str(evidence_path), "--json",
        )
        result = json.loads(verified.stdout)
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["level"], "byte")

        self.artifact.write_bytes(b"different")
        failed = self.cli(
            "provenance", "verify", str(self.artifact),
            "--evidence", str(evidence_path), check=False,
        )
        self.assertEqual(failed.returncode, 1)
        self.assertIn("provenance failed", failed.stdout)


if __name__ == "__main__":
    unittest.main()

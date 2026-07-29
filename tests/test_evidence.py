import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import proofpress_evidence as evidence


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "proofpress.py"


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
            ["python3", str(CLI), *args],
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
                evidence.EvidenceError, "does not support semantic"):
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

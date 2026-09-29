import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from proofpress.kernel import operations
from proofpress.oaff_export import export_claim
import rfc8785


SOURCE = b"The documented cap is one year of fees.\n"
QUOTE = "one year of fees"


class OaffExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.previous = Path.cwd()
        os.chdir(self.tmp.name)
        subprocess.run(["git", "init", "-q"], check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], check=True)
        self.evidence_id = operations.submit_evidence_v2({
            "schema_version": "proofpress/retrieval-evidence/v1",
            "source": {"uri": "private/source.txt", "content_digest":
                       "sha256:" + hashlib.sha256(SOURCE).hexdigest()},
            "evidence": {"quote": QUOTE, "locator": {
                "kind": "text_span", "start": 22, "end": 22 + len(QUOTE),
                "text_digest": "sha256:" + hashlib.sha256(SOURCE.decode().encode()).hexdigest(),
            }},
            "retrieval": {"adapter": "test", "version": "1", "query": "cap",
                          "config_digest": "sha256:" + "a" * 64},
        })["evidence"][0]
        self.sources = {self.evidence_id: ("https://example.org/sources/cap", SOURCE)}
        self.claim = operations.propose_v2(
            "The cap is one year of fees.", [self.evidence_id],
            proposer="agent:tester", applicability={
                "description": "The identified contract revision.",
                "validity_conditions": ["Only this contract revision"],
            })["claim"]

    def tearDown(self):
        os.chdir(self.previous)
        self.tmp.cleanup()

    def export(self):
        return export_claim(self.claim["id"], namespace="https://example.org/oaff",
                            sources=self.sources)

    def test_candidate_has_exact_digest_and_no_private_source_uri(self):
        package = self.export()
        self.assertEqual(package["receipts"], [])
        self.assertNotIn("private/source.txt", json.dumps(package))
        unsigned = {key: value for key, value in package.items() if key != "integrity"}
        self.assertEqual(package["integrity"]["digest"],
                         hashlib.sha256(rfc8785.dumps(unsigned)).hexdigest())
        self.assertEqual(package["finding"]["evidence"][0]["content_digest"]["value"],
                         hashlib.sha256(SOURCE).hexdigest())

    def test_missing_or_changed_bytes_and_scope_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "exactly one source"):
            export_claim(self.claim["id"], namespace="https://example.org/oaff", sources={})
        with self.assertRaisesRegex(ValueError, "do not match"):
            export_claim(self.claim["id"], namespace="https://example.org/oaff",
                         sources={self.evidence_id: ("https://example.org/source", b"different")})
        with self.assertRaisesRegex(ValueError, "credential-free"):
            export_claim(self.claim["id"], namespace="https://example.org/oaff",
                         sources={self.evidence_id: ("https://example.org/source?token=secret", SOURCE)})
        unscoped = operations.propose_v2(
            "A second observation.", [self.evidence_id], proposer="agent:tester"
        )["claim"]
        with self.assertRaisesRegex(ValueError, "explicit applicability"):
            export_claim(unscoped["id"], namespace="https://example.org/oaff",
                         sources=self.sources)

    def test_human_admission_is_attributed_not_local_authority(self):
        operations.evaluate_v2(self.claim["id"])
        operations.review_v2(self.claim["id"], "admit", "human:reviewer")
        package = self.export()
        receipt = package["receipts"][0]
        self.assertEqual(receipt["authority_basis"], "human_approval")
        self.assertEqual(receipt["subject_revision"], package["finding"]["revision"])

    @unittest.skipUnless(importlib.util.find_spec("oaff"), "standalone OAFF verifier unavailable")
    def test_standalone_verifier_keeps_local_authority_unassessed(self):
        from oaff.verify import verify_bytes
        package = self.export()
        report = verify_bytes(json.dumps(package).encode())
        self.assertEqual(report["status"], "valid_with_limits")
        self.assertEqual(report["local_authority"], "not_evaluated")


if __name__ == "__main__":
    unittest.main()

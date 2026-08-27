import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "studies/rsi-exam-experiment-provenance/fixtures/valid"
VERIFIER_PATH = REPO_ROOT / "studies/rsi-exam-experiment-provenance/verify_capsule.py"

_SPEC = importlib.util.spec_from_file_location("rsi_exam_verifier", VERIFIER_PATH)
assert _SPEC and _SPEC.loader
_VERIFIER = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_VERIFIER)


class RsiExamProvenanceVerifierTests(unittest.TestCase):
    def materialize(self):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name) / "capsule"
        shutil.copytree(FIXTURE_ROOT, root)
        self.addCleanup(temp.cleanup)
        return root / "capsule.json", root

    @staticmethod
    def load(capsule_path):
        return json.loads(capsule_path.read_text(encoding="utf-8"))

    @staticmethod
    def save(capsule_path, data):
        capsule_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    @staticmethod
    def refresh_manifest_digest(capsule_path, root):
        data = RsiExamProvenanceVerifierTests.load(capsule_path)
        manifest = root / "source/manifest.json"
        data["source"]["manifest"]["sha256"] = hashlib.sha256(manifest.read_bytes()).hexdigest()
        RsiExamProvenanceVerifierTests.save(capsule_path, data)

    def test_valid_fixture_is_complete(self):
        capsule, root = self.materialize()

        result = _VERIFIER.verify_capsule(capsule, root)

        self.assertTrue(result["ok"])
        self.assertEqual(result["integrity"], "pass")
        self.assertEqual(result["coverage"], "complete")

    def test_artifact_tampering_is_rejected(self):
        capsule, root = self.materialize()
        (root / "artifacts/v2.py").write_text(
            (root / "artifacts/v2.py").read_text(encoding="utf-8") + "\n# tampered\n",
            encoding="utf-8",
        )

        result = _VERIFIER.verify_capsule(capsule, root)

        self.assertFalse(result["ok"])
        self.assertIn("artifact:v2:digest_mismatch", result["errors"])

    def test_receipt_tampering_is_rejected(self):
        capsule, root = self.materialize()
        (root / "receipts/v2-hidden.json").write_text("{}\n", encoding="utf-8")

        result = _VERIFIER.verify_capsule(capsule, root)

        self.assertFalse(result["ok"])
        self.assertIn("hidden:receipt:digest_mismatch", result["errors"])

    def test_score_tampering_is_rejected(self):
        capsule, root = self.materialize()
        data = self.load(capsule)
        data["hidden_evaluation"]["score"] = 0.99
        self.save(capsule, data)

        result = _VERIFIER.verify_capsule(capsule, root)

        self.assertFalse(result["ok"])
        self.assertIn("hidden:receipt:score_mismatch", result["errors"])

    def test_final_hidden_version_binding_is_rejected(self):
        capsule, root = self.materialize()
        data = self.load(capsule)
        data["hidden_evaluation"]["version_id"] = "v1"
        self.save(capsule, data)

        result = _VERIFIER.verify_capsule(capsule, root)

        self.assertFalse(result["ok"])
        self.assertIn("final_hidden_version_binding", result["errors"])

    def test_missing_parent_is_rejected(self):
        capsule, root = self.materialize()
        data = self.load(capsule)
        data["versions"][2]["parent_ids"] = ["missing-version"]
        self.save(capsule, data)

        result = _VERIFIER.verify_capsule(capsule, root)

        self.assertFalse(result["ok"])
        self.assertIn("version:v2:missing_parent", result["errors"])

    def test_non_acyclic_version_edges_are_rejected(self):
        capsule, root = self.materialize()
        data = self.load(capsule)
        data["versions"][0]["parent_ids"] = ["v2"]
        self.save(capsule, data)

        result = _VERIFIER.verify_capsule(capsule, root)

        self.assertFalse(result["ok"])
        self.assertIn("version:v0:parent_order", result["errors"])

    def test_evaluator_and_configuration_drift_are_rejected(self):
        capsule, root = self.materialize()
        data = self.load(capsule)
        data["versions"][1]["visible_evaluation"]["evaluator_digest"] = "9" * 64
        self.save(capsule, data)

        result = _VERIFIER.verify_capsule(capsule, root)

        self.assertFalse(result["ok"])
        self.assertIn("visible:v1:evaluator_drift", result["errors"])

        data["versions"][1]["visible_evaluation"]["evaluator_digest"] = "6" * 64
        self.save(capsule, data)
        manifest_path = root / "source/manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["config_digest"] = "a" * 64
        manifest_path.write_text(json.dumps(manifest, separators=(",", ":")), encoding="utf-8")
        self.refresh_manifest_digest(capsule, root)

        result = _VERIFIER.verify_capsule(capsule, root)

        self.assertFalse(result["ok"])
        self.assertIn("manifest:config_mismatch", result["errors"])

    def test_forbidden_raw_payload_is_rejected(self):
        capsule, root = self.materialize()
        data = self.load(capsule)
        data["prompt"] = "never store this in a capsule"
        self.save(capsule, data)

        result = _VERIFIER.verify_capsule(capsule, root)

        self.assertFalse(result["ok"])
        self.assertIn("forbidden_payload:$.prompt", result["errors"])

    def test_manifest_with_unrepresented_event_is_partial(self):
        capsule, root = self.materialize()
        manifest_path = root / "source/manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["event_ids"].append("unrepresented-event")
        manifest_path.write_text(json.dumps(manifest, separators=(",", ":")), encoding="utf-8")
        self.refresh_manifest_digest(capsule, root)

        result = _VERIFIER.verify_capsule(capsule, root)

        self.assertTrue(result["ok"])
        self.assertEqual(result["coverage"], "partial")

    def test_missing_manifest_is_unverifiable_not_complete(self):
        capsule, root = self.materialize()
        data = self.load(capsule)
        data["source"]["manifest"] = None
        self.save(capsule, data)

        result = _VERIFIER.verify_capsule(capsule, root)

        self.assertTrue(result["ok"])
        self.assertEqual(result["coverage"], "unverifiable")


if __name__ == "__main__":
    unittest.main()

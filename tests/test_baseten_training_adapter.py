import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "baseten_training_v0.json"
sys.path.insert(0, str(ROOT / "src"))

from proofpress import ProofpressClient
from proofpress.integrations.baseten_training import to_external_experiment


class BasetenTrainingAdapterTests(unittest.TestCase):
    def bundle(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_projects_provider_records_without_retaining_raw_payloads(self):
        bundle = self.bundle()
        manifest = to_external_experiment(bundle)

        self.assertEqual(manifest["source"]["system"], "baseten.training_jobs")
        self.assertEqual(manifest["source"]["run_id"], "job-42")
        self.assertEqual(manifest["adapter"], {
            "name": "baseten_training", "version": "0"})
        self.assertEqual(len(manifest["evidence"]), 2)
        expected = "sha256:" + hashlib.sha256(json.dumps(
            bundle["records"][0]["payload"], ensure_ascii=False,
            sort_keys=True, separators=(",", ":"), allow_nan=False,
        ).encode("utf-8")).hexdigest()
        self.assertEqual(manifest["evidence"][0]["source_digest"], expected)
        self.assertEqual(manifest["evidence"][1]["locator"], {
            "kind": "json_pointer", "value": "/checkpoints/0"})
        serialized = json.dumps(manifest)
        self.assertNotIn("payload", serialized)
        self.assertNotIn("artifact_presigned_urls", serialized)

    def test_selection_plan_and_source_payload_are_digest_bound(self):
        first = to_external_experiment(self.bundle())
        changed_payload = self.bundle()
        changed_payload["records"][0]["payload"]["training_job"]["updated_at"] = (
            "2026-09-17T19:46:00Z")
        second = to_external_experiment(changed_payload)
        self.assertNotEqual(first["evidence"][0]["source_digest"],
                            second["evidence"][0]["source_digest"])
        self.assertEqual(first["binding"]["config_digest"],
                         second["binding"]["config_digest"])

        changed_selection = self.bundle()
        changed_selection["records"][0]["selections"][0]["artifact_type"] = "other"
        third = to_external_experiment(changed_selection)
        self.assertNotEqual(first["binding"]["config_digest"],
                            third["binding"]["config_digest"])

    def test_rejects_identity_mismatch_and_unresolved_pointer(self):
        mismatch = self.bundle()
        mismatch["records"][0]["payload"]["training_job"]["id"] = "job-other"
        with self.assertRaisesRegex(ValueError, "job id does not match"):
            to_external_experiment(mismatch)

        missing = self.bundle()
        missing["records"][1]["selections"][0]["pointer"] = "/checkpoints/9"
        with self.assertRaisesRegex(ValueError, "does not resolve"):
            to_external_experiment(missing)

        unbound = self.bundle()
        unbound["records"][1]["payload"].pop("training_job")
        with self.assertRaisesRegex(ValueError, "must contain training_job identity"):
            to_external_experiment(unbound)

    def test_rejects_noncanonical_array_indices(self):
        bundle = self.bundle()
        bundle["records"][1]["selections"][0]["pointer"] = "/checkpoints/00"
        with self.assertRaisesRegex(ValueError, "does not resolve"):
            to_external_experiment(bundle)

    def test_rejects_credential_bearing_source_uris(self):
        bundle = self.bundle()
        bundle["records"][0]["source_uri"] += "?access_token=secret"
        with self.assertRaisesRegex(ValueError, "credential query parameters"):
            to_external_experiment(bundle)

    def test_loops_identity_and_checkpoint_uri_are_supported(self):
        bundle = self.bundle()
        bundle["source"] = {
            "product": "loops", "run_id": "loops-run-1",
            "session_id": "session-1",
            "uri": "https://app.baseten.co/loops/runs/loops-run-1",
            "capture_mode": "exported_bundle",
            "provenance_status": "importer_attested",
            "coverage": "partial",
            "known_omissions": ["raw_rollouts"],
        }
        bundle["records"] = [{
            "name": "run", "record_type": "job",
            "source_uri": "https://api.baseten.co/v1/loops/runs/loops-run-1",
            "payload": {"run": {
                "id": "loops-run-1", "session_id": "session-1",
                "base_model": "Qwen/Qwen3-0.6B", "status": "ACTIVE",
                "checkpoint_uri": "bt://loops:loops-run-1/weights/step-100",
            }},
            "selections": [{
                "pointer": "/run/checkpoint_uri",
                "observation": "Loops run loops-run-1 published checkpoint step-100.",
                "artifact_type": "checkpoint",
                "selection_reason": "Bind the stable Loops checkpoint URI.",
            }],
        }]
        manifest = to_external_experiment(bundle)
        self.assertEqual(manifest["source"]["system"], "baseten.loops")
        self.assertEqual(manifest["evidence"][0]["artifact_type"], "checkpoint")

    def test_cli_projects_locally_then_ingests_only_generic_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"],
                           cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"],
                           cwd=repo, check=True)
            previous = Path.cwd()
            try:
                os.chdir(repo)
                client = ProofpressClient.in_process(repo)
                run = client.start_run(
                    "Review Baseten training evidence", actor="agent:researcher")
                bundle = self.bundle()
                bundle["binding"]["proofpress_run_id"] = run["id"]
                path = repo / "baseten-export.json"
                path.write_text(json.dumps(bundle), encoding="utf-8")
                env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
                result = subprocess.run([
                    sys.executable, "-m", "proofpress.cli", "experiment",
                    "--actor", "agent:researcher", "ingest-baseten", str(path),
                    "--idempotency-key", "baseten-job-42-v1",
                ], cwd=repo, env=env, text=True, capture_output=True, check=True)
                output = json.loads(result.stdout)
                self.assertEqual(output["external_run_id"], "job-42")
                self.assertEqual(len(output["imported_evidence"]), 2)
                detail = client.get_run(run["id"], actor="agent:researcher")
                serialized = json.dumps(detail["external_evidence"])
                self.assertNotIn("reward-model-v4", serialized)
                self.assertNotIn('"payload"', serialized)
            finally:
                os.chdir(previous)


if __name__ == "__main__":
    unittest.main()

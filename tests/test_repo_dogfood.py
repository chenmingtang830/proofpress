import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proofpress.integrations import repository as proofpress_repo
from proofpress import client as proofpress_sdk


class RepoDogfoodTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.repo, check=True)
        subprocess.run(["git", "remote", "add", "origin",
                        "https://github.com/chenmingtang830/proofpress.git"],
                       cwd=self.repo, check=True)
        (self.repo / "README.md").write_text("base\n", encoding="utf-8")
        self._commit("base")
        self.base = self._head()
        self.previous = Path.cwd()
        os.chdir(self.repo)
        self.client = proofpress_sdk.ProofpressClient.in_process(self.repo)

    def tearDown(self):
        os.chdir(self.previous)
        self.tmp.cleanup()

    def _commit(self, message):
        subprocess.run(["git", "add", "README.md"], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", message], cwd=self.repo, check=True)

    def _head(self):
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=self.repo, text=True).strip()

    def _change(self, text, name):
        (self.repo / "README.md").write_text(text, encoding="utf-8")
        self._commit(name)
        head = self._head()
        receipt = self.repo / f"{name}-check.json"
        receipt.write_text(json.dumps({
            "name": "unit tests", "status": "pass", "commit": head,
            "command": "python3 -m unittest",
            "output_digest": "sha256:" + hashlib.sha256(b"OK").hexdigest(),
        }), encoding="utf-8")
        bundle_path = self.repo / f"{name}-bundle.json"
        bundle = proofpress_repo.build_bundle(
            self.repo, base_ref=self.base, head_ref=head,
            check_receipts=[receipt], pr_number=72,
            pr_url="https://github.com/chenmingtang830/proofpress/pull/72")
        proofpress_repo.write_bundle(bundle_path, bundle)
        return bundle_path, bundle

    def test_bundle_binds_repository_diff_commit_and_check_receipt(self):
        bundle_path, bundle = self._change("head\n", "head")
        checks = proofpress_repo.verify_bundle(bundle, self.repo)
        self.assertTrue(all(checks.values()), checks)
        self.assertEqual(bundle["change"]["changed_paths"], ["README.md"])
        self.assertEqual(bundle["checks"][0]["commit"], self._head())
        imported = self.client.import_evidence(bundle_path, idempotency_key="repo-import")
        self.assertEqual(len(imported["imported_evidence"]), 1)

    def test_candidate_stops_before_human_approval_and_roadmap_is_blocked(self):
        bundle_path, _ = self._change("head\n", "head")
        prepared = proofpress_repo.propose_candidate(
            self.client, bundle_path,
            statement="The repository dogfood profile is planned for Cloud deployment.",
            claim_kind="roadmap", scope="repo:proofpress", proposer="agent:coder",
            idempotency_prefix="repo-roadmap")
        self.assertFalse(prepared["evaluation"]["eligible"])
        self.assertFalse(prepared["evaluation"]["checks"]["repo_claim_is_current_fact"])
        self.assertEqual(self.client.context(scope="repo:proofpress")["knowledge"], [])
        with self.assertRaises(proofpress_sdk.ProofpressError):
            self.client.review_conclusion(
                prepared["candidate"]["id"], "admit", "human:maintainer",
                review_request_id="review-roadmap")

    def test_admitted_capability_reaches_context_and_can_be_superseded(self):
        first_path, _ = self._change("first\n", "first")
        first = proofpress_repo.propose_candidate(
            self.client, first_path, statement="The repo workflow supports version one.",
            claim_kind="capability", scope="repo:proofpress", proposer="agent:coder",
            idempotency_prefix="repo-first")
        first_id = first["candidate"]["id"]
        self.client.review_conclusion(
            first_id, "admit", "human:maintainer",
            review_request_id="review-first")
        self.assertEqual(
            [row["id"] for row in self.client.context(scope="repo:proofpress")["knowledge"]],
            [first_id])

        second_path, _ = self._change("second\n", "second")
        second = proofpress_repo.propose_candidate(
            self.client, second_path, statement="The repo workflow supports version two.",
            claim_kind="capability", scope="repo:proofpress", proposer="agent:coder",
            idempotency_prefix="repo-second")
        second_id = second["candidate"]["id"]
        self.client.review_conclusion(
            second_id, "admit", "human:maintainer",
            review_request_id="review-second")
        self.client.supersede_conclusion(
            first_id, second_id, "human:maintainer", note="version two replaces version one")
        context_ids = [row["id"] for row in
                       self.client.context(scope="repo:proofpress")["knowledge"]]
        self.assertEqual(context_ids, [second_id])

    def test_bundle_fails_closed_for_wrong_check_commit_and_credentials(self):
        (self.repo / "README.md").write_text("head\n", encoding="utf-8")
        self._commit("head")
        receipt = self.repo / "bad.json"
        receipt.write_text(json.dumps({"name": "tests", "status": "pass",
                                       "commit": self.base}), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "head commit"):
            proofpress_repo.build_bundle(
                self.repo, base_ref=self.base, check_receipts=[receipt])
        subprocess.run(["git", "remote", "set-url", "origin",
                        "https://token@example.com/repo.git"], cwd=self.repo, check=True)
        with self.assertRaisesRegex(ValueError, "credentials"):
            proofpress_repo.build_bundle(
                self.repo, base_ref=self.base, check_receipts=[receipt])


if __name__ == "__main__":
    unittest.main()

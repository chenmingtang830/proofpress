import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proofpress.integrations import research_blueprint as rd
from proofpress import ProofpressClient


class RdBlueprintTests(unittest.TestCase):
    def fixture(self):
        return json.loads((ROOT / "studies/proofpress-rd/lineage/pr55-pr61.json").read_text())

    def test_real_lineage_compiles_deterministically(self):
        first = rd.compile_plan(self.fixture())
        second = rd.compile_plan(self.fixture())
        self.assertEqual(first, second)
        self.assertEqual(len(first["records"]), 5)
        self.assertEqual(first["records"][3]["qualifier"]["conclusion_kind"], "failed-attempt")

    def test_sync_proposes_bounded_records_without_admission(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            previous = Path.cwd(); os.chdir(root)
            try:
                client = ProofpressClient.in_process(root)
                result = rd.sync(client, rd.compile_plan(self.fixture()), "agent:test")
                self.assertEqual(len(result["conclusions"]), 5)
                self.assertGreaterEqual(len(result["relations"]), 4)
                self.assertEqual(client.context(scope="rd:proofpress")["knowledge"], [])
                summary = client.review_summary("rd:proofpress")
                self.assertEqual(summary["counts"]["needs_review"], 5)
            finally:
                os.chdir(previous)

    def test_aborted_phase_requires_structured_failure(self):
        value = self.fixture()
        value["phases"][3].pop("failure")
        with self.assertRaisesRegex(ValueError, "requires failure"):
            rd.compile_plan(value)


if __name__ == "__main__":
    unittest.main()

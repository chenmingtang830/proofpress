import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "scripts" / "seed_local_ui_demo.py"
CLI = ROOT / "proofpress.py"


class LocalUIDemoTests(unittest.TestCase):
    def test_seed_creates_three_review_states_and_one_eligible_conclusion(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(SEED), "--repo", directory],
                cwd=ROOT, text=True, capture_output=True, check=True,
            )
            payload = json.loads(result.stdout)
            self.assertTrue(payload["synthetic"])
            self.assertEqual(set(payload["states"]), {
                "admitted", "needs_review", "rejected",
            })
            self.assertEqual(
                payload["eligible_context"], [payload["states"]["admitted"]]
            )
            self.assertEqual(
                {row["reason"] for row in payload["blocked"]},
                {"needs_review", "rejected"},
            )

    def test_demo_cli_refuses_to_mix_synthetic_data_into_existing_ledger(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(["git", "init", "-q"], cwd=directory, check=True)
            subprocess.run(
                ["git", "config", "user.name", "Proofpress Test"],
                cwd=directory, check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.invalid"],
                cwd=directory, check=True,
            )
            first = subprocess.run(
                [sys.executable, str(CLI), "demo"], cwd=directory,
                text=True, capture_output=True, check=True,
            )
            self.assertTrue(json.loads(first.stdout)["synthetic"])
            second = subprocess.run(
                [sys.executable, str(CLI), "demo"], cwd=directory,
                text=True, capture_output=True,
            )
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("already exists", second.stderr)


if __name__ == "__main__":
    unittest.main()

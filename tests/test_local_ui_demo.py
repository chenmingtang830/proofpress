import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "scripts" / "seed_local_ui_demo.py"


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


if __name__ == "__main__":
    unittest.main()

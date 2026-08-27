import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "examples/openwiki-conflict-gate/run_demo.py"


class OpenWikiConflictDemoTests(unittest.TestCase):
    def test_fresh_successor_receives_only_resolved_winner_and_receipts(self):
        result = subprocess.run(
            [sys.executable, str(DEMO), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["fixture"]["official_preflight_issues"], 0)
        self.assertEqual(payload["fixture"]["rechecked_claims"], 10)
        self.assertEqual(payload["handoff"]["otherwise_admitted_before_relation"], 2)
        self.assertEqual(payload["handoff"]["quarantined_knowledge"], 0)
        self.assertEqual(
            set(payload["handoff"]["blocked_reasons"].values()),
            {"contradiction_unresolved"},
        )
        successor = payload["fresh_successor"]
        self.assertEqual(successor["knowledge_count"], 1)
        self.assertTrue(successor["loser_statement_absent"])
        self.assertEqual(successor["evidence_digest_count"], 4)
        self.assertEqual(successor["identity_basis"], "self_asserted")
        for key in ("relation_id", "resolution_event", "supersession_event"):
            self.assertTrue(successor[key])


if __name__ == "__main__":
    unittest.main()

import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/summarize_governed_workflow_v10_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("v10_summary", PATH)
runner = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(runner)


class GovernedWorkflowV10SummaryTests(unittest.TestCase):
    def test_decision_reports_every_failed_check(self):
        result = runner.decision({"a": True, "b": False})
        self.assertEqual(result["status"], "do_not_promote")
        self.assertEqual(result["failed_checks"], ["b"])

    def test_stopped_panel_cannot_promote(self):
        result = runner.decision({"a": True}, stopped_reason="gate")
        self.assertEqual(result["status"], "do_not_promote")
        self.assertEqual(result["stopped_reason"], "gate")


if __name__ == "__main__":
    unittest.main()

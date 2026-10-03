import contextlib
import io
import json
import os
from pathlib import Path
import runpy
from types import SimpleNamespace
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify_gmi_judge.py"


class GmiVerificationTests(unittest.TestCase):
    def test_live_check_uses_proofpress_workflow_without_admission(self):
        verdict = {"recommendation": "escalate", "rationale": "Synthetic check.",
                   "adapter": "proofpress-gmi_cloud-judge/v1",
                   "model": "deepseek-ai/DeepSeek-V4.1-Flash"}
        output = io.StringIO()
        with patch.dict(os.environ, {"GMI_API_KEY": "gmi-synthetic-test-key"}, clear=False), \
             patch("sys.argv", [str(SCRIPT), "--live"]), \
             patch("proofpress.kernel.operations.subprocess.run",
                   return_value=SimpleNamespace(returncode=0, stdout=json.dumps(verdict))), \
             contextlib.redirect_stdout(output):
            runpy.run_path(str(SCRIPT), run_name="__main__")
        result = json.loads(output.getvalue())
        self.assertEqual(result["provider"], "gmi_cloud")
        self.assertEqual(result["receipt_state"], "needs_review")
        self.assertEqual(result["governed_context_count"], 0)
        self.assertNotIn("gmi-synthetic-test-key", output.getvalue())

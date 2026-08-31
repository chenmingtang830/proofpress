import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "studies/apex-agent-eval/retrieval_adapter"))
from run_paddle_extraction_panel_private import isolated_run


class PaddleExtractionPanelIsolationTests(unittest.TestCase):
    def test_success_has_terminal_output_digests(self):
        result = isolated_run([sys.executable, "-c", "print('ok')"], 5)
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["returncode"], 0)
        self.assertTrue(result["stdout_digest"].startswith("sha256:"))

    def test_timeout_kills_child_process_group(self):
        result = isolated_run([sys.executable, "-c", "import time; time.sleep(30)"], 1)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["failure_type"], "TimeoutExpired")
        self.assertIsNotNone(result["returncode"])

    def test_cuda_requirement_precedes_panel_open(self):
        runner = Path(__file__).resolve().parents[1] / "studies/apex-agent-eval/retrieval_adapter/run_paddle_extraction_panel_private.py"
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run([sys.executable, str(runner), "--panel", "/does/not/exist.json",
                                     "--source-manifest", "/does/not/exist.json", "--out", temp,
                                     "--require-cuda"], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("compatible CUDA host", result.stderr)

    def test_deepseek_runner_rejects_before_input_open(self):
        runner = Path(__file__).resolve().parents[1] / "studies/apex-agent-eval/retrieval_adapter/run_deepseek_ocr2_private.py"
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run([sys.executable, str(runner), "--input", "/does/not/exist.pdf",
                                     "--uri", "fixture://unsupported.pdf", "--out", temp,
                                     "--model-revision", "a" * 40], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("compatible CUDA host", result.stderr)


if __name__ == "__main__":
    unittest.main()

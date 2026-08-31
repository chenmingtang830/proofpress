import hashlib
import json
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
                                     "--require-cuda", "--device", "cuda"], capture_output=True, text=True)
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

    def test_deepseek_panel_wrapper_rejects_before_panel_open(self):
        runner = Path(__file__).resolve().parents[1] / "studies/apex-agent-eval/retrieval_adapter/run_deepseek_ocr2_panel_private.py"
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run([sys.executable, str(runner), "--panel", "/does/not/exist.json",
                                     "--source-manifest", "/does/not/exist.json", "--out", temp,
                                     "--model-revision", "a" * 40], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("compatible CUDA host", result.stderr)

    def test_deepseek_panel_wrapper_rejects_unpinned_revision(self):
        runner = Path(__file__).resolve().parents[1] / "studies/apex-agent-eval/retrieval_adapter/run_deepseek_ocr2_panel_private.py"
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run([sys.executable, str(runner), "--panel", "/does/not/exist.json",
                                     "--source-manifest", "/does/not/exist.json", "--out", temp,
                                     "--model-revision", "main"], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("pinned 40-character git commit", result.stderr)

    def test_different_runner_configuration_does_not_reuse_saved_document_result(self):
        runner = Path(__file__).resolve().parents[1] / "studies/apex-agent-eval/retrieval_adapter/run_paddle_extraction_panel_private.py"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); source = root / "fixture.pdf"; source.write_bytes(b"fixture")
            content_digest = "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()
            (root / "source-manifest.json").write_text(json.dumps({"sources": [{
                "path": str(source), "uri": "fixture://test.pdf", "content_digest": content_digest}]}))
            (root / "panel.json").write_text(json.dumps({"panel_digest": "sha256:panel", "sources": [{
                "source_id": "source_1", "content_digest": content_digest, "split": "development"}]}))
            child = root / "child.py"; child.write_text("import sys; raise SystemExit(1)\n")
            prior = root / "out" / "source_1"; prior.mkdir(parents=True)
            (prior / "run-summary-isolated.json").write_text(json.dumps({
                "status": "complete", "run_configuration_digest": "sha256:stale"}))
            result = subprocess.run([sys.executable, str(runner), "--panel", str(root / "panel.json"),
                                     "--source-manifest", str(root / "source-manifest.json"), "--out", str(root / "out"),
                                     "--child-runner", str(child), "--route", "test/route"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            saved = json.loads((prior / "run-summary-isolated.json").read_text())
            self.assertEqual(saved["status"], "failed")
            self.assertNotEqual(saved["run_configuration_digest"], "sha256:stale")


if __name__ == "__main__":
    unittest.main()

import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/run_claim_construction_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("claim_construction_runner", PATH)
runner = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(runner)


class GatewayStartupTimeoutTests(unittest.TestCase):
    def test_readiness_read_is_bounded(self):
        proc = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(2)"],
            stdout=subprocess.PIPE,
            text=True,
        )
        try:
            with self.assertRaisesRegex(TimeoutError, "readiness"):
                runner._read_ready_line(proc.stdout, 0.01)
        finally:
            proc.terminate()
            proc.wait(timeout=2)
            proc.stdout.close()


if __name__ == "__main__":
    unittest.main()

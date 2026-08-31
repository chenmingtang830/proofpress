import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/freeze_v25_phase_c_inputs_private.py"
SPEC = importlib.util.spec_from_file_location("freeze_phase_c", PATH)
freeze_phase_c = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(freeze_phase_c)
MANIFEST = ROOT / "studies/apex-agent-eval/results/exact-knowledge-transfer-v25-manifest.json"


class FreezeV25PhaseCInputsTests(unittest.TestCase):
    def test_freeze_replaces_every_control_with_a_digest(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); controls = {}
            for index, field in enumerate(freeze_phase_c.CONTROL_ARGUMENTS):
                path = root / f"control-{index}.json"; path.write_text(json.dumps({"index": index}))
                controls[field] = path
            frozen, receipt = freeze_phase_c.freeze(json.loads(MANIFEST.read_text()), controls)
        self.assertEqual(receipt["status"], "frozen")
        self.assertFalse(receipt["executor_called"])
        self.assertFalse(receipt["grader_called"])
        self.assertTrue(all(value.startswith("sha256:") for value in frozen["frozen_controls"].values()))

    def test_freeze_rejects_missing_control(self):
        with self.assertRaisesRegex(ValueError, "every Phase C control"):
            freeze_phase_c.freeze({}, {})


if __name__ == "__main__":
    unittest.main()

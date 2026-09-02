import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "studies/apex-agent-eval/retrieval_adapter"
PATH = ADAPTER / "run_v10_formal_construction_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("v10_formal_construction", PATH)
runner = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(runner)


class V10FormalConstructionTests(unittest.TestCase):
    def test_profile_gate_blocks_risk_signal_before_proposer(self):
        profile = json.loads((ADAPTER / "LEGAL_DOMAIN_PROFILE_V1.json").read_text())
        gate = {"state": "claimable", "proposer_allowed": True, "reasons": [],
                "requirement_id": "R1", "atom_ids": ["A1"]}
        result = runner.apply_profile_gate(gate, profile, {"type": "risk_signal"})
        self.assertEqual(result["state"], "needs_domain_analysis")
        self.assertFalse(result["proposer_allowed"])

    def test_profile_gate_preserves_factual_claimability(self):
        profile = json.loads((ADAPTER / "LEGAL_DOMAIN_PROFILE_V1.json").read_text())
        gate = {"state": "claimable", "proposer_allowed": True, "reasons": [],
                "requirement_id": "R1", "atom_ids": ["A1"]}
        self.assertIs(runner.apply_profile_gate(gate, profile, {"type": "factual_input"}), gate)


if __name__ == "__main__":
    unittest.main()

import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/run_v10_profile_filter_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("v10_profile_filter", PATH)
runner = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(runner)


class V10ProfileFilterTests(unittest.TestCase):
    def test_analysis_types_are_not_automatically_constructed(self):
        self.assertNotIn("risk_signal", runner.AUTO_CONSTRUCTION_REQUIREMENT_TYPES)
        self.assertNotIn("domain_analysis", runner.AUTO_CONSTRUCTION_REQUIREMENT_TYPES)

    def test_filter_preserves_only_profile_eligible_requirements(self):
        source = {"requirements": [{"requirement_id": "F", "type": "factual_input"},
                                   {"requirement_id": "R", "type": "risk_signal"}],
                  "claims": [{"id": "C1", "requirement_id": "F", "claim_type": "observed_fact"},
                             {"id": "C2", "requirement_id": "R", "claim_type": "risk_signal"}],
                  "verdicts": [{"claim_id": "C1", "verdict": "supported"},
                               {"claim_id": "C2", "verdict": "supported"}]}
        claims, supported = runner.filter_claims(source)
        self.assertEqual([row["id"] for row in claims], ["C1"])
        self.assertEqual([row["id"] for row in supported], ["C1"])


if __name__ == "__main__":
    unittest.main()

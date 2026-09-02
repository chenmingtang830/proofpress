import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/run_v10_deterministic_compiler_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("v10_deterministic_compiler", PATH)
runner = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(runner)


class V10DeterministicCompilerTests(unittest.TestCase):
    def test_compiler_uses_minimum_contiguous_bound_span(self):
        atom = {"requirement_id": "R1", "evidence_id": "E1", "atom_id": "A1",
                "exact_excerpt": "Before Buyer shall pay $10 after.",
                "field_bindings": {"subject": {"start": 7, "end": 12},
                                   "predicate": {"start": 13, "end": 22},
                                   "value": {"start": 23, "end": 26}},
                "qualification": None}
        gate = {"R1": {"requirement_id": "R1", "state": "claimable",
                        "proposer_allowed": True, "atom_ids": ["A1"]}}
        claims = runner.compile_claims([atom], gate)
        self.assertEqual(claims[0]["statement"], "Buyer shall pay $10")
        self.assertEqual(claims[0]["claim_type"], "observed_fact")
        self.assertEqual(claims[0]["status"], "unresolved")

    def test_type_schema_cannot_rewrite_statement(self):
        item = runner.TYPE_OUTPUT["properties"]["assignments"]["items"]
        self.assertNotIn("statement", item["properties"])

    def test_luna_is_narrow_type_classifier_only(self):
        self.assertEqual(runner.TYPE_CLASSIFIER_MODELS["luna"]["reasoning"], "low")
        self.assertNotIn("luna", runner.MODELS)


if __name__ == "__main__":
    unittest.main()

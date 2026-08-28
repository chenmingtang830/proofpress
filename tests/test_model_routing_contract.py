import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/model_routing_contract.py"
SPEC = importlib.util.spec_from_file_location("model_routing_contract", PATH)
contract = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(contract)


class ModelRoutingContractTests(unittest.TestCase):
    def atom(self, **updates):
        row = {"atom_id": "atom_1", "requirement_id": "R1", "evidence_id": "E1",
               "subject": "Buyer", "predicate": "shall pay", "value": "$10",
               "receipt_digest": "sha256:x", "exact_excerpt": "Buyer shall pay $10",
               "support_mode": "explicit", "qualification": "at closing"}
        row.update(updates); return row

    def test_observed_claim_is_deterministic_and_keeps_qualification_separate(self):
        requirement = {"requirement_id": "R1", "requirement": "Purchase price",
                       "lifecycle_category": "economics_calculations"}
        claim = contract.atom_to_observed_claim(self.atom(), requirement, 1)
        self.assertEqual(claim["statement"], "Buyer shall pay $10")
        self.assertEqual(claim["qualification"], "at closing")
        self.assertNotIn("at closing", claim["statement"])
        self.assertEqual(claim["status"], "unresolved")

    def test_inferred_atom_never_becomes_observed_claim(self):
        with self.assertRaisesRegex(ValueError, "explicit"):
            contract.atom_to_observed_claim(self.atom(support_mode="inferred"),
                                             {"requirement_id": "R1"}, 1)

    def test_construct_deduplicates_and_caps(self):
        reqs = [{"requirement_id": "R1", "requirement": "x"}]
        atoms = [self.atom(atom_id=f"atom_{i}") for i in range(6)]
        self.assertEqual(len(contract.construct_observed_claims(atoms, reqs)), 1)

    def test_material_supported_claim_escalates(self):
        claims = [{"id": "C1", "category": "termination_remedies"},
                  {"id": "C2", "category": "other"}]
        primary = {row["id"]: {"claim_id": row["id"], "verdict": "supported"}
                   for row in claims}
        premium = {"C1": {"claim_id": "C1", "verdict": "unsupported"},
                   "C2": {"claim_id": "C2", "verdict": "supported"}}
        final, escalated = contract.route_verdicts(
            claims, primary, premium, mode="non_supported_or_material_to_premium")
        self.assertEqual(escalated, {"C1"})
        self.assertEqual(final["C1"]["verdict"], "unsupported")

    def test_verdict_validation_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            contract.validate_verdicts([{"id": "C1"}], {"verdicts": []})

    def test_type_assignment_cannot_rewrite_claim(self):
        claims = [{"id": "C1", "statement": "Buyer shall pay $10",
                   "claim_type": "observed_fact", "evidence_ids": ["E1"]}]
        result = contract.apply_type_assignments(
            claims, {"assignments": [{"claim_id": "C1",
                                       "claim_type": "contract_allocation"}]})
        self.assertEqual(result[0]["claim_type"], "contract_allocation")
        self.assertEqual(result[0]["statement"], claims[0]["statement"])
        self.assertEqual(result[0]["evidence_ids"], ["E1"])


if __name__ == "__main__": unittest.main()

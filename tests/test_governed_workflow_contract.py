import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "studies/apex-agent-eval/retrieval_adapter"
SPEC = importlib.util.spec_from_file_location(
    "governed_workflow_contract", ADAPTER / "governed_workflow_contract.py")
workflow = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(workflow)


class GovernedWorkflowContractTests(unittest.TestCase):
    def receipt(self):
        return {"evidence_id": "E1", "receipt_digest": "sha256:" + "a" * 64,
                "source_digest": "sha256:" + "b" * 64, "custody_valid": True,
                "quote": "Buyer shall pay $10 at Closing.",
                "locator": {"kind": "page_span", "page_start": 1, "page_end": 1}}

    def atom(self, **updates):
        excerpt = "Buyer shall pay $10 at Closing."
        row = {"schema_version": workflow.ATOM_SCHEMA, "atom_id": "A1",
               "requirement_id": "R1", "evidence_id": "E1",
               "receipt_digest": "sha256:" + "a" * 64,
               "subject": "Buyer", "predicate": "shall pay", "value": "$10",
               "effective_date": None, "qualification": "at Closing",
               "document_version": "signed", "exact_excerpt": excerpt,
               "locator": self.receipt()["locator"], "support_mode": "explicit",
               "field_bindings": {"subject": {"start": 0, "end": 5},
                                  "predicate": {"start": 6, "end": 15},
                                  "value": {"start": 16, "end": 19}}}
        row.update(updates); return row

    def test_domain_profile_is_separate_and_digest_bound(self):
        profile = json.loads((ADAPTER / "LEGAL_DOMAIN_PROFILE_V1.json").read_text())
        validated = workflow.validate_profile(profile)
        self.assertEqual(validated["profile_id"], "proofpress/legal-matter/v1")
        self.assertTrue(validated["profile_digest"].startswith("sha256:"))
        self.assertNotIn("parties_capacity_authority", workflow.CLAIM_TYPES)
        self.assertFalse(hasattr(workflow, "LIFECYCLE_CHECKLIST"))

    def test_profile_construction_eligibility_is_explicit_and_fail_closed(self):
        profile = json.loads((ADAPTER / "LEGAL_DOMAIN_PROFILE_V1.json").read_text())
        allowed = workflow.profile_construction_eligibility(
            profile, {"type": "factual_input"})
        blocked = workflow.profile_construction_eligibility(
            profile, {"type": "risk_signal"})
        unknown = workflow.profile_construction_eligibility(
            profile, {"type": "future_domain_type"})
        self.assertTrue(allowed["eligible"])
        self.assertEqual(blocked["state"], "needs_domain_analysis")
        self.assertFalse(unknown["eligible"])

    def test_claimability_requires_field_binding_and_custody(self):
        receipt = self.receipt()
        gate = workflow.claimability_decision(
            {"requirement_id": "R1"}, [self.atom()], {"E1": receipt})
        self.assertEqual(gate["state"], "claimable")
        self.assertTrue(gate["proposer_allowed"])
        missing = self.atom(field_bindings={})
        gate = workflow.claimability_decision(
            {"requirement_id": "R1"}, [missing], {"E1": receipt})
        self.assertEqual(gate["state"], "partial")
        self.assertIn("unbound_subject", gate["reasons"])
        bad = {**receipt, "custody_valid": False}
        gate = workflow.claimability_decision(
            {"requirement_id": "R1"}, [self.atom()], {"E1": bad})
        self.assertEqual(gate["state"], "gap")
        self.assertFalse(gate["proposer_allowed"])

    def test_conflict_and_inference_never_reach_proposer(self):
        receipts = {"E1": self.receipt()}
        conflict = self.atom(conflict_group="price")
        self.assertEqual(workflow.claimability_decision(
            {"requirement_id": "R1"}, [conflict], receipts)["state"], "conflict")
        inferred = self.atom(support_mode="inferred")
        self.assertEqual(workflow.claimability_decision(
            {"requirement_id": "R1"}, [inferred], receipts)["state"],
            "needs_domain_analysis")

    def test_candidate_cannot_bypass_gate_or_carry_admission(self):
        claim = {"id": "C1", "requirement_id": "R1", "claim_type": "observed_fact",
                 "atom_ids": ["A1"], "status": "unresolved"}
        gate = {"requirement_id": "R1", "state": "gap", "proposer_allowed": False,
                "atom_ids": []}
        with self.assertRaisesRegex(ValueError, "forbidden"):
            workflow.validate_compiled_claim(claim, {"A1": self.atom()}, gate)
        good = {**gate, "state": "claimable", "proposer_allowed": True,
                "atom_ids": ["A1"]}
        with self.assertRaisesRegex(ValueError, "authority"):
            workflow.validate_compiled_claim({**claim, "admission": "admitted"},
                                             {"A1": self.atom()}, good)

    def test_layered_critic_fails_closed_and_downgrades(self):
        claim = {"id": "C1", "requirement_id": "R1"}
        verdict = {"schema_version": workflow.CRITIC_SCHEMA, "claim_id": "C1",
                   **{field: True for field in workflow.CRITIC_FIELDS},
                   "verdict": "supported", "failure_reasons": []}
        workflow.validate_layered_verdict(claim, verdict)
        broken = {**verdict, "value_supported": False, "verdict": "unsupported",
                  "failure_reasons": ["value_not_entailed"]}
        result = workflow.apply_layered_verdicts(
            [{"requirement_id": "R1"}], [claim], [broken])
        self.assertEqual(result["supported_claims"], [])
        self.assertEqual(result["requirement_statuses"][0]["status"], "partial")
        with self.assertRaisesRegex(ValueError, "contradicts"):
            workflow.validate_layered_verdict(claim, {**broken, "verdict": "supported"})


if __name__ == "__main__":
    unittest.main()

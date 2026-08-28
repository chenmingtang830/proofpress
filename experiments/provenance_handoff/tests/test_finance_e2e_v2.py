import unittest

from pp_eval.finance_e2e_v2 import (
    ATOM_SCHEMA,
    apply_type_assignments,
    atom_to_observed_fact,
    execution_gate,
    executor_qualification,
    requirement_completeness,
    validate_finance_atom,
)


def atom():
    return {
        "schema_version": ATOM_SCHEMA,
        "atom_id": "atom_001",
        "requirement_id": "req_1",
        "evidence_id": "ev_1",
        "receipt_digest": "sha256:receipt",
        "subject": "FY2025 revenue",
        "predicate": "equals",
        "value": "100",
        "support_mode": "explicit",
        "locator": "Workbook.xlsx#Sheet1!B2",
        "exact_source_value": 100,
        "unit": "USDm",
        "currency": "USD",
        "period": "FY2025",
    }


def receipts():
    return {"ev_1": {
        "receipt_digest": "sha256:receipt",
        "locator": "Workbook.xlsx#Sheet1!B2",
        "source_value": 100,
        "unit": "USDm",
        "currency": "USD",
        "period": "FY2025",
    }}


class FinanceAtomTests(unittest.TestCase):
    def test_atom_requires_exact_receipt_binding(self):
        self.assertEqual(validate_finance_atom(atom(), receipts())["atom_id"], "atom_001")
        bad = atom()
        bad["currency"] = "EUR"
        with self.assertRaisesRegex(ValueError, "currency"):
            validate_finance_atom(bad, receipts())

    def test_inferred_atom_cannot_become_observed_fact(self):
        bad = atom()
        bad["support_mode"] = "inferred"
        with self.assertRaisesRegex(ValueError, "explicit"):
            atom_to_observed_fact(bad, 1)

    def test_type_assignment_cannot_rewrite_record(self):
        fact = atom_to_observed_fact(atom(), 1)
        value = {"assignments": [{"record_id": fact["id"],
                                    "record_type": "observed_fact",
                                    "statement": "rewrite"}]}
        with self.assertRaisesRegex(ValueError, "only assign"):
            apply_type_assignments([fact], value)


class FinanceGateTests(unittest.TestCase):
    def test_material_gap_blocks_completeness(self):
        result = requirement_completeness(
            [{"requirement_id": "req_1"}], [],
            [{"gap_id": "gap_1", "requirement_id": "req_1",
              "kind": "unresolved_methodology", "material": True}],
        )
        self.assertFalse(result["complete"])
        self.assertEqual(result["requirements"][0]["state"], "material_gap")

    def test_execution_gate_fails_closed(self):
        fact = atom_to_observed_fact(atom(), 1)
        result = execution_gate(
            records=[fact], critic_verdicts={fact["id"]: {"verdict": "supported"}},
            completeness={"complete": True}, conflicts=[],
            source_bindings_complete=True, telemetry_complete=True,
            requested_output_leakage=False,
        )
        self.assertEqual(result["decision"], "allow")
        blocked = execution_gate(
            records=[fact], critic_verdicts={fact["id"]: {"verdict": "supported"}},
            completeness={"complete": False}, conflicts=[],
            source_bindings_complete=True, telemetry_complete=True,
            requested_output_leakage=False,
        )
        self.assertEqual(blocked["decision"], "block")

    def test_executor_qualification_uses_frozen_denominator(self):
        cells = [{"terminal_telemetry_complete": True,
                  "workbook_finalized": True,
                  "required_outputs_valid": True,
                  "unauthorized_source_access": False} for _ in range(5)]
        cells.append({"terminal_telemetry_complete": True,
                      "workbook_finalized": False,
                      "required_outputs_valid": False,
                      "failure_kind": "transport",
                      "unauthorized_source_access": False})
        result = executor_qualification(cells)
        self.assertEqual(result["decision"], "allow")
        cells[0]["terminal_telemetry_complete"] = False
        self.assertEqual(executor_qualification(cells)["decision"], "block")


if __name__ == "__main__":
    unittest.main()


#!/usr/bin/env python3
import unittest

from run_governed_reuse_private import select_source_cell, validate_reuse


class GovernedReuseTests(unittest.TestCase):
    def test_source_cell_requires_complete_zero_error_admission_gate(self):
        cell = {"task_id": "task", "condition": "projection", "executor_model": "model",
                "status": "scored", "artifact_checks": {"artifact_valid": True},
                "unsupported_claims": 0, "citation_errors": 0, "authority_errors": 0}
        report = {"qualification": {"status": "pass"}, "cells": [cell]}
        self.assertIs(select_source_cell(report, "task", "projection", "model"), cell)
        cell["authority_errors"] = 1
        with self.assertRaises(ValueError):
            select_source_cell(report, "task", "projection", "model")

    def test_reuse_requires_exact_receipts_and_bounded_basis(self):
        artifact, receipt = "sha256:artifact", "sha256:receipt"
        value = {"authority_scope": "evaluation-only governed reuse; not matter authority",
                 "relied_on_artifact_digest": artifact, "admission_receipt_digest": receipt,
                 "actions": [{"basis_ids": [artifact, receipt]}]}
        self.assertEqual(validate_reuse(value, artifact, receipt), [])
        value["actions"][0]["basis_ids"].append("foreign")
        self.assertIn("downstream action has an invalid governed basis",
                      validate_reuse(value, artifact, receipt))


if __name__ == "__main__":
    unittest.main()

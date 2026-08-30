#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from run_workflow_utility_private import (aggregate_criterion_grades,
                                          normalize_criterion_grade)


class CriterionDiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.rubric = [{"verifier_id": "v1", "criteria": "Exact amount"},
                       {"verifier_id": "v2", "criteria": "Exact authority"}]
        self.value = {"criteria": [
            {"verifier_id": "v1", "score": 0, "requirement_identified": True,
             "graph_object_present": False, "projected": False, "derivation_capable": False,
             "artifact_used": False, "delivery_aligned": False,
             "primary_failure_stage": "graph_sufficiency"},
            {"verifier_id": "v2", "score": 1, "requirement_identified": True,
             "graph_object_present": True, "projected": True, "derivation_capable": True,
             "artifact_used": True, "delivery_aligned": True,
             "primary_failure_stage": "satisfied"}],
            "unsupported_claims": 0, "citation_errors": 0, "authority_errors": 0}

    def test_normalization_derives_fraction_from_complete_matrix(self):
        grade = normalize_criterion_grade(self.value, self.rubric)
        self.assertEqual(grade["rubric_fraction"], .5)
        self.assertEqual([row["verifier_id"] for row in grade["criteria"]], ["v1", "v2"])

    def test_normalization_rejects_missing_or_foreign_verifier(self):
        broken = {**self.value, "criteria": self.value["criteria"][:1]}
        with self.assertRaises(ValueError):
            normalize_criterion_grade(broken, self.rubric)
        foreign = {**self.value, "criteria": [{**self.value["criteria"][0], "verifier_id": "x"},
                                                self.value["criteria"][1]]}
        with self.assertRaises(ValueError):
            normalize_criterion_grade(foreign, self.rubric)

    def test_aggregate_preserves_denominator_and_failure_votes(self):
        grades = [normalize_criterion_grade(self.value, self.rubric) for _ in range(3)]
        rows = aggregate_criterion_grades(grades)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["primary_failure_stage"], "graph_sufficiency")
        self.assertEqual(rows[0]["failure_stage_counts"], {"graph_sufficiency": 3})


if __name__ == "__main__":
    unittest.main()

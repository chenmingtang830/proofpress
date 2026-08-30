#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from run_workflow_utility_private import (aggregate_criterion_grades,
                                          diagnostic_projection_inventory,
                                          model_telemetry_summary,
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

    def test_projection_inventory_keeps_identity_and_drops_source_text(self):
        inventory = diagnostic_projection_inventory({"candidate_evidence": [{
            "receipt_digest": "sha256:abc", "object_kind": "authority_candidate",
            "status": "not_governed", "evidence": {"quote": "very long private text",
                                                       "locator": {"page_start": 2}},
        }]})
        self.assertEqual(inventory["object_count"], 1)
        self.assertEqual(inventory["objects"][0]["receipt_digest"], "sha256:abc")
        self.assertNotIn("very long private text", str(inventory))
        self.assertFalse(inventory["source_text_included"])

    def test_model_telemetry_aggregates_route_tokens_cost_and_latency(self):
        summary = model_telemetry_summary(
            [{"model": "m", "provider": "p", "status": "ok", "latency_ms": 10},
             {"model": "m", "provider": "p", "status": "inconclusive", "latency_ms": 30}],
            [{"model": "m", "provider": "p", "input_tokens": 100,
              "output_tokens": 20, "cost_usd": .1},
             {"model": "m", "provider": "p", "input_tokens": 50,
              "output_tokens": 10, "cost_usd": .05}])
        route = summary["routes"][0]
        self.assertEqual(route["calls"], 2)
        self.assertEqual(route["successful_calls"], 1)
        self.assertEqual(route["input_tokens"], 150)
        self.assertEqual(route["latency_ms"]["mean"], 20)


if __name__ == "__main__":
    unittest.main()

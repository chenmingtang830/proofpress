#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from open_discovery_private import (AUTHORITY_NODE_SCHEMA, DERIVATION_NODE_SCHEMA,
                                    EVIDENCE_ATOM_SCHEMA, bind_authority_node,
                                    bind_evidence_atom, calculate_derivation,
                                    select_objects, task_knowledge_objects)
from agentic_disclosure_private import run_quality_open_discovery


class OpenDiscoveryTests(unittest.TestCase):
    def test_task_objects_never_invent_missing_typed_objects(self):
        graph = {"task": {"task_id": "task-1"}, "construction": {"claims": [{"id": "c1"}]}}
        value = task_knowledge_objects(graph)
        self.assertEqual(value["availability"], {
            "evidence_atom_count": 0, "authority_node_count": 0, "derivation_node_count": 0})
        self.assertFalse(value["admission_authority"])

    def test_task_objects_preserve_only_declared_schemas(self):
        graph = {"task": {"task_id": "task-1"}, "construction": {
            "evidence_atoms": [{"schema_version": EVIDENCE_ATOM_SCHEMA, "atom_id": "a1"},
                               {"schema_version": "wrong", "atom_id": "a2"}],
            "authority_nodes": [{"schema_version": AUTHORITY_NODE_SCHEMA, "authority_id": "u1"}],
            "derivation_nodes": [{"schema_version": DERIVATION_NODE_SCHEMA, "derivation_id": "d1"}],
        }}
        value = task_knowledge_objects(graph)
        self.assertEqual(value["availability"], {
            "evidence_atom_count": 1, "authority_node_count": 1, "derivation_node_count": 1})
        selected = select_objects(value, "evidence_atoms", ["a1"])
        self.assertEqual(selected["object_count"], 1)
        self.assertFalse(selected["governed_reliance_allowed"])

    def test_calculation_is_decimal_deterministic_and_non_admitting(self):
        value = calculate_derivation("income * federal_rate + income * state_rate",
                                     {"income": 100, "federal_rate": .21, "state_rate": .0884},
                                     output_unit="USD", round_places=2)
        self.assertEqual(value["result"], "29.84")
        self.assertTrue(value["deterministic"])
        self.assertFalse(value["admission_authority"])
        self.assertEqual(value["status"], "not_governed_derived")

    def test_calculation_rejects_code_and_division_by_zero(self):
        with self.assertRaises(ValueError):
            calculate_derivation("__import__('os').system('echo no')", {"x": 1})
        with self.assertRaises(ValueError):
            calculate_derivation("x / y", {"x": 1, "y": 0})

    def test_typed_candidates_require_exact_visible_receipt_binding(self):
        receipt = {"receipt_digest": "sha256:r", "source": {"uri": "private://source"},
                   "evidence": {"quote": "Wisconsin is a community property state.",
                                "locator": {"page_start": 1}}}
        atoms = {"sha256:r": receipt}
        atom = bind_evidence_atom({"receipt_digest": "sha256:r", "requirement_id": "R1",
                                   "subject": "Wisconsin", "predicate": "is",
                                   "value": "community property state",
                                   "exact_excerpt": "Wisconsin is a community property state."}, atoms)
        self.assertEqual(atom["schema_version"], EVIDENCE_ATOM_SCHEMA)
        self.assertEqual(atom["status"], "not_governed_candidate")
        authority = bind_authority_node({"receipt_digest": "sha256:r", "citation": "Source 1",
                                         "proposition": "Wisconsin classification",
                                         "jurisdiction": "Wisconsin",
                                         "exact_excerpt": "Wisconsin is a community property state."}, atoms)
        self.assertEqual(authority["schema_version"], AUTHORITY_NODE_SCHEMA)
        self.assertFalse(authority["normative_authority_confirmed"])
        with self.assertRaises(ValueError):
            bind_evidence_atom({"receipt_digest": "sha256:r", "requirement_id": "R1",
                                "subject": "x", "predicate": "y", "value": "z",
                                "exact_excerpt": "not in receipt"}, atoms)

    def test_raw_control_pages_search_and_calculates_without_admission(self):
        class FakeIndex:
            doc_meta = {"private://source": {}}
            sections = [1]
            def inventory(self):
                return [{"title": "source", "media_type": "text/plain"}]
            def search(self, query, max_documents=1, max_sections=1):
                section = {"id": "s1", "text": "Income was 100.", "text_digest": "sha256:text",
                           "page_start": 1, "page_end": 1, "heading": "Income",
                           "source": {"uri": "private://source", "content_digest": "sha256:source",
                                      "media_type": "text/plain"}}
                return [{"section": section, "score": 1.0, "rank": 1}][:max_sections]
        decisions = iter([
            {"action": "search_gap", "query": "income", "offset": 0, "page_size": 1,
             "reason": "retrieve input"},
            {"action": "calculate", "expression": "income * rate",
             "variables": {"income": 100, "rate": .21}, "output_unit": "USD",
             "round_places": 2, "reason": "compute exact amount"},
            {"action": "answer", "reason": "ready"},
        ])
        value = run_quality_open_discovery(
            query="calculate", scope="task-1", index=FakeIndex(), decide=lambda _: next(decisions),
            graph={"task": {"task_id": "task-1"}, "construction": {}}, raw_corpus_control=True)
        self.assertEqual(value["used_actions"], ["calculate", "search_gap"])
        self.assertTrue(value["used_calculate"])
        self.assertEqual(value["state"]["limits"]["max_lifetime_results"], None)
        self.assertFalse(value["state"]["governance_boundary"]["automatic_admission"])


if __name__ == "__main__":
    unittest.main()

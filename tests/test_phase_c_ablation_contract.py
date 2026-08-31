import unittest

from phase_c_ablation_contract import CONDITIONS, project, validate_projection


DIGEST = "sha256:" + "a" * 64


def graph():
    return {
        "graph_digest": DIGEST, "source_manifest_digest": DIGEST,
        "automatic_admission": False, "human_approval_required": True,
        "claims": [{"claim_id": "claim-1", "text": "A governed research claim",
                    "basis_object_id": "atom-1", "basis_object_kind": "numeric_atom"}],
        "numeric_atoms": [{"atom_id": "atom-1", "display": "120", "normalized_value": "120",
                           "kind": "decimal", "unit": "count", "entity": "Company", "period": "current",
                           "source_content_digest": DIGEST, "status": "not_governed_candidate",
                           "admitted": False}],
        "authority_nodes": [{"authority_id": "authority-1", "source_content_digest": DIGEST}],
        "table_cells": [{"cell_id": "cell-1", "source_content_digest": DIGEST,
                         "locator": {"page": 1}, "row": 0, "column": 0, "raw_text": "120"}],
        "derivations": [{"derivation_id": "derivation-1", "input_cell_ids": ["cell-1"],
                         "derivation_digest": DIGEST}],
    }


class PhaseCAblationContractTests(unittest.TestCase):
    def test_projection_nests_only_the_treatment_objects(self):
        ordinary = project(graph(), CONDITIONS[0])
        cells = project(graph(), CONDITIONS[1])
        derivation = project(graph(), CONDITIONS[2])
        self.assertNotIn("table_cells", ordinary)
        self.assertNotIn("numeric_atoms", ordinary)
        self.assertIn("numeric_atoms", cells)
        self.assertIn("table_cells", cells)
        self.assertNotIn("derivations", cells)
        self.assertIn("derivations", derivation)
        self.assertEqual(ordinary["claims"], cells["claims"])
        self.assertEqual(cells["authority_nodes"], derivation["authority_nodes"])

    def test_projection_is_digest_bound_and_not_admitted(self):
        value = project(graph(), CONDITIONS[2])
        validate_projection(value, graph())
        self.assertFalse(value["automatic_admission"])
        self.assertTrue(value["human_approval_required"])

    def test_rejects_derivation_without_cell_binding(self):
        value = graph(); value["derivations"][0]["input_cell_ids"] = ["missing"]
        with self.assertRaisesRegex(ValueError, "known typed objects"):
            project(value, CONDITIONS[2])


if __name__ == "__main__":
    unittest.main()

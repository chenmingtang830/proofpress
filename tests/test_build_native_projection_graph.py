import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "studies/apex-agent-eval/retrieval_adapter"
sys.path.insert(0, str(ROOT))
SPEC = importlib.util.spec_from_file_location(
    "native_projection_graph", ADAPTER / "build_native_projection_graph_private.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class NativeProjectionGraphTests(unittest.TestCase):
    def artifact(self):
        digest = "sha256:" + "a" * 64
        receipt = {"source_digest": "sha256:" + "b" * 64}
        atom = {"atom_id": "atom_fact", "evidence_id": "E1", "receipt_digest": digest,
                "subject": "Revenue", "predicate": "was", "value": "$100", "locator": {"page_start": 2},
                "support_mode": "explicit"}
        numeric = {"atom_id": "atom_cell", "evidence_id": "E1", "receipt_digest": digest,
                   "subject": "Revenue", "predicate": "2024", "value": "$100", "locator": {"page_start": 2},
                   "support_mode": "explicit", "numeric": {"display": "$100", "decimal_value": "100",
                   "kind": "currency", "unit": "USD", "currency": "USD", "entity": "Revenue", "period": "2024"},
                   "table_cell_binding": {"row_index": 1, "column_index": 2}}
        derivation = {"derivation_id": "D1", "basis_object_ids": ["atom_cell"],
                      "expression": "x", "derivation_digest": "sha256:" + "c" * 64}
        return {"task": {"task_id": "task_1", "prompt": "private", "expected_output": "make_new_doc"},
                "receipts": {"E1": receipt},
                "objects": {"evidence_atoms": [atom], "numeric_atoms": [numeric], "authority_nodes": []},
                "derivations": [derivation]}

    def test_compiles_source_bound_candidate_graph(self):
        graph, receipt = module.build(exact_artifact=self.artifact(),
                                      catalog={"catalog_digest": "sha256:" + "d" * 64})
        self.assertEqual(receipt["claim_count"], 2)
        self.assertEqual(receipt["numeric_atom_count"], 1)
        self.assertEqual(receipt["table_cell_count"], 1)
        self.assertEqual(receipt["derivation_count"], 1)
        self.assertFalse(graph["automatic_admission"])
        self.assertTrue(all(row["status"] == "not_governed_candidate" for row in graph["claims"]))

    def test_derivation_accepts_mixed_table_and_numeric_inputs(self):
        artifact = self.artifact()
        text_numeric = {"atom_id": "atom_text", "evidence_id": "E1",
                        "receipt_digest": "sha256:" + "a" * 64,
                        "subject": "Rate", "predicate": "was", "value": "10%",
                        "locator": {"page_start": 2}, "support_mode": "explicit",
                        "numeric": {"display": "10%", "decimal_value": "10", "kind": "percentage",
                                    "unit": "%", "currency": None, "entity": "Rate", "period": "current"}}
        artifact["objects"]["numeric_atoms"].append(text_numeric)
        artifact["derivations"][0]["basis_object_ids"] = ["atom_cell", "atom_text"]
        graph, receipt = module.build(exact_artifact=artifact,
                                      catalog={"catalog_digest": "sha256:" + "d" * 64})
        refs = graph["derivations"][0]["input_refs"]
        self.assertEqual([row["object_kind"] for row in refs], ["table_cell", "numeric_atom"])
        self.assertEqual(receipt["derivation_count"], 1)

    def test_recovers_generic_cell_from_frozen_atom_without_model_call(self):
        artifact = self.artifact()
        atom = artifact["objects"]["numeric_atoms"][0]
        atom.pop("table_cell_binding")
        atom["exact_excerpt"] = "Revenue\t$100"
        artifact["receipts"]["E1"]["quote"] = "Metric\tValue\nRevenue\t$100\n"
        graph, receipt = module.build(exact_artifact=artifact,
                                      catalog={"catalog_digest": "sha256:" + "d" * 64})
        self.assertEqual(receipt["generic_table_cell_bindings_recovered"], 1)
        self.assertEqual(graph["table_cells"][0]["row"], 1)

    def test_rejects_rubric_bearing_artifact(self):
        artifact = self.artifact()
        artifact["task"]["rubric"] = []
        with self.assertRaisesRegex(ValueError, "rubric"):
            module.build(exact_artifact=artifact, catalog={"catalog_digest": "sha256:" + "d" * 64})


if __name__ == "__main__":
    unittest.main()

import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/run_v10_role_matrix_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("v10_matrix", PATH)
matrix = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(matrix)


class V10RoleMatrixTests(unittest.TestCase):
    def test_extractor_rejects_unsafe_batch_sizes(self):
        with self.assertRaisesRegex(ValueError, "batch_size"):
            matrix.call_extractor(None, [], {}, [], batch_size=0)

    def test_matrix_uses_only_canary_qualified_routes(self):
        self.assertEqual(set(matrix.MODELS), {"deepseek", "ling", "qwen", "sol"})
        self.assertEqual(matrix.MODELS["ling"]["reasoning"], "high")
        self.assertEqual(matrix.MODELS["qwen"]["provider"], "alibaba")

    def test_atom_normalization_calculates_exact_field_spans(self):
        receipt = {"evidence_id": "E1", "receipt_digest": "sha256:" + "a" * 64,
                   "source_digest": "sha256:" + "b" * 64, "custody_valid": True,
                   "quote": "Buyer shall pay $10.",
                   "locator": {"kind": "page_span", "page_start": 1, "page_end": 1}}
        value = {"atoms": [{"requirement_id": "R1", "evidence_id": "E1",
                            "exact_excerpt": "Buyer shall pay $10.", "subject": "Buyer",
                            "predicate": "shall pay", "value": "$10", "effective_date": None,
                            "qualification": None, "document_version": None,
                            "support_mode": "explicit", "conflict_group": None}]}
        atoms = matrix.normalize_atoms(value, [{"requirement_id": "R1"}], {"E1": receipt},
                                       [{"requirement_id": "R1", "evidence_ids": ["E1"]}])
        self.assertEqual(atoms[0]["field_bindings"]["subject"], {"start": 0, "end": 5})
        self.assertEqual(atoms[0]["field_bindings"]["value"], {"start": 16, "end": 19})

    def test_atom_normalization_rejects_model_claimed_nonexact_field(self):
        receipt = {"evidence_id": "E1", "receipt_digest": "sha256:" + "a" * 64,
                   "source_digest": "sha256:" + "b" * 64, "custody_valid": True,
                   "quote": "Buyer shall pay $10.",
                   "locator": {"kind": "page_span", "page_start": 1, "page_end": 1}}
        value = {"atoms": [{"requirement_id": "R1", "evidence_id": "E1",
                            "exact_excerpt": "Buyer shall pay $10.", "subject": "Seller",
                            "predicate": "shall pay", "value": "$10", "effective_date": None,
                            "qualification": None, "document_version": None,
                            "support_mode": "explicit", "conflict_group": None}]}
        self.assertEqual(matrix.normalize_atoms(value, [{"requirement_id": "R1"}], {"E1": receipt},
                                                [{"requirement_id": "R1", "evidence_ids": ["E1"]}]), [])

    def test_critic_aggregate_is_deterministic_not_model_authority(self):
        self.assertIn("verdict", matrix.VERDICT_OUTPUT["properties"]["verdicts"]["items"]["required"])
        self.assertEqual(len(matrix.CRITIC_FIELDS), 7)


if __name__ == "__main__":
    unittest.main()

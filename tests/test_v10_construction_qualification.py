import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/run_v10_construction_qualification_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("v10_construction", PATH)
runner = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(runner)


class V10ConstructionQualificationTests(unittest.TestCase):
    def test_selected_route_is_cross_model_and_qwen_decomposed(self):
        self.assertEqual(runner.DECOMPOSER, "qwen")
        self.assertEqual(runner.EXTRACTOR, "deepseek")
        self.assertEqual(runner.PROPOSER, "deepseek")
        self.assertEqual(runner.CRITIC, "sol")
        self.assertEqual(runner.EXTRACTOR_BATCH_SIZE, 4)
        self.assertNotEqual(runner.PROPOSER, runner.CRITIC)

    def test_opportunity_scoring_separates_honest_gaps_and_loss_stages(self):
        reference = [
            {"requirement_id": "covered", "evidence_sufficient": True},
            {"requirement_id": "extractor", "evidence_sufficient": True},
            {"requirement_id": "critic", "evidence_sufficient": True},
            {"requirement_id": "gap", "evidence_sufficient": False},
        ]
        resolutions = [
            {"requirement_id": "covered", "status": "covered"},
            {"requirement_id": "extractor", "status": "gap"},
            {"requirement_id": "critic", "status": "partial"},
            {"requirement_id": "gap", "status": "gap"},
        ]
        score = runner.score_requirement_opportunities(
            reference,
            resolutions,
            [{"requirement_id": "covered"}, {"requirement_id": "critic"}],
            {"covered": {"proposer_allowed": True}, "critic": {"proposer_allowed": True}},
            [{"requirement_id": "covered"}, {"requirement_id": "critic"}],
            [{"requirement_id": "covered"}],
        )
        self.assertEqual(score["coverage_precision"], 1.0)
        self.assertEqual(score["coverage_recall"], 1 / 3)
        self.assertEqual(score["honest_gap_recall"], 1.0)
        self.assertEqual(score["loss_funnel"], {
            "extractor": 1,
            "claimability": 0,
            "proposer": 0,
            "critic": 1,
            "claim_shape": 0,
        })

    def test_frozen_retrieval_mode_is_explicit(self):
        self.assertEqual(runner.SCHEMA, "proofpress/v10-construction-qualification/v2")

    def test_multiquery_rrf_merges_queries_and_preserves_source_diversity(self):
        class Index:
            def search(self, query, max_documents=10, max_sections=6):
                uri = "private://a" if query == "alpha" else "private://b"
                return [{"section": {"uri": uri, "id": query}, "rank": 1, "score": 1.0,
                         "considered_documents": [uri]}]
        hits, query = runner._multiquery_hits(
            {"requirement": "beta", "evidence_search_queries": ["alpha"]}, Index(), 2)
        self.assertEqual([row["section"]["uri"] for row in hits], ["private://a", "private://b"])
        self.assertEqual(query, "alpha || beta")

    def test_retrieval_rejects_unknown_mode(self):
        with self.assertRaisesRegex(ValueError, "unknown retrieval mode"):
            runner.retrieve([], object(), mode="unknown")

    def test_requirement_plus_task_reserves_two_safety_hits(self):
        class Index:
            def search(self, query, max_documents=10, max_sections=6):
                prefix = "task" if query == "whole task" else "req"
                return [{"section": {"uri": f"private://{prefix}-{i}", "id": str(i),
                                     "text": prefix, "heading": prefix,
                                     "representation_digest": "sha256:" + ("a" if prefix == "task" else "e") * 64,
                                     "source": {"uri": f"private://{prefix}-{i}",
                                                "content_digest": "sha256:" + "b" * 64,
                                                "media_type": "text/plain"},
                                     "text_digest": "sha256:" + ("c" if prefix == "task" else "d") * 63 + str(i),
                                     "page_start": i + 1, "page_end": i + 1},
                         "rank": i + 1, "score": 1.0,
                         "considered_documents": [f"private://{prefix}-{i}"]}
                        for i in range(max_sections)]
        receipts, audit = runner.retrieve(
            [{"requirement_id": "R", "evidence_search_queries": ["specific"]}],
            Index(), max_sections=4, mode="requirement_plus_task", task_query="whole task")
        uris = [receipts[eid]["source"]["uri"] for eid in audit[0]["evidence_ids"]]
        self.assertEqual(uris[:2], ["private://task-0", "private://task-1"])
        self.assertEqual(len(uris), 4)


if __name__ == "__main__":
    unittest.main()

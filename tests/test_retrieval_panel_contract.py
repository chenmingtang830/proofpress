import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "studies/apex-agent-eval/retrieval_adapter"
sys.path.insert(0, str(ADAPTER))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


panel = load("private_panel", ROOT / "studies/apex-agent-eval/retrieval_adapter/run_private_panel.py")
contract = load("legal_contract", ROOT / "studies/apex-agent-eval/retrieval_adapter/legal_pipeline_contract.py")
panel_manifest = load("panel_manifest", ROOT / "studies/apex-agent-eval/retrieval_adapter/panel_manifest.py")
claim_runner = load("claim_runner", ROOT / "studies/apex-agent-eval/retrieval_adapter/run_claim_construction_private.py")
gap_runner = load("gap_runner", ROOT / "studies/apex-agent-eval/retrieval_adapter/run_gap_retrieval_private.py")
claim_scorer = load("claim_scorer", ROOT / "studies/apex-agent-eval/retrieval_adapter/score_claim_construction_private.py")
ask_freezer = load("ask_freezer", ROOT / "studies/apex-agent-eval/retrieval_adapter/freeze_workflow_asks_private.py")
workflow_runner = load("workflow_runner", ROOT / "studies/apex-agent-eval/retrieval_adapter/run_workflow_utility_private.py")


class RetrievalPanelContractTests(unittest.TestCase):
    def test_rrf_is_deterministic_and_deduplicates(self):
        left = {"source": {"uri": "a", "content_digest": "sha256:" + "a" * 64},
                "evidence": {"locator": {"kind": "page_span", "page_start": 1, "page_end": 1}}}
        duplicate = {"source": dict(left["source"]), "evidence": dict(left["evidence"])}
        right = {"source": {"uri": "b", "content_digest": "sha256:" + "b" * 64},
                 "evidence": {"locator": {"kind": "page_span", "page_start": 2, "page_end": 2}}}
        result = panel.hybrid_rrf([left, duplicate], [right], 2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["source"]["uri"], "a")

    def test_decomposition_contract_forbids_rubric_and_freezes_limits(self):
        inventory = [{"uri": "private://source-1", "media_type": "application/pdf"}]
        requirements = [{"requirement_id": "req-1", "requirement": "Identify parties",
                         "applicability": "applicable", "rationale": "lifecycle checklist"}]
        result = contract.validate_decomposition("review authority", inventory, requirements)
        self.assertFalse(result["frozen"])
        frozen = contract.freeze_requirements(contract.coverage_pass(requirements, []))
        self.assertTrue(frozen["frozen"])
        with self.assertRaisesRegex(ValueError, "rubric"):
            contract.validate_decomposition("review authority", inventory, requirements, rubric={})

    def test_conformance_manifest_has_the_24_frozen_cases(self):
        manifest = panel_manifest.manifest()
        self.assertEqual(manifest["case_count"], 24)
        self.assertEqual(len(manifest["cases"]), 24)
        self.assertEqual(sum(case["pageindex_should_call"] for case in manifest["cases"]), 12)
        self.assertTrue(all(case["expected_automatic_admission"] is False for case in manifest["cases"]))

    def test_claim_runner_accepts_only_bounded_json_and_compacts_inventory(self):
        self.assertEqual(claim_runner._parse_json_completion("```json\n{\"ok\":true}\n```"), {"ok": True})
        with self.assertRaisesRegex(ValueError, "bounded JSON"):
            claim_runner._parse_json_completion("no structured completion")
        with self.assertRaisesRegex(ValueError, "bounded JSON"):
            claim_runner._parse_json_completion("```json\n{\"truncated\":")
        index = claim_runner.SectionIndex({"representations": [{
            "source": {"uri": "private://same", "media_type": "text/plain", "content_digest": "sha256:" + "a" * 64},
            "representation_digest": "sha256:" + "b" * 64,
            "sections": [{"id": "sec-1", "heading": "TITLE", "text": "one", "text_digest": "sha256:" + "c" * 64, "page_start": 1, "page_end": 1}],
        }, {
            "source": {"uri": "private://other", "media_type": "application/pdf", "content_digest": "sha256:" + "d" * 64},
            "representation_digest": "sha256:" + "e" * 64,
            "sections": [{"id": "sec-2", "heading": "TERM", "text": "two", "text_digest": "sha256:" + "f" * 64, "page_start": 1, "page_end": 1}],
        }]})
        inventory = index.inventory()
        self.assertEqual(len(inventory), 2)
        self.assertLess(len(str(inventory)), 500)
        self.assertNotIn("content_digest", str(inventory))

    def test_claim_runner_accepts_nested_gateway_requirement_envelope(self):
        rows = claim_runner._safe_requirements({"output": {"requirements": [{
            "id": "R1", "requirement": "Identify the parties",
            "applicability": "always", "rationale": "required",
        }]}})
        self.assertEqual(rows[0]["requirement_id"], "R1")
        self.assertEqual(rows[0]["applicability"], "applicable")
        direct = claim_runner._safe_requirements([{
            "requirement_id": "R2", "requirement": "Identify economics",
            "applicability": "uncertain", "rationale": "source dependent",
        }])
        self.assertEqual(direct[0]["requirement_id"], "R2")

    def test_claim_runner_drops_unbound_placeholder_but_keeps_governed_candidate(self):
        requirements = [{"requirement_id": "R1", "status": "covered", "type": "factual_input"}]
        evidence = {"E1": {"evidence_id": "E1"}}
        claims, relations = claim_runner._normalize_candidate_output({
            "claims": [
                {"requirement_id": "R1", "claim_type": "extraction", "statement": "Fact",
                 "evidence_ids": ["E1"], "status": "unresolved"},
                {"requirement_id": "DUMMY", "claim_type": "analysis", "statement": "Placeholder",
                 "evidence_ids": [], "status": "unresolved"},
            ],
            "relations": [],
        }, requirements, evidence, [{"requirement_id": "R1", "evidence_ids": ["E1"]}])
        self.assertEqual(len(claims), 1)
        self.assertEqual(claims[0]["claim_type"], "observed_fact")
        self.assertEqual(relations, [])

    def test_claim_runner_drops_hallucinated_evidence_without_losing_the_task(self):
        requirements = [{"requirement_id": "R1", "status": "covered", "type": "factual_input"},
                        {"requirement_id": "R2", "status": "covered", "type": "risk_signal"}]
        evidence = {"E1": {"evidence_id": "E1"}}
        claims, _ = claim_runner._normalize_candidate_output({"claims": [
            {"requirement_id": "R1", "statement": "Bound fact", "evidence_ids": ["E1"]},
            {"requirement_id": "R2", "statement": "Hallucinated", "evidence_ids": ["E404"]},
        ]}, requirements, evidence, [
            {"requirement_id": "R1", "evidence_ids": ["E1"]},
            {"requirement_id": "R2", "evidence_ids": ["E1"]},
        ])
        self.assertEqual([row["statement"] for row in claims], ["Bound fact"])
        self.assertEqual(next(row for row in requirements if row["requirement_id"] == "R2")["status"], "partial")

    def test_critic_repairs_only_bound_requirements(self):
        requirements = [{"requirement_id": "R1"}, {"requirement_id": "R2"}, {"requirement_id": "R3"}]
        claims = [{"id": "C1", "requirement_id": "R1"}, {"id": "C2", "requirement_id": "R2"}]
        targets = claim_runner._critic_target_requirement_ids({
            "repair_instructions": [{"claim_id": "C1", "instruction": "split"}],
            "supplemental_queries": [{"requirement_id": "R3", "query": "missing evidence"}],
        }, requirements, claims)
        self.assertEqual(targets, {"R1", "R3"})

    def test_gap_rrf_collapses_overlapping_page_spans(self):
        def receipt(uri, start, end):
            return {"source": {"uri": uri, "content_digest": "sha256:" + "a" * 64},
                    "evidence": {"locator": {"kind": "section_span", "page_start": start, "page_end": end}}}
        result = gap_runner.hybrid_rrf([receipt("private://a", 1, 2)],
                                       [receipt("private://a", 2, 3)])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["retrieval"]["systems"], ["bm25", "pageindex"])

    def test_claim_scorer_counts_each_silver_locator_once(self):
        evidence = {"source": {"uri": "private://a"},
                    "locator": {"page_start": 1, "page_end": 2}}
        silver = {"source_uri": "private://a", "locator": {"page_start": 2, "page_end": 3}}
        self.assertTrue(claim_scorer.locator_hit(evidence, silver))
        self.assertFalse(claim_scorer.locator_hit(evidence,
                                                  {"source_uri": "private://b", "locator": silver["locator"]}))

    def test_workflow_freeze_interleaves_tasks_and_grades_fail_closed(self):
        rows = [("task-a", 1), ("task-a", 2), ("task-b", 3)]
        self.assertEqual(ask_freezer.interleave_by_task(rows, ["task-a", "task-b"], 3),
                         [("task-a", 1), ("task-b", 3), ("task-a", 2)])
        grade = workflow_runner.normalize_grade({"rubric_fraction": 0.75, "unsupported_claims": 1})
        self.assertEqual(grade["rubric_fraction"], 0.75)
        with self.assertRaisesRegex(ValueError, "rubric_fraction"):
            workflow_runner.normalize_grade({"rubric_fraction": 2})


if __name__ == "__main__":
    unittest.main()

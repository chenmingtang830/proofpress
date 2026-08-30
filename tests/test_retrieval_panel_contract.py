import importlib.util
import json
import sys
import tempfile
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
warm_runner = load("warm_runner", ROOT / "studies/apex-agent-eval/retrieval_adapter/run_gap_warm_replay_private.py")
claim_scorer = load("claim_scorer", ROOT / "studies/apex-agent-eval/retrieval_adapter/score_claim_construction_private.py")
semantic_runner = load("semantic_runner", ROOT / "studies/apex-agent-eval/retrieval_adapter/run_claim_semantic_adjudication_private.py")
ask_freezer = load("ask_freezer", ROOT / "studies/apex-agent-eval/retrieval_adapter/freeze_workflow_asks_private.py")
workflow_runner = load("workflow_runner", ROOT / "studies/apex-agent-eval/retrieval_adapter/run_workflow_utility_private.py")
agentic_disclosure = load("agentic_disclosure", ADAPTER / "agentic_disclosure_private.py")
native_artifact = (load("native_artifact", ADAPTER / "native_legal_artifact.py")
                   if importlib.util.find_spec("docx") else None)
v7_preserver = load("v7_preserver", ADAPTER / "run_v7_claim_preservation_private.py")
budget_runner = load("budget_runner", ROOT / "studies/apex-agent-eval/retrieval_adapter/build_private_budget_ledger.py")
pipeline_summary = load("pipeline_summary", ROOT / "studies/apex-agent-eval/retrieval_adapter/summarize_private_legal_pipeline.py")
v9_selector = load("v9_selector", ADAPTER / "select_v9_proposer_private.py")
v9_diagnostic = load("v9_diagnostic", ADAPTER / "run_v9_gate_diagnostic_private.py")


class RetrievalPanelContractTests(unittest.TestCase):
    def test_formal_executor_matrix_uses_reasoning_routes(self):
        routes = workflow_runner.EXECUTOR_ROUTES
        self.assertEqual(set(routes), {"deepseek", "muse", "glm", "ling", "sol"})
        self.assertEqual(routes["deepseek"][3], "high")
        self.assertNotIn("none", {route[3] for route in routes.values()})
        self.assertEqual(routes["muse"][:2], ("meta/muse-spark-1.2", "meta"))
        self.assertEqual(routes["glm"][:2], ("zai/glm-5.3-flash", "baseten"))
        self.assertEqual(routes["ling"][:2], ("inclusionai/ling-3.0-flash-fin", "novita"))
        self.assertEqual(routes["sol"][:2], ("openai/gpt-5.6-sol", "openai"))
        self.assertEqual(routes["sol"][3], "high")

    def test_agentic_disclosure_matrix_and_tool_schema_are_frozen(self):
        self.assertEqual(workflow_runner.AGENTIC_CONDITIONS, (
            "v12-full-claim-graph-control", "v12-static-disclosure-baseline",
            "v12.1-agentic-disclosure-finalize"))
        actions = agentic_disclosure.TOOL_DECISION_SCHEMA["properties"]["action"]["enum"]
        self.assertEqual(actions, ["traverse_graph", "search_gap", "answer"])
        self.assertEqual(agentic_disclosure.MAX_AGENT_TOOL_CALLS, 3)
        self.assertEqual(agentic_disclosure.MAX_AGENT_RESULTS_PER_CALL, 5)

    def test_agentic_disclosure_host_executes_bounded_model_choices(self):
        original_initial = agentic_disclosure.initial_context
        original_traverse = agentic_disclosure.traverse_graph
        original_search = agentic_disclosure.search_gap
        agentic_disclosure.initial_context = lambda query, scope: {
            "governed_context": [{"id": "claim-1"}], "coverage": "partial"}
        agentic_disclosure.traverse_graph = lambda query, scope, seeds, relations: {
            "governed_context": [{"id": "claim-2"}], "coverage": "covered"}
        agentic_disclosure.search_gap = lambda index, query: {
            "candidate_evidence": [{"status": "not_governed"}], "admission_authority": False}
        decisions = iter([
            {"action": "traverse_graph", "query": "related covenant",
             "seed_claim_ids": ["claim-1"], "relation_types": ["depends_on"], "reason": "expand"},
            {"action": "search_gap", "query": "missing schedule",
             "seed_claim_ids": [], "relation_types": [], "reason": "find evidence"},
            {"action": "answer", "query": "", "seed_claim_ids": [],
             "relation_types": [], "reason": "enough"},
        ])
        try:
            result = agentic_disclosure.run_agentic_disclosure(
                query="review", scope="task-1", index=object(), decide=lambda state: next(decisions))
        finally:
            agentic_disclosure.initial_context = original_initial
            agentic_disclosure.traverse_graph = original_traverse
            agentic_disclosure.search_gap = original_search
        self.assertEqual(result["tool_call_count"], 2)
        self.assertTrue(result["used_traverse_graph"])
        self.assertTrue(result["used_search_gap"])
        self.assertEqual(result["stop_reason"], "executor_ready")
        self.assertFalse(result["state"]["tool_results"][1]["result"]["admission_authority"])

    def test_agentic_resume_requires_decision_trace(self):
        legacy = {"artifact": {"answer": "x"}, "grades": []}
        traced = {**legacy, "agentic_trace": [{"action": "answer", "status": "accepted"}]}
        self.assertTrue(workflow_runner.resume_artifact_eligible(
            legacy, "v12-static-disclosure-baseline"))
        self.assertFalse(workflow_runner.resume_artifact_eligible(
            legacy, workflow_runner.AGENTIC_CONDITION))
        self.assertTrue(workflow_runner.resume_artifact_eligible(
            traced, workflow_runner.AGENTIC_CONDITION))

    def test_agentic_tool_budget_forces_answer_finalization(self):
        original_initial = agentic_disclosure.initial_context
        original_search = agentic_disclosure.search_gap
        agentic_disclosure.initial_context = lambda query, scope: {
            "governed_context": [{"id": "claim-1"}], "coverage": "partial"}
        agentic_disclosure.search_gap = lambda index, query: {
            "candidate_evidence": [], "admission_authority": False}
        decision = {"action": "search_gap", "query": "still missing",
                    "seed_claim_ids": [], "relation_types": [], "reason": "search again"}
        try:
            result = agentic_disclosure.run_agentic_disclosure(
                query="review", scope="task-1", index=object(), decide=lambda state: decision)
        finally:
            agentic_disclosure.initial_context = original_initial
            agentic_disclosure.search_gap = original_search
        self.assertEqual(result["tool_call_count"], 3)
        self.assertEqual(result["stop_reason"], "executor_ready_forced_finalization")
        self.assertEqual(result["trace"][-1]["next_action"], "finalize_without_more_tools")

    def test_v7_preserver_routes_are_frozen_and_never_generate_new_claims(self):
        self.assertEqual(v7_preserver.ROUTES["sol"]["model"], "openai/gpt-5.6-sol")
        decisions = v7_preserver.OUTPUT_SCHEMA["properties"]["decisions"]["items"]
        self.assertEqual(set(decisions["properties"]["verdict"]["enum"]),
                         {"keep", "repair", "reject"})
        self.assertNotIn("new_claim", decisions["properties"])

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

    def test_evidence_atom_and_claimability_gate_fail_closed(self):
        receipt = {"evidence_id": "E1", "receipt_digest": "sha256:" + "a" * 64,
                   "quote": "Buyer must deliver the certificate at Closing.",
                   "locator": {"kind": "section_span", "section_id": "S1",
                               "page_start": 2, "page_end": 2}}
        atom = {"schema_version": contract.EVIDENCE_ATOM_SCHEMA, "atom_id": "A1",
                "requirement_id": "R1", "evidence_id": "E1",
                "receipt_digest": receipt["receipt_digest"], "locator": receipt["locator"],
                "exact_excerpt": "Buyer must deliver the certificate",
                "subject": "Buyer", "predicate": "must deliver", "value": "certificate",
                "effective_date": None, "qualification": "at Closing",
                "document_version": None, "support_mode": "explicit"}
        self.assertEqual(contract.validate_evidence_atom(atom, {"E1": receipt}), atom)
        gate = contract.claimability_gate({"requirement_id": "R1"}, [atom])
        self.assertEqual(gate["state"], "claimable")
        self.assertEqual(contract.claimability_gate({"requirement_id": "R2"}, [atom])["state"], "gap")
        inferred = {**atom, "support_mode": "inferred"}
        self.assertEqual(contract.claimability_gate({"requirement_id": "R1"}, [inferred])["state"],
                         "needs_legal_analysis")
        with self.assertRaisesRegex(ValueError, "exact receipt substring"):
            contract.validate_evidence_atom({**atom, "exact_excerpt": "invented"}, {"E1": receipt})

    def test_v9_selector_reads_candidate_system_summary_and_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "score.json"
            path.write_text(json.dumps({
                "candidate_label": "evidence-first-v9",
                "paired": {"status": "scored", "paired_task_count": 4,
                           "candidate_unsupported_factual_claim_rate": 0.1,
                           "candidate_honest_gap_recall": 0.95},
                "systems": {"pr36-v7": {}, "evidence-first-v9": {
                    "supported_claim_coverage": 0.8,
                    "evidence_binding_pass_rate": 1.0,
                    "receipt_pass_rate": 1.0,
                    "mean_requirement_count": 20.0,
                }},
            }))
            row = v9_selector.candidate(str(path))
            self.assertEqual(row["supported_claim_coverage"], 0.8)
            passed, failures = v9_selector.eligible(row, {
                "unsupported_factual_claim_rate": 0.2,
                "supported_claim_coverage": 0.7,
                "mean_requirement_count": 20.0,
            })
            self.assertTrue(passed, failures)
            row["receipt_pass_rate"] = None
            self.assertIn("receipt_validity_not_one", v9_selector.eligible(row, {
                "unsupported_factual_claim_rate": 0.2,
                "supported_claim_coverage": 0.7,
                "mean_requirement_count": 20.0,
            })[1])

    def test_v9_gate_diagnostic_freezes_models_and_three_gate_placements(self):
        self.assertEqual(set(v9_diagnostic.EXTRACTORS), {"ling", "deepseek", "sol"})
        self.assertEqual(v9_diagnostic.MODES, (
            "strict_atom_preproposal", "receipt_preproposal", "postproposal_binding"))
        self.assertEqual(v9_diagnostic.EXTRACTORS["sol"],
                         ("gpt-5.6-sol", "openai", "low"))
        with self.assertRaisesRegex(ValueError, "unsupported claimability mode"):
            claim_runner._construct_v9({}, {}, None, None, None,
                                       claimability_mode="invented")

        class FakeGateway:
            calls = [{"status": "ok"}, {"status": "inconclusive"}]

            @staticmethod
            def receipt_rows():
                return [{"usage": {"cost_usd": 0.1}},
                        {"usage": {"cost_usd": 0.2}}]

        cost, missing = v9_diagnostic._cost([FakeGateway()])
        self.assertAlmostEqual(cost, 0.3)
        self.assertEqual(missing, 0)

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

    def test_v8_model_call_passes_stage_schema_and_fails_after_three_same_route_attempts(self):
        class FakeGateway:
            def __init__(self):
                self.calls = []

            def call(self, system, prompt, max_tokens, schema, schema_name):
                self.calls.append((schema, schema_name))
                return {"ok": False, "record": {"status": "inconclusive"}}

        gateway = FakeGateway()
        result = claim_runner._model_call(
            gateway, "system", "prompt", 100,
            claim_runner.CANDIDATE_SCHEMA, "proofpress_candidate_claims")
        self.assertFalse(result["ok"])
        self.assertEqual(len(gateway.calls), 3)
        self.assertTrue(all(schema is claim_runner.CANDIDATE_SCHEMA for schema, _ in gateway.calls))
        self.assertTrue(all(name == "proofpress_candidate_claims" for _, name in gateway.calls))
        self.assertEqual(result["record"]["attempt"], 3)
        self.assertEqual(claim_runner.DECOMPOSITION_SCHEMA["additionalProperties"], False)
        self.assertEqual(claim_runner.COVERAGE_SCHEMA["properties"]["additions"]["maxItems"], 8)

    def test_coverage_additions_rekey_cross_call_id_collisions(self):
        value = {"additions": [
            {"requirement_id": "req1", "requirement": "Check authority",
             "rationale": "Needed", "evidence_search_queries": ["authority"],
             "applicability": "applicable"},
            {"requirement_id": "new", "requirement": "Check tax",
             "rationale": "Needed", "evidence_search_queries": ["tax"],
             "applicability": "uncertain"},
        ]}
        additions = claim_runner._safe_additions(value, {"req1", "req2"})
        self.assertEqual(additions[0]["requirement_id"], "coverage_req_01")
        self.assertEqual(additions[1]["requirement_id"], "new")
        self.assertEqual(additions[0]["requirement"], "Check authority")

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

    def test_unresolved_critic_scope_becomes_partial_or_gap_not_task_failure(self):
        requirements = [
            {"requirement_id": "R1", "status": "covered"},
            {"requirement_id": "R2", "status": "covered"},
        ]
        claims = [{"id": "C1", "requirement_id": "R1"}]
        critic = {"repair_instructions": [
            {"requirement_id": "R1", "category": "evidence_fidelity"},
            {"requirement_id": "R2", "category": "honest_gap"},
        ]}
        changed = claim_runner._preserve_open_critic_gaps(requirements, claims, critic)
        self.assertEqual(changed, ["R1", "R2"])
        self.assertEqual(requirements[0]["status"], "partial")
        self.assertEqual(requirements[1]["status"], "gap")
        self.assertTrue(all(row["critic_open"] for row in requirements))

    def test_gap_cost_telemetry_does_not_erase_valid_retrieval_quality(self):
        with tempfile.TemporaryDirectory() as tmp:
            receipts = Path(tmp) / "receipts.jsonl"
            rows = [
                {"model": "m", "provider": "p", "fallback_used": False, "terminal": True,
                 "status": "ok", "cost_usd": 0.01},
                {"model": "m", "provider": "p", "fallback_used": False, "terminal": True,
                 "status": "inconclusive", "cost_usd": None},
            ]
            receipts.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
            summary = gap_runner.gateway_cost_summary(receipts, 0, "m", "p")
        self.assertEqual(summary["known_cost_usd"], 0.01)
        self.assertIsNone(summary["cost_usd"])
        self.assertEqual(summary["cost_status"], "inconclusive_missing_cost")
        self.assertEqual(summary["missing_cost_call_count"], 1)

    def test_critic_repairs_only_bound_requirements(self):
        requirements = [{"requirement_id": "R1"}, {"requirement_id": "R2"}, {"requirement_id": "R3"}]
        claims = [{"id": "C1", "requirement_id": "R1"}, {"id": "C2", "requirement_id": "R2"}]
        targets = claim_runner._critic_target_requirement_ids({
            "repair_instructions": [{"claim_id": "C1", "instruction": "split"}],
            "supplemental_queries": [{"requirement_id": "R3", "query": "missing evidence"}],
        }, requirements, claims)
        self.assertEqual(targets, {"R1", "R3"})

    def test_critic_diagnostic_exposes_round_scope_without_finding_text(self):
        diagnostic = claim_runner._critic_diagnostic({
            "decision": "needs repair",
            "repair_instructions": [{"claim_id": "C1", "instruction": "sensitive prose"},
                                    {"claim_id": "missing", "instruction": "other prose"}],
            "supplemental_queries": [{"requirement_id": "R2", "query": "private query"}],
        }, [{"requirement_id": "R1"}, {"requirement_id": "R2"}],
           [{"id": "C1", "requirement_id": "R1"}], 1)
        self.assertEqual(diagnostic["decision"], "needs_repair")
        self.assertEqual(diagnostic["target_requirement_ids"], ["R1", "R2"])
        self.assertEqual(diagnostic["unbound_finding_count"], 1)
        self.assertNotIn("sensitive prose", str(diagnostic))

    def test_claim_scorer_pairs_only_real_common_scored_artifacts(self):
        v7 = [{"task_id": "A", "status": "scored", "evidence_set_coverage": .4,
               "evidence_binding_pass_rate": 1.0},
              {"task_id": "B", "status": "inconclusive", "evidence_set_coverage": .2,
               "evidence_binding_pass_rate": .5}]
        v8 = [{"task_id": "A", "status": "scored", "evidence_set_coverage": .7,
               "evidence_binding_pass_rate": 1.0},
              {"task_id": "C", "status": "scored", "evidence_set_coverage": .9,
               "evidence_binding_pass_rate": 1.0}]
        paired = claim_scorer.paired_metrics(v7, v8)
        self.assertEqual(paired["paired_task_ids"], ["A"])
        self.assertAlmostEqual(paired["evidence_set_coverage_mean_delta_v8_minus_v7"], .3)
        self.assertEqual(paired["evidence_set_coverage_delta_bootstrap_95_ci"],
                         [paired["evidence_set_coverage_mean_delta_v8_minus_v7"]] * 2)
        self.assertIsNone(paired["requirement_recall_mean_delta_v8_minus_v7"])
        self.assertIn("requirement_to_rubric_mapping", paired["missing_semantic_adjudication"])

    def test_claim_pair_qualification_rejects_mismatched_or_unlabeled_v7(self):
        v8 = {"system": "v8", "catalog_digest": "sha256:cat", "raw_private_dir": "/private/v8",
              "tasks": [{"task_id": "A"}]}
        unlabeled = {"catalog_digest": "sha256:cat", "raw_private_dir": "/private/v7",
                     "tasks": [{"task_id": "A"}]}
        self.assertEqual(claim_scorer.qualify_pair_reports(unlabeled, v8)["status"], "fail")
        v7 = dict(unlabeled, system="pr36-v7", protocol=claim_scorer.PR36_V7_PROTOCOL)
        self.assertEqual(claim_scorer.qualify_pair_reports(v7, v8)["status"], "pass")
        routed = dict(v8, system="evidence-first-routed-deepseek")
        self.assertEqual(claim_scorer.qualify_pair_reports(v7, routed)["status"], "pass")

        v7_superset = dict(v7, tasks=[{"task_id": "A"}, {"task_id": "B"}])
        self.assertEqual(claim_scorer.qualify_pair_reports(v7_superset, v8)["status"], "fail")
        qualification = dict(v8, qualification={"requested": True})
        qualified = claim_scorer.qualify_pair_reports(v7_superset, qualification)
        self.assertEqual(qualified["status"], "pass")
        self.assertEqual(qualified["task_set_mode"], "qualification_v8_subset_of_v7")

    def test_claim_score_denominators_separate_panel_from_run(self):
        run = {"tasks": [{"task_id": "A"}, {"task_id": "B"}]}
        silver = {"tasks": [{"task_id": "A"}, {"task_id": "B"}, {"task_id": "C"}]}
        rows = [{"task_id": "A", "status": "scored", "silver_locator_count": 1},
                {"task_id": "B", "status": "inconclusive", "silver_locator_count": 1}]
        denominators, absent = claim_scorer.score_denominators(run, silver, rows, [])
        self.assertEqual(denominators["panel_expected_tasks"], 3)
        self.assertEqual(denominators["run_expected_tasks"], 2)
        self.assertEqual(denominators["inconclusive_tasks"], 1)
        self.assertEqual(denominators["panel_tasks_absent_from_run"], 1)
        self.assertEqual(absent, ["C"])

    def test_semantic_adjudication_rejects_unknown_ids(self):
        systems = {"v7": {"requirements": [{"requirement_id": "R7"}], "claims": [{"id": "C7"}]},
                   "v8": {"requirements": [{"requirement_id": "R8"}], "claims": [{"id": "C8"}]}}
        value = {"systems": {
            "system_a": {"requirement_to_rubric": [{"rubric_id": "rubric-1", "requirement_ids": ["R7"]}],
                         "factual_claim_ids": ["C7"], "unsupported_factual_claim_ids": [],
                         "expected_open_gap_requirement_ids": [], "honest_open_gap_requirement_ids": [],
                         "gap_to_silver_candidates": []},
            "system_b": {"requirement_to_rubric": [], "factual_claim_ids": ["unknown"],
                         "unsupported_factual_claim_ids": [], "expected_open_gap_requirement_ids": [],
                         "honest_open_gap_requirement_ids": [], "gap_to_silver_candidates": []}}}
        with self.assertRaisesRegex(ValueError, "factual claim"):
            semantic_runner._normalize_labels(value, {"system_a": "v7", "system_b": "v8"},
                                              systems, {"rubric-1"}, {"silver-1"})

    def test_semantic_adjudication_closes_factual_set_over_unsupported_labels(self):
        systems = {"v7": {"requirements": [{"requirement_id": "R7"}],
                           "claims": [{"id": "C7"}]},
                   "v8": {"requirements": [{"requirement_id": "R8"}],
                           "claims": [{"id": "C8"}]}}
        empty = {"requirement_to_rubric": [], "factual_claim_ids": [],
                 "unsupported_factual_claim_ids": [],
                 "expected_open_gap_requirement_ids": [],
                 "honest_open_gap_requirement_ids": [], "gap_to_silver_candidates": []}
        value = {"systems": {"system_a": empty,
                             "system_b": {**empty, "unsupported_factual_claim_ids": ["C8"]}}}
        normalized = semantic_runner._normalize_labels(
            value, {"system_a": "v7", "system_b": "v8"}, systems, set(), set())
        self.assertEqual(normalized["systems"]["v8"]["factual_claim_ids"], ["C8"])
        self.assertEqual(normalized["systems"]["v8"]["unsupported_factual_claim_ids"], ["C8"])

    def test_claim_scorer_uses_post_output_semantic_labels_when_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp)
            labels = {"rubric_atom_ids": ["r1", "r2"], "labels": {"systems": {
                "v7": {"requirement_to_rubric": [{"rubric_id": "r1", "requirement_ids": ["R1"]}],
                       "factual_claim_ids": ["C1", "C2"], "unsupported_factual_claim_ids": ["C2"],
                       "expected_open_gap_requirement_ids": ["R2"], "honest_open_gap_requirement_ids": []},
                "v8": {"requirement_to_rubric": [{"rubric_id": "r1", "requirement_ids": ["R1"]},
                                                   {"rubric_id": "r2", "requirement_ids": ["R2"]}],
                       "factual_claim_ids": ["C1", "C2"], "unsupported_factual_claim_ids": [],
                       "expected_open_gap_requirement_ids": ["R3"], "honest_open_gap_requirement_ids": ["R3"]},
            }}}
            (raw / "A.json").write_text(json.dumps(labels))
            metrics = claim_scorer.semantic_paired_metrics({"raw_private_dir": str(raw)}, ["A"])
        self.assertEqual(metrics["requirement_recall_mean_delta_v8_minus_v7"], .5)
        self.assertEqual(metrics["unsupported_factual_claim_rate_mean_delta_v8_minus_v7"], -.5)
        self.assertEqual(metrics["v8_honest_gap_recall"], 1.0)
        self.assertEqual(metrics["requirement_recall_delta_bootstrap_95_ci"], [.5, .5])

    def test_gap_rrf_collapses_overlapping_page_spans(self):
        def receipt(uri, start, end):
            return {"source": {"uri": uri, "content_digest": "sha256:" + "a" * 64},
                    "evidence": {"locator": {"kind": "section_span", "page_start": start, "page_end": end}}}
        result = gap_runner.hybrid_rrf([receipt("private://a", 1, 2)],
                                       [receipt("private://a", 2, 3)])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["retrieval"]["systems"], ["bm25", "pageindex"])

    def test_gap_inconclusive_primary_is_not_scored_as_zero(self):
        metrics = {f"k={k}": {"evidence_set_coverage": 0.0,
                               "complete_evidence_set_success": False,
                               "citation_precision": 0.0, "receipt_pass_rate": 0.0}
                   for k in gap_runner.K_VALUES}
        report = {"denominators": {}, "pageindex": {"mean_rebuild_locator_jaccard": 1.0},
                  "tasks": [{"gold_locator_count": 1,
                             "pageindex_builds": [{"status": "inconclusive"},
                                                   {"status": "inconclusive"},
                                                   {"status": "inconclusive"}],
                             "primary_to_rebuild_locator_jaccard": [1.0, 1.0],
                             "systems": {"bm25-page/v1": metrics,
                                         "pageindex-tree/v1": metrics,
                                         "hybrid-rrf/v1": metrics}}]}
        corrected = gap_runner.enforce_inconclusive_build_semantics(report)
        self.assertIsNone(corrected["systems"]["pageindex-tree/v1"]["k=5"]["evidence_set_coverage"])
        self.assertEqual(corrected["paired_pageindex_minus_bm25_at_5"]["denominator"], 0)
        self.assertIsNone(corrected["pageindex"]["mean_rebuild_locator_jaccard"])

    def test_gap_gold_outside_catalog_custody_is_not_scored(self):
        metrics = {f"k={k}": {"evidence_set_coverage": 0.0,
                               "complete_evidence_set_success": False,
                               "citation_precision": 0.0, "receipt_pass_rate": 1.0}
                   for k in gap_runner.K_VALUES}
        report = {"denominators": {}, "pageindex": {},
                  "systems": {name: dict(metrics) for name in
                              ("bm25-page/v1", "pageindex-tree/v1", "hybrid-rrf/v1")},
                  "tasks": [{"task_id": "T1", "gold_locator_count": 1,
                             "pageindex_builds": [{"status": "inconclusive"}] * 3,
                             "primary_to_rebuild_locator_jaccard": [None, None],
                             "systems": {name: dict(metrics) for name in
                                         ("bm25-page/v1", "pageindex-tree/v1", "hybrid-rrf/v1")}}]}
        manifest = {"tasks": [{"task_id": "T1", "gold": [{"source_uri": "private://text"}]}]}
        catalog = {"representations": [{"source": {"uri": "private://pdf",
                                                      "media_type": "application/pdf"}}]}
        corrected = gap_runner.enforce_adapter_eligible_gold(report, manifest, catalog)
        self.assertEqual(corrected["denominators"]["tasks_with_adapter_eligible_gold"], 0)
        self.assertIsNone(corrected["systems"]["bm25-page/v1"]["k=5"]["evidence_set_coverage"])

    def test_gap_qualification_rejects_any_frozen_task_without_adapter_gold(self):
        with self.assertRaisesRegex(ValueError, "T2"):
            gap_runner.qualify_gap_manifest({
                "tasks": [{"task_id": "T1", "query": "q", "gold": [{"source_uri": "private://a"}]}],
                "excluded_tasks": [{"task_id": "T2", "reason": "no adapter gold"}],
            })
        with self.assertRaisesRegex(ValueError, "no frozen-gap tasks"):
            gap_runner.qualify_gap_manifest({"tasks": [], "excluded_tasks": []})

    def test_gap_qualification_reports_but_does_not_score_non_retrieval_gaps(self):
        manifest = {
            "tasks": [{"task_id": "T1", "query": "q",
                       "gold": [{"source_uri": "private://a"}]}],
            "excluded_tasks": [{"task_id": "T2",
                                "reason": "open gaps have no frozen retrievable silver target",
                                "qualification_blocking": False}],
        }
        gap_runner.qualify_gap_manifest(manifest)

    def test_gap_freeze_accepts_non_pdf_canonical_gold(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_run, raw_silver = root / "run", root / "silver"
            raw_run.mkdir(); raw_silver.mkdir()
            (raw_run / "T1.json").write_text(json.dumps({"construction": {"requirements": [{
                "requirement_id": "R1", "requirement": "Find email", "status": "gap",
                "evidence_search_queries": ["email evidence"]}]}}))
            (raw_silver / "T1.json").write_text(json.dumps({"locators": [{
                "source_uri": "private://mail", "locator": {"page_start": 1, "page_end": 1}}],
                "silver_digest": "sha256:" + "a" * 64}))
            manifest = gap_runner.freeze_gaps(
                {"raw_private_dir": str(raw_run), "tasks": [{"task_id": "T1"}]},
                {"raw_private_dir": str(raw_silver)},
                {"representations": [{"source": {"uri": "private://mail", "media_type": "application/mbox"},
                                      "sections": [{"id": "s1"}]}], "catalog_digest": "x"})
            self.assertEqual(len(manifest["tasks"]), 1)
            self.assertEqual(manifest["excluded_tasks"], [])
            gap_runner.qualify_gap_manifest(manifest)

    def test_materializes_non_pdf_catalog_sections_with_locator_map(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = {"representations": [{
                "source": {"uri": "private://mail", "media_type": "application/mbox",
                           "content_digest": "sha256:" + "a" * 64},
                "representation_digest": "sha256:" + "b" * 64,
                "transform_digest": "sha256:" + "c" * 64, "page_count": 2,
                "sections": [{"id": "s1", "heading": "Message", "text": "Body",
                              "text_digest": "sha256:" + "d" * 64,
                              "page_start": 2, "page_end": 2}]}]}
            sources = gap_runner.materialize_pageindex_sources(payload, Path(tmp))
            self.assertEqual(len(sources), 1)
            self.assertEqual(sources[0]["representation_kind"], "canonical_markdown")
            self.assertEqual(sources[0]["locator_map"][0]["section_id"], "s1")
            self.assertEqual(sources[0]["locator_map"][0]["page_start"], 2)
            self.assertTrue(Path(sources[0]["path"]).is_file())

    def test_pageindex_request_preserves_dual_custody_and_locator_mapping(self):
        source = {"source_id": "s1", "path": "/private/canonical.md",
                  "uri": "private://original.docx",
                  "content_digest": "sha256:" + "a" * 64,
                  "path_digest": "sha256:" + "b" * 64,
                  "representation_digest": "sha256:" + "c" * 64,
                  "transform_digest": "sha256:" + "d" * 64,
                  "media_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                  "representation_kind": "canonical_markdown",
                  "locator_map": [{"line": 1, "section_id": "sec-1",
                                   "section_digest": "sha256:" + "e" * 64,
                                   "page_start": 2, "page_end": 2}]}
        request = panel.tree_request("authority", [source], {"config_digest": "sha256:x"},
                                     5, Path("/private/cache"))
        emitted = request["sources"][0]
        self.assertEqual(emitted["content_digest"], source["content_digest"])
        self.assertEqual(emitted["path_digest"], source["path_digest"])
        self.assertEqual(emitted["representation_kind"], "canonical_markdown")
        self.assertEqual(emitted["locator_map"], source["locator_map"])

    def test_claim_scorer_counts_each_silver_locator_once(self):
        evidence = {"source": {"uri": "private://a"},
                    "locator": {"page_start": 1, "page_end": 2}}
        silver = {"source_uri": "private://a", "locator": {"page_start": 2, "page_end": 3}}
        self.assertTrue(claim_scorer.locator_hit(evidence, silver))
        self.assertFalse(claim_scorer.locator_hit(evidence,
                                                  {"source_uri": "private://b", "locator": silver["locator"]}))

    def test_pageindex_document_router_is_query_ranked_and_digest_bound(self):
        def representation(uri, text, digest_char):
            return {"source": {"uri": uri, "media_type": "text/plain",
                                "content_digest": "sha256:" + digest_char * 64},
                    "representation_digest": "sha256:" + digest_char.upper() * 64,
                    "sections": [{"id": uri[-1], "heading": uri, "text": text,
                                  "text_digest": "sha256:" + digest_char * 64,
                                  "page_start": 1, "page_end": 1}]}
        catalog = {"representations": [
            representation("private://a", "employment tax", "a"),
            representation("private://b", "closing indemnity indemnity", "b"),
        ]}
        index = claim_runner.SectionIndex(catalog)
        sources = [{"uri": "private://a"}, {"uri": "private://b"}]
        routed, audit = gap_runner.route_pageindex_sources(index, "indemnity", sources, 1)
        self.assertEqual([row["uri"] for row in routed], ["private://b"])
        self.assertEqual(audit["adapter"], "bm25-document-router/v1")
        self.assertTrue(audit["route_digest"].startswith("sha256:"))
        full, full_audit = gap_runner.route_pageindex_sources(index, "indemnity", sources, len(sources))
        self.assertEqual([row["uri"] for row in full], ["private://b", "private://a"])
        self.assertEqual(full_audit["adapter"], "bm25-full-corpus-order/v1")

    def test_hierarchical_hybrid_keeps_global_safety_lane(self):
        def representation(uri, text, page):
            char = str(page)
            return {"source": {"uri": uri, "media_type": "text/plain",
                                "content_digest": "sha256:" + char * 64},
                    "representation_digest": "sha256:" + char * 64,
                    "sections": [{"id": f"s{page}", "heading": "Closing Conditions",
                                  "text": text, "text_digest": "sha256:" + char * 64,
                                  "page_start": page, "page_end": page}]}
        catalog = {"representations": [
            representation("private://a", "closing certificate delivery", 1),
            representation("private://b", "closing condition consent", 2),
            representation("private://c", "closing schedule date", 3),
        ]}
        index = claim_runner.SectionIndex(catalog)
        global_rows = gap_runner.bm25_receipts(index, "closing risk")
        pageindex_rows = [global_rows[-1]]
        result = gap_runner.prior_bm25(index, "closing risk", global_rows, pageindex_rows, 5)
        self.assertGreaterEqual(sum(row["retrieval"]["global_safety_lane"] for row in result[:5]), 2)
        self.assertTrue(all(row["retrieval"]["adapter"] == "pageindex-prior-bm25/v1" for row in result))
        exact = gap_runner.prior_bm25(index, "Section 4.2", global_rows, pageindex_rows, 5)
        self.assertTrue(all(row["retrieval"].get("route_bypassed") == "exact_query" for row in exact))

    def test_gap_route_preflight_reports_locator_ceiling(self):
        def representation(uri, text):
            return {"source": {"uri": uri, "media_type": "text/plain",
                                "content_digest": "sha256:" + "a" * 64},
                    "representation_digest": "sha256:" + "b" * 64,
                    "sections": [{"id": uri[-1], "heading": uri, "text": text,
                                  "text_digest": "sha256:" + "c" * 64,
                                  "page_start": 1, "page_end": 1}]}
        catalog = {"representations": [representation("private://a", "indemnity"),
                                        representation("private://b", "unrelated")]}
        index = claim_runner.SectionIndex(catalog)
        sources = [{"uri": "private://a"}, {"uri": "private://b"}]
        manifest = {"tasks": [{"task_id": "T1", "query": "indemnity", "gold": [
            {"source_uri": "private://a"}, {"source_uri": "private://a"},
            {"source_uri": "private://missing"}]}]}
        rows, ceiling = gap_runner.route_reachability_preflight(manifest, index, sources)
        self.assertEqual(rows[0]["gold_locators_routed"], 2)
        self.assertEqual(rows[0]["gold_locator_count"], 3)
        self.assertAlmostEqual(ceiling, 2 / 3)

    def test_scored_gap_run_requires_never_existing_cache_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            paths = gap_runner.require_fresh_cache_dirs(out)
            self.assertEqual(len(paths), 3)
            paths[1].mkdir()
            with self.assertRaisesRegex(ValueError, "pageindex-cache-build-2"):
                gap_runner.require_fresh_cache_dirs(out)

    def test_bounded_route_scores_unreachable_gold_as_misses_or_stays_diagnostic(self):
        self.assertEqual(gap_runner.qualify_route_ceiling(0.75, False), (True, False))
        self.assertEqual(gap_runner.qualify_route_ceiling(0.75, True), (True, True))
        self.assertEqual(gap_runner.qualify_route_ceiling(1.0, False), (False, False))
        with self.assertRaisesRegex(ValueError, "invalid locator"):
            gap_runner.qualify_route_ceiling(1.1, False)

    def test_warm_replay_requires_every_routed_source_to_hit_cache(self):
        self.assertEqual(
            warm_runner.validate_warm_telemetry(
                {"index_cache_hits": 20, "index_cache_misses": 0}, 20),
            (20, 0),
        )
        with self.assertRaisesRegex(RuntimeError, "non-warm cache state"):
            warm_runner.validate_warm_telemetry(
                {"index_cache_hits": 19, "index_cache_misses": 1}, 20)
        with self.assertRaisesRegex(RuntimeError, "non-warm cache state"):
            warm_runner.validate_warm_telemetry(
                {"index_cache_hits": 19, "index_cache_misses": 0}, 20)

    def test_workflow_freeze_interleaves_tasks_and_grades_fail_closed(self):
        rows = [("task-a", 1), ("task-a", 2), ("task-b", 3)]
        self.assertEqual(ask_freezer.interleave_by_task(rows, ["task-a", "task-b"], 3),
                         [("task-a", 1), ("task-b", 3), ("task-a", 2)])
        grade = workflow_runner.normalize_grade({"rubric_fraction": 0.75, "unsupported_claims": 1})
        self.assertEqual(grade["rubric_fraction"], 0.75)
        with self.assertRaisesRegex(ValueError, "rubric_fraction"):
            workflow_runner.normalize_grade({"rubric_fraction": 2})
        self.assertEqual(
            workflow_runner.normalize_grade({"rubric_fraction": 0.5,
                                             "unsupported_claims": ["one", "two"],
                                             "citation_errors": [],
                                             "authority_errors": [{"finding": "staged"}]}),
            {"rubric_fraction": 0.5, "unsupported_claims": 2,
             "citation_errors": 0, "authority_errors": 1},
        )
        with self.assertRaisesRegex(ValueError, "unsupported_claims"):
            workflow_runner.normalize_grade({"rubric_fraction": 0.5,
                                             "unsupported_claims": "one"})
        self.assertFalse(workflow_runner.EXECUTOR_SCHEMA["additionalProperties"])
        self.assertEqual(
            set(workflow_runner.EXECUTOR_SCHEMA["required"]),
            {"answer", "ask_answers", "citations", "gaps"},
        )
        self.assertFalse(workflow_runner.GRADER_SCHEMA["additionalProperties"])
        self.assertEqual(workflow_runner.GRADER_SCHEMA["properties"]["unsupported_claims"]["type"],
                         "integer")

    def test_workflow_runtime_paths_survive_workspace_chdir(self):
        original = Path.cwd()
        relative = Path("tools/pageindex-sidecar/gateway_openai_server.mjs")
        resolved = Path(workflow_runner.resolve_runtime_path(str(relative)))
        self.assertTrue(resolved.is_absolute())
        self.assertTrue(resolved.is_file())
        self.assertEqual(resolved, original / relative)
        self.assertEqual(workflow_runner.gateway_bridge_values("shared", None, None),
                         ("shared", "shared"))
        self.assertEqual(workflow_runner.gateway_bridge_values(None, "pageindex", "claim"),
                         ("pageindex", "claim"))
        with self.assertRaisesRegex(ValueError, "both PageIndex and claim"):
            workflow_runner.gateway_bridge_values(None, "pageindex", None)

    def test_workflow_disclosure_receipt_normalizes_panel_rows(self):
        row = {"source": {"uri": "private://a", "content_digest": "sha256:" + "a" * 64,
                          "media_type": "text/plain"},
               "evidence": {"quote": "x", "locator": {"kind": "section_span",
                   "section_id": "S", "section_digest": "sha256:" + "b" * 64,
                   "page_start": 1, "page_end": 1}},
               "retrieval": {"adapter": "bm25-page/v1", "rank": 1}}
        receipt = workflow_runner.disclosure_receipt(row, "query", "sha256:" + "c" * 64)
        self.assertEqual(receipt["schema_version"], "proofpress/retrieval-evidence/v1")
        self.assertEqual(receipt["retrieval"]["query"], "query")
        self.assertEqual(receipt["retrieval"]["version"], "1")
        self.assertEqual(receipt["evidence"]["locator"]["section_id"], "S")

    def test_workflow_grade_normalization_is_safe_for_resume(self):
        prior = [{"rubric_fraction": 0.8, "unsupported_claims": ["x"],
                  "citation_errors": 0, "authority_errors": 0}]
        resumed = [workflow_runner.normalize_grade(row) for row in prior]
        self.assertEqual(resumed[0]["unsupported_claims"], 1)

    def test_workflow_staging_rejects_self_relations_without_crashing(self):
        graph = {
            "task": {"task_id": "task-a"},
            "construction": {
                "evidence": [{
                    "evidence_id": "e1",
                    "source": {"uri": "private://a", "content_digest": "sha256:" + "a" * 64},
                    "quote": "Authority is documented.",
                    "locator": {"kind": "page_span", "page_start": 1, "page_end": 1},
                    "retrieval": {"query": "authority"},
                }],
                "claims": [{"id": "c1", "statement": "Authority is documented.",
                            "evidence_ids": ["e1"]}],
                "relations": [{"from": "c1", "to": "c1", "type": "supports"}],
            },
        }
        knowledge = workflow_runner.knowledge
        originals = (knowledge._import_retrieval_evidence_v2, knowledge.propose_v2, knowledge.review_v2)
        knowledge._import_retrieval_evidence_v2 = lambda payload: [{"evidence": {"id": "imported-e1"}}]
        knowledge.propose_v2 = lambda *args: {"conclusion": {"id": "staged-c1"}}
        knowledge.review_v2 = lambda *args: None
        try:
            mapping, diagnostics = workflow_runner.stage_graph(
                graph, {"private://a": "/private/a.pdf"})
        finally:
            (knowledge._import_retrieval_evidence_v2, knowledge.propose_v2,
             knowledge.review_v2) = originals
        self.assertEqual(mapping, {"c1": "staged-c1"})
        self.assertEqual(diagnostics["candidate_count"], 1)
        self.assertEqual(diagnostics["admitted_count"], 0)
        self.assertEqual(diagnostics["rejected_counts"], {"self_relation": 1})
        self.assertTrue(diagnostics["rejected_relation_digest"].startswith("sha256:"))

    def test_workflow_staging_keeps_policy_blocked_relation_out_of_graph(self):
        graph = {
            "task": {"task_id": "task-a"},
            "construction": {
                "evidence": [{"evidence_id": "e1", "source": {"uri": "private://a"},
                              "quote": "q", "locator": {}, "retrieval": {}}],
                "claims": [{"id": "c1", "statement": "one", "evidence_ids": ["e1"]},
                           {"id": "c2", "statement": "two", "evidence_ids": ["e1"]}],
                "relations": [{"from": "c1", "to": "c2", "type": "supports"}],
            },
        }
        knowledge = workflow_runner.knowledge
        names = ("_import_retrieval_evidence_v2", "propose_v2", "review_v2",
                 "propose_relation_v2", "review_relation_v2")
        originals = [getattr(knowledge, name) for name in names]
        knowledge._import_retrieval_evidence_v2 = lambda payload: [{"evidence": {"id": "e"}}]
        ids = iter(("staged-c1", "staged-c2"))
        knowledge.propose_v2 = lambda *args: {"conclusion": {"id": next(ids)}}
        knowledge.review_v2 = lambda *args: None
        knowledge.propose_relation_v2 = lambda *args: {"relation": {"id": "r1"}}
        reviews = []
        def review_relation(relation_id, decision, actor):
            reviews.append(decision)
            if decision == "admit":
                raise ValueError("relation is blocked by deterministic policy")
        knowledge.review_relation_v2 = review_relation
        try:
            _, diagnostics = workflow_runner.stage_graph(graph, {"private://a": "/private/a"})
        finally:
            for name, value in zip(names, originals):
                setattr(knowledge, name, value)
        self.assertEqual(reviews, ["admit", "reject"])
        self.assertEqual(diagnostics["admitted_count"], 0)
        self.assertEqual(diagnostics["rejected_counts"], {"policy_admission_rejected": 1})

    def test_workflow_compacts_large_disclosure_without_emptying_context(self):
        packet = {"schema_version": "proofpress/governed-disclosure/v1", "coverage": "covered",
                  "governed_context": [{"id": "c1", "statement": "x" * 100000,
                                         "scope": "s", "digest": "sha256:" + "a" * 64}],
                  "lineage": [{"conclusion": {"id": "c1"}, "state": "admitted",
                               "evidence": []}], "gaps": [], "blocked": [],
                  "discovered_evidence": []}
        compact = workflow_runner.compact_disclosure_packet(packet, 10000)
        self.assertTrue(compact["governed_context"])
        self.assertLess(len(compact["governed_context"][0]["statement"]), 5000)

    def test_workflow_qualification_fails_closed_on_missing_comparator(self):
        result = workflow_runner.qualification_preflight(
            {"full-catalog-bm25-prefetch": '[{"text":"x"}]',
             "pr36-v7-prefetched-context": None}, ["task-a"], None)
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["failures"][0]["condition"], "pr36-v7-prefetched-context")

    def test_workflow_oracle_controls_are_explicitly_leaky_and_nonempty(self):
        graph = {"task": {"rubric": ["must not enter oracle claims"]},
                 "construction": {"claims": [{"id": "C1", "statement": "Closing is scheduled"}],
                                  "relations": [], "requirements": [{"requirement_id": "R1",
                                                                      "status": "gap"}]}}
        silver = {"locators": [{"source_uri": "private://a",
                                  "candidate_id": "S1",
                                  "locator": {"page_start": 2, "page_end": 2}}],
                  "judgments": {"a": {"minimum_evidence_sets": [{"candidate_ids": ["S1"]}]}}}
        catalog = {"representations": [{"source": {"uri": "private://a"},
                                         "sections": [{"section_id": "s2", "page_start": 2,
                                                       "page_end": 2, "text": "Closing is June 1."}]}]}
        controls = workflow_runner.oracle_diagnostic_contexts(graph, silver, catalog, [{"coverage": "partial"}])
        oracle = controls["oracle-claim-graph"]
        direct = controls["v9-claim-graph-plus-direct-gap-evidence"]
        self.assertTrue(oracle["diagnostic_only"])
        self.assertFalse(oracle["rubric_leakage"])
        self.assertEqual(oracle["claims"][0]["statement"], "Closing is scheduled")
        self.assertNotIn("rubric_atom", oracle["claims"][0])
        self.assertEqual(oracle["evidence"][0]["section_id"], "s2")
        self.assertEqual(oracle["gap_bindings"][0]["gap_id"], "R1")
        self.assertEqual(direct["direct_gap_evidence"][0]["gap_ids"], ["R1"])
        self.assertTrue(direct["direct_gap_evidence"])

    def test_workflow_custody_manifest_binds_original_source_not_canonical_path(self):
        catalog = {"source_navigation": [{"uri": "private://source", "path": "/private/original.docx"}],
                   "representations": [{"source": {
                       "uri": "private://source", "content_digest": "sha256:" + "a" * 64,
                       "media_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"},
                       "representation_digest": "sha256:" + "b" * 64}]}
        rows = workflow_runner.custody_manifest_sources(catalog)
        self.assertEqual(rows, [{"uri": "private://source", "path": "/private/original.docx",
                                 "content_digest": "sha256:" + "a" * 64,
                                 "media_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}])

    def test_workflow_context_compaction_is_valid_json_and_conservatively_bounded(self):
        text, upper_bound = workflow_runner.bounded_json(
            {"claims": [{"statement": "é" * 50000}]}, max_tokens=2000)
        decoded = json.loads(text)
        self.assertIsInstance(decoded, dict)
        self.assertEqual(len(decoded["claims"]), 1)
        self.assertTrue(decoded["claims"][0]["statement"])
        self.assertLessEqual(len(text.encode()), 2000)
        self.assertEqual(upper_bound, len(text.encode()))

    def test_workflow_context_compaction_preserves_single_disclosure_packet(self):
        packet = [{"schema_version": "proofpress/governed-disclosure/v1",
                   "coverage": "partial",
                   "governed_context": [{"id": "claim-1", "statement": "x" * 50000}],
                   "gaps": [{"gap_id": "gap-1", "query": "y" * 50000}]}]
        text, upper_bound = workflow_runner.bounded_json(packet, max_tokens=2000)
        decoded = json.loads(text)
        self.assertEqual(len(decoded), 1)
        self.assertEqual(decoded[0]["schema_version"], "proofpress/governed-disclosure/v1")
        self.assertEqual(decoded[0]["coverage"], "partial")
        self.assertTrue(decoded[0]["governed_context"])
        self.assertTrue(decoded[0]["gaps"])
        self.assertLessEqual(upper_bound, 2000)

    def test_workflow_enforces_three_disclosure_calls_per_task(self):
        self.assertEqual(len(workflow_runner.disclosure_bundles([{"query": "q"}] * 12)), 3)
        with self.assertRaisesRegex(ValueError, "disclosure limit exceeded"):
            workflow_runner.disclosure_bundles([{"query": "q"}] * 13)

    def test_native_docx_creation_and_edit_preserve_output_contract(self):
        if native_artifact is None:
            self.skipTest("native DOCX fixture requires the bundled document runtime")
        content = {"title": "Tax Memo", "sections": [{"heading": "Conclusion", "body": "A bounded conclusion."}]}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); created = root / "created.docx"
            create_checks = native_artifact.materialize_docx(content, created)
            self.assertTrue(create_checks["artifact_valid"])
            edited = root / "edited.docx"
            edit_checks = native_artifact.materialize_docx(
                {"title": "Amendment", "sections": [{"heading": "Covenant", "body": "Sellers shall cooperate."}]},
                edited, source=created)
            self.assertTrue(edit_checks["artifact_valid"])
            self.assertTrue(edit_checks["actually_modified"])
            self.assertTrue(edit_checks["basic_structure_preserved"])

    def test_full_graph_cap_telemetry_reports_text_truncation(self):
        graph = {"claims": [{"id": "c1", "statement": "x" * 30000, "evidence_ids": ["e1"]}],
                 "relations": [], "evidence": [{"evidence_id": "e1", "quote": "y" * 30000}]}
        text, upper, telemetry = workflow_runner.bounded_graph_json(graph)
        self.assertLessEqual(upper, workflow_runner.MAX_CONTEXT_TOKEN_UPPER_BOUND)
        self.assertTrue(telemetry["truncated_by_context_cap"])
        self.assertEqual(telemetry["before"]["claims"], telemetry["after"]["claims"])
        self.assertTrue(json.loads(text)["claims"])

    def test_workflow_uses_full_canonical_custody_and_normalizes_v7_raw_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            catalog = {"source_navigation": [], "representations": [{
                "source": {"uri": "private://mail", "media_type": "application/mbox",
                           "content_digest": "sha256:" + "a" * 64},
                "representation_digest": "sha256:" + "b" * 64,
                "transform_digest": "sha256:" + "c" * 64, "page_count": 1,
                "sections": [{"id": "mail-s1", "heading": "Message", "text": "Closing email",
                              "text_digest": "sha256:" + "d" * 64,
                              "page_start": 1, "page_end": 1}]}]}
            sources = workflow_runner.materialize_pageindex_sources(catalog, Path(tmp))
            self.assertEqual(sources[0]["representation_kind"], "canonical_markdown")
            self.assertEqual(sources[0]["locator_map"][0]["section_id"], "mail-s1")
        context = workflow_runner.prefetched_context_from_construction_artifact({
            "construction": {"claims": [{"id": "c1"}], "relations": [], "evidence": [{"id": "e1"}]},
            "raw": {"private": True}})
        self.assertEqual(context, {"claims": [{"id": "c1"}], "relations": [],
                                   "evidence": [{"id": "e1"}]})

    def test_budget_report_argument_and_nested_cost_are_explicit(self):
        label, path, field = budget_runner.parse_report(
            "formal=/private/report.json::telemetry.known_cost_usd")
        self.assertEqual(label, "formal")
        self.assertEqual(path, Path("/private/report.json"))
        self.assertEqual(field, "telemetry.known_cost_usd")
        self.assertEqual(budget_runner.nested(
            {"telemetry": {"known_cost_usd": 1.25}}, field), 1.25)

    def test_incomplete_workflow_report_is_not_promotable(self):
        complete = {"qualification": {"status": "pass"},
                    "denominators": {"planned_cells": 28, "scored_cells": 28,
                                     "inconclusive_cells": 0}}
        incomplete = {"qualification": {"status": "fail"},
                      "denominators": {"planned_cells": 28, "scored_cells": 27,
                                       "inconclusive_cells": 1}}
        self.assertTrue(pipeline_summary.workflow_report_complete(complete))
        self.assertFalse(pipeline_summary.workflow_report_complete(incomplete))


if __name__ == "__main__":
    unittest.main()

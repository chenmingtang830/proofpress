import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "studies/apex-agent-eval/retrieval_adapter"
sys.path.insert(0, str(ADAPTER))
SPEC = importlib.util.spec_from_file_location(
    "exact_knowledge_contract", ADAPTER / "exact_knowledge_contract.py")
exact = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(exact)
RUNNER_SPEC = importlib.util.spec_from_file_location(
    "run_exact_knowledge_readiness_private",
    ADAPTER / "run_exact_knowledge_readiness_private.py")
runner = importlib.util.module_from_spec(RUNNER_SPEC); RUNNER_SPEC.loader.exec_module(runner)
REVIEW_SPEC = importlib.util.spec_from_file_location(
    "build_exact_knowledge_review_queue_private",
    ADAPTER / "build_exact_knowledge_review_queue_private.py")
review = importlib.util.module_from_spec(REVIEW_SPEC); REVIEW_SPEC.loader.exec_module(review)
STAGE_RUNNER_SPEC = importlib.util.spec_from_file_location(
    "run_exact_knowledge_stage_a_private",
    ADAPTER / "run_exact_knowledge_stage_a_private.py")
stage_runner = importlib.util.module_from_spec(STAGE_RUNNER_SPEC)
STAGE_RUNNER_SPEC.loader.exec_module(stage_runner)


class ExactKnowledgeContractTests(unittest.TestCase):
    def receipt(self):
        return {"evidence_id": "E1", "receipt_digest": "sha256:" + "a" * 64,
                "source_digest": "sha256:" + "b" * 64, "custody_valid": True,
                "quote": "Laura owned 26% in 2024 and the exact tax was $18,486.",
                "locator": {"kind": "page_span", "page_start": 1, "page_end": 1}}

    def atom(self, *, atom_id="A_TAX", requirement_id="R_TAX", display="$18,486",
             decimal_value="18486", kind="currency", entity="Laura", period="2024"):
        excerpt = self.receipt()["quote"]
        return {"schema_version": "proofpress/evidence-atom/v2", "atom_id": atom_id,
                "requirement_id": requirement_id, "evidence_id": "E1",
                "receipt_digest": "sha256:" + "a" * 64,
                "subject": "Laura", "predicate": "exact tax was", "value": display,
                "effective_date": period, "qualification": None,
                "document_version": "filed", "exact_excerpt": excerpt,
                "locator": self.receipt()["locator"], "support_mode": "explicit",
                "field_bindings": {"subject": {"start": 0, "end": 5},
                                   "predicate": {"start": 38, "end": 51},
                                   "value": {"start": 52, "end": 59}},
                "status": "not_governed_candidate", "admission_authority": False,
                "numeric": {"display": display, "decimal_value": decimal_value,
                            "kind": kind, "currency": "USD" if kind == "currency" else None,
                            "unit": "dollars" if kind == "currency" else "percentage points",
                            "entity": entity, "period": period, "precision": "exact"}}

    def authority(self):
        receipt = {"evidence_id": "E2", "receipt_digest": "sha256:" + "c" * 64,
                   "source_digest": "sha256:" + "d" * 64, "custody_valid": True,
                   "quote": "Treas. Reg. § 1.1362-6 requires consent.",
                   "locator": {"kind": "page_span", "page_start": 2, "page_end": 2}}
        node = {"schema_version": exact.AUTHORITY_NODE_SCHEMA, "authority_id": "U1",
                "requirement_id": "R_AUTH", "evidence_id": "E2",
                "receipt_digest": receipt["receipt_digest"],
                "citation": "Treas. Reg. § 1.1362-6", "proposition": "consent is required",
                "jurisdiction": "federal", "effective_date": "current",
                "authority_level": "regulation", "exact_excerpt": receipt["quote"],
                "locator": receipt["locator"], "status": "not_governed_candidate",
                "normative_authority_confirmed": False, "admission_authority": False}
        return node, {"E2": receipt}

    def test_numeric_inventory_preserves_display_spans_and_scale(self):
        text = "Tax was $18,486, ownership was 26%, and the year was 2024."
        rows = exact.extract_numeric_candidates(text)
        self.assertEqual([row["raw_text"] for row in rows], ["$18,486", "26%", "2024"])
        self.assertEqual([row["normalized_value"] for row in rows], ["18486", "26", "2024"])
        self.assertEqual([text[row["start"]:row["end"]] for row in rows],
                         ["$18,486", "26%", "2024"])

    def test_numeric_inventory_and_normalization_preserve_shorthand_scale(self):
        text = "Purchase was $350k and sale was $1.2M."
        rows = exact.extract_numeric_candidates(text)
        self.assertEqual([row["raw_text"] for row in rows], ["$350k", "$1.2M"])
        self.assertEqual([row["normalized_value"] for row in rows], ["350000", "1200000"])

    def test_numeric_inventory_does_not_attach_unbalanced_closing_parenthesis(self):
        text = "Amounts were $350k) and 26%) in the malformed source text."
        rows = exact.extract_numeric_candidates(text)
        self.assertEqual([row["raw_text"] for row in rows], ["$350k", "26%"])
        self.assertEqual([row["normalized_value"] for row in rows], ["350000", "26"])

    def test_period_domain_inventory_preserves_exact_multi_year_spans(self):
        text = "Header 2026\n\nAnnual schedule: 2022, 2023, and 2024.\n\nFooter"
        rows = exact.extract_period_domain_candidates(text)
        schedule = next(row for row in rows if row["periods"] == ["2022", "2023", "2024"])
        self.assertEqual(schedule["exact_excerpt"],
                         text[schedule["start"]:schedule["end"]])
        self.assertTrue(schedule["candidate_id"].startswith("period_candidate_"))
        self.assertNotIn("2026", schedule["periods"])

    def test_period_domain_inventory_is_syntactic_and_non_governing(self):
        rows = exact.extract_period_domain_candidates("Range endpoints: 2022 through 2024.")
        self.assertEqual(rows[0]["periods"], ["2022", "2024"])
        self.assertNotIn("status", rows[0])
        self.assertNotIn("admission_authority", rows[0])

    def test_numeric_atom_requires_exact_value_entity_period_and_currency(self):
        checked = exact.validate_numeric_atom(self.atom(), {"E1": self.receipt()})
        self.assertEqual(checked["numeric"]["decimal_value"], "18486")
        with self.assertRaisesRegex(ValueError, "disagree"):
            exact.validate_numeric_atom(self.atom(decimal_value="18485"), {"E1": self.receipt()})
        with self.assertRaisesRegex(ValueError, "currency"):
            broken = self.atom(); broken["numeric"]["currency"] = None
            exact.validate_numeric_atom(broken, {"E1": self.receipt()})

    def test_numeric_atom_can_only_be_built_from_an_exact_receipt_span(self):
        atom = exact.bind_numeric_atom(
            {"requirement_id": "R_TAX", "evidence_id": "E1", "subject": "Laura",
             "predicate": "exact tax was", "display": "$18,486", "kind": "currency",
             "currency": "USD", "unit": "dollars", "entity": "Laura", "period": "2024",
             "precision": "exact", "exact_excerpt": self.receipt()["quote"]},
            {"E1": self.receipt()})
        self.assertEqual(atom["numeric"]["decimal_value"], "18486")
        self.assertTrue(atom["atom_digest"].startswith("sha256:"))
        self.assertFalse(atom["admission_authority"])
        with self.assertRaisesRegex(ValueError, "receipt-bound"):
            exact.bind_numeric_atom(
                {"requirement_id": "R_TAX", "evidence_id": "E1", "subject": "Laura",
                 "predicate": "exact tax was", "display": "$18,486", "kind": "currency",
                 "currency": "USD", "unit": "dollars", "entity": "Laura", "period": "2024",
                 "precision": "exact", "exact_excerpt": "invented $18,486"},
                {"E1": self.receipt()})

    def test_general_evidence_atom_remains_source_bound_and_unresolved(self):
        atom = exact.bind_evidence_atom(
            {"requirement_id": "R_STATUS", "evidence_id": "E1", "subject": "Laura",
             "predicate": "owned", "value": "26%", "effective_date": "2024",
             "exact_excerpt": self.receipt()["quote"]},
            {"E1": self.receipt()})
        self.assertEqual(atom["value"], "26%")
        self.assertTrue(atom["atom_digest"].startswith("sha256:"))
        self.assertFalse(atom["admission_authority"])

    def test_task_numeric_parameter_is_not_matter_evidence_but_can_feed_derivation(self):
        prompt = "Assume the federal tax rate is 21%."
        parameter = exact.bind_task_numeric_parameter(
            prompt, {"requirement_id": "R_TAX", "display": "21%", "kind": "percentage",
                     "unit": "percentage points", "entity": "federal tax rate",
                     "period": "task assumption", "precision": "exact",
                     "parameter_role": "explicit_assumption"})
        self.assertFalse(parameter["governed_reliance_allowed"])
        income = exact.validate_numeric_atom(self.atom(atom_id="A_INCOME"), {"E1": self.receipt()})
        derivation = exact.build_exact_derivation(
            requirement_id="R_TAX", expression="income * rate / 100",
            variables={"income": "18486", "rate": "21"},
            input_bindings={"income": "A_INCOME", "rate": parameter["parameter_id"]},
            numeric_atoms={"A_INCOME": income}, task_parameters={parameter["parameter_id"]: parameter},
            output_unit="USD", entity="Laura", period="2024")
        self.assertEqual(derivation["input_kinds"]["rate"], "task_parameter")
        self.assertEqual(derivation["result"], "3882.06")
        with self.assertRaisesRegex(ValueError, "task parameter display"):
            exact.bind_task_numeric_parameter(
                prompt, {"requirement_id": "R_TAX", "display": "20%", "kind": "percentage",
                         "unit": "percentage points", "entity": "federal tax rate",
                         "period": "task assumption", "precision": "exact",
                         "parameter_role": "explicit_assumption"})

    def test_authority_candidate_cannot_self_confirm_or_admit(self):
        node, receipts = self.authority()
        checked = exact.validate_authority_node(node, receipts)
        self.assertFalse(checked["normative_authority_confirmed"])
        with self.assertRaisesRegex(ValueError, "self-confirm"):
            exact.validate_authority_node({**node, "normative_authority_confirmed": True}, receipts)
        with self.assertRaisesRegex(ValueError, "admission"):
            exact.validate_authority_node({**node, "admission_authority": True}, receipts)

    def test_controlled_authority_must_match_official_source_metadata(self):
        node, receipts = self.authority()
        receipts["E2"]["source"] = {
            "uri": "https://www.ecfr.gov/api/versioner/v1/full/2019-02-19/title-26.xml",
            "official_authority": {"official": True, "jurisdiction": "federal",
                                   "effective_on": "2019-02-19",
                                   "authority_level": "regulation",
                                   "canonical_citations": ["Treas. Reg. § 1.1362-6"]}}
        node["effective_date"] = "2019-02-19"
        self.assertEqual(exact.validate_authority_node(node, receipts)["authority_level"],
                         "regulation")
        with self.assertRaisesRegex(ValueError, "controlled source metadata"):
            exact.validate_authority_node({**node, "authority_level": "statute"}, receipts)
        receipts["E2"]["source"]["official_authority"]["canonical_citations"] = ["26 CFR 1.1362-6"]
        with self.assertRaisesRegex(ValueError, "outside the controlled"):
            exact.validate_authority_node(node, receipts)

    def plan(self):
        return exact.compile_requirement_plan(
            "Calculate the exact 2024 tax and cite the controlling regulation.",
            [{"slot_id": "R_TAX", "slot_type": "exact_value",
              "description": "Exact 2024 tax", "required_object_kinds": ["derivation_node"],
              "expected_periods": ["2024"], "output_format": "USD"},
             {"slot_id": "R_AUTH", "slot_type": "controlling_authority",
              "description": "Controlling regulation Treas. Reg. § 1.1362-6",
              "required_object_kinds": ["authority_node"]},
             {"slot_id": "R_OUTPUT", "slot_type": "output_structure",
              "description": "Console response", "required_object_kinds": []}],
            output_type="message_in_console")

    def test_requirement_compiler_is_prompt_bound_and_forbids_gold(self):
        plan = self.plan()
        self.assertEqual(plan["source_basis"], "task_prompt_only_no_rubric_or_gold")
        self.assertFalse(plan["admission_authority"])
        with self.assertRaisesRegex(ValueError, "rubric"):
            exact.compile_requirement_plan("Task", [{"slot_id": "R", "slot_type": "exact_value",
                "description": "x", "required_object_kinds": ["evidence_atom"],
                "rubric": "hidden"}], output_type="message_in_console")

    def test_readiness_separates_candidate_coverage_from_governed_coverage(self):
        plan = exact.bind_requirement_objects(self.plan(),
            {"R_TAX": ["D1"], "R_AUTH": ["U1"]})
        derivation = {"derivation_id": "D1", "requirement_id": "R_TAX"}
        authority, receipts = self.authority()
        authority = exact.validate_authority_node(authority, receipts)
        screen = exact.screen_authority_applicability(
            "Controlling regulation Treas. Reg. § 1.1362-6", authority)
        candidate = exact.assess_requirement_readiness(
            plan, authority_nodes=[authority], derivations=[derivation],
            authority_screens=[screen])
        self.assertEqual(candidate["candidate_coverage"], 3)
        self.assertEqual(candidate["governed_coverage"], 1)
        self.assertFalse(candidate["executor_ready"])
        governed = exact.assess_requirement_readiness(
            plan, authority_nodes=[authority], derivations=[derivation],
            authority_screens=[screen],
            governed_object_ids=["D1", "U1", screen["screen_id"]])
        self.assertTrue(governed["executor_ready"])

    def test_value_by_period_requires_every_declared_period(self):
        plan = exact.compile_requirement_plan(
            "Report 2022 and 2023 values.",
            [{"slot_id": "R_SERIES", "slot_type": "value_by_period",
              "description": "Annual values", "required_object_kinds": ["evidence_atom"],
              "expected_periods": ["2022", "2023"]},
             {"slot_id": "R_OUTPUT", "slot_type": "output_structure",
              "description": "Console", "required_object_kinds": []}],
            output_type="message_in_console")
        plan = exact.bind_requirement_objects(plan, {"R_SERIES": ["A_2022"]})
        atom = {"atom_id": "A_2022", "requirement_id": "R_SERIES",
                "numeric": {"period": "2022"}}
        receipt = {**self.receipt(), "quote": "Annual schedule: 2022 and 2023."}
        domain = exact.bind_period_domain(
            {"requirement_id": "R_SERIES", "evidence_id": "E1",
             "exact_excerpt": receipt["quote"], "periods": ["2022", "2023"]},
            {"E1": receipt})
        readiness = exact.assess_requirement_readiness(
            plan, evidence_atoms=[atom], period_domains=[domain])
        series = next(row for row in readiness["slots"] if row["slot_id"] == "R_SERIES")
        self.assertEqual(series["state"], "gap")
        self.assertEqual(series["missing_periods"], ["2023"])

    def test_value_by_period_requires_one_source_bound_period_domain(self):
        plan = exact.compile_requirement_plan(
            "Report every annual value.",
            [{"slot_id": "R_SERIES", "slot_type": "value_by_period",
              "description": "Every annual value", "required_object_kinds": ["evidence_atom"],
              "expected_periods": ["each affected year"]},
             {"slot_id": "R_OUTPUT", "slot_type": "output_structure",
              "description": "Console", "required_object_kinds": []}],
            output_type="message_in_console")
        atom = {"atom_id": "A_2022", "requirement_id": "R_SERIES",
                "numeric": {"period": "2022"}}
        plan = exact.bind_requirement_objects(plan, {"R_SERIES": ["A_2022"]})
        no_domain = exact.assess_requirement_readiness(plan, evidence_atoms=[atom])
        series = next(row for row in no_domain["slots"] if row["slot_id"] == "R_SERIES")
        self.assertEqual(series["state"], "gap")
        self.assertTrue(series["period_domain_invalid"])
        receipt = {**self.receipt(), "quote": "Schedule years: 2022, 2023."}
        with self.assertRaisesRegex(ValueError, "every period"):
            exact.bind_period_domain(
                {"requirement_id": "R_SERIES", "evidence_id": "E1",
                 "exact_excerpt": receipt["quote"], "periods": ["2022", "2024"]},
                {"E1": receipt})

    def test_authority_applicability_rejects_related_but_different_citation(self):
        node, receipts = self.authority()
        node = exact.validate_authority_node(node, receipts)
        matched = exact.screen_authority_applicability(
            "Apply Treas. Reg. § 1.1362-6", node)
        self.assertEqual(matched["outcome"], "exact_reference_match_candidate")
        self.assertTrue(matched["human_review_required"])
        mismatch = exact.screen_authority_applicability(
            "Apply Rev. Proc. 2013-30", node)
        self.assertEqual(mismatch["outcome"], "citation_mismatch")
        with self.assertRaisesRegex(ValueError, "cannot override"):
            exact.bind_independent_authority_review(
                "Apply Rev. Proc. 2013-30", node, supports_candidate=True,
                review_record_digest="sha256:" + "e" * 64,
                reviewer_route="openai/gpt-5.6-sol")

    def test_independent_authority_review_remains_non_governing(self):
        node, receipts = self.authority()
        node = exact.validate_authority_node(node, receipts)
        review = exact.bind_independent_authority_review(
            "Identify the controlling consent authority", node,
            supports_candidate=True, review_record_digest="sha256:" + "e" * 64,
            reviewer_route="openai/gpt-5.6-sol")
        self.assertEqual(review["outcome"], "independent_review_supports_candidate")
        self.assertFalse(review["legal_applicability_confirmed"])
        self.assertTrue(review["human_review_required"])
        self.assertFalse(review["admission_authority"])

    def test_independent_authority_support_is_bound_only_as_candidate(self):
        node, receipts = self.authority()
        node = exact.validate_authority_node(node, receipts)
        review = exact.bind_independent_authority_review(
            "Identify the controlling consent authority", node,
            supports_candidate=True, review_record_digest="sha256:" + "e" * 64,
            reviewer_route="openai/gpt-5.6-sol")
        plan = exact.bind_candidate_objects(
            self.plan(), authority_nodes=[node], authority_screens=[review])
        authority_slot = next(row for row in plan["slots"] if row["slot_id"] == "R_AUTH")
        self.assertEqual(authority_slot["object_ids"], ["U1"])
        readiness = exact.assess_requirement_readiness(
            plan, authority_nodes=[node], authority_screens=[review])
        authority_row = next(row for row in readiness["slots"] if row["slot_id"] == "R_AUTH")
        self.assertEqual(authority_row["state"], "covered_candidate_not_governed")
        self.assertFalse(review["legal_applicability_confirmed"])
        self.assertFalse(readiness["executor_ready"])

    def test_rejected_independent_authority_is_not_bound(self):
        node, receipts = self.authority()
        node = exact.validate_authority_node(node, receipts)
        review = exact.bind_independent_authority_review(
            "Identify the controlling consent authority", node,
            supports_candidate=False, review_record_digest="sha256:" + "e" * 64,
            reviewer_route="openai/gpt-5.6-sol")
        plan = exact.bind_candidate_objects(
            self.plan(), authority_nodes=[node], authority_screens=[review])
        authority_slot = next(row for row in plan["slots"] if row["slot_id"] == "R_AUTH")
        self.assertEqual(authority_slot["object_ids"], [])

    def test_review_queue_attributes_authority_and_period_gaps(self):
        authority_slot = {"slot_id": "R_AUTH", "slot_type": "controlling_authority"}
        gap = {"state": "gap", "eligible_object_ids": [], "period_domain_invalid": False,
               "missing_periods": []}
        task_runs = [{"authority_screens": [{"requirement_id": "R_AUTH",
                                              "outcome": "independent_review_rejects_candidate"}]}]
        self.assertEqual(
            review._failure_layer(authority_slot, [gap], task_runs, set()),
            "authority_responsiveness_not_qualified")
        period_slot = {"slot_id": "R_SERIES", "slot_type": "value_by_period"}
        period_gap = {**gap, "period_domain_invalid": True}
        self.assertEqual(
            review._failure_layer(period_slot, [period_gap], [{}], set()),
            "period_inventory_missing")
        inventory_run = {
            "stage_status": {"period_extraction": {
                "inventory_candidate_count_by_requirement": {"R_SERIES": 3}}}}
        self.assertEqual(
            review._failure_layer(period_slot, [period_gap], [inventory_run], set()),
            "period_inventory_selector_rejected")

    def test_period_retrieval_scans_all_bm25_matches_without_rank_cap(self):
        class FakeIndex:
            def __init__(self):
                self.sections = [object(), object(), object()]
                self.doc_meta = {"one": {}, "two": {}}
                self.calls = []

            def search(self, query, max_documents, max_sections):
                self.calls.append((query, max_documents, max_sections))
                hits = []
                for rank in (1, 2):
                    text = f"Annual schedule 202{rank} and 202{rank + 1}"
                    hits.append({"rank": rank, "score": 1.0 / rank,
                                 "section": {
                                     "uri": f"source-{rank}", "id": f"section-{rank}",
                                     "text": text, "text_digest": exact.digest(text),
                                     "representation_digest": exact.digest(f"rep-{rank}"),
                                     "page_start": rank, "page_end": rank,
                                     "source": {"uri": f"source-{rank}",
                                                "content_digest": exact.digest(f"source-{rank}"),
                                                "media_type": "text/plain"}}})
                return hits

        index = FakeIndex()
        slots = [{"slot_id": "R_SERIES", "slot_type": "value_by_period",
                  "description": "Annual schedule", "search_queries": ["schedule", "annual"]}]
        receipts, audit = stage_runner._unbounded_period_retrieval(slots, index)
        self.assertEqual(len(receipts), 2)
        self.assertEqual(audit[0]["period_candidate_section_count"], 2)
        self.assertIsNone(audit[0]["retrieval_limit"])
        self.assertTrue(all(call[1:] == (2, 3) for call in index.calls))

    def test_authority_slot_needs_qualified_applicability_screen(self):
        plan = exact.bind_requirement_objects(self.plan(), {"R_AUTH": ["U1"]})
        node, receipts = self.authority()
        node = exact.validate_authority_node(node, receipts)
        pending = exact.assess_requirement_readiness(plan, authority_nodes=[node])
        authority_row = next(row for row in pending["slots"] if row["slot_id"] == "R_AUTH")
        self.assertEqual(authority_row["state"], "gap")
        screen = exact.screen_authority_applicability(
            "Controlling regulation Treas. Reg. § 1.1362-6", node)
        covered = exact.assess_requirement_readiness(
            plan, authority_nodes=[node], authority_screens=[screen])
        authority_row = next(row for row in covered["slots"] if row["slot_id"] == "R_AUTH")
        self.assertEqual(authority_row["state"], "covered_candidate_not_governed")

    def test_derivation_requires_every_variable_to_match_a_bound_atom(self):
        income = exact.validate_numeric_atom(
            self.atom(atom_id="A_INCOME", display="$18,486", decimal_value="18486"),
            {"E1": self.receipt()})
        rate = exact.validate_numeric_atom(
            self.atom(atom_id="A_RATE", display="26%", decimal_value="26",
                      kind="percentage"), {"E1": self.receipt()})
        atoms = {"A_INCOME": income, "A_RATE": rate}
        value = exact.build_exact_derivation(
            requirement_id="R_TAX", expression="income * rate / 100",
            variables={"income": "18486", "rate": "26"},
            input_bindings={"income": "A_INCOME", "rate": "A_RATE"},
            numeric_atoms=atoms, output_unit="USD", entity="Laura", period="2024")
        self.assertEqual(value["result"], "4806.36")
        self.assertFalse(value["admission_authority"])
        self.assertEqual(exact.validate_exact_derivation(value, atoms)["result"], "4806.36")
        with self.assertRaisesRegex(ValueError, "do not recompute"):
            exact.validate_exact_derivation({**value, "result": "4806.35"}, atoms)
        with self.assertRaisesRegex(ValueError, "disagrees"):
            exact.build_exact_derivation(
                requirement_id="R_TAX", expression="income * rate / 100",
                variables={"income": "18485", "rate": "26"},
                input_bindings={"income": "A_INCOME", "rate": "A_RATE"},
                numeric_atoms=atoms, output_unit="USD", entity="Laura", period="2024")
        tampered = {**income, "numeric": {**income["numeric"], "decimal_value": "18485"}}
        with self.assertRaisesRegex(ValueError, "not a numeric evidence atom"):
            exact.build_exact_derivation(
                requirement_id="R_TAX", expression="income * rate / 100",
                variables={"income": "18485", "rate": "26"},
                input_bindings={"income": "A_INCOME", "rate": "A_RATE"},
                numeric_atoms={"A_INCOME": tampered, "A_RATE": rate},
                output_unit="USD", entity="Laura", period="2024")

    def test_derivation_can_bind_explicit_cross_slot_dependencies(self):
        income = exact.validate_numeric_atom(
            self.atom(atom_id="A_INCOME", requirement_id="R_INCOME"),
            {"E1": self.receipt()})
        rate = exact.validate_numeric_atom(
            self.atom(atom_id="A_RATE", requirement_id="R_RATE", display="26%",
                      decimal_value="26", kind="percentage"), {"E1": self.receipt()})
        value = exact.build_exact_derivation(
            requirement_id="R_TAX", expression="income * rate / 100",
            variables={"income": "18486", "rate": "26"},
            input_bindings={"income": "A_INCOME", "rate": "A_RATE"},
            input_requirement_ids={"income": "R_INCOME", "rate": "R_RATE"},
            numeric_atoms={"A_INCOME": income, "A_RATE": rate},
            output_unit="USD", entity="Laura", period="2024")
        self.assertEqual(value["input_requirement_ids"],
                         {"income": "R_INCOME", "rate": "R_RATE"})
        with self.assertRaisesRegex(ValueError, "declared source requirement"):
            exact.build_exact_derivation(
                requirement_id="R_TAX", expression="income * rate / 100",
                variables={"income": "18486", "rate": "26"},
                input_bindings={"income": "A_INCOME", "rate": "A_RATE"},
                input_requirement_ids={"income": "R_TAX", "rate": "R_RATE"},
                numeric_atoms={"A_INCOME": income, "A_RATE": rate},
                output_unit="USD", entity="Laura", period="2024")

    def test_numeric_gate_rejects_unbound_and_accepts_exact_atom_binding(self):
        tax_atom = exact.validate_numeric_atom(self.atom(), {"E1": self.receipt()})
        claim = {"id": "C1", "requirement_id": "R_TAX", "status": "unresolved",
                 "statement": "The exact 2024 tax is $18,486.",
                 "numeric_mentions": [], "authority_mentions": []}
        failed = exact.numeric_binding_gate(
            claim, numeric_atoms={"A_TAX": tax_atom}, derivations={}, authority_nodes={})
        self.assertFalse(failed["proposer_allowed"])
        self.assertIn("unbound_material_number", failed["reasons"])
        statement = claim["statement"]
        year_atom = exact.validate_numeric_atom(
            self.atom(atom_id="A_YEAR", display="2024", decimal_value="2024",
                      kind="year"), {"E1": self.receipt()})
        mentions = []
        for raw, object_id in (("2024", "A_YEAR"), ("$18,486", "A_TAX")):
            start = statement.index(raw)
            mentions.append({"start": start, "end": start + len(raw), "object_id": object_id})
        passed = exact.numeric_binding_gate(
            {**claim, "numeric_mentions": mentions},
            numeric_atoms={"A_TAX": tax_atom, "A_YEAR": year_atom},
            derivations={}, authority_nodes={})
        self.assertTrue(passed["proposer_allowed"])
        self.assertFalse(passed["admission_authority"])

    def test_numeric_gate_allows_section_numbers_only_through_authority_binding(self):
        node, receipts = self.authority()
        node = exact.validate_authority_node(node, receipts)
        statement = "Treas. Reg. § 1.1362-6 requires consent."
        start = 0
        claim = {"id": "C2", "requirement_id": "R_AUTH", "status": "unresolved",
                 "statement": statement, "numeric_mentions": [],
                 "authority_mentions": [{"start": start, "end": len(node["citation"]),
                                          "object_id": "U1"}]}
        gate = exact.numeric_binding_gate(
            claim, numeric_atoms={}, derivations={}, authority_nodes={"U1": node})
        self.assertTrue(gate["proposer_allowed"])

    def test_numeric_gate_never_accepts_admission_on_candidate_claim(self):
        claim = {"id": "C3", "requirement_id": "R_TAX", "status": "unresolved",
                 "statement": "No number is asserted.", "numeric_mentions": [],
                 "authority_mentions": [], "admission": "admitted"}
        gate = exact.numeric_binding_gate(
            claim, numeric_atoms={}, derivations={}, authority_nodes={})
        self.assertFalse(gate["proposer_allowed"])
        self.assertIn("candidate_claim_cannot_carry_admission", gate["reasons"])

    def test_candidate_readiness_runner_sanitizes_private_content(self):
        bundle = {
            "task_prompt": "Report the exact 2024 tax.",
            "output_type": "message_in_console",
            "slots": [
                {"slot_id": "R_TAX", "slot_type": "exact_value",
                 "description": "Exact 2024 tax",
                 "required_object_kinds": ["evidence_atom"],
                 "expected_periods": ["2024"], "output_format": "USD"},
                {"slot_id": "R_OUTPUT", "slot_type": "output_structure",
                 "description": "Console response", "required_object_kinds": []},
            ],
            "receipts": [self.receipt()],
            "numeric_atom_payloads": [
                {"requirement_id": "R_TAX", "evidence_id": "E1", "subject": "Laura",
                 "predicate": "exact tax was", "display": "$18,486", "kind": "currency",
                 "currency": "USD", "unit": "dollars", "entity": "Laura",
                 "period": "2024", "precision": "exact",
                 "exact_excerpt": self.receipt()["quote"]},
            ],
            "assignments": {},
        }
        # Discover the content-addressed atom ID first, as a private harness would.
        atom = exact.bind_numeric_atom(bundle["numeric_atom_payloads"][0], {"E1": self.receipt()})
        bundle["assignments"] = {"R_TAX": [atom["atom_id"]]}
        report = runner.build_candidate_readiness(bundle)
        serialized = str(report)
        self.assertEqual(report["candidate_coverage"], 2)
        self.assertEqual(report["governed_coverage"], 1)
        self.assertFalse(report["executor_ready"])
        self.assertNotIn("18,486", serialized)
        self.assertNotIn("Report the exact", serialized)
        self.assertNotIn("Laura", serialized)
        self.assertFalse(report["admission_authority"])


if __name__ == "__main__":
    unittest.main()

import unittest
import json
from pathlib import Path
import tempfile
import zipfile

from pp_eval.finance_e2e_v2 import (
    ATOM_SCHEMA,
    apply_type_assignments,
    atom_to_observed_fact,
    execution_gate,
    executor_qualification,
    legacy_working_set_preflight,
    requirement_completeness,
    retrieve_receipts,
    pdf_pages_to_receipts,
    fresh_task_audit,
    validate_derived_calculation,
    validate_finance_atom,
    validate_requirements,
    workbook_index_to_receipts,
)
from pp_eval.finance_gateway import audit_receipts
from pp_eval.finance_workflow_private import (
    ATOM_OUTPUT_SCHEMA,
    materialize_compiler_data_room,
    materialize_governed_overlay,
    select_data_room_members,
)
from run_finance_e2e_v2 import audit_executor_qualification, normalized_cell


def atom():
    return {
        "schema_version": ATOM_SCHEMA,
        "atom_id": "atom_001",
        "requirement_id": "req_1",
        "evidence_id": "ev_1",
        "receipt_digest": "sha256:receipt",
        "subject": "FY2025 revenue",
        "predicate": "equals",
        "value": "100",
        "support_mode": "explicit",
        "locator": "Workbook.xlsx#Sheet1!B2",
        "exact_source_value": 100,
        "unit": "USDm",
        "currency": "USD",
        "period": "FY2025",
    }


def receipts():
    return {"ev_1": {
        "receipt_digest": "sha256:receipt",
        "locator": "Workbook.xlsx#Sheet1!B2",
        "source_value": 100,
        "unit": "USDm",
        "currency": "USD",
        "period": "FY2025",
    }}


class FinanceAtomTests(unittest.TestCase):
    def test_atom_output_schema_can_emit_validator_required_version(self):
        self.assertEqual(ATOM_OUTPUT_SCHEMA["required"], ["evidence_ids"])
        self.assertNotIn("atoms", ATOM_OUTPUT_SCHEMA["properties"])

    def test_workbook_index_becomes_deterministic_receipts(self):
        rows = workbook_index_to_receipts(
            artifact="filesystem/model.xlsx", source_sha256="sha256:abc",
            sheets=[{"sheet": "Model", "cells": [
                {"cell": "B2", "value": 100},
                {"cell": "B3", "value": 110, "formula": "B2*1.1"},
            ]}],
        )
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1]["value_semantics"], "cached_formula_result")
        self.assertEqual(rows[1]["formula"], "B2*1.1")
        self.assertTrue(rows[1]["receipt_digest"].startswith("sha256:"))

    def test_deterministic_receipt_retrieval_uses_local_labels(self):
        rows = workbook_index_to_receipts(
            artifact="filesystem/model.xlsx", source_sha256="sha256:abc",
            sheets=[{"sheet": "Model", "cells": [
                {"cell": "A2", "value": "Revenue"},
                {"cell": "B2", "value": 100},
                {"cell": "A9", "value": "Debt"},
                {"cell": "B9", "value": 40},
            ]}],
        )
        result = retrieve_receipts(
            [{"requirement_id": "req_revenue", "requirement": "Use reported revenue"}], rows,
            limit_per_requirement=2)
        self.assertTrue(result["req_revenue"])
        self.assertIn("!B2", {row["locator"][-3:] for row in result["req_revenue"]})

    def test_pdf_pages_become_exact_page_receipts(self):
        rows = pdf_pages_to_receipts(
            artifact="filesystem/report.pdf", source_sha256="sha256:abc",
            pages=["Revenue was $100 million.\n\nDebt was $40 million."],
        )
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["locator"], "filesystem/report.pdf#page=1&block=1")
        self.assertEqual(rows[0]["quote"], "Revenue was $100 million.")

    def test_requirements_forbid_hidden_material(self):
        frozen = validate_requirements([{
            "requirement_id": "req_1", "kind": "calculation",
            "requirement": "Calculate sensitivity",
        }])
        self.assertEqual(frozen["count"], 1)
        with self.assertRaisesRegex(ValueError, "hidden"):
            validate_requirements([{
                "requirement_id": "req_1", "kind": "output",
                "requirement": "Return result", "gold": "42",
            }])

    def test_derived_calculation_requires_formula_dependencies_and_units(self):
        row = {"record_type": "derived_calculation", "formula": "a/b",
               "dependency_ids": ["a", "b"], "unit": "%"}
        self.assertIs(validate_derived_calculation(row, {"a", "b"}), row)
        row["dependency_ids"] = ["missing"]
        with self.assertRaisesRegex(ValueError, "unknown"):
            validate_derived_calculation(row, {"a", "b"})

    def test_atom_requires_exact_receipt_binding(self):
        self.assertEqual(validate_finance_atom(atom(), receipts())["atom_id"], "atom_001")
        bad = atom()
        bad["currency"] = "EUR"
        with self.assertRaisesRegex(ValueError, "currency"):
            validate_finance_atom(bad, receipts())

    def test_inferred_atom_cannot_become_observed_fact(self):
        bad = atom()
        bad["support_mode"] = "inferred"
        with self.assertRaisesRegex(ValueError, "explicit"):
            atom_to_observed_fact(bad, 1)

    def test_type_assignment_cannot_rewrite_record(self):
        fact = atom_to_observed_fact(atom(), 1)
        value = {"assignments": [{"record_id": fact["id"],
                                    "record_type": "observed_fact",
                                    "statement": "rewrite"}]}
        with self.assertRaisesRegex(ValueError, "only assign"):
            apply_type_assignments([fact], value)


class FinanceGateTests(unittest.TestCase):
    def test_legacy_untyped_gap_fails_closed(self):
        result = legacy_working_set_preflight({
            "task_id": "task_1",
            "residual_gaps": [{"gap_id": "gap_1", "description": "method unclear"}],
        })
        self.assertEqual(result["decision"], "block")
        self.assertEqual(result["blocker_count"], 1)
        self.assertNotIn("description", result["blockers"][0])

    def test_explicit_immaterial_bound_gap_may_pass(self):
        result = legacy_working_set_preflight({
            "task_id": "task_1",
            "residual_gaps": [{"gap_id": "gap_1", "kind": "immaterial_residual",
                               "material": False, "requirement_id": "req_1"}],
        })
        self.assertEqual(result["decision"], "allow")

    def test_material_gap_blocks_completeness(self):
        result = requirement_completeness(
            [{"requirement_id": "req_1"}], [],
            [{"gap_id": "gap_1", "requirement_id": "req_1",
              "kind": "unresolved_methodology", "material": True}],
        )
        self.assertFalse(result["complete"])
        self.assertEqual(result["requirements"][0]["state"], "material_gap")

    def test_output_requirement_may_be_covered_by_dependency_audit(self):
        requirements = [{"requirement_id": "output_1", "kind": "output",
                         "requirement": "Calculate the requested output"}]
        result = requirement_completeness(
            requirements, [], [], covered_requirement_ids={"output_1"})
        self.assertTrue(result["complete"])

    def test_fresh_task_audit_excludes_consumed_without_hidden_material(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            used = root / "used"
            used.mkdir()
            (used / "manifest.json").write_text(json.dumps({
                "world_id": "world1", "task_id": "task_used",
                "agent_model": "executor/a", "status": "completed"}))
            tasks = [
                {"world_id": "world1", "task_id": "task_used", "task_name": "Used",
                 "domain": "Investment Banking", "expected_output": "message_in_console",
                 "prompt": "public", "rubric": "hidden", "gold_response": "hidden"},
                {"world_id": "world1", "task_id": "task_fresh", "task_name": "Fresh",
                 "domain": "Investment Banking", "expected_output": "edit_existing_sheet",
                 "prompt": "public", "rubric": "hidden", "gold_response": "hidden"},
            ]
            result = fresh_task_audit(
                task_rows=tasks, world_id="world1", manifest_roots=[root],
                executor_model="executor/a")
            self.assertEqual(result["candidate_count"], 1)
            self.assertEqual(result["excluded_count"], 1)
            self.assertFalse(result["hidden_material_retained"])
            self.assertNotIn("rubric", json.dumps(result))

    def test_execution_gate_fails_closed(self):
        fact = atom_to_observed_fact(atom(), 1)
        result = execution_gate(
            records=[fact], critic_verdicts={fact["id"]: {"verdict": "supported"}},
            completeness={"complete": True}, conflicts=[],
            source_bindings_complete=True, telemetry_complete=True,
            requested_output_leakage=False,
        )
        self.assertEqual(result["decision"], "allow")
        blocked = execution_gate(
            records=[fact], critic_verdicts={fact["id"]: {"verdict": "supported"}},
            completeness={"complete": False}, conflicts=[],
            source_bindings_complete=True, telemetry_complete=True,
            requested_output_leakage=False,
        )
        self.assertEqual(blocked["decision"], "block")

    def test_executor_qualification_uses_frozen_denominator(self):
        cells = [{"terminal_telemetry_complete": True,
                  "workbook_finalized": True,
                  "required_outputs_valid": True,
                  "unauthorized_source_access": False} for _ in range(5)]
        cells.append({"terminal_telemetry_complete": True,
                      "workbook_finalized": False,
                      "required_outputs_valid": False,
                      "failure_kind": "transport",
                      "unauthorized_source_access": False})
        result = executor_qualification(cells)
        self.assertEqual(result["decision"], "allow")
        cells[0]["terminal_telemetry_complete"] = False
        self.assertEqual(executor_qualification(cells)["decision"], "block")

    def test_executor_qualification_blocks_infrastructure_invalid_cell(self):
        cells = [{"terminal_telemetry_complete": True,
                  "workbook_finalized": True, "required_outputs_valid": True,
                  "unauthorized_source_access": False} for _ in range(6)]
        cells[0]["infrastructure_invalid"] = True
        result = executor_qualification(cells)
        self.assertEqual(result["decision"], "block")
        self.assertEqual(result["reason"], "infrastructure_invalid_cells")

    def test_normalized_qualification_cell_requires_final_artifact(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary)
            output = run_dir / "output"
            output.mkdir()
            with zipfile.ZipFile(output / "neutral_final.zip", "w") as archive:
                archive.writestr(
                    "filesystem/04_Models/Merger-Acquisition Analysis/"
                    "Merger Model - Barings BDC vF.xlsx", b"xlsx")
            result = {
                "run_id": "run_1", "run_dir": str(run_dir),
                "task_id": "task_9ba58a6197114140877a1df1754d2993",
                "agent_model": "inclusionai/ling-3.0-flash-fin",
                "status": "completed", "watchdog_timeout": False,
                "elapsed_seconds": 1,
                "telemetry": {"status": "complete", "calls": 1,
                              "total_tokens": 2, "known_cost_usd": 0,
                              "providers": ["novita"],
                              "no_fallback_observed": True},
            }
            cell = normalized_cell(result)
            self.assertTrue(cell["workbook_finalized"])
            self.assertTrue(cell["required_outputs_valid"])

    def test_normalized_cell_detects_host_suspend_gap(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary)
            (run_dir / "launcher.log").write_text(
                "Request timed out. time taken=38590.25 seconds\n"
                "Connection error., after 2 attempts\n")
            result = {"run_id": "run_1", "run_dir": str(run_dir),
                      "task_id": "task_9ba58a6197114140877a1df1754d2993",
                      "agent_model": "inclusionai/ling-3.0-flash-fin",
                      "status": "infrastructure_abort_or_incomplete",
                      "watchdog_timeout": False, "elapsed_seconds": 1,
                      "telemetry": {"status": "complete", "calls": 2}}
            cell = normalized_cell(result)
            self.assertEqual(cell["failure_kind"], "host_suspend_or_clock_gap")
            self.assertTrue(cell["infrastructure_invalid"])

    def test_executor_audit_preserves_source_and_invalidates_suspend_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run = root / "cell-1"
            run.mkdir()
            (run / "launcher.log").write_text("time taken=38590.25 seconds\n")
            manifest = {
                "run_id": "cell-1", "task_id": "task_9ba58a6197114140877a1df1754d2993",
                "agent_model": "inclusionai/ling-3.0-flash-fin",
                "status": "infrastructure_abort_or_incomplete", "watchdog_timeout": False,
                "telemetry": {"status": "complete", "calls": 1},
            }
            (run / "manifest.json").write_text(json.dumps(manifest))
            source = {"status": "running", "scheduled_cells": 6,
                      "cells": [{"manifest": str(run / "manifest.json")}]}
            (root / "report.json").write_text(json.dumps(source))
            result = audit_executor_qualification(root, root / "audit.json")
            self.assertEqual(result["qualification_decision"], "invalid_root")
            self.assertEqual(result["infrastructure_invalid_cells"], 1)

    def test_executor_audit_recomputes_allow_for_frozen_model_and_provider(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cells = []
            for ordinal in range(1, 7):
                run = root / f"cell-{ordinal}"
                output = run / "output"
                output.mkdir(parents=True)
                with zipfile.ZipFile(output / "neutral_final.zip", "w") as archive:
                    archive.writestr(
                        "filesystem/04_Models/Merger-Acquisition Analysis/"
                        "Merger Model - Barings BDC vF.xlsx", b"xlsx")
                (run / "launcher.log").write_text("")
                manifest = {
                    "run_id": f"cell-{ordinal}",
                    "task_id": "task_9ba58a6197114140877a1df1754d2993",
                    "agent_model": "openai/gpt-5.6-luna",
                    "status": "completed", "watchdog_timeout": False,
                    "telemetry": {"status": "complete", "calls": 1,
                                  "total_tokens": 2, "known_cost_usd": 0.01,
                                  "providers": ["openai"],
                                  "no_fallback_observed": True},
                }
                (run / "manifest.json").write_text(json.dumps(manifest))
                cells.append({"manifest": str(run / "manifest.json")})
            source = {"status": "completed", "scheduled_cells": 6,
                      "executor_model": "openai/gpt-5.6-luna",
                      "executor_provider": "openai", "cells": cells}
            (root / "report.json").write_text(json.dumps(source))
            result = audit_executor_qualification(root, root / "audit.json")
            self.assertEqual(result["qualification_decision"], "allow")
            self.assertEqual(result["qualification"]["completed"], 6)

    def test_gateway_receipt_audit_requires_exact_route_and_cost(self):
        route = {"model": "model/a", "provider": "provider-a", "reasoning": "low"}
        row = {
            "terminal": True, "status": "ok", "requested_model": "model/a",
            "resolved_model": "model/a", "requested_provider": "provider-a",
            "resolved_provider": "provider-a", "fallback_used": False,
            "model_attempt_count": 1, "provider_attempt_count": 1,
            "input_tokens": 10, "output_tokens": 2, "cost_usd": 0.01,
        }
        self.assertEqual(audit_receipts([row], route, 1)["decision"], "allow")
        row["resolved_provider"] = "provider-b"
        self.assertEqual(audit_receipts([row], route, 1)["decision"], "block")

    def test_governed_overlay_excludes_full_data_room(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evidence = root / "evidence"
            target_path = "filesystem/04_Models/target.xlsx"
            (evidence / target_path).parent.mkdir(parents=True)
            (evidence / target_path).write_bytes(b"pristine")
            (evidence / "filesystem/source-secret.xlsx").parent.mkdir(parents=True, exist_ok=True)
            (evidence / "filesystem/source-secret.xlsx").write_bytes(b"do-not-copy")
            receipt = {"evidence_id": "ev1", "receipt_digest": "sha256:r",
                       "locator": "source#S!A1", "source_value": 1}
            record = {"id": "r1", "requirement_id": "req1",
                      "record_type": "observed_fact", "statement": "Revenue equals 1",
                      "evidence_ids": ["ev1"], "status": "supported"}
            destination = root / "overlay"
            manifest = materialize_governed_overlay(
                evidence_root=evidence, destination=destination,
                task={"task_id": "task1", "prompt": "do work"},
                requirements=[{"requirement_id": "req1", "kind": "input",
                               "requirement": "use revenue"}],
                records=[record], receipts={"ev1": receipt},
                execution_receipt={"decision": "allow"},
                target_artifacts=[target_path])
            self.assertFalse(manifest["full_data_room_present"])
            self.assertTrue((destination / target_path).is_file())
            self.assertFalse((destination / "filesystem/source-secret.xlsx").exists())

    def test_data_room_selection_is_global_deterministic_and_task_scoped(self):
        members = ["filesystem/model.xlsx", "filesystem/FDUS/FDUS_10Q_09.30.2025.pdf",
                   "filesystem/WHF/WHF_10K_12.31.2024.pdf"]
        selected = select_data_room_members(
            members, "Use FDUS filings for the September 2025 account")
        self.assertIn("filesystem/model.xlsx", selected)
        self.assertIn("filesystem/FDUS/FDUS_10Q_09.30.2025.pdf", selected)
        self.assertNotIn("filesystem/WHF/WHF_10K_12.31.2024.pdf", selected)

    def test_data_room_selection_excludes_archive_workbooks(self):
        selected = select_data_room_members([
            "filesystem/Model/Archive/model-v1.xlsx",
            "filesystem/Model/model-vF.xlsx",
        ], "edit the model")
        self.assertEqual(selected, ["filesystem/Model/model-vF.xlsx"])

    def test_compiler_data_room_binds_frozen_world_archive(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            world = root / "world.zip"
            with zipfile.ZipFile(world, "w") as archive:
                archive.writestr("filesystem/source.txt", b"source")
            output = root / "evidence"
            report = materialize_compiler_data_room(
                world_zip=world, destination=output,
                public_task={"task_id": "task1", "world_id": "world1",
                             "prompt": "inspect source", "expected_output": "x"})
            self.assertEqual(report["world_zip_sha256"],
                             __import__("hashlib").sha256(world.read_bytes()).hexdigest())
            self.assertNotIn("rubric", json.loads(
                (output / "filesystem/Governed/public_task.json").read_text()))


if __name__ == "__main__":
    unittest.main()

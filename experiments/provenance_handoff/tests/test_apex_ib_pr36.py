from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from pp_eval.apex_ib_pr36 import (
    ALL_TASK_IDS,
    FORMAL_TASK_IDS,
    MERGER_MODEL,
    TASK_SPECS,
    TREATMENT_PROPOSER_MODEL,
    WHF_10K,
    WORLD_ID,
    builder_instruction,
    extract_xlsx_index,
    write_xlsx_evidence_index,
    deterministic_gate,
    derived_grading_llm_source,
    compact_apex_output,
    derived_launcher_source,
    filter_snapshot,
    frozen_protocol,
    load_public_task,
    materialize_evidence_overlay,
    materialize_proofpress_executor_overlay,
    majority_native_result,
    randomized_formal_schedule,
    run_stress_cells,
    validate_working_set,
    trajectory_telemetry,
    grader_telemetry,
)


def _tasks() -> list[dict]:
    return [
        {
            "task_id": task_id,
            "world_id": WORLD_ID,
            "domain": "Investment Banking",
            "task_name": task_id,
            "prompt": f"public prompt for {task_id}",
            "expected_output": "spreadsheet",
            "gold_response": "SECRET",
            "rubric": [{"criteria": "SECRET CRITERION"}],
        }
        for task_id in ALL_TASK_IDS
    ]


def _make_world(path: Path) -> None:
    required = {item for spec in TASK_SPECS.values() for item in spec.evidence_allowlist}
    with zipfile.ZipFile(path, "w") as archive:
        for member in required:
            archive.writestr(member, f"bytes for {member}".encode())
        archive.writestr("filesystem/secret/unrelated.txt", b"must not enter bounded overlay")


def _working_set(overlay: Path, task_id: str, artifact: str = MERGER_MODEL) -> dict:
    source = overlay / artifact
    return {
        "schema_version": "proofpress/apex-ib-working-set/v1",
        "task_id": task_id,
        "requirements": [{"id": "r1", "text": "perform the public task"}],
        "claims": [{
            "claim_id": "c1",
            "statement": "The workbook contains the transaction model inputs.",
            "value": None,
            "unit": None,
            "source": {
                "artifact": artifact,
                "locator": "Merger Analysis!A1:L24",
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            },
            "state": "proposed",
        }],
        "relations": [],
        "coverage": [{"requirement_id": "r1", "claim_ids": ["c1"]}],
        "residual_gaps": [],
    }


class ApexIbPr36Tests(unittest.TestCase):
    def test_grader_telemetry_requires_model_provider_tokens_cost_and_no_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "receipts.jsonl"
            path.write_text(json.dumps({
                "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12},
                "gateway": {"cost": "0.02", "routing": {
                    "originalModelId": "judge/a", "finalProvider": "provider-a", "modelAttemptCount": 1,
                }},
            }) + "\n")
            telemetry = grader_telemetry(path, "judge/a")
            self.assertEqual(telemetry["status"], "complete")
            self.assertEqual(telemetry["total_tokens"], 12)
            self.assertEqual(telemetry["known_cost_usd"], 0.02)

    def test_grader_telemetry_fails_closed_on_missing_receipts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            telemetry = grader_telemetry(Path(directory) / "missing.jsonl", "judge/a")
            self.assertEqual(telemetry["status"], "incomplete")

    def test_derived_grading_llm_source_instruments_terminal_response(self) -> None:
        source_path = Path("/private/tmp/proofpress-ling-fin-apex-ckOStP/archipelago/grading/runner/utils/llm.py")
        if not source_path.exists():
            self.skipTest("pinned local Archipelago checkout is not present")
        source = source_path.read_text()
        if "APEX_IB_GRADER_RECEIPTS" in source:
            self.skipTest("pinned local checkout is already instrumented")
        rendered = derived_grading_llm_source(source)
        self.assertIn("APEX_IB_GRADER_RECEIPTS", rendered)
        compile(rendered, "derived_grading_llm.py", "exec")

    def test_trajectory_telemetry_requires_matching_terminal_cost_receipts(self) -> None:
        trajectory = {
            "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12,
                      "call_log": [{"total_tokens": 12}]},
            "messages": [{"provider_specific_fields": {"provider_metadata": {"gateway": {
                "cost": "0.01", "routing": {"originalModelId": "model/a",
                "finalProvider": "provider-a", "modelAttemptCount": 1}
            }}}}],
        }
        telemetry = trajectory_telemetry(trajectory, "model/a")
        self.assertEqual(telemetry["status"], "complete")
        self.assertEqual(telemetry["known_cost_usd"], 0.01)

    def test_trajectory_telemetry_fails_on_missing_cost_or_fallback(self) -> None:
        trajectory = {"usage": {"call_log": [{}]}, "messages": [
            {"provider_specific_fields": {"provider_metadata": {"gateway": {
                "routing": {"originalModelId": "model/a", "finalProvider": "provider-b",
                            "modelAttemptCount": 2}
            }}}}
        ]}
        telemetry = trajectory_telemetry(trajectory, "model/a")
        self.assertEqual(telemetry["status"], "incomplete")
        self.assertFalse(telemetry["no_fallback_observed"])

    def test_public_task_loader_drops_gold_and_rubric(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            path.write_text(json.dumps(_tasks()))
            public = load_public_task(path, FORMAL_TASK_IDS[0])
            self.assertNotIn("gold_response", public)
            self.assertNotIn("rubric", public)
            self.assertEqual(public["world_id"], WORLD_ID)

    def test_bounded_overlay_contains_only_allowlisted_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            world = root / "world.zip"
            _make_world(world)
            overlay = root / "overlay"
            manifest = materialize_evidence_overlay(world, FORMAL_TASK_IDS[0], overlay)
            self.assertEqual({item["path"] for item in manifest["files"]}, {MERGER_MODEL, WHF_10K})
            self.assertFalse((overlay / "filesystem/secret/unrelated.txt").exists())

    def test_public_task_is_digest_bound_when_builder_overlay_is_materialized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            world = root / "world.zip"
            _make_world(world)
            overlay = root / "overlay"
            public_task = {"task_id": FORMAL_TASK_IDS[0], "prompt": "public prompt"}
            manifest = materialize_evidence_overlay(
                world, FORMAL_TASK_IDS[0], overlay, public_task=public_task,
            )
            record = next(
                item for item in manifest["files"]
                if item["path"] == "filesystem/Governed/public_task.json"
            )
            task_path = overlay / record["path"]
            self.assertEqual(record["sha256"], hashlib.sha256(task_path.read_bytes()).hexdigest())
            self.assertEqual(json.loads(task_path.read_text()), public_task)
            validator = overlay / "filesystem/Governed/validate_candidate.py"
            self.assertTrue(validator.is_file())
            self.assertIn("references missing claim IDs", validator.read_text())

    def test_working_set_binds_sources_and_cannot_admit_itself(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            world = root / "world.zip"
            _make_world(world)
            overlay = root / "overlay"
            materialize_evidence_overlay(world, FORMAL_TASK_IDS[0], overlay)
            working = _working_set(overlay, FORMAL_TASK_IDS[0])
            validated = validate_working_set(working, FORMAL_TASK_IDS[0], overlay)
            self.assertIn("working_set_sha256", validated)
            working["admission"] = {"actor": "model"}
            with self.assertRaisesRegex(ValueError, "cannot admit"):
                validate_working_set(working, FORMAL_TASK_IDS[0], overlay)

    def test_unambiguous_relation_alias_is_normalized_but_unknown_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            world = root / "world.zip"
            _make_world(world)
            overlay = root / "overlay"
            materialize_evidence_overlay(world, FORMAL_TASK_IDS[0], overlay)
            working = _working_set(overlay, FORMAL_TASK_IDS[0])
            second = dict(working["claims"][0])
            second["claim_id"] = "c2"
            working["claims"].append(second)
            working["relations"] = [{"from": "c2", "to": "c1", "type": "deriv"}]
            validated = validate_working_set(working, FORMAL_TASK_IDS[0], overlay)
            self.assertEqual(validated["relations"][0]["type"], "derived_from")

            working["relations"][0]["type"] = "related_to"
            with self.assertRaisesRegex(ValueError, "unknown relation type"):
                validate_working_set(working, FORMAL_TASK_IDS[0], overlay)

    def test_requested_final_output_value_is_rejected_but_formula_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            world = root / "world.zip"
            _make_world(world)
            overlay = root / "overlay"
            materialize_evidence_overlay(world, FORMAL_TASK_IDS[0], overlay)
            working = _working_set(overlay, FORMAL_TASK_IDS[0])
            working["claims"][0]["statement"] = "Pro Forma NII per share accretion"
            working["claims"][0]["value"] = 0.2602506878
            with self.assertRaisesRegex(ValueError, "leaks a requested final output"):
                validate_working_set(working, FORMAL_TASK_IDS[0], overlay)

            working["claims"][0]["value"] = "=J34/G34-1"
            validate_working_set(working, FORMAL_TASK_IDS[0], overlay)

    def test_digest_drift_and_material_conflict_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            world = root / "world.zip"
            _make_world(world)
            overlay = root / "overlay"
            materialize_evidence_overlay(world, FORMAL_TASK_IDS[0], overlay)
            validated = validate_working_set(_working_set(overlay, FORMAL_TASK_IDS[0]), FORMAL_TASK_IDS[0], overlay)
            self.assertEqual(deterministic_gate(validated, overlay)["decision"], "allow")
            (overlay / MERGER_MODEL).write_bytes(b"tampered")
            gate = deterministic_gate(validated, overlay)
            self.assertEqual(gate["decision"], "block")
            self.assertFalse(gate["executor_invocation_allowed"])

            overlay2 = root / "overlay2"
            materialize_evidence_overlay(world, FORMAL_TASK_IDS[0], overlay2)
            working = _working_set(overlay2, FORMAL_TASK_IDS[0])
            second = dict(working["claims"][0])
            second["claim_id"] = "c2"
            working["claims"].append(second)
            working["relations"] = [{"from": "c1", "to": "c2", "type": "conflicts_with", "material": True}]
            validated = validate_working_set(working, FORMAL_TASK_IDS[0], overlay2)
            self.assertEqual(deterministic_gate(validated, overlay2)["decision"], "block")

    def test_executor_overlay_keeps_research_only_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            world = root / "world.zip"
            _make_world(world)
            evidence = root / "evidence"
            materialize_evidence_overlay(world, FORMAL_TASK_IDS[0], evidence)
            validated = validate_working_set(_working_set(evidence, FORMAL_TASK_IDS[0]), FORMAL_TASK_IDS[0], evidence)
            package = materialize_proofpress_executor_overlay(evidence, validated, root / "executor")
            self.assertEqual(package["gate_decision"], "allow")
            self.assertEqual(package["production_reliance"], "prohibited")

    def test_neutral_grading_filter_excludes_treatment_sidecars(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.zip"
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr(MERGER_MODEL, b"final workbook")
                archive.writestr("filesystem/Governed/working_set.json", b"treatment")
            target = root / "neutral.zip"
            result = filter_snapshot(source, target, (MERGER_MODEL,))
            with zipfile.ZipFile(target) as archive:
                self.assertEqual(archive.namelist(), [MERGER_MODEL])
            self.assertIn("sha256", result)

    def test_schedule_is_reproducible_and_has_twelve_cells(self) -> None:
        first = randomized_formal_schedule(7)
        self.assertEqual(first, randomized_formal_schedule(7))
        self.assertEqual(len(first), 6)
        self.assertEqual(sum(len(block["arm_order"]) for block in first), 12)

    def test_frozen_protocol_has_twelve_artifact_denominator(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tasks = root / "tasks.json"
            tasks.write_text(json.dumps(_tasks()))
            world = root / "world.zip"
            _make_world(world)
            protocol = frozen_protocol(tasks, world)
            self.assertEqual(protocol["formal_artifact_denominator"], 12)
            self.assertEqual(protocol["treatment_proposer_model"], TREATMENT_PROPOSER_MODEL)
            self.assertNotEqual(protocol["treatment_proposer_model"], protocol["executor_model"])
            serialized = json.dumps(protocol)
            self.assertNotIn("SECRET", serialized)

    def test_builder_instruction_distinguishes_ambiguity_from_source_conflict(self) -> None:
        prompt = builder_instruction({"prompt": "Choose a reasonable valuation combination."})
        self.assertIn("Interpretive ambiguity", prompt)
        self.assertIn("record it in `residual_gaps`", prompt)
        self.assertIn("only when two source-bound claims assert materially incompatible", prompt)

    def test_xlsx_index_preserves_cells_formulas_and_sheet_names(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workbook = Path(directory) / "fixture.xlsx"
            with zipfile.ZipFile(workbook, "w") as archive:
                archive.writestr("xl/workbook.xml", '''<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Model" sheetId="1" r:id="rId1"/></sheets></workbook>''')
                archive.writestr("xl/_rels/workbook.xml.rels", '''<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Target="worksheets/sheet1.xml" Type="worksheet"/></Relationships>''')
                archive.writestr("xl/sharedStrings.xml", '''<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><si><t>Revenue</t></si></sst>''')
                archive.writestr("xl/worksheets/sheet1.xml", '''<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData><row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1"><f>1+1</f><v>2</v></c></row></sheetData></worksheet>''')
            index = extract_xlsx_index(workbook)
            self.assertEqual(index, [{"sheet": "Model", "cells": [
                {"cell": "A1", "value": "Revenue"},
                {"cell": "B1", "value": 2, "formula": "1+1"},
            ]}])

    def test_xlsx_index_is_partitioned_into_catalog_and_sheet_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "filesystem" / "model.xlsx"
            source.parent.mkdir(parents=True)
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("xl/workbook.xml", '''<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Model" sheetId="1" r:id="rId1"/></sheets></workbook>''')
                archive.writestr("xl/_rels/workbook.xml.rels", '''<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Target="worksheets/sheet1.xml" Type="worksheet"/></Relationships>''')
                archive.writestr("xl/worksheets/sheet1.xml", '''<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData><row r="1"><c r="A1"><v>7</v></c></row></sheetData></worksheet>''')
            records = [{"path": "filesystem/model.xlsx", "sha256": hashlib.sha256(source.read_bytes()).hexdigest()}]
            catalog = write_xlsx_evidence_index(root, records)
            self.assertEqual(len(catalog["sheets"]), 1)
            index_path = root / catalog["sheets"][0]["index_path"]
            self.assertTrue(index_path.is_file())
            self.assertEqual(json.loads(index_path.read_text())["cells"], [{"cell": "A1", "value": 7}])

    def test_derived_launcher_has_bounded_world_and_neutral_grading_hooks(self) -> None:
        source_path = Path("/private/tmp/proofpress-ling-fin-apex-ckOStP/archipelago/examples/hugging_face_task/main.py")
        if not source_path.exists():
            self.skipTest("pinned local Archipelago checkout is not present")
        rendered = derived_launcher_source(source_path.read_text())
        self.assertIn("APEX_IB_BOUNDED_WORLD", rendered)
        self.assertIn("APEX_IB_OVERLAY_DIR", rendered)
        self.assertIn("APEX_IB_NEUTRAL_GRADING_MEMBERS", rendered)
        self.assertIn("APEX_IB_SKIP_GRADING", rendered)
        compile(rendered, "derived_launcher.py", "exec")

    def test_output_compaction_preserves_evidence_and_hashes_intermediates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            (output / f"{WORLD_ID}.zip").write_bytes(b"world")
            (output / "world_filesystem.tar.gz").write_bytes(b"tar")
            (output / "final_snapshot.zip").write_bytes(b"converted")
            (output / "final_snapshot.tar.gz").write_bytes(b"final")
            (output / "trajectory.json").write_text("{}")
            manifest = compact_apex_output(output)
            self.assertEqual(manifest["bytes_reclaimed"], len(b"worldtarconverted"))
            self.assertTrue((output / "final_snapshot.tar.gz").exists())
            self.assertTrue((output / "trajectory.json").exists())
            self.assertFalse((output / "final_snapshot.zip").exists())

    def test_output_compaction_can_retain_failed_cell_partial_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            (output / f"{WORLD_ID}.zip").write_bytes(b"world")
            (output / "final_snapshot.zip").write_bytes(b"converted")
            (output / "final_snapshot.tar.gz").write_bytes(b"partial")
            manifest = compact_apex_output(output, preserve_final_tar=True)
            self.assertTrue(manifest["retained_final_snapshot_tar"])
            self.assertTrue((output / "final_snapshot.tar.gz").is_file())
            self.assertFalse((output / f"{WORLD_ID}.zip").exists())
            self.assertFalse((output / "final_snapshot.zip").exists())

    def test_majority_native_result_uses_three_independent_judgments(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory)
            grading = run_dir / "grading_repetitions"
            grading.mkdir()
            scores = ((1, 0), (1, 1), (0, 1))
            for repetition, pair in enumerate(scores, start=1):
                (grading / f"repetition-{repetition:02d}.json").write_text(json.dumps({
                    "grading_run_status": "completed",
                    "verifier_results": [
                        {"verifier_id": "criterion-a", "score": pair[0]},
                        {"verifier_id": "criterion-b", "score": pair[1]},
                    ],
                }))
            result = majority_native_result(run_dir)
            self.assertEqual((result["passed"], result["total"]), (2, 2))
            self.assertTrue(result["exact_success"])

    def test_two_frozen_stress_cells_block_without_executor_or_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            world = root / "world.zip"
            _make_world(world)
            treatments = {}
            for task_id in FORMAL_TASK_IDS:
                treatment_root = root / f"treatment-{task_id}"
                evidence = treatment_root / "evidence"
                materialize_evidence_overlay(world, task_id, evidence)
                artifact = TASK_SPECS[task_id].evidence_allowlist[0]
                validated = validate_working_set(_working_set(evidence, task_id, artifact), task_id, evidence)
                (treatment_root).mkdir(exist_ok=True)
                (treatment_root / "validated_working_set.json").write_text(json.dumps(validated))
                executor = treatment_root / "executor"
                materialize_proofpress_executor_overlay(evidence, validated, executor)
                treatments[task_id] = {"treatment_root": str(treatment_root), "executor_overlay": str(executor)}
            report = run_stress_cells(treatments, root / "stress")
            self.assertEqual(report["status"], "passed")
            self.assertTrue(all(not item["executor_invoked"] for item in report["receipts"]))


if __name__ == "__main__":
    unittest.main()

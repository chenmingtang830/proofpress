#!/usr/bin/env python3
import unittest

from native_e2e_contract import (EXPECTED_OUTPUTS, inconclusive_cell, native_completion_failures,
                                 native_denominators, native_output_breakdown, validate_task_panel)


class NativeE2EContractTests(unittest.TestCase):
    def test_qualification_requires_one_of_each_output(self):
        rows = [{"task_id": str(i), "expected_output": value}
                for i, value in enumerate(EXPECTED_OUTPUTS)]
        self.assertEqual(validate_task_panel(rows, qualification=True)["status"], "pass")
        self.assertEqual(validate_task_panel(rows[:2], qualification=True)["status"], "fail")

    def test_formal_panel_requires_12_unique_tasks_and_all_outputs(self):
        rows = [{"task_id": str(i), "expected_output": EXPECTED_OUTPUTS[i % 3]} for i in range(12)]
        self.assertEqual(validate_task_panel(rows, qualification=False)["status"], "pass")
        rows[-1]["task_id"] = "0"
        self.assertEqual(validate_task_panel(rows, qualification=False)["status"], "fail")

    def test_denominators_and_output_gate_are_task_native(self):
        tasks = [{"task_id": str(i), "expected_output": EXPECTED_OUTPUTS[i % 3]} for i in range(12)]
        cells = [{"task_id": str(i), "condition": condition, "status": "scored"}
                 for i in range(12) for condition in ("a", "b")]
        denominators = native_denominators(tasks, ("a", "b"), 1, cells)
        self.assertEqual(denominators["planned_cells"], 24)
        self.assertNotIn("lawyer_ask_count", denominators)
        self.assertEqual(native_completion_failures(tasks, ("a", "b"), 1, cells), [])
        cells[-1]["status"] = "inconclusive"
        failures = native_completion_failures(tasks, ("a", "b"), 1, cells)
        self.assertEqual(len(failures), 2)

    def test_inconclusive_cell_records_stage_without_raw_error(self):
        row = inconclusive_cell("native_artifact_materialization", "materialization failed",
                                ValueError("private source path"), task_id="task-1")
        self.assertEqual(row["status"], "inconclusive")
        self.assertEqual(row["failure_stage"], "native_artifact_materialization")
        self.assertEqual(row["failure_type"], "ValueError")
        self.assertTrue(row["failure_digest"].startswith("sha256:"))
        self.assertNotIn("private source path", str(row))

    def test_output_breakdown_preserves_native_output_denominators(self):
        tasks = [{"task_id": "a", "expected_output": "message_in_console"},
                 {"task_id": "b", "expected_output": "make_new_doc"}]
        cells = [{"task_id": task_id, "condition": "projection", "executor_model": "model",
                  "status": "scored", "rubric_fraction": score, "unsupported_claims": 0,
                  "citation_errors": 0, "authority_errors": 0, "context_token_upper_bound": 10}
                 for task_id, score in (("a", .25), ("b", .75))]
        rows = native_output_breakdown(tasks, cells)
        self.assertEqual([row["scored_tasks"] for row in rows], [1, 1])
        self.assertEqual({row["expected_output"] for row in rows},
                         {"message_in_console", "make_new_doc"})


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
import unittest

from native_e2e_contract import (EXPECTED_OUTPUTS, native_completion_failures,
                                 native_denominators, validate_task_panel)


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


if __name__ == "__main__":
    unittest.main()

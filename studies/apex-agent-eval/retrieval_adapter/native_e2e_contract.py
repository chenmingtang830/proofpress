#!/usr/bin/env python3
"""Contract and completion gates for the task-native APEX Legal panel."""
from __future__ import annotations

from collections import Counter
from typing import Any, Iterable


SCHEMA_VERSION = "proofpress/private-apex-legal-native-e2e/v1"
EXPECTED_OUTPUTS = ("message_in_console", "make_new_doc", "edit_existing_doc")
FORMAL_TASK_COUNT = 12


def output_type_counts(task_rows: Iterable[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(str(row.get("expected_output")) for row in task_rows)
    return {key: counts.get(key, 0) for key in EXPECTED_OUTPUTS}


def validate_task_panel(task_rows: list[dict[str, Any]], *, qualification: bool) -> dict[str, Any]:
    """Fail closed unless the selected panel has the preregistered native shape."""
    task_ids = [str(row.get("task_id") or "") for row in task_rows]
    counts = output_type_counts(task_rows)
    failures: list[dict[str, Any]] = []
    if len(task_ids) != len(set(task_ids)) or any(not value for value in task_ids):
        failures.append({"reason": "native panel task IDs must be present and unique"})
    unknown = sorted({str(row.get("expected_output")) for row in task_rows} - set(EXPECTED_OUTPUTS))
    if unknown:
        failures.append({"reason": "unknown native expected_output", "values": unknown})
    if qualification:
        if len(task_rows) != len(EXPECTED_OUTPUTS) or any(counts[key] != 1 for key in EXPECTED_OUTPUTS):
            failures.append({"reason": "native qualification requires exactly one task per output type",
                             "expected": {key: 1 for key in EXPECTED_OUTPUTS}, "actual": counts})
    else:
        if len(task_rows) != FORMAL_TASK_COUNT:
            failures.append({"reason": "formal native panel requires exactly 12 tasks",
                             "expected": FORMAL_TASK_COUNT, "actual": len(task_rows)})
        missing = [key for key in EXPECTED_OUTPUTS if counts[key] == 0]
        if missing:
            failures.append({"reason": "formal native panel must cover every output type", "missing": missing})
    return {"status": "pass" if not failures else "fail", "failures": failures,
            "task_count": len(task_rows), "output_type_counts": counts}


def native_denominators(task_rows: list[dict[str, Any]], conditions: Iterable[str],
                        executor_count: int, cells: list[dict[str, Any]]) -> dict[str, Any]:
    """Expose task/output denominators without reusing lawyer-ask terminology."""
    condition_count = len(tuple(conditions))
    planned = len(task_rows) * condition_count * executor_count
    scored = sum(row.get("status") == "scored" for row in cells)
    return {"planned_cells": planned, "task_count": len(task_rows),
            "output_type_task_counts": output_type_counts(task_rows),
            "condition_count": condition_count, "executor_count": executor_count,
            "scored_cells": scored, "inconclusive_cells": len(cells) - scored}


def native_completion_failures(task_rows: list[dict[str, Any]], conditions: Iterable[str],
                               executor_count: int, cells: list[dict[str, Any]]) -> list[dict[str, Any]]:
    denominators = native_denominators(task_rows, conditions, executor_count, cells)
    failures: list[dict[str, Any]] = []
    if denominators["scored_cells"] != denominators["planned_cells"]:
        failures.append({"reason": "not every task-native cell produced three valid blind grades",
                         "expected": denominators["planned_cells"],
                         "actual": denominators["scored_cells"]})
    for expected_output in EXPECTED_OUTPUTS:
        task_ids = {str(row["task_id"]) for row in task_rows if row.get("expected_output") == expected_output}
        output_cells = [row for row in cells if str(row.get("task_id")) in task_ids]
        expected = len(task_ids) * denominators["condition_count"] * executor_count
        actual = sum(row.get("status") == "scored" for row in output_cells)
        if actual != expected:
            failures.append({"reason": "native output type has incomplete scored cells",
                             "expected_output": expected_output, "expected": expected, "actual": actual})
    return failures

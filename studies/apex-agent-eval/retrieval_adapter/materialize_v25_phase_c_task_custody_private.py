#!/usr/bin/env python3
"""Materialize only the frozen v25 task-held-out custody slice.

The source task manifest may carry a gold response.  This helper never copies
that field: its task records retain the prompt/native output contract for the
executor, the rubric for the later official grader, and private world/overlay
metadata for the native harness.  Exact-knowledge construction separately
whitelists its own rubric-free input from these custody records.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
CONTROLS_PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/build_phase_c_task_controls_private.py"
SPEC = importlib.util.spec_from_file_location("phase_c_task_controls", CONTROLS_PATH)
controls = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(controls)

SCHEMA = "proofpress/v25-phase-c-task-custody/v1"
TASK_FIELDS = ("task_id", "prompt", "expected_output", "rubric", "task_name", "world_id")


def digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _write_private(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.parent.chmod(0o700)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    path.chmod(0o600)


def _rows(value: Any) -> list[dict[str, Any]]:
    rows = value.get("tasks", value) if isinstance(value, dict) else value
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError("source task manifest must be a task object array")
    return rows


def build(*, frozen_manifest: dict[str, Any], source_tasks: Any,
          task_files_root: Path) -> tuple[dict[str, dict[str, Any]], dict[str, Any], dict[str, Any]]:
    """Return private task custody, overlay routing, and a content-free receipt."""
    task_ids = controls.expected_heldout_ids(frozen_manifest)
    by_id = {row.get("task_id"): row for row in _rows(source_tasks)}
    if set(task_ids) - set(by_id):
        raise ValueError("source task manifest is missing a frozen held-out task")
    custody: dict[str, dict[str, Any]] = {}
    overlay_rows: list[dict[str, Any]] = []
    for task_id in task_ids:
        raw = by_id[task_id]
        if not all(isinstance(raw.get(field), str) and raw[field]
                   for field in ("task_id", "prompt", "expected_output", "world_id")):
            raise ValueError("frozen task is missing executor or world metadata")
        if not isinstance(raw.get("rubric"), list) or not raw["rubric"]:
            raise ValueError("frozen task is missing the official rubric")
        task = {field: raw[field] for field in TASK_FIELDS if field in raw}
        # Mechanical anti-leak boundary.  The only source of gold is the input
        # manifest; any gold-like field would be a custody bug.
        if any("gold" in field.lower() for field in task):
            raise ValueError("task custody must not contain gold fields")
        custody[task_id] = {"task": task}
        input_files = raw.get("task_input_files")
        # APEX manifests use either a single private path string or an array
        # of paths.  Custody routes only on the presence of an overlay; it
        # never carries these private path strings forward.
        if input_files is not None and not isinstance(input_files, (str, list)):
            raise ValueError("task_input_files must be a string or list when present")
        overlay = task_files_root / task_id
        uses_overlay = bool(input_files)
        if uses_overlay and not overlay.is_dir():
            raise ValueError("frozen task overlay is missing from private source custody")
        if not uses_overlay and overlay.exists():
            raise ValueError("unexpected task overlay would expand source access")
        overlay_rows.append({"task_id": task_id,
                             "overlay_root": str(overlay) if uses_overlay else None})
    overlay_index = {"schema_version": SCHEMA, "task_ids_digest": digest(list(task_ids)),
                     "overlays": overlay_rows}
    receipt = {"schema_version": SCHEMA, "status": "materialized-private-custody",
               "task_count": len(task_ids), "task_ids_digest": digest(list(task_ids)),
               "custody_digest": digest(custody), "overlay_index_digest": digest(overlay_index),
               "overlay_task_count": sum(row["overlay_root"] is not None for row in overlay_rows),
               "gold_copied": False, "automatic_admission": False,
               "human_approval_required": True,
               "decision_boundary": "Private custody only; construction and execution controls remain separate."}
    return custody, overlay_index, receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen-manifest", required=True, type=Path)
    parser.add_argument("--source-tasks", required=True, type=Path)
    parser.add_argument("--task-files-root", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    frozen = json.loads(args.frozen_manifest.read_text())
    source = json.loads(args.source_tasks.read_text())
    custody, overlays, receipt = build(frozen_manifest=frozen, source_tasks=source,
                                        task_files_root=args.task_files_root)
    args.out.mkdir(parents=True, exist_ok=True); args.out.chmod(0o700)
    task_dir = args.out / "tasks"; task_dir.mkdir(exist_ok=True); task_dir.chmod(0o700)
    for task_id, value in custody.items():
        _write_private(task_dir / f"{task_id}.json", value)
    _write_private(args.out / "task-ids-private.json", list(custody))
    _write_private(args.out / "task-overlays-private.json", overlays)
    _write_private(args.out / "task-custody-receipt-sanitized.json", receipt)
    print(json.dumps({key: receipt[key] for key in ("status", "task_count", "task_ids_digest",
                                                     "custody_digest", "overlay_task_count", "gold_copied")},
                     sort_keys=True))


if __name__ == "__main__":
    main()

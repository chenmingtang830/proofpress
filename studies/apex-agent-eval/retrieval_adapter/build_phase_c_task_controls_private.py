#!/usr/bin/env python3
"""Compile restored private task files into the two Phase C task controls.

The executor must receive the frozen task prompt and native-output type, but
never a rubric or a gold answer.  The blind grader receives the frozen rubric,
but the task-source control does not carry it.  This helper makes that split
deterministic when a caller restores the private, one-task-per-file custody
directory; it writes only caller-owned private artifacts and prints digests.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
SCHEMA = "proofpress/phase-c-task-controls/v1"


def digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return "sha256:" + value.hexdigest()


def expected_heldout_ids(manifest: dict[str, Any]) -> tuple[str, ...]:
    """Return only the preregistered Phase C transfer panel.

    The five development tasks remain in the public manifest to make their
    exclusion auditable, but they are deliberately not restored, disclosed, or
    run in Phase C.  Requiring them here would turn the held-out estimate into
    a mixed development-and-transfer panel and needlessly expand private
    custody scope.
    """
    development = manifest.get("development_task_ids")
    heldout = manifest.get("held_out_task_ids")
    if (not isinstance(development, list) or not isinstance(heldout, list)
            or not all(isinstance(item, str) and item for item in development + heldout)):
        raise ValueError("frozen manifest requires non-empty string task IDs")
    if len(development) != 5 or len(heldout) != 7:
        raise ValueError("frozen manifest requires five development and seven held-out task IDs")
    identifiers = tuple(heldout)
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("frozen manifest task IDs must be unique")
    return identifiers


def _task(value: Any, path: Path) -> dict[str, Any]:
    candidate = value.get("task") if isinstance(value, dict) and isinstance(value.get("task"), dict) else value
    if not isinstance(candidate, dict):
        raise ValueError(f"{path.name} must be a task object or contain a task object")
    if not all(isinstance(candidate.get(field), str) and candidate[field]
               for field in ("task_id", "prompt", "expected_output")):
        raise ValueError(f"{path.name} requires task_id, prompt, and expected_output")
    if not isinstance(candidate.get("rubric"), list):
        raise ValueError(f"{path.name} requires a rubric array")
    return candidate


def build(*, manifest: dict[str, Any], task_root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Return private executor/grader controls and a source-safe receipt."""
    identifiers = expected_heldout_ids(manifest)
    if not task_root.is_dir():
        raise ValueError("task root must be a directory")
    by_id: dict[str, dict[str, Any]] = {}
    files = sorted(path for path in task_root.iterdir() if path.is_file() and path.suffix == ".json")
    for path in files:
        task = _task(json.loads(path.read_text()), path)
        task_id = task["task_id"]
        if task_id in by_id:
            raise ValueError(f"duplicate private task ID: {task_id}")
        by_id[task_id] = task
    if set(by_id) != set(identifiers):
        missing = sorted(set(identifiers) - set(by_id))
        unexpected = sorted(set(by_id) - set(identifiers))
        raise ValueError(f"private task files do not match frozen panel; missing={missing}; unexpected={unexpected}")
    panel_digest = digest({"task_ids": identifiers})
    source = {"schema_version": SCHEMA, "control": "executor-task-source/v1",
              "panel_task_ids_digest": panel_digest, "automatic_admission": False,
              "human_approval_required": True, "rubric_access": "forbidden",
              "tasks": [{key: by_id[task_id][key] for key in ("task_id", "prompt", "expected_output")}
                        for task_id in identifiers]}
    rubrics = {"schema_version": SCHEMA, "control": "blind-grader-rubric/v1",
               "panel_task_ids_digest": panel_digest, "automatic_admission": False,
               "human_approval_required": True, "executor_access": "forbidden",
               "rubrics": [{"task_id": task_id, "rubric": by_id[task_id]["rubric"]}
                           for task_id in identifiers]}
    receipt = {"schema_version": SCHEMA, "status": "compiled-private-controls",
               "automatic_admission": False, "human_approval_required": True,
               "task_count": len(identifiers), "panel_task_ids_digest": panel_digest,
               "task_source_digest": digest(source), "rubric_manifest_digest": digest(rubrics),
               "decision_boundary": "No task, rubric, or candidate is admitted by control compilation."}
    return source, rubrics, receipt


def _write_private(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    path.chmod(0o600)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen-manifest", required=True, type=Path)
    parser.add_argument("--task-root", required=True, type=Path,
                        help="Private directory containing exactly one JSON task object per frozen task.")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    source, rubrics, receipt = build(manifest=json.loads(args.frozen_manifest.read_text()), task_root=args.task_root)
    args.out.mkdir(parents=True, exist_ok=True); args.out.chmod(0o700)
    source_path = args.out / "phase-c-task-source-private.json"
    rubric_path = args.out / "phase-c-rubric-manifest-private.json"
    receipt_path = args.out / "phase-c-task-controls-sanitized.json"
    _write_private(source_path, source); _write_private(rubric_path, rubrics); _write_private(receipt_path, receipt)
    print(json.dumps({"status": receipt["status"], "task_count": receipt["task_count"],
                      "task_source_digest": file_digest(source_path),
                      "rubric_manifest_digest": file_digest(rubric_path)}, sort_keys=True))


if __name__ == "__main__":
    main()

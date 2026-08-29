#!/usr/bin/env python3
"""Aggregate three blinded semantic adjudications by deterministic item-level majority."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from run_claim_construction_private import digest
from score_claim_construction_private import semantic_paired_metrics

SCHEMA = "proofpress/private-claim-semantic-adjudication-majority/v1"


def majority_set(values: list[list[str]]) -> list[str]:
    threshold = len(values) // 2 + 1
    counts = Counter(item for rows in values for item in set(rows))
    return sorted(item for item, count in counts.items() if count >= threshold)


def majority_mappings(values: list[list[dict]]) -> list[dict]:
    threshold = len(values) // 2 + 1
    rubric_presence = Counter()
    requirement_counts: dict[str, Counter] = {}
    mappings_by_rubric: dict[str, list[tuple[str, ...]]] = {}
    for rows in values:
        for row in rows:
            rubric_id = row["rubric_id"]
            refs = tuple(sorted(set(row.get("requirement_ids", []))))
            if refs:
                rubric_presence[rubric_id] += 1
                requirement_counts.setdefault(rubric_id, Counter()).update(refs)
                mappings_by_rubric.setdefault(rubric_id, []).append(refs)
    output = []
    for rubric_id, count in sorted(rubric_presence.items()):
        if count < threshold:
            continue
        refs = sorted(ref for ref, ref_count in requirement_counts[rubric_id].items()
                      if ref_count >= threshold)
        if not refs:
            refs = list(Counter(mappings_by_rubric[rubric_id]).most_common(1)[0][0])
        output.append({"rubric_id": rubric_id, "requirement_ids": refs})
    return output


def aggregate_system(rows: list[dict]) -> dict:
    expected = majority_set([row.get("expected_open_gap_requirement_ids", []) for row in rows])
    honest = set(majority_set([row.get("honest_open_gap_requirement_ids", []) for row in rows]))
    return {
        "requirement_to_rubric": majority_mappings([row.get("requirement_to_rubric", []) for row in rows]),
        "factual_claim_ids": majority_set([row.get("factual_claim_ids", []) for row in rows]),
        "unsupported_factual_claim_ids": majority_set([row.get("unsupported_factual_claim_ids", []) for row in rows]),
        "expected_open_gap_requirement_ids": expected,
        "honest_open_gap_requirement_ids": sorted(honest & set(expected)),
        "gap_to_silver_candidates": [],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", action="append", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    if len(args.report) != 3:
        raise SystemExit("majority aggregation requires exactly three frozen adjudication reports")
    reports = [json.loads(Path(path).read_text()) for path in args.report]
    identity_fields = ("v7_report_digest", "candidate_report_digest", "candidate_label", "silver_report_digest")
    if any(any(report.get(field) != reports[0].get(field) for report in reports[1:]) for field in identity_fields):
        raise SystemExit("adjudication reports do not score the same frozen artifact")
    task_ids = sorted({row["task_id"] for row in reports[0]["tasks"] if row["status"] == "ok"})
    if any(sorted(row["task_id"] for row in report["tasks"] if row["status"] == "ok") != task_ids
           for report in reports):
        raise SystemExit("adjudication task denominators differ")
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw = out / "raw"; raw.mkdir(exist_ok=True); raw.chmod(0o700)
    summaries = []
    candidate_label = reports[0]["candidate_label"]
    for task_id in task_ids:
        source_rows = [json.loads((Path(report["raw_private_dir"]) / f"{task_id}.json").read_text())
                       for report in reports]
        systems = {}
        for label in ("v7", candidate_label):
            systems[label] = aggregate_system([row["labels"]["systems"][label] for row in source_rows])
        private = {"schema_version": SCHEMA, "task_id": task_id,
                   "boundary": "item-level two-of-three majority over independent blinded post-output adjudications",
                   "rubric_atom_ids": source_rows[0]["rubric_atom_ids"], "labels": {"systems": systems},
                   "source_label_digests": [digest(row["labels"]) for row in source_rows]}
        target = raw / f"{task_id}.json"
        target.write_text(json.dumps(private, indent=2, sort_keys=True) + "\n"); target.chmod(0o600)
        summaries.append({"task_id": task_id, "status": "ok", "label_digest": digest(private["labels"])})
    report = {"schema_version": SCHEMA,
              "boundary": "Post-output two-of-three model-adjudicated majority; not human gold, pre-output silver, or admission.",
              **{field: reports[0][field] for field in identity_fields},
              "source_report_digests": [digest(report) for report in reports],
              "denominators": {"adjudications_per_artifact": 3, "tasks": len(task_ids)},
              "tasks": summaries, "raw_private_dir": str(raw)}
    # The scorer only depends on the raw labels and candidate label; use the
    # established function to keep metric semantics identical to prior panels.
    report["metrics"] = semantic_paired_metrics(report, task_ids, candidate_label)
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "pass", "metrics": report["metrics"]}, sort_keys=True))


if __name__ == "__main__":
    main()

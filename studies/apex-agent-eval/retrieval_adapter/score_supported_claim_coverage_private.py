#!/usr/bin/env python3
"""Score paired rubric coverage backed by non-unsupported candidate claims."""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

from governed_workflow_contract import digest

SCHEMA = "proofpress/private-supported-claim-coverage/v1"


def system_claims(raw: dict[str, Any]) -> dict[str, set[str]]:
    construction = raw.get("construction", {})
    result: dict[str, set[str]] = {}
    for row in construction.get("claims", []):
        if row.get("id") and row.get("requirement_id"):
            result.setdefault(str(row["requirement_id"]), set()).add(str(row["id"]))
    return result


def task_coverage(labels: dict[str, Any], raw: dict[str, Any]) -> tuple[int, int, float | None]:
    claims = system_claims(raw)
    factual = set(labels.get("factual_claim_ids", []))
    unsupported = set(labels.get("unsupported_factual_claim_ids", []))
    supported_factual = factual - unsupported
    covered = 0
    mappings = labels.get("requirement_to_rubric", [])
    for mapping in mappings:
        requirement_ids = mapping.get("requirement_ids", [])
        if any(claims.get(requirement_id, set()) & supported_factual for requirement_id in requirement_ids):
            covered += 1
    total = len(mappings)
    return covered, total, covered / total if total else None


def paired_bootstrap(deltas: list[float], seed: int = 10_001, draws: int = 10_000) -> list[float] | None:
    if not deltas:
        return None
    rng = random.Random(seed)
    values = sorted(sum(rng.choice(deltas) for _ in deltas) / len(deltas) for _ in range(draws))
    return [values[int(draws * .025)], values[int(draws * .975) - 1]]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--majority-report", required=True)
    parser.add_argument("--v7-report", required=True)
    parser.add_argument("--candidate-report", required=True)
    parser.add_argument("--candidate-label", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    majority = json.loads(Path(args.majority_report).read_text())
    reports = {"v7": json.loads(Path(args.v7_report).read_text()),
               args.candidate_label: json.loads(Path(args.candidate_report).read_text())}
    task_ids = sorted(row["task_id"] for row in majority.get("tasks", []) if row.get("status") == "ok")
    rows = []
    for task_id in task_ids:
        label_artifact = json.loads((Path(majority["raw_private_dir"]) / f"{task_id}.json").read_text())
        task = {"task_id": task_id}
        for label, report in reports.items():
            raw = json.loads((Path(report["raw_private_dir"]) / f"{task_id}.json").read_text())
            covered, total, fraction = task_coverage(label_artifact["labels"]["systems"][label], raw)
            task[label] = {"covered_rubric_atoms": covered, "mapped_rubric_atoms": total,
                           "supported_claim_coverage": fraction}
        if task["v7"]["supported_claim_coverage"] is not None and task[args.candidate_label]["supported_claim_coverage"] is not None:
            task["delta"] = (task[args.candidate_label]["supported_claim_coverage"]
                             - task["v7"]["supported_claim_coverage"])
        rows.append(task)
    paired = [row["delta"] for row in rows if "delta" in row]
    means = {label: (sum(row[label]["supported_claim_coverage"] for row in rows
                         if row[label]["supported_claim_coverage"] is not None)
                     / sum(row[label]["supported_claim_coverage"] is not None for row in rows))
             for label in reports}
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    report = {"schema_version": SCHEMA,
              "boundary": "Post-output model-adjudicated supported candidate coverage; not human gold or admission.",
              "definition": "A mapped rubric atom is covered when at least one mapped requirement has a claim labeled factual and not unsupported by the frozen majority adjudication; unadjudicated non-factual claims do not count.",
              "candidate_label": args.candidate_label, "tasks": rows,
              "metrics": {"v7_supported_claim_coverage": means["v7"],
                          "candidate_supported_claim_coverage": means[args.candidate_label],
                          "mean_paired_delta": sum(paired) / len(paired) if paired else None,
                          "paired_bootstrap_95_ci": paired_bootstrap(paired)},
              "denominators": {"tasks": len(task_ids), "paired_tasks": len(paired)},
              "input_digests": {"majority": digest(majority),
                                "v7": digest(reports["v7"]),
                                "candidate": digest(reports[args.candidate_label])}}
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report["metrics"], sort_keys=True))


if __name__ == "__main__":
    main()

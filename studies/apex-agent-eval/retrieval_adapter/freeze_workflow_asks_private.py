#!/usr/bin/env python3
"""Freeze twelve lawyer-style asks from two staged v8 task graphs."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def digest(value: Any) -> str:
    body = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(body.encode()).hexdigest()


def interleave_by_task(rows: list[tuple[str, Any]], task_ids: list[str], limit: int) -> list[tuple[str, Any]]:
    buckets = {task_id: [row for row in rows if row[0] == task_id] for task_id in task_ids}
    output = []
    while len(output) < limit and any(buckets.values()):
        for task_id in task_ids:
            if buckets[task_id] and len(output) < limit:
                output.append(buckets[task_id].pop(0))
    return output


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--claim-report", required=True)
    ap.add_argument("--task-id", action="append", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    if len(args.task_id) != 2:
        raise SystemExit("exactly two sequential task IDs are required")
    report = json.loads(Path(args.claim_report).read_text())
    raw_dir = Path(report["raw_private_dir"])
    graphs = []
    for task_id in args.task_id:
        path = raw_dir / f"{task_id}.json"
        if not path.exists():
            raise SystemExit(f"claim artifact unavailable for {task_id}")
        value = json.loads(path.read_text())
        if value.get("construction", {}).get("status") != "ok":
            raise SystemExit(f"claim construction unavailable for {task_id}")
        graphs.append(value)
    requirements, claims, relations = {}, {}, []
    task_for_requirement = {}
    for graph in graphs:
        task_id = graph["task"]["task_id"]
        for row in graph["construction"].get("requirements", []):
            requirements[(task_id, row["requirement_id"])] = row
            task_for_requirement[row["requirement_id"]] = task_id
        for row in graph["construction"].get("claims", []):
            claims[row["id"]] = (task_id, row)
        relations.extend((task_id, row) for row in graph["construction"].get("relations", []))
    asks = []
    covered = [(task_id, row) for _, (task_id, row) in sorted(claims.items()) if row.get("evidence_ids")]
    if len(covered) < 3 or len(relations) < 3:
        raise SystemExit("two-task graph lacks three covered claims or three relations")
    for index, (task_id, claim) in enumerate(interleave_by_task(covered, args.task_id, 3), 1):
        requirement = requirements.get((task_id, claim["requirement_id"]), {})
        asks.append({"ask_id": f"covered-{index}", "category": "graph-fully-covered", "task_id": task_id,
                     "query": "What does the governed record establish about " + requirement.get("requirement", claim.get("category", "this issue")) + "?",
                     "expected_claim_ids": [claim["id"]], "expected_relation_ids": [], "expected_gap_ids": []})
    for index, (task_id, relation) in enumerate(interleave_by_task(relations, args.task_id, 3), 1):
        left, right = claims.get(relation.get("from")), claims.get(relation.get("to"))
        if not left or not right:
            raise SystemExit("relation references an unknown staged claim")
        left_req = requirements.get((left[0], left[1]["requirement_id"]), {}).get("requirement", "the first issue")
        right_req = requirements.get((right[0], right[1]["requirement_id"]), {}).get("requirement", "the second issue")
        asks.append({"ask_id": f"relation-{index}", "category": "relation-dependent", "task_id": task_id,
                     "query": f"How do the governed positions on {left_req} and {right_req} interact?",
                     "expected_claim_ids": [left[1]["id"], right[1]["id"]],
                     "expected_relation_ids": [relation.get("id") or digest(relation)], "expected_gap_ids": []})
    gaps = []
    for graph in graphs:
        task_id = graph["task"]["task_id"]
        gaps.extend((task_id, row) for row in graph["construction"].get("requirements", [])
                    if row.get("status") in {"partial", "gap"})
    if len(gaps) < 3:
        raise SystemExit("two-task graph lacks three explicit gaps")
    for index, (task_id, row) in enumerate(interleave_by_task(gaps, args.task_id, 3), 1):
        asks.append({"ask_id": f"partial-{index}", "category": "partial-gap", "task_id": task_id,
                     "query": "What is known, and what remains unresolved, about " + row.get("requirement", "this issue") + "?",
                     "expected_claim_ids": [], "expected_relation_ids": [],
                     "expected_gap_ids": [row["requirement_id"]]})
    novel_topics = ("environmental permits not represented in the staged graph",
                    "sanctions screening evidence not represented in the staged graph",
                    "real-property liens not represented in the staged graph")
    for index, topic in enumerate(novel_topics, 1):
        asks.append({"ask_id": f"novel-{index}", "category": "novel", "task_id": args.task_id[(index - 1) % 2],
                     "query": f"Does the data room establish anything about {topic}?",
                     "expected_claim_ids": [], "expected_relation_ids": [], "expected_gap_ids": [f"novel-{index}"]})
    manifest = {"schema_version": "proofpress/private-lawyer-ask-manifest/v1",
                "claim_report_digest": digest(report), "task_ids": args.task_id,
                "staged_evaluation": True, "non_authoritative": True, "asks": asks}
    manifest["manifest_digest"] = digest(manifest)
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    private = out / "lawyer-asks-private.json"
    private.write_text(json.dumps(manifest, indent=2) + "\n"); private.chmod(0o600)
    sanitized = {"schema_version": "proofpress/private-lawyer-ask-freeze-report/v1",
                 "manifest_digest": manifest["manifest_digest"], "task_ids": args.task_id,
                 "ask_count": len(asks), "categories": {category: sum(a["category"] == category for a in asks)
                                                          for category in sorted({a["category"] for a in asks})},
                 "staged_evaluation": True, "non_authoritative": True,
                 "private_manifest": str(private)}
    (out / "sanitized-report.json").write_text(json.dumps(sanitized, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"ok": True, "ask_count": len(asks), "report": str(out / "sanitized-report.json")}))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Extend a frozen private-evaluation budget floor with explicit report costs.

The baseline is intentionally retained as one opaque, previously audited
receipt aggregate.  Later reports are named explicitly so reruns and failed
diagnostics remain in the budget instead of being replaced by the final panel.
Missing telemetry keeps the exact total inconclusive; it is never projected as
zero.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def nested(value: dict[str, Any], path: str) -> Any:
    current: Any = value
    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def parse_report(value: str) -> tuple[str, Path, str]:
    try:
        label, specification = value.split("=", 1)
        path, field = specification.rsplit("::", 1)
    except (IndexError, ValueError) as exc:
        raise argparse.ArgumentTypeError("report must be LABEL=PATH::FIELD") from exc
    if not label or not path or not field:
        raise argparse.ArgumentTypeError("report must be LABEL=PATH::FIELD")
    return label, Path(path), field


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--report", action="append", default=[], type=parse_report,
                    help="Explicit LABEL=PATH::dotted.cost.field entry; repeatable")
    ap.add_argument("--limit", type=float, default=50.0)
    ap.add_argument("--unknown-note", action="append", default=[])
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    baseline_path = Path(args.baseline)
    baseline = json.loads(baseline_path.read_text())
    baseline_known = baseline.get("known_cost_usd")
    if not isinstance(baseline_known, (int, float)):
        raise SystemExit("baseline must contain numeric known_cost_usd")
    entries: list[dict[str, Any]] = [{
        "label": "frozen-pre-extension-receipt-floor",
        "cost_usd": baseline_known,
        "source": str(baseline_path),
        "source_schema": baseline.get("schema_version"),
        "telemetry_status": "known_floor",
    }]
    seen_labels: set[str] = set()
    for label, path, field in args.report:
        if label in seen_labels:
            raise SystemExit(f"duplicate budget label: {label}")
        seen_labels.add(label)
        report = json.loads(path.read_text())
        cost = nested(report, field)
        if not isinstance(cost, (int, float)):
            raise SystemExit(f"{label}: nonnumeric or missing cost field {field}")
        entries.append({"label": label, "cost_usd": cost, "source": str(path),
                        "source_schema": report.get("schema_version"),
                        "cost_field": field, "telemetry_status": "reported_known_cost"})
    for index, note in enumerate(args.unknown_note, 1):
        entries.append({"label": f"unknown-cost-attempts-{index}", "cost_usd": None,
                        "telemetry_status": "inconclusive", "reason": note})

    known_total = sum(float(row["cost_usd"]) for row in entries
                      if isinstance(row.get("cost_usd"), (int, float)))
    exact = all(isinstance(row.get("cost_usd"), (int, float)) for row in entries)
    output = {
        "schema_version": "proofpress/private-evaluation-budget/v1",
        "limit_usd": args.limit,
        "entries": entries,
        "known_cost_usd": known_total,
        "exact_total_usd": known_total if exact else None,
        "known_floor_within_limit": known_total <= args.limit,
        "budget_status": "complete" if exact and known_total <= args.limit else
            "fail_limit_exceeded" if known_total > args.limit else
            "inconclusive_missing_cost_telemetry",
        "fallback": "forbidden",
        "boundary": "A known floor below the limit is not proof that the exact total is below it when telemetry is missing.",
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"ok": True, "out": str(out), "known_cost_usd": known_total,
                      "status": output["budget_status"]}))


if __name__ == "__main__":
    main()

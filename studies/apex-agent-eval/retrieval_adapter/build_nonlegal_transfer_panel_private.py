#!/usr/bin/env python3
"""Build the frozen non-legal exact-knowledge transfer panel privately.

The public repository contains the deterministic builder, never prompts,
source tables, calculation inputs, or gold outputs.  The sanitized manifest
contains only content digests and coverage labels.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "proofpress/nonlegal-exact-transfer-panel/v1"
FAMILIES = ("financial_table_reconciliation", "operational_kpi", "contract_payment_schedule")
VARIANTS = ("period_rows", "period_columns", "missing_or_conflicting_input")


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def build_tasks() -> list[dict[str, str]]:
    """Return source-backed exercises with their deterministic hidden outputs."""
    return [
        {"id": "fin-row-variance", "family": FAMILIES[0], "variant": VARIANTS[0],
         "source": "| Period | Actual | Budget |\n|---|---:|---:|\n| Jan | 120 | 100 |\n| Feb | 80 | 90 |\n| Mar | 150 | 130 |\n",
         "ask": "What is total actual-minus-budget variance across all listed periods? Return one integer.", "gold": "30"},
        {"id": "fin-column-gross-margin", "family": FAMILIES[0], "variant": VARIANTS[1],
         "source": "| Metric | Q1 | Q2 | Q3 |\n|---|---:|---:|---:|\n| Revenue | 300 | 360 | 340 |\n| Cost | 180 | 216 | 204 |\n",
         "ask": "What is aggregate gross margin percentage: (total Revenue minus total Cost) divided by total Revenue? Return exactly two decimals and a percent sign.", "gold": "40.00%"},
        {"id": "fin-conflicting-invoice", "family": FAMILIES[0], "variant": VARIANTS[2],
         "source": "| Invoice | Amount |\n|---|---:|\n| A-17 | 480 |\n| A-17 | 510 |\n",
         "ask": "State whether the invoice amount can be reconciled exactly. If not, return CONFLICT followed by the invoice identifier.", "gold": "CONFLICT A-17"},
        {"id": "ops-row-conversion", "family": FAMILIES[1], "variant": VARIANTS[0],
         "source": "| Week | Visits | Conversions |\n|---|---:|---:|\n| 1 | 800 | 32 |\n| 2 | 1000 | 50 |\n| 3 | 1200 | 48 |\n",
         "ask": "What is the weighted conversion rate across all weeks? Return exactly two decimals and a percent sign.", "gold": "4.55%"},
        {"id": "ops-column-resolution", "family": FAMILIES[1], "variant": VARIANTS[1],
         "source": "| KPI | Apr | May | Jun |\n|---|---:|---:|---:|\n| Tickets opened | 120 | 150 | 130 |\n| Tickets resolved | 108 | 144 | 130 |\n",
         "ask": "What is the total resolution rate across all listed months? Return exactly two decimals and a percent sign.", "gold": "95.00%"},
        {"id": "ops-missing-denominator", "family": FAMILIES[1], "variant": VARIANTS[2],
         "source": "| Week | Active users | Churned users |\n|---|---:|---:|\n| 1 | 1000 | 20 |\n| 2 |  | 25 |\n",
         "ask": "Can a two-week churn rate be calculated exactly? If not, return INSUFFICIENT followed by the missing field name.", "gold": "INSUFFICIENT Active users"},
        {"id": "contract-row-payment-total", "family": FAMILIES[2], "variant": VARIANTS[0],
         "source": "Clause 4: Payments are due on the dates and in the amounts stated below.\n\n| Due date | Amount |\n|---|---:|\n| 2026-01-15 | 2500 |\n| 2026-02-15 | 2500 |\n| 2026-03-15 | 3000 |\n",
         "ask": "Under Clause 4, what is the total scheduled payment amount? Return one integer.", "gold": "8000"},
        {"id": "contract-column-payment-total", "family": FAMILIES[2], "variant": VARIANTS[1],
         "source": "Clause 7: The customer owes each monthly installment shown below.\n\n| Field | Jan | Feb | Mar |\n|---|---:|---:|---:|\n| Installment | 900 | 900 | 1200 |\n",
         "ask": "Under Clause 7, what is the total scheduled installment amount? Return one integer.", "gold": "3000"},
        {"id": "contract-conflicting-installment", "family": FAMILIES[2], "variant": VARIANTS[2],
         "source": "Clause 7: The customer owes each stated installment.\n\n| Due date | Installment |\n|---|---:|\n| 2026-04-01 | 900 |\n| 2026-04-01 | 950 |\n",
         "ask": "Can the April 1 installment be calculated exactly under Clause 7? If not, return CONFLICT followed by the due date.", "gold": "CONFLICT 2026-04-01"},
    ]


def validate_tasks(tasks: list[dict[str, str]]) -> None:
    if len(tasks) != 9 or len({task["id"] for task in tasks}) != len(tasks):
        raise ValueError("non-legal panel requires nine unique tasks")
    pairs = {(task["family"], task["variant"]) for task in tasks}
    if pairs != {(family, variant) for family in FAMILIES for variant in VARIANTS}:
        raise ValueError("non-legal panel must cover every family and required variant once")
    for task in tasks:
        if not all(isinstance(task.get(key), str) and task[key] for key in ("source", "ask", "gold")):
            raise ValueError("every task requires source, ask, and gold")


def write_panel(out: Path) -> dict[str, Any]:
    tasks = build_tasks(); validate_tasks(tasks)
    out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    private_rows = []
    for task in tasks:
        source_path = out / f"{task['id']}.md"
        source_path.write_text(task["source"], encoding="utf-8"); source_path.chmod(0o600)
        private_rows.append({"task_id": task["id"], "family": task["family"], "variant": task["variant"],
                             "source_path": str(source_path), "source_digest": "sha256:" + hashlib.sha256(source_path.read_bytes()).hexdigest(),
                             "prompt": task["ask"], "gold": task["gold"]})
    private = {"schema_version": SCHEMA, "rows": private_rows}
    private["panel_digest"] = digest(private)
    private_path = out / "tasks-and-gold-private.json"
    private_path.write_text(json.dumps(private, ensure_ascii=False, indent=2) + "\n"); private_path.chmod(0o600)
    sanitized = {"schema_version": SCHEMA, "task_count": len(private_rows), "families": list(FAMILIES),
                 "variants": list(VARIANTS), "tasks": [{key: row[key] for key in ("task_id", "family", "variant", "source_digest")}
                                                      for row in private_rows],
                 "panel_digest": private["panel_digest"], "automatic_admission": False,
                 "human_approval_required": True, "task_outcome_access_before_freeze": False}
    sanitized["sanitized_digest"] = digest(sanitized)
    return sanitized


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--sanitized-out", type=Path, required=True); args = parser.parse_args()
    sanitized = write_panel(args.out)
    args.sanitized_out.write_text(json.dumps(sanitized, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"task_count": sanitized["task_count"], "panel_digest": sanitized["panel_digest"],
                      "sanitized_digest": sanitized["sanitized_digest"]}, sort_keys=True))


if __name__ == "__main__":
    main()

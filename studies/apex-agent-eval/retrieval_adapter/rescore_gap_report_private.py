#!/usr/bin/env python3
"""Correct aggregation semantics for an already completed private gap report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from run_gap_retrieval_private import enforce_adapter_eligible_gold


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    corrected = enforce_adapter_eligible_gold(
        json.loads(Path(args.report).read_text(encoding="utf-8")),
        json.loads(Path(args.manifest).read_text(encoding="utf-8")),
        json.loads(Path(args.catalog).read_text(encoding="utf-8")))
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(corrected, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "out": str(target),
                      "paired_denominator": corrected["paired_pageindex_minus_bm25_at_5"]["denominator"]}))


if __name__ == "__main__":
    main()

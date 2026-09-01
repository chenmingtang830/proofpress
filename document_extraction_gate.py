#!/usr/bin/env python3
"""Frozen, deterministic advancement gate for document extraction routes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

GATE_SCHEMA="proofpress/document-extraction-gate/v1"
THRESHOLDS={"text_blocks_f1":0.90,"table_cells_f1":1.0,"numeric_values_f1":1.0,
            "locator_rate":0.90,"reading_order_rate":0.80,
            "cross_page_continuations_f1":1.0,"repeatability_rate":1.0,
            "conformance_completion_rate":1.0,"ecological_completion_rate":1.0}


def evaluate_gate(conformance: dict[str, Any], ecological: dict[str, Any],
                  *, thresholds: dict[str, float] | None=None) -> dict[str, Any]:
    limits=dict(THRESHOLDS); limits.update(thresholds or {})
    metrics=conformance["metrics"]
    observed={"text_blocks_f1":metrics["text_blocks"]["f1"],
              "table_cells_f1":metrics["table_cells"]["f1"],
              "numeric_values_f1":metrics["numeric_values"]["f1"],
              "locator_rate":metrics["locators"]["rate"],
              "reading_order_rate":metrics["reading_order"]["rate"],
              "cross_page_continuations_f1":metrics["cross_page_continuations"]["f1"],
              "repeatability_rate":metrics["repeatability"]["rate"],
              "conformance_completion_rate":conformance["documents_scored"]/conformance["documents_expected"],
              "ecological_completion_rate":ecological["complete"]/ecological["attempted"] if ecological["attempted"] else 0.0}
    checks={key:{"observed":observed[key],"minimum":minimum,
                 "pass":observed[key] is not None and observed[key]>=minimum}
            for key,minimum in limits.items()}
    invariants={"automatic_admission":conformance.get("automatic_admission") is False and ecological.get("automatic_admission") is False,
                "human_approval_required":conformance.get("human_approval_required") is True and ecological.get("human_approval_required") is True,
                "same_panel_split":"development"==conformance.get("split"),
                "no_heldout_opened":ecological.get("pending",0)>0}
    passed=all(row["pass"] for row in checks.values()) and all(invariants.values())
    return {"schema_version":GATE_SCHEMA,"status":"pass" if passed else "block",
            "thresholds":limits,"checks":checks,"invariants":invariants,
            "heldout_authorized":passed}


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--conformance",required=True,type=Path)
    parser.add_argument("--ecological",required=True,type=Path); parser.add_argument("--out",required=True,type=Path)
    args=parser.parse_args(); result=evaluate_gate(json.loads(args.conformance.read_text()),json.loads(args.ecological.read_text()))
    args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,sort_keys=True))


if __name__=="__main__": main()

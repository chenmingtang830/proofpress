#!/usr/bin/env python3
"""Score completed extraction envelopes against frozen structure ground truth."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[3]; sys.path.insert(0,str(ROOT))
from document_extraction_qualification import score_envelope


def aggregate_fraction(rows: list[dict[str, Any]], field: str) -> dict[str, Any]:
    matched=sum(row[field]["matched"] for row in rows); expected=sum(row[field]["expected"] for row in rows)
    observed=sum(row[field].get("observed",row[field]["expected"]) for row in rows)
    precision=matched/observed if observed else (1.0 if not expected else 0.0)
    recall=matched/expected if expected else 1.0
    return {"matched":matched,"expected":expected,"observed":observed,"precision":precision,
            "recall":recall,"f1":2*precision*recall/(precision+recall) if precision+recall else 0.0}


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--fixture-panel",required=True,type=Path)
    parser.add_argument("--run-dir",required=True,type=Path); parser.add_argument("--out",required=True,type=Path)
    parser.add_argument("--repeat-run-dir",type=Path)
    parser.add_argument("--split",choices=("development","heldout"),default="development"); args=parser.parse_args()
    panel=json.loads(args.fixture_panel.read_text()); gold_by_digest={row["source_content_digest"]:row for row in panel["gold"]}
    cells=[]; missing=[]
    for source in panel["sources"]:
        if source["split"] != args.split: continue
        target=args.run_dir/source["source_id"]; envelope_path=target/"isolated"/"extraction-envelope.json"
        summary_path=target/"run-summary-isolated.json"
        if not summary_path.is_file() or json.loads(summary_path.read_text()).get("status")!="complete" or not envelope_path.is_file():
            missing.append(source["source_id"]); continue
        gold_ref=gold_by_digest[source["content_digest"]]; gold=json.loads(Path(gold_ref["gold_path"]).read_text())
        repeat_digest=None
        if args.repeat_run_dir:
            repeat_path=args.repeat_run_dir/source["source_id"] / "isolated" / "extraction-envelope.json"
            if repeat_path.is_file(): repeat_digest=json.loads(repeat_path.read_text()).get("extraction_digest")
        score=score_envelope(json.loads(envelope_path.read_text()),gold,repeat_extraction_digest=repeat_digest)
        score["case_id"]=gold["case_id"]; cells.append(score)
    metrics={field:aggregate_fraction(cells,field) for field in
             ("text_blocks","table_cells","numeric_values","cross_page_continuations")}
    for field in ("locators","reading_order"):
        matched=sum(row[field]["matched"] for row in cells); expected=sum(row[field]["expected"] for row in cells)
        metrics[field]={"matched":matched,"expected":expected,"rate":matched/expected if expected else 1.0}
    comparable=sum(row["repeatability"]["comparable"] for row in cells)
    identical=sum(row["repeatability"]["identical"] is True for row in cells)
    metrics["repeatability"]={"identical":identical,"comparable":comparable,
                              "rate":identical/comparable if comparable else None}
    report={"schema_version":"proofpress/document-extraction-ground-truth-score/v1",
            "panel_digest":panel["panel_digest"],"split":args.split,
            "documents_expected":sum(source["split"]==args.split for source in panel["sources"]),
            "documents_scored":len(cells),"documents_missing":len(missing),"metrics":metrics,
            "qualification_status":"complete" if not missing else "inconclusive-missing-extractions",
            "automatic_admission":False,"human_approval_required":True,"cells_private":cells,"missing_private":missing}
    args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n"); args.out.chmod(0o600)
    print(json.dumps({key:value for key,value in report.items() if key not in {"cells_private","missing_private"}},sort_keys=True))


if __name__=="__main__": main()

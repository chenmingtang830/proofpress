#!/usr/bin/env python3
"""Execute a frozen extraction panel with one reused PaddleOCR-VL instance."""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import signal
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from document_extraction_adapters import paddle_result_to_envelope


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return "sha256:" + value.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--panel", required=True, type=Path)
    parser.add_argument("--source-manifest", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--pages-per-document", type=int, default=1)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--document-timeout-seconds", type=int, default=600)
    args = parser.parse_args()
    if args.pages_per_document < 1 or args.document_timeout_seconds < 1:
        raise SystemExit("page count and document timeout must be positive")

    import numpy as np
    import pypdfium2 as pdfium
    from paddleocr import PaddleOCRVL

    panel = json.loads(args.panel.read_text()); manifest = json.loads(args.source_manifest.read_text())
    paths = {}
    for source in manifest["sources"]:
        path = Path(source["path"]).resolve(); paths[file_digest(path)] = (path, source)
    args.out.mkdir(parents=True, exist_ok=True); args.out.chmod(0o700)
    pipeline_started = time.monotonic()
    pipeline = PaddleOCRVL(pipeline_version="v1.6", device=args.device)
    cells = []

    def timeout_handler(signum, frame):
        raise TimeoutError("document extraction exceeded the frozen wall-time circuit")

    signal.signal(signal.SIGALRM, timeout_handler)
    for item in panel["sources"]:
        started = time.monotonic(); path, manifest_source = paths[item["content_digest"]]
        target = args.out / item["source_id"]; target.mkdir(exist_ok=True); target.chmod(0o700)
        summary_path = target / "run-summary.json"
        if summary_path.is_file():
            cells.append(json.loads(summary_path.read_text()))
            continue
        try:
            signal.alarm(args.document_timeout_seconds)
            document = pdfium.PdfDocument(str(path)); results = []
            for page_index in range(min(len(document), args.pages_per_document)):
                image = np.asarray(document[page_index].render(scale=2).to_pil())
                predictions = list(pipeline.predict(image, temperature=0))
                if len(predictions) != 1:
                    raise RuntimeError("one result per page is required")
                raw = predictions[0].json["res"]; raw["page_index"] = page_index; results.append(raw)
            source = {"uri": manifest_source["uri"], "content_digest": item["content_digest"],
                      "media_type": manifest_source.get("media_type", "application/pdf")}
            envelope = paddle_result_to_envelope(
                {"pages": results}, source=source, version="1.6",
                config={"pipeline_version": "v1.6", "device": args.device,
                        "pages_per_document": args.pages_per_document, "temperature_requested": 0,
                        "temperature_support": "ignored_by-local-model"})
            envelope_path = target / "extraction-envelope.json"
            envelope_path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n")
            envelope_path.chmod(0o600)
            row = {"source_id": item["source_id"], "split": item["split"], "status": "complete",
                   "pages_processed": len(results), "blocks": len(envelope["blocks"]),
                   "tables": len(envelope["tables"]), "cells": sum(len(t["cells"]) for t in envelope["tables"]),
                   "extraction_digest": envelope["extraction_digest"],
                   "elapsed_seconds": round(time.monotonic() - started, 3)}
        except Exception as exc:
            row = {"source_id": item["source_id"], "split": item["split"], "status": "failed",
                   "failure_type": type(exc).__name__,
                   "failure_digest": "sha256:" + hashlib.sha256(str(exc).encode()).hexdigest(),
                   "elapsed_seconds": round(time.monotonic() - started, 3)}
        finally:
            signal.alarm(0)
        cells.append(row)
        summary_path.write_text(json.dumps(row, indent=2, sort_keys=True) + "\n")
        if row.get("failure_type") == "TimeoutError":
            # Paddle's internal VLM worker may outlive the interrupted request.
            # Stop this process and require content-addressed resume in a fresh
            # process so later documents are not contaminated by stale work.
            break
    complete = [row for row in cells if row["status"] == "complete"]
    report = {"schema_version": "proofpress/document-extraction-panel-run/v1",
              "panel_digest": panel["panel_digest"], "route": "PaddlePaddle/PaddleOCR-VL-1.6",
              "host": {"architecture": "Apple-Silicon", "device": args.device},
              "document_timeout_seconds": args.document_timeout_seconds,
              "documents": len(panel["sources"]), "attempted": len(cells),
              "pending": len(panel["sources"]) - len(cells),
              "complete": len(complete), "failed": len(cells) - len(complete),
              "pages_processed": sum(row.get("pages_processed", 0) for row in complete),
              "blocks": sum(row.get("blocks", 0) for row in complete),
              "tables": sum(row.get("tables", 0) for row in complete),
              "cells": sum(row.get("cells", 0) for row in complete),
              "elapsed_seconds": round(time.monotonic() - pipeline_started, 3),
              "peak_rss_mib": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024), 1),
              "known_model_cost_usd": 0, "automatic_admission": False,
              "human_approval_required": True,
              "qualification_status": "awaiting-structure-ground-truth-review",
              "cells_private": cells}
    target = args.out / "sanitized-report.json"; target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n"); target.chmod(0o600)
    print(json.dumps({key: value for key, value in report.items() if key != "cells_private"}, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Run PaddleOCR-VL into source-bound private extraction envelopes."""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
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
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--uri", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--max-pages", type=int, default=1)
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()
    if args.max_pages < 1:
        raise SystemExit("max-pages must be positive")

    # Heavy optional dependencies stay outside the product environment.
    import numpy as np
    import pypdfium2 as pdfium
    from paddleocr import PaddleOCRVL

    args.out.mkdir(parents=True, exist_ok=True); args.out.chmod(0o700)
    source = {"uri": args.uri, "content_digest": file_digest(args.input),
              "media_type": "application/pdf"}
    config = {"pipeline_version": "v1.6", "device": args.device,
              "max_pages": args.max_pages, "temperature": 0}
    started = time.monotonic()
    pipeline = PaddleOCRVL(pipeline_version="v1.6", device=args.device)
    document = pdfium.PdfDocument(str(args.input)); results = []
    for page_index in range(min(len(document), args.max_pages)):
        bitmap = document[page_index].render(scale=2)
        image = np.asarray(bitmap.to_pil())
        items = list(pipeline.predict(image, temperature=0))
        if len(items) != 1:
            raise RuntimeError("PaddleOCR-VL did not return exactly one page result")
        raw = items[0].json["res"]
        raw["page_index"] = page_index
        results.append(raw)
        private = args.out / f"raw-page-{page_index + 1}.json"
        private.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n")
        private.chmod(0o600)
    envelope = paddle_result_to_envelope({"pages": results}, source=source,
                                         version="1.6", config=config)
    envelope_path = args.out / "extraction-envelope.json"
    envelope_path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n")
    envelope_path.chmod(0o600)
    report = {"schema_version": "proofpress/document-extraction-run/v1",
              "status": "complete", "source_content_digest": source["content_digest"],
              "extraction_digest": envelope["extraction_digest"],
              "pages_processed": len(results), "blocks": len(envelope["blocks"]),
              "tables": len(envelope["tables"]),
              "elapsed_seconds": round(time.monotonic() - started, 3),
              "peak_rss_mib": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024), 1),
              "known_model_cost_usd": 0, "automatic_admission": False,
              "human_approval_required": True}
    report_path = args.out / "sanitized-report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    report_path.chmod(0o600)
    print(json.dumps({"ok": True, "report": str(report_path), **report}, sort_keys=True))


if __name__ == "__main__":
    main()

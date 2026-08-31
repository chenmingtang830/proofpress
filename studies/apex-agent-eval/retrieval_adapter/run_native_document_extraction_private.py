#!/usr/bin/env python3
"""Run the existing native PDF text representation as a B.5 control."""
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

from document_extraction_adapters import native_text_to_envelope


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
    from pypdf import PdfReader

    args.out.mkdir(parents=True, exist_ok=True); args.out.chmod(0o700)
    source = {"uri": args.uri, "content_digest": file_digest(args.input),
              "media_type": "application/pdf"}
    started = time.monotonic()
    reader = PdfReader(str(args.input))
    pages = [{"page": page_index + 1, "text": reader.pages[page_index].extract_text() or ""}
             for page_index in range(min(len(reader.pages), args.max_pages))]
    envelope = native_text_to_envelope(pages, source=source,
                                       config={"adapter": "native-pdf-text/v1", "max_pages": args.max_pages})
    envelope_path = args.out / "extraction-envelope.json"
    envelope_path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n")
    envelope_path.chmod(0o600)
    report = {"schema_version": "proofpress/document-extraction-run/v1", "status": "complete",
              "source_content_digest": source["content_digest"], "extraction_digest": envelope["extraction_digest"],
              "pages_processed": len(pages), "blocks": len(envelope["blocks"]), "tables": 0, "cells": 0,
              "elapsed_seconds": round(time.monotonic() - started, 3),
              "peak_rss_mib": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024), 1),
              "backend": "native_pdf_text", "known_model_cost_usd": 0,
              "automatic_admission": False, "human_approval_required": True}
    report_path = args.out / "sanitized-report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    report_path.chmod(0o600)
    print(json.dumps({"ok": True, "report": str(report_path), **report}, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Run the official DeepSeek-OCR-2 Transformers path into an extraction envelope.

This sensitivity route is intentionally CUDA-only.  A non-CUDA host fails
before it opens source bytes; it is never silently replaced with CPU, MPS, or
another model.
"""
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

from document_extraction_adapters import deepseek_markdown_to_envelope
from document_extraction_contract import digest


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
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--model-name", default="deepseek-ai/DeepSeek-OCR-2")
    parser.add_argument("--model-revision", required=True)
    args = parser.parse_args()
    if args.max_pages < 1:
        raise SystemExit("max-pages must be positive")
    if args.device != "cuda":
        raise SystemExit("DeepSeek-OCR-2 sensitivity route requires device=cuda")
    try:
        import torch
    except ModuleNotFoundError as exc:
        raise SystemExit("DeepSeek-OCR-2 sensitivity route requires a compatible CUDA host") from exc
    if not torch.cuda.is_available():
        raise SystemExit("DeepSeek-OCR-2 sensitivity route requires a compatible CUDA host")

    # Imports occur after the hard capability check: no source bytes are opened
    # on an unsupported host.
    import numpy as np
    import pypdfium2 as pdfium
    from transformers import AutoModel, AutoTokenizer

    args.out.mkdir(parents=True, exist_ok=True); args.out.chmod(0o700)
    source = {"uri": args.uri, "content_digest": file_digest(args.input),
              "media_type": "application/pdf"}
    config = {"backend": "official-transformers", "device": "cuda", "prompt": "grounding-markdown",
              "base_size": 1024, "image_size": 768, "crop_mode": True,
              "model_name": args.model_name, "model_revision": args.model_revision}
    started = time.monotonic()
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, revision=args.model_revision, trust_remote_code=True)
    model = AutoModel.from_pretrained(args.model_name, revision=args.model_revision,
                                      _attn_implementation="flash_attention_2", trust_remote_code=True,
                                      use_safetensors=True).eval().cuda().to(torch.bfloat16)
    document = pdfium.PdfDocument(str(args.input)); markdown_pages = []
    for page_index in range(min(len(document), args.max_pages)):
        image_path = args.out / f"render-{page_index + 1}.png"
        bitmap = document[page_index].render(scale=2)
        bitmap.to_pil().save(image_path)
        page_out = args.out / f"deepseek-page-{page_index + 1}"
        page_out.mkdir(exist_ok=True)
        result = model.infer(tokenizer, prompt="<image>\n<|grounding|>Convert the document to markdown. ",
                             image_file=str(image_path), output_path=str(page_out), base_size=1024,
                             image_size=768, crop_mode=True, save_results=True)
        markdown_pages.append({"page": page_index + 1, "markdown": str(result),
                               "render_digest": digest({"source_content_digest": source["content_digest"],
                                                        "page": page_index + 1, "scale": 2})})
    envelope = deepseek_markdown_to_envelope(markdown_pages, source=source, version="2", config=config)
    envelope_path = args.out / "extraction-envelope.json"
    envelope_path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n"); envelope_path.chmod(0o600)
    report = {"schema_version": "proofpress/document-extraction-run/v1", "status": "complete",
              "source_content_digest": source["content_digest"], "extraction_digest": envelope["extraction_digest"],
              "pages_processed": len(markdown_pages), "blocks": len(envelope["blocks"]),
              "tables": len(envelope["tables"]), "cells": sum(len(table["cells"]) for table in envelope["tables"]),
              "elapsed_seconds": round(time.monotonic() - started, 3),
              "peak_rss_mib": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024), 1),
              "backend": "official-transformers", "known_model_cost_usd": 0,
              "automatic_admission": False, "human_approval_required": True}
    report_path = args.out / "sanitized-report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n"); report_path.chmod(0o600)
    print(json.dumps({"ok": True, "report": str(report_path), **report}, sort_keys=True))


if __name__ == "__main__":
    main()

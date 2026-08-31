#!/usr/bin/env python3
"""Run the frozen extraction panel through the CUDA-only DeepSeek adapter.

This is deliberately a thin, source-blind invocation wrapper.  It pins the
only permitted route/device combination and delegates the CUDA preflight to
the panel runner, which executes before it opens the private panel or source
manifest.  The model revision remains an explicit immutable input: this
repository never substitutes a branch, a local model, CPU, or MPS fallback.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PANEL_RUNNER = HERE / "run_paddle_extraction_panel_private.py"
CHILD_RUNNER = HERE / "run_deepseek_ocr2_private.py"
REVISION = re.compile(r"^[0-9a-f]{40}$")


def command(args: argparse.Namespace) -> list[str]:
    if not REVISION.fullmatch(args.model_revision):
        raise ValueError("DeepSeek model revision must be a pinned 40-character git commit")
    result = [sys.executable, str(PANEL_RUNNER), "--panel", str(args.panel),
              "--source-manifest", str(args.source_manifest), "--out", str(args.out),
              "--pages-per-document", str(args.pages_per_document), "--device", "cuda",
              "--require-cuda", "--document-timeout-seconds", str(args.document_timeout_seconds),
              "--route", "deepseek-ai/DeepSeek-OCR-2/official-transformers",
              "--child-runner", str(CHILD_RUNNER), "--child-extra=--model-revision",
              "--child-extra", args.model_revision]
    if args.include_heldout:
        result.append("--include-heldout")
    if args.retry_failed_development:
        result.append("--retry-failed-development")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--panel", required=True, type=Path)
    parser.add_argument("--source-manifest", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--model-revision", required=True)
    parser.add_argument("--pages-per-document", type=int, default=1)
    parser.add_argument("--document-timeout-seconds", type=int, default=600)
    parser.add_argument("--include-heldout", action="store_true")
    parser.add_argument("--retry-failed-development", action="store_true")
    args = parser.parse_args()
    if args.pages_per_document < 1 or args.document_timeout_seconds < 1:
        raise SystemExit("page count and document timeout must be positive")
    try:
        result = subprocess.run(command(args), check=False)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()

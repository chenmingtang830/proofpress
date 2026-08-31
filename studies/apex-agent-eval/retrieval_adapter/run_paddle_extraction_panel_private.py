#!/usr/bin/env python3
"""Execute a frozen Paddle panel with one killable process per document."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

CHILD = Path(__file__).with_name("run_paddle_document_extraction_private.py")


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return "sha256:" + value.hexdigest()


def receipt_digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _terminate_group(process: subprocess.Popen[str]) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=5)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=5)


def isolated_run(command: list[str], timeout: int) -> dict[str, object]:
    started = time.monotonic()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
        status = "complete" if process.returncode == 0 else "failed"
        return {"status": status, "returncode": process.returncode,
                "stdout_digest": receipt_digest(stdout), "stderr_digest": receipt_digest(stderr),
                "elapsed_seconds": round(time.monotonic() - started, 3)}
    except subprocess.TimeoutExpired:
        _terminate_group(process)
        process.communicate()
        return {"status": "failed", "failure_type": "TimeoutExpired",
                "returncode": process.returncode,
                "stdout_digest": receipt_digest("timeout-output-withheld"),
                "stderr_digest": receipt_digest("timeout-output-withheld"),
                "elapsed_seconds": round(time.monotonic() - started, 3)}


def backfill_cells(row: dict[str, object], target: Path) -> dict[str, object]:
    if row.get("status") != "complete" or "cells" in row:
        return row
    envelope_path = target / "isolated" / "extraction-envelope.json"
    if envelope_path.is_file():
        envelope = json.loads(envelope_path.read_text())
        row["cells"] = sum(len(table["cells"]) for table in envelope["tables"])
    return row


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--panel", required=True, type=Path)
    parser.add_argument("--source-manifest", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--pages-per-document", type=int, default=1)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--document-timeout-seconds", type=int, default=600)
    parser.add_argument("--retry-failed-development", action="store_true")
    parser.add_argument("--include-heldout", action="store_true",
                        help="Open held-out only after the development gate is frozen as passed.")
    parser.add_argument("--vl-rec-backend")
    parser.add_argument("--vl-rec-server-url")
    parser.add_argument("--vl-rec-api-model-name",default="PaddlePaddle/PaddleOCR-VL-1.6")
    parser.add_argument("--vl-rec-model-revision")
    parser.add_argument("--child-runner", type=Path, default=CHILD)
    parser.add_argument("--child-extra", action="append", default=[],
                        help="One literal argument forwarded to an alternate child runner.")
    parser.add_argument("--route", default="PaddlePaddle/PaddleOCR-VL-1.6/paddle_dynamic")
    args = parser.parse_args()
    if args.pages_per_document < 1 or args.document_timeout_seconds < 1:
        raise SystemExit("page count and document timeout must be positive")

    panel = json.loads(args.panel.read_text()); manifest = json.loads(args.source_manifest.read_text())
    paths = {}
    for source in manifest["sources"]:
        path = Path(source["path"]).resolve(); paths[file_digest(path)] = (path, source)
    args.out.mkdir(parents=True, exist_ok=True); args.out.chmod(0o700)
    started = time.monotonic(); rows = []
    for item in panel["sources"]:
        if item["split"] == "heldout" and not args.include_heldout:
            break
        path, manifest_source = paths[item["content_digest"]]
        target = args.out / item["source_id"]; target.mkdir(exist_ok=True); target.chmod(0o700)
        summary_path = target / "run-summary-isolated.json"
        if summary_path.is_file():
            saved = backfill_cells(json.loads(summary_path.read_text()), target)
            if not (args.retry_failed_development and item["split"] == "development"
                    and saved.get("status") == "failed"):
                rows.append(saved); continue
        command = [sys.executable, str(args.child_runner), "--input", str(path), "--uri",
                   manifest_source["uri"], "--out", str(target / "isolated"),
                   "--max-pages", str(args.pages_per_document), "--device", args.device]
        command.extend(args.child_extra)
        if args.vl_rec_backend:
            if not args.vl_rec_server_url: raise SystemExit("vl-rec-server-url is required with a backend")
            command.extend(["--vl-rec-backend",args.vl_rec_backend,"--vl-rec-server-url",args.vl_rec_server_url,
                            "--vl-rec-api-model-name",args.vl_rec_api_model_name])
            if args.vl_rec_model_revision:
                command.extend(["--vl-rec-model-revision", args.vl_rec_model_revision])
        terminal = isolated_run(command, args.document_timeout_seconds)
        child_report_path = target / "isolated" / "sanitized-report.json"
        if terminal["status"] == "complete" and child_report_path.is_file():
            child = json.loads(child_report_path.read_text())
            envelope_path = target / "isolated" / "extraction-envelope.json"
            envelope = json.loads(envelope_path.read_text()) if envelope_path.is_file() else {"tables": []}
            cell_count = child.get("cells", sum(len(table["cells"]) for table in envelope["tables"]))
            row = {"source_id": item["source_id"], "split": item["split"],
                   "pages_processed": child["pages_processed"], "blocks": child["blocks"],
                   "tables": child["tables"], "cells": cell_count,
                   "extraction_digest": child["extraction_digest"],
                   "peak_rss_mib": child["peak_rss_mib"], **terminal}
        else:
            row = {"source_id": item["source_id"], "split": item["split"], **terminal}
        row["terminal_receipt_digest"] = receipt_digest(row)
        summary_path.write_text(json.dumps(row, indent=2, sort_keys=True) + "\n")
        summary_path.chmod(0o600); rows.append(row)
    complete = [row for row in rows if row["status"] == "complete"]
    report = {"schema_version": "proofpress/document-extraction-panel-run/v2",
              "panel_digest": panel["panel_digest"],
              "route": ("PaddlePaddle/PaddleOCR-VL-1.6/" + args.vl_rec_backend
                        if args.vl_rec_backend else args.route),
              "isolation": "one-process-group-per-document/v1",
              "host": {"architecture": "Apple-Silicon", "device": args.device},
              "document_timeout_seconds": args.document_timeout_seconds,
              "documents": len(panel["sources"]), "attempted": len(rows),
              "pending": len(panel["sources"]) - len(rows), "complete": len(complete),
              "failed": len(rows) - len(complete),
              "pages_processed": sum(row.get("pages_processed", 0) for row in complete),
              "blocks": sum(row.get("blocks", 0) for row in complete),
              "tables": sum(row.get("tables", 0) for row in complete),
              "cells": sum(row.get("cells", 0) for row in complete),
              "elapsed_seconds": round(time.monotonic() - started, 3),
              "peak_child_rss_mib": max((row.get("peak_rss_mib", 0) for row in complete), default=0),
              "known_model_cost_usd": 0, "automatic_admission": False,
              "human_approval_required": True,
              "qualification_status": "awaiting-structure-ground-truth-review",
              "cells_private": rows}
    target = args.out / "sanitized-report-isolated.json"
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n"); target.chmod(0o600)
    print(json.dumps({key: value for key, value in report.items() if key != "cells_private"}, sort_keys=True))


if __name__ == "__main__":
    main()

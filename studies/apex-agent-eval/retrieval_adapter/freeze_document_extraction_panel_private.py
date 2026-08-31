#!/usr/bin/env python3
"""Freeze an outcome-blind document panel for extraction qualification."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "proofpress/document-extraction-panel/v1"


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return "sha256:" + value.hexdigest()


def digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def freeze(manifest: dict[str, Any], *, development_count: int,
           heldout_count: int) -> dict[str, Any]:
    sources = manifest.get("sources")
    if not isinstance(sources, list) or development_count < 1 or heldout_count < 1:
        raise ValueError("non-empty development and held-out source counts are required")
    rows = []
    for source in sources:
        path = Path(source["path"]).resolve()
        if not path.is_file():
            raise ValueError("panel source is not a file")
        content_digest = file_digest(path)
        if source.get("content_digest") and source["content_digest"] != content_digest:
            raise ValueError("panel source digest mismatch")
        rows.append({"source_id": "source_" + content_digest[7:27],
                     "uri_digest": digest(source["uri"]),
                     "content_digest": content_digest,
                     "media_type": source.get("media_type", "application/octet-stream"),
                     "byte_length": path.stat().st_size,
                     "selection_key": digest({"content_digest": content_digest,
                                              "purpose": "extraction-panel-v1"})})
    rows.sort(key=lambda row: row["selection_key"])
    required = development_count + heldout_count
    if len(rows) < required:
        raise ValueError("source manifest is smaller than the requested panel")
    selected = rows[:required]
    for index, row in enumerate(selected):
        row["split"] = "development" if index < development_count else "heldout"
        del row["selection_key"]
    panel = {"schema_version": SCHEMA, "selection": "digest-order-outcome-blind/v1",
             "development_count": development_count, "heldout_count": heldout_count,
             "sources": selected,
             "routes": ["current-canonical-native-representation",
                        "PaddlePaddle/PaddleOCR-VL-1.6",
                        "deepseek-ai/DeepSeek-OCR-2"],
             "deepseek_host_requirement": "recorded-compatible-CUDA-host-required",
             "downstream_task_outcome_access": False, "automatic_admission": False,
             "human_approval_required": True}
    panel["panel_digest"] = digest(panel)
    return panel


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-manifest", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--development-count", type=int, default=4)
    parser.add_argument("--heldout-count", type=int, default=8)
    args = parser.parse_args()
    panel = freeze(json.loads(args.source_manifest.read_text()),
                   development_count=args.development_count,
                   heldout_count=args.heldout_count)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(panel, indent=2, sort_keys=True) + "\n")
    args.out.chmod(0o600)
    print(json.dumps({"ok": True, "panel_digest": panel["panel_digest"],
                      "development": panel["development_count"],
                      "heldout": panel["heldout_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()

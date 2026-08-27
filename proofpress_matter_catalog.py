#!/usr/bin/env python3
"""Deterministic, source-custody-first matter evidence catalog.

The catalog is a retrieval substrate only.  It never creates claims, changes
the knowledge ref, or grants authority.  A caller supplies a manifest with
``path``, ``uri`` and ``media_type`` entries; every representation is bound to
the original SHA-256 and a transform/config digest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mailbox
import os
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser
from pathlib import Path
from typing import Any

SCHEMA = "proofpress/matter-evidence-catalog/v1"
RENDERER_VERSION = "deterministic-renderer/v1"


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canon(value)).hexdigest()


def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return "sha256:" + h.hexdigest()


def _text_pages(text: str) -> list[str]:
    pages = text.replace("\r\n", "\n").replace("\r", "\n").split("\f")
    return pages or [""]


def _json_text(raw: bytes) -> str:
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return raw.decode("utf-8", errors="replace")
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def _mbox_text(path: Path) -> str:
    lines = []
    box = mailbox.mbox(path, create=False)
    for index, message in enumerate(box):
        lines.append(f"Message {index + 1}")
        lines.append(message.as_string(policy=policy.default))
        lines.append("")
    return "\n".join(lines)


def _office_text(path: Path, libreoffice: str | None) -> str:
    executable = libreoffice or os.environ.get("PROOFPRESS_LIBREOFFICE", "soffice")
    with tempfile.TemporaryDirectory(prefix="proofpress-office-") as tmp:
        target = Path(tmp)
        result = subprocess.run([executable, "--headless", "--convert-to", "txt:Text",
                                 "--outdir", str(target), str(path)],
                                capture_output=True, text=True)
        if result.returncode:
            raise ValueError("fixed LibreOffice renderer failed closed: " +
                             (result.stderr.strip() or result.stdout.strip() or "non-zero exit"))
        rendered = target / (path.stem + ".txt")
        if not rendered.exists():
            raise ValueError("fixed LibreOffice renderer did not produce text")
        return rendered.read_text(encoding="utf-8", errors="replace")


def render_source(path: Path, media_type: str, libreoffice: str | None = None) -> tuple[list[str], dict[str, Any]]:
    raw = path.read_bytes()
    lower = media_type.lower()
    transform = {"renderer": RENDERER_VERSION, "media_type": media_type}
    # PDFs remain byte-faithful.  Text is represented as one deterministic
    # page unless a form-feed marker is supplied by a fixture/parser.
    if lower == "application/pdf" or path.suffix.lower() == ".pdf":
        pages = [raw.decode("utf-8", errors="replace")]
        transform["mode"] = "pdf-original"
    elif lower in {"application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                   "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                   "application/msword", "application/vnd.ms-excel"} or path.suffix.lower() in {".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"}:
        pages = _text_pages(_office_text(path, libreoffice))
        transform["mode"] = "libreoffice-text"
    elif lower in {"application/json", "application/ld+json"} or path.suffix.lower() == ".json":
        pages = _text_pages(_json_text(raw)); transform["mode"] = "json-canonical"
    elif lower in {"message/rfc822", "application/mbox"} or path.suffix.lower() in {".mbox", ".eml"}:
        pages = _text_pages(_mbox_text(path)); transform["mode"] = "mbox-canonical"
    else:
        pages = _text_pages(raw.decode("utf-8", errors="replace")); transform["mode"] = "text-canonical"
    return pages, transform


def _sections(page: str, page_number: int) -> list[dict[str, Any]]:
    lines = page.splitlines(keepends=True)
    sections, start, buffer, heading = [], 0, [], None
    def flush(end: int) -> None:
        nonlocal buffer, start, heading
        text = "".join(buffer)
        if not text.strip():
            buffer = []; return
        section_id = "sec_" + hashlib.sha256((str(page_number) + "\n" + str(start) + "\n" + text).encode()).hexdigest()[:16]
        sections.append({"id": section_id, "heading": heading,
                         "page_start": page_number, "page_end": page_number,
                         "text": text, "text_digest": "sha256:" + hashlib.sha256(text.encode()).hexdigest(),
                         "line_start": start, "line_end": end})
        buffer = []; heading = None; start = end
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped and (stripped.startswith("#") or (len(stripped) < 120 and stripped.isupper())):
            flush(index)
            heading = stripped.lstrip("# ")
            start = index
        buffer.append(line)
    flush(len(lines))
    return sections


def build_catalog(manifest: str | os.PathLike[str] | dict[str, Any], *, cache_dir: str | os.PathLike[str] | None = None,
                  libreoffice: str | None = None) -> dict[str, Any]:
    if isinstance(manifest, (str, os.PathLike)):
        manifest_path = Path(manifest)
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest_path = None
        payload = manifest
    rows = payload.get("sources") if isinstance(payload, dict) else None
    if not isinstance(rows, list) or not rows:
        raise ValueError("matter catalog manifest requires non-empty sources")
    transform_config = {"renderer_version": RENDERER_VERSION,
                        "libreoffice": libreoffice or os.environ.get("PROOFPRESS_LIBREOFFICE", "soffice")}
    transform_digest = digest(transform_config)
    sources, representations = [], []
    cache = Path(cache_dir) if cache_dir else None
    if cache: cache.mkdir(parents=True, exist_ok=True)
    for raw in rows:
        if not isinstance(raw, dict) or not isinstance(raw.get("path"), str) or not isinstance(raw.get("uri"), str):
            raise ValueError("each matter catalog source requires path and uri")
        path = Path(raw["path"]).resolve()
        if not path.is_file(): raise ValueError("matter catalog source is not a file: " + str(path))
        source_sha = file_digest(path)
        if raw.get("content_digest") and raw["content_digest"] != source_sha:
            raise ValueError("matter catalog source digest mismatch: " + raw["uri"])
        media = raw.get("media_type") or "application/octet-stream"
        source = {"uri": raw["uri"], "media_type": media, "content_digest": source_sha,
                  "byte_length": path.stat().st_size}
        source["source_digest"] = digest(source)
        sources.append(source)
        key = hashlib.sha256((source_sha + "\n" + transform_digest).encode()).hexdigest()
        cached = cache / (key + ".json") if cache else None
        item = None
        if cached and cached.exists():
            try:
                candidate = json.loads(cached.read_text(encoding="utf-8"))
                if candidate.get("source", {}).get("content_digest") == source_sha and candidate.get("transform_digest") == transform_digest:
                    # Representation bytes/sections are content-addressed, but
                    # custody identity is per manifest URI.  Rebind the cached
                    # representation to the current source so identical files
                    # at distinct paths never inherit one another's URI.
                    item = candidate
                    item["source"] = source
            except (OSError, json.JSONDecodeError):
                item = None
        if item is None:
            pages, transform = render_source(path, media, libreoffice)
            sections = []
            for number, page in enumerate(pages, 1): sections.extend(_sections(page, number))
            item = {"source": source, "representation_digest": digest({"pages": pages, "sections": sections}),
                    "transform_digest": transform_digest, "transform": transform,
                    "page_count": len(pages), "pages": [{"page": i + 1, "text_digest": "sha256:" + hashlib.sha256(page.encode()).hexdigest()} for i, page in enumerate(pages)],
                    "sections": sections}
            if cached: cached.write_text(json.dumps(item, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        representations.append(item)
    return {"schema_version": SCHEMA, "sources": sources, "representations": representations,
            "manifest_digest": digest(sources), "transform_config": transform_config,
            "transform_digest": transform_digest, "catalog_digest": digest(representations),
            "source_navigation": [{"uri": row["uri"], "path": raw["path"]} for row, raw in zip(sources, rows)]}


def main() -> None:
    parser = argparse.ArgumentParser(description="build a source-custody-first Proofpress matter catalog")
    parser.add_argument("manifest"); parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--cache-dir"); parser.add_argument("--libreoffice")
    args = parser.parse_args()
    result = build_catalog(args.manifest, cache_dir=args.cache_dir, libreoffice=args.libreoffice)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "schema_version": SCHEMA,
                      "sources": len(result["sources"]), "representations": len(result["representations"]),
                      "catalog_digest": result["catalog_digest"]}))


if __name__ == "__main__": main()

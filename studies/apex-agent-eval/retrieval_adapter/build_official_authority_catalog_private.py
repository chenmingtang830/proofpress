#!/usr/bin/env python3
"""Fetch a frozen, official-only authority catalog for private evaluation.

The catalog provides custody-bound candidates only.  Official provenance does
not admit an authority node or establish that it controls a particular matter.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

from exact_knowledge_contract import AUTHORITY_LEVELS, OFFICIAL_AUTHORITY_HOSTS, digest


SCHEMA = "proofpress/official-authority-source-manifest/v1"
CATALOG_SCHEMA = "proofpress/official-authority-catalog/v1"


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(); self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def _plain_text(raw: bytes, media_type: str) -> str:
    decoded = raw.decode("utf-8", errors="replace")
    if "xml" in media_type:
        root = ET.fromstring(decoded)
        text = "\n".join(value.strip() for value in root.itertext() if value.strip())
    else:
        parser = _TextExtractor(); parser.feed(decoded)
        text = "\n".join(value.strip() for value in parser.parts if value.strip())
    return re.sub(r"[ \t]+", " ", re.sub(r"\n{3,}", "\n\n", text)).strip()


def _fetch(entry: dict[str, object], timeout: float) -> tuple[bytes, str]:
    uri = str(entry["uri"])
    host = urlparse(uri).hostname
    if urlparse(uri).scheme != "https" or host not in OFFICIAL_AUTHORITY_HOSTS:
        raise ValueError("authority source must use an allowlisted official HTTPS host")
    request = urllib.request.Request(uri, headers={"User-Agent": "Proofpress private research audit"})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read(8_000_001)
                media_type = response.headers.get_content_type()
            break
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(attempt + 1)
    else:
        raise RuntimeError(f"official authority fetch failed for {uri}") from last_error
    if len(raw) > 8_000_000:
        raise ValueError("authority source exceeds the private catalog size limit")
    return raw, media_type


def _chunks(text: str, citation: str, limit: int = 5000) -> list[str]:
    paragraphs = [row.strip() for row in text.split("\n") if row.strip()]
    chunks: list[str] = []; current: list[str] = []
    for paragraph in paragraphs:
        if current and len("\n".join(current)) + len(paragraph) + 1 > limit:
            chunks.append("\n".join(current)); current = []
        if len(paragraph) > limit:
            for start in range(0, len(paragraph), limit):
                if current:
                    chunks.append("\n".join(current)); current = []
                chunks.append(paragraph[start:start + limit])
        else:
            current.append(paragraph)
    if current:
        chunks.append("\n".join(current))
    prefix = f"Canonical source citation: {citation}\nSource excerpt:\n"
    return [prefix + row for row in chunks]


def build(manifest: dict[str, object], timeout: float) -> dict[str, object]:
    if manifest.get("schema_version") != SCHEMA:
        raise ValueError("official authority manifest schema is required")
    rows = manifest.get("sources")
    if not isinstance(rows, list) or not rows:
        raise ValueError("official authority manifest needs sources")
    representations = []
    seen = set()
    for index, entry in enumerate(rows, 1):
        if not isinstance(entry, dict):
            raise ValueError("official authority source entry must be an object")
        required = ("uri", "canonical_citations", "jurisdiction", "effective_on", "authority_level")
        if any(not entry.get(key) for key in required):
            raise ValueError("official authority source metadata is incomplete")
        if entry["uri"] in seen or entry["authority_level"] not in AUTHORITY_LEVELS:
            raise ValueError("official authority source identity or level is invalid")
        citations = entry["canonical_citations"]
        if not isinstance(citations, list) or not citations or any(not isinstance(row, str) for row in citations):
            raise ValueError("official authority citations must be a non-empty string list")
        raw, media_type = _fetch(entry, timeout)
        text = _plain_text(raw, media_type)
        if any(citation not in text for citation in citations):
            raise ValueError("canonical authority citation is absent from fetched source text")
        source = {
            "uri": entry["uri"], "media_type": media_type,
            "content_digest": "sha256:" + hashlib.sha256(raw).hexdigest(),
            "official_authority": {
                "official": True, "jurisdiction": entry["jurisdiction"],
                "effective_on": entry["effective_on"], "authority_level": entry["authority_level"],
                "canonical_citations": citations,
            },
        }
        sections = []
        for chunk_index, chunk in enumerate(_chunks(text, citations[0]), 1):
            section_id = f"authority_{index:03d}_{chunk_index:03d}"
            sections.append({"id": section_id, "heading": citations[0], "text": chunk,
                             "text_digest": digest(chunk), "page_start": chunk_index,
                             "page_end": chunk_index, "line_start": 1,
                             "line_end": chunk.count("\n") + 1})
        representation = {"source": source, "sections": sections,
                          "transform": "normalized_text_chunks_with_canonical_citation_header/v1"}
        representation["representation_digest"] = digest(representation)
        representations.append(representation); seen.add(entry["uri"])
    result = {"schema_version": CATALOG_SCHEMA,
              "manifest_digest": digest(manifest), "representations": representations}
    result["catalog_digest"] = digest(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=60)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    catalog = build(manifest, args.timeout)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(catalog, indent=2, sort_keys=True) + "\n")
    args.out.chmod(0o600)
    print(json.dumps({"sources": len(catalog["representations"]),
                      "catalog_digest": catalog["catalog_digest"]}, sort_keys=True))


if __name__ == "__main__":
    main()

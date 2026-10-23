"""Build one retrieval envelope from explicitly selected local files; never submit it.

The caller extracts UTF-8 text first and records the actual extraction configuration.
This helper does not crawl directories or extract arbitrary document formats.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(body: bytes) -> str:
    return "sha256:" + hashlib.sha256(body).hexdigest()


def prepare(source: Path, text: Path, quote_file: Path, config: Path, query: str,
            adapter: str, version: str, page: int | None = None) -> dict:
    projection = text.read_bytes()
    content = projection.decode("utf-8")
    quote = quote_file.read_bytes().decode("utf-8")
    configuration = json.loads(config.read_text(encoding="utf-8"))
    if not isinstance(configuration, dict) or not configuration:
        raise ValueError("config must be a non-empty JSON object describing the actual extraction")
    if not all(isinstance(value, str) and value.strip() for value in (quote, query, adapter, version)):
        raise ValueError("quote, query, adapter and version must be non-empty strings")
    if quote not in content:
        raise ValueError("quote must occur verbatim in the extracted text; preserve whitespace")
    if page is not None and (type(page) is not int or page < 1):
        raise ValueError("page must be a positive 1-based integer")
    if page is None:
        if content.count(quote) != 1:
            raise ValueError("quote is ambiguous in the text; select a unique bounded excerpt")
        start = content.index(quote)
        locator = {"kind": "text_span", "start": start, "end": start + len(quote), "text_digest": digest(projection)}
    else:
        # With --page, --text must contain only that page/slide, not a whole deck.
        locator = {"kind": "page_span", "page_start": page, "page_end": page, "page_digest": digest(projection)}
    return {"schema_version": "proofpress/retrieval-evidence/v1",
            "source": {"uri": source.resolve().as_uri(), "content_digest": digest(source.read_bytes())},
            "evidence": {"quote": quote, "locator": locator},
            "retrieval": {"adapter": adapter, "version": version, "query": query,
                          "config_digest": digest(json.dumps(configuration, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source", "text", "quote-file", "config"):
        parser.add_argument("--" + name, required=True, type=Path)
    for name in ("query", "adapter", "version"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--page", type=int, help="1-based page/slide; --text must contain only this page")
    args = parser.parse_args()
    try:
        payload = prepare(args.source, args.text, args.quote_file, args.config,
                          args.query, args.adapter, args.version, args.page)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(2, f"Cannot prepare evidence: {exc}\n")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

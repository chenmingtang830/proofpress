#!/usr/bin/env python3
"""Compile a private, source-bound APEX world into a retrieval catalog.

The APEX corpus mixes born-digital Word files, PDFs, legacy Office documents,
mailboxes, calendars, and JSON application state.  Treating its world snapshot
as PDF-only silently drops the native table structure that exact-knowledge
construction needs.  This helper keeps all extracted text in a caller-owned
private output directory while emitting a content-free receipt on stdout.

DOCX table cells are read directly from ``word/document.xml``; no raster OCR is
used for that source type.  PDFs use Poppler's layout-preserving text path.
Legacy ``.doc`` files use an isolated LibreOffice text conversion when
available.  Scanned PDFs remain explicit empty-text candidates for a separately
qualified OCR fallback rather than being invented as text here.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import mailbox
import mimetypes
import shutil
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass
from email.message import Message
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from urllib.parse import quote
from xml.etree import ElementTree as ET


SCHEMA = "proofpress/apex-private-source-catalog/v1"
SUPPORTED_SUFFIXES = {".doc", ".docx", ".ics", ".json", ".mbox", ".pdf"}
WORD_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def digest(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return "sha256:" + value.hexdigest()


@dataclass(frozen=True)
class SourceFile:
    root_label: str
    root: Path
    path: Path

    @property
    def relative_path(self) -> PurePosixPath:
        return PurePosixPath(self.path.relative_to(self.root).as_posix())

    @property
    def uri(self) -> str:
        return "apex://" + quote(self.root_label, safe="") + "/" + quote(str(self.relative_path), safe="/")


def _media_type(path: Path) -> str:
    explicit = {
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".ics": "text/calendar",
        ".json": "application/json",
        ".mbox": "application/mbox",
        ".pdf": "application/pdf",
    }
    return explicit.get(path.suffix.lower(), mimetypes.guess_type(path.name)[0] or "application/octet-stream")


def _xml_text(node: ET.Element) -> str:
    paragraphs = []
    for paragraph in node.findall(".//w:p", WORD_NS):
        text = "".join(value.text or "" for value in paragraph.findall(".//w:t", WORD_NS))
        if text:
            paragraphs.append(text)
    return "\n".join(paragraphs)


def _docx_units(path: Path) -> list[tuple[str, int, str]]:
    """Return ordered paragraph/table units with logical page-one locators."""
    with zipfile.ZipFile(path) as document:
        try:
            xml = ET.fromstring(document.read("word/document.xml"))
        except KeyError as exc:
            raise ValueError("DOCX lacks word/document.xml") from exc
    body = xml.find(".//w:body", WORD_NS)
    if body is None:
        raise ValueError("DOCX lacks a document body")
    units: list[tuple[str, int, str]] = []
    paragraph_index = table_index = 0
    for child in list(body):
        if child.tag == "{" + WORD_NS["w"] + "}p":
            paragraph_index += 1
            text = _xml_text(child).strip()
            if text:
                units.append((f"paragraph-{paragraph_index}", 1, text))
        elif child.tag == "{" + WORD_NS["w"] + "}tbl":
            table_index += 1
            rows = []
            for row in child.findall("./w:tr", WORD_NS):
                cells = []
                for cell in row.findall("./w:tc", WORD_NS):
                    text = _xml_text(cell).replace("\n", " ").strip()
                    cells.append(text)
                if cells:
                    rows.append("\t".join(cells))
            if rows:
                units.append((f"table-{table_index}", 1, "\n".join(rows)))
    return units


def _pdf_units(path: Path) -> list[tuple[str, int, str]]:
    result = subprocess.run(["pdftotext", "-q", "-layout", "-enc", "UTF-8", str(path), "-"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=False, timeout=120)
    if result.returncode:
        raise ValueError("pdftotext failed")
    pages = result.stdout.decode("utf-8", errors="replace").split("\f")
    units = [(f"page-{index}", index, page.strip())
             for index, page in enumerate(pages, 1) if page.strip()]
    # A scanned PDF is recorded as an explicit gap candidate.  This preserves
    # custody and makes an OCR sensitivity route necessary rather than faking
    # a native-text representation.
    return units or [("page-1-native-text-unavailable", 1, "")]


def _legacy_doc_units(path: Path) -> list[tuple[str, int, str]]:
    soffice = shutil.which("soffice")
    if not soffice:
        raise ValueError("legacy DOC conversion requires soffice")
    with tempfile.TemporaryDirectory(prefix="proofpress-apex-doc-") as temp:
        target = Path(temp)
        result = subprocess.run([soffice, "--headless", "--convert-to", "txt:Text",
                                 "--outdir", str(target), str(path)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                check=False, timeout=120)
        converted = target / (path.stem + ".txt")
        if result.returncode or not converted.is_file():
            raise ValueError("legacy DOC conversion failed")
        text = converted.read_text(encoding="utf-8", errors="replace").strip()
    return [("legacy-doc-text", 1, text)] if text else [("legacy-doc-text-unavailable", 1, "")]


def _message_text(message: Message) -> str:
    headers = [f"{name}: {message.get(name, '')}" for name in ("From", "To", "Cc", "Date", "Subject")
               if message.get(name)]
    payloads: list[bytes | str] = []
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/plain" and not part.get_filename():
                payloads.append(part.get_payload(decode=True) or "")
    elif message.get_content_type() == "text/plain":
        payloads.append(message.get_payload(decode=True) or "")
    bodies = [value.decode("utf-8", errors="replace") if isinstance(value, bytes) else str(value)
              for value in payloads]
    return "\n".join(headers + bodies).strip()


def _mbox_units(path: Path) -> list[tuple[str, int, str]]:
    units = []
    for index, message in enumerate(mailbox.mbox(path), 1):
        text = _message_text(message)
        if text:
            units.append((f"message-{index}", index, text))
    return units or [("mailbox-empty", 1, "")]


def _plain_units(path: Path) -> list[tuple[str, int, str]]:
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    return [("content", 1, text)] if text else [("content-empty", 1, "")]


def extract_units(path: Path) -> list[tuple[str, int, str]]:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return _docx_units(path)
    if suffix == ".pdf":
        return _pdf_units(path)
    if suffix == ".doc":
        return _legacy_doc_units(path)
    if suffix == ".mbox":
        return _mbox_units(path)
    return _plain_units(path)


def _chunk(unit_name: str, page: int, text: str, maximum: int) -> Iterable[tuple[str, int, str]]:
    if len(text) <= maximum:
        yield unit_name, page, text
        return
    lines = text.splitlines(keepends=True)
    current = ""
    chunk_index = 1
    for line in lines:
        if current and len(current) + len(line) > maximum:
            yield f"{unit_name}-part-{chunk_index}", page, current.rstrip("\n")
            chunk_index += 1
            current = ""
        if len(line) > maximum:
            for start in range(0, len(line), maximum):
                if current:
                    yield f"{unit_name}-part-{chunk_index}", page, current.rstrip("\n")
                    chunk_index += 1
                    current = ""
                yield f"{unit_name}-part-{chunk_index}", page, line[start:start + maximum].rstrip("\n")
                chunk_index += 1
        else:
            current += line
    if current or not lines:
        yield f"{unit_name}-part-{chunk_index}", page, current.rstrip("\n")


def representation(source_file: SourceFile, *, max_section_chars: int) -> tuple[dict[str, Any], int, bool]:
    if max_section_chars < 256:
        raise ValueError("max_section_chars must be at least 256")
    source = {"uri": source_file.uri, "media_type": _media_type(source_file.path),
              "content_digest": file_digest(source_file.path)}
    sections = []
    line = 1
    units = extract_units(source_file.path)
    native_text_unavailable = any(not text and unit_name.endswith("native-text-unavailable")
                                  for unit_name, _, text in units)
    for unit_name, page, text in units:
        for heading, page_number, section_text in _chunk(unit_name, page, text, max_section_chars):
            section = {"id": f"section_{len(sections) + 1:04d}", "heading": heading,
                       "text": section_text, "text_digest": digest(section_text),
                       "page_start": page_number, "page_end": page_number,
                       "line_start": line, "line_end": line + section_text.count("\n")}
            sections.append(section)
            line = section["line_end"] + 1
    payload = {"source": source, "sections": sections,
               "transform": "native-multiformat-apex-representation/v1"}
    if native_text_unavailable:
        payload["extraction_gap"] = "native_text_unavailable"
    payload["representation_digest"] = digest(payload)
    return (payload, sum(1 for section in sections if section["heading"].startswith("table-")),
            native_text_unavailable)


def iter_sources(roots: list[Path]) -> list[SourceFile]:
    result = []
    labels: Counter[str] = Counter()
    for root in roots:
        if not root.is_dir():
            raise ValueError("every source root must be a directory")
        label = root.name or "apex-world"
        labels[label] += 1
        if labels[label] > 1:
            label = f"{label}-{labels[label]}"
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
                result.append(SourceFile(label, root, path))
    if not result:
        raise ValueError("source roots did not contain supported files")
    return result


def build(roots: list[Path], *, max_section_chars: int = 6000) -> tuple[dict[str, Any], dict[str, Any]]:
    representations = []
    formats: Counter[str] = Counter()
    table_sections = extraction_failures = 0
    for source_file in iter_sources(roots):
        formats[source_file.path.suffix.lower()] += 1
        try:
            item, tables, has_native_gap = representation(source_file, max_section_chars=max_section_chars)
        except (OSError, ValueError, subprocess.TimeoutExpired, zipfile.BadZipFile) as exc:
            # A source is never silently omitted.  The catalog retains an
            # explicit, source-bound candidate gap that later routes may repair.
            source = {"uri": source_file.uri, "media_type": _media_type(source_file.path),
                      "content_digest": file_digest(source_file.path)}
            text = "[native extraction unavailable]"
            item = {"source": source, "sections": [{"id": "section_0001", "heading": "native-extraction-gap",
                    "text": text, "text_digest": digest(text), "page_start": 1, "page_end": 1,
                    "line_start": 1, "line_end": 1}],
                    "transform": "native-multiformat-apex-representation/v1",
                    "extraction_gap": type(exc).__name__}
            item["representation_digest"] = digest({key: value for key, value in item.items()
                                                      if key != "representation_digest"})
            tables = 0
            has_native_gap = True
        representations.append(item)
        table_sections += tables
        extraction_failures += int(has_native_gap)
    catalog = {"schema_version": SCHEMA, "representations": representations,
               "automatic_admission": False, "human_approval_required": True}
    catalog["catalog_digest"] = digest({key: value for key, value in catalog.items() if key != "catalog_digest"})
    receipt = {"schema_version": SCHEMA, "status": "compiled-private-source-catalog",
               "source_count": len(representations), "section_count": sum(len(row["sections"]) for row in representations),
               "table_section_count": table_sections, "format_counts": dict(sorted(formats.items())),
               "native_extraction_gap_count": extraction_failures,
               "catalog_digest": catalog["catalog_digest"], "automatic_admission": False,
               "human_approval_required": True,
               "decision_boundary": "Source representations are evidence candidates only; no extraction is admitted."}
    receipt["receipt_digest"] = digest(receipt)
    return catalog, receipt


def _write_private(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    path.chmod(0o600)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, action="append", required=True,
                        help="Private APEX world/task directory; repeat for multiple roots.")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-section-chars", type=int, default=6000)
    args = parser.parse_args()
    catalog, receipt = build(args.source_root, max_section_chars=args.max_section_chars)
    args.out.mkdir(parents=True, exist_ok=True)
    args.out.chmod(0o700)
    _write_private(args.out / "apex-source-catalog-private.json", catalog)
    _write_private(args.out / "apex-source-catalog-receipt-sanitized.json", receipt)
    print(json.dumps({key: receipt[key] for key in ("status", "source_count", "section_count",
                                                     "table_section_count", "format_counts",
                                                     "native_extraction_gap_count", "catalog_digest")},
                     sort_keys=True))


if __name__ == "__main__":
    main()

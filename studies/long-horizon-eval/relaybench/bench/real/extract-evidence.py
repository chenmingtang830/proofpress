#!/usr/bin/env python3
"""Deterministically extract bounded text from RelayBench evidence files."""
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


def xml_text(data):
    root = ET.fromstring(data)
    return " ".join(t.strip() for t in root.itertext() if t.strip())


def extract(path):
    suffix = path.suffix.lower()
    if suffix == ".docx" and zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zf:
            return xml_text(zf.read("word/document.xml"))
    if suffix == ".xlsx" and zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zf:
            names = [n for n in zf.namelist() if n == "xl/sharedStrings.xml" or re.match(r"xl/worksheets/sheet\d+\.xml$", n)]
            return "\n".join(xml_text(zf.read(name)) for name in sorted(names))
    return path.read_bytes().decode("utf-8", errors="replace")


payload = json.loads(sys.argv[1])
limit = int(payload.get("max_chars_per_file", 12000))
print(json.dumps({str(p): extract(Path(p))[:limit] for p in payload["paths"]}))

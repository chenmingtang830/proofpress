#!/usr/bin/env python3
"""HTTP service for the single-owner Proofpress self-hosting reference."""
from pathlib import Path

_DIR = Path(__file__).resolve().parent
_SOURCE = "".join(
    (_DIR / name).read_text(encoding="utf-8")
    for name in ("_svc_a.py", "_svc_b.py", "_svc_c.py")
)
exec(compile(_SOURCE, str(Path(__file__).resolve()), "exec"), globals())

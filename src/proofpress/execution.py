"""Stable client-side trigger keys for explicitly retried pilot workflows."""
from __future__ import annotations

import hashlib
import json


def external_trigger_key(operation: str, source_system: str,
                         trigger_id: str, source_version: str) -> str:
    """Return a bounded key for one source event and its immutable version.

    A corrected source version intentionally gets a different key. Callers
    must not use a raw credential or private source body as an identifier.
    """
    fields = (operation, source_system, trigger_id, source_version)
    if any(not isinstance(value, str) or not value.strip() or len(value) > 512
           for value in fields):
        raise ValueError("trigger key fields must be non-empty strings of at most 512 characters")
    payload = json.dumps(fields, ensure_ascii=False, separators=(",", ":"))
    return "trigger-v1-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()

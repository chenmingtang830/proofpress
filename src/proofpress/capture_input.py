"""Side-effect-free MCP checks before a mutation or idempotency reservation."""
from __future__ import annotations

from proofpress.kernel.operations import normalize_retrieval_evidence_v1
from proofpress.profiles.experiment import normalize_claim


def validate_evidence_input(payload, profile=None):
    if profile not in {None, "experiment"}:
        raise ValueError(f"unsupported evidence profile: {profile}; omit profile for retrieval evidence or use experiment")
    if profile is None:
        normalize_retrieval_evidence_v1(payload)


def validate_claim_input(qualifiers, profile=None):
    if profile == "experiment":
        if qualifiers is not None and not isinstance(qualifiers, dict):
            raise ValueError("experiment qualifiers must be an object")
        normalize_claim(qualifiers)


def format_error(exc):
    return (f"Capture format rejected before submission: {exc}. "
            "No submission was attempted; this call did not consume an idempotency key. "
            "Read proofpress_get_capture_schema and correct the full payload before retrying.")

"""Source-bound document extraction candidates; never an admission path."""

from proofpress.integrations.document_extraction.contract import (
    build_envelope,
    compare_envelopes,
    digest,
    validate_envelope,
)

__all__ = ["build_envelope", "compare_envelopes", "digest", "validate_envelope"]

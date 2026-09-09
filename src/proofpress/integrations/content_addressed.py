"""Build bounded, content-addressed retrieval-evidence receipts.

This is an adapter *seam*, not a connector marketplace or a universal semantic
model.  An integration supplies an owner-controlled source URI, immutable
source digest, a reviewer-readable bounded quote, and a locator supported by
the Proofpress contract.  Source bytes and raw traces never enter the receipt.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping

from proofpress.kernel.operations import (
    RETRIEVAL_EVIDENCE_SCHEMA,
    normalize_retrieval_evidence_v1,
)


class ContentAddressedReceiptError(ValueError):
    """Raised when an adapter cannot produce a bounded receipt."""


def _nonempty(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContentAddressedReceiptError(f"{field} must be a non-empty string")
    return value


def _sha256(value: Any) -> str:
    """Digest a stable, non-secret adapter configuration locally."""
    try:
        encoded = json.dumps(value, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise ContentAddressedReceiptError(
            "adapter config must be JSON-serializable") from error
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _config_digest(config: Mapping[str, Any] | None, config_digest: str | None) -> str:
    if (config is None) == (config_digest is None):
        raise ContentAddressedReceiptError(
            "provide exactly one of adapter config or config_digest")
    if config is not None:
        if not isinstance(config, Mapping):
            raise ContentAddressedReceiptError("adapter config must be an object")
        return _sha256(dict(config))
    if not isinstance(config_digest, str) or not config_digest.strip():
        raise ContentAddressedReceiptError("config_digest must be a non-empty string")
    return config_digest


@dataclass(frozen=True)
class ContentAddressedReceiptAdapter:
    """Emit the standard receipt envelope for one external adapter version.

    ``config`` is digested locally and omitted from the returned envelope.
    Pass a previously computed ``config_digest`` when the integration cannot
    expose its configuration.  Do not put source bytes, prompts, tokens, or
    raw execution traces in either value.
    """

    adapter: str
    version: str
    config: Mapping[str, Any] | None = None
    config_digest: str | None = None

    def __post_init__(self):
        _nonempty(self.adapter, "adapter")
        _nonempty(self.version, "version")
        object.__setattr__(self, "_bound_config_digest",
                           _config_digest(self.config, self.config_digest))

    @property
    def bound_config_digest(self) -> str:
        """The digest that will be bound into every emitted receipt."""
        return self._bound_config_digest

    def evidence(self, *, source_uri: str, source_content_digest: str,
                 quote: str, locator: Mapping[str, Any], query: str,
                 media_type: str | None = None,
                 selection_reason: str | None = None) -> dict[str, Any]:
        """Return a normalized ``proofpress/retrieval-evidence/v1`` envelope.

        The kernel validates the digest format and typed locator.  This helper
        deliberately accepts no source-content or trace-content parameter.
        """
        if not isinstance(locator, Mapping):
            raise ContentAddressedReceiptError("locator must be an object")
        source = {"uri": _nonempty(source_uri, "source_uri"),
                  "content_digest": _nonempty(source_content_digest,
                                                "source_content_digest")}
        if media_type is not None:
            source["media_type"] = _nonempty(media_type, "media_type")
        retrieval = {"adapter": self.adapter, "version": self.version,
                     "query": _nonempty(query, "query"),
                     "config_digest": self.bound_config_digest}
        if selection_reason is not None:
            retrieval["selection_reason"] = _nonempty(selection_reason,
                                                         "selection_reason")
        try:
            normalized = normalize_retrieval_evidence_v1({
                "schema_version": RETRIEVAL_EVIDENCE_SCHEMA,
                "source": source,
                "evidence": {"quote": _nonempty(quote, "quote"),
                             "locator": dict(locator)},
                "retrieval": retrieval,
            })
        except ValueError as error:
            raise ContentAddressedReceiptError(str(error)) from error
        # The normalizer's canonical receipt is an internal ledger projection.
        # Return the validated public envelope so callers can pass it directly
        # to ``ProofpressClient.submit_evidence`` and every other transport.
        return {
            "schema_version": normalized["schema_version"],
            "source": normalized["source"],
            "evidence": {"quote": normalized["quote"],
                         "locator": normalized["locator"]},
            "retrieval": normalized["retrieval"],
        }


def build_retrieval_evidence(*, adapter: str, version: str,
                             config: Mapping[str, Any] | None = None,
                             config_digest: str | None = None,
                             source_uri: str, source_content_digest: str,
                             quote: str, locator: Mapping[str, Any], query: str,
                             media_type: str | None = None,
                             selection_reason: str | None = None) -> dict[str, Any]:
    """One-shot form of :class:`ContentAddressedReceiptAdapter`."""
    return ContentAddressedReceiptAdapter(
        adapter=adapter, version=version, config=config,
        config_digest=config_digest,
    ).evidence(
        source_uri=source_uri, source_content_digest=source_content_digest,
        quote=quote, locator=locator, query=query, media_type=media_type,
        selection_reason=selection_reason,
    )

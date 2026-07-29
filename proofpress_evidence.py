"""Format-agnostic evidence records for the Artifact Provenance Protocol.

The built-in implementation deliberately stops at byte verification. Higher
verification levels require an explicitly registered adapter and provider that
understand the artifact format and the checks they claim to perform.
"""

from __future__ import annotations

import hashlib
import json
import mimetypes
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol


PROTOCOL = "proofpress.artifact-provenance"
PROTOCOL_VERSION = 1
VERIFICATION_LEVELS = ("linked", "byte", "render", "semantic", "native")
VERIFICATION_STATUSES = ("verified", "failed", "indeterminate")


class EvidenceError(ValueError):
    """Raised when evidence is malformed or overstates registered capability."""


@dataclass(frozen=True)
class VerificationResult:
    status: str
    level: str
    provider: str
    adapter: str
    checks: tuple[dict[str, Any], ...]

    @property
    def ok(self) -> bool:
        return self.status == "verified"

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "level": self.level,
            "provider": self.provider,
            "adapter": self.adapter,
            "checks": list(self.checks),
        }


class EvidenceAdapter(Protocol):
    adapter_id: str
    max_level: str

    def supports(self, path: Path, media_type: str) -> bool:
        """Return whether this adapter can describe the artifact."""

    def describe(self, path: Path, media_type: str) -> dict[str, Any]:
        """Return non-verification subject metadata."""


class EvidenceProvider(Protocol):
    provider_id: str
    supported_levels: frozenset[str]

    def create(
        self, path: Path, adapter: EvidenceAdapter, subject: dict[str, Any],
        level: str,
    ) -> dict[str, Any]:
        """Create the verification portion of an evidence envelope."""

    def verify(
        self, path: Path, adapter: EvidenceAdapter, envelope: dict[str, Any],
    ) -> VerificationResult:
        """Verify an evidence envelope against the current artifact."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _level_at_most(level: str, maximum: str) -> bool:
    return VERIFICATION_LEVELS.index(level) <= VERIFICATION_LEVELS.index(maximum)


class GenericBinaryAdapter:
    """Fallback adapter that knows only carrier-independent byte facts."""

    adapter_id = "proofpress.generic-binary"
    max_level = "byte"

    def supports(self, path: Path, media_type: str) -> bool:
        return path.is_file()

    def describe(self, path: Path, media_type: str) -> dict[str, Any]:
        return {
            "name": path.name,
            "media_type": media_type,
            "byte_length": path.stat().st_size,
        }


class DigestEvidenceProvider:
    """Built-in provider for exact byte digest and length verification."""

    provider_id = "proofpress.digest"
    supported_levels = frozenset({"byte"})

    def create(
        self, path: Path, adapter: EvidenceAdapter, subject: dict[str, Any],
        level: str,
    ) -> dict[str, Any]:
        if level != "byte":
            raise EvidenceError("proofpress.digest can only create byte evidence")
        digest = _sha256(path)
        subject["digest"] = {"algorithm": "sha256", "value": digest}
        checks = [
            {
                "type": "digest",
                "status": "passed",
                "algorithm": "sha256",
                "value": digest,
            },
            {
                "type": "byte_length",
                "status": "passed",
                "value": path.stat().st_size,
            },
        ]
        return {
            "status": "verified",
            "level": "byte",
            "provider": self.provider_id,
            "adapter": adapter.adapter_id,
            "verified_at": _utc_now(),
            "checks": checks,
        }

    def verify(
        self, path: Path, adapter: EvidenceAdapter, envelope: dict[str, Any],
    ) -> VerificationResult:
        subject = envelope["subject"]
        expected_digest = subject["digest"]["value"]
        expected_size = subject["byte_length"]
        actual_digest = _sha256(path)
        actual_size = path.stat().st_size
        checks = (
            {
                "type": "digest",
                "status": "passed" if actual_digest == expected_digest else "failed",
                "algorithm": "sha256",
                "expected": expected_digest,
                "actual": actual_digest,
            },
            {
                "type": "byte_length",
                "status": "passed" if actual_size == expected_size else "failed",
                "expected": expected_size,
                "actual": actual_size,
            },
        )
        status = "verified" if all(c["status"] == "passed" for c in checks) else "failed"
        return VerificationResult(
            status=status,
            level="byte",
            provider=self.provider_id,
            adapter=adapter.adapter_id,
            checks=checks,
        )


class EvidenceRegistry:
    """Registry boundary for format adapters and verification providers."""

    def __init__(self) -> None:
        self._adapters: dict[str, EvidenceAdapter] = {}
        self._providers: dict[str, EvidenceProvider] = {}

    def register_adapter(self, adapter: EvidenceAdapter) -> None:
        _require_id(adapter.adapter_id, "adapter_id")
        _require_level(adapter.max_level)
        if adapter.adapter_id in self._adapters:
            raise EvidenceError(f"adapter already registered: {adapter.adapter_id}")
        self._adapters[adapter.adapter_id] = adapter

    def register_provider(self, provider: EvidenceProvider) -> None:
        _require_id(provider.provider_id, "provider_id")
        if not provider.supported_levels:
            raise EvidenceError("provider must support at least one verification level")
        for level in provider.supported_levels:
            _require_level(level)
        if provider.provider_id in self._providers:
            raise EvidenceError(f"provider already registered: {provider.provider_id}")
        self._providers[provider.provider_id] = provider

    def adapter(self, adapter_id: str) -> EvidenceAdapter:
        try:
            return self._adapters[adapter_id]
        except KeyError as exc:
            raise EvidenceError(f"unknown evidence adapter: {adapter_id}") from exc

    def provider(self, provider_id: str) -> EvidenceProvider:
        try:
            return self._providers[provider_id]
        except KeyError as exc:
            raise EvidenceError(f"unknown evidence provider: {provider_id}") from exc

    def resolve_adapter(self, path: Path, media_type: str) -> EvidenceAdapter:
        # Later registrations take precedence, so consumers can add a specific
        # adapter to a registry that already contains the generic fallback.
        for adapter in reversed(self._adapters.values()):
            if adapter.supports(path, media_type):
                return adapter
        raise EvidenceError(f"no evidence adapter supports {path}")

    def create(
        self, artifact: os.PathLike[str] | str, *, level: str = "byte",
        provider_id: str = "proofpress.digest", adapter_id: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        path = _artifact_path(artifact)
        media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        adapter = (self.adapter(adapter_id) if adapter_id
                   else self.resolve_adapter(path, media_type))
        provider = self.provider(provider_id)
        _assert_capability(adapter, provider, level)
        subject = adapter.describe(path, media_type)
        verification = provider.create(path, adapter, subject, level)
        envelope: dict[str, Any] = {
            "protocol": PROTOCOL,
            "protocol_version": PROTOCOL_VERSION,
            "subject": subject,
            "verification": verification,
        }
        if context:
            envelope["context"] = context
        envelope["evidence_id"] = _evidence_id(envelope)
        validate_evidence(envelope, registry=self)
        return envelope

    def verify(
        self, artifact: os.PathLike[str] | str, envelope: dict[str, Any],
    ) -> VerificationResult:
        path = _artifact_path(artifact)
        validate_evidence(envelope, registry=self)
        verification = envelope["verification"]
        adapter = self.adapter(verification["adapter"])
        provider = self.provider(verification["provider"])
        _assert_capability(adapter, provider, verification["level"])
        return provider.verify(path, adapter, envelope)


def _artifact_path(artifact: os.PathLike[str] | str) -> Path:
    path = Path(artifact)
    if not path.is_file():
        raise EvidenceError(f"artifact is not a readable file: {path}")
    return path


def _require_id(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value or any(c.isspace() for c in value):
        raise EvidenceError(f"{field} must be a non-empty identifier")


def _require_level(level: Any) -> None:
    if level not in VERIFICATION_LEVELS:
        raise EvidenceError(
            f"unknown verification level {level!r}; "
            f"expected one of {', '.join(VERIFICATION_LEVELS)}"
        )


def _assert_capability(
    adapter: EvidenceAdapter, provider: EvidenceProvider, level: str,
) -> None:
    _require_level(level)
    if level not in provider.supported_levels:
        raise EvidenceError(
            f"provider {provider.provider_id} does not support {level} verification"
        )
    if not _level_at_most(level, adapter.max_level):
        raise EvidenceError(
            f"adapter {adapter.adapter_id} is capped at {adapter.max_level}; "
            f"it cannot claim {level} verification"
        )


def _evidence_id(envelope: dict[str, Any]) -> str:
    encoded = json.dumps(
        envelope, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    return "ppe_" + hashlib.sha256(encoded).hexdigest()[:24]


def validate_evidence(
    envelope: dict[str, Any], *, registry: EvidenceRegistry | None = None,
) -> None:
    """Validate a V1 evidence envelope and registered capabilities."""
    if not isinstance(envelope, dict):
        raise EvidenceError("evidence envelope must be an object")
    if envelope.get("protocol") != PROTOCOL:
        raise EvidenceError("unsupported evidence protocol")
    if envelope.get("protocol_version") != PROTOCOL_VERSION:
        raise EvidenceError("unsupported evidence protocol version")
    _require_id(envelope.get("evidence_id"), "evidence_id")
    unsigned = {key: value for key, value in envelope.items()
                if key != "evidence_id"}
    if envelope["evidence_id"] != _evidence_id(unsigned):
        raise EvidenceError("evidence_id does not match the envelope")

    subject = envelope.get("subject")
    if not isinstance(subject, dict):
        raise EvidenceError("subject must be an object")
    if not isinstance(subject.get("name"), str) or not subject["name"]:
        raise EvidenceError("subject.name must be a non-empty string")
    if (not isinstance(subject.get("byte_length"), int)
            or isinstance(subject.get("byte_length"), bool)
            or subject["byte_length"] < 0):
        raise EvidenceError("subject.byte_length must be a non-negative integer")
    digest = subject.get("digest")
    if not isinstance(digest, dict) or digest.get("algorithm") != "sha256":
        raise EvidenceError("subject.digest must use sha256")
    value = digest.get("value")
    if (not isinstance(value, str) or len(value) != 64
            or any(c not in "0123456789abcdef" for c in value)):
        raise EvidenceError("subject.digest.value must be lowercase sha256 hex")

    verification = envelope.get("verification")
    if not isinstance(verification, dict):
        raise EvidenceError("verification must be an object")
    _require_level(verification.get("level"))
    if verification.get("status") not in VERIFICATION_STATUSES:
        raise EvidenceError("verification.status is invalid")
    _require_id(verification.get("provider"), "verification.provider")
    _require_id(verification.get("adapter"), "verification.adapter")
    if not isinstance(verification.get("checks"), list) or not verification["checks"]:
        raise EvidenceError("verification.checks must be a non-empty list")

    if registry is not None:
        adapter = registry.adapter(verification["adapter"])
        provider = registry.provider(verification["provider"])
        _assert_capability(adapter, provider, verification["level"])


def default_registry() -> EvidenceRegistry:
    registry = EvidenceRegistry()
    registry.register_adapter(GenericBinaryAdapter())
    registry.register_provider(DigestEvidenceProvider())
    return registry


DEFAULT_REGISTRY = default_registry()


def create_evidence(
    artifact: os.PathLike[str] | str, *, level: str = "byte",
    provider_id: str = "proofpress.digest", adapter_id: str | None = None,
    context: dict[str, Any] | None = None,
    registry: EvidenceRegistry = DEFAULT_REGISTRY,
) -> dict[str, Any]:
    return registry.create(
        artifact, level=level, provider_id=provider_id, adapter_id=adapter_id,
        context=context,
    )


def verify_evidence(
    artifact: os.PathLike[str] | str, envelope: dict[str, Any], *,
    registry: EvidenceRegistry = DEFAULT_REGISTRY,
) -> VerificationResult:
    return registry.verify(artifact, envelope)


def dump_evidence(envelope: dict[str, Any]) -> str:
    validate_evidence(envelope)
    return json.dumps(envelope, ensure_ascii=False, sort_keys=True, indent=2) + "\n"

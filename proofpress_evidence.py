"""Format-aware evidence records for the Artifact Provenance Protocol.

The built-in implementation supports exact byte verification for every file,
format-aware byte evidence for PDF, and canonical semantic evidence for OOXML
Word documents. Other higher verification levels still require explicitly
registered adapters and providers.
"""

from __future__ import annotations

import hashlib
import json
import mimetypes
import os
import re
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol
from xml.etree import ElementTree


PROTOCOL = "proofpress.artifact-provenance"
PROTOCOL_VERSION = 1
VERIFICATION_LEVELS = ("linked", "byte", "render", "semantic", "native")
VERIFICATION_STATUSES = ("verified", "failed", "indeterminate")
AUTO_LEVEL = "auto"
MAX_OOXML_PART_BYTES = 16 * 1024 * 1024
MAX_OOXML_TOTAL_BYTES = 64 * 1024 * 1024
WORD_CONTENT_TYPES = {
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml",
    "application/vnd.ms-word.document.macroEnabled.main+xml",
}


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


class SemanticEvidenceAdapter(EvidenceAdapter, Protocol):
    def semantic_snapshot(self, path: Path) -> dict[str, Any]:
        """Return a deterministic, format-aware semantic snapshot."""


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


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


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


def _pdf_metadata(path: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        head = stream.read(1024)
        stream.seek(max(0, path.stat().st_size - 8192))
        tail = stream.read()
    version_match = re.match(br"%PDF-(\d+\.\d+)", head)
    if not version_match or b"%%EOF" not in tail:
        raise EvidenceError("PDF is missing a valid header or end marker")
    # Page count is descriptive only. It intentionally does not claim that the
    # pages can be rendered, and is omitted when no page dictionaries are found.
    page_count = 0
    encrypted = False
    overlap = b""
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            searchable = overlap + chunk
            encrypted = encrypted or bool(re.search(br"/Encrypt\b", searchable))
            if len(searchable) > 64:
                page_count += len(
                    re.findall(br"/Type\s*/Page(?!s)\b", searchable[:-64]))
                overlap = searchable[-64:]
            else:
                overlap = searchable
    page_count += len(re.findall(br"/Type\s*/Page(?!s)\b", overlap))
    metadata: dict[str, Any] = {
        "version": version_match.group(1).decode("ascii"),
        "encrypted": encrypted,
        "linearized": bool(re.search(br"/Linearized\b", head)),
    }
    if page_count:
        metadata["page_count_hint"] = page_count
    return metadata


class PdfAdapter:
    """Recognize PDF structure without overstating render verification."""

    adapter_id = "proofpress.pdf"
    max_level = "byte"
    default_level = "byte"
    default_provider = "proofpress.digest"

    def supports(self, path: Path, media_type: str) -> bool:
        if not path.is_file():
            return False
        try:
            _pdf_metadata(path)
        except (EvidenceError, OSError):
            return False
        return True

    def describe(self, path: Path, media_type: str) -> dict[str, Any]:
        return {
            "name": path.name,
            "media_type": "application/pdf",
            "byte_length": path.stat().st_size,
            "format": "pdf",
            "pdf": _pdf_metadata(path),
        }


def _safe_word_archive(path: Path) -> tuple[zipfile.ZipFile, list[zipfile.ZipInfo]]:
    try:
        archive = zipfile.ZipFile(path)
        infos = archive.infolist()
    except (OSError, zipfile.BadZipFile) as exc:
        raise EvidenceError(f"invalid OOXML Word package: {exc}") from exc
    names = {info.filename for info in infos}
    if len(names) != len(infos):
        archive.close()
        raise EvidenceError("OOXML package contains duplicate part names")
    if "[Content_Types].xml" not in names or "word/document.xml" not in names:
        archive.close()
        raise EvidenceError("OOXML package is not a Word document")
    total = 0
    for info in infos:
        if info.is_dir():
            continue
        if info.file_size > MAX_OOXML_PART_BYTES:
            archive.close()
            raise EvidenceError(
                f"OOXML part exceeds {MAX_OOXML_PART_BYTES} bytes: {info.filename}")
        total += info.file_size
        if total > MAX_OOXML_TOTAL_BYTES:
            archive.close()
            raise EvidenceError(
                f"OOXML package exceeds {MAX_OOXML_TOTAL_BYTES} expanded bytes")
    return archive, infos


def _safe_xml(data: bytes, part_name: str) -> ElementTree.Element:
    if b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
        raise EvidenceError(f"unsafe XML declaration in OOXML part: {part_name}")
    try:
        return ElementTree.fromstring(data)
    except ElementTree.ParseError as exc:
        raise EvidenceError(f"invalid XML in OOXML part {part_name}: {exc}") from exc


def _canonical_xml(data: bytes, part_name: str) -> bytes:
    root = _safe_xml(data, part_name)

    def remove_indentation(element: ElementTree.Element) -> None:
        if len(element) and element.text is not None and not element.text.strip():
            element.text = None
        for child in element:
            remove_indentation(child)
            if child.tail is not None and not child.tail.strip():
                child.tail = None

    remove_indentation(root)
    normalized = ElementTree.tostring(root, encoding="utf-8")
    try:
        canonical = ElementTree.canonicalize(
            xml_data=normalized, with_comments=False, rewrite_prefixes=True)
    except (ElementTree.ParseError, ValueError) as exc:
        raise EvidenceError(
            f"cannot canonicalize OOXML part {part_name}: {exc}") from exc
    return canonical.encode("utf-8")


def _word_part_is_semantic(name: str) -> bool:
    if name == "[Content_Types].xml" or name == "_rels/.rels":
        return True
    return name.startswith("word/") and not name.endswith("/")


def _docx_semantic_snapshot(path: Path) -> dict[str, Any]:
    archive, infos = _safe_word_archive(path)
    try:
        content_types = archive.read("[Content_Types].xml")
        content_root = _safe_xml(content_types, "[Content_Types].xml")
        content_values = {
            element.attrib.get("ContentType")
            for element in content_root.iter()
            if element.tag.rsplit("}", 1)[-1] == "Override"
        }
        if not WORD_CONTENT_TYPES.intersection(content_values):
            raise EvidenceError("OOXML package does not declare a Word main document")

        part_records = []
        metrics = {
            "paragraphs": 0,
            "tables": 0,
            "comments": 0,
            "tracked_insertions": 0,
            "tracked_deletions": 0,
            "headers": 0,
            "footers": 0,
            "media_parts": 0,
        }
        for info in sorted(infos, key=lambda item: item.filename):
            name = info.filename
            if info.is_dir() or not _word_part_is_semantic(name):
                continue
            raw = archive.read(info)
            if name.endswith((".xml", ".rels")):
                canonical = _canonical_xml(raw, name)
                root = _safe_xml(raw, name)
                local_names = [
                    element.tag.rsplit("}", 1)[-1] for element in root.iter()
                ]
                if name == "word/document.xml":
                    metrics["paragraphs"] = local_names.count("p")
                    metrics["tables"] = local_names.count("tbl")
                    metrics["tracked_insertions"] = local_names.count("ins")
                    metrics["tracked_deletions"] = local_names.count("del")
                elif name == "word/comments.xml":
                    metrics["comments"] = local_names.count("comment")
                elif name.startswith("word/header"):
                    metrics["headers"] += 1
                elif name.startswith("word/footer"):
                    metrics["footers"] += 1
            else:
                canonical = raw
                if name.startswith("word/media/"):
                    metrics["media_parts"] += 1
            part_records.append({
                "name": name,
                "digest": _sha256_bytes(canonical),
            })
    except EvidenceError:
        raise
    except (KeyError, OSError, RuntimeError, zipfile.BadZipFile) as exc:
        raise EvidenceError(f"cannot read OOXML Word package: {exc}") from exc
    finally:
        archive.close()

    combined = hashlib.sha256()
    for part in part_records:
        combined.update(part["name"].encode("utf-8"))
        combined.update(b"\0")
        combined.update(part["digest"].encode("ascii"))
        combined.update(b"\n")
    return {
        "algorithm": "sha256",
        "normalization": "ooxml-word-c14n-v1",
        "digest": combined.hexdigest(),
        "parts": part_records,
        "metrics": metrics,
    }


class OoxmlWordAdapter:
    """Canonicalize the logical Word package independently of ZIP packaging."""

    adapter_id = "proofpress.ooxml-word"
    max_level = "semantic"
    default_level = "semantic"
    default_provider = "proofpress.ooxml-semantic"

    def supports(self, path: Path, media_type: str) -> bool:
        if not path.is_file() or not zipfile.is_zipfile(path):
            return False
        try:
            archive, _ = _safe_word_archive(path)
            try:
                root = _safe_xml(
                    archive.read("[Content_Types].xml"),
                    "[Content_Types].xml",
                )
                values = {
                    element.attrib.get("ContentType")
                    for element in root.iter()
                    if element.tag.rsplit("}", 1)[-1] == "Override"
                }
                return bool(WORD_CONTENT_TYPES.intersection(values))
            finally:
                archive.close()
        except (EvidenceError, KeyError, OSError, RuntimeError, zipfile.BadZipFile):
            return False

    def describe(self, path: Path, media_type: str) -> dict[str, Any]:
        return {
            "name": path.name,
            "media_type": media_type,
            "byte_length": path.stat().st_size,
            "format": "docx",
        }

    def semantic_snapshot(self, path: Path) -> dict[str, Any]:
        return _docx_semantic_snapshot(path)


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


class OoxmlSemanticEvidenceProvider:
    """Verify canonical OOXML Word parts rather than ZIP container bytes."""

    provider_id = "proofpress.ooxml-semantic"
    supported_levels = frozenset({"semantic"})

    def create(
        self, path: Path, adapter: EvidenceAdapter, subject: dict[str, Any],
        level: str,
    ) -> dict[str, Any]:
        if level != "semantic" or not hasattr(adapter, "semantic_snapshot"):
            raise EvidenceError(
                "proofpress.ooxml-semantic requires a semantic Word adapter")
        snapshot = adapter.semantic_snapshot(path)
        subject["digest"] = {"algorithm": "sha256", "value": _sha256(path)}
        subject["semantic"] = snapshot
        subject["document"] = {
            "normalization": snapshot["normalization"],
            "metrics": snapshot["metrics"],
        }
        return {
            "status": "verified",
            "level": "semantic",
            "provider": self.provider_id,
            "adapter": adapter.adapter_id,
            "verified_at": _utc_now(),
            "checks": [
                {
                    "type": "ooxml_package",
                    "status": "passed",
                    "normalization": snapshot["normalization"],
                    "parts": len(snapshot["parts"]),
                },
                {
                    "type": "semantic_digest",
                    "status": "passed",
                    "algorithm": snapshot["algorithm"],
                    "value": snapshot["digest"],
                },
            ],
        }

    def verify(
        self, path: Path, adapter: EvidenceAdapter, envelope: dict[str, Any],
    ) -> VerificationResult:
        try:
            actual = adapter.semantic_snapshot(path)
        except (EvidenceError, OSError, zipfile.BadZipFile) as exc:
            return VerificationResult(
                status="failed",
                level="semantic",
                provider=self.provider_id,
                adapter=adapter.adapter_id,
                checks=({
                    "type": "ooxml_package",
                    "status": "failed",
                    "error": str(exc),
                },),
            )
        expected = envelope["subject"]["semantic"]
        digest_ok = actual["digest"] == expected["digest"]
        metrics_ok = actual["metrics"] == expected["metrics"]
        checks = (
            {
                "type": "semantic_digest",
                "status": "passed" if digest_ok else "failed",
                "algorithm": "sha256",
                "expected": expected["digest"],
                "actual": actual["digest"],
            },
            {
                "type": "logical_metrics",
                "status": "passed" if metrics_ok else "failed",
                "expected": expected["metrics"],
                "actual": actual["metrics"],
            },
        )
        return VerificationResult(
            status="verified" if digest_ok else "failed",
            level="semantic",
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
        self, artifact: os.PathLike[str] | str, *, level: str = AUTO_LEVEL,
        provider_id: str | None = None, adapter_id: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        path = _artifact_path(artifact)
        media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        adapter = (self.adapter(adapter_id) if adapter_id
                   else self.resolve_adapter(path, media_type))
        auto_level = level == AUTO_LEVEL
        if level == AUTO_LEVEL:
            level = getattr(adapter, "default_level", "byte")
        if provider_id is None:
            provider_id = (
                getattr(adapter, "default_provider", "proofpress.digest")
                if auto_level
                else ("proofpress.ooxml-semantic"
                      if level == "semantic" else "proofpress.digest")
            )
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
    if verification.get("level") == "semantic":
        semantic = subject.get("semantic")
        if not isinstance(semantic, dict):
            raise EvidenceError("semantic evidence requires subject.semantic")
        if semantic.get("algorithm") != "sha256":
            raise EvidenceError("subject.semantic must use sha256")
        semantic_digest = semantic.get("digest")
        if (not isinstance(semantic_digest, str) or len(semantic_digest) != 64
                or any(c not in "0123456789abcdef" for c in semantic_digest)):
            raise EvidenceError(
                "subject.semantic.digest must be lowercase sha256 hex")
        if not isinstance(semantic.get("metrics"), dict):
            raise EvidenceError("subject.semantic.metrics must be an object")

    if registry is not None:
        adapter = registry.adapter(verification["adapter"])
        provider = registry.provider(verification["provider"])
        _assert_capability(adapter, provider, verification["level"])


def default_registry() -> EvidenceRegistry:
    registry = EvidenceRegistry()
    registry.register_adapter(GenericBinaryAdapter())
    registry.register_adapter(PdfAdapter())
    registry.register_adapter(OoxmlWordAdapter())
    registry.register_provider(DigestEvidenceProvider())
    registry.register_provider(OoxmlSemanticEvidenceProvider())
    return registry


DEFAULT_REGISTRY = default_registry()


def create_evidence(
    artifact: os.PathLike[str] | str, *, level: str = AUTO_LEVEL,
    provider_id: str | None = None, adapter_id: str | None = None,
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

#!/usr/bin/env python3
"""Experimental, read-only OpenWiki Claims schema-v1 inspection.

This module deliberately stops before Proofpress admission.  It consumes the
exact generated page bytes, OpenWiki's page-local Claims sidecar, and the
repository snapshot referenced by each ``repo://`` evidence record.  Passing
inspection means only that the producer packet is well-formed, page-bound, and
current against that snapshot.  It does not authenticate the producer or admit
the claims into governed context.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import posixpath
import re
import stat
from pathlib import Path
from urllib.parse import quote, unquote


REPORT_SCHEMA = "proofpress/openwiki-inspection/v1"
HANDOFF_MANIFEST_SCHEMA = "proofpress/openwiki-handoff-manifest/v1"
HANDOFF_SELECTION_MODES = {"full_snapshot", "selected_pages"}
OPENWIKI_CLAIMS_SCHEMA_VERSION = 1
PAGE_VERSION = re.compile(r"^sha256:[a-f0-9]{64}$")
SHA256 = re.compile(r"^[a-f0-9]{64}$")
WHOLE_FILE_VERSION = re.compile(r"^repo-file-v1:sha256:([a-f0-9]{64})$")
LINE_RANGE_PREFIX = "repo-lines-v1:sha256:"
LINE_RANGE = re.compile(r"^L([1-9][0-9]*)(?:-L([1-9][0-9]*))?$")
PERCENT_ESCAPE = re.compile(r"%(?![0-9A-Fa-f]{2})")
DRIVE_PATH = re.compile(r"^[A-Za-z]:/")
CONTROL_CHARACTER = re.compile(r"[\x00-\x1f\x7f]")
RESERVED_PAGES = {"index.md", "log.md", "instructions.md"}
RANGE_CONTEXT_LINE_COUNT = 3
METADATA_KEYS = {
    "selectedLineCount",
    "firstSelectedLineHash",
    "lastSelectedLineHash",
    "precedingContextLineCount",
    "precedingContextHash",
    "followingContextLineCount",
    "followingContextHash",
}


class OpenWikiInspectionError(ValueError):
    """One unsafe or unsupported OpenWiki input boundary."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _issue(code: str, message: str, **details):
    return {"code": code, "message": message, **details}


def _hash_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _hash_text(payload: str) -> str:
    return _hash_bytes(payload.encode("utf-8"))


def _canonical_string(value, field: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise OpenWikiInspectionError(
            "invalid_required_field",
            f"{field} must be a non-empty string without surrounding whitespace",
        )
    return value


def _reject_duplicate_keys(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise OpenWikiInspectionError(
                "duplicate_json_key", f"duplicate JSON object key: {key}"
            )
        value[key] = item
    return value


def _reject_json_constant(value):
    raise OpenWikiInspectionError(
        "invalid_json_value", f"non-finite JSON number is not supported: {value}"
    )


def _load_json(payload: bytes, label: str):
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise OpenWikiInspectionError(
            "invalid_utf8", f"{label} is not valid UTF-8"
        ) from exc
    try:
        return json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_json_constant,
        )
    except OpenWikiInspectionError:
        raise
    except json.JSONDecodeError as exc:
        raise OpenWikiInspectionError(
            "invalid_json", f"invalid JSON in {label}: {exc.msg}"
        ) from exc


def _canonical_digest(value) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return "sha256:" + _hash_bytes(payload)


def _collect_extensions(raw):
    """Preserve uninterpreted additive fields while keeping them out of trust logic."""
    extensions = []

    def record(path, row, known):
        if not isinstance(row, dict):
            return
        for field in sorted(set(row) - set(known)):
            value = row[field]
            extensions.append(
                {
                    "path": path,
                    "field": field,
                    "value": value,
                    "digest": _canonical_digest(value),
                }
            )

    if not isinstance(raw, dict):
        return extensions
    record("$", raw, {"schemaVersion", "pageVersion", "claims", "verification"})
    claims = raw.get("claims")
    if isinstance(claims, list):
        for claim_index, claim in enumerate(claims):
            claim_path = f"$.claims[{claim_index}]"
            record(claim_path, claim, {"id", "statement", "evidence"})
            if isinstance(claim, dict) and isinstance(claim.get("evidence"), list):
                for evidence_index, evidence in enumerate(claim["evidence"]):
                    record(
                        f"{claim_path}.evidence[{evidence_index}]",
                        evidence,
                        {"resource", "version"},
                    )
    verification = raw.get("verification")
    record("$.verification", verification, {"by", "at"})
    return extensions


def _normalize_relative_path(value: str, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise OpenWikiInspectionError("invalid_path", f"{label} is required")
    if CONTROL_CHARACTER.search(value):
        raise OpenWikiInspectionError(
            "path_traversal", f"{label} contains a control character"
        )
    slashed = value.replace("\\", "/")
    if slashed.startswith("/") or DRIVE_PATH.match(slashed):
        raise OpenWikiInspectionError(
            "path_traversal", f"{label} must be repository-relative: {value}"
        )
    segments = slashed.split("/")
    if any(segment in {"", ".", ".."} for segment in segments):
        raise OpenWikiInspectionError(
            "path_traversal", f"{label} contains an unsafe path segment: {value}"
        )
    normalized = posixpath.normpath(slashed)
    if normalized != slashed or normalized.startswith("../"):
        raise OpenWikiInspectionError(
            "path_traversal", f"{label} is not canonical: {value}"
        )
    return normalized


def _normalize_page(value: str) -> str:
    candidate = value.strip().lstrip("/").replace("\\", "/")
    if not candidate.startswith("openwiki/"):
        candidate = "openwiki/" + candidate
    page = _normalize_relative_path(candidate, "OpenWiki page")
    parts = page.split("/")
    if (
        len(parts) < 2
        or parts[0] != "openwiki"
        or ".claims" in {part.lower() for part in parts}
        or not page.endswith(".md")
        or parts[-1].lower() in RESERVED_PAGES
    ):
        raise OpenWikiInspectionError(
            "invalid_page_path",
            f"page must be a grounded Markdown file below openwiki/: {value}",
        )
    return page


def _sidecar_for_page(page: str) -> str:
    relative = page[len("openwiki/") : -len(".md")]
    return f"openwiki/.claims/{relative}.json"


def _page_for_sidecar(sidecar: str) -> str:
    prefix = "openwiki/.claims/"
    if not sidecar.startswith(prefix) or not sidecar.endswith(".json"):
        raise OpenWikiInspectionError(
            "invalid_sidecar_path", f"invalid OpenWiki Claims sidecar: {sidecar}"
        )
    return _normalize_page(
        "openwiki/" + sidecar[len(prefix) : -len(".json")] + ".md"
    )


def _safe_read(root: Path, relative_path: str) -> bytes:
    relative_path = _normalize_relative_path(relative_path, "snapshot path")
    root = root.resolve(strict=True)
    candidate = root.joinpath(*relative_path.split("/"))
    try:
        metadata = candidate.lstat()
    except FileNotFoundError as exc:
        raise OpenWikiInspectionError(
            "missing_file", f"snapshot file does not exist: {relative_path}"
        ) from exc
    except OSError as exc:
        raise OpenWikiInspectionError(
            "unreadable_file", f"unable to inspect snapshot file {relative_path}: {exc}"
        ) from exc
    if stat.S_ISLNK(metadata.st_mode):
        raise OpenWikiInspectionError(
            "filesystem_alias", f"snapshot file may not be a symbolic link: {relative_path}"
        )
    if not stat.S_ISREG(metadata.st_mode):
        raise OpenWikiInspectionError(
            "invalid_file_type", f"snapshot path is not a regular file: {relative_path}"
        )
    try:
        physical = candidate.resolve(strict=True)
    except OSError as exc:
        raise OpenWikiInspectionError(
            "unreadable_file", f"unable to resolve snapshot file {relative_path}: {exc}"
        ) from exc
    expected = root.joinpath(*relative_path.split("/"))
    if physical != expected:
        raise OpenWikiInspectionError(
            "filesystem_alias",
            f"snapshot path traverses a symbolic link or filesystem alias: {relative_path}",
        )
    try:
        return physical.read_bytes()
    except OSError as exc:
        raise OpenWikiInspectionError(
            "unreadable_file", f"unable to read snapshot file {relative_path}: {exc}"
        ) from exc


def _discover_sidecars(root: Path):
    wiki_root = root / "openwiki"
    claims_root = root / "openwiki" / ".claims"
    if wiki_root.is_symlink() or not wiki_root.is_dir():
        raise OpenWikiInspectionError(
            "filesystem_alias", "openwiki must be a real directory inside the snapshot"
        )
    if not claims_root.exists():
        raise OpenWikiInspectionError(
            "missing_claims_directory", "snapshot has no openwiki/.claims directory"
        )
    if claims_root.is_symlink() or not claims_root.is_dir():
        raise OpenWikiInspectionError(
            "filesystem_alias", "openwiki/.claims must be a real directory"
        )
    if wiki_root.resolve(strict=True) != wiki_root or claims_root.resolve(strict=True) != claims_root:
        raise OpenWikiInspectionError(
            "filesystem_alias", "OpenWiki directories may not traverse filesystem aliases"
        )
    sidecars = []
    for directory, dirs, files in os.walk(claims_root, followlinks=False):
        directory_path = Path(directory)
        for name in list(dirs):
            candidate = directory_path / name
            if candidate.is_symlink():
                raise OpenWikiInspectionError(
                    "filesystem_alias",
                    f"Claims directory may not contain a symbolic link: {candidate.relative_to(root).as_posix()}",
                )
        for name in files:
            if name.endswith(".json"):
                sidecars.append((directory_path / name).relative_to(root).as_posix())
    if not sidecars:
        raise OpenWikiInspectionError(
            "no_claim_sidecars", "snapshot contains no OpenWiki Claims sidecars"
        )
    return sorted(sidecars)


def _validate_sidecar(raw, label: str):
    if not isinstance(raw, dict):
        raise OpenWikiInspectionError(
            "invalid_required_field", f"{label} must contain a JSON object"
        )
    if "schemaVersion" not in raw:
        raise OpenWikiInspectionError(
            "missing_required_field", f"{label} is missing schemaVersion"
        )
    schema_version = raw["schemaVersion"]
    if isinstance(schema_version, bool) or not isinstance(schema_version, int):
        raise OpenWikiInspectionError(
            "invalid_required_field", f"{label}.schemaVersion must be an integer"
        )
    if schema_version != OPENWIKI_CLAIMS_SCHEMA_VERSION:
        raise OpenWikiInspectionError(
            "unsupported_schema_version",
            f"unsupported OpenWiki Claims schemaVersion: {schema_version}",
        )
    if "pageVersion" not in raw:
        raise OpenWikiInspectionError(
            "missing_required_field", f"{label} is missing pageVersion"
        )
    page_version = raw["pageVersion"]
    if not isinstance(page_version, str) or not PAGE_VERSION.fullmatch(page_version):
        raise OpenWikiInspectionError(
            "invalid_required_field",
            f"{label}.pageVersion must be a lowercase sha256 digest",
        )
    if "claims" not in raw:
        raise OpenWikiInspectionError(
            "missing_required_field", f"{label} is missing claims"
        )
    if not isinstance(raw["claims"], list):
        raise OpenWikiInspectionError(
            "invalid_required_field", f"{label}.claims must be an array"
        )
    claims, seen_claims = [], set()
    for claim_index, claim in enumerate(raw["claims"]):
        claim_label = f"{label}.claims[{claim_index}]"
        if not isinstance(claim, dict):
            raise OpenWikiInspectionError(
                "invalid_required_field", f"{claim_label} must be an object"
            )
        for field in ("id", "statement", "evidence"):
            if field not in claim:
                raise OpenWikiInspectionError(
                    "missing_required_field", f"{claim_label} is missing {field}"
                )
        claim_id = _canonical_string(claim["id"], f"{claim_label}.id")
        statement = _canonical_string(
            claim["statement"], f"{claim_label}.statement"
        )
        if claim_id in seen_claims:
            raise OpenWikiInspectionError(
                "duplicate_claim_id", f"duplicate claim id in {label}: {claim_id}"
            )
        seen_claims.add(claim_id)
        if not isinstance(claim["evidence"], list) or not claim["evidence"]:
            raise OpenWikiInspectionError(
                "invalid_required_field",
                f"{claim_label}.evidence must be a non-empty array",
            )
        evidence_rows, seen_resources = [], set()
        for evidence_index, evidence in enumerate(claim["evidence"]):
            evidence_label = f"{claim_label}.evidence[{evidence_index}]"
            if not isinstance(evidence, dict):
                raise OpenWikiInspectionError(
                    "invalid_required_field", f"{evidence_label} must be an object"
                )
            for field in ("resource", "version"):
                if field not in evidence:
                    raise OpenWikiInspectionError(
                        "missing_required_field", f"{evidence_label} is missing {field}"
                    )
            resource = _canonical_string(
                evidence["resource"], f"{evidence_label}.resource"
            )
            version = _canonical_string(
                evidence["version"], f"{evidence_label}.version"
            )
            if resource in seen_resources:
                raise OpenWikiInspectionError(
                    "duplicate_evidence_resource",
                    f"duplicate evidence resource in {claim_label}: {resource}",
                )
            seen_resources.add(resource)
            evidence_rows.append({"resource": resource, "version": version})
        claims.append(
            {"id": claim_id, "statement": statement, "evidence": evidence_rows}
        )
    verification = None
    if "verification" in raw:
        verification = raw["verification"]
        if not isinstance(verification, dict):
            raise OpenWikiInspectionError(
                "invalid_required_field", f"{label}.verification must be an object"
            )
        for field in ("by", "at"):
            if field not in verification:
                raise OpenWikiInspectionError(
                    "missing_required_field",
                    f"{label}.verification is missing {field}",
                )
        verification = {
            "by": _canonical_string(
                verification["by"], f"{label}.verification.by"
            ),
            "at": _canonical_string(
                verification["at"], f"{label}.verification.at"
            ),
        }
    return {
        "schemaVersion": schema_version,
        "pageVersion": page_version,
        "claims": claims,
        **({"verification": verification} if verification is not None else {}),
    }


def _parse_repository_resource(resource: str):
    if not resource.startswith("repo://"):
        raise OpenWikiInspectionError(
            "unsupported_evidence_resource", f"unsupported evidence resource: {resource}"
        )
    body = resource[len("repo://") :]
    if body.count("#") > 1:
        raise OpenWikiInspectionError(
            "invalid_evidence_resource", f"resource has multiple fragments: {resource}"
        )
    encoded_path, separator, encoded_fragment = body.partition("#")
    if PERCENT_ESCAPE.search(encoded_path) or (
        separator and PERCENT_ESCAPE.search(encoded_fragment)
    ):
        raise OpenWikiInspectionError(
            "invalid_evidence_resource", f"resource has invalid percent encoding: {resource}"
        )
    try:
        decoded_path = unquote(encoded_path, errors="strict")
        decoded_fragment = unquote(encoded_fragment, errors="strict") if separator else None
    except UnicodeError as exc:
        raise OpenWikiInspectionError(
            "invalid_evidence_resource", f"resource has invalid Unicode encoding: {resource}"
        ) from exc
    if CONTROL_CHARACTER.search(decoded_path) or (
        decoded_fragment is not None and CONTROL_CHARACTER.search(decoded_fragment)
    ):
        raise OpenWikiInspectionError(
            "invalid_evidence_resource", f"resource contains a control character: {resource}"
        )
    path = _normalize_relative_path(decoded_path.replace("\\", "/"), "evidence path")
    lowered = path.lower()
    if lowered == ".git" or lowered.startswith(".git/"):
        raise OpenWikiInspectionError(
            "invalid_evidence_resource", f"evidence may not reference Git metadata: {resource}"
        )
    if lowered == "openwiki" or lowered.startswith("openwiki/"):
        raise OpenWikiInspectionError(
            "invalid_evidence_resource", f"evidence may not reference generated OpenWiki output: {resource}"
        )
    line_range = None
    if decoded_fragment is not None:
        match = LINE_RANGE.fullmatch(decoded_fragment)
        if not match:
            raise OpenWikiInspectionError(
                "invalid_evidence_resource",
                f"evidence fragment must be a line range: {resource}",
            )
        start = int(match.group(1))
        end = int(match.group(2) or match.group(1))
        if end < start or end > 9_007_199_254_740_991:
            raise OpenWikiInspectionError(
                "invalid_evidence_resource", f"invalid evidence line range: {resource}"
            )
        line_range = (start, end)
    encoded_canonical = "/".join(
        quote(segment, safe="-_.!~*'()") for segment in path.split("/")
    )
    canonical = "repo://" + encoded_canonical
    if line_range:
        canonical += f"#L{line_range[0]}-L{line_range[1]}"
    if canonical != resource:
        raise OpenWikiInspectionError(
            "invalid_evidence_resource", f"evidence resource is not canonical: {resource}"
        )
    return path, line_range


def _split_source_lines(source: str):
    lines, start = [], 0
    while start < len(source):
        newline = source.find("\n", start)
        end = len(source) if newline == -1 else newline + 1
        lines.append(source[start:end])
        start = end
    return lines


def _decode_line_version(version: str):
    if not version.startswith(LINE_RANGE_PREFIX):
        raise OpenWikiInspectionError(
            "unsupported_evidence_version", f"unsupported evidence version: {version}"
        )
    body = version[len(LINE_RANGE_PREFIX) :]
    content_hash, separator, encoded = body.partition(":")
    if not separator or not SHA256.fullmatch(content_hash):
        raise OpenWikiInspectionError(
            "invalid_evidence_version", f"invalid line-range evidence version: {version}"
        )
    try:
        padded = encoded + "=" * (-len(encoded) % 4)
        decoded = base64.b64decode(padded, altchars=b"-_", validate=True)
        if base64.urlsafe_b64encode(decoded).decode("ascii").rstrip("=") != encoded:
            raise ValueError("non-canonical base64url")
        metadata = json.loads(
            decoded.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_json_constant,
        )
    except Exception as exc:
        raise OpenWikiInspectionError(
            "invalid_evidence_version", "invalid line-range relocation metadata"
        ) from exc
    if not isinstance(metadata, dict) or set(metadata) != METADATA_KEYS:
        raise OpenWikiInspectionError(
            "invalid_evidence_version", "invalid line-range relocation metadata shape"
        )
    for field, minimum, maximum in (
        ("selectedLineCount", 1, 9_007_199_254_740_991),
        ("precedingContextLineCount", 0, RANGE_CONTEXT_LINE_COUNT),
        ("followingContextLineCount", 0, RANGE_CONTEXT_LINE_COUNT),
    ):
        value = metadata[field]
        if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
            raise OpenWikiInspectionError(
                "invalid_evidence_version", f"invalid line-range metadata field: {field}"
            )
    for field in (
        "firstSelectedLineHash",
        "lastSelectedLineHash",
        "precedingContextHash",
        "followingContextHash",
    ):
        if not isinstance(metadata[field], str) or not SHA256.fullmatch(metadata[field]):
            raise OpenWikiInspectionError(
                "invalid_evidence_version", f"invalid line-range metadata field: {field}"
            )
    return content_hash, metadata


def _line_content(lines, span):
    return "".join(lines[span[0] : span[1]])


def _context_matches(lines, span, metadata):
    before_count = metadata["precedingContextLineCount"]
    after_count = metadata["followingContextLineCount"]
    before = (
        span[0] == 0
        if before_count == 0
        else span[0] >= before_count
        and _hash_text("".join(lines[span[0] - before_count : span[0]]))
        == metadata["precedingContextHash"]
    )
    after = (
        span[1] == len(lines)
        if after_count == 0
        else span[1] + after_count <= len(lines)
        and _hash_text("".join(lines[span[1] : span[1] + after_count]))
        == metadata["followingContextHash"]
    )
    return before and after


def _locate_unchanged(lines, hinted_span, content_hash, metadata):
    selected_count = metadata["selectedLineCount"]
    if (
        hinted_span
        and hinted_span[1] - hinted_span[0] == selected_count
        and _hash_text(_line_content(lines, hinted_span)) == content_hash
    ):
        return hinted_span
    line_hashes = [_hash_text(line) for line in lines]
    matches = []
    for start in range(0, len(lines) - selected_count + 1):
        end = start + selected_count
        if (
            line_hashes[start] == metadata["firstSelectedLineHash"]
            and line_hashes[end - 1] == metadata["lastSelectedLineHash"]
            and _hash_text(_line_content(lines, (start, end))) == content_hash
        ):
            matches.append((start, end))
    if len(matches) == 1:
        return matches[0]
    context_matches = [
        span for span in matches if _context_matches(lines, span, metadata)
    ]
    return context_matches[0] if len(context_matches) == 1 else None


def _context_boundaries(lines, count, expected_hash, side):
    if count == 0:
        return [0 if side == "before" else len(lines)]
    result = []
    for start in range(0, len(lines) - count + 1):
        if _hash_text("".join(lines[start : start + count])) == expected_hash:
            result.append(start + count if side == "before" else start)
    return result


def _locate_changed(lines, metadata):
    starts = _context_boundaries(
        lines,
        metadata["precedingContextLineCount"],
        metadata["precedingContextHash"],
        "before",
    )
    ends = _context_boundaries(
        lines,
        metadata["followingContextLineCount"],
        metadata["followingContextHash"],
        "after",
    )
    candidates = [(start, end) for start in starts for end in ends if end > start]
    return candidates[0] if len(candidates) == 1 else None


def _format_line_version(lines, span):
    preceding_start = max(0, span[0] - RANGE_CONTEXT_LINE_COUNT)
    following_end = min(len(lines), span[1] + RANGE_CONTEXT_LINE_COUNT)
    metadata = {
        "selectedLineCount": span[1] - span[0],
        "firstSelectedLineHash": _hash_text(lines[span[0]]),
        "lastSelectedLineHash": _hash_text(lines[span[1] - 1]),
        "precedingContextLineCount": span[0] - preceding_start,
        "precedingContextHash": _hash_text("".join(lines[preceding_start : span[0]])),
        "followingContextLineCount": following_end - span[1],
        "followingContextHash": _hash_text("".join(lines[span[1] : following_end])),
    }
    encoded = base64.urlsafe_b64encode(
        json.dumps(metadata, separators=(",", ":")).encode("utf-8")
    ).decode("ascii").rstrip("=")
    return LINE_RANGE_PREFIX + _hash_text(_line_content(lines, span)) + ":" + encoded


def _check_evidence(root: Path, evidence):
    resource, expected_version = evidence["resource"], evidence["version"]
    try:
        source_path, line_range = _parse_repository_resource(resource)
    except OpenWikiInspectionError as exc:
        return {
            **evidence,
            "current": False,
            "status": "invalid",
            "issue": _issue(exc.code, str(exc)),
            "format_valid": False,
        }
    try:
        source_bytes = _safe_read(root, source_path)
        source = source_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return {
            **evidence,
            "current": False,
            "status": "invalid",
            "issue": _issue("invalid_utf8", f"evidence source is not UTF-8: {source_path}"),
            "format_valid": True,
        }
    except OpenWikiInspectionError as exc:
        return {
            **evidence,
            "current": False,
            "status": "missing" if exc.code == "missing_file" else "invalid",
            "issue": _issue(exc.code, str(exc)),
            "format_valid": True,
        }
    if line_range is None:
        match = WHOLE_FILE_VERSION.fullmatch(expected_version)
        if not match:
            return {
                **evidence,
                "current": False,
                "status": "invalid",
                "issue": _issue(
                    "unsupported_evidence_version",
                    f"unsupported whole-file evidence version: {expected_version}",
                ),
                "format_valid": False,
            }
        observed = "repo-file-v1:sha256:" + _hash_bytes(source_bytes)
        current = observed == expected_version
        return {
            **evidence,
            "current": current,
            "status": "current" if current else "mismatch",
            "observed_version": observed,
            "format_valid": True,
            **(
                {}
                if current
                else {
                    "issue": _issue(
                        "evidence_version_mismatch",
                        f"evidence version changed for {resource}",
                    )
                }
            ),
        }
    try:
        content_hash, metadata = _decode_line_version(expected_version)
    except OpenWikiInspectionError as exc:
        return {
            **evidence,
            "current": False,
            "status": "invalid",
            "issue": _issue(exc.code, str(exc)),
            "format_valid": False,
        }
    lines = _split_source_lines(source)
    start, end = line_range
    hinted = (start - 1, end) if end <= len(lines) else None
    unchanged = _locate_unchanged(lines, hinted, content_hash, metadata)
    if unchanged:
        return {
            **evidence,
            "current": True,
            "status": "current",
            "observed_version": expected_version,
            "format_valid": True,
        }
    changed = _locate_changed(lines, metadata)
    if not changed:
        return {
            **evidence,
            "current": False,
            "status": "unresolved",
            "issue": _issue(
                "evidence_range_unresolved",
                f"evidence range no longer resolves uniquely: {resource}",
            ),
            "format_valid": True,
        }
    observed = _format_line_version(lines, changed)
    return {
        **evidence,
        "current": False,
        "status": "mismatch",
        "observed_version": observed,
        "issue": _issue(
            "evidence_version_mismatch", f"evidence version changed for {resource}"
        ),
        "format_valid": True,
    }


def _inspect_page(root: Path, page: str, sidecar: str):
    result = {
        "page": page,
        "sidecar": sidecar,
        "format_valid": True,
        "page_bound": False,
        "evidence_current": False,
        "origin_authenticated": False,
        "origin_authentication": "not_provided_by_openwiki_claims_schema_v1",
        "issues": [],
        "claims": [],
    }
    try:
        sidecar_bytes = _safe_read(root, sidecar)
        result["sidecar_digest"] = "sha256:" + _hash_bytes(sidecar_bytes)
        raw = _load_json(sidecar_bytes, sidecar)
        extensions = _collect_extensions(raw)
        result["extension_fields_present"] = bool(extensions)
        result["extension_fields"] = extensions
        result["extension_fields_digest"] = _canonical_digest(extensions)
        parsed = _validate_sidecar(raw, sidecar)
    except OpenWikiInspectionError as exc:
        result["format_valid"] = False
        result["issues"].append(_issue(exc.code, str(exc)))
        return result
    result["schema_version"] = parsed["schemaVersion"]
    result["expected_page_version"] = parsed["pageVersion"]
    result["producer_verification"] = parsed.get("verification")
    try:
        page_bytes = _safe_read(root, page)
        observed_page_version = "sha256:" + _hash_bytes(page_bytes)
        result["observed_page_version"] = observed_page_version
        result["page_bound"] = observed_page_version == parsed["pageVersion"]
        if not result["page_bound"]:
            result["issues"].append(
                _issue(
                    "page_version_mismatch",
                    f"sidecar pageVersion does not match exact page bytes: {page}",
                )
            )
    except OpenWikiInspectionError as exc:
        result["issues"].append(_issue(exc.code, str(exc)))
    evidence_all_current = True
    for claim in parsed["claims"]:
        checked = [_check_evidence(root, row) for row in claim["evidence"]]
        for row in checked:
            if not row.pop("format_valid"):
                result["format_valid"] = False
            if row.get("issue"):
                result["issues"].append(
                    {**row["issue"], "claim_id": claim["id"], "resource": row["resource"]}
                )
        claim_current = all(row["current"] for row in checked)
        evidence_all_current = evidence_all_current and claim_current
        result["claims"].append(
            {
                "id": claim["id"],
                "statement": claim["statement"],
                "evidence": checked,
                "evidence_current": claim_current,
                "lineage": "exact_producer_claim",
                "proofpress_admission": "not_inherited",
            }
        )
    result["evidence_current"] = evidence_all_current
    result["claim_count"] = len(result["claims"])
    return result


def inspect_openwiki_snapshot(root, pages=None):
    """Inspect an OpenWiki schema-v1 repository snapshot without mutating it."""
    root = Path(root)
    report = {
        "schema_version": REPORT_SCHEMA,
        "mode": "experimental_read_only",
        "openwiki_claims_schema_version": OPENWIKI_CLAIMS_SCHEMA_VERSION,
        "trust_semantics": {
            "exact_copy": "preserves producer lineage signals but does not inherit Proofpress admission",
            "rewrite": "is a derived claim requiring new identity, evidence, and admission",
        },
        "pages": [],
        "issues": [],
    }
    try:
        root = root.resolve(strict=True)
        if not root.is_dir():
            raise OpenWikiInspectionError(
                "invalid_snapshot_root", "snapshot root must be a directory"
            )
        if pages:
            normalized_pages = sorted({_normalize_page(page) for page in pages})
            sidecars = [_sidecar_for_page(page) for page in normalized_pages]
        else:
            sidecars = _discover_sidecars(root)
            normalized_pages = [_page_for_sidecar(sidecar) for sidecar in sidecars]
        report["pages"] = [
            _inspect_page(root, page, sidecar)
            for page, sidecar in zip(normalized_pages, sidecars)
        ]
    except (OSError, OpenWikiInspectionError) as exc:
        code = exc.code if isinstance(exc, OpenWikiInspectionError) else "invalid_snapshot_root"
        report["issues"].append(_issue(code, str(exc)))
    owners = {}
    for page_result in report["pages"]:
        for claim in page_result["claims"]:
            owners.setdefault(claim["id"], []).append(page_result)
    for claim_id, page_results in owners.items():
        if len(page_results) > 1:
            for page_result in page_results:
                page_result["format_valid"] = False
                page_result["issues"].append(
                    _issue(
                        "duplicate_claim_id",
                        f"claim id is owned by multiple pages: {claim_id}",
                        claim_id=claim_id,
                    )
                )
    format_valid = not report["issues"] and bool(report["pages"]) and all(
        page["format_valid"] for page in report["pages"]
    )
    page_bound = bool(report["pages"]) and all(
        page["page_bound"] for page in report["pages"]
    )
    evidence_current = bool(report["pages"]) and all(
        page["evidence_current"] for page in report["pages"]
    )
    report["summary"] = {
        "page_count": len(report["pages"]),
        "claim_count": sum(page.get("claim_count", 0) for page in report["pages"]),
        "format_valid": format_valid,
        "page_bound": page_bound,
        "evidence_current": evidence_current,
        "origin_authenticated": False,
        "origin_authentication": "not_provided_by_openwiki_claims_schema_v1",
        "extension_fields_present": any(
            page.get("extension_fields_present", False) for page in report["pages"]
        ),
        "proofpress_review_required": True,
    }
    report["inspection_passed"] = format_valid and page_bound and evidence_current
    return report


def canonical_handoff_manifest_bytes(manifest) -> bytes:
    """Serialize one manifest without embedding host-specific path state."""
    return json.dumps(
        manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def handoff_manifest_digest(manifest) -> str:
    """Return the deterministic digest used by a producer-origin attestation."""
    return "sha256:" + _hash_bytes(canonical_handoff_manifest_bytes(manifest))


def _ancestor_indexes(page: str):
    parts = page.split("/")[:-1]
    return ["/".join(parts[:depth] + ["index.md"]) for depth in range(1, len(parts) + 1)]


def build_handoff_manifest(root, report=None, *, selection_mode="full_snapshot"):
    """Bind the exact files consumed by a read-only OpenWiki inspection.

    The manifest is intentionally a byte inventory, not an admission record.
    Its digest can be the subject of a producer-origin attestation without
    changing page binding, evidence freshness, or Proofpress admission.
    """
    root = Path(root).resolve(strict=True)
    if selection_mode not in HANDOFF_SELECTION_MODES:
        raise OpenWikiInspectionError(
            "invalid_selection_mode",
            f"unsupported handoff selection mode: {selection_mode}",
        )
    report = report or inspect_openwiki_snapshot(root)
    pages = sorted(page["page"] for page in report.get("pages", []))
    if not pages:
        raise OpenWikiInspectionError(
            "empty_selection", "handoff manifest requires at least one inspected page"
        )
    if selection_mode == "full_snapshot":
        discovered_pages = sorted(
            _page_for_sidecar(sidecar) for sidecar in _discover_sidecars(root)
        )
        if pages != discovered_pages:
            raise OpenWikiInspectionError(
                "selection_mismatch",
                "full_snapshot manifest requires every discovered Claims sidecar",
            )
    roles = {}

    def add(path, role, *, optional=False):
        try:
            path = _normalize_relative_path(path, "manifest material")
            _safe_read(root, path)
        except OpenWikiInspectionError:
            if optional:
                return
            raise
        roles.setdefault(path, set()).add(role)

    for page in report.get("pages", []):
        add(page["page"], "page")
        add(page["sidecar"], "claims_sidecar")
        for index in _ancestor_indexes(page["page"]):
            add(index, "navigation_index", optional=True)
        for claim in page.get("claims", []):
            for evidence in claim.get("evidence", []):
                evidence_path, _ = _parse_repository_resource(evidence["resource"])
                add(evidence_path, "source_evidence")

    for metadata_path in (
        ".openwikiignore",
        "openwiki/.openwikiignore",
        "openwiki/.last-update.json",
    ):
        add(metadata_path, "producer_metadata", optional=True)

    materials = [
        {
            "path": path,
            "roles": sorted(roles[path]),
            "sha256": _hash_bytes(_safe_read(root, path)),
        }
        for path in sorted(roles)
    ]
    return {
        "schema_version": HANDOFF_MANIFEST_SCHEMA,
        "claims_schema_version": OPENWIKI_CLAIMS_SCHEMA_VERSION,
        "selection": {"mode": selection_mode, "pages": pages},
        "materials": materials,
    }


def _print_text(report):
    summary = report["summary"]
    status = "passed" if report["inspection_passed"] else "failed"
    print(f"OpenWiki Claims v1 inspection {status}")
    print(f"  format valid:        {'yes' if summary['format_valid'] else 'no'}")
    print(f"  exact page bound:     {'yes' if summary['page_bound'] else 'no'}")
    print(f"  evidence current:     {'yes' if summary['evidence_current'] else 'no'}")
    print("  origin authenticated: no (not provided by schema v1)")
    print(f"  pages / claims:       {summary['page_count']} / {summary['claim_count']}")
    issues = list(report["issues"])
    for page in report["pages"]:
        issues.extend({**issue, "page": page["page"]} for issue in page["issues"])
    for issue in issues:
        location = f" [{issue['page']}]" if issue.get("page") else ""
        print(f"  {issue['code']}{location}: {issue['message']}")
    print("  admission:            not performed")


def cmd_inspect(args):
    report = inspect_openwiki_snapshot(args.root, args.page)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _print_text(report)
    if not report["inspection_passed"]:
        raise SystemExit(1)


def add_cli(subparsers):
    parser = subparsers.add_parser(
        "openwiki", help="experimental read-only OpenWiki Claims interoperability"
    )
    commands = parser.add_subparsers(dest="openwiki_cmd", required=True)
    inspect_parser = commands.add_parser(
        "inspect",
        help="check schema-v1 sidecars against exact page bytes and source evidence",
    )
    inspect_parser.add_argument("root", help="frozen OpenWiki repository snapshot")
    inspect_parser.add_argument(
        "--page",
        action="append",
        default=[],
        help="grounded page below openwiki/; repeat to inspect selected pages",
    )
    inspect_parser.add_argument("--json", action="store_true")
    inspect_parser.set_defaults(f=cmd_inspect)

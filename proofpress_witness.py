"""Offline verification for purpose-scoped Cloud Witness attestations.

The signed object is a DSSE envelope containing an in-toto Statement. It is
not a live transparency-service receipt: offline verification can establish a
signature, exact subject/binding coverage, and authorization recorded in an
external trust snapshot, but current authority remains unknown.
"""

import base64
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import tempfile
from typing import Any


TRUST_PROTOCOL = "proofpress.witness-trust"
TRUST_PROTOCOL_VERSION = 1
DSSE_PAYLOAD_TYPE = "application/vnd.in-toto+json"
IN_TOTO_STATEMENT_TYPE = "https://in-toto.io/Statement/v1"
OPENWIKI_PRODUCER_ORIGIN_PROFILE = (
    "https://proofpress.dev/attestation/openwiki-producer-origin/v1"
)
GOVERNANCE_DECISION_PROFILE = (
    "https://proofpress.dev/attestation/governance-decision/v1"
)
SUPPORTED_PROFILES = {
    OPENWIKI_PRODUCER_ORIGIN_PROFILE,
    GOVERNANCE_DECISION_PROFILE,
}
# No predicate extensions have critical semantics in v1. A later implementation
# must add an extension here only after it implements and tests that extension.
SUPPORTED_CRITICAL_EXTENSIONS: frozenset[str] = frozenset()
# DER SubjectPublicKeyInfo encoding prefix for the Ed25519 OID (1.3.101.112).
# The remaining 32 bytes are the raw public key. Checking this output from the
# crypto provider prevents a PEM for another key type from masquerading behind
# the unsigned ``algorithm: ed25519`` trust-store label.
ED25519_SPKI_PREFIX = bytes.fromhex("302a300506032b6570032100")


class WitnessError(ValueError):
    """Raised when an attestation, expectation, or trust store is malformed."""


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise WitnessError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_nonfinite_json(value: str) -> None:
    raise WitnessError(f"non-finite JSON number is not allowed: {value}")


def loads_json(payload: str | bytes) -> Any:
    """Parse JSON while rejecting duplicate keys at every object depth."""
    try:
        return json.loads(
            payload,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_nonfinite_json,
        )
    except WitnessError:
        raise
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise WitnessError("invalid JSON") from exc


def load_json_file(path: os.PathLike[str] | str) -> Any:
    return loads_json(Path(path).read_bytes())


def dsse_pae(payload_type: str, payload: bytes) -> bytes:
    """Return DSSE v1 pre-authentication encoding for exact payload bytes."""
    if not isinstance(payload_type, str) or not payload_type:
        raise WitnessError("DSSE payloadType must be a non-empty string")
    try:
        encoded_type = payload_type.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise WitnessError("DSSE payloadType must be UTF-8") from exc
    return b" ".join((
        b"DSSEv1",
        str(len(encoded_type)).encode("ascii"),
        encoded_type,
        str(len(payload)).encode("ascii"),
        payload,
    ))


def _sha256_file(path: os.PathLike[str] | str) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require_nonempty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise WitnessError(f"{field} must be a non-empty string")
    return value


def _require_sha256(value: Any, field: str) -> None:
    if (not isinstance(value, str) or len(value) != 64
            or any(char not in "0123456789abcdef" for char in value)):
        raise WitnessError(f"{field} must be lowercase sha256 hex")


def _require_sha256_binding(value: Any, field: str) -> None:
    if not isinstance(value, dict) or value.get("algorithm") != "sha256":
        raise WitnessError(f"{field} must use sha256")
    _require_sha256(value.get("digest"), f"{field}.digest")


def _require_string_list(
    value: Any, field: str, *, allow_empty: bool = False
) -> list[str]:
    if (not isinstance(value, list) or (not value and not allow_empty)
            or any(not isinstance(item, str) or not item for item in value)):
        qualifier = "" if allow_empty else "non-empty "
        raise WitnessError(f"{field} must be a {qualifier}string array")
    if len(set(value)) != len(value):
        raise WitnessError(f"{field} must not contain duplicates")
    return value


def _parse_timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        raise WitnessError(f"{field} must be an RFC3339 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise WitnessError(f"{field} must be an RFC3339 timestamp") from exc
    if parsed.tzinfo is None:
        raise WitnessError(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _validate_profile_bindings(profile: str, bindings: Any, field: str) -> None:
    if not isinstance(bindings, dict):
        raise WitnessError(f"{field} must be an object")
    if profile == OPENWIKI_PRODUCER_ORIGIN_PROFILE:
        _require_sha256_binding(
            bindings.get("handoff_manifest"), f"{field}.handoff_manifest")
        producer = bindings.get("producer")
        if not isinstance(producer, dict):
            raise WitnessError(f"{field}.producer must be an object")
        _require_nonempty_string(producer.get("id"), f"{field}.producer.id")
        _require_nonempty_string(
            producer.get("run_id"), f"{field}.producer.run_id")
        return
    if profile == GOVERNANCE_DECISION_PROFILE:
        _require_sha256_binding(
            bindings.get("handoff_manifest"), f"{field}.handoff_manifest")
        _require_sha256_binding(bindings.get("decision"), f"{field}.decision")
        contradiction = bindings.get("contradiction")
        if not isinstance(contradiction, dict):
            raise WitnessError(f"{field}.contradiction must be an object")
        if contradiction.get("type") != "contradicts":
            raise WitnessError(f"{field}.contradiction.type must be contradicts")
        _require_nonempty_string(
            contradiction.get("left_claim_id"),
            f"{field}.contradiction.left_claim_id")
        _require_nonempty_string(
            contradiction.get("right_claim_id"),
            f"{field}.contradiction.right_claim_id")
        if contradiction["left_claim_id"] == contradiction["right_claim_id"]:
            raise WitnessError(f"{field}.contradiction endpoints must differ")
        resolution = bindings.get("resolution")
        if not isinstance(resolution, dict) or resolution.get("action") not in {
                "supersede_left", "supersede_right", "withhold_both"}:
            raise WitnessError(f"{field}.resolution.action is unsupported")
        policy = bindings.get("policy")
        if not isinstance(policy, dict):
            raise WitnessError(f"{field}.policy must be an object")
        _require_nonempty_string(policy.get("id"), f"{field}.policy.id")
        _require_sha256(policy.get("digest"), f"{field}.policy.digest")
        epoch = policy.get("epoch")
        if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 0:
            raise WitnessError(f"{field}.policy.epoch must be non-negative")
        ledger = bindings.get("ledger")
        if not isinstance(ledger, dict):
            raise WitnessError(f"{field}.ledger must be an object")
        previous = _require_nonempty_string(
            ledger.get("previous_head"), f"{field}.ledger.previous_head")
        resulting = _require_nonempty_string(
            ledger.get("resulting_head"), f"{field}.ledger.resulting_head")
        if previous == resulting:
            raise WitnessError(f"{field}.ledger heads must differ")
        return
    raise WitnessError("unsupported attestation profile")


def _decode_attestation(attestation: dict[str, Any]) -> tuple[
        dict[str, Any], dict[str, Any], dict[str, Any], bytes]:
    if not isinstance(attestation, dict):
        raise WitnessError("DSSE envelope must be an object")
    envelope = attestation
    payload_type = envelope.get("payloadType")
    if payload_type != DSSE_PAYLOAD_TYPE:
        raise WitnessError("unsupported DSSE payloadType")
    encoded_payload = envelope.get("payload")
    if not isinstance(encoded_payload, str):
        raise WitnessError("envelope.payload must be base64")
    try:
        payload = base64.b64decode(encoded_payload, validate=True)
    except (ValueError, TypeError) as exc:
        raise WitnessError("envelope.payload must be base64") from exc
    statement = loads_json(payload)
    if not isinstance(statement, dict):
        raise WitnessError("in-toto statement must be an object")
    if statement.get("_type") != IN_TOTO_STATEMENT_TYPE:
        raise WitnessError("unsupported in-toto statement type")
    subjects = statement.get("subject")
    if not isinstance(subjects, list) or len(subjects) != 1:
        raise WitnessError("statement must contain exactly one subject")
    subject = subjects[0]
    if not isinstance(subject, dict):
        raise WitnessError("statement subject must be an object")
    _require_nonempty_string(subject.get("name"), "statement.subject[0].name")
    digest = subject.get("digest")
    if not isinstance(digest, dict):
        raise WitnessError("statement.subject[0].digest must be an object")
    _require_sha256(digest.get("sha256"), "statement.subject[0].digest.sha256")
    profile = statement.get("predicateType")
    if profile not in SUPPORTED_PROFILES:
        raise WitnessError("unsupported attestation profile")
    predicate = statement.get("predicate")
    if not isinstance(predicate, dict):
        raise WitnessError("statement.predicate must be an object")
    _require_nonempty_string(predicate.get("issuer"), "predicate.issuer")
    _require_nonempty_string(predicate.get("tenant"), "predicate.tenant")
    _require_nonempty_string(predicate.get("audience"), "predicate.audience")
    _require_nonempty_string(predicate.get("principal"), "predicate.principal")
    _require_nonempty_string(predicate.get("key_id"), "predicate.key_id")
    _require_nonempty_string(predicate.get("statement_id"), "predicate.statement_id")
    critical = _require_string_list(
        predicate.get("critical"), "predicate.critical", allow_empty=True)
    unknown_critical = sorted(
        set(critical).difference(SUPPORTED_CRITICAL_EXTENSIONS))
    if unknown_critical:
        raise WitnessError(
            "unsupported critical extension: " + ", ".join(unknown_critical))
    issued_at = _parse_timestamp(predicate.get("issued_at"), "predicate.issued_at")
    expires_at = _parse_timestamp(predicate.get("expires_at"), "predicate.expires_at")
    if expires_at <= issued_at:
        raise WitnessError("predicate.expires_at must be later than issued_at")
    _validate_profile_bindings(
        profile, predicate.get("bindings"), "predicate.bindings")
    signatures = envelope.get("signatures")
    if not isinstance(signatures, list) or len(signatures) != 1:
        raise WitnessError("envelope must contain exactly one signature")
    signature = signatures[0]
    if not isinstance(signature, dict):
        raise WitnessError("envelope signature must be an object")
    _require_nonempty_string(signature.get("keyid"), "signature.keyid")
    encoded_signature = signature.get("sig")
    if not isinstance(encoded_signature, str):
        raise WitnessError("signature.sig must be base64")
    try:
        base64.b64decode(encoded_signature, validate=True)
    except (ValueError, TypeError) as exc:
        raise WitnessError("signature.sig must be base64") from exc
    return envelope, statement, predicate, payload


def validate_trust_store(trust_store: dict[str, Any]) -> None:
    if not isinstance(trust_store, dict):
        raise WitnessError("trust store must be an object")
    if trust_store.get("protocol") != TRUST_PROTOCOL:
        raise WitnessError("unsupported witness trust protocol")
    if trust_store.get("protocol_version") != TRUST_PROTOCOL_VERSION:
        raise WitnessError("unsupported witness trust protocol version")
    issuers = trust_store.get("issuers")
    if not isinstance(issuers, dict):
        raise WitnessError("trust store issuers must be an object")
    for issuer, issuer_entry in issuers.items():
        _require_nonempty_string(issuer, "trust store issuer id")
        keys = issuer_entry.get("keys") if isinstance(issuer_entry, dict) else None
        if not isinstance(keys, dict):
            raise WitnessError(f"trust store issuer {issuer!r} must contain keys")
        for key_id, key in keys.items():
            _require_nonempty_string(key_id, "trust store key id")
            if not isinstance(key, dict) or key.get("algorithm") != "ed25519":
                raise WitnessError("trust store keys must use ed25519")
            pem = key.get("public_key_pem")
            if not isinstance(pem, str) or "BEGIN PUBLIC KEY" not in pem:
                raise WitnessError("trust store keys require public_key_pem")
            if not _public_key_is_ed25519(pem):
                raise WitnessError("trust store public key is not Ed25519")
            if key.get("status") not in {"active", "revoked", "suspended"}:
                raise WitnessError("trust store key status is unsupported")
            not_before = _parse_timestamp(
                key.get("not_before"), "trust store key not_before")
            not_after = _parse_timestamp(
                key.get("not_after"), "trust store key not_after")
            if not_after <= not_before:
                raise WitnessError("trust store key validity window is invalid")
            profiles = _require_string_list(key.get("profiles"), "key.profiles")
            if any(profile not in SUPPORTED_PROFILES for profile in profiles):
                raise WitnessError("trust store key profile is unsupported")
            _require_string_list(key.get("tenants"), "key.tenants")
            _require_string_list(key.get("audiences"), "key.audiences")
            _require_string_list(key.get("principals"), "key.principals")


def _public_key_is_ed25519(public_key_pem: str) -> bool:
    """Cryptographically identify an Ed25519 SPKI, not just its metadata."""
    with tempfile.TemporaryDirectory(prefix="proofpress-witness-key-") as directory:
        key_path = Path(directory) / "witness-public.pem"
        key_path.write_text(public_key_pem, encoding="utf-8")
        completed = subprocess.run(
            ["openssl", "pkey", "-pubin", "-in", str(key_path),
             "-pubout", "-outform", "DER"],
            capture_output=True,
        )
    return (
        completed.returncode == 0
        and len(completed.stdout) == len(ED25519_SPKI_PREFIX) + 32
        and completed.stdout.startswith(ED25519_SPKI_PREFIX)
    )


def _verify_ed25519(payload: bytes, signature: bytes, public_key_pem: str) -> bool:
    """Use the system crypto provider without retaining a local private key."""
    with tempfile.TemporaryDirectory(prefix="proofpress-witness-") as directory:
        root = Path(directory)
        payload_path = root / "payload.bin"
        signature_path = root / "attestation.sig"
        key_path = root / "witness-public.pem"
        payload_path.write_bytes(payload)
        signature_path.write_bytes(signature)
        key_path.write_text(public_key_pem, encoding="utf-8")
        completed = subprocess.run(
            ["openssl", "pkeyutl", "-verify", "-rawin", "-pubin",
             "-inkey", str(key_path), "-in", str(payload_path),
             "-sigfile", str(signature_path)],
            capture_output=True, text=True,
        )
    return completed.returncode == 0


def _contains_expected(actual: Any, expected: Any) -> bool:
    """Match an independently supplied expectation, allowing additive fields."""
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return all(
            key in actual and _contains_expected(actual[key], value)
            for key, value in expected.items()
        )
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(
            _contains_expected(observed, wanted)
            for observed, wanted in zip(actual, expected)
        )
    return actual == expected


def _base_result() -> dict[str, Any]:
    return {
        "attestation_format_valid": False,
        "expectations_valid": False,
        "signature_valid": False,
        "subject_bound": False,
        "bindings_bound": False,
        "profile_bound": False,
        "tenant_bound": False,
        "audience_bound": False,
        "principal_bound": False,
        "key_id_bound": False,
        "statement_identity_bound": False,
        "statement_identity_conflict": False,
        "statement_identity_status": "unverified",
        "handoff_manifest_digest": None,
        "trust_scope_authorized": False,
        "key_status_allowed": False,
        "key_valid_at_issuance": False,
        "attestation_time_valid": False,
        "producer_origin_authenticated": False,
        "decision_authority_authenticated": False,
        "authority_current": "unknown",
        "checks": [],
    }


def _check(result: dict[str, Any], name: str, passed: bool) -> None:
    result["checks"].append({
        "type": name,
        "status": "passed" if passed else "failed",
    })


def statement_identity_conflict(
    previous: dict[str, Any], current: dict[str, Any]
) -> bool:
    """Detect equivocation without treating an exact re-verification as conflict."""
    previous_id = _require_nonempty_string(
        previous.get("statement_id"), "previous.statement_id")
    current_id = _require_nonempty_string(
        current.get("statement_id"), "current.statement_id")
    previous_digest = previous.get("statement_digest")
    current_digest = current.get("statement_digest")
    _require_sha256(previous_digest, "previous.statement_digest")
    _require_sha256(current_digest, "current.statement_digest")
    return previous_id == current_id and previous_digest != current_digest


def verify_attestation_digest(
    observed_sha256: str,
    attestation: dict[str, Any],
    trust_store: dict[str, Any],
    *,
    expected_profile: str,
    expected_bindings: dict[str, Any],
    expected_tenant: str,
    expected_audience: str,
    expected_principal: str,
    expected_statement_id: str | None = None,
    expected_statement_digest: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Verify an exact digest against an external, purpose-scoped trust contract."""
    result = _base_result()
    try:
        _require_sha256(observed_sha256, "observed_sha256")
        envelope, statement, predicate, payload = _decode_attestation(attestation)
        validate_trust_store(trust_store)
    except WitnessError as exc:
        result["checks"].append({
            "type": "attestation_format", "status": "failed",
            "detail": str(exc),
        })
        return result
    result["attestation_format_valid"] = True
    _check(result, "attestation_format", True)

    try:
        if expected_profile not in SUPPORTED_PROFILES:
            raise WitnessError("expected_profile is unsupported")
        _require_nonempty_string(expected_tenant, "expected_tenant")
        _require_nonempty_string(expected_audience, "expected_audience")
        _require_nonempty_string(expected_principal, "expected_principal")
        if ((expected_statement_id is None)
                != (expected_statement_digest is None)):
            raise WitnessError(
                "expected statement id and digest must be provided together")
        if expected_statement_id is not None:
            _require_nonempty_string(
                expected_statement_id, "expected_statement_id")
            _require_sha256(
                expected_statement_digest, "expected_statement_digest")
        _validate_profile_bindings(
            expected_profile, expected_bindings, "expected_bindings")
    except WitnessError as exc:
        result["checks"].append({
            "type": "expectation_contract", "status": "failed",
            "detail": str(exc),
        })
        return result
    result["expectations_valid"] = True
    _check(result, "expectation_contract", True)

    profile = statement["predicateType"]
    result["profile"] = profile
    result["statement_id"] = predicate["statement_id"]
    result["statement_digest"] = hashlib.sha256(payload).hexdigest()
    result["handoff_manifest_digest"] = predicate["bindings"][
        "handoff_manifest"]["digest"]
    if expected_statement_id is None:
        result["statement_identity_bound"] = True
        result["statement_identity_status"] = "unconstrained"
    else:
        same_id = result["statement_id"] == expected_statement_id
        same_digest = result["statement_digest"] == expected_statement_digest
        result["statement_identity_bound"] = same_id and same_digest
        result["statement_identity_conflict"] = same_id and not same_digest
        if result["statement_identity_bound"]:
            result["statement_identity_status"] = "matched"
        elif result["statement_identity_conflict"]:
            result["statement_identity_status"] = "conflict"
        else:
            result["statement_identity_status"] = "different"
    result["profile_bound"] = profile == expected_profile
    result["tenant_bound"] = predicate["tenant"] == expected_tenant
    result["audience_bound"] = predicate["audience"] == expected_audience
    result["principal_bound"] = predicate["principal"] == expected_principal
    result["subject_bound"] = (
        statement["subject"][0]["digest"]["sha256"] == observed_sha256)
    result["bindings_bound"] = _contains_expected(
        predicate["bindings"], expected_bindings)
    _check(result, "profile_binding", result["profile_bound"])
    _check(result, "tenant_binding", result["tenant_bound"])
    _check(result, "audience_binding", result["audience_bound"])
    _check(result, "principal_binding", result["principal_bound"])
    _check(result, "statement_identity", result["statement_identity_bound"])
    _check(result, "subject_binding", result["subject_bound"])
    _check(result, "expected_bindings", result["bindings_bound"])

    issuer = predicate["issuer"]
    signature_entry = envelope["signatures"][0]
    key_id = predicate["key_id"]
    result["key_id_bound"] = signature_entry["keyid"] == key_id
    _check(result, "signed_key_id", result["key_id_bound"])
    key = trust_store.get("issuers", {}).get(issuer, {}).get(
        "keys", {}).get(key_id)
    key_trusted = key is not None
    _check(result, "trusted_key", key_trusted)

    if key_trusted:
        result["key_status_allowed"] = key["status"] == "active"
        result["trust_scope_authorized"] = all((
            profile in key["profiles"],
            predicate["tenant"] in key["tenants"],
            predicate["audience"] in key["audiences"],
            predicate["principal"] in key["principals"],
        ))
        issued_at = _parse_timestamp(predicate["issued_at"], "issued_at")
        not_before = _parse_timestamp(key["not_before"], "key.not_before")
        not_after = _parse_timestamp(key["not_after"], "key.not_after")
        result["key_valid_at_issuance"] = not_before <= issued_at <= not_after
        try:
            signature = base64.b64decode(signature_entry["sig"], validate=True)
            result["signature_valid"] = _verify_ed25519(
                dsse_pae(envelope["payloadType"], payload),
                signature,
                key["public_key_pem"],
            )
        except (OSError, ValueError):
            result["signature_valid"] = False
    _check(result, "signature", result["signature_valid"])
    _check(result, "trust_scope", result["trust_scope_authorized"])
    _check(result, "key_status", result["key_status_allowed"])
    _check(result, "key_valid_at_issuance", result["key_valid_at_issuance"])

    current_time = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    issued_at = _parse_timestamp(predicate["issued_at"], "issued_at")
    expires_at = _parse_timestamp(predicate["expires_at"], "expires_at")
    result["attestation_time_valid"] = issued_at <= current_time <= expires_at
    _check(result, "attestation_time", result["attestation_time_valid"])

    authenticated = all((
        result["attestation_format_valid"],
        result["expectations_valid"],
        result["signature_valid"],
        result["subject_bound"],
        result["bindings_bound"],
        result["profile_bound"],
        result["tenant_bound"],
        result["audience_bound"],
        result["principal_bound"],
        result["key_id_bound"],
        result["statement_identity_bound"],
        result["trust_scope_authorized"],
        result["key_status_allowed"],
        result["key_valid_at_issuance"],
        result["attestation_time_valid"],
    ))
    result["producer_origin_authenticated"] = (
        authenticated and expected_profile == OPENWIKI_PRODUCER_ORIGIN_PROFILE)
    result["decision_authority_authenticated"] = (
        authenticated and expected_profile == GOVERNANCE_DECISION_PROFILE)
    # A local trust snapshot cannot prove live revocation, key, or tenant-policy
    # status. Only an online status source/checkpoint may upgrade this field.
    result["authority_current"] = "unknown"
    return result


def verify_attestation(
    artifact: os.PathLike[str] | str,
    attestation: dict[str, Any],
    trust_store: dict[str, Any],
    **kwargs: Any,
) -> dict[str, Any]:
    """File wrapper for :func:`verify_attestation_digest`."""
    return verify_attestation_digest(
        _sha256_file(artifact), attestation, trust_store, **kwargs)

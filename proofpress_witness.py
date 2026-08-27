"""Detached Proofpress Cloud Witness receipt verification.

This module deliberately verifies receipts only. Receipt issuance, key custody,
identity, revocation, and live status are Cloud Witness responsibilities.
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


PROTOCOL = "proofpress.cloud-witness-receipt"
PROTOCOL_VERSION = 1
TRUST_PROTOCOL = "proofpress.witness-trust"
TRUST_PROTOCOL_VERSION = 1


class WitnessError(ValueError):
    """Raised when a receipt or trust store is malformed."""


def canonical_payload(receipt: dict[str, Any]) -> bytes:
    """Return the bytes signed by a detached receipt signature."""
    unsigned = {key: value for key, value in receipt.items() if key != "signature"}
    return json.dumps(
        unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _sha256_file(path: os.PathLike[str] | str) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require_sha256(value: Any, field: str) -> None:
    if (not isinstance(value, str) or len(value) != 64
            or any(char not in "0123456789abcdef" for char in value)):
        raise WitnessError(f"{field} must be lowercase sha256 hex")


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


def validate_receipt(receipt: dict[str, Any]) -> None:
    if not isinstance(receipt, dict):
        raise WitnessError("receipt must be an object")
    if receipt.get("protocol") != PROTOCOL:
        raise WitnessError("unsupported witness receipt protocol")
    if receipt.get("protocol_version") != PROTOCOL_VERSION:
        raise WitnessError("unsupported witness receipt protocol version")
    for field in ("issuer", "key_id"):
        if not isinstance(receipt.get(field), str) or not receipt[field]:
            raise WitnessError(f"{field} must be a non-empty string")
    issued_at = _parse_timestamp(receipt.get("issued_at"), "issued_at")
    expires_at = _parse_timestamp(receipt.get("expires_at"), "expires_at")
    if expires_at <= issued_at:
        raise WitnessError("expires_at must be later than issued_at")
    bindings = receipt.get("bindings")
    if not isinstance(bindings, dict):
        raise WitnessError("bindings must be an object")
    material = bindings.get("material")
    decision = bindings.get("decision")
    policy = bindings.get("policy")
    ledger = bindings.get("ledger")
    if not isinstance(material, dict) or material.get("algorithm") != "sha256":
        raise WitnessError("bindings.material must use sha256")
    _require_sha256(material.get("digest"), "bindings.material.digest")
    if not isinstance(decision, dict) or decision.get("algorithm") != "sha256":
        raise WitnessError("bindings.decision must use sha256")
    _require_sha256(decision.get("digest"), "bindings.decision.digest")
    if not isinstance(policy, dict):
        raise WitnessError("bindings.policy must be an object")
    if not isinstance(policy.get("id"), str) or not policy["id"]:
        raise WitnessError("bindings.policy.id must be a non-empty string")
    _require_sha256(policy.get("digest"), "bindings.policy.digest")
    if not isinstance(policy.get("epoch"), int) or isinstance(policy["epoch"], bool) or policy["epoch"] < 0:
        raise WitnessError("bindings.policy.epoch must be a non-negative integer")
    if not isinstance(ledger, dict) or not isinstance(ledger.get("head"), str) or not ledger["head"]:
        raise WitnessError("bindings.ledger.head must be a non-empty string")
    signature = receipt.get("signature")
    if not isinstance(signature, dict) or signature.get("algorithm") != "ed25519":
        raise WitnessError("signature.algorithm must be ed25519")
    if not isinstance(signature.get("value"), str):
        raise WitnessError("signature.value must be base64")
    try:
        base64.b64decode(signature["value"], validate=True)
    except (ValueError, TypeError) as exc:
        raise WitnessError("signature.value must be base64") from exc


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
        if not isinstance(issuer, str) or not issuer:
            raise WitnessError("trust store issuer ids must be non-empty strings")
        keys = issuer_entry.get("keys") if isinstance(issuer_entry, dict) else None
        if not isinstance(keys, dict):
            raise WitnessError(f"trust store issuer {issuer!r} must contain keys")
        for key_id, key in keys.items():
            if not isinstance(key_id, str) or not key_id:
                raise WitnessError("trust store key ids must be non-empty strings")
            if not isinstance(key, dict) or key.get("algorithm") != "ed25519":
                raise WitnessError("trust store keys must use ed25519")
            pem = key.get("public_key_pem")
            if not isinstance(pem, str) or "BEGIN PUBLIC KEY" not in pem:
                raise WitnessError("trust store keys require public_key_pem")


def _verify_ed25519(payload: bytes, signature: bytes, public_key_pem: str) -> bool:
    """Use the system crypto provider without creating or retaining a local key."""
    with tempfile.TemporaryDirectory(prefix="proofpress-witness-") as directory:
        root = Path(directory)
        payload_path = root / "payload.json"
        signature_path = root / "receipt.sig"
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


def verify_receipt(
    artifact: os.PathLike[str] | str, receipt: dict[str, Any],
    trust_store: dict[str, Any], *, now: datetime | None = None,
) -> dict[str, Any]:
    """Verify a witness receipt without changing local artifact checks."""
    checks: list[dict[str, Any]] = []
    try:
        validate_receipt(receipt)
        validate_trust_store(trust_store)
    except WitnessError as exc:
        return {
            "format_valid": False, "material_bound": False,
            "authority_at_issuance": False, "origin_authenticated": False,
            "checks": [{"type": "receipt_format", "status": "failed", "detail": str(exc)}],
        }

    checks.append({"type": "receipt_format", "status": "passed"})
    actual_digest = _sha256_file(artifact)
    expected_digest = receipt["bindings"]["material"]["digest"]
    material_bound = actual_digest == expected_digest
    checks.append({"type": "material_binding", "status": "passed" if material_bound else "failed"})

    issuer = receipt["issuer"]
    key_id = receipt["key_id"]
    key = trust_store.get("issuers", {}).get(issuer, {}).get("keys", {}).get(key_id)
    trusted_key = key is not None
    checks.append({"type": "trusted_key", "status": "passed" if trusted_key else "failed"})
    signature_valid = False
    if trusted_key:
        try:
            signature = base64.b64decode(receipt["signature"]["value"], validate=True)
            signature_valid = _verify_ed25519(
                canonical_payload(receipt), signature, key["public_key_pem"])
        except (OSError, ValueError):
            signature_valid = False
    checks.append({"type": "detached_signature", "status": "passed" if signature_valid else "failed"})

    authority_at_issuance = material_bound and trusted_key and signature_valid
    current_time = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    issued_at = _parse_timestamp(receipt["issued_at"], "issued_at")
    expires_at = _parse_timestamp(receipt["expires_at"], "expires_at")
    fresh = issued_at <= current_time <= expires_at
    checks.append({"type": "freshness_window", "status": "passed" if fresh else "failed"})
    return {
        "format_valid": True,
        "material_bound": material_bound,
        "authority_at_issuance": authority_at_issuance,
        "origin_authenticated": authority_at_issuance and fresh,
        "checks": checks,
    }

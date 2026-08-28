#!/usr/bin/env python3
"""Issuer-side fixture helpers for the real Proofpress witness verifier.

Production verification lives in :mod:`proofpress_witness`. This file only
creates signed test statements and composes orthogonal verification results;
it deliberately contains no second verifier.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path
import subprocess
import tempfile
from typing import Any

import proofpress_witness as witness


class BoundaryError(ValueError):
    """Invalid fixture construction or unsafe trust-axis composition."""


def make_statement(
    *, profile: str, subject_name: str, subject_sha256: str, predicate: dict[str, Any]
) -> dict[str, Any]:
    if profile not in witness.SUPPORTED_PROFILES:
        raise BoundaryError(f"unsupported attestation profile: {profile}")
    return {
        "_type": witness.IN_TOTO_STATEMENT_TYPE,
        "subject": [
            {"name": subject_name, "digest": {"sha256": subject_sha256}}
        ],
        "predicateType": profile,
        "predicate": predicate,
    }


def sign_statement(
    statement: dict[str, Any], private_key: Path, *, key_id: str
) -> dict[str, Any]:
    """Act as the demo issuer; the consumer still uses the real verifier."""
    payload = json.dumps(
        statement, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    with tempfile.TemporaryDirectory(prefix="proofpress-dsse-sign-") as directory:
        root = Path(directory)
        message = root / "pae.bin"
        signature = root / "signature.bin"
        message.write_bytes(witness.dsse_pae(witness.DSSE_PAYLOAD_TYPE, payload))
        completed = subprocess.run(
            [
                "openssl",
                "pkeyutl",
                "-sign",
                "-rawin",
                "-inkey",
                str(private_key),
                "-in",
                str(message),
                "-out",
                str(signature),
            ],
            capture_output=True,
            text=True,
        )
        if completed.returncode:
            raise BoundaryError(completed.stderr.strip() or "OpenSSL signing failed")
        signature_bytes = signature.read_bytes()
    return {
        "payloadType": witness.DSSE_PAYLOAD_TYPE,
        "payload": base64.b64encode(payload).decode("ascii"),
        "signatures": [
            {
                "keyid": key_id,
                "sig": base64.b64encode(signature_bytes).decode("ascii"),
            }
        ],
    }


def compose_trust_axes(
    inspection: dict[str, Any],
    *,
    handoff_manifest_digest: str,
    producer_origin: dict[str, Any] | None = None,
    decision_authority: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compose facts only when all trusted axes name one recomputed manifest."""
    producer_origin = producer_origin or {}
    decision_authority = decision_authority or {}
    if (not isinstance(handoff_manifest_digest, str)
            or len(handoff_manifest_digest) != 64
            or any(char not in "0123456789abcdef"
                   for char in handoff_manifest_digest)):
        raise BoundaryError("handoff_manifest_digest must be lowercase sha256 hex")
    claims = [
        claim
        for page in inspection.get("pages", [])
        for claim in page.get("claims", [])
    ]
    if any(claim.get("proofpress_admission") != "not_inherited" for claim in claims):
        raise BoundaryError("OpenWiki inspection unexpectedly inherited admission")
    if producer_origin.get("authority_current") not in {None, "unknown"}:
        raise BoundaryError("offline producer authority currentness was overclaimed")
    if decision_authority.get("authority_current") not in {None, "unknown"}:
        raise BoundaryError("offline decision authority currentness was overclaimed")
    producer_manifest_joined = (
        producer_origin.get("handoff_manifest_digest") == handoff_manifest_digest
    )
    decision_manifest_joined = (
        decision_authority.get("handoff_manifest_digest") == handoff_manifest_digest
    )
    return {
        "inspection_passed": bool(inspection.get("inspection_passed")),
        "format_valid": bool(inspection.get("summary", {}).get("format_valid")),
        "page_bound": bool(inspection.get("summary", {}).get("page_bound")),
        "evidence_current": bool(
            inspection.get("summary", {}).get("evidence_current")
        ),
        "handoff_manifest_digest": handoff_manifest_digest,
        "producer_manifest_joined": producer_manifest_joined,
        "decision_manifest_joined": decision_manifest_joined,
        "producer_origin_authenticated": bool(
            producer_origin.get("producer_origin_authenticated")
        ) and producer_manifest_joined,
        "decision_authority_authenticated": bool(
            decision_authority.get("decision_authority_authenticated")
        ) and decision_manifest_joined,
        "authority_current": "unknown",
        "proofpress_admission": "not_performed",
        "proofpress_review_required": True,
    }

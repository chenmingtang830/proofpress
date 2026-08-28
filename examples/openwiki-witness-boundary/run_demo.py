#!/usr/bin/env python3
"""Run the real OpenWiki importer plus hardened witness verifier."""
from __future__ import annotations

import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


DEMO_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = DEMO_DIR.parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))

import proofpress_openwiki as openwiki  # noqa: E402
import proofpress_witness as witness  # noqa: E402
from boundary import compose_trust_axes, make_statement, sign_statement  # noqa: E402


FIXTURE = REPOSITORY_ROOT / "examples/openwiki-conflict-gate/openwiki-fixture.json"
NOW = datetime(2026, 8, 27, 12, 0, tzinfo=timezone.utc)
ISSUER = "https://witness.example.test"
TENANT = "proofpress-demo"
AUDIENCE = "proofpress-governed-context"
PRODUCER_PRINCIPAL = "service:openwiki"
DECISION_PRINCIPAL = "human:geometry-steward"
PRODUCER_KEY_ID = "openwiki-producer-key"
DECISION_KEY_ID = "governance-decision-key"
MANIFEST_RELATIVE = ".proofpress/openwiki-handoff-manifest.json"


def canonical_json(value) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256_json(value) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def materialize_fixture(root: Path) -> None:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    for relative, record in fixture["files"].items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(record["content"].encode("utf-8"))


def generate_keypair(root: Path, stem: str) -> tuple[Path, Path]:
    private = root / f"{stem}-private.pem"
    public = root / f"{stem}-public.pem"
    subprocess.run(
        ["openssl", "genpkey", "-algorithm", "Ed25519", "-out", str(private)],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "openssl",
            "pkey",
            "-in",
            str(private),
            "-pubout",
            "-out",
            str(public),
        ],
        check=True,
        capture_output=True,
    )
    return private, public


def producer_bindings(manifest_sha256: str) -> dict:
    return {
        "handoff_manifest": {
            "algorithm": "sha256",
            "digest": manifest_sha256,
        },
        "producer": {
            "id": "openwiki/0.4.2",
            "run_id": "frozen-fixture-run",
        },
    }


def producer_predicate(manifest_sha256: str, *, statement_id="producer-origin-001") -> dict:
    return {
        "issuer": ISSUER,
        "tenant": TENANT,
        "audience": AUDIENCE,
        "principal": PRODUCER_PRINCIPAL,
        "key_id": PRODUCER_KEY_ID,
        "statement_id": statement_id,
        "critical": [],
        "issued_at": "2026-08-27T00:00:00Z",
        "expires_at": "2026-08-28T00:00:00Z",
        "bindings": producer_bindings(manifest_sha256),
    }


def governance_bindings(
    manifest_sha256: str,
    *,
    resolution_action="supersede_left",
    policy_epoch=7,
    resulting_head="ppe_after_resolution",
) -> dict:
    contradiction = {
        "type": "contradicts",
        "left_claim_id": "claim_257972d8bab14f8cb86e3aada65935ee",
        "right_claim_id": "claim_a99b812909714605a5b3af22b16f06fc",
    }
    resolution = {"action": resolution_action}
    policy_body = {"id": "geometry-review-policy", "epoch": policy_epoch}
    policy = {**policy_body, "digest": sha256_json(policy_body)}
    ledger = {
        "previous_head": "ppe_before_resolution",
        "resulting_head": resulting_head,
    }
    decision_material = {
        "contradiction": contradiction,
        "resolution": resolution,
        "policy": policy,
        "ledger": ledger,
    }
    return {
        "handoff_manifest": {
            "algorithm": "sha256",
            "digest": manifest_sha256,
        },
        "decision": {
            "algorithm": "sha256",
            "digest": sha256_json(decision_material),
        },
        **decision_material,
    }


def decision_predicate(manifest_sha256: str, *, statement_id="decision-authority-001") -> dict:
    return {
        "issuer": ISSUER,
        "tenant": TENANT,
        "audience": AUDIENCE,
        "principal": DECISION_PRINCIPAL,
        "key_id": DECISION_KEY_ID,
        "statement_id": statement_id,
        "critical": [],
        "issued_at": "2026-08-27T00:00:00Z",
        "expires_at": "2026-08-28T00:00:00Z",
        "bindings": governance_bindings(manifest_sha256),
    }


def trust_store(producer_public: Path, decision_public: Path) -> dict:
    common = {
        "algorithm": "ed25519",
        "status": "active",
        "not_before": "2026-08-01T00:00:00Z",
        "not_after": "2026-09-30T00:00:00Z",
        "tenants": [TENANT],
        "audiences": [AUDIENCE],
    }
    return {
        "protocol": witness.TRUST_PROTOCOL,
        "protocol_version": witness.TRUST_PROTOCOL_VERSION,
        "issuers": {
            ISSUER: {
                "keys": {
                    PRODUCER_KEY_ID: {
                        **common,
                        "profiles": [witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE],
                        "principals": [PRODUCER_PRINCIPAL],
                        "public_key_pem": producer_public.read_text(encoding="utf-8"),
                    },
                    DECISION_KEY_ID: {
                        **common,
                        "profiles": [witness.GOVERNANCE_DECISION_PROFILE],
                        "principals": [DECISION_PRINCIPAL],
                        "public_key_pem": decision_public.read_text(encoding="utf-8"),
                    },
                }
            }
        },
    }


def manifest_subject(root: Path) -> tuple[dict, str, dict, Path]:
    inspection = openwiki.inspect_openwiki_snapshot(root)
    manifest = openwiki.build_handoff_manifest(root, inspection)
    payload = openwiki.canonical_handoff_manifest_bytes(manifest)
    digest = hashlib.sha256(payload).hexdigest()
    if openwiki.handoff_manifest_digest(manifest) != "sha256:" + digest:
        raise AssertionError("handoff manifest digest helpers disagree")
    artifact = root / MANIFEST_RELATIVE
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(payload)
    return inspection, digest, manifest, artifact


def verify_manifest(
    artifact: Path,
    envelope: dict,
    trust: dict,
    *,
    profile: str,
    bindings: dict,
    principal: str,
    expected_statement_id: str | None = None,
    expected_statement_digest: str | None = None,
) -> dict:
    return witness.verify_attestation(
        artifact,
        envelope,
        trust,
        expected_profile=profile,
        expected_bindings=bindings,
        expected_tenant=TENANT,
        expected_audience=AUDIENCE,
        expected_principal=principal,
        expected_statement_id=expected_statement_id,
        expected_statement_digest=expected_statement_digest,
        now=NOW,
    )


def execute_demo(root: Path) -> dict:
    if not shutil.which("openssl"):
        raise RuntimeError("OpenSSL is required for the Ed25519 demo")
    root.mkdir(parents=True, exist_ok=True)
    snapshot = root / "snapshot"
    keys = root / "keys"
    snapshot.mkdir()
    keys.mkdir()
    materialize_fixture(snapshot)
    producer_private, producer_public = generate_keypair(keys, "producer")
    decision_private, decision_public = generate_keypair(keys, "decision")
    trust = trust_store(producer_public, decision_public)

    fresh_inspection, fresh_digest, manifest, manifest_artifact = manifest_subject(
        snapshot
    )
    producer_statement = make_statement(
        profile=witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
        subject_name=MANIFEST_RELATIVE,
        subject_sha256=fresh_digest,
        predicate=producer_predicate(fresh_digest),
    )
    producer_envelope = sign_statement(
        producer_statement, producer_private, key_id=PRODUCER_KEY_ID
    )
    producer_result = verify_manifest(
        manifest_artifact,
        producer_envelope,
        trust,
        profile=witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
        bindings=producer_bindings(fresh_digest),
        principal=PRODUCER_PRINCIPAL,
    )

    decision_statement = make_statement(
        profile=witness.GOVERNANCE_DECISION_PROFILE,
        subject_name=MANIFEST_RELATIVE,
        subject_sha256=fresh_digest,
        predicate=decision_predicate(fresh_digest),
    )
    decision_envelope = sign_statement(
        decision_statement, decision_private, key_id=DECISION_KEY_ID
    )
    decision_result = verify_manifest(
        manifest_artifact,
        decision_envelope,
        trust,
        profile=witness.GOVERNANCE_DECISION_PROFILE,
        bindings=governance_bindings(fresh_digest),
        principal=DECISION_PRINCIPAL,
    )
    fresh_axes = compose_trust_axes(
        fresh_inspection,
        handoff_manifest_digest=fresh_digest,
        producer_origin=producer_result,
        decision_authority=decision_result,
    )

    wrong_profile = verify_manifest(
        manifest_artifact,
        decision_envelope,
        trust,
        profile=witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
        bindings=producer_bindings(fresh_digest),
        principal=PRODUCER_PRINCIPAL,
    )
    winner_flip = verify_manifest(
        manifest_artifact,
        decision_envelope,
        trust,
        profile=witness.GOVERNANCE_DECISION_PROFILE,
        bindings=governance_bindings(
            fresh_digest, resolution_action="supersede_right"),
        principal=DECISION_PRINCIPAL,
    )

    repeated = verify_manifest(
        manifest_artifact,
        producer_envelope,
        trust,
        profile=witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
        bindings=producer_bindings(fresh_digest),
        principal=PRODUCER_PRINCIPAL,
        expected_statement_id=producer_result["statement_id"],
        expected_statement_digest=producer_result["statement_digest"],
    )
    conflicting_predicate = {
        **producer_predicate(fresh_digest),
        "additive_note": "different signed bytes under the same statement id",
    }
    conflicting_statement = make_statement(
        profile=witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
        subject_name=MANIFEST_RELATIVE,
        subject_sha256=fresh_digest,
        predicate=conflicting_predicate,
    )
    conflicting_envelope = sign_statement(
        conflicting_statement, producer_private, key_id=PRODUCER_KEY_ID
    )
    conflicting = verify_manifest(
        manifest_artifact,
        conflicting_envelope,
        trust,
        profile=witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
        bindings=producer_bindings(fresh_digest),
        principal=PRODUCER_PRINCIPAL,
        expected_statement_id=producer_result["statement_id"],
        expected_statement_digest=producer_result["statement_digest"],
    )

    stale_snapshot = root / "stale-snapshot"
    shutil.copytree(snapshot, stale_snapshot)
    evidence = stale_snapshot / "evidence/gravitational-evidence.json"
    evidence.write_text(
        evidence.read_text(encoding="utf-8").replace(
            '"dt": 86400.0', '"dt": 86000.0', 1
        ),
        encoding="utf-8",
    )
    stale_inspection, stale_digest, _, stale_artifact = manifest_subject(
        stale_snapshot
    )
    stale_statement = make_statement(
        profile=witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
        subject_name=MANIFEST_RELATIVE,
        subject_sha256=stale_digest,
        predicate=producer_predicate(
            stale_digest, statement_id="producer-origin-stale-001"
        ),
    )
    stale_envelope = sign_statement(
        stale_statement, producer_private, key_id=PRODUCER_KEY_ID
    )
    stale_origin = verify_manifest(
        stale_artifact,
        stale_envelope,
        trust,
        profile=witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
        bindings=producer_bindings(stale_digest),
        principal=PRODUCER_PRINCIPAL,
    )
    stale_axes = compose_trust_axes(
        stale_inspection, handoff_manifest_digest=stale_digest,
        producer_origin=stale_origin)

    assertions = {
        "fresh_local_inspection_passes": fresh_axes["inspection_passed"],
        "producer_attestation_authenticates_only_origin": (
            producer_result["producer_origin_authenticated"]
            and not producer_result["decision_authority_authenticated"]
        ),
        "decision_attestation_authenticates_only_decision_authority": (
            decision_result["decision_authority_authenticated"]
            and not decision_result["producer_origin_authenticated"]
        ),
        "decision_profile_cannot_authenticate_origin": not wrong_profile[
            "producer_origin_authenticated"
        ],
        "winner_flip_fails_expected_binding": (
            not winner_flip["bindings_bound"]
            and not winner_flip["decision_authority_authenticated"]
        ),
        "exact_reverification_is_idempotent": (
            repeated["statement_identity_bound"]
            and repeated["statement_identity_status"] == "matched"
            and repeated["producer_origin_authenticated"]
        ),
        "same_id_different_statement_is_rejected": (
            conflicting["statement_identity_conflict"]
            and not conflicting["statement_identity_bound"]
            and not conflicting["producer_origin_authenticated"]
        ),
        "authenticated_origin_does_not_make_stale_evidence_current": (
            stale_axes["producer_origin_authenticated"]
            and not stale_axes["evidence_current"]
            and not stale_axes["inspection_passed"]
        ),
        "neither_attestation_admits_claims": (
            fresh_axes["proofpress_admission"] == "not_performed"
            and stale_axes["proofpress_admission"] == "not_performed"
        ),
        "offline_authority_current_is_not_overclaimed": (
            producer_result["authority_current"] == "unknown"
            and decision_result["authority_current"] == "unknown"
            and fresh_axes["authority_current"] == "unknown"
        ),
    }
    if not all(assertions.values()):
        raise AssertionError(f"boundary invariant failed: {assertions}")
    return {
        "demo": "proofpress/openwiki-witness-boundary/v2",
        "verifier": "proofpress_witness.verify_attestation",
        "handoff_manifest": {
            "schema_version": manifest["schema_version"],
            "sha256": fresh_digest,
            "material_count": len(manifest["materials"]),
            "pages": manifest["selection"]["pages"],
        },
        "fresh": fresh_axes,
        "stale_but_authentic": stale_axes,
        "statement_identity": {
            "repeated": repeated["statement_identity_status"],
            "conflicting": conflicting["statement_identity_status"],
        },
        "assertions": assertions,
    }


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="proofpress-openwiki-witness-") as directory:
        result = execute_demo(Path(directory))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

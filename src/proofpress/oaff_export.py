"""Explicit, byte-checked export of one Proofpress claim as an OAFF snapshot.

This is a projection for transfer, never a Proofpress admission or a signature.
Callers choose the public namespace and source URIs; local workspace paths and
source bytes are not serialized.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

from .kernel import operations


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _uri(namespace: str, kind: str, value: str) -> str:
    return f"{namespace.rstrip('/')}/{kind}/{_digest(value.encode('utf-8'))}"


def _actor(namespace: str, raw: str, kind: str) -> dict:
    return {"id": _uri(namespace, "actors", raw), "kind": kind}


def _utc(value: str) -> str:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("OAFF export requires a recorded UTC timestamp")
    return value


def export_claim(
    claim_id: str,
    *,
    namespace: str,
    sources: dict[str, tuple[str, bytes]],
) -> dict:
    """Return an OAFF v0.1 package for a claim with verified source bytes.

    ``sources`` maps every bound retrieval-evidence ID to a caller-approved
    source URI and the exact source bytes. Nothing is fetched automatically.
    Only claims with an explicit validity condition and retrieval evidence are
    supported. Unsupported claims fail rather than receiving invented scope.
    """
    parsed = urlparse(namespace)
    if (parsed.scheme != "https" or not parsed.netloc or parsed.username
            or parsed.password or parsed.query or parsed.fragment):
        raise ValueError("namespace must be an organization-controlled HTTPS URI")
    try:
        import rfc8785
    except ImportError as exc:
        raise RuntimeError("Install proofpress-local[oaff] for OAFF export") from exc

    ledger_head = operations.v2_head()
    projection = operations.v2_projection()
    if operations.v2_head() != ledger_head:
        raise ValueError("Proofpress ledger changed during export; retry")
    claim = projection["claims"].get(claim_id)
    if claim is None:
        raise ValueError("claim not found")
    if claim.get("digest") != operations._claim_digest(claim):
        raise ValueError("claim digest does not match its recorded value")
    card = claim.get("applicability") or {}
    conditions = card.get("validity_conditions") or []
    description = card.get("description")
    if not description or not conditions:
        raise ValueError("claim needs explicit applicability description and validity conditions")
    refs = claim.get("evidence_refs") or []
    if not refs or set(refs) != set(sources):
        raise ValueError("provide exactly one source URI and byte sequence per bound evidence")

    evidence = []
    for ref in refs:
        row = projection["evidence"].get(ref)
        if not row or row.get("kind") != "retrieval_evidence" or not operations._retrieval_receipt_valid(row):
            raise ValueError(f"unsupported or invalid retrieval evidence: {ref}")
        source_uri, source_bytes = sources[ref]
        source_parsed = urlparse(source_uri)
        if (not source_parsed.scheme or not isinstance(source_bytes, bytes)
                or source_parsed.username or source_parsed.password
                or "?" in source_uri or "#" in source_uri):
            raise ValueError(f"source {ref} needs a credential-free URI and bytes")
        recorded = row["source_content_digest"]
        if recorded != "sha256:" + _digest(source_bytes):
            raise ValueError(f"source bytes do not match recorded digest: {ref}")
        evidence.append({
            "id": _digest(ref.encode("utf-8"))[:24],
            "source_uri": source_uri,
            "content_digest": {"algorithm": "sha-256", "value": _digest(source_bytes)},
            "availability": "restricted",
        })

    finding_id = _uri(namespace, "findings", claim_id)
    revision = _uri(namespace, "revisions", claim_id + ":" + claim["digest"])
    finding = {
        "id": finding_id,
        "revision": revision,
        "statement": claim["statement"],
        "type": "observation",
        "applicability": {"description": description, "conditions": conditions},
        "producer": _actor(namespace, claim["proposer"], "agent" if claim["proposer"].startswith("agent:") else "human"),
        "created_at": _utc(claim["created_at"]),
        "evidence": evidence,
    }
    receipts = []
    admission = projection.get("admissions", {}).get(claim_id)
    if admission and admission.get("claim_digest") == claim["digest"]:
        automatic = admission["type"] == "claim_auto_admitted"
        issuer = admission.get("authorized_by") if automatic else admission.get("reviewer")
        if issuer:
            receipts.append({
                "id": _uri(namespace, "receipts", admission["event_id"]),
                "kind": "adoption_decision", "subject_revision": revision,
                "issuer": _actor(namespace, issuer, "system" if automatic else "human"),
                "issued_at": _utc(admission["created_at"]),
                "method": "Proofpress owner policy" if automatic else "Proofpress human review",
                "result": "admitted",
                "authority_basis": "owner_policy" if automatic else "human_approval",
            })
    withdrawal = projection.get("withdrawals", {}).get(claim_id)
    if withdrawal and admission and withdrawal.get("prior_admission_ref") == admission.get("event_id"):
        receipts.append({
            "id": _uri(namespace, "receipts", withdrawal["event_id"]),
            "kind": "lifecycle", "subject_revision": revision,
            "issuer": _actor(namespace, withdrawal["reviewer"], "human"),
            "issued_at": _utc(withdrawal["created_at"]),
            "method": "Proofpress withdrawal", "result": "withdrawn",
        })
    package = {
        "oaff_version": "0.1.0", "finding": finding, "receipts": receipts,
        "extensions": {
            namespace.rstrip("/") + "/proofpress/ledger-head": ledger_head,
            namespace.rstrip("/") + "/proofpress/exported-at": operations.now(),
        },
    }
    package["integrity"] = {"algorithm": "sha-256-jcs", "digest": _digest(rfc8785.dumps(package))}
    return package


def export_claim_file(claim_id: str, *, namespace: str,
                      sources: dict[str, tuple[str, Path]], output: Path) -> dict:
    """Write a package without embedding the supplied source bytes."""
    package = export_claim(claim_id, namespace=namespace,
                           sources={ref: (uri, path.read_bytes())
                                    for ref, (uri, path) in sources.items()})
    output.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return package


def main() -> int:
    parser = argparse.ArgumentParser(description="Export one bounded Proofpress claim as OAFF v0.1")
    parser.add_argument("claim_id")
    parser.add_argument("--namespace", required=True)
    parser.add_argument("--source", nargs=3, action="append", metavar=("EVIDENCE_ID", "URI", "FILE"),
                        required=True, help="repeat for each bound retrieval evidence")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sources = {ref: (uri, Path(path)) for ref, uri, path in args.source}
    if len(sources) != len(args.source):
        parser.error("duplicate evidence ID")
    try:
        export_claim_file(args.claim_id, namespace=args.namespace,
                          sources=sources, output=args.output)
    except (ValueError, OSError, RuntimeError) as exc:
        parser.exit(1, f"OAFF export failed: {exc}\n")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

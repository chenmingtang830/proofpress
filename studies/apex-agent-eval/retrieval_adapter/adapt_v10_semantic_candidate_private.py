#!/usr/bin/env python3
"""Adapt filtered, critic-supported v10 claims to the blinded semantic scorer contract."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from governed_workflow_contract import digest
from run_v10_profile_filter_private import AUTO_CONSTRUCTION_REQUIREMENT_TYPES

SCHEMA = "proofpress/v10-semantic-candidate-adapter/v1"


def adapt(source: dict, resolution_rows: list[dict] | None = None) -> dict:
    requirement_types = {row["requirement_id"]: row.get("type") for row in source["requirements"]}
    verdicts = {row["claim_id"]: row for row in source["verdicts"]}
    atoms = {row["atom_id"]: row for row in source["atoms"]}
    claims = []
    evidence_ids = set()
    for row in source["claims"]:
        if requirement_types.get(row["requirement_id"]) not in AUTO_CONSTRUCTION_REQUIREMENT_TYPES:
            continue
        if verdicts.get(row["id"], {}).get("verdict") != "supported":
            continue
        bound_evidence = sorted({atoms[atom_id]["evidence_id"] for atom_id in row["atom_ids"] if atom_id in atoms})
        evidence_ids.update(bound_evidence)
        claims.append({"id": row["id"], "requirement_id": row["requirement_id"],
                       "claim_type": row["claim_type"], "statement": row["statement"],
                       "evidence_ids": bound_evidence})
    evidence = []
    for evidence_id in sorted(evidence_ids):
        receipt = source["receipts"][evidence_id]
        evidence.append({"evidence_id": evidence_id, "quote": receipt["quote"],
                         "source": receipt.get("source", {}), "locator": receipt["locator"]})
    resolution = {row["requirement_id"]: row.get("status") for row in (resolution_rows or [])}
    requirements = []
    for row in source["requirements"]:
        status = resolution.get(row["requirement_id"], "gap")
        if row.get("type") not in AUTO_CONSTRUCTION_REQUIREMENT_TYPES:
            gap_reason = "profile_requires_domain_analysis"
        elif status == "partial":
            gap_reason = "supported_claim_set_is_incomplete"
        elif status == "gap":
            gap_reason = "no_complete_supported_claim_set"
        else:
            gap_reason = None
        requirements.append({
            **row,
            "status": status,
            "gap_reason": gap_reason,
            "missing_evidence": (row.get("required_evidence_type") or row.get("requirement"))
                if status in {"partial", "gap"} else None,
            "gap_queries": row.get("evidence_search_queries", [])
                if status in {"partial", "gap"} else [],
        })
    return {"construction": {"requirements": requirements, "claims": claims, "evidence": evidence,
                             "status": "staged-evaluation", "authority": "non-authoritative"}}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-raw", required=True)
    parser.add_argument("--profile-filter-raw")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    paths = sorted(Path(args.candidate_raw).glob("*.json"))
    if len(paths) != 4:
        raise SystemExit("semantic candidate adapter requires four frozen tasks")
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    raw = out / "raw"; raw.mkdir(exist_ok=True); raw.chmod(0o700)
    tasks = []
    for path in paths:
        resolution_rows = None
        if args.profile_filter_raw:
            profile = json.loads((Path(args.profile_filter_raw) / path.name).read_text())
            resolution_rows = profile["requirement_resolutions"]["sol"]
        value = adapt(json.loads(path.read_text()), resolution_rows)
        target = raw / path.name
        target.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n"); target.chmod(0o600)
        tasks.append({"task_id": path.stem, "status": "ok", "artifact_digest": digest(value)})
    report = {"schema_version": SCHEMA, "system": "evidence-first-v10-profile-filtered",
              "boundary": "Private adapter for post-output blinded scoring. Claims are critic-supported unresolved candidates, never admissions.",
              "tasks": tasks, "qualification": {"requested": True, "status": "pass"},
              "raw_private_dir": str(raw)}
    (out / "sanitized-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "pass", "tasks": len(tasks)}, sort_keys=True))


if __name__ == "__main__":
    main()

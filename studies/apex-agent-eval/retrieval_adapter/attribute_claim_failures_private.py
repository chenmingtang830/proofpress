#!/usr/bin/env python3
"""Attribute model-adjudicated unsupported claims without publishing corpus text."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Any

from governed_workflow_contract import digest

SCHEMA = "proofpress/private-claim-failure-attribution/v1"
CATEGORIES = (
    "retrieval_miss", "erroneous_evidence_atom", "task_prompt_leakage",
    "proposer_external_fact", "overbroad_or_compound_claim",
    "qualification_loss", "fact_risk_conclusion_confusion",
    "version_or_conflict_merge", "critic_false_accept", "adjudication_dispute",
)


def _tokens(value: str) -> set[str]:
    return {part.casefold().strip(".,;:()[]{}\"'") for part in value.split()
            if len(part.strip(".,;:()[]{}\"'")) > 2}


def classify(claim: dict[str, Any], construction: dict[str, Any], task_prompt: str) -> list[str]:
    atoms = {row.get("atom_id"): row for row in construction.get("evidence_atoms", [])}
    evidence = {row.get("evidence_id"): row for row in construction.get("evidence", [])}
    bound_atoms = [atoms[row] for row in claim.get("atom_ids", []) if row in atoms]
    bound_evidence = [evidence[row] for row in claim.get("evidence_ids", []) if row in evidence]
    statement = str(claim.get("statement", ""))
    categories: list[str] = []
    if not bound_evidence:
        categories.append("retrieval_miss")
    if not bound_atoms or any(row.get("support_mode") != "explicit" for row in bound_atoms):
        categories.append("erroneous_evidence_atom")
    evidence_text = " ".join(str(row.get("exact_excerpt", "")) for row in bound_atoms)
    evidence_tokens, statement_tokens = _tokens(evidence_text), _tokens(statement)
    prompt_tokens = _tokens(task_prompt)
    unsupported_tokens = statement_tokens - evidence_tokens
    if unsupported_tokens and unsupported_tokens <= prompt_tokens:
        categories.append("task_prompt_leakage")
    elif unsupported_tokens:
        categories.append("proposer_external_fact")
    if any(token in statement.casefold() for token in (" and ", ";", " as well as ", " including ")):
        categories.append("overbroad_or_compound_claim")
    qualifications = [str(row.get("qualification")) for row in bound_atoms if row.get("qualification")]
    if qualifications and any(value.casefold() not in str(claim.get("qualification") or "").casefold()
                              and value.casefold() not in statement.casefold()
                              for value in qualifications):
        categories.append("qualification_loss")
    requirement = next((row for row in construction.get("requirements", [])
                        if row.get("requirement_id") == claim.get("requirement_id")), {})
    requirement_type = requirement.get("type")
    if claim.get("claim_type") == "observed_fact" and requirement_type in {
            "risk_signal", "legal_conclusion", "needs_legal_analysis"}:
        categories.append("fact_risk_conclusion_confusion")
    versions = {str(row.get("document_version")) for row in bound_atoms if row.get("document_version")}
    conflicts = {str(row.get("conflict_group")) for row in bound_atoms if row.get("conflict_group")}
    if len(versions) > 1 or conflicts:
        categories.append("version_or_conflict_merge")
    critic_rows = construction.get("critic_verdicts", {})
    if isinstance(critic_rows, list):
        critic_rows = {row.get("claim_id"): row for row in critic_rows if isinstance(row, dict)}
    critic = critic_rows.get(claim.get("id"), {}) if isinstance(critic_rows, dict) else {}
    if critic.get("verdict") == "supported":
        categories.append("critic_false_accept")
    return [row for row in CATEGORIES if row in set(categories)] or ["adjudication_dispute"]


def attribute(construction_report: dict[str, Any], semantic_report: dict[str, Any],
              output: Path, system_label: str | None = None) -> dict[str, Any]:
    construction_root = Path(construction_report["raw_private_dir"])
    semantic_root = Path(semantic_report["raw_private_dir"])
    candidate_label = system_label or semantic_report.get("candidate_label")
    if not candidate_label:
        raise ValueError("semantic system label is required")
    counts: Counter[str] = Counter()
    system_counts: Counter[str] = Counter()
    affected_requirements: dict[str, set[str]] = defaultdict(set)
    rows = []
    raw = output / "raw"
    raw.mkdir(parents=True, exist_ok=True); raw.chmod(0o700)
    for semantic_path in sorted(semantic_root.glob("*.json")):
        task_id = semantic_path.stem
        semantic = json.loads(semantic_path.read_text())
        labels = semantic["labels"]["systems"][candidate_label]
        unsupported = set(labels.get("unsupported_factual_claim_ids", []))
        construction_path = construction_root / f"{task_id}.json"
        if not construction_path.exists():
            rows.append({"task_id": task_id, "status": "inconclusive",
                         "reason": "construction_artifact_missing"})
            continue
        value = json.loads(construction_path.read_text())
        construction = value["construction"]
        claims = {row["id"]: row for row in construction.get("claims", [])}
        private_items = []
        for claim_id in sorted(unsupported):
            claim = claims.get(claim_id)
            if not claim:
                private_items.append({"claim_id": claim_id, "categories": ["adjudication_dispute"],
                                      "reason": "claim_not_in_current_construction"})
                counts["adjudication_dispute"] += 1
                continue
            categories = classify(claim, construction, str(value.get("task", {}).get("prompt", "")))
            for category in categories:
                counts[category] += 1
                affected_requirements[category].add(str(claim.get("requirement_id")))
            private_items.append({"claim_id": claim_id,
                                  "claim_digest": digest(claim),
                                  "requirement_id": claim.get("requirement_id"),
                                  "categories": categories})
        private = {"task_id": task_id, "unsupported_count": len(unsupported), "items": private_items}
        target = raw / f"{task_id}.json"
        target.write_text(json.dumps(private, indent=2, sort_keys=True) + "\n"); target.chmod(0o600)
        system_counts["unsupported_claims"] += len(unsupported)
        rows.append({"task_id": task_id, "status": "ok", "unsupported_count": len(unsupported),
                     "category_counts": dict(Counter(cat for item in private_items
                                                      for cat in item["categories"])),
                     "artifact_digest": digest(private)})
    denominator = system_counts["unsupported_claims"]
    report = {
        "schema_version": SCHEMA,
        "boundary": "Model-adjudicated development diagnosis; categories may overlap and are not human gold.",
        "system": candidate_label,
        "denominators": {"tasks": len(rows), "unsupported_claims": denominator},
        "categories": [{"category": category, "count": counts[category],
                        "fraction_of_unsupported": counts[category] / denominator if denominator else None,
                        "affected_requirement_count": len(affected_requirements[category])}
                       for category in CATEGORIES],
        "tasks": rows,
        "raw_private_dir": str(raw),
    }
    output.mkdir(parents=True, exist_ok=True); output.chmod(0o700)
    (output / "sanitized-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--construction-report", required=True)
    parser.add_argument("--semantic-report", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--system-label")
    args = parser.parse_args()
    report = attribute(json.loads(Path(args.construction_report).read_text()),
                       json.loads(Path(args.semantic_report).read_text()), Path(args.out),
                       args.system_label)
    print(json.dumps({"status": "ok", "system": report["system"],
                      "denominators": report["denominators"]}, sort_keys=True))


if __name__ == "__main__":
    main()

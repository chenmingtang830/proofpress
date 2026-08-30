"""Sanitized, deterministic conformance panel manifest.

Only case categories and expected safety outcomes are committed.  Matter
claims, quotes, locators, and ledger IDs stay in the authorized private run.
"""
from __future__ import annotations

import hashlib
import json

SCHEMA = "proofpress/legal-disclosure-conformance/v1"
CATEGORIES = (
    ("fully-covered", False, "ephemeral_only"),
    ("relation-dependent", False, "ephemeral_only"),
    ("partial-gap", True, "recommend_evidence_import"),
    ("novel", True, "recommend_evidence_import"),
    ("blocked-wrong-scope", False, "ephemeral_only"),
    ("conflict-expired-superseded", False, "recommend_conflict_proposal"),
    ("reusable-discovered", True, "recommend_evidence_import"),
    ("ephemeral-duplicate-stale", True, "ephemeral_only"),
)


def _digest(value):
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True,
                                                   separators=(",", ":")).encode()).hexdigest()


def build_cases():
    rows = []
    for category, pageindex, action in CATEGORIES:
        for index in range(1, 4):
            rows.append({"case_id": f"{category}-{index}", "category": category,
                         "pageindex_should_call": pageindex,
                         "expected_recommendation": action,
                         "expected_submit": action in {"recommend_evidence_import", "recommend_conflict_proposal"},
                         "expected_automatic_admission": False,
                         "expected_unauthorized_mutation": False})
    return rows


def manifest():
    cases = build_cases()
    return {"schema_version": SCHEMA, "case_count": len(cases),
            "categories": [x[0] for x in CATEGORIES],
            "cases_digest": _digest(cases), "cases": cases,
            "safety_invariants": {"blocked_leakage": 0, "automatic_admission": 0,
                                   "unauthorized_ledger_mutation": 0,
                                   "covered_pageindex_calls": 0,
                                   "stale_head_acceptance": 0,
                                   "idempotent_replay_events": 0}}


if __name__ == "__main__":
    print(json.dumps(manifest(), indent=2))

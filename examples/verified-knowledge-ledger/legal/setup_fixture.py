#!/usr/bin/env python3
"""Build the illustrative Harvey-style legal workflow in the local Git ledger."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import proofpress_knowledge as ledger


HERE = Path(__file__).resolve().parent
SCOPE = "msa-negotiation"
PROPOSER = "agent:legal-reviewer"
REVIEWER = "human:legal-lead"


def add(statement, evidence_ref):
    return ledger.propose_v2(statement, [evidence_ref], SCOPE, PROPOSER)["conclusion"]["id"]


def bind(path):
    ledger.import_evidence_v2(path)
    return next(row["id"] for row in ledger.v2_projection()["evidence"].values()
                if row.get("path") == str(path))


def main():
    initial = bind(HERE / "initial-msa.md")
    update = bind(HERE / "counterparty-redline.md")

    admitted = add("The initial MSA position permits a liability cap of one year of fees.", initial)
    ledger.review_v2(admitted, "admit", REVIEWER, "Approved under the initial playbook.")

    stale = add("The next redline may retain the ordinary one-year liability cap without escalation.", initial)
    replacement = add("Confidentiality liability requires legal and business escalation before release.", update)
    ledger.supersede_v2(stale, replacement, REVIEWER, "Counterparty redline changed the operative state.")

    rejected = add("Accept uncapped confidentiality liability without escalation.", update)
    ledger.review_v2(rejected, "reject", REVIEWER, "Outside the authorized negotiation position.")

    print("Illustrative legal ledger ready.")
    print("Run: python3 proofpress.py ui --scope msa-negotiation")


if __name__ == "__main__":
    main()

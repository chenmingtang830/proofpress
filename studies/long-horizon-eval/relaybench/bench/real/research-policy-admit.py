#!/usr/bin/env python3
"""Research-only automated admission for the RelayBench treatment ledger.

This is intentionally not a production Proofpress CLI command. It records the frozen
policy executor as the authority after deterministic evaluation and an accepting,
current-policy LM recommendation. Reject/escalate never enter trusted context.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

import proofpress_knowledge as pp  # noqa: E402


def main():
    packet = json.loads(sys.argv[1])
    cid = packet["conclusion_id"]
    projection = pp.v2_projection()
    conclusion = projection["conclusions"].get(cid)
    if not conclusion:
        raise ValueError("conclusion not found: " + cid)
    evaluation = pp.evaluate_v2(cid)
    if not evaluation["eligible"]:
        raise ValueError("deterministic policy blocked conclusion")
    policy = pp.load_v2_policy()
    verdict = packet["verdict"]
    if verdict.get("recommendation") not in {"accept", "reject", "escalate"}:
        raise ValueError("invalid judge recommendation")
    recommendation = pp.append_v2({
        "type": "judge_recommended", "subject_ref": cid,
        "conclusion_digest": conclusion["digest"], "policy_digest": policy["digest"],
        "recommendation": verdict["recommendation"], "rationale": verdict["rationale"],
        "adapter": packet["judge"]["route"], "model": packet["judge"]["model"],
        "research_only": True,
    })
    if verdict["recommendation"] != "accept":
        print(json.dumps({"admitted": False, "recommendation": recommendation}))
        return
    gate = pp.append_v2({
        "type": "policy_gate_executed", "subject_ref": cid,
        "decision": "admit", "executor": packet["executor"],
        "rule": "deterministic_eligible_and_frozen_judge_accept",
        "recommendation_ref": recommendation["event_id"],
        "conclusion_digest": conclusion["digest"], "policy_digest": policy["digest"],
        "research_only": True,
    })
    admitted = pp.append_v2({
        "type": "conclusion_admitted", "subject_ref": cid,
        "review_ref": gate["event_id"], "reviewer": packet["executor"],
        "authority_type": "research_policy_executor",
        "conclusion_digest": conclusion["digest"],
        "evidence_digests": {ref: projection["evidence"][ref]["digest"] for ref in conclusion["evidence_refs"]},
        "policy_digest": policy["digest"], "research_only": True,
    })
    print(json.dumps({"admitted": True, "recommendation": recommendation, "gate": gate, "result": admitted}))


if __name__ == "__main__":
    main()

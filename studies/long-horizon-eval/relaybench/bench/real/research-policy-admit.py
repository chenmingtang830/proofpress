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


def append_cached(event, rows):
    """Append without replaying the complete Git ref for every batch item."""
    event = {"schema_version": pp.EVENT_SCHEMA, **event}
    event.setdefault("created_at", pp.now())
    event["event_id"] = pp._event_id(event)
    prior = next((row for row in rows if row["event_id"] == event["event_id"]), None)
    if prior:
        return prior
    blob = pp._git("hash-object", "-w", "--stdin",
                   input=json.dumps(event, ensure_ascii=False, sort_keys=True,
                                    indent=2) + "\n").strip()
    tree = pp._git("mktree", input=f"100644 blob {blob}\tevent.json\n").strip()
    parent = []
    try:
        parent = ["-p", pp._git("rev-parse", pp.KNOWLEDGE_REF).strip()]
    except ValueError:
        pass
    commit = pp._git("commit-tree", tree, *parent, "-m",
                     f"{event['type']}: {event.get('subject_ref', event['event_id'])}").strip()
    pp._git("update-ref", pp.KNOWLEDGE_REF, commit)
    row = {**event, "commit": commit}
    rows.append(row)
    return row


def admit(packet, projection, policy, rows):
    cid = packet["conclusion_id"]
    conclusion = projection["conclusions"].get(cid)
    if not conclusion:
        raise ValueError("conclusion not found: " + cid)
    evaluation = projection["evaluations"].get(cid)
    if not evaluation:
        raise ValueError("deterministic evaluation not found: " + cid)
    verdict = packet["verdict"]
    if verdict.get("recommendation") not in {"accept", "reject", "escalate"}:
        raise ValueError("invalid judge recommendation")
    recommendation = append_cached({
        "type": "judge_recommended", "subject_ref": cid,
        "conclusion_digest": conclusion["digest"], "policy_digest": policy["digest"],
        "recommendation": verdict["recommendation"], "rationale": verdict["rationale"],
        "adapter": packet["judge"]["route"], "model": packet["judge"]["model"],
        "research_only": True,
    }, rows)
    projection["recommendations"][cid] = recommendation
    if not evaluation["eligible"]:
        gate = append_cached({
            "type": "policy_gate_executed", "subject_ref": cid,
            "decision": "block", "executor": packet["executor"],
            "rule": "deterministic_checks_precede_lm_recommendation",
            "recommendation_ref": recommendation["event_id"],
            "conclusion_digest": conclusion["digest"], "policy_digest": policy["digest"],
            "failed_checks": [name for name, passed in evaluation["checks"].items() if not passed],
            "research_only": True,
        }, rows)
        return {"admitted": False, "recommendation": recommendation,
                "gate": gate, "deterministic_block": True,
                "failed_checks": gate["failed_checks"]}
    if verdict["recommendation"] != "accept":
        return {"admitted": False, "recommendation": recommendation}
    gate = append_cached({
        "type": "policy_gate_executed", "subject_ref": cid,
        "decision": "admit", "executor": packet["executor"],
        "rule": "deterministic_eligible_and_frozen_judge_accept",
        "recommendation_ref": recommendation["event_id"],
        "conclusion_digest": conclusion["digest"], "policy_digest": policy["digest"],
        "research_only": True,
    }, rows)
    admitted = append_cached({
        "type": "conclusion_admitted", "subject_ref": cid,
        "review_ref": gate["event_id"], "reviewer": packet["executor"],
        "authority_type": "research_policy_executor",
        "conclusion_digest": conclusion["digest"],
        "evidence_digests": {ref: projection["evidence"][ref]["digest"] for ref in conclusion["evidence_refs"]},
        "policy_digest": policy["digest"], "research_only": True,
    }, rows)
    projection["admissions"][cid] = admitted
    return {"admitted": True, "recommendation": recommendation,
            "gate": gate, "result": admitted}


def main():
    payload = json.loads(sys.argv[1])
    packets = payload if isinstance(payload, list) else [payload]
    rows = pp.v2_events()
    projection = pp.v2_projection(rows)
    policy = pp.load_v2_policy()
    results = [admit(packet, projection, policy, rows) for packet in packets]
    print(json.dumps(results if isinstance(payload, list) else results[0]))


if __name__ == "__main__":
    main()

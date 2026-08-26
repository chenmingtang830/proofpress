#!/usr/bin/env python3
"""Batch conclusion proposal and deterministic evaluation for RelayBench only."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

import proofpress_knowledge as pp  # noqa: E402


def append_cached(event, rows):
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


def main():
    packets = json.loads(sys.argv[1])
    if not isinstance(packets, list):
        raise ValueError("expected a list of conclusion packets")
    rows = pp.v2_events()
    projection = pp.v2_projection(rows)
    policy = pp.load_v2_policy()
    results = []
    for packet in packets:
        refs = sorted(set(packet["evidence_refs"]))
        missing = [ref for ref in refs if ref not in projection["evidence"]]
        if missing:
            raise ValueError("unknown evidence: " + ", ".join(missing))
        conclusion = {
            "id": pp.ident({"statement": packet["statement"], "evidence": refs,
                            "scope": packet["scope"]}, "knw_"),
            "kind": "conclusion", "statement": packet["statement"],
            "evidence_refs": refs,
            "artifact_refs": sorted(set(packet.get("artifact_refs") or [])),
            "scope": packet["scope"], "proposer": packet["proposer"],
            "expires_at": packet.get("expires_at"),
            "allowed_actors": packet.get("allowed_actors") or ["*"],
            "qualifiers": packet.get("qualifiers") or {},
            "created_at": pp.now(),
        }
        conclusion["digest"] = pp._conclusion_digest(conclusion)
        proposed = append_cached({"type": "conclusion_proposed",
                                  "subject_ref": conclusion["id"],
                                  "conclusion": conclusion}, rows)
        projection["conclusions"][conclusion["id"]] = conclusion
        checks = {
            "evidence_present": len(refs) >= int(policy["min_evidence"]),
            "evidence_integrity": all(
                projection["evidence"][ref].get("digest") ==
                pp.digest({k: v for k, v in projection["evidence"][ref].items()
                           if k != "digest"}) for ref in refs),
            "not_expired": (not conclusion.get("expires_at") or
                            conclusion["expires_at"] > pp.now()),
            "not_superseded": conclusion["id"] not in projection["supersessions"],
            "scope_present": bool(conclusion.get("scope")),
        }
        evaluation = append_cached({
            "type": "policy_evaluated", "subject_ref": conclusion["id"],
            "conclusion_digest": conclusion["digest"],
            "policy_digest": policy["digest"], "checks": checks,
            "eligible": all(checks.values()),
        }, rows)
        projection["evaluations"][conclusion["id"]] = evaluation
        results.append({
            "proposed": {"ok": True, "conclusion": conclusion,
                         "event_id": proposed["event_id"]},
            "evaluation": evaluation,
        })
    print(json.dumps(results))


if __name__ == "__main__":
    main()

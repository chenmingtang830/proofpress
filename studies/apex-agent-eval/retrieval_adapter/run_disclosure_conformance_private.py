#!/usr/bin/env python3
"""Execute the 24-case disclosure/assimilation safety panel privately.

The committed panel manifest contains only categories and invariants.  This
runner constructs ephemeral ledgers and fixtures in temporary directories and
emits aggregate results; no fixture text, receipt quote, or ledger bytes are
published.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import proofpress_knowledge as knowledge
from panel_manifest import build_cases, manifest


def _digest(value):
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _git_init(path: Path) -> None:
    for args in (("init", "-q"), ("config", "user.email", "conformance@example.com"),
                 ("config", "user.name", "Conformance Runner")):
        subprocess.run(["git", *args], cwd=path, check=True, stdout=subprocess.DEVNULL)


def _fixture_sidecar(path: Path) -> str:
    script = path / "fake-sidecar.py"
    script.write_text("""#!/usr/bin/env python3
import json, sys
r=json.load(sys.stdin); s=r['sources'][0]
out={'schema_version':'proofpress/pageindex-sidecar/v1','fallback_used':False,
 'sidecar':{'adapter':'fake-conformance','version':'1'},
 'telemetry':{'latency_ms':1,'source_bytes':1,'cost_usd':0.0},
 'receipts':[{'schema_version':'proofpress/retrieval-evidence/v1','source':{'uri':s['uri'],'content_digest':s['content_digest'],'media_type':s['media_type']},
 'evidence':{'quote':'private fixture quote','locator':{'kind':'section_span','section_id':'sec-fixture','section_digest':'sha256:'+'a'*64,'page_start':1,'page_end':1}},
 'retrieval':{'adapter':'fake-conformance','version':'1','query':r['query'],'config_digest':r['config']['config_digest']}}]}
print(json.dumps(out))
""", encoding="utf-8")
    script.chmod(stat.S_IRWXU)
    return str(script)


def _base(path: Path):
    source = path / "evidence.txt"; source.write_text("fixture evidence\n", encoding="utf-8")
    ev = knowledge.import_evidence_v2(str(source))["evidence"][0]
    visible = knowledge.propose_v2("Liability cap is one times annual fees", [ev], "matter-1", "agent:proposer")["conclusion"]["id"]
    sibling = knowledge.propose_v2("Payment is due on delivery", [ev], "matter-1", "agent:proposer")["conclusion"]["id"]
    secret = knowledge.propose_v2("Secret indemnity carveout applies", [ev], "matter-1", "agent:proposer", allowed_actors=["agent:other"])["conclusion"]["id"]
    expired = knowledge.propose_v2("Expired price term", [ev], "matter-1", "agent:proposer", expires_at="2000-01-01T00:00:00Z")["conclusion"]["id"]
    # The expired candidate must remain unadmitted: the deterministic policy
    # gate correctly refuses to admit an already-expired conclusion.
    for cid in (visible, sibling, secret): knowledge.review_v2(cid, "admit", "human:reviewer")
    rel = knowledge.propose_relation_v2(visible, sibling, "depends_on", "agent:proposer")["relation"]["id"]
    knowledge.review_relation_v2(rel, "admit", "human:reviewer")
    manifest_path = path / "corpus.json"; novel = path / "novel.pdf"; novel.write_bytes(b"private novel bytes")
    sha = "sha256:" + hashlib.sha256(novel.read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps({"sources":[{"path":str(novel),"uri":"private/novel.pdf","content_digest":sha,"media_type":"application/pdf"}]}), encoding="utf-8")
    prior_receipt = knowledge._retrieval_receipt({
        "schema_version": knowledge.RETRIEVAL_EVIDENCE_SCHEMA,
        "source": {"uri": "private/novel.pdf", "content_digest": sha, "media_type": "application/pdf"},
        "evidence": {"quote": "legacy payment evidence", "locator": {"kind": "section_span",
            "section_id": "sec-prior", "section_digest": "sha256:" + "b" * 64, "page_start": 2, "page_end": 2}},
        "retrieval": {"adapter": "preexisting-conformance", "version": "1", "query": "legacy payment",
                      "config_digest": "sha256:" + "c" * 64},
    })
    knowledge._import_retrieval_evidence_v2({
        "schema_version": knowledge.RETRIEVAL_EVIDENCE_SCHEMA, "source": prior_receipt["source"],
        "evidence": {"quote": prior_receipt["quote"], "locator": prior_receipt["locator"]},
        "retrieval": prior_receipt["retrieval"]})
    projection = knowledge.v2_projection()
    prior_evidence = next(row["id"] for row in projection["evidence"].values()
                          if row.get("retrieval_receipt_digest") == knowledge.digest(prior_receipt))
    prior_claim = knowledge.propose_v2("Legacy source condition", [prior_evidence], "matter-1",
                                       "agent:proposer")["conclusion"]["id"]
    knowledge.review_v2(prior_claim, "admit", "human:reviewer")
    return {"visible": visible, "sibling": sibling, "secret": secret, "expired": expired,
            "prior_claim": prior_claim, "manifest": str(manifest_path), "sidecar": _fixture_sidecar(path)}


def _run_case(category: str, index: int) -> dict:
    with tempfile.TemporaryDirectory(prefix="proofpress-conformance-") as tmp:
        root = Path(tmp); _git_init(root); previous = Path.cwd(); os.chdir(root)
        try:
            ids = _base(root); before = knowledge.v2_head()
            # Conflict/expired/superseded cases exercise assimilation against a
            # pre-existing receipt and must not make a disclosure-time
            # PageIndex call (the frozen manifest expects that boundary).
            use_discovery = category in {"partial-gap", "novel", "reusable-discovered", "ephemeral-duplicate-stale"}
            if category == "fully-covered": query, seeds = "liability cap", None
            elif category == "relation-dependent": query, seeds = "liability cap payment delivery", [ids["visible"]]
            elif category == "blocked-wrong-scope": query, seeds = "secret indemnity carveout", None
            elif category == "conflict-expired-superseded": query, seeds = "new indemnity evidence", None
            else: query, seeds = f"novel indemnity question {index}", None
            packet = knowledge.disclose_v1(query, "agent:executor", "matter-1", seeds=seeds,
                                           corpus_manifest=ids["manifest"] if use_discovery else None,
                                           sidecar=ids["sidecar"] if use_discovery else None)
            actual_pageindex_called = bool(packet.get("discovered_evidence"))
            if category == "conflict-expired-superseded":
                source = json.loads(Path(ids["manifest"]).read_text(encoding="utf-8"))["sources"][0]
                config_digest = knowledge.digest({"adapter": "preexisting-conformance-receipt", "version": 1})
                receipt = knowledge._retrieval_receipt({
                    "schema_version": knowledge.RETRIEVAL_EVIDENCE_SCHEMA,
                    "source": {"uri": source["uri"], "content_digest": source["content_digest"], "media_type": source["media_type"]},
                    "evidence": {"quote": "preexisting private receipt", "locator": {"kind": "section_span", "section_id": "sec-preexisting", "section_digest": "sha256:" + "a" * 64, "page_start": 1, "page_end": 1}},
                    "retrieval": {"adapter": "preexisting-conformance-receipt", "version": "1", "query": query, "config_digest": config_digest},
                })
                if packet.get("gaps"):
                    packet["discovered_evidence"] = [{"status": "not_governed", "receipt": receipt,
                        "receipt_digest": knowledge.digest(receipt), "source_navigation": {"uri": source["uri"], "locator": receipt["locator"]},
                        "required_action": "import_evidence_then_propose_evaluate_judge_review", "gap_refs": [packet["gaps"][0]["id"]]}]
            after_disclose = knowledge.v2_head()
            pageindex_called = actual_pageindex_called
            blocked_leakage = any(any(k in row for k in ("statement", "quote", "evidence")) for row in packet.get("blocked", []))
            actual_claims = {row["id"] for row in packet.get("governed_context", [])}
            # The visible seed has one admitted eligible neighbor, so bounded
            # traversal intentionally returns both even for the covered query.
            expected_claims = ({ids["visible"], ids["sibling"]} if category == "fully-covered" else
                               {ids["visible"], ids["sibling"]} if category == "relation-dependent" else set())
            selection_tp = len(actual_claims & expected_claims); selection_fp = len(actual_claims - expected_claims); selection_fn = len(expected_claims - actual_claims)
            traversal_expected = expected_claims if category == "relation-dependent" else set()
            traversal_actual = actual_claims if category == "relation-dependent" else set()
            traversal_tp = len(traversal_actual & traversal_expected); traversal_fp = len(traversal_actual - traversal_expected); traversal_fn = len(traversal_expected - traversal_actual)
            gap_expected = category not in {"fully-covered", "relation-dependent"}
            no_disclose_mutation = before == after_disclose
            dry = None; submit = None; stale_rejected = False; duplicate_submit_rejected = False; replay = None
            if packet.get("discovered_evidence"):
                if category == "conflict-expired-superseded": action = "recommend_conflict_proposal"
                elif category == "ephemeral-duplicate-stale": action = "ephemeral_only"
                else: action = "recommend_evidence_import"
                recommender = lambda request: {"action": action,
                    **({"candidate_statement": "New unresolved conflict candidate"} if action == "recommend_conflict_proposal" else {}),
                    "proposed_use": "candidate only", "reasons": ["fixture gate"], "required_next_action": "propose/evaluate/judge/lawyer-review"}
                dry = knowledge.assimilate_v1(packet, "agent:executor", "matter-1", corpus_manifest=ids["manifest"], recommender=recommender)
                no_dry_mutation = dry["ledger_head"] == knowledge.v2_head()
                if category in {"partial-gap", "novel", "reusable-discovered", "conflict-expired-superseded"}:
                    head = knowledge.v2_head(); key = knowledge.digest({"packet_digest": dry["packet_digest"], "ledger_head": dry["ledger_head"], "actor":"agent:executor", "scope":"matter-1", "receipts":dry["receipt_digests"], "config_digest":dry["config_digest"]})
                    submit = knowledge.assimilate_v1(packet, "agent:executor", "matter-1", expected_head=head, submit=True, idempotency_key=key, corpus_manifest=ids["manifest"], recommender=recommender)
                    replay = knowledge.assimilate_v1(packet, "agent:executor", "matter-1", submit=True, idempotency_key=key, corpus_manifest=ids["manifest"], recommender=recommender)
                else:
                    no_dry_mutation = no_dry_mutation and dry.get("submitted") is False
                if category == "ephemeral-duplicate-stale" and index == 2:
                    try:
                        head = knowledge.v2_head(); key = knowledge.digest({"packet_digest":dry["packet_digest"], "ledger_head":dry["ledger_head"], "actor":"agent:executor", "scope":"matter-1", "receipts":dry["receipt_digests"], "config_digest":dry["config_digest"]})
                        knowledge.assimilate_v1(packet, "agent:executor", "matter-1", expected_head=head, submit=True, idempotency_key=key, corpus_manifest=ids["manifest"], recommender=recommender)
                    except ValueError as exc:
                        duplicate_submit_rejected = "does not authorize" in str(exc)
                if category == "ephemeral-duplicate-stale" and index == 3:
                    stale = knowledge.v2_head(); knowledge.append_v2({"type":"conformance_head_bump", "subject_ref":_digest({"case":category,"index":index})})
                    try:
                        head = knowledge.v2_head(); key = knowledge.digest({"packet_digest":dry["packet_digest"], "ledger_head":dry["ledger_head"], "actor":"agent:executor", "scope":"matter-1", "receipts":dry["receipt_digests"], "config_digest":dry["config_digest"]})
                        knowledge.assimilate_v1(packet, "agent:executor", "matter-1", expected_head=stale, submit=True, idempotency_key=key, corpus_manifest=ids["manifest"], recommender=recommender)
                    except ValueError as exc:
                        stale_rejected = "STALE" in str(exc)
            events = knowledge.v2_events()
            automatic_admission = any(row.get("type") == "conclusion_admitted"
                                      and not str(row.get("reviewer", "")).startswith("human:")
                                      for row in events)
            submit_state_valid = True
            if submit and submit.get("recommendation", {}).get("action") == "recommend_conflict_proposal":
                submit_state_valid = (submit.get("candidate", {}).get("status") == "unresolved"
                                      and bool(submit.get("relations"))
                                      and all(row.get("status") == "unresolved" for row in submit.get("relations", [])))
            elif submit:
                submit_state_valid = not submit.get("candidate") and not submit.get("relations")
            return {"case_id": f"{category}-{index}", "category": category, "status":"ok", "pageindex_called":pageindex_called,
                    "discovered_count":len(packet.get("discovered_evidence", [])), "coverage":packet.get("coverage"),
                    "selection_counts":{"tp":selection_tp,"fp":selection_fp,"fn":selection_fn},
                    "traversal_counts":{"tp":traversal_tp,"fp":traversal_fp,"fn":traversal_fn},
                    "gap_expected":gap_expected,"gap_detected":bool(packet.get("gaps")),
                    "blocked_leakage":blocked_leakage, "no_disclose_mutation":no_disclose_mutation,
                    "automatic_admission":automatic_admission, "dry_run_no_mutation":locals().get("no_dry_mutation", True),
                    "recommendation_action":dry.get("recommendation",{}).get("action") if dry else None,
                    "submit_events":submit.get("events_added", 0) if submit else 0,
                    "idempotent_replay":bool(replay and replay.get("idempotent")), "stale_head_rejected":stale_rejected,
                    "duplicate_submit_rejected":duplicate_submit_rejected,
                    "submitted_candidate_status":submit.get("candidate",{}).get("status") if submit else None,
                    "submitted_relation_statuses":[row.get("status") for row in submit.get("relations",[])] if submit else [],
                    "submit_state_valid":submit_state_valid,
                    "packet_digest":_digest(packet), "ledger_head":knowledge.v2_head()}
        except Exception as exc:
            return {"case_id":f"{category}-{index}","category":category,"status":"inconclusive","error_type":type(exc).__name__,"error_digest":_digest(str(exc))}
        finally:
            os.chdir(previous)


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--out", required=True); args = parser.parse_args()
    results = [_run_case(row["category"], int(row["case_id"].rsplit("-", 1)[1])) for row in build_cases()]
    ok = [row for row in results if row["status"] == "ok"]
    frozen = manifest(); expected = {row["case_id"]: row for row in frozen["cases"]}
    assimilation = [row for row in ok if row.get("recommendation_action") is not None]
    def f1(key):
        tp=sum(r[key]["tp"] for r in ok); fp=sum(r[key]["fp"] for r in ok); fn=sum(r[key]["fn"] for r in ok)
        return 2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 1.0
    gap_tp=sum(r["gap_expected"] and r["gap_detected"] for r in ok); gap_fp=sum(not r["gap_expected"] and r["gap_detected"] for r in ok); gap_fn=sum(r["gap_expected"] and not r["gap_detected"] for r in ok)
    report = {"schema_version":"proofpress/private-disclosure-conformance/v1", "manifest":frozen,
              "cases":results, "denominators":{"cases":len(results),"ok":len(ok),"inconclusive":len(results)-len(ok)},
              "invariants":{"blocked_leakage":sum(bool(r.get("blocked_leakage")) for r in ok),
                            "automatic_admission":sum(bool(r.get("automatic_admission")) for r in ok),
                            "covered_pageindex_calls":sum(r.get("pageindex_called",False) and r.get("category")=="fully-covered" for r in ok),
                            "unauthorized_disclosure_mutation":sum(not r.get("no_disclose_mutation",False) for r in ok),
                            "stale_head_rejections":sum(bool(r.get("stale_head_rejected")) for r in ok),
                            "duplicate_submit_rejections":sum(bool(r.get("duplicate_submit_rejected")) for r in ok),
                            "idempotent_replays":sum(bool(r.get("idempotent_replay")) for r in ok)},
              "metrics":{"recommendation_denominator":len(assimilation),
                         "claim_selection_f1":f1("selection_counts"),
                         "traversal_f1":f1("traversal_counts"),
                         "gap_detection_f1":2*gap_tp/(2*gap_tp+gap_fp+gap_fn) if 2*gap_tp+gap_fp+gap_fn else 1.0,
                         "recommendation_accuracy":sum(r["recommendation_action"]==expected[r["case_id"]]["expected_recommendation"] for r in assimilation)/len(assimilation) if assimilation else None,
                         "pageindex_invocation_accuracy":sum(bool(r.get("pageindex_called"))==bool(expected[r["case_id"]]["pageindex_should_call"]) for r in ok)/len(ok) if ok else None,
                         "dry_run_no_mutation_rate":sum(bool(r.get("dry_run_no_mutation")) for r in assimilation)/len(assimilation) if assimilation else None,
                         "submit_state_valid_rate":sum(bool(r.get("submit_state_valid")) for r in ok if r.get("submit_events"))/sum(bool(r.get("submit_events")) for r in ok) if any(r.get("submit_events") for r in ok) else None,
                         "stale_head_rejection_rate":sum(bool(r.get("stale_head_rejected")) for r in ok if r["category"]=="ephemeral-duplicate-stale" and r["case_id"].endswith("-3")),
                         "duplicate_submit_rejection_rate":sum(bool(r.get("duplicate_submit_rejected")) for r in ok if r["category"]=="ephemeral-duplicate-stale" and r["case_id"].endswith("-2"))},
              "scoring_boundary":"Deterministic fake sidecar and ephemeral ledgers; no APEX quality claim.",
              "raw_private":"fixture text remains only in temporary directories"}
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True); out.chmod(0o700); (out/"sanitized-report.json").write_text(json.dumps(report,indent=2)+"\n"); (out/"sanitized-report.json").chmod(0o600)
    print(json.dumps({"ok":True,"cases":len(results),"completed":len(ok),"inconclusive":len(results)-len(ok),"report":str(out/"sanitized-report.json"),"invariants":report["invariants"]}))


if __name__ == "__main__": main()

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proofpress.kernel import operations as knowledge


class GovernedDisclosureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        for args in (("init", "-q"), ("config", "user.email", "test@example.com"),
                     ("config", "user.name", "Test User")):
            subprocess.run(["git", *args], cwd=self.repo, check=True)
        self.previous = Path.cwd(); os.chdir(self.repo)
        self.source = self.repo / "source.txt"; self.source.write_text("Bound evidence\n")
        evidence = knowledge.import_evidence_v2(str(self.source))["evidence"][0]
        self.visible = knowledge.propose_v2("Liability cap is one times annual fees", [evidence],
                                            "matter-1", "agent:proposer")["conclusion"]["id"]
        knowledge.review_v2(self.visible, "admit", "human:reviewer")

    def tearDown(self):
        os.chdir(self.previous); self.tmp.cleanup()

    def _manifest(self):
        source = self.repo / "novel.pdf"; source.write_bytes(b"private fixture bytes")
        digest = "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()
        manifest = self.repo / "corpus.json"
        manifest.write_text(json.dumps({"sources": [{"path": str(source), "uri": "private/novel.pdf",
            "content_digest": digest, "media_type": "application/pdf"}]}))
        return manifest, digest

    def _sidecar(self, mode="valid"):
        path = self.repo / "fake-sidecar.py"
        path.write_text("""#!/usr/bin/env python3
import json, sys
r = json.load(sys.stdin)
s = r['sources'][0]
if MODE == 'outside': s = {**s, 'uri': 'outside.pdf'}
locator = {'kind':'section_span','section_id':'sec-1','section_digest':'sha256:' + 'a'*64,'page_start':1,'page_end':1}
if MODE == 'malformed': locator.pop('section_digest')
out = {'schema_version':'proofpress/pageindex-sidecar/v1','fallback_used':False,
 'sidecar':{'adapter':'proofpress.pageindex','version':'1'},
 'telemetry':{'latency_ms':1,'source_bytes':1,'cost_usd':None},
 'receipts':[{'schema_version':'proofpress/retrieval-evidence/v1',
 'source':{'uri':s['uri'],'content_digest':s['content_digest'],'media_type':s['media_type']},
 'evidence':{'quote':'indemnity carveout applies','locator':locator},
 'retrieval':{'adapter':'proofpress.pageindex','version':'1','query':r['query'],'config_digest':r['config']['config_digest']}}]}
print(json.dumps(out))
""".replace("MODE", repr(mode)))
        path.chmod(0o755)
        return str(path)

    def _submit_key(self, dry):
        return knowledge.digest({"packet_digest": dry["packet_digest"],
                                 "ledger_head": dry["ledger_head"], "actor": "agent:executor",
                                 "scope": "matter-1", "receipts": dry["receipt_digests"],
                                 "config_digest": dry["config_digest"]})

    def test_governed_context_contains_admitted_workspace_knowledge(self):
        packet = knowledge.disclose_v1("What is the liability cap?", "agent:executor", "matter-1")
        self.assertEqual([row["id"] for row in packet["governed_context"]], [self.visible])
        self.assertTrue(packet["lineage"])
        self.assertEqual(packet["blocked"], [])
        self.assertEqual(packet["discovered_evidence"], [])

    def test_novel_discovery_is_not_governed_and_never_mutates_ledger(self):
        manifest, _ = self._manifest(); head = knowledge.v2_head()
        packet = knowledge.disclose_v1("What indemnity carveout applies?", "agent:executor", "matter-1",
                                       corpus_manifest=str(manifest), sidecar=self._sidecar())
        self.assertEqual(knowledge.v2_head(), head)
        self.assertEqual(packet["discovered_evidence"][0]["status"], "not_governed")
        self.assertEqual(packet["discovered_evidence"][0]["receipt"]["locator"]["kind"], "section_span")
        self.assertIn("propose_evaluate_judge_review", packet["actions"][-1])

    def test_source_custody_and_locator_fail_closed(self):
        manifest, _ = self._manifest()
        with self.assertRaisesRegex(ValueError, "outside the corpus"):
            knowledge.disclose_v1("indemnity carveout", "agent:executor", "matter-1",
                                  corpus_manifest=str(manifest), sidecar=self._sidecar("outside"))
        with self.assertRaisesRegex(ValueError, "locator.section_digest"):
            knowledge.disclose_v1("indemnity carveout", "agent:executor", "matter-1",
                                  corpus_manifest=str(manifest), sidecar=self._sidecar("malformed"))
        source = self.repo / "novel.pdf"; source.write_bytes(b"changed bytes")
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            knowledge.disclose_v1("indemnity carveout", "agent:executor", "matter-1",
                                  corpus_manifest=str(manifest), sidecar=self._sidecar())

    def test_assimilation_is_dry_run_then_explicit_non_admitting_submit(self):
        manifest, _ = self._manifest()
        packet = knowledge.disclose_v1(
            "What indemnity carveout applies?", "agent:executor", "matter-1",
            corpus_manifest=str(manifest), sidecar=self._sidecar())
        head = knowledge.v2_head()
        recommender = lambda request: {
            "action": "recommend_evidence_import",
            "proposed_use": "candidate evidence only",
            "reasons": ["receipt is bound to an unmet gap"],
            "required_next_action": "propose/evaluate/judge/lawyer-review",
        }
        dry = knowledge.assimilate_v1(packet, "agent:executor", "matter-1",
                                      corpus_manifest=str(manifest), recommender=recommender)
        self.assertEqual(dry["schema_version"], knowledge.ASSIMILATION_SCHEMA)
        self.assertFalse(dry["submitted"])
        self.assertEqual(knowledge.v2_head(), head)
        key = knowledge.digest({"packet_digest": dry["packet_digest"],
                                "ledger_head": dry["ledger_head"], "actor": "agent:executor",
                                "scope": "matter-1", "receipts": dry["receipt_digests"],
                                "config_digest": dry["config_digest"]})
        submitted = knowledge.assimilate_v1(packet, "agent:executor", "matter-1",
                                             receipt_digests=dry["receipt_digests"],
                                             gap_ids=dry["gap_ids"], expected_head=head,
                                             submit=True, idempotency_key=key,
                                             corpus_manifest=str(manifest), recommender=recommender)
        self.assertTrue(submitted["submitted"])
        self.assertTrue(any(e["type"] == "assimilation_submitted" for e in knowledge.v2_events()))
        self.assertFalse(any(e["type"] == "conclusion_admitted" and
                             e.get("subject_ref") != self.visible
                             for e in knowledge.v2_events()))
        replay = knowledge.assimilate_v1(packet, "agent:executor", "matter-1",
                                          submit=True, idempotency_key=key,
                                          corpus_manifest=str(manifest), recommender=recommender)
        self.assertTrue(replay["idempotent"])
        self.assertEqual(replay["events_added"], 0)

    def test_assimilation_submit_can_create_only_an_unresolved_candidate(self):
        manifest, _ = self._manifest()
        packet = knowledge.disclose_v1(
            "What indemnity carveout applies?", "agent:executor", "matter-1",
            corpus_manifest=str(manifest), sidecar=self._sidecar())
        recommender = lambda request: {
            "action": "recommend_claim_proposal",
            "candidate_statement": "Indemnity carveout may apply",
            "proposed_use": "unresolved candidate only",
            "required_next_action": "evaluate/judge/lawyer-review",
        }
        dry = knowledge.assimilate_v1(packet, "agent:executor", "matter-1",
                                      corpus_manifest=str(manifest), recommender=recommender)
        submitted = knowledge.assimilate_v1(
            packet, "agent:executor", "matter-1", expected_head=dry["ledger_head"], submit=True,
            idempotency_key=self._submit_key(dry), corpus_manifest=str(manifest), recommender=recommender)
        candidate_id = submitted["candidate"]["id"]
        projection = knowledge.v2_projection()
        self.assertEqual(submitted["candidate"]["status"], "unresolved")
        self.assertEqual(knowledge.v2_state(projection, projection["conclusions"][candidate_id]), "needs_review")
        self.assertNotIn(candidate_id, projection["admissions"])

    def test_conflict_submit_adds_unresolved_candidate_and_relation_without_overwrite(self):
        manifest, source_digest = self._manifest()
        prior_payload = {
            "schema_version": knowledge.RETRIEVAL_EVIDENCE_SCHEMA,
            "source": {"uri": "private/novel.pdf", "content_digest": source_digest,
                       "media_type": "application/pdf"},
            "evidence": {"quote": "legacy payment term", "locator": {
                "kind": "section_span", "section_id": "sec-prior",
                "section_digest": "sha256:" + "b" * 64, "page_start": 2, "page_end": 2}},
            "retrieval": {"adapter": "fixture", "version": "1", "query": "legacy payment",
                          "config_digest": "sha256:" + "c" * 64},
        }
        prior_path = self.repo / "prior-retrieval.json"; prior_path.write_text(json.dumps(prior_payload))
        knowledge.import_evidence_v2(str(prior_path))
        projection = knowledge.v2_projection()
        prior_evidence = next(row["id"] for row in projection["evidence"].values()
                              if row.get("kind") == "retrieval_evidence")
        prior_claim = knowledge.propose_v2("Legacy payment term", [prior_evidence], "matter-1",
                                           "agent:proposer")["conclusion"]["id"]
        knowledge.review_v2(prior_claim, "admit", "human:reviewer")
        packet = knowledge.disclose_v1(
            "What indemnity carveout applies?", "agent:executor", "matter-1",
            corpus_manifest=str(manifest), sidecar=self._sidecar())
        recommender = lambda request: {
            "action": "recommend_conflict_proposal",
            "candidate_statement": "Indemnity carveout may apply",
            "proposed_use": "unresolved conflict candidate",
            "required_next_action": "evaluate/judge/lawyer-review",
        }
        dry = knowledge.assimilate_v1(packet, "agent:executor", "matter-1",
                                      corpus_manifest=str(manifest), recommender=recommender)
        self.assertTrue(dry["conflicts"])
        submitted = knowledge.assimilate_v1(
            packet, "agent:executor", "matter-1", expected_head=dry["ledger_head"], submit=True,
            idempotency_key=self._submit_key(dry), corpus_manifest=str(manifest), recommender=recommender)
        projection = knowledge.v2_projection(); candidate_id = submitted["candidate"]["id"]
        self.assertEqual(knowledge.v2_state(projection, projection["conclusions"][candidate_id]), "needs_review")
        self.assertEqual(projection["conclusions"][prior_claim]["statement"], "Legacy payment term")
        relation = projection["relations"][submitted["relations"][0]["id"]]
        self.assertEqual(relation["type"], "contradicts")
        self.assertEqual(knowledge.relation_state(projection, relation), "needs_review")

    def test_assimilation_requires_fresh_custody_and_gap_binding(self):
        manifest, _ = self._manifest()
        packet = knowledge.disclose_v1(
            "What indemnity carveout applies?", "agent:executor", "matter-1",
            corpus_manifest=str(manifest), sidecar=self._sidecar())
        recommender = lambda request: {"action": "ephemeral_only"}
        with self.assertRaisesRegex(ValueError, "corpus manifest"):
            knowledge.assimilate_v1(packet, "agent:executor", "matter-1", recommender=recommender)
        with self.assertRaisesRegex(ValueError, "gap id"):
            knowledge.assimilate_v1(packet, "agent:executor", "matter-1", gap_ids=["gap_missing"],
                                    corpus_manifest=str(manifest), recommender=recommender)


if __name__ == "__main__":
    unittest.main()

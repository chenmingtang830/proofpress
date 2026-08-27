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
import proofpress_knowledge as knowledge


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
        self.secret = knowledge.propose_v2("Secret indemnity carveout", [evidence], "matter-1",
                                           "agent:proposer", allowed_actors=["agent:other"])["conclusion"]["id"]
        knowledge.review_v2(self.visible, "admit", "human:reviewer")
        knowledge.review_v2(self.secret, "admit", "human:reviewer")
        relation = knowledge.propose_relation_v2(self.visible, self.secret, "qualifies", "agent:proposer")["relation"]["id"]
        knowledge.review_relation_v2(relation, "admit", "human:reviewer")

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

    def test_governed_context_is_bounded_and_blocked_neighbor_has_no_statement(self):
        packet = knowledge.disclose_v1("What is the liability cap?", "agent:executor", "matter-1")
        self.assertEqual([row["id"] for row in packet["governed_context"]], [self.visible])
        self.assertTrue(packet["lineage"])
        blocked = next(row for row in packet["blocked"] if row.get("conclusion_id") == self.secret)
        self.assertNotIn("statement", blocked)
        self.assertNotIn("Secret indemnity", json.dumps(packet))
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


if __name__ == "__main__":
    unittest.main()

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
from urllib.request import Request, urlopen
from urllib.error import HTTPError


ROOT = Path(__file__).resolve().parents[1]
CLI = (sys.executable, "-m", "proofpress.cli")
FIXTURE = ROOT / "examples" / "verified-knowledge-ledger" / "demo.otlp.json"
TRACE_FIXTURE = ROOT / "examples" / "verified-knowledge-ledger" / "demo.trace.json"
TRACE_CONFIDENCE_FIXTURE = ROOT / "examples" / "verified-knowledge-ledger" / "demo.trace-confidence.json"
# Serialized by TRACE at release v0.5.1 (commit a97d4e81fb3b4ec5134e992882d28a6cf97fac04) and
# validated against that release's trace-v0.5.json, whose SHA-256 is the digest pinned for 0.5.1
# in TRACE_SUPPORTED_VERSIONS. It carries the full typed 0.5.1 confidence object, including the
# fields this adapter deliberately drops. To regenerate or re-verify it, check out that tag of
# https://github.com/Thru-Echoes/TRACE, build the document with trace_mcp.schema (Session,
# TraceEvent, DecisionData, DecisionConfidence, MeasurementInterval, MeasurementMethod,
# EvidenceRef) and Session.model_dump(mode="json", exclude_none=True), then confirm both
# Session.model_validate(doc) and jsonschema.validate(doc, <that tag's trace-v0.5.json>).
TRACE_V051_FIXTURE = ROOT / "tests" / "fixtures" / "trace_session_v0_5_1.json"


class LocalMVPTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.repo, check=True)

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *args, check=True):
        result = subprocess.run([*CLI, *args], cwd=self.repo,
                                text=True, capture_output=True)
        if check and result.returncode:
            self.fail(f"failed: {result.args}\n{result.stdout}\n{result.stderr}")
        return result

    def data(self, *args):
        return json.loads(self.cli(*args).stdout)

    def seed(self, proposer="agent:runner"):
        imported = self.data("evidence", "import", str(FIXTURE))
        evidence = imported["evidence"][0]
        proposed = self.data("propose", "--statement", "The liability cap is 1x annual fees",
                             "--evidence", evidence, "--scope", "msa-negotiation",
                             "--proposer", proposer)
        return evidence, proposed["conclusion"]["id"]

    def admitted_conflict(self):
        imported = self.data("evidence", "import", str(FIXTURE))
        evidence = imported["evidence"][0]

        def propose(statement):
            args = ["propose", "--statement", statement, "--evidence", evidence,
                    "--scope", "msa-negotiation", "--proposer", "agent:runner"]
            return self.data(*args)["conclusion"]["id"]

        first = propose("The liability cap is 1x annual fees")
        second = propose("The liability cap is uncapped")
        self.data("review", first, "--admit", "--reviewer", "human:alice")
        self.data("review", second, "--admit", "--reviewer", "human:alice")
        relation = self.data("relation", "propose", first, "--to", second,
                             "--type", "contradicts",
                             "--proposer", "agent:resolver")["relation"]["id"]
        self.data("relation", "review", relation, "--admit",
                  "--reviewer", "human:alice")
        return evidence, first, second, relation

    def count_events(self):
        return int(subprocess.run(["git", "rev-list", "--count", "refs/proofpress/knowledge"],
                                  cwd=self.repo, text=True, capture_output=True, check=True).stdout)

    def retrieval_envelope(self, locator):
        quote = "liability cap is 1x annual fees"
        return {
            "schema_version": "proofpress/retrieval-evidence/v1",
            "source": {
                "uri": "dataroom/msa.pdf",
                "content_digest": "sha256:" + "a" * 64,
                "media_type": "application/pdf",
            },
            "evidence": {"quote": quote, "locator": locator},
            "retrieval": {
                "adapter": "proofpress.lexical-chunk",
                "version": "1",
                "query": "What is the liability cap?",
                "config_digest": "sha256:" + "b" * 64,
                "selection_reason": "highest lexical overlap",
            },
        }

    def import_retrieval_envelope(self, locator):
        path = self.repo / "retrieval-evidence.json"
        path.write_text(json.dumps(self.retrieval_envelope(locator)))
        return self.data("evidence", "import", str(path))

    def trace_document_at_version(self, version):
        """Write the confidence fixture restamped to `version` under a session identity of its
        own, so several versions can be imported into one repository without colliding."""
        payload = json.loads(TRACE_CONFIDENCE_FIXTURE.read_text())
        session_id = f"{payload['id']}_{version.replace('.', '_')}"
        payload["trace_version"] = version
        payload["id"] = session_id
        for event in payload["events"]:
            event["session_id"] = session_id
        path = self.repo / f"trace-{version}.json"
        path.write_text(json.dumps(payload))
        return path

    def test_import_is_idempotent_and_events_are_git_backed(self):
        first = self.data("evidence", "import", str(FIXTURE))
        count = self.count_events()
        second = self.data("evidence", "import", str(FIXTURE))
        self.assertEqual(first["evidence"], second["evidence"])
        self.assertEqual(self.count_events(), count)
        self.assertTrue(subprocess.run(["git", "show-ref", "--verify", "refs/proofpress/knowledge"],
                                       cwd=self.repo, capture_output=True).returncode == 0)

    def test_trace_session_binds_safe_v2_evidence_without_admission(self):
        first = self.data("evidence", "import", str(TRACE_FIXTURE))
        self.assertEqual(len(first["evidence"]), 3)
        count = self.count_events()
        second = self.data("evidence", "import", str(TRACE_FIXTURE))
        self.assertEqual(first["evidence"], second["evidence"])
        self.assertEqual(self.count_events(), count)
        sys.path.insert(0, str(ROOT))
        from proofpress.kernel import events as knowledge_events
        from proofpress.kernel import operations as knowledge
        previous = Path.cwd()
        try:
            os.chdir(self.repo)
            projection = knowledge.v2_projection()
        finally:
            os.chdir(previous)
        decision = next(row for row in projection["sources"].values()
                        if row["name"] == "trace.decision")
        self.assertEqual(decision["source_protocol"], "TRACE")
        self.assertEqual(decision["source_schema"],
                         json.loads(TRACE_FIXTURE.read_text())["trace_version"])
        self.assertEqual(decision["attributes"]["event"]["disposition"], "accepted")
        self.assertNotIn("secret", json.dumps(projection["sources"]))
        self.assertNotIn("conversion_rate", json.dumps(projection["sources"]))
        self.assertTrue(knowledge_events.verify_history_envelopes(
            knowledge_events.history_envelopes(projection["events"]))["ok"])
        self.assertEqual(projection["conclusions"], {})
        self.assertEqual(projection["admissions"], {})
        self.assertEqual(self.data("context")["knowledge"], [])

    def test_trace_confidence_fixture_is_verifier_compatible_and_evidence_only(self):
        imported = self.data("evidence", "import", str(TRACE_CONFIDENCE_FIXTURE))
        self.assertEqual(len(imported["evidence"]), 1)
        sys.path.insert(0, str(ROOT))
        from proofpress.kernel import events as knowledge_events
        from proofpress.kernel import operations as knowledge
        previous = Path.cwd()
        try:
            os.chdir(self.repo)
            projection = knowledge.v2_projection()
        finally:
            os.chdir(previous)
        decision = next(row for row in projection["sources"].values()
                        if row["name"] == "trace.decision")
        self.assertEqual(decision["source_schema"],
                         json.loads(TRACE_CONFIDENCE_FIXTURE.read_text())["trace_version"])
        self.assertEqual(decision["attributes"]["event"]["confidence"], {
            "interval": {"lower": -29, "upper": 578, "level": 0.9},
            "method": {"name": "paired_bootstrap", "resamples": 5000},
            "sample_size": 8,
            "evidence_digests": {
                "parent_results": "sha256:" + "1" * 64,
                "candidate_results": "sha256:" + "2" * 64,
            },
        })
        self.assertTrue(knowledge_events.verify_history_envelopes(
            knowledge_events.history_envelopes(projection["events"]))["ok"])
        self.assertEqual(projection["conclusions"], {})
        self.assertEqual(projection["admissions"], {})
        self.assertEqual(self.data("context")["knowledge"], [])

    def test_trace_adapter_rejects_unpinned_or_malformed_confidence(self):
        for version in ("0.5.2", "0.6.0"):
            unsupported = json.loads(TRACE_CONFIDENCE_FIXTURE.read_text())
            unsupported["trace_version"] = version
            unsupported_path = self.repo / f"unsupported-{version}.trace.json"
            unsupported_path.write_text(json.dumps(unsupported))
            result = self.cli("evidence", "import", str(unsupported_path), check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsupported TRACE trace_version: " + version, result.stderr)
            self.assertIn("accepted: 0.5.0, 0.5.1", result.stderr)

        malformed = json.loads(TRACE_CONFIDENCE_FIXTURE.read_text())
        malformed["events"][0]["decision"]["confidence"]["interval"]["lower"] = 579
        malformed_path = self.repo / "malformed-confidence.trace.json"
        malformed_path.write_text(json.dumps(malformed))
        result = self.cli("evidence", "import", str(malformed_path), check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("interval.lower must not exceed interval.upper", result.stderr)

    def test_a_released_trace_051_document_imports_and_projects_only_bounded_fields(self):
        """The load-bearing acceptance case: a document TRACE 0.5.1 itself serialized, carrying the
        typed measurement fields 0.5.1 added, reaches the same bounded projection."""
        payload = json.loads(TRACE_V051_FIXTURE.read_text())
        self.assertEqual(payload["trace_version"], "0.5.1")
        confidence = payload["events"][0]["decision"]["confidence"]
        for field in ("statistic", "direction", "estimate", "contract", "unit", "evidence"):
            self.assertIn(field, confidence)
        imported = self.data("evidence", "import", str(TRACE_V051_FIXTURE))
        self.assertEqual(len(imported["imported_evidence"]), 1)
        sys.path.insert(0, str(ROOT))
        from proofpress.kernel import events as knowledge_events
        from proofpress.kernel import operations as knowledge
        previous = Path.cwd()
        try:
            os.chdir(self.repo)
            projection = knowledge.v2_projection()
        finally:
            os.chdir(previous)
        decision = next(row for row in projection["sources"].values()
                        if row["name"] == "trace.decision")
        self.assertEqual(decision["source_schema"], "0.5.1")
        self.assertEqual(decision["attributes"]["event"]["confidence"], {
            "interval": {"lower": 41.25, "upper": 583.75, "level": 0.9},
            "method": {"name": "paired_percentile_bootstrap", "resamples": 5000},
            "sample_size": 8,
            "evidence_digests": {
                "parent-results": "sha256:" + "a" * 64,
                "candidate-results": "sha256:" + "b" * 64,
            },
        })
        rendered = json.dumps(projection["sources"])
        for dropped in ("mean_paired_delta", "rsi-exam-gate/percentile-bootstrap/1",
                        "methods/results/v3/visible.json", "20260902"):
            self.assertNotIn(dropped, rendered)
        self.assertTrue(knowledge_events.verify_history_envelopes(
            knowledge_events.history_envelopes(projection["events"]))["ok"])
        self.assertEqual(projection["conclusions"], {})
        self.assertEqual(projection["admissions"], {})

    def test_an_accepted_051_document_still_meets_the_bounded_confidence_profile(self):
        """Accepting a wire version does not widen the profile. TRACE 0.5.1 makes evidence_digests
        optional and this adapter requires it, and a malformed consumed field is still refused
        under 0.5.1 rather than waved through by the version gate."""
        for label, mutate in (
            ("omitted", lambda c: c.pop("evidence_digests")),
            ("null", lambda c: c.__setitem__("evidence_digests", None)),
            ("empty", lambda c: c.__setitem__("evidence_digests", {})),
        ):
            payload = json.loads(TRACE_V051_FIXTURE.read_text())
            mutate(payload["events"][0]["decision"]["confidence"])
            path = self.repo / f"digests-{label}.trace.json"
            path.write_text(json.dumps(payload))
            result = self.cli("evidence", "import", str(path), check=False)
            self.assertNotEqual(result.returncode, 0, label)
            self.assertIn("evidence_digests must be a non-empty object", result.stderr)

        payload = json.loads(TRACE_V051_FIXTURE.read_text())
        payload["events"][0]["decision"]["confidence"]["interval"]["lower"] = 584.0
        path = self.repo / "malformed-051.trace.json"
        path.write_text(json.dumps(payload))
        result = self.cli("evidence", "import", str(path), check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("interval.lower must not exceed interval.upper", result.stderr)

    def test_trace_allowlist_gate_accepts_every_registered_version(self):
        """Gate coverage, not release conformance: it restamps one document, so it proves
        no registered version is silently dropped, never that a version has a real
        upstream release behind it."""
        sys.path.insert(0, str(ROOT))
        from proofpress.kernel import operations as knowledge
        versions = sorted(knowledge.TRACE_SUPPORTED_VERSIONS)
        self.assertIn("0.5.0", versions)
        self.assertIn("0.5.1", versions)
        for version in versions:
            imported = self.data("evidence", "import", str(self.trace_document_at_version(version)))
            self.assertEqual(len(imported["imported_evidence"]), 1)
        self.assertEqual(len(imported["evidence"]), len(versions))
        previous = Path.cwd()
        try:
            os.chdir(self.repo)
            projection = knowledge.v2_projection()
        finally:
            os.chdir(previous)
        decisions = [row for row in projection["sources"].values()
                     if row["name"] == "trace.decision"]
        self.assertEqual(sorted(row["source_schema"] for row in decisions), versions)
        for row in decisions:
            self.assertEqual(row["attributes"]["event"]["confidence"],
                             decisions[0]["attributes"]["event"]["confidence"])

    def test_restamping_an_imported_session_to_a_new_trace_version_fails_closed(self):
        """Re-emitting an already imported session under a different accepted version keeps its
        session and event identities but changes the recorded content, so the immutable source
        rule refuses it. Widening the allowlist therefore cannot overwrite imported evidence. Any
        rollout that changes the version a producer stamps has to avoid restamping identities that
        are already imported, or define a migration; this records the behavior, not that policy."""
        payload = json.loads(TRACE_V051_FIXTURE.read_text())
        payload["trace_version"] = "0.5.0"
        first = self.repo / "restamp-050.trace.json"
        first.write_text(json.dumps(payload))
        self.data("evidence", "import", str(first))
        result = self.cli("evidence", "import", str(TRACE_V051_FIXTURE), check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("immutable source_recorded conflict", result.stderr)

    def test_trace_version_registry_entries_are_well_formed(self):
        """Shape only. Nothing here can prove a commit is a release commit or that a digest
        belongs to the schema at it; the pull request record carries that verification."""
        sys.path.insert(0, str(ROOT))
        from proofpress.kernel import operations as knowledge
        for version, pin in knowledge.TRACE_SUPPORTED_VERSIONS.items():
            self.assertRegex(version, r"\A\d+\.\d+\.\d+\Z")
            self.assertEqual(sorted(pin), ["commit", "sha256"])
            self.assertRegex(pin["commit"], r"\A[0-9a-f]{40}\Z")
            self.assertRegex(pin["sha256"], r"\Asha256:[0-9a-f]{64}\Z")

    def test_trace_source_conflict_fails_closed(self):
        self.data("evidence", "import", str(TRACE_FIXTURE))
        changed = json.loads(TRACE_FIXTURE.read_text())
        changed["events"][1]["decision"]["disposition"] = "rejected"
        path = self.repo / "changed.trace.json"
        path.write_text(json.dumps(changed))
        result = self.cli("evidence", "import", str(path), check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("immutable source_recorded conflict", result.stderr)

    def test_artifact_evidence_import_is_idempotent(self):
        artifact = self.repo / "task-evidence.json"
        artifact.write_text('{"task":"protect the buyer"}\n')
        first = self.data("evidence", "import", str(artifact))
        count = self.count_events()
        second = self.data("evidence", "import", str(artifact))
        self.assertEqual(first["evidence"], second["evidence"])
        self.assertEqual(self.count_events(), count)

    def test_claim_and_relation_proposals_are_resumable(self):
        evidence, first = self.seed()
        second = self.data("propose", "--statement", "The exception narrows the cap",
                           "--evidence", evidence, "--scope", "msa-negotiation",
                           "--proposer", "agent:runner")["conclusion"]["id"]
        relation_args = ("relation", "propose", second, "--to", first,
                         "--type", "qualifies", "--proposer", "agent:runner")
        relation = self.data(*relation_args)["relation"]["id"]
        count = self.count_events()
        repeated_first = self.seed()[1]
        repeated_relation = self.data(*relation_args)["relation"]["id"]
        self.assertEqual((repeated_first, repeated_relation), (first, relation))
        self.assertEqual(self.count_events(), count)

    def test_retrieval_receipt_binds_locator_and_provenance(self):
        quote = "liability cap is 1x annual fees"
        imported = self.import_retrieval_envelope({
            "kind": "text_span", "start": 120, "end": 120 + len(quote),
            "text_digest": "sha256:" + "c" * 64,
        })
        evidence_id = imported["evidence"][0]
        sys.path.insert(0, str(ROOT))
        from proofpress.kernel import operations as knowledge
        previous = Path.cwd()
        try:
            os.chdir(self.repo)
            evidence = knowledge.v2_projection()["evidence"][evidence_id]
        finally:
            os.chdir(previous)
        self.assertEqual(evidence["kind"], "retrieval_evidence")
        self.assertEqual(evidence["retrieval_receipt"]["locator"]["kind"], "text_span")
        self.assertEqual(evidence["retrieval_receipt"]["retrieval"]["adapter"], "proofpress.lexical-chunk")
        self.assertTrue(knowledge._retrieval_receipt_valid(evidence))
        cid = self.data("propose", "--statement", "The liability cap is 1x annual fees",
                        "--evidence", evidence_id, "--scope", "msa-negotiation",
                        "--proposer", "agent:runner")["conclusion"]["id"]
        self.assertTrue(self.data("evaluate", cid)["checks"]["retrieval_receipts"])

    def test_page_and_section_locators_are_accepted_but_malformed_locators_fail(self):
        page = self.import_retrieval_envelope({
            "kind": "page_span", "page_start": 4, "page_end": 4,
            "page_digest": "sha256:" + "d" * 64,
        })
        self.assertEqual(len(page["evidence"]), 1)
        section = self.import_retrieval_envelope({
            "kind": "section_span", "section_id": "sec-liability",
            "section_digest": "sha256:" + "e" * 64,
            "page_start": 4, "page_end": 5,
        })
        self.assertEqual(len(section["evidence"]), 2)
        bad = self.retrieval_envelope({"kind": "page_span", "page_start": 4,
                                       "page_end": 4})
        path = self.repo / "bad-retrieval-evidence.json"
        path.write_text(json.dumps(bad))
        result = self.cli("evidence", "import", str(path), check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("locator.page_digest", result.stderr)

    def test_admission_and_context_gate(self):
        _, cid = self.seed()
        evaluation = self.data("evaluate", cid)
        self.assertTrue(evaluation["eligible"])
        self.data("review", cid, "--admit", "--reviewer", "human:alice")
        context = self.data("context", "--scope", "msa-negotiation",
                            "--actor", "agent:successor")
        self.assertEqual([row["id"] for row in context["knowledge"]], [cid])
        self.assertEqual(context["blocked"], [])
        self.assertIn("admission_event", context["knowledge"][0]["receipt"])
        sys.path.insert(0, str(ROOT))
        from proofpress.kernel import operations as knowledge
        previous = Path.cwd()
        try:
            os.chdir(self.repo)
            graph = knowledge.graph_v2("msa-negotiation")
        finally:
            os.chdir(previous)
        self.assertTrue({"raw", "evidence", "conclusion", "review", "governed"}
                        <= {node["type"] for node in graph["nodes"]})

    def test_self_approval_rejection_and_supersession_fail_closed(self):
        evidence, old = self.seed()
        blocked = self.cli("review", old, "--admit", "--reviewer", "agent:runner", check=False)
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("self-approve", blocked.stderr)
        new = self.data("propose", "--statement", "The liability cap requires escalation",
                        "--evidence", evidence, "--scope", "msa-negotiation",
                        "--proposer", "agent:runner")["conclusion"]["id"]
        self.data("supersede", old, "--by", new, "--reviewer", "human:alice")
        packet = self.data("context", "--scope", "msa-negotiation")
        reasons = {row["id"]: row["reason"] for row in packet["blocked"]}
        self.assertEqual(reasons[old], "superseded")
        self.data("review", new, "--reject", "--reviewer", "human:alice")
        packet = self.data("context", "--scope", "msa-negotiation")
        reasons = {row["id"]: row["reason"] for row in packet["blocked"]}
        self.assertEqual(reasons[new], "rejected")
        self.assertTrue(all("statement" not in row for row in packet["blocked"]))

    def test_request_changes_is_append_only_and_excluded_from_context(self):
        evidence, cid = self.seed()
        head = subprocess.run(["git", "rev-parse", "refs/proofpress/knowledge"], cwd=self.repo,
                              text=True, capture_output=True, check=True).stdout.strip()
        request_id = "review-request-001"
        result = self.data("review", cid, "--request-changes", "--reviewer", "human:alice",
                           "--note", "Bind the conclusion to the operative schedule.",
                           "--request-id", request_id, "--expected-head", head)
        count_after_review = self.count_events()
        self.assertEqual(result["review"]["decision"], "request_changes")
        self.assertEqual(result["result"]["type"], "conclusion_revision_requested")
        packet = self.data("context", "--scope", "msa-negotiation")
        blocked = next(row for row in packet["blocked"] if row["id"] == cid)
        self.assertEqual((blocked["reason"], blocked["required_action"]),
                         ("needs_revision", "propose_revision"))
        graph = self.data("graph", "--scope", "msa-negotiation")
        conclusion = next(row for row in graph["nodes"] if row["id"] == cid)
        self.assertEqual(conclusion["state"], "needs_revision")
        self.assertEqual(self.count_events(), count_after_review)
        repeated = self.data("review", cid, "--request-changes", "--reviewer", "human:alice",
                             "--note", "Bind the conclusion to the operative schedule.",
                             "--request-id", request_id, "--expected-head", head)
        self.assertTrue(repeated["idempotent"])
        self.assertEqual(self.count_events(), count_after_review)
        stale = self.cli("review", cid, "--reject", "--reviewer", "human:alice",
                         "--request-id", "review-request-002", "--expected-head", head,
                         check=False)
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn("STALE_LEDGER_HEAD", stale.stderr)
        revised = self.data("propose", "--statement", "The operative schedule sets a 1x cap",
                            "--evidence", evidence, "--scope", "msa-negotiation",
                            "--proposer", "agent:runner")["conclusion"]["id"]
        self.assertNotEqual(revised, cid)
        self.assertEqual(next(row for row in self.data("graph", "--scope", "msa-negotiation")["nodes"]
                              if row["id"] == revised)["state"], "needs_review")

    def test_relation_request_changes_uses_the_same_general_review_state(self):
        evidence, first = self.seed()
        second = self.data("propose", "--statement", "The exception narrows the cap",
                           "--evidence", evidence, "--scope", "msa-negotiation",
                           "--proposer", "agent:runner")["conclusion"]["id"]
        relation = self.data("relation", "propose", second, "--to", first,
                             "--type", "qualifies")["relation"]["id"]
        result = self.data("relation", "review", relation, "--request-changes",
                           "--reviewer", "human:alice", "--note", "Clarify directionality.")
        self.assertEqual(result["result"]["type"], "relation_revision_requested")
        graph = self.data("graph", "--scope", "msa-negotiation")
        edge = next(row for row in graph["edges"] if row.get("id") == relation)
        self.assertEqual(edge["state"], "needs_revision")

    def test_general_claim_relations_require_structural_checks_and_human_admission(self):
        evidence, first = self.seed()
        second = self.data("propose", "--statement", "The liability cap excludes fraud",
                           "--evidence", evidence, "--scope", "msa-negotiation",
                           "--proposer", "agent:runner")["conclusion"]["id"]
        relation = self.data("relation", "propose", second, "--to", first,
                             "--type", "qualifies", "--proposer", "agent:runner",
                             "--confidence", "0.82")["relation"]
        evaluation = self.data("relation", "evaluate", relation["id"])
        self.assertTrue(evaluation["eligible"])
        self.assertIn("do not establish semantic correctness", evaluation["semantic_boundary"])
        blocked = self.cli("relation", "review", relation["id"], "--admit",
                           "--reviewer", "agent:runner", check=False)
        self.assertIn("self-approve", blocked.stderr)
        self.data("review", first, "--admit", "--reviewer", "human:alice")
        self.data("review", second, "--admit", "--reviewer", "human:alice")
        self.data("relation", "review", relation["id"], "--admit",
                  "--reviewer", "human:alice")
        packet = self.data("context", "--scope", "msa-negotiation")
        self.assertEqual([row["id"] for row in packet["relations"]], [relation["id"]])
        graph = self.data("graph", "--scope", "msa-negotiation")
        edge = next(row for row in graph["edges"] if row.get("id") == relation["id"])
        self.assertEqual((edge["type"], edge["state"]), ("qualifies", "admitted"))
        policy_dir = self.repo / ".proofpress"; policy_dir.mkdir()
        (policy_dir / "policy.json").write_text(json.dumps({"min_evidence": 2}))
        graph = self.data("graph", "--scope", "msa-negotiation")
        edge = next(row for row in graph["edges"] if row.get("id") == relation["id"])
        self.assertEqual(edge["state"], "unresolved")

    def test_admitted_contradiction_quarantines_context_until_human_resolution(self):
        _, first, second, relation = self.admitted_conflict()
        quarantined = self.data("context", "--scope", "msa-negotiation",
                                "--include-blocked-statements")
        self.assertEqual(quarantined["knowledge"], [])
        self.assertEqual({row["id"] for row in quarantined["blocked"]}, {first, second})
        self.assertTrue(all(row["reason"] == "contradiction_unresolved"
                            for row in quarantined["blocked"]))
        self.assertTrue(all(row["required_action"] == "human_conflict_review"
                            for row in quarantined["blocked"]))

        rereview = self.cli("relation", "review", relation, "--reject",
                            "--reviewer", "human:mallory", check=False)
        self.assertNotEqual(rereview.returncode, 0)
        self.assertIn("may only transition through relation resolve", rereview.stderr)
        bypass = self.cli("supersede", second, "--by", first,
                          "--reviewer", "human:mallory", check=False)
        self.assertNotEqual(bypass.returncode, 0)
        self.assertIn("through relation resolve", bypass.stderr)
        for decision in ("--reject", "--request-changes"):
            lifecycle_bypass = self.cli("review", second, decision,
                                        "--reviewer", "human:mallory", check=False)
            self.assertNotEqual(lifecycle_bypass.returncode, 0)
            self.assertIn("through relation resolve", lifecycle_bypass.stderr)

        resolved = self.data("relation", "resolve", relation, "--disposition", "supersede",
                             "--winner", first, "--reviewer", "human:bob",
                             "--note", "The capped reading is the admitted current interpretation.")
        self.assertEqual(resolved["resolution"]["identity_basis"], "self_asserted")
        context = self.data("context", "--scope", "msa-negotiation")
        self.assertEqual([row["id"] for row in context["knowledge"]], [first])
        self.assertEqual(next(row for row in context["blocked"] if row["id"] == second)["reason"],
                         "superseded")
        receipt = context["knowledge"][0]["receipt"]["conflict_resolutions"][0]
        self.assertEqual((receipt["relation_id"], receipt["winner"], receipt["loser"]),
                         (relation, first, second))
        self.assertEqual(receipt["identity_basis"], "self_asserted")
        self.assertEqual(receipt["resolution_event"], resolved["resolution"]["event_id"])
        self.assertEqual(receipt["supersession_event"], resolved["supersession"]["event_id"])
        raw = self.cli("context", "--scope", "msa-negotiation").stdout
        self.assertNotIn("The liability cap is uncapped", raw)

    def test_contradiction_quarantine_precedes_actor_filtering_and_graph_traversal(self):
        _, first, second, relation = self.admitted_conflict()
        context = self.data("context", "--scope", "msa-negotiation",
                            "--actor", "agent:successor")
        self.assertEqual(context["knowledge"], [])
        blocked = {row["id"]: row for row in context["blocked"]}
        self.assertEqual(blocked[first]["reason"], "contradiction_unresolved")
        self.assertEqual(blocked[second]["reason"], "contradiction_unresolved")
        self.assertEqual(blocked[first]["peer_ids"], [second])
        traversal = self.cli("graph", "--scope", "msa-negotiation",
                             "--seed", first, "--actor", "agent:successor", check=False)
        self.assertNotEqual(traversal.returncode, 0)
        self.assertIn("no eligible seeds", traversal.stderr)
        self.assertIn(relation, blocked[first]["relation_ids"])

    def test_conflict_resolver_allowlist_and_withhold_are_fail_closed(self):
        policy_dir = self.repo / ".proofpress"; policy_dir.mkdir()
        (policy_dir / "policy.json").write_text(json.dumps({
            "conflict_resolvers": ["human:bob"],
        }))
        _, first, second, relation = self.admitted_conflict()
        denied = self.cli("relation", "resolve", relation, "--disposition", "supersede",
                          "--winner", first, "--reviewer", "human:mallory", check=False)
        self.assertNotEqual(denied.returncode, 0)
        self.assertIn("not allowed", denied.stderr)
        bypass = self.cli("supersede", second, "--by", first,
                          "--reviewer", "human:mallory", check=False)
        self.assertNotEqual(bypass.returncode, 0)
        self.data("relation", "resolve", relation, "--disposition", "withhold",
                  "--reviewer", "human:bob", "--note", "No safe winner yet.")
        context = self.data("context", "--scope", "msa-negotiation")
        self.assertEqual(context["knowledge"], [])
        self.assertTrue(all(row["reason"] == "contradiction_withheld"
                            for row in context["blocked"]))

    def test_partial_supersede_resolution_stays_quarantined_and_repairs_on_retry(self):
        _, first, second, relation = self.admitted_conflict()
        sys.path.insert(0, str(ROOT))
        from proofpress.kernel import operations as knowledge
        original_append = knowledge.append_v2

        def fail_supersession(event, existing_rows=None):
            if event.get("type") == "conclusion_superseded":
                raise RuntimeError("simulated interruption")
            return original_append(event, existing_rows)

        previous = Path.cwd()
        try:
            os.chdir(self.repo)
            with patch.object(knowledge, "append_v2", side_effect=fail_supersession):
                with self.assertRaisesRegex(RuntimeError, "simulated interruption"):
                    knowledge.resolve_contradiction_v2(
                        relation, "supersede", "human:bob", first, "Choose the capped reading.")
        finally:
            os.chdir(previous)

        interrupted = self.data("context", "--scope", "msa-negotiation")
        self.assertEqual(interrupted["knowledge"], [])
        self.assertTrue(all(row["reason"] == "contradiction_resolution_incomplete"
                            for row in interrupted["blocked"]))
        repaired = self.data("relation", "resolve", relation, "--disposition", "supersede",
                             "--winner", first, "--reviewer", "human:bob",
                             "--note", "Choose the capped reading.")
        self.assertTrue(repaired["idempotent"])
        final = self.data("context", "--scope", "msa-negotiation")
        self.assertEqual([row["id"] for row in final["knowledge"]], [first])
        self.assertEqual(next(row for row in final["blocked"] if row["id"] == second)["reason"],
                         "superseded")

    def test_relation_semantic_judge_is_advisory_and_policy_enforced(self):
        evidence, first = self.seed()
        second = self.data("propose", "--statement", "The exception narrows the cap",
                           "--evidence", evidence, "--scope", "msa-negotiation",
                           "--proposer", "agent:runner")["conclusion"]["id"]
        relation = self.data("relation", "propose", second, "--to", first,
                             "--type", "qualifies", "--proposer", "agent:runner")["relation"]["id"]
        policy_dir = self.repo / ".proofpress"; policy_dir.mkdir()
        judge_code = ("import json,sys; p=json.load(sys.stdin); "
                      "assert p['schema_version']=='proofpress/relation-judge-request/v1'; "
                      "print(json.dumps({'recommendation':'accept','rationale':'the exception narrows the target claim','adapter':'fixture'}))")
        (policy_dir / "policy.json").write_text(json.dumps({
            "require_judge": True,
            "judge": {"command": [sys.executable, "-c", judge_code], "timeout_seconds": 5},
        }))
        missing = self.cli("relation", "review", relation, "--admit",
                           "--reviewer", "human:alice", check=False)
        self.assertIn("accepting relation judge", missing.stderr)
        recommendation = self.data("relation", "judge", relation)
        self.assertEqual(recommendation["recommendation"], "accept")
        self.data("relation", "review", relation, "--admit", "--reviewer", "human:alice")

    def test_directed_relation_cycles_fail_closed(self):
        evidence, first = self.seed()
        second = self.data("propose", "--statement", "Second conclusion",
                           "--evidence", evidence, "--scope", "msa-negotiation",
                           "--proposer", "agent:runner")["conclusion"]["id"]
        forward = self.data("relation", "propose", first, "--to", second,
                            "--type", "depends_on")["relation"]["id"]
        self.data("relation", "review", forward, "--admit", "--reviewer", "human:alice")
        reverse = self.data("relation", "propose", second, "--to", first,
                            "--type", "depends_on")["relation"]["id"]
        evaluation = self.data("relation", "evaluate", reverse)
        self.assertFalse(evaluation["eligible"])
        self.assertFalse(evaluation["checks"]["acyclic_when_directed"])

    def test_legal_profile_is_optional_and_validated(self):
        evidence = self.data("evidence", "import", str(FIXTURE))["evidence"][0]
        qualifiers = self.repo / "legal.json"
        qualifiers.write_text(json.dumps({"legal": {
            "jurisdiction": "US-DE", "authority": "agreement",
            "citation_locator": "Section 8.1", "effective_from": "2026-01-01",
            "document_type": "stock_purchase_agreement"
        }}))
        row = self.data("propose", "--statement", "The closing condition applies",
                        "--evidence", evidence, "--scope", "deal", "--profile", "legal",
                        "--qualifiers", str(qualifiers))["conclusion"]
        self.assertEqual(row["qualifiers"]["profile"], "proofpress/profile/legal/v1")
        qualifiers.write_text(json.dumps({"legal": {"jurisdiction": "US-DE"}}))
        failed = self.cli("propose", "--statement", "Incomplete legal metadata",
                          "--evidence", evidence, "--scope", "deal", "--profile", "legal",
                          "--qualifiers", str(qualifiers), check=False)
        self.assertIn("legal profile missing", failed.stderr)

    def test_external_judge_is_advisory_and_required_policy_is_enforced(self):
        _, cid = self.seed()
        policy_dir = self.repo / ".proofpress"
        policy_dir.mkdir()
        judge_code = "import json,sys; json.load(sys.stdin); print(json.dumps({'recommendation':'accept','rationale':'policy requirements satisfied','adapter':'fixture'}))"
        (policy_dir / "policy.json").write_text(json.dumps({
            "require_judge": True,
            "judge": {"command": [sys.executable, "-c", judge_code], "timeout_seconds": 5},
        }))
        missing = self.cli("review", cid, "--admit", "--reviewer", "human:alice", check=False)
        self.assertIn("requires an accepting judge", missing.stderr)
        recommendation = self.data("judge", cid)
        self.assertEqual(recommendation["recommendation"], "accept")
        self.data("review", cid, "--admit", "--reviewer", "human:alice")
        self.assertEqual(len(self.data("context", "--scope", "msa-negotiation")["knowledge"]), 1)

    def test_transaction_level_batch_judge_records_individual_receipts(self):
        evidence, first = self.seed()
        second = self.data("propose", "--statement", "The indemnity requires escalation",
                           "--evidence", evidence, "--scope", "msa-negotiation",
                           "--proposer", "agent:runner")["conclusion"]["id"]
        policy_dir = self.repo / ".proofpress"; policy_dir.mkdir()
        judge_code = (
            "import json,sys; p=json.load(sys.stdin); "
            "vs=[{'conclusion_id':x['conclusion']['id'],'recommendation':'accept','risk_level':'low','rationale':'supported'} for x in p['conclusions']]; "
            "print(json.dumps({'verdicts':vs,'adapter':'fixture-batch'}))"
        )
        (policy_dir / "policy.json").write_text(json.dumps({
            "judge": {"command": [sys.executable, "-c", judge_code], "timeout_seconds": 5},
        }))
        result = self.data("judge", "--batch", "--scope", "msa-negotiation")
        self.assertEqual(len(result["verdicts"]), 2)
        self.assertEqual(result["individual_reviews"], [])
        self.assertTrue(all(row["batch_receipt"] == result["batch_receipt"] for row in result["verdicts"]))
        self.assertEqual({row["subject_ref"] for row in result["verdicts"]}, {first, second})

    def test_batch_judge_loads_history_once_and_resumes_without_duplicates(self):
        evidence, first = self.seed()
        second = self.data("propose", "--statement", "The indemnity requires escalation",
                           "--evidence", evidence, "--scope", "msa-negotiation",
                           "--proposer", "agent:runner")["conclusion"]["id"]
        policy_dir = self.repo / ".proofpress"; policy_dir.mkdir()
        judge_code = (
            "import json,sys; p=json.load(sys.stdin); "
            "vs=[{'conclusion_id':x['conclusion']['id'],'recommendation':'accept','risk_level':'low','rationale':'supported'} for x in p['conclusions']]; "
            "print(json.dumps({'verdicts':vs,'adapter':'fixture-batch'}))"
        )
        (policy_dir / "policy.json").write_text(json.dumps({
            "judge": {"command": [sys.executable, "-c", judge_code], "timeout_seconds": 5},
        }))
        self.data("evaluate", first)
        self.data("evaluate", second)
        sys.path.insert(0, str(ROOT))
        from proofpress.kernel import operations as knowledge
        original_run = subprocess.run
        git_commands = []

        def counted_run(args, *positional, **kwargs):
            if args and args[0] == "git": git_commands.append(tuple(args[1:3]))
            return original_run(args, *positional, **kwargs)

        previous = Path.cwd(); os.chdir(self.repo)
        try:
            evaluations_before = len([row for row in knowledge.v2_events()
                                      if row.get("type") == "policy_evaluated"])
            with patch.object(knowledge.subprocess, "run", side_effect=counted_run):
                result = knowledge.judge_batch_v2("msa-negotiation")
            traversals = [command for command in git_commands
                          if command[0] in {"rev-list", "cat-file", "show"}]
            self.assertEqual(traversals.count(("rev-list", "--reverse")), 1)
            self.assertEqual(traversals.count(("cat-file", "--batch")), 1)
            self.assertFalse(any(command[0] == "show" for command in traversals))
            self.assertEqual({row["subject_ref"] for row in result["verdicts"]}, {first, second})
            evaluations_after = len([row for row in knowledge.v2_events()
                                     if row.get("type") == "policy_evaluated"])
            self.assertEqual(evaluations_after, evaluations_before)

            third = knowledge.propose_v2("第三项有界结论 — Unicode survives event loading", [evidence],
                                         "msa-negotiation", "agent:runner")["conclusion"]["id"]
            resumed = knowledge.judge_batch_v2("msa-negotiation")
            self.assertEqual([row["subject_ref"] for row in resumed["verdicts"]], [third])
            idempotent = knowledge.judge_batch_v2("msa-negotiation")
            self.assertTrue(idempotent["idempotent"])
            self.assertIsNone(idempotent["batch_receipt"])
            self.assertEqual(len(idempotent["batch_receipts"]), 2)
            self.assertIn("第三项有界结论", knowledge.v2_projection()["conclusions"][third]["statement"])
            recommendations = [row for row in knowledge.v2_events()
                               if row.get("type") == "judge_recommended"]
            self.assertEqual({row["subject_ref"] for row in recommendations}, {first, second, third})
            self.assertEqual(len(recommendations), 3)
        finally:
            os.chdir(previous)
            sys.path.remove(str(ROOT))

    def test_v1_migration_is_one_way_and_idempotent(self):
        legacy = self.repo / "legacy.json"
        self.cli("knowledge", "ingest", str(FIXTURE), "-o", str(legacy),
                 "--scope", "legacy")
        legacy_data = json.loads(legacy.read_text())
        claim = legacy_data["claims"][0]
        self.cli("knowledge", "review", str(legacy), "--claim", claim["id"],
                 "--decision", "accept", "--reviewer", "human:alice")
        original = legacy.read_bytes()
        self.data("import-v1", str(legacy))
        migrated = self.cli("context", "--scope", "legacy").stdout
        self.assertIn("unresolved", migrated)
        event_types = [json.loads(line)["type"] for line in subprocess.run(
            ["git", "log", "--format=%H", "refs/proofpress/knowledge"], cwd=self.repo,
            text=True, capture_output=True, check=True).stdout.splitlines()
            for line in [subprocess.run(["git", "show", f"{line}:event.json"], cwd=self.repo,
                                        text=True, capture_output=True, check=True).stdout]]
        self.assertIn("conclusion_admitted", event_types)
        self.assertIn("human_reviewed", event_types)
        count = self.count_events()
        self.data("import-v1", str(legacy))
        self.assertEqual(self.count_events(), count)
        self.assertEqual(legacy.read_bytes(), original)

    def test_local_ui_reads_real_ledger_and_rejects_missing_token(self):
        self.seed()
        process = subprocess.Popen([*CLI, "ui", "--no-open", "--port", "0"],
                                   cwd=self.repo, text=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        try:
            line = process.stdout.readline().strip()
            url = line.split(": ", 1)[1]
            body = urlopen(url, timeout=5).read().decode()
            self.assertIn("REVIEW QUEUE", body)
            base, token = url.split("/?token=")
            request = Request(base + "/api/summary", headers={"X-Proofpress-Token": token})
            summary = json.loads(urlopen(request, timeout=5).read())
            self.assertEqual(summary["total"], 1)
            with self.assertRaises(HTTPError) as caught:
                urlopen(base + "/api/summary", timeout=2)
            caught.exception.close()
        finally:
            process.terminate()
            process.communicate(timeout=5)


if __name__ == "__main__":
    unittest.main()

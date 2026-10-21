import unittest
from proofpress.kernel.temporal import in_temporal_window, temporal_window
from test_context_discovery import ContextDiscoveryTests, evidence_payload
from proofpress.hosted import mcp_http


class TemporalContextTests(ContextDiscoveryTests):
    def test_window_is_applied_before_discovery_limit_and_never_uses_import_date(self):
        k = self.kernel_ops
        evidence = k.submit_evidence_v2(evidence_payload())["evidence"][0]
        old = k.propose_v2("Old observation", [evidence], proposer="agent:test", scope="test", qualifiers={"effective_date": "2026-08-01", "imported_at": "2026-10-20T00:00:00Z"})["claim"]
        recent = k.propose_v2("Recent observation", [evidence], proposer="agent:test", scope="test", qualifiers={"effective_date": "2026-10-15", "report_date": "2026-10-19", "original_first_seen_at": "2026-10-19T10:00:00-04:00"})["claim"]
        unknown = k.propose_v2("Undated observation", [evidence], proposer="agent:test", scope="test")["claim"]
        # Synthetic test owner, not a real workspace approval.
        for row in (old, recent, unknown):
            k.review_v2(row["id"], "admit", "human:test")
        query = {"since": "2026-09-20", "until": "2026-10-20", "timezone": "America/New_York"}
        data = k.context_v2(temporal_window=query)
        self.assertEqual([row["id"] for row in data["governed_context"]], [recent["id"]])
        cards = k.discover_context_v2(limit=1, temporal_window=query)["cards"]
        self.assertEqual(cards[0]["id"], recent["id"])
        self.assertEqual(cards[0]["temporal"]["effective_date"], "2026-10-15")
        self.assertEqual(k.context_v2(temporal_window={**query, "known_before": "2026-10-18T00:00:00-04:00"})["governed_context"], [])
        self.assertEqual(len(k.context_v2()["governed_context"]), 3)

    def test_staged_context_keeps_authority_and_time_boundaries(self):
        k = self.kernel_ops
        evidence = k.submit_evidence_v2(evidence_payload())["evidence"][0]
        row = k.propose_v2("Historical candidate", [evidence], proposer="agent:test", scope="test", qualifiers={"effective_date": "2026-10-15", "historical_reconstruction": True})["claim"]
        k.evaluate_v2(row["id"])
        k.append_v2({"type": "judge_recommended", "subject_ref": row["id"],
                     "claim_digest": row["digest"], "policy_digest": k.load_v2_policy()["digest"],
                     "judge": "judge:test", "recommendation": "escalate", "rationale": "Synthetic test advice."})
        query = {"since": "2026-10-01", "until": "2026-10-20"}
        data = k.context_v2(temporal_window=query)
        self.assertEqual(data["governed_context"], [])
        self.assertEqual([x["id"] for x in data["staged_context"]], [row["id"]])
        self.assertEqual(k.context_v2(temporal_window={**query, "known_before": "2026-10-20"})["staged_context"], [])


class TemporalBoundaryTests(unittest.TestCase):
    def test_exclusive_bound_and_calendar_timezone(self):
        w = temporal_window({"since": "2026-11-01", "until": "2026-11-02", "timezone": "America/New_York"})
        for value, expected in [("2026-11-01T03:59:59Z", False), ("2026-11-01T04:00:00Z", True), ("2026-11-02T04:59:59Z", True), ("2026-11-02T05:00:00Z", False)]:
            self.assertEqual(in_temporal_window({"qualifiers": {"effective_date": value}}, w), expected)

    def test_missing_invalid_or_naive_times_never_pass(self):
        w = temporal_window({"since": "2026-10-01"})
        for q in [{}, {"effective_date": "invalid"}, {"effective_date": "2026-10-16T11:00:00"}]:
            self.assertFalse(in_temporal_window({"qualifiers": q, "created_at": "2026-10-20"}, w))
        for invalid in [{}, {"since": "x"}, {"since": "2026-10-20", "until": "2026-10-01"}, {"since": "2026-10-01", "timezone": "invalid"}, {"extra": 1}]:
            with self.assertRaises(ValueError): temporal_window(invalid)

    def test_date_only_first_known_is_conservative(self):
        r = {"qualifiers": {"original_first_seen_at": "2026-10-15"}}
        self.assertFalse(in_temporal_window(r, temporal_window({"known_before": "2026-10-15T12:00:00Z"})))
        self.assertTrue(in_temporal_window(r, temporal_window({"known_before": "2026-10-16"})))

    def test_overflowing_first_known_date_is_excluded(self):
        row = {"qualifiers": {"original_first_seen_at": "9999-12-31"}}
        self.assertFalse(in_temporal_window(row, temporal_window({"known_before": "2026-10-20"})))

    def test_hosted_mcp_publishes_window(self):
        for name in ("proofpress_get_context", "proofpress_discover_context"):
            tool = next(t for t in mcp_http.TOOLS if t["name"] == name)
            self.assertIn("temporal_window", tool["inputSchema"]["properties"])

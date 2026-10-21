import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from proofpress.hosted import capture_policy
from proofpress.hosted.control_plane import HostedAuthError, HostedControlPlane


class PolicyHistoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.control = HostedControlPlane(Path(self.tmp.name) / "history.db")
        self.owner = self.control.bootstrap("workspace:history", "human:owner")["token"]
        self.control.legacy_default_workspace_id = None
        self.agent = self.control.issue_agent_credential(self.owner, "agent:test", "Test")["token"]

    def test_defaults_are_not_fabricated_saved_versions(self):
        for kind in ("capture", "criteria"):
            self.assertEqual(self.control.get_policy_history(self.owner, kind), {
                "kind": kind, "current_version": 0, "versions": [], "next_before_version": None})

    def test_saved_text_metadata_pagination_and_restart(self):
        for version in range(1, 5):
            self.control.save_capture_policy(self.owner, {
                **capture_policy.DEFAULT_SETTINGS, "purpose": f"Capture {version}"}, version - 1)
            self.control.save_review_criteria(self.owner, f"Criteria {version}", version - 1)
        restarted = HostedControlPlane(self.control.database)
        for kind in ("capture", "criteria"):
            page = restarted.get_policy_history(self.owner, kind, limit=2)
            self.assertEqual([row["version"] for row in page["versions"]], [4, 3])
            self.assertEqual(page["current_version"], 4)
            self.assertEqual(page["next_before_version"], 3)
            older = restarted.get_policy_history(self.owner, kind, limit=2, before_version=3)
            self.assertEqual([row["version"] for row in older["versions"]], [2, 1])
            self.assertIsNone(older["next_before_version"])
            for row in page["versions"] + older["versions"]:
                self.assertEqual(row["actor"], "human:owner")
                self.assertIsNotNone(row["updated_at"])
                if kind == "capture":
                    self.assertEqual(row["settings"]["purpose"], f"Capture {row['version']}")
                else:
                    self.assertEqual(row["criteria"], f"Criteria {row['version']}")

    def test_history_is_read_only_workspace_scoped_and_projects_no_provider_configuration(self):
        prior = self.control.save_review_criteria(self.owner, "Original criteria", 0)
        self.control.save_review_policy(self.owner, {**prior["settings"], "zdr": False}, 1)
        with self.control._db() as connection:
            connection.execute("INSERT INTO hosted_workspaces VALUES (?, ?)", ("workspace:other", "test"))
            connection.execute("INSERT INTO hosted_review_policies VALUES (?, ?, ?, ?, ?, ?)", (
                "workspace:other", 99, json.dumps({"criteria": "Other tenant private text"}), "{}", "human:other", "test"))
            connection.execute("INSERT INTO hosted_capture_policies VALUES (?, ?, ?, ?, ?)", (
                "workspace:other", 99, json.dumps(capture_policy.DEFAULT_SETTINGS), "human:other", "test"))
        before = self.control.get_review_policy(self.owner)
        with patch.object(self.control, "_provider_credential", side_effect=AssertionError("No secret access")), \
             patch.object(self.control, "_schedule_judge") as schedule:
            result = self.control.get_policy_history(self.owner, "criteria")
        schedule.assert_not_called()
        self.assertEqual(result["versions"], [
            {"version": row["version"], "actor": "human:owner", "updated_at": row["updated_at"], "criteria": "Original criteria"}
            for row in result["versions"]])
        self.assertEqual([row["version"] for row in result["versions"]], [2, 1])
        self.assertEqual(self.control.get_policy_history(self.owner, "capture")["versions"], [])
        self.assertEqual(before, self.control.get_review_policy(self.owner))

    def test_agent_revocation_and_bounded_queries(self):
        with self.assertRaises(HostedAuthError):
            self.control.get_policy_history(self.agent, "capture")
        for kind, kwargs in [("invalid", {}), ([], {}), ("criteria", {"limit": True}),
                             ("criteria", {"limit": 0}), ("criteria", {"limit": 51}),
                             ("criteria", {"before_version": 0}), ("criteria", {"before_version": "1"})]:
            with self.assertRaises(HostedAuthError):
                self.control.get_policy_history(self.owner, kind, **kwargs)
        reviewer = self.control.issue_reviewer_credential(self.owner, "human:reviewer", "Reviewer")["token"]
        context = self.control.authenticate(reviewer)
        self.control.get_policy_history(context, "criteria")
        self.control.revoke_credential(self.owner, context.credential_id)
        with self.assertRaises(HostedAuthError):
            self.control.get_policy_history(context, "criteria")

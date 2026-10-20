"""Cloud capture guidance stays versioned, workspace-local and owner-controlled."""
import json
from pathlib import Path
import tempfile
import unittest

from proofpress.hosted import capture_policy, mcp_http
from proofpress.hosted.control_plane import HostedAuthError, HostedControlPlane
from proofpress.kernel.contracts import AGENT_OPERATIONS


class CapturePolicyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.database = Path(self.tmp.name) / "hosted.db"
        self.control = HostedControlPlane(self.database)
        self.owner = self.control.bootstrap("workspace:A", "human:owner")["token"]
        self.agent = self.control.issue_agent_credential(self.owner, "agent:A", "Agent A")["token"]
        self.control.legacy_default_workspace_id = None

    def test_defaults_are_readable_over_mcp_before_review_policy_exists(self):
        context = self.control.authenticate(self.agent)
        record = mcp_http.call_tool(self.control, context, "proofpress_get_capture_policy", {}, "http://localhost")
        self.assertEqual(record["version"], 0)
        self.assertTrue(record["policy_digest"].startswith("sha256:"))
        self.assertEqual(record["settings"], capture_policy.DEFAULT_SETTINGS)
        self.assertTrue(record["limits"]["agent_cannot_approve_or_change_policy"])
        self.assertIn("proofpress_get_capture_policy", {tool["name"] for tool in mcp_http.TOOLS})

    def test_owner_saves_versioned_guidance_and_agent_cannot_write(self):
        settings = {**capture_policy.DEFAULT_SETTINGS, "purpose": "Market research"}
        for token in (self.agent, self.control.issue_reviewer_credential(
                self.owner, "human:reviewer", "Reviewer")["token"]):
            with self.assertRaises(HostedAuthError):
                self.control.save_capture_policy(token, settings, 0)
        saved = self.control.save_capture_policy(self.owner, settings, 0)
        self.assertEqual(saved["version"], 1)
        self.assertEqual(saved["actor"], "human:owner")
        with self.assertRaisesRegex(HostedAuthError, "changed"):
            self.control.save_capture_policy(self.owner, settings, 0)
        self.assertEqual(self.control.save_capture_policy(self.owner, settings, 1)["version"], 1)
        restarted = HostedControlPlane(self.database)
        self.assertEqual(restarted.get_capture_policy(self.agent)["settings"], settings)
        with restarted._db() as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM hosted_review_policies").fetchone()[0], 0)

    def test_guidance_cannot_override_fixed_authority_limits(self):
        for settings in ({**capture_policy.DEFAULT_SETTINGS, "limits": {}},
                         {**capture_policy.DEFAULT_SETTINGS, "capture": "anything"},
                         {**capture_policy.DEFAULT_SETTINGS, "capture": []},
                         {**capture_policy.DEFAULT_SETTINGS, "exclude": ["x" * 501]}):
            with self.assertRaises(ValueError):
                self.control.save_capture_policy(self.owner, settings, 0)
        self.assertEqual(self.control.get_capture_policy(self.agent)["version"], 0)

    def test_read_obeys_revocation_and_configuration_permission(self):
        restricted = self.control.issue_agent_credential(
            self.owner, "agent:restricted", "Restricted", permissions={"context.get"})["token"]
        with self.assertRaises(HostedAuthError):
            self.control.get_capture_policy(restricted)
        context = self.control.authenticate(self.agent)
        self.control.revoke_credential(self.owner, context.credential_id)
        with self.assertRaises(HostedAuthError):
            self.control.get_capture_policy(context)

    def test_other_workspace_sees_only_its_own_defaults(self):
        self.control.save_capture_policy(self.owner, {**capture_policy.DEFAULT_SETTINGS,
                                                       "purpose": "Private workspace A purpose"}, 0)
        with self.control._db() as connection:
            connection.execute("INSERT INTO hosted_workspaces VALUES (?, ?)", ("workspace:B", "test"))
            connection.execute("INSERT INTO hosted_principals VALUES (?, ?, ?, ?, ?)",
                               ("workspace:B", "agent:B", "agent", "B", "test"))
            credential_id, token, salt, hashed = self.control._new_credential_values()
            connection.execute("INSERT INTO hosted_credentials VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL)",
                               (credential_id, "workspace:B", "agent:B", "B", salt, hashed,
                                json.dumps(sorted(AGENT_OPERATIONS)), "test"))
            connection.commit()
        record = self.control.get_capture_policy(token)
        self.assertEqual(record["workspace_id"], "workspace:B")
        self.assertEqual(record["version"], 0)
        self.assertNotIn("Private workspace A", json.dumps(record))

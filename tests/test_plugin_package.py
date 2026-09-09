from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "proofpress"
CANONICAL_SKILL = ROOT / ".agents" / "skills" / "proofpress-governed-context"
PACKAGED_SKILL = PLUGIN / "skills" / "proofpress-governed-context"
MANAGED_MCP_URL = "https://proofpress-personal-hosted.onrender.com/mcp"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class ProofpressPluginPackageTests(unittest.TestCase):
    def test_portable_package_has_consistent_manifests(self):
        portable = load_json(PLUGIN / "plugin.json")
        portable_mcp = load_json(PLUGIN / "mcp.json")
        codex = load_json(PLUGIN / ".codex-plugin" / "plugin.json")
        claude = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
        claude_mcp = load_json(PLUGIN / ".mcp.json")

        self.assertEqual(portable["name"], "proofpress")
        self.assertEqual(portable["version"], "0.1.0")
        self.assertEqual(codex["name"], portable["name"])
        self.assertEqual(codex["version"], portable["version"])
        self.assertEqual(claude["name"], portable["name"])
        self.assertEqual(claude["version"], portable["version"])
        self.assertEqual(
            portable_mcp["mcpServers"]["proofpress"],
            {"type": "streamable-http", "url": MANAGED_MCP_URL},
        )
        self.assertEqual(
            claude_mcp["mcpServers"]["proofpress"],
            {"type": "http", "url": MANAGED_MCP_URL},
        )
        self.assertEqual(
            codex["interface"]["defaultPrompt"],
            ["Retrieve eligible Proofpress governed context for this task."],
        )
        interface = portable["extensions"]["com.openai"]["interface"]
        self.assertEqual(interface["privacyPolicyURL"].split("/")[-1], "PLUGIN_PRIVACY.md")
        self.assertEqual(interface["termsOfServiceURL"].split("/")[-1], "PLUGIN_TERMS.md")
        self.assertEqual(interface["logo"], "./assets/logo-on-light.svg")
        self.assertEqual(interface["screenshots"], ["./assets/owner-home.png"])
        self.assertTrue((PLUGIN / "LICENSE").is_file())
        self.assertIn("Initial public package release", (PLUGIN / "CHANGELOG.md").read_text(encoding="utf-8"))

    def test_marketplaces_expose_the_same_plugin(self):
        codex_marketplace = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
        claude_marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")

        self.assertEqual(codex_marketplace["name"], "proofpress-plugins")
        codex_entry = codex_marketplace["plugins"][0]
        self.assertEqual(codex_entry["name"], "proofpress")
        self.assertEqual(codex_entry["source"]["path"], "./plugins/proofpress")
        self.assertEqual(codex_entry["policy"], {"installation": "AVAILABLE", "authentication": "ON_USE"})
        self.assertEqual(claude_marketplace["name"], "proofpress-plugins")
        self.assertEqual(claude_marketplace["plugins"][0]["name"], "proofpress")
        self.assertEqual(claude_marketplace["plugins"][0]["source"], "./plugins/proofpress")

    def test_packaged_skill_and_assets_match_the_canonical_source(self):
        for relative in (
            Path("SKILL.md"),
            Path("assets/context-policy.yaml"),
            Path("assets/judge-criteria.md"),
            Path("scripts/initialize_policy.py"),
        ):
            self.assertEqual(
                (PACKAGED_SKILL / relative).read_bytes(),
                (CANONICAL_SKILL / relative).read_bytes(),
                relative.as_posix(),
            )

    def test_package_has_no_hooks_or_mcp_credentials(self):
        self.assertFalse((PLUGIN / "hooks").exists())
        for path in (PLUGIN / "mcp.json", PLUGIN / ".mcp.json"):
            server = load_json(path)["mcpServers"]["proofpress"]
            self.assertNotIn("headers", server)
            self.assertNotIn("env", server)
            self.assertNotIn("token", json.dumps(server).lower())
        readme = (PLUGIN / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("cannot approve", readme)
        self.assertIn("or administer credentials", readme)

    def test_policy_initializer_previews_creates_and_never_overwrites(self):
        script = PACKAGED_SKILL / "scripts" / "initialize_policy.py"
        template = (PACKAGED_SKILL / "assets" / "context-policy.yaml").read_text(encoding="utf-8")

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            command = [sys.executable, str(script), "--workspace", str(workspace)]
            preview = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertEqual(preview.returncode, 0, preview.stderr)
            self.assertIn("Preview only", preview.stdout)
            target = workspace / ".proofpress" / "context-policy.yaml"
            self.assertFalse(target.exists())

            created = subprocess.run(command + ["--apply"], text=True, capture_output=True, check=False)
            self.assertEqual(created.returncode, 0, created.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), template)

            unchanged = subprocess.run(command + ["--apply"], text=True, capture_output=True, check=False)
            self.assertEqual(unchanged.returncode, 0, unchanged.stderr)
            self.assertIn("already exists", unchanged.stdout)
            self.assertEqual(target.read_text(encoding="utf-8"), template)

            target.write_text("schema_version: unknown/v9\n", encoding="utf-8")
            blocked = subprocess.run(command + ["--apply"], text=True, capture_output=True, check=False)
            self.assertEqual(blocked.returncode, 2)
            self.assertIn("blocked", blocked.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), "schema_version: unknown/v9\n")

            target.write_text(
                "schema_version: proofpress/context-policy/v1alpha1 trailing-text\n",
                encoding="utf-8",
            )
            malformed = subprocess.run(command + ["--apply"], text=True, capture_output=True, check=False)
            self.assertEqual(malformed.returncode, 2)
            self.assertIn("blocked", malformed.stderr)
            self.assertEqual(
                target.read_text(encoding="utf-8"),
                "schema_version: proofpress/context-policy/v1alpha1 trailing-text\n",
            )

            target.write_text(
                "schema_version: proofpress/context-policy/v1alpha1\n"
                "schema_version: unknown/v9\n",
                encoding="utf-8",
            )
            duplicate = subprocess.run(command + ["--apply"], text=True, capture_output=True, check=False)
            self.assertEqual(duplicate.returncode, 2)
            self.assertIn("blocked", duplicate.stderr)
            self.assertEqual(
                target.read_text(encoding="utf-8"),
                "schema_version: proofpress/context-policy/v1alpha1\n"
                "schema_version: unknown/v9\n",
            )

    def test_policy_initializer_rejects_a_symlinked_policy_directory(self):
        script = PACKAGED_SKILL / "scripts" / "initialize_policy.py"

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            outside = Path(tmp) / "outside"
            workspace.mkdir()
            outside.mkdir()
            (workspace / ".proofpress").symlink_to(outside, target_is_directory=True)

            blocked = subprocess.run(
                [sys.executable, str(script), "--workspace", str(workspace), "--apply"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(blocked.returncode, 2)
            self.assertIn("symbolic link", blocked.stderr)
            self.assertFalse((outside / "context-policy.yaml").exists())

    def test_policy_initializer_rejects_a_special_policy_file(self):
        script = PACKAGED_SKILL / "scripts" / "initialize_policy.py"

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            policy_dir = workspace / ".proofpress"
            policy_dir.mkdir()
            os.mkfifo(policy_dir / "context-policy.yaml")

            blocked = subprocess.run(
                [sys.executable, str(script), "--workspace", str(workspace), "--apply"],
                text=True,
                capture_output=True,
                check=False,
                timeout=2,
            )
            self.assertEqual(blocked.returncode, 2)
            self.assertIn("safe regular file", blocked.stderr)

    def test_policy_initializer_blocks_non_utf8_policy(self):
        script = PACKAGED_SKILL / "scripts" / "initialize_policy.py"

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            policy_dir = workspace / ".proofpress"
            policy_dir.mkdir()
            (policy_dir / "context-policy.yaml").write_bytes(b"schema_version: \xff\n")

            blocked = subprocess.run(
                [sys.executable, str(script), "--workspace", str(workspace), "--apply"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(blocked.returncode, 2)
            self.assertIn("not valid UTF-8", blocked.stderr)

    def test_documented_manual_install_and_privacy_boundary_are_non_overwriting(self):
        remote_mcp = (ROOT / "docs" / "REMOTE_MCP.md").read_text(encoding="utf-8")
        privacy = (ROOT / "docs" / "PLUGIN_PRIVACY.md").read_text(encoding="utf-8")

        self.assertEqual(remote_mcp.count('assets/context-policy.yaml -o "$skill_root/assets/context-policy.yaml"'), 3)
        self.assertEqual(remote_mcp.count('scripts/initialize_policy.py -o "$skill_root/scripts/initialize_policy.py"'), 3)
        self.assertIn("Do not substitute a path-based shell script for that helper.", remote_mcp)
        self.assertNotIn("mktemp .proofpress", remote_mcp)
        self.assertNotIn('ln "$temporary_policy"', remote_mcp)
        self.assertIn("Installing the plugin does not itself transfer workspace content", privacy)
        self.assertIn("may use the configured MCP", privacy)
        self.assertIn("task summary", privacy)
        self.assertIn("output references, content digests", privacy)
        self.assertIn("observation kinds, sources, meanings", privacy)
        self.assertIn("run start/finish/read", privacy)
        self.assertNotIn("only when a user directs it to use", privacy)

    def test_policy_template_carries_no_secrets_or_owner_permissions(self):
        template = (PACKAGED_SKILL / "assets" / "context-policy.yaml").read_text(encoding="utf-8").lower()

        for sensitive_field in ("api_key:", "token:", "password:", "owner_permissions:"):
            self.assertNotIn(sensitive_field, template)
        self.assertIn("agent_may_not_self_approve: true", template)
        self.assertIn("owner_or_recovery_credentials_forbidden: true", template)

    def test_skill_uses_the_current_claim_proposal_operation(self):
        skill = (PACKAGED_SKILL / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("`claim.propose`", skill)
        self.assertNotIn("`conclusion.propose`", skill)
        self.assertIn("reports that its platform safeguards are\n   unavailable", skill)


if __name__ == "__main__":
    unittest.main()

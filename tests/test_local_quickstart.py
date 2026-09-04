import json
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from proofpress import quickstart


CLI = (sys.executable, "-m", "proofpress.cli")
ROOT = Path(__file__).resolve().parents[1]


class LocalQuickstartTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *args, check=True):
        environment = dict(os.environ)
        environment["PYTHONPATH"] = str(ROOT / "src")
        return subprocess.run(
            [*CLI, *args], cwd=self.root, text=True, capture_output=True,
            check=check, env=environment,
        )

    def test_noninteractive_quickstart_creates_isolated_local_mcp_demo(self):
        completed = self.cli("quickstart", "--no-browser")
        result = json.loads(completed.stdout)
        workspace = self.root / "proofpress-demo"

        self.assertEqual(Path(result["workspace"]), workspace.resolve())
        self.assertTrue(result["synthetic"])
        self.assertEqual(result["scope"], "demo")
        self.assertFalse(result["review"]["launched"])
        self.assertIn(str(workspace.resolve()), result["review"]["command"])
        self.assertTrue((workspace / ".git").is_dir())
        self.assertTrue((workspace / "proofpress-mcp.json").is_file())

        config = result["mcp_config"]["mcpServers"]["proofpress"]
        self.assertEqual(
            config["env"],
            {"PROOFPRESS_MCP_PRINCIPAL": "agent:quickstart"},
        )
        self.assertIn(str(workspace.resolve()), config["args"])
        self.assertNotIn("base-url", " ".join(config["args"]))
        self.assertNotIn("token", json.dumps(config).lower())
        self.assertEqual(
            json.loads((workspace / "proofpress-mcp.json").read_text()),
            result["mcp_config"],
        )

        context = subprocess.run(
            [*CLI, "context", "--scope", "demo", "--actor", "agent:test"],
            cwd=workspace, text=True, capture_output=True, check=True,
        )
        projected = json.loads(context.stdout)
        self.assertEqual(len(projected["knowledge"]), 1)
        self.assertEqual(len(projected["blocked"]), 2)

    def test_existing_target_is_refused_without_touching_it(self):
        workspace = self.root / "occupied"
        workspace.mkdir()
        marker = workspace / "keep.txt"
        marker.write_text("keep", encoding="utf-8")

        failed = self.cli(
            "quickstart", "--workspace", str(workspace), check=False
        )

        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("quickstart workspace already exists", failed.stderr)
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep")
        self.assertFalse((workspace / ".git").exists())

    def test_ui_mode_serves_from_new_workspace_without_opening_browser(self):
        workspace = self.root / "ui-demo"
        observed = {}

        def fake_serve(port, scope, open_browser):
            observed.update(
                port=port,
                scope=scope,
                open_browser=open_browser,
                cwd=Path.cwd(),
            )

        with patch.object(quickstart, "serve_ui", side_effect=fake_serve):
            output = io.StringIO()
            with patch.object(sys, "stdout", output):
                quickstart.main([
                    "--workspace", str(workspace), "--ui", "--no-browser",
                    "--port", "7441",
                ])

        result = json.loads(output.getvalue())

        self.assertEqual(observed["port"], 7441)
        self.assertEqual(observed["scope"], "demo")
        self.assertFalse(observed["open_browser"])
        self.assertEqual(observed["cwd"], workspace.resolve())
        self.assertTrue(result["review"]["launched"])


if __name__ == "__main__":
    unittest.main()

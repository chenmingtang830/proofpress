import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
CLI = (sys.executable, "-m", "proofpress.cli")
EXAMPLE = ROOT / "examples" / "portable-handoff"
SCREENSHOT_SCRIPT = ROOT / "scripts" / "generate_quickstart_screenshots.py"


class QuickstartExampleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        subprocess.run(
            ["git", "init", "-q"], cwd=self.root, check=True, capture_output=True
        )
        subprocess.run(
            ["git", "config", "user.name", "Proofpress Quickstart"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "quickstart@example.invalid"],
            cwd=self.root,
            check=True,
        )

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *args, check=True):
        return subprocess.run(
            [*CLI, *args],
            cwd=self.root,
            text=True,
            capture_output=True,
            check=check,
        )

    def copy(self, filename):
        shutil.copy2(EXAMPLE / filename, self.root / filename)

    def test_markdown_and_html_carry_two_verified_versions(self):
        for filename in ("strategy.md", "strategy.html"):
            with self.subTest(filename=filename):
                self.copy(filename)

                inspected = json.loads(
                    self.cli("inspect", filename, "--json").stdout
                )
                self.assertEqual(inspected["status"], "ok")
                self.assertEqual(inspected["policy"], "portable")
                self.assertEqual(inspected["versions"], 2)

                self.cli("import", filename)
                history = json.loads(self.cli("log", filename, "--json").stdout)
                self.assertEqual(len(history), 2)
                self.assertEqual(history[0]["stats"], {"modified": 3})
                self.assertIn("3 blocks modified", self.cli("diff", filename).stdout)
                self.assertIn("3 verified", self.cli("verify", filename).stdout)

    def test_docx_sidecar_verifies_and_detects_content_change(self):
        self.copy("proposal.docx")
        self.copy("proposal.provenance.json")

        verified = json.loads(
            self.cli(
                "provenance",
                "verify",
                "proposal.docx",
                "--evidence",
                "proposal.provenance.json",
                "--json",
            ).stdout
        )
        self.assertEqual(verified["status"], "verified")
        self.assertEqual(verified["level"], "semantic")
        self.assertEqual(verified["adapter"], "proofpress.ooxml-word")
        self.assertEqual(verified["provider"], "proofpress.ooxml-semantic")

        document = self.root / "proposal.docx"
        with zipfile.ZipFile(document) as source:
            parts = {name: source.read(name) for name in source.namelist()}
        parts["word/document.xml"] = parts["word/document.xml"].replace(
            b"focused community garden planting day",
            b"unreviewed community garden planting day",
        )
        with zipfile.ZipFile(document, "w", zipfile.ZIP_DEFLATED) as target:
            for name, payload in parts.items():
                target.writestr(name, payload)

        failed = self.cli(
            "provenance",
            "verify",
            "proposal.docx",
            "--evidence",
            "proposal.provenance.json",
            check=False,
        )
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("provenance failed", failed.stdout)

    def test_cli_screenshots_match_current_output_and_hide_local_paths(self):
        subprocess.run(
            ["python3", str(SCREENSHOT_SCRIPT), "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        widths = set()
        for screenshot in (ROOT / "assets" / "quickstart").glob("*.svg"):
            payload = screenshot.read_text(encoding="utf-8")
            self.assertNotIn(str(ROOT), payload)
            self.assertNotIn("proofpress-quickstart-", payload)
            self.assertNotIn("\x1b", payload)
            self.assertRegex(
                payload,
                r'fill="#(?:5FB3C4|6FBF8E|C87E82|D7B56D|787B87)"',
            )
            widths.add(int(re.search(r'<svg[^>]+ width="(\d+)"', payload).group(1)))
        self.assertEqual(len(widths), 1)
        self.assertGreater(next(iter(widths)), 1120)

    def test_legacy_index_keeps_the_portable_quickstart_discoverable(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        legacy_index = (ROOT / "docs" / "legacy" / "README.md").read_text(
            encoding="utf-8"
        )
        for filename in (
            "strategy.md",
            "strategy.html",
            "proposal.docx",
            "proposal.provenance.json",
        ):
            self.assertTrue((EXAMPLE / filename).is_file())
        self.assertIn("0.6 compatibility window", readme)
        self.assertIn("Portable handoff example", legacy_index)


if __name__ == "__main__":
    unittest.main()

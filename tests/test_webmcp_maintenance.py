import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


coverage = load_script("check_webmcp_coverage")
patches = load_script("validate_webmcp_patch")


class WebmcpMaintenanceTests(unittest.TestCase):
    def test_new_changed_and_deleted_surface_files_require_review(self):
        import json
        manifest = json.loads((ROOT / coverage.MANIFEST).read_text())
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for source in coverage.snapshot(ROOT):
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((ROOT / source).read_bytes())
            manifest["sources"] = coverage.snapshot(root)
            self.assertEqual(coverage.check(root, manifest), [])
            path = root / "web/owner/src/new-feature.tsx"
            path.write_text("export const feature = 'new user behavior';")
            self.assertTrue(any("new-feature.tsx" in error for error in coverage.check(root, manifest)))
            path.unlink()
            existing = root / "web/owner/src/main.tsx"
            existing.write_text(existing.read_text() + "\n// changed workflow\n")
            self.assertTrue(any("main.tsx" in error for error in coverage.check(root, manifest)))
            existing.unlink()
            self.assertTrue(any("main.tsx" in error for error in coverage.check(root, manifest)))

    def test_allowed_paths_exclude_workflows_guards_secrets_and_authorization_backend(self):
        for path in (".github/workflows/ci.yml", "scripts/validate_webmcp_patch.py",
                     "web/owner/package.json", "src/proofpress/hosted/service.py", ".env",
                     "web/owner/src/../../package.json", "web/owner/src/.secret.ts"):
            self.assertFalse(patches.allowed(path), path)
        self.assertTrue(patches.allowed("web/owner/src/webmcp.ts"))
        self.assertTrue(patches.allowed("web/owner/src/components/new-tool.tsx"))

    def test_patch_can_be_applied_without_running_any_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                            "commit", "--allow-empty", "-qm", "Synthetic base"], check=True)
            path = root / "candidate.patch"
            path.write_text("diff --git a/web/owner/src/tool.ts b/web/owner/src/tool.ts\n"
                            "new file mode 100644\n--- /dev/null\n+++ b/web/owner/src/tool.ts\n"
                            "@@ -0,0 +1 @@\n+throw new Error('must not execute');\n")
            result = subprocess.run(["python3", str(ROOT / "scripts/validate_webmcp_patch.py"), str(path)], cwd=root, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertIn("must not execute", (root / "web/owner/src/tool.ts").read_text())
            for bad_path, mode in ((".github/workflows/evil.yml", "100644"), ("web/owner/src/link.ts", "120000")):
                path.write_text("diff --git a/" + bad_path + " b/" + bad_path + "\nnew file mode " + mode
                                + "\n--- /dev/null\n+++ b/" + bad_path + "\n@@ -0,0 +1 @@\n+bad\n")
                result = subprocess.run(["python3", str(ROOT / "scripts/validate_webmcp_patch.py"), str(path)], cwd=root, capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((root / bad_path).exists())


if __name__ == "__main__":
    unittest.main()

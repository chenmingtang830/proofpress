#!/usr/bin/env python3
"""Apply a bounded generated patch without executing its contents."""
from pathlib import Path, PurePosixPath
import subprocess
import sys

MAX_BYTES = 3 * 1024 * 1024
EXACT = {
    "docs/WEBMCP.md", "web/owner/webmcp-coverage.json",
    "web/owner/scripts/webmcp-smoke.mjs", "tests/test_webmcp_owner_surface.py",
    "src/proofpress/hosted/static/index.html",
}


def allowed(path):
    parts = PurePosixPath(path).parts
    if not parts or any(part in {".", ".."} or part.startswith(".") for part in parts):
        return False
    if path in EXACT:
        return True
    return (path.startswith("web/owner/src/") and Path(path).suffix in {".ts", ".tsx"}
            or path.startswith("src/proofpress/hosted/static/assets/")
            and Path(path).suffix in {".js", ".css"})


def apply_patch(patch):
    if not 0 < patch.stat().st_size <= MAX_BYTES:
        raise ValueError("Patch must be non-empty and at most 3 MiB")
    result = subprocess.run(["git", "apply", "--numstat", "-z", str(patch)], check=True, capture_output=True)
    paths = []
    for entry in result.stdout.split(b"\0"):
        if not entry:
            continue
        fields = entry.decode("utf-8").split("\t", 2)
        if len(fields) != 3 or not allowed(fields[2]):
            raise ValueError("Generated patch changes an unapproved path or uses a rename")
        paths.append(fields[2])
    if not paths or len(paths) > 50:
        raise ValueError("Patch must change between 1 and 50 allowed files")
    # Git rejects traversal and symbolic-link targets. Reject new symlinks,
    # submodules and executable modes before writing any file.
    for line in patch.read_text().splitlines():
        if line.startswith(("new mode ", "new file mode ")) and line.rsplit(" ", 1)[-1] != "100644":
            raise ValueError("Generated files must be regular non-executable files")
    subprocess.run(["git", "apply", "--index", "--check", str(patch)], check=True)
    subprocess.run(["git", "apply", "--index", str(patch)], check=True)
    print(f"Applied bounded patch ({len(paths)} files); no patch content was executed.")


if __name__ == "__main__":
    apply_patch(Path(sys.argv[1]).resolve())

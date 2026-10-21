#!/usr/bin/env python3
"""Detect surface drift; a fingerprint is an audit reminder, never semantic proof."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "web/owner/webmcp-coverage.json"



def snapshot(root):
    sources = [path for path in (root / "web/owner/src").rglob("*")
               if path.is_file() and path.suffix in {".ts", ".tsx", ".css"}
               and ".test." not in path.name]
    sources.extend((root / "src/proofpress/hosted").rglob("*.py"))
    return {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(sources)}


def check(root, manifest, allow_stale_sources=False):
    errors = []
    actual = snapshot(root)
    saved = manifest.get("sources", {})
    drift = sorted(path for path in set(actual) | set(saved) if actual.get(path) != saved.get(path))
    if drift:
        message = "Changed surfaces need a WebMCP audit: " + ", ".join(drift)
        if allow_stale_sources:
            print("::warning::" + message)
        else:
            errors.append(message)
    source = (root / "web/owner/src/webmcp.ts").read_text()
    names = re.findall(r'name:\s*"([a-z_]+)"', source)
    declared = [name for item in manifest.get("capabilities", []) for name in item.get("tools", [])]
    if len(names) != len(set(names)):
        errors.append("Duplicate WebMCP registration names")
    if set(names) != set(declared):
        errors.append("Tool inventory differs from capability map: " + ", ".join(sorted(set(names) ^ set(declared))))
    if not manifest.get("audit_note", "").strip():
        errors.append("Record the semantic coverage review and remaining exceptions in audit_note")
    for capability in manifest.get("capabilities", []):
        if not capability.get("capability") or not capability.get("authority"):
            errors.append("Every capability needs a name and authority boundary")
    if not manifest.get("human_only"):
        errors.append("Document the human-only surfaces and their reasons")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="Refresh fingerprints after a semantic audit")
    parser.add_argument("--audit-note", help="What was reviewed; explain new tools or why none are needed")
    parser.add_argument("--allow-stale-sources", action="store_true", help="Warn on source drift; still fail invalid inventory (CI before post-main maintenance)")
    args = parser.parse_args()
    manifest = json.loads((ROOT / MANIFEST).read_text())
    if args.refresh:
        if not args.audit_note or len(args.audit_note.strip()) < 20:
            parser.error("--refresh requires a substantive --audit-note after inspecting the changed workflow")
        manifest["sources"] = snapshot(ROOT)
        manifest["audit_note"] = args.audit_note.strip()
        (ROOT / MANIFEST).write_text(json.dumps(manifest, indent=2) + "\n")
    errors = check(ROOT, manifest, args.allow_stale_sources)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print("Use .agents/skills/proofpress-webmcp-maintenance/SKILL.md before refreshing.", file=sys.stderr)
        return 1
    print("WebMCP inventory and surface fingerprints are current; semantic completeness still requires review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

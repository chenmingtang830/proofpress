#!/usr/bin/env python3
"""Safely preview or initialize a repository Proofpress context policy."""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path


EXPECTED_SCHEMA = "proofpress/context-policy/v1alpha1"


def policy_paths(workspace: Path) -> tuple[Path, Path]:
    skill_root = Path(__file__).resolve().parents[1]
    return (
        workspace.resolve() / ".proofpress" / "context-policy.yaml",
        skill_root / "assets" / "context-policy.yaml",
    )


def schema_version(content: str) -> str | None:
    match = re.search(r"^schema_version:\s*([^#\s]+)", content, re.MULTILINE)
    return match.group(1) if match else None


def preview(path: Path, template: str) -> str:
    return "".join(
        difflib.unified_diff(
            [],
            template.splitlines(keepends=True),
            fromfile="/dev/null",
            tofile=str(path),
        )
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Preview or initialize a Proofpress repository policy without overwriting one."
    )
    parser.add_argument("--workspace", default=".", type=Path)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create the template only when the target policy is absent.",
    )
    args = parser.parse_args(argv)

    target, template_path = policy_paths(args.workspace)
    template = template_path.read_text(encoding="utf-8")
    if schema_version(template) != EXPECTED_SCHEMA:
        print(f"Template schema is invalid: {template_path}", file=sys.stderr)
        return 2

    if target.exists():
        existing = target.read_text(encoding="utf-8")
        version = schema_version(existing)
        if version != EXPECTED_SCHEMA:
            observed = version or "missing"
            print(
                f"Policy initialization blocked: {target} has schema_version {observed!r}; "
                "no file was changed.",
                file=sys.stderr,
            )
            return 2
        print(f"Policy already exists: {target}; no file was changed.")
        return 0

    if not args.apply:
        sys.stdout.write(preview(target, template))
        print("Preview only. Re-run with --apply after explicit user direction to create this file.")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(template, encoding="utf-8")
    print(f"Created {target}. Review, narrow, version, and commit this repository policy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

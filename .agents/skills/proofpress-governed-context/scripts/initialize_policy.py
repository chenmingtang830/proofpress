#!/usr/bin/env python3
"""Safely preview or initialize a repository Proofpress context policy."""

from __future__ import annotations

import argparse
import difflib
import os
import re
import secrets
import stat
import sys
from pathlib import Path


EXPECTED_SCHEMA = "proofpress/context-policy/v1alpha1"


def policy_paths(workspace: Path) -> tuple[Path, Path]:
    skill_root = Path(__file__).resolve().parents[1]
    return (
        workspace.resolve() / ".proofpress" / "context-policy.yaml",
        skill_root / "assets" / "context-policy.yaml",
    )


class PolicyPathError(Exception):
    """The policy path is unsafe or cannot be opened without following links."""


def open_policy_directory(workspace: Path, *, create: bool) -> int | None:
    """Open `.proofpress` without following a symlink in the target repository."""
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise PolicyPathError("this platform cannot safely initialize a policy")

    root = workspace.resolve()
    root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
    try:
        if create:
            try:
                os.mkdir(".proofpress", mode=0o755, dir_fd=root_fd)
            except FileExistsError:
                pass
        try:
            return os.open(
                ".proofpress",
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=root_fd,
            )
        except FileNotFoundError:
            return None
        except OSError as error:
            raise PolicyPathError(".proofpress is not a safe directory or is a symbolic link") from error
    finally:
        os.close(root_fd)


def read_existing_policy(policy_fd: int) -> str | None:
    """Read a regular policy file through an already-open policy directory."""
    if not hasattr(os, "O_NONBLOCK"):
        raise PolicyPathError("this platform cannot safely inspect policy file types")
    try:
        target_fd = os.open(
            "context-policy.yaml",
            os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
            dir_fd=policy_fd,
        )
    except FileNotFoundError:
        return None
    except OSError as error:
        raise PolicyPathError("context-policy.yaml is not a safe regular file") from error
    if not stat.S_ISREG(os.fstat(target_fd).st_mode):
        os.close(target_fd)
        raise PolicyPathError("context-policy.yaml is not a safe regular file")
    with os.fdopen(target_fd, "r", encoding="utf-8") as file:
        return file.read()


def create_policy_exclusively(policy_fd: int, template: str) -> bool:
    """Publish a complete policy once, without exposing a partial target file."""
    temporary_name = f".context-policy-{secrets.token_hex(16)}.tmp"
    target_fd = os.open(
        temporary_name,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
        0o600,
        dir_fd=policy_fd,
    )
    try:
        with os.fdopen(target_fd, "w", encoding="utf-8") as file:
            file.write(template)
            file.flush()
            os.fsync(file.fileno())
        try:
            os.link(
                temporary_name,
                "context-policy.yaml",
                src_dir_fd=policy_fd,
                dst_dir_fd=policy_fd,
                follow_symlinks=False,
            )
        except FileExistsError:
            return False
        return True
    finally:
        try:
            os.unlink(temporary_name, dir_fd=policy_fd)
        except FileNotFoundError:
            pass


def schema_version(content: str) -> str | None:
    matches = list(
        re.finditer(
            r"^schema_version:\s*([^#\r\n]+?)(?:\s+#.*)?\s*$",
            content,
            re.MULTILINE,
        )
    )
    if len(matches) != 1:
        return None
    return matches[0].group(1).strip()


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

    try:
        policy_fd = open_policy_directory(args.workspace, create=args.apply)
        existing = read_existing_policy(policy_fd) if policy_fd is not None else None
    except (OSError, PolicyPathError) as error:
        print(f"Policy initialization blocked: {error}; no file was changed.", file=sys.stderr)
        return 2

    if existing is not None:
        assert policy_fd is not None
        os.close(policy_fd)
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
        if policy_fd is not None:
            os.close(policy_fd)
        sys.stdout.write(preview(target, template))
        print("Preview only. Re-run with --apply after explicit user direction to create this file.")
        return 0

    assert policy_fd is not None
    try:
        created = create_policy_exclusively(policy_fd, template)
        if not created:
            existing = read_existing_policy(policy_fd)
            if existing is None:
                raise PolicyPathError("policy appeared but could not be read safely")
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
    except (OSError, PolicyPathError) as error:
        print(f"Policy initialization blocked: {error}; no file was changed.", file=sys.stderr)
        return 2
    finally:
        os.close(policy_fd)
    print(f"Created {target}. Review, narrow, version, and commit this repository policy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

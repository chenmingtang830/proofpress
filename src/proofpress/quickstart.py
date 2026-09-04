"""Isolated local first-run workspace for Proofpress."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import sys
from typing import Iterator

from proofpress.kernel.operations import seed_demo_v2, serve_ui


DEFAULT_WORKSPACE = "proofpress-demo"
DEFAULT_PRINCIPAL = "agent:quickstart"
MCP_CONFIG_NAME = "proofpress-mcp.json"


@contextmanager
def _working_directory(path: Path) -> Iterator[None]:
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def _run_git(workspace: Path, *args: str) -> None:
    result = subprocess.run(
        ["git", *args], cwd=workspace, text=True, capture_output=True
    )
    if result.returncode:
        raise ValueError(
            "git " + " ".join(args) + ": " + result.stderr.strip()
        )


def _proofpress_command() -> tuple[str, list[str]]:
    installed = shutil.which("proofpress")
    if installed:
        return str(Path(installed).resolve()), []
    return str(Path(sys.executable).resolve()), ["-m", "proofpress.cli"]


def create_quickstart_workspace(
        workspace: str | Path, principal: str = DEFAULT_PRINCIPAL) -> dict:
    target = Path(workspace).expanduser().resolve()
    if target.exists():
        raise ValueError(
            f"quickstart workspace already exists: {target}; choose a new path"
        )
    if not principal.strip():
        raise ValueError("quickstart MCP principal must be non-empty")

    target.mkdir(parents=True)
    try:
        _run_git(target, "init", "-q")
        _run_git(target, "config", "user.name", "Proofpress Quickstart")
        _run_git(
            target, "config", "user.email", "quickstart@example.invalid"
        )
        with _working_directory(target):
            demo = seed_demo_v2()

        command, prefix_args = _proofpress_command()
        config = {
            "mcpServers": {
                "proofpress": {
                    "command": command,
                    "args": [
                        *prefix_args,
                        "mcp",
                        "--transport",
                        "stdio",
                        "--workspace",
                        str(target),
                    ],
                    "env": {
                        "PROOFPRESS_MCP_PRINCIPAL": principal.strip(),
                    },
                }
            }
        }
        config_path = target / MCP_CONFIG_NAME
        config_path.write_text(
            json.dumps(config, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except Exception:
        shutil.rmtree(target, ignore_errors=True)
        raise

    return {
        **demo,
        "workspace": str(target),
        "mcp_config_path": str(config_path),
        "mcp_config": config,
        "review": {
            "command": (
                f"cd {shlex.quote(str(target))} && "
                "proofpress ui --scope demo"
            ),
            "launched": False,
        },
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="proofpress quickstart",
        description=(
            "Create a fresh Git-backed synthetic demo and local MCP config"
        ),
    )
    parser.add_argument(
        "--workspace",
        default=DEFAULT_WORKSPACE,
        help=(
            "new directory for the isolated demo; it must not already exist "
            f"(default: ./{DEFAULT_WORKSPACE})"
        ),
    )
    parser.add_argument(
        "--ui", action="store_true",
        help="serve the loopback-only local review UI after setup",
    )
    parser.add_argument(
        "--no-browser", action="store_true",
        help="with --ui, serve without opening a browser",
    )
    parser.add_argument("--port", type=int, default=7331)
    args = parser.parse_args(argv)

    try:
        result = create_quickstart_workspace(args.workspace)
    except ValueError as exc:
        parser.error(str(exc))

    if args.ui:
        result["review"]["launched"] = True
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)

    if args.ui:
        with _working_directory(Path(result["workspace"])):
            serve_ui(args.port, "demo", not args.no_browser)


if __name__ == "__main__":
    main()

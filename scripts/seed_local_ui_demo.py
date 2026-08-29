#!/usr/bin/env python3
"""Create a disposable synthetic Proofpress ledger for the Local UI."""

import argparse
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "proofpress.py"
def git(cwd, *args, check=True):
    return subprocess.run(
        ["git", *args], cwd=cwd, text=True, capture_output=True, check=check,
    )

def main():
    parser = argparse.ArgumentParser(
        description="Seed an empty Git repository with synthetic Local UI data."
    )
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    repo.mkdir(parents=True, exist_ok=True)

    if not (repo / ".git").exists():
        git(repo, "init", "-q")
        git(repo, "config", "user.name", "Proofpress Synthetic Demo")
        git(repo, "config", "user.email", "demo@example.invalid")
    result = subprocess.run(
        [sys.executable, str(CLI), "demo"], cwd=repo, text=True,
        capture_output=True, check=True,
    )
    print(result.stdout, end="")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Create a disposable synthetic Proofpress ledger for the Local UI."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "proofpress.py"
FIXTURE = ROOT / "examples" / "verified-knowledge-ledger" / "demo.otlp.json"
KNOWLEDGE_REF = "refs/proofpress/knowledge"


def command(cwd, *args):
    result = subprocess.run(
        [sys.executable, str(CLI), *args], cwd=cwd, text=True,
        capture_output=True, check=True,
    )
    return json.loads(result.stdout)


def git(cwd, *args, check=True):
    return subprocess.run(
        ["git", *args], cwd=cwd, text=True, capture_output=True, check=check,
    )


def propose(cwd, statement, evidence):
    args = [
        "propose", "--statement", statement, "--scope", "demo",
        "--proposer", "agent:analyst",
    ]
    for evidence_id in evidence:
        args.extend(["--evidence", evidence_id])
    return command(cwd, *args)["conclusion"]["id"]


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
    if git(repo, "show-ref", "--verify", "--quiet", KNOWLEDGE_REF,
           check=False).returncode == 0:
        raise SystemExit(
            f"ref {KNOWLEDGE_REF} already exists; use an empty demo repository"
        )

    imported = command(repo, "evidence", "import", str(FIXTURE))
    baseline, candidate_b, timed_out = imported["evidence"]

    admitted = propose(
        repo,
        "Candidate B increased synthetic conversion from 12% to 18% in the recorded experiment.",
        [baseline, candidate_b],
    )
    rejected = propose(
        repo,
        "Candidate C is ready for rollout despite the recorded timeout.",
        [timed_out],
    )
    needs_review = propose(
        repo,
        "The observed Candidate B lift should be revalidated before a production rollout.",
        [candidate_b],
    )

    for conclusion in (admitted, rejected, needs_review):
        command(repo, "evaluate", conclusion)
    command(
        repo, "review", admitted, "--admit", "--reviewer",
        "human:product-owner", "--note",
        "Synthetic demo admission: reuse only within the demo scope.",
    )
    command(
        repo, "review", rejected, "--reject", "--reviewer",
        "human:product-owner", "--note",
        "Synthetic demo rejection: the source run timed out.",
    )
    context = command(
        repo, "context", "--scope", "demo", "--actor", "agent:successor"
    )
    print(json.dumps({
        "synthetic": True,
        "repo": str(repo),
        "scope": "demo",
        "states": {
            "admitted": admitted,
            "needs_review": needs_review,
            "rejected": rejected,
        },
        "eligible_context": [row["id"] for row in context["knowledge"]],
        "blocked": context["blocked"],
        "launch": (
            f"cd {repo} && {sys.executable} {CLI} ui --scope demo"
        ),
    }, indent=2))


if __name__ == "__main__":
    main()

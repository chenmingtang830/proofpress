"""Safe two-run demonstration; writes only inside a temporary workspace."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

from proofpress.client import ProofpressClient


ROOT = Path(__file__).resolve().parents[2]


def main():
    with tempfile.TemporaryDirectory(prefix="proofpress-run-demo-") as tmp:
        workspace = Path(tmp)
        subprocess.run(["git", "init", "-q"], cwd=workspace, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@proofpress.dev"], cwd=workspace, check=True)
        subprocess.run(["git", "config", "user.name", "Proofpress Fixture"], cwd=workspace, check=True)
        previous = Path.cwd(); os.chdir(workspace)
        try:
            client = ProofpressClient.in_process(workspace)
            evidence = client.import_evidence(
                ROOT / "examples/verified-knowledge-ledger/demo.otlp.json")["evidence"][0]
            claim = client.propose_claim(
                "This synthetic claim exists only to demonstrate task-run linkage.",
                [evidence], "synthetic-dogfood", "agent:fixture-proposer",
                title="Synthetic task-run fixture")["claim"]
            client.evaluate_claim(claim["id"])
            client.review_claim(claim["id"], "admit", "human:fixture-owner",
                                note="Fixture admission inside an isolated demo workspace.")
            results = []
            for number in (1, 2):
                run = client.start_run(f"Synthetic Proofpress development run {number}", actor="agent:dogfood")
                receipt = client.capture_context(run["id"], actor="agent:dogfood", scope="synthetic-dogfood")
                reliance = client.record_reliance(
                    run["id"], receipt["id"], claim["id"], claim["digest"],
                    "Preserve the fixture-only boundary", actor="agent:dogfood")
                output = client.record_output(
                    run["id"], "repo://synthetic/result.json",
                    "sha256:" + hashlib.sha256(f"result-{number}".encode()).hexdigest(),
                    actor="agent:dogfood", summary=f"Synthetic output {number}",
                    reliance_ids=[reliance["id"]])
                client.record_observation(
                    run["id"], "test", "synthetic fixture assertion",
                    f"Run {number} retained its exact receipt and output hash.",
                    actor="agent:fixture-observer", output_ids=[output["id"]])
                client.finish_run(run["id"], "completed", actor="agent:dogfood")
                results.append(client.get_run(run["id"]))
            print(json.dumps({"schema_version": "proofpress/task-run-demo/v1",
                              "claim": claim["id"], "runs": results,
                              "claim_of_improvement": False}, indent=2))
        finally:
            os.chdir(previous)


if __name__ == "__main__":
    main()

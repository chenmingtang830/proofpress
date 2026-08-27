#!/usr/bin/env python3
"""Run the OpenWiki-to-Proofpress contradiction quarantine demonstration."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any


DEMO_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = DEMO_DIR.parents[1]
PROOFPRESS = REPOSITORY_ROOT / "proofpress.py"
FIXTURE = DEMO_DIR / "openwiki-fixture.json"
SCOPE = "openwiki:geometry:physical-horizon-control"
RESOLVER = "human:geometry-steward"
PROPOSER = "agent:openwiki-handoff"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def exact_lines(source: str) -> list[str]:
    """Match OpenWiki's newline-preserving source splitter."""
    return source.splitlines(keepends=True)


def decode_range_version(version: str) -> tuple[str, dict[str, Any]]:
    prefix = "repo-lines-v1:sha256:"
    if not version.startswith(prefix):
        raise AssertionError(f"unsupported range version: {version}")
    content_hash, encoded = version[len(prefix) :].split(":", 1)
    padding = "=" * (-len(encoded) % 4)
    metadata = json.loads(base64.urlsafe_b64decode(encoded + padding))
    return content_hash, metadata


def verify_evidence_resource(root: Path, resource: str, version: str) -> None:
    match = re.fullmatch(r"repo://([^#]+)(?:#L([1-9][0-9]*)-L([1-9][0-9]*))?", resource)
    if not match:
        raise AssertionError(f"unsupported OpenWiki evidence resource: {resource}")
    relative, start_raw, end_raw = match.groups()
    source = (root / relative).read_text(encoding="utf-8")
    if start_raw is None:
        expected = "repo-file-v1:sha256:" + sha256(source.encode())
        if version != expected:
            raise AssertionError(f"whole-file evidence changed: {resource}")
        return

    lines = exact_lines(source)
    start, end = int(start_raw), int(end_raw)
    if start > end or end > len(lines):
        raise AssertionError(f"invalid evidence range: {resource}")
    selected = lines[start - 1 : end]
    content_hash, metadata = decode_range_version(version)
    if sha256("".join(selected).encode()) != content_hash:
        raise AssertionError(f"range evidence changed: {resource}")
    if metadata["selectedLineCount"] != len(selected):
        raise AssertionError(f"range line count changed: {resource}")
    if sha256(selected[0].encode()) != metadata["firstSelectedLineHash"]:
        raise AssertionError(f"range first-line anchor changed: {resource}")
    if sha256(selected[-1].encode()) != metadata["lastSelectedLineHash"]:
        raise AssertionError(f"range last-line anchor changed: {resource}")

    preceding_count = metadata["precedingContextLineCount"]
    following_count = metadata["followingContextLineCount"]
    preceding = lines[max(0, start - 1 - preceding_count) : start - 1]
    following = lines[end : end + following_count]
    if sha256("".join(preceding).encode()) != metadata["precedingContextHash"]:
        raise AssertionError(f"range preceding anchor changed: {resource}")
    if sha256("".join(following).encode()) != metadata["followingContextHash"]:
        raise AssertionError(f"range following anchor changed: {resource}")


def materialize_and_verify_openwiki(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if fixture["schema"] != "proofpress.openwiki-frozen-fixture.v1":
        raise AssertionError("unexpected fixture schema")
    for relative, record in fixture["files"].items():
        data = record["content"].encode()
        if sha256(data) != record["sha256"]:
            raise AssertionError(f"embedded file digest mismatch: {relative}")
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    page_path = root / "openwiki/geometry/physical-horizon-control.md"
    sidecar_path = root / "openwiki/.claims/geometry/physical-horizon-control.json"
    sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
    page_version = "sha256:" + sha256(page_path.read_bytes())
    if sidecar["pageVersion"] != page_version:
        raise AssertionError("OpenWiki pageVersion does not match the page bytes")
    if 'okf_version: "0.2"' not in (root / "openwiki/index.md").read_text(encoding="utf-8"):
        raise AssertionError("OpenWiki root does not declare OKF v0.2")

    preflight = fixture["official_preflight"]
    if preflight["runtime"] != "openwiki/0.4.2" or preflight["issueCount"] != 0:
        raise AssertionError("frozen official OpenWiki preflight was not clean")
    if preflight["issues"] or preflight["orphanPages"]:
        raise AssertionError("frozen official OpenWiki preflight recorded issues")

    verified_claims = 0
    for relative in (
        "openwiki/.claims/geometry/physical-horizon-control.json",
        "openwiki/.claims/quickstart.json",
    ):
        claims = json.loads((root / relative).read_text(encoding="utf-8"))["claims"]
        for claim in claims:
            for evidence in claim["evidence"]:
                verify_evidence_resource(root, evidence["resource"], evidence["version"])
            verified_claims += 1
    if verified_claims != sum(page["claimCount"] for page in preflight["pages"]):
        raise AssertionError("OpenWiki preflight claim count does not match the bundle")

    manifest = json.loads((root / "proofpress-openwiki-manifest.json").read_text(encoding="utf-8"))
    if manifest["okf"]["page_version"] != page_version:
        raise AssertionError("OpenWiki manifest page version does not match")
    claim_index = {claim["id"]: claim for claim in sidecar["claims"]}
    for selected in manifest["proofpress_claim_pair"]:
        if claim_index[selected["claim_id"]]["statement"] != selected["statement"]:
            raise AssertionError("selected OpenWiki claim changed")
    return manifest, claim_index


def run_process(command: list[str], cwd: Path, *, expect_json: bool = True) -> Any:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(
            f"command failed ({result.returncode}): {' '.join(command)}\n{result.stderr.strip()}"
        )
    return json.loads(result.stdout) if expect_json else result.stdout


def git(root: Path, *args: str) -> str:
    return run_process(["git", *args], root, expect_json=False).strip()


def proofpress(root: Path, *args: str) -> dict[str, Any]:
    return run_process(["python3", str(PROOFPRESS), *args], root)


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def import_one(root: Path, path: str, known: set[str]) -> str:
    result = proofpress(root, "evidence", "import", path)
    current = set(result["evidence"])
    added = current - known
    if len(added) != 1:
        raise AssertionError(f"expected one new evidence receipt for {path}, got {sorted(added)}")
    known.update(current)
    return added.pop()


def propose(
    root: Path,
    statement: str,
    evidence: list[str],
    qualifiers: dict[str, Any],
    qualifier_name: str,
) -> str:
    qualifier_path = root / qualifier_name
    write_json(qualifier_path, qualifiers)
    command = [
        "propose",
        "--statement",
        statement,
        "--scope",
        SCOPE,
        "--proposer",
        PROPOSER,
        "--artifact",
        "openwiki/geometry/physical-horizon-control.md",
        "--artifact",
        "openwiki/.claims/geometry/physical-horizon-control.json",
        "--qualifiers",
        str(qualifier_path),
    ]
    for evidence_id in evidence:
        command.extend(("--evidence", evidence_id))
    return proofpress(root, *command)["conclusion"]["id"]


def execute_demo(work_root: Path) -> dict[str, Any]:
    manifest, openwiki_claims = materialize_and_verify_openwiki(work_root)
    frozen_fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    frozen_preflight = frozen_fixture["official_preflight"]
    git(work_root, "init", "--quiet")
    git(work_root, "config", "user.name", "Proofpress Demo")
    git(work_root, "config", "user.email", "proofpress@example.test")

    policy_path = work_root / ".proofpress/policy.json"
    policy_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(policy_path, {"conflict_resolvers": [RESOLVER]})
    git(work_root, "add", ".")
    git(work_root, "commit", "--quiet", "-m", "freeze OpenWiki geometry bundle")

    known: set[str] = set()
    evidence_ids = [
        import_one(work_root, "evidence/gravitational-evidence.json", known),
        import_one(work_root, "openwiki/index.md", known),
        import_one(work_root, "openwiki/geometry/physical-horizon-control.md", known),
        import_one(work_root, "openwiki/.claims/geometry/physical-horizon-control.json", known),
    ]

    pair = manifest["proofpress_claim_pair"]
    old_origin = openwiki_claims[pair[0]["claim_id"]]
    current_origin = openwiki_claims[pair[1]["claim_id"]]
    quote_match = re.search(r"‘(.+)’", old_origin["statement"])
    if not quote_match:
        raise AssertionError("preserved assertion quotation is missing")
    losing_statement = quote_match.group(1)
    winning_statement = current_origin["statement"]

    common = {
        "producer": manifest["producer"],
        "okf": manifest["okf"],
        "source_freshness": "current_in_frozen_openwiki_bundle",
        "source_sha256": manifest["source"]["sha256"],
        "truth_boundary": "Freshness is claim-to-file evidence, not independent physics validation.",
    }
    loser = propose(
        work_root,
        losing_statement,
        evidence_ids,
        {
            **common,
            "openwiki_claim_id": old_origin["id"],
            "openwiki_evidence": old_origin["evidence"],
            "handoff_transformation": "historical quotation promoted as an unqualified candidate",
            "origin_statement": old_origin["statement"],
            "origin_status": "preserved_superseded_assertion",
        },
        "loser-qualifiers.json",
    )
    winner = propose(
        work_root,
        winning_statement,
        evidence_ids,
        {
            **common,
            "openwiki_claim_id": current_origin["id"],
            "openwiki_evidence": current_origin["evidence"],
            "handoff_transformation": "none",
            "origin_statement": current_origin["statement"],
            "origin_status": "current_source_interpretation",
        },
        "winner-qualifiers.json",
    )
    proofpress(work_root, "review", loser, "--admit", "--reviewer", "human:fixture-reviewer")
    proofpress(work_root, "review", winner, "--admit", "--reviewer", "human:fixture-reviewer")

    before_conflict = proofpress(work_root, "context", "--scope", SCOPE)
    if {row["id"] for row in before_conflict["knowledge"]} != {loser, winner}:
        raise AssertionError("both otherwise-current candidates were not admitted before the conflict")

    relation_qualifiers = work_root / "relation-qualifiers.json"
    write_json(
        relation_qualifiers,
        {
            "admission_basis": "human semantic review",
            "automatic_conflict_detection": False,
            "reason": "The status-stripped prior assertion and the current physical-horizon assertion cannot both govern a successor.",
        },
    )
    relation = proofpress(
        work_root,
        "relation",
        "propose",
        loser,
        "--to",
        winner,
        "--type",
        "contradicts",
        "--proposer",
        "agent:semantic-linker",
        "--qualifiers",
        str(relation_qualifiers),
    )["relation"]["id"]
    proofpress(
        work_root,
        "relation",
        "review",
        relation,
        "--admit",
        "--reviewer",
        "human:fixture-reviewer",
    )

    quarantined = proofpress(
        work_root,
        "context",
        "--scope",
        SCOPE,
        "--include-blocked-statements",
    )
    blocked = {row["id"]: row for row in quarantined["blocked"]}
    if quarantined["knowledge"]:
        raise AssertionError("admitted contradiction leaked into governed context")
    if {blocked[loser]["reason"], blocked[winner]["reason"]} != {"contradiction_unresolved"}:
        raise AssertionError("contradiction did not deterministically quarantine both endpoints")

    resolved = proofpress(
        work_root,
        "relation",
        "resolve",
        relation,
        "--disposition",
        "supersede",
        "--winner",
        winner,
        "--reviewer",
        RESOLVER,
        "--note",
        "Retain the structured current-source interpretation; withhold the status-stripped prior assertion.",
    )

    # This subprocess starts after resolution and receives no in-memory state from
    # the producer or resolver. It reads the frozen worktree policy and the
    # append-only knowledge ref.
    fresh_process = subprocess.run(
        ["python3", str(PROOFPRESS), "context", "--scope", SCOPE],
        cwd=work_root,
        text=True,
        capture_output=True,
    )
    if fresh_process.returncode:
        raise RuntimeError(fresh_process.stderr.strip())
    fresh_raw = fresh_process.stdout
    successor = json.loads(fresh_raw)
    if [row["id"] for row in successor["knowledge"]] != [winner]:
        raise AssertionError("fresh successor did not receive exactly the winning claim")
    if losing_statement in fresh_raw:
        raise AssertionError("fresh successor received the losing statement")

    receipt = successor["knowledge"][0]["receipt"]
    conflict_receipts = receipt["conflict_resolutions"]
    if len(conflict_receipts) != 1:
        raise AssertionError("fresh successor is missing the conflict decision receipt")
    conflict_receipt = conflict_receipts[0]
    expected_ids = {
        "relation_id": relation,
        "resolution_event": resolved["resolution"]["event_id"],
        "supersession_event": resolved["supersession"]["event_id"],
    }
    if any(conflict_receipt[key] != value for key, value in expected_ids.items()):
        raise AssertionError("fresh successor conflict receipt does not match the ledger")
    if conflict_receipt["identity_basis"] != "self_asserted":
        raise AssertionError("demo must not overstate resolver authentication")
    if len(receipt["evidence_digests"]) != len(evidence_ids):
        raise AssertionError("fresh successor is missing evidence digests")
    if not re.fullmatch(r"[a-f0-9]{40}", successor["ledger_head"] or ""):
        raise AssertionError("fresh successor is missing the Git ledger head")

    source = json.loads((work_root / manifest["source"]["path"]).read_text(encoding="utf-8"))
    row = source["rows"][0]
    control = row["matched_compute_control"]
    return {
        "schema": "proofpress.openwiki-conflict-demo.v1",
        "fixture": {
            "openwiki_runtime": "0.4.2",
            "openwiki_commit": "3c2e43eda6f47c0dca572a21b308f94603d00843",
            "bundle_commit": "69cf2dff0a9440057f60fccfe137150fe2959384",
            "okf_version": "0.2",
            "page_version": manifest["okf"]["page_version"],
            "source_sha256": manifest["source"]["sha256"],
            "official_preflight_issues": frozen_preflight["issueCount"],
            "rechecked_claims": sum(page["claimCount"] for page in frozen_preflight["pages"]),
        },
        "handoff": {
            "otherwise_admitted_before_relation": len(before_conflict["knowledge"]),
            "relation_id": relation,
            "quarantined_knowledge": len(quarantined["knowledge"]),
            "blocked_reasons": {cid: blocked[cid]["reason"] for cid in (loser, winner)},
            "semantic_detection": "human_admitted",
        },
        "fresh_successor": {
            "knowledge_count": len(successor["knowledge"]),
            "winner_id": winner,
            "winner_statement": winning_statement,
            "loser_statement_absent": losing_statement not in fresh_raw,
            "evidence_digest_count": len(receipt["evidence_digests"]),
            "ledger_head": successor["ledger_head"],
            "policy_digest": successor["policy_digest"],
            **expected_ids,
            "resolver": conflict_receipt["reviewer"],
            "identity_basis": conflict_receipt["identity_basis"],
        },
        "geometry": {
            "physical_horizon_seconds": row["horizon"],
            "corrected_energy_error": row["corrected_absolute"],
            "control_energy_error": control["invariant_absolute"],
            "corrected_trajectory_rms_km": row["trajectory_pair"]["corrected_absolute"],
            "control_trajectory_rms_km": control["trajectory_absolute"],
            "corrected_wall_seconds": row["compute_cost"]["wall_seconds_corrected"],
            "control_wall_seconds": control["wall_seconds"],
            "initial_condition_count": row["seed_or_ic_count"],
            "claim_scope": row["claim_scope"],
        },
        "truth_boundary": {
            "openwiki": "deterministic claim-to-file freshness",
            "proofpress": "deterministic quarantine and receipt-bearing release after human admission",
            "authority": "resolver allowlist only; identity is self_asserted, not authenticated",
            "physics": "aggregate evidence only; simulation code, full outputs, and source preimage are absent",
            "cle": "not evaluated in this demo",
        },
    }


def print_human(result: dict[str, Any]) -> None:
    fixture = result["fixture"]
    handoff = result["handoff"]
    successor = result["fresh_successor"]
    print(
        f"PASS OpenWiki {fixture['openwiki_runtime']} / OKF {fixture['okf_version']}: "
        f"frozen preflight recorded 0 issues; {fixture['rechecked_claims']} claims rechecked "
        "against embedded evidence versions"
    )
    print(
        f"PASS Proofpress quarantine: {handoff['otherwise_admitted_before_relation']} admitted before conflict, "
        f"{handoff['quarantined_knowledge']} released after conflict"
    )
    print(
        "PASS Fresh successor: 1 winner, losing statement absent, "
        f"{successor['evidence_digest_count']} evidence digests"
    )
    print(
        "PASS Decision receipt: "
        f"relation={successor['relation_id']} resolution={successor['resolution_event']} "
        f"supersession={successor['supersession_event']}"
    )
    print(
        "BOUNDARY Resolver identity is self_asserted. The fixture proves claim-to-file freshness and "
        "governed handoff, not the underlying physics."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit only the machine-readable result")
    parser.add_argument("--workdir", type=Path, help="use and retain this empty work directory")
    args = parser.parse_args()

    if args.workdir:
        args.workdir.mkdir(parents=True, exist_ok=True)
        if any(args.workdir.iterdir()):
            parser.error("--workdir must be empty")
        result = execute_demo(args.workdir.resolve())
    else:
        with tempfile.TemporaryDirectory(prefix="proofpress-openwiki-demo-") as temporary:
            result = execute_demo(Path(temporary))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human(result)


if __name__ == "__main__":
    main()

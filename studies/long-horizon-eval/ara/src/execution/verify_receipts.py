"""Verify content-addressed receipts for the frozen Proofpress handoff study.

This is the ARA code kernel for the receipt verifier and publication compiler.
The protocol controller, governed handoff builder, and paired evaluator remain
in the adjacent RelayBench harness and are referenced by src/artifacts.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ARA_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ARA_ROOT / "evidence" / "FINAL_RESULTS_RECEIPTS.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_receipts(manifest_path: Path) -> list[dict[str, str | bool]]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    receipts = [
        *manifest.get("admitted_panel_receipts", []),
        *manifest.get("secondary_receipts", []),
    ]
    results: list[dict[str, str | bool]] = []
    for receipt in receipts:
        target = (manifest_path.parent / receipt["path"]).resolve()
        actual = sha256_file(target) if target.is_file() else "missing"
        expected = receipt["sha256"]
        results.append(
            {
                "path": str(target),
                "expected_sha256": expected,
                "actual_sha256": actual,
                "verified": actual == expected,
            }
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    results = verify_receipts(args.manifest.resolve())
    print(json.dumps({"receipts": results}, indent=2))
    return 0 if results and all(item["verified"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

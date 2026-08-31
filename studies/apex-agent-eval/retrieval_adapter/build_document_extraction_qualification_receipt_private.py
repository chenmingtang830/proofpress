#!/usr/bin/env python3
"""Compile private B.5 artifacts into a source-safe Phase C gate receipt.

The receipt contains metrics and cryptographic provenance only: it never
copies page text, table values, OCR output, source URIs, prompts, or outcomes.
It makes a passed document-extraction panel a real content-addressed Phase C
input while retaining the rule that extraction is a not-governed candidate and
Human Approval is required for any later admission.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
CONTRACT_PATH = ROOT / "document_extraction_contract.py"
SPEC = importlib.util.spec_from_file_location("document_extraction_contract", CONTRACT_PATH)
contract = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(contract)

SCHEMA = "proofpress/document-extraction-phase-c-qualification/v1"


def digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def read_object(path: Path, label: str) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def heldout_metrics(score: dict[str, Any]) -> dict[str, Any]:
    if score.get("split") != "heldout":
        raise ValueError("held-out conformance receipt must be the heldout split")
    metrics = score.get("metrics")
    if not isinstance(metrics, dict):
        raise ValueError("held-out conformance metrics are missing")
    def f1(name: str) -> Any:
        row = metrics.get(name); return row.get("f1") if isinstance(row, dict) else None
    def rate(name: str) -> Any:
        row = metrics.get(name); return row.get("rate") if isinstance(row, dict) else None
    output = {"documents_scored": score.get("documents_scored"),
              "documents_expected": score.get("documents_expected"),
              "text_blocks_f1": f1("text_blocks"), "table_cells_f1": f1("table_cells"),
              "numeric_values_f1": f1("numeric_values"), "locator_rate": rate("locators"),
              "reading_order_rate": rate("reading_order"),
              "cross_page_continuations_f1": f1("cross_page_continuations")}
    if (not isinstance(output["documents_scored"], int) or not isinstance(output["documents_expected"], int)
            or output["documents_scored"] != output["documents_expected"] or output["documents_scored"] < 1):
        raise ValueError("held-out conformance completion is incomplete")
    return output


def collect_envelopes(root: Path, *, model_revision: str) -> dict[str, Any]:
    paths = sorted(root.rglob("extraction-envelope.json"))
    if not paths:
        raise ValueError("no extraction envelopes found for qualification receipt")
    extractors, envelope_digests = [], []
    for path in paths:
        envelope = read_object(path, "extraction envelope")
        contract.validate_envelope(envelope)
        extractors.append(envelope["extractor"]); envelope_digests.append(envelope["extraction_digest"])
    canonical = json.loads(json.dumps(extractors[0], sort_keys=True))
    if any(row != canonical for row in extractors[1:]):
        raise ValueError("qualification receipt cannot combine different extractor configurations")
    return {"provider": canonical["provider"], "model": canonical["model"],
            "version": canonical["version"], "license": canonical["license"],
            "config_digest": canonical["config_digest"], "model_revision": model_revision,
            "envelope_count": len(envelope_digests),
            "envelope_set_digest": digest(sorted(envelope_digests)),
            "status": "not_governed_candidate", "admitted": False,
            "human_approval_required": True}


def build(*, key: str, route: str, model_revision: str, development_gate: dict[str, Any],
          heldout: dict[str, Any], ecological: dict[str, Any], envelope_root: Path) -> dict[str, Any]:
    if not key or not route or not model_revision:
        raise ValueError("extractor key, route, and model revision are required")
    if development_gate.get("status") != "pass" or development_gate.get("heldout_authorized") is not True:
        raise ValueError("development extraction gate did not pass")
    if ecological.get("automatic_admission") is not False or ecological.get("human_approval_required") is not True:
        raise ValueError("ecological extraction report changed the admission boundary")
    if ecological.get("failed") != 0 or ecological.get("pending") != 0:
        raise ValueError("ecological extraction panel is not complete")
    provenance = collect_envelopes(envelope_root, model_revision=model_revision)
    if provenance["envelope_count"] < ecological.get("documents", 0):
        raise ValueError("ecological report has more documents than retained extraction envelopes")
    receipt = {"schema_version": SCHEMA, "automatic_admission": False,
               "human_approval_required": True,
               key: {"route": route, "development_gate": development_gate,
                     "heldout_conformance": heldout_metrics(heldout),
                     "ecological": {field: ecological.get(field) for field in (
                         "documents", "attempted", "pending", "complete", "failed", "pages_processed",
                         "blocks", "tables", "cells", "elapsed_seconds", "peak_child_rss_mib",
                         "known_model_cost_usd")},
                     "envelope_provenance": provenance,
                     "conflict_status": "not_compared"}}
    receipt["qualification_digest"] = digest(receipt)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extractor-key", required=True)
    parser.add_argument("--route", required=True)
    parser.add_argument("--model-revision", required=True)
    parser.add_argument("--development-gate", required=True, type=Path)
    parser.add_argument("--heldout-conformance", required=True, type=Path)
    parser.add_argument("--ecological", required=True, type=Path)
    parser.add_argument("--envelope-root", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    receipt = build(key=args.extractor_key, route=args.route, model_revision=args.model_revision,
                    development_gate=read_object(args.development_gate, "development gate"),
                    heldout=read_object(args.heldout_conformance, "held-out conformance"),
                    ecological=read_object(args.ecological, "ecological report"),
                    envelope_root=args.envelope_root)
    args.out.parent.mkdir(parents=True, exist_ok=True); args.out.parent.chmod(0o700)
    args.out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n"); args.out.chmod(0o600)
    print(json.dumps({"schema_version": receipt["schema_version"], "route": args.route,
                      "qualification_digest": receipt["qualification_digest"],
                      "automatic_admission": False, "human_approval_required": True}, sort_keys=True))


if __name__ == "__main__":
    main()

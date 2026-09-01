#!/usr/bin/env python3
"""Build the separately versioned Phase C replication graph from qualified OCR.

This compiler is intentionally unavailable until the original frozen Phase C
panel completed.  It retains the original ordinary claims and authorities,
but replaces its table-cell substrate with cells directly bound to the passed
Paddle extraction-envelope set.  Derivations are recompiled only from an
explicit private manifest that refers to those new cells; neither extraction
nor a derivation self-admits as governed knowledge.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]


def _load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


envelopes = _load("document_extraction_contract.py", "document_extraction_contract")
freeze = _load("studies/apex-agent-eval/retrieval_adapter/freeze_v25_phase_c_inputs_private.py", "freeze_phase_c")
transfer = _load("studies/apex-agent-eval/retrieval_adapter/transfer_validation_contract.py", "transfer_validation")
projection = _load("phase_c_ablation_contract.py", "phase_c_ablation_contract")

SCHEMA = "proofpress/phase-c-qualified-extraction-rebuild/v1"
DERIVATION_SCHEMA = "proofpress/phase-c-rebuild-derivations/v1"


def digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def file_digest(path: Path) -> str:
    return freeze.file_digest(path)


def read_object(path: Path, label: str) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def _digest(value: Any, label: str) -> None:
    if not isinstance(value, str) or len(value) != 71 or not value.startswith("sha256:"):
        raise ValueError(f"{label} must be a sha256 digest")
    try:
        int(value[7:], 16)
    except ValueError as exc:
        raise ValueError(f"{label} must be a sha256 digest") from exc


def validate_first_run(*, base_graph_path: Path, first_frozen_manifest: dict[str, Any],
                       first_result: dict[str, Any]) -> None:
    """Prove the replication cannot precede or silently replace the first run."""
    expected = transfer.validate_transfer_manifest(first_frozen_manifest)
    if first_result.get("status") != "complete":
        raise ValueError("qualified-extraction rebuild requires a complete first Phase C result")
    if (first_result.get("automatic_admission") is not False
            or first_result.get("human_approval_required") is not True):
        raise ValueError("first Phase C result changed the Human Approval boundary")
    if first_result.get("frozen_manifest_digest") != expected["manifest_digest"]:
        raise ValueError("first Phase C result does not bind the supplied frozen manifest")
    if tuple(first_result.get("conditions") or ()) != tuple(projection.CONDITIONS):
        raise ValueError("first Phase C result does not cover the frozen conditions")
    expected_cells = 12 * len(projection.CONDITIONS)
    if (first_result.get("planned_cells") != expected_cells or first_result.get("scored_cells") != expected_cells
            or first_result.get("inconclusive_cells") != 0):
        raise ValueError("first Phase C result is not a complete task-by-condition panel")
    controls = first_frozen_manifest.get("frozen_controls")
    if not isinstance(controls, dict) or controls.get("graph_digest") != file_digest(base_graph_path):
        raise ValueError("base graph bytes do not match the first frozen Phase C manifest")


def qualified_identity(qualification: dict[str, Any]) -> dict[str, Any]:
    route = qualification.get("paddleocr_vl_1_6_mlx")
    if not isinstance(route, dict):
        raise ValueError("Paddle qualification route is missing")
    # Reuse the same full B.5 minimum and no-admission validation that gates
    # the initial Phase C graph.
    freeze.validate_extraction_qualification(qualification,
                                             route="PaddlePaddle/PaddleOCR-VL-1.6/mlx-vlm-server",
                                             key="paddleocr_vl_1_6_mlx")
    provenance = route["envelope_provenance"]
    _digest(qualification.get("qualification_digest"), "extraction qualification_digest")
    if not isinstance(route.get("conflict_status"), str) or not route["conflict_status"]:
        raise ValueError("Paddle qualification conflict status is missing")
    return {**provenance, "qualification_digest": qualification.get("qualification_digest"),
            "conflict_status": route.get("conflict_status")}


def collect_qualified_envelopes(root: Path, identity: dict[str, Any]) -> list[dict[str, Any]]:
    paths = sorted(root.rglob("extraction-envelope.json"))
    if not paths:
        raise ValueError("no retained extraction envelopes found for rebuild")
    rows = []
    for path in paths:
        envelope = read_object(path, "extraction envelope")
        envelopes.validate_envelope(envelope)
        extractor = envelope["extractor"]
        if any(extractor.get(key) != identity.get(key) for key in ("provider", "model", "version", "license", "config_digest")):
            raise ValueError("rebuild envelope extractor identity differs from passed qualification")
        rows.append(envelope)
    extraction_digests = sorted(row["extraction_digest"] for row in rows)
    if digest(extraction_digests) != identity.get("envelope_set_digest"):
        raise ValueError("rebuild envelope set does not exactly match the passed qualification")
    if len(rows) != identity.get("envelope_count"):
        raise ValueError("rebuild envelope count does not match the passed qualification")
    return rows


def cells_from_envelopes(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[tuple[str, str, int, int], str]]:
    cells, references = [], {}
    for envelope in rows:
        source_digest = envelope["source"]["content_digest"]
        extraction_digest = envelope["extraction_digest"]
        for table in envelope["tables"]:
            for cell in table["cells"]:
                key = (source_digest, table["id"], cell["row"], cell["column"])
                if key in references:
                    raise ValueError("qualified extraction envelopes contain duplicate source table-cell coordinates")
                cell_id = "qcell_" + digest({"extraction_digest": extraction_digest, "table_id": table["id"],
                                               "row": cell["row"], "column": cell["column"]})[7:27]
                row = {"cell_id": cell_id, "source_content_digest": source_digest,
                       "source_table_id": table["id"], "source_extraction_digest": extraction_digest,
                       "locator": cell["locator"], "row": cell["row"], "column": cell["column"],
                       "raw_text": cell["raw_text"], "status": "not_governed_candidate",
                       "admitted": False, "human_approval_required": True}
                cells.append(row); references[key] = cell_id
    if not cells:
        raise ValueError("qualified extraction envelope set has no table cells for the rebuilt graph")
    return sorted(cells, key=lambda row: row["cell_id"]), references


def compile_derivations(manifest: dict[str, Any], references: dict[tuple[str, str, int, int], str]) -> list[dict[str, Any]]:
    if (manifest.get("schema_version") != DERIVATION_SCHEMA or manifest.get("automatic_admission") is not False
            or manifest.get("human_approval_required") is not True or not isinstance(manifest.get("derivations"), list)):
        raise ValueError("rebuild derivation manifest must preserve candidate and Human Approval boundaries")
    output, seen = [], set()
    for row in manifest["derivations"]:
        if not isinstance(row, dict) or not isinstance(row.get("derivation_id"), str) or not row["derivation_id"]:
            raise ValueError("rebuild derivations require unique derivation_id values")
        if row["derivation_id"] in seen:
            raise ValueError("rebuild derivation IDs must be unique")
        seen.add(row["derivation_id"])
        if (not isinstance(row.get("formula"), str) or not row["formula"]
                or not isinstance(row.get("input_cells"), list) or not row["input_cells"]
                or not isinstance(row.get("assumptions", []), list)):
            raise ValueError("rebuild derivations require explicit formula and input_cells")
        input_ids = []
        for ref in row["input_cells"]:
            if not isinstance(ref, dict) or not isinstance(ref.get("source_content_digest"), str) or not isinstance(ref.get("table_id"), str):
                raise ValueError("rebuild derivation inputs require source digest and table ID")
            if not isinstance(ref.get("row"), int) or not isinstance(ref.get("column"), int):
                raise ValueError("rebuild derivation inputs require integer row and column")
            key = (ref["source_content_digest"], ref["table_id"], ref["row"], ref["column"])
            if key not in references:
                raise ValueError("rebuild derivation refers to an unavailable qualified table cell")
            input_ids.append(references[key])
        evidence = {"derivation_id": row["derivation_id"], "formula": row["formula"],
                    "assumptions": row.get("assumptions", []), "input_cell_ids": input_ids}
        output.append({**evidence, "derivation_digest": digest(evidence), "status": "not_governed_candidate",
                       "admitted": False, "human_approval_required": True})
    return sorted(output, key=lambda row: row["derivation_id"])


def rebuild(*, base_graph: dict[str, Any], first_frozen_manifest: dict[str, Any], first_result: dict[str, Any],
            base_graph_path: Path, qualification: dict[str, Any], envelope_root: Path,
            derivation_manifest: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    projection.validate_graph(base_graph)
    validate_first_run(base_graph_path=base_graph_path, first_frozen_manifest=first_frozen_manifest,
                       first_result=first_result)
    identity = qualified_identity(qualification)
    envelope_rows = collect_qualified_envelopes(envelope_root, identity)
    cells, references = cells_from_envelopes(envelope_rows)
    derivations = compile_derivations(derivation_manifest, references)
    source_manifest = {"base_source_manifest_digest": base_graph["source_manifest_digest"],
                       "qualified_envelope_set_digest": identity["envelope_set_digest"],
                       "qualification_digest": identity["qualification_digest"]}
    graph = {"schema_version": SCHEMA, "automatic_admission": False, "human_approval_required": True,
             "source_manifest_digest": digest(source_manifest),
             "claims": base_graph["claims"], "authority_nodes": base_graph["authority_nodes"],
             "table_cells": cells, "derivations": derivations,
             "lineage": {"base_graph_digest": base_graph["graph_digest"],
                         "first_phase_c_frozen_manifest_digest": first_result["frozen_manifest_digest"],
                         "extraction_qualification_digest": identity["qualification_digest"],
                         "envelope_set_digest": identity["envelope_set_digest"],
                         "extractor": {key: identity[key] for key in ("provider", "model", "version", "license", "config_digest", "model_revision")},
                         "conflict_status": identity["conflict_status"],
                         "derivation_manifest_digest": digest(derivation_manifest)},
             "rebuild_status": "not_governed_candidate"}
    graph["graph_digest"] = digest({key: value for key, value in graph.items() if key != "graph_digest"})
    projection.validate_graph(graph)
    receipt = {"schema_version": SCHEMA, "status": "rebuilt-private-graph", "automatic_admission": False,
               "human_approval_required": True, "rebuilt_graph_digest": graph["graph_digest"],
               "base_graph_digest": base_graph["graph_digest"],
               "first_phase_c_frozen_manifest_digest": first_result["frozen_manifest_digest"],
               "extraction_qualification_digest": identity["qualification_digest"],
               "envelope_set_digest": identity["envelope_set_digest"], "envelope_count": len(envelope_rows),
               "table_cell_count": len(cells), "derivation_count": len(derivations),
               "conflict_status": identity["conflict_status"],
               "decision_boundary": "Rebuilt candidate graph only; no extraction, derivation, or claim is admitted."}
    receipt["receipt_digest"] = digest(receipt)
    return graph, receipt


def _write_private(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.parent.chmod(0o700)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"); path.chmod(0o600)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-graph", required=True, type=Path)
    parser.add_argument("--first-frozen-manifest", required=True, type=Path)
    parser.add_argument("--first-phase-c-result", required=True, type=Path)
    parser.add_argument("--qualification", required=True, type=Path)
    parser.add_argument("--envelope-root", required=True, type=Path)
    parser.add_argument("--derivation-manifest", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--receipt-out", required=True, type=Path)
    args = parser.parse_args()
    try:
        graph, receipt = rebuild(base_graph=read_object(args.base_graph, "base graph"),
                                 first_frozen_manifest=read_object(args.first_frozen_manifest, "first frozen manifest"),
                                 first_result=read_object(args.first_phase_c_result, "first Phase C result"),
                                 base_graph_path=args.base_graph,
                                 qualification=read_object(args.qualification, "extraction qualification"),
                                 envelope_root=args.envelope_root,
                                 derivation_manifest=read_object(args.derivation_manifest, "derivation manifest"))
        _write_private(args.out, graph); _write_private(args.receipt_out, receipt)
        print(json.dumps({key: receipt[key] for key in ("status", "rebuilt_graph_digest", "envelope_count",
                                                        "table_cell_count", "derivation_count", "receipt_digest")}, sort_keys=True))
    except Exception as exc:
        # Never print task/source values, OCR text, formulas, or graph contents.
        print(f"phase-c-qualified-extraction-rebuild: {type(exc).__name__}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()

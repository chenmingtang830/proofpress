"""JSON Schemas the MCP servers publish for tool inputs, shared by the hosted and the stdio transports.

Standard library only, so a transport can import it without loading the other's dependencies. Publishing a schema
does not replace validation: the kernel validates every payload. The schemas publish a selection of the kernel's rules;
some are deliberately left to the kernel and stated in descriptions only: a page range's order, a text span's length
against its quote, a spreadsheet cell's bounds, the pairing of spreadsheet history digests, and that integers are
integers (JSON Schema reads 2.0 as an integer; the kernel refuses it). Each transport publishes its own copy
(`retrieval_evidence_schema`, `stdio_evidence_payload_schema`), so neither can alter the other's.
"""
from __future__ import annotations

import copy

SHA256_PATTERN = r"^sha256:[0-9a-f]{64}(?![\s\S])"  # end of input under ECMA-262 and Python alike ($ allows a final newline in Python)

_DIGEST = {"type": "string", "pattern": SHA256_PATTERN}
_DIGEST_OR_NULL = {"anyOf": [_DIGEST, {"type": "null"}]}
_TEXT = {"type": "string", "pattern": "\\S"}  # the kernel refuses an empty or whitespace-only string
_PAGE = {"type": "integer", "minimum": 1, "description": "A JSON integer such as 2; the kernel refuses 2.0."}
_OFFSET = {"type": "integer", "minimum": 0, "description": "A JSON integer such as 2; the kernel refuses 2.0."}
EXPERIMENT_PROFILE = "proofpress/profile/experiment/v1"  # proofpress.profiles.experiment.PROFILE, kept literal so this module stays standalone


def _kind(kind: str, description: str, properties: dict, required: list[str], **extra) -> dict:
    return {"type": "object", "description": description, "properties": {"kind": {"const": kind}, **properties},
            "required": ["kind", *required], **extra}


# Where in the source the quote sits: one of the kinds the kernel accepts (kernel/operations.py, _normalize_locator),
# each with the fields it requires. The digests are supplied by the adapter; Proofpress records them and does not
# recompute them.
LOCATOR_SCHEMA = {
    "description": "Where the quote sits in the source: one of text_span, page_span, section_span, spreadsheet_cell, json_pointer.",
    "oneOf": [
        _kind("text_span", "Character offsets of the quote in the source text: end > start and end - start equals the quote's "
              "length (checked by the kernel).", {"start": _OFFSET, "end": _OFFSET, "text_digest": _DIGEST}, ["start", "end", "text_digest"]),
        _kind("page_span", "The 1-based pages the quote is on, page_end >= page_start (checked by the kernel), with a digest of "
              "that page text.", {"page_start": _PAGE, "page_end": _PAGE, "page_digest": _DIGEST}, ["page_start", "page_end", "page_digest"]),
        _kind("section_span", "A named section of the source, its digest, and its 1-based pages, page_end >= page_start (checked by "
              "the kernel).", {"section_id": _TEXT, "section_digest": _DIGEST, "page_start": _PAGE, "page_end": _PAGE},
              ["section_id", "section_digest", "page_start", "page_end"]),
        _kind("spreadsheet_cell", "One cell of a workbook by its A1 address (at most column XFD and row 1048576, checked by the "
              "kernel), with a digest of the cell. previous_source_content_digest and previous_cell_digest are given together or "
              "not at all (null counts as not given; checked by the kernel).",
              {"sheet": _TEXT, "cell": {"type": "string", "pattern": "^[A-Z]{1,3}[1-9][0-9]*(?![\\s\\S])"}, "cell_digest": _DIGEST,
               "previous_source_content_digest": _DIGEST_OR_NULL, "previous_cell_digest": _DIGEST_OR_NULL},
              ["sheet", "cell", "cell_digest"]),
        _kind("json_pointer", "An RFC 6901 JSON pointer into a JSON source; the empty string is the whole document.",
              {"value": {"type": "string", "maxLength": 2000, "pattern": "^(/([^~]|~[01])*)*(?![\\s\\S])"}}, ["value"], additionalProperties=False),
    ],
}

RETRIEVAL_EVIDENCE_INPUT_SCHEMA = {
    "type": "object",
    "description": (
        "A proofpress/retrieval-evidence/v1 envelope. Use profile=experiment "
        "only for an experiment-profile payload."
    ),
    "properties": {
        "schema_version": {
            "type": "string", "const": "proofpress/retrieval-evidence/v1",
        },
        "source": {
            "type": "object",
            "properties": {
                "uri": {"type": "string", "minLength": 1},
                "content_digest": {"type": "string", "pattern": SHA256_PATTERN},
                "media_type": {"type": "string", "minLength": 1},
            },
            "required": ["uri", "content_digest"],
        },
        "evidence": {
            "type": "object",
            "properties": {
                "quote": {"type": "string", "minLength": 1},
                "locator": LOCATOR_SCHEMA,
            },
            "required": ["quote", "locator"],
        },
        "retrieval": {
            "type": "object",
            "properties": {
                "adapter": {"type": "string", "minLength": 1},
                "version": {"type": "string", "minLength": 1},
                "query": {"type": "string", "minLength": 1},
                "config_digest": {"type": "string", "pattern": SHA256_PATTERN},
                "selection_reason": {"type": "string", "minLength": 1},
            },
            "required": ["adapter", "version", "query", "config_digest"],
        },
    },
    "required": ["schema_version", "source", "evidence", "retrieval"],
}


def _closed(properties: dict, required: list[str] | None = None, **extra) -> dict:
    return {"type": "object", "properties": properties,
            "required": list(properties) if required is None else required,
            "additionalProperties": False, **extra}


EXPERIMENT_IDENTITY_SCHEMA = _closed({
    **{key: _TEXT for key in ("experiment_id", "run_id", "model_revision", "dataset_revision")},
    "environment_digest": _DIGEST, "config_digest": _DIGEST,
})
_REFS = {"type": "array", "items": _TEXT, "minItems": 1, "uniqueItems": True}
_NUMBER = {"type": ["number", "string"], "description": "A finite decimal value; the kernel checks numeric strings."}
_FAILURE = _closed({
    **{key: _TEXT for key in ("intervention", "expected_outcome", "observed_outcome", "next_action")},
    "feedback_evidence_refs": _REFS, "invalidated_hypotheses": _REFS,
    "repeat_policy": {"enum": ["do-not-repeat", "retry-if-changed", "informational"]},
    "changed_dimension_required": _TEXT,
}, required=["intervention", "expected_outcome", "observed_outcome", "next_action",
             "feedback_evidence_refs", "invalidated_hypotheses", "repeat_policy"],
    description="retry-if-changed requires changed_dimension_required; other repeat policies forbid it.")
EXPERIMENT_CLAIM_SCHEMA = _closed({
    "schema_version": {"const": EXPERIMENT_PROFILE},
    "claim_kind": {"enum": ["finding", "regression", "no-change", "failed-attempt", "decision"]},
    "experiment": EXPERIMENT_IDENTITY_SCHEMA, "failure": _FAILURE,
}, required=["schema_version", "claim_kind", "experiment"],
    description="Value of qualifiers.experiment (not the whole qualifiers object). failed-attempt requires failure; other kinds forbid it.")
CLAIM_QUALIFIERS_SCHEMA = {"type": "object", "properties": {"experiment": EXPERIMENT_CLAIM_SCHEMA},
                           "description": "profile=experiment requires qualifiers.experiment. Omit profile for ordinary source-backed findings."}
_OBSERVATION = _closed({
    **{key: _TEXT for key in ("name", "version", "unit", "population", "slice", "source_evidence_ref")},
    "value": _NUMBER,
}, required=["name", "version", "unit", "source_evidence_ref", "value"],
    oneOf=[{"required": ["population"], "not": {"required": ["slice"]}},
           {"required": ["slice"], "not": {"required": ["population"]}}])
_CELL = _closed({**{key: _TEXT for key in ("table_id", "row", "column", "unit", "source_evidence_ref")}, "value": _NUMBER})
_DERIVATION = _closed({
    "formula": _closed({"name": _TEXT, "version": _TEXT, "operation": {"enum": ["sum", "difference", "product", "ratio"]}}),
    "input_evidence_refs": _REFS, "output": _closed({"value": _NUMBER, "unit": _TEXT}),
    "recomputation_digest": _DIGEST,
}, description="The kernel checks existing metric/table inputs, arithmetic, units and the recomputation digest.")
EXPERIMENT_PAYLOAD_SCHEMA = {
    "description": "Experiment evidence; pass profile=experiment. Submit the original retrieval evidence first and bind its returned evd_ ID. Do not invent run identity for literature or slide findings.",
    "oneOf": [_closed({"schema_version": {"const": EXPERIMENT_PROFILE}, "kind": {"const": kind},
                       "experiment": EXPERIMENT_IDENTITY_SCHEMA, field: schema})
              for kind, field, schema in (("metric_observation", "observation", _OBSERVATION),
                                          ("table_cell", "cell", _CELL), ("derivation", "derivation", _DERIVATION))],
}


def retrieval_evidence_schema() -> dict:
    """A copy of the retrieval evidence envelope's schema for one transport to publish."""
    return copy.deepcopy(RETRIEVAL_EVIDENCE_INPUT_SCHEMA)


def stdio_evidence_payload_schema() -> dict:
    """The stdio tool's payload schema: a retrieval envelope or an experiment-profile payload, told apart by their
    schema_version, so a payload naming the retrieval version must satisfy the envelope. A copy."""
    return copy.deepcopy({"anyOf": [RETRIEVAL_EVIDENCE_INPUT_SCHEMA, EXPERIMENT_PAYLOAD_SCHEMA]})


def claim_qualifiers_schema() -> dict:
    return copy.deepcopy(CLAIM_QUALIFIERS_SCHEMA)


def capture_schema() -> dict:
    """Read-only, transport-independent contract discovery; no workspace data."""
    return {"schema_version": "proofpress/capture-schema/v1",
            "retrieval_evidence": retrieval_evidence_schema(),
            "experiment_evidence": copy.deepcopy(EXPERIMENT_PAYLOAD_SCHEMA),
            "claim_qualifiers": claim_qualifiers_schema(),
            "guidance": [
                "Input quote and locator belong under payload.evidence; flattened quote/locator in a receipt are output only.",
                "quote is one exact string. Hash actual source bytes, extracted page/text, and extraction configuration separately; never invent digests.",
                "For a slide use page_span with 1-based slide bounds and that slide text digest. section_span also requires page bounds.",
                "Ordinary literature or slide findings omit profile. experiment requires recorded run identity and qualifiers.experiment; do not downgrade a required profile to bypass validation.",
                "MCP checks retrieval envelope format and experiment claim qualifiers before submission. Other kernel checks still run at submission; format success is not evidence verification or approval.",
                "After uncertain transport failure, read back before retrying with the same key and identical request. Never change keys repeatedly to guess a format.",
            ]}


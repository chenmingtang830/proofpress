# Content-addressed receipt adapter

This is the reusable integration seam for sources that are not Git: documents,
spreadsheets, database rows, data warehouses, object stores, or vendor systems.
It emits the existing `proofpress/retrieval-evidence/v1` envelope; it does not
introduce a second ledger, upload source bytes, or claim that every source has
the same semantic model.

## What every adapter binds

| Receipt field | Responsibility |
|---|---|
| `source.uri` | An owner-controlled source or revision locator. It need not be an HTTP URL. |
| `source.content_digest` | SHA-256 of the exact source revision the adapter observed. |
| `evidence.quote` | A small, reviewer-readable projection—not a raw artifact or trace. |
| `evidence.locator` | A typed, contract-validated locator such as `text_span`, `page_span`, `section_span`, or `spreadsheet_cell`. |
| `retrieval.{adapter,version,query,config_digest}` | Which adapter made the projection, why, and its content-addressed configuration. |

The adapter establishes byte custody and a reproducible projection boundary.
It does **not** establish that a quote is true, recompute external data, or
approve a conclusion. Those are separate verification and human-governance
steps.

## Python SDK helper

```python
from proofpress.integrations import ContentAddressedReceiptAdapter

adapter = ContentAddressedReceiptAdapter(
    adapter="company.workbook-diff",
    version="1.0.0",
    config={"canonical_cell_projection": "value-and-formula-v1"},
)

receipt = adapter.evidence(
    source_uri="workspace://finance/annual-plan.xlsx?revision=v18",
    source_content_digest="sha256:<workbook-bytes>",
    quote="Revenue!F12 changed from 1180000 to 1050000.",
    locator={
        "kind": "spreadsheet_cell",
        "sheet": "Revenue", "cell": "F12",
        "cell_digest": "sha256:<current-cell-projection>",
        "previous_source_content_digest": "sha256:<previous-workbook-bytes>",
        "previous_cell_digest": "sha256:<previous-cell-projection>",
    },
    query="Annual Plan Revenue!F12 revision",
)

client.submit_evidence(receipt)
```

Only `config_digest` appears in the resulting receipt. If an integration cannot
expose its configuration, initialize the helper with an already computed
`config_digest` instead. Configurations must be stable and must not contain
credentials, source payloads, prompts, or raw traces.

## Adding source-specific meaning

The generic helper only accepts locator kinds the kernel already validates. Add
a new locator kind when a source needs a stable, reviewable address that the
existing kinds cannot express. Specify its minimal fields, canonicalization,
and digest binding, then add validation and adapter tests. Do not use an opaque
`"generic"` locator to imply semantics that Proofpress cannot check.

For workbooks, see [spreadsheet cell evidence](SPREADSHEET_ADAPTER.md).

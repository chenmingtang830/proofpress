# Spreadsheet cell evidence

`proofpress/retrieval-evidence/v1` supports a source-bound `spreadsheet_cell`
locator. It lets a workbook adapter bind a bounded cell observation to immutable
workbook bytes without uploading the workbook itself.

## Contract

The existing `source` object identifies the current workbook:

- `source.uri` is an owner-controlled locator, such as a document-management
  URI or immutable object-store revision.
- `source.content_digest` is the SHA-256 digest of the current workbook bytes.

For `evidence.locator.kind: "spreadsheet_cell"`, provide:

| Field | Required | Meaning |
|---|---:|---|
| `sheet` | yes | Non-empty worksheet name. |
| `cell` | yes | Canonical uppercase A1 address, from `A1` through `XFD1048576`; no `$`, ranges, or named references. |
| `cell_digest` | yes | SHA-256 of the adapter's canonical current-cell projection. The adapter configuration is already bound by `retrieval.config_digest`. |
| `previous_source_content_digest` | paired | SHA-256 of the prior workbook bytes when the evidence is about a change. |
| `previous_cell_digest` | paired | SHA-256 of the prior canonical cell projection. |

The two `previous_*` fields are optional together. Their presence records a
revision comparison; their absence records only the current-cell observation.
Proofpress does not fetch a workbook, recompute formulas, or infer a change
from digests.

```json
{
  "schema_version": "proofpress/retrieval-evidence/v1",
  "source": {
    "uri": "workspace://finance/annual-plan.xlsx?revision=v18",
    "content_digest": "sha256:<current-workbook-bytes>",
    "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
  },
  "evidence": {
    "quote": "Revenue!F12 changed from 1180000 to 1050000.",
    "locator": {
      "kind": "spreadsheet_cell",
      "sheet": "Revenue",
      "cell": "F12",
      "cell_digest": "sha256:<current-canonical-cell>",
      "previous_source_content_digest": "sha256:<previous-workbook-bytes>",
      "previous_cell_digest": "sha256:<previous-canonical-cell>"
    }
  },
  "retrieval": {
    "adapter": "company.workbook-diff",
    "version": "1.0.0",
    "query": "Annual Plan Revenue!F12 revision",
    "config_digest": "sha256:<adapter-configuration>"
  }
}
```

The evidence quote is the bounded, reviewer-readable assertion. Digests bind
that assertion to the current source, cell projection, and—where present—the
prior revision. A later conclusion may bind this evidence only when the cell
observation supports the conclusion; an agent merely retrieving another
document does not make that document claim evidence.

## Universal adapter seam

Git is a strong source of revision history, but it is not the universal
adapter. This workbook contract uses the shared
[content-addressed receipt adapter](CONTENT_ADDRESSED_ADAPTER.md): `URI +
source digest + bounded quote + typed locator + adapter configuration digest`.
Each typed locator must be explicitly specified and validated; a generic helper
may establish byte custody, but must not claim semantic verification it cannot
perform.

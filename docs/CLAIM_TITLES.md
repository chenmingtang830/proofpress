# Claim titles

Claims accept an optional `title` (1–120 characters after trimming) through
`claim.propose`, the Python SDK, hosted and local MCP, and `proofpress remote
propose --title`.

- `title`: a concise heading supplied by the proposer.
- `statement`: the complete claim examined for admission; remains required.
- `applicability`: reuse circumstances and limits, not a claim summary.

Home and Knowledge show the title with a two-line statement preview. Review
and the Knowledge record show the full statement without truncation. Untitled
claims retain their statement as the heading; no summary is fabricated.

Titles are included in claim identity and digest when supplied. Changing a
title produces a new candidate, not a silent edit to an admitted claim.
Omitting title preserves the historical identity and digest shape. Existing
records are not rewritten or backfilled.

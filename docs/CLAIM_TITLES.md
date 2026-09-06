# Claim titles

New proposals require `title` (1–120 characters after trimming) and a non-empty
`statement` through
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
Historical untitled records remain readable with their original identity and
digest. The internal legacy constructor still supports that shape; public
submission tools reject a missing title. Existing records are not rewritten
or backfilled. Local CLI also requires `proofpress propose --title`.

# Claim titles

New proposals require `title` (1–120 characters after trimming) and a non-empty
`statement` through
`claim.propose`, the Python SDK, hosted and local MCP, and `proofpress remote
propose --title`.

- `title`: a concise heading supplied by the proposer.
- `statement`: the complete claim examined for admission; remains required.
- `applicability`: reuse circumstances and limits. Its recorded title is also
  used as a compatibility heading for historical claims that predate required
  claim titles.

Every owner surface uses the same display order: claim title, then the recorded
applicability title for a historical untitled claim, then the statement. When a
concise heading exists, the exact statement remains available in a labeled
disclosure or statement preview. This display fallback does not alter the claim.

Titles are included in claim identity and digest when supplied. Changing a
title produces a new candidate, not a silent edit to an admitted claim.
Historical untitled records remain readable with their original identity and
digest; using their stored applicability title for display does not rewrite or
backfill them. The internal legacy constructor still supports that shape; public
submission tools reject a missing title. Existing records are not rewritten
or backfilled. Local CLI also requires `proofpress propose --title`.

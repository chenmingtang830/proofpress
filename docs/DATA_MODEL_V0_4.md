# Data Model v0.4.0 — Claim lifecycle closure

Data Model v0.4.0 closes a bounded reuse-safety gap without adding a second
source of truth. The append-only `events` history remains authoritative. Claim,
relation, graph, review, receipt, and governed-context views are projections.

## Events and derived state

- `claim_withdrawn` records Owner withdrawal without a replacement.
- `relation_retired` records that an admitted relationship no longer
  participates in current governance. It does not delete the relationship.
- `dependency_invalidated` is derived, not independently asserted.
- A `governance_transaction` atomically contains the logical events produced by
  one reassessment. This gives SQLite, Git, and Memory stores the same
  all-or-nothing replay result.

For `depends_on`, `from` is the dependent and `to` is the required upstream.
If an admitted, non-retired dependency points to an unavailable upstream, the
dependent and every transitive dependent are excluded from governed context.
Cycles fail closed. A dependency or upstream authority/lifecycle change after
the dependent's latest admission makes that admission stale.

`claim.withdraw` and `claim.reassess` are Owner-only, require a note, request
identifier, and expected ledger head. `retain` retires selected direct invalid
dependencies and records fresh Human Review and Admission for the same immutable
claim. It fails if an invalid dependency remains. `request_changes` records the
existing revision request and continues through `revision_of`.

Prior approvals, evidence, withdrawal receipts, and retired relations remain
inspectable. Supersession never redirects a dependency to its replacement.

## Compatibility and privacy

The open-ended `state` and `reason` fields extend the existing context schema.
Agent operations remain read-only with respect to authority. A blocked context
item may expose dependency identifiers and paths only when the requesting actor
can read every claim on that path; otherwise it reports the invalidation without
revealing hidden claim content or identifiers.

## Later, only when measurements justify it

The following disposable read models may be added after real event volume,
cold-start replay time, or read latency crosses an agreed threshold:

- rebuildable `claim_current` and `relation_current` projections;
- a dependency reverse index and impact cache;
- projection checkpoints and full-replay verification.

Deleting these caches must always permit complete reconstruction from `events`.
They cannot become a second authority. v0.4.0 does not add a graph database,
automatic proof sufficiency, AND/OR support logic, weighting, or propagation
scores.

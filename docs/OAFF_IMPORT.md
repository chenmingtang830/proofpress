# OAFF v0.1 hosted candidate intake

Status: authenticated candidate intake only. The public name is AFF — Agent
Findings Format; published v0.1 packages still use `oaff_version` and
`.oaff.json`.

The hosted service accepts exact JSON package bytes at
`POST /v1/oaff/candidates` with `Content-Type: application/json` and an agent
Bearer credential allowed to propose claims. It revalidates that credential,
derives the workspace from the hosted principal, requires that workspace's
review policy, verifies the package with the independent OAFF library, and
stores a candidate or quarantine result in a separate SQLite inbox beside the
hosted database. The package cannot select a workspace. `GET
/v1/oaff/candidates` returns that authenticated workspace's counts and latest
candidate snapshot per immutable Finding revision. `GET
/v1/oaff/candidates/{package_digest}` returns one selected package for review;
a digest from another workspace returns `candidate_not_found`.

The response separates `verification` from `local_authority`, which is always
`none`. Originating admission receipts are untrusted attribution. Intake does
not create a Proofpress claim, run model review, admit a claim, or place the
Finding in governed context. A valid package alone does not satisfy local
approval gates.

`POST /v1/oaff/candidates/{package_digest}/proposals` accepts a JSON
`evidence_map` from every package-local evidence ID to an already submitted
Proofpress retrieval evidence ID in the same workspace. The bridge checks
those local receipt digests against the foreign descriptors, creates a new
local candidate claim, and retains the Finding ID, revision and package digest
as attributed origin metadata. It does **not** project the origin's approval
receipt into local authority. The normal local evaluation and Human Approval
or explicit Owner-policy path still decides reuse. The bridge refuses an older
receipt snapshot, a package with a withdrawal or rejection receipt, or links
that need O5 lifecycle and dependency reconciliation. It never fetches a
source URI or copies the source bytes from the package.

The OAFF Python package is a prerequisite for this optional route. Until the
first versioned OAFF distribution is released, install the public source at
commit `9ce7bdf2ae075c65a872f1656dbf6f7ea20773d9` alongside Proofpress;
the `oaff-import` extra declares the expected package version for later
distribution. The CI integration test installs that exact commit. Absence of
the package returns `oaff_unavailable` instead of accepting unverified bytes.

Example, after configuring a hosted workspace and issuing an agent credential:

```sh
curl -fsS -X POST "$PROOFPRESS_BASE/v1/oaff/candidates" \
  -H "Authorization: Bearer $PROOFPRESS_AGENT_TOKEN" \
  -H 'Content-Type: application/json' \
  --data-binary @finding.oaff.json
```

The request is capped by the hosted server's JSON request size limit. Invalid
packages are quarantined; oversized packages are rejected without retaining
their bytes. Reimporting an identical snapshot is idempotent. A distinct
immutable Finding value under the same revision URI is quarantined. The inbox
is an untrusted staging store and is not an event-ledger replacement.

After independently submitting receiver-local retrieval evidence through the
normal `evidence.submit` operation, a caller can propose the selected package:

```sh
curl -fsS -X POST "$PROOFPRESS_BASE/v1/oaff/candidates/$PACKAGE_DIGEST/proposals" \
  -H "Authorization: Bearer $PROOFPRESS_AGENT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"evidence_map":{"source-1":"evd_REPLACE_WITH_LOCAL_ID"}}'
```

The bridge compares recorded SHA-256 source digests. It does not independently
rehash source bytes, authenticate the originating producer, or decide whether
the local evidence supports the statement. The normal evaluation and local
review must do that work.

Next O4 product slice: an owner decision surface for comparing the foreign
Finding and local evidence before review. The API path has a synthetic
two-workspace handoff test; a real independent producer/receiver and hosted
deployment remain external validation gates.

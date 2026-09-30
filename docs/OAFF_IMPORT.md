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
/v1/oaff/candidates` returns only that authenticated workspace's revision,
snapshot, and quarantine counts.

The response separates `verification` from `local_authority`, which is always
`none`. Originating admission receipts are untrusted attribution. Intake does
not create a Proofpress claim, run model review, admit a claim, or place the
Finding in governed context. Any local proposal must bind locally accessible
evidence and pass the ordinary receiver-side evaluation and Human Approval or
explicit Owner-policy gates. A valid package alone does not satisfy those
gates.

The OAFF Python package is a prerequisite for this optional route. Until the
first versioned OAFF distribution is released, install the public source at
commit `54bf6435530a8f1793111fc24da04186fcf2b88f` alongside Proofpress;
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

Next O4 slice: an owner review surface and an explicit bridge from a selected
candidate to a local evidence-bound proposal. That bridge must never inherit
the origin receipt's authority, must not fetch arbitrary source URIs, and
must prove two-workspace isolation through the full local approval flow.

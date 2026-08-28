OpenWiki witness boundary demo
==============================

This local experiment composes four independent facts:

1. OpenWiki format, page binding, and evidence freshness are checked locally.
2. A producer-origin attestation authenticates only the exact handoff manifest.
3. A governance-decision attestation authenticates only an expected decision,
   policy, and ledger transition.
4. Neither attestation admits an OpenWiki claim into Proofpress context.

The handoff manifest deterministically hashes every selected page and Claims
sidecar, their referenced source files, ancestor indexes, and available
OpenWiki producer metadata. Paths are repository-relative and sorted.

The consumer path uses the real proofpress_witness verifier on a DSSE v1
envelope over an in-toto Statement v1 payload. Demo-only code is limited to
ephemeral Ed25519 key generation, fixture signing, and trust-axis composition.

Run from the repository root:

  python3 examples/openwiki-witness-boundary/run_demo.py

Expected assertions:

  - producer attestation authenticates origin, not decision authority
  - decision attestation authenticates decision authority, not origin
  - a winner-flipped expectation fails
  - exact statement re-verification is idempotent
  - the same statement ID with different signed bytes fails
  - authentic origin does not make stale evidence current
  - Proofpress admission remains not performed
  - offline authority_current remains unknown

Focused tests:

  python3 -m unittest tests.test_openwiki_witness_boundary -v

Trust boundary
--------------

The external trust policy authorizes a key for a profile, tenant, audience, and
principal. The signed predicate key_id must match the DSSE keyid lookup hint.
A signed statement is not an admission, not a bearer capability, and not a
transparency-service inclusion receipt.

# Export one Proofpress claim as OAFF v0.1

Install the optional canonicalization dependency with `pip install -e '.[oaff]'`.
The open format and standalone verifier live at
[only-then-labs/oaff](https://github.com/only-then-labs/oaff).

From a local Proofpress workspace with its claim ledger, run:

```sh
python -m proofpress.oaff_export clm_EXAMPLE \
  --namespace https://your-organization.example/oaff \
  --source evd_EXAMPLE https://your-organization.example/sources/contract-v2 ./contract-v2.pdf \
  --output finding.aff
aff verify finding.aff --evidence EVIDENCE_ID_IN_PACKAGE=./contract-v2.pdf
```

`.aff` is the preferred filename for new packages. Its bytes remain v0.1 JSON
with `oaff_version: "0.1.0"`; older `.oaff.json` files remain readable.

Repeat `--source` for **every** evidence reference on the claim. The package
uses a derived package-local evidence ID, shown in its `finding.evidence`
array, for standalone verification. Source bytes are read locally, hashed,
and checked against the Proofpress retrieval receipt. They are not embedded.
The caller supplies an externally suitable source URI and organization-owned
HTTPS namespace; private workspace paths and raw actor IDs are not copied.
The output describes restricted availability because export does not grant
public access to the source.
Namespaced package extensions record the exact local ledger head and export
time for audit. They do not turn the package into a signed Proofpress history.

The exporter rejects claims without explicit applicability description and
validity conditions, non-retrieval evidence, unavailable or changed source
bytes, and inconsistent claim or retrieval digests. It exports an existing
admission or withdrawal as an **attributed originating receipt** where the
recorded event binds to this claim revision. That receipt has no authority in
the recipient's workspace. OAFF v0.1 does not authenticate the named issuer,
and this exporter does not sign the package. Review the package before sharing:
the statement and applicability may themselves contain private information.

This first exporter treats each immutable Proofpress claim as a separate
Finding. It does not infer revision chains, relation links, evidence support,
or causal outcomes. A subsequent PR can project those only with explicit,
validated identities and authority.

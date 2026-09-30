# Repository structure

This repository is a Python product with two separately built web surfaces,
plus examples and research studies. The canonical production code lives under
`src/proofpress/`; top-level Python modules exist only for compatibility.

## Canonical ownership map

| Path | Owns | May depend on |
|---|---|---|
| `src/proofpress/kernel/` | Governance operations, operation authority classes, policy, projections, and event-store contracts | Standard library and built-in validation profiles; never hosted services or source adapters |
| `src/proofpress/hosted/` | Single-owner hosted control plane, HTTP/MCP boundaries, review policy, and packaged Owner assets | `kernel`, `transports`, and bounded integrations |
| `src/proofpress/transports/` | Client-side HTTP and MCP transport adapters | Public client contracts, not hosted internals |
| `src/proofpress/integrations/` | Optional source translation, evidence-entry, and repository workflow adapters | Public client contracts and validation profiles |
| `src/proofpress/profiles/` | Versioned evidence and advisory-audit validation profiles | Standard library and domain contracts; no provider calls or admission |
| `src/proofpress/legacy/` | Maintained portable-ledger compatibility surface | Must not become a dependency of new product behavior |
| `src/proofpress/client.py` | Supported Python SDK facade | Transports and public operation schema |
| `src/proofpress/cli.py` | Supported `proofpress` command router | Product entry points |
| `web/owner/` | Source for the authenticated Owner workspace | Hosted JSON endpoints |
| `web/landing/` | Public marketing site | No product-runtime dependency |
| `tests/` | Product, storage, transport, CLI, and compatibility tests | Public and intentionally tested internal contracts |
| `deploy/` and `render.yaml` | Provider-neutral and Render deployment configuration | Packaged CLI only |
| `examples/` | Small runnable demonstrations | Supported public interfaces |
| `studies/` | Reproducible research and evaluation harnesses | May exercise public interfaces; results are not product guarantees |

Hosted workspace ownership and legacy deployment defaults are documented in
`docs/WORKSPACE_OWNERSHIP.md`.

## Deliberate compatibility boundaries

- Files such as `src/proofpress_sdk.py` and `src/proofpress_service.py` are
  deprecated forwarding shims declared in `pyproject.toml`. Do not add new
  behavior there.
- `src/proofpress_self_hosted/` and old console aliases remain for the 0.6
  compatibility window. New code and deployment examples use
  `proofpress hosted`.
- `src/proofpress/legacy/` preserves the optional portable artifact ledger.
  New governed-context behavior belongs in the canonical kernel and hosted
  paths, not in legacy.
- `src/proofpress/hosted/static/` is generated from `web/owner/`. Edit the web
  source, run its build/export workflow, and commit the resulting packaged
  assets together.

## Change placement rules

1. Put reusable governance semantics in `kernel`; keep HTTP, HTML, OAuth, and
   provider details outside it.
2. Put external-system translation in `integrations`; do not make the kernel
   import an integration.
3. Keep transport adapters thin. A transport maps requests and errors but does
   not define a second governance lifecycle.
4. Add new public behavior through `proofpress.client` and `proofpress.cli`;
   compatibility shims only forward.
5. Keep studies isolated and explicit about fixtures, model/provider inputs,
   and output locations. A study must not be required to install or run the
   product.
6. Keep generated output out of source directories unless packaging requires
   it; document the generator beside any committed generated asset.

## Service and authority contracts

The existing `proofpress/local-operation/v1alpha1` envelope is the shared
in-process and hosted operation interface. `kernel/operations.py` defines its
parameters and results; `kernel/contracts.py` classifies every operation as
agent, Owner, or local-only. Hosted execution must reject unclassified
operations. Local CLI review is an operator action in a local workspace; the
hosted service additionally authenticates the Owner and binds the actor to the
credential. Neither MCP adapter exposes an Owner operation.

| Boundary | Existing interface | Owner of the decision |
|---|---|---|
| Evidence submission | `evidence.submit` binds a bounded evidence envelope and returns evidence IDs | Kernel validates and appends; integrations only translate source material |
| Verification | `claim.evaluate` and `relation.evaluate` record deterministic checks; `claim.judge` and `relation.judge` record optional advice | Kernel decides check state; an advisory provider cannot admit |
| Admission | `claim.review` and `relation.review` are Owner-only hosted operations; Owner-policy automatic claim admission is an internal hosted path | Kernel enforces lifecycle gates; hosted verifies the human or policy authority |
| Governed retrieval | `context.get`, `context.discover`, and `graph.traverse` return eligible admitted context with staged candidates separate | Kernel projects eligibility; hosted binds the reader identity and workspace |
| Operational audit | `HostedControlPlane.execute_as` emits a bounded `hosted_audit` row after allowed or denied calls | Hosted control plane records actor, operation, outcome, and event head; adapters do not issue audit or authority events |

Repository verification and external experiment manifest validation live in
`profiles`; the repository and Baseten integration modules retain their
existing import paths as adapter and compatibility surfaces. The Jev audit
profile validates a versioned advisory receipt without importing the hosted
provider transport. Existing local CLI execution wiring remains in
`kernel/operations.py`; this slice changes module ownership and authority
classification without a service split or a wire-format change.

## Verification map

- Python product: `python -m unittest discover -s tests -v`
- Owner workspace: `npm --prefix web/owner test`, build, and browser smoke test
- Landing: `npm --prefix web/landing test` and build
- RelayBench contracts: `npm --prefix studies/long-horizon-eval/relaybench run check`
- Distribution: build wheel and sdist, install the wheel into a clean virtual
  environment, then run `proofpress --help`

CI runs all of these gates. Large modules should be split incrementally behind
existing public interfaces; directory clarity does not justify a compatibility-
breaking rewrite.

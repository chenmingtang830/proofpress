# Repository structure

This repository is a Python product with two separately built web surfaces,
plus examples and research studies. The canonical production code lives under
`src/proofpress/`; top-level Python modules exist only for compatibility.

## Canonical ownership map

| Path | Owns | May depend on |
|---|---|---|
| `src/proofpress/kernel/` | Governance operations, policy, projections, and event-store contracts | Python standard library and narrowly declared runtime dependencies |
| `src/proofpress/hosted/` | Single-owner hosted control plane, HTTP/MCP boundaries, review policy, and packaged Owner assets | `kernel`, `transports`, and bounded integrations |
| `src/proofpress/transports/` | Client-side HTTP and MCP transport adapters | Public client contracts, not hosted internals |
| `src/proofpress/integrations/` | Optional evidence-entry and repository adapters | Kernel/public contracts |
| `src/proofpress/profiles/` | Domain-specific evidence validation profiles | Kernel/public contracts |
| `src/proofpress/legacy/` | Maintained portable-ledger compatibility surface | Must not become a dependency of new product behavior |
| `src/proofpress/client.py` | Supported Python SDK facade | Transports and public operation schema |
| `src/proofpress/cli.py` | Supported `proofpress` command router | Product entry points |
| `web/owner/` | Source for the authenticated Owner workspace | Hosted JSON endpoints |
| `web/landing/` | Public marketing site | No product-runtime dependency |
| `tests/` | Product, storage, transport, CLI, and compatibility tests | Public and intentionally tested internal contracts |
| `deploy/` and `render.yaml` | Provider-neutral and Render deployment configuration | Packaged CLI only |
| `examples/` | Small runnable demonstrations | Supported public interfaces |
| `studies/` | Reproducible research and evaluation harnesses | May exercise public interfaces; results are not product guarantees |

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

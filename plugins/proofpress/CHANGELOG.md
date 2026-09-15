# Changelog

## 0.2.0 — 2026-09-15

- Removes the maintainer's personal MCP endpoint from the generic package.
- Requires each Hosted customer or self-hosted operator to configure its own
  assigned `/mcp` endpoint after installing the plugin.
- Keeps the governed-context skill, policy template, Judge criteria, and Human
  Approval boundary unchanged.

## 0.1.0 — 2026-09-08

Initial public package release.

- Bundles `proofpress-governed-context` with its policy template and Judge
  criteria.
- Connects to the OAuth-protected managed Proofpress MCP endpoint.
- Adds explicit, non-overwriting policy initialization.
- Includes portable Agent Plugin metadata plus Codex and Claude Code adapters.
- Does not include approval, policy mutation, credential administration, or
  installation hooks.

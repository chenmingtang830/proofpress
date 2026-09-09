# Proofpress plugin release checklist

The repository is the public source of truth for the `proofpress` plugin.
Marketplace listings are not live until the relevant platform accepts them.

## Preflight

1. Update the same semantic version in the portable manifest, Claude manifest,
   and both marketplace records.
2. Validate package files and parity tests. Test Codex/ChatGPT, Claude Code,
   and Cursor against a non-production workspace.
3. Confirm the production MCP resource and OAuth discovery document are live.
4. Review `PLUGIN_PRIVACY.md` and `PLUGIN_TERMS.md`, then confirm their public
   GitHub URLs resolve from the release branch.
5. Confirm the listing makes no approval, security, retention, or marketplace
   availability claim beyond what has been verified.

## Publish

- **OpenAI / Codex:** register the managed MCP in ChatGPT Developer Mode, keep
  the generated `plugin_asdk_app_...` identifier out of source control until
  platform review requires it, then add the registered mapping through the
  platform submission flow. Submit the portable package to the shared public
  Plugins Directory.
- **Claude Code:** submit `proofpress` from the public GitHub marketplace using
  the official Claude Code submission form. The fallback source is
  `.claude-plugin/marketplace.json` in this repository.
- **Cursor:** submit the portable Agent Plugin from `plugins/proofpress` to the
  Cursor Marketplace, using the same hosted MCP endpoint and privacy/terms
  URLs.

Do not describe any directory listing as approved or installed until that
platform confirms it. GitHub remains the direct installation fallback.

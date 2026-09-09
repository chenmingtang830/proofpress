# Proofpress plugin

Proofpress governs whether an evidence-backed, agent-produced claim may be
reused downstream. This plugin bundles the governed-context workflow with the
hosted Proofpress MCP server. It is not a memory store, an approval bot, or an
owner administration client.

## What is included

- `proofpress-governed-context`: retrieves eligible context, prepares bounded
  proposals, and stops for Human Approval.
- A default repository policy template at
  `skills/proofpress-governed-context/assets/context-policy.yaml`.
- One preconfigured OAuth-protected Streamable HTTP MCP server at
  `https://proofpress-personal-hosted.onrender.com/mcp`. This is the
  maintainer's private reference service, not a public hosted workspace.

## First use

Ask the agent to **Initialize a Proofpress policy for this repository**. The
skill creates `.proofpress/context-policy.yaml` only when that file is absent;
it never overwrites or repairs an existing policy. Review, narrow, and commit
the generated copy before relying on it for proposal selection.

Before connecting, choose a workspace: use a Hosted endpoint that Proofpress
has provisioned for your team, or replace the preconfigured MCP URL with your
own self-hosted `/mcp` endpoint. Installing this package alone does not create
an account, workspace, or ledger, and unprovisioned users are not authorized to
use the reference endpoint.

Complete the OAuth flow when the client requests it. Each client receives a
separate, revocable agent credential. The plugin never asks for an owner or
recovery credential.

## Authority boundary

The MCP server can submit bounded evidence, propose claims, retrieve governed
context, traverse bounded lineage, and return review links. It cannot approve,
admit, reject, supersede, mutate policy, or administer credentials. Human
Approval remains in the Owner surface.

## Self-hosted Proofpress

The default server is a private Proofpress reference endpoint. Self-hosted
operators can use this same skill and replace the MCP URL with their own `/mcp`
endpoint; provisioned Hosted users should use their team's endpoint instead.
See [Remote MCP](../../docs/REMOTE_MCP.md).

See [Plugin privacy](../../docs/PLUGIN_PRIVACY.md) and
[Plugin terms](../../docs/PLUGIN_TERMS.md).

## Direct-install fallback

Until a directory listing is approved, install from this repository:

- **Codex / ChatGPT:** add `chenmingtang830/proofpress` as a marketplace with
  its `.agents/plugins` directory, then install `proofpress` from that
  marketplace.
- **Claude Code:** add the repository as a marketplace, then install
  `proofpress@proofpress-plugins`.
- **Cursor:** clone this repository and add `plugins/proofpress` as a local
  plugin.

Each client should show one `proofpress` plugin, the
`proofpress-governed-context` skill, and one remote MCP server. Complete the
OAuth flow in that client; never copy another user's token or agent
credentials.

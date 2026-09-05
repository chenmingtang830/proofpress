# Remote MCP

Proofpress can expose its safe agent surface as a public Streamable HTTP MCP
endpoint at `/mcp`. The endpoint uses OAuth 2.1 authorization-code flow with
PKCE and is backed by the same hosted operation contract as the Python SDK,
CLI, and local stdio bridge.

## Connect

Install the `proofpress-governed-context` skill in the target project before
adding the MCP server. Run the matching setup from the root of that project.

### Codex

```sh
mkdir -p .agents/skills/proofpress-governed-context
curl -fsSL \
  https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/SKILL.md \
  -o .agents/skills/proofpress-governed-context/SKILL.md
```

### Claude Code

```sh
mkdir -p .claude/skills/proofpress-governed-context
curl -fsSL \
  https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/SKILL.md \
  -o .claude/skills/proofpress-governed-context/SKILL.md
```

### Cursor

```sh
mkdir -p .cursor/skills/proofpress-governed-context
curl -fsSL \
  https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/SKILL.md \
  -o .cursor/skills/proofpress-governed-context/SKILL.md
```

These are project-level installations, so the skill travels with the
repository. Review the downloaded `SKILL.md` before committing it. Then add the
remote MCP server for the same client.

Install the maintained customer policy template once per target repository:

```sh
mkdir -p .proofpress
curl -fsSL \
  https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/assets/context-policy.yaml \
  -o .proofpress/context-policy.yaml
```

Commit and customize `.proofpress/context-policy.yaml` with narrow examples of
the durable decisions, validated conclusions, integration contracts,
reproducible results, and incident learnings that belong in that repository's
Proofpress workflow. The core skill reads this file before choosing `Draft
only` or `Propose`.

This is an agent-side proposal-selection policy, not a server authorization
policy. It may narrow what an agent proposes, but cannot weaken server checks,
credential isolation, lifecycle rules, or Human Approval. Customers configure
this file instead of forking the Proofpress-maintained core skill.

If the workspace enables the advisory LM Judge, copy and adapt the maintained
[`judge-criteria.md`](../.agents/skills/proofpress-governed-context/assets/judge-criteria.md)
in Hosted Admin. Keep it separate from the repository intake policy: Judge
criteria assess evidence support and never replace Human Approval.

Open `/connect` on the deployed Proofpress origin and copy the displayed MCP
URL into a client that supports remote Streamable HTTP servers. The client
discovers the authorization server and opens `/authorize` in a browser.

Paste the credential issued for that specific agent or device. Owner and
recovery credentials are rejected. After authorization, the client receives a
short-lived access token and a rotating refresh token; the original agent
credential is not returned to the client.

The generic server configuration contains no secret:

```json
{
  "mcpServers": {
    "proofpress": {
      "url": "https://proofpress.example.com/mcp"
    }
  }
}
```

Copy-paste setup examples:

```bash
# Codex
codex mcp add proofpress --url https://proofpress.example.com/mcp
codex mcp login proofpress

# Claude Code
claude mcp add --transport http --scope user proofpress \
  https://proofpress.example.com/mcp
# Then run /mcp inside Claude Code and authorize Proofpress.
```

In Cursor, create a remote MCP server named `proofpress` with the same `/mcp`
URL and complete the OAuth prompt. Each client should receive its own revocable
agent credential.

The local stdio bridge remains available for clients without remote HTTP or
OAuth support.

## Authorization endpoints

- `GET /.well-known/oauth-protected-resource`
- `GET /.well-known/oauth-authorization-server`
- `POST /register`
- `GET|POST /authorize`
- `POST /token`
- `POST /mcp`

OAuth clients are public clients. Redirect URIs must use HTTPS or loopback
HTTP, authorization requires PKCE S256, codes are single-use and expire after
five minutes, access tokens expire after 30 minutes, and refresh tokens rotate
on every use. Access tokens are audience-bound to the exact MCP resource URL.
Revoking the underlying Proofpress agent credential invalidates all derived
OAuth sessions immediately.

## Authority boundary

Remote MCP exposes evidence submission, conclusion proposal, governed-context
retrieval, bounded graph and lineage reads, and review links. It never exposes
Human Approval, policy mutation, credential administration, or recovery.

`proofpress_propose_conclusion` accepts `reproposal_of` when an agent is
submitting a corrected successor to a rejected conclusion. The referenced
predecessor must exist, be rejected, and use the same scope. Proofpress records
the lineage and supplies the prior rejection reason to the advisory Judge, but
does not reopen, overwrite, or approve either conclusion. The new candidate
still requires a fresh human decision.

## Discovering governed context

An agent does not need to know a scope string before it can find relevant
knowledge. `proofpress_discover_context(task?)` first applies the workspace and
actor visibility checks, then returns only admitted, current context cards. A
card is deliberately small and YAML-frontmatter-shaped: `title`,
`description`, `when_relevant`, `keywords`, and `validity_conditions`. Task
words rank those visible cards; this ranking is a discovery aid, never an
authorization decision.

New proposals may provide that card as `applicability` and omit `scope`.
`scope` remains an optional exact filter for legacy callers and existing
records. The hosted credential supplies the authenticated workspace and agent
identity; new proposals do not configure per-knowledge reader lists. Historical
rows that already contain a restrictive `allowed_actors` value retain that
legacy restriction until an owner explicitly migrates them. Semantic matching
never broadens access. After selecting a card, the agent still reads governed
context and its receipt before relying on the conclusion.

`proofpress_get_lineage` follows one conclusion backward through `supports`,
`derived_from`, and `bound_as` edges to the original source records.
`proofpress_traverse_graph` follows admitted conclusion-to-conclusion relations
with server-enforced actor, scope, state, depth, and result limits.

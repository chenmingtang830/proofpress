# Remote MCP

Proofpress can expose its safe agent surface as a public Streamable HTTP MCP
endpoint at `/mcp`. The endpoint uses OAuth 2.1 authorization-code flow with
PKCE and is backed by the same hosted operation contract as the Python SDK,
CLI, and local stdio bridge.

## Connect

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

`proofpress_get_lineage` follows one conclusion backward through `supports`,
`derived_from`, and `bound_as` edges to the original source records.
`proofpress_traverse_graph` follows admitted conclusion-to-conclusion relations
with server-enforced actor, scope, state, depth, and result limits.

# Pioneer POC onboarding

This POC uses one private Proofpress workspace for Pioneer. Start with MCP; do
not modify Pioneer's application or pipeline for the first validation run.

## What each person gets

- Kelton receives the owner credential and uses the owner web workspace for
  review, Judge advice, policy, and Human Approval.
- Claude Code, Codex, and Cursor each receive a different revocable agent
  credential. Never reuse one credential across clients.
- Agents can submit bounded evidence, propose conclusions, read review status,
  and retrieve governed context. They cannot approve, reject, change policy, or
  administer credentials.

The POC URL is `https://proofpress-kelton-poc.onrender.com`.

## Ten-minute agent setup

Use Python 3.11 or newer in a small virtual environment:

```sh
git clone https://github.com/chenmingtang830/proofpress.git
cd proofpress
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[mcp]'
```

Store the credential for this client in its local secret store or shell
environment. Do not commit it to the repository or paste it into prompts:

```sh
export PROOFPRESS_MCP_TOKEN='<credential for this client only>'
proofpress-mcp \
  --base-url https://proofpress-kelton-poc.onrender.com \
  --review-base-url https://proofpress-kelton-poc.onrender.com
```

Add that command as a local STDIO MCP server named `proofpress` in Claude Code,
Codex, or Cursor, forwarding `PROOFPRESS_MCP_TOKEN` from the local environment.
For Codex, local MCP configuration belongs in `~/.codex/config.toml`, or in a
trusted project's `.codex/config.toml` when the server should be project-scoped.

After restarting the client, call `proofpress_capabilities`. Confirm that the
reported principal matches the client you are configuring and that
`human_approval_available` is `false`.

## First real workflow

1. Ask the agent to retrieve context for the agreed POC scope. An empty result
   is correct before anything has been approved.
2. Give it one real Pioneer experiment result. Keep raw files in Pioneer's
   system; submit only the minimum evidence projection, locator, and digest
   needed to support the conclusion.
3. The agent calls `proofpress_submit_evidence`, then
   `proofpress_propose_conclusion`, using stable idempotency keys.
4. The agent calls `proofpress_get_review_link` and sends the URL to Kelton.
5. Kelton signs in to the owner workspace, inspects deterministic checks, runs
   the advisory LM Judge, and makes the Human Approval decision himself.
6. Start a fresh agent session with a different client credential and call
   `proofpress_get_context` for the same scope. Only admitted, current, in-scope
   conclusions should appear.

## When to integrate with Pioneer's system

Do not build a native integration until the MCP loop has succeeded on several
real work items. If repeated use shows that evidence is produced
programmatically, integrate the same hosted operation contract through the
Python client or HTTPS endpoint. Keep Proofpress downstream of Pioneer's
systems: Pioneer retains raw artifacts and traces; Proofpress receives bounded
evidence projections and governs which resulting conclusions may be reused.

## POC success checks

- No Richard workspace data, claims, credentials, or audit events are present.
- The three agent credentials resolve to three distinct principals and can be
  revoked independently.
- An agent cannot perform Human Approval or credential administration.
- Judge output is visibly advisory and does not admit the conclusion.
- A fresh successor agent retrieves the admitted conclusion without receiving
  blocked candidates or raw private evidence.


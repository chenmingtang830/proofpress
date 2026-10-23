# Remote MCP

Proofpress can expose its safe agent surface as a public Streamable HTTP MCP
endpoint at `/mcp`. The endpoint uses OAuth 2.1 authorization-code flow with
PKCE and is backed by the same hosted operation contract as the Python SDK,
CLI, and local stdio bridge.

## Localhost first use

For an empty workspace on your own machine, follow the
[localhost quick start](LOCALHOST_QUICKSTART.md). It uses the full Owner UI and
SQLite server on `127.0.0.1:7334`, with the same OAuth agent boundary at `/mcp`.
Install the skill/plugin in your research project and connect to that server;
the synthetic quickstart's generated stdio configuration targets a separate
Git-backed demo ledger.

## Recommended plugin installation

The public [`proofpress` Agent Plugin](../plugins/proofpress/README.md) bundles
the governed-context Skill and the same policy template. Prefer it when the
client supports plugins, then add the Hosted or self-hosted `/mcp` endpoint
assigned to that team:

- **Codex / ChatGPT:** add this repository's `.agents/plugins` marketplace and
  install `proofpress` from the Plugins Directory.
- **Claude Code:** add this repository as a marketplace, then install
  `proofpress@proofpress-plugins`.
- **Cursor:** install the portable package from the Cursor Marketplace after
  its listing is approved, or import `plugins/proofpress` locally for testing.

Marketplace review is independent for each client. Until a listing is approved,
the public repository is the direct installation fallback; do not claim that a
directory listing is live before the platform confirms it.

The generic plugin does not bundle a customer MCP URL. Installing it does not
create a workspace or connection. A provisioned Hosted customer must configure
its assigned `/mcp` URL and agent authorization; a self-hosted operator uses
the same plugin with its own `/mcp` URL.

## Hosted workspace setup

After installing the skill and connecting once, manage capture guidance in
**Admin -> Knowledge rules**. Built-in capture defaults are usable immediately;
a local `.proofpress/context-policy.yaml` is optional. The current skill reads
the workspace's versioned guidance through `proofpress_get_capture_policy` at
run start. Existing clients need the updated skill to pick up this behavior;
an MCP connection alone does not make an older skill read new configuration.

Admin separates **API keys & credentials**, **Knowledge rules** and **Verification settings**. Knowledge rules only guide what agents should capture. Verification settings
contain required evidence checks, optional model advice, and the separate
owner-controlled approval gate. Capture rules guide
proposal selection; they do not authorize admission. The review gate still
requires an explicit owner choice before governed work begins. Model advice
and external processing are optional.

Local source paths and agent scheduling remain in the execution environment.
A local context policy can add stricter project restrictions. Conflicts must
be reported, never silently resolved by weakening hosted rules.

## Manual connection or self-hosting

Install the `proofpress-governed-context` skill in the target project before
adding the MCP server. Run the matching setup from the root of that project.

### Codex

```sh
skill_root=.agents/skills/proofpress-governed-context
mkdir -p "$skill_root/assets" "$skill_root/scripts" "$skill_root/references"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/SKILL.md -o "$skill_root/SKILL.md"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/assets/context-policy.yaml -o "$skill_root/assets/context-policy.yaml"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/assets/judge-criteria.md -o "$skill_root/assets/judge-criteria.md"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/scripts/initialize_policy.py -o "$skill_root/scripts/initialize_policy.py"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/scripts/prepare_evidence.py -o "$skill_root/scripts/prepare_evidence.py"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/references/capture-input.md -o "$skill_root/references/capture-input.md"
```

### Claude Code

```sh
skill_root=.claude/skills/proofpress-governed-context
mkdir -p "$skill_root/assets" "$skill_root/scripts" "$skill_root/references"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/SKILL.md -o "$skill_root/SKILL.md"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/assets/context-policy.yaml -o "$skill_root/assets/context-policy.yaml"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/assets/judge-criteria.md -o "$skill_root/assets/judge-criteria.md"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/scripts/initialize_policy.py -o "$skill_root/scripts/initialize_policy.py"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/scripts/prepare_evidence.py -o "$skill_root/scripts/prepare_evidence.py"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/references/capture-input.md -o "$skill_root/references/capture-input.md"
```

### Cursor

```sh
skill_root=.cursor/skills/proofpress-governed-context
mkdir -p "$skill_root/assets" "$skill_root/scripts" "$skill_root/references"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/SKILL.md -o "$skill_root/SKILL.md"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/assets/context-policy.yaml -o "$skill_root/assets/context-policy.yaml"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/assets/judge-criteria.md -o "$skill_root/assets/judge-criteria.md"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/scripts/initialize_policy.py -o "$skill_root/scripts/initialize_policy.py"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/scripts/prepare_evidence.py -o "$skill_root/scripts/prepare_evidence.py"
curl -fsSL https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/references/capture-input.md -o "$skill_root/references/capture-input.md"
```

These are project-level installations, so the skill travels with the
repository. Review the downloaded `SKILL.md` before committing it. Then add the
remote MCP server for the same client.

For optional repository-specific restrictions, the user must explicitly ask an
agent to initialize a local policy. The installed Skill previews its bundled template first and uses its helper
to create `.proofpress/context-policy.yaml` only with `--apply`; it refuses
symbolic links, partial targets, replacements, and unknown policy versions.
Do not substitute a path-based shell script for that helper. Commit and
customize the created policy with narrow examples of the durable decisions,
validated claims, integration contracts, reproducible results, and incident
learnings that belong in that repository's Proofpress workflow. The core skill
reads this file before choosing `Draft only` or `Propose`.

This is an agent-side proposal-selection policy, not a server authorization
policy. It may narrow what an agent proposes, but cannot weaken server checks,
credential isolation, lifecycle rules, or owner admission controls. Customers configure
this file instead of forking the Proofpress-maintained core skill.

If the workspace enables the advisory LM Judge, copy and adapt the maintained
[`judge-criteria.md`](../.agents/skills/proofpress-governed-context/assets/judge-criteria.md)
in Hosted Admin. Keep it separate from the repository intake policy: Judge
criteria assess evidence support and never admit a claim by themselves. Owners
may separately enable workspace-wide automatic admission for qualifying new
claims; resulting system decisions remain distinct from human approval.

Open `/connect` on the deployed Proofpress origin for the complete setup guide.
Select Codex, Claude Code, or Cursor; install the project-level skill with the
displayed commands, then add that workspace's MCP server. Admin also exposes
the Codex skill installation commands inline after issuing an agent key.
The client discovers the authorization server and opens `/authorize` in a browser.

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

Keep the CLI process that initiated authorization open until the browser returns
to its loopback callback. Submit the Proofpress authorization form once. If the
browser stalls or cannot reach the callback, do not keep clicking the form:
return to `/mcp` in Claude Code or rerun `codex mcp login proofpress` and start a
fresh authorization. Authorization codes are short-lived and single-use, so an
old browser page cannot repair a stopped callback listener. After the MCP client
reports that it is connected, start a fresh agent conversation if the existing
conversation still has a stale tool registry.

### Automatic deterministic checks

Hosted claim submission records deterministic checks before returning, even
when LM review is manual or off. The proposal result includes `evaluation`;
an execution failure is reported separately as `evaluation_error` without
discarding the submitted candidate. Retries reuse current checks and recover
a missing evaluation after an interrupted submission. These checks cover
evidence integrity, source receipts and reuse boundaries; they do not establish
that a prediction is correct. They neither call a model nor grant approval.
Older candidates can still be checked or rechecked from Review.

### Readable source details

After binding evidence to a claim, use the hosted
`proofpress_describe_evidence` tool to record the original filename, the source
section or spreadsheet cells, and the relevant named values. Pass the actual
claim/evidence IDs and the evidence digest from `proofpress_get_review_receipt`.
Use `details: {filename, location, fields: [{name, value}]}`; never substitute a
local path for the filename or invent a source field. For a derived projection,
name the original file and identify the derivation in its location.

Descriptions are attributed, append-only presentation metadata. They do not
replace the source URI, quote, locator, evidence digest, checks or Owner
authorization. The original evidence and claim remain immutable. Identical
retries reuse the description; different replacements are refused. The
`evidence.describe` operation requires a readable claim proposed by the caller and evidence-submission
permission (existing submission credentials do not need rotation). Review
receipts return labels separately in `evidence_details`.

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

Remote MCP exposes evidence submission, claim proposal, approved and separately
staged context retrieval, bounded graph and lineage reads, and review links.
Staged context is for unapproved drafts only and cannot be recorded as governed
reliance. It never exposes
Human Approval, policy mutation, credential administration, or recovery.

`proofpress_propose_claim` accepts `reproposal_of` when an agent is
submitting a corrected successor to a rejected claim. The referenced
predecessor must exist, be rejected, and use the same scope. Proofpress records
the lineage and supplies the prior rejection reason to the advisory Judge, but
does not reopen, overwrite, or approve either claim. The new candidate
must bind at least one evidence reference not present on the predecessor and
include a non-empty `qualifiers.reproposal_response` explaining how that new
evidence addresses the recorded rejection. It still requires a fresh human
decision.

## Discovering governed context

An agent does not need to know a scope string before it can find relevant
knowledge. `proofpress_discover_context(task?)` first applies the workspace and
actor visibility checks, then returns only admitted, current context cards. A
card is deliberately small and YAML-frontmatter-shaped: `title`,
`description`, `when_relevant`, `keywords`, and `validity_conditions`. Task
words rank those visible cards; this ranking is a discovery aid, never an
authorization decision.

New proposals may provide that card as `applicability` and omit `scope`.
`title` and `description` are strings; `when_relevant`, `keywords`, and
`validity_conditions` are arrays of strings, so one sentence must still be
wrapped in a list. Both MCP transports publish this shape in the tool's input
schema. Over the local stdio server a rejected call comes back as an error
result whose text is `Error executing tool <name>: ` followed by the reason.
For an argument that breaks the published schema, the SDK names the field and
what it expected. For any other rejected call (an evidence URL where an `evd_`
ID belongs, an unknown profile, an empty card) the reason starts with a stable
code: `invalid_tool_request` for a check in the MCP layer, otherwise the
operation envelope's code such as `operation_rejected`, followed by the
envelope's details when there are any and by `(retryable)` when a retry may
succeed. A failure of the server's own environment (a transport error, an I/O
error on the workspace) returns only its code and a fixed phrase; the detail
stays in the server log. An unexpected exception in the server still returns
only the generic line. The hosted transport returns the same reasons in its
error result under the single code `invalid_tool_request`.
`scope` remains an optional exact filter for legacy callers and existing
records. The hosted credential supplies the authenticated workspace and agent
identity; new proposals do not configure per-knowledge reader lists. Historical
rows that already contain a restrictive `allowed_actors` value retain that
legacy restriction until an owner explicitly migrates them. Semantic matching
never broadens access. After selecting a card, the agent still reads governed
context and its receipt before relying on the claim.

`proofpress_get_lineage` follows one claim backward through `supports`,
`derived_from`, and `bound_as` edges to the original source records.
`proofpress_traverse_graph` follows admitted claim-to-claim relations
with server-enforced actor, scope, state, depth, and result limits.

## Evidence envelope and locators

`proofpress_submit_evidence` publishes the `proofpress/retrieval-evidence/v1`
envelope in its input schema, on the hosted and the local stdio server alike
(`proofpress.mcp_schemas`). The evidence `locator` says where the quote sits in
the source, as one of five kinds:

- `text_span`: `start`, `end` (character offsets; `end - start` is the quote's
  length), `text_digest`
- `page_span`: `page_start`, `page_end` (1-based), `page_digest`
- `section_span`: `section_id`, `section_digest`, `page_start`, `page_end`
- `spreadsheet_cell`: `sheet`, `cell` (an A1 address), `cell_digest`, and
  optionally `previous_source_content_digest` with `previous_cell_digest`
- `json_pointer`: `value` (an RFC 6901 pointer), and nothing else

For example, a quote on page 2 of a PDF:

```json
{"kind": "page_span", "page_start": 2, "page_end": 2,
 "page_digest": "sha256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"}
```

Digests are supplied by the submitting adapter; Proofpress records them and
does not recompute them. The published schema states a selection of the
kernel's rules; others (a page range's order, a text span's length, a cell's
bounds, paired history digests, integers written as 2.0) are left to the
kernel, which validates every payload. The schema tells clients more about the
locator than before; what the kernel accepts is unchanged.
On the stdio server the payload may instead be an experiment-profile payload
(`schema_version` `proofpress/profile/experiment/v1`, with `profile=experiment`).


### Time-bounded research context

`proofpress_get_context` and `proofpress_discover_context` accept an optional
`temporal_window` object. For example, the 30 New York calendar dates before
October 20, 2026 are:

```json
{"temporal_window":{"since":"2026-09-20","until":"2026-10-20","timezone":"America/New_York"}}
```

`since` is inclusive and `until` exclusive. Filtering uses a finding's
`qualifiers.effective_date`, falling back to `qualifiers.report_date` only when
no effective date was provided. It never uses proposal/import time to make old
observations appear recent. Missing or invalid dates are excluded from a dated
query; omit the window to inspect undated findings or older open questions.
Discovery cards include a descriptive `temporal` object; full claims retain
original qualifiers and evidence.

For a strict information-availability cutoff, add `known_before` as an ISO date
or timezone-aware timestamp. This requires `qualifiers.original_first_seen_at`;
unknown first-known time is excluded, not inferred from the report or import.
Date-only first-known values are conservatively available after that calendar
day ends. This does not replay past approval state or establish a point-in-time
backtest: authority eligibility is always evaluated now. Windows never delete
history or approve findings. Use short finding titles and structured dates;
retain dates in statements when they define a comparison or forecast horizon.

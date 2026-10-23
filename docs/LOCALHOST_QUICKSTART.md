# Localhost: from an empty workspace to Claude Code

Run your own Proofpress workspace on your laptop, let Claude Code read selected
research files, review its findings in your browser, then retrieve an approved
finding in a fresh conversation.

This uses the full Owner UI with a local SQLite database. The command is named
`proofpress hosted`, but the server below binds only to your own machine.
The synthetic `proofpress quickstart --ui` demo is a separate workspace.

## Before you start

- macOS or Linux, or a Linux shell inside Windows WSL2. The commands below use
  a POSIX shell; they are not PowerShell commands. Run Proofpress and Claude
  Code in the same environment. With WSL, use its forwarded browser port.
- [Python 3.11+](https://www.python.org/downloads/),
  [Git](https://git-scm.com/downloads), and
  [uv](https://docs.astral.sh/uv/getting-started/installation/).
- [Claude Code](https://code.claude.com/docs/en/setup) installed and signed in
  to an account allowed to process your chosen research material.
- Start with one small project and 1–3 permitted files. No Docker, Node build,
  cloud account, or separate Proofpress model key is needed for human review.

**Where data goes:** Proofpress stores the submitted evidence excerpts, claims,
review history and metadata in the local database. Source files stay in your
project. Claude Code processes what it reads under your Claude configuration;
localhost does not make Claude offline. Optional Proofpress AI-assisted checks
send bounded findings/evidence to the provider you explicitly configure.

## 1. Install and create your workspace

In a normal terminal:

```sh
uv tool install --with "mcp>=2,<3" "git+https://github.com/chenmingtang830/proofpress.git"
uv tool update-shell
```

Open a new terminal if `proofpress` is not found. Check the tools:

```sh
proofpress hosted --help
claude --version
```

Create the local data directory and bootstrap **once**. Run this yourself in a
private terminal; do not delegate it to an agent:

```sh
umask 077
mkdir -p "$HOME/.local/share/proofpress"
proofpress hosted --database "$HOME/.local/share/proofpress/workspace.db" \
  bootstrap --workspace-id workspace:research --owner-principal human:owner
```

The JSON output includes `token` (your Owner sign-in credential) and
`recovery_secret`. Save both in your password manager. They are shown once.
Keep them out of Git, chat and agent configuration. The database path is where
knowledge persists; it is independent of your research project directory.

**Checkpoint:** the bootstrap returned `workspace:research`. On subsequent
starts, skip bootstrap and use the same database. An “already bootstrapped”
error means you should start the existing workspace, not delete it.

## 2. Start the server and configure human review

Keep this terminal running:

```sh
proofpress hosted --database "$HOME/.local/share/proofpress/workspace.db" \
  serve --host 127.0.0.1 --port 7334
```

Open **[http://127.0.0.1:7334](http://127.0.0.1:7334)** and sign in with the
Owner `token`. Use this same origin everywhere, including MCP; do not alternate
between `localhost` and `127.0.0.1` during authorization.

In another terminal, check server readiness:

```sh
curl --fail --silent --show-error http://127.0.0.1:7334/readyz
```

Expect `database_integrity: "ok"`. An empty Home is normal: this workspace has
no findings yet.

In **Admin → Verification settings**:

1. Review the criteria, edit them for your project, and click **Save review criteria**.
2. For a first local run without a model key, leave **AI-assisted checks** off.
   Keep automatic approval off. Saving criteria confirms the human-review path;
   deterministic evidence checks still run.
3. Reload the page and confirm your saved criteria/version.

In **Admin → API keys & credentials**, issue a key for **Agent** with identity
`agent:claude-research` and a recognizable key name such as `Claude Code · laptop`.
Save this one-time **agent** key privately for browser authorization in step 3.
It is different from your Owner credential and from a model-provider API key.

**Checkpoint:** review criteria are saved and a separate Agent credential exists.

## 3. Connect Claude Code to this same workspace

Open a second terminal **at the root of your own research project**, not the
Proofpress source checkout. Create a project folder first if you do not have one.
Use `pwd` to confirm where you are. These commands install the maintained workflow
and add a connection private to you in this project:

```sh
claude plugin marketplace add chenmingtang830/proofpress
claude plugin install proofpress@proofpress-plugins --scope local
claude mcp add --transport http --scope local proofpress \
  http://127.0.0.1:7334/mcp
claude
```

If you already have a `proofpress` MCP entry, inspect it with `claude mcp get
proofpress` first. Reuse it if it targets this exact workspace; resolve a mismatch
before adding a duplicate. The plugin contains the governed-context skill, not
a workspace URL or credentials.

Inside Claude Code, run `/mcp`, select `proofpress`, and complete authentication.
In the browser, enter the **Agent** key you just issued. Keep Claude Code open
until the browser callback completes. Submit the authorization form once.
No key belongs in the MCP command or a committed `.mcp.json`.

Start a fresh Claude conversation after connecting. Paste:

```text
Use the installed proofpress-governed-context skill. Check the Proofpress
connection and report the workspace ID, authenticated agent principal, capture
policy and review policy. Expect workspace:research and agent:claude-research.
Retrieve relevant governed context, keeping unapproved staged_context separate.
Do not read Owner/recovery credentials or change settings. Do not submit a test
claim yet. If the connection, identity or review policy is wrong, stop and explain.
```

**Checkpoint:** `/mcp` reports connected; the capabilities identify the intended
workspace and Agent. No governed context in a brand-new workspace is expected.
Connection alone does not make the skill run: explicitly invoke it for this first task.

Client command references: [Claude MCP](https://code.claude.com/docs/en/mcp),
[plugin installation](https://code.claude.com/docs/en/discover-plugins).
If plugins are unavailable, install the maintained project skill using the
[manual Claude Code instructions](REMOTE_MCP.md#claude-code) before adding MCP.

## 4. Ingest selected files into evidence-backed findings

There is no generic file-upload button or automatic folder crawler in this
release. Claude Code reads your chosen files locally and submits **bounded
evidence projections and candidate findings** through MCP. Importing a file or
passing checks does not approve a finding.

Put your allowed files in an `inputs/` folder in the research project. Keep
private inputs, derived extracts and local credentials out of Git according to
your project's data policy. Begin with text/Markdown or a small CSV; add PDFs
and Excel after the first loop works.

| File | What to preserve |
|---|---|
| Markdown/text notes | Exact quote, section or character span, source version digest. |
| CSV/JSON experiment results | Column names, units, sample size, baseline and a precise location; keep a named derived projection if needed. |
| PDF paper | DOI/version, exact page and passage. If extraction/OCR is unavailable, report the gap; do not invent text. |
| XLSX workbook | Sheet, cell/range, actual named values and workbook version. |
| Images, raw sequencing data, large instrument files | Keep originals in their source system; supply a checked summary or selected results with provenance. |

Paste this into Claude Code from that project:

```text
Use proofpress-governed-context for this project. Read the current workspace
capture guidance and any local context policy, then retrieve relevant eligible
context. Inspect only the files in ./inputs that I have selected for this task.

First list each file, whether you can read it, and the source locations you will
use. Do not recurse outside ./inputs, fetch additional sources, or install an
extraction dependency without explaining what is needed. Keep originals intact.

Extract at most 3 atomic candidate findings that could help the next research
session. For each, preserve the exact source/version SHA-256, bounded quote or
selected values, a precise supported locator, method/conditions, limitations
and intended applicability. Compute digests from actual bytes/text, not guesses.
Identify derived projections honestly and retain them locally. Use the MCP tool
schema to submit evidence; bind the returned evd_ IDs when proposing each claim.
Use stable idempotency keys so a retry does not create duplicates.

Return each claim ID, review URL, checks/advice state, source location and gaps.
Do not generalize beyond the evidence or call an unapproved candidate knowledge.
Stop for my human review; do not approve, change policy or use Owner credentials.
If extraction or evidence binding cannot be verified, report the gap and do not
submit that finding.
```

For biology research, preserve organism/cell line, assay, treatment/dose/time,
controls, replicate count and uncertainty where the source supplies them.
A paper's reported result is an attributed literature finding, not independent
replication or clinical guidance. Start with public papers or permitted,
de-identified aggregate results; exclude patient records and sensitive raw data.

**Checkpoint:** the local UI shows the candidates and their bound evidence.
A readable source label should let you locate the original passage or values.

## 5. Review, then prove reuse in a fresh conversation

Open **Review** in the local UI. For each finding, compare its statement,
applicability and evidence against the source. Inspect checks and any advice.
Approve only supported findings; reject or request changes when needed. With
AI-assisted checks off, handle requested revisions by passing the recorded
feedback to Claude Code and asking for a linked revision with adequate evidence.

Then start a **fresh Claude Code conversation in the same project** and paste:

```text
Use proofpress-governed-context. Before planning the next experiment or literature
review, discover and retrieve relevant eligible governed context from Proofpress.
Show the admitted claim IDs, evidence and applicability limits. Keep staged
candidates separate and identify which approved findings you actually use.
Suggest one next action supported by that context. If no eligible finding exists,
say so; do not reconstruct approval from the previous conversation.
```

**Done means:** selected source → bound evidence → candidate → checks → your
review decision → retrieval and appropriate use in a fresh conversation. A
successful connection or a synthetic demo alone does not establish this loop.

## Keep using it

Stop the server with `Ctrl-C`. Restart with the step 2 command and **the same
database path**. Files and approved findings survive the server restart.

| Setting | Where to change it |
|---|---|
| Which findings to capture | Admin → Knowledge rules; local restrictions are optional. |
| Review criteria, AI provider and approval policy | Admin → Verification settings; only the human Owner saves changes. |
| Agent access/revocation | Admin → API keys & credentials. |
| Which source files Claude reads | Your task prompt and research project. |

To add optional project restrictions, explicitly ask Claude to initialize a
Proofpress policy for this repository, review the template and version your
changes. Do not edit the installed core skill. If you enable Proofpress AI checks,
configure persistent encrypted provider-key storage first; see
[self-hosting configuration](SELF_HOSTING.md#workspace-review-policy-and-provider-credentials).
Choose the provider and processing consent yourself. AI advice and automatic
approval are separate settings.

Create an integrity-checked backup using a new filename each time:

```sh
proofpress hosted --database "$HOME/.local/share/proofpress/workspace.db" \
  backup "$HOME/.local/share/proofpress/workspace-backup-$(date +%Y%m%dT%H%M%S).db"
```

Copy backups to a protected location on another device. Back up source files
separately. If using encrypted provider-key storage, retain its encryption key
privately as well. See [backup verification and restore](SELF_HOSTING.md) before
relying on recovery.

## Troubleshooting

| Symptom | Next action |
|---|---|
| `uv` or Python missing | Follow the prerequisite installation links; then open a new terminal. |
| `proofpress: command not found` | Run `uv tool update-shell`, reopen the terminal, and check `uv tool list`. |
| Port 7334 already in use | Stop the other process you recognize or select another port; update browser and MCP URL together. |
| Browser cannot connect / MCP unavailable | Keep the server terminal running; check `/readyz`. Run both tools on the same host/environment. |
| Already bootstrapped | Reuse the existing database and saved Owner credential; skip bootstrap. |
| OAuth callback stalls | Keep the initiating Claude process open; restart auth from `/mcp`. Old codes are single-use; do not repeatedly submit the old form. |
| Unauthorized / credential rejected | Use this workspace's Agent key for OAuth; Owner/recovery credentials cannot authorize MCP. |
| Policy not configured / submissions blocked | Have the Owner save review criteria in Verification settings, then retry. |
| No relevant tools in a conversation | Check `/mcp`, plugin installation and project folder; start a fresh conversation and explicitly invoke the skill. |
| No governed context | Normal before an eligible finding has been approved; inspect the candidate receipt and review decision. |
| PDF/Excel cannot be read | Use an approved local extraction tool or an inspected text/CSV projection; preserve original provenance and disclose the gap. |

For support, share the command, sanitized error, OS, package revision and claim
ID if relevant. Keep credentials and private research material out of screenshots
and logs.

### Capture format troubleshooting

Before submitting a selected file excerpt, ask the connected agent to read
`proofpress_get_capture_schema` and follow the installed governed-context skill's
[capture input guide](../.agents/skills/proofpress-governed-context/references/capture-input.md).
The bundled `prepare_evidence.py` builds the envelope and real hashes locally
from selected source, extracted text, quote and extraction configuration files.
For a slide, use `page_span` with 1-based slide bounds and that slide's text
hash. Input `quote` and `locator` both go inside `payload.evidence`.

Ordinary paper/slide findings omit `profile`. `profile=experiment` is for
recorded reproducible runs and requires `qualifiers.experiment`, including run
identity. Missing run metadata means draft work, not an excuse to fabricate
fields or bypass a required profile. MCP rejects retrieval format and experiment
claim qualifier errors before submission, without consuming a key. Read back
uncertain or executed attempts before retrying; do not keep changing keys to
learn the format. Reconnect MCP after upgrading the server and update the
installed plugin/skill so both sides expose the current contract.

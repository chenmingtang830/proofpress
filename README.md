[//]: # (ob:6ec771b4)
<p align="center">
  <img src="assets/logo.svg" alt="Proofpress logo" width="88" height="88">
</p>

[//]: # (ob:de7999eb)
# Proofpress

[//]: # (ob:e667d986)
Proofpress is a verifiable `log.md` for knowledge work: a shared history of who
changed what, when, and why, checked against the artifact itself.

[//]: # (ob:0e0e9d9a)
Agents can produce a document quickly, but the reasoning that shaped its final
form is usually scattered across chat sessions, Slack, meetings, and somebody's
memory. Git is excellent when the work already lives in Git; most knowledge
artifacts do not. Proofpress keeps the accepted version history and consequential
decisions attached to a Markdown or static HTML artifact so that history can
travel with it.

[//]: # (ob:169d8523)
## Status

[//]: # (ob:d6f9f208)
Proofpress is a V0 reference implementation. The CLI is usable and its portable
artifact behaviors are covered by black-box tests, but the embedded carrier and
command interfaces may still change before a stable release. The npm package is
published under the `next` tag while these interfaces settle.

[//]: # (ob:19210f53)
## Install the alpha

[//]: # (ob:989f25ec)
Proofpress keeps its zero-dependency Python engine and adds a thin npm launcher
plus repository setup command. Python 3 and Git are required:

[//]: # (ob:7b197ac1)
```sh
npm install --save-dev proofpress@next
npx --no-install proofpress --version
npx --no-install proofpress setup --agent codex
```

[//]: # (ob:5ae48e1b)
`setup` installs a package-aware adapter and writes
`.proofpress/manifest.json`. It is idempotent and supports `codex`, `claude`,
`cursor`, or `all`. Portable history remains opt-in per artifact.

[//]: # (ob:2b655d31)
To add a visible, transparent distribution mark to a repository README:

[//]: # (ob:d4916c37)
```sh
npx --no-install proofpress setup --agent codex --badge README.md
```

[//]: # (ob:5796ae98)
The badge says that revision provenance uses Proofpress; it is not an
instruction for agents to download or execute software. Installed adapters use
`npx --no-install`, so an agent can use an existing local installation but
cannot silently fetch the package.

[//]: # (ob:e7b4f799)
## Single-file install

[//]: # (ob:d8cafbd3)
Proofpress is a single Python file with no third-party runtime dependencies:

[//]: # (ob:0b5b4916)
```sh
git clone https://github.com/chenmingtang830/proofpress.git
cd proofpress
python3 proofpress.py --help
```

[//]: # (ob:166fd594)
To use it in another repository, vendor `proofpress.py` at that repository's
root and install the matching adapter from [`skills/`](skills/).

[//]: # (ob:949eb6a5)
## What “portable” means

[//]: # (ob:2173502c)
Turn portability on once:

[//]: # (ob:c44f6768)
```sh
python3 proofpress.py policy proposal.md portable
```

[//]: # (ob:79416c44)
The setting is sticky. Later accepted revisions refresh a compact, hidden
capsule inside the carrier file. Send the original file to a collaborator and
their agent can inspect and import its history without access to your Git repo,
chat session, or Proofpress ledger ref.

[//]: # (ob:af7113fa)
```sh
python3 proofpress.py inspect proposal.md
python3 proofpress.py import proposal.md
python3 proofpress.py log proposal.md
```

[//]: # (ob:bfc931ca)
The capsule is declarative data, not agent instructions. It is tamper-evident
for accidental drift and inconsistent rewrites, but V0 does not claim signed
authorship or protection from wholesale malicious replacement.

[//]: # (ob:839fc8a1)
Portable carriers include a non-rendering discovery marker with
`Verifiable revision history by Proofpress` and the project URL. The capsule's
canonical discovery object also names `proofpress@next`. An agent may explain
this provenance and offer installation, but must obtain user consent before
downloading or executing anything.

[//]: # (ob:cc095bd4)
## Static HTML carrier

[//]: # (ob:e6463f5e)
Proofpress also supports static `.html` and `.htm` artifacts. `anchor` writes a
stable `data-proofpress-id` onto supported visible blocks (headings, paragraphs,
list items, block quotes, preformatted blocks, table cells, and figure captions).
The metadata marker lives in `<head>`; a portable capsule is a non-executing
`application/vnd.proofpress+json` data block before `</body>`.

[//]: # (ob:b8abc9df)
```sh
python3 proofpress.py policy launch-plan.html portable
python3 proofpress.py anchor launch-plan.html
python3 proofpress.py snapshot launch-plan.html --kind agent --author codex \
  --why "made the accepted review scope explicit"
python3 proofpress.py verify launch-plan.html
```

[//]: # (ob:00768820)
This is a static-HTML carrier MVP, not a framework or CMS integration. Proofpress
does not yet promise round-trip preservation through React/Vue builds, HTML
sanitizers, editors, or CMS pipelines; if they strip transport data, the file
degrades to an ordinary HTML artifact — `identify` can still recognize it
locally, but its provenance does not come back.

[//]: # (ob:226a29fd)
## What gets recorded

[//]: # (ob:cfc1c3aa)
Proofpress records accepted artifact versions, their computed block changes,
explicit actor roles, the reason for the change, and consequential rejected
directions when the authoring agent supplies them. The account is checked
against the actual artifact diff.

[//]: # (ob:5e0b34ed)
It does not automatically store raw prompts, transcripts, tool traces, casual
brainstorming, or every save. A fallback hook checks Git candidates and current
paths already admitted to the ledger, including Git-ignored artifacts. It can
preserve an otherwise missed version, but identifies itself only as
`recorded_by`; it does not guess who wrote the content or why. Harness skills
can also capture a specific existing file before an agent edits it, keeping
unattributed human drift separate from the agent's revision.

[//]: # (ob:d8387b0b)
## Privacy modes

[//]: # (ob:5df13acf)
Each artifact has one policy:

[//]: # (ob:3b52e3b3)
- `portable`: future accepted versions refresh the embedded capsule.
- `local`: versions stay in the local/Git ledger; the current capsule is

[//]: # (ob:126978a2)
  removed.

[//]: # (ob:0890e114)
- `ignored`: future capture is skipped.

[//]: # (ob:c6642117)
Switching from portable to local cannot recall copies already sent. Re-enabling
portable starts a clean lineage at the current body, so private-interval actors,
reasons, rejected paths, event IDs, and omitted-event counts do not leak.

[//]: # (ob:18995a53)
For a one-off history-free copy, use:

[//]: # (ob:f28051ef)
```sh
python3 proofpress.py clean proposal.md --output proposal-clean.md
```

[//]: # (ob:bfac82a8)
## Core workflow

[//]: # (ob:706dcea3)
```sh
python3 proofpress.py anchor proposal.md
python3 proofpress.py snapshot proposal.md --kind agent --author codex \
  --produced-by codex --recorded-by codex \
  --attribution-basis harness_attested \
  --note "incorporated review" --claims /tmp/claims.json \
  --why "the team chose the smaller launch scope"
python3 proofpress.py verify proposal.md
```

[//]: # (ob:33e05aa8)
Use `--rejected` only for consequential dead branches that future collaborators
should not repeat. Source code stays in Git; Proofpress is for Markdown and
static HTML knowledge artifacts.

[//]: # (ob:59769c11)
## Merged lineage and stripped copies

[//]: # (ob:91a8deb1)
When one document merges several Proofpress-managed sources, record the
upstream references — identity, head version, and digest, never copied
history:

[//]: # (ob:100c5aa7)
```sh
python3 proofpress.py merge-lineage proposal.md \
  --from research-a.md --from research-b.md
```

[//]: # (ob:144c3d60)
When a copy lost its metadata and capsule (pasted as plain text, reformatted,
sanitized), the ledger can still recognize it by a deterministic content
fingerprint:

[//]: # (ob:28dec45f)
```sh
python3 proofpress.py identify pasted-copy.md
```

[//]: # (ob:b705ac38)
`identify` answers identity — "this is that artifact" — on a machine holding
the ledger. It does not restore history or prove the copy was never altered,
and a copy with wording changes intentionally does not match.

[//]: # (ob:2a955c60)
## Surfaces

[//]: # (ob:8deed5b3)
- `proofpress.py`: zero-dependency engine and CLI.
- npm package: thin cross-platform launcher and idempotent repository setup.
- `refs/proofpress/ledger`: local/Git-backed ledger, separate from branches.
- `skills/`: Claude Code, Codex, Cursor, and Pi authoring contracts plus

[//]: # (ob:1f7d312f)
  best-effort fallback hooks.

[//]: # (ob:605a678d)
- Embedded portable capsule: path-independent handoff outside Git.

[//]: # (ob:820f39ab)
Start with the [documentation index](docs/README.md). The executable behavior is
defined by the [Portable Artifact V0 contract](docs/PORTABLE_ARTIFACT_SPEC.md),
with its disclosure limits in
[Privacy Boundaries for Portable Artifacts](docs/PRIVACY_AND_DISCLOSURE.md).

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzU1NmIxMTVkZTcxMWIwY2QzM2VlZDI2MCIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)

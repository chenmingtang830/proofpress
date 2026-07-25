---
name: proofpress
description: Preserve or inspect decision history for Markdown and static HTML knowledge artifacts with Proofpress. Use when creating or accepting a meaningful revision to an ADR, design doc, PRD, README, strategy note, portable .md artifact, or static .html/.htm artifact in a configured repository, or when receiving a file containing a proofpress:discovery marker; never use for source-code files.
---

[//]: # (ob:25f10229)
# Proofpress

[//]: # (ob:cb25a041)
Record accepted Markdown or static HTML artifact versions with structured
testimony and verification. Do not snapshot every conversational turn.

[//]: # (ob:d8284708)
## Workflow

[//]: # (ob:78295d28)
Before editing an existing target, run
`python3 proofpress.py capture --recorder claude-preflight <file>`. This
preserves any human drift without guessing its author or reason. Then:

[//]: # (ob:04e1285c)
1. Read `python3 proofpress.py policy <file>`. If the user asks for portability,

[//]: # (ob:0fab4251)
   run `policy <file> portable` once; it remains sticky. If Git history exists
   without a ledger, run `ingest <file>`.

[//]: # (ob:a5e7461c)
2. Preserve carrier-native anchors while editing: Markdown uses

[//]: # (ob:01348595)
   `[//]: # (ob:xxxxxxxx)`; static HTML uses `data-proofpress-id`. Run
   `anchor <file>` and inspect inherited/new/gone IDs.

[//]: # (ob:ac191e68)
3. Write claims JSON with one honest entry per touched or removed block; do not

[//]: # (ob:29b54f6f)
   enumerate untouched blocks.

[//]: # (ob:4623b792)
4. Snapshot the accepted version with `--why`, claims, and explicit actors:

[//]: # (ob:c89d4269)
   ```sh
   python3 proofpress.py snapshot <file> --kind agent --author claude \
     --produced-by claude --recorded-by claude \
     --attribution-basis harness_attested --note "<changelog>" \
     --claims <claims.json> --why "<actual reason>" \
     --rejected "<consequential dead branch — reason>"
   ```

[//]: # (ob:3b3f299e)
   Omit `--rejected` unless the dead branch matters to future collaborators.
   Never infer it from casual discussion or include raw prompts/transcripts.

[//]: # (ob:64c98298)
5. Run `verify <file>` and report its output verbatim. Never re-snapshot merely

[//]: # (ob:0928adea)
   to force green.

[//]: # (ob:e96a23df)
For an incoming file with a `proofpress:discovery` marker but no local CLI,
tell the user it carries verifiable revision history, show the marker's
canonical project URL, and ask whether to install `proofpress`. Never
download or execute it without explicit consent. If the CLI is available, run
`inspect` before trusting the capsule and then `import`.

[//]: # (ob:3bec4947)
Fallback `capture` records only `recorded_by`; it cannot know authorship or
reasoning. Never snapshot source-code files.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzhmOWYxNjA4MjZlMzM2YTQ2ZWI2MmJkNCIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)

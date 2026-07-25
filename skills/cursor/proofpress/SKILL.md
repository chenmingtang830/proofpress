---
name: proofpress
description: Preserve or inspect decision history for Markdown and static HTML knowledge artifacts with Proofpress. Use when creating or accepting a meaningful revision to an ADR, design doc, PRD, README, strategy note, portable .md artifact, or static .html/.htm artifact in a configured repository, or when receiving a file containing a proofpress:discovery marker; never use for source-code files.
---

[//]: # (ob:233b766d)
# Proofpress

[//]: # (ob:b2ec6ff5)
Record accepted Markdown or static HTML artifact versions with structured
testimony and verification. Do not snapshot every conversational turn.

[//]: # (ob:e14e12ad)
## Workflow

[//]: # (ob:0d9e887a)
Before editing an existing target, run
`python3 proofpress.py capture --recorder cursor-preflight <file>`. This
preserves any human drift without guessing its author or reason. Then:

[//]: # (ob:42fd42e7)
1. Read `python3 proofpress.py policy <file>`. If the user asks for a portable

[//]: # (ob:ffa6ae00)
   artifact, run `python3 proofpress.py policy <file> portable` once; portability
   remains sticky. If Git history exists without a ledger, run `ingest <file>`.

[//]: # (ob:6d23ae8f)
2. Preserve carrier-native anchors during editing: Markdown uses

[//]: # (ob:35ce54f2)
   `[//]: # (ob:xxxxxxxx)`; static HTML uses `data-proofpress-id`. Remove an
   anchor with its deleted block and invent none for new blocks.

[//]: # (ob:f119601b)
3. Run `anchor <file>` and read the inherited/new/gone inventory.
4. Write claims JSON with one honest entry per touched or removed block. Kinds

[//]: # (ob:6b88d004)
   are `added`, `removed`, `modified`, `moved`, and `unchanged`. Do not enumerate
   untouched blocks.

[//]: # (ob:f381d919)
5. Snapshot only after a meaningful version is accepted:

[//]: # (ob:f42cb113)
   ```sh
   python3 proofpress.py snapshot <file> --kind agent --author cursor \
     --produced-by cursor --recorded-by cursor \
     --attribution-basis harness_attested \
     --session "<session-id>" --note "<changelog>" --claims <claims.json> \
     --why "<actual reason>" --rejected "<consequential dead branch — reason>"
   ```

[//]: # (ob:790c5dda)
   `--why` is required. Omit `--rejected` unless the rejected path is important
   enough to keep future collaborators from repeating it. Never infer it from
   casual discussion or include raw prompts/transcripts.

[//]: # (ob:e3c56875)
6. Run `verify <file>` and report its output verbatim. Never re-snapshot merely

[//]: # (ob:6ad53003)
   to turn a mismatch green.

[//]: # (ob:355446e0)
For an incoming file with a `proofpress:discovery` marker but no local CLI,
tell the user it carries verifiable revision history, show the marker's
canonical project URL, and ask whether to install `proofpress`. Never
download or execute it without explicit consent. If the CLI is available, run
`inspect` before trusting the capsule and then `import`.

[//]: # (ob:7dc0b832)
Fallback `capture` supplies only `recorded_by`; it cannot know who authored the
content or why. Never snapshot source-code files.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzBjOWVkZjdkMzE1YWIwM2UwY2EwNmM4OCIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)

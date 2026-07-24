[//]: # (ob:e43408a0)
# Project instructions

[//]: # (ob:bbe579fd)
## Proofpress: ledger Markdown and static HTML knowledge artifacts

[//]: # (ob:34d3dbf3)
For accepted, meaningful revisions to Markdown or static HTML knowledge
artifacts—never source code—close this loop. Do not snapshot every
conversational turn.

[//]: # (ob:1be95c90)
1. Read `python3 proofpress.py policy <file>`. If the user asks for portability,

[//]: # (ob:950c5740)
   run `policy <file> portable` once; it remains sticky. Use `ingest <file>` for
   Git history not yet represented in the ledger.

[//]: # (ob:406bcda8)
2. Preserve carrier-native block anchors while editing: Markdown uses invisible

[//]: # (ob:3ce94304)
   `ob` markers; static HTML uses `data-proofpress-id`. Then run `anchor <file>`
   and inspect inherited/new/gone IDs.

[//]: # (ob:f5265244)
3. Write claims JSON with one honest item per touched or removed block. Do not

[//]: # (ob:2d919674)
   enumerate untouched blocks.

[//]: # (ob:fd4e6530)
4. Snapshot with `--why`, claims, and explicit actors (`requested_by`,

[//]: # (ob:1a021614)
   `produced_by`, `edited_by`, `recorded_by`, and `attribution_basis` when
   known). Omit `--rejected` unless a consequential dead branch should stop
   future collaborators from repeating it. Never capture raw prompts or
   transcripts.

[//]: # (ob:b2cfcee6)
5. Run `verify <file>` and report its output verbatim. Never re-snapshot just to

[//]: # (ob:94b5efc1)
   force green.

[//]: # (ob:32ab4de4)
For incoming portable files, run `inspect` and then `import`. Fallback `capture`
records only `recorded_by`; it cannot know authorship or reasoning.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzc5NWU0MTc0YjU2ZDdkNWNmODkxOTNlYSIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)

[//]: # (ob:c350cb3a)
<!-- Append to AGENTS.md — the Proofpress contract for Codex agents. -->

[//]: # (ob:51ac24b5)
## Proofpress: ledger Markdown and static HTML knowledge artifacts

[//]: # (ob:10265f5d)
For accepted, meaningful revisions to Markdown or static HTML knowledge
artifacts—never source code—close this loop. Do not snapshot every
conversational turn.

[//]: # (ob:af9efd22)
Before editing an existing target, run
`python3 proofpress.py capture --recorder codex-preflight <file>`. This
preserves any human drift as a separate version without guessing its author or
reason. Then:

[//]: # (ob:d181cc6e)
1. Read `python3 proofpress.py policy <file>`. If the user asks for portability,

[//]: # (ob:6c0f813b)
   run `policy <file> portable` once; it remains sticky. Use `ingest <file>` for
   Git history not yet represented in the ledger.

[//]: # (ob:0ba00342)
2. Preserve carrier-native block anchors while editing: Markdown uses invisible

[//]: # (ob:0b96e11b)
   `ob` markers; static HTML uses `data-proofpress-id`. Then run `anchor <file>`
   and inspect inherited/new/gone IDs.

[//]: # (ob:55bb7174)
3. Write claims JSON with one honest item per touched or removed block. Do not

[//]: # (ob:3b3c1156)
   enumerate untouched blocks.

[//]: # (ob:311b1408)
4. Snapshot with `--why`, claims, and explicit actors:

[//]: # (ob:08f435e4)
   ```sh
   python3 proofpress.py snapshot <file> --kind agent --author codex \
     --produced-by codex --recorded-by codex \
     --attribution-basis harness_attested --note "<changelog>" \
     --claims <claims.json> --why "<actual reason>" \
     --rejected "<consequential dead branch — reason>"
   ```

[//]: # (ob:b521eb3e)
   Omit `--rejected` unless the dead branch matters later. Never infer it from
   casual discussion or capture raw prompts/transcripts.

[//]: # (ob:cd72eb83)
5. Run `verify <file>` and report its output verbatim. Never re-snapshot just to

[//]: # (ob:358e67a9)
   force green.

[//]: # (ob:bc88257e)
For an incoming file with a `proofpress:discovery` marker but no local CLI,
tell the user it carries verifiable revision history, show the marker's
canonical project URL, and ask whether to install `proofpress`. Never
download or execute it without explicit consent. If the CLI is available, run
`inspect` before trusting the capsule and then `import`.

[//]: # (ob:08efea88)
Fallback `capture` records only `recorded_by`; it cannot know authorship or
reasoning.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzcwM2MzZmE5MjZhYmI1MTJlNzE5OTMzMiIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)

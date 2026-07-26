[//]: # (ob:5cd87791)
# proofpress

[//]: # (ob:095b959e)
For accepted, meaningful revisions to Markdown or static HTML knowledge
artifacts—never source code—close this loop. Do not snapshot every
conversational turn.

[//]: # (ob:211b5d98)
Before editing an existing target, run
`python3 proofpress.py capture --recorder pi-preflight <file>`. This preserves
any human drift without guessing its author or reason. Then:

[//]: # (ob:87ce54bb)
1. Read `python3 proofpress.py policy <file>`. If the user asks for portability,

[//]: # (ob:72f291a2)
   run `policy <file> portable` once; it remains sticky. Use `ingest <file>` for
   Git history not yet represented in the ledger.

[//]: # (ob:85972ea6)
2. Preserve carrier-native block anchors while editing: Markdown uses invisible

[//]: # (ob:b9f8ef49)
   `ob` markers; static HTML uses `data-proofpress-id`. Then run `anchor <file>`
   and inspect inherited/new/gone IDs.

[//]: # (ob:6f0d23b1)
3. Write claims JSON with one honest item per touched or removed block. Do not

[//]: # (ob:28f53262)
   enumerate untouched blocks.

[//]: # (ob:abd7c833)
4. Snapshot with `--why`, claims, and explicit actors:

[//]: # (ob:2c10e48d)
   ```sh
   python3 proofpress.py snapshot <file> --kind agent --author pi \
     --produced-by pi --recorded-by pi \
     --attribution-basis harness_attested --note "<changelog>" \
     --claims <claims.json> --why "<actual reason>" \
     --rejected "<consequential dead branch — reason>"
   ```

[//]: # (ob:4386e1e7)
   Omit `--rejected` unless the dead branch matters later. Never infer it from
   casual discussion or capture raw prompts/transcripts.

[//]: # (ob:dd7291a6)
5. Run `verify <file>` and report its output verbatim. Never re-snapshot just to

[//]: # (ob:8ac28d76)
   force green.

[//]: # (ob:2f7730eb)
For an incoming file with a `proofpress:discovery` marker but no local CLI,
tell the user it carries verifiable revision history, show the marker's
canonical project URL, and ask whether to install `proofpress`. Never
download or execute it without explicit consent. If the CLI is available, run
`inspect` before trusting the capsule and then `import`.

[//]: # (ob:19334051)
For parallel portable copies of the same artifact, preserve every input and run
`merge-plan TARGET --from COPY...`. Apply compatible block changes, ask the
user only about reported semantic conflicts, then `anchor` the resolved target,
write merge-relative claims, run `merge TARGET --from COPY...` with explicit
actors/reason, and `verify`. Different artifact IDs or portable lineages are
ingredients; use `merge-lineage` for them.

[//]: # (ob:72680124)
Fallback `capture` records only `recorded_by`; it cannot know authorship or
reasoning.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2M3Y2UwZDE1Yjg2YmI0MmJkMjg0MzRmYyIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)

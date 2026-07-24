[//]: # (ob:df70df88)
# Proofpress harness adapters

[//]: # (ob:93121540)
The skill captures rich decision context when an accepted Markdown or static
HTML artifact version is still fresh. The hook is only a best-effort fallback. `ingest`
backfills Git history, and the embedded capsule carries portable history beyond
Git.

[//]: # (ob:1744e48a)
| Layer | What it knows | Attribution rule |
|---|---|---|
| Skill | accepted version, claims, why, consequential rejection | supplies known actor roles and basis |
| Hook / `capture` | Git candidates, admitted ledger paths, or explicit files | supplies only `recorded_by` |
| `ingest` | committed content and Git author | attributes from Git metadata |
| Portable capsule | admitted records attached to the artifact | preserves recorded fields; invents none |

[//]: # (ob:50c32349)
## Shared contract

[//]: # (ob:666c5555)
Before editing an existing target, run `capture --recorder
<harness>-preflight <file>` so any human drift becomes a separate unattributed
version. Then:

[//]: # (ob:a2f15f7d)
1. Work only on Markdown or static HTML knowledge artifacts, never source code.
2. Read the artifact policy. Enable `portable` once when requested; it stays on

[//]: # (ob:23c62cea)
   until explicitly changed.

[//]: # (ob:7109fe56)
3. Preserve carrier-native block anchors (Markdown `ob` markers; static HTML

[//]: # (ob:f8ee70a6)
   `data-proofpress-id`), run `anchor`, and write honest claims for touched or
   removed blocks.

[//]: # (ob:9d481ea6)
4. Snapshot accepted, meaningful versions—not every turn or save—with `--why`

[//]: # (ob:9710997f)
   and explicit known actors.

[//]: # (ob:c8f43a25)
5. Use `--rejected` only for consequential dead branches. Never infer rejected

[//]: # (ob:41bb2485)
   paths from casual discussion or store raw prompts/transcripts.

[//]: # (ob:3991a868)
6. Run `verify` and report its output verbatim. A mismatch is evidence, not a

[//]: # (ob:a08bfb00)
   reason to manufacture another snapshot.

[//]: # (ob:a8bc86e1)
7. On receipt of a portable artifact, run `inspect` before `import`.

[//]: # (ob:f5f3a858)
## Install

[//]: # (ob:8a9fcf71)
The npm installer is the recommended path. It installs package-aware adapters
that use `npx --no-install`, so agents never download the package implicitly:

[//]: # (ob:5ee2d540)
```sh
npm install --save-dev proofpress@next
npx --no-install proofpress setup --agent codex
```

[//]: # (ob:3328131b)
Use `--agent claude`, `--agent cursor`, or `--agent all` for the other supported
harnesses. Add `--badge README.md` only when the repository owner wants a
visible Proofpress provenance mark.

[//]: # (ob:041482f5)
For a vendored `proofpress.py`, install adapters manually:

[//]: # (ob:0e468706)
- Claude Code: copy `claude-code/proofpress/` to `.claude/skills/` and merge

[//]: # (ob:225dd61c)
  `claude-code/hooks-example.json` into `.claude/settings.json`.

[//]: # (ob:3e5fba6b)
- Codex: append `codex/AGENTS-snippet.md` to `AGENTS.md` and merge

[//]: # (ob:3ef5e70c)
  `codex/config-hooks.toml` into the Codex configuration.

[//]: # (ob:9d561c7d)
- Cursor: copy `cursor/proofpress/` to `.cursor/skills/proofpress/` or

[//]: # (ob:9cddddf2)
  `.agents/skills/proofpress/`, then start a new Agent chat.

[//]: # (ob:2202e132)
- Pi: install `pi/proofpress-skill.md`; `pi/extension-skeleton.ts` is an

[//]: # (ob:cc2d6144)
  intentionally untested extension sketch whose event API should be checked
  against the installed Pi version.

[//]: # (ob:c883ac9d)
Adapters expect `proofpress.py` at the repository root.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2U3NGJlMDlhOWQyOGYxODU1ZGI0YTAwNyIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)

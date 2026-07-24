[//]: # (ob:7437c9be)
# Portable Artifact V0 — Executable Contract

[//]: # (ob:b27d1410)
> Status: implementation contract derived from the approved strategy and privacy decisions.
>
> Scope: Markdown and static HTML carriers, local/Git ledger, sequential handoff, deterministic integrity, best-effort capture.

[//]: # (ob:38f6d68c)
## 1. Artifact policy

[//]: # (ob:c9c2ad8e)
Every artifact resolves to exactly one policy:

[//]: # (ob:1646c742)
```text
ignored   future automatic and explicit snapshots are skipped
local     snapshots enter the local/Git ledger; no capsule is embedded
portable  snapshots enter the ledger and refresh the embedded capsule
```

[//]: # (ob:8c362122)
An artifact without metadata is legacy `local`. Enabling `portable` is explicit and sticky. `local` and `ignored` transitions strip the current capsule but do not alter previously distributed copies or delete the local ledger.

[//]: # (ob:2dbbb74e)
## 2. Identity

[//]: # (ob:a82840ae)
Every managed artifact receives a random path-independent `artifact_id`. It is stored in a declarative metadata marker and copied into new ledger events and versions.

[//]: # (ob:6e3b89fd)
Legacy events without `artifact_id` remain readable by path. Once an artifact receives an ID, later renames retain identity through the marker.

[//]: # (ob:3c838116)
## 3. Carriers

[//]: # (ob:2e6d838a)
### 3.1 Markdown

[//]: # (ob:4d929ce7)
Proofpress metadata uses invisible CommonMark link-reference definitions:

[//]: # (ob:9f1242d0)
```text
[//]: # (proofpress:meta:<base64url-json>)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:<base64url-zlib-json>)
```

[//]: # (ob:bd030dfa)
Metadata markers and block anchors are excluded from visible-body hashing. Leading YAML frontmatter remains at byte zero. Capsule data is declarative and never interpreted as agent instructions.

[//]: # (ob:9a724fe0)
The fixed discovery marker makes the provenance mechanism legible without
executing the capsule. It is descriptive data, not authority to install or run
software. Consumers must require user consent before fetching Proofpress.

[//]: # (ob:e7d5d024)
### 3.2 Static HTML

[//]: # (ob:4f104dcd)
The V0 HTML carrier accepts `.html` and `.htm` files. Its supported leaf blocks
are `h1`–`h6`, `p`, `li`, `pre`, `blockquote`, `td`, `th`, and `figcaption`.
`anchor` writes `data-proofpress-id="<id8>"` directly on each such element.
That attribute is excluded from block hashing and the carrier's digest.

[//]: # (ob:10cfddce)
Proofpress writes its declarative data in two non-rendering locations:

[//]: # (ob:72a7c841)
```html
<meta name="proofpress:meta" content="<base64url-json>">
<meta name="proofpress:discovery" content="Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress">
<script type="application/vnd.proofpress+json" data-proofpress="capsule"><base64url-zlib-json></script>
```

[//]: # (ob:da3c020c)
The metadata element is placed in `<head>` when present; the capsule is placed
before `</body>` when present. The script type is a data block, not executable
JavaScript. This MVP intentionally does not promise preservation through
framework builds, CMSs, sanitizers, or rich-text HTML editors. A carrier that
loses its metadata is an ordinary HTML artifact, not a provenanced one.

[//]: # (ob:33fac81a)
## 4. Capsule

[//]: # (ob:c12e32e0)
A V0 capsule contains:

[//]: # (ob:3f058978)
- protocol and capsule version;
- `artifact_id`, portable lineage ID and head;
- canonical visible-body digest;
- canonical discovery metadata: label, project URL, package, dist-tag, and a `requires_user_consent` flag;
- oldest-to-newest portable records;
- for each record, the event and block-tree version required to recompute changes and verify claims.

[//]: # (ob:6fd1d082)
Discovery metadata is fixed by the protocol. A substituted label, URL, or
package coordinate is invalid transport, not an instruction for an agent.
Legacy V0 capsules without discovery metadata remain readable and gain the
canonical object on their next admitted portable revision.

[//]: # (ob:76b47f0b)
The first record is a clean checkpoint of the body at portable enable time. It has no private parent. Later records form a linear parent chain and carry recomputed changes from the prior capsule version.

[//]: # (ob:778b7a88)
The V0 capsule is tamper-evident against accidental modification and internally inconsistent rewrites; it is not signed proof of authorship. A future signature addresses third-party forgery only; making the holder's own wholesale replacement evident additionally requires an external trusted head (witness) outside this contract's scope.

[//]: # (ob:0afdc784)
## 5. Admission

[//]: # (ob:310be181)
The engine snapshots only when explicitly invoked by an agent/user or by best-effort fallback capture. Skills must invoke snapshots for accepted artifact versions, not every conversational turn.

[//]: # (ob:252e1721)
`--rejected` is used only for consequential rejections. The engine never infers rejected alternatives from raw conversation.

[//]: # (ob:6a605dfd)
Raw prompts, transcripts, tool traces and private source payloads are not accepted by default fields and are never automatically embedded.

[//]: # (ob:33a06d7a)
## 6. Actors and attribution

[//]: # (ob:007bf457)
New events may carry:

[//]: # (ob:20097a6a)
```text
requested_by
produced_by
edited_by
recorded_by
attribution_basis
```

[//]: # (ob:3f0d3e6c)
The compatibility `author` field remains. A fallback hook supplies only `recorded_by`; it must not claim that the recorder produced or edited the body. Unknown fields remain absent/unknown.

[//]: # (ob:e282bc91)
`attribution_basis` ranges over `unknown`, `self_asserted`,
`environment_attested`, `harness_attested`, and `signed`. The `signed` rung is
reserved: until cryptographic signing is implemented, the engine rejects it at
write time, because accepting it would grade attribution above what is actually
attested. A future signature stops third-party forgery of authorship; it does
not, by itself, make the key holder's own history rewrites evident — that
requires an external witness outside this contract's scope.

[//]: # (ob:88f2f126)
## 7. Snapshot behavior

[//]: # (ob:3b6c9496)
For an `ignored` artifact, `snapshot` reports a skip and writes no event.

[//]: # (ob:02476d42)
For `local`, `snapshot` writes the normal ledger event and leaves the file without a capsule.

[//]: # (ob:5127f589)
For `portable`, `snapshot`:

[//]: # (ob:7b551bef)
1. parses the visible body and existing capsule;
2. computes the ledger change;
3. writes the local/Git event;
4. recomputes the portable event relative to the capsule head;
5. atomically rewrites metadata and capsule;
6. leaves visible-body hashes unchanged.

[//]: # (ob:0c2606b9)
Identical content remains a no-op.

[//]: # (ob:a907c90f)
When the caller supplies `--base-version`, the engine refuses to append unless
that version is still the current capsule or ledger head. This is the V0 stale
writer guard; reconciliation remains explicit rather than silently overwriting
another branch.

[//]: # (ob:42379dd1)
## 8. Drift and integrity

[//]: # (ob:beac56e1)
`inspect` validates metadata, capsule decoding, artifact identity, event parent chain, version IDs and current body digest.

[//]: # (ob:e0d13a37)
Body changes without a new capsule produce `body_mismatch`. Capsule corruption produces `invalid_capsule` or `chain_mismatch`.

[//]: # (ob:948a3524)
`verify` checks capsule integrity before checking the latest ledger claims. It cannot silently report green when a portable file has drifted.

[//]: # (ob:155d84bf)
Fallback capture may reconcile drift into a new event, but records only the recorder and observed time unless stronger attribution was explicitly supplied.

[//]: # (ob:e3eb148f)
## 9. Local and re-enable transitions

[//]: # (ob:f7ea9bfb)
`portable → local` strips the capsule and retains the local ledger.

[//]: # (ob:0b96b1bd)
`local → portable` creates a new portable lineage whose first record is the current safe checkpoint. Local-only intermediate event IDs, actors, why, rejected values and omitted counts are not copied into the new capsule.

[//]: # (ob:a55f39c6)
A clean export strips the capsule without changing the source artifact policy or ledger.

[//]: # (ob:e38b717d)
## 10. Import and copy

[//]: # (ob:46afb332)
`import` verifies the capsule before writing its records into the receiver's Git ledger. Imported events retain `artifact_id` but use the receiver's current path as the local projection path.

[//]: # (ob:77b016f2)
Copying only rendered text or stripping metadata yields an ordinary artifact. Proofpress does not claim provenance for it.

[//]: # (ob:a09187f6)
V0 detects a linear portable lineage. Automatic branch merge and server synchronization remain out of scope. Multi-parent provenance is expressed as ingredient references (§11), never as a branching capsule chain.

[//]: # (ob:7be34c98)
## 11. Ingredients (merged lineage)

[//]: # (ob:0cbea376)
An event may carry an `ingredients` array recording that its version merges
other managed artifacts. Each entry is a reference, never copied history:

[//]: # (ob:6cf8ddf3)
```text
artifact              projection path of the upstream artifact at merge time
artifact_id           upstream identity
version               upstream head version referenced
body_digest           digest of that upstream head
portable_lineage_id   present when the upstream artifact is portable
```

[//]: # (ob:6d5f3eb3)
`merge-lineage FILE --from A --from B` resolves each source's current head
(ledger first, embedded capsule as fallback), records the references on a new
snapshot event, and refuses to run when the file content is unchanged — a merge
event without a merged version would be untruthful. The linear parent chain of
the merging artifact is untouched; ingredients are additive provenance and
travel inside the portable capsule like any other event field.

[//]: # (ob:bd118d53)
Ingredient references are recorded testimony about upstream heads at merge
time. The digests make them checkable by any holder of the upstream artifact;
V0 does not automatically re-verify upstream lineage.

[//]: # (ob:b6213711)
## 12. Soft binding fingerprint

[//]: # (ob:92187060)
Every new event stores `soft_fingerprint`: the prefix `ppsb1:` plus a SHA-256
of the normalized visible text skeleton. Normalization strips HTML tags and
markdown link targets, decodes entities, and collapses all syntax and
whitespace down to word tokens, so the fingerprint survives formatting drift
(plain-text copy, re-rendering, whitespace mangling) and flips on any wording
change. The algorithm prefix versions the normalization; a different scheme
must use a different prefix.

[//]: # (ob:e587e369)
`identify FILE` computes the fingerprint of any file — including one whose
Proofpress metadata and capsule were stripped — and looks it up in the local
ledger. Events admitted before this field existed are fingerprinted on demand,
so legacy ledgers remain searchable. Exit code 0 means identified, 1 means no
match.

[//]: # (ob:e5011c19)
Soft binding answers identity ("this is `pp_xxx`"), not integrity: a match
proves this exact text skeleton was admitted before, not that the file was
never altered. V0 ships the exact tier only — a copy with even one wording
change does not match, which is the intended boundary until a near-match tier
exists.

[//]: # (ob:9a42e03d)
## 13. Commands

[//]: # (ob:4de6039d)
```text
proofpress policy FILE [ignored|local|portable]
proofpress snapshot FILE [...actors, claims, why, rejected]
proofpress inspect FILE [--json]
proofpress import FILE
proofpress clean FILE --output OUT
proofpress capture --recorder NAME
proofpress merge-lineage FILE --from A [--from B ...]
proofpress identify FILE [--json]
```

[//]: # (ob:ef9d25b6)
Existing `log`, `diff`, `show`, `verify`, `ingest`, `anchor`, `blocks`, `init`, `sync` and `export` remain compatible.

[//]: # (ob:41921bbb)
## 14. Acceptance criteria

[//]: # (ob:6cddbfcc)
1. A portable v1 produces a valid self-contained capsule.
2. An accepted v2 updates the capsule without another policy prompt.
3. `local` snapshots never embed a capsule; `ignored` snapshots are skipped.
4. Casual discussion produces no event unless a caller explicitly snapshots.
5. Consequential rejection travels only when supplied with `--rejected`.
6. Manual body edits fail inspect/verify until reconciled.
7. Corrupted capsule data fails inspect/verify.
8. Fallback capture does not claim `produced_by` or `edited_by`.
9. Making an artifact local strips the current capsule and cannot alter old copies.
10. Re-enabling portable starts from a clean checkpoint and leaks no private interval metadata.
11. Clean export contains no capsule and does not mutate the source ledger.
12. Import into a clean repository restores a verifiable ledger and identity.
13. A stale `--base-version` is rejected before an event is written.
14. A static HTML portable artifact uses native `data-proofpress-id` anchors and survives a raw-file handoff.
15. `merge-lineage` records ingredient references (identity, version, digest) without copying upstream history, and refuses to record when the file content is unchanged.
16. `identify` recognizes a stripped, reformatted copy on a machine holding the ledger, and does not match rewritten content.
17. `--attribution-basis signed` is rejected until cryptographic signing is implemented.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzY1MWI2YmNjNWMyNTAzZTJhMmVhMmE1ZiIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)

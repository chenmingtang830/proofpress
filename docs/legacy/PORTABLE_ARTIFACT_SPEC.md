[//]: # (ob:7437c9be)
# Portable Artifact V1 — Executable Contract

[//]: # (ob:b27d1410)
> Status: V1 implementation contract.
>
> Scope: Markdown and static HTML carriers, local/Git ledger, sequential and
> parallel handoff, deterministic integrity, agent-guided merge, and
> best-effort capture. Source code is out of scope.

[//]: # (ob:85343175)
## Fast path

[//]: # (ob:751264f7)
Use the [README](../README.md) for a first run. Use this contract when
implementing, reviewing, or testing protocol behavior.

[//]: # (ob:428778ee)
| Task | Read |
|---|---|
| Choose a policy and carrier | Sections 1–4 |
| Record and verify a revision | Sections 5–8 |
| Hand off or merge copies | Sections 9–12 |
| Build an integration | Sections 13–15 |

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
The V1 HTML carrier accepts `.html` and `.htm` files. Its supported leaf blocks
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
JavaScript. V1 intentionally does not promise preservation through
framework builds, CMSs, sanitizers, or rich-text HTML editors. A carrier that
loses its metadata is an ordinary HTML artifact, not a provenanced one.

[//]: # (ob:33fac81a)
## 4. Capsule

[//]: # (ob:c12e32e0)
A V1 capsule contains:

[//]: # (ob:3f058978)
- protocol and capsule version;
- `artifact_id`, portable lineage ID, body head, and head event;
- canonical visible-body digest;
- canonical discovery metadata: label, project URL, package, `latest` dist-tag,
  and a `requires_user_consent` flag;
- topologically ordered portable records;
- for each record, the event and block-tree version required to recompute changes and verify claims.

[//]: # (ob:6fd1d082)
Discovery metadata is fixed by the protocol. A substituted label, URL, package
coordinate, or unknown dist-tag is invalid transport, not an instruction for
an agent. Legacy V0 capsules without discovery metadata and capsules carrying
the historical `next` tag remain readable; their next admitted portable
revision writes the canonical `latest` object.

[//]: # (ob:76b47f0b)
The first record is a clean checkpoint of the body at portable enable time. It
has no private parent. Each record has a stable `event_id` distinct from its
content-derived `version` ID. Sequential events have one parent; a resolved
parallel edit has two or more. Every parent edge records the parent event and
version plus the computed changes and stats from that parent to the new body.
The compatibility `parent`, `changes`, and `stats` fields reflect the first
(primary) parent.

[//]: # (ob:a93fd2c1)
Version IDs identify body states; event IDs identify admissions and testimony.
Therefore two collaborators who independently produce identical text retain
both actor/reason records when their histories are reunited.

[//]: # (ob:778b7a88)
The V1 capsule is tamper-evident against accidental modification and internally inconsistent rewrites; it is not signed proof of authorship. A future signature addresses third-party forgery only; making the holder's own wholesale replacement evident additionally requires an external trusted head (witness) outside this contract's scope.

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
that version is still the current capsule or ledger head. This is the legacy
content-level stale writer guard; reconciliation remains explicit rather than
silently overwriting another branch.

[//]: # (ob:12c384d0)
For a V1 DAG, `--base-event` is the precise stale-writer guard. A body version
can have more than one admission event, so `--base-version` remains a
content-level compatibility check rather than an exact lineage check.

[//]: # (ob:42379dd1)
## 8. Drift and integrity

[//]: # (ob:beac56e1)
`inspect` validates metadata, capsule decoding, artifact identity, event and
version IDs, topological parent edges, per-parent diffs, a unique declared head,
and the current body digest.

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
`import` verifies the capsule before writing its records into the receiver's
Git ledger. Imported events retain `artifact_id` but use the receiver's current
path as the local projection path. Deduplication uses `event_id`, not
`version`, so independent testimony about identical text is preserved.

[//]: # (ob:77b016f2)
Copying only rendered text or stripping metadata yields an ordinary artifact. Proofpress does not claim provenance for it.

[//]: # (ob:a09187f6)
Legacy linear capsules remain readable and importable. Sequential appends stay
compatible; the first multi-parent merge upgrades the public capsule to V1.
Server synchronization and special-ref transport remain separate concerns.

[//]: # (ob:6a0a916f)
## 11. Parallel copies of one artifact

[//]: # (ob:76ea412b)
`merge-plan TARGET --from COPY...` accepts portable Markdown/HTML files with
the same `artifact_id`, portable lineage, carrier type, and a unique common
ancestor. It does not modify any input. It reports each head, the common base,
compatible block changes, and semantic conflicts. A target body may already
contain unrecorded resolution work; every non-target input must still match its
capsule head.

[//]: # (ob:08fef0ad)
Changes to separate stable block IDs and identical results are compatible.
Divergent edits to the same block, delete-versus-edit, and ambiguous ordering
of concurrent insertions are conflicts. Multiple lowest common ancestors are
not guessed: callers must merge a smaller set first.

[//]: # (ob:70ebd65c)
After an agent or user writes the resolved visible body,
`merge TARGET --from COPY...` revalidates the inputs, unions their public
records by `event_id`, and writes one event whose ordered parents are the input
heads. It never reconstructs or formats the visible body. The target capsule
head is the primary parent, so its edge supplies compatibility
`parent`/`changes`/`stats` and the normal claims-verification view.

[//]: # (ob:c4357d18)
The merge only unions records already disclosed in the supplied capsules.
Local ledger intervals are not consulted or copied. A merge event is meaningful
even when the accepted body equals one parent, because it closes the other
public branches without discarding their testimony.

[//]: # (ob:7be34c98)
## 12. Ingredients (merged lineage)

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
event without a merged version would be untruthful. The parent graph of the
merging artifact is untouched; ingredients are additive provenance and
travel inside the portable capsule like any other event field.

[//]: # (ob:bd118d53)
Ingredient references are recorded testimony about upstream heads at merge
time. The digests make them checkable by any holder of the upstream artifact;
V1 does not automatically re-verify upstream lineage.

[//]: # (ob:b6213711)
## 13. Soft binding fingerprint

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
never altered. V1 ships the exact tier only — a copy with even one wording
change does not match, which is the intended boundary until a near-match tier
exists.

[//]: # (ob:9a42e03d)
## 14. Commands

[//]: # (ob:4de6039d)
```text
proofpress policy FILE [ignored|local|portable]
proofpress snapshot FILE [...actors, claims, why, rejected]
proofpress inspect FILE [--json]
proofpress import FILE
proofpress clean FILE --output OUT
proofpress capture --recorder NAME
proofpress merge-plan TARGET --from COPY [--from COPY ...] [--json]
proofpress merge TARGET --from COPY [--from COPY ...] [...actors, claims, why, rejected]
proofpress merge-lineage FILE --from A [--from B ...]
proofpress identify FILE [--json]
```

[//]: # (ob:ef9d25b6)
Existing `log`, `diff`, `show`, `verify`, `ingest`, `anchor`, `blocks`, `init`, `sync` and `export` remain compatible.

[//]: # (ob:41921bbb)
## 15. Acceptance criteria

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
18. Linear capsules remain readable and upgrade without losing public records.
19. Parallel copies of one lineage produce a deterministic conflict plan without modifying inputs.
20. A resolved merge retains every distinct event, records all input heads as parents, and remains inspectable/importable without the source ledger.
21. Same-body events with different testimony survive import and merge as distinct events.
22. Different artifacts or portable lineages are rejected as parents and remain expressible only as ingredients.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzY1MWI2YmNjNWMyNTAzZTJhMmVhMmE1ZiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImVkMjg2OTIzIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8wODI0NTNkZTRlODIxYjk2MWU3NWJiMjgiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzUzZDQ5NmU1MWI0MGIwNWE0YmE1ZmZmMyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfety3EaW5qsg2D_GjiFLuF8ojyNkWe72hNXtsNSemDAdrERmgsSwCqgGqkjRl4j-tQ-ws0_YT7LnnLwgq0iCVBXt6J2Fo1uiqoDEQea5Xz7-fMS6dV0xvj6vxdHp0Wp1niZBmZacJzxM_EiGLJQsZEl1dHxUtuL2XNQXsl_Dtf0lC5P0NOBhXKVFWYjQj4IgzoKMJQUvgyAPo6oosiz1K1EUkRRRkTEZRawqg6pK8yKJAhHAuqLueXstu9uj05_xH-vzNbuAJyzYGh91DD-UcgEffC-7uqpZuZBeJ6_rvm4b7xKub7tbr7z1vu3atlp1su_hnhXjV-xC4kttfdy1_yXhdTcdLni5Xq_60xcvLur15aac8Xb5gl_KZlk3F2vWXOSR_2Lr7k7-bVPDz-ebXnbnvG162cBerLuN_PX46FIy3EQpwjwtwuhIfXIur-ki2Fx57udhnERCxjIPg7JIA5klZRnmSFnbrfHVzhd1I4FycyKLc7ghLlIJBxP7pZ-wuITzqKpIvY6m7pyzVb9ZwAuHSCdvO9Efnf7w85F-_M9HcMpt1-NP6mspzkvY8h-OeCvkh6Mf4Q0MN8CDRcv7F9_-5bv3r7745s35q-_ef_3Vq9fvz999--b1bCmOjj-Kc9h63dXlZg0Hdl6yvu5x71nXIN3wHZyypCU368u2Qwqv6gZX7W_hmyV807AlHqWi9PiohxthraPTZrNYAN38Ek5LqvctFy2_gmuzOMp4UUq4HA5qLT_gW32rN9l7pan3vg-8f_z9_3hvPki-UV-9hqs7BrdpIpgQRN0KeU7ewCd_8J6-DkcGXt-ukHxkB2Cto1-PBzLLMBNBHPi_AZmfe-_WbL3pT716uVrIJfABwyPwuKbMEyBQ11J4VdcuvfWl9NgKOAo_GYheMXiKS3GUV6lIc75FcTAbaF21i5rfjm7gH7x7bxjZJ17wkIlcHvDUN6hjPMO3oEL6dnEte2_devIDfLK49dpG6oVOR3YgSOOUZ3F4AC3z-RzvO2vqi6btYMM9r9qsNx0cwWbdLuGcuMcaAYStYKl67fUNyPdlu-7hBQbSUCC2SMt5lIZBeAhpr5phj25AMbabtbeUaybYmnl17y3kBeO33hyeyBbzmfemAX6E4_Lmq3Zk00JRlmUWbx9gOPO-FsCX9foxftm-coRRWB7msc_2eo7ikCVrQP8Kl1O4rJFTmNfBoYCsrNj68gRWkSvZ4LrenI28eiqjMi8qsQ9J36jdJi3e2_OYO9p3DvQtWd3AX3BGqBrAFiKBszEh5nmUB0G6RVI0816zrqtl1z9yGttXjpxGKFMBT2I7zwm8t6y7Eu1NM_4gfNLWtSOPikURFlxmez1q8B0GXgcj33t1g46GUrjLZdvgYh6w-9VJJyvZyYbLkW0uqiCMQ-HvRZPVET-8ePHjqfcH75PB3J8ilaefgTGVaQzOzMl_9W3z-afOtSNKohR-5Itqv0N5a7ZnCRfD-ZOaopXhJw72GzWUBMXFFxthbIvew7GdYhk4knK_nXoPpquqP8DTrC-pyYO_rlDFwwVk2RqgUcIRo8dQ90tvlCaZiUT4YbxDU0h2FRT0n96__eZx_t29fIyFq8CPBRf7PhD3ATwFvMzjSj49xrlcgeqYzy7Xy8Wcjot-nsOWLWQPagi-7Tdj9s7nlRBc7kuWI1w3Xb1GqYJHCskX8KQ1aFZP2ZbGW9-0XtM2IFsN-iZgVEbIykKW8TwO9iUL5Au35Kz5DIXJQx_z386OdmTs7IjcJdC-8N22vI1ImGAR90OfH3KQVg9J5buh7V0tGAcuh52af4YM9Pncu4GAxUN64ZKXyOhjWj8Cm5EH24Ifoy5XscO40t-6cMxVC0IZhTui_LSnvEL21ZEM7TvYtX7MFYsqP8mLLN_jWSeoEdYtbxckE-apoDwwtnh51pxsm9ljz4RooP8HkhYQgG5b-0oEAgK9PUj6ctBejsOlNBsYda3FiGZw6UBoyx78hw1ET95iTFDSMs4qv9yDIqVZu56cIAgakR7m8YVkEEZcSn61amtgzbYi4jBD4LG13qgRilgRVSLkwR4Ufa_Ox_v6S1Aj5EBVt-rB_RoTBi-Vr7T9PRPLGkLGsT3K8jJjeb7nHjlsCzu0ZsuV7E7gAnIO2QWy8RpVMX3AFt6yFXVV8zGv0WeV4Fm-bX0SOHf1Lu0jrpO3c-mIwEaBX8ogD_Z6Er69bC5qiJyGGKVtIJgizWQCGPg3uFLtleJk4B5wsZuxcCEJZZCF-9E0PwELgnkeCd4xnAd4ckLRVLWdR3mbv22QNeAk1IWwIFhCfJcxP56lfiJ2_Pin0vQdu0HhXYItPvYg_G563tXqHy2oIAzIpXKmVhCUAyd7fbvpwFlZsdtRlc78VGTbKj0FmijbQ-s52ZdHWGbsvhH-8f2srOIkO5yGP8sbE-os2S35MKOReOj7RcbSZ3h762xjjo8SUufl7VkDJyY2XP9Ditp87qTQzhp6xIg3AEZKRDLlh1OJDMqBh8CJKOsFhI5goihphs6cXAgdCvZoHSq2WJQM3PLLtr0ad_BkmIclL4Jn2MY7qb45xswXwNpo2Lz5prlqwJsHazrv5aI6Z30vO5TT47MxdZDnVQix1Ha8ms28d1rleKW8ZNd12z3C4Q_cMqYcy5QXcXHYk78CtQM6b66zPXObW8Bt0AthHI-GEw1sf1WvaNtvujGjBbFJloqdRNQ-tOlkzhY12lVHuw5EL0FVLqS4gDNU9hWpG3M6kiDMKvDNDqfNuF1b5I1phaxMkqCU1UGPDmagebte74BJAigPhxJz4PdhgKLNPviL4YxkE9yxfsQ99HmY-ml52L6ozBEcmQlOjOAD7zTtSbuajTpffsYL_7Dt-Q807rgzQMQCmKLfrMDQw26B7cUo6UT70XBo68FD6GQFtngs1Ax5lMc7CZO9pA1dsi9f_fHYEkRsS-6A8qMlr3uJTuNCnhCvd97FZswhi8MoK4TY1pL5zPuyqyslD-AKy4vu8WTmgzeNFQok40kqD336HJhkBQ7P3Ltmi1qgx2yDjWPrw0Js3iIFx0MSFDzXMQviiyBiUXYgdV-geOlqjk12AkuDW2BI0xbZm1M5EhyvJVvzy_lszHEr4pxFyU4iZ4-9u8YC5O1cRT794PGbm4E7wcGU6ntUDshptoz5IM8nicjjsjqQuq-MvQeyqJKAHhT6KQ2v8UhpNVip1RtK8nDsga32urGTjWQZxPk2dcXM-wYtBlHXgWw1FBeTW1uTM_2IBDxpgRFpqDLJirIqn5Eqa2e8f_yv_-0pgwjqAZz0Xis6ddpqccpMqPOlR45Z6bJIy6AUz0mreigSaq2jxztJ4qyO10lWUD0ZwrG2V8H8mG1IkioqePqMtL7S6QKIBIGk-3bUCDoJvhEbin5G-RIC9iDb3tXAn3lfL-k5lNNpV4_WIe-9YyxHm7KqjKLwkOfOa7p27pFCqeX2dmglgjYJNwNzpbqgj-I7msMo_SCtDiLtNXyPT6VoWaVhIXbGtTywqnR4K_zeJqhuMe7AGMEbq_4xvwjyrEoPIU2XwoifO7Nb_Z3qFynMpWF_cB0woBuN6n1WwLZtkwbu37dwJfg26GOt8IzaiurDtkniEcZ60gojjJalksVBWD4nXfOl7C7kyWoBx_X-1Xd_fPPeOzmhCs3rv3z7n7PZbG7rBVZ_3K2-3dVweSUrn4nnJPW19gLAXvUSn7gmZ42ccKo2YYKPztr6wp0EjsD4aUxGfFmKNOHPSeqrCp1HndMiOcH-IDeA0r0GYiuOgIgXzmOEVh5HSSaC_DlpVZUFYAIl4ZsG1bfVL2yBYnRLZbRF26tSA2ljdO9HQy4ZxbzYIRVr3M0FKJCaUjqf0IOFsUifPiZBj98-lpTi4DFHWfpsFL1qdORrM1MqpB-Ww7C-005XJ5QhY2tU4GPqh1e5ENTN9Tx02kyWdd23_tMdcJhCxyYBk7rfrEC3SzaSxUoFuAayfEZClTIy_slXX3_zxmijV-aHL-ZDnw4EQJc6KfovIxtaiiDIRfJ8dA73ebbmr4rcJgvooYdfL9sGWKJET0bv5nLMLSzTMIiyYDugCyIwWC046iVQgxxUwR-yW3XK8o-Ky_itI6JShGCb_dR_FkpUD40NMDxsz8S0QA9rnTtrzE9NHF7VH7z5atWXwZi7l-SZjNLiWWic28IQMt3cpm2IImcNFA4Gh4qFcuq_qxu-GE2kJn4Q8OB5qNy6B1ztG-y2qHXPkPfJ2dH6su4xnwGbd_7hw4f52dGnx17TUpQ33msRh9KPdsw1Frva5RJM6mPB286loz05MvWjYr8nWUU2lOR1-5rSFT_obOovFAz9YhyWH9UNI5pMVoUIkzLdi6o3JvEHMdgFpiRFXVWUmrxsb_BvnSQ4JtMAegF_Up0x87HkUgBSWJY73h4Wl8gfo7YVTlmqmj12PA_eNXJSKReirDg_9PnYazj4jteByddgWEoZJw_T_ie6ti9t3X2G-dPdtOmPx6Z9-UinE89VkIvPpG9M97E8lzIvqkrCwYaiqsI8TkNfpiHKAYgE7fluRDwUsKlhvKMnYUux-Rd2FP-IrdnUMzms4LZrO4tQI_iendy76pHuAJV4mqRpVOWFH-S88qsqCRK_DOOIww9FxXJRplnJixCCHx7wtEqYTKJSxkzEIZeFjx4ZFsap8Vsd12mW_gob3VP9LExP_OwkTN_72WkcnYbZv_r-qY-mQO84CpBMqtCvCmCY4dOff7NucWJJ1cx9yfpLZLMyS0XF80o1StMaTn-35tbnaMvWD4QXDoI4ETnPI_NAp1NbP_CQBmvwD4CPL26Hii-oNYE5aSpFnzWfw_-8d-Dgy1MbgtHF_dBCZJq8-mOVhXrxx3qtqzTHnlPjhttwtZUJGy6xi7WqjuGBINDLukGVxoc047GKZE4uNjV6N-QrHZtVStBpJ7KqMGzXqUa0b1SrRlWLFgl9ILCdPZJ_XylCb3NRpRV4QFkYsNhss9Nebs716d3iet0wSUWe-0kkqTuM1nUayPW6B_eD66fxqkirQkZZEVfmaU6LuH7aQR3fkiqCKwkHoDJ_-N9wAZwVxJs2GemwwUvwB9zOFLksJSoBsJFGVu5fR5X6VMKvgq25VGUcfbtZEiLY-fweS6t3JsijvJAJ6qvS7IzToa535pCGc5P7xFczG6eEpOZXtzNzk-p6tNVXJ3OpUloq_7bpUOkPeTigQ7TkULEFbgxZuXbTLyhAVnVuKWwQ3oE4LUCgnKyw2sYRCahKWVR-KjmLpNkhp1N-kIBH-9_1glnIqyhJqqQQdkGnJX6L9fdrdHda4rB3FLeefHzKFbCtts7ldq-wyfLVdC2IGUYJblFZJXS0ielHti1LijwoRBqIygq402Wv3_KQ3nnvL-jxsOa-zcHms2Oq63SYImVLykKiPzO45-vLrt1cKKlRbz_yOnEaxXnMEpnwzOrBoUN_4IJH--71gr5kRSQzlpY-s2w1tOLbBZ_SX29oZFGR5rIMKhaaJZ2WezO5dEAfPbAOOEBKLEfUbZTyMvQFDhpao-H02e-q272a551rbUf56ZPHD71fvI-aLHzgyVoPuYT-tKhLS-2o6o3LjOdpwLOoshzg9P3rXTqkmf-EeiHwcfBSM-8bxTLef74CvwSua9ZLHO3rhs4ECGZvQTv-JLvW9lV6Rsm7agOJaCS2C6FHAv6wRDXLep1fxV7KbqN79kZ0RJYwlqVpkJVWEzpTBnoHDhkduCB-1nrlrJHkZJr6lYlrtIoUUvX7mW53Fair5i3SFy29F_hnaEi6TXPWYEhww9C7Ap-13yzxfJYbasWlMVSVZdZTqKZqVMk1xwNx2HFkj9KEB5lMK4jSU7NHztTDlp54whyD8Z6LMqnSQoA2G1TFMNrg7Py-wwortPyYvpOsUvzaY75TevPLYP6Pv__3_DLFsHuFfyxq-rGj_iG69m8bCAjxX2tBf17Oj9WTqvoCPVpsWwEP3ETtJpE_x3M7GQT0pBY4E1CL_POzoznwD1gI5TTqVOUG_tDN-7Dce8wFm_Y45YxtiZUSOy1PRI9iI9qZfwEOosnrkcMMGXjOfgQB42AUndGNuxr6o4cx0Kl5TD2XsYjB9WYp9-3hO5Mag3o-aPYCwqOjzx--28ry1hK_mQJXtCgB93Bf4GEM-6HUdr24bsRsuPpfkX4gbIed4B7jVR99fq_O_-yFesTnj-j-NKrKXKBBTGz06kykOPK374yJG1Ko688arYDmn71Aw7Bzl-qtdnZIDRLQs4nxlT6UNk4_a_6dXbN3dAPeDJe__f5bMggN7ikoSvDCW2BfvA8bq7Gbi57WXasoXLtgZ03VAYPctOBwlJt6ISBafv32HfzZM_Q2fqL4GZVuzS9PqNJNOgm7fcEAYj7LqCcs52AE1mupcaMULIBj0YcBM9H9Q4snaXrHiGAv-lhYXKVJEVQiSJLAWi5ndGdwBx-byNHr5QWr8jyCeDS2YZgzpGPCsKfO3uhVkzLKgqiKk5wXlsphHEevetCUjUrTobOtfA14NaWp8Sfl19MKnIGeohLwlm-iNObOFeLOjM2pRwATx6Y05v31u2_gHwpA4phCvZM1u1BPZt78XhQIMFALdkHPWrerdtFe4NPQGnSqhcK-lq610qU4jkC2Qn2oeyVtfy1Jxsm6k3bDjO0X6DDgTVS4sC1zOnzCygbo83rZz-7pRDXmogjLQhYpK7nlMmd2SZ_fISNJaldpN9vurNE7CrylBEUZQQgMKC1MMTlukpaXxvXzaKNMgR1sqY7svveHNhAT3t0933s7RHAkB6k_awbWaEs6flIdsu7ABwVdgKND6_X2ASrbMSLBLBZ-kYcsjGK7t84U1pbvud9w1QJ7alUbVr0kL_OsgYdjusfMj6gc9sx7MzAYuhfYXq4WmJsU-pyYvG7g5ckVAd0G-6Ls5onJYc5NRy8IpO6qUdlFHV9fsmupEmb03JeYRNBtD3j2OvWIWpWoQO8CDnXZooOr8hHqRg8TArYjgRhMf27k4qwx0rBabHTvlBIEsSUJlPc2uVfcObUOSA41tcsb2lNyze6MVahr0T3UKxofkRbV4xYY9lcL5Jm1OcqzBkK4GiKI20_NAYzE_VkOAih4yrPEJmuG0TjNJodMvGGGi1xJU6BWb9spW41nAIILgtqC74fR3s0lxiE23QP6y_TbDm02ZCJVvgOsfru-9Aha5gXIV08aSp3cje4QB0FSTlZtq-abBgdpRjYmKBOs5iR5KGxc4kzobUcQew3ekVYxvbWdcidq5PkeaFWlfuUevwRpwKVRKfX1BZasyGej2jCFb-Cwr2jgRqVz8SKmErtCoGNHQWTdiRN4yzWNoF0gt2P_zUsMMk3EeNkuBHn6mOmHgwCtxkjdkIe1VCKgX0yI2npBxh551GSp3gbU6QaHmJSl_ASUI4LtfIqJ-R6W8Kh0bMoU8MjHMvU5B07Nk5LJwio0Z0BxcEkenzq0QWJc8EiCIx0N7sMwiOgc8b7ThesXFCCDkilvt6oW1U6nNGizq3qx0NG1Wsh5HNkeCkzdXKnJUmrHlRQYbCh-zNTReLD2mJEQYcYDFpRxkFkmd8YeTaR0wCyj3jmTS6kwg2AWUznthkI-rSQ7drP1CmMCmmZRkOR5GlLCVTkPw3ikpv2QmcdFy4TSF-QOmP0vsUpWsc1ibVQweWWdeUtbTCHRMPWKkTdJeFymImKVPyQrnKHKgbM_cjjSZGK54DwFLo9LbgVnmJfUyz917tEEeLEoslhWGY_s7jujkLsp0H1HGt0xvkdCzownwMxhGmZMOMGAGXt0pHnf8UU9XkScP3donZOCJslFRiG3V5l71XhJF3bGjAlUB-qlrVM18_6qhhIHo07-Iit7UiLqyzFhqJgvwghUY2XjbWek0hzHIaORc9lc113boBWwkGl45S6MmnVTyFTNlR4w_8K84oWHh6niZClOvQ2ojoXHu9vVur3o2Oqy5mTCqPW8HyrbUuxMcqEawTDYw5iYbCW5ohCrSc5AS2mZVS3s3k27gfOFB4DxcTYC--WucTaBkZEFxbpBwSUGpPe517CCN7F6wKi6Rpk4A3MEZw2wxjHqDvBsYWuPKbdLr3Mlb7cNr0kIGftvbS72EagEwL0GV5vYvS1sFGVlVFWZL6UtazhTr4MeevoIq6myJ4kI0yiqwsLaGWeqVa98yIjqmtIwSoONvKIfgBZMQ7_gwioJZ4TVIWTfeVTJrm0XnzNYwmw2fmT_gwAsb1YEUWx3yZlhdYl78kCqibTBwc-jvGQ-s_rBmVEdUNr2Hzh1i_YqYIHvo5m7aUNrgEmcxLMhhaAjLRtbXisfeKFSwjpkMp42MhncD74eRA1LbWutwNi420n4wNVgP_X53CkgwWebRpEtRjIWBedBmYMXCpGB5Z9hnFbv416zseYJoMGrPGIsG1wyZ1xWP-GQ2VdqL2ErjK_gnReYPG7IWpmQlsrp4I3e25IA3KcPGY9A50Vrc_qYExni9gWc4ULNt3rDfGsnXtqhwFpFQWZ7bAMFxIKXKtuJVSgQJAoE0UiZmSQG-hQvKTuskYyaxiqXGQ8rX9oNdWZ8Xd2z58BuRyaCWElvIaV0VDpiSVHuJeZmcT7CBCZm9rFv7xzZwCy7O7ntuFB-xt0pZQwwMthqLxzzPMMyK3jFk0Tmtkw2zBgPGv9jxoVtCpnBh1VSRaFVtc4EsXFJDhgGpjaH4_uSMl9_SQ6-TYK6eR34BgN0_Qm2zsInDMdQwEXVVSgdtYLXY4tgWgycrO7YvopQBGkeRty3--rMJ-t3P2TU-LXNknfdZqVmKUyb61wnNA0g7xyFFpNIdeMsMaaCZCmzrIpFbE_OmV82J3fAKLK1EypDjAVqEBiV39Cyrsw8uGtSNirSZoNtINOKKTwaKR4NriSYPsGSMsoz29jijDsb8T9gclknmygs2HL4kXfaUnm55JhqdYsNX21DzW2OG3rDejeZoDX6aNwI0W-SsrJMIuuvObPSg_TuO-psUskZC0K_xNKuLd4408-GHw4aXn60TU3yIItEwIXveG7DWLMh4qCpZDcL7gp9zyq3VVvv5gmdOCXvlhDPYe7AZkGPVUIS_r65BBVlMx4glxudb2h1Up-3m2Y9pBnc5jSTI37cdUx90LJJBp6Db1NZziC1ra_tPwc9zPaZCQjrCYzQxQXPBeNF4QfZwKJ2bNppr33qELSJ9ouc-UGVB7K0vO_MRVvrsv-Uc2uEGVvuIDQ7a4aeVkOrFCZnopvvtjv7UD1gGLq9kGErLElg5toVg53ROLC6UmxsFV_1sQ01E0r8QWQ-OHv9Vu78zlDYTgYdS-cmDB-rEVRgDJKKh7Ecgodh0Fvv9SFj26ZqbXZv5nZC2BK7Sqw4nVCYfqzH7HAeyxKCvaAqk8GZHubAt5s095rq1t3t5E2jYmfk_io3DWKOoSrjLTeLdW3cDjX_ullRNkJ7l5sSztkyJ_Df98HsrHmHpwP7dwteLliN-qehboCOEzwd2xeH2qUh204sow2T3WifWgJKtQRBkklaDalUO5PuSOm-E-WGk6TwizSB2MYPhqKkHTI3UnvAiPgLanygTi1SZhjagAZjYHwfKfIfDz0WQL8ptWu3kFPH6BmxHSZnyGWxjEkVnVua06sbCGXpW5OnoOK66hvQZUJYyUOP_9hlFd18pd1B9fgejhLlFc-wAuZYU1pyzWB3tCeKboqemFbBAh79xiZSVflT-xdtd_VSVwmwp0ovQwSr5KUK-sg91PVXJ9ge6_pKqhB8BC5Ebo2PM49v9MMB0_TdkLSlOa0vUZNeKI8e1bZW1nTMupdHNcJTULXpT_AyfaTLsr7YtJtetUUAg541wMIoJdrag2MiO9WZrx5s9_4tivAKWaa9QS9Wn6VhCrqeEn0QFWLVTZzq-FzXdZTUMw9ccBW1y7VSDmOWPWJB6fOgkEMY5SAIGMt-yPw_EvWAnHVyCMtwFeIW4E49tK9qq0pzmfR9j0lO10Y5GTpUFMpHUk6X7UxRs2603_YxZw3ynYoOVGWFHHLVkUHDDhUm4dZ3s1Uq5awZ3M6JUB3ShvJUINcPVnYTZRXr_jaXshVuw07pgvwLW49_YUrxJkrUWUEV1pwop0ObbhxOHIu5ojzncSRZ5dvEkgO-sNUwtx90Qj3MzOBw1zeO262cWDhp1w1tUPZUtUL5pKh71MPVEdYYqTPM0lebxRmeUGMr7k61DNUUWEpcfGjNGFL0Ndr11uQcKacDjpGyhSq3s9NZwwyuAbLe0FQwklZNytQPy1KybJCgASzCsW57oT2YptMAe9yChHHmZAYtAMQwaLQ3goPNzxFZoJ5VAmx3hKbX7TawGKxO_Tx2vuFYC5IOMnShYTRvzHkm8lImifXfHbiI3TLfPngPyyGwYEZFYrA8rAZqxFnN3mYyQEPaZ_s_eyEJ_tC9pvcC-0WHXyfl3Kc_ICrZenuZYWjNGa2lV6Qe04H_775cPXgrjzXPJpzFomRSpDZ75EBfbHtJe2FX2BhEv9QnWg-QMTq-M2OHMYophn56vNUY5cBRoCXEcPWsMRUJkybRM3wm99xtHEVBqRyTJq-dLDxVu5hiCKVd1k6STIumOVVV2ysxwwLmYX0JGkkZAe1vU1lRM95ZgzdTDtk5G7ix3YCyES89RxpJH6pWl-utIQxKN4LTjWlZcBhUuc2pXpidW9RXkhxDJazqNajIO24MRBJGgoVDA7uDKWKqDAeAgpBltfIGb0IdfLhhivt7W55cqsSHmUzDV1HFygfF-OVZ830wOMfb7RCdPNHdofY-zcFjvYxFlKQiFZWMrRZysEscDf7RACSmEaYUvArSNGCx1d4OJsnWzOJ-wCKnc9UqyLx3f3p1EiYpuZ2D01D_5PhmFDX3V-jCts3M-7O-QnkSOm1Dgc6aXfSKF5dmQBsn2rTv0x-rzLmkuVrgYRNYUMfdCsURp30gtlyzD2qZm0t01FYMZ-FwNRDXG8yIrdsriZ1GfXsHoaTfdNeqg4fcMcqlUMIUGxHBE2pURzumdFB3DMMcmByzTwMzdoEjtZ8SgeBxr5RGAX67UYbwTGsGxadscYFjS5dLs82mG2prT2nHsA8U8_xSJfOAn9G6kEdOTQLOl2qtsQJyXoVFVlWV0y_pAMPYvNMh6C5CpVF0ZvKsuW-i0e1kv5HUkNDReLZSm1iJbtsrao7YrIwfSDmms8bksN7ogVfTXqzzYdQ2oJphqOIrVXOTQza1fwFrIVLJMU6JmQFptXI_5CBYB2dG2ZI3H9DTw-F8n9xG2yhaY1tHoD9rWuTk9WhBT4pIJpznYZA4R2BRb_QRHAZdQwWMU7QzSAx1LKmyPs1MocnYElFK3u_so1rMtgGpbgCGjSCqSwx739CpBl2JnSKKN_TamIUgD1_ZQBQdsn2kdxRrbMuEk4tAgkmyMIo3UdsaZQ6d8U0jMO5RLTdorll3oiJ-fChOEMKJ96MdFJHvB6COw6oYZhotmo-jix-F6DGFwkqkWVnIyEnSOag9uz7mXlA8-gbrmKhbIMQ1aXoVsu2k67dv1pVKfe8JDUTtXKES2HjB1ucq6649NLDDmHH5y1_fb1-jC0_Ya6nrR39-9XZ7ndG8GJI0_ANe7cf7iXwo3r_v_o_boDGH1Cz-Ba28vWuurnRoHvWRizBisR8XBRe2qdEBVTIG-wCkJDOq2atva_oO07B6JlQVUez4vpOfGkm0ZtwvgyjOg8KiyDiwS47wfAyAklk8qHKQQ1nIoQHSwVRyfhPj3uhIHgJlmMj-OgTTMqSGdktIpkFDC6lqwp1RS5CBxBganJVOpLhjaJV66bSC3QtFMqMGotes3-ipqo3qrbCvZDrCTOGVmX4Zt9BqVp5RO9Hr-9uZPeXru53fNqtCmtltkp5Rq9Fb1iBdKgFCacqK1QujRl4YN5g0sS014ztlSAWV9Z0QjKw-LtDvrAA35DPvTgF7p2oyd3puVT-A7btFcgsk90qZyiEsUjUpt0y40wykvJBmwCeByEDXBWBRrOl9p6vNuLTluh7cUzMWc8-0ke6ju9oaJTIpKusC4QOAmV-7FU0zM-hCzuBqg3Xc4LyKW9XUzhAsFtoKpC70K8Iwj9_XuiFTe_xMFxRV_WAAqjH-BS4X0TAa9T7d6fCpnSZ47XWxZkirYbYULDauEutVLN6S3UR7ShRWqy76-wbE5wOOApYUjLOO-Co3J7qRgrCY8HEgANt5hblTEr0v3Pxk6MPRb3esQ8hPh2KyrgwO0afKO91NDKjq--O5ASQVJMy62YrKiwaCKDVcpnxhNFQ6KFEgObcqSbFkCFCgxl1sY4rGrNpmF_KMVFshEGFowceDkMKxOg0cJ9RQ7Zk-Z_eIn97gjCuDNH_zhFKkLh7aXV4Al6KQqdSpPjVcr3iwZmdMtekyYjtoXKb04ZHLYYGRqNpFtFM1AC2Dj2xqSwzKxTBNHqrkZMf7dE5oSFovdA1K5yR6Uw0w7KGa4bTSw9d_MVRhLVH3SXQI6uEdW-ouTweDxwn4hgyJlgzjxOGzdb2m3yGe3hi0xZd2FZt7Rc26W1g0ORkz9NIP5Q77fqjAUF4p-icTw1yJuztE--OvaPnv-c3qVq07v1edfku70f5bn9__e9jVr5k38xr4xXcQTbBO_FP-inYqee33G9rzJIqjgCL5AXLyK9avKVH9CMile90YiHoShGlcZR__jL_q1pEfvnvz6su3b378ZDZ7oX6Ezf1UDYWZvqVNM_PU9arnf_SXyORZlkv58QT94r1n_ZX3C1h1JrxfzppfTk5O6P_wo_f6sm0pnaI9PuUcqJL6L947ByBAIVgitqaKKh46kx1CNIjmK0pNM28NtJBdFeAXaervNjBRJshkbxUKgBlZmD10Tr_rc53j-O2f-6Nz5j8fQSwH69tBFPABamwoAfvHNwOUJCMH-EQxGs0BgHBim0Tr9eD8ISTnkyFScxFmIip5mXBQAAG8d17GBQvs27rYpy7up4uH-vMky_-Msvx0NNxdNNjo1_uxXh8Dvn0WdNsiCDmTIiryqJCi4kEZphkTcHeVQ1guY5GyqIjigJc8r6KKh1GeFTHclfssp6GM-95nF9w2CE6T7DRI7wG3zSuZRthrPYHbTuC2zwluCywsAsGTUHK7zY6aHNJNj6g_00ghgwTESfpRYXtuHY2olztE06lTxfjvrLFnTpUipbfox1a3fWCwc9fEPdwLKiNZ-CJjQVEMsy5WfWrqD1OLavLdC_7x9_-O6WZYhkJaBxWHDchfzi0J3JKrW_5E3eFVRdgkFIHoqM25vIDLg1Bd_wUiSim0GuQvJSIuNRFenHi_3FHaEwzyBIM8wSBPMMgTDPIEgzzBIE8wyBMM8gSDPMEgTzDIEwzyBIM8wSBPMMgTDPIEgzzBIE8wyBMM8gSDPMEgTzDIEwzyBIM8wSBPMMgTDPIEgzzBIE8wyBMM8gSDPMEgTzDIEwzyBIM8wSBPMMgTDPIEgzzBIE8wyBMM8gSDPMEgTzDIEwzyBIM8wSBPMMgTDPIEgzzBIE8wyBMM8gSDPMEgTzDIEwzyBIM8wSBPMMgTDPIEgzzBIE8wyBMM8gSDPMEgTzDIEwzyBIM8wSBPMMj_tDDInYJBRtyB3x0KeWsS4ZlxkB3sxQFG9OlojwPOqBrqI_oegix18A-GZ90FNXn6gs6o-7Dg1kD-g2vZvmazljN2_bFrKbruxzR29vfu_RrmF4LE1UKacRgQgxOtwxYMFf4AlKHEZcVo-BzfQFs2BP95aKd_x6c6x_E7PtU5uN_6qfdhKPO9ln47JCvdZ3wUojK8c5xEQsYyh_ipSAOZJWUZ5g8hKluw2ccRlSet8Ixa4elA2BZN2K52Gv96P17w7wKQLKosS6s84mUUhrKKZRLyJOEIIxWXfhFnRYULlUXswyaloqiqIqkkS4LUDyKWPfxKdzCSo1M_Ow3yezCSpQjztAij_38wkktRhrC3cVKy6ikYyfCYB2CSJ7TjCe14Qjue0I4ntOMJ7XhCO57Qjie04wnteEI7ntCOJ7TjCe14Qjue0I6fC-2YV36WBWlWxsP83P_baMeYU5lwjv9ZcI5zmcgg4QhFyf8n4xzPFTrEfAA8Pmu8_2GYx4WMQVWImIUx-80xj_XO4mioATwm-dM4b3afPwoFGadgNQyy93EoyA5b9mr6iVpYCXlU4bMi28wR9HiOre27weLLUVRkHEDURsaZexzY0XKXAlmesJMn7OQJO3nCTp6wkyfs5Ak7ecJOnrCTJ-zkCTt5wk6esJMn7OQJO3nCTp6wkyfs5Ak7ecJOnrCTJ-zkCTt5wk6esJMn7OQJO3nCTp6wkyfs5Ak7ecJOnrCTJ-zkCTt5wk6esJMn7OQJO3nCTp6wkyfs5Ak7ecJOnrCTJ-zkCTt5wk6esJMn7OQJO3nCTp6wkyfs5Ak7ecJOnrCT_4mwk3_89f8Cof14fw)

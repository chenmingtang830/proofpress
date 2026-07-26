[//]: # (ob:7437c9be)
# Portable Artifact V1 — Executable Contract

[//]: # (ob:b27d1410)
> Status: implementation contract derived from the approved strategy and privacy decisions.
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
JavaScript. This MVP intentionally does not promise preservation through
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
- canonical discovery metadata: label, project URL, package, dist-tag, and a `requires_user_consent` flag;
- topologically ordered portable records;
- for each record, the event and block-tree version required to recompute changes and verify claims.

[//]: # (ob:6fd1d082)
Discovery metadata is fixed by the protocol. A substituted label, URL, or
package coordinate is invalid transport, not an instruction for an agent.
Legacy V0 capsules without discovery metadata remain readable and gain the
canonical object on their next admitted portable revision.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzY1MWI2YmNjNWMyNTAzZTJhMmVhMmE1ZiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjhmZTYzZDRkIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV84ZDI3ZDNiY2I1Y2MyNTE3OGU4YjQ5YTEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzUzZDQ5NmU1MWI0MGIwNWE0YmE1ZmZmMyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfely40aW7qsg1D_GjhFZ2BeVryPK5XK3J-xuh6vaExNWhZjITIgYkQAbIKWSl4j-NQ9w5z5hP8mcc3JBklJBVWT1jfkBR7ctkUDiIPMs31n16xnrtnXF-PaqFmcXZ5vNVZoEZVpynvAw8SMZslCykCXV2flZ2Yr7K1Ffy34L1_ZLFibpReSzokrisBQpi2OesFDEhWCBTPNSBvCTn1ZxEYhEJgErRODLMC_yIs049_NYhLCuqHve3sru_uziV_xle7Vl1_CERr7bwtcrVsoV_PqT7OqqZuVKep28rfu6bbwlXN1291557_3QtW216WTfwz0bxm_YtcRX2vu4a_9TwsvuOlxwud1u-otnz67r7XJXznm7fsaXslnXzfWWNdd55D_bu7uTf9vV8PPVrpfdFW-bXjawE9tuJ38_P1tKhluYVzKNRCzO1CdX8pYugq2VV7kIMxGVvEw47G6Q5TIv44IFSFnbbfHVrlZ1I4Fycx6rqwRWK1LYvTL2Sz9hcQmnUVWReh1N3RVnm363ghcOkU7edqI_u_j51zP9-F_P4Izbrsef1NdSXJWw4T-f8VbId2dv4Q0ML8CDRcv7Zz_85cc3L7767tXVix_ffPvNi5dvrl7_8OrlfI3v9jF8w7bbri53Wziwq5L1dY97z7oG6YbvgJ0kLbnbLtsOKbypG1y1v4dv1vBNw9Z4lIrS87MeboS1zi6a3WoFdPMlnJZU71uuWn4D12ZxlPGilHA5HNQWOeni7Ae9yd4LTb33U-D94-__z3v1TvKd-uolXN0xuE0TwYQg6jbIc_IOPvmD9-HrcGTg7f0GyUd2ANY6-_18ILMEhgjiwP8nkPml93rLtrv-wqvXm5VcAx8wPAKPa8o8AQJ1K4VXde3a2y6lxzbAUfjJQPSGwVNciqO8SkWa8z2Kg_lA66Zd1fx-dAP_4D16w8g-8YKHTOTyhKe-Qg3jGb4FFdK3q1vZe9vWk-_gk9W91zZSL3QxsgNBGqc8i8MTaFksFnjfZVNfN20HG-551W676-AIdtt2DefEPdYIIGwDS9Vbr29AvpfttocXGEhDgdgjLedRGgbhKaS9aIY9ugPF2O623lpumWBb5tW9t5LXjN97C3giWy3m3qsG-BGOy1ts2pFNC0VZllm8f4Dh3PtWAF_W26f4Zf_KEUZheZjHPjvqOYpD1qwB_StcTuGyRk5hXgeHArKyYdvlDFaRG9ngut6Cjbx6KqMyLypxDEnfqd0mLd7b81g42ncB9K1Z3cB_4IxQNYAtRALnY0LM8ygPgnSPpGjuvWRdV8uuf-I09q8cOY1QpgKexA6eE3jfs-5GtHfN-IPwSXvXjjwqFkVYcJkd9agBOwy8Dka-9-oGgYZSuOt12-BiHrD7zayTlexkw-XINhdVEMah8I-iyeqIn589e3vh_cH7bDD3F0jlxRdgTGUaA5iZ_WffNl9-7lw7oiRK4Ue-qI47lO_N9qzhYjh_UlO0MvzEwX6jhpKguPhqJ4xt0Xs4tlMsC-NKHrdTb8B0VfU7eJpFkpo8-M8Nqni4gCxbAzRKOGJEDHW_9kZpkplIhB_GBzSFZFdBQf_pzfffPc2_h5ePsXAV-LHg4tgH4j4AUsDLPK7k02Ocyw2ojsV8uV2vFnRc9PMCtmwle1BD8G2_G7N3Pq-E4PJYshzhuuvqLUoVPFJIvoInbUGzesq2NN72rvWatgHZahCbgFEZISsLWcbzODiWLJAv3JLL5gsUJg8x5v-5PDuQscszgkugfeG7fXkbkTDBIu6HPj_lIK0ekgq7oe3drBgHLoedWnyBDPTlwrsDh8VDeuGS58joY1o_ApuRB_uCH6MuV77DuNLfu3AMqgWhjMIDUf6wp7xA9tWeDO072LV-DIpFlZ_kRZYf8awZaoRty9sVyYR5KigP9C2eXzazfTN77hkXDfT_QNIKHNB9a1-JQPh5eARJXw_aywFcSrOBUddajGgGSAdCW_aAH3bgPXmrMUFJyzir_PIIipRm7XoCQeA0Ij3M4yvJwI1YSn6zaWtgzbYi4jA-4LGt3qgRilgRVSLkwREU_aTOx_v2a1AjBKCqe_XgHmRL9s8VVtr_nol1DS7j2B5leZmxPD9yjxy2hR3asvVGdjO4gMAhu0Y23qIqpg_Yylu3oq5qPoYafVYJnuX71ieBc1fv0j4BnbyDS0cENgr8UgZ5cNST8O1lc12D5zT4KG0DzhRpJuPAwO8ApdobxcnAPQCxmzF3IQllkIXH0bSYgQXBOI8EdAznAUhOKJqqtvMobvO3HbIGnIS6EBYES4jvMobjWeon4gDHfyhNP7I7FN412OJzD9zvpuddrX5pQQWhQy4VmNqAUw6c7PXtrgOwsmH3oyqd-anI9lV6CjRRtIfWc6IvT7DM2H0j_OP7WVnFSXY6DX-Wd8bVWbN7wjCjnnjo-0XG0k_w9hZsY4yPAlJX5f1lAycmdlz_IkVtPndCaJcNPWIEDYCREpFM-elUIoNy4CEAEWW9AtcRTBQFzRDMyZXQrmCP1qFiq1XJAJYv2_ZmHODJMA9LXgSfYBsfhPoW6DNfA2ujYfMWu-amATQP1nTRy1V1xfpediin55dj6iDPqxB8qX1_NZt7r7XK8Uq5ZLd12z3B4e-5ZUw5likv4uK0J38Dagd03kJHexY2toDboBdCPx4NJxrY_qbe0LbfdWNGC3yTLBUHgahjaNPBnD1qNFRHuw5Er0FVrqS4hjNU9hWpGwMdSRBmFWCz02kzsGuPvDGtkJVJEpSyOunRwRw0b9frHTBBAIVwKDAHuA8dFG32AS-Gc5JNgGP9CDz0eZj6aXnavqjIERyZcU6M4APvNO2s3cxHwZef8cI_bXv-HY077gwQsQKm6HcbMPSwW2B70UuaaRwNh7YdEEInK7DFY65myKM8PgiYHCVtCMm-fvHHc0sQsS3BAYWjJa97iaBxJWfE6513vRsDZHEYZYUQ-1oyn3tfd3Wl5AGgsLzung5mvvemsUSBZDxJ5alPXwCTbADwLLxbtqoFImbrbJxbDAu-eYsUnA9BUECuYxbEF0HEouxE6r5C8dLZHBvsBJYGWGBI0xbZW1AyEoDXmm35cjEfA25FnLMoOQjkHLF3t5iAvF8oz6cfEL-5GbgTAKZU36NyQE5b4R5vx3g-SUQel9WJ1H1j7D2QRZkERFCIUxpe45HSarBSqzeU5OHcA1vtdWMnG8kyiPN96oq59x1aDKKuA9lqyC8mWFsTmH5CAj5ogRFpqDLJirIqPyFV1s54__iv_-spgwjqAUB6rxWdOm21OEUm1PnSI8esdFmkZVCKT0mreigSaq2jxztJ4qyO1wlWUD4Z3LG2V878mG1IkioqePoJaX2hwwXgCQJJj-2oEXQSfCM25P2M8iU47EG2v6uBP_e-XdNzKKbTbp7MQz56x1iMNmVVGUXhKc9d1HTtwiOFUsv97dBKBG0SbgbGSnVCH8V3NIZR-kFanUTaS_gen0resgrDgu-Ma3lgVenwNvi9DVDdo9-BPoI3lv1jfhHkWZWeQppOhRE_d2a3-gfZL1KYa8P-AB3QoRv16n1WwLbtkwbw7we4ErANYqwNnlFbUX7YFkk8wVgftMIIo2WpZHEQlp-SrsVadtdytlnBcb158eMfX73xZjPK0Lz8yw__MZ_PFzZfYPXHw-zbQw2XV7LymfiUpL7UKADsVS_xiVsCawTCKduEAT46a4uFOwkcgf7TmIz4shRpwj8lqS8qBI86pkVygvVBrgOlaw3Enh8BHi-cxwitPI6STAT5p6RVZRaACZSE7xpU31a_sBWK0T2l0VZtr1INpI0R3o-6XDKKeXFAKua4m2tQIDWFdD6jBwtjkT5_SoKevn0sKMUBMUdZ-skoetFoz9dGppRLPyyHbn2nQVcnlCFjW1TgY-qHV7kQVM31aei0kSwL3ff-0RVwGELHIgETut9tQLdLNhLFSgVAA1l-QkKVMjL45Jtvv3tltNEL88NXi6FOBxygpQ6K_svIhpYiCHKRfDo6h_s8m_NXSW4TBfQQ4dfrtgGWKBHJ6N1cj8HCMg2DKAv2HbogAoPVAlAvgRrkoAr-JbtNpyz_qLiM3zoiKkUIttlP_U9CiaqhsQ6Gh-WZGBboYa0rZ43FhfHDq_qdt9hs-jIYg3tJnskoLT4JjQubGEKmW9iwDVHkrIHCweBQMVFO9Xd1w1ejgdTEDwIefBoq9-4BqH2H1Ra1rhnyPrs82y7rHuMZsHlX7969W1yefX7uNS15eeO1FnEo_ejAXGOyq12vwaQ-5bwdXDpakyNTPyqOe5JVZENKXpevKV3xs46m_kbO0G8GsLxVN4xoMlkVIkzK9CiqXpnAH_hg1xiSFHVVUWhy2d7hf3WQ4JxMA-gF_ElVxizGgksBSGFZHqA9TC4RHqOyFU5Rqpo9dTzvvWvkpFIuRFlxfurzsdZwwI63gYnXoFtKEScPw_4znduXNu8-x_jpYdj07bkpXz7T4cQr5eTiM-kbU30sr6TMi6qScLChqKowj9PQl2mIcgAiQXt-6BEPCWwqGO_oSVhSbH7DiuK3WJpNNZPDCm65trMIFYIfWcl9qB7pDlCJF0maRlVe-EHOK7-qkiDxyzCOOPxQVCwXZZqVvAjB-eEBT6uEySQqZcxEHHJZ-IjIMDFOhd_quC6y9HfY6J7yZ2E687NZmL7xs4s4ugizf_X9Cx9Ngd5xFCCZVKFfFcAww6e__tOqxYklVTH3kvVLZLMyS0XF80oVStMaTn235tZPUZatHwgvHARxInKeR-aBTqW2fuApBdaAD4CPr--HjC-oNYExaUpFXzZfwv-81wDw5YV1wejifighMkVe_bmKQj37Y73VWZpzz8lxw2242sa4DUusYq2qc3ggCPS6blCl8SHMeK48mdn1rkZ0Q1jp3KxSgk6byapCt12HGtG-Ua4aVS1aJMRAYDt7JP-xVITe5qJKK0BAWRiw2GyzU15uzvXDq8X1umGSijz3k0hSdRit6xSQ63VPrgfXT-NVkVaFjLIirszTnBJx_bSTKr4lZQQ3Eg5ARf7wn-ECOCvwN20w0mGD54AH3MoUuS4lKgGwkUZWHl9HpfpUwK-CrVmqNI6-3SwJHuxi8Yil1TsT5FFeyAT1VWl2xqlQ1ztzSsG5iX3iq5mNU0JS85v7ublJVT3a7KsTuVQhLRV_23Wo9Ic4HNAhWgJUbIUbQ1au3fUrcpBVnlsK64R3IE4rECgnKqy2cUQCqlIWlZ9KziJpdsiplB8k4Mn6d71gFvIqSpIqKYRd0CmJ32P94wrdnZI4rB3FrSeMT7ECtlfWud6vFTZRvpquBTFDL8FNKquAjjYx_ci2ZUmRB4VIA1FZAXeq7PVbnlI77_0FEQ9rHtscLD47p7xOhyFStqYoJOKZAZ5vl127u1ZSo95-5HXiNIrzmCUy4ZnVg0OF_sAFT9bd6wV9yYpIZiwtfWbZaijFtwt-SH29oZFFRZrLMqhYaJZ0Su5N59IJdfTAOgCAlFiOqNso5WXoiyzIBqPh1Nkfqtujiueda21F-cUHtx96v3kf1Vn4nidrPeQS-suqLi21o6o3LjOepwHPospygFP3r3fplGL-GdVC4OPgpebed4plvP94AbgErmu2a2zt64bKBHBm70E7_iK71tZVekbJu2oDiWgklgshIgE8LFHNsl7HV7GWstvpmr0RHZEljGVpGmSl1YROl4HegVNaB66Jn7VeuWwkgUyTvzJ-jVaRQqp6P1Ptrhx1VbxF-qKl9wJ8hoak2zWXDboEdwzRFWDWfrfG81nvqBSX2lBVlFl3oZqsUSW3HA_EYceRPUoTHmQyrcBLT80eOV0Pe3riA_oYDHouyqRKCwHabFAVQ2uDs_PHNits0PJj-E6ySvFrj_FO6S2WweIff__vxTJFt3uD_1rV9GNH9UN07d924BDib1tB_14uztWTqvoaES2WrQACN167CeQv8Nxmg4DOaoE9AbXIv7w8WwD_gIVQoFGHKnfwL128D8u9wViwKY9TYGxPrJTYaXkiehQb0c78C3AQ9V2PHGbIADn7ETiMg1F0WjceauiPbsZAUPOUei5jEQP0Zin37eE7nRqDej6p9wLco7Mv33-3leW9Jf5pClzRogTcw32BhzGsh1Lb9ey2EfPh6n9F-oGwA3aCewyqPvvyUZ3_xTP1iC-f0P1pVJW5QIOYWO_V6Uhx5O_YHhPXpVDXXzZaAS2-eIaG4eAuVVvt7JBqJKBnE-MrfSitn37Z_Bu7Za_pBrwZLv_-px_IIDS4p6AoAYW3wL54HxZWYzUXPa27VV64hmCXTdUBg9y1ADjKXb0S4C2__P41_LtniDZ-If8ZlW7NlzPKdJNOwmpfMIAYzzLqCdM56IH1WmpcLwUT4Jj0YcBMdP9Q4kma3jEiWIs-5hZXaVIElQiSJLCWy2ndGeDgUx05er28YFWeR-CPxtYNc5p0jBv2ob03etWkjLIgquIk54WlcmjH0aue1GWjwnQIthXWgFdTmhp_UrieVuAM9BSlgPewidKYB1eIBz02Fx4NmDg3qTHvrz9-B7-oARLn5OrNtuxaPZl5i0enQICBWrFreta23bSr9hqfhtagUyUU9rV0rpUuxXYEshXqQ10raetrSTJm207aDTO2XyBgwJsocWFL5rT7hJkN0Of1up8_UolqzEURloUsUlZyy2VO75I-v1NaktSu0m623WWjdxR4SwmKMoLgGFBYmHxy3CQtL42L82ijTIIdbKn27H7yhzIQ4949PN9HK0SwJQepv2wG1mhLOn5SHbLuPBw_Qq1D2-3-ASrbMSLBLBZ-kYcsjGK7t04X1h72PK65aoU1taoMq14Tyrxs4OEY7jH9IyqGPfdeDQyG8ALLy9UCCxNCXxCT1w28PEER0G2wL8puzkwMc2EqekEgdVWNii5q_3rJbqUKmNFzn2MQQZc94Nnr0CNqVaIC0QUc6rpFgKviEepGDwMCtiKBGEx_buTisjHSsFntdO2UEgSxJwkU9zaxV9w5tQ5IDhW1yzvaU4JmD9oq1LUID_WKBiPSorrdAt3-aoU8szVHedmAC1eDB3H_uTmAEb8_y0EABU95lthgzdAap9nklI43jHARlDQJavW2nbLVeAYguCCoLWA_9PbuluiH2HAP6C9TbzuU2ZCJVPEOsPrtdunRaJlnIF89aSh1cne6QhwESYGs2mbNdw020oxsTFAmmM1J8lBYv8Tp0Nv3II5qvCOtYmprOwUnauT5HmhVqX4Fj5-DNODSqJT6-hpTVoTZKDdM7hsA9g013KhwLl7EVGBXCAR25ETWnZjBW26pBe0auR3rb56jk2k8xmW7EoT0MdIPBwFajZG6IYS1ViKgX0yI2qIgY488KrJUbwPqdIdNTMpSfgbKEYftfI6B-R6W8Ch1bNIU8MinIvU5B07Nk5LJwio0p0FxgCRPdx1aJzEueCQBSEcDfBgaEZ0jPra7cPuMHGRQMuX9XtaiOqiUBm12U69W2rtWCzmPI9tDjqkbKzVRSg1cSYHBhuLHTB2NB2uPGQkRZjxgQRkHmWVyp-3ReEon9DLqnTOxlAojCGYxFdNuyOXTSrJjd3uvMCagaRYFSZ6nIQVcFXgY2iM17af0PK5aJpS-IDhg9r_ELFnFdqutUcGEyjrzljaZQqJh8hUjb5LwuExFxCp_CFY4TZUDZ39kc6SJxHLBeQpcHpfcCs7QL6mX_9C-R-PgxaLIYlllPLK777RCHoZAj21pdNv4nnA5M54AM4dpmDHhOAOm7dGR5mPbF3V7EXH-wqF1QQqaJBcZhWCvMveq8JIu7IwZE6gO1EtbUDX3_qqaEgejTniRlT0pEfXlmDBUzBdhBKqxsv6201JpjuOU1siFbG7rrm3QCtiRaXjl4Rg1C1PIVC2UHjC_YVzx2sPDVH6yFBfeDlTHyuPd_WbbXndss6w5mTAqPe-HzLYUB51cqEbQDfbQJyZbSVAUfDXJGWgpLbOqhN27a3dwvvAAMD7ORmC93C32JjAysqBYdyi4xID0Po8aVkATm_cYVdcoE2dgjOCyAdY4R90ByBa29pxiu_Q6N_J-3_CagJCx_9bmYh2BCgA8anC1iT3awkZRVkZVlflS2rSG0_U66KEPb2E1WfYkEWEaRVVYWDvjdLXqlU9pUd1SGEZpsJFX9APQgmnoF1xYJeG0sDqEHNuPKtmtreJzGkuYjcaP7H8QgOXNiiCK7S45PawucR_ckGo8bQD4eZSXzGdWPzg9qsOUtuMbTt2kvXJY4Pto7m7aUBpgAifxfAghaE_L-pa3CgOvVEhYu0wGaSOTwf2A9cBrWGtbawXG-t1OwAeuBvupz-dBAgk-2zWKbDESsSg4D8ocUCh4BpZ_hnZavY9H9caaJ4AGr_KIsWyAZE67rH7CKb2vVF7CNuhfwTuvMHjckLUyLi2l0wGNPlqSANynDxmPQMdFa3P6GBMZ_PYVnOFK9bd6Q39rJ57bpsBaeUFme2wBBfiCSxXtxCwUCBI5gmikTE8SA32Kl5Qd5khGTWOVy4yHlS_thjo9vq7uObJhtyMTQaykt5BCOiocsSYvd4mxWeyPMI6J6X3s2wdHNjDL4U7uAxeKz7g7pYwBegZ75YVjyDMss4JXPElkbtNkQ4_xoPE_pl3YhpAZfFglVRRaVet0EBtIckIzMJU5nD8WlPn2awL4NgjqxnXgG3TQ9SdYOgufMGxDAYiqs1DaawXUY5NgWgycqO7YvopQBGkeRty3--r0J-t3P6XV-KWNknfdbqN6KUyZ60IHNM1A3gUKLQaR6sZZYkwFyVJmWRWrEcIqbT30L5uTO6EV2doJFSHGBDUIjIpvaFlXZh7gmpSN8rTZYBvItGIIj1qKR50rCaZPsKSM8swWtjjtzkb8T-hc1sEmcgv2AD_yTlsqlEvAVKtbLPhqGypuc2DoHevdYILW6KN-I3i_ScrKMoksXnN6pQfpPbbV2YSSMxaEfompXZu8cbqfDT-c1Lz8ZJma5EEWiYAL30FuQ1uzIeKkrmQ3Cu4Kfc8qt1Rb7-aMTpyCd2vw5zB2YKOg5yogCf-9W4KKshEPkMudjje0OqjP212zHcIMbnGaiRE_DR1TH7RskgFy8G0oy2mktvm14_ugh94-0wFhkcAIXVzwXDBeFH6QDSxq26ad8toPbYI23n6RMz-o8kCWlvedvmhrXY7vcm6NMGPJHbhml81Q02polcLETHTx3X5lH6oHdEP3FzJshSkJjFy7YnDQGgdWV4qdzeKrOrYhZ0KBP_DMB7DX78XOHzSFHUTQMXVu3PCxHEEFxiCpeBjLwXkYGr31Xp_Stm2y1mb35m4lhE2xq8CKUwmF4cd6zA7nsSzB2QuqMhnA9NAHvl-keVRXt65uJzSNip0R_FUwDXyOISvjrXerbW1gh-p_3W0oGqHR5a6Ec7bMCfz3UzC_bF7j6cD-3QPKBatR_zLkDRA4wdOxfHHIXRqybccy2jDZjdapJaBUSxAkmaTVEEq1PemOlB7bUW44SQq_SBPwbfxgSEraJnMjtSe0iD-jwgeq1CJlhq4NaDAGxveJJP_5UGMB9JtUu4aFnCpGL4ntMDhDkMUyJmV07qlPr27AlaVvTZyCkuuqbkCnCWElDxH_ucsquvhKw0H1-B6OEuUVz7AC5thSWHLLYHc0EkWYojumlbOAR7-zgVSV_tT4ou1unussAdZU6WWIYBW8VE4fwUOdf3Wc7bGqr6QKASNwIXJrfJx-fKMfTuim74agLfVpfY2a9FohelTbWlnTMetaHlUIT07Vrp_hZfpI12V9vWt3vSqLAAa9bICFUUq0tQdgIjtVma8ebPf-exThDbJMe4coVp-lYQq6ngJ94BVi1k1caP9c53WU1DMPILjy2uVWKYcxyx6xoPR5UMjBjXImCBjLfkr_PxL1Hjnr5OCW4SrELcCdumlf5VaV5jLh-x6DnK6NciJ0qCgURlKgy1amqF432m_7mMsG-U55ByqzQoBcVWRQs0OFQbjtw2iVCjlrBrd9IpSHtK48Jcj1g5XdRFnFvL-Npey527BTOiH_zObjn5lUvPESdVRQuTUzBTq06cbmxDGfK8pzHkeSVb4NLDnDF_YK5o4bnVAPPTPY3PWdA7sViIWTdmFog7KnshUKk6LuUQ9XR1ijp84wSl_tVpd4Qo3NuDvZMlRTYClx8aE0YwjR12jXWxNzpJgOACNlC1Vs56Cyhpm5Bsh6Q1HBSFg1KVM_LEvJskGChmERjnU7atqDKToNsMYtSBhnTmTQDoAYGo2OnuBg43NEFqhnFQA7bKHpdbkNLAarUz2P7W8414KknQydaBiNG3OeibyUSWLxuzMu4jDNd8y8h_XgWDCjItFZHlYDNeKsZm8zEaAh7LP_j72QBH-oXtN7gfWiwx-Tcu7THxCVbLu_zNC05rTW0itSjenA_w9frh7QylPFswlnsSiZFKmNHjmjL_ZR0lGzK6wPol_qM60HyBidP-ixQx_FJEM_P98rjHLGUaAlRHf1sjEZCRMm0T18Jvbc7RxFQaEcEyavnSg8ZbuYYgilXbZOkEyLpjlVldsrMcIC5mG7BI2kjIDG25RW1Ix32eDNFEN2zgZubHegbMRzz5FG0oeq1OV2rwmDwo0AujEsC4BBpduc7IXZuVV9IwkYKmFVr0FJ3nFjIJIwEiwcCtidmSImy3DCUBCyrFbe4E2ogg83THF_b9OTaxX4MJ1p-CoqWfleMX5-2fwUDOB4vxyikzNdHWrv0xw8VstYREkqUlHJ2GohZ3aJo8E_egCJKYQpBa-CNA1YbLW3M5Nkr2fxuMEiFwtVKsi81396MQuTlGDnABrqXxxsRl5zf4MQtm3m3p_1FQpJ6LANOTpbdt0rXlybBm3saNPYpz9XkXNJfbXAw8axoIq7DYojdvuAb7ll79Qyd0sEahuGvXC4GojrHUbEtu2NxEqjvn0woaTfdbeqgofgGMVSKGCKhYiAhBpV0Y4hHdQdQzMHBsfs08CMXWNL7edEICDujdIowG93yhBeas2g-JStrrFtabk222yqofb2lHYM60Axzi9VMA_4Ga0LIXIqEnC-VGuNJZDzKiyyqqqceklnMIyNO50y3UWoMIqOTF42j3U0upXsd5IKEjpqz1ZqEzPRbXtDxRG7jcGBFGO6bEwM65VueDXlxToeRmUDqhiGMr5SFTc5ZFP5F7AWTio5xy4x0yCtVu6HGATr4MwoWvLqHSI9bM73CTbaQtEayzoC_VnTIidvRxN6UkQy4TwPg8Q5Ajv1Rh_BaaNrKIFxgXYGiaGKJZXWp54pNBl7IkrB-4N9VIvZMiBVDcCwEERViWHtG4Jq0JVYKaJ4Q6-NUQhC-MoGouiQ7SO9o1hjXyacWAQSTJKFXrzx2rYocwjGd41Av0eV3KC5Zt1Mefz4UOwghBPvRysoIt8PQB2HVTH0NNppPo4ufnJEj0kUViLNykJGTpDOmdpziDGPGsWjb7DARN0CLq4J0yuX7SBcv3-zzlTqe2fUEHVwhQpg4wV7n6uou0ZoYIcx4vKXv77Zv0YnnrDWUueP_vzi-_11RuNiSNLwC7za28eJfJ-__9j9H7dBY4DULP4Vrby_a66udGgexchFGLHYj4uCC1vU6AxVMgb7hElJplWzV9_W9B2GYXVPqEqi2PZ9Jz41EmjNuF8GUZwHhZ0i44xdcoTnYwYomcWDKgc5lIUcCiCdmUrOX2I8ejqSh4MyjGd_G4JpGUJDhykkU6ChhVQV4c6pJMiMxBgKnJVOJL9jKJV67pSCPTqKZE4FRC9Zv9NdVTtVW2FfyVSEmcQrM_UybqLVrDyncqKXj5czewrru5XfNqpCmtktkp5TqdH3rEG6VACEwpQVq1dGjTwzMJg0sU014ztlSAWl9R0XjKw-LtAfrAA35HPvQQL7IGuycGpuVT2ArbtFcgsk90aZysEtUjkpN014UAykUEgzzCcBz0DnBWBRzOn9qLPNuLTluh7gqWmLeaTbSNfR3ey1EpkQlYVA-ABg5pduRtP0DLojZ3C1wTrusF_FzWpqMASLhTYDqRP9ijCM4_e1LsjUiJ_phKLKHwyDagy-wOUiakaj2qcHFT61UwSvURdrhrAaRkvBYuMqsV7Fzluym2hPidxqVUX_WIP4YpijgCkFA9ZxvsrdTBdS0CwmfBwIwH5cYeGkRB9zNz8b6nD0251rF_LzIZmsM4OD96niTg8DAyr7_nRsAEkFCbMwW1F53YATpZrLFBZGQ6WdEjUk514FKdYMBxSodhdbmKJnVu2zCyEjVVYIRBha8PEgpHCsTgHHjAqqPVPn7B7xhxc448ogzd99QCpSJw_tLq-AS1HIVOhUnxquV7w3Z2dMtakyYgfTuEzqwyPIYQcjUbaLaKdsAFoGH9nUphgUxDBFHirlZNv7dExoCFqvdA5KxyR6kw0w7KGK4bTSw9d_NmRhLVGPSXQI6uE1W-sqT2cGj-PwDRESLRkGxOGzdb6mPyCe3hi0xdd2FRt7Rc16mFg0MRnT9NIP6Q77fqjAUF7J-ycTw1yJe9hE-_Z3tPyP_GV1q9adv6tOf6XdaP-9zx__O-zqz8ybfg384kfwJlgn_lf-iXZKeR33F9rzJIqjgDz5YeTkN6zfUqD6iSGX7nVjQ9STIEzjKvv4Z_xVl478_OOrF19__-rtZ_P5M_UjbO7nqinM1C3tmrmnrlc1_6N_RCbPslzKjyfoN-8N62-838CqM-H9dtn8NpvN6P_wo_dy2bYUTtGIT4EDlVL_zXvtDAhQEyxxtqbyKt53JgeE6CGaLyg0zbwt0EJ2VQAu0tQ_LGCiSJCJ3qopAKZlYf6-c_r_-lznOP75z33rnPmvZ-DLwfq2EQUwQI0FJWD_-G4YJckIAM8Uo1EfAAgnlkm0Xg_gD0dyfvCI1FyEmYhKXiYcFEAA752XccEC-7bu7FN37qc7D_XXSZb_N8ryh0_DPZwGG_3--KzXpwbffpLptkUQciZFVORRIUXFgzJMMybg7ioHt1zGImVREcUBL3leRRUPozwrYrgr91lOTRmPvc_hcNsguEiyiyB9ZLhtXsk0wlrrabjtNNz2Uw63BRYWgeBJKLndZkdNDuGmJ9SfKaSQQQLiJP2osDW3jkbUy52i6dSpov932dgzp0yR0lv0Y6vLPtDZeWji3l8LKiNZ-CJjQVEMvS5WfWrqT1OLqvPdC_7x9_-O6WZYhlxaZyoOGyZ_ObckcEuubvkTVYdXFc0mIQ9Ee23O5QVcHoTq-q9wopSaVoP8pUTEpSbCixPvtwdKexqDPI1BnsYgT2OQpzHI0xjkaQzyNAZ5GoM8jUGexiBPY5CnMcjTGORpDPI0BnkagzyNQZ7GIE9jkKcxyNMY5GkM8jQGeRqDPI1BnsYgT2OQpzHI0xjkaQzyNAZ5GoM8jUGexiBPY5CnMcjTGORpDPI0BnkagzyNQZ7GIE9jkKcxyNMY5GkM8jQGeRqDPI1BnsYgT2OQpzHI0xjkaQzyNAZ5GoM8jUGexiBPY5CnMcjTGORpDPI0BnkagzyNQZ7GIE9jkKcxyNMY5GkM8jQGeRqDPI1BnsYgT2OQP2oM8tvf_wdBSMya)

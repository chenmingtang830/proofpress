[//]: # (ob:7437c9be)
# Portable Artifact V1 — Executable Contract

[//]: # (ob:b27d1410)
> Status: implementation contract derived from the approved strategy and privacy decisions.
>
> Scope: Markdown and static HTML carriers, local/Git ledger, sequential and
> parallel handoff, deterministic integrity, agent-guided merge, and
> best-effort capture. Source code is out of scope.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzY1MWI2YmNjNWMyNTAzZTJhMmVhMmE1ZiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImNlNWYyMGY5IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9lZTg5ZmZlZDI1MmRmZjI4NDYyMGU2MmUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzUzZDQ5NmU1MWI0MGIwNWE0YmE1ZmZmMyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNq1fety40aS7qsgND_WjiUpXIib2uuInnbPrDfaMw53jzc2hg6xUFUQsSIBDgBKLXscsb_2Ac45TzhPcjKzLihQaqhNajoc3RIJVBWq8vLll5nwLxes7auS8f66EhdXF_v9dRIHRVJwHvMw9iMZslCykMXlxeyiaMTDtahuZNfDtd2GhXFyteSCpTxh-TKKgiAIkzIs2VIWgkdRHC2DNChZVPhBGqZhAL9lskySPA45DwM_yiSMK6qON3eyfbi4-gV_6a97dgMz1PJjD19vWSG38OuPsq3KihVb6bXyruqqpvY2cHXTPnjFg_d92zTlvpVdB_fsGb9lNxIfafRx2_y3hIc9tDjgpu_33dXl5U3Vbw7Fgje7S76R9a6qb3pW32SRfzm6u5V_O1Tw8_Whk-01b-pO1rATfXuQv84uNpLhFnIZl6Ff5hfqk2t5RxfB1sprKbO8LKUI41CUZZgtk9CXSYh7sG_aHh_telvVElZuzmN7HUdimScSjmXpF37MlgWcRllG6nH06q4523eHLTxwiOvkTSu6i6u__nKhp__lAs64aTv8SX0txXUBG_7XC94I-fHiJ3gCIwswsWh4d_n9n3_48Pr3795ev_7hw7d_eP3mw_X779--WezExew3yQ3r-7YqDj0c2HXBuqrDvWdtjeuG70CcJA156DdNiyu8rWoctXuAb3bwTc12eJRqpbOLDm6EsS6u6sN2C-vmGzgtqZ632Db8Fq5Nl1HK8wK3Fg6qR0m6uvheb7L3Wq_e-zHw_vE__897-1Hyg_rqDVzdMrhNL4IJQavbo8zJe_jkd97nj8NRgPuHPS4fxQFE6-LX2bDMIkxFsAz8f8Iyv_be96w_dFdetdtv5Q7kgOEReFyvzBOgUHdSeGXb7Lx-Iz22B4nCT4ZF7xnM4q44yspEJBkfrThYDGvdN9uKP0xu4O-8J2-Y2Cee85CJTJ4x61u0MJ6RWzAhXbO9k53XN578CJ9sH7ymlnqgq4kdCJJlwtNleMZa1us13reqq5u6aWHDPa889IcWjuDQNzs4J-6xWsDC9jBU1XtdDfq9afoOHmBYGirEaGkZj5IwCM9Z2ut62KN7MIzNofd2smeC9cyrOm8rbxh_8NYwI9uuF97bGuQRjstb75uJTQtFURTpcnyA4cL7VoBcVv1z8jK-ckJQWAZm1WcnzaMkZMdqsL_ClRQuK5QU5rVwKKAre9Zv5jCK3Msax_XWbOLRExkVYPfFKUt6p3abrHhnz2PtWN81rG_Hqhr-gTNC0wC-EBe4mFJinkVZECSjJUUL7w1r20q23TOnMb5y4jRCmQiYiR3NE3jfsfZWNPf19EQ40-jaiamWIg9zLtOTphqwwyDr4OQ7r6oRaCiDu9s1NQ7mgbjfzltZylbWXE5sc14G4TIU_klrsjbir5eXP115v_O-GNz9Fa7y6itwpjJZApiZ_3fX1F9_6Vw7YSQK4Ue-KE87lO_M9uzgYjh_MlM0MvzEwX-jhZJguPj2IIxv0Xs4tVMsDZelPG2nPoDrKquPMJtFknp58M8tmni4gDxbDWuUcMSIGKpu502uSaYiFn64PFpTSH4VDPS_f_ju3fPye3z5lAiXgb8UXJw6Ie4DIAW8zONKPz3GudyD6VgvNv1uu6bjop_XsGVb2YEZgm-7w5S_83kpBJenLstRrvu26lGrYEoh-RZm6sGyesq31F5_33h1U4Nu1YhNwKlMLCsNIe7IlsGpywL9wi1Z1V-hMnmIMf9tdXGkY6sLgktgfeG7sb5NaJhgEfdDn59zkNYOSYXd0Pfut4yDlMNOrb9CAfp67d1DwOLheuGSVyjoU1Y_Ap-RBWPFX6ItV7HDtNEfXTgF1YJQRuGRKn_eLK9RfHUkQ_sOfq2bgmJR6cdZnmYnzDVHi9A3vNmSTphZwXhgbPFqVc_HbnbmmRAN7P-wpC0EoGNvX4pA-Fl4wpK-GayXA7iUZQOnrq0YrRkgHSht0QF-OED05G2nFCUplmnpFyesSFnWtiMQBEEjrod5fCsZhBEbyW_3TQWi2ZS0OOQHPNbrjZpYEcujUoQ8OGFFP6rz8b79BswIAajyQU3cgW7J7pXCSuPvmdhVEDJO7VGaFSnLshP3yBFb2KGe7fayncMFBA7ZDYpxj6aYPmBbb9eIqqz4FGr0WSl4mo29Twznrp6leQY6eUeXTihsFPiFDLLgpJnw6WV9U0HkNMQoTQ3BFFkmE8DA7wClmlslySA9ALHrqXAhDmWQhqetaT0HD4I8jwR0DOcBSE6oNZVN6xFv87cDigachLoQBgRPiM8yheNZ4sfiCMd_7pp-YPeovDvwxTMPwu-6422lfmnABGFALhWY2kNQDpLsdc2hBbCyZw-TJp35iUjHJj2BNRHbQ-M57MszIjN134T8-H5alMs4PX8Nf5L3JtTZsQfCMJOReOj7ecqSF3h6C7aR4yNC6rp4WNVwYuLA9S9SVOZzh0Jb1TTFBBoAJyUimfDzV4kCykGGAEQU1RZCR3BRRJohmJNboUPBDr1DybbbggEs3zTN7TTAk2EWFjwPXmAbH1F9a4yZb0C00bF560N9WwOaB2-67uS2vGZdJ1vU09lqyhxkWRlCLDWOV9OF916bHK-QG3ZXNe0zEv6JW6aMY5HwfJmfN_MfwOyAzVtrtmdtuQXcBj0QxvHoONHBdrfVnrb9vp1yWhCbpIk4IqJOWZsmc0ar0VAd_TosegemcivFDZyh8q-4uinQEQdhWgI2O39tBnaNljdlFdIijoNClmdNHSzA8rad3gFDAiiEQ8Qc4D4MULTbB7wYLkg3AY51E_DQ52HiJ8V5-6KYIzgyE5wYxQfZqZt5s19Mgi8_5bl_3vb8Jzp33BlYxBaEojvswdHDboHvxShprnE0HFo_IIRWluCLp0LNkEfZ8ogwOUnbEJJ98_qPM7sgEluCAwpHS151EkHjVs5J1lvv5jAFyJZhlOZCjK1ktvC-aatS6QNAYXnTPk9mfvKmqUSBZDxO5Lmzr0FI9gB41t4d21YCEbMNNmYWw0Js3uAKZgMJCsh1yoP4IohYlJ65ut-jeulsjiU7QaQBFpilaY_srSkZCcBrx3q-WS-mgFu-zFgUHxE5J-zdHSYgH9Yq8ukGxG9uBukEgCnV92gcUNK2uMf9lMzHsciWRXnm6v5g_D0sizIJiKAQp9S8wiOl0WCkRm8o6cPMA1_ttVMnG8kiWGbj1eUL7x16DFpdC7pVU1xMsLYiMP2MBnzWABPaUKaS5UVZvOCqrJ_x_vG__8dTDhHMA4D0Ths6ddpqcGIm1PnSlFNeusiTIijES65VTYoLtd7R460kdVbH65AVlE-GcKzpVDA_5RviuIxynrzgWl9rugAiQVjSUztqFJ0U36gNRT-TcgkBe5COdzXwF963O5qHOJ1m_2we8sk7pjjahJVFFIXnzLuu6Nq1RwalkuPt0EYEfRJuBnKlOqGP6jvJYRR-kJRnLe0NfI-zUrSsaFiInXEsD7wqHd4ev7cE1QPGHRgjeFPZP-bnQZaWyTlL06kwkufW7Fb3KPtFBnNnxB-gAwZ0k1G9z3LYtvHSAP59D1cCtkGMtcczakrKD9siiWcE67NGmBC0NJFsGYTFS65rvZPtjZzvt3BcH17_8Me3H7z5nDI0b_78_X8tFou1zRdY-_E4-_bYwmWlLH0mXnKpbzQKAH_VSZyxJ7BGIJyyTUjw0VlbLNxKkAiMn6Z0xJeFSGL-kkt9XSJ41JwW6QnWB7kBlK41EKM4AiJeOI-JtfJlFKciyF5yrSqzAEKgNPxQo_m29oVtUY0eKI22bTqVaiBrjPB-MuSS0ZLnR0vFHHd9AwakIkrnC5pYGI_05XMa9PztU6QUB8QcpcmLreh1rSNfy0ypkH4YDsP6VoOuVihHxno04FPmh5eZEFTN9TLrtEyWhe6jP7oCDil0LBIw1P1hD7ZdsgkWKxEADWTxggtVxsjgkz98--6tsUavzQ-_Xw91OhAAbTQp-i8TG1qIIMhE_HLrHO7zbM5fJbkNC-ghwq92TQ0iUSCS0bu5m4KFRRIGURqMA7ogAofVAFAvYDUoQSX8Jdt9qzz_pLpM3zqhKnkIvtlP_BdZiaqhsQGGh-WZSAt0MNa1M8b6ysThZfXRW-_3XRFMwb04S2WU5C-yxrVNDKHQrS1tQytyxkDlYHComCin-ruq5ttJIjX2g4AHL7PK0T0Ate-x2qLSNUPeF6uLflN1yGfA5l1__Phxvbr4cubVDUV507UWy1D60ZG7xmRXs9uBS30ueDu6dLImRyZ-lJ82kzVkQ0pel68pW_FXzab-nYKhvxvA8pO6YcKSyTIXYVwkJ63qrSH-IAa7QUpSVGVJ1OSmucd_NUkwI9cAdgF_UpUx6ylyKQAtLIojtIfJJcJjVLbCiaWq2HPH88m7Jk4q4UIUJefnzo-1hgN2vAsMX4NhKTFOHtL-c53blzbvvkD-9Jg2_WlmypcvNJ14rYJcnJO-MdXHk6XVoBK058cR8ZDApoLxlmbCkmLzG1YU_4Sl2VQzOYzglms7g1Ah-ImV3Mfmke4Ak3gVJ0lUZrkfZLz0yzIOYr8IlxGHH_KSZaJI0oLnIQQ_POBJGTMZR4VcMrEMucx9RGSYGKfCb3VcV2nyK2x0R_mzMJn76TxMPvjp1TK6CtN_9f0rH12B3nG3ov1X59Nf_mnV4iSSqph7w7oNilmRJqLkWakKpWkMp75bS-tLlGXrCeGBg2AZi4xnkZnQqdTWE55TYA34AOT45mHI-IJZE8hJUyp6VX8N_3nvAeDLKxuC0cXdUEJkiry6mWKhLv9Y9TpLM_OcHDfchqPtTdiwwSrWspzBhKDQu6pGk8YHmnGmIpn5zaFCdENYaWZGKcCmzWVZYtiuqUb0b5SrRlOLHgkxEPjODpf_VCpCb3NeJiUgoDQM2NJss1Nebs7186vF9bhhnIgs8-NIUnUYjesUkOtxz64H17PxMk_KXEZpvizNbE6JuJ7trIpvSRnBvYQDUMwf_hkugLOCeNOSkY4YvAI84FamyF0h0QiAjzS68vQ4KtWnCL8Stmaj0jj6djMkRLDr9ROeVu9MkEVZLmO0V4XZGadCXe_MOQXnhvvERzMbp5Sk4rcPC3OTqnq02VeHuVSUluLfDi0a_YGHg3WIhgAV2-LGkJdrDt2WAmSV55bCBuEtqNMWFMphhdU2TmhAWci89BPJWSTNDjmV8oMGPFv_rgdMQ15GcVzGubADOiXxI9E_rdDdKYnD2lHcesL4xBWwUVnnblwrbFi-iq4FNcMowU0qK0JHu5huYtvSOM-CXCSBKK2CO1X2-inPqZ33_oyIh9VPbQ4Wn80or9MiRcp2xEIinhngeb9pm8ON0hr19BOPs0yiZbZksYx5au3gUKE_SMGzdfd6QF-yPJIpSwqfWbEaSvHtgJ9TX2_WyKI8yWQRlCw0Qzol96Zz6Yw6ehAdAEBKLSfMbZTwIvRFGqSD03Dq7I_N7UnF8861tqL86rPbD72_e7-ps_ATM2s75C70521V2NVOmt5lkfIsCXgalVYCnLp_vUvnFPPPqRYCp4OHWnjvlMh4__UacAlcV_c7bO1rh8oECGYfwDr-LNvG1lV6xsi7ZgMXUUssF0JEAnhYopllneZXsZayPeiavQkbkcaMpUkSpIW1hE6Xgd6Bc1oHbkietV1Z1ZJApslfmbhGm0ghVb2fqXZXgboq3iJ70dBzAT5DR9Ie6lWNIcE9Q3QFmLU77PB8dgcqxaU2VMUy6y5UkzUqZc_xQBxxnNijJOZBKpMSovTE7JHT9TCyE5_Rx2DQc17EZZILsGaDqRhaG5ydP7VZYY-eH-k7yUolrx3yndJbb4L1P_7n_643CYbde_xrW9GPLdUP0bV_O0BAiL_1gv7erGdqprK6QUSLZSuAwE3Uboj8NZ7bfFDQeSWwJ6AS2derizXID3gIBRo1VXmAv3TxPgz3AblgUx6nwNhIrZTaaX2i9Sgxop35F5Ag6rueOMyQAXL2IwgYB6fotG48ttC_uRkDQc1z5rlYiiVAb5Zw3x6-06kxmOezei8gPLr4-tN3W10eDfFPM-BqLUrBPdwXmIxhPZTarsu7WiyGq_8V1w8LOxInuMeg6ouvn7T5X12qKb5-xvYnUVlkAh1ibKNXpyPF0b9Te0zckEJdv6q1AVp_dYmO4eguVVvt7JBqJKC5SfCVPZQ2Tl_V_8Hu2Hu6AW-Gy7_78XtyCDXuKRhKQOENiC_eh4XVWM1Fs7V3KgrXEGxVly0IyH0DgKM4VFsB0fKb797D3x1DtPEzxc9odCu-mVOmm2wSVvuCA0Q-y5gnTOdgBNZprXGjFEyAY9KHgTDR_UOJJ1l6x4lgLfpUWFwmcR6UIojjwHoup3VngIPPdeTo8bKclVkWQTy6tGGY06RjwrDP7b3Ro8ZFlAZRuYwznttVDu04etSzumwUTYdgW2ENeDRlqfEnhetpBM7ATlEKeIRNlMU8ukI86rG58ugFEzOTGvP-8sM7-EW9QGJGod68ZzdqZuatn3wLBDioLbuhufpm32ybG5wNvUGrSijsY-lcK12K7QjkK9SHulbS1teSZsz7VtoNM75fIGDAmyhxYUvmdPiEmQ2w59WuWzxRiWrcRR4WucwTVnArZU7vkj6_c1qS1K7SbjbtqtY7CrKlFEU5QQgMiBammBw3SetL7eI82iiTYAdfqiO7H_2hDMSEd4_P98kKEWzJwdWv6kE0moKOn0yHrFoPXz9CrUN9Pz5A5TsmNJgthZ9nIQujpd1bpwtrhD1Pa67aYk2tKsOqdoQyVzVMjnSP6R9RHPbCezsIGMILLC9XA6wNhb4mIa9qeHiCImDbYF-U35wbDnNtKnpBIXVVjWIXdXy9YXdSEWY07yskEXTZA569ph7RqtIqEF3Aoe4aBLiKj1A3ekgI2IoEEjD9udGLVW20Yb896NoppQhipAnEexvuFXdOjQOaQ0Xt8p72lKDZo7YKdS3CQz2iwYg0qG63wLC_3KLM9OYoVzWEcBVEEA9fmgOYiPvTDBRQ8ISnsSVrhtY4LSbndLwhw0VQ0iSo1dO2ylfjGYDigqI2gP0w2rvfYBxi6R6wX6bediizIRep-A7w-k2_8ejVMpegXx1ZKHVy97pCHBRJgazKZs0PNTbSTGxMUMSYzYmzUNi4xOnQG0cQJzXekVUxtbWtghMVynwHa1WpfgWPX4E24NBolLrqBlNWhNkoN0zhGwD2PTXcKDoXL2KK2BUCgR0FkVUr5vCUPbWg3aC0Y_3NKwwyTcS4abaCkD4y_XAQYNUYmRtCWDulAvrBhKgsCjL-yKMiS_U0YE4P2MSkPOUXYBzxZTtfIjHfwRAepY5NmgKmfI6pzzhIahYXTObWoDkNigMkeb7r0AaJy5xHEoB0NMCHoRHROeJTuwv7SwqQwcgUD6OsRXlUKQ3W7LbabnV0rQZypiPfQ4Gpy5UallIDVzJgsKH4MVNH48HYU05ChCkPWFAsg9QKudP2aCKlM3oZ9c4ZLqVEBsEMpjjtmkI-bSRbdj96hCkFTdIoiLMsCYlwVeBhaI_Uaz-n53HbMKHsBcEBs_8FZslKdtj2xgQTKmvNU9pkCqmGyVdMPEnMl0UiIlb6A1nhNFUOkv0bmyMNE8sF5wlI-bLgVnGGfkk9_Of2PZoAbynydCnLlEd2951WyGMK9NSWRreN75mQM-UxCHOYhCkTTjBg2h4dbT61fVG3F5Hkr521rslAk-aioBDsVe5eFV7Sha1xYwLNgXpoC6oW3l9UU-Lg1AkvsqIjI6K-nFKGkvkijMA0ljbedloqzXGc0xq5lvVd1TY1egH7yjS88vg1ahamkKtaKztgfkNe8cbDw1RxshRX3gFMx9bj7cO-b25att9UnFwYlZ53Q2ZbiqNOLjQjGAZ7GBOTryQoCrGa5AyslNZZVcLu3TcHOF-YAJyPsxFYL3eHvQmMnCwY1gMqLgkgPc-TjhXQxP4TTtV1yiQZyBGsahCNGdoOQLawtTPidulxbuXD2PEaQsj4f-tzsY5AEQBPOlztYk_2sFGUFlFZpr6UNq3hdL0OdujzW1hNlj2ORZhEURnm1s84Xa165HNaVHuiYZQFm3hEPwArmIR-zoU1Ek4Lq7OQU_tRJbuzVXxOYwmzbPzE_gcBeN40D6Kl3SWnh9Vd3Gc3pJpIGwB-FmUF85m1D06P6vCWttMbTt2kvQpY4Pto4W7aUBpgiJPlYqAQdKRlY8s7hYG3ihLWIZNB2ihkcD9gPYgadtrXWoWxcbdD-MDV4D_1-TxKIMFnh1otW0wwFjnnQZEBCoXIwMrP0E6r9_Gk3lgzA1jwMosYSwdI5rTL6hnO6X2l8hK2x_gKnnmL5HFN3sqEtJROBzT6ZEkCSJ8-ZDwCzYtW5vSRExni9i2c4Vb1t3pDf2srXtmmwEpFQWZ7bAEFxIIbxXZiFgoUiQJBdFKmJ4mBPcVLihZzJJOuscxkysPSl3ZDnR5f1_ac2LDbkosgUdJbSJSOoiN2FOVukJvF_ggTmJjex655dGSDsBzv5Bi4ED_j7pRyBhgZjMoLp5BnWKQ5L3kcy8ymyYYe48Hi_5Z2YUshM_iwjMsotKbW6SA2kOSMZmAqc5g9Rcp8-w0BfEuCurwOfIMBuv4ES2fhE4ZtKABRdRZKR62AemwSTKuBw-pO7asIRZBkYcR9u69Of7J-9nNajd9YlrxtD3vVS2HKXNea0DQv5F2j0iKJVNXOEFMmSBYyTculWNqTc_qXzcmd0Yps_YRiiDFBDQqj-A2t68rNA1yTslaRNht8A7lWpPCopXgyuJLg-gSLiyhLbWGL0-5s1P-MzmVNNlFYMAL8KDtNoVAuAVNtbrHgq6mpuM2Bofesc8kEbdEn40aIfuOEFUUcWbzm9EoP2ntqq7OhklMWhH6BqV2bvHG6n408nNW8_GyZmuRBGomAC99BbkNbs1nEWV3JLgvuKn3HSrdUW-_mnE6cyLsdxHPIHVgWdKYISfj3fgMmyjIeoJcHzTc0mtTnzaHuB5rBLU4zHPHz0DHxwcrGKSAH31JZTiO1za-d3gc99PaZDgiLBCbWxQXPBON57gfpIKK2bdopr_3cJmgT7ecZ84MyC2RhZd_pi7be5fQu58YoM5bcQWi2qoeaVrNWKQxnoovvxpV9aB4wDB0PZMQKUxLIXLtqcNQaB15XioPN4qs6tiFnQsQfROYD2OtG3PmjprAjBh1T5yYMn8oRlOAM4pKHSzkED0Ojt97rc9q2Tdba7N7CrYSwKXZFrDiVUEg_VlN-OFvKAoK9oCziAUwPfeDjIs2Turp1dTuhaTTsjOCvgmkQcwxZGW932PaVgR2q__WwJzZCo8tDAedshRPk78dgsarf4-nA_j0AygWvUf085A0QOMHsWL445C7Nsm3HMvow2U7WqcVgVAtQJBkn5UCl2p50R0tP7Sg3kiSFnycxxDZ-MCQlbZO50dozWsQvqfCBKrXImGFoAxaMgfN9Jsk_G2osYP0m1a5hIaeK0RWJHZIzBFmsYFJG54H69KoaQln61vAUlFxXdQM6TQgjeYj4Z66o6OIrDQfV9B0cJeornmEJwtETLdkz2B2NRBGm6I5pFSzg0R8skarSnxpfNO3tK50lwJoqPQwtWJGXKugjeKjzr06wPVX1FZchYAQuRGadj9OPb-zDGd307UDaUp_WN2hJbxSiR7OtjTUds67lUYXwFFQdujlepo90V1Q3h-bQqbIIENBVDSKMWqK9PQAT2arKfDWx3fvvUIX3KDLNPaJYfZZGKOh6IvogKsSsm7jS8bnO6yitZx5AcBW1y14ZhynPHrGg8HmQyyGMct4gYDz7Of3_uKhP6Fkrh7AMRyFpAenUTfsqt6osl6HvOyQ5XR_lMHRoKBRGUqDLVqaoXjfabzvNqka5U9GByqwQIFcVGdTsUCIJ1z9mqxTlrAXc9olQHtKG8pQg1xMrv4m6inl_y6WMwm3YKZ2Qv7T5-EuTijdRomYFVVgzV6BDu25sTpyKuaIs48tIstK3xJLz8oVRwdxpr06ohp4ZbO5658BuBWLhpF0YWqPuqWyFwqRoe9Tk6ggrjNQZsvTlYbvCE6ptxt3JlqGZAk-Jgw-lGQNFX6FfbwznSJwOACPlCxW3c1RZw8x7DVD0hqKCCVo1LhI_LArJ0kGDhpdFON7tpLc9mKLTAGvcgphx5jCD9gUQQ6PRyW9wsPwcLQvMsyLAjltoOl1uA4PB6FTPY_sbZlqRdJChEw2TvDHnqcgKGccWvzuvizhO853yvofdEFgwYyIxWB5GAzPijGZvMwzQQPuM_9gLSfGH6jW9F1gvOvzPpJz79Ae0StaPhxma1pzWWnpEqjEd5P_xw1UDWnmueDbmbCkKJkVi2SPn1RdjlHTSuytsDKIf6gttB8gZzR712GGMYpKhX85GhVHO6yjQE2K4uqpNRsLQJLqHz3DP7cExFETlGJq8clh4ynYxJRDKuvQOSaZV05yqyu0VyLCAe-g3YJGUE9B4m9KKWvBWNd5MHLJzNnBjcwBjI155jjaSPVSlLnejJgyiGwF0Iy0LgEGl25zshdm5bXUrCRgqZVWPQUneaWcg4jASLBwK2J13ipgswxkvBSHPavUNnoQq-HDDlPR3Nj25U8SH6UzDR1HJyk-q8atV_WMwgONxOUQr57o61N6nJXiqljGP4kQkopRLa4Wcd5c4Fvw3v4DEFMIUgpdBkgRsaa23806SUc_iaS8WuVqrUkHmvf_31_MwTgh2DqCh-tnBZhQ1d7cIYZt64f1JX6GQhKZtKNDp2U2nZHFnGrSxo01jn26mmHNJfbUgwyawoIq7PaojdvtAbNmzj2qY-w0CtT3DXjgcDdT1HhmxvrmVWGnUNY_eUNId2jtVwUNwjLgUIkyxEBGQUK0q2pHSQdsxNHMgOWZnAzd2gy21X9ICAXHvlUUBebtXjnClLYOSU7a9wbalzc5ss6mGGu0p7RjWgSLPLxWZB_KM3oUQORUJOF-qsaYSyFkZ5mlZlk69pPNiGMs7nfN2F6FoFM1MruqnOhrdSvZ7SQUJLbVnK7OJmeimuaXiiMPe4EDimFa14bDe6oZXU16s-TAqG1DFMJTxlaq4yVk2lX-BaOGbSmbYJWYapNXI3cBBsBbOjNiStx8R6WFzvk-w0RaKVljWEejP6gYluZ9M6EkRyZjzLAxi5wjsW2_0EZz36hpKYFyhn8HFUMWSSutTzxS6jJGKEnl_tI9qMFsGpKoBGBaCqCoxrH1DUA22EitFlGzosZGFIISvfCCqDvk-sjtKNMY64XARuGDSLIziTdTWo84hGD_UAuMeVXKD7pq1cxXx46TYQQgn3k1WUES-H4A5Dst86Gm0b_NxbPGzr-gxicJSJGmRy8gh6Zy39hxjzJNexaNvsMBE3QIhrqHpVch2RNePb9aZSn3vnBqijq5QBDZeMPpcse4aoYEfRsblz3_5ML5GJ56w1lLnj_70-rvxOJO8GC5p-AUe7aenF_mpeP-p-3_bBk0BUjP472nk8a65ttJZ8yRGzsOILf1lnnNhixqdlyoZh33Gm5JMq2anvq3oO6RhdU-oSqLY9n2Hn5ogWlPuF0G0zILcvkXGee2Sozy_5QVKZvCgzEAPZS6HAkjnnUrO_4nx5LcjefiiDBPZ34XgWgZq6DiFZAo0tJKqItwFlQSZV2IMBc7KJlLcMZRKvXJKwZ58FcmCCojesO6gu6oOqrbCPpKpCDOJV2bqZdxEqxl5QeVEb54uZ_YU1ncrvy2rQpbZLZJeUKnRd6zGdSkChGjKklVbY0YuDQwmS2xTzfhMKa6C0vpOCEZeHwfojkaAG7KF9yiBfZQ1WTs1t6oewNbd4nJzXO6tcpVDWKRyUm6a8KgYSKGQeng_CUQGOi8Ag2JO7wedbcahrdR1AE9NW8wT3Ua6ju521EpkKCoLgXACEOY3bkbT9Ay6r5zB0QbveMB-FTerqcEQDBbaDKRO9KuFIY_fVbogUyN-phOKKn8wvKjG4AscLqJmNKp9elThUzlF8Bp1sXqg1ZAtBY-Noyz1KPZ9S3YT7SlRWK2q6J9qEF8P71HAlIIB6_h-lfu5LqSgdzHhdKAAY15h7aREnwo3vxjqcPTTzXQI-eWQTNaZwSH6VLzTY2JAZd-f5wZwqaBhFmarVd7UEESp5jKFhdFR6aBEvSTnQZEUO4YvKFDtLrYwRb-zaiwuhIxUWSEswqwFpwclhWN1CjjmVFDtmTpn94g_v8AZRwZtfvcZqUidPLS7vAUpRSVT1Kk-NRwv_2TOzrhqU2XEjt7GZVIfHkEO-2IkynbR2ikbgJ7BRzG1KQYFMUyRh0o52fY-zQkNpPVW56A0J9GZbIARD1UMp40ePv7lkIW1i3pKo0MwD-_ZTld5Ou_gcQK-gSHRmmFAHM6t8zXd0eLpicFafGNHsdwrWtbjxKLhZEzTSzekO-zzoQFDfaXon1wMczXucRPtT7_Cf_8f6744LQ)

[//]: # (ob:6ec771b4)
<p align="center">
  <img src="assets/logo.svg" alt="Proofpress logo" width="88" height="88">
</p>

[//]: # (ob:de7999eb)
# Proofpress

[//]: # (ob:7542280e)
[![npm version](https://img.shields.io/npm/v/proofpress.svg)](https://www.npmjs.com/package/proofpress)
[![CI](https://github.com/chenmingtang830/proofpress/actions/workflows/ci.yml/badge.svg)](https://github.com/chenmingtang830/proofpress/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

[//]: # (ob:e667d986)
**Verified knowledge infrastructure for autonomous AI agents.**

[//]: # (ob:0e0e9d9a)
Proofpress lets long-horizon and multiplayer agents build on evidence-bound,
governed knowledge—not unverified memory or opaque summaries. In high-stakes
workflows, every trusted conclusion remains traceable to its source, version,
policy, and reviewer.

[//]: # (ob:92fbc10e)
Its native ledger travels with Markdown and static HTML artifacts—even when Git
does not. Its format-agnostic evidence envelope can also bind provenance to the
exact bytes of any file without pretending to understand that file's semantics.

[//]: # (ob:815b673d)
Proofpress also includes a **verified knowledge ledger** for long-horizon agent
work: it distills bounded telemetry and artifacts into candidate knowledge,
binds it to inspectable evidence, records deterministic, policy, and human
review gates, and projects only governed current context for the next human or
agent. It is not a trace backend, generic memory store, or truth oracle.

[//]: # (ob:6ef36a68)
> Git made code collaborative. Proofpress makes intelligence compound.

[//]: # (ob:df7a085e)
<p align="center">
  <img src="assets/articles/memory-table-stakes-provenance-engineering-hero.png" alt="Illustration of a provenance ledger traveling with an artifact" width="1200">
</p>

[//]: # (ob:cd8c1f66)
Think C2PA for knowledge work: a portable, inspectable record of admitted
history—not a claim of C2PA compatibility, signed authorship, or complete
capture.

[//]: # (ob:9c6c7f6a)
## Evidence

[//]: # (ob:30685e8d)
We published a bounded evaluation of Proofpress for agent handoffs. In a preregistered controlled task where a document had changed, ordinary handoff continued incorrectly in 12/12 trials; Proofpress-assisted handoff did so in 0/12. Both conditions continued correctly in all 12 unchanged-document trials. This is evidence for the version-checking mechanism on that task, not a general claim that Proofpress improves agent capability.

[//]: # (ob:cf466876)
[![Controlled agent-handoff study: ordinary handoff 12/12 incorrect continues; Proofpress 0/12](assets/articles/agent-handoff-study-card-2026-08.png)](studies/agent-handoff-artifact-provenance/README.md)

[//]: # (ob:aea6ced7)
Read the [open study package](studies/agent-handoff-artifact-provenance/README.md) for the technical report, evidence, methods, limitations, and checksums.

[//]: # (ob:6a39b2e1)
## Why admitted history matters

[//]: # (ob:6c80c41a)
Agent-native work is not a linear document followed from start to finish. It
is a graph of hypotheses, source material, decisions, revisions, handoffs, and
evidence. Different tools can generate different views of that graph—a brief,
a research artifact, a design review, or an executable task—but the work only
compounds when collaborators can tell which changes became dependable shared
knowledge.

[//]: # (ob:6dfb284f)
Proofpress operates at that boundary. It does not attempt to orchestrate every
agent or capture every thought. It records meaningful, accepted transitions in
the artifacts that survive the workflow, so a later person or agent can inspect
and verify the history without needing the original session, workspace, or
orchestrator.

[//]: # (ob:cc376e2b)
## Install

[//]: # (ob:d6f9f208)
Requires Python 3.11+, Git, and Node 22+:

[//]: # (ob:7b197ac1)
```sh
npm install --save-dev proofpress
npx --no-install proofpress --version
npx --no-install proofpress setup --agent codex
```

[//]: # (ob:5ae48e1b)
`setup` installs the agent adapter and writes `.proofpress/manifest.json`. Use
`--agent claude`, `cursor`, or `all` for another supported harness.

[//]: # (ob:4ccd51b9)
## Verified knowledge ledger quickstart

[//]: # (ob:460f8108)
Bring a bounded OpenTelemetry-style JSON export. The sample below creates
candidate claims from the included fixture, checks them against the current
policy, records a human review, and exposes only admitted knowledge to a fresh
agent:

[//]: # (ob:8b9b3369)
```sh
npx --no-install proofpress knowledge ingest \
  node_modules/proofpress/examples/verified-knowledge-ledger/demo.otlp.json \
  -o /tmp/proofpress-ledger.json \
  --scope demo --proposer agent:experiment-runner

npx --no-install proofpress knowledge policy-review /tmp/proofpress-ledger.json \
  --claim CLAIM_ID
npx --no-install proofpress knowledge review /tmp/proofpress-ledger.json \
  --claim CLAIM_ID --decision accept --reviewer human:reviewer
npx --no-install proofpress knowledge context /tmp/proofpress-ledger.json --scope demo
npx --no-install proofpress knowledge verify /tmp/proofpress-ledger.json
```

[//]: # (ob:20fbea6e)
`context` excludes rejected, unresolved, expired, and superseded candidates by
default. `view` emits a stable graph read model, and `materialize` writes a
portable Markdown projection. See the repository's
[`examples/verified-knowledge-ledger/README.txt`](examples/verified-knowledge-ledger/README.txt)
for the complete local walkthrough.

[//]: # (ob:8fb4a17c)
## Choose your path

[//]: # (ob:eac911f1)
| If you need to… | Start here |
|---|---|
| Verify a document or portable handoff | [Artifact provenance quickstart](#try-proofpress-in-two-minutes) |
| Turn bounded agent telemetry into governed context | [Verified knowledge ledger quickstart](#verified-knowledge-ledger-quickstart) |
| Understand the ledger's scope and integration boundary | [Verified Knowledge Ledger overview](docs/VERIFIED_KNOWLEDGE_LEDGER.md) |
| Implement a portable artifact carrier | [Portable Artifact V1 contract](docs/PORTABLE_ARTIFACT_SPEC.md) |

[//]: # (ob:32f0ea79)
## Current focus

[//]: # (ob:4902cb38)
Proofpress is validating the developer wedge for trusted continuation:
**bounded telemetry or artifacts → evidence-bound candidate knowledge →
verification and review → governed current context for the next human or
agent.**

[//]: # (ob:99c9f31b)
The next proof point is a real design-partner workflow with a measurable
handoff or fresh-session decision. The published agent-handoff study establishes
a bounded stale-reuse mechanism; it does not establish general long-horizon
agent efficacy. We keep the portable artifact protocol and the knowledge ledger
compatible, but do not yet promise a hosted service, real-time trace backend,
or general-purpose memory system.

[//]: # (ob:2f4c353f)
## Try Proofpress in two minutes

[//]: # (ob:d61fe659)
Start with a real Markdown artifact that already carries two admitted versions.
`inspect` reads its portable capsule before any local Proofpress ledger exists;
`import` reconstructs that ledger from the file alone. The demo uses a
repository-local Git identity, so it also works on a clean machine:

[//]: # (ob:9a25e119)
```sh
mkdir proofpress-quickstart && cd proofpress-quickstart
git init
git config user.name "Proofpress Quickstart"
git config user.email "quickstart@example.invalid"
npm init -y
npm install --save-dev proofpress
curl -LO https://raw.githubusercontent.com/chenmingtang830/proofpress/main/examples/portable-handoff/strategy.md

npx --no-install proofpress inspect strategy.md
npx --no-install proofpress import strategy.md
npx --no-install proofpress log strategy.md
```

[//]: # (ob:862797da)
![Proofpress inspect, import, and log output](assets/quickstart/native-history.svg)

[//]: # (ob:66c93d16)
Review the accepted change and check that its recorded claims match the actual
document diff:

[//]: # (ob:d63d3ab4)
```sh
npx --no-install proofpress diff strategy.md
npx --no-install proofpress verify strategy.md
```

[//]: # (ob:399f86cf)
![Proofpress diff and verify output](assets/quickstart/native-diff-verify.svg)

[//]: # (ob:07612948)
Static HTML carries the same native ledger. Download
[`strategy.html`](examples/portable-handoff/strategy.html) and substitute it for
`strategy.md` in the commands above.

[//]: # (ob:ec2e5323)
DOCX uses a sidecar evidence record rather than an embedded revision ledger:

[//]: # (ob:3ebf7611)
```sh
curl -LO https://raw.githubusercontent.com/chenmingtang830/proofpress/main/examples/portable-handoff/proposal.docx
curl -LO https://raw.githubusercontent.com/chenmingtang830/proofpress/main/examples/portable-handoff/proposal.provenance.json
npx --no-install proofpress provenance verify proposal.docx \
  --evidence proposal.provenance.json
```

[//]: # (ob:a528a698)
![Proofpress DOCX provenance verification output](assets/quickstart/docx-provenance.svg)

[//]: # (ob:4149c80a)
To continue the native-ledger demo, edit the visible Markdown or HTML content,
then admit the new version and inspect the updated history:

[//]: # (ob:9df616af)
```sh
npx --no-install proofpress snapshot strategy.md --kind human --author you \
  --why "accepted the revised volunteer plan"
npx --no-install proofpress log strategy.md
```

[//]: # (ob:20a32f50)
See the [complete portable handoff example](examples/portable-handoff/README.md)
for the files, expected behavior, and security boundary.

[//]: # (ob:4273537d)
## Create a portable document

[//]: # (ob:1160e434)
Run these commands on a Markdown or static HTML file:

[//]: # (ob:2b655d31)
```sh
npx --no-install proofpress policy proposal.md portable
npx --no-install proofpress anchor proposal.md
npx --no-install proofpress snapshot proposal.md --kind agent --author codex \
  --why "accepted the smaller launch scope"
npx --no-install proofpress verify proposal.md
```

[//]: # (ob:f46e6643)
Applications that need clause-, issue-, or work-item-level handoff context
can attach a host-defined admitted-decision register to the same portable
event:

[//]: # (ob:d7acbb2d)
```sh
npx --no-install proofpress snapshot proposal.md --kind agent --author codex \
  --decisions decisions.json \
  --why "accepted the revised implementation state"
```

[//]: # (ob:eb60d5b2)
The register uses `proofpress/admitted-decisions/v1` and travels inside the
portable capsule. Its target and evidence identifiers remain host-defined;
Proofpress validates the record shape and integrity, not the truth of the
decision.

[//]: # (ob:5796ae98)
The policy is sticky. Each accepted snapshot refreshes the hidden capsule in
the file. Source code stays in Git; the native Proofpress ledger manages only
Markdown and static HTML knowledge artifacts. Artifact evidence may reference
other file types without placing them in that ledger.

[//]: # (ob:d8a43a89)
## Verify documents and other artifacts

[//]: # (ob:b8c9468f)
Create a sidecar evidence record. Proofpress automatically selects the
strongest built-in adapter: semantic OOXML verification for Word documents,
format-aware byte verification for PDFs, and byte verification for other
files.

[//]: # (ob:989efad2)
```sh
npx --no-install proofpress provenance create proposal.docx \
  --output proposal.provenance.json
npx --no-install proofpress provenance verify proposal.docx \
  --evidence proposal.provenance.json
```

[//]: # (ob:227de120)
For DOCX, `semantic` verification canonicalizes the meaningful OOXML package:
document content, tables, styles, relationships, headers, footers, comments,
footnotes, and embedded media. Repacking the ZIP does not change the result,
while changing document content does. PDF evidence remains `byte` level; it
records format metadata but does not claim the document rendered correctly.
Use `--level byte` when exact DOCX package bytes are required.

[//]: # (ob:949eb6a5)
## Hand off a document

[//]: # (ob:2173502c)
Send the original file. The recipient does not need your repository, session,
or local ledger:

[//]: # (ob:af7113fa)
```sh
npx --no-install proofpress inspect proposal.md
npx --no-install proofpress import proposal.md
npx --no-install proofpress log proposal.md
```

[//]: # (ob:5e991c72)
### GitHub or a raw file

[//]: # (ob:398568bb)
| Route | What travels |
|---|---|
| GitHub | The file and capsule move through ordinary commits and pull requests |
| Outside Git | The raw file carries its own public history |

[//]: # (ob:a908fde7)
`refs/proofpress/ledger` remains the complete local working record. Portable
files do not depend on it: their capsule crosses the repository boundary with
the file. A team that also wants to share the complete ledger must run
`npx --no-install proofpress sync` explicitly; an ordinary `git push` does not
push the special ref.

[//]: # (ob:226a29fd)
## What is—and is not—recorded

[//]: # (ob:cfc1c3aa)
Proofpress records accepted versions, computed block changes, stated actor
roles, reasons, and consequential rejections. Claims are checked against the
actual document diff.

[//]: # (ob:5e0b34ed)
It does not automatically store raw prompts, transcripts, private reasoning,
tool traces, casual brainstorming, or every save. See the
[privacy boundary](docs/PRIVACY_AND_DISCLOSURE.md) for the complete rules.

[//]: # (ob:47f21d3a)
## Merge parallel copies

[//]: # (ob:55bcd98e)
Keep every original copy. First, ask Proofpress to find the common ancestor and
report only genuine block conflicts:

[//]: # (ob:8f498c01)
```sh
npx --no-install proofpress merge-plan proposal-alice.md \
  --from proposal-bob.md --json
```

[//]: # (ob:d4ed0d79)
After an agent or user resolves the visible body, record the reunion:

[//]: # (ob:74883804)
```sh
npx --no-install proofpress anchor proposal-alice.md
npx --no-install proofpress merge proposal-alice.md --from proposal-bob.md \
  --kind agent --author codex --why "resolved the parallel review copies"
npx --no-install proofpress verify proposal-alice.md
```

[//]: # (ob:1575e201)
Same-document branches become `parents`. Other source documents remain
`ingredients`; record those with `merge-lineage`.

[//]: # (ob:2a955c60)
## Go deeper

[//]: # (ob:8deed5b3)
- [Two-minute portable handoff demo](examples/portable-handoff/README.md)
- [Documentation map](docs/README.md)
- [Executable V1 contract](docs/PORTABLE_ARTIFACT_SPEC.md)
- [Artifact Provenance Protocol and adapter API](docs/ARTIFACT_PROVENANCE_PROTOCOL.md)
- [Privacy boundaries](docs/PRIVACY_AND_DISCLOSURE.md)
- [Agent adapters](skills/README.md)
- [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) ·
  [Security](SECURITY.md) · [Code of Conduct](CODE_OF_CONDUCT.md)

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzU1NmIxMTVkZTcxMWIwY2QzM2VlZDI2MCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImFiZWNhY2Q5IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8wMWRkOTQyYTY4ZGNjOWE4NmE2MmY2N2YiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2UyOWYxODUxZTBiNDhhYTFkNDIxM2ZjMiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtvUuTI8e1JvhXouuatUgqgYr3I6mW3VKxJNVcUmQXS1T3MGmVHuEemXELCOAigCqmJJrdVc--ra1XM9v-C7Ofn6LFmM2_mHP8FY4EEHhkFkhRZyEqKxPw8HA_fp7fd_wvT9hi2dSsWr5p-JPLJ_P5myRJyyBIuMiCoPQrHkVC8DD1n1w8KWf87g1vbkS3hM92tyxM0ktW-XFZVHUYBlXtB1mWlBWvw1RkZVbEgsWFn8VhgT-EWREmIvGLNGBMFLlflSWDcXnTVbN3YnH35PIv-I_lmyW7gSdM2BIfdQE_lGICv_hGLJq6YeVEeAvxrumaWevdwudnizuvvPO-Wsxm9Xwhug6-M2fVW3Yj8KXWfr2Y_auA110tcMDb5XLeXT59etMsb1fluJpNn1a3op027c2StTd55D9d-_ZC_NuqgZ_frDqxeFPN2k60sBbLxUr8cPHkVjBcRJhsxSpePFG_eSPeyQ_B4oo3fsB5EYcszXlVFSxPWRrWaVbjzGaLJb7am0nTCpi52ZHJGxEWdZAngfDLOGcs4HEYRHUVqtfRs3tTsXm3msALhzjParbg3ZPLb__yRD_-L09gl2eLDn9Sfxb8TQlL_u2TasbF90--gzcw0gAPfvXi2WdfvBhP-ZOLo4SELZeLplwtYW_elKxrOlxmtmhxivA32FAhh1wtb2cLnMzbpsVRuzv4yxT-0rIp7pqa1MWTDr4IYz25bFeTCUyxuoWNEerVysmsegufTUWVZUEZw8dhT5bie3yBj_7f__l__H__639-DL_Uj2Ccy2fPUXjEe_jNr-YemzQ37X-6elLBKonF1ZNfX7We96tmeuN1iwp-z7pOLLunk9nNbNy9u7l6At9Ywu-1sMFwy7u5FDO2YE9-uOhnBatTFIUo12a1JqM75_VP67Ksn4DSBJK59hCRphkv8vSEh_Sf8prOW94KD-S4W3oTdicWXj1beNPVZNnM1b-fvbz0WOvN5qK98NjAa_vCFwUv2Akz-v1qytoOHsM9OADtsvMqeCTIOF9VwmMen1WrKfzeg1NYvZ3cXXggaHLmXAzMqKqiLBXhKRvx-rZp33rPw6-eqWfhqrxtZ-8ngt8I7_1s8RZWxTNH98Jr2m4O6kWqqIEZpaKO4OjnJ8zo197vmqU3ZVx4eETgPxNQj7MFWzbvxNiRG_jMWwFbC8NPQMZFWw2tUZAWPE_CaG1GXy_ZcjUsqP_k2Q8NSClP66IO_fzI0Z2X8cfB2DdyWq0WCxSDTi10O5-CPZgI1sECgI2QdmHoXYsw8Otk_V1ftjDaZLLnZftPDbxtkcPLJqI6dnzndd8KMYe9gxPwZ7GYjbiAY8dhC8HI3YHibD3R3oCZUEeF827odbMyKDJWBcdO5_r6uru9anF1G_VpbzTq2DsB03nn9ZYHP_I9_Kmdjczn4I_9hFBM1yaUMBHnIiiPnhBo4tX82symw5OnrPyIvWcLWA3O5qDE5aq8XzRgbK7a67Ga6ZCiZn5Q8Pro_bru1-CfpXxe7xBQLZwe2q5WTMbe69uB6cRhFiVRxtemI12fO0fXeDAWn9U1rIZXw9H3wGlZLcUe-T10mD3nOQhSX8RR_OhTfA2L9-3G97mYzr77SHzPpvOJ6J6av4_0359-7OEsBpY0LNMk4VHw-POd4fGDMdAblRZguQATBhPA7Udf1jhDoI4Xb70lfB7EYT7rmqH58rgIUrBajz5fe6Y3D6xRPfKQwV-lBZY2Bj9bMn4zdKSzIkWX_oMIBD5beB27w8PFlr3vD7MG55aBZfPAIe8c4_cp6M4hnQjRSVyDe7ZukEDMQarqBmbaHGQOtn9jyBDmFatLHj3kuet-G_M6-XVjGOQo7yGe8doZLFez4CN4--Wdt1i1y2bIbyuTEsXuIVPT4gXhlFdNZmCfjgmwBsQrSNOaJ0X8kLnBUQUhQbkA6WPtDPT0whxFCCAvPBAlDu6do9XH87trDwRu6KgWMbj4KUvWpvYnFNO__fv_aQT_b__-f3lTAYphjzwNfW9AqsIALIYfVg-fw-vVotXHtZk0IDUgUTM4X5dD7nUcQwh7z5k96elafOZSkiNvbSNgVpMG_B_4JWwZm0BkavUKWPnr6wHxyYoY1GkcP8L6gDoCBbmEHcDD1y0hDrkbe58z6XZUlQD_g1sF1cFPNcz_Fk5pNRtYQlZDIB3V7AMvoY5O3DVc_-iQhhdFEVRZuDbF1-9n2uDBHL0FayZ7JPyfvO1fGRDuqMiTNC_LhzwYnLkGYiWInH6_Ki-ki_YFmGM-e98-_f3rLz5XWhPdxkYGnTKTgg94JyZD21b4eQ1h_kOm9uVquTG32aIB755N4Nvv1dRsgK7HHXsvl4NOf1lXRRRU7CFTQ2E3awET4KKaMBVnepwt2QVYmKUK1KX-XawqdHQ6nNvQ1PKoqKucBQ-Z2lfGo6jYYtFAyAczqCYrjlmCdtaOFhguLfCU2uSidMDglL4fzBT4RVLyeCNObSpPyol-3AEh8eY3BrM4cRrViXjIcx23gE26mdet5riWqKTkONfj2-V0ci2lXP4MP-q8XjckSDkrK4iOHjK1Q_T6hK3a6nY0n7BWTtQq9wGd5PtgdvLQf8jcXt82xo-SXxy5X_S--OYrLeZevWBTgRkfOJ7e8y--BokbijjClIVFzTc1-o1Yol1QGdhD_IH7XxiQo6qugipi7AFPdcRIZ5F7u2bkBVwlmWTppLpqFmDcpnPlyO9aj0T4ZRSLh6wHaBU-Ay9fbsdqOZvidoHTd-dhBUBIZQmiNZ0vOx2GVYtG_WPI9vI8yrPSv58dbN4xkMopiNw-p-3-Zwf2J-F1ELGqPu1ZL1h12-_BLes8dLHV-Rly0KIyCUVURqc9dQQesT6K15devVquMNNiRMJIgvV00EyJaSlwHMcKTCAUXnfpw7TIchaeNikPnjcFtc7HQxFNXvgiCOKT37u5aUGweP_aYA3l_6Pr97aZz9eev_GKVZrGYRBkpz3_awjiqls0YTUIdR9DL2cejA_OQcVaPApwdDCCr2bzRqDqX2AVaiD5mRdFwpITheG3oPsYit0Iw3hdexvBzmMieg5BFIRYQ6JYh7mfBOLEAzBoR6qJUMUCGx6MRrPVEvSS-uWAHSnhQOUhW49gnqNOQX1fT2bv96iA-58dUAGZn_JKsOi0Zw2uAAMDCvuz07uvB5YgioSfsFOX4I8QWF-PwOvC2iocGJAQUMtYLJE10n9bgY_YgMhyWBCvXOBEhU7m1ENGo8jSogrWPcUvxOIGVIuukkp3BrNseBj1IdizWQcNMLCDcVaHAY_uFbhg7pOJsOdwVktN2IHPYMtW-0KjA8cYsi9YfC9y8ahTs742RiIQBsw8pXZkKVxWo0AlTXFRx96_CDH3hHS3ZRAzFAbUcZFXfvCocx08H3KO0sO0Z2TEwHgKVBZXV1du0WjjgHBwXnyeFY86XRlhzaZTlMEWlw2WVRUuVFVTDzH2nrU60MKCKHyjHHQ-szgHp8aPz7e091SPXVb7-aHkXpIlInxkQXgGJrFpQfl33hSL2qXoLeiWIa8diMP1ULYvYDkX5ePO9U-3opWunK1vS0nFVDyIBKjN3icfgagw1F7dbLWoRHcxZOl9vwKVnp37gBnF6ppiebrAIA-JQRxXEU_9x19aJn0T8JpADjC_MxVLhgkMqfpNguOjOetkjNN5oCGadjDpG4IQVHFSn29pG44mtIZwWU5zhG8kz9dw5rPMwKpXUf64EzWTwWRC915mX-Rvlnfe3_79f3hXT5Y6qJYW3hytqyfyr7N2ED4SsiJJqnti8PVqASPstezOxwaMJOyd4Mm9cOiQJ4zu1wYuN6rzTln--ecvx1ftSKIT5qwaCoVYmafhvajwkAl50jnDEMH4VJ86Wk4JNoQEYKVxf-erErSyNxcLrJkMKbnQz4K6zE5ZIAiLJpPuKSzN8wnDfNxzEMkL-d_v4f9Wi262uJDr81XjKRAYzt_Njm-uT53xKAhPWZ9SdMuRqGtMKtYg9CWr3nq3s9nbbihwTOHQpFnOT1iAFyb0vb8PlyAEy9sRfFNLy9JWQ2cyBTywAHno11HByqPn8_USDp-qBqIEfGtON5MVaZzL9999BL_snlq438eIToAQ_vv76_PdhYESPtFB_5sKYk0F55N_MfBA8SYvMp-lIkk4j3JeFmXMijCV0QX4jnJMszzGWoD0Vm_ns0aqHlU_V5g_8y-E_H2HMElMdzgjuNBJZxAJyjwRVdnN6uWbGuRSLOaLRoM3uzK4rHhWV3GW8ixI6lRkYVokcZVXgZ-GgmURF36VC_hjUuNHy5LxOitYHAec-ZUs0GGWUYIw1W5dpsUPsNCIkgz9MB352ShMX_vZZRxdhukvff_SR1WoVxyTGgXncSBiEJD-t395DOSmlDYFrLxl3S1GOnWQsjTOk0pG7HIMB2upBfHhIEpMNuLf4PfvG768hb_kOfzjVjQ3t0v9LxjzV0_nv95ybPVs8yRL6ygP0sKPzGwdDKae7X5opR6OFyn6_FleSpyLHM5BW26A9o4HUaJDP2pVQUUCChdXrbSYqvDU9QfXbON499sHGWhJn9V-XQozXQeKqaf7EIRlpWuacordLYN4-apFf6qWtSp416m0NatupbKyFeJ9F-hTVYsZLFAlv6jwvN2F9_UElPEFeGMCy6mdtApXbTebCgSa_wL9tOlscTeWISYsrvi-EuC2wOTeo1eHk5LpeJXyAv8O1hHrQPj5T70peHtXbY_VtLUOHcCuQSUV3I7hW8F8L5Qy0tAtTEyDi3TV2pynhiBfyIqBLPeyTr7RerJDZUPUu-KCq1T5Qkyk9oWtnq3tLbqmYlKDi9TN1BobaDtukRKJXiLwzQekAcSesxS0Ui5Bl1IaHBisKbo9AN1qFwanc9WauTI-bZa4KA2-H0zciq5nKy0Iv2Bw3u9MaaUCh3uKQ-FUrlqsJsAaKQQCrDLoFhQi6Sx0t838wpupksNELG1OdmAxkrqoyqxO01iwXo1ZBK5ejIcAaz04NauJ-uTApqR-EIqchUVVmHk4uFujoIYhtXosxnJw0sIsYLV9Jwdlu6mdjgbQ-uNw7EMgP79l4wDCEuVUdGv6zFpxoze6Szk--L5SanGf7_4MrudGxHHVYsBrivC4oZ1TtzNCc-Hh5MUCFGQ5A8lXUtYIfaK0DMqD5ZxP-MpsokB3DE-1nPFIY_KkpwLb2SgNogGkpo6hVMvdbHXVtgKFDpTb90qaxc1CuU2dcrwGNjqvOc-rHOxskdmN7kHH_UYPwon1YH6aBDm4USLk1gg7COPNnT4aO8wQJ9ZKKVBVWDRE88mqc-BRGhaok1VjM1QkR8GDg5pf5wT55e6lqXhcF34ZZayyZsoBKOu3eRj02CzEaKR39WjA466w2iiUNIwKXjLQsla7OqBm8xIPgSvjzJ7CUjc1RDDjfwX7ci1xFY2Mtadz8KJhsjJ3ber813Lq1xfwgwy9ri9guEpGXNdSZV7DLGAUm881OnshpgwmCW7JEtYHA8RDHI68qv2wiKQDaTVQj6Q2i_AAjDQ6HXMsby3R07j2xzDANWZnKnE7m3CYZoPVYHAd0VPXXkrN4LSbNR8yCrwuSsQPgKNupu8gr_sz-kDItHHPgjyKeBKKNKusSuhR1NYgnw5_VlsI57oVK_AWJtKOTlfgod3JnHcr0TDGv5OOBEKR2eSir9e-C7y__bf_7r0LtT8KIifTZ1hau2rxmLuASXOWnD2-vlC5Nln_ue5gHqA3MVF1LaECLaJQYSu1I4Gy2kzxfa6VQr9-Jxf7Wu0-bH0D5gJmi7oYtlo0ErQpk1Uy_3nVOhqqnS3W0VPa1RwQgjIBnyBndRBXVoYdrLjZlQeAvHFiKiAbUooJi1kds6zMrVJ0IOD3leIp2G3h2bBwj3IrBBicOOTcT-2aOPBuR1JPxWU3GsMBkuDgxqT3qYMSWEF0CyYzxlFxie9FBSfMw7gcNefYGE600EqJdvgkeLP7qwOC1Sk_1JZPEAUM_ye-h43DM6Gq6frzysTDbsLxUfX1rsGYA8uZYlnduk7DgGAxsP5RyJOsCu0iOphzx9U7FEGuB67rMC1Knos8sabHAZVvjUqPg4hPpdpVLgN4WgNiG6Z1lVdZDDrfqlAHRb4utqdhwrsxfAq2gq8Z_e0p8tHoVkzme6Q7KsK8rHyeVGnQ--AWXd6f-JOx4uokmI_-AqYLn1Gm2pxYlKEp0-gO4wVIlMe3NoH63Uf6p48HxIyneSSKKGDgi1jfsAek92J2JLDcLBb4OKAI6qzk1mg5WHOzWEdgxk1iKaqKskKNEth5OzDydcl5NDi40bY-BH88qvMot4kdByHuKLhTkd4QvmLsctuAUW1RkWgMrUIhS-dH4wvxKI69r4VKD_SmSx5RaUf6MHS2UBkSlUfo9ZlBdUsJk9ZUOv863W-cPDzvM4jxceqd1LAQ5Sx6o36xlp6R_qKbnZPuAL6kMc21dRuXqogto_GrVmrTp2pUjM4-xbqbXEQHvte079ik4bCWrl-FL60SEXKQEToRTmZBBnzmXI0mAvMhk9nsLVg8XeIA3d6yd6yZ4HADxybjkZ8kUVyVvYlzIPiHiN9eKL3zUbUnB3xyMrtZ_9igHIP3CpFhHaRZ0EchPUrfHv4jMPfGBYiyKouCKKn7c-_A8HuG5Mmgevj0Yra6uQUxg4ezxZ3yVhtEa5palnIJ56vJRAaWEAd1Y-8aJK9z7MNTJZnXVhrZVdsJ3PBlL5VGfNdFSNU_PoVABARsOkKRlib-aXfXVnjmwQTUK_CjUSIdyAvHw2PlV_oDrgQPyF3KoqAWoq78wiZtHA6BXteHMALMKtuAQCbntCqwWE10p-E10OHSciyPvJO7xO9DVMPUH6TaUenqm1WDX8VKPx5qFUZoA6k8f6eYrGsuQykxwbOI87zgYWJWxKEuOLr4VCICrhMETmIxAlWNZberVjqaVSX_haA0CDmMfcYMLugbHMkgcZRG-ibotZdKV6q0JKyLzUt6CgGzFNqfRYP-HiJVAccZDT7sQTNTWRWMYSWyZ0BJVamAeDGJs9iWMxzqhPH0HkCEgL0DFXNwU5Vrk8X2dBMV74-vPlfmQG8OOjtgkWYt4rKdB85K-XHs7NG5PtM_qw4v1w6-acruwDOXCAy0dLB7TjCBz4eAVyzWvHW1QRLlMytR6vHgauRhi8gf2G84BCagwLWwMYV0wNo7zH_dDIlpVCdhzgsQzN5f6bki65nbg5gfxp0HnRrldZSzKOiLTJYMsunOH03tAJWpwFnXOsckNaSSmWs8PaN-P0aNhG4u7RMwJaBiXk9VB72P9EvAscBFulmw-W13AWa_keAaMcXzgh_1_m01k6cHRsbSEJNVATUK6DQlswIcXKXm6-bGAKzx6H48vmpRsCxUR8usrfFc_won8uvrT10HwtERSvrtJoOcs_kcDqCUmKfvWu7k2X4p02tSlei5K5mBhzzFUtSvr4fySJXIEW0HNtOKhsOZOcKV3cmA2QO6u_-9XR_vWlie29ly80GjESII9AkcjZRG0-kDg9x6f3vnXT2R5RFZtXI9YPHeg6M-F_LkgpJbXj3ZNQmV4Nky5-GcRAWBc8ICXgXWZXfIP30562Qqj03vu5UeVBpa598J6cFNGwgLwXNp-Qghw6Y8obIGxqd5JeDgPf1mBYdm1Uw4SDhOBE4da5tl82dQ0hee4OiDdBdmBvNmLtBcYoZEWtA7BUp2_DZl6nDx0QGAueGUuZC-PBaVtSe1XkGRkCsHsIUBA8Qy0qeqZjctTMfDCFt63KbeK8OHXu32hm82xaxPNVR5DPKUV4yxwI_7mLEnQ90LSQ_gNhlziJnSnEPgHpdWBfd0p01NeTR7SWsnW969ao04e7J1Fuz7RKgv6ZKv9KBk-CO_ojTZtiIw-gkcXEfll_T16x4Apc4eqt1Jo9C_U2VaYfogbtKPkVVp6XLcoG-31AdxuYLn2JfjTV0PbI-fVX4mEs6CRPRBg-VmGdf-AVSr2QR_g9hUEDaEAoADvZDzBSsArypFXkHEsaIDtn8dmaVes5NFJZBWLt1sBVnQJQPQLWx529nCv60564q68vYvtCeEqwtjjTSZx7WML-UTZG1TFRnxGKEr-x6POZz1rmc46ZOhDhJukSrXq0w3w8qN01Xt-tO1cPdmhQIJriCY4JmOGSSQC_YVFgNU69j7veqR5qmsj_SjlLE3nCPQauCpw7OrPnUpIwFtrGyOE1ULTu9CVgKl8YOwWLdlgxe6RQyI9nptqCSdVSlPOMYvOusLDslSmCcZiyFuDqo-F2nZdP1RP4AhZ1KKRYnxbBLGgW_FsyfN6SGPJcIZUx1E4FvVSZb7NthwuHF68Ifw3bQDInGf11KlwhD2K2CVMOhUMmrTJEpaP12rifWOzBZUoEkxlxnz_ZQlcW2TGA6pTr_NIFHOhKVxkfKQMawpW-vac-f6dTmRD2cmzOOShWHlV5U14g5FzsAaH0B7wyo1FvdfiRGYLoh5UfbtCB2CITtTzur5P8u1pUeHT9YM5ii0SzFC3wAs_EQZATQLFu9jlLuEdqJRR2yB9_Iz7dPOlFoaqV9LNW7pMzCFISvKRBBWSV4XSdiXC3vmnl6rU9l4Zt8DMKhJVSEWxjzEIegd4rruI90hF0R-Zn86K6qiKI6ipMyrqE8FWGJer00OINsZBZUEceInMGzvizj8u0NecC-nbtO9Xl-N_Z61Rt_xEUTbpmRnbEn_O_Npp7_mSPbX9O5317QfRagt-OyY1VjMMYNs3fWrJ_BnmcbovKfL6fyp-lniDO55_DLJJNgUzPKsU6arm2LpzQQeyvXf6_EfntfkWZ6GfhGzrC9qOPREvWsPoRxq5eVk1sHgwt6tJlwn-uaCgR75WhaZFRwMlXePLlwvsOFTLZRJoRidPMAWDOLAya-Dsgz9zI_8Hlbh8CD7Y3AqjdH403AOYjR-Pre5SIfZ6GSPT6clGj1TRkERl2WWhNZ1d5iK9zNZJ9AMW5mynKsiAeveXrXOBsHX6sbiLzHNDEJuLCwGOJ0urcjcMARaMgxQBQZMS7c1-BXLoUJoXtRBnJVJzrjdM4feeIie2c9NhBOpLKL5czkrlYrBU7vnTNWZKMvcL8O6h0A6jEY3z3oiHVF4DrUBlk0FUWZD5PdlWk75yyWWomCEFX6xE_BEPC52reEJ9VIhPdDcdrPJOwzPwDRLAJRyocCcQ_ioq0bWhUffVynt7h5GEEdataA3B3YSDl2d-UmCjpS1GD2b8gSLsUmF3LbzWzZ9x3YbWdhtV4zmtuumIAv6EOt8jTrLB2tt5y2G5ayIfD-BmLwMU-u39PxOvX4PIWeqopDNjJkSA8bKcLpR-3QwnsxUXGviyLUZTS21RoBusC4hTEKwCgbQQiF7DKgVYaSGcCmBAddrTEcF8YMnoxM_QxgKvKZYSAiS-pauToEH3d6AA93IWalslJ7jgEWAkCjgfiRqB6nm8FBtL5XTSaRrh2Q1BzOCBh8iHFwHnD4mkQzF70Iuch8W436opvAXWmnILeS2cjtw3OowiqI040nuIKJ72urhinOIcyqPEaoHtqhuR8w5W_aX5X7JzqI8DwRLRZX0kt1TVt1dOJFvCiPgTthk-UWfMeQfXziZjR1JPKzWMPB3QPSmTYsZgspkGa5ah800FBGEAcSBUR7noS1HOFzXgwrjxxFVTdYw8UWdxCV4I9ZFcLir5sEPJp56U4bBpfAQQCrDw35ZZT7I5mwWQqW6TClMqfR3JnkDb_qedVrg2UTyXGDDpLnTf8bS6HuZlb0xOUWZaG7Rd5fJNPswCQYaD1KbSpFWae1zK3wOUdapPw0yYPvyvvCLPOV-bRfbIcU6eZCT2a4Ij7tUsHLJ_UHPZikZQgZhrgquPZT5PtRc5VB2VPsvndK-SaSMMIOIDrHO_q2ltnZnJUSWVkkU-uAc9YCwnpBr0yinM21tvXQ4mxZXaeEHVeEXPZzDYeL2u3IyxbbFvCym9iergbxSGaVBWfOQB3GfV-oZuHZBjqPWWnBp5IcFC4o86ak4PdvWvuTpNFoZKgxkoYK88Ms6C-sy6H31nl_bN5E7mTiLJUc55VLcsncNgiywkiRABaMTe6dGtOHOM5PH_Cawe6TH_urLV6-f_ebzF2-evXr98rfPnr9-8_VXL57js0DVyMmhecE6O9gaDGknzVTmfiEc-NYkXX-D1SqGpBkZp248tzMPe_Xym2fP_-ubZ3_47M1nL79-_vmXX__xlXqxDSrwD7igWy4WwdTz_WtF5CUlMsFx__fbryFRt6zITIb-w6sG1OeC_9g3lEhn-7QLSg66_2A641hZ4A_uVO8M1K7gIOHefPvtE0m_gN9JYteT777b5HerLNCumW8ZXXG5_zjnMrekCmOKxtHJl3PKCsgj8zSJzBRqNAxBTmiNV2bIaLte_qCpmDOLjm7Pc7tP-FrOvDWKCkxlrBbDLPBfnkA8hcuEWl1n_LeS4FR4YVYAvQN43juXToek7YNJ9OBZFmVZZCxJWVxkUVrFUVyHhX1blx3vMsNdxvxf_p7l8fCuApZVb591Gf6wnTa_r4fA4zQKiMC5yoOiYCyvwXTykNUsiCsmMOleh0lR1yEP_ZilMcuTqszKUoDVTWoRpqV0vne80v1WAUFwGWeXfr6lVUCYg8zATKhVALUKoFYB1CqAWgX8Y7YKyNKyjnlYlll0YKuA8LBWAS-XikDu6C2n3n50TwDvXkuA9TLaCT0BLGxDFxEe2BPAUy0BMJlGPQGoJwD1BNjCCI3jKEmzss78Q3sChNQTgHoCUE8A6glAPQGoJwD1BKCeANQTgHoCUE8A6glAPQGoJwD1BKCeANQTgHoCUE8A6glAPQGoJwD1BKCeANQTgHoCUE8A6glAPQGoJwD1BKCeANQTgHoCUE8A6glAPQGoJwD1BKCeANQTgHoCUE8A6glAPQGoJwD1BKCeAD_RngAOQbTnTq8RTg_nYTvszQeP5XD_DuN0bzEqgzzzA8bamJTDpHnYQA6dox_ouaTgu6gBJ4dx1As79I2HDr8xdYeE8NCxratl17cH8z_6vB3wcT_27zVuxyESH7vWDur45HE3Ba0HS_aDKtSdJzPrBmx37GwdrOTpA6tmBe6wDlTw9GE3Ra0vzvejyuJ804HbLN006aXCP5xK_VEL4hTqH-UZW7bSlrA_zAOc1Gj_gC9U6mY9P3rs2jiZ0AeMvNmuo8_uPeawTjLnMYd1ghlHtGcQzYKbtzh2SZ1g5sjRrLdohnII4f1Q_Qi6uIo9RVRi7YGM8aGV7ynhh85kD2fcjtxTk48YeZC7bO1BT1Q-dOiHMJmPbV8zPJOHcFcHT6Zl9h08k4dQ_wZcAYeSdoxMHcpZs2_cE9ROkIKjGWxDznNPTzty7U_jrw2svcM6O3QqD6GlDUUBPfPqyEV5NGqWmYrDwzp4UR5A1BpYFIeFcMxMTqUpDMzEAf0ffHoewAoYDBct5P1IE3QQJr6Pli0A_gR1cTRCfkgIeiD3Y56MnUjvgZPhwJ0Pl8fT8dBD9quH-B0hBQdgAK1H3AP-Dn3AsYhAG6n18L9DH_UQfOCAo-lA9w6dySC2z8pND-Q74g1PRPpZRdHD-g596ENwf0Necw-aO3Qmp6LqzCMdCN2jKI19GLsBpeHg5444qgcA7Ky97tF0j_Kue-F2Ay_rYMQOnctDQGRD2Yger3XEsp8K6LKxVo8JOPSpDwENDB26voT_KFKxv8Y_5Gf3RfqjluXEKv5QkqOvpD_KshxZardKoa-rHzyNBxfeh6Slr7YebvlOL8cOZa_7cusRtvLkeuyQN9AXXA9fk-MqsjbD1ZdfD3_p0-uzAy_tlGEP9hoeUKd9clBTbKd0t7MT9SuhornVQqPtJNhLUuVBCLH-avIkF2Y1lEAoQBrTceCuMt9Zn-uUBM_63EOaj3-I5zrVxrM-1ylOnvW5TtXyrM91Kprn3d--2nnW5zqV0POuc18pPe8698XUsz7XqbWe9blOMfa8-9uXa89rF_oS7pnlylZ2z6uf-4Lved-3Lwef1_729eLz2qO-oHzec9RXnM_6XKc2fdbnOoXsDX_6Q25vX7U-62P7kvY5H-uUu8_52M3bcs7z2L6Qfc7HOkXrs75tX8Q-52OdivV5z62tTp_zsU4p-pyPdcrO53ysU2M-52OdgvJZ97avHp9VXfTV5LPubV86Pqu66MvE51WOtiZ8zsc6leJzPtapGp9VJ_cl4rOKVF9BPqu66GvIZ13kvmB8zsc6RePzWiBbID6rve3Lxmc9t32F-Kxaqi8HnzUY6evBZz1AffH3rI_ty7znfKxT0z3rue1ruGdd5L5Ue1ZJ7uuyZ33bvgh7zsc6BdmzRgV99fWDP3bblbtIhlC9zuu6qSTqZq2Yq749qptFp7p1C9YhjhG7FVesPeq63SJktV_ldQAbXGVRVbFKFLzyd123a29X3X_dLlE9iepJVE-iehLVk6ieRPUkqidRPYnqSVRPonoS1ZOonkT1JKonUT2J6klUT6J6EtWTqJ5E9SSqJ1E9iepJVM_zUz3vVQRBbRRlWWQsSVlcZBFEplFch5guQY9adre1OcTLMLqwc7yM_R8uTMnRrRXiU5Rbis_o3X7z4xut5cwkJm9EWNRBDg6FX8Y5YwEHzyqqK3QUu1m9fOM0cZff6MrgMg-LIC5EXqZlHRd-Ekchz-oyTDJf5BmLglQUReRXRRpkLIjygGc8Z1kZllmS1YV_6AviJ56EfpiO_GwUpq-D4DLJLoP4l75_6eMo_QpkCfejuoieuOvyl8do3auuj5X1VtM1uw5SlsZ5UkkvTDWUFlWWBaVzYcev5uA-gqP7n66eVALv87p68mu0Jr9qpjdet6jg96zrxLJ7OpndzMbduxvQZ2yyhN874Sb-DX7_vuHLW_hLnsM_bkVzc7vU_4Ixf_V0_uvBPu5pDXuQFr694wresygK4d6Y563VeAduy8tCljBRl4L5_e3Btv68eSfmjbw-172qyHNvKmLq7kV5yE3fe6nl1aXtnb4y2lxBCgofT5G6zvJ3zoWHAw3AIxbVoV-UYAlsu3WnzO1c7gTjyYHnYjbX98jLhIq-mlBsXkJk76c2IRp23a50Lui9vN2pv91R38jRVdjyWd4LKRvVY2IX77GcCrFU1xwr_MIU1mKoQX_NeV7lILZF1l8QbSvufYP-wVS6vVfR9_PSD-MgtZ3gnZK7HuyVuhmpM4nS6AL3QM33D1iMCPJfDlz1UPEYTn8ZZayyt2xlZQAasNq8swi7-ptE9GiE13aOuHjn-CjDCevRSKuBo_Pa-64KC-MkBQ2Rs9reXOhgCsxLyIGvzRt0_T2XHrh586W-jEDfdHTt3Az9FDzhpgZbK29Gux57f8TbXa7tFKUTcH3hXVfS9F_Lu02v4RnXMrIwedv-Nm3dZ3xAknjCs1hEIuUitPdy9egG5xq8oTL-buFiYQGRg19UIeuvXOnhDUa4VvKOpc7eB9Wp6zOs6oC3czUHqoMhYQsFuB2Mh2VoH-rgHo64JHt7pvlHu7tP3bRkU0JnuB0vzeM4ykKR5Lk1eA7Mw7nJS6-YkyhXqTMzWfvSOn-lb_m6bcDb6y9Iw7sEjMI_8EY8FT52KsLeYmyu2hPuxfPzqIxLkaRxZI-6A0Hpz8V2qMjuA5EU4GWAi5uyzKpuB4NiLoQQ2rbY--bUgryWl0FXzbxRN0bpC11acFm8O1istZqNvirg4qrFa9tlqkvdVjJwdCA48JMkiqsytfdVsBpco6hmh17J0-LNwctDDkIzlTfgHfBJcIaOudMxSkDtZHVYs6C_dtpicpzbBneAXHbvX5Rm4LdnoC_7e3AdVI4e-q_eKwhKhPdXde-4cWj-etX-dTQayf_Bj-bpf5X7KkuPbgpgqu7_Ube82_vWUUOqW-dAJa3kpUzy_go1uvdlfy2JHte8ls7Pq7I3HhEdvRrX66_bEEJGLJI8BNMXRiKzGtUBDRmx2HF_jvZ-dIV77SodG24r7MzapUhgvoW6Zlv5SuomdHtvT6luGlFZNccuyXeFL70DHxwv8x6699b3Y55kWR5XB9wePwj4GZAYsH68zDgECf5pV8n3N8jvuDteajrpVMLKXLX65nh7cfCue-JVjfC5upgVcxr6ynfPufH9qtVXvlu3d8-V71WcZnXAauEz_iGufNcXJeu3wxvewWJsXgPvDd8C_7UQ6u2-nevykRGnvffTSHlbk-QFJoWGnCxQPSzJRA5O-9Dlp94uuNOAOSk5q2MI6eC_uy873XWB6dj7LeKbL-SdmdvvMDU3mLo3l-LVllJxS5Nr7tXUIvmzuMA0jHhUV4nPk9zffYGpujWUmdtJYXHknaP6JkylsBAcIG9nkhd99zcfenQ76Ie-HTSo0hgiNQbKNtt9O-jXENOPrHKzpZj7l3qOvS9VcKVc0v6yTmXbYCruZZuf9juN11jLNOK9WzyHLmUuojjIsjDfd_-eizzcrSPqJKuyPAx5JaqhC_i-_W0DkTaoS_RcrDk1SVYuprPvPhLfM1R6YOX130f6704aFK_S-_aztXzplM03sqXyYy_6-8uOuZBMfverdc0NIrRXd8vvPXNjcfiOTrP3M7ufSaYLyH4mF5BtxdxuG4txfh7sbQUuQVCn6Qkzen3btG-95-FXz6RH0se36FJfOh7xhQnJNKQUpPBxm1HODEELXqGSudLFqluOJuxO3h67FDfor0vHXV5KeWzjyecziAQqk_HYGBDdFauueqiOCmv2tSUy6zr0OqDJVhO50SN3Wz110GX8OoXPjXft7AGPktvIwC-b3ei7XMX3czBzeA-9XEwb7VTgv7LlLlqbuUdWpoaWeCHpDd7Lu7Fk728xSkIYNAZf-GmlXuw7ywS4w4E7ivAGcXcWQvSdBEEOP9ZJKcB4yTu6txLebAnn75fwRqplt2o5nA5pa4NqTpfhhVsl_GF72e8shc-ijENWRX4cFyH8z49YkFZ1GaZ1HfkQfNVVVae-Dx57kcZpUaR5mQqR5EGMvpwae9_LbRQ9w0s_vgySLUXPiqdBHkQlFT0_cNFTVKjIWCn8oaLnJ59gpk1qak-ZPTw3YDWWzVz9-9nL8SefDFzHnEcirXlUxizZXai8x11ovdlctBcq8hq1ChCuL23fKKSupcav2rVCrEmI7y6xYl5OkWZsVsokn9RYEgl_QL7JWzYqp4c2B9XJQByU1EVVZqDCYtFf39zrWb0oD1GfjmkfLAYUccZ8CJ9SewAc7WqLIKcrTSwhQEQybZayjqx9F9gOBaOWvhl-RI6OeSeYctlMmiWm-eHQYc5O-u_dbTOXyS6TnLpqNcCWyslUTqZyMpWTqZxM5WQqJ1M5mcrJVE6mcjKVk6mcTOVkKidTOZnKyVRO_omWk7MkDkF6xQmVjG__w7eY_tEuz3cfmRYrzfRm3N02YsK7cTN7Cp95-s5xNTE9_fFjVHt2VY62F1ydF91eM3wmqXEw2wvv-UvliaHyAl9M-myrDkm-bzvpU-gQfiFPsEzbDFdCt9Rd5V5wa3hmrSl1Kip9nzyVXjX4L3h0dlQmGZ_Nl_ZDyGuV-QYQHVA4ZngwwDcry1FeLUAoMdBowTND737Oqrfmr-WqmXD91kcVJ9OKB1GaVKzMqyQQZVaKOi9Evqs4aUst-4uTP09BPby4e7_CFbgVruCH7QWss5Tv4iovecbSzPdFXBVVXUd5EomgCLIgCeI4CoqMh7nIRBb7LOdBmQt4hRxi_Cou6uyQl9tSvguK7eU73w8rwXxB5bsPXL4r45hFZVgkinuqnN7-lOrhHnL4-k-_f_9-DB_510527tK6yvk4uAvwoOcv-28c0uire6obGT81jTO6p1UzvptOnmIPNnFvEg8bUk3xc2VSLr1n8BK3YhSO_Z1rIufwVBuhkf4CfmNUTlZmcp-_fP7iD1-_-Hj3tlOZ9ccrs_IsT1Jw5hMRhR-qzGp9AyqyUpGViqxUZKUiKxVZqchKRVYqslKRlYqsVGSlIisVWanISkVWKrJSkfXvsMi6UEVWTLV-yEJrJyb1G8zDLx6_ynr0NWvtaloKXNRvv30SYdfeaBwEsDjfPglwkDB88t13P85FZE70c_KlXhuDOtbuARcUbV5M0VuHxxz2oTcVbS9QOzIywNZVLpa2Gwsw-SposQVpXezF_QCnhDUL2Zxa3rNYqR62412icsanOkJ0xqc6UnbGpzpCeM537WX0Qz91GyKhOmlom61af8ZREIQsLdICoq0srkSeB-C1FmURhDsvBLXl4v0QBNLipMXXtPjh6JctjZnTH7ajFs6D2YjrLEyjksNJiYo059xPBWNpkcHJCcPYr_0ySFmRZkkN_jKvWc0SjtTyKCnSOtz9ShtIjejSz7YjNfK6ZtyPU0JqEFKDkBqE1CCkBiE1jkFqhJi5SplfB2V2BFIDfLBf3kdrhCGhNQit8ZNAa_hhlrIc_HM_DPaiNYZEZBCzMfTFbciNQVk8A35j6PmE4iAUxyCKI82iMCogiCyycC-KY0jStmI5Br-wBdEx9HnCdRCug3AdhOsgXMfPANeRRDzjEI74SVnvxXUMWYV_CHRH7ecpxOB-7rO96I4jvFcHHbF3iX9EpMcR_i3hPY7De2SihlAK9EfRe_uE9xjAe8hPPce5SIxEe_PdR8-__MPrVy9_88fXL__wO2kc_p__Gz4izTK4rPD33z_7w-9efP6l-SOejm-_hndbNEswNV-_eP7HVy9f_9f-qxj8YJZp1mKbZ3zAZy_efPnbN_Cgz_74_DVx-x8BdeJ4rk6Fa3skcBKn3nnA7iLzhEntJXPEm9f9qpBBagiIJExCubtrK30HJHwLieymlbZ1RjAQAxdvBL64-Rb4q6az946ydCfwddzjbYIQ6XtJYy_1_WyOGwXug3k2yOoWr149-Kj6dO37oHnSWCRBWJZRnsQJxFlJvrliMjFuW5W7K4OOuRCa5m4K2baatr-Q_biCcXgBfkvJcJ253lcEz1IFTUQVFKHIMliOBIKjuAjigIdZktY1j0TpJ2GeZFHkZ3lYFwm4SHERhQXLShElYRDufqWNKmh8GYWX8bY7doOg9nmV0h27VAWlKihVQakKSlVQqoJSFZSqoFQFpSooVUGpCkpV0DNXQQVL6yyOISbMgg9bBf3KamKccwdSL2WeizkeErAfzfISx2kWdp1kjVTsrpKi4-3qmWfeUrCpcs7ZpJt57xmmrcEdxtSOuDdL5clPMahYrDCrPajx79rq2mZoJnefyvjAbN01hF-w6t3ttVPpxX8rDa_SV6gxqXBLhVsq3FLhlgq3VLilwi0Vbqlw-49euH3My3OdiP6hLNKNsXnO4ojlxdrY3yilx9o7G43_AtTS3VIMNukGrTD8zS16wsyjzKsiTqWSePA87NJgYAVBFLgl8AMmrrVmVDDMrz777YX3ZV03jk69GFiqIi9EzXj4GFM8JOu1gHCyZTLfrl5IeUTj-QAjNgwzLlSl9sFzxFgU28gvYXbogcEolc2dqrnotM41jnWtbCW42HDOBpbxw7ReOOSi9M9Eja3-XS9U99l_Zq5F_6pfdPhxOavA6VeXgePnxeKdATGs141kdm-869DuAVY02oGz8W8plu-FqiVdbD5MxVpWpFGWVcJZoYlhqe7dZeAc8e3XJrwEayP1tbwZAcKkEbtpZ5gnlELi7uu96-mdU7t96BcQWdtMgp2zOZemXjnedc62D4qbBCMgVMRa8M3TgqukvTeTzh7vOivbn_M1RrydLgrC_O-fARtdYokMTkTL4ZeYIwe3rMXVU3J6fFeHz-UtFXLnhYxRlSDKS-f1s5999dIqLbMx2-Ay4vs5fs0ReelTa4ky-dinMger3UMMzZgK5hfv1Oec1V3HsoPKMipFid5RQJooroowgQhVZFEqqiBlYRAH8caRHT6f-H5ma6S8GjlzoTUWorEfWkOmm0w3me4PZLoPh9Ldv1Akdi8UiX7Yjr86C-aMZ1GUML9ivKz8pAqqwk_rIE4SmEeaR6WfF3VaxFGe13la8DL0RZqyNCyjooDA2j_k5dbRZ8Vr379M8ks_2oI-S3I_i9OEenAQ-ozQZ2dEn5VJKpLaj1iQVIeiz2TReA6-_aBHs4mFQigZ4m3W0Wq7gGreQTi1q9Y4sLrmtAOq5u1FqmGyfjdUDae-EVhYuy5aeAdYErzHTFb3rtoSE7uODdWDie9xvaTtk9AvsIky5DHAc1jkJfjgMkKDUVbojsPUDQQdP_uLzjrnHUHoCEJHEDqC0BGE7h8aQpdDCJIFMcs4Yz8lCJ2T93N9Yo1ucUB1V-1O078NVNd7HtYET9kdzlks8F9X7f1sYm9gJ6zS-U9Ua8qsqhkNHMzUZ3UpAnDEa3twnNRFfzCPTkBYECTo4zIRYdKjQZycxP2kywmZBa-ZwnKDiVhUt7AhqK3cZRo6wFWaFiIIwqKy5VQnGXHEAd6ZUuC1PUOwSfPV0v7FfmWsgAgHjq-P0JbxnSXb_oTBk1alAavziqVRGvZIKJv0cE7aqamL9tL7-vfPRmGSKgiJzAZOBEQttyDky-p2PQ29pZGH9nkU1AyFQad10T2CD8M3lhNwfkCK5nhzMBxygetdsUmFd_0KLi0ZeLL3REhqDe15IgQJ3VPlX3OEjc7kDcWLGeYadNZYwgTBV8HBLINQedGu9b1q3feX2whvtyDsLGFnCTtL2FnCzhJ2lrCzhJ0l7CxhZwk7-_eFnRVRKIIqFH6RxT8n7OxeMIeDcdEj2oG-evXlNy_-8OwPz1_gj6-_fP7l54TJPQ8mF7Xmjw3IvV1BCN0DclctZrjaQ2_wGsDL9HpBBr1SZdic2RCw4VhAzMkPOgrTcvJTjkKlPPBddtyhtYFW3MTHcYHuZilsVfE9escWiOZmRPbAFbeMbUyKdXutPurERHnle-CKm4PC2fE--_L5f-mhgWtZG5lLFd6_rZrqLVjRxXIPTnHzAULhLO89RCL_PvutQsX1anE7UtBofk8Fj-B3mvzzetZJ7Xa_OmtvUopb9q6ZLcbHXfiUiCAqeFiFPAlATYTgjIMLJXZd-GQRLwdc-ESH_qd26A8HgW7pzBX_sB36dBbgl1_jdUqYCyoghs45S_IgFXEQJgkL4SUiGJNVSRIGzAdntU44y8IsrGoYvwyDavcrbcC90ku_uEzyLXCvDM5hWiWc4F4E9yK4F8G9CO5FcC-CexHci-BeBPciuBfBvX5kuBcP4hRvps3KuDoE7rUvntx9ROuKRXnOOcRu7HTc15rlvlfqlPmeThUiNTwHvEeLTtJa8bJPuHz55X-BfVjLiKCC-xPaXvuiF1ftWt5qg2Mrv_PVZ7_Vvtf2v8uV0sCBIa8iy6MqLdMgYPUjA9DsoYM3-_4-Bs3-8YEotO0PsXu4-zGDWkCwKPL9KmeCx7uhaL-FZcaEGhgus8PrcDN0YmctSkvzZ338p4Jh0bteTbQw6FjuEt1vnWCTORWEFUqFLD3uO40ImMhx0b-Cf6LMg0NwAfs9W8of0MpYEZotMTmmhURMS4FUMpgAb9jYeyXwwYat_r-__MqBuElHX5c3QUktYTTFcZd_we_cn6r88ljmEp3jo3AuGoY3gWBj8qmHcYYBSOi84VQs4aQsGRycLUA7ByNnoHaeRdqNr1pwJTzwJOTwnnqU7qqPSk3mO_US61gBj5TGznGCwREMjmBwBIMjGBzB4AgGRzA4gsERDI5gcASDIxgcweD-jmFwD-hL6RRGH9zc6jEbZRVhXVaBLKwPj7XZ7AjrjadWSgdmlLKoKEH1rM3oT2AUTAXNRlFT3KvFvv5ae746AC1Kq9yv4oA9ykyeuddeYSSm4wQIhqVuX_QudD2bTGbvYXhpQ2HphlaL12WYx_WjzNHx8WZgHmQXPtmDD_5jHOB12iaOCV44uISHoQydY7ATU_dK1As4YMr0L9kNLg8IDT5_861kHev-0o53HZedz9T9Eo2_oc3BL8BOz7D0jYmvuZjNddZAPrBTxeVO76bcKwahCog56L_77Qedc7aj6aG-X5PrIjy8H8bqEHgzVQte7wC4dvC69daUptYva-Ezm4OQUxnvOmvbZ_VM5jaZ16l4EAeUehyn9n5Ayg7ZF-d4bX_4ZxpuyjdHwgaizLtZsPmtEs9KOfloYgy4RKCnjQnhHqAKYn5vX5zzs30SpleohjcMBeJ9R0aMSBuF0zBVHX1ScOHE97ds1cl3mS3QbVwulL8jI0dMQeH76Lr-VszowhyRzZaqZkdGZkd60M3mKm60WEVZAS9hIXPQG6LXHNtnsgiSPC5qVnNexcxnQVBlNS934UstxG4_vpTsKdnTfzR7ejh6e7DNYfjDdljreaC8LM3gwzxKoqJK8zTFomia5kWQBTwEbz3lWZ2FPGRBFoO3HsV-WkZ-4IdFGLK8POTlNkC9-WWcX4bFFlBvWKd5GRaCQL0E6iVQL5YjyrJO_Fgkdc32gXqPcTUGIb5hiVpMJGGQ8A8P8X3WXbWbznw3B09HGxL0ml1X_kKWmbDwAAdNLNRrdRJjZFKTqoyCVYdOTBXyE0v82gXv834wHy6qRhdsnFeSqGBVOtswNWAVcDst3tfooUtw4JgBFvAL9a_3rHdJJcJghvlT8BaauWqUI8GE-EkbMMwWul7iQAFl8GX92KEqWc7DENQ2qDZbvnC8IFvROd252QOrPhb57G0HPl-1RyGfPQI-_8SBz0HByyjIWZwEvb3tnWG3fHusR2ueIEQQZuCXsCC3T-idXFMBeoCnuljqalvT3aKcX7VNH_jCyt3ezWcSCItVXlVjgImLRcNAIzmKBl1S_aPOvKvCLwi9Pidj77OmluBEfOQMDiaeF9kIDOup3P5RBtH4bCn1ciZY-PZKCA9rUDgMVZ_Alm328GLjLi5wR3UFx3Trci6SWLLuLYyDWCVDadC4SyPKnTr7_TEAuZCTRLHHUBaeqENFrMNAfKyhDHJ8iTeA97UCPCQ5fhrBGWXwHws-dwKDTXt0tHfvBP5ClV6vWlsg1KKtS7I6IyBHMimHHu120acf3KyDgb9a9amm1a0gzH8n7Aqjy4GCg6KIYuPBe3QqEaEh5Kw1xxom2N_soRC36qQY9YhYKQN8s3VkA5WSj-vAKzFd_Oz7zxZEXiDyApEXiLxA5AUiLxB5gcgLRF4g8gKRF4i8QOQFIi8QeYHIC0ReIPICkReIvEDkBSIvEHmByAsfkrywnY7w4WgHnZjUbxA0sHh8zkFelzELsmoNy_YaDKWLpGi95fuZp07APujfvu8OYP94GtQiTYrHmcvXsjIqVQyWG8Hk9_lNC8JVbjteF3RnQxoYfwi8ycJEBMEjTVLbrelb3iwc1T7q2816__E_ehXf-reBLqF5GmZFxtnjzPI_fPvVRnh-ocNu5V5jSK0SdN99pKFneppDOMq0KiIepI8zyVfKdMra0nrfPBUAoG-vNrxZmiADP4Lu_9BN7il4QUyi7x5vv4esOsYXnqr63tyt-ycDGx4VRZ2nVf0BNlxOyKnrbt9nENWnss4wBKLO0iAs4vzRDritUNizi7EvVvXXcERj7zM49pMZg8X89lqu7cAsBcLMojB6nFnKROIKUwq7r7eD-aAPBcLZSsSDSbkOTDISZQ2rGTyqWIL5nHijz7_0DH4QwtCxAimiT69ztvfxigNSyZIwZ2mRfwCpVAnae2l9kz7fFNGBpYyDuKhUdPEIk3w9k-4afFA4tbeRTv2gt3jhIftxLS7SlmnI7PA6DVJWn00N2Sqko4pUYDPUnNpnUVgn_iMdcJWk8L61mYYN71v73ZsO-MBSOj5-P0k3ZNjJ5NB-4VbWmuNIrb3QDgdn52cc_2LnZxzrvvMzjnEdmI-1bTs_4xiWnZ9x9PrOzzhadfezeqW28zOOStn5GedE717n_kDt_Iwjzrv3opem-3KzlZYlR1DI2fczE1U67h4aWklOG-kq1_PPXxoxP45ZJaKgEEkYCZ4HIiorwaua-xHfxayyPIf9zCqKGihqoKiBogaKGihqoKiBogaKGg6JGg5nvt-nrwZr_NXgh-301LOQc0VR-DnMNgvLggVRkIk44WWVBXUaJjmrRMBEXCR5EFV-wnJ4QpFWZZ4lkUhLEcQHvd0aOzfyX4fRZZJc-sEWdm6aFxE8JyB2LrFziZ1L7Fxi5xI7l9i5xM4ldi6xc4mdS-xcYuf-nNi5SVXWvBBFUvYC4BQjemk6oaBgVq3i4CrzEoL9spcxW2Mw8MgH1Al6U2WQ7WOJk5SHFAkOjCtihU1cGHZCKWrpw4JfoxgPm5RO2RWy-xQHlJn2a6lykGW4skpEf1SaqKVli0xm7SCHuMh4XQlR1rFdeqessX4kTitNgIZCVgPYyqU5VfDP0d1BR-y0NOT9cA5Bq093oznXMuyH0Zi2J-V305gO_jxWT9Y-PKgMojwWURSJICqtRnPqPXr7HlKzsbl8YcJJGbPulqgiCkTiF7UQvfvqVHesNj-9QoOO9bK61V9GHofDlkSHaEDeozqP4iJMkL7Z6wFb1jkceD5QmtkN6j58Y-tAZAnyS-B49iQyW9fZtrFH1mbgrMEXRurDe_a05Kmfgd1MytSSu5wCTq89Ty_C4KrcLqeT6yHY9donP1ZB6aqEuHKJ9fYGHXXwYa6dZb5WVHSn4wL4qO-GnMwoAvFIwjJPU4tHd8pA-l0fUsoxTv9-9mXN_BLOd1GEsQ1knGrPurSeRVWuEazP_cyfJDkcnIgwilPOIDixxMe-1rXtpB5ZrzLHFqc9ciY3fGZFGJWZiHxwruyZdcpbJo3wgBKVjEfUadcUdRnctMoTUsOBjtfukDytxnzi31ZzzpzIfohaFaZFFIY8LHuyoVMEO1xp7y5kwTRWoB96Xs_dbDXUfUSeYfT1ZpMVvDuGaBPW7uP2HGfcw7woYlGCdPG-v0tfVbPU8NMrY9sJLYYKKOm1MscKW4b0THHL3jWzhXIZOs3L6GNqar9D7Xeo_Q6136H2O9R-h9rvUPsdar9D7Xeo_Q6136H2O9R-h9rvUPsdar9D7Xeo_c7Pu_0Owq4S8EOiJCkG2--87nmS1H2Huu_c677z_EfvviPLAX33nedHdN95CC10k2iiNM020rGEoKKmc2AY-F4j_KS60xSzHhMBduT5S3SOW0ROHsM2LpOAl2Etgtgvi6DI_LiO_CRLd7GNLW9jP9v4A63S4XRpS1jZxcHpSShn4eBEQV6F4M8xXsdhUQXg0eRB7cdVjuq5LNC7iYK0qlkJ6rmM0IPIQ59VrAz8SmJnd7zSNuJNcZmkW4g3cZHUicgTIt4Q8YaIN0S8IeINEW-IeEPEGyLeEPGGiDdEvCHiDRFviHjzCMQbERR5GEKoD67POYg3-BPWUZobWUoYY17LWwuR_3P_vSebn8fM8wS-0I_-zzpBO27adxChc5VZJ3oP0XuI3kP0HqL3EL2H6D1E7yF6D9F7iN5D9B6i9xC9h-g9RO8heg_Re4jeQ_QeovcQvYfoPUTvIXoP0XuI3kP0HqL3EL2H6D10ufZP_3Lth1xNt0lcUQd2--2TmzdLOt9X_JsnL8DXBaXhoYa8xwVS8I3VQlYxe8d8pBx_DFAwe7CE7R8fTjCCcRYzEAhpmx5KL2JxEiZB6IN6iqIqyXzGstzPol30IstO2U8v-kC7dDg_ai-9qKfanIVelOYsKPy05GlaJHnsVwl4KiHnOYSUfhUEkfATnsZhDR5WWflFHoC_JVgdhkUYZEV5KL0oeC1ZRZdJsoVeVIEBjapcEL2I6EVELyJ6EdGLiF5E9CKiFxG9iOhFRC8iehHRi4hedBS9KCuiKg7BykRZ9g9HL1IIBUynaqy6qrLsTPNI1dOYoisqCIWQVDmcKfi8DXGWiLNEnCXiLBFniThLxFkizhJxloizRJwl4iwRZ4k4S8RZIs4ScZaIs0ScJeIsEWeJOEvEWSLOEnGWiLNEnCXiLBFniThLxFkiztLPiLOENYb7FxJdPFHsl83fb7_ACH8vPW37B1SaP6WLjVYSodceyH2q41SkEPGusWoGM-SGb8WV_zhXmg_tyRwdXpWuUH61jFERh9SJ0QV4n90K_x80Kvr7I0SG6yj-dovusLyfjFVlGfJHmOEx1ZuN9PUWvWymKMoUbG0ZPsIUVbR_A4IsFqr2e-2yHQxhwCJTn74LrqVyAEVzGAfN2fF7s9AEtM-sKXCx9PaRVoOusMjBOjHetV3bh3_GuS7Zm6XWlRJTQoKBMRZkFn5rF2S8a9W3PwmxAtqP2YByqULhUtyslZekiwwWbglvW8v7tuxC72DUmcXas1bwHdH2FUpFa7j38PFRTLs8RzZUmKZZUOWch1lS8SRkYhfTzhK19jPtSCf8rHXC4ZRNSw9Uc7qMfthO_TsL3TFL8pqDyQx5kkUBS6IwE1UJw4QQj2Z1XBZ-WkdhXZZ1VRRhVvogIQgmZWkB1pbteB-H65iP_OJ1UFwm8WW07Sq1LM3hjAUFcR2J60hcR-I6EteRuI7EdSSuI3EdietIXEfiOhLXkbiOxHUkriNxHYnrSFxH4joS15G4jsR1JK4jcR2J60hcR-I6_vhcRx4ndVIgSS61AadT7Tc5yAcU7fUJ0SVvzLy2uiIBgrGGrNgES9gat65cSD-n3zlZtx6QnziMgzAswPMUVmgdoMAJWu3YbbU5VAc2ghbvEMXXoCLpEYYSGI_7P7yfGS9CsJQsC-1-OsADh7t6Kn5AVl1gjRqucef3EwWqoAL29EYsFe_M2H8VuNcNmCsNKl0TgE-vWseEy4DWwnW0w9fdsvk9qM6FzI2qehNsgUotw7TM5AfTg0T0JaIvEX2J6EtEXyL6EtGXiL5E9CWiLxF9iehLRF8i-hLRl4i-RPQloi8RfX9mRN9qB9G32kH0rX4soq-GpL1B4Gf3AW45rDPm54lYI6StEXJ2EtAOpxlJ7gAesymcusXdSB21Ay9H7Ce4kzmqtbFBGq8h80HJzSDSxHSALiCoHZcHWW2U1JKIcVjARmntBotRNZ1ka3i4KjuInhhbSbOp9qT5Mz4cQ6ru1qRa9s1KIyc2ZvWpySNvp6oab673thvlP-K6HUcahWA2ibK4zLMiZGWU5VEYRUwi3DfW2Jk40wwadKb0Quo5KEH7FFxurjxljrl6tBSeFgU1hHQ-LRfVEukOuPXxJyW1h3Nw71MN12-K7JmEf6_UyeA-dTLwX_vBZRRd-sUW6mQelHUSxTlRJ4k6SdRJok4SdZKok_8o1MnAT0TCs1SUfp-k6d2ao-3Rdm8FVggm58AZRwILekKAJ3AzQmduPG97G_ZyMllJ5JyESGKFy9moNcnBbVDkk55v4pi8IPT9A8wc8UeJP0r8UeKPEn-U-KPEHyX-KPFHiT9K_FHijxJ_lPijxB8l_ijxR4k_SvxR4o8Sf5T4o8QfJf4o8UeJP0r8UeKPEn-U-KPEHyX-KPFHiT9K_FHijxJ_lPijxB8l_ijxR4k_SvxR4o9-eP7ol-BKPnvp7bov9v6f77FJN_-8Tip9rquw3mt49b_fa2SLKq2yOmVrNL0XOt4fIunBWXY-tuUomydEfpon4GAc_YQ_CcPTRL9PCbfANDObrCz83XENLK0GNMDAFZRVHadpnqVHzwcpUXgUZmAOtAUxugRcwxW_u-xDAPP7IHwahJ573-TGfBgEXSCV2dHzeQWLrQqWkuYjp2DyInCW4Z-gCJ6uzXNkZfQgYq8jHEPEXmZCTIdSsoRFmM8aiVZf9HDP9QUb7xKUHdfCrqZTpgi8OKARCFgRU-SQmBBMb9nbWmU5bbxLAIbfSlNlJ0htMJUpd5HHu_Zx-7CfwzhygjLDZ0aUe7cU1a3MKXrafV2rp_SP28Zv_oK9VbGsc1g2lxpiI1gKcEuk5bKoTE1p9m7Bc5jrVzqclZwGYZVkTCSx79dxmJYMPJUiinZdZWvJpPvpw6SXSC9tpW4PMOHvU53jH7Yzmc9C3U4qERVlWhR5zLMyYFmNKR0_yaqsKooqroLAT9LAjzmE2jwNg7Cs0gDjcXg7UYod77NO3Y5eB9FlklzG26jbEMnGcVgSdZuo20TdJuo2UbeJuk3UbaJu_3yo21EaJFUtIlY7p7OPG_qk43BAYAS3irMyjIK46EmkToygR3uI868Y1XCkW7n1btRa9Q48UpxRE6BG7ktbt4z3unDDnTfIc8TLWSAF4reUn79Epnf3qTOvEcg1Ppv32dKGS55d6_nwlbH3m5lqscU1V7h_xNoDMO8NT0Doqpxcn5dWD0V0QyONmlVaJiGgPaGRLO2hxE8FDtJ0U6z_Sr2Da3GhWfCKZD6xIBK2XCNfTuVZ6iwjec6UoA3IT5n5UeaHMcvDpC9_2iis99tODq_0UtnFW9sDudCWnmA1zHpgJJ8wqtiCj7TXjyrl431xlKOTnHTugKqI8piJPM39yibcnQDQcs1Oj-y2z8gKw_0MyIWVlwsEE93OOLgUkwY0jUJLXfTstm417ajBAzV4oAYP1OCBGjxQgwdq8EANHqjBAzV4oAYP1OCBGjxQgwdq8EANHqjBAzV4oAYP1OCBGjxQgwdq8EANHqjBAzV4oAYP1OCBGjxQgwdq8EANHqjBAzV4oAYP1OCBGjxQgwdq8EANHqjBAzV4oAYPP_EGD_KMX-66JvzeX--1d9j463p3B1niulw04OUs-Gj5gVs8HHKB-IO6PDgst-HLmKczjnldPsALzoOkhHiTn3Cxs5uUm0iyQTVZcYkM-OQTlYMBpdxnPJXP_skn6PYMzAg8aJ4EZbE2o292Def1deI9PPIDhxjgmMepX-eBhJU-3sx-g-wih3uCnUpeCywxLBd3I5l28v63r7_8A4YvoBJV-qGTStIb2teyKKMofdxVPMA36EduVCpW2fEWjuabLYbUTDf06xKiWfG409VDYeinRVOFK8i6WbXGb5CVXkxF6fruar5GERhqqeGcxM0jpxtF_FGW-01Yb1o0yHi4kWEHOslbjkvT1gumMJqSOLXj1G7vTvESKS6oPw03Z8dC9swa9e5YzXQK2zvO5c5GG55ClqNQSJP75evPvxotZ6Mb7FXRCj7SO-Js4HjXEdv-EGP2Te2HWQSDdfhUiXu86zjsGRcsH_pjdqYdBKDLO5csuUNud7cJMXXSGvNCbg7Qe88mb3UqaUc_EDsvHMAfx2N_YDffq8qSpPcqQZOxAheKV7q4t-yHtwYpeSjqyo9FEERZmpdJivfV1-Wu1iC2WcH-1iBkzMiYkTE7uzE7vPfP_b4lyUV_FC-DH7b3KDlLUxaccgwnnldVWMRpEvOqDEWJkKtCxGmRRaBaeFFlvK7SAhRDGkYpqzK_zPOUh_UhL7fWoSWMXvvxZRJdBuGWDi1ZVGVZFWTUoYU6tFCHFtyTrGICT4UfiqEOLd_sc363N2qR70jdWqhbC3VrMRQkOF2RH0WZELYe7PjEm_J-tKsLxgB7ocwWzZ9nuk4BoiBbizRY0IMlQr6o8f-WxvdTJ8LylqXwwrpxiSXsnwVyhYuIxXBcCrdDSd9AwFQ1Oawa1uTwodWFDggv-ogQi0syJLxhFoMDu_OvEjCmCk46LDVBn4HD2sJci_9Q4SWWQ-X7Ss62JfvLWqFXgl2AHbxQ1HqQEtVYRpUgZclQoyDh0xNB_Xao3w7126F-O9Rvh_rtUL8d6rdD_Xao3w7126F-O38f_XZizn0BIQkc7R6D2Jc57rGHTqpR2HA2BiGIyiLkNm3olC30kx5Scyghgn-vyTKdJEHqiFT327DtcHSMDDal-R7VyoU2nop55aBcTSiJBDwVj1oQ7lqdUlNCYEqdZo311rNfL8wXeZK6pjXbwHnJwR2rWBZHzOmD1BdODof3DVU9pjO-kuisXgItYsukDkZ2AE2nf4rQrvFsOZmvsSxn3tPldO4MpT--TsVUJWnZfmg0UgA9oRXrJTK0Fw0a_dFi1bZItjr01dTujHSG4JCJKM_5-efPXn7x5uVnhz7n5Ac4NFVtneA3ajR4f41o0v88dDImvTE0G3fFDx1X27OBYffhY0seJLxKwAvMe8a_raIZ2X1ACUzILjrmfINvc4dc1JqtJqARrnEZYVTF4ECXEZ0d5R9i6y0PxN6kYq-Na9j8GXlOSiUzh29rU44614RZToMSd4gQv-iwBcwBh0e7-0t4bwceecjnnZYG9-kdLu6AOqtRZzXqrEad1aizGnVWo85q1FmNOqtRZzXqrEad1aizGnVWo85q1FmNOqtRZzXqrEad1aizGnVWo85q1FmNOqtRZzXqrEad1aizGnVWo85q1FmNOqtRZzXqrEad1aizGnVW-zvvrOag2_rOHc9vZ6gIZAA6Z8vboZY02zqtCFYVQVAHBw662frjr97LWlYPZSC8nP3t3_8XhDoKFCeZbvfDLJ1dNDH7tjjHTC4Ka1-wbL21ynNNh63h692eTjT3PzvUcqbww6qM8tOetU7T19lyk-PpWxypHki1otxKjh48a6C3TFFURR1JNP4Jk3ptSMLS5IHqbVpJDtYwRcXXGSFPvhULyxZRRmVgUmEdV1ES1WuT2oeyHNqlYxGa29udOcdjZ7uzVwJT56KnTzu4QT28QXK27F1zo6wMLDbMUC7feNfh2d11DGlPI1ASsNnOmKVYvhfCgYg6CVamPef71ITxrsMx0PLM5BVM5zApNOZdx7tOwPYBEfAkTHEHpXeksRTqle6J-XiXJO8b_J5cusKrWfKySV1vRse7xHP7k16JJdMoqS0MRlckZLcDmaFBYIfpirejGdoX7K2av15xJ_nhCFCn-hC0N6umu926-xaLu7uVmso2SaqyS-uwekcWImCfj-ujJqKkCFgiclHBSWI5r-sgyyWzcmsfNdtSaH8fNTJdZLrIdN1sa2420L3wiOZmfXuvszQ3K4I8EFHA8jKv6zCLOWd-FcdJEiZIuq-qxIcfUubnPCvyKuF1ktYiTnwImaM8Eqc0NwuKSz-59KMtzc2SLItZIVJqbkbNzai5GTU3o-Zm1NyMmptRczNqbkbNzai5GTU3o-Zm1NyMmptRczNqbkbNzai5GTU3o-Zm1NyMmptRczNqbkbNzX6Szc2wo1HCwQRHPVd6a3OzLeXuAVpmXNY1i2KelVarO0V0y5Z5WFVcOYEbOM-_OsDKrWiL7z76JzQbjhQ37WhpkaPdx4pS83q1aK3FUba2z3XK7GafW9SHDh59iEWECezcW6eJmJ7HH91ksRkNs8XyDPekaA33MfQXdy7_YufyuZoLThwPhMaFfvPi1cvfvnzx2Zt_-cOXf_r8xWe_e_FG_veVjEDlLF4aWrrbQ8KiShTHaIEPNUyevrhyDC52kI6ELdryqmA569MRDvzBEdb9kAYT1sdBnkR5muShTYM6KIet5aPjkAsWtnR51X7yyWbWfOZwnb2__bf_bsP6kfzsthQ6fuyqXWOhqgqStEM4xmlZ76E6GwM3l2dxwIvYKgoHeeGQ5k9FUzCM1iDwUjQwc5pnC-UcjXSAZIN15eQ5qcbNvJMnpJrHv3cYb5vFRzMnwNCuOtGn1D6V1Q0Tgdpv2qyaWxUxMaiocQMqiF7_JGQVTsGyNo7H3AV1bwPcqeAdc7-YRVYkWTmPOyG_PW06oftm4Pzx8KoyCZuMluAd3atRSDKonvhovlqgQ2XrFXcwxvTIfpcOnIX6XVK_S-p3Sf0uqd8l9bukfpfU75L6XVK_S-p3Sf0uqd8l9bukfpfU75L6XVK_S-p3Sf0uqd8l9bukfpfU75L6XVK_S-p3Sf0uqd8l9bukfpfU75L6XVK_S-p3Sf0uqd_lB-53-XxHp8vnO3pcPt_V3fKV6mvpvf7AfS1F-65ZzFoUwg_X29JpTtI3ZlprSrOzNdhGkyenz8hpY23vL-hMcai_4Mxw2FBNq32Q6RNUV-AzSvAoOnDtbDpbdd6zl7pdyXjXO-x8mOyYp57joiAvIFyYLBsw8ndC1_Jum5tbTfrHzPbK2Kehdnbg5VqqnI7VzDck62f3m-hc_SbUFlO3R8xU9nY5qoOdH3BexCFLc14hIDllaViDd72rg53tG7W_g91PTUAP791nG2317bXCH7Z3zzpL7zBw66MoCgVEeX4BsWNQi7jkOQ8Y97MCbHVVxXVZxDzKfFH5JcRCvh_ytIrCFMxvuPuVtnQMC9LLMNnSMYwhwxacfuoYRh3DqGMY6jcegzzzLE54_ggdw7YZuEEeQ5KGcRXHIvPrg_qFTeAk3GuJBObDsSfGGGGNTKbu1gkcF1etZWPYV9ENYFat7cWk0flY5Zoz8L-8bjWdqqaz2A7FMVeqGZPcywtDfe9tYDVZaUyBzkVi7kU1DpjJlKgKhy7MEbjoWaw9h2Sw2klNu6hpFzXtoqZd1LSLmnZR0y5q2kVNu6hpFzXtoqZd1LSLmnZR0y5q2kVNu6hpFzXtoqZd1LSLmnZR0y5q2kVNu6hpFzXtoqZd1LSLmnZR0y5q2kVNu6hpFzXtoqZd1LSLmnZR0y5q2kVNu6hpFzXtoqZd1LSLmnZR0y5q2kVNu6hpFzXtoqZd1LSLmnZR0y5q2kVNu6hpFzXtoqZd1LSLmnZR0y5q2vX327Trux_-fyPFT-U)

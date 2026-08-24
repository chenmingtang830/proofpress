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
Bring a bounded OpenTelemetry-style export or an artifact. Proofpress binds it
as evidence in a local append-only Git ledger, then exposes only admitted,
current conclusions to the next agent:

[//]: # (ob:8b9b3369)
```sh
npx --no-install proofpress evidence import \
  node_modules/proofpress/examples/verified-knowledge-ledger/demo.otlp.json

npx --no-install proofpress propose --statement "The current conclusion" \
  --evidence EVIDENCE_ID --scope demo --proposer agent:runner
npx --no-install proofpress evaluate CONCLUSION_ID
npx --no-install proofpress review CONCLUSION_ID \
  --admit --reviewer human:reviewer
npx --no-install proofpress context --scope demo --actor agent:successor
npx --no-install proofpress ui --scope demo
```

[//]: # (ob:20fbea6e)
`context` excludes rejected, unresolved, expired, superseded, and actor-mismatched
conclusions by default. `ui` opens the local review queue, trusted-context
preview, and lineage graph. The 0.4 `proofpress knowledge ...` command group is
retained temporarily as a deprecated migration surface. See the repository's
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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzU1NmIxMTVkZTcxMWIwY2QzM2VlZDI2MCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjBhMjg1NjYyIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV81MWUxYzJkMDQ2MGI1ZDcyOWY4NWU2NjEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2UyOWYxODUxZTBiNDhhYTFkNDIxM2ZjMiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtvVuTG0eWJvhXYthmU1J1Aoz7JVVTNmyK1cVtSdRSlGpmlTKmR7hHZjSBABoBkMqqklk_zb6Prc3T7uv8hX3fn1IPa7b_Ys_xWzgSQOCSSZRKdcy6VclMwMPDL8fP5fs-_9MTtlg2NauWbxv-5PLJfP42SdIyCBIusiAo_YpHkRA8TP0nF0_KGb97y5sb0S3hs90tC5P0MkvCOmdRyUIeh0GdRAL_D5rgaVaxsvR9xtO6DqtYRFVcJhX386JO4oznaZhUJbTLm66avReLuyeXf8J_LN8u2Q08YcKW-KgL-KEUE_jFd2LR1A0rJ8JbiPdN18xa7xY-P1vceeWd9_ViNqvnC9F18J05q96xG4EvtfbrxexfBbzuaoEN3i6X8-7y6dObZnm7KsfVbPq0uhXttGlvlqy9ySP_6dq3F-LfVg38_HbVicXbatZ2ooWxWC5W4qeLJ7eC4SD6LMyTNA2fqN-8Fe_lh2BwxdskEEEVcj9O_TLhWVjUeSLSNMCezRZLfLW3k6YV0HMzI5O3Aj4W5PBVv4xzxgIc6KiuQvU6undvKzbvVhN44RD7Wc0WvHty-f2fnujH_-kJzPJs0eFP6s-Cvy1hyL9_Us24-PHJD_AGZjXAg1-_ePb5ly_GU_7k4qhFwpbLRVOuljA3b0vWNR0OM1u02EX4G0yokE2ulrezBXbmXdNiq90d_GUKf2nZFGdNderiSQdfhLaeXLaryQS6WN3CxAj1auVkVr2Dz6aiyrKgjOHjMCdL8SO-wCf_7__43_-___k_PoVf6kcwzuWz57h4xAf4zW_mHps0N-1_unpSwSiJxdWT3161nvebZnrjdYsKfs-6Tiy7p5PZzWzcvb-5egLfWMLv9WKD5pZ3c7nM2II9-emi7xWMTlEUolzr1doa3dmvf1hfy_oJuJpgZa49BBZPxos8PeEh_ae8pvOWt8KDddwtvQm7Ewuvni286WqybObq389eXnqs9WZz0V54bOC1feGLghfshB79fjVlbQeP4R5sgHbZeRU8EtY4X1XCYx6fVasp_N6DXVi9m9xdeLDQZM-5GOhRVUVZKsJTJuLNbdO-856HXz9Tz8JRedfOPkwEvxHeh9niHYyKZ7buhde03RzMizRRAz1KRR2lLM1P6NFvvX9ult6UceHhFoH_TMA8zhZs2bwXY2fdwGfeCZhaaH4Ca1y01dAYBWnB8ySM1nr0zZItV8ML9R88-6GBVQonQFGHfn5k687L-ONg7Jt1Wq0WC1wGnRrodj6F82AiWAcDAGeEPBeG3rUIAx9OqrXevGyhtclkz8v2nxp42wIOuDAR1bHtO6_7Tog5zB3sgD-KxWzEBWw7DlMIh9wdGM7WE-0NHBNqq3DeDb1uVgZFxqrg2O5cX193t1ctjm6jPu2NRh17L6A7773-5MGP_Ah_amcj8zn4Y98hXKZrHUqYiHMRlEd3CCzxan5tetPhzlOn_Ih9YAsYDc7mYMTlqHxYNHDYXLXXY9XTIUPN_KDg9dHzdd2PwX-W6_N6xwLVi9PDs6sVk7H35nagO3GYRUmU8bXuSNfnzrE1HrTFZ3UNo-HVsPU9cFpWS7Fn_R7azJ79HASpL-IofvQuvoHB-37j-1xMZz98In5k0_lEdE_N30f6708_9bAXA0MalmmS8Ch4_P7OcPtBG-iNyhNguYAjDDqA04--rHGGwBwv3nlL-Dwsh_msa4b6y-MiSOHUevT-2j29uWGN6ZGbDP4qT2B5xuBnS8ZvhrZ0VqRMFPlHWRD4bOF17A43F1v2vj_0GpxbBiebBw555xx-n4HtHLKJIivjGtyz9QMJljmsqrqBnjYHHQfbvzF0EOYVq0sePeS5634b8zr5dXMwyFY-QDzjtTMYrmbBR_D2yztvsWqXzZDfViYlLruHdE0vLwinvGoyg_PpmABrYHkFaVrzpIgf0jfYqrBIcF3A6mPtDOz0wmxFCCAvPFhKHNw7x6qP53fXHiy4oa1axODipyxZ69ofcJn-5d__T7Pw__Lv_5c3FWAY9qynoe8NrKowgBPDD6uH9-HNatHq7dpMGlg1sKJmsL8uh9zrOK7T7J4ze9LT9fKZy5UceWsTAb2aNOD_wC9hytgEIlNrV-CUv74eWD5ZEYM5jeNHGB8wR2AglzADuPm6JcQhd2PvCybdjqoS4H9wa6A6-KmG_t_CLq1mA0PIagiko5p95CHU0Yk7husfHbLwoiiCKgvXuvjmw0wfeNBHb8GayZ4V_g_e9q8MLO6oyJM0L8uHPBicuQZiJYicfr8qL6SL9iUcx3z2oX36-zdffqGsJrqNjQw6ZSYFH_BeTIamrfDzGsL8h3Tt1Wq50bfZogHvnk3g2x9U12yArtsdey-Xg05_WVdFFFTsIV3DxW7GAjrARTVhKs70OFuyCzhhlipQl_Z3sarQ0emwb0Ndy6OirnIWPKRrXxuPomKLRQMhH_Sgmqw4ZgnaWTtaYLi0wF1qk4vSAYNd-mEwU-AXScnjjTi1qTy5TvTjDgiJN78xmMWJ06hOxEOe67gFbNLNvG41x7FEIyXbuR7fLqeTa7nK5c_wo87rdUMLKWdlBdHRQ7p2iF2fsFVb3Y7mE9bKjlrjPmCTfB-OnTz0H9K3N7eN8aPkF0fuF70vv_taL3OvXrCpwIwPbE_v-ZffwIobijjClIVFzTct-o1Y4rmgMrCH-AP3vzCwjqq6CqqIsQc81VlGOovcn2tmvYCrJJMsnTRXzQIOt-lcOfK7xiMRfhnF4iHjAVaFz8DLl9OxWs6mOF3g9N15WAEQ0ljC0prOl50Ow6pFo_4xdPbyPMqz0r-fHWzeM1iVU1hy-5y2-58dmJ-E10HEqvq0Z71g1W0_B7es89DFVvtnyEGLyiQUURmd9tQReMR6K15fevVqucJMi1kSZiVYTwePKTEtBbbjnAITCIXXXfowLbKchad1yoPnTcGs8_FQRJMXvgiC-OT3bm5aWFi8f204DeX_ouv3rpnP156_8YpVmsZhEGSnPf8bCOKqWzzCaljUfQy9nHnQPjgHFWtxK8DWwQi-ms0bgaZ_gVWogeRnXhQJS05cDL8D28dw2Y0wjNe1txHMPCai5xBEQYg1tBTrMPeTQJy4AQbPkWoiVLHAhgej0Wy1BLukfjlwjpSwofKQrUcwz9GmoL2vJ7MPe0zA_c8OmIDMT3klWHTaswZHgMEBCvOz07uvB4YgioSfsFOH4FsIrK9H4HVhbRU2DKwQMMtYLJE10n9bgY_YwJLlMCBeucCOCp3MqYcOjSJLiypY9xS_FIsbMC26SirdGcyy4WbUm2DPZB3UwMAMxlkdBjy6V-CCvk8mwu7DWS0tYQc-gy1b7QuNDmxj6HxJyooXuXjUrllfGyMRCANmnjI7shQuq1FgkqY4qGPvX4SYe0K62zKIGQoD6rjIKz941L4O7g_ZR-lh2j0yYnB4CjQWV1dXbtFoY4NwcF58nhWP2l0ZYc2mU1yDLQ4bDKsqXKiqpm5i7D1rdaCFBVH4RjnofGZxDk6NH59vaO-ZHjus9vNDyb0kS0T4yAvhGRyJTQvGv_OmWNQuRX-Cbmny2oE4XA9l-wKWc1E-bl__cCta6crZ-rZcqZiKhyUBZrP3yUewVBhar262WlSiuxg66X2_ApOenXuDGcPqHsVyd8GBPLQM4riKeOo__tAy6ZuA1wTrAPM7U7FkmMCQpt8kOD6Zs07GOJ0HFqJpB5O-ISyCKk7q8w1tw_EIrSFclt0c4RvJ_TWc-SwzONWrKH_cjprOYDKh-yCzL_I3yzvvL__-f3hXT5Y6qJYnvNlaV0_kX2ftIHwkZEWSVPeWwTerBbSw92R3PjZwSMLcCZ7cC4cOecLofm3gcqM675Tln3_xcnzVjiQ6Yc6qoVCIlXka3osKD-mQJ50zDBGMT_WZY-XUwoaQAE5pnN_5qgSr7M3FAmsmQ0Yu9LOgLrNTBgjCosmkewpD83zCMB_3HJbkhfzvj_A_q0U3W1zI8fm68RQIDPvvZsc3x6fOeBSEp4xPKbrlSNQ1JhVrWPQlq955t7PZu24ocExh06RZzk8YgBcm9L0_D5ewCJa3I_imXi1LWw2dyRTwwADkoV9HBSuP7s83S9h8qhqIK-B7s7uZrEhjX3784RP4ZffUwv0-RXQChPA_3h-fHy4MlPCJDvrfVhBrKjif_IuBB4q3eZH5LBVJwnmU87IoY1aEqYwuwHeUbZrhMacFrN7q3XzWSNOj6ucK82f-hZC_HxAmiekOpwUXOuk0IkGZJ6Iqu1m9fFvDuhSL-aLR4M2uDC4rntVVnKU8C5I6FVmYFklc5VXgp6FgWcSFX-UC_pjU-NGyZLzOChbHAWd-JQt0mGWUIEw1W5dp8RMMNKIkQz9MR342CtM3fnYZR5dh-o--f-mjKdQjjkmNgvM4EDEskP63f3oM5KZcbQpYecu6W4x06iBlaZwnlYzYZRsO1lIvxIeDKDHZiH-D339o-PIW_pLn8I9b0dzcLvW_oM3fPJ3_dsu21b3NkyytozxICz8yvXUwmLq3-6GVujlepOjzZ3kpcS6yOQdtuQHaOx5EiQ79qFUFFQkoXFy18sRUhaeu37hmGse73z7IwEr6rPbrUpjuOlBM3d2HICwrXdOUXexuGcTLVy36U7WsVcG7TuVZs-pWKitbId53gT5VtZjBAFXyiwrP211430zAGF-ANyawnNrJU-Gq7WZTgUDzX6GfNp0t7sYyxITBFT9WAtwW6NwH9OqwUzIdr1Je4N_BOGIdCD__mTcFb--q7bGattahA9g1qKSC2zF8K-jvhTJGGrqFiWlwka5am_PUEOQLWTGQ5V7WyTdaT3aobIh6VxxwlSpfiIm0vjDVs7W5RddUTGpwkbqZGmMDbccpUkuiXxH45gOrAZY9ZylYpVyCLuVqcGCwpuj2AHSrHRjszlVr-sr4tFnioDT4ftBxu3Q9W2lB-AWD_X5nSisVONxTbAq7ctViNQHGSCEQYJTBtuAiks5Cd9vML7yZKjlMxNLmZAcGI6mLqszqNI0F682YReDqwXgIsNaDXbOaqE8OTErqB6HIWVhUhemHg7s1BmoYUqvbYiwHJy3MAlbbd3JQtpvW6WgArT8Oxz4E8vNbNg4gLFFORbdmz-wpbuxGdynbB99Xrlqc57s_guu5EXFctRjwmiI8Tmjn1O3MornwsPNiAQaynMHKV6usEXpH6TUoN5azP-Ers4kC3THc1bLHI43Jk54KTGejLIgGkJo6hjItd7PVVdsKXHRg3H5Uq1ncLJTb1CnHa2Ci85rzvMrhnC0yO9E96Lif6EE4sW7MT5MgBzdKhNwewg7CeHOmj8YOM8SJtXIVqCosHkTzyapz4FEaFqiTVWPTVCRbwY2Dll_nBPnl7qGpeFwXfhllrLLHlANQ1m_zMOixGYjRSM_q0YDHXWG1MShpGBW8ZGBlrXV1QM3mJR4CV8aePYWhbmqIYMb_CufLtcRVNDLWns7Bi4bOyty1qfNfy65fX8APMvS6voDmKhlxXUuTeQ29gFZsPtfY7IWYMugkuCVLGB8MEA9xOPKq9sMikg6ktUA9ktoMwgMw0uh0zLG8tURP49ofQwPXmJ2pxO1swqGbDVaDwXVET117KTWD3W7GfOhQ4HVRIn4AHHXTfQd53e_RB0KmjXsW5FHEk1CkWWVNQo-itgfy6fBnNYWwr1uxAm9hIs_R6Qo8tDuZ824lGsb4d9KRQCgym1z09dr3gfeX__bfvfeh9kdhycn0GZbWrlrc5i5g0uwlZ46vL1SuTdZ_rjvoB9hNTFRdS6hAiyhUmErtSOBabab4PtfKoF-_l4N9rWYfpr6B4wJ6i7YYplo0ErQpk1Uy_3nVOhaqnS3W0VPa1RxYBGUCPkHO6iCu7Bp2sOJmVh4A8saOqYBsyCgmLGZ1zLIyt0bRgYDfN4qnYLeFZ8PCPcatEHDgxCHnfmrHxIF3Oyv1VFx2ozEcsBIc3Jj0PnVQAiOIbsFkxjgaLvGjqGCHeRiXo-Ucm4MTT2hlRDt8ErzZ_dGBhdUpP9SWTxAFDP8jfoSJwz2hqun68-qIh9mE7aPq612DMQeWM8WyunWdhoGFxeD0j0KeZFVoB9HBnDuu3qEIct1wXYdpUfJc5Ik9ehxQ-dao9DiI-FSaXeUygKc1sGzDtK7yKovB5lsT6qDI15ftaZjwbgyfgqnga4f-9hT5aHQrJvM9qzsqwrysfJ5UknSrfXCLLu93_MlYcbUTzEd_Bd2Fz6ij2uxYXENTptEdxguQKI_vbQL1h0_0T58OLDOe5pEoooCBL2J9wx6Q3i-zI4HlZrA40rp5nZXcHloO1twM1hGYcZNYiqqirNCiBLbfDox8feU8GhzcWFsfgj8e1XmU28SOgxB3DNypSG8IXzF2uW3gUG3RkGgMrUIhS-dH4wtxK469b4RKD_RHl9yi8hzpw9DZQmVIVB6ht2cG1S1XmDxNpfOv0_3GycP9PoMYH7veSQsLUc6iP9Qv1tIz0l90s3PSHcCXNEdzbd3GpSpiy2j8qpXW9KlqFaOzz7DuJgfRge817Xs2aTiMpetX4UurRIRsZIROhJNZkAGf2VejicB8yGQ2ewcnni5xgG1v2XvWTLC5gW2T8chPkiiuyv6IcyD4hyy_vVB656NqTg745GR2s_6xwXUM3itEhnWQZkEfhfQofbv5j8DcGxcgyqosCqKk7ve9A8PvGZIng-rh04vZ6uYWlhk8nC3ulLfaIFrT1LKUSzhfTSYysIQ4qBt717DyOud8eKpW5rVdjeyq7QRO-LJflWb5ri8hVf_4DAIRWGDTES5pecQ_7e7aCvc8HAH1CvxoXJEO5IXj5rHrV_oD7goeWHcpi4JaiLryC5u0cTgEelwfwggwo2wDApmc06bAYjXRnYbXQIdLr2O55Z3cJX4fohqm_iDNjkpX36wa_CpW-nFTqzBCH5DK83eKybrmMpQSEzyLOM8LHiZmRBzqgmOLTyUi4DhB4CQWIzDVWHa7aqWjWVXyXwhKg5DDnM-YwQV7gy0ZJI6ySN8FvfVS6UqVloRxsXlJTyFglkL7s3igf4BIVcB2xgMf5qCZqawKxrAS2TNgpKpUQLyYxFlsyxkOdcJ4eg8gQsDcgYk5WFTl2mSxPS2i4n37-gt1HOjJQWcHTqRZi7hs54GzUn4clT0612f6z0rh5drBN03ZHXjmEoGBJx3MnhNM4PMh4BWLNW9dTZBE-cxKXPW4cTXysEXkD8w3bAITUOBY2JhCOmDtHea_boaWaVQnYc4LWJi9v9JzRdYztwcxP4w7DzY1yusoZ1HQF5ksGWTTnT-a2gEmU4GzrnWOSVpItWaucfeM-vkYNRK6ubRPwJSAink9VR30PtEvAdsCB-lmwea33QUc-40E14gp7hf8qPdvq5ncPdAyloaYrAqoVsCmqTUrwMFVZr5ubgzAGrfup-OrFheWheroNWtrPNe_wY789voz14FwbIRa_XaSYZ2z-Rw2oFwxT9-33Mmz_aNMr0lTovuu1gw85CmWon57PZRHqkSOaDs4M-3ScDgzR7iyOxkwe0B397-36-NdC8NzO1tuPmg0QgSB3oGjkbJoOn1gkFsfbu-8qyeyPCKrVq4HLD54sNXnQu5cMHLLqye7OqESPFv6PJyTqCBwTljAq8C67A75py9nnUzlsel9t9KDRkPb_DshPbhpA2EheC4tHyFk2JQnVNbA-DSvBWy8p9-tYNOsmgmHFY4dgV3H2mbZ_BGM9IUnOPog3YXpwbyZCzwuMUMiT9A7BUp2_DZ11OHgowMAfcMucyF9eSwqa09qvYIiIVcOYAsDBohlpE9VzW5a6I6HEbb0uE29V4YPvdntD77ZFLM-1VDlMchTXjHGAj_uY8aeDHUvJD2A22SOQ8yU5hwC97i0JrinO21ayqPZS9o62fLuVWuWsyels2DeJ0J9SZd8pQclwx_5FWXJthWB0U_g4Doqv6SvX_cAKLX30OxOGoX-naqjFboPy036MbIqLV2OG_TtlnojLlfwHPtyvKnrgenxs8rPRMJZkIg-aLDcLOPaP4BqNZvgbxCbCosNoQDgQC9kf-EUgFeVS15BxLGiA2f_OjJLvWYni0qwWrl0sxVkQZcMwLaw5W1nC_-25qwr6srbv9CeEI4utDXSZB73ZHwpnyBrm6rIiNsIXdkPuM1hr3c9w0nvDLWRcIpUuV5luhlWbhxVtevP1sLdmxUuSHAF4Qie6ZhBArlgXmEwwLSOvd8rjTRPZX2kH6UOe8M5AqsGnjo8u-pTlzIS0IeVzXGiacHuXchKoDz8ICzWsmzwQreIAdFerw2VpLMq1xO28avO-oJDaynMk4zFEDcHVZ-LtGy6fqsfwJAzKcWixHg2CePAt8uzJ83pJo8lwpmjOojAt6qTLPdtsOFw43TjD-G7aQdE4j6vpUmFJuxX4FTCoFOtUZsmUav1s7WaWO_IbEEFmhRzmTHfT1kS1zaJ4ZDq9NsMEuVMWBoXKQ8Zw5qyPV177lw_Lify4UyHeVyyMKz8qrKHuEORM7DGB9DesEqNxf3XYgRHF8S8uPZtCx2CITtTzur5P8u1oUeHT9YM5rhol2KEvgGc8BN1COCxYPE-xrhLaCce6ogt8F5-rn3amTJLI_VracYtfQa6MHSKMhGEVZLXRRL25cKeuafH6lQ2npn3AA7UpKoQC2Me4hD0DnFd95HukAsiP7M_nRVVURRHUVLmVdSnAiwxr7cmB5DtjIFKgjjxE2i290Uc_t0hL7iXU7fpXq-Pxn7PWqPv-AiibVOyM2dJ_zvzaUdfcyT1Nb376pr2owi1BZ8dsxqLOWaQrbt-9QT-LNMYnfd0OZ0_VT9LnME9j18mmQSbwrE869TR1U2x9GYCD-X67_X4D89r8ixPQ7-IWdYXNRx6op61h1AOtfFyMutw4MLcrSZcJ_rmgoEd-UYWmRUcDI13jy5cL7DhUy2USaEYnTzAFgziwM6vg7IM_cyP_B5W4fAg-21wKo3R-NOwD2I8_Hxuc5EOs9HJHp9OSzR2poyCIi7LLAmt6-4wFe9nsk6gGbYyZTlXRQLWvbtqnQmCr9WNxV9imhkWuTlhMcDpdGlF5oYh0JJhgCowYFq6rcGvWA4VQvOiDuKsTHLG7Zw59MZD7Mx-biLsSHUimj-Xs1KZGNy1e_ZUnYmyzP0yrHsIpMNodPOsJ9IRhedQG2DYVBBlJkR-X6bllL9cYikKWljhFzsBT8TtYscanlAvFdIDj9tuNnmP4RkczRIApVwoOM4hfNRVI-vCo--rjHZ3DyOILa1asJsDMwmbrs78JEFHyp4YPZvyhBNjkwq5bea3TPqO6TZrYfe5Yiy3HTcFWdCbWOdr1F4-2Go7bzG8zorI9xOIycswtX5Lz-_U4_cQcqYqCtnMmCkxYKwMuxutTwftyUzFtSaOXJvW1FBrBOgG6xLCJASrYAAtFLLHgFoRRmoIlxIYcL3GdFQQP3gyOvEzhKHAa4qFhCCpb-nqFHjQ7Q040I3slcpG6T4OnAgFiqn7kagdpJrDQ7VaKqeTSNc2yWoOxwge-BDh4Dhg9zGJZCh-F3KQ-7AY50OJwl9ooyGnkNvK7cB2q8MoitKMJ7mDiO5pq4cbziHOqdxGaB7YorodMWdv2V-W-1d2FuV5IFgqqqRf2T1l1Z2FE_mm0ALOhE2WX_QZQ_7phZPZ2JHEw2oNA38Hlt60aTFDUJksw1XrsJmGIoIwgDgwyuM8tOUIh-t6UGH8OKKqyRomvqiTuARvxLoIDnfVPPjBxFNvyjC4FB4CSGV42A-rzAfZnM1CqFSXKYUpk_7eJG_gTT-wTi94NpE8F5gwedzpP2Np9IPMyt6YnKJMNLfou8tkmn2YBAONB6lNpUirtPa5XXwOUdapPw0yYPvyvvCLPOV-bQfbIcU6eZCT2a4Ij7tUsHLJ_UHPZikZQgZhrgquPZT5PtRc5VB2VPsvndK-SaSMMIOIDrHO_q2ltnZnJUSWVkkU-uAc9YCwnpBr0yinM21tvXQ4mxZXaeEHVeEXPZzDYeL2s3IyxbbFvCym9iergbxSGaVBWfOQB3GfV-oZuHZAjqPWWnBp5IcFC4o86ak4PdvWvuTpNFoZKgxkoYK88Ms6C-sy6H31nl_bi8idTJzFkqPscilu2fsGQRZYSRJggtGJvVMt2nDnmcljfhfYOdJtf_3q9Ztn__TFi7fPXr95-btnz9-8_ebrF8_xWWBqZOfweME6O5w1GNJOmqnM_UI48L1Juv4TVqsYkmZknLrx3M487PXL7549_69vn331-dvPX37z_ItX33z7Wr3YBhX4JxzQLReLYOr5_rUi8pISmeC4__vt15CoW1ZkJkP_4XUD5nPB_9o3lEhn-7QLSg66_2A641hZ4A9WqncaalewkXBuvv_-iaRfwO8ksevJDz9s8rtVFmhXz7e0rrjc3865zC2pwpiicXTy5ZyyAvLIPE0iM4UaDUOQHVrjlRky2q6XP6grZs-io9vz3O4TvpYzb42iAl0Zq8EwA_ynJxBP4TChVdcZ_60kOBVemBFA7wCe996l0yFp-2ASPXiWRVkWGUtSFhdZlFZxFNdhYd_WZce7zHCXMf-nv-X1eLiqgGXV22ddhj9tp83v0xB4HKGACJyrPCgKxvIajk4espoFccUEJt3rMCnqOuShH7M0ZnlSlVlZCjh1k1qEaSmd7x2vdF8qIAgu4-zSz7dIBYQ5rBnoCUkFkFQASQWQVABJBfx9SgVkaVnHPCzLLDpQKiA8TCrg5VIRyB275dTbj9YE8O5JAqyX0U7QBLCwDV1EeKAmgKckATCZRpoApAlAmgBbGKFxHCVpVtaZf6gmQEiaAKQJQJoApAlAmgCkCUCaAKQJQJoApAlAmgCkCUCaAKQJQJoApAlAmgCkCUCaAKQJQJoApAlAmgCkCUCaAKQJQJoApAlAmgCkCUCaAKQJQJoApAlAmgCkCUCaAKQJQJoApAlAmgCkCUCaAKQJQJoApAlAmgCkCfAz1QRwCKI9d3qNcHo4D9thbz64LYf7dxine8uhMsgzP6CtjU45TJqHNeTQOfqGnksKvosacHIYR72wQ994aPMbXXdICA9t27padnx7MP-j99sBH_dt_17jdhwi8bFj7aCOT253c6H1YMm-UYW682Rm3YDtju2tg5U8vWElVuA260AFT292c6n1xfm-VVmcbzpwm6WbJr1U-IdTqT9qQJxC_aM8Y8tU2hL2x3mAkxrtH_ClSt2s50ePHRsnE_qAljflOvrs3mM26yRzHrNZJ5hxlvYMollw8xbHDqkTzBzZmvUWTVMOIbxvqm9BF1dRU0Ql1h7IGB8a-Z4SfmhP9nDGbcs9NfmIlge5y_Y86InKhzb9ECbzsfI1wz15CHd1cGdaZt_BPXkI9W_AFXAoacesqUM5a_aNe4LaCavgaAbbkPPc09OOHPvT-GsDY--wzg7tykNoaUNRQM-8OnJQHo2aZbri8LAOHpQHELUGBsVhIRzTk1NpCgM9cUD_B--eB7ACBsNFC3k_8gg6CBPfR8sWAH-CuTgaIT-0CHog92PujJ1I74Gd4cCdD1-Pp-Ohh86vHuJ3xCo4AANoPeIe8HfoA45FBNpIrYf_Hfqoh-ADBxxNB7p3aE8GsX123fRAviPe8ESknzUUPazv0Ic-BPc35DX3oLlDe3Iqqs480oHQPYrR2IexGzAaDn7uiK16AMDOntc9mu5R3nUv3G7gZR2M2KF9eQiIbCgb0eO1jhj2UwFdNtbqMQGHPvUhoIGhTdeX8B9lVeyv8Q_52X2R_qhhObGKP5Tk6CvpjzIsR5barVHo6-oHd-PBhfeh1dJXWw8_-U4vxw5lr_ty6xFn5cn12CFvoC-4Hj4mx1VkbYarL78e_tKn12cHXtopwx7sNTygTvvkIFFsp3S3U4n6tVDR3Gqh0XYS7CWp8rAIsf5q8iQXZjTUglCANKbjwF1lvrM-1ykJnvW5h4iPf4znOtXGsz7XKU6e9blO1fKsz3Uqmued377aedbnOpXQ845zXyk97zj3xdSzPteptZ71uU4x9rzz25drz3su9CXcM68rW9k9r33uC77nfd--HHze87evF5_3POoLyufdR33F-azPdWrTZ32uU8je8Kc_5vT2VeuzPrYvaZ_zsU65-5yP3bwt5zyP7QvZ53ysU7Q-69v2RexzPtapWJ9339rq9Dkf65Siz_lYp-x8zsc6NeZzPtYpKJ91bvvq8VnNRV9NPuvc9qXjs5qLvkx8XuNoa8LnfKxTKT7nY52q8Vltcl8iPuuS6ivIZzUXfQ35rIPcF4zP-VinaHzeE8gWiM963vZl47Pu275CfFYr1ZeDzxqM9PXgs26gvvh71sf2Zd5zPtap6Z513_Y13LMOcl-qPetK7uuyZ33bvgh7zsc6BdmzRgV99fWjP3bblbtIhlBa53XdVBJ1s1bMVd8e1c2iU2rdgnWIY0S14oq1R123W4Ss9qu8DmCCqyyqKlaJglf-rut27e2q-6_bJaonUT2J6klUT6J6EtWTqJ5E9SSqJ1E9iepJVE-iehLVk6ieRPUkqidRPYnqSVRPonoS1ZOonkT1JKonUT2J6nl-que9iiCYjaIsi4wlKYuLLILINIrrENMl6FFLdVubQ7wMowvbx8vY_-nClBzdWiE-Rbml-Ize7Tc_vtVWznRi8laERR3k4FD4ZZwzFnDwrKK6Qkexm9XLt46Iu_xGVwaXeVgEcSHyMi3ruPCTOAp5Vpdhkvkiz1gUpKIoIr8q0iBjQZQHPOM5y8qwzJKsLvxDXxA_8ST0w3TkZ6MwfRMEl0l2GcT_6PuXPrbSj0CWcD-qi-iJOy5_egzpXnV9rKy3GtXsOkhZGudJJb0wJSgtqiwLSufCjt_MwX0ER_c_XT2pBN7ndfXkt3ia_KaZ3njdooLfs64Ty-7pZHYzG3fvb8CesckSfu-Em_g3-P2Hhi9v4S95Dv-4Fc3N7VL_C9r8zdP5bwd13NMa5iAtfHvHFbxnURTCvTHPW6vxDtyWl4UsYaIuBfP724Nt_XnzTswbeX2ue1WR595UxNTdi3KTG917aeXVpe2dvjLaXEEKBh93kbrO8p-dCw8HBMAjFtWhX5RwEli5dafM7VzuBO3JhudiNtf3yMuEir6aUGxeQmTvpzYhGqpuVzoX9EHe7tTf7qhv5OgqlHyW90JKoXpM7OI9llMhluqaY4VfmMJYDAn015znVQ7Ltsj6C6Jtxb0X6B9Mpdt7FX0_L_0wDlKrBO-U3HVjr9XNSJ1JlEYXOAeqv19hMSLI_3HgqoeKx7D7yyhjlb1lKysDsIDV5p1FqOpvEtGjEV7bOeLiveOjDCesRyNtBo7Oa--7KiyMkxQsRM5qe3OhgykwLyEbvjZv0PX3XHrg5s2X-jICfdPRtXMz9FPwhJsazlp5M9r12PsWb3e5tl2UTsD1hXddyaP_Wt5teg3PuJaRhcnb9rdpa53xgZXEE57FIhIpF6G9l6tHNzjX4A2V8XcvLhYWEDn4RRWy_sqVHt5gFtdK3rHU2fugOnV9hjUd8Hau5UBzMLTYQgFuB-NhGdqHOriHIy7J3p5p_qvd3aduWrIpoTPcjpfmcRxloUjy3B54DszDuclLj5iTKFepM9NZ-9I6f6Vv-bptwNvrL0jDuwSMwT_wRjwVPnYqwt5y2Fy1J9yL5-dRGZciSePIbnUHgtLvi-1Qkd0bIinAywAXN2WZNd0OBsVcCCH02WLvm1MD8kZeBl0180bdGKUvdGnBZfHuYLDWajb6qoCLqxavbZepLnVbycDWgeDAT5IorsrU3lfBanCNopodeiVPizcHLw_ZCM1U3oB3wCfBGTrmTscoAbOT1WHNgv7aaYvJcW4b3AFy2T1_UZqB356BvezvwXVQObrpP3uvISgR3p_VvePGofnzVfvn0Wgk_x9-NE__s5xXWXp0UwBTdf-PuuXd3reOFlLdOgcmaSUvZZL3V6jWvVf9tSS6XfNaOj-vyt64RXT0alyvP29DCJllkeQhHH1hJDJrUR3QkFkWO-7P0d6PrnCvXaVjw22FnVm7FAmOb6Gu2Va-kroJ3d7bU6qbRlRWzTmX5LvCl96DD46XeQ_de-v7MU-yLI-rA26PHwT8DKwYOP14mXEIEvzTrpLvb5DfcXe8tHTSqYSRuWr1zfH24uBd98SrGuFzdTEr5jT0le-ec-P7VauvfLdu754r36s4zeqA1cJn_GNc-a4vStZvhze8w4mxeQ28N3wL_DdCqLf7fq7LR2Y57b2fRq63tZW8wKTQkJMFpoclmcjBaR-6_NTbBXcaOE5KzuoYQjr47-7LTnddYDr2fof45gt5Z-b2O0zNDabuzaV4taU03PLINfdq6iX5i7jANIx4VFeJz5Pc332Bqbo1lJnbSWFw5J2j-iZMZbAQHCBvZ5IXffc3H3p0O-jHvh00qNIYIjUGxjbbfTvoNxDTj6xxs6WY-5d6jr1XKrhSLml_Wac626Ar7mWbn_UzjddYyzTivVs8hy5lLqI4yLIw33f_nos83G0j6iSrsjwMeSWqoQv4vv9dA5E2mEv0XOxxapKsXExnP3wifmRo9OCU138f6b87aVC8Su_7z9fypVM238iWyo-96O8vO-ZCMvndr9ctNyyhvbZbfu-ZG4vDd3Save_Z_UwyXUD2C7mAbCvmdltbjPPzYG8rcAmCOk1P6NGb26Z95z0Pv34mPZI-vkWX-tLxiC9MSKYhpbAKH1eMcmYIWvAKlcyVLlbdcjRhd_L22KW4QX9dOu7yUspjhSefzyASqEzGY6NBdFesueqhOiqs2SdLZMZ16HXAkq0mcqJH7rR6aqPL-HUKnxvvmtkDHiWnkYFfNrvRd7mKH-dwzOE99HIwbbRTgf_KlrtobeYeWZkaWuKFpDd4L-_GkH24xSgJYdAYfOGnlXmx7ywT4A4H7ijCG8TdWQjRdxIEOfxYJ6WAw0ve0b2V8GZLOH-7hDcyLbtNy-F0SFsbVH26DC_cKuFP28t-Zyl8FmUcsiry47gI4f_9iAVpVZdhWteRD8FXXVV16vvgsRdpnBZFmpepEEkexOjLqbb3vdxG0TO89OPLINlS9Kx4GuRBVFLR8yMXPUWFhoyVwh8qev7615hpk5baU8ce7hs4NZbNXP372cvxr389cB1zHom05lEZs2R3ofIed6H1ZnPRXqjIa9QqQLi-tH2jkLqWGr9q1wqxJiG-u8SKeTlFmrFZKZN8Um1JJPwB-SZv2aicHp45aE4G4qCkLqoyAxMWi_765t7O6kF5iPl0jvbBYkARZ8yH8Cm1G8CxrrYIcrrRxBICRCTTZinryNp3gelQMGrpm-FHZOuYd4Iul82kWWKaHzYd5uyk_97dNnOZ7DLJqatWA2ypnEzlZConUzmZyslUTqZyMpWTqZxM5WQqJ1M5mcrJVE6mcjKVk6mcTOXkn2k5OUviEFavOKGS8f1_-B7TP9rl-eETI7HSTG_G3W0jJrwbN7On8Jmn7x1XE9PTnz5GtWdX5Wh7wdV50e01w2eSGge9vfCev1SeGBov8MWkz7bqkOT7rpM-hQ7hF3IHy7TNcCV0S91VzgW3B8-sNaVORaXvk6fSqwb_BbfOjsok47P50n4Iea0y3wBLBwyOaR4O4JuV5SivFrAoMdBowTND737Oqnfmr-WqmXD91kcVJ9OKB1GaVKzMqyQQZVaKOi9Evqs4aUst-4uTv8yFenhx936FK3ArXMFP2wtYZynfxVVe8oylme-LuCqquo7yJBJBEWRBEsRxFBQZD3ORiSz2Wc6DMhfwCjnE-FVc1NkhL7elfBcU28t3vh9WgvmCyncfuXxXxjGLyrBIFPdUOb39LtXNPWTz9Z_-8OHDGD7yr51U7tK2yvk4uAvwoOcv-28cIvTVPdVCxk-NcEb3tGrGd9PJU9RgE_c68bAmVRe_UEfKpfcMXuJWjMKxv3NMZB-e6kNopL-A3xiVk5Xp3Bcvn7_46psXn-6ediqz_vXKrDzLkxSc-URE4ccqs1rfgIqsVGSlIisVWanISkVWKrJSkZWKrFRkpSIrFVmpyEpFViqyUpGViqxUZP0bLLIuVJEVU60fs9DaiUn9FvPwi8evsh59zVq7mpYCB_X7759EqNobjYMABuf7JwE2EoZPfvjhr3MRmRP9nHyp10ajzmn3gAuKNi-m6E-Hx2z2oTcVbS9QO2tkgK2rXCx9bizgyFdBiy1I62Ivzgc4JaxZSHFqec9ipTRsx7uWyhmf6iyiMz7VWWVnfKqzCM_5rv0a_dhP3YZIqE5q2mar1p9xFAQhS4u0gGgriyuR5wF4rUVZBOHOC0FtuXg_BIGsOFnxNSt-OPplizBz-tN21MJ5MBtxnYVpVHLYKVGR5pz7qWAsLTLYOWEY-7VfBikr0iypwV_mNatZwpFaHiVFWoe7X2kDqRFd-tl2pEZe14z7cUpIDUJqEFKDkBqE1CCkxjFIjRAzVynz66DMjkBqgA_2j_fRGmFIaA1Ca_ws0Bp-mKUsB__cD4O9aI2hJTKI2Rj64jbkxuBaPAN-Y-j5hOIgFMcgiiPNojAqIIgssnAvimNopW3Fcgx-YQuiY-jzhOsgXAfhOgjXQbiOXwCuI4l4xiEc8ZOy3ovrGDoV_i7QHbWfpxCD-7nP9qI7jvBeHXTE3iH-KyI9jvBvCe9xHN4jEzWEUmA_it7bJ7zHAN5Dfuo59kViJNqbHz55_uqrN69f_tO3b15-9c_ycPh__m_4iDyWwWWFv__-2Vf__OKLV-aPuDu-_wbebdEs4aj55sXzb1-_fPNf-69i8INZplmLMs_4gM9fvH31u7fwoM-_ff6GuP2PgDpxPFenwrU9EjiJU-88YHeRecKk9ZI54s3rflXIIC0ERBImodzdtZW-AxK-hUR2I6VtnREMxMDFG4Evbr4F_qpR9t5Rlu4Evo67vU0QIn0vedhLez-b40SB-2CeDWt1i1evHnxUfbr2fbA8aSySICzLKE_iBOKsJN8cMZkYt1Ll7sigYy6EprmbQratpu0vZD_uwji8AL-lZLjOXO8rgmepgiaiCopQZBkMRwLBUVwEccDDLEnrmkei9JMwT7Io8rM8rIsEXKS4iMKCZaWIkjAId7_SRhU0vozCy3jbHbtBUPu8SumOXaqCUhWUqqBUBaUqKFVBqQpKVVCqglIVlKqgVAWlKuiZq6CCpXUWxxATZsHHrYJ-bS0x9rmDVS_XPBdz3CRwfjTLS2ynWdhxkjVSsbtKio63a2eeeUvBpso5Z5Nu5n1gmLYGdxhTO-JeL5UnP8WgYrHCrPagxb9rq2uboZncfSbjAzN11xB-wah3t9dOpRf_rSy8Sl-hxaTCLRVuqXBLhVsq3FLhlgq3VLilwu3fe-H2MS_PdSL6h7JIN9rmOYsjlhdrbX-njB5r72w0_iswS3dLMSjSDVZh-Jtb7ITpR5lXRZxKI_HgftihwcAKgihwS-AHTFxry6hgmF9__rsL71VdN45NvRgYqiIvRM14-BhdPCTrtYBwsmUy365eSHlE4_kAIzYMMy5UpfbBfcRYFGXkl9A79MCglcrmTlVfdFrnGtu6VmcluNiwzwaG8eNILxxyUfrnokapf9cL1Tr7z8y16F_3gw4_LmcVOP3qMnD8vFi8NyCG9bqRzO6Nd23aPcCKRjtwNv4txfKDULWki82HqVjLLmlcyyrhrNDEMFT37jJwtvj2axNewmkj7bW8GQHCpBG7aWeYJ5SLxJ3Xe9fTO7t2e9MvILK2mQTbZ7MvTb1yvGufbW8UJwlaQKiIPcE3dwuOkvbeTDp7vGuvbH_ONxjxdrooCP2_vwdsdIklMtgRLYdfYo4c3LIWR0-t0-NVHb6Qt1TImRcyRlULUV46r5_97OuX1miZidkGlxE_zvFrzpKXPrVeUSYf-1TmYLV7iKEZU8H84r36nDO661h2MFnGpKildxSQJoqrIkwgQhVZlIoqSFkYxEG8sWWH9ye-n5kauV7NOnOhNRaisR9aQ0c3Hd10dH-ko_twKN39C0Vi90KR6Kft-KuzYM54FkUJ8yvGy8pPqqAq_LQO4iSBfqR5VPp5UadFHOV5nacFL0NfpClLwzIqCgis_UNebh19Vrzx_cskv_SjLeizJPezOE1Ig4PQZ4Q-OyP6rExSkdR-xIKkOhR9JovGc_DtBz2aTSwUQskQb7OOVtsFVPMOwqldtcaB1TWnHVA1by9SDZP1u6Fq2PWNwMKe66KFd4AhwXvMZHXvqi0xseucobox8SOOlzz7JPQLzkQZ8hjgOQzyEnxwGaFBKyt0x6HrBoKOn_1VZ53zjiB0BKEjCB1B6AhC93cNocshBMmCmGWcsZ8ThM7J-7k-sUa3OKC6q3bn0b8NVNd7HvYInrI77LNY4L-u2vvZxP6AnbBK5z_RrKljVfVoYGOmPqtLEYAjXtuN46Qu-o15dALCgiDBHpeJCJMeDeLkJO4nXU7ILHjNFIYbjohFdQsTgtbKHaahDVylaSGCICwqW051khFHbOCdKQVe2z0EkzRfLe1f7FfGCohwYPt6C21p3xmy7U8Y3GlVGrA6r1gapWGPhLJJD2ennZq6aC-9b37_bBQmqYKQyGzgREDUcguLfFndrqehtwh5aJ9HQc1wMei0LrpH8GH4xnICzg-sojneHAybXOB4V2xS4V2_gsuTDDzZe0tIWg3teSIECd1T5V9zhI3O5A3FixnmGnTWWMIEwVfBxiyDUHnR7ul71brvL6cR3m5B2FnCzhJ2lrCzhJ0l7CxhZwk7S9hZws4SdvZvCzsrolAEVSj8Iot_SdjZvWAOB-OiW7QNff361Xcvvnr21fMX-OObV89ffUGY3PNgctFq_rUBubcrCKF7QO6qxQxXe-gNXgN4md4uyKBXmgybMxsCNhwLiDn5QUdhWk5-ylGolAe-y447tDbQipv4OC7Q3SyFrSp-QO_YAtHcjMgeuOKWts2RYt1ea486MVFe-R644majsHe8z189_y89NHAtayNzqcL7t1VTvYNTdLHcg1PcfIBQOMt7D5HIv89_p1BxvVncjhQ0lt9TwSP4nSb_vJ51UrPdj87am5Tilr1vZovxcRc-JSKICh5WIU8CMBMhOOPgQoldFz5ZxMsBFz7Rpv-5bfrDQaBblLnin7ZDn84C_PJrvE4Jc0EFxNA5Z0kepCIOwiRhIbxEBG2yKknCgPngrNYJZ1mYhVUN7ZdhUO1-pQ24V3rpF5dJvgXulcE-TKuEE9yL4F4E9yK4F8G9CO5FcC-CexHci-BeBPciuNdfGe7FgzjFm2mzMq4OgXvtiyd3b9G6YlGecw6xGzsd97V2ct8rdcp8T6cKkRqeA96jRSdpq3jZJ1xevfovMA9rGRE0cH_As9e-6MVVu5a32uDYyu98_fnvtO-1_e9ypDRwYMiryPKoSss0CFj9yAA0u-ngzX68j0Gzf3wgCm37Q-wc7n7MoBUQLIp8v8qZ4PFuKNrvYJgxoQYHl5nhdbgZOrGzFldL80e9_aeCYdG7Xk30YtCx3CW63zrBJnMqCCuUBll63HcaETCR7aJ_Bf_ENQ8OwQXM92wpf8BTxi6h2RKTY3qRiGkpkEoGHeANG3uvBT7YsNX_t5dfOxA36ejr8iYYqSW0pjju8i_4nftdlV8ey1yis30UzkXD8CYQbEw-8zDOMAAJnTeciiXslCWDjbMFaOdg5AzUzrNIu_FVC66EB56EbN5Tj9Kq-mjUZL5TD7GOFXBLaewcJxgcweAIBkcwOILBEQyOYHAEgyMYHMHgCAZHMDiCwREM7m8YBvcAXUqnMPpgcavHFMoqwrqsAllYH25rU-wI642nVkoHepSyqCjB9Kz16A9wKJgKmo2ipjhXi336Wnu-OgAtSqvcr-KAPUpPnrnXXmEkpuMECIalbV_0LnQ9m0xmH6B5eYbC0A2NFq_LMI_rR-mj4-PN4HiQKnxSgw_-YxzgddomtgleOLiEh6EMnW2wE1P3WtQL2GDq6F-yGxweWDT4_M23knWs-0M73rVddj5T6yUaf0MfB7-Cc3qGpW9MfM3FbK6zBvKBnSoud3o25VwxCFVgmYP9uy8_6OyzHaKH-n5Nrovw8H4Yq0PgzVQteF0BcG3jdevSlKbWL2vhM5uDkF0Z79pr23v1TOY2mdepeBAblHYcu_ZhYJUdMi_O9tr-8M813JRvtoQCosy7WbD5rVqelXLy8Ygx4BKBnjYmhHuAKizze_Pi7J_tnTBaoRreMBSI94qMGJE2Cqdhqjp6p-DAiR9v2aqT7zJboNu4XCh_R0aOmILC99F1_a2Y0YXZIpuSqmZGRmZGetDN5ihuSKziWgEvYSFz0BtLrzlWZ7IIkjwualZzXsXMZ0FQZTUvd-FLLcRuP76UzlM6T__eztPD0duDMofhT9threeB8rI0gw_zKImKKs3TFIuiaZoXQRbwELz1lGd1FvKQBVkM3noU-2kZ-YEfFmHI8vKQl9sA9eaXcX4ZFltAvWGd5mVYCAL1EqiXQL1YjijLOvFjkdQ12wfqPcbVGIT4hiVaMZGEQcI_PsT3WXfVbjrz3Rw8HX2QoNfsuvIXssyEhQfYaGKhXquTGCOTmlRlFKw6dGKqkJ9Y4tcueJ_3g_5wUTW6YOO8kkQFq9LZxlEDpwJOp8X7Gjt0CQ4cM8ACfqH-9YH1LqlEGMwwfwreQjNXQjkSTIiftAHDbKHrJQ4UUAZf1o8dqpLlPAzBbINps-ULxwuyFZ3TnZs9sOpjkc_eduDzVXsU8tkj4PPPHPgcFLyMgpzFSdCft70z7JZvj_VozROECMIM_BIW5PYJvZNrKkAP8FQXS11ta7pbXOdXbdMHvjByt3fzmQTCYpVX1Rig42LRMLBIjqFBl1T_qDPvqvALi17vk7H3eVNLcCI-cgYbE_eLFALDeiq3f5RBND5brnrZEyx8eyWEhzUYHIamT6Bkm928KNzFBc6oruAYtS7nIokl695BO4hVMpQGjbs0S7lTe7_fBrAuZCdx2WMoC0_UoSLWYSA-1lAG2b7EG8D72gU8tHL8NII9yuA_FnzuBAab59HR3r0T-AtVer1qbYFQL21dktUZAdmSSTn0aLeLPv3gZh0M_NWaT9WtbgVh_nthRxhdDlw4uBRx2XjwHp1KRGgIOWvNtoYO9jd7KMSt2inGPCJWygDfbB3ZQKXk4zrwSoyKn33_2YLIC0ReIPICkReIvEDkBSIvEHmByAtEXiDyApEXiLxA5AUiLxB5gcgLRF4g8gKRF4i8QOQFIi8QeeFjkhe20xE-Hu2gE5P6LYIGFo_POcjrMmZBVq1h2d7AQekiKVpv-WHmqR2wD_q377sD2D-eBrVIk-Jx-vKNrIxKE4PlRjjy-_ymBeEqtx2vC7qzIQ20PwTeZGEiguCROqnPrek73iwc0z7q5Wa9__gfvYpv_duASmiehlmRcfY4vfwP33-9EZ5f6LBbudcYUqsE3Q-faOiZ7uYQjjKtiogH6eN08rU6OmVtaV03TwUA6NurCW-WJsjAj6D7P3STewpeEJPou8eb76FTHeMLT1V9b-7W_ZOBCY-Kos7Tqv4IEy475NR1t88zLNWnss4wBKLO0iAs4vzRNritUNi9i7EvVvXXcERj73PY9pMZg8H8_lqO7UAvBcLMojB6nF7KROIKUwq7r7eD_qAPBYuzlYgHk3Id6GQkyhpGM3jUZQnH58QbffHKM_hBCEPHCqSIPr3O2d7HKw6sSpaEOUuL_COsSpWgvZfWN-nzzSU6MJRxEBeVii4eoZNvZtJdgw8Kp_Y20qkf9BYvPGQ_rsVF-mQaOnZ4nQYpq89mhmwV0jFFKrAZEqf2WRTWif9IG1wlKbzvbaZhw_vWfvemAz4wlI6P33fSDRl2Mjm0X7iVteY4UmsvtMPB2fkZx7_Y-RnndN_5GedwHeiPPdt2fsY5WHZ-xrHrOz_jWNXdz-qN2s7POCZl52ecHb17nPsNtfMzznLePRf9arq_brbSsmQLCjn7YWaiSsfdw4NWktNGusr1_IuXZpkfx6wSUVCIJIwEzwMRlZXgVc39iO9iVlmew35mFUUNFDVQ1EBRA0UNFDVQ1EBRA0UNh0QNhzPf79NXgzX-avDTdnrqWci5oij8HHqbhWXBgijIRJzwssqCOg2TnFUiYCIukjyIKj9hOTyhSKsyz5JIpKUI4oPebo2dG_lvwugySS79YAs7N82LCJ4TEDuX2LnEziV2LrFziZ1L7Fxi5xI7l9i5xM4ldi6xc39J7NykKmteiCIp-wXgFCP61XRCQcGMWsXBVeYlBPtlv8ZsjcHAIx9QJ-iPKoNsH0ucpNykSHBgXBErbOLCsBNKUUsfFvwaxXjYpHRKVcjuM2xQZtqvpclBluHKGhH9UXlELS1bZDJrBznERcbrSoiyju3QO2WN9S1xWmkCLBSyGuCsXJpdBf8c3R20xU5LQ94P5xC0-nQ3mnMtw34YjWl7Un43jengz2P1ZO3Dg8YgymMRRZEIotJaNKfeo6fvITUbm8sXJpyUMevuFVVEgUj8ohaid1-d6o615qdXaNCxXla3-svI43DYkugQDaz3qM6juAgTpG_2dsCWdQ4Hng-UZnaDug-f2DoQWYL8EtiePYnM1nW2TeyRtRnYa_CFkfrwnjkteepncG4mZWrJXU4Bp7eepxdhcFRul9PJ9RDseu2Tn6qgdFVCXLnEenuDjjr4MNfOMF8rKrqjuAA-6vshJzOKYHkkYZmnqcWjO2Ug_a4PKeUYp38_-7Jmfgn7uyjC2AYyTrVnfbWexVSuEazP_cyfJTkcnIgwilPOIDixxMe-1rVtpx5ZrzLbFrs9cjo3vGdFGJWZiHxwruyedcpbJo3wgBKVjEfUbtcUdRnctMoTUs2BjdfukNyt5vjEv63mnDmR_RC1KkyLKAx5WPZkQ6cIdrjR3l3Igm6swD70vJ672WpIfUTuYfT1ZpMVvDuGaBPW7uP2HHe4h3lRxKKE1cV7fZe-qmap4adXxrYTWgwVUNJrZY4VpgzpmeKWvW9mC-UydJqX0cfUJL9D8jskv0PyOyS_Q_I7JL9D8jskv0PyOyS_Q_I7JL9D8jskv0PyOyS_Q_I7JL_zy5bfQdhVAn5IlCTFoPzOm54nSeo7pL5zT33n-V9dfUeWA3r1nedHqO88hBa6STRRlmYb6VhCUNHSOTAMfK8RflLdaYpZj4mAc-T5S3SOW0ROHsM2LpOAl2Etgtgvi6DI_LiO_CRLd7GNLW9jP9v4I43S4XRpS1jZxcHpSShn4eBEQV6F4M8xXsdhUQXg0eRB7cdVjua5LNC7iYK0qlkJ5rmM0IPIQ59VrAz8SmJnd7zSNuJNcZmkW4g3cZHUicgTIt4Q8YaIN0S8IeINEW-IeEPEGyLeEPGGiDdEvCHiDRFviHjzCMQbERR5GEKoD67POYg3-BPWUZobWUoYY17LWwuR_9f-e082P4-Z5wl8oW_9P-sE7bhp30OEzlVmneg9RO8heg_Re4jeQ_QeovcQvYfoPUTvIXoP0XuI3kP0HqL3EL2H6D1E7yF6D9F7iN5D9B6i9xC9h-g9RO8heg_Re4jeQ_QeovfQ5do__8u1H3I13SZxRW3Y7bdPbt4s6Xxf8W-evABfF4yGhxbyHhdIwTdWC1nF7B3zkXL8MUDB7MESpn98OMEI2lnMYEHIs-mh9CIWJ2EShD6YpyiqksxnLMv9LNpFL7LslP30oo80S4fzo_bSi3qqzVnoRWnOgsJPS56mRZLHfpWApxJynkNI6VdBEAk_4Wkc1uBhlZVf5AH4W4LVYViEQVaUh9KLgjeSVXSZJFvoRRUcoFGVC6IXEb2I6EVELyJ6EdGLiF5E9CKiFxG9iOhFRC8iehHRi46iF2VFVMUhnDJRlv3d0YsUQgHTqRqrrqosO9M80vQ0puiKBkIhJFUOZwo-b0OcJeIsEWeJOEvEWSLOEnGWiLNEnCXiLBFniThLxFkizhJxloizRJwl4iwRZ4k4S8RZIs4ScZaIs0ScJeIsEWeJOEvEWSLOEnGWiLP0C-IsYY3h_oVEF08U-2Xz99svMMLfS0_b_gGN5s_pYqOVROi1B3Kf6jgVKUS8a6yawQy54Vtx5T_OleXD82SODq9KVyi_WsaoiEPqxOgCvM9uhf8LFhX9_REiw3UUf7vFdljeT8aqsgz5I_TwmOrNRvp6i102XRRlCmdtGT5CF1W0fwMLWSxU7ffaZTsYwoBFpj59H1xL4wCG5jAOmjPj93qhCWif26PAxdLbR1oLusIiB-vEeNd0bW_-Gee6ZG-GWldKTAkJGsZYkFn4rR2Q8a5R3_4kxApoP2YDyqUKhUtxs1Zeki4ynHBLeNta3rdlB3oHo84M1p6xgu-Itq9QKlrDvYePj2La5TmyocI0zYIq5zzMkoonIRO7mHaWqLWfaUc24RdtEw6nbFp6oOrTZfTTdurfWeiOWZLXHI7MkCdZFLAkCjNRldBMCPFoVsdl4ad1FNZlWVdFEWalDysEwaQsLeC0ZTvex-E65iO_eBMUl0l8GW27Si1Lc9hjQUFcR-I6EteRuI7EdSSuI3EdietIXEfiOhLXkbiOxHUkriNxHYnrSFxH4joS15G4jsR1JK4jcR2J60hcR-I6EteRuI5_fa4jj5M6KZAkl9qA06n2mxzkA4r2eofokjdmXltdkYCFsYas2ARL2Bq3rlxIP6efOVm3Hlg_cRgHYViA5ynsonWAAidYtWOn1eZQHdgInniHGL4GDUmPMJTAeJz_4fnMeBHCScmy0M6nAzxwuKun4gdk1QXGqOEad34_UaAKKnCe3oil4p2Z818F7nUDx5UGla4tgM-uWucIlwGthetoh6-7ZfN7UJ0LmRtV9SaYApVahm6Zzg-mB4noS0RfIvoS0ZeIvkT0JaIvEX2J6EtEXyL6EtGXiL5E9CWiLxF9iehLRF8i-v7CiL7VDqJvtYPoW_21iL4akvYWgZ_dR7jlsM6YnydijZC2RsjZSUA7nGYkuQO4zaaw6xZ3I7XVDrwcse_gTuaotsYGabyGzAcjN4NIE9MBuoCgZlxuZDVR0koixmEBE6WtGwxG1XSSreHhqOwgemJsJY9NNSfNH_HhGFJ1tybVsq9XGjmx0avPTB55O1XVeHO9t90o_xHH7TjSKASzSZTFZZ4VISujLI_CKGIS4b4xxk7HmWbQoDOlB1L3QS20z8Dl5spT5pirx5PC00tBNSGdT8tFtUS6A259_Fmt2sM5uPephus3RfZMwr9V6mRwnzoZ-G_84DKKLv1iC3UyD8o6ieKcqJNEnSTqJFEniTpJ1Mm_F-pk4Cci4VkqSr9P0vRuzdHn0XZvBUYIOufAGUcCC3pCgCdwM0Jnbjxv-zPs5WSyksg5CZHECpczUWsrB6dBkU96volz5AWh7x9wzBF_lPijxB8l_ijxR4k_SvxR4o8Sf5T4o8QfJf4o8UeJP0r8UeKPEn-U-KPEHyX-KPFHiT9K_FHijxJ_lPijxB8l_ijxR4k_SvxR4o8Sf5T4o8QfJf4o8UeJP0r8UeKPEn-U-KPEHyX-6Mfnj74CV_LZS2_XfbH3_3yPTbr553VS6XNdhfXewKv_7V4jW1RpldUpW6PpvdDx_hBJD_ay87EtW9k8IfLTPAEH4-gn_EEYnib6fWpxC0wzs8nKwt8d18DSasACDFxBWdVxmuZZenR_kBKFW2EGx4E-QYwtAddwxe8u-xDA_D4Inwah5943udEfBkEXrMrs6P68hsFWBUtJ85FdMHkR2MvwTzAET9f6ObJr9CBir7M4hoi9zISYDqVkCYMwnzUSrb7o4Z7rAzbetVB2XAu7mk6ZIvBig2ZBwIiYIofEhGB6y97WKstp410LYPitNFV2gtQGU5lyB3m8ax63N_sFtCM7KDN8pkU5d0tR3cqcoqfd17V6Sv-4bfzmL9k7Fcs6m2VzqCE2gqEAt0SeXBaVqSnN3i14DnP9SoezktMgrJKMiST2_ToO05KBp1JE0a6rbC2ZdD99mOwS2aWt1O0BJvx9qnP803Ym81mo20kloqJMiyKPeVYGLKsxpeMnWZVVRVHFVRD4SRr4MYdQm6dhEJZVGmA8Dm8nSrHjfdap29GbILpMkst4G3UbItk4DkuibhN1m6jbRN0m6jZRt4m6TdTtXw51O0qDpKpFxGpnd_ZxQ590HA4IzMKt4qwMoyAuehKpEyPo1h7i_CtGNWzpVk69G7VWvQOPFGe0BGiR-9LWLeO9Ldxw5w3yHPFyFkiB-C3l5y-R6d195vRrBOsan837bGnDJc-u9Xz4ytj7p5mS2OKaK9w_Yu0BmPeGJyB0VXauz0urhyK6oZGHmjVaJiGgPaGRLO3hip8KbKTpplj_lXYHx-JCs-AVyXxiQSRsuUa-nMq91FlG8pyphTawfsrMjzI_jFkeJn3500Zhvd92cnilh8oO3tocyIG29ARrYdYDI_mEUcUWfKS9fjQpn-6Loxyb5KRzB0xFlMdM5GnuVzbh7gSAlmt2emS3vUd2MdzPgFzY9XKBYKLbGQeXYtKApVFoqYue3datph0JPJDAAwk8kMADCTyQwAMJPJDAAwk8kMADCTyQwAMJPJDAAwk8kMADCTyQwAMJPJDAAwk8kMADCTyQwAMJPJDAAwk8kMADCTyQwAMJPJDAAwk8kMADCTyQwAMJPJDAAwk8kMADCTyQwAMJPPzMBR7kHr_cdU34vb_ek3fY-Ou6uoMscV0uGvByFny0_MgSD4dcIP4glQeH5TZ8GfN0xjGvywd4wXmQlBBv8hMudnaTchNJNqgmKy6RAb_-tcrBgFHuM57KZ__1r9HtGegReNA8CcpirUff7WrO6-vEe3jkBzYxwDGPU7_OAwkrfbye_ROyixzuCSqVvBFYYlgu7kYy7eT9L9-8-grDFzCJKv3QSSPpDc1rWZRRlD7uKB7gG_QtNyoVq87xFrbm2y0Hqelu6NclRLPicburm8LQTy9NFa4g62bVGr9BVnoxFaXru6v5GkVgSFLD2YmbW04LRXwry_0mrDcSDTIebmTYgU7ylu3StPWCKYymJE7t2LXb1SleIsUF7afh5uwYyJ5Zo94dq5lOYXvHvtwptOEpZDkuCnnkvnrzxdej5Wx0g1oVreAjPSPOBI53bbHtDzHHvqn9MItgsA6fKnGPd22HPe3CyYf-mO1pBwHo8s4lS-5Yt7tlQkydtMa8kJsD9D6wyTudStqhB2L7hQ3443jsD8zmB1VZkvRetdBkrMCF4pUu7g374dIgJQ9FXfmxCIIoS_MySfG--rrcJQ1ixQr2S4PQYUaHGR1mZz_MDtf-ua9bklz0W_Ey-Gm7RslZRFmwyzHseF5VYRGnScyrMhQlQq4KEadFFoFp4UWV8bpKCzAMaRilrMr8Ms9THtaHvNyaQksYvfHjyyS6DMItCi1ZVGVZFWSk0EIKLaTQgnOSVUzgrvBDMaTQ8t0-53e7UIt8R1JrIbUWUmsxFCTYXZEfRZkQth7s-MSb6_1oVxcOA9RCmS2aP850nQKWgpQWabCgB0OEfFHj_y2N76d2hOUty8UL48YllrB_FqwrHEQshuNQuAolvYCAqWpyGDWsyeFDqwsdEF70ESEWl2RIeMMsBgdm518lYEwVnHRYaoI-A4e1hbkW_6HCSyyHyveVnG1L9pe1Qq-EcwFm8EJR62GVKGEZVYKUJUONgoRPTwTp7ZDeDuntkN4O6e2Q3g7p7ZDeDuntkN4O6e2Q3s7fht5OzLkvICSBrd1jEPsyxz320Ek1ChvOxrAIorIIuU0bOmUL_aSH1BxKiOA_aLJMJ0mQOiLVehtWDkfHyHCmND-iWbnQh6diXjkoVxNKIgFPxaMWhLtWp9SUEOhSp1lj_enZjxfmizxJXdOWbWC_5OCOVSyLI-boIPWFk8PhfUNVj-mMryQ6q1-BFrFlUgcj24Cm0z9FaNd4tpzM11iWM-_pcjp3mtIfX6diqpK0lB8ajRRAT2jDeokM7UWDh_5osWpbJFsd-mpqdkY6Q3BIR5Tn_PyLZy-_fPvy80Ofc_IDHJqqPp3gN6o1eH-NaNL_PLQzJr0x1Bt3xA9tV59nA83uw8eWPEh4lYAXmPeMf1tFM2v3ASUwIVV0zP4G3-YOuag1W03AIlzjMEKrisGBLiM6O8o_ROktD5a9ScVeG9ew-SPynJRJZg7f1qYcda4Js5wGJe4QIX7VoQTMAZtHu_tLeG8HHnnI5x1Jg_v0Dhd3QMpqpKxGymqkrEbKaqSsRspqpKxGymqkrEbKaqSsRspqpKxGymqkrEbKaqSsRspqpKxGymqkrEbKaqSsRspqpKxGymqkrEbKaqSsRspqpKxGymqkrEbKaqSsRspqpKz2N66s5qDbeuWO57czNAQyAJ2z5e2QJM02pRXBqiII6uDARjelP_7svaxl9VAGwsvZX_79f0Koo0Bxkul2P8zS2UUTs2-Lc0znorD2BcvWpVWeazpsDV_v9ijR3P_skORM4YdVGeWnPWudpq-z5SbH00scKQ2kWlFuJUcPnjWgLVMUVVFHEo1_QqfeGJKwPPLA9DatJAdrmKLi64yQJ9-KhWWLqENloFNhHVdREtVrndqHshyapWMRmtvlzpztsVPu7LXA1Lno6dMOblA3b5CcLXvf3KhTBgYbeiiHb7xr8-xWHUPa0wiMBEy202Yplh-EcCCiToKVac_5PjVhvGtzDEiembyCUQ6Ti8a863jXDtjeIAKehCnu4OodaSyFeqV7y3y8ayXva_zeunQXr2bJS5G6_hgd71qe25_0WiyZRkltYTC6S0KqHcgMDQI7jCreDjG0L9k71X894k7yw1lAndIhaG9WTXe7dfYtFne3lJrKNkmqskvrsHZHFiJgno_TURNRUgQsEbmoYCexnNd1kOWSWblVR81KCu3XUaOji44uOrputombDagXHiFu1st7nUXcrAjyQEQBy8u8rsMs5pz5VRwnSZgg6b6qEh9-SJmf86zIq4TXSVqLOPEhZI7ySJwibhYUl35y6UdbxM2SLItZIVISNyNxMxI3I3EzEjcjcTMSNyNxMxI3I3EzEjcjcTMSNyNxMxI3I3EzEjcjcTMSNyNxMxI3I3EzEjcjcTMSNyNxs5-luBkqGiUcjuCo50pvFTfbUu4eoGXGZV2zKOZZaa26U0S3bJmHVcWVE7iB8_yzA6zcirb44ZN_wGPDWcVNO1pa5Gj3qaLUvFktWnviqLO2z3XK7GafW9SbDh59yIkIHdg5t46ImO7Ht26y2LSG2WK5h3tStIb7GPqL25d_sX35QvUFO44bQuNCv3vx-uXvXr74_O2_fPXqD1-8-PyfX7yV_30tI1DZi5eGlu5qSFhUieIYLfChhsnTF1eOwcUO0pFQoi2vCpazPh3hwB-cxbof0mDC-jjIkyhPkzy0aVAH5bC1fHQccsHCli6v2l__ejNrPnO4zt5f_tt_t2H9SH52WwodP3bVrrFQVQVJnkPYxmlZ76E6GwM3l2dxwIvYGgoHeeGQ5k9FUzCM1iDwUjQws5tnC-UcjXSAZIN15eQ5qcbNvJMnpJnHv3cYb5vBx2NOwEG76kSfUvtMVjdMBGq_abNqblXExKCixgmoIHr9g5BVOAXL2tgecxfUvQ1wp4J3zP1iFlmRZGU_7oT89rTphNbNwP7j5lVlEjYZLcE7ulejkGRQ3fHRfLVAh8rWK-6gjemRepcOnIX0LknvkvQuSe-S9C5J75L0LknvkvQuSe-S9C5J75L0LknvkvQuSe-S9C5J75L0LknvkvQuSe-S9C5J75L0LknvkvQuSe-S9C5J75L0LknvkvQuSe-S9C5J75L0Lj-y3uXzHUqXz3doXD7fpW75Wulaem8-sq6laN83i1mLi_DjaVs64iS9MNOaKM1OabANkSdHZ-S0trbrCzpdHNIXnBkOG5ppNQ8yfYLmCnxGCR5FB66dTWerznv2UsuVjHe9w86HScU89RwXBXkB4cJk2cAhfyd0Le-2ubnVpH_MbK_M-TQkZwderqXK6VjNfEOyfna_ic7Vb0JtMXV7RE-ltstRCnZ-wHkRhyzNeYWA5JSlYQ3e9S4FO6sbtV_B7ue2QA_X7rNCW728VvjTdvWss2iHgVsfRVEoIMrzC4gdg1rEJc95wLifFXBWV1Vcl0XMo8wXlV9CLOT7IU-rKEzh-A13v9IWxbAgvQyTLYphDBm24PSTYhgphpFiGNo3HsN65lmc8PwRFMO2HXCDPIYkDeMqjkXm1wfphU1gJ9yTRILjwzlPzGGENTKZulsncFxctZaNYV9FC8CsWqvFpNH5WOWaM_C_vG41nSrRWZRDcY4rJcYk5_LCUN_7M7CarDSmQOciMfeihANmMiWqwqELswUuehZrzyEZrHaSaBeJdpFoF4l2kWgXiXaRaBeJdpFoF4l2kWgXiXaRaBeJdpFoF4l2kWgXiXaRaBeJdpFoF4l2kWgXiXaRaBeJdpFoF4l2kWgXiXaRaBeJdpFoF4l2kWgXiXaRaBeJdpFoF4l2kWgXiXaRaBeJdpFoF4l2kWgXiXaRaBeJdpFoF4l2kWgXiXaRaBeJdpFoF4l2kWgXiXaRaBeJdpFoF4l2_aJFuxR-vtoh3XXvr_cEvDb-ui7jpaHpSsxrtPzIYl6dmNRvsYq5-BgqXg7bpBc2OpDXcrh8ksPSeLynWPNpnuLg6R_7XbbrizmDt1Py63OBHmIJQd8cg5uRdE36ZLmKkNXu15A93ffxrhEckjKbIA5SwXLhKKqk843rQlLqnDdWFr6eYH4XI7TRl999bct5412juvPJLyAWwkS_wdlK9oIODVQE-O3LCwv_RHbjbKHD3J7yj1oLrNuhbfZC8ojk1_1xojtdo5Oo0Mam1L4Gqp1pligcc2gawdr1i8COynF6ZUkggirkPkx9mfAMArI8EamE82zVK7OqVfv1ymgrHroVD9eQ2yI7Fv20XVXsLEpqFfjsWcSrROSpEHVWVEEYJXmOINVCoPucRRCSJWUY1SHLSxElPA2LLA2KmAVVvPuV1pXU4jd-dBkWl36wRUnNZ2GepGlISmqkpEZKaqSkRkpqpKRGSmqkpEZKaqSkRkpqpKRGSmqkpEZKaqSkRkpqpKRGSmqkpPa3oKSWlHWV5EXIA_ZAJTUloqbtpdnOa4GSCTthgzrOFrpoutjhlnow-lKvcuEtFYx1iyLaheSAmrjSFE8MI0aGlvvU0UQaC56k3E_j8kHqaPeLU48sjna1HxEuSz2jkQSPyWP6SvIzNkcIIrUNgPiL715-_gIL5VJhbEhczSiqDQ-GDDeE9_zVV8-_-Pabl6--2quNplMJa9-w_VSkzhOFzkzO4d57yRK4fqluBcdT1832tLRq7umgDZNzq7TMYIdhYeUx1ct65TJl6uWLjKYQmKAyAXoP7m4o77xe0GzVXKMX0JrblJRDKwf-31ZiJS5MBnJkSWlzV5hQl3OUP6VQ2P44dilSji0aj8fXpjwK35iBZW86zBktmSS1mYpmg1u6k86XLb9OGyNOBc5AjQVH0kojrTTSSiOtNNJKI6000kojrTTSSiOtNNJKI6000kojrTTSSiOtNNJKI6000kojrTTSSiOtNNJKI6000kojrTTSSiOtNNJKI6000kojrTTSSiOtNNJKI6000kojrTTSSiOtNNJKI6000kojrbTtWmk__PT_A_0n2B0)

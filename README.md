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
**Verified knowledge infrastructure for agent-native workflows.**

[//]: # (ob:0e0e9d9a)
Proofpress is the open Artifact Provenance Protocol for knowledge work. As
people and agents split work into atomic items, explore alternatives in
parallel, and reassemble results into documents or decisions, Proofpress keeps
the admitted history attached to the artifact: what changed, what was accepted,
who participated, and what evidence or reason supported the transition.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzU1NmIxMTVkZTcxMWIwY2QzM2VlZDI2MCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjU3NzRhOWU2IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9lMzU5MWE1ZThlY2I0YWE4ZGZmMTc4MWYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2UyOWYxODUxZTBiNDhhYTFkNDIxM2ZjMiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtvUuTI8e1JvhXouuatUgpgYr3I6mW3VKxJNVcvrpYorqHSav0CPfIjFtAABcBVDEl0eyuevZtbb2a2fZfmP38FC3GbP7FnOOvcCSAwCOzQIo6C1FZmYCHh_vx8_y-4395whbLpmbV8k3Dn1w-mc_fJElaBkHCRRYEpV_xKBKCh6n_5OJJOeN3b3hzI7olfLa7ZWGSXoqwjOMq8YUf-zzP47DMyzAr6zJJ4pJXdRqFgciyKix4GCVJwMosj7I8FKkflmFewbi86arZO7G4e3L5F_zH8s2S3cATJmyJj7qAH0oxgV98IxZN3bByIryFeNd0zaz1buHzs8WdV955Xy1ms3q-EF0H35mz6i27EfhSa79ezP5VwOuuFjjg7XI57y6fPr1plrerclzNpk-rW9FOm_ZmydqbPPKfrn17If5t1cDPb1adWLypZm0nWliL5WIlfrh4cisYLmKSZTErRPpE_eaNeCc_BIsr3ogoKQKWiFxUZcxYzus6yPKgxpnNFkt8tTeTphUwc7MjkzciLOogTwLhl3HOWMDjMIjqKlSvo2f3pmLzbjWBFw5xntVswbsnl9_-5Yl-_F-ewC7PFh3-pP4s-JsSlvzbJ9WMi--ffAdvYKQBHvzqxbNPP38xnvInF0cJCVsuF025WsLevClZ13S4zGzR4hThb7ChQg65Wt7OFjiZt02Lo3Z38Jcp_KVlU9w1NamLJx18EcZ6ctmuJhOYYnULGyPUq5WTWfUWPpuKKsuCMoaPw54sxff4Ah_9v__z__j__tf__Bh-qR_BOJfPnqPwiPfwm1_PPTZpbtr_dPWkglUSi6snv7lqPe_XzfTG6xYV_J51nVh2Tyezm9m4e3dz9QS-sYTfa2GD4ZZ3cylmbMGe_HDRzwpWpygKUa7Nak1Gd87rn9ZlWT8BpQkkc-0hIk0zXuTpCQ_pP-U1nbe8FR7Icbf0JuxOLLx6tvCmq8mymat_P3t56bHWm81Fe-GxgdcGTSAKXrATZvSH1ZS1HTyGe3AA2mXnVfBIkHG-qoTHPD6rVlP4vQensHo7ubvwQNDkzLkYmFFVRVkKeuqEGb2-bdq33vPwq2fqWbgqb9vZ-4ngN8J7P1u8hVXxzNG98Jq2m4N6kSpqYEapqKOUpfkJM_qN9_tm6U0ZFx4eEfjPBNTjbMGWzTsxduQGPvNWwNbC8BOQcdFWQ2sUpAXPkzBam9HXS7ZcDQvqP3n2QwNSytO6qEM_P3J052X8cTD2jZxWq8UCxaBTC93Op2APJoJ1sABgI6RdGHrXIgz8Oll_15ctjDaZ7HnZ_lMDb1vk8LKJqI4d33ndt0LMYe_gBPxZLGYjLuDYcdhCMHJ3oDhbT7Q3YCbUUeG8G3rdrAyKjFXBsdO5vr7ubq9aXN1GfdobjTr2TsB03nm95cGPfA9_amcj8zn4Yz8hFNO1CSVMxLkIyqMnBJp4Nb82s-nw5CkrP2Lv2QJWg7M5KHG5Ku8XDRibq_Z6rGY6pKiZHxS8Pnq_rvs1-Gcpn9c7BFQLp4e2qxWTsff6dmA6cZhFSZTxtelI1-fO0TUejMVndQ2r4dVw9D1wWlZLsUd-Dx1mz3kOgtQXcRQ_-hRfw-J9u_F9Lqaz7z4S37PpfCK6p-bvI_33px97OIuBJQ3LNEl4FDz-fGd4_GAM9EalBVguwITBBHD70Zc1zhCo48VbbwmfB3GYz7pmaL48LoIUrNajz9ee6c0Da1SPPGTwV2mBpY3Bz5aM3wwd6axImSjyDyIQ-GzhdewODxdb9r4_zBqcWwaWzQOHvHOM3yegO4d0osjKuAb3bN0ggZiDVNUNzLQ5yBxs_8aQIcwrVpc8eshz1_025nXy68YwyFHeQzzjtTNYrmbBR_D2yztvsWqXzZDfViYlit1DpqbFC8Ipr5rMwD4dE2ANiFeQpjVPivghc4OjCkKCcgHSx9oZ6OmFOYoQQF54IEoc3DtHq4_nd9ceCNzQUS1icPFTlqxN7U8opn_79__TCP7f_v3_8qYCFMMeeRr63oBUhQFYDD-sHj6H16tFq49rM2lAakCiZnC-Lofc6ziu0-yeM3vS07X4zKUkR97aRsCsJg34P_BL2DI2gcjU6hWw8tfXA-KTFTGo0zh-hPUBdQQKcgk7gIevW0Iccjf2PmPS7agqAf4Htwqqg59qmP8tnNJqNrCErIZAOqrZB15CHZ24a7j-0SENL4oiqLJwbYqv38-0wYM5egvWTPZI-D95278yINxRkSdpXpYPeTA4cw3EShA5_WFVXkgX7XMwx3z2vn36h9eff6a0JrqNjQw6ZSYFH_BOTIa2rfDzGsL8h0zty9VyY26zRQPePZvAt9-rqdkAXY879l4uB53-sq6KKKjYQ6aGwm7WAibARTVhKs70OFuyC7AwSxWoS_27WFXo6HQ4t6Gp5VFRVzkLHjK1r4xHUbHFooGQD2ZQTVYcswTtrB0tMFxa4Cm1yUXpgMEpfT-YKfCLpOTxRpzaVJ6UE_24A0LizW8MZnHiNKoT8ZDnOm4Bm3Qzr1vNcS1RSclxrse3y-nkWkq5_Bl-1Hm9bkiQclZWEB09ZGqH6PUJW7XV7Wg-Ya2cqFXuAzrJ98Hs5KH_kLm9vm2MHyW_OHK_6H3-zVdazL16waYCMz5wPL3nn38NEjcUcYQpC4uab2r0G7FEu6AysIf4A_e_MCBHVV0FVcTYA57qiJHOIvd2zcgLuEoyydJJddUswLhN58qR37UeifDLKBYPWQ_QKnwGXr7cjtVyNsXtAqfvzsMKgJDKEkRrOl92OgyrFo36x5Dt5XmUZ6V_PzvYvGMglVMQuX1O2_3PDuxPwusgYlV92rNesOq234Nb1nnoYqvzM-SgRWUSiqiMTnvqCDxifRSvL716tVxhpsWIhJEE6-mgmRLTUuA4jhWYQCi87tKHaZHlLDxtUh48bwpqnY-HIpq88EUQxCe_d3PTgmDx_rXBGsr_R9fvbTOfrz1_4xWrNI3DIMhOe_7XEMRVt2jCahDqPoZezjwYH5yDirV4FODoYARfzeaNQNW_wCrUQPIzL4qEJScKw-9A9zEUuxGG8br2NoKdx0T0HIIoCLGGRLEOcz8JxIkHYNCOVBOhigU2PBiNZqsl6CX1ywE7UsKBykO2HsE8R52C-r6ezN7vUQH3PzugAjI_5ZVg0WnPGlwBBgYU9mend18PLEEUCT9hpy7BHyGwvh6B14W1VTgwICGglrFYImuk_7YCH7EBkeWwIF65wIkKncyph4xGkaVFFax7ip-LxQ2oFl0lle4MZtnwMOpDsGezDhpgYAfjrA4DHt0rcMHcJxNhz-GslpqwA5_Blq32hUYHjjFkX5Ky4kUuHnVq1tfGSATCgJmn1I4shctqFKikKS7q2PsXIeaekO62DGKGwoA6LvLKDx51roPnQ85Repj2jIwYGE-ByuLq6sotGm0cEA7Oi8-z4lGnKyOs2XSKMtjissGyqsKFqmrqIcbes1YHWlgQhW-Ug85nFufg1Pjx-Zb2nuqxy2o_P5TcS7JEhI8sCM_AJDYtKP_Om2JRuxS9Bd0y5LUDcbgeyvYFLOeifNy5_ulWtNKVs_VtKamYigeRALXZ--QjEBWG2qubrRaV6C6GLL3vV6DSs3MfMKNYXVMsTxcY5CExiOMq4qn_-EvLpG8CXhPIAeZ3pmLJMIEhVb9JcHw0Z52McToPNETTDiZ9QxCCKk7q8y1tw9GE1hAuy2mO8I3k-RrOfJYZWPUqyh93omYymEzo3svsi_zN8s7727__D-_qyVIH1dLCm6N19UT-ddYOwkdCViRJdU8Mvl4tYIS9lt352ICRhL0TPLkXDh3yhNH92sDlRnXeKcs__-zl-KodSXTCnFVDoRAr8zS8FxUeMiFPOmcYIhif6hNHyynBhpAArDTu73xVglb25mKBNZMhJRf6WVCX2SkLBGHRZNI9haV5PmGYj3sOInkh__s9_N9q0c0WF3J9vmo8BQLD-bvZ8c31qTMeBeEp61OKbjkSdY1JxRqEvmTVW-92NnvbDQWOKRyaNMv5CQvwwoS-9_fhEoRgeTuCb2ppWdpq6EymgAcWIA_9OipYefR8vl7C4VPVQJSAb83pZrIijXP5_ruP4JfdUwv3-xjRCRDCf39_fb67MFDCJzrof1NBrKngfPIvBh4o3uRF5rNUJAnnUc7LooxZEaYyugDfUY5plsdYC5De6u181kjVo-rnCvNn_oWQv-8QJonpDmcEFzrpDCJBmSeiKrtZvXxTg1yKxXzRaPBmVwaXFc_qKs5SngVJnYosTIskrvIq8NNQsCziwq9yAX9MavxoWTJeZwWL44Azv5IFOswyShCm2q3LtPgBFhpRkqEfpiM_G4Xpaz-7jKPLMP2V71_6qAr1imNSo-A8DkQMAtL_9i-PgdyU0qaAlbesu8VIpw5SlsZ5UsmIXY7hYC21ID4cRInJRvwb_P59w5e38Jc8h3_ciubmdqn_BWP--un8N1uOrZ5tnmRpHeVBWviRma2DwdSz3Q-t1MPxIkWfP8tLiXORwzloyw3Q3vEgSnToR60qqEhA4eKqlRZTFZ66_uCabRzvfvsgAy3ps9qvS2Gm60Ax9XQfgrCsdE1TTrG7ZRAvX7XoT9WyVgXvOpW2ZtWtVFa2QrzvAn2qajGDBarkFxWet7vwvp6AMr4Ab0xgObWTVuGq7WZTgUDzX6CfNp0t7sYyxITFFd9XAtwWmNx79OpwUjIdr1Je4N_BOmIdCD__iTcFb--q7bGattahA9g1qKSC2zF8K5jvhVJGGrqFiWlwka5am_PUEOQLWTGQ5V7WyTdaT3aobIh6V1xwlSpfiInUvrDVs7W9RddUTGpwkbqZWmMDbcctUiLRSwS--YA0gNhzloJWyiXoUkqDA4M1RbcHoFvtwuB0rlozV8anzRIXpcH3g4lb0fVspQXhFwzO-50prVTgcE9xKJzKVYvVBFgjhUCAVQbdgkIknYXutplfeDNVcpiIpc3JDixGUhdVmdVpGgvWqzGLwNWL8RBgrQenZjVRnxzYlNQPQpGzsKgKMw8Hd2sU1DCkVo_FWA5OWpgFrLbv5KBsN7XT0QBafxyOfQjk57dsHEBYopyKbk2fWStu9EZ3KccH31dKLe7z3Z_B9dyIOK5aDHhNER43tHPqdkZoLjycvFiAgixnIPlKyhqhT5SWQXmwnPMJX5lNFOiO4amWMx5pTJ70VGA7G6VBNIDU1DGUarmbra7aVqDQgXL7XkmzuFkot6lTjtfARuc153mVg50tMrvRPei43-hBOLEezE-TIAc3SoTcGmEHYby500djhxnixFopBaoKi4ZoPll1DjxKwwJ1smpshorkKHhwUPPrnCC_3L00FY_rwi-jjFXWTDkAZf02D4Mem4UYjfSuHg143BVWG4WShlHBSwZa1mpXB9RsXuIhcGWc2VNY6qaGCGb8r2BfriWuopGx9nQOXjRMVuauTZ3_Wk79-gJ-kKHX9QUMV8mI61qqzGuYBYxi87lGZy_ElMEkwS1ZwvpggHiIw5FXtR8WkXQgrQbqkdRmER6AkUanY47lrSV6Gtf-GAa4xuxMJW5nEw7TbLAaDK4jeuraS6kZnHaz5kNGgddFifgBcNTN9B3kdX9GHwiZNu5ZkEcRT0KRZpVVCT2K2hrk0-HPagvhXLdiBd7CRNrR6Qo8tDuZ824lGsb4d9KRQCgym1z09dp3gfe3__bfvXeh9kdB5GT6DEtrVy0ecxcwac6Ss8fXFyrXJus_1x3MA_QmJqquJVSgRRQqbKV2JFBWmym-z7VS6Nfv5GJfq92HrW_AXMBsURfDVotGgjZlskrmP69aR0O1s8U6ekq7mgNCUCbgE-SsDuLKyrCDFTe78gCQN05MBWRDSjFhMatjlpW5VYoOBPy-UjwFuy08GxbuUW6FAIMTh5z7qV0TB97tSOqpuOxGYzhAEhzcmPQ-dVACK4huwWTGOCou8b2o4IR5GJej5hwbw4kWWinRDp8Eb3Z_dUCwOuWH2vIJooDh_8T3sHF4JlQ1XX9emXjYTTg-qr7eNRhzYDlTLKtb12kYECwG1j8KeZJVoV1EB3PuuHqHIsj1wHUdpkXJc5En1vQ4oPKtUelxEPGpVLvKZQBPa0Bsw7Su8iqLQedbFeqgyNfF9jRMeDeGT8FW8DWjvz1FPhrdisl8j3RHRZiXlc-TKg16H9yiy_sTfzJWXJ0E89FfwHThM8pUmxOLMjRlGt1hvACJ8vjWJlC_-0j_9PGAmPE0j0QRBQx8Eesb9oD0XsyOBJabxQIfBxRBnZXcGi0Ha24W6wjMuEksRVVRVqhRAjtvB0a-LjmPBgc32taH4I9HdR7lNrHjIMQdBXcq0hvCV4xdbhswqi0qEo2hVShk6fxofCEexbH3tVDpgd50ySMq7Ugfhs4WKkOi8gi9PjOobilh0ppK51-n-42Th-d9BjE-Tr2TGhainEVv1C_W0jPSX3Szc9IdwJc0prm2buNSFbFlNH7VSm36VI2K0dknWHeTi-jA95r2HZs0HNbS9avwpVUiQg4yQifCySzIgM-cq9FEYD5kMpu9BYunSxyg21v2jjUTHG7g2GQ88pMkiquyN3EOBP8Q8dsLpXc-qvbkgE9OZjfrHxuUY_BeITKsgzQL-iikR-nbw38E5t64AFFWZVEQJXV_7h0Yfs-QPBlUD59ezFY3tyBm8HC2uFPeaoNoTVPLUi7hfDWZyMAS4qBu7F2D5HWOfXiqJPPaSiO7ajuBG77spdKI77oIqfrHJxCIgIBNRyjS0sQ_7e7aCs88mIB6BX40SqQDeeF4eKz8Sn_AleABuUtZFNRC1JVf2KSNwyHQ6_oQRoBZZRsQyOScVgUWq4nuNLwGOlxajuWRd3KX-H2Iapj6g1Q7Kl19s2rwq1jpx0OtwghtIJXn7xSTdc1lKCUmeBZxnhc8TMyKONQFRxefSkTAdYLASSxGoKqx7HbVSkezquS_EJQGIYexz5jBBX2DIxkkjtJI3wS99lLpSpWWhHWxeUlPIWCWQvuzaNDfQ6Qq4DijwYc9aGYqq4IxrET2DCipKhUQLyZxFttyhkOdMJ7eA4gQsHegYg5uqnJtstiebqLi_fHVZ8oc6M1BZwcs0qxFXLbzwFkpP46dPTrXZ_pn1eHl2sE3TdkdeOYSgYGWDnbPCSbw-RDwisWat642SKJ8ZiVKPR5cjTxsEfkD-w2HwAQUuBY2ppAOWHuH-a-bITGN6iTMeQGC2fsrPVdkPXN7EPPDuPOgU6O8jnIWBX2RyZJBNt35o6kdoDIVOOta55ikhlQyc42nZ9Tvx6iR0M2lfQKmBFTM66nqoPeRfgk4FrhINws2v-0uwOw3Elwjpnhe8KPev61m8vTAyFgaYrIqoEYBnaZkVoCDq9R83dwYgDUe3Y_HVy0KloXqaJm1NZ7rX-NEfnP9ietAODpCSb_dZJBzNp_DAZQS8_Rdy508269kek2qEj13JTPwkKdYivrN9VAeqRI5ou3AZlrRcDgzR7iyOxkwe0B397-36-NdC8tzO1tuPmg0QgSBPoGjkdJoOn1gkFvvb--8qyeyPCKrVq4HLN57cNTnQp5cUHLLqye7JqESPFvmPJyTqCBwTljAq8C67A75py9nnUzlsel9t9KDSkPr_DshPbhpA2EheC4tHyFk2JQnVNbA-DSvBBy8p9-s4NCsmgkHCceJwKljbbNs_gxK-sITHH2Q7sLMYN7MBZpLzJBIC3qnQMmO36ZMHS4-OgAwN5wyF9KXx6Ky9qTWKygScuUAtjBggFhG-lTV7KaF6XgYYUuP29R7ZfjQq93e8M2mmPWphiqPQZ7yijEW-HEfM_ZkqHsh6QHcJmMOMVOacwjc49Kq4J7utKkpj2Yvae1ky7tXrRFnT7bOgn2fCPUlXfKVHpQMf-RXlCbbVgRGP4GD66j8kr5-3QOg1NlDtTtpFPp3qkwrTB_ETfoxsiotXY4b9O2W-iAuV_Ac-3K8qeuB7fGzys9EwlmQiD5osNws49o_gGo1m-BvEJsKwoZQAHCgF3K-YAXgVaXIK4g4VnTA9q8js9RrdrKoBNLKpZutIAu6ZAC6hS1vO1v4tzVnXVFX3v6F9oRwdWGskSbzuJbxpXyCrG2qIiMeI3Rl3-Mxh7Pe9QwnfTLUQcItUuV6lelmWLlxuqpdf7IW7t6sUCDBFQQTPNMxgwRywb7CYoBqHXt_UD3SPJX1kX6UMvaGcwRaDTx1eHbVpy5lJKCNlc1xomrB6V3ISqA0fhAW67Zs8EK3iAHRXq8NlaSzKuUJx_hFZ33BIVkK8yRjMcTNQdXnIi2brj_qBzDkTEqxKDGeTcI48K149qQ5PeSxRDhjqoMIfKs6yXLfBhsON04P_hC-m3ZAJO7zWqpUGMJ-BawSBp1KRm2aREnrJ2s1sd6R2YIKNCnmMmO-n7Ikrm0SwyHV6bcZJMqZsDQuUh4yhjVla1177ly_Lify4cyEeVyyMKz8qrJG3KHIGVjjA2hvWKXG4v4rMQLTBTEvyr4doUMwZGfKWT3_Z7m29OjwyZrBHIV2KUboG4CFnygjgGbB4n2McpfQTjTqiC3wXn6qfdqZUksj9Wupxi19BqYwZEWZCMIqyesiCftyYc_c02t1KhvP7HsABjWpKsTCmIc4BL1DXNd9pDvkgsjP7E9nRVUUxVGUlHkV9akAS8zrtckBZDujoJIgTvwEhu19EYd_d8gL7uXUbbrX66ux37PW6Ds-gmjblOyMLel_Zz7t9Nccyf6a3v3umvajCLUFnx2zGos5ZpCtu371BP4s0xid93Q5nT9VP0ucwT2PXyaZBJuCWZ51ynR1Uyy9mcBDuf57Pf7D85o8y9PQL2KW9UUNh56od-0hlEOtvJzMOhhc2LvVhOtE31ww0CNfyyKzgoOh8u7RhesFNnyqhTIpFKOTB9iCQRw4-XVQlqGf-ZHfwyocHmR_DE6lMRp_Gs5BjMbP5zYX6TAbnezx6bREo2fKKCjissyS0LruDlPxfibrBJphK1OWc1UkYN3bq9bZIPha3Vj8JaaZQciNhcUAp9OlFZkbhkBLhgGqwIBp6bYGv2I5VAjNizqIszLJGbd75tAbD9Ez-7mJcCKVRTR_LmelUjF4avecqToTZZn7ZVj3EEiH0ejmWU-kIwrPoTbAsqkgymyI_L5Myyl_ucRSFIywwi92Ap6Ix8WuNTyhXiqkB5rbbjZ5h-EZmGYJgFIuFJhzCB911ci68Oj7KqXd3cMI4kirFvTmwE7CoaszP0nQkbIWo2dTnmAxNqmQ23Z-y6bv2G4jC7vtitHcdt0UZEEfYp2vUWf5YK3tvMWwnBWR7ycQk5dhav2Wnt-p1-8h5ExVFLKZMVNiwFgZTjdqnw7Gk5mKa00cuTajqaXWCNAN1iWESQhWwQBaKGSPAbUijNQQLiUw4HqN6aggfvBkdOJnCEOB1xQLCUFS39LVKfCg2xtwoBs5K5WN0nMcsAgQEgXcj0TtINUcHqrtpXI6iXTtkKzmYEbQ4EOEg-uA08ckkqH4XchF7sNi3A_VFP5CKw25hdxWbgeOWx1GUZRmPMkdRHRPWz1ccQ5xTuUxQvXAFtXtiDlny_6y3C_ZWZTngWCpqJJesnvKqrsLJ_JNYQTcCZssv-gzhvzjCyezsSOJh9UaBv4OiN60aTFDUJksw1XrsJmGIoIwgDgwyuM8tOUIh-t6UGH8OKKqyRomvqiTuARvxLoIDnfVPPjBxFNvyjC4FB4CSGV42C-rzAfZnM1CqFSXKYUplf7OJG_gTd-zTgs8m0ieC2yYNHf6z1gafS-zsjcmpygTzS367jKZZh8mwUDjQWpTKdIqrX1uhc8hyjr1p0EGbF_eF36Rp9yv7WI7pFgnD3Iy2xXhcZcKVi65P-jZLCVDyCDMVcG1hzLfh5qrHMqOav-lU9o3iZQRZhDRIdbZv7XU1u6shMjSKolCH5yjHhDWE3JtGuV0pq2tlw5n0-IqLfygKvyih3M4TNx-V06m2LaYl8XU_mQ1kFcqozQoax7yIO7zSj0D1y7IcdRaCy6N_LBgQZEnPRWnZ9valzydRitDhYEsVJAXfllnYV0Gva_e82v7JnInE2ex5CinXIpb9q5BkAVWkgSoYHRi79SINtx5ZvKY3wR2j_TYX3356vWz33724s2zV69f_u7Z89dvvv7qxXN8FqgaOTk0L1hnB1uDIe2kmcrcL4QD35qk62-xWsWQNCPj1I3nduZhr15-8-z5f33z7ItP33z68uvnn3359R9fqRfboAL_gAu65WIRTD3fv1ZEXlIiExz3f7_9GhJ1y4rMZOg_vGpAfS74j31DiXS2T7ug5KD7D6YzjpUF_uBO9c5A7QoOEu7Nt98-kfQL-J0kdj357rtNfrfKAu2a-ZbRFZf7j3Muc0uqMKZoHJ18OaesgDwyT5PITKFGwxDkhNZ4ZYaMtuvlD5qKObPo6PY8t_uEr-XMW6OowFTGajHMAv_lCcRTuEyo1XXGfysJToUXZgXQO4DnvXPpdEjaPphED55lUZZFxpKUxUUWpVUcxXVY2Ld12fEuM9xlzP_l71keD-8qYFn19lmX4Q_bafP7egg8TqOACJyrPCgKxvIaTCcPWc2CuGICk-51mBR1HfLQj1kaszypyqwsBVjdpBZhWkrne8cr3W8VEASXcXbp51taBYQ5yAzMhFoFUKsAahVArQKoVcA_ZquALC3rmIdlmUUHtgoID2sV8HKpCOSO3nLq7Uf3BPDutQRYL6Od0BPAwjZ0EeGBPQE81RIAk2nUE4B6AlBPgC2M0DiOkjQr68w_tCdASD0BqCcA9QSgngDUE4B6AlBPAOoJQD0BqCcA9QSgngDUE4B6AlBPAOoJQD0BqCcA9QSgngDUE4B6AlBPAOoJQD0BqCcA9QSgngDUE4B6AlBPAOoJQD0BqCcA9QSgngDUE4B6AlBPAOoJQD0BqCcA9QSgngDUE4B6AlBPAOoJ8BPtCeAQRHvu9Brh9HAetsPefPBYDvfvME73FqMyyDM_YKyNSTlMmocN5NA5-oGeSwq-ixpwchhHvbBD33jo8BtTd0gIDx3bulp2fXsw_6PP2wEf92P_QeN2HCLxsWvtoI5PHndT0HqwZD-oQt15MrNuwHbHztbBSp4-sGpW4A7rQAVPH3ZT1PrifD-qLM43HbjN0k2TXir8w6nUH7UgTqH-UZ6xZSttCfvDPMBJjfYP-Fylbtbzo8eujZMJfcDIm-06-uzeYw7rJHMec1gnmHFEewbRLLh5i2OX1AlmjhzNeotmKIcQ3g_Vj6CLq9hTRCXWHsgYH1r5nhJ-6Ez2cMbtyD01-YiRB7nL1h70ROVDh34Ik_nY9jXDM3kId3XwZFpm38EzeQj1b8AVcChpx8jUoZw1-8Y9Qe0EKTiawTbkPPf0tCPX_jT-2sDaO6yzQ6fyEFraUBTQM6-OXJRHo2aZqTg8rIMX5QFErYFFcVgIx8zkVJrCwEwc0P_Bp-cBrIDBcNFC3o80QQdh4vto2QLgT1AXRyPkh4SgB3I_5snYifQeOBkO3PlweTwdDz1kv3qI3xFScAAG0HrEPeDv0Acciwi0kVoP_zv0UQ_BBw44mg5079CZDGL7rNz0QL4j3vBEpJ9VFD2s79CHPgT3N-Q196C5Q2dyKqrOPNKB0D2K0tiHsRtQGg5-7oijegDAztrrHk33KO-6F2438LIORuzQuTwERDaUjejxWkcs-6mALhtr9ZiAQ5_6ENDA0KHrS_iPIhX7a_xDfnZfpD9qWU6s4g8lOfpK-qMsy5GldqsU-rr6wdN4cOF9SFr6auvhlu_0cuxQ9rovtx5hK0-uxw55A33B9fA1Oa4iazNcffn18Jc-vT478NJOGfZgr-EBddonBzXFdkp3OztRvxIqmlstNNpOgr0kVR6EEOuvJk9yYVZDCYQCpDEdB-4q8531uU5J8KzPPaT5-Id4rlNtPOtzneLkWZ_rVC3P-lynonne_e2rnWd9rlMJPe8695XS865zX0w963OdWutZn-sUY8-7v3259rx2oS_hnlmubGX3vPq5L_ie9337cvB57W9fLz6vPeoLyuc9R33F-azPdWrTZ32uU8je8Kc_5Pb2VeuzPrYvaZ_zsU65-5yP3bwt5zyP7QvZ53ysU7Q-69v2RexzPtapWJ_33Nrq9Dkf65Siz_lYp-x8zsc6NeZzPtYpKJ91b_vq8VnVRV9NPuve9qXjs6qLvkx8XuVoa8LnfKxTKT7nY52q8Vl1cl8iPqtI9RXks6qLvoZ81kXuC8bnfKxTND6vBbIF4rPa275sfNZz21eIz6ql-nLwWYORvh581gPUF3_P-ti-zHvOxzo13bOe276Ge9ZF7ku1Z5Xkvi571rfti7DnfKxTkD1rVNBXXz_4Y7dduYtkCNXrvK6bSqJu1oq56tujull0qlu3YB3iGLFbccXao67bLUJW-1VeB7DBVRZVFatEwSt_13W79nbV_dftEtWTqJ5E9SSqJ1E9iepJVE-iehLVk6ieRPUkqidRPYnqSVRPonoS1ZOonkT1JKonUT2J6klUT6J6EtWTqJ5E9Tw_1fNeRRDURlGWRcaSlMVFFkFkGsV1iOkS9Khld1ubQ7wMows7x8vY_-HClBzdWiE-Rbml-Ize7Tc_vtFazkxi8kaERR3k4FD4ZZwzFnDwrKK6Qkexm9XLN04Td_mNrgwu87AI4kLkZVrWceEncRTyrC7DJPNFnrEoSEVRRH5VpEHGgigPeMZzlpVhmSVZXfiHviB-4knoh-nIz0Zh-joILpPsMoh_5fuXPo7Sr0CWcD-qi-iJuy5_eYzWver6WFlvNV2z6yBlaZwnlfTCVENpUWVZUDoXdvx6Du4jOLr_6epJJfA-r6snv0Fr8utmeuN1iwp-z7pOLLunk9nNbNy9uwF9xiZL-L0TbuLf4PfvG768hb_kOfzjVjQ3t0v9Lxjz10_nvxns457WsAdp4ds7ruA9i6IQ7o153lqNd-C2vCxkCRN1KZjf3x5s68-bd2LeyOtz3auKPPemIqbuXpSH3PS9l1peXdre6SujzRWkoPDxFKnrLH_vXHg40AA8YlEd-kUJlsC2W3fK3M7lTjCeHHguZnN9j7xMqOirCcXmJUT2fmoTomHX7Urngt7L25362x31jRxdhS2f5b2QslE9JnbxHsupEEt1zbHCL0xhLYYa9Nec51UOYltk_QXRtuLeN-gfTKXbexV9Py_9MA5S2wneKbnrwV6pm5E6kyiNLnAP1Hy_wGJEkP9q4KqHisdw-ssoY5W9ZSsrA9CA1eadRdjV3ySiRyO8tnPExTvHRxlOWI9GWg0cndfed1VYGCcpaIic1fbmQgdTYF5CDnxt3qDr77n0wM2bL_VlBPqmo2vnZuin4Ak3NdhaeTPa9dj7I97ucm2nKJ2A6wvvupKm_1rebXoNz7iWkYXJ2_a3aes-4wOSxBOexSISKRehvZerRzc41-ANlfF3CxcLC4gc_KIKWX_lSg9vMMK1kncsdfY-qE5dn2FVB7ydqzlQHQwJWyjA7WA8LEP7UAf3cMQl2dszzT_a3X3qpiWbEjrD7XhpHsdRFookz63Bc2Aezk1eesWcRLlKnZnJ2pfW-St9y9dtA95ef0Ea3iVgFP6BN-Kp8LFTEfYWY3PVnnAvnp9HZVyKJI0je9QdCEp_LrZDRXYfiKQALwNc3JRlVnU7GBRzIYTQtsXeN6cW5LW8DLpq5o26MUpf6NKCy-LdwWKt1Wz0VQEXVy1e2y5TXeq2koGjA8GBnyRRXJWpva-C1eAaRTU79EqeFm8OXh5yEJqpvAHvgE-CM3TMnY5RAmonq8OaBf210xaT49w2uAPksnv_ojQDvz0Dfdnfg-ugcvTQf_VeQVAivL-qe8eNQ_PXq_avo9FI_g9-NE__q9xXWXp0UwBTdf-PuuXd3reOGlLdOgcqaSUvZZL3V6jRvS_7a0n0uOa1dH5elb3xiOjo1bhef92GEDJikeQhmL4wEpnVqA5oyIjFjvtztPejK9xrV-nYcFthZ9YuRQLzLdQ128pXUjeh23t7SnXTiMqqOXZJvit86R344HiZ99C9t74f8yTL8rg64Pb4QcDPgMSA9eNlxiFI8E-7Sr6_QX7H3fFS00mnElbmqtU3x9uLg3fdE69qhM_VxayY09BXvnvOje9Xrb7y3bq9e658r-I0qwNWC5_xD3Hlu74oWb8d3vAOFmPzGnhv-Bb4r4VQb_ftXJePjDjtvZ9GytuaJC8wKTTkZIHqYUkmcnDahy4_9XbBnQbMSclZHUNIB__dfdnprgtMx97vEN98Ie_M3H6HqbnB1L25FK-2lIpbmlxzr6YWyZ_FBaZhxKO6Snye5P7uC0zVraHM3E4KiyPvHNU3YSqFheAAeTuTvOi7v_nQo9tBP_TtoEGVxhCpMVC22e7bQb-GmH5klZstxdy_1HPsfamCK-WS9pd1KtsGU3Ev2_yk32m8xlqmEe_d4jl0KXMRxUGWhfm--_dc5OFuHVEnWZXlYcgrUQ1dwPft7xqItEFdoudizalJsnIxnX33kfieodIDK6__PtJ_d9KgeJXet5-u5UunbL6RLZUfe9HfX3bMhWTyu1-ta24Qob26W37vmRuLw3d0mr2f2f1MMl1A9jO5gGwr5nbbWIzz82BvK3AJgjpNT5jR69umfes9D796Jj2SPr5Fl_rS8YgvTEimIaUghY_bjHJmCFrwCpXMlS5W3XI0YXfy9tiluEF_XTru8lLKYxtPPp9BJFCZjMfGgOiuWHXVQ3VUWLOvLZFZ16HXAU22msiNHrnb6qmDLuPXKXxuvGtnD3iU3EYGftnsRt_lKr6fg5nDe-jlYtpopwL_lS130drMPbIyNbTEC0lv8F7ejSV7f4tREsKgMfjCTyv1Yt9ZJsAdDtxRhDeIu7MQou8kCHL4sU5KAcZL3tG9lfBmSzh_v4Q3Ui27VcvhdEhbG1Rzugwv3CrhD9vLfmcpfBZlHLIq8uO4COF_fsSCtKrLMK3ryIfgq66qOvV98NiLNE6LIs3LVIgkD2L05dTY-15uo-gZXvrxZZBsKXpWPA3yICqp6PmBi56iQkXGSuEPFT1_-UvMtElN7Smzh-cGrMaymat_P3s5_uUvB65jziOR1jwqY5bsLlTe4y603mwu2gsVeY1aBQjXl7ZvFFLXUuNX7Voh1iTEd5dYMS-nSDM2K2WST2osiYQ_IN_kLRuV00Obg-pkIA5K6qIqM1Bhseivb-71rF6Uh6hPx7QPFgOKOGM-hE-pPQCOdrVFkNOVJpYQICKZNktZR9a-C2yHglFL3ww_IkfHvBNMuWwmzRLT_HDoMGcn_ffutpnLZJdJTl21GmBL5WQqJ1M5mcrJVE6mcjKVk6mcTOVkKidTOZnKyVROpnIylZOpnEzlZCon_0TLyVkShyC94oRKxrf_4VtM_2iX57uPTIuVZnoz7m4bMeHduJk9hc88fee4mpie_vgxqj27KkfbC67Oi26vGT6T1DiY7YX3_KXyxFB5gS8mfbZVhyTft530KXQIv5AnWKZthiuhW-quci-4NTyz1pQ6FZW-T55Krxr8Fzw6OyqTjM_mS_sh5LXKfAOIDigcMzwY4JuV5SivFiCUGGi04Jmhdz9n1Vvz13LVTLh-66OKk2nFgyhNKlbmVRKIMitFnRci31WctKWW_cXJn6egHl7cvV_hCtwKV_DD9gLWWcp3cZWXPGNp5vsiroqqrqM8iURQBFmQBHEcBUXGw1xkIot9lvOgzAW8Qg4xfhUXdXbIy20p3wXF9vKd74eVYL6g8t0HLt-VccyiMiwSxT1VTm9_SvVwDzl8_affv38_ho_8ayc7d2ld5Xwc3AV40POX_TcOafTVPdWNjJ-axhnd06oZ300nT7EHm7g3iYcNqab4mTIpl94zeIlbMQrH_s41kXN4qo3QSH8BvzEqJyszuc9ePn_xxdcvPt697VRm_fHKrDzLkxSc-URE4Ycqs1rfgIqsVGSlIisVWanISkVWKrJSkZWKrFRkpSIrFVmpyEpFViqyUpGViqxUZP07LLIuVJEVU60fstDaiUn9BvPwi8evsh59zVq7mpYCF_Xbb59E2LU3GgcBLM63TwIcJAyffPfdj3MRmRP9nHyp18agjrV7wAVFmxdT9NbhMYd96E1F2wvUjowMsHWVi6XtxgJMvgpabEFaF3txP8ApYc1CNqeW9yxWqofteJeonPGpjhCd8amOlJ3xqY4QnvNdexn90E_dhkioThraZqvWn3EUBCFLi7SAaCuLK5HnAXitRVkE4c4LQW25eD8EgbQ4afE1LX44-mVLY-b0h-2ohfNgNuI6C9Oo5HBSoiLNOfdTwVhaZHBywjD2a78MUlakWVKDv8xrVrOEI7U8Soq0Dne_0gZSI7r0s-1IjbyuGffjlJAahNQgpAYhNQipQUiNY5AaIWauUubXQZkdgdQAH-xX99EaYUhoDUJr_CTQGn6YpSwH_9wPg71ojSERGcRsDH1xG3JjUBbPgN8Yej6hOAjFMYjiSLMojAoIIoss3IviGJK0rViOwS9sQXQMfZ5wHYTrIFwH4ToI1_EzwHUkEc84hCN-UtZ7cR1DVuEfAt1R-3kKMbif-2wvuuMI79VBR-xd4h8R6XGEf0t4j-PwHpmoIZQC_VH03j7hPQbwHvJTz3EuEiPR3nz30fMvv3j96uVv__j65Re_l8bh__m_4SPSLIPLCn__w7Mvfv_isy_NH_F0fPs1vNuiWYKp-frF8z--evn6v_ZfxeAHs0yzFts84wM-ffHmy9-9gQd9-sfnr4nb_wioE8dzdSpc2yOBkzj1zgN2F5knTGovmSPevO5XhQxSQ0AkYRLK3V1b6Tsg4VtIZDettK0zgoEYuHgj8MXNt8BfNZ29d5SlO4Gv4x5vE4RI30sae6nvZ3PcKHAfzLNBVrd49erBR9Wna98HzZPGIgnCsozyJE4gzkryzRWTiXHbqtxdGXTMhdA0d1PIttW0_YXsxxWMwwvwW0qG68z1viJ4lipoIqqgCEWWwXIkEBzFRRAHPMyStK55JEo_CfMkiyI_y8O6SMBFiosoLFhWiigJg3D3K21UQePLKLyMt92xGwS1z6uU7tilKihVQakKSlVQqoJSFZSqoFQFpSooVUGpCkpVUKqCnrkKKlhaZ3EMMWEWfNgq6FdWE-OcO5B6KfNczPGQgP1olpc4TrOw6yRrpGJ3lRQdb1fPPPOWgk2Vc84m3cx7zzBtDe4wpnbEvVkqT36KQcVihVntQY1_11bXNkMzuftExgdm664h_IJV726vnUov_ltpeJW-Qo1JhVsq3FLhlgq3VLilwi0VbqlwS4Xbf_TC7WNenutE9A9lkW6MzXMWRywv1sb-Rik91t7ZaPwXoJbulmKwSTdoheFvbtETZh5lXhVxKpXEg-dhlwYDKwiiwC2BHzBxrTWjgmF-9envLrwv67pxdOrFwFIVeSFqxsPHmOIhWa8FhJMtk_l29ULKIxrPBxixYZhxoSq1D54jxqLYRn4Js0MPDEapbO5UzUWnda5xrGtlK8HFhnM2sIwfpvXCIRelfypqbPXveqG6z_4zcy36V_2iw4_LWQVOv7oMHD8vFu8MiGG9biSze-Ndh3YPsKLRDpyNf0uxfC9ULeli82Eq1rIijbKsEs4KTQxLde8uA-eIb7824SVYG6mv5c0IECaN2E07wzyhFBJ3X-9dT--c2u1Dv4DI2mYS7JzNuTT1yvGuc7Z9UNwkGAGhItaCb54WXCXtvZl09njXWdn-nK8x4u10URDmf_8M2OgSS2RwIloOv8QcObhlLa6ektPjuzp8Jm-pkDsvZIyqBFFeOq-f_eyrl1ZpmY3ZBpcR38_xa47IS59aS5TJxz6VOVjtHmJoxlQwv3inPues7jqWHVSWUSlK9I4C0kRxVYQJRKgii1JRBSkLgziIN47s8PnE9zNbI-XVyJkLrbEQjf3QGjLdZLrJdH8g0304lO7-hSKxe6FI9MN2_NVZMGc8i6KE-RXjZeUnVVAVfloHcZLAPNI8Kv28qNMijvK8ztOCl6Ev0pSlYRkVBQTW_iEvt44-K177_mWSX_rRFvRZkvtZnCbUg4PQZ4Q-OyP6rExSkdR-xIKkOhR9JovGc_DtBz2aTSwUQskQb7OOVtsFVPMOwqldtcaB1TWnHVA1by9SDZP1u6FqOPWNwMLaddHCO8CS4D1msrp31ZaY2HVsqB5MfI_rJW2fhH6BTZQhjwGewyIvwQeXERqMskJ3HKZuIOj42V901jnvCEJHEDqC0BGEjiB0_9AQuhxCkCyIWcYZ-ylB6Jy8n-sTa3SLA6q7anea_m2gut7zsCZ4yu5wzmKB_7pq72cTewM7YZXOf6JaU2ZVzWjgYKY-q0sRgCNe24PjpC76g3l0AsKCIEEfl4kIkx4N4uQk7iddTsgseM0UlhtMxKK6hQ1BbeUu09ABrtK0EEEQFpUtpzrJiCMO8M6UAq_tGYJNmq-W9i_2K2MFRDhwfH2EtozvLNn2JwyetCoNWJ1XLI3SsEdC2aSHc9JOTV20l97Xf3g2CpNUQUhkNnAiIGq5BSFfVrfraegtjTy0z6OgZigMOq2L7hF8GL6xnIDzA1I0x5uD4ZALXO-KTSq861dwacnAk70nQlJraM8TIUjonir_miNsdCZvKF7MMNegs8YSJgi-Cg5mGYTKi3at71Xrvr_cRni7BWFnCTtL2FnCzhJ2lrCzhJ0l7CxhZwk7S9jZvy_srIhCEVSh8Iss_jlhZ_eCORyMix7RDvTVqy-_efHFsy-ev8AfX3_5_MvPCJN7Hkwuas0fG5B7u4IQugfkrlrMcLWH3uA1gJfp9YIMeqXKsDmzIWDDsYCYkx90FKbl5KcchUp54LvsuENrA624iY_jAt3NUtiq4nv0ji0Qzc2I7IErbhnbmBTr9lp91ImJ8sr3wBU3B4Wz43365fP_0kMD17I2MpcqvH9bNdVbsKKL5R6c4uYDhMJZ3nuIRP59-juFiuvV4nakoNH8ngoewe80-ef1rJPa7X511t6kFLfsXTNbjI-78CkRQVTwsAp5EoCaCMEZBxdK7LrwySJeDrjwiQ79T-3QHw4C3dKZK_5hO_TpLMAvv8brlDAXVEAMnXOW5EEq4iBMEhbCS0QwJquSJAyYD85qnXCWhVlY1TB-GQbV7lfagHull35xmeRb4F4ZnMO0SjjBvQjuRXAvgnsR3IvgXgT3IrgXwb0I7kVwL4J7_chwLx7EKd5Mm5VxdQjca188ufuI1hWL8pxziN3Y6bivNct9r9Qp8z2dKkRqeA54jxadpLXiZZ9w-fLL_wL7sJYRQQX3J7S99kUvrtq1vNUGx1Z-56tPf6d9r-1_lyulgQNDXkWWR1VapkHA6kcGoNlDB2_2_X0Mmv3jA1Fo2x9i93D3Ywa1gGBR5PtVzgSPd0PRfgfLjAk1MFxmh9fhZujEzlqUlubP-vhPBcOid72aaGHQsdwlut86wSZzKggrlApZetx3GhEwkeOifwX_RJkHh-AC9nu2lD-glbEiNFtickwLiZiWAqlkMAHesLH3SuCDDVv9f3_5lQNxk46-Lm-CklrCaIrjLv-C37k_VfnlscwlOsdH4Vw0DG8CwcbkEw_jDAOQ0HnDqVjCSVkyODhbgHYORs5A7TyLtBtfteBKeOBJyOE99SjdVR-Vmsx36iXWsQIeKY2d4wSDIxgcweAIBkcwOILBEQyOYHAEgyMYHMHgCAZHMDiCwf0dw-Ae0JfSKYw-uLnVYzbKKsK6rAJZWB8ea7PZEdYbT62UDswoZVFRgupZm9GfwCiYCpqNoqa4V4t9_bX2fHUAWpRWuV_FAXuUmTxzr73CSEzHCRAMS92-6F3oejaZzN7D8NKGwtINrRavyzCP60eZo-PjzcA8yC58sgcf_Mc4wOu0TRwTvHBwCQ9DGTrHYCem7pWoF3DAlOlfshtcHhAafP7mW8k61v2lHe86LjufqfslGn9Dm4NfgJ2eYekbE19zMZvrrIF8YKeKy53eTblXDEIVEHPQf_fbDzrnbEfTQ32_JtdFeHg_jNUh8GaqFrzeAXDt4HXrrSlNrV_Wwmc2ByGnMt511rbP6pnMbTKvU_EgDij1OE7t_YCUHbIvzvHa_vBPNdyUb46EDUSZd7Ng81slnpVy8tHEGHCJQE8bE8I9QBXE_N6-OOdn-yRMr1ANbxgKxPuOjBiRNgqnYao6-qTgwonvb9mqk-8yW6DbuFwof0dGjpiCwvfRdf2tmNGFOSKbLVXNjozMjvSgm81V3GixirICXsJC5qA3RK85ts9kESR5XNSs5ryKmc-CoMpqXu7Cl1qI3X58KdlTsqf_aPb0cPT2YJvD8IftsNbzQHlZmsGHeZRERZXmaYpF0TTNiyALeAjeesqzOgt5yIIsBm89iv20jPzAD4swZHl5yMttgHrzyzi_DIstoN6wTvMyLASBegnUS6BeLEeUZZ34sUjqmu0D9R7jagxCfMMStZhIwiDhHx7i-6y7ajed-W4Ono42JOg1u678hSwzYeEBDppYqNfqJMbIpCZVGQWrDp2YKuQnlvi1C97n_WA-XFSNLtg4ryRRwap0tmFqwCrgdlq8r9FDl-DAMQMs4BfqX-9Z75JKhMEM86fgLTRz1ShHggnxkzZgmC10vcSBAsrgy_qxQ1WynIchqG1QbbZ84XhBtqJzunOzB1Z9LPLZ2w58vmqPQj57BHz-iQOfg4KXUZCzOAl6e9s7w2759liP1jxBiCDMwC9hQW6f0Du5pgL0AE91sdTVtqa7RTm_aps-8IWVu72bzyQQFqu8qsYAExeLhoFGchQNuqT6R515V4VfEHp9Tsbep00twYn4yBkcTDwvshEY1lO5_aMMovHZUurlTLDw7ZUQHtagcBiqPoEt2-zhxcZdXOCO6gqO6dblXCSxZN1bGAexSobSoHGXRpQ7dfb7YwByISeJYo-hLDxRh4pYh4H4WEMZ5PgSbwDvawV4SHL8NIIzyuA_FnzuBAab9uho794J_IUqvV61tkCoRVuXZHVGQI5kUg492u2iTz-4WQcDf7XqU02rW0GY_07YFUaXAwUHRRHFxoP36FQiQkPIWWuONUywv9lDIW7VSTHqEbFSBvhm68gGKiUf14FXYrr42fefLYi8QOQFIi8QeYHIC0ReIPICkReIvEDkBSIvEHmByAtEXiDyApEXiLxA5AUiLxB5gcgLRF4g8gKRFz4keWE7HeHD0Q46ManfIGhg8ficg7wuYxZk1RqW7TUYShdJ0XrL9zNPnYB90L993x3A_vE0qEWaFI8zl69lZVSqGCw3gsnv85sWhKvcdrwu6M6GNDD-EHiThYkIgkeapLZb07e8WTiqfdS3m_X-43_0Kr71bwNdQvM0zIqMs8eZ5X_49quN8PxCh93KvcaQWiXovvtIQ8_0NIdwlGlVRDxIH2eSr5TplLWl9b55KgBA315teLM0QQZ-BN3_oZvcU_CCmETfPd5-D1l1jC88VfW9uVv3TwY2PCqKOk-r-gNsuJyQU9fdvs8gqk9lnWEIRJ2lQVjE-aMdcFuhsGcXY1-s6q_hiMbep3DsJzMGi_nttVzbgVkKhJlFYfQ4s5SJxBWmFHZfbwfzQR8KhLOViAeTch2YZCTKGlYzeFSxBPM58UaffekZ_CCEoWMFUkSfXuds7-MVB6SSJWHO0iL_AFKpErT30vomfb4pogNLGQdxUano4hEm-Xom3TX4oHBqbyOd-kFv8cJD9uNaXKQt05DZ4XUapKw-mxqyVUhHFanAZqg5tc-isE78RzrgKknhfWszDRvet_a7Nx3wgaV0fPx-km7IsJPJof3Craw1x5Fae6EdDs7Ozzj-xc7PONZ952cc4zowH2vbdn7GMSw7P-Po9Z2fcbTq7mf1Sm3nZxyVsvMzzonevc79gdr5GUecd-9FL0335WYrLUuOoJCz72cmqnTcPTS0kpw20lWu55-9NGJ-HLNKREEhkjASPA9EVFaCVzX3I76LWWV5DvuZVRQ1UNRAUQNFDRQ1UNRAUQNFDRQ1HBI1HM58v09fDdb4q8EP2-mpZyHniqLwc5htFpYFC6IgE3HCyyoL6jRMclaJgIm4SPIgqvyE5fCEIq3KPEsikZYiiA96uzV2buS_DqPLJLn0gy3s3DQvInhOQOxcYucSO5fYucTOJXYusXOJnUvsXGLnEjuX2LnEzv05sXOTqqx5IYqk7AXAKUb00nRCQcGsWsXBVeYlBPtlL2O2xmDgkQ-oE_SmyiDbxxInKQ8pEhwYV8QKm7gw7IRS1NKHBb9GMR42KZ2yK2T3CQ4oM-3XUuUgy3BllYj-qDRRS8sWmczaQQ5xkfG6EqKsY7v0Tllj_UicVpoADYWsBrCVS3Oq4J-ju4OO2GlpyPvhHIJWn-5Gc65l2A-jMW1Pyu-mMR38eayerH14UBlEeSyiKBJBVFqN5tR79PY9pGZjc_nChJMyZt0tUUUUiMQvaiF699Wp7lhtfnqFBh3rZXWrv4w8DoctiQ7RgLxHdR7FRZggfbPXA7asczjwfKA0sxvUffjG1oHIEuSXwPHsSWS2rrNtY4-szcBZgy-M1If37GnJUz8Du5mUqSV3OQWcXnueXoTBVbldTifXQ7DrtU9-rILSVQlx5RLr7Q066uDDXDvLfK2o6E7HBfBR3w05mVEE4pGEZZ6mFo_ulIH0uz6klGOc_v3sy5r5JZzvoghjG8g41Z51aT2LqlwjWJ_7mT9Jcjg4EWEUp5xBcGKJj32ta9tJPbJeZY4tTnvkTG74zIowKjMR-eBc2TPrlLdMGuEBJSoZj6jTrinqMrhplSekhgMdr90heVqN-cS_reacOZH9ELUqTIsoDHlY9mRDpwh2uNLeXciCaaxAP_S8nrvZaqj7iDzD6OvNJit4dwzRJqzdx-05zriHeVHEogTp4n1_l76qZqnhp1fGthNaDBVQ0mtljhW2DOmZ4pa9a2YL5TJ0mpfRx9TUfofa71D7HWq_Q-13qP0Otd-h9jvUfofa71D7HWq_Q-13qP0Otd-h9jvUfofa71D7nZ93-x2EXSXgh0RJUgy233nd8ySp-w5137nXfef5j959R5YD-u47z4_ovvMQWugm0URpmm2kYwlBRU3nwDDwvUb4SXWnKWY9JgLsyPOX6By3iJw8hm1cJgEvw1oEsV8WQZH5cR35SZbuYhtb3sZ-tvEHWqXD6dKWsLKLg9OTUM7CwYmCvArBn2O8jsOiCsCjyYPaj6sc1XNZoHcTBWlVsxLUcxmhB5GHPqtYGfiVxM7ueKVtxJviMkm3EG_iIqkTkSdEvCHiDRFviHhDxBsi3hDxhog3RLwh4g0Rb4h4Q8QbIt4Q8eYRiDciKPIwhFAfXJ9zEG_wJ6yjNDeylDDGvJa3FiL_5_57TzY_j5nnCXyhH_2fdYJ23LTvIELnKrNO9B6i9xC9h-g9RO8heg_Re4jeQ_QeovcQvYfoPUTvIXoP0XuI3kP0HqL3EL2H6D1E7yF6D9F7iN5D9B6i9xC9h-g9RO8heg_Re-hy7Z_-5doPuZpuk7iiDuz22yc3b5Z0vq_4N09egK8LSsNDDXmPC6TgG6uFrGL2jvlIOf4YoGD2YAnbPz6cYATjLGYgENI2PZRexOIkTILQB_UURVWS-YxluZ9Fu-hFlp2yn170gXbpcH7UXnpRT7U5C70ozVlQ-GnJ07RI8tivEvBUQs5zCCn9Kggi4Sc8jcMaPKyy8os8AH9LsDoMizDIivJQelHwWrKKLpNkC72oAgMaVbkgehHRi4heRPQiohcRvYjoRUQvInoR0YuIXkT0IqIXEb3oKHpRVkRVHIKVibLsH45epBAKmE7VWHVVZdmZ5pGqpzFFV1QQCiGpcjhT8Hkb4iwRZ4k4S8RZIs4ScZaIs0ScJeIsEWeJOEvEWSLOEnGWiLNEnCXiLBFniThLxFkizhJxloizRJwl4iwRZ4k4S8RZIs4ScZaIs0ScpZ8RZwlrDPcvJLp4otgvm7_ffoER_l562vYPqDR_ShcbrSRCrz2Q-1THqUgh4l1j1QxmyA3fiiv_ca40H9qTOTq8Kl2h_GoZoyIOqROjC_A-uxX-P2hU9PdHiAzXUfztFt1heT8Zq8oy5I8ww2OqNxvp6y162UxRlCnY2jJ8hCmqaP8GBFksVO332mU7GMKARaY-fRdcS-UAiuYwDpqz4_dmoQlon1pT4GLp7SOtBl1hkYN1Yrxru7YP_4xzXbI3S60rJaaEBANjLMgs_NYuyHjXqm9_EmIFtB-zAeVShcKluFkrL0kXGSzcEt62lvdt2YXewagzi7VnreA7ou0rlIrWcO_h46OYdnmObKgwTbOgyjkPs6TiScjELqadJWrtZ9qRTvhZ64TDKZuWHqjmdBn9sJ36dxa6Y5bkNQeTGfIkiwKWRGEmqhKGCSEezeq4LPy0jsK6LOuqKMKs9EFCEEzK0gKsLdvxPg7XMR_5xeuguEziy2jbVWpZmsMZCwriOhLXkbiOxHUkriNxHYnrSFxH4joS15G4jsR1JK4jcR2J60hcR-I6EteRuI7EdSSuI3EdietIXEfiOhLXkbiOxHX88bmOPE7qpECSXGoDTqfab3KQDyja6xOiS96YeW11RQIEYw1ZsQmWsDVuXbmQfk6_c7JuPSA_cRgHYViA5yms0DpAgRO02rHbanOoDmwELd4hiq9BRdIjDCUwHvd_eD8zXoRgKVkW2v10gAcOd_VU_ICsusAaNVzjzu8nClRBBezpjVgq3pmx_ypwrxswVxpUuiYAn1y1jgmXAa2F62iHr7tl83tQnQuZG1X1JtgClVqGaZnJD6YHiehLRF8i-hLRl4i-RPQloi8RfYnoS0RfIvoS0ZeIvkT0JaIvEX2J6EtEXyL6_syIvtUOom-1g-hb_VhEXw1Je4PAz-4D3HJYZ8zPE7FGSFsj5OwkoB1OM5LcATxmUzh1i7uROmoHXo7YT3Anc1RrY4M0XkPmg5KbQaSJ6QBdQFA7Lg-y2iipJRHjsICN0toNFqNqOsnW8HBVdhA9MbaSZlPtSfNnfDiGVN2tSbXsm5VGTmzM6hOTR95OVTXeXO9tN8p_xHU7jjQKwWwSZXGZZ0XIyijLozCKmES4b6yxM3GmGTToTOmF1HNQgvYJuNxcecocc_VoKTwtCmoI6XxaLqol0h1w6-NPSmoP5-Depxqu3xTZMwn_XqmTwX3qZOC_9oPLKLr0iy3UyTwo6ySKc6JOEnWSqJNEnSTqJFEn_1Gok4GfiIRnqSj9PknTuzVH26Pt3gqsEEzOgTOOBBb0hABP4GaEztx43vY27OVkspLIOQmRxAqXs1FrkoPboMgnPd_EMXlB6PsHmDnijxJ_lPijxB8l_ijxR4k_SvxR4o8Sf5T4o8QfJf4o8UeJP0r8UeKPEn-U-KPEHyX-KPFHiT9K_FHijxJ_lPijxB8l_ijxR4k_SvxR4o8Sf5T4o8QfJf4o8UeJP0r8UeKPEn-U-KPEH_3w_NEvwZV89tLbdV_s_T_fY5Nu_nmdVPpcV2G91_Dqf7_XyBZVWmV1ytZoei90vD9E0oOz7Hxsy1E2T4j8NE_AwTj6CX8ShqeJfp8SboFpZjZZWfi74xpYWg1ogIErKKs6TtM8S4-eD1Ki8CjMwBxoC2J0CbiGK3532YcA5vdB-DQIPfe-yY35MAi6QCqzo-fzChZbFSwlzUdOweRF4CzDP0ERPF2b58jK6EHEXkc4hoi9zISYDqVkCYswnzUSrb7o4Z7rCzbeJSg7roVdTadMEXhxQCMQsCKmyCExIZjesre1ynLaeJcADL-VpspOkNpgKlPuIo937eP2YT-DceQEZYbPjCj3bimqW5lT9LT7ulZP6R-3jd_8OXurYlnnsGwuNcRGsBTglkjLZVGZmtLs3YLnMNevdDgrOQ3CKsmYSGLfr-MwLRl4KkUU7brK1pJJ99OHSS-RXtpK3R5gwt-nOsc_bGcyn4W6nVQiKsq0KPKYZ2XAshpTOn6SVVlVFFVcBYGfpIEfcwi1eRoGYVmlAcbj8HaiFDveZ526Hb0OosskuYy3Ubchko3jsCTqNlG3ibpN1G2ibhN1m6jbRN3--VC3ozRIqlpErHZOZx839EnH4YDACG4VZ2UYBXHRk0idGEGP9hDnXzGq4Ui3cuvdqLXqHXikOKMmQI3cl7ZuGe914YY7b5DniJezQArEbyk_f4lM7-4TZ14jkGt8Nu-zpQ2XPLvW8-ErY--3M9Vii2uucP-ItQdg3huegNBVObk-L60eiuiGRho1q7RMQkB7QiNZ2kOJnwocpOmmWP-VegfX4kKz4BXJfGJBJGy5Rr6cyrPUWUbynClBG5CfMvOjzA9jlodJX_60UVjvt50cXumlsou3tgdyoS09wWqY9cBIPmFUsQUfaa8fVcrH--IoRyc56dwBVRHlMRN5mvuVTbg7AaDlmp0e2W2fkRWG-xmQCysvFwgmup1xcCkmDWgahZa66Nlt3WraUYMHavBADR6owQM1eKAGD9TggRo8UIMHavBADR6owQM1eKAGD9TggRo8UIMHavBADR6owQM1eKAGD9TggRo8UIMHavBADR6owQM1eKAGD9TggRo8UIMHavBADR6owQM1eKAGD9TggRo8UIMHavBADR5-4g0e5Bm_3HVN-L2_3mvvsPHX9e4OssR1uWjAy1nw0fIDt3g45ALxB3V5cFhuw5cxT2cc87p8gBecB0kJ8SY_4WJnNyk3kWSDarLiEhnwy1-qHAwo5T7jqXz2X_4S3Z6BGYEHzZOgLNZm9M2u4by-TryHR37gEAMc8zj16zyQsNLHm9lvkV3kcE-wU8lrgSWG5eJuJNNO3v_29ZdfYPgCKlGlHzqpJL2hfS2LMorSx13FA3yDfuRGpWKVHW_haL7ZYkjNdEO_LiGaFY87XT0Uhn5aNFW4gqybVWv8BlnpxVSUru-u5msUgaGWGs5J3DxyulHEH2W534T1pkWDjIcbGXagk7zluDRtvWAKoymJUztO7fbuFC-R4oL603Bzdixkz6xR747VTKewveNc7my04SlkOQqFNLlfvv7sq9FyNrrBXhWt4CO9I84Gjncdse0PMWbf1H6YRTBYh0-VuMe7jsOeccHyoT9mZ9pBALq8c8mSO-R2d5sQUyetMS_k5gC992zyVqeSdvQDsfPCAfxxPPYHdvO9qixJeq8SNBkrcKF4pYt7y354a5CSh6Ku_FgEQZSleZmkeF99Xe5qDWKbFexvDULGjIwZGbOzG7PDe__c71uSXPRH8TL4YXuPkrM0ZcEpx3DieVWFRZwmMa_KUJQIuSpEnBZZBKqFF1XG6yotQDGkYZSyKvPLPE95WB_ycmsdWsLotR9fJtFlEG7p0JJFVZZVQUYdWqhDC3VowT3JKibwVPihGOrQ8s0-53d7oxb5jtSthbq1ULcWQ0GC0xX5UZQJYevBjk-8Ke9Hu7pgDLAXymzR_Hmm6xQgCrK1SIMFPVgi5Isa_29pfD91IixvWQovrBuXWML-WSBXuIhYDMelcDuU9A0ETFWTw6phTQ4fWl3ogPCijwixuCRDwhtmMTiwO_8qAWOq4KTDUhP0GTisLcy1-A8VXmI5VL6v5Gxbsr-sFXol2AXYwQtFrQcpUY1lVAlSlgw1ChI-PRHUb4f67VC_Heq3Q_12qN8O9duhfjvUb4f67VC_Heq38_fRbyfm3BcQksDR7jGIfZnjHnvopBqFDWdjEIKoLEJu04ZO2UI_6SE1hxIi-PeaLNNJEqSOSHW_DdsOR8fIYFOa71GtXGjjqZhXDsrVhJJIwFPxqAXhrtUpNSUEptRp1lhvPfv1wnyRJ6lrWrMNnJcc3LGKZXHEnD5IfeHkcHjfUNVjOuMric7qJdAitkzqYGQH0HT6pwjtGs-Wk_kay3LmPV1O585Q-uPrVExVkpbth0YjBdATWrFeIkN70aDRHy1WbYtkq0NfTe3OSGcIDpmI8pyff_bs5edvXn566HNOfoBDU9XWCX6jRoP314gm_c9DJ2PSG0OzcVf80HG1PRsYdh8-tuRBwqsEvMC8Z_zbKpqR3QeUwITsomPON_g2d8hFrdlqAhrhGpcRRlUMDnQZ0dlR_iG23vJA7E0q9tq4hs2fkeekVDJz-LY25ahzTZjlNChxhwjxiw5bwBxweLS7v4T3duCRh3zeaWlwn97h4g6osxp1VqPOatRZjTqrUWc16qxGndWosxp1VqPOatRZjTqrUWc16qxGndWosxp1VqPOatRZjTqrUWc16qxGndWosxp1VqPOatRZjTqrUWc16qxGndWosxp1VqPOatRZjTqrUWe1v_POag66re_c8fx2hopABqBztrwdakmzrdOKYFURBHVw4KCbrT_-6r2sZfVQBsLL2d_-_X9BqKNAcZLpdj_M0tlFE7Nvi3PM5KKw9gXL1lurPNd02Bq-3u3pRHP_s0MtZwo_rMooP-1Z6zR9nS03OZ6-xZHqgVQryq3k6MGzBnrLFEVV1JFE458wqdeGJCxNHqjeppXkYA1TVHydEfLkW7GwbBFlVAYmFdZxFSVRvTapfSjLoV06FqG5vd2Zczx2tjt7JTB1Lnr6tIMb1MMbJGfL3jU3ysrAYsMM5fKNdx2e3V3HkPY0AiUBm-2MWYrleyEciKiTYGXac75PTRjvOhwDLc9MXsF0DpNCY951vOsEbB8QAU_CFHdQekcaS6Fe6Z6Yj3dJ8r7B78mlK7yaJS-b1PVmdLxLPLc_6ZVYMo2S2sJgdEVCdjuQGRoEdpiueDuaoX3O3qr56xV3kh-OAHWqD0F7s2q62627b7G4u1upqWyTpCq7tA6rd2QhAvb5uD5qIkqKgCUiFxWcJJbzug6yXDIrt_ZRsy2F9vdRI9NFpotM18225mYD3QuPaG7Wt_c6S3OzIsgDEQUsL_O6DrOYc-ZXcZwkYYKk-6pKfPghZX7OsyKvEl4naS3ixIeQOcojcUpzs6C49JNLP9rS3CzJspgVIqXmZtTcjJqbUXMzam5Gzc2ouRk1N6PmZtTcjJqbUXMzam5Gzc2ouRk1N6PmZtTcjJqbUXMzam5Gzc2ouRk1N6PmZtTc7CfZ3Aw7GiUcTHDUc6W3NjfbUu4eoGXGZV2zKOZZabW6U0S3bJmHVcWVE7iB8_yrA6zcirb47qN_QrPhSHHTjpYWOdp9rCg1r1eL1locZWv7XKfMbva5RX3o4NGHWESYwM69dZqI6Xn80U0Wm9EwWyzPcE-K1nAfQ39x5_Ivdi6fqbngxPFAaFzoNy9evfzdyxefvvmXL77802cvPv39izfyv69kBCpn8dLQ0t0eEhZVojhGC3yoYfL0xZVjcLGDdCRs0ZZXBctZn45w4A-OsO6HNJiwPg7yJMrTJA9tGtRBOWwtHx2HXLCwpcur9pe_3Myazxyus_e3__bfbVg_kp_dlkLHj121ayxUVUGSdgjHOC3rPVRnY-Dm8iwOeBFbReEgLxzS_KloCobRGgReigZmTvNsoZyjkQ6QbLCunDwn1biZd_KEVPP49w7jbbP4aOYEGNpVJ_qU2ieyumEiUPtNm1VzqyImBhU1bkAF0eufhKzCKVjWxvGYu6DubYA7Fbxj7hezyIokK-dxJ-S3p00ndN8MnD8eXlUmYZPREryjezUKSQbVEx_NVwt0qGy94g7GmB7Z79KBs1C_S-p3Sf0uqd8l9bukfpfU75L6XVK_S-p3Sf0uqd8l9bukfpfU75L6XVK_S-p3Sf0uqd8l9bukfpfU75L6XVK_S-p3Sf0uqd8l9bukfpfU75L6XVK_S-p3Sf0uqd8l9bt8SL_L7374_wFuBkKq)

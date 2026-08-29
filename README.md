[//]: # (ob:6ec771b4)
<p align="center">
  <img src="assets/logo.svg" alt="Proofpress logo" width="88" height="88">
</p>

[//]: # (ob:de7999eb)
# Proofpress

[//]: # (ob:7542280e)
[![npm version](https://img.shields.io/npm/v/proofpress.svg)](https://www.npmjs.com/package/proofpress)
[![npm next](https://img.shields.io/npm/v/proofpress/next.svg?label=next)](https://www.npmjs.com/package/proofpress)
[![CI](https://github.com/chenmingtang830/proofpress/actions/workflows/ci.yml/badge.svg)](https://github.com/chenmingtang830/proofpress/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

[//]: # (ob:e667d986)
**Proofpress — The Governance Layer for Agent-Produced Knowledge.**

[//]: # (ob:0e0e9d9a)
Agents don't just consume enterprise knowledge. They create a new knowledge
layer. Proofpress governs it.

[//]: # (ob:92fbc10e)
Proofpress gives a checkable answer to: **What may a future agent or human rely
on, why, and under whose authority?** It governs selected conclusions, claims,
and decisions produced through agent research, reasoning, and work—not the
enterprise knowledge agents start from.

[//]: # (ob:815b673d)
> Existing knowledge infrastructure organizes what agents reason from.
> Proofpress governs what their reasoning produces.

[//]: # (ob:6ef36a68)
## Two knowledge layers

[//]: # (ob:8fb4a17c)
Enterprise knowledge is the business or organizational knowledge an agent uses:
documents, databases, policies, domain ontology, and memory. Agent-produced
knowledge is newly synthesized work: conclusions, claims, findings, analyses,
and decisions. Proofpress governs the latter; it is not another enterprise
knowledge graph, ontology, memory system, workspace, or orchestrator.

[//]: # (ob:eac911f1)
```mermaid
flowchart LR
  EK["Enterprise Knowledge<br/>business data · documents · policies<br/>domain ontology · memory"]
  A["Agents<br/>research · reason · work"]
  APK["Agent-Produced Knowledge<br/>conclusions · claims · findings<br/>analyses · decisions"]
  PP["Proofpress<br/>evidence · verification · authority<br/>admission · lifecycle"]
  GAK["Governed Agent Knowledge<br/>current · scoped · authorized"]
  DA["Downstream agents<br/>and humans"]
  EK --> A --> APK --> PP --> GAK --> DA
```

[//]: # (ob:8f7c2d11)
## Why governance becomes infrastructure

[//]: # (ob:9317a2bd)
As agent adoption and autonomy increase, the underlying enterprise knowledge
usually grows relatively steadily while the accumulated conclusions and work
generated from it can grow much faster. More agents, more runs, branching
research, and agent-to-agent reuse all add derived knowledge without requiring
the original enterprise corpus to grow at the same rate.

[//]: # (ob:bf4b55ec)
![Why-now curve showing enterprise knowledge growing gradually while accumulated agent-produced conclusions and work accelerate as agent adoption and autonomy increase, crossing a governance threshold where verification becomes infrastructure.](assets/architecture/agent-produced-knowledge-growth.png)

[//]: # (ob:f64abc15)
This is a directional product model, not a claim of a universal mathematical
growth law. The bottleneck shifts from giving agents access to knowledge to
governing the knowledge they create.

[//]: # (ob:1423b1c1)
## Governed Claim Graph: the product object

[//]: # (ob:821f22af)
Proofpress turns selected agent-produced work into a governed claim graph. Its
objects are conclusions and the claims they depend on—not enterprise entities.
Candidate claims enter from the left, cross three distinct governance gates,
and become reusable graph nodes only after authorized admission. Scoped
projections then flow to downstream humans and agents on the right.

[//]: # (ob:836f405e)
```mermaid
flowchart LR
  subgraph U["Agent-produced work"]
    E1["Evidence A<br/>source · version · provenance"]
    E2["Evidence B<br/>source · version · provenance"]
    P1["Candidate claim A"]
    P2["Candidate claim B"]
    E1 -->|supports| P1
    E2 -->|supports| P2
  end

  subgraph V["Three governance gates"]
    V1["1 · Integrity<br/>deterministic checks"]
    V2["2 · Policy<br/>recommend · escalate"]
    V3["3 · Authority<br/>admit · reject"]
    V1 --> V2 --> V3
  end

  subgraph G["Governed Claim Graph"]
    C1["Conclusion A"]
    C2["Conclusion B"]
    K1["Admitted claim A"]
    K2["Admitted claim B"]
    K3["Admitted claim C"]
    AU["Authority + scope"]
    PR["Provenance + receipts"]
    C1 -->|depends on| K1
    C1 -->|depends on| K2
    C2 -->|depends on| K3
    K1 -->|supports| K2
    K2 -.->|contradicts| K3
    C2 -.->|supersedes| C1
    AU --- C1
    AU --- C2
    PR --- K1
    PR --- K3
  end

  subgraph D["Scoped downstream consumption"]
    CP["Eligible context<br/>current · in scope · actor-matched"]
    H["Humans<br/>review · decide · act"]
    A["Agents<br/>reason · research · continue"]
    CP --> H
    CP --> A
  end

  P1 --> V1
  P2 --> V1
  V3 -->|authorized admission| C1
  V3 -->|authorized admission| C2
  G -->|project| CP
```

[//]: # (ob:09cd9aa3)
The graph preserves a claim's evidence and provenance, verification and review
record, authority and scope, dependencies, and any later contradiction or
supersession. It does not turn a source or a model output into truth; it makes
the basis and current eligibility for reliance inspectable.

[//]: # (ob:4fe9b290)
## From agent work to governed knowledge

[//]: # (ob:9b060e32)
The implemented mechanism follows five steps: **extraction → evidence binding →
verification → admission or review → governed claim graph**. Agent work is
selectively extracted into a bounded evidence projection; the configured
authority alone decides whether a checked conclusion may enter governed
context. The diagram below zooms into the three governance gates shown in the
architecture above.

[//]: # (ob:2e6c722b)
[![Implemented knowledge-admission lifecycle: extracted evidence becomes a scoped candidate, is evaluated and reviewed, and only then crosses the admission boundary into governed context.](assets/architecture/knowledge-admission-lifecycle.svg)](docs/VERIFIED_KNOWLEDGE_LEDGER.md)

[//]: # (ob:b5752df0)
Evaluation can recommend; it cannot authorize reuse. Rejected, unresolved,
expired, superseded, unauthorized, or dependency-blocked conclusions remain
auditable but stay out of the default context.

[//]: # (ob:3ce2d48b)
## How downstream agents consume it

[//]: # (ob:827e8ea8)
Today, downstream actors can consume governed knowledge through the local
ledger and CLI, the local review and context UI, supported agent adapters, and
portable Markdown/static-HTML artifact carriers. The `context` command projects
only admitted, current conclusions that match the requested scope and actor.

[//]: # (ob:76acc27a)
A supported public API/SDK and MCP server are **planned, not shipped**. The
local UI's internal endpoints are implementation details, not a public
integration contract. See the [ledger scope and integration boundary](docs/VERIFIED_KNOWLEDGE_LEDGER.md).

[//]: # (ob:159c6149)
## Choose the path that matches your workflow

[//]: # (ob:893ea267)
| If you are… | Start here |
|---|---|
| Building an agent or multi-agent product | [Govern selected conclusions for a fresh session](#quickstart-governed-context) |
| Shipping a high-stakes review workflow | [Try the legal cold-handoff fixture](examples/verified-knowledge-ledger/legal/) |
| Handing documents across people or systems | [Try a portable artifact handoff](examples/portable-handoff/) |
| Evaluating the product mechanism or claims | [Read the frozen seven-model study](studies/long-horizon-eval/relaybench/PUBLIC_RESULTS.md) |
| Integrating memory, traces, or a workspace | [See what Proofpress owns—and does not own](docs/VERIFIED_KNOWLEDGE_LEDGER.md) |

[//]: # (ob:09822b9b)
**Start here:** [run the 0.5 alpha quickstart](#quickstart-governed-context) ·
[see the integration boundary](docs/VERIFIED_KNOWLEDGE_LEDGER.md) ·
[choose a design-partner integration path](docs/VERIFIED_KNOWLEDGE_LEDGER.md#design-partner-integration-path) ·
[bring us a real handoff workflow](https://github.com/chenmingtang830/proofpress/issues/new?template=design_partner.yml)

[//]: # (ob:4ccd51b9)
## Quickstart: governed context

[//]: # (ob:cc376e2b)
### Install the 0.5 alpha

[//]: # (ob:d6f9f208)
Proofpress 0.5 is published on npm's `next` channel. It requires Python 3.11+,
Git, and Node 22+:

[//]: # (ob:7b197ac1)
```sh
mkdir proofpress-quickstart && cd proofpress-quickstart
git init
npm init -y
npm install --save-dev proofpress@next
npx --no-install proofpress --version
npx --no-install proofpress setup --agent codex
```

[//]: # (ob:5ae48e1b)
`setup` installs the agent adapter and writes `.proofpress/manifest.json`. Use
`--agent claude`, `cursor`, or `all` for another supported harness.

[//]: # (ob:460f8108)
Import a bounded telemetry export or artifact, propose one scoped conclusion,
evaluate it, record an explicit human admission, and request context for the
next actor:

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
Each command prints the identifier needed by the next step. `context` excludes
rejected, unresolved, expired, superseded, and actor-mismatched conclusions by
default. `ui` opens the local review queue, governed-context preview, and
lineage graph. The 0.4 `proofpress knowledge ...` command group remains only as
a temporary migration surface.

[//]: # (ob:9c6c7f6a)
## Evidence, with the boundary attached

[//]: # (ob:30685e8d)
The strongest current product evidence is a frozen panel of **7 models, 3
Harvey LAB-derived legal task families, and 126 valid paired runs**. Across that
bounded panel, Proofpress governed handoffs raised rubric completion from
**89.3% to 93.4%** (+4.1 percentage points) and reduced observed unsafe
propagation from **8 to 0** across 63 controlled stress pairs.

[//]: # (ob:cf466876)
[![Frozen Proofpress product study: seven Harvey LAB-derived task models, rubric completion from 89.3% to 93.4%, and observed unsafe propagation from 8 to 0.](assets/articles/harvey-proofpress.png)](studies/long-horizon-eval/relaybench/PUBLIC_RESULTS.md)

[//]: # (ob:aea6ced7)
This is a descriptive product-mechanism result for frozen,
Proofpress-composed handoff episodes derived from public Harvey LAB Contracts
materials—not an official Harvey leaderboard score, a population-level causal
claim, statistical-significance result, or evidence of improved legal
intelligence. Read the [results, boundaries, and retained receipts](studies/long-horizon-eval/relaybench/PUBLIC_RESULTS.md).

[//]: # (ob:8c55fe43)
The [Athena/APEX governed-working-set pilot](studies/apex-agent-eval/) adds a
conditional efficiency signal: across its two evaluated tasks, Muse Spark 1.1
used 38.3% fewer **executor-generation** tokens and 46.2% less executor latency
under the Proofpress treatment, while majority-scored quality did not decline.
It does not establish lower end-to-end cost: treatment construction and
cross-task amortization remain incompletely measured.

[//]: # (ob:41600981)
The separate [artifact version-check study](studies/agent-handoff-artifact-provenance/)
isolates the underlying mechanism: on one preregistered changed-document task,
ordinary handoff continued incorrectly in 12/12 trials and Proofpress-assisted
handoff in 0/12. It is mechanism evidence, not the primary product result.

[//]: # (ob:cd8c1f66)
## Portable artifact provenance

[//]: # (ob:ec2e5323)
Proofpress also maintains an open portable-artifact path. Markdown and static
HTML can carry an inspectable record of admitted revision history even when Git
does not travel with the file. A format-agnostic evidence envelope can bind
provenance to the exact bytes of other files without pretending to understand
their semantics.

[//]: # (ob:20a32f50)
Start with the [portable handoff example](examples/portable-handoff/README.md),
then use the [Portable Artifact V1 contract](docs/PORTABLE_ARTIFACT_SPEC.md) or
[Artifact Provenance Protocol](docs/ARTIFACT_PROVENANCE_PROTOCOL.md) when you
need the implementation boundary. Think C2PA for knowledge work—not a claim of
C2PA compatibility, signed authorship, or complete capture.

[//]: # (ob:22a54f46)
The example includes portable [`strategy.md`](examples/portable-handoff/strategy.md)
and [`strategy.html`](examples/portable-handoff/strategy.html), plus a
[`proposal.docx`](examples/portable-handoff/proposal.docx) with its
[`proposal.provenance.json`](examples/portable-handoff/proposal.provenance.json)
evidence record.

[//]: # (ob:226a29fd)
## What is—and is not—recorded

[//]: # (ob:cfc1c3aa)
Proofpress records selected evidence, candidate conclusions, lifecycle state,
scope, stated actor roles, policy recommendations, and explicit admission or
rejection. Portable documents also record accepted versions and computed block
changes.

[//]: # (ob:5e0b34ed)
It does not automatically store raw prompts, transcripts, private reasoning,
casual brainstorming, or every save. External workflow dispositions never
become Proofpress admission decisions automatically. See the
[privacy boundary](docs/PRIVACY_AND_DISCLOSURE.md).

[//]: # (ob:32f0ea79)
## Current status

[//]: # (ob:4902cb38)
The implemented developer wedge is:
**bounded telemetry or artifacts → evidence-bound candidate knowledge →
verification and review → governed current context for the next human or
agent.** The local ledger, CLI, review UI, artifact provenance, and portable
Markdown/static-HTML carrier are available now.

[//]: # (ob:99c9f31b)
What is not established yet: a hosted service, production connectors,
general-purpose memory, or broad efficacy across long-horizon workflows. The
next proof point is a real design-partner handoff with a measurable fresh-session
decision. If that matches your workflow, [open a private-data-free integration
conversation](https://github.com/chenmingtang830/proofpress/issues/new?template=design_partner.yml).

[//]: # (ob:8deed5b3)
## Go deeper

[//]: # (ob:17d6b002)
- [Ledger scope and integration boundary](docs/VERIFIED_KNOWLEDGE_LEDGER.md)
- [Interactive verified-knowledge-ledger demo](examples/verified-knowledge-ledger/demo.partner-style.html)
- [Two-minute portable handoff demo](examples/portable-handoff/README.md)
- [Published controlled handoff study](studies/agent-handoff-artifact-provenance/README.md)
- [Documentation map](docs/README.md)
- [Privacy boundaries](docs/PRIVACY_AND_DISCLOSURE.md)
- [Agent adapters](skills/README.md)
- [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) ·
  [Security](SECURITY.md) · [Code of Conduct](CODE_OF_CONDUCT.md)

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzU1NmIxMTVkZTcxMWIwY2QzM2VlZDI2MCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjYxNDQxMWJmIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV83ODkxM2MwZTAyZDEwNzgyNzY0ODJmZmIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2VmM2MyZDU2NDRmOWRlZThmZmU5OWQ3ZCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfety3EaW5qug1TFjW2YVcb-wezxLUWyZYVnWSrR7J0QtlQASJFpFoKZQJZrddkT_mv27sTExjzCvsP_3UfrHRuxb7DmZiURWEQCLF6vt7uPotllVQGbiZObJc_s-_OkRWyzLgmXL0zJ_tPdoPj8NgjB1nCDnkeOkdpZ7Hue5G9qPdh6ldX51mpdnvFnCtc05c4NwL2a5nScsTfyMx0kcB56fO4z7YWbHCXfsJLbzwHFD7iZ27DoMmvcDLwlDHiQB4zm0m5dNVn_gi6tHe3_CD8vTJTuDHmZsiV3twB8pn8EX3_FFWZQsnXFrwT-UTVlX1jlcXy-urPTKermo62K-4E0D98xZ9p6dcXyota8X9R84PO5qgQ2eL5fzZm9396xcnq_SaVZf7GbnvLooq7Mlq85iz95du3vB_3VVwt-nq4YvTrO6angFslguVvzHnUfnnKEQQ8f3QXbFI_nNKf8gLgLh8tMoThwvs7nt5o4dxW4U-rFbFCmOrF4s8dFOZ2XFYeTtjMxOeeFlbh6Evl8kOedxUfAkyaNcPo4a3WnG5s1qBg_s4jizepE3j_be_OmR6v5Pj2CW60WDf8mfeX6agsjfPPpmzqv9I-ugzvn3j97Cg7SLAvp_dbj_9OvD6QV2dpu1wpbLRZmuljBFpylrygZXDJ8Vp6wB0S3FvLPV8rxe4IDelxU22Vw1S34Bv1TsAmdubWA7cH-DU_5or1rNZjDM7BzmiMunTGd19h6Fz7MoclIfLofpWfLv8SE-_b__8T_-33_-x2fwpeqJ5TmX8oN1xC_hm9_OLTYrz6p_OnmUgcD44uTRFyeVZf22vDizmkUG3-PQl83urD6rp82Hs5NHcMcSvlfrDppbXs3FimML9ujHnW5UIKEkSXi6Nqq15To4rl-vL2vVAy4sWKRrnUSB77qxze_QyZtfvanmFxbsQRTw20_bfQHPPm3OSz7Lm2lZ78I1ux-MHYFS-GzksXkYRnkSh3cY0ePHcrPz3Hpf1Zcznp9xq6yKBWtgt2XL1YJbRb2wYA3VVX1RrxoLVgpsm2rZjIwIdh5PQF3dYUTdVdZZ-YE31vKcWxW0YJ2vLlhl4WCwe4tZoENA-aCaYlVzyRfWyIgSt0gz506z9i_1amHBbOQgD-s95_PGKpeNdQHbZdbsWMu6xv9c8AvQjzvWZb1434BW5DvWnI8t1tgJ0jDy8jvN2uslaAnrnC_43uPH1pvFqhJysqcBbJb5ObNAgWbvG7zq7ae_7j5MzkZGFIIGDFkY32FEX1jPyqV1wXJuZbX41wxOk3rBljCHU2NvwTXvYVJLaH4GeoBXGR_b0EXE7Di4y6xtr2hQ32Yz3uzKKZyI42EyNnNF6jMnytZGdXBe1w0XszBny3P4g6FAlrBIG-sKlxCujGI2qoR-bW3bTH05rqU4yxLHKZwHH-MP1lGB11pswf_y5_-0frC6tWj9cFL9MJlMxP_hT-vJqpzh0GCDql1bd8MWct4QbAQnsLM-6C_rSwt0ERxZuYXfltWK4Xknd9oN4rzx5hERJp4TMTfNH2g0xh5oUH-kfHnJeWUt2KWSDTYBksrFBKkuQc0Vq-XIYozsPMz99KFk9qs3x_K-ydp9bJGdl0suDoQ9Mb7zumm1IX7EhkdGmRZ-GgQ8e3hZlo1V1UtLnAy4jpegc-oFqOUF6GArBfOUV3mrni0wYkdG6WcZGNFpsjbK_6qV5551hvZzpYaLP4-vvhtuHVl7WeZFYMuvWzJHFbQ1m61r-vEh_Noaummk8zwsksK14_t1bswRXg_zNF-ls7I5BxnAHIOR80ljvcOT_Z2FJmbFZ1PraGmh8T-23lMniVjm3G9w7969a85Pqov3eSnOdjXSSXdSWv_4j1aW9_7WjQ7PurXRgavlx9y557y9g3NpNX8Hp6S4Ue4wZfXkbA6HmVATlwvYkiDDaTfI3Yux5R3aRezcd16PLtCFAr2U1qsKfrTgJOcXfAm7i38vfkITTfkwOyjAOR46dcWtMZMxTpPU88LkQea1mn9vTSZVPVESNKbRgktzNDusUj7IyQmaBRXM5OnFyMy6dpFyFvL7je-QZeegAS4ucP7mCzCD5OTikJZohy_A1uUoVXC0teULGnI-HbVuszCLinDd3j5UDwo2aSkOey6njMFMgd8IIxGDG1NgWzYxoks8OwT7Lc4fdGRHlVhO8MWCn5UgnYXSqwswO-FP0CZ5XRTWkjXvrUthmTArr7PVBa9GpJgVfhjGUfigYwWf76AbmdjEk3Z8zXKVX-3BfgGxYXvt946767iw-0fGymAtZjyPHnSsx-egpZvVHPeFXJfKVZ0IVwsNuQuOurpsLlCHC_sRhQyKe0yueZw5Rbjhn6o4jFYVuEc_8IpJj2BsVd5w65hVnLk88FzvQUZiHHBs1tRgSMN2hv83whiZg2nXxpomXctgdk-tr9mItFybeW4R2A8yRmmb69Xwph2RXmr8e3Yxn_G3n6o_ml096LExuiFzk2J9V_8eV0PZ_OXP_47KTdpl8KGNgt0wqTffPWYuFZmTeYw91HiMqVUxPquBUy5DS5XrTZZBu2XOlsJYz2Yr3CnNzojYAm6nns8fTGxgLeU1VwbwalmDK1dmcB4JOxeUHroWsE4u5stGGMRVky1K8WE0jAbLz-YsWj-KD1aLBRogcOAtVze5XdcuHpk7P7HdLPXiO_Z2fC5OcjRBKpyenH_gM9h94MvKYFazd1I9fnzdWEErZexITbKk8DYsue2HpWZVTA04Jay1fK84-AJMeE_wqeGLD6UIFcnwEjo_2ZiHEudgHQTpugJ7VsNTcxltGpsV87qRCXGiPExt2719HxPrzb7hKAojFSM9Zwvp17WH0dtP4TBudvdfHXx5dHx4cPztq8NpNyaQ1PLRj2932pD6I3UInWYLzmRIW_zSxsf5aVG4XurZdswzcIcjJwt8xnIfVSjIXwiy1Xsq6i9jh_MaRieSGAvREwa8208Y736L6YJZmV0ZLZgpBKMRkZy4Y3ahqYvlaQHTwBfCJBR3NKmzx-KwsG0_jFkW8cyJ3CjL4jxPGI98z2GOG8LGSVLfs3kSZkWe5WkIVmpaeDFzPRH8wZUqkhFytva8-EcQdCPOGTec2PHEjY7teM-293zvc_i3jVJTEkdfMA1iniYRrJDu2z89ROpCLDeZVThnzTlqgsIJWejHQcYxqyPaMBINaiXeP4OAah1_g-8vy3x5Dr_EMXw45-XZ-VJ9gjZ_uzv_omcvqtHGQRSCoJ0wsb12tEYCQo325ryCai4oeBHmRZTldtA2Z6QaVHP3ySB0V19eXk7hkj80IhWnUnjG5Z-dVKojdD-27mUXr8au_llkEv8JP96614Oj7o6t8oW7TOjNZrcNjDa7WTm9upjtpgwOgI1Hv1-TcojPQWVXDd-z9udoUk_cqT0oIzGG3Zm8Y6JuwDsm6WzVDu750cHhi9eHnw0vNp77sIvyyA_yuF0dRtpHrY77ZHOmjx-PdA_6JwpZ5vh51nZv5HiuBeZvn7pZ1nvW48eX52UG7rthToFVfWUdgRUGRg1GjerLHRn7OL_658ePMV6UwmlkmGfmvcv6pOrMtSYDs2Cn3Ttw5grVLpuTR9gOjrgCmxhayDna8VfLc_R6FvwPovWdk2pVwQPWsw_wAeMd5QL_AJ8JWkW_fQefclXJnGv5RxhQAQbYtejfdFjWTuaCyowLNwq0IjCyV0rW90lKXZSNNFXlo7PLk0qbRWu5GjnqBgQ_U9EItljUYrowbKtsY5VGwC-aFdgzH2BST6rWwQBxFNDYuaXSyiNPzsIocVjhhr7wwcWTG1kyvcjvnvxSszBRs_CZ9X_-N-zohsucyLamykWubkwXuDhgFzEQBZtpp6pVG7dVOzAvK45q9PKflxxsWrB2_gnWIRx2pyCrZcUXQgkNSzCP4iDMeBZwz-1OUJ3VUxK8T7IOg1dzlM3YCrYDHuRRyFNhTMiTscvk3foc70_QwZTC4CadHzzh1RlYXRwnZQKro57Oq-7sP5qBVliq2a0LmLLuTktoSlzVDJwHnFPhMWPSShk0hqnguLa9hXlQOD7Lsih0PT_Si7lLHLbmwf0zfq3Q4zwJArfI40CbI0YSUPV33-zdAvb5bFlO5MdW__xgvXkmtla_GhZHzroWuGlfiv5fn5fzuejfOgfLTM240tVaKtj78ULqpxk_g20I6znXMbai_B7PPSPA8UGdkRN9Rk7k_O-K23dV71-idw-dq7ghKFeWLWrYFHNeQzsoC1lI07QjYDrg04Vp1DD64ivqp7a_ww9shvkv6BIfxQi0LaxsxkrZzyuYeblWdDJlLZr49lP8Twn9rIUadQTK2C9tx0et2hPhPXlgiOxZIw4z1p0eOIDXoCwvcYkaaqK-rNr4hY5HwHdDuvOHvhxwa1U7sQcWtJ2GvtNtG50W7rbNXTK7bR9-bvtJ5Dvc1frJSPZet2Zuna9FQ2vd5jmp0JApK9ho5XJq7evsiU5HqJI5cfjAuXoBcuwCTHqp_uYE7lriGQ5rA9SitKQaMQxp0ECLciFBQ2D71YsLtWN-053jMNiiPINR5icVy5U9YCmjZXmFHVvahIHbVw0f0fdJkbOoKPI08RLtunRpaSXP-2SWcZ__xlxx3c9w8DbYjKFxhM2YqnHn07ef6nOk62p32TOYiXnFUNWVemg35yE4pjyPXd4-tJHlvr6Ibp2oXmCIEU5bsELh8Hlf4m4ES20B8wJ_MTgRVb5UBihRGNeM3dauxeUxKwueXcFt7RHzXhhqPSrbgkPwrEQ9hqpbTr_1WlpJYPYUq9lsbd5E89060h0NKICRpRSGQRx7aRYmvjZgjKx8t_1vn1pve8iZn0WFnSYRa3swsu26h1tlzrX5lXqFF4R-JgxWafh0yfTra-LWiXGsirVeglcCF3pTx_kcPBIw5uQEv0BjznU_3xsxzZw4SoooSeNcWwlGRl2N8F7ZcVB1YO2C6imXmIi9EH9Zk6v2gxTqZNKArTXJ-Qejkf-CDz2evZ1MlP82fplIoMOvUlGjlfv9SQWP1ZPgbefO9cF0zr2YFdrtMrL5rWTukZmH07yAbT_9A-ird1Pr2wb20js9xBkDl_PdjvUuWy2aevFOnL3voI930n4C3QFnR5udE8c-rPmmGdlMgctZHAVpYnN9lho1AG0O-x75fFQypuLYQX9bnD7gTS13WgeRoU89h8OpbEMBWlm07ve_guOz1IcoPrHQNSJ6ICqqRxY1D32eB2Fuh36qbYaunGB9Ud-1NAAsXWG9dRO6hUGZgzKf1svZXEz6yQ2LthXtBC3dpUhoWCciwZGpvEMnaXBI5OgmEz3qw--Onh6-ODg8PXqKbeDkWDgC-KCaVsbIHrjM4EzeJAw1kQffvDh4_u3ro29eQMPj9yjTfO0OPU6cc1AEE3kRjEUshb3243jL7crYeC6xNNRDNasMbNamvqGlVbnWyA1qwbXTNLBzP8xcHXgzSkHaxPs9yjreqUd7p-NOJ5WON1k3hpvE0YtSmMCOkm7juveVXqHJWDDw26CzVflO5Kbl-GZ1Bv6SmjXYgiswGTadMWtuGBEnVZtAAY9hfj61jsXh6FvvDAl3scfpdPpOy-VsUYNOXvALkSMXtiiDZ2UWxjrAoAGFc1G28ZdmtQB9M2p1hq4TOCx1PEfHJI06mM5UuHsRiw6-htxn3M6SUB-aRl2LrgW6e1EK-om5JYEWGGS8VhGirFSO-TRQqaBXlzN0J1SpyHJRslljWsgTsHlxEHkXiQNXwmpqvMmGe6bWEzhRsOG8FMFuo4-1HnD7OC4GPtX4JnrQstuROUoj24ts12exqw9Vo8qmS2rcuURGDVUPfk0I4kEN81-FkdY9Y9HDJGOLfKJSYhg3-uw2jrROgY34CzbYmDmLcydg2rI1iniUKO5TgaOKAR4_BlPh8WOrOa8xsLvhqsOz8IUoEYAzDp-gUeZLxuYsLWfo_YFG1SlrOHrAFblA9QzaEmQwtXQI4o0ochHys1Q651bhhxP0TuF5wJrNmx1wG-B8ELu_QcsBS2nWyi1Qh0hvd3XR4DAajk6INZ8xUXOTo96EVdTM0Y3-wNsxNUrnWGjegE3VjvCd1gdg5daXlYyytLoBrhhZ2L7HCzsLcp_lOlRtlDl1yuf2tUrtwcPzLIu9kPmx7sEoX7ruS9y6BmnxPsenRrGivVFmJ9WXx18_F84_bAfUjhhBEOJUYEBhzWHwFI9yNEKv4QMxM4_arcIYM6yZNhwkQ6udBi5KdF_30dKDQwuM4KoW4QxtzPBK1nGI4WCO56QyArbLWvq73-MDpVdobMOwpImMTTeip3olTq8ll5E8uEksAXhabE5OfIOrGnoem20vd3zbLvIg84vOCNBlWmou7lNr1cYCO02yIwYIi1bFht_olbTfTuR3jjxf4G_lab_85tXx_pPnh6f7r46Pfrd_cHz6-uXhgQi6oVn0Rt_6shMl_Lmss3qmnXV158tX33x3-GIf7Un48_ibg2-ei4bE5F7VKzTOuVQEuv5mPXeC1kFZvbcO3Jdiog3DAIM6f_nzv4uAiNp3dXFSiStFzGNZSmUExk55hnpAhqOa83IuPCO8aMax9Aq8LozWjKSVbNvPgyiK_UwbCkYBW7dX71SC1ioEHhcsCl3f9o2TTlelXd-ut64rM-I3wj2ABaKCPOKjsgItOEUxcKtigdjLBcxM3upVfDLti3UhG1wd0ujEFF2ntYzgN6qX1p8DQ3uOXarDSYYfcUpW-K2o7DhR5sLYvgqdJPb91MkDW-8ro0auNazuUeVWfkAxyhghzBjILGPNCmzedIFaEu7HVJxYURyh0RZGJabW4fdgvlVwmU4y5GUDDpSylCq89qSSYVrzdO0EmvOsVKIxh2yG0cToYI42Uo0vXx19t3_wL6f7L56ePj16ffD8m9c3x80KnroZd0I7c7Srb5TxGdmmLSrzWq3nO2kIlptbxHp2jGI9bbHco_5OqaPG-su__S-9ASbi2r7gN152Ukl3O1PhY528F210ocDOYzYjCuvlCOB8oJUyBWvpWHtD0nXfsQ6eH7XxU-tb-LPnAN9RYXe5WU6q9kzdlefpRB2niwU6gAwN_g-snImNBY80Mp08KHI_y72wCHzt23QFieuVo3eqMQTlLXDqsCOUSTiZrxYi_NDmgEBi6aIGW48XKG5YqSoBNqsxwYq5AZVuESUywhdUERvhDFqiMg4HqNLjMpU9UansLlsucq3QLezMhRCOSBVOVKoQDU-5l6aYvBxOj-4og5S1-34Cq4dNoLG11L4oL0HFJT79RCn6sa2awMaKIje2O9PRKOvstuoN5Zrt6ZbwQNRMgCnaNmdUcKrm7lOZCZrnpIIGdG3RV3o_Ppd5c9x0uE_U3d8dvjr63dHh09OvXnzz--eHT58dnop_v9JNYcoRzRa00gejZyI8s1XeVoTZlPjBn7sC0_J8Kaq1oK_jy3oCkwknk3XNItvoYcQcE0291HH6Hr_-1unXjcafqqNWTsgFmytpbo5h_dSArm48N8R9-2aQGu5p3pez2bXWhR8uCCWqs7efHnzz4vjV0ZNvj49ePFNVL3CJONZnNf7-5f6LZ4fPv3mmS2IsTBCD7gXL7e2nrw8Pvn11dPwv3a2YoADFAL2gJsIOnh6efvO7U-jo6bcHx-setKoD_hEXew-7Bs9hNfdzawjCDuhh8OdRZg7JP8KbrvUDpQ-sY3j0vyp1h1hVHXNHdgvKjq35Bi7qXOyzMcaJh0GXX-_pOib8XsjhLR5l22r3603pOnVZnTEk7Ov3q5r05-AbKQfq4Hi_dWnB7AFTtTNEulhla4tPh6Zim55Mpb-oUSnesV9jXrbpdy1d3KwuLrDlO3ZtTNlg169As3_Qz_yBzcocbL_LjbR1a9KJGk2ccatiH8ozIZ6pnNt2Tfzp0eU54gBeCaGtNTODx2zah2EzsHVEQPGmh7JYgflCsV9kekYEYuCiGQaSu8GBzYiBXzCTDVdDlQQxOG2WMufImjaDoIpOZXnEDOwqjgLcHk_h8MjzCha4YWiDK2YHoROGXuBq8ZpACRMkYIIn_kRa6KNqoe0xMRoTolvb83_sB33chIB5EJhLljpwj-tkLMlCL41tnsCsBkVk-1FuF2An88KJYt91nRgWZsSKIrfzoHDdzI09pxh-pD6gi7_nhn1AF1jrmZtwAroQ0IWALgR0IaALAV1-KqBLzKI0i2KHBfbPDegyGrsh1AuhXn5eqJeYB1nqu1GRJjmhXgj18vNBvYwrUoLAEATmFw-BScMC4bqeBzbc3xkERh2dsoz4hmTaqCYgLAxhYQgLQ1gYwsIQFoawMISFISwMYWEIC0NYGMLCEBaGsDCEhSEsDGFhCAtDWBjCwhAWhrAwN2Bh0jB1XS-KmdSZw1iY5w8VvidgDAFjCBjzywbGuC4L_MJ_mNfTHEtPDLcNRmRkeZ3eXm_eiZwnP7sCsbzb3GCberIfWmIMd2MUCvrwFdijyoLTHRvZKlUaAlacimu174VWx40CDsxUIYiaxQEwBJdmp3BTQEayzQ4QIcLNw2No2jyejgWL7F9m1VVas4Xov_XqlHVztpAzauE7q2-HauB-EURpkTpFHLDYycElse1cuCj9qIa2IvxmVMPPeQltj-3YfFeE82N_gfxHAQUEWZbByIrCsVnkJW7ou1GehGHs8cgPIzfwkzyFz4Ud-KEdJ3mWsiIqwOz3wQyInYHn6UMERHtu0IMIiGCkCTwyIQIIEUCIAEIEECKAEAGECCBEACECCBFAiABCBBAigBABhAggRAAhAggRQIgAQgQQIoAQAYQIIEQAIQIIEUCIAEIEECKAEAGECCBEwM8bEQDnDcsLrE3oUiVGOYtR2XzXmhRzBo3rQMHh5jLuxdLE7e4WRYzgbc0w5wQz905a8Gw2hVn6frSNtSs_kwuyXDZrjXRbSbqjW7W3cdNnXf5VqQaCZRAsg2AZBMsgWAbBMgiWQbAMgmUQLINgGYOwjJ_mxRy3eXcEs_IVmqF4wCOkofWrG3iYsVdV9CMlsE1xe9coPsqke-OE7OTyHDx0dMzFqaiqYK69TULqSOgPHMlboSC8MHFjP4kK244SP4oLzpI0FSZZLwpCV8HfjIJ4-JcYjEA2ehj_1_EKXfn-R8ErxLkfJXacZkmUhDwIHa9IGAPJxtAU89LcTWwvSXmQB3EcBPAYaeQFbhTGYe7x2B9-pB7IguPu2U4PZKHICu7mUUSQBYIsEGSBIAsEWSDIAkEWCLJAkAWCLBBkgSALBFkgyAJBFgiyQJAFgiwQZIEgCwRZIMgCQRYIskCQBYIsEGSBIAsEWSDIAkEWCLJAkAWCLBBkgSALBFkgyAJBFgiy8HcHWUiYmxZ5Esdp5n1EyALhDAhn8KA4g2wAYJANIAuyIUjBogTDY5Evf2JAgcqBnMJvovcHxhQY9WkGT79Z8jtYoj72Sgaj2UFQwXP5ToTuHQcy7SbrhqTzu6HJTU3SuoUD6ILD7-dtIdIWjXQveVBDaYuBBJxAHjC3AxW4nNlgz6R5xvzEC4KAsTS3_WwIVKDr1G8GFTzElG0PgbgRVdBV2H8cVIHr8CjjrpeEiZf5PHBcJ89yO2dZDEdeloCZ7-apx10_iSPugfPlw7HlMS9N4jx1boUq8J09z-1BFXiBnztwuhKqgFAFhCogVAGhCghV8JOhCvzMDXN80ML_5aEKMlkQzsasMLT4VItPD18fPXtx-nL_1fGLw1enRy-OD5-92j8--uYFARUIqEBABQIqEFCBgAoEVCCgAgEVCKhAQAUCKhBQgYAKBFQgoAIBFQioQEAFAioQUIGACgRUIKACARUIqEBABQIqEFCBgAoEVCCgAgEVCKhAQAUCKhBQgYAKPyegwoEKmhnNbzRmvmihVRht7dRmGd3tQAoJd-00TMAiByPTduIs9FnBEncIpKDL3v8qIIURSMWNIIWuYP9vEKTg7vl9rz5gthuA2uAEUiCQAoEUCKRAIAUCKfxUIAVYTjzLUh56UfE3D1IYa_HX601MjCYm2ARhGAjDQBgGwjAQhoEwDIRhIAwDYRgIw0AYBsIwEIaBMAyEYSAMA2EYCMNAGAbCMBCGgTAMhGEgDANhGAjDQBgGwjAQhoEwDIRhIAwDYRgIw0AYBsIwEIbhF4hhMKpquqL4bat4xkrmu_qHtisjnth1tWXk8obKfKMXI_b2AL1Uq4uU4yp68-aRg3ouTqbeP8ByUB8Tb-rLjzh_cfeDPX309u3wKI2w2E8oizgLgoL73j16Ybn0SFSEXBlib_bRcWe7-y8P_1sXTcdFgeVqDYeTuZzVS0PHzfn3E3Y2MlYfjEo7iZ0HH2vDsS_Q6W-0ZbUWcBxSxyNjNer_urF241jAWfFhYyT3LRAcGY1RkLLtaO5TsbIdiMnQK4Mgplf1CqNaRlUPmG8YvGpjX8Wi_iOGX1GnT0Qxsq7SE5M2HZqVa4_e9ii-aBQ-KlNVolgwWGPeAL-WuhvO6kbkOvDsqDEHAM4HrIzpkOS36dEUr0wuIXCrXqtvsT6Uwm9sc0j4WwOu9vhADNU6KG1wHy_qpRpKj2RlkFtJHizbC9xk-qUzanjTIV07PMkcjNdMdasD-zIlgT5L3m3tL9niA7-ynu8_mcAqgIlBl6tZzcBvk1KZDunQwd5fY8iiWXsk0fMnDXoJwn_HBdApFVFNhNg6LIwDU4Cjhz8d0qobikd1up-roqXWGf0aI5z8ezB3MIkp3JwSpHklAn8wo_pVP6ZaFRp0OqQj-3t-xZd61VxLZUmRs8aog-gSLVLQA4DAr7GgamDZ9EyaWkmGzNWm6kJPMvehxyEe2JALTsO6kt4cqQoxrVSZRrc7jAIHtU22Bx9GqZt7mR84mWP7kRcyL_WylMVD4EMNZ7sZfEh2FtlZZGeRnXUvO2t7rLSG6sq52nN3DNCuv6MHu-f-2I_P_SiY5MSzbaw7ieEu7qaJE-WRxwPXYTzyktjnLA7ywE8K3-V-jnWdeeiHbuxFIbjNwmW-1YNeQyone7a7Z8c9SOU0in3H9TJCKhNSmZDKhFQmpDIhlQmpTEjlnzFS-WODdJ0gDgMG_nHRvQWQQLq_XJBuK9ubwLpDscPOtTMT9xMM7-7COcauUljJ57svv30C5_7pq8PX3z4_fi1hs4TcJeTuwyJ3CcRKIFYCsRKIlUCsBGIlECuBWAnE-rcPYg1St3D9LPGdLB4GsYpc1XJRY4p2qXfsZqGDLCdWrg7YeODk1IX1-HGkQ03eSdWT-5b-oADAFuyinJVchZscN7Rgp5aw7hiuDgv2dvP4MZjd0sdDo--kanW76HHnekyqqyKFTczKRrSTLtDmlmghnBOMvGEtvMihYkWHyJ4-fmx9-rk_dTAShgkEXByicrr5TOl2UQ5p1SlWcsMfMD5WcIFJm7MzppsGKcTYqg0tKgc19Mw6V5CuUJPwnKMAQz_zXQanXtpFTXqRs7-Ts_ByTQN3VUB70hXtq0QQ89BOWL-grHUpycnakIF1TQRSANPrwNtzMYiJkYJYR9re0jUell6WR6yIw8JnYXgD2FYsZbPcRYlvsllUIc5zuebBQjCQ1iL61BglzHxeNjWGiltJC6kosuhuIqwDBd5r0NcEqwvB1C0oDpnrsOKD6SKSmSj_SmusCgLNjx4WRjjmq5mMAc4Q8wGO4Kphs5NKhCYkKkm4nWw2wZidwGxIwBY-k8LcqF0Ne1iBgtVWPanMMJuJ_NV1Jl39dGsEKdxuWx5059kdZZ6KHGYzHtt2F3PoygwMXXbXGgHMvoshwvbHgiUm8g8SKY91NJtVSnvtZsfAw_Ky1oaH3GYgHFHm9Bqe5L3lTJ2TCjmqLC_G7VUIQ-LxY10EJcEg2BdokWX9nitwlx9O3X-AqUHDRl1rYUAWxoE5CEQ34-wYumCJ1Txog8G5cV6CU3zB_iAiBhOxhHI4L5nAfCM5AC68nGd4OE5PKhPx1cHBZyLSD97-ZFlPuACcNeC96n5Q1cm8kgIGgeBQMBOhbdgFWKTlH9t6RoHKRgy_xHLCWSrxJ3wskpskfhQ4HuNeoY9Mo27DPMjuWHQxClmHrT3TZXNC5rOrNVj-Hvq_PUwQ18gTQCB3pnoQy2GU7UHTPBwJ9E-nzbo4i8Bl99QztuVuhH4n9Duh3wn9Tuh3Qr8T-p3Q74R-J_Q7od8J_U7od0K__y2i32UGZggDv_HrBhL-2q_reHjwYxZ7HwkUD-ZccYqh18UAIl6cPR0iflXhXqi2xcR3BcZ3e1GcARoxqoUf8h2BxhBvQl5KD46ljfAjN8uil-wMg2GdV8vyWhidKpYLU45hEzxjdqxn7bnf2QpFm9bbAEkazz04wIMZU1Xb4rjRVsWCz0rhucoa6UYWemnq-1kpCjAw3KeqmGVc8PJc1KG2BUMDWMZ9fD5ZcDTjYC0s2idtDU8MJHwy-qSfqEAjziAe-xh5EHXBG7JlbfIOkS8TLJCyVDClLdBSCpyJaM6Gk60za7dBMAZZEId-FiWFHTpxzBKbBzxP8iEEo4a5bIFg_Jntiu2xmz3vLVyHPXVgn48Ce8pj8L2SMApY5GVJmLhgqAQez6AhO2dOERap5zA3SmMW-oHrRoGf-nbh-YUbM5jN4UdaBzjFx068F9h7btgDcAoynwURYwRwIoATAZz-egAnO83sNMht5vMxgNP40TuGYYqcMHDB1eVpxP_6GKbxM9uENvWWvgpqkNtDm06qEWyTdVto00lF2CbCNhG2ibBNhG0ibBNhmwjbRNgmwjYRtomwTYRtImwTYZsI20TYJsI2EbaJsE2EbSJsE2GbCNtE2CbCNhG2ibBNhG0ibBNhmwjbRNgmwjYRtomwTYRtImwTYZsI20TYJsI2fRxs00-ER9oG7vOKFwsYclu-A4eZELIo-lD2JFhk-l1oIgIpwDW6Wk6euph3QrceKwv7MT7fKrdTNgH6QOIJMJQL5pqKuFp6kvXRLgalw4wahtQO83ZQHBAIdzx8oU2S5j4DIyiJC1dUefdCcTQg42Yozk8AnxkBDvVgTZwf-6EkHwU-Y6fcyRLbd92cxTyNbN9hcEsYFJmIONl2CF9msRcHQYFvGPLsPAp9N4k9H_7mw4_UB5_x9ty-9wOBWZylUUTwGYLPEHzmbxk-E4JiCu0oL_zYuQV8ZhAm8_sWy6p9yY3jDeEyJ1Vd_bP1-62xMg_5GiDCyhBWhrAyhJUhrAxhZQgrQ1gZwsoQVoawMoSVIawMYWUIK0NYGcLKEFaGsDKElSGsDGFlCCtDWBnCyhBWhrAyhJUhrAxhZQgrQ1gZwsoQVoawMoSVIawMYWUIK0NYGcLKEFbmp8LKqJzqKfwmhtAHlxHD7eAyctwGWAYefhJEj34J7wIy2jIqYu_dllFjeu-2jHLHri1QKYZZMWNXsKPGWjUVrx5kV8F494avDdeoU7x7qzoH2Y1VF4V1rf7-_EoZTMIbb-uo1t8ZdFupGKVhD9jTNTEZFVMP2M01uRWhz2BVB_fphuXSeVRZ0PXcR7mQPhebdVWOmBWSAcIuQAF_ripEjo3IxPFdL3WyjaVj1E_WKXp4aBtq9MGBaP_Zgo2NF4yRbZuZn9-waVyncF1WPPgYzbj7CkvktWMtz_H2QJF1iGD71NCFchfGNBHY4L4d8Acf77t37y744oKVCEgA6xVPp6V1_ARP4IM3J48OuqK6Xe1Nnjx6K37fxwtGlq2dZKDVmffgo8Y2RN6-fdWYBJbgrZ8Y1S-yiKFzk4ThNyJlv-BJ6ib22nixZtUoHW232dkmcOaGlbttM_wGvZbaoS2r6B92iPvd_WW7amGjz7B4SgRYRTJCLNdrVbAjInV5mEWuqEh82PG--dWbr_RR1AU8dHRqTw6zG2TbC7OaMYUeRIGbFw-_BA67At9MgJlUROw3VrnEb1RYaa1613oly2dGxutl3M39eF2-T7HQG9NxFyIVt7qYY783LNDBm0bVaMRjzuJ79n5c5ww8_by7UVrnMhEj2uA9OwWc8EU9IpsoZFnmRuyeo9s3ahVVAn__5dHu66dfCQXz9cFLEdxQsZXHj8EbryqsaIIpHTsmgyQLHT9ZG922yJMb5vK-ABY9v4nHmRtGDz7G-4Je-sAI3akTg8JJ0gcf9H0AZg_59tJluZypvJP0GUGKQtcZ1qAGcXYWh943t38h6dobU0WgDuuEME-DGU-sSjHekzrQK8aul2WVtYQBvS7b4AheywpdTT1gPCqcSWsJCilXGRTt4t-KjgDrFjtVPh1y9wbHsZ_nSgwCSj5flA2flNV8JesKMFclnr9eLfE7LSOdERxyCreTfTOrz2AXaGEvL2sziiU8MtBGPUI23MTBrp7yQtTtdI8mqzKHZlRmcUSmcO0mYZrtWLD5ahjvVS_cVFSRaSCJSP5cwrrC9OZ0yBPdTkZyf4vwnIrp9kpJ5VMYDPZiOuSlbsfZUdQzaAw1lBI9vrj2chv3bDrktG6xAE2n7WxRX8KjSkmyWe_-v77gDe91i_5UH9lq8YFrBFVVVxNQo-dc5ZYm8ioQ8iUs_g-w56ZDnuyGnr3WX59XpyvzpOfQyRv3et9cGi7ITf3p0rBugc_LORdvgZb5HVGvJasuhC476zM8LVHxOB2yk24ahaElNXqN5R_KRtaWaCNSbEyNJu8GMh0ygfo7boPFRq4q77WQ2kLmjddZG1ZMfweYjBo2nGCfKHMJ1-65KF4D_YZaYI4VYAPGSH9Xr7jIxEo56pSpUAcSgw1boljyNgN3KY4NPl9iIrbEMLzKS02HzIktujWQRZvJjUzibGqLqTWrx2IOcYC5R74S_EraLT1IfLNQXpI3qK3C1wRrKGlDjcvrZXpaFKqqw7MtU2tXhjrh2hkbWh3bUwGFeR57HvNYmvgxzzIW5KmXx_Y1PXs3Q-eRwSKkeWl-YS_0ptA2hbYptE2hbQptU2ibQtsU2qbQNoW2KbRNoe2fdWh7e8ZXTTgqx7TnBDsm96j9Yz-36EfhU42dMGAp_LsosKDZt72siELPD23bK2JuB07Ower3Mt8J4DDw8yzy8yD24iJx8jj2t3u8dW7V5Nix91xvz-njVkXKxTTjAXGrErcqcav-1bhVA59Hfhy6sdcxL_Vxqxor_C9__nfh4D3rnNrnGGMQ4Sthn05etu6Ttv1G6VfTMAJPj6dO4aTD9Kv7MrSX19UnS-sPK8lMI2yOvkigqJ2_UqkysCYxRqp_PKlEVKSXB7QcQ4rmoBNB1fo8DOxh3tI7EMVq1rYBoljEO29BFNs-RB9Ros4mSiBbl07Uzi4aaquzczUGdNnYIjvfMcA-kkipg_sJ2M1YIFaGjzEOO4a_zVw_yJ008zo-vOucqF9Yh22qoutmPYwCcjtjFVjmjeQLvB4Nnp5UX_TNurhcYkj107aCGcNbJWDUswL-gXUxzAaKIZH-oNwIZNgGm73wUi-I_WGGz8M-2ZcSzZ3CvFeCK3HRCkbl1Nbynmq6wZNBXJGGp4Ghz8AAYY3GvglShLwWKPcuH4orQuZEp2r3t-vppFobEuxABJhdIRK2EYkeXEh7_QlvsGFQICL1zWZXOIiNZdu7eQV_DhaKL4TDpnn-JJa4W6jm0AYyvIp-cy3RKwTZEQaO0XxlsCryIMrAShvmS-0P6zx_hWbH4VdvTszp1ar0t-li9ws9tzhJiCPoYIXwoZ0ucenGjOHv8glVfAjDQ1K3isvbbY_XqY0Df6EQ2utfftXe0aPoRRtmBgduVryi8Fc7reKqdmbF8NtpVZ28fPnGNKvE9TpGANevIdbgs1aEsmUdaICfdKxBNf1sH8evI1kyorIxfpUkgrsVnVrXBfJdy4aeouQMR5V1QsSVKhR4-zyHX1mTyRfWvvz3S_np5UvxHxiQ-O_T_Rt4rxJYUyyLGZrmo9yk28acR8C3nmP74OCkaRQMU5TuN5pnr56bqdy6qi-Q5AGP34bvbJJL9J0YSCGyEhhUTLuj0p4xFdqCfQgDhD8k54eozMlguSNVzAaxVns-tRi8ZUtXI8M3om3rYgXLu2DIZDG1vq7bUxe5xAX6dYWaKF2A7JAYHWG87UnYlZAs60l7TCKoH_nMwC_SFDkGOF5RF0imSNEePgCspLNScK90ssjqxXwl0qpimPJEshrMGeKTjKgbN4_cII-9xOuM_OsMqLC4loLMcd-QHo5fGCamGHeVEC3rv-O_frBu8c9QBvNWDU0nn2x9_bbXbnMdXCP--5d_-59rdVnniJ-sZ_neaAvt3e0_gl1hTVX1b8XBRrsh9xpZ1qnxD174-eS2_3yxuYN3u_2Lz28tywt-k17KvSAJEt9PmT7sjFzYdXqqW-exGrjSLM2B7S0reGbsUvLdpfVyOYMtjzQ452UB56B8J4HxdqFGoOwbscGM6GQNjYmZbrmxzcildiHGzvrQz8PEL2w_0_BTI7tm2ID3TIu1TkjgxmnBbTdh3SsEukzZdSfk1imuXM2A4hPcFwDfNsFUKrS-9MGYJYqKYK6w3z2pZxGe3bRvZ0J6A0W0CH38YSVUAewMYZKxa-Fk4Q6h24O8Q6POWOG7RWh7zA5Yx4HfZeBGbazbpM6EKPbbr57or560Zzte9WQtjdH-8mToF2XetLQtN1o0EmMsDKU5r7ClUhpOinayMUctrIkDaWsc7htfPZFfPWm_mlgvb9jaPs8j27WTTIaXpWve5QuNZOFdE33XaQfwwMVVs2MQggteI8nNYUpAncjVleANWygGnbyUVUlIR2DKR5BHdSRGsCswzVSvFhmXrPOS4F7Vu4otISi-hS8h3tMgz26BTJUEHcpQlCTdguNG8XSr2l6DcWlkJduh44RFXtge116kkeVcJ52_R3qy5UJwCjtL4H9Z3rF0dhlLM95yx1RjxyWvKPVO8MLBhSCiIy1xqiBK0pxUGAnhs1xJVVBHCENSzkTHI9-tlan1jaAxVS3stJO0A6NVHLNrVKxChu0ZsNXba-IkDuKsYI7dKR4jg9qFVO-c-lQczi1fxw7OQEfB122VVmYtsX5lCT4JpXy7TjW3qpiwa49qUFuCybvkwijZ7cqMdUMTPXoVYbyZ22AkduKxwo0dl9ueDvsZid02wnGPjOw6Vy--9GiArNd8m9Ha6lCkfmyVl7IMO10Jppcr1BInFR57WOgqqXy3WTqu64aF5xZZqpeOkRzudvpt8rz61UJBkbIgc7ww6-wCnfptdfU9srgYHNQUxSeVoqRAAQpql2vsxZLDSNLFIOFLl6Fdo2dvFI2xpqLoZX3RbDGK_kXSoxhUzR3Xs1A-DcZN-xTB-vuzdIZR2Svt-yI7Vg8hnzFCuTh2IrD9wjTQMXQjqd2q03vkp9siYqQQFpQwUsrfHn0i3xy0kI5kLil-RQMbLG458pgiMa40sOUAJB-qrulV7HOaUMn6KG-X6HuTkZF0_yhvMjIS6PQmI3qT0d_Gm4z63jRnFF3Qm-Z-7m-ao_fu0Ht36L079N4deu8OvXeH3rtD792h9-7Qe3fovTv03h167w69d4feu0Pv3aH37tB7d-i9O_TeHXrvDr13h967Q-_doffu0Ht36L079N4deu8OvXeH3rtD79352bx3Z4ImHGzxgdfv9DKR9aEi9tYKfiSC4tY8fH2UYg_R2XZkYA_R0zUCr15CrN9hsNioFTfrfs0y8dvx9fXxWt27p-3oqB6-m14WqYfvppf8CSv5803sqK6_Lbdb1_3M68Z-GqRC_prlfJiZWEaFlGu1vjCnQ7tpsCtJ91qKKIeCNEqsCApDRNk2AZyqem-A7BWzyMtyk7zX2G2DIzn8fs6qlpzYQDi1dMs41805TIyJY-hFqxjQlJ1hXMoa9mRox25Hjt_FXTVNtKSPFczp6CmWXeLsptU7HdrTNy-XAqykCebq1zwlIyqsVs10aD_fZpkolupBYmoUeZm15QV945kO7fcbOML1XF5NxM0bZQQ6cCr54idwck46iIAIYmwsT0MHbDfhhm7YmPG2jEuDAgZolr9m73nPybJjzKGWU_uGgfapDUlrPVBW5msa9NsAKnAKBVD7dnTJfuykfhQ5LEkYt4vISWMviGLPeE0CPD04LgLUgnt1IveqqPHQeJT1lccqplASmitZ80zdzJVMdgjZIWSH3NEO2Z4NXfPIdeRx8Y_91HAfhxrPhm3oBn4ehhH3vTxxWOxHRcoTnnKXuZnvMBtWNfdZkvKQc9cBMXLbjxnPJAR74JH66PB8-F8PHZ4dJn6UgC9GdHhEh0d0eESHR3R4RIdHdHhEh0d0eESHR3R4RIdHdHhEh0d0eESH9_OnwwttluShmySOl43S4d0iBjliFyZ5FuVOFufM-ShkeEeCWEYMTDKtbOpbnVxqpMBkVB0MDuUk9KWyTiqFmtRcdDeT6FnDHHoIBNqSRC_PHJaGgRukHQzir0ai16ITrX1Jeiep2aR909ovXUrOJNnTdz65xZ3fwY3fmepot2WgU6bdt2jZaQ66z6X1o358jtaOScb3-d25-L6TX8k-u7-fC4q-A6Lo-xlQ9HlF4PHcTZ0wc0cp-raN2w-rtMwJo9QNfdsX6JYBer7joZyneoVzI_J8Alfd7AlUmMA4oNDNElWBCkFVf70gFS8z66r7q1M73SiAtiZpIEztHVkDf2Ots_udVMY6myEqCpVMLgIbrRJUJIKmEkUtKNStHq8ombyBo83Lcy_049TNk3SU3u_IEH8PWZ5J9dc9_N8t3V_ug02URyljNvsr0v2ZVH8ihHFDrl_CC3EB9lEAWrdmAHScLC-80PPCDqrfywC4RWaOuACJC5C4AIkLkLgAiQuQuACJC5C4AIkLkLgAiQuQuACJC5C4AIkLkLgAiQuQuACJC5C4AIkLkLgAiQuQuACJC5C4AIkLkLgAiQuQuACJC5C4AIkLkLgAiQuQuACJC5C4AIkL8GNwAYJ7C5ZKM0QGaMC0OpKSbQF8PxtSnB5ittNNFJq4QJkailQJ9Icsz2_zZCY06PL8aoIXyHolhudPB-qTUpW0WDto1uFGWYFOQDddAAavDODJxIT7CuCQCCdLDGAHJhQmdNFB4jawMn1AQx0lwJEslrIQrR-0ZBmYpW5uTjcRKKaYesnqWvI2YTJcoverxzUpykWDVqFcItCnsHvgmVpgdeeeGOtLOTE7HRmdgl8KX0MKN5Mw_hZiDWLrHBk1ogFerm9FKZOkxIRH6eawneDygp3Js0xHGzWmaNJiOMz12I2kp_b8drRcLAtZhAUDts-cHNy_jNtREDkmSxmYB5leOKBTP_BWUHAOXq0R65mbU1Nyaa6bmym5_ma0wfbsZz1cQu6P_VRBH4UeKbKDxLXjICmcgiXczuzQDQsnhkHEnh-zIHT81M4zHsVFGPlxkjEepa4Xhx5Pw9wffqQeeiTP23OcHnokOJ1iv3A50SMRPRLRIxE9EtEjET0S0SMRPRLRIxE9EtEjET0S0SPdhh4p9ME7iGzw7bk_TI_0qze_VwEJ6eMjM_7QdIgh4I-gHnM5L1L6puS3CR9hDnYmZkJEuLZaLiJ9IyNNfRxFWF-x4NvwDg0A49fHbUT5ZQhEFJyOnPnEBkRsQL8UNiCfBcyL7TRlafL3xgb0TJ_zRhBY3D9oPugjXzXxSj-IjhdLo8rkCUITZ40DBxsZYA76Qd6JqJAfQHQD30vBC2vhhw4Hl1790DIOPen76YlqbTqxnnV_viK2IWIbIrYhYhsitiFiGyK2IWIbIrYhYhsitiFiGyK2IWIbIrYhYhsitiFiGyK2IWIbIrYhYhsitiFiGyK2IWIbIrYhYhsitiFiGyK2IWIbIrYhYhsitiFiGyK2IWIbIrYhYhsitiFiGyK2IWIbIrYhYhv6-GxDBmnKxKw_HaIfMsAiD8sE8rE5R4yejGrurqdtC8dveKAeoqN1KV6_X_HIHCi6GBEH6KJxsOPwjNgR-C0-OUPbpUN17ShUwUbi2igp7aq6LXO-p0OyHxxfy3MjQHUwKtCHRq03mP9gI-Nf7ckriu4wSQ1DBwnlE2Fs9TIWmQOzGmhIoKtWc_UIa_AIjR2SNbDGk6oUfosxVBW0Aik3HZr_wad9youykg_buUgi-yGZpv5Yg5Wea_okvE5MkIm4OxNRxQUTURwwMdCKyFfoJgk4n_nQ4wxJr88Fj5OwdwbkutaayE4MWr4bEjQGrA7wuq2gGJFoF31-35b_XZMT2MeZCIqjIFQ2AwV2OwamKEaonM1tN3fsKHaj0I_doki7uTrEtbeGhVgXh4Sd9U2OycKkKXVuZmEipXhrpbg9rVYPOZL3Yz_30UfhewrADEbiJlh4ruOGnus7PEhg0IXDChGhCcLCSdKCFWBa2PA_m3kFPg_4uamo_x94pB6-J9_dc4MevqfQ8X0wFQrieyK-J-J7Ir4n4nsivifieyK-J-J7Ir4n4nsivifieyK-J-J7Ir6nxPUcnkcs8A0z6BfI93SwGa2UPCIdwzwvlmrhq9CeZqHfjPEpS0jVVWjufhknrERVtwR9FAImp4-tLqY-tV6LY01U7KlgeiMJQEQZB4hnMwzddLoPm5eEBhjWGFkpUZH5eRYwboQetuWakkZQs0rlY32rTY61qVSnK5yvzl3ppOBe966EUmCnYL8bc6tpr-Bnt-fnJ8aoTdqm5gdorh3S5g8u_sCxKnJNLt-9QeBaXyRYd_IdDtHB8Us8eWsk5RyWx0VZidp76aAaN-HAXbzppYhHKtNQlUnh97wBxQQddbd4cIuHP-1fM8aW0prEpWaMS1g937nyP17_Az4zbTVDkehmDpx1PrJO-Afu-i-d3L_Ce_bbEtnNSfvKvf6rca93_dcD_eu-WKiaW-jzNfIwWA-vpFnblnZ-rjEIxvNco__6yhn-yW2f9fpPXvuwG2upvecrF_nAvvihY9BqursO1I8aAge_HTjtQ0KLk2sf3fYZxcd20O3Hgfl9CgKRyshUOUZephMMugSHgnVrxtuKpU1zHRwdWbqBBrtE60monm7mS2jlS6HR1JoWGS_lguTtjd2EbnpHrUdk-kltPbwxVrGov1z7tL8mgZdq-QsxvXSND995YsL6FHc7B-OXiIl4Jq5Q-h2-fEm0b39ftG88ybGg1438JCLat5-K9k1Y4-0LilKO1hNm0hu1qIaz6Oh8IXpDxlDX07spXEyEckQoR4RyRChHhHJEKEeEckQoR4RyRChHhHJEKEeEckQoR4RyRChHhHJEKEeEckQoR4RyRChHhHJEKEeEckQoR4RyRChHhHJEKEeEckQoR4RyRChHhHJEKEeEckQoR4RyRChHhHJ_f4Ryb3_8_8Puwds)

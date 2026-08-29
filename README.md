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
Each conclusion carries the record needed to judge whether a downstream actor
may rely on it.

[//]: # (ob:836f405e)
```mermaid
flowchart TB
  C["Conclusion / decision"]
  CA["Claim A"]
  CB["Claim B"]
  EA["Evidence A<br/>source · version · provenance"]
  EB["Evidence B<br/>source · version · provenance"]
  G["Governance record<br/>verification · authority · scope"]
  R["Claim relations<br/>dependencies · contradiction · supersession"]
  C -->|depends on| CA
  C -->|depends on| CB
  CA -->|supported by| EA
  CB -->|supported by| EB
  C -.- G
  C -.- R
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
context.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzU1NmIxMTVkZTcxMWIwY2QzM2VlZDI2MCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjNlZTg0ZjJlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9hYzZhN2QwNjQwNGExZDRlOGNlMDc1NzEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2VmM2MyZDU2NDRmOWRlZThmZmU5OWQ3ZCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfety3EaW5qug1TFjW80q4n5h97iXothqhmVJK9HunRC1VAJIkLCqgBqgShTHdkT_mv27sTExjzCvsP_3UfrHRuxb7DmZCSCrCIDFi2XZfRzdNqsKyEyczDx5bt-H7x-waplnLFme5umDvQeLxann-bFleSkPLCs2k9RxOE9t33yw8yAu08vTND_j9RKurc-Z7fl7pplYzIv80A6dKA0sM8rg5jR2rSjyE9uNMjfxbMaixI88brPUi9Iw88zU5aljewm0m-Z1Ur7n1eWDve_xw_J0yc6ghxlbYlc78EfMZ_DFt7zKs5zFM25U_H1e52VhnMP1ZXVpxJfGi6oss0XF6xruWbDkHTvj-FBrX1fldxwed1Vhg-fL5aLe2909y5fnq3ialPPd5JwX87w4W7LiLHTM3bW7K_4vqxz-Pl3VvDpNyqLmBchiWa34jzsPzjlDIYLAQjez-QP5zSl_Ly4C4fJTlvgsSE3fNV1mgQjChJuBF1g4srJa4qOdzvKCw8ibGZmd8sxJ7NTzXTeLUmg8y3gEok7l46jRnSZsUa9m8MA2jjMpq7R-sPf6-weq--8fwCyXVY1_yZ95ehqDyF8_eL7gxf6RcVCm_MODN_AgzaKA_l8e7j_--nA6x85uslbYclnl8WoJU3QaszqvccXwWXbKahDdkov2VsvzssIBvcsLbLK-rJd8Dr8UbI4ztzawHbi_xil_sFesZjMYZnIOc8TlU8azMnkHt_g8CQIrduFymJ4l_4AP8fn__Y__8f_-8z--gC9VTyxNuZQfrCN-Ad_8YWGwWX5W_NPJgwQExquTB1-eFIbxh3x-ZtRVAt_j0Jf17qw8K6f1-7OTB3DHEr5X6w6aW14uxIpjFXvw4043KpBQFEU8XhvV2nIdHNdv15e16gEXFizStU4Cz7Xt0OS36OT1b14Xi7kBexAF_ObzZl_As0_r85zP0nqal7twze57bUegFL4YeWzu-0Eahf4tRvTwodzsPDXeFeXFjKdn3MiLrGI17LZkuaq4kZWVAWuoLMp5uaoNWCmwbYplPTIik5s8SiN2ixF1Vxln-XteG8tzbhTQgnG-mrPCwMFg9wYzQIeA8kE1xYr6glfGyIgiO4sT61az9s_lqjJgNlKQh_GO80Vt5MvamMN2mdU7xrIs8T9zPgf9uGNclNW7GrQi3zEWfGyxhpYX-4GT3mrWXi1BSxjnvOJ7Dx8ar6tVIeRkTj3YLItzZoACTd7VeNWbz3_bfZicjYzIBw3oMz-8xYi-NJ7kS2POUm4kpfjXDE6TsmJLmMOptrfgmncwqTk0PwM9wIuEj23oLGBm6N1m1rZXNKhvkxmvd-UUTsTxMBmbuSyGYyVI1kZ1cF6WNRezsGDLc_iDoUCWsEhr4xKXEK6MbDaqhH5rbNtMeTGupThLIsvKrHsf4w_GUYbXGqzif_vrfxo_GN1aNH44KX6YTCbi__Cn8WiVz3BosEHVri27YQs5bwg2gBPYWh_0n8sLA3QRHFmpgd_mxYrheSd32jXivPbmERFGjhUwO07vaTTaHqhRf8R8ecF5YVTsQskGmwBJpWKCVJeg5rLVcmQxBmbqp258XzL7zetjed9k7T5WJef5kosDYU-M77ysG22IH7HhkVHGmRt7Hk_uX5Z5bRTl0hAnA67jJeicsgK1XIEONmIwT3mRNurZACN2ZJRukqSeFUdro_yvrfLcM87Qfi7UcPHn8dV3za0jay9JnMDn9rolc1RAW7PZuqYfH8JvjaGbRjpP_SzKbDO8W-faHOH1ME-LVTzL63OQAcwxGDmf1cZbPNnfGmhiFnw2NY6WBhr_Y-s9tqKAJdbdBvf27dv6_KSYv0tzcbarkU66k9L4x380krT3t250eNatjc5j3A25dcd5ewvn0mrxFk5JcaPcYcrqSdkCDjOhJi4q2JIgw2k3yN352PL2zSy07jqvR3N0oUAvxeWqgB8NOMn5nC9hd_EP4ic00ZQPs4MCXOChUxbcGDMZwziKHceP7mVei8UHYzIpyomSoDaNBlyaotlh5PJBTk7QLChgJk_nIzNrm1nMmc_vNr5DlpyDBpjPcf4WFZhBcnJxSEu0wyuwdTlKFRzt1vIFDbmYjlq3iZ8Emb9ubx-qBwWbNBeHPZdTxmCmwG-EkYjBjSmwLZsY0SWO6YP9Fqb3OrKjQiwn-KLiZzlIp1J6tQKzE_4EbZKWWWYsWf3OuBCWCTPSMlnNeTEixSRzfT8M_HsdK_h8B93IxCaeNOOrl6v0cg_2C4gN22u-t-xdy4bdPzJWBmsx4Wlwr2M9PgctXa8WuC_kulSu6kS4WmjIzTnq6ryeow4X9iMKGRT3mFzTMLEyf8M_VXGYVlXgHn3PCyY9grFVec2tY1ZxYnPPsZ17GYl2wLFZXYIhDdsZ_l8LY2QBpl0Ta5p0LYPZPTW-ZiPSsk3m2Jln3ssYpW3erobXzYjapcY_sPlixt98rv6od9tBj43R9pkdZeu7-i-4GvL6b3_9d1Ru0i6DD00U7JpJvf7uMXMpS6zEYey-xqNNrYrxGTWccglaqrzdZAm0m6dsKYz1ZLbCnVLvjIjN42bsuPzexAbWUlpyZQCvliW4cnkC55Gwc0HpoWsB62S-WNbCIC7qpMrFh9EwGiw_k7Ng_Sg-WFUVGiBw4C1X17ldVy4emTs3Mu0kdsJb9nZ8Lk5yNEEKnJ6Uv-cz2H3gy8pgVr13Ujx8eNVYQStl7EiNkihzNiy57YelZlVMDTglrLF8Lzn4Akx4T_Cp5tX7XISKZHgJnZ9kzEMJU7AOvHhdgT0p4am5jDaNzYp-3ciEWEHqx6Zp37yPifF6X3MUhZGKkZ6zSvp1zWH05nM4jOvd_ZcHfz46Pjw4_ubl4bQbE0hq-eDHNztNSP2BOoROk4ozGdIWvzTxcX6aZbYTO6YZ8gTc4cBKPJex1EUVCvIXgmz0nor6y9jhooTRiSRGJXrCgHfzCePdbzBdMMuTS60FPYWgNSKSE7fMLtRltjzNYBp4JUxCcUcdW3ss9DPTdP2QJQFPrMAOkiRM04jxwHUsZtk-bJwodh2TR36SpUka-2ClxpkTMtsRwR9cqSIZIWdrzwl_BEHX4pyx_YkZTuzg2Az3THPPdX4H_zZRakri6AvGXsjjKIAV0n37_X2kLsRyk1mFc1afoybILJ_5buglPIMLRBtaokGtxLtnEFCt42_w_UWeLs_hlzCED-c8Pztfqk_Q5h92F1_27EU12tALfBC05Uem04xWS0Co0V6fV1DNeRnP_DQLktT0mua0VINq7i4ZhO7qi4uLKVzyXS1ScSqFp13-xUmhOkL3Y-tedvFq7OqPIpP4T_jxxr0eHHV3bJUv3GVCb9a7TWC03k3y6eV8thszOAA2Hv1uTcohPgWVXdR8z9hfoEk9safmoIzEGHZn8o6JugHvmMSzVTO4p0cHh89eHX4xvNh46sIuSgPXS8NmdWhpH7U67pLNmT58ONI96J_AZ4nlpknTvZbjuRKYv3nqZlnuGQ8fXpznCbjvmjkFVvWlcQRWGBg1GDUqL3Zk7OP88o8PH2K8KIbTSDPP9HuX5UnRmWt1AmbBTrN34MwVql02J4-wHRxxATYxtJBytOMvl-fo9VT8O9H6zkmxKuABy9l7-IDxjrzCP8BnglbRb9_Bp1wVMuea_ysMKAMD7Er0bzosayuxQWWGmR14rSLQsldK1ndJSs3zWpqq8tHZxUnRmkVruRo56hoEP1PRCFZVpZguDNsq21ilEfCLegX2zHuY1JOicTBAHBk0dm6otPLIkzM_iCyW2b4rfHDx5FqWrF3kt09-qVmYqFn4wvg__xt2dM1lTmRbU2WeqhvjChcH7CIGomCz1qlq1MZN1Q7My4qjGr3445KDTQvWzj_BOoTD7hRktSx4JZTQsATTIPT8hCced-zuBG2zekqCd0nWYfBqgbIZW8Gmx7008HksjAl5MnaZvBuf4_0JOphSGNyk84MnvDgDq4vjpExgdZTTRdGd_Ucz0ApLNbtlBlPW3WkITYmrmoHzgHMqPGZMWimDRjMVLNs0tzAPMstlSRL4tuMG7WLuEoeNeXD3jF8j9DCNPM_O0tBrzREtCaj6u2v2roJ9PlvmE_mx0T8_GK-fiK3Vr4bFkbOuBa7bl6L_V-f5YiH6N87BMlMzrnR1KxXs_biS-mnGz2AbwnpO2xhbln_Ac08LcLxXZ-SkPSMncv53xe27qvc_o3cPnau4IShXllQlbIoFL6EdlIUspKmbEbA24NOFadQw-uIr6qemv8P3bIb5L-gSH0ULtFVGMmO57OclzLxcK20yZS2a-OZz_E8O_ayFGtsIlLZfmo6PGrUnwnvywBDZs1ocZqw7PXAAr0BZXuAS1dREeVE08Ys2HgHfDenOH_pywI1VbYUOWNBm7LtWt23atHC3bW6T2W36cFPTjQLX4narn7Rk71Vr5sb5WjS01m2ekwINmbyAjZYvp8Z-mz1p0xGqZE4cPnCuzkGOXYCpXaq_P4G7lniGw9oAtSgtqVoMQxo00KJcSNAQ2H5lNVc75vfdOQ6DzfIzGGV6UrBU2QOGMlqWl9ix0ZowcPuq5iP6PspSFmRZGkdO1LouXVpayfMumWXc57_XV1z3Mxy8NTajaRxhM8Zq3On0zeftOdJ1tbvsGcxEv2Ko6ko9tJ1yHxxTnoaiBFE8tJblvrqIbpyorjDECKctWKFw-LzLcTeCpVbBvMBfDE5ElS-VAUoUxhVjt7FrcXnM8ownl3Bbc8S8E4Zaj8o24BA8y1GPoeqW02-8klYSmD3ZajZbmzfRfLeO2o4GFMDIUvJ9LwydOPEjtzVgtKx8t_1vnlpvekiZmwSZGUcBa3rQsu1tDzfKnLfmV-xkjue7iTBYpeHTJdOvrokbJ8axKtZ4AV4JXOhMLet34JGAMScn-Bkac7b9u70R08wKgygLojhMWytBy6irEd4pOw6qDqxdUD35EhOxc_GXMblsPkihTiY12FqTlL_XGvkv-NDj2dvJRPlv45eJBDr8KhU1WrkfTgp4rJ4EbzN3tgumc-qELGvdLi2b30jmDpl5OM0z2PbT70BfvZ0a39Swl962Q5wxcDnf7hhvk1VVl9Vbcfa-hT7eSvsJdAecHU12Thz7sObremQzeTZnYeDFkcnbs1SrAWhy2HfI56OS0RXHDvrb4vQBb2q50ziIDH3qBRxOeRMKaJVF437_Czg-y_YQxScWukZED0RF9cii5r7LU8_Heu-4tRm6coL1RX3b0gCwdIX11k3oFgZlCsp8Wi5nCzHpJ9cs2ka0E7R0lyKhYZyIBEei8g6dpMEhkaObTNpRH3579Pjw2cHh6dFjbAMnx8ARwAfVtDJG9sBlBmfyOmGoiTx4_uzg6Tevjp4_g4bH71Gm-dod7ThxzkERTORFMBaxFPaaj-MtNytj47nE0lAPVa8SsFnr8pqWVvlaI9eoBduMY0RR-IndBt60UpAm8X6Hso636tHetnGnk6KNNxnXhpvE0YtSmMCOkm7juvcVX6LJmDHw26CzVf5W5Kbl-GZlAv6SmjXYgiswGTadMWOhGREnRZNAAY9hcT41jsXh6BpvNQl3scfpdPq2lctZVYJOrvhc5MiFLcrgWZmBsQ4waEDhzPMm_lKvKtA3o1anb1uexWLLsdqYpFYH05kKty9iaYOvPncZN5PIbw9Nra6lrQW6fVEK-ompIYEWGGS8UhGirFSO-TRQqaBXlzN0J1SpyLLK2azWLeQJ2Lw4iLSLxIErYdQl3mTCPVPjEZwo2HCai2C31sdaD7h9LBsDn2p8k3bQstuROYoD0wlM22Wh3R6qWpVNl9S4dYmMGmo7-DUhiAfVzH8VRlr3jEUPk4RV6USlxDBu9MVNHOk2BTbiL5hgY6YsTC2PtZatVsSjRHGXChxVDPDwIZgKDx8a9XmJgd0NVx2ehVeiRADOOHyCWpkvCVuwOJ-h9wcatU1Zw9EDrsgc1TNoS5DB1GhDEK9FkYuQn6HSOTcKP5ygdwrPA9ZsWu-A2wDng9j9NVoOWEqzVm6BOkR6u6t5jcOoOTohxmLGRM1NinoTVlG9QDf6PW_GVCudY6B5AzZVM8K3rT4AK7e8KGSUpdENcMXIwnYdnpmJl7osbUPVWplTp3xuXqvUHDw8TZLQ8Zkbtj1o5UtXfYkb1yBV71J8ahQr2ht5clL8-fjrp8L5h-2A2hEjCEKcCgworDkMnuJRjkboFXwgZuZRuxUYY4Y104SDZGi108BZju7rPlp6cGiBEVyUIpzRGjO8kHUcYjiY4zkptIDtspT-7gd8oPgSjW0YljSRsela9FSuxOm15DKSBzeJJQBPi83Jia9xVUPPY7PtpJZrmlnqJW7WGQFtmZaai7vUWjWxwE6T7IgBwqJVseHX7UrabybyW0ueL_C38rRfPH95vP_o6eHp_svjoz_tHxyfvnpxeCCCbmgWvW5vfdGJEv5clkk5a511deeLl8-_PXy2j_Yk_Hn8_OD5U9GQmNzLcoXGOZeKoK2_Wc-doHWQF--MA_uFmGjNMMCgzt_--u8iIKL2XZmdFOJKEfNY5lIZgbGTn6EekOGo-jxfCM8IL5pxLL0CrwujNSNpJdN0Uy8IQjdpDQWtgK3bq7cqQWsUAg8zFvi2a7raSddWpV3drjeuK9PiN8I9gAWigjzio7ICDThFMXCrYoHYyxxmJm30Kj5Z64t1IRtcHdLoxBRdp7W04Deql8afA0N7gV2qw0mGH3FKVvitqOw4UebC2L7yrSh03dhKPbPdV1qNXGNY3aHKLX-PYpQxQpgxkFnC6hXYvHGFWhLux1ScWFEcodEGRiWmxuEHMN8KuKxNMqR5DQ6UspQKvPakkGFa_XTtBJryJFei0Yesh9HE6GCONlKNL14efbt_8M-n-88enz4-enXw9Pmr6-NmGY_thFu-mVitq6-V8WnZpi0q8xqt51qxD5abnYXt7GjFeq3Fcof6O6WOauNv__a_2g0wEdf2Bb_xspNCutuJCh-3yXvRRhcK7DxmPaKwXo4AzgdaKVOwlo5bb0i67jvGwdOjJn5qfAN_9hzgOyrsLjfLSdGcqbvyPJ2o47Sq0AFkaPC_Z_lMbCx4pJHp5F6Wuknq-Jnntr5NV5C4Xjl6qxpDUN4Cpw47QpmEk8WqEuGHJgcEEourEmw9nqG4YaWqBNisxAQr5gZUukWUyAhfUEVshDNoiMo4HKBKj8tU9kSlsrtsuci1QrewMyshHJEqnKhUIRqeci9NMXk5nB7dUQYpa_b9BFYPm0Bja6l9UV6Cikt8-olS9GNbNYKNFQR2aHamo1bW2W3Va8o1m9Mt4p6omQBTtGlOq-BUzd2lMhM0z0kBDbS1RV-1-_GpzJvjpsN9ou7-9vDl0Z-ODh-ffvXs-V-eHj5-cngq_v2ybQpTjmi2oJU-GD0T4Zmt8rYizKbED_7cJZiW50tRrQV9HV-UE5hMOJmMKxbZRg8j5pho6kUbp-_x62-cft1o_LE6auWEzNlCSXNzDOunBnR17bkh7tvXg9RwT_0un82utC78cEEoUZy9-fzg-bPjl0ePvjk-evZEVb3AJeJYn5X4-5_3nz05fPr8SVsSY2CCGHQvWG5vPn91ePDNy6Pjf-5uxQQFKAboBTURdvD48PT5n06ho8ffHByve9CqDvhHXOw97Bo8hdXcz60hCDugh8GfR5k5JP8Ir7vWD5Q-MI7h0X9W6g6xqjrmjuQGlB1b8w3My1TsszHGiftBl1_t6Som_E7I4S0eZdtq96tNtXXqsjpjSNhX71c16U_BN1IO1MHxfuPSgtkDpmpniHSxysYWnw5NxTY96Uq_KlEp3rJfbV626XctXVyv5nNs-ZZda1M22PVL0Ozv22d-z2Z5CrbfxUbaujHpRI0mzrhRsPf5mRDPVM5tsya-f3BxjjiAl0Joa83M4DHr5mHYDGwdEVC87qEMlmG-UOwXmZ4RgRi4aIaB5G5wYDNi4BfMZM3VUCVBDE6bpcw5srrJIKiiU1keMQO7iqMAt8dTWDxwnIx5tu-b4IqZnm_5vuPZrXh1oIQOEtDBE9-TFvqoWmh7TEyLCWlb23N_7Ad9XIeAuReYSxJbcI9tJche5sShySOYVS8LTDdIzQzsZJ5ZQejathXCwgxYlqVm6mW2ndihY2XDj9QHdHH3bL8P6AJrPbEjTkAXAroQ0IWALgR0IaDLTwV0CVkQJ0FoMc_81IAuo7EbQr0Q6uXTQr2E3Eti1w6yOEoJ9UKol08H9TKuSAkCQxCYXzwEJvYzhOs6Dthwf2cQGHV0yjLia5Jpo5qAsDCEhSEsDGFhCAtDWBjCwhAWhrAwhIUhLAxhYQgLQ1gYwsIQFoawMISFISwMYWEIC0NYGMLCXIOFif3Ytp0gZFJnDmNhnt5X-J6AMQSMIWDMLxsYY9vMczP3fl5Pcyw9Mdw2GJGR5XXt9nr9VuQ8-dkliOXt5gbb1JP90BJtuBujUNCHr8AeVRZc27GWrVKlIWDFqbhW815oddwo4MBMFYKoWRwAQ3Bpdgo3BWQk2-wAESLcPDyGusnjtbFgkf1LjLKIS1aJ_huvTlk3Z5WcUQPfWX0zVAN3My-Is9jKQo-FVgouiWmmwkXpRzU0FeHXoxo-5SW0PbZj810R1o_9BfIfBRTgJUkCI8syy2SBE9m-awdp5PuhwwPXD2zPjdIYPmem5_pmGKVJzLIgA7PfBTMgtAaepw8REOzZXg8iIICRRvDIhAggRAAhAggRQIgAQgQQIoAQAYQIIEQAIQIIEUCIAEIEECKAEAGECCBEACECCBFAiABCBBAigBABhAggRAAhAggRQIgAQgQQIoAQAZ82IgDOG5ZmWJvQpUq0chatsvm2NSn6DGrXgYLDzaXdi6WJ290tihjB25phzglm7q204NlsCrP0YbSNtSu_kAsyX9ZrjXRbSbqjW7W3cdMXXf5VqQaCZRAsg2AZBMsgWAbBMgiWQbAMgmUQLINgGYOwjJ_mxRw3eXcEM9IVmqF4wCOkofGra3iYsVdV9CMlsE1xe9coPsqke-OE7OTiHDx0dMzFqaiqYK68TULqSOgPHMkboSAcP7JDNwoy0wwiNwgzzqI4FiZZLwqirYK_HgVx_y8xGIFs9DD-r-MVuvL9j4JXCFM3iMwwTqIg8rnnW04WMQaSDaEp5sSpHZlOFHMv9cLQ8-Ax4sDx7MAP_dThoTv8SD2QBcveM60eyEKWZNxOg4AgCwRZIMgCQRYIskCQBYIsEGSBIAsEWSDIAkEWCLJAkAWCLBBkgSALBFkgyAJBFgiyQJAFgiwQZIEgCwRZIMgCQRYIskCQBYIsEGSBIAsEWSDIAkEWCLJAkAWCLBBk4e8OshAxO87SKAzjxPmIkAXCGRDO4F5xBskAwCAZQBYkQ5CCKgfDo0qXPzGgQOVATuE30fs9Ywq0-jSNp18v-R0sUR97JYPW7CCo4Kl8J0L3jgOZdpN1Q9L53dDkuiZp3MIBdMHhh0VTiLRFI91LHtRQmmIgASeQB8zNQAU2ZybYM3GaMDdyPM9jLE5NNxkCFbR16teDCu5jyraHQFyLKugq7D8OqsC2eJBw24n8yElc7lm2lSapmbIkhCMvicDMt9PY4bYbhQF3wPly4dhymBNHYRpbN0IVuNaeY_egChzPTS04XQlVQKgCQhUQqoBQBYQq-MlQBW5i-yk-aOb-8lAFiSwIZ2NWGFp8qsXHh6-Onjw7fbH_8vjZ4cvTo2fHh09e7h8fPX9GQAUCKhBQgYAKBFQgoAIBFQioQEAFAioQUIGACgRUIKACARUIqEBABQIqEFCBgAoEVCCgAgEVCKhAQAUCKhBQgYAKBFQgoAIBFQioQEAFAioQUIGACgRUIKDCpwRUOFBBM635jcb0Fy00CqOpndoso7sZSCHithn7EVjkYGSaVpj4LstYZA-BFNqy958FpDACqbgWpNAV7P8KQQr2ntv36gNm2h6oDU4gBQIpEEiBQAoEUiCQwk8FUoDlxJMk5r4TZL96kMJYi79db2KiNTHBJgjDQBgGwjAQhoEwDIRhIAwDYRgIw0AYBsIwEIaBMAyEYSAMA2EYCMNAGAbCMBCGgTAMhGEgDANhGAjDQBgGwjAQhoEwDIRhIAwDYRgIw0AYBsIwEIaBMAy_QAyDVlXTFcVvW8UzVjLf1T80XWnxxK6rLSOX11Tma71osbd76KVYzWOOq-j16wcW6rkwmjr_AMtBfYycqSs_4vyF3Q_m9MGbN8Oj1MJiP6EswsTzMu46d-iFpdIjURFyZYi93kfHne3uvzj8b100HRcFlqvVHE7mfFYuNR234B8m7GxkrC4YlWYUWvc-1ppjX6DTX7eW1VrAcUgdj4xVq__rxtqNo4Kz4v3GSO5aIDgyGq0gZdvR3KViZTsQk6ZXBkFML8sVRrW0qh4w3zB41cS-sqr8Vwy_ok6fiGLktkpPTNp0aFauPHrTo_iiVvioRFWJYsFgiXkD_Frqbjira5HrwLOjxBwAOB-wMqZDkt-mR128MrmEwK1yrb7FeJ8Lv7HJIeFvNbja4wPRVOugtMF9nJdLNZQeycogt5I8WLZz3GTtS2fU8KZDunZ4kjkYr4nqtg3sy5QE-ixpt7X_zKr3_NJ4uv9oAqsAJgZdrno1A79NSmU6pEMHe3-FIYt67ZFEz5_V6CUI_x0XQKdURDURYuuwMA5MAY4e_nRIq24oHtXpfqqKlhpn9GuMcPIPYO5gElO4OTlI81IE_mBG21f96GpVaNDpkI7s7_klX7ar5koqS4qc1VodRJdokYIeAAR-jQVVA8umZ9LUStJkrjZVF3qSuY92HOKBNbngNKwr6c2RqhDTSpVpdLtDK3BQ22R78GEQ26mTuJ6VWKYbOD5zYieJWTgEPmzhbNeDD8nOIjuL7Cyys-5kZ22PlW6hunKu9uwdDbTr7rSD3bN_7MfnfhRMcuSYJtadhHAXt-PICtLA4Z5tMR44UehyFnqp50aZa3M3xbrO1Hd9O3QCH9xm4TLf6EGvIJWjPdPeM8MepHIchK5lOwkhlQmpTEhlQioTUpmQyoRUJqTyJ4xU_tggXcsLfY-Bf5x1bwEkkO4vF6TbyPY6sO5Q7LBz7fTE_QTDu7twjrHLGFby-e6Lbx7BuX_68vDVN0-PX0nYLCF3Cbl7v8hdArESiJVArARiJRArgVgJxEogVgKx_vpBrF5sZ7abRK6VhMMgVpGrWlYlpmiX7Y7dLHSQ5cTK1QEbD5ycMjMePgzaUJNzUvTkvqU_KACwGZvns5yrcJNl-wbs1BzWHcPVYcDerh8-BLNb-nho9J0UjW4XPe5cjUl1VaSwiVlei3biCm1uiRbCOcHIG9bCixwqVnSI7OnDh8bnv3OnFkbCMIGAi0NUTtdfKN0uyiGNMsZKbvgDxscyLjBpC3bG2qZBCiG2akKLykH1Hb3OFaQr1CQ85yjA0E1cm8GpF3dRk17k7J_kLLxY08BdFdCedEX7KhHEPDQT1i8oY11KcrI2ZGBcEYEUwPQq8PZcDGKipSDWkbY3dI2HpZekActCP3OZ718DthVLWS93UeKbbBZViPNcrnmwEDSktYg-1VoJM1_kdYmh4kbSQiqKLLqbCONAgfdq9DXB6kIwdQOKQ-Y6rPhgbRHJTJR_xSVWBYHmRw8LIxyL1UzGAGeI-QBHcFWz2UkhQhMSlSTcTjabYMxOYDYkYAufSWFu1K6GPaxAwWqrnhR6mE1H_rZ1Jl39dGMEKdxuUx5069kdZZ4KLGYyHppmF3Poygw0XXbbGgHMvoshwvbHgiUm8g8SKY91NJtVSnvNZsfAw_KibA0Puc1AOKLM6RU8yTvDmlonBXJUGU6I2ysThsTDh20RlASDYF-gRZblO67AXa4_tf8BpgYNG3WtgQFZGAfmIBDdjLOj6YIlVvOgDQbnxnkOTvGcfSciBhOxhFI4L5nAfCM5AC68lCd4OE5PCh3x1cHBZyLSD97-ZFlOuACc1eC9tv2gqpN5JQUMAsGhYCZC27A5WKT5vzb1jAKVjRh-ieWEs1TiT_hYJDeK3MCzHMadrD0ytboN_SC7ZdHFKGQdtvasLZsTMp9drsHy99D_7WGCuEKeAAK5NdWDWA6jbA8tzcORQP902qyLswhcdk89Y1PuRuh3Qr8T-p3Q74R-J_Q7od8J_U7od0K_E_qd0O-Efif0-68R_S4zMEMY-I1fN5DwV35dx8ODH1PtfSRQPJhz2SmGXqsBRLw4ezpE_KrAvVBsi4nvCoxv96I4DTSiVQvf5zsCtSFeh7yUHhyLa-FHbpZFL9kZBsM6r5alpTA6VSwXphzDJnjG7BhPmnO_sxWyJq23AZLUnntwgAczpqq2xXHTWhUVn-XCc5U10rUs9Gqp72e5KMDAcJ-qYpZxwYtzUYfaFAwNYBn38flkwdGMg7VQNU_aGJ4YSPhs9Ek_U4FGnEE89jHyIOqCN2TLmuQdIl8mWCBlqGBKU6ClFDgT0ZwNJ7vNrN0EweglXui7SRBlpm-FIYtM7vE0SocQjC3MZQsE4ye2K7bHbva8t3Ad9tSBfT4K7CkNwfeK_MBjgZNEfmSDoeI5PIGGzJRZmZ_FjsXsIA6Z73q2HXhu7JqZ42Z2yGA2hx9pHeAUHlvhnmfu2X4PwMlLXOYFjBHAiQBOBHD6-QBOZpyYsZeazOVjAKfxo3cMwxRYvmeDq8vjgP_8GKbxM1uHNvWWvgpqkJtDm06KEWyTcVNo00lB2CbCNhG2ibBNhG0ibBNhmwjbRNgmwjYRtomwTYRtImwTYZsI20TYJsI2EbaJsE2EbSJsE2GbCNtE2CbCNhG2ibBNhG0ibBNhmwjbRNgmwjYRtomwTYRtImwTYZsI20TYJsI2fRxs00-ER9oG7vOSZxUMuSnfgcNMCFkUfSh7Eiyy9l1oIgIpwDVttZw8dTHvhG49Vhb2Y3y-UW6nbAL0gcQTYCgXzDUVcTXaSW6PdjGoNszYwpCaYd4MigMC4ZaDL7SJ4tRlYARFYWaLKu9eKE4LyLgeivMTwGdGgEM9WBPrx34oyUeBz5gxt5LIdG07ZSGPA9O1GNzie1kiIk6m6cOXSeiEnpfhG4YcMw18145Cx4W_-fAj9cFnnD277_1AYBYncRAQfIbgMwSf-TXDZ3xQTL4ZpJkbWjeAzwzCZP7SYFlbX3LjeEO4zElRFn80_rI1VuY-XwNEWBnCyhBWhrAyhJUhrAxhZQgrQ1gZwsoQVoawMoSVIawMYWUIK0NYGcLKEFaGsDKElSGsDGFlCCtDWBnCyhBWhrAyhJUhrAxhZQgrQ1gZwsoQVoawMoSVIawMYWUIK0NYGcLK_FRYGZVTPYXfxBD64DJiuB1cRo5bA8vAw0-84MEv4V1AWltaReyd29JqTO_cllbu2LUFKkUzK2bsEnbUWKu64m0H2VUw3r7hK8PV6hRv32qbg-zG2haFda3-5fxSGUzCG2_qqNbfGXRTqWilYffY0xUxaRVT99jNFbllvstgVXt36Yal0nlUWdD13EdeSZ-LzboqR8wKyQBhF6CAP1cFIsdGZGK5thNbycbS0eonyxg9PLQNW_TBgWj_ScXGxgvGyLbNLM6v2TS2ldk2y-59jHrcfYUl8q1jLc_x5kCRdYhg-5TQhXIXxjQR2OCu6fF7H-_bt2_nvJqzHAEJYL3i6bQ0jh_hCXzw-uTBQVdUt9t6kycP3ojf9_GCkWVrRglodebc-6ixDZG3b141JoEleOtnWvWLLGLo3CRh-I1I2c14FNuRuTZerFnVSkebbXa2CZy5ZuVu2wy_Rq_Fpm_KKvr7HeJ-d3_erFrY6DMsnhIBVpGMEMv1ShXsiEht7ieBLSoS73e8r3_z-qv2KOoCHm10ak8Osxtk0wsz6jGF7gWenWb3vwQOuwLfRICZVETs90a-xG9UWGmtetd4KctnRsbrJNxO3XBdvo-x0BvTcXORilvNF9jvNQt08KZRNRrwkLPwjr0flykDTz_tbpTWuUzEiDZ4z04BJ7wqR2QT-CxJ7IDdcXT7Wq2iSuDvvzjaffX4K6Fgvj54IYIbKrby8CF440WBFU0wpWPHpBclvuVGa6PbFnlyzVzeFcDSzm_kcGb7wb2P8a6glz4wQnfqhKBwovjeB30XgNl9vr10mS9nKu8kfUaQotB1mjXYgjg7i6PdNzd_IenaG1NFoA7rhDBPgxlPrErR3pM60CvGrpd5kTSEAb0u2-AIXskK3ZZ6QHtUOJPWEhRSrjIo2sW_FR0B1i12qnw65O4NjmM_TZUYBJR8UeU1n-TFYiXrCjBXJZ6_XC3xu1ZGbUZwyCncTvb1rDyDXdAKe3lR6lEs4ZGBNuoRsuYmDnb1mGeibqd7NFmVOTSjMosjMoVrNwnTbMeAzVfCeC974aaiiqwFkojkzwWsK0xvToc80e1kJPe3CM-pmG6vlFQ-hcFg59MhL3U7zo6snEFjqKGU6PHFtRfbuGfTIad1iwWoO21nVXkBjyolyWa9-__qgte81y36U30kq-o9bxFURVlMQI2ec5VbmsirQMgXsPjfw56bDnmyG3r2Sn99Xl1bmSc9h07euNf75lJzQa7rry0N6xb4Il9w8RZomd8R9Vqy6kLosrM-w9MQFY_TITvpulFoWrJFr7H0fV7L2pLWiBQbs0WTdwOZDplA_R03wWItV5X2WkhNIfPG66w1K6a_A0xGDRtOsE-UuYRr91wUr4F-Qy2wwAqwAWOkv6uXXGRipRzblKlQBxKDDVsiW_ImA3chjg2-WGIiNscwvMpLTYfMiS261ZBFm8mNROJsSoOpNduORR_iAHOPfCX4pbRbepD4eqG8JG9QW4WvCVZT0poal9fL9LQoVFWHZ1Om1qwMdcI1Mza0OranAvLTNHQc5rA4ckOeJMxLYycNzSt69naGzgONRajlpfmFvdCbQtsU2qbQNoW2KbRNoW0KbVNom0LbFNqm0DaFtj_p0Pb2jK8t4agc057l7ejco-aP_dyiH4VPNbR8j8Xw7yzDgmbXdJIs8B3XN00nC7npWSkHq99JXMuDw8BNk8BNvdAJs8hKw9Dd7vHWuVWjY8vcs509q49bFSkX44R7xK1K3KrErfqzcat6Lg_c0LdDp2Ne6uNW1Vb43_7678LBe9I5tU8xxiDCV8I-nbxo3KfW9hulX439ADw9HluZFQ_Tr-7L0F5aFp8tje9WkplG2Bx9kUBRO3-pUmVgTWKMtP3xpBBRkV4e0HwMKZqCTgRV63LfM4d5S29BFNuytg0QxSLeeQui2OYh-ogS22yiBLJ16cTW2UVDbXV2rsaALhurkvMdDewjiZQ6uJ-A3YwFYmX4GOOwY_jbxHa91IoTp-PDu8qJ-qVx2KQqum7WwyggtzNWgGVeS77Aq9Hg6UnxZd-si8slhrR92kYwY3irCIx6lsE_sC6G2UAxJNIflBuBDJtgs2dO7HihO8zwedgn-1yiuWOY90JwJVaNYFRObS3vqaYbPBnEFbXwNDD0GRggrG6xb4IUIS0Fyr3Lh-KKkDnRqdr9zXo6KdaGBDsQAWaXiIStRaIHF9Jef8IbbBgUiEh9s9klDmJj2fZuXsGfg4XilXDYWp4_iSXuFqo-tIEMr6LfXEv0CkF2hIFjNF8JrIrUCxKw0ob5UvvDOk9fotlx-NXrE316W1X6h7ja_bKdW5wkxBF0sEL40EyXuHRjxvB3-YQqPoThIalbxeXNtsfr1MaBv1AIzfUvvmru6FH0og09gwM3K15R-KuZVnFVM7Ni-M20qk5evHitm1Xi-jZGANevIdbgc6sIZcttoAF-amMNqukn-zj-NpIlIyob41dJIrhb0al1XSDftWzoMUpOc1RZJ0RcqUKBN89z-JUxmXxp7Mt_v5CfXrwQ_4EBif8-3r-G9yqCNcWSkKFpPspNum3MeQR861imCw5OHAfeMEXpft3y7JULPZVbFuUcSR7w-K35zia5RN-JgRQiK4FBxbQ7Ku0ZU6Et2IcwQPhDcn6IypwEljtSxWwQazXnU4PBWzZ0NTJ8I9o25itY3hlDJoup8XXZnLrIJS7QryvURHEFskNidITxNidhV0KyLCfNMYmgfuQzA7-opcjRwPGKukAyRYr28AFgJZ3lgnulk0VSVouVSKuKYcoTyagxZ4hPMqJu7DSwvTR0Iqcz8q8yoMLiWgoyx31Nejh-YZjoYtxVQjSM_47_-sG4wT9DGcwbNTSdfLb19dteu811cI3479_-7X-u1WWdI36ynKV7oy00dzf_CHaFNVXVvxUHG-2G3GtkGafaP3jh7yY3_efLzR282-1ffH5jmc_5dXopdbzIi1w3Zu1hp-XCrtJT3TiPVcOVemkObG9ZwTNjF5LvLi6XyxlseaTBOc8zOAflOwm0twvVAmVfiw2mRSdLaEzMdMONrUcuWxdi7Kz33dSP3Mx0kxZ-qmXXNBvwjmmxxgnx7DDOuGlHrHuFQJcpu-qE3DjFlaoZUHyC-wLg2ySYcoXWlz4YM0RREcwV9rsn9SzCs-vm7UxIb6CIFqGP71ZCFcDOECYZuxJOFu4Quj3IOzTqjGWunfmmw0yPdRz4XQZu1Ma6SepMiGK_-epR-9Wj5mzHqx6tpTGaXx4N_aLMm4a25VqLRmKMhaG04AW2lEvDSdFO1vqohTVxIG2Nw33tq0fyq0fNVxPjxTVb2-VpYNpmlMjwsnTNu3yhliy8baLvKu0AHri4anY0QnDBayS5OXQJqBO5uBS8YZVi0ElzWZWEdAS6fAR5VEdiBLsC00zlqkq4ZJ2XBPeq3lVsCUHxLXwJ8Z4GeXYLZKok6FCGoiTpFhw3iqdb1fZqjEsjK9n0LcvP0sx0eOtFalnOddL5O6QnGy4EKzOTCP6XpB1LZ5ex1OMtt0w1dlzyilLvBC8cXAgiOtIQpwqipJaTCiMhfJYqqQrqCGFIypnoeOS7tTI1ngsaU9XCTjNJOzBaxTG7RsUqZNicAVu9vSaMQi9MMmaZneLRMqhdSPXWqU_F4dzwdezgDHQUfN1WaWTWEOsXhuCTUMq367TlVhUTduVRNWpLMHmXXBglu12ZcdvQpB29ijBez20wEjtxWGaHls1Npw37aYndJsJxh4zsOlcvvvRogKxXf5vR2upQpH5sleayDDteCaaXS9QSJwUee1joKql8t1k6tm37mWNnSdwuHS053O30m-R521cLeVnMvMRy_KSzC9rUb6Or75DFxeBgS1F8UihKChSgoHa5wl4sOYwkXQwSvnQZ2jV69lrRGLdUFL2sLy1bjKJ_kfQoGlVzx_UslE-NcdM-RbD-_qw2w6jsleZ9kR2rh5DPGKFcGFoB2H5-7LUxdC2p3ajTO-SnmyJipBAWlDBSyt8cfSbfHFRJRzKVFL-igQ0WtxR5TJEYVxrYcgCSD7Wt6VXscy2hkvFR3i7R9yYjLen-Ud5kpCXQ6U1G9CajX8ebjPreNKcVXdCb5j71N83Re3fovTv03h167w69d4feu0Pv3aH37tB7d-i9O_TeHXrvDr13h967Q-_doffu0Ht36L079N4deu8OvXeH3rtD792h9-7Qe3fovTv03h167w69d4feu0Pv3aH37nwy792ZoAkHW3zg9Tu9TGR9qIi9tYIfiaC4MQ9fH6XYfXS2HRnYffR0hcCrlxDrTxgs1mrF9bpfvUz8Znx9fbxWd-5pOzqq---ml0Xq_rvpJX_CSv50Ezva1t_m263rfuZ1bT8NUiF_zVI-zEwso0LKtVpfmNOh3TTYlaR7zUWUQ0EaJVYEhSGibJsATlW9N0D2ilnkZb5J3qvttsGRHH5YsKIhJ9YQTg3dMs51fQ4To-MYetEqGjRlZxiXsoY9Gdqx25Hjd3HXliZa0scK5nT0FPMucXbd6p0O7enrl0sGVtIEc_VrnpIWFVarZjq0n2-yTBRL9SAxNYo8T5rygr7xTIf2-zUc4e1cXk7EzRtlBG3gVPLFT-DknHQQARHE2Fiemg7YbsI13bAx400ZVwsKGKBZ_pq94z0ny442h62cmjcMNE-tSbrVA3mhv6ahfRtAAU6hAGrfjC7ZDa3YDQKLRRHjZhZYceh4Qehor0mApwfHRYBacK9O5F4VNR4tHmV95bGCKZREy5Xc8kxdz5VMdgjZIWSH3NIO2Z4NveWR68jjwh_7qeE-DjWeCdvQ9tzU9wPuOmlksdANsphHPOY2sxPXYiasau6yKOY-57YFYuSmGzKeSAj2wCP10eG58L8eOjzTj9wgAl-M6PCIDo_o8IgOj-jwiA6P6PCIDo_o8IgOj-jwiA6P6PCIDo_o8IgO79Onw_NNFqW-HUWWk4zS4d0gBjliF0ZpEqRWEqbM-ihkeEeCWEYMTDKtbOrbNrlUS4HJqDoYHMpJ6EtlnRQKNdly0V1PomcMc-ghEGhLEr00sVjse7YXdzCIn41Er0EnGvuS9E5Ss0n7prFfupScTrLX3vnoBnd-Czd-q6uj3YaBTpl236Bl13LQ_U5aP-rHp2jt6GR8v7s9F9-38ivZZ_f3U0HRd0AUfZ8ARZ-TeQ5P7djyE3uUom_buP2wSkssP4ht3zVdgW4ZoOc7Hsp5qlc41yLPJ3DV9Z5AhQmMAwpdL1EVqBBU9VcLUvEyva66vzq1040CaKuTBsLU3pI18PfGOrvfSaGtsxmiolDJpCKw0ShBRSKoK1HUgkLdtuMVJZPXcLQ5aer4bhjbaRSP0vsdaeLvIcvTqf66h_-7pftLXbCJ0iBmzGQ_I92fTvUnQhjX5PolvBAXYB8FoHFjBkDLStLM8R3H76D6vQyAW2TmiAuQuACJC5C4AIkLkLgAiQuQuACJC5C4AIkLkLgAiQuQuACJC5C4AIkLkLgAiQuQuACJC5C4AIkLkLgAiQuQuACJC5C4AIkLkLgAiQuQuACJC5C4AIkLkLgAiQuQuACJC5C4AD8GFyC4t2Cp1ENkgBpMqyMp2RbA98mQ4vQQs51uotDEBcrUUKRKoD9keX6TJ9OhQRfnlxO8QNYrMTx_OlCflKqkxdpBsw43ygp0ArrpAjB4qQFPJjrcVwCHRDhZYgA7MKEwobMOEreBlekDGrZRAhxJtZSFaP2gJUPDLHVzc7qJQNHF1EtW15C3CZPhAr3fdlyTLK9qtArlEoE-hd0Dz9QAqzv3RFtfyonZ6cjoFPxS-BpSuImE8TcQaxBb58ioEQ3wcn0jSpkkJSY8SjeHzQTnc3Ymz7I22thiiiYNhkNfj91IemrPb0bLxRKfBVgwYLrMSsH9S7gZeIGls5SBeZC0Cwd06nveCArOwcs1Yj19c7aUXC3XzfWUXL8abbA9-1kPl5D9Yz9V0EehRwpML7LN0IsyK2MRNxPTt_3MCmEQoeOGzPMtNzbThAdh5gduGCWMB7HthL7DYz91hx-phx7JcfYsq4ceCU6n0M1sTvRIRI9E9EhEj0T0SESPRPRIRI9E9EhEj0T0SESPRPRIN6FH8l3wDgITfHvuDtMj_eb1X1RAQvr4yIw_NB1iCPgjqMdUzouUvi75bcJHmIOdiZkQEa6tlotI38hIUx9HEdZXVHwb3qEBYPz6uLUovwyBiILTkTOf2ICIDeiXwgbkMo85oRnHLI7-3tiAnrTnvBYEFvcPmg_tka-aeNk-SBsvlkaVzhOEJs4aBw42MsAc9IO8E1EhP4DoBr6XghfWwg8dDi6-_KFhHHrU99Mj1dp0Yjzp_nxJbEPENkRsQ8Q2RGxDxDZEbEPENkRsQ8Q2RGxDxDZEbEPENkRsQ8Q2RGxDxDZEbEPENkRsQ8Q2RGxDxDZEbEPENkRsQ8Q2RGxDxDZEbEPENkRsQ8Q2RGxDxDZEbEPENkRsQ8Q2RGxDxDZEbEPENkRsQ3dkG3rz4_8HjcChXg)

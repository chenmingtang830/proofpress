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
**Governed knowledge for agents.**

[//]: # (ob:0e0e9d9a)
Proofpress gives a checkable answer to: **What may the next agent or human rely
on? Why, and under whose authority?** It binds selected conclusions to
evidence, scope, version, policy, and review, then
excludes anything rejected, unresolved, expired, superseded, or unauthorized
from governed context.

[//]: # (ob:92fbc10e)
Your product keeps its models, tools, memory, workspace, permissions, and raw
telemetry. Proofpress governs only the narrower trust record that must survive a
handoff or fresh session.

[//]: # (ob:815b673d)
**Start here:** [run the 0.5 alpha quickstart](#quickstart-governed-context) ·
[see the integration boundary](docs/VERIFIED_KNOWLEDGE_LEDGER.md) ·
[choose a design-partner integration path](docs/VERIFIED_KNOWLEDGE_LEDGER.md#design-partner-integration-path) ·
[bring us a real handoff workflow](https://github.com/chenmingtang830/proofpress/issues/new?template=design_partner.yml)

[//]: # (ob:6ef36a68)
> Git made code collaborative. Proofpress makes intelligence compound.

[//]: # (ob:8fb4a17c)
## Choose the path that matches your workflow

[//]: # (ob:eac911f1)
| If you are… | Start here |
|---|---|
| Building an agent or multi-agent product | [Govern selected conclusions for a fresh session](#quickstart-governed-context) |
| Shipping a high-stakes review workflow | [Try the legal cold-handoff fixture](examples/verified-knowledge-ledger/legal/) |
| Handing documents across people or systems | [Try a portable artifact handoff](examples/portable-handoff/) |
| Evaluating the product mechanism or claims | [Read the frozen seven-model study](studies/long-horizon-eval/relaybench/PUBLIC_RESULTS.md) |
| Integrating memory, traces, or a workspace | [See what Proofpress owns—and does not own](docs/VERIFIED_KNOWLEDGE_LEDGER.md) |

[//]: # (ob:8f7c2d11)
## How trusted continuation works

[//]: # (ob:9317a2bd)
Proofpress sits between raw agent work and the context a future human or agent
may inherit. A bounded evidence projection becomes candidate knowledge;
deterministic checks and policy evaluation inform review; only the configured
admission authority can authorize reuse.

[//]: # (ob:bf4b55ec)
Proofpress is not an orchestrator, trace backend, memory store, company wiki, or
truth oracle. It records the evidence, scope, review, and lifecycle that make a
selected conclusion eligible for reuse. See the
[ledger scope and integration boundary](docs/VERIFIED_KNOWLEDGE_LEDGER.md).

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzU1NmIxMTVkZTcxMWIwY2QzM2VlZDI2MCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImVhN2NiNzdhIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8wZTllMTNkNzNlOWJkNGEyMmY5OGYyNGUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2VmM2MyZDU2NDRmOWRlZThmZmU5OWQ3ZCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtndty20iaoF8Fo4qZttUihfOBfRqVrHYp2mV7Zbl6O0yHlEAmRJRBgAOAktVVjuir3fuNiXmEeYW930fpi43Yt9j_TyQOlEjoaHdVzX9RLpEEMhN5-M8f-cMWK6okZlF1kvCtydZiceI4bmgYDheeYYR6xC1LCG66-tbOVpjzyxOenImygmvLGTMddxKZnudYcew7bmQ4lsUsSxdO5DNuuMKOw1BEroitUOdChB5zfbjJZa5g8D9hBgG0y5Myys9Fcbk1-QFfVCcVO4MeUlZhVzvwRyhSeOM7USRxwsJUaIU4T8okz7QZXJ8Xl1p4qb0u8jxeFKIs4Z4Fiz6wM4EPtfJ2kX8v4HGXBTY4q6pFOdndPUuq2TIcR_l8N5qJbJ5kZxXLznxL3125uxD_tkzg75NlKYqTKM9KkcFcVMVSfNrZmgmGkyiYF4Wex7bqd07EubwIJlec6CIQhsU9SwQht5lpxoEfm7bAkeVFhY92kiaZgJE3K5KewPRFJndc244DmEU_jkUQcI_Xj6NGdxKxRblM4YFNHGeUF7zcmrz7YUt1_8MWrHJelPhX_bHgJyFM-butVwuR7R1q-zkXH7few4M0mwL6PzrYe_btwXiOnd1lr7CqKpJwWcESnYSsTErcMSKNT1gJU1cJ2d6ymuUFDuhDkmGT5WVZiTl8krE5rtzKwHbg_hKXfGuSLdMUhhnNYI1E_ZRhmkcf4BZXRJ5nhDZcDstTiY_4EE_-73_8z__3n__xFN5UPTHORT1_sI_EBbzz24XG0uQs-910K4IJE8V06_fTTNN-m8zPtLKI4H0celXupvlZPi7Pz6ZbcEcF76t9B81Vlwu541jBtj7tdKOCGQqCQIQro1rZrhvH9dXqtlY94MaCTbrSiefYpunr4h6dvPund9lirsEZxAl-_6Q5F_Ds43KWiJSX4yTfhWt2z3snAmfh6cBjC9f1eOC79xjR9nZ92AXXPmT5RSr4mdCSLC5YCactqpaF0OK80GAP5Vk-z5elBjsFjk1WlQMj0gWcQB6we4you0o7S85FqVUzoWXQgjZbzlmm4WCwe41pIENA-KCYYll5IQptYESBGYeRca9V-0u-LDRYDQ7zoX0QYlFqSVVqczguabmjVXmO_5uLOcjHHe0iLz6UIBXFjrYQQ5vVN5zQ9Sx-r1V7U4GU0GaiEJPtbe1dsczkPOljBw7LYsY0EKDRhxKvev_kq-7F6GxgRKhAQGf49xjR77XnSaXNGRdalMt_UtAmecEqWMNx72zBNR9gURNoPgU5ILJIDB3o2GO679xn1W4vaFDeRqkod-slHEn1MBpauTi0meFFK6Pan-V5KeQqLFg1gz8YTkgFm7TULnEL4c6I00Eh9JV222byi2EpJVgUGEZsPPoYf9QOY7xWY4X4-9_-U_tR6_ai9uM0-3E0Gsn_4E_t62WS4tDggKpTm3fDlvN8ZWI90MDG6qC_yS80kEWgsriG7ybZkqG-q0_aDdN5480DUxhYhsfMkD_SaHpnoET5EYrqQohMK9iFmhtsAmaKywVSXYKYi5fVwGb0dO5yO3ysOfund8f1faOV-1gRzZJKSIUwkeOb5WUjDfElNjwwyjC2Q8cR0ePPZVJqWV5pUjPgPq5A5uQFiOUCZLAWgnkqMt6IZw2M2IFR2lHEHSMMVkb531rhOdHO0H7O1HDx4-Hdd8OtA3sviiwP7PZVS-Ywg7bSdFXSDw_hK23TTQOdczcOYlP3H9Z5b43welinxTJMk3IGcwBrDEbOr0rtFDX7qYYmZibSsXZYaWj8D-330Ag8FhkPG9zp6Wk5m2bzDzyRul2NdNRpSu1f_kWL-NrPutGhrlsZncOE7Qvjget2CnppuTgFLSlvrE-Ysno4W4Ayk2LiooAjCXM47ga5Ox_a3q4e-8ZD1_Vwji4UyKUwX2bwoQaaXMxFBadLfJQfoYmmfJgdnMAFKp08E9qQyeiHQWhZbvAo65otPmqjUZaP1Az2llGDSzmaHVpSP8h0imZBBit5Mh9YWVOPQwEO9cPGd8CiGUiA-RzXb1GAGVQvLg6pQju8AFtX4KyCo91aviAhF-NB6zZyIy92V-3tA_WgYJMmUtmLeskYrBT4jTASObghAXbLJgZkiaW7YL_5_FFHdpjJ7QRvFOIsgdkplFwtwOyEP0Ga8DyOtYqVH7QLaZkwjefRci6ygVmMYtt1fc991LGCz7ffjUwe4lEzvrJa8ssJnBeYNmyved8wdw0TTv_AWBnsxUhw71HHejwDKV0uF3gu6n2pXNWRdLXQkJsLlNVJOUcZLu1HnGQQ3EPzyv3IiN0r_qmKw7SiAs_ouchY7REM7cobbh2yiiNTOJZpPcpIegqOpWUOhjQcZ_ivlMbIAky7JtY06loGs3usfcsGZsvUmWXGjv4oY6xt83Y3vGtG1G418ZHNF6l4_0T9Ue62gx4ao-kyM4hXT_WfcTck5d__9u8o3Gq7DF40UbAbFvXmu4fMpTgyIouxxxpPb2lVjE8rQctFaKmK9pBF0G7CWSWN9Shd4kkpdwamzRF6aNni0aYNrCWeC2UAL6scXLkkAn0k7VwQeuhawD6ZL6pSGsRZGRWJfDEYRoPtpwvmrari_WVRoAECCq9a3uR2Xbt4YO3sQDej0PLv2dvxTGpyNEEyXB4uzkUKpw982TqYVU6m2fb2dWMFrZQhlRpEQWxdseRuPyy1qnJpwClhjeV7KcAXYNJ7glelKM4TGSqqw0vo_ERDHorPwTpwwlUB9jyHpxZ1tGloVfrXDSyI4XE31HXz7n2MtHd7PUdRGqkY6Tkrar-uUUbvn4AyLnf3jva_OTw-2D9-e3Qw7sYEM1VtfXq_04TUt5QSOokKweqQtvykiY-Lkzg2rdDSdV9E4A57RuTYjHEbRSjMv5zIRu6pqH8dO1zkMDqZxChkTxjwbl5hvPs9pgvSJLrstdBPIfQakcmJe2YXyjyuTmJYBlFIk1DeUYbGhPlurOu267PIE5HhmV4U-ZwHTHi2ZTDDdOHgBKFt6SJwo5hHPHTBSg1jy2emJYM_uFNlMqJerYnlf4KJLqWeMd2R7o9M71j3J7o-sa1fw786zpqacfQFQ8cXYeDBDune_eExUhdyu9VZhRkrZygJYsNlru07kYjhAtlGL9GgduLDMwgo1vEzeP8i4dUMPvF9eDETydmsUq-gzd_uLn6_5iyq0fqO58JEG26gW81oewkINdqb8wqqOScWsctjL-K60zTXSzWo5h6SQeiuvri4GMMl35cyFadSeL3Ln04z1RG6H7fuZRevxq7-IDOJv8OXd-51_7C741b5wl0m5Wa52wRGy90oGV_O092QgQK48ugPa7Ie4gsQ2VkpJtreAk3qkTnWN86RHMNuWt8xUjfgHaMwXTaDe3G4f_DyzcHTzZtNcBtOEfdsh_vN7uilfdTueEg2Z7y9PdA9yB_PZZFh86jpvpfjuRaYv3vqpson2vb2xSyJwH3vmVNgVV9qh2CFgVGDUaP8YqeOfcwu_7C9jfGiELRRzzzr31vl06wz18oIzIKd5uyAzpWivW6uVmE7OOIMbGJogQu04y-rGXo9hfhetr4zzZYZPGCensMLjHckBf4BPhO0in77Dj7lMqtzrslfYUAxGGDXon_jzXNtRCaITD82PacVBL3slZrrhySl5klZm6r1o7OLadaaRSu5mnrUJUx8qqIRrChyuVwYtlW2sUoj4BvlEuyZc1jUadY4GDAdMTQ201RaeeDJmesFBotN15Y-uHzyXpas3eT3T36pVRipVXiq_Z__DSe6FHVO5LamypyrG8MCNwecIgZTwdLWqWrExl3FDqzLUqAYvfhDJcCmBWvnd7APQdmdwFxVmSikENo8g9zD-hAROcIyOw3aZvXUDD4kWYfBqwXOzdAO1h3hcM8VoTQmas3YZfLurMfXJ-hgSWFwo84PHonsDKwugYsygt2RjxdZp_sPU5AKlVrdPIYl6-7UpKTEXc3AecA1lR4zJq2UQdMzFQxT129hHsSGzaLIc03L9trN3CUOG_Pg4Rm_ZtJ9HjiOGXPfac2RXhJQ9ffQ7F0B5zytklH9spE_P2rvnsujtV4MS5WzKgVuOpey_zezZLGQ_WszsMzUiitZ3c4K9n5c1PIpFWdwDGE_8zbGFicfUe_1AhznSkeOWh05qtd_V96-q3r_Br176FzFDUG4sqjI4VAsRA7t4FzUhTRlMwLWBny6MI0axrr4ivqo6e_gnKWY_4Iu8VF6gbZCi1KW1P0cwcrXe6VNpqxEE98_wf8l0M9KqLGNQPXOS9PxYSP2ZHivVhgye1ZKZcY67YEDeAPC8gK3aE9M5BdZE79o4xHw3ibZ-eO6HHBjVRu-BRa0Hrq20R2bNi3cHZv7ZHabPmyu24FnG8Js5VMv2XvdmrlzvhYNrVWbZ5qhIZNkcNCSaqzttdmTNh2hSuak8gG9Ood57AJM7Vb9zRTuqlCHw94AsVhbUqUcRm3QQIv1RoKGwPbLi7k6Mb_p9DgMNk7OYJR8mjGu7AFNGS3VJXastSYM3L4sxYC8D2LOvDjmYWAFrevSpaXVfD4ks4zn_Df9Hdd9DIq3xGZ6EkfajKEaNx-_f9Lqka6r3WrNYEb9KzZVXamHNrlwwTEV3DdF89C9LPf1TXTnRHWBIUbQtmCFgvL5kOBpBEutgHWBvxhoRJUvrQOUOBnXjN3GrsXtkSaxiC7htkbFfJCG2hqRrYESPEtQjqHorpdfe1NbSWD2xMs0XVk32Xy3j9qONgiAga3kuo7vW2HkBnZrwPSy8t3xv3tqvemBMzvyYj0MZOmo7KGXbW97uFPmvDW_Qiu2HNeOpMFaGz5dMv36nrhzYhyrYrXX4JXAhdbYMH4NHgkYc_UCv0RjzjR_PRkwzQzfC2IvCH3eWgm9jLoa4YOy4yDqwNoF0ZNUmIidy7-00WXzop7U0agEW2vExXmvkX_Fhx7O3o5Gyn8bvkwm0OHTWlCjlftxmsFjrUnwNmtn2mA6c8tncet29bL5zcw8IDMP2jyGYz_-HuTV6Vh7W8JZOm2HmDJwOU93tNNoWZR5cSp17yn0cVrbTyA7QHc02Tmp9mHPl-XAYXJMwXzPCQNdtLq0VwPQ5LAfkM9HIdMXHDvob0vtA95UtdM4iAx96gUop6QJBbTConG__w0cn6pVovjEUtbI6IGsqB7Y1MK1BXdcrrt22NoMXTnB6qa-b2kAWLrSeusW9BYGJQdhPs6rdCEXfXrDpm2mdoSWbiUTGtpUJjgilXfoZhocknp0o1E76oPvDp8dvNw_ODl8hm3g4mg4AnihmlbGyARcZnAmb5oMtZD7r17uv3j75vDVS2h4-B5lmq_c0Y4T1xwEwai-CMYit8KkeTnccrMzrjyX3BrqocplBDZrmd_Q0jJZaeQGsWDqYejo3HYjsw289UpBmsT7A8o6TtWjnbZxp2nWxpu0G8NNUvXiLIzgRNVu46r3FV6iyRgz8Nugs2VyKnPT9fjSPAJ_Sa0aHMElmAxXnTFt0TMiplmTQAGPYTEba8dSOdraaW-Gu9jjeDw-beflrMhBJhdiLnPk0hZl8KxMw1gHGDQgcOZJE38plwXIm0Gr0zUNx2ChYRltTLJXB9OZCvcvYmmDr66wmdCjwG2VZq-upa0Fun9RCvqJXKtBCwwyXqsIUVaqwHwaiFSQq1WK7oQqFamKhKVl30Iegc2Lg-BdJA5cCa3M8SYd7hlrX4NGwYZ5IoPdvT5WesDjY5gY-FTjG7WDrrsdWKPQ0y1PN23mm61S7VXZdEmNe5fIqKG2g1-ZBPmgPfNfhZFWPWPZwyhiBR-plBjGjZ7exZFuU2AD_oIONiZnPjcc1lq2vSIeNRUPqcBRxQDb22AqbG9r5SzHwO4VVx2eRRSyRAB0HD5BqcyXiC1YmKTo_YFEbVPWoHrAFZmjeAZpCXMw1toQxDtZ5CLnT1PpnDuFH6boncLzgDXLyx1wG0A_yNNfouWApTQr5RYoQ2pvdzkvcRilQCdEW6RM1txwlJuwi8oFutHnohlTqWSOhuYN2FTNCE9beQBWbn6R1VGWRjbAFQMb27ZErEcOtxlvQ9W9MqdO-Ny9VqlRPIJHkW-5zPbbHnrlS9d9iTvXIBUfOD41TivaG0k0zb45_vaFdP7hOKB0xAiCnE4FA0prDoOnqMrRCL3GB2JmHqVbhjFm2DNNOKgOrXYSOE7Qfd1DSw-UFhjBWS7DGa0xI7K6jkMOB3M806wXsK3y2t_9iA8UXqKxDcOqTWRsupQ95UupvSpRR_LgJrkF4GmxuXrhS9zV0PPQalvcsHU95k5kx50R0JZpqbV4SK1VEwvsJMmOHCBsWhUbftfupL1mIb8zav0CfytP-_Wro-O9r18cnOwdHR_-cW__-OTN64N9GXRDs-hde-vrbirhzyqP8rR11tWdr49efXfwcg_tSfjz-NX-qxeyIbm4l_kSjXNRC4K2_mY1d4LWQZJ90PbN13Khe4YBBnX-_rd_lwERde7yeJrJK2XMo0pqYQTGTnKGcqAOR5WzZCE9I7woFVh6BV4XRmsG0kq6bnPH83w7ag2FXgFbd1bvVYLWCAThx8xzTVu3e5qurUq7flzvXFfWi99I9wA2iAryyJfKCtRAi2LgVsUCsZc5rAxv5Co-WeuLdSEb3B210Ykpuk5q9YLfKF4afw4M7QV2qZRTHX7EJVniu7KyY6rMhaFz5RqBb9uhwR29PVe9GrnGsHpAlVtyjtNYxwhhxWDOIlYuweYNC5SScD-m4uSOEohGaxiVGGsHH8F8y-CyNsnAkxIcKGUpZXjtNKvDtH3t2k0oF1GipqY_5H4YTY4O1uhKqvH10eF3e_t_Odl7-ezk2eGb_Rev3twcN4tFaEbCcPXIaF39XhlfL9t0i8q8RurZRuiC5WbGfrs6vWK91mJ5QP2dEkel9vf_8b_aAzCS164LfuNl06x2tyMVPm6T97KNLhTYecz9iMJqOQI4H2iljMFaOm69odp139H2Xxw28VPtLfy5RoHvqLB7fVimWaNTd2t9OlLqtCjQAWRo8J-zJJUHCx5pYDmFE3M74pYbO3br23QFiauVo_eqMQThLTl1OBHKJBwtloUMPzQ5IJixsMjB1hMxTjfsVJUAS3NMsGJuQKVbZImM9AVVxEY6g5qsjMMBqvR4ncoeqVR2ly2XuVboFk5mISdHpgpHKlWIhmd9lsaYvNycHt1RBilrzv0Idg8bQWMrqX1ZXoKCS776TCn6oaMawMHyPNPXO9OxV9bZHdUbyjUb7RYIR9ZMgCnaNNer4FTNPaQyEyTPNIMG2tqiP7Xn8UWdN8dDh-dE3f3dwdHhHw8Pnp386eWrP784ePb84ET-e9Q2hSlHNFvQSt8YPZPhmVvlbWWYTU0_-HOXYFrOKlmtBX0dX-QjWEzQTNo1i-xKDwPmmGzqdRunX-PX3zn9eqXxZ0rV1gsyZws1m1fHsKo1oKsb9Ya8b68fpIZ7yg9Jml5rXfrh8gslsrP3T_ZfvTw-Ovz67fHhy-eq6gUukWo9zfHzb_ZePj948ep5WxKjYYIYZC9Ybu-fvDnYf3t0ePyX7lZMUIBggF5QEmEHzw5OXv3xBDp69nb_eNWDVnXAn3Czr_l2DcFhN6__bg35hR3Qw8aPB7-Zo_7-EVF2re8reaAdw6P_Q7-6Q-6q7ps7ojt8Zcetv29gnnN5zoa-ceJx6PLrPV1nwh9EDt_iUW5b7X69qbZOva7O2DTZ1-9XNekvwDdSDtT-8V7j0oLZA6ZqZ4h0scrGFh9vWorb9NQX-kWOQvGe_fbW5Tb9rqSLy-V8ji3fs-vekm3s-ggk-3n7zOcsTTjYfhdX0taNSSdrNHHFtYydJ2dyesb12jZ74oetixlyAEdy0laaSeExy-ZhWAq2jgwo3vRQGosxXyjPS52ekYEYuCjFQHI3OLAZMfALZnLP1VAlQQy0TVXnHFnZZBBU0WldHpGCXSVwAm_PUxjCs6yYOabr6uCK6Y5ruK7lmO309kGJPiTQhyd-ICn0RaXQ7ZmYlglpW5vYn9ZDHzcRMI-CuUShAfeYRsSCyLVCXxcBrKoTe7rtcT0GO1nEhufbpmn4sDE9Fsdc505smpHpW0a8-ZHWgS72xHTXgS6w1yMzEAS6EOhCoAuBLgS6EOjyuUAXn3lh5PkGc_SfGugyGLsh6oWol58W9eILJwpt04vDgBP1QtTLT4d6GRakhMAQAvOzR2BCN0Zc17LAhvsvhsAo1VmXEd-QTBuUBMTCEAtDLAyxMMTCEAtDLAyxMMTCEAtDLAyxMMTCEAtDLAyxMMTCEAtDLAyxMMTCEAtDLMwNLEzohqZpeT6rZeZmFubFY4XvCYwhMIbAmJ83GGOazLFj-3F-nua49sTw2GBEpi6va4_Xu1OZ8xRnlzAtp1cP2FU5uR4t6Q33yigU-vAnsEeVBdd23MtWqdIQsOJUXKv5XWilbhQ4kKpCELWKG2AIUZud0k2BOarb7IAIGW7ePIayyeO1sWCZ_Yu0PAtzVsj-G69OWTdnRb2iGv5m9d2oBmHHjhfGoRH7DvMNDi6JrnPpoqynGpqK8Juphp_yFro923H1tyKMT-sL5L8IFOBEUQQji2NDZ54VmK5tejxwXd8Snu16pmMHPITXse7Yru4HPApZ7MVg9ttgBvjGhudZRwR4E9NZQwR4MNIAHpmIACICiAggIoCIACICiAggIoCIACICiAggIoCIACICiAggIoCIACICiAggIoCIACICiAggIoCIACICiAggIoCIACICiAggIuCnTQSAvmE8xtqELlXSK2fpVTbftyalv4K960DA4eHq3Yulibe7WxYxgreVYs4JVu60tuBZOoZV-jjYxsqVT-sNmVTlSiPdUard0Vu1d-Wmp13-VYkGwjIIyyAsg7AMwjIIyyAsg7AMwjIIyyAsYyOW8Xl-mOMuvx3BNL5EMxQVPCINjV9dwsMM_VTFelIC25S3d43io4y6X5yoO7mYgYeOjrnUiqoK5tqvSdQyEvoDR_JOFITlBqZvB16s615ge34sWBCG0iRbS0G0VfA3UxCP_yMGA8jGmm_8X-UVuvL9L8Ir-Nz2At0Po8ALXOG4hhUHjMHM-tAUs0JuBroVhMLhju87DjxG6FmO6bm-yy3h25sfaQ2yYJgT3ViDLMRRLEzueYQsELJAyAIhC4QsELJAyAIhC4QsELJAyAIhC4QsELJAyAIhC4QsELJAyAIhC4QsELJAyAIhC4QsELJAyAIhC4QsELJAyAIhC4QsELJAyAIhC4QsELJAyAIhC__lkIWAmWHMA98PI-sLIgvEGRBn8KicQbQBMIg2kAXRJqSgSMDwKHj1mYEClQM5gc9k74_MFPTq03rf098v-d1Yoj70kwy9ZjdCBS_q30TofuOgTrvVdUO183tFkvclSeMWbqALDj4umkKkWzTS_ciDGkpTDCRxglrB3A0qMAXTwZ4JecTswHIch7GQ63a0CSpo69RvhgoeY8luj0DcSBV0FfZfhiowDeFFwrQCN7AiWziGafCI65xFPqi8KAAz3-ShJUw78D1hgfNlg9qymBUGPg-NO1EFtjGxzDVUgeXY3ADtSlQBUQVEFRBVQFQBUQWfjSqwI9Pl-KCx_fOjCqK6IJwNWWFo8akWnx28OXz-8uT13tHxy4Ojk8OXxwfPj_aOD1-9JFCBQAUCFQhUIFCBQAUCFQhUIFCBQAUCFQhUIFCBQAUCFQhUIFCBQAUCFQhUIFCBQAUCFQhUIFCBQAUCFQhUIFCBQAUCFQhUIFCBQAUCFQhUIFCBQIWfEqiwr4JmveavNNb_oYVGYDS1U1fL6O4GKQTC1EM3AIscjEzd8CPXZjELzE2QQlv2_g-BFAaQihshha5g_xcIKZgTe91PHzDddEBsCIIUCFIgSIEgBYIUCFL4XJACbCcRRaFwLS_-xUMKQy1-tdrEqNfECJsghoEYBmIYiGEghoEYBmIYiGEghoEYBmIYiGEghoEYBmIYiGEghoEYBmIYiGEghoEYBmIYiGEghoEYBmIYiGEghoEYBmIYiGEghoEYBmIYiGEghuFnyDD0qmq6ovjbVvEMlcx39Q9NV714YtfVLSOXN1Tm93rpxd4eoZdsOQ8F7qJ377YMlHN-MLb-GbaDehlYY7t-ievndx_o46337zePshcW-4xz4UeOEwvbekAvjNceiYqQK0Ps3R467mx37_XBf--i6bgpsFytFKCZkzSvejJuIT6O2NnAWG0wKvXANx59rKXAvkCmv2stq5WA4yZxPDDWXv1fN9ZuHAXoivMrI3logeDAaHoFKbcdzUMqVm4HMfXkykaI6ShfYlSrV9UD5hsGr5rYV1zkf8XwK8r0kSxGbqv05KKNN63KtUdvepRvlIqPilSVKBYM5pg3wLdr2Q26upS5DtQdOeYAwPmAnTHeNPO36bE_vXVyCcGtfKW-RTtPpN_Y5JDwsxJc7eGB9ETrxtkG93GeV2ooa2a2DnKrmQfLdo6HrP3RGTW88SZZu3mRBRivkeq2DezXKQn0WXh3tL9hxbm41F7sfT2CXQALgy5XuUzBb6tnZbxJhm7s_Q2GLMqVR5I9_6pEL0H677gBOqEiq4mQrcPCODAFBHr4401S9YrgUZ3ucVW01Dij32KEU3wEcweTmNLNSWA2L2XgD1a0_amfvliVEnS8SUau7_lIVO2uuZbKqqeclb06iC7RUk_0BiDwWyyo2rBt1iya2km9OVeHqgs91bmPdhzygXvzgsuwKqSvjlSFmJaqTKM7Hb0CB3VMbg8feqHJrch2jMjQbc9ymRVaUcj8TfBhi7PdDB-SnUV2FtlZZGc9yM66PSvdorr1Wk3MnR60a--0g52Yn9bzuV-ESQ4sXce6Ex_uEmYYGB73LOGYBhOeFfi2YL7DHTuIbVPYHOs6uWu7pm95LrjN0mW-04NeI5WDiW5OdH8NqRx6vm2YVkSkMpHKRCoTqUykMpHKRCoTqfwTJpW_NKRrOL7rMPCP4-5XAAnS_flCus3c3gTrbooddq5dP3E_wvDuLugxdhnCTp7tvn77Nej9k6ODN29fHL-psVkid4ncfVxylyBWglgJYiWIlSBWglgJYiWIlSDWXz7E6oRmbNpRYBuRvxlilbmqqsgxRVu1J_ZqoUNdTqxcHbDxwMnJY21722tDTdY0W5P7rv1BCcDGbJ6kiVDhJsN0NTipCew7hrtDg7Ndbm-D2V37eGj0TbNGtssed67HpLoqUjjELCllO2GBNndNC-GaYOQNa-FlDhUrOmT2dHtbe_Jre2xgJAwTCLg5ZOV0-VTJdlkOqeUhVnLDHzA-FgvJpC3YGWubhlnwsVUdWlQOqmv161xhdqWYhOccBAztyDYZaL2wi5qsJWf_WK_C6xUJ3FUBTWpXdF0lglyHZsHWT5S2Okv1Yl2ZA-3aFNQTML4O3s7kIEa9FMQqaXtH13jz7EXcY7HvxjZz3RtgW7mV--UuavpGV4sqpD6v9zxYCD3SWkafyl4Js1gkZY6h4mam5ayoL4vuFkLbV_Beib4mWF0IUzdQHH5zHVZ8sLaIJJXlX2GOVUEg-dHDwgjHYpnWMcAUmQ9wBJclS6eZDE3UVJJ0O1k6wpidZDZqYAufSTE36lTDGVZQsDqq06wfZuuTv22dSVc_3RhBitttyoPuvbqD3zzlGUxnwtf1LubQlRn0ZNl9awQw-y6HCMcfC5aYzD_UpDzW0VytUpo0hx0DD9VF3hoe9TGDyZFlTm_gST5oxtiYZvgdVZrl4_GKpSGxvd0WQdUwCPYFUqTKPwgFd9nu2PxnWBo0bNS1GgZkYRyYg0C6GVenJwsqrOZBGwz0xiwBp3jOvpcRg5HcQhz0JZPMN345AG48LiJUjuNp1ie-Ohw8lZF-8PZHVT4SEjgrwXtt-0FRV-eVFBgEE4cTM5LShs3BIk3-2tQzSiobGf6a5QRdWvMnYiiSGwS25xgWE1bcqsxe3UZfkd2z6GIQWYejnbZlc3LO08sVLH-C_u-ab4K49uUJMCH3_qoHuR0Gv-2h_ZqHQ0n_dNKsi7NILntNPWNT7kb0O9HvRL8T_U70O9HvRL8T_U70O9HvRL8T_U70O9Hvv0T6vc7AbGLgr3x6hYS_9ukqDw9-TDH5QlA8mHPxCYZeiw1EvNQ9HRG_zPAsZLdl4rsC4_v9UFwPGulVCz_mbwT2hngTeVl7cCwspR95tSy6YmcYDOu8WsZzaXSqWC4sOYZNUMfsaM8bvd_ZCnGT1rsCSfaee-MA91OmqralummtikKkifRc6xrpsi70ar_6Pk1kAQaG-1QVcx0XvJjJOtSmYGgDy7iHz1cXHKUCrIWiedLG8MRAwq8Gn_RXKtCIK4hqHyMPsi74ytyyJnmH5MsIC6Q0FUxpCrSUAGcymnPFyW4za3chGJ3I8V078oJYdw3fZ4EuHMEDvolgbDGXWxCMP7FTcXt2c83vFq5iTx3s80WwJ-6D7xW4nsM8KwrcwARDxbFEBA3pnBmxG4eWwUwv9JlrO6bpOXZo67Flx6bPYDU3P9Iq4OQfG_7E0SemuwZwciKbOR5jBDgR4ESA0z8OcNLDSA8drjNbDAFOw6p3iGHyDNcxwdUVoSf-8QzTsM7uo01rS1_lV4PcHW2aZgNsk3ZXtGmaEdtEbBOxTcQ2EdtEbBOxTcQ2EdtEbBOxTcQ2EdtEbBOxTcQ2EdtEbBOxTcQ2EdtEbBOxTcQ2EdtEbBOxTcQ2EdtEbBOxTcQ2EdtEbBOxTcQ2EdtEbBOxTcQ2EdtEbNOXYZs-E490G9znSMQFDLkp3wFlJidZFn0oexIssva30GQEUsI1bbVcrXUx74RuPVYWrmd83iq3s24C5EHNE2AoF8w1FXHV2kVuVbscVBtmbDGkZph3Q3FgQoRh4Q_aBCG3GRhBgR-bssp7LYrTAhk3ozifAZ8ZAIfWsCbGp_UoyRfBZ_RQGFGg26bJmS9CT7cNBre4ThzJiJOuu_Bm5Fu-48T4C0OWzj3XNgPfsuFvsfmR1uEz1sRc9_tAYBZHoecRPkP4DOEzv2R8xgXB5Ooej23fuAM-sxGT-XPDsra-5BX1hrjMNMuzP2h_vjUr85g_A0SsDLEyxMoQK0OsDLEyxMoQK0OsDLEyxMoQK0OsDLEyxMoQK0OsDLEyxMoQK0OsDLEyxMoQK0OsDLEyxMoQK0OsDLEyxMoQK0OsDLEyxMoQK0OsDLEyxMoQK0OszJdmZd5_-v9n9anb)

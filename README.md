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
**Verified knowledge infrastructure for autonomous AI agents.**

[//]: # (ob:0e0e9d9a)
Proofpress gives the next human or agent a checkable answer to: **which
conclusions may I rely on now, and why?** It binds selected conclusions to
evidence, scope, version, policy, and review, then excludes anything rejected,
unresolved, expired, superseded, or unauthorized from governed context.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzU1NmIxMTVkZTcxMWIwY2QzM2VlZDI2MCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImI3ODQxMjNjIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV83YjJkM2M0NTFjMTA0NzM2YTNiM2NiYTgiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2VmM2MyZDU2NDRmOWRlZThmZmU5OWQ3ZCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXVtz40Z2_iuIXNnMaEUK94v2Flkjj1U7nploNN5siVNSo7shwgIBLgBKo7Wnap-S91QqP2H_Qt7zU_YhVfkXOae7caFEQld77d1-8Fgkge6D093nfOfykd9ukLJOE0Lrk5Rt7GzM5yee58eW5TEeWFZsUuY4nDPbNze2NuKCXZ2w9IxXNVxbTYnt-TteGMWUJ5ZlMdfnTmB5rut7sc8ppbZFopi7LomCwIxJHFgBdxKThiSiiZnYFmUhjMvSihYXvLza2PkWX9QnNTmDGTJS41Rb8EfMM3jja16mSUrijBslv0irtMiNKVxflFdGfGW8LYsimZe8quCeOaHn5IzjQy29XRbfcHjcRYkDTut6Xu1sb5-l9XQRj2kx26ZTns_S_Kwm-VnomNtLd5f8D4sU_j5ZVLw8oUVe8Rx0UZcL_mlrY8oJKjEOQteyHboh3znhF-IiUC4_CWKbOdT1LGqZbuD4xIkdGhPUwrwoa3y0kyzNOUjerEh2whOH2szzXTeJGOdhkvAoYgGTj6OkO6FkXi0yeGAb5aRFyaqNneNvN9T0327AKhdlhX_Jjzk7iUHlxxtv5jzfPTD2CsY_bnyAB2k2Bcx_uL_74qv98Qwnu89eIXVdpvGihiU6iUmVVrhjeJackApUV3Mx3qKeFiUKdJ7mOGR1VdV8Bp_kZIYrtyTYFtxf4ZJv7OSLLAMx6RTWiMunjLOCnsMtsO-CwIpduByWp-Yf8SGe_e9__fv__fm_nsObaibCGJf6g33EL-GdX84NkqVn-a8mGxQUxsvJxq8nuWH8Mp2dGVVJ4X0Uva62s-KsGFcXZ5MNuKOG99W-g-Hqq7nYcaQkG5-2OqlAQ1EU8XhJqqXtulauz5a3tZoBNxZs0qVJAs-17dDkD5jk-B-O8_nMgDOICv7wrDkX8OzjapryjFXjtNiGa7YveicCtfB84LG57wcsCv0HSLS5KQ87Z8Z5XlxmnJ1xI82TklRw2mi9KLmRFKUBe6jIi1mxqAzYKXBs8roakMjkJo9YRB4gUXeVcZZe8Mqop9zIYQRjupiR3EBhcHqDGGBDwPigmSJ5dclLY0CiyE5iMAYPWbXfF4vSgNVgoA_jnPN5ZaR1ZczguGTVllEXBf5vxmdgH7eMy6I8r8Aq8i1jzoc2a2iB-Q4c9qBVe1eDlTCmvOQ7m5vGcbnIhZ7MsQeHZT4lBhhQel7hVR-efda9GJ0NSOSDBfSJHz5Aol8bL9PamBHGDVqIfzLwJkVJaljDce9swTXnsKgpDJ-BHeA55UMHOgmIGXoPWbW7Gxq0tzTj1bZcwpFwD6OhlUtil1gBXZJqb1oUFRerMCf1FP4gqJAaNmllXOEWwp2RZING6DPjrsMUl8NWihMaWVZiPbmM3xkHCV5rkJL_5U9_Nr4zur1ofDfJvxuNRuI_-NP4fJFmKBocUHVqi05soedrig3AA1vLQn9ZXBpgi8BlMQPfTfMFQX8nT9ot6rz15gEVRo4VEDtmTyRN7wxUaD9iXl9ynhsluVS6wSFAU0wskJoSzFyyqAc2Y2Ayn7nxU-nsH46P5H2jpftISadpzYVD2BHyTYuqsYb4EgcekDJO3NjzOH16XaaVkRe1ITwD7uMabE5RglkuwQYbMcBTnrPGPBsAYgekdCllnhVHS1L-S2s8d4wzxM-5Ehc_Ht59t9w6sPcodQKf28tI5iCHsbJs2dIPi_CZse6mgcmZn0SJbYaPm7y3Rng9rNN8EWdpNQUdwBoDyPmnyjhFz35qIMTMeTY2DmoDwf_Qfo-tKCDUepxwp6en1XSSz85ZKny7knTUeUrjZz8zKFv5WScd-rol6TzC3ZBbj1y3U_BLi_kpeElxozxhCvUwMgdnJszEZQlHEnQ47oTcng1tb99MQuux63owwxAK7FJcLHL40ABPzme8htPFP4qPEKKpGGYLFThHp1Pk3BiCjGEcxY7jR0-yrvn8ozEa5cVIabC3jAZcyhB2GKl8kMkEYUEOK3kyG1hZ20xiTnz-OPn2CZ2CBZjNcP3mJcAgubgoUo04vASsy1GrEGi3yBcs5Hw8iG6pT4PEX8bb--pBAZOmwtlzuWQEVgriRpBECDdkwO44xIAtcUwf8FvInlSyg1xsJ3ij5GcpaKdUdrUE2Al_gjVhRZIYNanOjUuBTIjBCrqY8XxAizRxfT8M_CeVFWK-vU4ycYhHjXxVvWBXO3BeQG04XvO-ZW9bNpz-AVkJ7EXKWfCksh5NwUpXizmeC7kvVag6EqEWArkZR1udVjO04QI_opLBcA_plYXUSvxr8anKw7SmAs_oBc-JjAiGduUttw6hYmpzz7GdJ5Gk5-BIVhUApOE4w3-VACNzgHZNrmnUjQywe2x8RQa0ZZvEsRPPfBIZJTZvd8NxI1G71fhHMptn_MMz9Ue13Qo9JKPtEztKlk_173A3pNVf_vSfaNwkLoMXTRbslkW9_e4huJRQizqEPJU8vaVVOT6jAi9HEany9pBRGDdlpBZgnWYLPCnV1oDaPG7GjsufTG2AlljBFQBe1AWEcikFfyRwLhg9DC1gn8zmdSUAcV7RMhUvBtNosP1MToJlV7y3KEsEIODw6sVtYdeNiwfWzo1Mm8ZO-MDZjqbCkyMEyXF5GL_gGZw-iGVlMqvameSbmzfBCqKUIZca0ShxriG5u4ulVlUsDQQlpEG-VxxiASKiJ3hV8fIiFakimV7C4IcORSghA3TgxcsG7GUBT81ltmloVfrXDSyIFTA_Nk37_nOMjOPdXqAoQCpmes5KGdc1zujDM3DG1fbu4d6XB0f7e0fvD_fHnUygqXrj04etJqW-oZzQCS05kSlt8UmTH-cnSWI7sWOaIacQDgcW9VxCmIsmFPQvFNnYPZX1l7nDeQHSiSJGKWbChHfzCvPdH7BckKX0qjdCv4TQG0QUJx5YXaiKpD5JYBl4KSChuKOKrR0S-olpun5IaMCpFdgBpSFjEeGB61jEsn04OFHsOiaPfJowymIfUGqcOCGxHZH8wZ0qihFytXac8BMouhJ-xvZHZjiygyMz3DHNHdf5OfxrotaUxjEWjL2Qx1EAO6R799unKF2I7SarClNSTdESJJZPfDf0KE_gAjFGr9CgduLjKwho1vEzeP8yZfUUPglDeDHl6dm0Vq9gzF9uz3-94iwqaUMv8EHRlh-ZTiNtrwChpL29rqCG8xKe-CwJKDO9ZrheqUEN95gKQnf15eXlGC75phKlOFXC613-fJKriTD8uPMs23g1TvUbUUn8Fb6896x7B90dd6oXbhNhN6vtJjFabdN0fDXLtmMCDuDaoz9uSCniKzDZecV3jN05QuqRPTbX6kjIsJ3JO0bqBrxjFGeLRrhXB3v7r9_tP1-_2Thz4RSxwPVEKVfsjl7ZR-2Ox1RzxpubA9OD_Ql8Qi2X0Wb6Xo3nRmL-_qWbutgxNjcvpymF8L0HpwBVXxkHgMIA1GDWqLjckrmP6dVvNjcxXxSDN-rBs_69dTHJO7hWUYAFW83ZAZ8rTLscTrqwLZQ4B0wMIzCOOP6qnmLUU_JvxOhbk3yRwwMW2QW8wHxHWuIfEDPBqBi3b-FTLnJZc03_CAIlAMBuZP_G63VtURtMZpjYgdcagl71Sun6MUWpWVpJqCofnVxO8hYWLdVqpNQVKD5T2QhSloVYLkzbKmysygj4RrUAPHMBizrJmwAD1JHAYFNDlZUHnpz4QWSRxPZdEYOLJ-9VydpN_vDil1qFkVqF58b__Dec6IrLmshdocqMqRvjEjcHnCICqiBZG1Q1ZuO-ZgfWZcHRjF7-puaAaQHt_Ar2ITi7E9BVnfNSGKH1GmRB6PmUU487dudB26qe0uBjinWYvJqjboZ2sOlxjwU-jwWYkJ6xq-Td24-vLtDBkoJwoy4OHvH8DFAXx0UZwe4oxvO88_0HGViFWq1ukcCSdXcawlLiriYQPOCaiogZi1YK0PSggmWb5h3gQWK5hNLAtx03aDdzVzhs4MHjK36N0kMWeZ6dsNBr4UivCKjme2z1roRzntXpSL5s7M93xvFLcbRWm2HhcpatwG3nUsz_bprO52J-YwrITK24stWtVnD2o1Lap4yfwTGE_czaHFuSfkS_10twXCgfOWp95Eiu_7a4fVvN_iVG9zC5yhuCcSW0LOBQzHkB46AuZCNN1UhA2oRPl6ZRYqzKr6iPmvn2L0iG9S-YEh-ll2grDZqRVM5zCCsv90pbTFnKJn54hv9LYZ6lVGObgeqdl2big8bsifSedBiielYJZ0Y674ECvANjeYlbtGcmisu8yV-0-Qh4b53t_G5VDbhB1VboAII2Y9-1umPTloW7Y_OQym4zh8tMNwpci9utfeoVe2-imXvXaxFoLWOeSY5AJs3hoKX12NhtqydtOUK1zAnnA351BnrsEkztVv3FBO6q0YfD3gCzKJFUJcSQgAZGlBsJBgLsV5QzdWJ-0flxEDZJz0BKNskJU3jAUKClvsKJjRbCwO2Lig_Y-yhhJEgSFkdO1IYuXVla6fMxlWU857_o77juY3C8FQ7TszgCM8ZKbjb-8Kz1I91U2_UKYUb9K9Z1XamHthn3ITDlLLR589C9KvfNTXTvQnWJKUbwtoBCwfmcp3gaAamVsC7wFwGPqOqlMkGJyrgBdhtci9sjSxNOr-C2xsWcC6C2wmQb4ATPUrRjaLrl8hvvJEoC2JMssmxp3cTw3T5qJ1pjAAa2ku97YejE1I_cFsD0qvLd8b9_ab2ZgRGXBokZRwFpZuhV29sZ7lU5b-FX7CSO57tUAFYJfLpi-s09ce_COHbFGm8hKoELnbFl_RwiEgBzcoFfI5iz7Z_vDEAzKwyiJIjikLUooVdRVxI-qjoOpg7QLpietMZC7Ez8ZYyumhdSqaNRBVhrxPhFb5B_xocert6ORip-G75MFNDhU2moEeV-nOTwWCsKvM3a2S5AZ-aEJGnDrl41v9HMIyrz4M0TOPbjb8BenY6N9xWcpdNWxIxAyHm6ZZzSRVkV5anwvacwx6nET2A7wHc01Tnh9mHPV9XAYfJsTsLAiyOTt7601wPQ1LAfUc9HI9M3HFsYbwvvA9FUvdUEiARj6jk4p7RJBbTGogm__wCBT906UXxiYWtE9kB0VA9sau67nHk-M303bjFD106wvKkf2hoASFegt25B7wAoGRjzcVFnc7Hok1s2baPaESLdWhQ0jIkocFBVd-g0DQGJlG40aqXe__rgxf7rvf2Tgxc4Bi6OgRLACzW0AiM7EDJDMHmbMtRC7r15vffq_buDN69h4OF7FDRfuqOVE9ccDMFIXgSyiK2w07wcHrnZGdeeS2wN9VDVggJmrYpbRlqkS4PcYhZsM449k7k-tdvEW68VpCm8P6Kt41Q92mmbd5rkbb7JuDXdJFwvamEEJ0qGjcvRV3yFkDEhELfBZIv0VNSmpXxZQSFeUqsGR3ABkOF6MGbMeyBikjcFFIgY5tOxcSSco2uc9jTc5R7H4_Fpq5ezsgCbXPKZqJELLErgWYmBuQ4ANGBwZmmTf6kWJdibQdTp25ZnkdhyrDYn2euD6aDCw5tY2uSrz13CTRr5rdPs9bW0vUAPb0rBOJEZkmiBScYbHSEKpXKsp4FJBbtaZxhOqFaRukxJVvUR8ggwLwrBukwchBJGVeBNJtwzNj4Hj4IDs1Qku3tzLM2Ax8eyMfGp5Bu1QstpB9YoDkwnMG2XhHbrVHtdNl1R48EtMkrUVvglJYgH7cF_lUZajozFDCNKSjZSJTHMGz2_TyDdlsAG4gUTMCYjIbM80iLbXhOPUsVjOnBUM8DmJkCFzU2jmhaY2L0WqsOz8FK0CICPwyeoFHyhZE7iNMPoDyxqW7IG1wOhyAzNM1hL0MHYaFMQx6LJRejPUOWce6UfJhidwvMAmmXVFoQN4B_E6a8QOWArzVK7BdoQGe0uZhWKUXEMQox5RkTPDUO7CbuommMYfcEbmSplcwyEN4CpGglPW3sAKLe4zGWWpbENcMXAxnYdnpjUYy5hbaq61-bUGZ_79yo1joczSkPHJ27YztBrX7oZS9y7B6k8Z_jUqFbEGymd5F8effVKBP9wHNA6YgZBqFORAQWaw-QpunIEoTf4gViZR-uWY44Z9kyTDpKp1c4CJymGr7uI9MBpAQjOC5HOaMEMz2UfhxAHazyTvJewrQsZ737EB4qvEGyDWBIi49CVmKlYCO9Vc5nJg5vEFoCnxeHkwle4q2HmodV2mOWaZsI86iYdCGjbtNRaPKbXqskFdpZkSwgIm1blho_bnbTbLOTXlvQv8LeKtN--OTza_fzV_snu4dHBF7t7Ryfv3u7viaQbwqLj9ta3nSrhz7qgRdYG6-rOt4dvvt5_vYt4Ev48erP35pUYSCzuVbFAcM6lIWj7b5ZrJ4gO0vzc2LPfioXuAQNM6vzlT_8pEiLq3BXJJBdXipxHnUpjBGAnPUM7INNR1TSdi8gIL8o4tl5B1IXZmoGykmm6zAuC0KUtUOg1sHVn9UEtaI1B4GFCAt92Tbfn6dqutJvH9d59Zb38jQgPYIOoJI94qVCgAV4UE7cqF4izzGBlWGNX8cnaWKxL2eDukKATS3Sd1eolv9G8NPEcAO05Tqmck0w_4pIs8F3R2TFRcGHoXPlWFLpubDHPbM9Vr0euAVaP6HJLL1CNMkcIKwY6o6RaAOaNS7SScD-W4sSO4kiNNjArMTb2PwJ8y-GytsjA0goCKIWUcrx2kss0bd-7dgplnKZKNX2R-2k0IR2s0bVS49vDg693935_svv6xcmLg3d7r968uz1vlvDYptzyTWq1oX6vja9XbbpDZ15j9Vwr9gG52UnYrk6vWa9FLI_ov1PmqDL-8m__0R6Akbh2VfIbL5vkMtymKn3cFu_FGF0qsIuY-xmF5XYECD4QpYwBLR210ZAM3beMvVcHTf7UeA9_rnDgWyrtLg_LJG986rb0pyPlTssSA0CCgP-CpJk4WPBIA8vJvYS5lDl-4rltbNM1JC53jj6oxxCMt-Cpw4lQkHA0X5Qi_dDUgEBjcVkA1uMJqht2qiqAZQUWWLE2oMotokVGxIIqYyOCQUN0xqGAqjwuS9kjVcruquWi1grTwskshXJEqXCkSoUIPOVZGmPxcn15dEsBUtKc-xHsHjKCwZZK-6K9BA2XePU9leiHjmoEBysI7NDsoGOvrbM7qre0azbeLeKe6JkAKNoM1-vgVMM9pjMTLM8khwHa3qLftufxlayb46HDc6Lu_nr_8OCLg_0XJ799_eZ3r_ZfvNw_Ef8etkNhyRFhC6L0tdkzkZ65U91WpNmU-iGeuwJoOa1FtxbMdXRZjGAxwTMZNxDZtRkG4JgY6m2bp18R19-7_Hpt8BfK1coFmZG50uZ1GZa9Bkx1q98Q9-32k9RwT3WeZtmN0UUcLr5QIj_78Gzvzeujw4PP3x8dvH6pul7gEuHWswI__3L39cv9V29eti0xBhaIwfYCcvvw7N3-3vvDg6Pfd7digQIMA8yClggneLF_8uaLE5joxfu9o-UIWvUBf8LNvuLbNTiD3bz6uzXEF3bADGs_HvxmDvn9I7zqRt9T9sA4gkf_q351h9hV3Td30Ht8Zcedv29gVjBxzoa-ceJp2OU3Z7rJCX8Uc_gOj3LXbvebQ7V96rI7Y52yb96vetJfQWykAqi9o90mpAXYA1C1AyJdrrLB4uN1S3GXmfpGvyzQKD5w3t663GXepXJxtZjNcOQHTt1bsrVTH4Jlv2if-YJkKQPsd3mtbN1AOtGjiStu5OQiPRPqGcu1bfbEtxuXU-QBHAqlLQ2TwWNWzcOQDLCOSCje9lAGSbBeKM6LLM-IRAxclGEiuRMOMCMmfgEm90IN1RJEwNvUsuZIqqaCoJpOZXtEBriKowLvzqeweOA4CfFs3zchFDM93_J9x7Nb9faJEn2SQJ888a22Qj-oFbo7J6blhLSj7bifVpM-bmPAPAnNhcYW3GNblETUd-LQ5BGsqpcEphswMwGczBMrCF3btkLYmAFJEmYyL7FtaoeOlax_pFVEF3fH9lcRXWCvUzvimuiiiS6a6KKJLproooku3xfRJSRBTIPQIp75YyO6DOZuNOtFs15-XKyXkHs0du0giSOmWS-a9fLjYb0MG1JNgdEUmJ88BSb2E6TrOg5guL8zCoxynbKN-JZi2qAl0FwYzYXRXBjNhdFcGM2F0VwYzYXRXBjNhdFcGM2F0VwYzYXRXBjNhdFcGM2F0VwYzYXRXBjNhdFcmFu4MLEf27YThETazPVcmFdPlb7XxBhNjNHEmJ82Mca2iecm7tP8PM2RjMTw2GBGRrbXtcfr-FTUPPnZFajl9PoBu24nV1NLeuJek0JRH34LeFQhuHbiXrVKtYYAilN5reZ3oZW7UcSBTDWCqFVcQ4bgEnaKMAV0JMfsCBEi3bxehqqp47W5YFH9o0aRxwUpxfxNVKfQzVkpV9TA36y-H6uBu4kXxElsJaFHQotBSGKaTIQoq1kNTUf47ayGH_MWuju34_pvRVifVjfI_yCkAI9SCpIliWWSwIls37UDFvl-6PDA9QPbcyMWw-vE9FzfDCNGY5IECcB-F2BAaK15nlWMgGDH9lYwAgKQNIJH1owAzQjQjADNCNCMAM0I0IwAzQjQjADNCNCMAM0I0IwAzQjQjADNCNCMAM0I0IwAzQjQjADNCNCMAM0I0IwAzQjQjADNCNCMAM0I0IwAzQj4cTMCwN8QlmBvQlcq6bWz9DqbH9qT0l_B3nVg4PBw9e7F1sS73S2aGCHayrDmBCt3KhE8ycawSh8Hx1i68rnckGldLQ3SHSUZjt5pvGs3Pe_qr8o0aFqGpmVoWoamZWhahqZlaFqGpmVoWoamZWhaxlpaxvfzwxz3-e0IYrAFwlB08EhpaOLqCh5m6KcqVjMlcExxezcoPsqo-8UJOcnlFCJ0DMyFV1RdMDd-TULaSJgPAsl7sSAcP7JDNwoS0wwiNwgTTqI4FpBsJQui7YK_nQXx9D9iMEDZWPGN_8t8ha59_wfhK4TMDSIzjGkURD73fMtJIkJAsyEMRZyY2ZHpRDH3mBeGngePEQeOZwd-6DOHh-76R1pBWbDsHdNaQVlIaMJtFgSasqApC5qyoCkLmrKgKQuasqApC5qyoCkLmrKgKQuasqApC5qyoCkLmrKgKQuasqApC5qyoCkLmrKgKQuasqApC5qyoCkLmrKgKQuasqApC5qyoCkLmrKgKQuasqApC5qyoCkLf3eUhYjYccKiMIyp8wNSFjTPQPMMnpRnQNcQDOgaZgFdRykoUwAeJau_Z0KBqoGcwGdi9ifmFPT603rf099v-V3boj70kwy9YdeSCl7J30TofuNAlt1k35AMfq9Z8r4lacLCNeyC_Y_zphHpDoN0P_KgRGmagQSdQDqY-5EKbE5MwDMxo8SNHM_zCImZ6dJ1pIK2T_12UsFTLNndKRC3sgq6DvsfhlVgWzyg3HYiP3Koyz3LthhlJiM0BJdHI4D5NosdbrtRGHAHgi8X3JZDnDgKWWzdi1XgWjuOvYJV4Hgus8C7alaBZhVoVoFmFWhWgWYVfG-sApfaPsMHTdyfHquAyoZwMoTCEPGpEV_svzt4-frk7e7h0ev9w5OD10f7Lw93jw7evNZEBU1U0EQFTVTQRAVNVNBEBU1U0EQFTVTQRAVNVNBEBU1U0EQFTVTQRAVNVNBEBU1U0EQFTVTQRAVNVNBEBU1U0EQFTVTQRAVNVNBEBU1U0EQFTVTQRAVNVNBEBU1U-DERFfZU0qw3_LXB-j-00BiMpnfqehvd_UgKEbfN2I8AkQPINK2Q-i5JSGSvIym0be9_FZLCAKXiVpJC17D_N0hSsHfcVT99QEzbA7PBNUlBkxQ0SUGTFDRJQZMUvi-SAmwnTmnMfSdI_uZJCkMjfrY8xKg3xAiH0BwGzWHQHAbNYdAcBs1h0BwGzWHQHAbNYdAcBs1h0BwGzWHQHAbNYdAcBs1h0BwGzWHQHAbNYdAcBs1h0BwGzWHQHAbNYdAcBs1h0BwGzWHQHAbNYdAcBs1h0ByGnyCHoddV0zXF37WLZ6hlvut_aKbq5RO7qe6YubylM783Sy_39gSz5ItZzHEXHR9vWGjnwmjs_CNsB_UycsaufInrF3YfmOONDx_WS9lLi32Pugip5yXcdR4xC2EyIlEZcgXEjncxcCfbu2_3_7XLpuOmwHa1ioNnTrOi7tm4Of84ImcDsroAKs0otJ5c1orjXGDTj1tktZRwXGeOB2Tt9f91snZylOArLq5J8tgGwQFpeg0pd5XmMR0rdyMx9ezKWhLTYbHArFavqwfgGyavmtxXUhZ_xPQr2vSRaEZuu_TEoo3XrcqNR29mFG9Uih9FVZcoNgwWWDfAt6XtBl9diVoH-o4CawAQfMDOGK_T_F1m7KtXFpeQuFUs9bcYF6mIG5saEn5WQag9LEjPtK7VNoSPs6JWoqzQrExyK80Dsp3hIWt_dEaJN15na9cvMgfwStW0bWJfliQwZmHd0f6SlBf8yni1-_kIdgEsDIZc1SKDuE1qZbzOhq6d_R2mLKqlRxIz_1OFUYKI33EDdEZFdBMhtw4b4wAKcIzwx-us6jXDoybdZappqQlGv8IMJ_8IcAeLmCLMSUGbVyLxByva_tRP36wKCzpeZyNXz3zI63bX3ChlSZWTqtcH0RVapKLXEAK_woaqNdtmxaKpndTTuTpUXepJ1j5aOcQD9_SCy7BspK9LqlJMC9Wm0Z2OXoODOiZ3Jx8Gsc0c6noWtUw3cHzixA6NSbiOfNjS2W4nH2qcpXGWxlkaZz0KZ92dK91SdeVa7dhbPdKuu9UKu2N_Ws3P_UE4yZFjmth3EsJd3I4jK2CBwz3bIjxwotDlJPSY50aJa3OXYV8n813fDp3Ah7BZhMz3etAbTOVox7R3zHAFUzkOQteyHaqZypqprJnKmqmsmcqaqayZypqp_CNmKv_QJF3LC32PQHycdL8CqEm6P12SbqPb28i663KHXWjXL9yPML27DX6MXMWwk6fbb99_Dn7_5HD_3ftXR-8kbVYzdzVz92mZu5rEqkmsmsSqSayaxKpJrJrEqkmsmsT6t09i9WI7sV0auRYN15NYRa2qLgss0dbtib3e6CDbiVWoAxgPgpwiMTY3gzbV5EzyFbVvGQ8KAmxCZmmWcpVusmzfgJOawr4juDsMONvV5ibAbhnjIeib5I1tFzNu3cxJdV2kcIhJWolx4hIxt2QL4Zpg5g174UUNFTs6RPV0c9N49nN3bGEmDAsIuDlE53T1XNl20Q5pFDF2csMfIB9JuOCkzckZaYcGLYQ4qgkjqgDVd_p9rqBdYSbhOQcJhi51bQJeL-6yJiuZs1_IVXi7ZIG7LqAdGYqu6kQQ69As2GpFGctakot1TQfGDRVIBYxvEm-nQohRrwSxzLS9Z2i8XnuUBSQJ_cQlvn8L2VZs5X67i1Lf6HpThfDncs8DQugxrUX2qeq1MPN5WhWYKm40LbSiviy6WwhjT5H3Kow1AXUhmbohxeE312HHB2mbSDLR_hUX2BUElh8jLMxwzBeZzAFmyPmAQHBRkWySi9SEZCWJsJNkI8zZCc6GJGzhMynOjTrVcIYVKVgd1UneT7P1mb9tn0nXP92AIMXbbdqDHry6g988FVjEJDw0zS7n0LUZ9GzZQ3sEsPouRITjjw1LRNQfJFMe-2iudyntNIcdEw_1ZdECD3nMQDmizekdPMm5YY2tSY7fUWU4IR6vRACJzc22CUqSQXAusCJ1cc4Vucv1x_Y_wtIgsFHXGpiQBTmwBoHsZlydni2osZsHMRj4jWkKQfGMfCMyBiOxhRj4SyI43_jlALjxGKfoHMeTvM_46ujgmcj0Q7Q_qosRF4SzCqLXdh40dbKupIhBoDhUzEhYGzIDRJr-selnFKxs5PBLLif4Usk_4UOZ3ChyA89yCHeS1mX2-jb6juyBTReDlHU42lnbNid0nl0t0fJ3MP5d8U0QN748ARTy4K96ENth8Nse2q95OBDsn86adXkWwcte0c_YtLtp9rtmv2v2u2a_a_a7Zr9r9rtmv2v2u2a_a_a7Zr9r9rtmv__k2O8fPv0_L5ibLA)

[//]: # (ob:87dd93fc)
# Verified Knowledge Ledger

[//]: # (ob:b71e5de6)
> Status: local MVP in `proofpress@0.5.0-alpha.1`. This overview describes the
> append-only ledger, context gate, and local review UI. It is not yet a frozen interchange
> specification or a claim of general long-horizon agent efficacy.

[//]: # (ob:24505103)
## What it is

[//]: # (ob:1e12da99)
The verified knowledge ledger turns **bounded** agent telemetry or artifacts
into candidate knowledge that a later human or agent can inspect before relying
on it. It is the trust layer above observability and memory:

[//]: # (ob:e2507278)
| Layer | Primary question |
|---|---|
| Logs, traces, commits, artifacts | What happened? |
| Memory and ontology | What does the system remember and how is it structured? |
| Proofpress | What may be relied on, why, by whom, and within what scope? |

[//]: # (ob:a0ce3955)
**Memory is retrieval. Ontology is structure. Proofpress is trust.**

[//]: # (ob:5e5ed818)
The ledger does not make a claim universally true. It records the source,
selected evidence, declared policy, review receipt, lifecycle state, scope, and
expiry or supersession semantics that determine whether an organization may
reuse it.

[//]: # (ob:7a1cac9c)
## Current workflow

[//]: # (ob:c3d2a28d)
```text
bounded OTLP-style telemetry or artifact
  → append-only source and evidence events
  → evidence-bound conclusions
  → deterministic checks + LM recommendation + human review
  → governed current context for a fresh human or agent
```

[//]: # (ob:2ef561dc)
The reference fixture is
[`examples/verified-knowledge-ledger/demo.otlp.json`](../examples/verified-knowledge-ledger/demo.otlp.json).

[//]: # (ob:5c8c136b)
```sh
proofpress evidence import demo.otlp.json
proofpress propose --statement "The current conclusion" \
  --evidence EVIDENCE_ID --scope demo --proposer agent:runner
proofpress evaluate CONCLUSION_ID
proofpress review CONCLUSION_ID --admit --reviewer human:reviewer
proofpress context --scope demo --actor agent:successor
proofpress ui --scope demo
```

[//]: # (ob:58bffc74)
`context` returns only admitted, current, in-scope and actor-eligible knowledge.
Rejected, unresolved, expired, and superseded conclusions remain in the
append-only audit history but are excluded by default. `ui` renders review,
receipt, context-preview, and lineage views from the same Git event projection.

[//]: # (ob:727d3616)
## Claim relations and profiles

[//]: # (ob:8bbc19d7)
The general ledger can record typed relationships between evidence-bound
claims: `supports`, `qualifies`, `contradicts`, `supersedes`, `depends_on`, and
`same_as`. Relationship structure is checked deterministically for valid
endpoints, shared scope, duplicates, and directed cycles. Those checks do not
establish semantic correctness. An external judge may recommend, but an
independent human must admit a relationship before it appears in governed
context.

[//]: # (ob:fdc2073a)
```sh
proofpress relation propose CLAIM_A --to CLAIM_B --type qualifies \
  --proposer agent:resolver --confidence 0.82
proofpress relation evaluate RELATION_ID
proofpress relation judge RELATION_ID
proofpress relation review RELATION_ID --admit --reviewer human:reviewer
proofpress graph --scope matter-123
```

[//]: # (ob:c82e0806)
Core claims remain domain-neutral. Optional profiles add bounded validation
without making domain fields universal. The first profile is
`proofpress/profile/legal/v1`; it requires jurisdiction, authority, and a
citation locator, and permits effective dates, document type, and legal status.
APEX-specific rubrics and task logic remain outside Proofpress core.

[//]: # (ob:5d269544)
## Relationship to artifact provenance

[//]: # (ob:1acc88ee)
Artifact provenance remains the portable trust primitive: it binds a durable
artifact to revision history, evidence, actors, and decisions. The knowledge
ledger generalizes the same trust semantics across bounded workflow activity so
that a fresh agent can start from governed conclusions rather than raw context.

[//]: # (ob:067a97a0)
The two surfaces are compatible. A portable artifact can be a materialized view
of governed knowledge; it does not need to carry the full telemetry graph.

[//]: # (ob:d228259c)
## Non-goals

[//]: # (ob:9a909f30)
- Not a full OpenTelemetry collector or real-time trace backend.
- Not a generic RAG, company brain, or replacement for memory.
- Not a semantic truth oracle or a guarantee that every relevant event was
  captured.
- Not a complete RBAC, connector marketplace, or hosted governance service.
- Not evidence of general agent capability improvement.

[//]: # (ob:b47338ab)
## Evidence boundary and current focus

[//]: # (ob:b324002e)
In the published controlled agent-handoff study, ordinary handoff reused stale
work in 12/12 trials and Proofpress-assisted handoff did so in 0/12; both
conditions continued unchanged work correctly in 12/12 trials. This supports a
version-checking mechanism on that task, not a general product-efficacy claim.
See the [open study package](../studies/agent-handoff-artifact-provenance/README.md).

[//]: # (ob:c8235573)
The next public proof point is a design-partner workflow: select two to five
conclusions from a real long-horizon or multi-agent run, bind them to evidence,
apply the review path, and measure whether governed context changes the next
decision. Until then, finance and agentic-commerce interfaces are illustrative
product fixtures, not customer validation.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzQ0NTQ2YTFiZjE4NzUyZGIzNGJjMWViNyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjQ5MzdlOTA4IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV83Y2RhODk1NjE5YmZkOTNjYThhZTI2NDciLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2YxMTNkN2FlYmE0MjJlM2U0NzQ1NTFjZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtW-1y20aWfZUuzp9dh6TwSQCaqtnV2JqUKrKdcpzMVoUuqtHdIBGDAIMPyYzjv_sA84jzJHtuNwCCikTZkrdma4tVjiQS6Ivb9-Pcc28jH0e8rNOEi3qRytHpaLNZeJ7vzbgdJ3YY-I6MXS8WtoqD0XgUF3K7kOlSVTXurVbc8WenfiCDwElci7uJb0lfStuzfVfFKvZnPPRmVshj6UZhJAIVxNL3pSsgkSfKjmeeC7kyrURxrcrt6PQjfagXNV_iCRmv6VFj_BGrDF_8pMo0SXmcKVaq67RKi5ytcH9Rblm8Zd-XRZFsSlVVWLPh4j1fKtrU3tdl8YvCdpuSBK7qelOdnpws03rVxFNRrE_ESuXrNF_WPF-GrnWyt7pUvzYp_l40lSoXosgrlcMWddmoT-PRSnEyohe5gYqscGS-WahrfROMqxaBkDyM_JkdxYmMXMFDrpyZR9bdFGVNW1tkaa6geeeRbJHYtisDrmLuOY5ylRd4vm8LZbbTarcQfFM1GTbskJ6iKGU1Ov3546h9_McRvFyUFf1lLiu5iGHyn0dN_j4vbvLRO-yhiwc8WhaiOvnp_M3F3y7OXyy-e_X675fnL749X-ifb6ZrORp_Ufjwui7TuKnhtUXMq7SiIFJZsuAVrFkrLa-pV0VJOr5PcxJZbatarXEl52tyZqfrGEsrCoDRad5kGTQXK3hMmT3HWSHe4-4wkLByInA7nFWrD3UfRUqy7yApU3Kp2CX9LHFX-1QupVZnQ2GmbvDNn9ihZfV2Q8qRuxE6o0_jnQpxYCtfqtnTVfgL-6HmdVOdMojmGXv50_cszdnVLgb-05r6U2vCs82KT-2rKXuL7GCUWjsdN7zkewo6nm_5tuXuKfj3Fa9Zin_VQaP8ie3deMAMtrIdyaPoEU95u1LsujPY-95g-mfJ6qbMK_bsWVw0OVY-e8aQO3nNapWptTqwb-X4VuAE4SM0-p1d8i2e_TsgJ11zoM-vDZCK4Oj3ef77ZDLR_-FPdlksqzGrSy4UfgNg1ulOJ53ve0pxSyg38v1HKPXs2Uu1JiSEy0uFVFPXPJuy13ldZMVSf10BqAQMpqYDrKQLB8zkK1_J0A4f6bjWS7JQFcuLmq35e8U4ExlP16zJUzi24lm2ZYShU3ZRMwNOBzQKuC24iPaT-nlTluT2m6J8n2TFzQNhe8ftB4JXuNLhTigf_cSrqytaNc_bKGWv315-P6nqLSqZCdQajitK1uHpPGfsn__9D8ZRNHI52aknCrkfMY5KUE7k461BXipVorBAKJakHyhA4Nl5_vOV-sDXm0xVJ13-Tfr8m-ifhwJHhMJ2Z_FTjFat5vkO3hiuSK1luqZqySQCflrU2Wb6S1Xke7duDpjMD-MkEYH3eM3aZVeUaBp_ihwhzOU6rVHHkOdG2Bj4PAG32SDkc8l0AT5kMenMIt_b1-uNAg0CslSrdMPqoo8Qhs2isvNc84BDsf55Eg5hNxciDJX6mnqd_fF2GHPNUxizRkR2bIhwoaK7UtgWaHEK2DlgQmsW8Cjg1tdUlRKkvilY1ZQJwTjWK0LyDYRCwyk722nbixY8Z7E6BKzScULHvwVjr4p8six49lDZHd53wHMRj6wI3PzLnzHBI2oAdQJyxV4DhN72MCWKLFMUygRYpeLZpE7XytQ4FoN273TKQM732ZAXuC4agj2Fzru01uhI5ZSypc0hlhSiecgcnyfhEEtzHc-yHPU19brITSQ3McywAuiT5JKMJw1HmYCxyiJJUJcbuR3DnNCLHrPiB-JGhI7r-4H7NVWlEM8hySgrmAZSRHWaU41HGEhVpct8AmXqHOW8A8lTVv2hBLwbdy3HiIo7sX2BKDH8Xl_pmgW1cG3LUgH0EZYStnRnoZOAJxJZBlnQMrvMarsihv5MvNea6Sav1E-iFqD7RB3AO2qnsJHtQMKwxRoI0c3bI7uvqkjqRYJYUiUAqm3yqtg-jUQS-qGIlfJnrjNzrND1PEfYgUoCzwshIIrtWSScwJ55XPqRa1lihoZZ2rHtebT_ClxfN2vGW6eOhR6Hvhk5ljObWOHE8d86zin-WdE3lnVqUZa3Fid666vAikSE2Nl9-_F_s7_TAWr6rxWvVrjfdaPAt0L0_Q4xWi1j0JK1sfvFrVUrXdoiEZHj-DJRnfRBt9VKf0rXRNlBoS_Qtypdl-b5XzpOpku-obdj1mYiWyLOxzr3zNNMhrEfLzS1TQ0H3iqNrGXxm8qhS61K07uS8GqjBGwhdMHSjLDlyshHYIYqITQr8uUEbXL6G24x3Y5KaI3YTu8AjtZcDvdsy_dDK3K9zlyD3q9zxsMtXSvPchIpYhkgYsNO3qDLa-U9pXm7xYnBSGGsgkqrTCUMPZBXk86c0cSoZKtmzY3ttDAqxaAVMGyNkpwUJTGNbIvtzHMYMK073xBaG7qR6faOxwgCVsQVIoHHaZbWBlbXus86vd_Uwp4lTpAknvKDzjSDdrM1zdO6yBp_9JaBDO21lY5NJf9DS2BtQ0g6F10b2N6pGzLasBmwEPdS65g2jZtXxQ3ZAzHQd4ydyEHf2Epa8y0xHZiUXFzkY3azQjGLt_hdrE0y3KT1Ckl3Q_drPgxpd7XBrf3AWEI-cwM0wz1uDDrj1n5PaXi1m6fPnt3vQw54UTPflb4XdzoMeuFBeD-2xW3tXzSlUON5XiliVTBh1-WMAT0QAtszU8zGHZxgvUo3aC-yNFFiK1AeqVxghTautvkc9XyTmgyqmg10MPMyVGxkR52KyiSNVEiZNYoevKOgEEUA1ix5nv5mQAgOnuelaipFuXK_xeIkShLXt5MgtDuLDXr1HcB8XvPdobwMQpWEcRDM-lgY9OOt1Kc22BrMjSt0wPadpiYsVXd39_VEP4ZQX2QNWbW_ozMniC94lOYZFfuGXb7UTl-v8TBj1W9amDIu7ZYvqezkakfdusKS6FKQIH5Xt_BtnmPzd3S7rf184YJWKIpc3sP-bmYwiONHDwHKk_1G_Ordv02nJ1-87N8PxBbn3I4cbCWKZZ-NuwHDLgqeMDEoi02BGJ9MdC6tyfpzbZiBL1p3z0dsPiefTSb9E85_unhx_ur5-eLiBcnQXT89Dh9a0a3DTssmRyG_pSfPGippz1-_en754w8Xr19Bzt4tbe7v3QDZeuiA3-ZyV_1Ou497IrpguqWenku0ulWNQI2piv2FTbq35oGQA6cV8FPMkyDqnbWbuXTOesIQZYJis6Tme0cBpvP8jfpFI-gYqAu1i-ya_tYwSH_Q6hYJpdpL3nbyQLxQc7whKPBGwr79KVNT6_ZffcBakoIyJ1XCmwws4qpJaTPAn7Jz15iQswXrdr-Ttu1qaWLb1tA3FXHCtakKHB31t3iwxh_WnlpB1wM5olwvQsFMYsfuWcdgpLTD30cPhDpI5iEwWSrLnc165rebEbUPesqEh8XoVHXf2ZR0D1zSSYO-t8_-xoOSaQ65jG1RPvV9FVH6QajM87Zkt4Q6_a3jQnzdqbOrklyUBVKgKyxd0aInpddECSvkQ8s_DT7vaCeQBKCjvbpD9mHccV1xsRqFgN90IXLAyZbnKQttI-hk7-TB0GsA548dWXEUfNSwVNtFMlOdqPvoNtDb8c_kqZ725ArXND0vkShkTj072lXfZck3qwNbS2I0c570_IT3sDEYku3i94HhVxellhS-o2RgqaQTN5iHteKeMudCpgN1Ogk6mFDz35x9Oza2zoEXJeJ9bARsMixcm3lM2TYRg_VdxFEA1iss4cTrdNlfNjAVIqPtcxSdlRPhRtXIO4i44ZqDCL7RdH0gmHTJQEvYm7-ePdcwlJttoed4r2qtllZxVVTEP42jdb5S55MK1Qvri92gG-2ifdO1SCi1lPG00-kdo8DO24oHIp7NrJnf85LBdHDn7UfP9toHzWLPmnF0FK5w-gftxn3tg54yrDPfa4YsKeUJrwgmqJ7YzontwKVIp0orvutDJhyEXFu8E4G2FmhCyyys-jN2XIPOQBOUII0XpFSaN1jS5GZmYAAJF2AOUaNe3XpmO81A3aOEhwrzvJ0GTTQ5hbEQiiQrrdaowCbCal69H-us5r2f4VSJZmrSjRpMg4PQ-EHHpWI_o0TnxjysfftCE0H6JgUP3DPjpIOdya48nLw5P3vx8ny6loeoYOA5lgpdz3c9q28IdjPRAQI-dqJJWa_hE2iWoCJpF_SYrdGca0DYn8RQRoEHpBOTEWB5Y13HyDhrktVXKc0wMgOSLa0DMq_G7XSBV0S-u3ZsWDg0e2tfdNCrc930dIVuyn5EfGR0Bc9OUpPEmjWRSqmY6BaEmhw9dtrVhjTD9oBstd5u6-quD6hMKCDR6gKrGbhqarqYP7jp3Sfy1B2vnCiEcP_CCRHGD6N3-vUVPOiP3996QWXHRCciS80NelbS39GS3hS2KeW_4kUWlV-nZZET6C1wXet21_ss2hG711nMjj_vZZbACaQ7s_ffJHmupwxlx-i0s2GuJEXn9dAZ-OGlB05Lwhi2iGTwVTShTO0nm4aXCd0XUwgw0kLupIKxgoqp-kYBatT1gWOSRArHClz-VXT8Y2PZyejbxueXZxcvF2fok5Dp5sNf6cP20Ek0cEtZofV1XPqcJpsalPuGRhb0a5KrBrlNs7ENiTRgruWh3ZJUWO84xDGS7ovAW1q0pzUvUI01wyFs2n94Ow_r7daPrqb3hdZnPOK2F8Z9Iz1mvzSIpW5kZqBVM1A454IR1E_vi5fPeHDRGfJSLXfm7CnK9D4v3y36O6U27Oz78__ShRdVZYmKVTR1hXoxHFwiI8hc7wbR8nF0s9re1q5Lp1smp-XjHc-kTtuMBDu1jZXu3htt6fMP9g6852j2PDyxG55WDU_xPh5h8AiD_2oY_PwT69sntt6nu89jHzqc_ion0EHkJp4T2L7jIP8cDrbsSgVtI_S_CQ8iy04CB4Jd3wvd2HdI-AwdGRJ3Fgrrnv3cfQDtBHccQPevQR8PoI8H0McD6OMB9PEA-ngAfTyAPh5AHw-gjwfQxwPo_4cH0IFUTjATwvOj_lx40K0P8PeLW-7uiDu0Xd9KYt9SPcIPuvABljy2lR7C6zw3beQpu-rOT67G7OrXhmeEJ_qDPiaCnsJc692rP0lFbqwWQKS2JF6RXRe8AsnfO4XveQJxAw3aSu5DuS7gBMJ6-o7imkt9mgEWVq10jW5Lr2w2GdF31Z2Cp6Up67pO6wMhQpm2MsiCKAPEVUSCUoB7Px9qz5RwCYvOYJwPNZ0LZmaypmlXX1LGJjBzYshm1xQ1pk6sidAalOB7du_IMF1AwHMELRKgq0D61OWB03AP7Z0bet5MiT7iBhOPe1H5C8YWivX-7iH3NpyaVC9xBSonLRxb09C5-6E91r45vzx7eyfStncaSz94W4vMg_u-EJfNYLRD2DUdYJQT23EfwFkvcZxIgV5ZPBwcxXWznG6Q84SBjKZSu_OmeU5Evmg0x6WjSyMIfEFloLM91zUvfCRpqV8sMbNZ4hKDpvuk_f4koynnybV9pV9n6P4Pb5i-TCvK65Q6CnOOg_7L5BRHcKZ1O8hGnw1oNhc2lLBoh9AOE1yie5MmE2U_n91uugZdj1crPRxA8aD576TrvlnZxKV--4TOD3dD4dZ-986Gjy8HHV8OOr4cdHw56Phy0PHloOPLQceXg_6vvRz07tP_AP08s84)

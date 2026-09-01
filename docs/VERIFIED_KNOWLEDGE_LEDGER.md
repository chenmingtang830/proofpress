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
Rejected, unresolved, expired, superseded, and unresolved contradictory
conclusions remain in the append-only audit history but are excluded by default.
`ui` renders review, receipt, context-preview, and lineage views from the same
Git event projection.

[//]: # (ob:727d3616)
## Claim relations and profiles

[//]: # (ob:8bbc19d7)
The general ledger can record typed relationships between evidence-bound
claims: `supports`, `qualifies`, `contradicts`, `supersedes`, `depends_on`, and
`same_as`. Relationship structure is checked deterministically for valid
endpoints, shared scope, duplicates, and directed cycles. Those checks do not
establish semantic correctness. An external judge may recommend, but an
independent human must admit a relationship before it appears in governed
context. An admitted `contradicts` relationship quarantines both otherwise
eligible claims from default context until an explicit human resolution either
supersedes one claim or records that both must remain withheld. The local MVP's
reviewer identity is `self_asserted`; a policy allowlist can restrict the
declared resolver, but is not authentication.

[//]: # (ob:fdc2073a)
```sh
proofpress relation propose CLAIM_A --to CLAIM_B --type qualifies \
  --proposer agent:resolver --confidence 0.82
proofpress relation evaluate RELATION_ID
proofpress relation judge RELATION_ID
proofpress relation review RELATION_ID --admit --reviewer human:reviewer
proofpress relation resolve RELATION_ID --disposition supersede \
  --winner CLAIM_A --reviewer human:resolver
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
- Not a complete RBAC, connector marketplace, or Proofpress-operated hosted
  governance service. The repository's single-owner self-hosting reference is
  operator-run and experimental.
- Not evidence of general agent capability improvement.

[//]: # (ob:0c8c8244)
## Design-partner integration path

[//]: # (ob:894f0ece)
The 0.5 alpha is CLI-first: the local append-only ledger and portable artifacts
are the canonical trust core. A partner should start with a small project-local
wrapper that invokes the CLI around one bounded handoff workflow; the partner
keeps raw telemetry, prompts, workspace state, and credentials, while
Proofpress imports only the selected evidence and requires explicit human
admission before reuse.

[//]: # (ob:ad275218)
The Python SDK is the typed integration contract for the currently supported
operations and lifecycle semantics. MCP is a
host-facing tool-discovery adapter, useful only when an agent host needs
structured tool calls. A plugin or skill is host-specific installation and UX
packaging, not the system of record. The intended order is therefore: **CLI
core, SDK contract, MCP adapter, host plugin.** The public repository includes
an experimental single-owner self-hosting reference; it does not include a
Proofpress-operated cloud service, enterprise tenancy, or an SLA.

[//]: # (ob:7f3b61a3)
A two-to-four-week design-partner pilot should qualify one concrete continuity
failure, govern two to five conclusions, compare the ordinary and governed
handoff, and measure whether the next actor reached the right current context
and whether review changed a real decision. Only after observed friction should
we choose a CLI wrapper, SDK, MCP adapter, or host plugin. The self-hosting
reference can support bounded cross-machine testing today. Organization-backed
identity, team collaboration, policy administration, checkpoints, and managed
retention remain later product surfaces; local and portable verification must
never depend on a hosted service being available.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzQ0NTQ2YTFiZjE4NzUyZGIzNGJjMWViNyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjNmNThmYTBjIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85MjllYTIzYTI2YjY5YTdmMjdmM2E5OGEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2YxMTNkN2FlYmE0MjJlM2U0NzQ1NTFjZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXety20aWfhWU5sfsOiSF-4Wpml2N7U25osQpx8lMVeSSGt0NEREIMLhYVpz83QfYR9wn2XP6ggtFUrKkTDI7XeXYEgF0nz73yxfw4xGp2zwjtD3P2dHyaLM59_3AD4mTZk4cBS5LPT-lDk-jo9lRWrGbc5Zf8qaFe5sVcYNwGaZuHFIS2HAnd2LOeOq6dhiFIfEDwhMaUdv2kzixeWw7NglCN_JJmHLfSxPuuLAuyxtavef1zdHyI_7SnrfkEnYoSItbzeCHlBfwwfe8zrOcpAW3av4-b_KqtFZwf1XfWOmN9U1dVdmm5k0Dz2wIvSKXHA81-biufuRw3K7GBVdtu2mWx8eXebvq0gWt1sd0xct1Xl62pLyMPft48nTNf-py-Pm8a3h9Tquy4SXwoq07_uvsaMUJMtHLgjgjNj2Sn5zz9-ImYC4_T9yEE9cjbpiGCYkyN8o8ksQEKavqFo92XuQlB8q1RIrzzHE8FhGeEt91ucf9yA8Ch3J5HEXdOSWbpivgwC7SSauaNUfLHz4eqe0_HoGUq7rBn-Rlzs5TYPkPR115VVbX5dE7OIPWB9iaVbQ5_v7lm1f_9erli_Mvv379t9OXL754eS7-frNYs6PZJ6kPads6T7sWpHaekiZvUIl4kZ2TBrjZcrFe166qGmm8yktcsrlpWr6GKyVZozA1rTN4tEEFOFqWXVEA5XQFEuPyzGlR0Su4O44YS7wMRQHCavmHttcizqwvYaWCs0tuneLfNdyldiWMCXI2qGb8Gj75k3XosfZmg8ShuEF1jn6dDSSkkcMDxsPHk_AX69uWtF2ztGBpUlhfff-NlZfWxaAD_2kvgoU9J8VmRRbOxcJ6C9ZhoWkNNG5ITSYEun5gB47tTQj824q0Vg5_moNM-ZM1ufEAGxwwdUaS5AG7vF1x671m2FXPMPF3bbVdXTbWs2dp1ZXw5LNnFthO2VotL_iaHzg3dwM7cqP4ART9Yp2SG9j7F3A5-ZqA9_mpA0-F7uiXs_KX-Xwu_oMfrdPqsplZbU0oh3_BwazzgSZh7xOiwG1wLwmCBxD17NlXfI2eEEReczA1_p4UC-t12VZFdSk-bsBRUWAYX4x8JV44wKaAB5zFTvxAwSkpsYo3Vlm11ppccYtYtCD52urKHATbkKK4sdCHLqxXrSWd0wGKIuJQQpOpUT_v6hrFfl3VV1lRXd-htjtuP6C81GMucWP24B0vLi7wqbNSaan1-u3pN_OmvYFIJhW1BcFVtaX96VlpWf_73_9jEQgaJZsP5NGKTTXG5VkQOuzh3EAp1Tzj8ADlVpZ_QAUByZ6VP1zwD2S9KXhzrO1v3tvfXPx9SHFoTB0vTB_DtGZ1Vg7uzYIrTFCZrzFaWgwUflG1xWbxY1OVk1s3B1gWxGmW0ch_OGXqsQs0NOF_qhJUmLB13kIcAzuXi83AP88ht9mAypfMEgH4EMeYGyaBP6XrDYc0CDxLs8o3Vlv1GmLBYSGyk1LkAYd0_X4rHPLdhNI45vwp6Tq5fTswc01yYGYLGqmzIfQLDd6VA2_BWyzB7RxgISSeJImI_ZSkooG015XVdHWGbhye5-jJN7AoULiwTgZq-6UpKa2UH3KszHVjN9hyY19X5fyyIsVdYXd83wHJJSSxk8yzP32POWzRgqPOILmyXoMTetu7KVoVBUdVRodVc1LM23zNZYyzUki7B5oKSM6n2ZAfeV5Mpk7hpTZr4R0xnKK1KBuysop2d7HjfiscytI817dtlz8lXa9KqcldCmxYgdPHlWtkHpM5yhwyVlZlGcTljt3MgJ1AF26zIgf0hsauFwSR95SkooqXsJIkllrCkYJW5yXGeFADxpv8spwDMW0J4Vw7yaXV3AoB72a65DjC4I7ZPgUtkfm9uKKLBX7uObbNI6CH2pw6zAtjN4M8EZNlSBbEmtqyVFVkQX1GrwRlosirxU5YAujfsAJ4h-UUHORmtMK4xBotIoq3B1ZfTZW15xnoEq_BQakir0mdZUKzOIhpynkQem7o2rHn-y51Ip5Fvh_DAknqhAl1Iyf0CQsSz7ZpmAYhc1LH9_H8DeT6oliT0lq6NtQ4-MmRa7vh3I7nbvDWdZfwx04-s-2ljVauOI7pbcAjO6EJ6M7w6cffsr4TCirrrxVpVlgJe0kU2HHEIxczWrHGqCRTuvvJpZVanTk0o4nrBizjevVRtaVWf0zVhNaBqk-hbuUiLp2Vf9E5mQj5Mr2dWcoSrUvQ85mwPbmbtDDru1citc1lDnzDhWetq595CbS0vJa1Ky7ebDgFXlARsERGqHJlsEfwGbyGRYuqvJxDmZz_DLfIaodn-Ay9WexwHIpdLvEdOwhiO_F8za5R7aeFcXdJp9az3YzRlEWgsbFeb1TlqfUeU7xt5cSQkQKzKgytLGfA6NF6LdJMLOwY1daqWxPJO7EYhmJIK4CxLYTkrKox0yhu4DhnJTAwb7Vs0FvLdKMQ5R1JQQmsKm1AE0iaF3kr3epa1FnL_aymToidncznQaRZMyo3FWseV0W28EPPGVhDSG0ldJOz_xArWKogRJorXQaqO0VBhgeWDRbMvfg6xUPDzavqGvkBOtBXjHrJUd2oVlqTG8x0gKUo4qqcWdcrCGbpDfxbraUxXOftCozuGu8X-TCstqsMVvyDjCUmoRdBMdz7jVFlrPj3mIJXiHnx7Nl-GRJwLzwMPBb4qaZhVAuP1PuhJa7if9XVlM_OyoZjVgUs1FXODFwPLAK8t2Qwm2l3As_zfAPlRZFnnN5QCI8YLuAJwVzB8zOI55tcWlDTbYAG2S-DiA3W0ea0kUbDOJjMGoIeSIcDQagB8MwlKfOfpRMCAZ-VNe8ajrayn2NplmSZFzhZFDuaY6NafXAw9yu-tZdnUcyzOI2isNeFUT2uVn1sgS2cuRSFUNi-0hQJS6Pv1h_PxTbo9WnRIVf7OzQ7IfGFPErkGY31mXX6lRD6eg2bSa5-ptyUFKl-_BLDTsmH1E0HlkyEggz0d7Xl385KOPyOalfxL6AepBUcNZf0bn_oGYz0-MFNgPp4WohfvPu3xeL4kx_79wO6RQhxEheOkqSst8ahwTBowSM6BnW1qUDH53NhS2vk_plgzEgWStxnR9bZGcpsPu93ePn9qxcvv37-8vzVC1xDVP24HfyillYCW9ZdCYF8i05SdBjSnr_--vnpd9--ev01rDO5Rdn-5AZYWzQd4F95WUe_pf51soRWpi3yRF9C0dZ0FGJMU00f7PLJM3eoHOS0FOSUkixKemENPRctrEc0UeYQbC6x-B5SgMVZ-Yb_KDzoDLwukF0V7_Fn4QbxB3xaeULGJ8arOg-YF4ocb-wUSMeAv_2UqWtF-c8_wLO4CoQ5xjPSFZBFXHQ5Hgb8T63FNUPPqZy1Ou9clV0qTVRlDX7SYE64llGBQEX9BWws_I-lplZA6wEb4Z6fQMDMUtfps45RS2nwvw9uCGmXTOIIB322F4Z95jf0iNRGj-nwWClUqqLu7Gq8B0SiVwN6t2d_s1HIlEMuyVsIn-K-BlP6kaqclSpkq4Q6_1nnQmStyRmiJKF1BSagA4sOWrhT_h5TwgbsQeWf0j8PaSd4EnA6QqqDZx_rHRERF56GQECutYocELLt-9yGshHSyV7Io6bXyJ0_tGVFIOBDDMsFX5gloxNWH_oAPR8_R0n1aU_J4ZpIz2swFGSn6B0N0feyJpvVgaNlKRRzPvODjPRuY9QkG_T3juaX1lKb0cDlLLJ5ppcb9cPUco_pc4Glg9fRKwhlgpj_5uSLmeR1Cf6iBn2fyQU2BTy4lv2YWhURo-e1xqECtit4hGBeJ8L-ZQesAs1QdQ7HWTkm3BA1Su0ironIQSjZiHR9tDDSUkBaYr3568lz4YZKeSyoOa54K8gSJK6qBvNPKWhhr1j55JT3i_XBblSNam3f6BIJQi1aPJ50saMVqKXNSUTTMLTDoM9LRt3BQdoP7u2pjcLUt0MCFYVH3X6jod2nNnpMs05-LjJkhiaP_grdBMYTxz12XBApmFMjCB_qkDmBhFxwXC8BZS14E3zMhqc-hxO3kM4AJRCChL9AovKyg0e6UvYMpEOCC8AO2kK82tpTdTMg7qHBAwlnpeoGzUVyCswCVcS18mYNEVhqWEuaq5mwatLLGYTKoJia61aDLHBANb4VesmtHyBEl5I9lkJfiEQQP8khD5ywca7dznwID8dvXp68-OrlYs0OpYKR79o89vzA8-2-IBh6oiMP-NCOJlq9cJ_gzTKISEIEvc8W3pwIhzDtxKBFQR6Qz6VFQJY3E3EMmbPGtfooJTKMQjpJldaBZ17NVHeBNJh863JsHDhE9qaADuLpUhQ9OtAtrO9APwq8AntnuTRikTUhSTmdixIEixzRdhpiQ17A8cCzteK4StS6DmikKoChtRU8bUGumssq5paY3v2KktoBOeGgwj3gBBPGD0fvBHwFNrr9-RZAZchE57TI5Q2iV9LfoZLeHHhTs98DyMLL93ldlej0zuG6oG0XnkUIYoCzyBPfD8wSuRHzQmeKJHkuugy1zuiEsIFdWQ6V110z8MOPHpiWxCnwImHRk1CCltp3NmVeRkVdjCpgIRVsWBUyVkjFeHvNwdXw9wfGJBmjrh155ElovF1Y6jX6svH56cmrr85PoE4CS5e__BV_uTk0iQa_xe3YfhqRPsfOpnDKfUHDKvxnXvIObBt7YxtcUjpzsR6UWwwD644hjlxpnwZuUaGmNS8gGosMB33TdHPVD-v51reuFvtU6x5bbEth1hfSM-vHDnRJt8ykaxUZKAjnlYWufrFPX-6xcaUZecovB3b2Kcpin5R3L_0l5xvr5JuXfxeBF6LKJUSsqmsbiBfjxiVYBLLr3UhbPh5dr262qdPmtMVyfHw25JlYacuWoCZbcmn32fBI9x_sRRSKxCQInSTNWOJREhPuhn7Un3k8sRtPq8ZTvI_GDRo3-Hu7wftPrLcntv6vu-exdw2nn2QCHSVe5ruRE7gu2J9LIFv2GAdqE6h_MxIltpNFLizsBX7spYGLi4dQkYHhhjG195xn9wDajXYMoP3Ei3hix2YAbQbQZgBtBtBmAG0G0GYAbQbQZgBtBtBmAP3_cQAdMe5GIaV-kPRz4VG1PvK_n1xy6xF37HiBnaWBzXsPP6rCR77koaX02L2elbKMXFoXen5yMbMufupIgf5E_CLGREAnldd68YrfGEcxNufgkVRIvEC-npMGkvzJFL7PEzA3EE6bs6krFwEcnbDovkNwLZmYZkAW1qxEjFahl3WbAtN3rqfgeS3DuojTYiCEXkZFBlZhygDLNZgE5eDc-_6QminBJXjoBJjzocW5YCE7ayLt6kPKTCpmiRmyPDVqjYwTa0xopZcgE77rZBgvgMITUFowAB2BxNTljmm4D-WdF_t-yGmvcaOOx16v_AltC2718u5d7rY7laZewxUgOVPu2F7E7u5Ne1_75uXpydudnlbdKTl9523KM4_u-0S_LBuj2sOucYBRzx3Xu8PP-pmL_z8zTWwSj0ZxupejGzmPaMiIVGqYN52VmMhXnchxcXQpF4J8gReQzva5rgR8ZHktgCWyN4u5xKjoPlafHxfY5Tx-71wIOIP-P7yB9XXeoF3nWFHIOQ7UX9KmCChn3qpGNtTZ4JrlhQ0aLJRDUA6ju4TqjUlLZH1_9majC3TRXm1EcwCCB_Z_57r6tuourQX6BOeHQ1NY8W9vb9iAgww4yICDDDjIgIMMOMiAgww46J8QHCRz6n0Qoa2rW0ChW1enKCF8a48GCc3xBT9_ZKSQSNcf-uKbT3zFwbpiokN2YJD8iGH3PVZ_xJj69uqyTNkNYRkx5vbzGukh-ym9TQHfdb-lGXV2rKH2r0RG0LuBuyAtO7ZU5UEzWhST2J9kcM9LLvpI4KxEjQIEdKowwZ4SL7K5fomS1dd76E9aiLl34VxuU3PC1Gyg31JW8hPa5gMZYiAElNyFTdl3Ntnxnu41Wh0zom1H92lwFAgHWeZ6hEZQnEQkYzb3wFLdfXCUfnZ9NxzFWNoOlMQB-E-PKuhXW3q_7sYN_EOAEomdZr7tZinLsjiz_ZgFPPOSJPNjP8z8hLskihMahcyPPVAjahPOYu54ts14IrLGPUeaYiWit7a7dMKl7-zASpCAUMJYarASBithsBIGK2GwEgYrYbASBithsBIGK_EbYyU49wIS0ZDbcfwHwkoMOAkZlPaV3dP22wRGYT0MRQH82gGjsB6Mojgr_3AwChvB4ZTGxI64gVH8q8AocHNtsFOOT5cb-jKNGDJYFWYa13kDqtybsprnC01nW_2yTvSZSXmgpcNzXBPyqF7Q4FC4rp7qUdIFWY8gQhxf2TdmqCteMDm67UvFPzeY-mx1v1ATLiavGb_4HBgokzQL1AFcEmiGUm1QoJy2snjsEzqN75DSUXUh9mtF25zcYc409pPUz-LYyYjBqDwcozJaSRxlaymWN3BeMQobgkfPjesco_iIhbd2lOwxqBiDijGoGIOKMagYg4oxqBiDijGoGIOK-ad8Zc5eDIyCv_xe6BfYGyvh3-odOTaNQbG3vkLjxVRvUY6XtaqtQIfueD_E3U8fekVE4mc2p_yp6EEbtReBJeafaJXPT1_NRUa_FMota-HbQ0_U6AOgAMJcEN7Wl_w8gsyT0vr2xZd6TJd1oiUjWiMQNmXnaLyc7EWA9YABl4e--Sfz0tAh3pORiS4Lqul5VnX1_Jrzq20ft8kLMOMGiquCqSL7RnYq7vfGnJE-7n71i4Da3HKt40M0umG4R6_2vK2GZ6KB0-uHUg3h1OfwB-t76ejALxGdKUDQWezTjD0bYVutvOwwBWgsyIxKdLwg_Zn11fNvVP1XdJcQZCE34KPmqM5HgMTFPjEfPpwuMKSUVBRo1FQUvcscE1KSVlrPoFbFNH0PTul5AQzIZIzZ1gPQJNUG7I-LWVshcjYgQbxUCE-m-i5jFsjjz0Z0WVO6dM3xaaAmGkVRmJIgiMM49gLXc7mTxizbB2rqQSZ3g5qMGzVu9Hdzo_fH7h1-484AqvrHvHGHBL4NiZkd2xENEy90vcj2oBSPfRYFCbEDxonPYifFAt1jWeQSEkZZYvuhF5DwXm_cid7a8dJ3l96ur3xxqZf6XswNisygyAyKzKDIDIrMoMgMisygyAyKzKDIDIrMoMgMisygyAyKzKDIDIrMoMgMisygyAyKzKDIDIrsXw1Fxhya-ikJwnDorozmfYO0HzSx6xFk1I4yHkbR0CkeDfFG1vLQMdxtO2rQWUlcFVhUVWKarpyKcOBoe-osahIlvQSGPVSDNaRxuraai60hJNa4ey3Fn5fvqyvlsXDeS2rREsKUUzspDUvTzupz6XHltmflFeebRjic3jpnuOV6g6UDPtRsUMlVa0-g9kCnMEMEq8M2a44-edzYXEuQmuCOcKXbPUWxSh96p8k0cGz4EhjdJ--ag8GOQdbJie0EDu0btcPcU8egR0wu0WLFyHvgm2Znow8yRA1IqupR5Tpqj-pAssApvECwnZVoaXNQFsxv2qoqMOGjlTBrwsCCMT2H84NTkhwV9BA9csGnhbsFVRva5GIhC2vCRuiYBDtgD_YqB42CjcWuffoBcbiFm-XJkebv_g4Jo0D_AVkSODZq01eZqmNkMEW2CVVDtFetOFwL2S2tZ89AL7FWwy_6QQFoxgokwnBEcRBJ6OLZM_TrwrPgrhq2IFwQ3ot9IeWglPUJMCDmMCjGASwo8G8q8AFPGDk0mko8kjAeO3Hm9JDE0Vxaq9EjJssQ7Wt0vgoACg7yrMxIXnTIG-lqx4jFcXqgwohSsx62Kr5Cqi-IlanvRiBqoKFMizCIUUTICvRifrlqt5u9YIg4M1FPqypHw1UVcnKALL4WvagMB19yVAU3ZbV6rY7kBdgMthUqLPmI8FbKlc0GCffqoEKQ1ghQYi1wMa2SpiMHbVPgSgZ2isfGuCqytfkaDoqTBd3WGo8V5iJ2A2m6qp71Uw7RANEtFMGwFm-pSpHqiKq9n7PIqCDalToEyH6zmqDKlocE5vaRFNwb2jx5DxqAjxxKhwzM2sCsDczavHzwaV8-OPmK0t_t7YOTHuaTv3ZwVOYNyLJx1bj3TWJ9lfI0WLp7vAjtcSi4fRvshgGP-LL_FYATIK38kklMbat6DgY7HtVKM--ry_3V4x1I3ts0fLcRLbU-ucMUsn_DIO6DTlmneAXIv8Nxle4bioMLt01KggHgeVF17C5s720qTnPR59OBdLI5OCtda-H_QCBiOhAoC6sJhkHlJo1OBOoKah2y2YP9PSlA7rLo1NgO2VSUi4kaUaQTijNQR0HOIW4ophQOgtJ8QZzwjaC058yoghsJ6_7Y3wR7w65H3DANExIh9AgS6pjsw_720MC7sb_Ght99CtT6zvcZDqjMfwgM1fFchxIWJDTmDo-8gBKPZnHGucOiMAhp6Hjci6mfZYwmcUBCsOXA8Xnshiwg5F7vM0zmtvPWDpdOsPS8HUhULwvijNjUIFENEtUgUQ0S1SBRDRLVIFENEtUgUQ0S1SBRDRLVIFENEtUgUQ0S1SBRDRLVIFENEtUgUQ0S9TdAooZ-GtpJSB0nYgaJeh8k6ggDIqePXL-yBlfeMWK0ZPEuQhUc5s-N1YAQCj6vrgXQcvdkLBeETuab6ivA-qGagb4a6OsfDPoKt0UscdOUE38_9BUl-80NJBITCOwBzCu6gtH7sLAXKMtKNDoDb308vPWths_RkaeCneQ3OiL0cmucf7cHm8Y9tRRKYJcDpQiD0B4TMhUcukGu02B3GL2pwOyhGL49PTmgfp5NEkZtnkZ2YiCzfzDI7Fvpf3pVwcpdRzuRBkqT7r3lFC2roSwSNW29PgyabTlZT4G4s77-Z7IxpD-e4GoF1yUABclTCFtdbcjx5RaOu_lcR6Jx2JnAbbGRcQb5BBbjA_SWaFiSwd8a_K3B3xr87btf4c__ASavrv0)

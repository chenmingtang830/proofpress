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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzQ0NTQ2YTFiZjE4NzUyZGIzNGJjMWViNyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImE1YWNhZGRiIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV81MzRmZjIzYWM3ODc4N2FmZDBlMzJkYjIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2YxMTNkN2FlYmE0MjJlM2U0NzQ1NTFjZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXOty20aWfpUuzo_ddUgKVwJQqmZXY2tSrjhxynEyWxW6qEZ3Q0QMAgwulhXHf_cB5hHnSfY73QAIyhRlS85OdheVRBcCffr0uXzn0id6N-FlnSZc1KtUTk4n2-3K83xvwe04scPAd2TserGwVRxMppO4kNcrmV6qqsa71Zo7_uI0dpyF8u0I7yUisjxl-4vEWkTKC13HDm2eRL503AV3VRhYdhxFInYXYeh60rWiRQS6Mq1E8UaV15PTd_RLvar5JXbIeE1bTfFDrDJ88KMq0yTlcaZYqd6kVVrkbI33i_Kaxdfsu7Iokm2pqgprtly85peKDrX3cVn8rHDcpiSC67reVqcnJ5dpvW7iuSg2J2Kt8k2aX9Y8vwxd62Rvdal-aVL8vGoqVa5EkVcqhyzqslHvp5O14iRE7nPBpYwn5pOVeqNfgnDVyne9JHFcLoIQ__BEWsqFkB3irChrOtoqS3MFzjuNZKvEtl0ZcBVzz3GUq7zA831bKHOclruV4NuqyXBgh_gURSmryelP7ybt9u8m0HJRVvSTeazkKobIf5o0-eu8uMonr3CGzh6wtSxEdfLj-Yunf316_mT19bfP__bs_MlX5yv99cV8IyfTTzIfXtdlGjc1tLaKeZVWZEQqS1a8gjRrpek19booicfXaU4kq-uqVhs8yfmGlNnxOsXSigxgcpo3WQbOxRoaU-bMcVaI13g7DKSM3ETgdSirVm_r3oqUZF-DUqbkpWLP6GuJt9pdoT7NzpbMTF3hkz-xY8vq6y0xR-qG6UzeT3csxIGtfKkWD2fhz-z7mtdNdcpAmmfsmx-_Y2nOLnY28B_W3J9bM55t13xuX8zZS3gHI9fa8bjlJd9j0PF8y7ctd4_Bv615zVL8Wx0Vyp_Y3otHxGAr25E8iu6xy8u1Ym86gb3uBaa_lqxuyrxijx7FRZNj5aNHDL6T16xWmdqoI-dWjm8FThDeg6Pf2DN-jb1_A-SkGw70-aUBUhEc_bbMf5vNZvo__MieFZfVlNUlFwrfATCbdMeT9vc9prgllBv5_j2YevToG7UhJITKSwVXU294NmfP87rIikv9cQWgEhCYmg-wkh4cEZOvfCVDO7yn4lotyUJVLC9qtuGvFeNMZDzdsCZPodiKZ9k1Iwyds6c1M-B0hKOA24KLaN-pHzdlSWq_KsrXSVZc3WG2B14_YrzClQ53QnnvHS8uLmjVMm-tlD1_-ey7WVVfI5IZQ62huKJkHZ4uc8b-8V9_ZxxBI5ezHXuikPsW46jEX9jy_tIgLZUqUVggFEvSt2Qg0Owy_-lCveWbbaaqk87_Zr3_zfTXY4YjQmG7i_ghQqvWy3wHbwxPpOYy3VC0ZBIGPy_qbDv_uSryvVe3R0Tmh3GSiMC7P2ftsgtyNI0_RQ4T5nKT1ohj8HNDbAp8niG32cLkc8l0AD4mMeksIt_b5-uFQhoEZKnW6ZbVRW8hDIdFZOe5zgOO2frHUTiG3VyIMFTqc_J19uHrEOaGpxBmDYvssiHChYreSiFboMUpYOeICK1FwKOAW5-TVXKQ-qpgVVMmBONYrwjJtyAKDufsbMdtT1rwnMXqGLBKxwkd_waMfVvks8uCZ3eF3eF7RzQX8ciKEtf69D1m2KIGUCdIrthzgNDLHqZEkWWKTJkAq1Q8m9XpRpkYx2Kk3TueMiTn-9mQF7huyPdB4bxza42OFE7JW1ofYkkhmrvE8XEUjmVpruNZlqM-J19Pc2PJTQwxrAH6RLkk4UmTo8yQscoiSRCXG3k9hTjBF22z5kfsRoSO6_uB-zlZJRPPQckwK5gGUlh1mlOMhxlIVaWX-QzM1DnCeQeSp6z6IAS8mnYlx4SCO2X7AlZi8nv9pCsW1Mq1LUsF4EdYStgSdaGTIE-kZBnJgqbZeVZbFTHUZ-K15kwXeaXeiUqA7jeqAF5ROYWDXA8oDEusARFdvN2z-qqKpF4lsCVVAqDaIq-K7dNIJKEfilgpf-E6C8dCues5wg5UEnheCAJRbC8i4QT2wuPSj1zLEovYX0g7tj2Pzl8h19fFmtHWqWOhxqFPJo7lLGZWOHP8l45zin-t6AvLOrXIy1uJU3rrq8CKRATb2X367ves77SBmvprzas13nfdKPCtMFCBQxmtpjEoyVrb_eTSqqUubZGIyHF8maiO-qDaaqk_pGoi7yDTF6hblY5Ly_zPXU6mQ75Jb6es9UR2CTufat8zuxkPYz881altanLga6WRtSx-VTl4qVVpalciXm2VgCyEDlg6I2xzZfgjMEOVIJoV-eUMZXL6K14x1Y5KaI24nh8AjlZcDvdsy_dDK3K9TlyD2q9Txt0lXUvPchIpYhnAYsOO3qDKa-k9pHi7kRMjI4WwCgqtMpUQ9IBeTTxzRh2jkq2bDTey08QoFCOtgGBrhOSkKCnTyK5xnGUOAaZ1pxtCa5NuZLq84zGMgBVxBUvgcZqltYHVja6zTm8XtbAXiRMkiaf8oBPNoNxsRfOwKrLGD71kQENrba1tU8l_1xRYWxASz0VXBrZv6oKMDmwaLJR7qU1Mh8bL6-KK5AEb6CvGjuSgbmwpbfg1ZToQKam4yKfsao1gFl_je7ExznCV1ms43RW9r_NhUDtUBrfyQ8YS8oUboBjucWNQGbfye0jBq9U8f_Todh1ywIta-K70vbjjYVALD8z7viVuK_-iKYWaLvNKUVYFEXZVzhTQAyKQPTPBbNrBCdardIvyIksTJa4FwiOFC6zQwtUyXyKeb1PjQVWzBQ-mX4aIDe-oU1EZp5EKLrNB0IN2FBgiC8CaS56nvxoQgoKXeamaSpGv3C6xOImSxPXtJAjtTmKDWn0HMB9XfHcoL4NQJWEcBIveFgb1eEv1oQW2BnOjCm2wfaWpE5aqe7v7eKa3IdQXWUNS7d_oxInEF3mUzjMq9gV79o1W-maDzYxUv2hhyqi0W35JYSdXu9StCyyJDgUJ7Hd9A9-WOQ5_oNpt5ecLF2mFIsvlPezvegYDO753E6A82S_EL17963x-8snL_u2IbXHO7cjBUaJY9t64azDsrOABHYOy2Baw8dlM-9KGpL_UghnoolX3csKWS9LZbNbvcP7j0yfn3z4-Xz19QjR01U_b4ZeWdKuw07LJEchv8MmzhkLa4-ffPn72w_dPn38LOnuvtL6_9wJo66YDvpvHXfQ77X7dI9EZ0w32dF-i5a1qBGJMVewvbNK9NXeYHHJaAT3FPAmiXlm7nkunrAc0UWYINpdUfO9SgPkyf6F-1gg6BeqC7SJ7Qz9rGKQfaHWLhFLtOW_beaC8UOd4Q1DgjYR8-1umptblv3qLtUQFYU6qhDcZsoiLJqXDAH_KTl1TQs4WrNvzztqyq00T27KGPqkoJ9yYqMBRUX-FjTX-sPbWCrwe8RHlehECZhI7dp91DFpKO_y9d0Oog2QeApOlstzFos_8dj2idqOHdHhYjEpV151NSe9AJR018Hvz7m86CJnmksvIFuFTv1dRSj8wlWXehuw2oU5_7XIhvunY2UVJLsoCLtAFli5o0U7pG0oJK_hDm38afN6lnUASgI7W6g7Zh3bHdcTFagQCftWZyBElW56nLJSNSCd7JQ-aXgM4v2_LiiPgI4alWi6SmehE1Ud3gF6OX5Km-rQnV3im0_MSjkLi1L2jXfS9LPl2feRoSYxizpOen_AeNgZNsp393tH86qzUksJ3lAwslXTkBv2wltxD-lzwdKBOR0EbE2L-i7OvpkbWOfCihL1PDYFthoUb048p2yJisL6zODLAeo0lnPI6HfYvG4gKltHWOYruyinhRtTIO4i44joHEXyr0_UBYeIlQ1rCXvzl7LGGodwcCzXHa1VrtjSL66Ki_NMoWvsrVT6pUD2xPtgNqtHO2rddiYRQSx5PJ50faAV22lY8EPFiYS38Pi8ZdAd32r53b6_daBF71oKjonCF02-0a_e1Gz2kWWc-1xmyJJcnvCKYoHhiOye2A5XCnSrN-K4OmXEk5FriHQmUtUATWmZh1Zc4cY10BpwgBGm8IKbSvMGSJjc9AwNIeABxiBrx6saebTcDcY8cHiws87YbNNPJKYQFUyRaabVBBDYWVvPq9VR7Ne_1DKVKFFOzrtVgChyYxvfaLhX7CSE6N-Jh7fSFTgTpkxR54J4YZx3szHbh4eTF-dmTb87nG3ksFQw8x1Kh6_muZ_UFwa4nOkDA-3Y0yes1fALNEkQkrYIeszWacw0I-50Y8ijkAenMeASyvKmOYyScDdHqo5TOMDIDkm1aB2ReT9vuAq8o-e7KsWHg0NlbO-igV-e66OkC3Zz9APvI6An2TlLjxDprIpZSMdMlCBU5uu20iw1phuMB2Wp93FbVXR1QGVOAo9UFVjPkqqmpYj5Q06v3pKkDIycKJtwPnFDC-HbySo-vYKMPP78xoLLLRGciS80LulfSv9EmvSlkU8p_xiCLyt-kZZET6K3wXPN2aJ5FK2I3zmJO_HHDLIETSHdh70-SPNZdhrLL6LSyIa4kReV11x348aVHbkvCGLKIZPBZOCFP7TubJi8Tui4mE2DEhdxRRcaKVEzVVwpQo94cuSZJpHCswOWfhccPC8uORl82Pn529vSb1RnqJHi6-eUv9Mv1sZto4JayQuvzqPQxdTY1KPcFjSzo2yxXDXybemNbImnAXNNDuSUpsB64xDGUbrPAG1y0tzVPEI11hkPYtL952w_r5da3rua3mdZHbHFTC9O-kJ6ynxvYUtcyM9CqM1Ao5ykjqJ_fZi8fsXHRCfKZutyJs09R5rdp-TDpr5XasrPvzv9TB15ElUtErKKpK8SLYeMSHkHiejWwlneTq_X1Te46d7ohclo-3eWZVGmblmDHtpHS4bPRkT7-Yi8QKBIjf2FHcSIjV_CQK2fhBf2Zhzd2w9uq4S3euxEGRxj8Z8Pgx99Y37yx9d4fvo-963L6s9xAB5GbeE5g-44D_3M4smVXKnAbof5NeBBZdhI4IOz6XujGvkPEF6jI4LiLUFi3nOfwBbQTHLiA9iI3UJEVjhfQ4wX0eAE9XkCPF9DjBfR4AT1eQI8X0OMF9HgB_X_xAjqQygkWQnh-1N8LD6r1Af5-csndXXGHtutbSexbqkf4QRU-wJL7ltJDeF3mpow8ZRfd_cnFlF380vCM8ET_oq-JwKcwz3r16t-kIjVWKyBSGxIvSK4rXiHJ37uF7_MEyg00aCu5D-U6gBMI6-47gmsu9W0GsrBqrWN0G3pls80ofVfdLXhamrCu47S-ECKUaSODLChlALmKkqAU4N73h9o7JTzCojMI521N94KZ6azptKsPKVNjmDllyObUZDUmTmwooTUowffk3iXD9AAGz2G0cIAuAulblztuwz2Ud27oeQsleosbdDxuReVPaFso1uu7h9ybcGpcvcQTsJy0cGzNQ-fwpj3Wvjh_dvbyINK2bxpJ3_lai8yD9z4Rl01jtEPYDV1glDPbce_AWS9xnEghvbJ4OLiK63o5XSPnAQ0ZnUrt7puWOSXyRaNzXLq6NISQL6gM6Wyf65qBjyQt9WCJ6c1SLjEouk_az08y6nKevLEv9DhD9394Q_RlWpFfp1RRmHsc1F_GpziMM63bRjbqbECzebAlh0U5hHKY4BLVmzSeKPv-7PW2K9B1e7XSzQEED-r_zrrqm5VNXOrpE7o_3DWFW_nd2hseh4PG4aBxOGgcDhqHg8bhoHE4aBwO-l84HGRy6ttGhG48vTEo9MHT_Skh-qs93ZDQjP7Azx95Ukin6_f9wzef-CcONoXUHbIjF8kPuOz-COoPuKb-kLopUw6PsAwE8-H6btLD9FN6n4Lcu35LNejssF3tX-iMoIeBu0ZaDmzZlgfVgCglsb-Y4J7mSveRAFa6RgEDTVuYUE9JZcms-yNKrK_3CE9qxNy75lw-5OZMtncD_Zamkt_jbbZjQ18IgZO7ZlNuO5vpeO_vNaBOGdFNoPu0cZQjf3br4DhKf3d99zjK6GkHpiSOjP_0UwU9tVP3_eG5gf-RQYnIihPPcpJYJkmYWF4ofZW4UZR4obdIvEg5PAgjESykF7owI2FxJUNlu5YlVaSzxluOtD8rEby0nFN7cerZB2Yl-j8ZN85KjLMS46zEOCsxzkqMsxLjrMQ4KzHOSoyzEr_vrIRSrs8DsVBWGP6BZiV2cxImKN1Wdu-33_bGKNj9piggrwNjFOzeUxTL_A83RmHRcLgQIbcCNY5R_H8Zo6DNO4fdl_g-uV1fptKXDKygTOMqrWDKvSu39_na0uWNflmj-8w8P9LSUSnRRB7VKxqAorrqqRwkXch6NBP6-K1_U4a6Vpk0V7d9qfgvFaU-N7pfZAkXe39m_OJLCNAkaQzmAEiCZbSmDQNKRW2Kxz6h6-Y7jHbaupD6tbptzu9wZxF6UewlYWgnfJxRuf-MyoCSPsoNUjKtcF59FbYLHr00rlKK4gMRfrCjEc84FTNOxYxTMeNUzDgVM07FjFMx41TMOBUzTsX8_lMxr97_N8nE1Lo)

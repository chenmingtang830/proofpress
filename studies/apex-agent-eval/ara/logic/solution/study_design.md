[//]: # (ob:3490ad43)
# Study Design

[//]: # (ob:a1372441)
## Unit of comparison

[//]: # (ob:8f43e120)
The normal-condition unit is one generated legal artifact for one task, executor, and context condition. Three verifier calls are applied to that artifact. They are grader replicates, not independent executor samples.

[//]: # (ob:584edb1e)
## Paired conditions

[//]: # (ob:f4dd76c4)
- **Baseline**: executor may inspect the full real data room and task instructions.
- **Proofpress**: executor receives a bounded governed working set derived through task decomposition, corpus selection, evidence-bound candidate claims, policy recommendation, staging, and graph selection.

[//]: # (ob:b9e25916)
The treatment is intentionally systems-level. It does not isolate retrieval, claim proposal, verification, graph traversal, or prompt constraint.

[//]: # (ob:6a19e280)
## Quality summaries

[//]: # (ob:d082f983)
No preregistration established a primary quality statistic. The following are therefore **co-primary descriptive summaries**:

[//]: # (ob:b9262aeb)
- **Majority passed**: the modal number of passed rubric cells across verifier replicates.
- **Mean passed**: the arithmetic mean of passed rubric cells across verifier replicates, exposing grader disagreement and rubric-level instability.
- A blocked stress cell has no artifact and therefore no quality score.

[//]: # (ob:38a73d09)
## Efficiency summaries

[//]: # (ob:8c061bc8)
Reported per-cell tokens and latency cover executor generation only. Preparation cost is maintained separately. Cross-task totals are descriptive and must not be presented as an end-to-end cost estimate.

[//]: # (ob:8d5c4f78)
## Safety endpoint

[//]: # (ob:c8ce9f50)
The endpoint is behavioral: whether a material unresolved conflict causes a block before executor invocation and whether a client DOCX is produced. It does not score the correctness of a nonexistent artifact.

[//]: # (ob:5ea723bb)
## Comparison with PR35 RelayBench

[//]: # (ob:1bd9b00f)
PR35 held substantive handoff bytes constant and varied ledger metadata/verification. The APEX pilot changes the amount and structure of context by substituting a bounded working set for full-corpus access. Therefore PR35 is a causal-design contrast, not an exchangeable replication.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2Y1MmIzNDVlNzZiODU5ZTgxM2MwZGNlMyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjNlM2JjNjc0IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8yYzk3Yjg0NDBmMDY3MzVkMjQ5NGZkY2QiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzA4M2JhNGJhY2NjY2I1ZDc4ODhjMGViZCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWllz20YS_itTzJuXlHAffFOcPOQhG6_j3UpV4mLN0SAnAjEwDklclf77dg8AErQlSiRjV2pLLrtMAoOePr7u_qbB-wmvGp1x2Sy0mswnZbnIQk_4QQhxJJIwhcT1paMk-JPpRBi1WSi9hLrBtfWKe2E0T6SIPMeNstTLXF-kkedGwveSzA2kk4RJFkAS8jgAmXHfc1JPAfd8vAugIuEplKt0Lc0NVJvJ_J6-NIuGL3GHnDe01RQ_CMjxwn-g0pnmIgdWwY2utSnYCtebasPEhr2rjMnKCuoanym5vOZLIKP2LlfmT0Bz24oErpqmrOeXl0vdrFpxIc36Uq6gWOti2fBimfjO5d7TFXxqNX5etDVUC2mKGgr0RVO18DCdrICTE33whYziYNJdWcCNXYTOhYUn01gkQeBkThT7ofKCNMiUJC-UpmrItEWuC0DNh4jkCyfxBQ8El_hHhCpOkkQ6IFRnTq_dQvKybnM02CM9palUPZn_fj_pt7-fYJRNVdOn7jaohUCX_z5525vMPqDNk49oyYAKCnPTKg31JS_hboZqFc0Mbnh-ebHbeiZanatLXvHZLDdLLWez2uRtg-HBT_g8ogZqvSwu1qTzMZDjTVNpYUUtBK91TRpBni14jRFowMprm5WpyK5rXZDIelM3sMY7BV8TAPbtm6KAmqAzmRdtnqO1coXXgbz1cTq4a4J4pEULWQHv9rF3BqVhoYIkVI5yIt9JY5_7QRzGHngp7WsaC7w-oqyPKENsyevS6KKxAK3sTqTE8K3XoTS5lpuRhDE8RkIs8E5ETm2yZpGhV6AqK90DtBbuHNHryCDw0iSTrnSDlGciC2SSplEmUi_wYg6BC0EUpCL1A8mDNExTV8QJhjEJQ5LdcDLlHn1L_088x4tmTjLzog-uP_eCeRD9w3HmjoNrez_jqiBx_CRS2eRhdPX-74NFkRt5bSP08DB9NK9A6WabVb-UUFz9xN4aBXeTjzZVVSufvP1ZTn55-1OLxfD_Nmetlqek7H0XF6q7QepwFZAKWJkbuCNX_EqmsB-sKXhj2E0p6MonthG4xSvfsc9WNpuSFKEKjnpMKOLDRtz1Yy8I3L2N_l3ohpmMYQ_BXNa1Obzdd-zRBw7sip3UB9dzztj1wwpYYao1z2coAsFKDbQlEbpmpgCGQYCKyh3LYclzNoSdZWanHG7E9zQLkwCUcGFPs3ccG6Vi233qZ9zx2PoD3sgCpeJIBqfvOWNv3nzPEZhYNN-8mTO4A9liJrM13zBd1CXSBNagxzKEHPINdIfiDWeYQuudbjnSjz3FRApemLrR6YpRlBrqOmtMCYoMVmf8hI_xPN-wrrvVsxwLUH7BfmqYMlBjXGntgShF3EXVkn38_KvluW5QaLteI37guSg9tv5AlJSTeFma-Kfv-U_D8EsFS_QzIpMAi2UQu52uV-hRjnc1StmwT4NU7D24VssLdsAZ2Mgij4M4XTGCz8_8T1PREyWVNkUoIsCsjUKwFO1aQEXJ2d1lVSsqLZlEKvs0fPyEx75y0j3FfswyLTUU8uWBeuKRQ_VFOpErZHLWzu-ByAgaW0I1Q0tz1phrKGrGC6wpWFlIkiX7u3zri44-EK5EhTLI4n3dfuUZoO-hUAOlOuSQL1cf8IVMJKRZ6Jy6H6XwsI4yWMCK32hT8XzObleAIKkQumv0R6URKm2BLdnkN7ZEHCq0wGPPF_uofbst_ewWjzHs3Xs_ZO8h55vv0durZ9zy_NMH3OQKlQrHyf4qfezSFeQKwSYwkbHo3QDDVq9MluEJD4-DVEPtHYuoGwIkNSu1_NxtyJlkzvX6SY7wmRY9Z7-irzaL7SMYuaUuCmIif-xxiT8miGy7rubYQPV_8amrdz_-xiyRYUS32q5cXb2_uniKPhyvw5cN_wxNRpTieE3OIROVXdDw-nq6rQNTG9EeR32rPMO2ESk53rYv-vUZioyYyvGKnEpQrC_Jv7QQT4nSWnFxhhkjXnMaVk6lNIbaBpqHhwrSb8psWmPfN6Wp6fuNnQrJM2wbUaPjbfuCNZyhyIgvHa_IOVSJApSZPDe3JItXQHtUgJkKyHOkmfXPngWgLeU63rZTmVaOzENWpq57lOCyCspcSxotnpMOI552vDWPsapzyviOuR2vyzmMDZUxRb65YO_Qqby_Ik1tU3zNMcnxH4o-x7Yd8zuhYe8ztjPUGBHC06rfqWywyBCs2A55W2NF5FvpNjO3AdHnsIARqzzetmfY3hlqjcjlCQ38DCaJ0VhDw6mXXva9xarYVUmrfalzczScPo5Y8v3kdrXZs2ErAxnRjVboPJgJ0xbqkNRBATQ3YnZqR20WyJEvH2QfeCfReXo8oR7PacdT6_vXkdzrSO51JPc6knsdyb2O5F5Hcq8jucdHci9_hz68Q-51mrvhw-Mvi597X_6XvBRPZZZm3PO4BHBE5PNEugHmZuCEAoLQhxAvuEkqHSdMHOW7CShkBl4KbuA4jv-UQY-8HveduZs88np8-7OSv_vr8fvJitcrKhFO6EiIQaqYTLEyRoywB-dLaF4vMKbfHARRFjsxDAJHzG8Q-HIi18uVUZJEKXAvVu4gd8TternfYuDZHzOQw-8GFpLbMQae9zjCl5LLsn7ebDewJ5ONXbKsuNobckw7GoLniBLLnz1CDFW-5usyh_rikfLWOyaMvFBhVw78LBocM6KWO4e_kCr2YpXw00CFKTJGbxA7Yo-92HPY4FPzz4KE7n4ntie2AglY3Owpuz94Lakt0gTj1lTXdLKsAbkdBubGntoq0y5X3TYKCGumttZP0RFV2da4PAfZXdk_1GFQ0VOKJpvdW4op64oYaWHWSDMV757DsoHH2mUHFoxuudpJvXiEtfQuhjRwA5nwNA6zwcUjHjyC9Neey_Z2dKojYaTaRbfR47h2XTZd_6hoXHQAikEWJUJgsxAyHgwa8ecdFF_Ih4eSkiU8k9hLYp4OYkcUuRf7LUarCKFaVrq0DXarPCL0aZ844GDjcbjr-uEuyFsaPcqjrzQ_ten0M_DiM7moerNaA9rP1nT3aNFUJSmb0GN9RVO65kusixaplAudpA6bNsu50OR7q9VVNxPCDTFgmOh2Q6QtBN5dXbZFYhsMvLMNH-YvHMiuBEGnhHITL9qiZnRM2IHx5Zx_qLge9kvkGo4fqW0r2h0DesnfYmhbd3eBlr6lOM1soWtMw_t2NAYsbbxuUQgVBwGULvTbWEoO0oqo96wxM7AdD5dh-mgi2wcyXoW-G4k0SbD7bF2xO3XsnPyic8SWQjgCKQjEcbz17-hoMaqLX3tie2O60mhdtxMqscPjpj_88vY32nn41eB-9bX4tJmGH7BjNAVhHLOM4-0C7hCuNk0GfvC0k3nkI4kDL_PV1h-jM83OySedSoba7WTIrNLMD-U2XUYHlWEi8w1mtqyfUnZVao2tuBPVcYQWnWpZY0fJxKbTRDdIkKl2b3nBmA4QuSMGMut7Pp4rMBh2476wWMM0YYFAgfSxo9h2n4rXTUfRKEnuOvX6X7h3xXC_z_cnqQf8-z_8Jv_B)

[//]: # (ob:a1c6f757)
# Related Work and Source Dependencies

[//]: # (ob:58b703ff)
## RW01: Mercor APEX Agents benchmark

[//]: # (ob:137f0b3b)
- **DOI**: not assigned
- **Type**: imports
- **Delta**:
  - What changed: The pilot selects two legal tasks from one public APEX world and adds a Proofpress context treatment.
  - Why: APEX supplies realistic data-room tasks and task-specific output rubrics.
- **Claims affected**: C01, C02, C03
- **Adopted elements**: task corpus, task instructions, rubric metadata, Archipelago output-verifier configuration.

[//]: # (ob:3cf6ca64)
## RW02: Archipelago native task harness

[//]: # (ob:6824d26d)
- **DOI**: not assigned
- **Type**: bounds
- **Delta**:
  - What changed: Artifacts are generated locally but scored with the native Output LLM verifier configuration.
  - Why: This enabled iterative evaluation while preserving the task verifier, but it creates a hybrid rather than official Pass@1 result.
- **Claims affected**: C01, C02
- **Adopted elements**: output-verifier source, Gemini 3.1 Pro Preview configuration, task rubric cells.

[//]: # (ob:00bda579)
## RW03: PR35 RelayBench long-horizon handoff study

[//]: # (ob:fb6980b0)
- **DOI**: not assigned
- **Type**: baseline
- **Delta**:
  - What changed: RelayBench holds substantive handoff content byte-identical and adds Proofpress representation and verification, whereas this APEX pilot substitutes a bounded governed working set for full-corpus access.
  - Why: The contrast motivates an information-parity versus information-starvation hypothesis.
- **Claims affected**: C03, C06
- **Adopted elements**: separation of clean quality and controlled trust stress, explicit claim boundaries, retention of invalid attempts.

[//]: # (ob:2db7e99a)
## RW04: Proofpress claim-centric ledger architecture

[//]: # (ob:1cdb24e8)
- **DOI**: not assigned
- **Type**: extends
- **Delta**:
  - What changed: The pilot applies source/evidence/claim/relation/recommendation/staging semantics to a real legal data room and task executor.
  - Why: The product mechanism is tested in a task-completion workflow rather than only as portable handoff state.
- **Claims affected**: C01, C03, C04, C05
- **Adopted elements**: deterministic bindings, append-only event projection, typed relations, non-authoritative recommendation, authorized admission boundary.

[//]: # (ob:2fc9a31c)
## RW05: Agent-Native Research Artifact methodology

[//]: # (ob:c83df30a)
- **DOI**: not assigned
- **Type**: imports
- **Delta**:
  - What changed: This study is compiled into a layered artifact with mechanism claims, source-bounded exploration history, evidence receipts, and falsification criteria.
  - Why: The pilot contains mixed and negative findings that should remain auditable rather than collapse into a launch headline.
- **Claims affected**: all
- **Adopted elements**: cognitive/artifact/evidence/trace layers and Seal Level 1/Level 2 review discipline.

[//]: # (ob:dbec14e1)
## Citation footprint

[//]: # (ob:3e3c466d)
- Mercor APEX Agents public dataset and task metadata.
- Mercor Intelligence Archipelago task harness.
- Proofpress PR35 RelayBench `PUBLIC_RESULTS.md`, `CLAIM_BOUNDARIES.md`, and public results visual.
- Proofpress repository claim-centric CLI and ledger semantics.
- ARA Compiler, Research Visualizer, and Rigor Reviewer local skill specifications.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzNlMWJlNDQ1YjQ2NGQxOWFlYmQ5YzBjNyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjZiMDc5MjgwIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9iYTViYjM1YWQxNDgxOTI4ZjQzMTUxNmYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzQyNmUwMDUyNWM3OWJkYzYyNjc0OTVlMCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWmlv20gS_SsN7besZPE-9Gk9zmBhwLMJnMzMApNA00dR6jVFcthNOxoj_32rm6REKZZ8DrJYGEhkiUf161evjm7ydkRrLTPK9VyK0WxUVXMfXAZBELIgCoSbUmAi5Q6PR-MRK8V6LuQClMZr1ZJ6YTQTQQA0oWkiPMFdx_d8xw1EksaecLKAU9_Do5yzOBCxDyn4kXASP0gyjyZR7KRoV0jFy2uo16PZrfmh55oucIScajPUGL8wyPHAL1DLTFKWA6nhWipZFmSJ15f1mrA1eV-XZVbVoBTeU1F-RRdgJrVzuC7_AzjdpjYGl1pXajadLqReNuyEl6spX0KxksVC02KR-M505-4a_mgkfp83Cuo5LwsFBXKh6wa-jkdLoIbEiDlx6iXOqD0yh2t7EZILc0ZDxvyQCjdIXLwoC3w3dKPMICtrbaY2z2UBiLz3SD4PvAgcJ_RCHqdM8MiL4iANwWmn06Gbc1qpJscJewYnL2uhRrPfbkfd8Lcj9HJZK_OtPQ1izpDy30Zn3ZTJR5zz6DPOpFeFcbNuhAQ1pRV8mSCsQk_gmubTk-3QE9bIXExpTSeTvFxIPpnUYJwn5jdlfXWyEqPxo4RGta4lazT6FxlTUhkckGdzqpB3tGuuafSyrM1srmRhTKq10rDCMwVdGbfvzmqMBpQRzGhWNHmOc-RLPA6Go8_jnqQRqtBcNOc10HYce6YHDfMQwjBOE9_3kthxeRZBxqPQXlmU2sqt8yPp_EhQUfyqKmWhrSxrO5IB0f_qMFRlLvl6YGEoioERK7cn6kWVmZ5nyArUVS07WSrmzsBnDg8CL00y7nI3SGnGMHyTNI0ylnqBF1MIXEBfpSz1Ma7RYpq6LE5CjyVhaGxraqZyi9yavyPP8aKJk0y86KPrz7xg5kd_d5yZY3B0PONVmRtHQCEZfR0cvf3eCmR5ya-sX75-Hd8ZQyCk3kTQuwqK03NyVgr4Mvpsw1I0_ODpvfj79vQfDSa-_7P4tNieEp63rTeMCZdHWRwaCJh7NXwxBFy2UyG_4lQILQT5UDY1B_IWkFYBBUd28IYehRAWXmUKCNzgkb-RB1rQ68oANzkdcY-MLnpgYcJix8-yXWC_Ou6M_AQ1Opucvv_x3-TUUKAIQ5PLFa2vjsJCXA8xcASV68eZw3z2gqgm5M2bt-_O37yZEUx3BP0tFwWIT4U58RGhmDNyZXKTag--hVxTPPqpIGSyxZtj2d4B62Mu5TQK9sF6M3Ja86Ws0EmLkhRUy2sgmqorsqR10dble1h8kI0jREaJFwgvEi-L7UFcsrIpxF1UkiNcOg4TFMvUPl5_Rt5f-qEV_PoH42-Sl8VigoEq_zS9FIq_vJ_OB5nJMmJS0_o4sxmL0sRhzosjfRi5FLMWVs9v6T1CridYDGlK9yEHs0EDSnhO5WrCMbJqyUkOAisuofX95D7IDGpOYxfb1HBPBuCCeQEW15fG-iB6cTi4W7zH6M14Sn2X70MOZ22imvyrjbJLUGCIwAhsCxdZgb6f3geZWZaixEJ5j3Z54ovMd-iLI_3rkqxggL0duDuQzyQ2bmYplZWlbrvC4zTeecMRonzweRDtpc_HjTq5q2JVDcOOmQiKGRe0rdw29yK91Bw8MeTgffuEYItlJX-wudiD0TX2p-Yn0Usg9hYsmAtZFKaF-fSgJuTTiOjS3q9oIbX8E6-307GdETFdW9NScnp5enKov3gCtnsr_jOQDXqMxyO7S-RPhzLoIJ5E0v3V_BngBi3E9-Zp0B08iadHlf9n4Bz0Bt-bskHNfxJljyzqz4nHbcX_7qRtK_mTSHtUqX4GzkEd_96UDerz46F8W1Gfk0y3NfvxSJ5Uqx-J9fOgmbgd3SzXO5g2NsZ4pzQFGCZ2KXXMag8As1vUZi-iawBDzMM3CI_s8LbMDXf-hvtfw93A29ftj9ftj9ftj9ftj9ftj9ftj9ftj9ftjxfe_nj4Q83-oV4Haub6X-9-enffA8wXeUqZBCBCJ03CxI3ciIVx5Lp-xISfZkaNjisiHlE_oiESjr7GriRKsTdxHREz4fFDE7rreWU684M7nldunu7_bz6vvB0tqVoa1UWBk7jgZDw0erc2Bg1kJ8PndH_dQCz0XcGiLPPSrB9o0BD2Az29n-vGiSMvjRxwQXDejzNo8bpxnpk8yK9LqknbfIsZ-YirgUrmaAgrJVYcRfRNiSViQXMba4pkdbkiZQF9NNp5oQ9zYclEkSlCd6pNmwLMyoLqFc7_pB94PWvvVg2GB7JO8AoTsV2MT9DGqhu1j_WJqoDLDK8oG101mtQNwyKmTtqpndldTkKzDLGDMFM_c9wxfnjmw2-vOhVlZRSAMzR4lLnMJhL0U9WocftDFkrXDTc5Cw-142xSzXinEWyxTK7t2zpYS3HKmVw0tU14J3fk587DoeOxJODcSd2Nhwd98Y6SntrTdkOlfhy4rss8yp1-qEGb-xgxHW5Rd7XUlz_0Rw0ElQ-1DTyMXJrna8LQfQopx0M3Ui_tSrSb1rvWuRcXP5EDpA409HEpFYHCJF1BsE-qWxuDpe7NUuYoWJQj1NdmxW6GstT11scWjUT0dplrJLxco8cFQWtLHF3jrAg2uZJLDIX3yMw_XNSranJ9v_YOy25fOcrmojH5J6xkIYl_4ppQwv-2MO5y0Om0UyaHPFdHtMa8KOBBHPHApb0ABuuGHa29QMPfjerRNPTjKOWhCPpRB2uAR8nuYPO-L7wB7GWZYz5SDcMqWFhZ9NhtWio0YWsNE7NhgmkHPbvJYYMMVoOVTtE1MOaS1mG888MNKgQo5kqjRJvSuhxqxpW6aQXVb8cszKt_hVE9ViCjRtPMZFgisibPJ20OIpRzHHpX5mBB11RhR1niZFqhFpip8O6VxTKpaC312uBTaGV4Bhmor9sZLNdViapW8mje9I12o8PaVYCDtQZL5DMHhPJHgxkcxzccWbBlbqISEymCxnyKcxrjOgHTPTfBZoZteUHYYNIsGKd0JmWBIYwhSLWGVaWPqRtYRGkYeiJ2oNfZYOG2o-4XWXF140ZJEkWZC4HvbXqBwSLsMfo-vHo6WKNpVzfbrDHtN_6mdk5T22AhlVPz9tUK3SbanyiERSu7lYkJrsw2ILXFt6v0psIRW303PTZ8Ad7ost5XZPvil1niGHxSrQiGgLYvc6H_0Kyt2jh-lUObi1H0WV7e7CbWAusBBtDmVcJthkGR35tgrVID8xEelqtAadUmq9oGg-HKA0lAySGJSM3EQrDLBNK9MtumWPQOFoGOSry8wFBqX_WyC5pr82bukF402J41-7lUrKR9y6sX-fqIhrlw0shNOLCEbTS8XR3vaPgFlrV9XRBpGoeZk_iw6UEGK92_qMtEkbT7zdI0iCuUs9WLFSImbzBNQb8caLuDrcDaR9njTvWbXW6TVcouH3XvSG_3wo2TQGIOGVtJZzRXm_yNNd90DZJ-o20bZCaNUWwGyUp-gbbJLTBKLO1ZpyKjYsxvy7LJjVhW1EgfF0WtmIdK55gQaaVgO9nG1il0jCluh6WOLdNhbfNyYbb_r2Hak7ZNBlgwcP6W1LaP_mAC_QKlnhN32v71SNdgmDfTZWWRHBaqEJGIEoA0TLxeMoOdhq1QH7px0NlNQt9nCS6S3TjctMPbvYSNFJ-xNWDuO8fCn-dyYXUx7KmHzbS9YVAm9vuh39___MPF-dn88scPP198_IAL2N_H5Pezi9Pzn-Y_vPv5X29PL89_7A4bNB3AtmNU5FoqrJT7g2CjUSpp3-7fLUtnF-fWSleeNpnbGjAPcs7aGMI-dpMJfrFDYBqqWwSXcoGTv7R-Rhu2CyfqSub42S2q2hz3jec_f8V__wXs7y75)

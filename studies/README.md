[//]: # (ob:11fd7444)
# Proofpress studies

[//]: # (ob:b85e1163)
This index separates research results from product mechanisms and planned
integrations. A result is only reported within the scope and denominator of its
canonical study package.

[//]: # (ob:9f40eb3c)
Status vocabulary is intentionally small: `design`, `running`, `frozen`,
`published`, and `archived`. Evidence types are `controlled study`,
`descriptive pilot`, `conformance test`, and `integration mechanism`.

[//]: # (ob:b748a645)
## Active and proposed research

[//]: # (ob:1243581b)
| Work | Status | Evidence type | PR | Canonical entry | Boundary |
| --- | --- | --- | --- | --- | --- |
| RSI-Exam experiment provenance | design | integration mechanism | this PR | [research plan](rsi-exam-experiment-provenance/RESEARCH_PLAN.md) | No real RSI-Exam rollout or efficacy result yet |
| North-Star workflow study | design | controlled study | [PR #22](https://github.com/chenmingtang830/proofpress/pull/22) | [North-Star plan](LONG_HORIZON_EVAL_RESEARCH_PLAN.md) | A future real-workflow study is still required |

[//]: # (ob:83307a40)
## Frozen and published studies

[//]: # (ob:383f78f5)
| Work | Status | Evidence type | PR | Canonical entry | Boundary |
| --- | --- | --- | --- | --- | --- |
| Agent Handoff Artifact Provenance | published | integration mechanism | [PR #20](https://github.com/chenmingtang830/proofpress/pull/20) | [study package](agent-handoff-artifact-provenance/README.md) | Version-checking evidence on the registered task; not general agent efficacy |
| Governed Handoff Pareto Study | frozen | controlled study | [PR #35](https://github.com/chenmingtang830/proofpress/pull/35) | [public results](long-horizon-eval/relaybench/PUBLIC_RESULTS.md) | Proofpress-composed LAB-derived panel; not an official Harvey leaderboard result |
| APEX Agent Evaluation | published | descriptive pilot | [PR #36](https://github.com/chenmingtang830/proofpress/pull/36) | [study package](apex-agent-eval/README.md) | Locally generated artifacts and native grading; not official APEX Pass@1 |

[//]: # (ob:2bfbdae4)
## Mechanism and conformance evidence

[//]: # (ob:1681c0f4)
| Work | Status | Evidence type | PR | Canonical entry | Boundary |
| --- | --- | --- | --- | --- | --- |
| TRACE decision-provenance adapter | published | integration mechanism | [PR #33](https://github.com/chenmingtang830/proofpress/pull/33) | [TRACE adapter](../docs/TRACE_ADAPTER.md) | Imports external events; TRACE dispositions do not become Proofpress admission |
| Retrieval evidence locators | published | integration mechanism | [PR #39](https://github.com/chenmingtang830/proofpress/pull/39) | [retrieval adapter history](../docs/TRACE_ADAPTER.md) | Evidence locator support, not a benchmark result |
| OpenWiki conflict gate | published | conformance test | [PR #45](https://github.com/chenmingtang830/proofpress/pull/45) | [conflict gate](../examples/openwiki-conflict-gate/README.txt) | Demonstrates quarantine of unresolved contradictions; not efficacy evidence |

[//]: # (ob:099a65fd)
## Archived and superseded records

[//]: # (ob:2bd2c5d4)
The [ProofPress Artifact-Native Experiment](https://app.notion.com/p/3b51bd5e74fc80908d2afecb6341d1af)
is retained as an archived Harvey/Gateway qualification record. It is not
rewritten into the active study set.

[//]: # (ob:13153b0a)
| Work | Status | Evidence type | PR | Canonical entry | Boundary |
| --- | --- | --- | --- | --- | --- |
| ProofPress Artifact-Native Experiment | archived | descriptive pilot | historical Notion record | [archived page](https://app.notion.com/p/3b51bd5e74fc80908d2afecb6341d1af) | Historical qualification record; not a current product-effect study |

[//]: # (ob:0f653d72)
## Published result notes

[//]: # (ob:ff6712cd)
- PR #35 is frozen at 7 models, 3 task families, and 126 valid paired runs:
  rubric completion moved from 89.3% to 93.4% (+4.1pp), while unsafe
  propagation stress pairs moved from 8/63 to 0/63. This is bounded,
  Proofpress-composed LAB-derived evidence, not an official Harvey leaderboard
  result.
- PR #36 is an independent descriptive pilot over two public APEX-world legal
  tasks; it is not official APEX Pass@1.
- PR #45 is OpenWiki conflict-quarantine conformance evidence, not a study.

[//]: # (ob:353c87ec)
## Reading this index

[//]: # (ob:7582f3d0)
- A study can be frozen without establishing a general product or capability
  claim.
- A mechanism demo can be useful implementation evidence without being a study.
- Planned work has no result until its declared execution, admission, and
  synthesis gates are complete.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2IxYzk4NzNlOTFmZjAwNmNhNjg4NTIyYSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6Ijk2ZjcwMTVkIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8zMDAyMzM1ZDI4NGYzMzQwOTExYTk5NTIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzBiZTk1ZTM2M2M5YTQ0ZjMwZmQ2ODJmYyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWvtTG0cS_lem5EqVXafHvh_KL6c4XOwqgilMkqszlJidmZX2WO1u9gEo4P_9umf2JSwEBqdyd6VfQKx2Zrq_fn09ze2A5mUUUlbOIz6YDrJsHujM91xT-HoYaprDqON5tmHQwXAQpHw959FCFCW8WyypYTvTwAh0eCG0A8s3TJcapuEKJnRueJanUZMF1A08zqmjMddyTeb4wnZ9RwSMuobFYF8eFSy9Evl6ML3FP8p5SRdwQkxLPGoIHwIRw4NfRR6FEQ1iQXJxFRVRmpAlvJ_maxKsyXGepmGWi6KANRlll3QhUKmNx3n6bwHqVjluuCzLrJhOJouoXFbBmKWrCVuKZBUli5ImC8_UJhurc_F7FcHneVWIfM7SpBAJYFHmlfg8HCwFRRB9J3Q13eYD9WQuruRLAK6Ym5pmmKaN4ISmaWm-rlPftw2ULM1LVG0eR4kAyRuLxHMtEL4tTMdkPrVgnRZyxzNCptSppZszmhVVDAobKCdLc14Mpp9uB_XxtwOwcpoX-El9Lfg8AMg_DarkMkmvk8E56ND4Axq4rHgkisnJwezHnw_GK1Toa9yFlmUeBVUJVpoHtIgK3FPE4ZwWgF4p5H5VuUxzlOkySnDLYl2UYgXfJHSFxmtkG8LSAg0-mCZVHIOkbAkWEkrHIE7ZJbyt6yF3LcuC18E4pbhBPTq3ILVK8HV9HOVcypGhP4lrePKKbH2_XGcoDhoUnGPwedgdGni20HXHfMGhp-DFBL4UN6QQGc3R8cHFC0FztsQPVVwWJMzTFQGL84qVZCUQgKhYdcLhwg3J_NDSRGCyF0j2saRlVZCrlNGgiikEmpS0BJ8CY9A4XpNiBb-m5IKLIlokF0NykVdJgig9LFngWh51LHtDshkroytBaMJRyywtBG9B2GmyV-SRpTuspxuWaXt68E0kuSO_pfkluSM1bHfk4CriImGCoAjw9_EJ_HhLkzSJGI0JwAiQ3pEf0qoTU6aBDSE909RcamkbQv4jT_8QiRKyCuKoWIKUT_HwV-SRpTvgMj0zdL3Q_iaS_FlwGUEYcCo208DPTcBIOeF5mOYrimeJ-tBHQHvSBrs8zfF0poXfUqo_C0DN96ljh3wzKMD5ISq4lLSoMpFDWMjAUMXmkQh9dPUO6IyAG8zm1reS53QpyCeZCI9lIpzVZW10RGXgH9zAbtEK0Dp_3XAEmmXjJC2jHVlNN3XbDDT6rcT8s8xr2ibzgKVtyHmicCdlW4sesejWBTuM6NpAWkyuveDUEZnJvLImjCYkEFgSMfNcA39Lq5IAXaQy_-CWlCxEInKARdbMTjh4oRx8Ph821GgA3BOpxZzlgipeIr9pSI6YG1ZAmQZM1xUOCx2m-4FN9cBFnpKW0hdq9kZq9kaAR7LLLIVSKcloLk9C6tL8hczlHGlfHLF1b4c-FextIknmM1likYblPARMRJ7lUU1Gi0CfmjTgHmWGT6lrc5fiatPXPcun3AgNzbGBooaUBrrtefCY8lCzLcc3DJdxwVB_QLyUpFJZa6pbwM3wycDQDGekeSPDPdWcqW5MNfNvmjbV0AFqxOGt0LedkDMbXKV7evsteaj0P8UTl7RYwvs8cA3GHEqF7cELco8edaxd8-lMsN7WcERoODrTNW402_bIYb3tS7heoWpsTJNE8LMEedgCNgDMijGEhlqMDC1NgJjlAr0FUg2GR5RAjAkCnVamiA3kkRQaHQpNAUlDEpXFWcLaTKKirG6ixltyXq2zR3XDcQxmBEYLZY921jq_hEXiRxXmF8Oz5KIlGPAc1bigdX69GG9mR8AqF-QCU02exnHNSNZyEziE5VEmc30WxWmJh_SLLzaezQE9lDtLXOzAxPIDw2aCWtDstn7QEd7GvZ7DWusTXBEGlFMKcai1DtwR2fqEl5SPhKOV7s6SOzIajcgjP_G1k4_vRwc3dEVEWzxRK0ikEtE7oiwLH7YCCs9lDZAifWrjAX39_DWkhZGAvUfd3qNub8gMHw9mJ2_fzY8PZ0eQIN7AFkcpQAk6tWKhE2CNAHcXYQj6snUTMGtRKh2OIF6WI4ArJ9cAXRin13Uk9MS_71EoL0j9yjA6svCkC4VJBuVgYhgo7qfe0Urnww9HP83ffTh5_68PR_ODX2eH821qzkhYlVUupLKje0JHmLeiOCb1vQUnd9toQe1Upsa5FVoO9W2zcape49G57dd3D_UJgUcNwU3N0sP2hF5D8Ze47WyBjvoOlEnDsCWCmPo7z-20fNh5lQtoz3MBTbrARs49f01RstFSSTZqKt6m39cVEZf_qornSHIG5D9NAwHFQKb-XCyA-Ah0g5IWl98ToC4tRZKHdYEhofkJL-Wg0LToHENGLVOwi_L6mnw9HBGm_Sw4TFvCIVFnTUU8fx2nyWK0TPPoD9BSXNF4kouYrgPQcTk5_uWHw_dvMUR-OTz9WEPS1e8RnKvy6-HshxGHHIKMPKOJiBUOQCdTVD4CLN7R_EqsSQwOLPIgpTlvEoXymOODf9ZucwBSVMoXNr3kiwLTQuI8DxJnq4dk4mak3ETiseEPh1BssbAqCyMNaFxIsYhEtTrgyximCoUWAqnjMS2Kv-s7cwa3XN0O7VDzadBEdK_77nLGc5vn-hwtsBg33dDm3G8LXtdP_yWZ4_Rk9vYALM3kRXQvLgmU5gwC7Wsyh2k-zy9M6RdKlPrY89fj8YSnrJjIx_PZj7Pj04OT2i3er5AUFlCl4dUEMcBWp_i-UScqIE4iSSkJT6VXBNCprkSfDVO-iuRtbF36RZlH6IFdzgHOjcyy-CoM_Odh4L9RlKERooG_Hg3sxuPgnsTYoiNCQ5UWiEwvKwpu1c8BHzKR_BZdRtKTIUtBIoUQu6fsfULZ6Gk9Ly1aKi1unCh1Q2aUxdAhAbVPrkGqUfPOCN9p0kJ5U-IGP4oV2LZUfcfvFXBXIOGJwB6gSuC0NMbUKFM6hCGTnqCyQ1sdWivvSg0hhKtnOJbQTNqEbO9eqceCn3MzVB_i6CK0bC30DWF0-ae9LGpbrudf96SJNE42MQNbD7gtXCtknuZrHjdoKFjgmJbOdRq-gX4MG7mSRlgzKWZZ0jQndU2Z_ASoX9M14h5HiKaMBKXpmLyXvRucegaGuM6jEhokDJlU1m-qugVVAwpR7uhAfMCdMqYxRq02XXaXU39JunwS_rCghWx7FVVBLcU5SnvoYWi0SzNZHp9vStjsXXfONmPVrIGwKs_rTgdb9RHEiIDYrGnQjvAIXMfnLrOE2Zmody_XhcdTr9kaFs9sxxOm8JnT7tu7eav3fclFGpM9FKMZDaI4KtdnCSEsptFqfJbgvl1e55BqmgOqQoRVTCLMVGhpBWabSZqDA6FOlMLJDY_VbYdsyAgoCcA3qbiCzBXjzQVW4ZgisxU3gsmR47ArUrKPRymLdQKBVACOC5n98IIAiWEsyv4dR30_-BlR3TI9FTwq29np2xQNci4nsQDNl8_vzVp7z3-vAOX2i5MIUAM3PoXs_18xiZW8cucgdrC7LR88MKTVQsc2uWtsTiXbulnbFu9VH5spPLhoxy10GDqubjD-wtNHRDU4mLDr2KElcckK7BsXQ2LKHouEdAUxIgp1laQbDgGCsuUmWsbPgzDdk6K-cp5xXpAAU_E9uQmwjlq8ofrtqPMV-Rg_hMf2Y7A4wJ5YgVpyM6qPK4TkB0oKKAhjpUyD6-3gerlWkm4XtFwCaPgfH2ClCnaWp9Rw1vjKRDCUX_TLgVJLVYW-cltbC9T46Zf9O_5HQ0HSv8Xv32D3b_Zv967_RNd_-qjl_qjB-Lx9kPDYVOWbjE5cjs2oq7EgoE5IPQt-GJ4wuCM0W7cEM3XNQZ5hmprhh65t2FrguZahMarpeviAPtsmJ_ZU97dMTtr_M9pPTvaTk_3kZD852U9O9pOT_eRkPznZT072k5P95GQ_OdlPTvaTk_3kZD85-T-bnAhDc12uWaahtybqXax14fE1d2RNU-76XHM8Hwh9W5V712bt9OT5N2ARYiw7CujSiymOJfIqALiaSYRM8CnaQt5keP7Y_I6AI_vm2PqOvP6bNdaz7M2QXC-jWEDiKcAAuAv2wXShkIYkhd6CBxUbm00cE_fS4PeYqPuU9g55iLs8RvyaBDZ8AveTuknk1SBHXdlGMrzxGgdyLkcP-NJZkT6T8jolNZNFUoUtWsxh_wWNcWeEGNJr1ET-VgrWHmxJY31RfEa9NL6NWjW1TI2j7t9e7qd5_0vTvPPP_wHJQMsc)

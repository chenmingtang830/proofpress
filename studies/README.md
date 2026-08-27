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
| RSI-Exam experiment provenance | design | integration mechanism | [PR #46](https://github.com/chenmingtang830/proofpress/pull/46) | [research plan](rsi-exam-experiment-provenance/RESEARCH_PLAN.md) | No real RSI-Exam rollout or efficacy result yet |
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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2IxYzk4NzNlOTFmZjAwNmNhNjg4NTIyYSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjU2OGUyMWMzIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV82MjM5OGQ2MzQ1ZDc1ZmU3NGJhZDA1MGYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzBiZTk1ZTM2M2M5YTQ0ZjMwZmQ2ODJmYyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtW2lz20YS_StTdKXKrpAUMLiVL6s42thVjq2SnWRrbRU1mEPECgRoHJIZy_99u2cAEJQpSpbszVaCLxKFY6anz9f9xI8jVlSJYryaJWK0P1ouZ7HNozBwZGQrZVk-Z34YepSy0XgU52I1E8mZLCt4tpwz6vn7KrS5IwPH8V0mPRYqSn0pPSmdQNp-5HnKExHzleuJgIfMcgWV0vZsW3CXRjKGdUVS8vxCFqvR_kf8o5pV7Ax2SFmFW43hQyxTuPCbLBKVsDiVpJAXSZnkGZnD83mxIvGKHBV5rpaFLEt4Z8n4OTuTeKiNy0X-HwnHrQtccF5Vy3J_b-8sqeZ1POX5Yo_PZbZIsrOKZWehY-1tvF3I93UCn2d1KYsZz7NSZqCLqqjlp_FoLhkq0fNDSUEpI3NlJi_0Q6BcOfOpE4XCd1AbnpKBGzNheZZCyfKiwqPN0iSTIHlrkXRmxTLypOM7PGKuqxxLCT-kipvjNNLNOFuWdQoHpignzwtRjvbffhw1238cgZXzosRP5rYUsxhU_nZUZ-dZfpmNTuAMrT-ggataJLLcOz48-OmXw-lCjMZf5C6sqookriuw0ixmZVLimjJVM1aC9iqp16ureV6gTOdJhkuWq7KSC7iTsQUar5VtDK-WaPDRflanKUjK52Ahac4Ypzk_h6dtW4nAdV14HIxTyQ94jrVbkOZIcLvZjgmh5ViiP8lLuPKIbH2-Wi1RHDQoOMfo03i9aRx60rZ95wGbvgEvJnBTfiClXLICHR9cvJSs4HP8UKdVSVSRLwhYXNS8IguJCkjKxVo4fHFDski5lowd_gDJXlesqktykXMW1ymDQNOSVuBTYAyWpitSLuDXPjkVskzOstMxOS3qLEMt3SxZHLgh811vQ7IDXiUXkrBM4CmXeSlFp4SdJntEbnl1h_Vs6jpeaMdfRZIr8ntenJMr0qjtihxeJEJmXBIUAf4-OoYfT1mWZwlnKQE1gkqvyI95vRZTp4ENIUPHsQLmWhtC_rPI_5CZEbKO06Scg5R38fBH5JZXd6jLCR0VhMr7KpJ8K3XRWMWCyc008EsbMFpOuK7yYsFwL9lseovS7rTALk_zoVRa6mtK9a0UaEVQsj0lNoMCnB-iQmhJy3opCwgLHRim2NwSobe-vUN1NBaUe8L9WvK8mUvyVifCI50ID5qyNnnJdOAffoDVkgVo6-RxixHYcjnN8irZkdVsx_ac2GJfS8xvZV7Hc3gYyM26cGz0TqquFt1i0a0v7DBi4AFocYT1gF0n5EDnlRXhLCOxxJKImecS8FteVwTgItP5B5dk5ExmsgC16Jq5Fg4eqEafTsYtNBoB9kRoMeOFZAaX6DstyJEzCjiNWzS2A-lz5XM7ij1mxwHilLzSvtCgN9KgNwI4kp8vcyiVGowWeieELu1fiFxOEPalCV_1VuhDwd4iGmTeEyWWuapmCnQii2WRNGC0jO19h8UiZJxGjAWASBm-7UR26EZMUEUt33OtSDEW214YwmUmlOW5fkRpwIXkeH7QeKVBpbHWvu0CNsMrI2pRf2KFExq8sfx9m-5bzveWtW-hAzQah6dU5PlKcA9cZX3149fEodr_DE6cs3IOz4s4oJz7DBqWEB7Qa_SgY-Oad0eCzbLQ-Cjq29y2BG2X7YHDZtmHYL3S1NiUZZkU7zLEYWewAOisnEJomJcRoeUZALNCordAqsHwSDKIMUmg01oaYAN5JIdGh0FTQHJFkqp8l_Euk5goa5qo6Zac15w5ZDb1fcppTDtV9mBnc-aHoEj8aML8dPwuO-0ABlzHY5yyJr-eTjezI-iqkOQUU02Rp2mDSFZ6EdiEF8lS5_plkuYVbtIvvth4thv0tLy2xOkOnbhRTD0umetwv_ODNeBt3es-qLXZIZAKGkfGIA6tzoHXQLbZ4SHlIxNopat32RWZTCbklp_42PHr55PDD2xBZFc88VSQSLVGr4ixLHzYqlC4rmuAFultFw_o6yePIS1MJKw9Wa89Wa8NmeH14cHx02ezoxcHLyFBPIElXuagSjhTJxY6AdYIcHepFJyXr9qAWcnKnOElxMt8AuoqyCWoTqX5ZRMJPfGvexTKC1I_onQNFu40UNhbQjnYoxTFfdvb2pz5xauXP8-evTp-_u9XL2eHvx28mG075gFRdVUXUh92ck3oBPNWkqakmVsIcrUNFjRO5VhCuMr1WeQ5rVP1Go-1235599DsEIeMSuFYrq26HXoNxZ_itgdn6KjP4DC5Uh0QxNS_9tz1KW92XuMC1v1cwNIusJFzTx4zlGwyN5JN2oq36fdNRcTXfzPFc6IxA-KftoGAYqBTfyHPAPhIdIOKlec_EIAuHUTSm60DQ6vmZxzKQaHptHMEGbXKwS7G6xvwdXNEON691OF4Wh1a67ytiCeP0zw7m8zzIvkDTikvWLpXyJStYjjjfO_o1x9fPH-KIfLrizevG5Ws6_cE9jX59cXBjxMBOQQR-ZJlMjV6ADiZ4-ET0MUzVlzIFUnBgWUR56wQbaIwHnN0-K_GbQ5Bitr4wqaXfFZgOpX491OJv9VDlvLDxLiJ1seGP7yAYouF1VgYYUDrQgZFZKbVAV_GMDVa6FSgz3jEyvIf9s6cIdzA9pSnrIjFbUT3uu91zrhv89zsY8UuF06gPCGiruCt--k_JXO8OT54egiW5noQ3YtLAqV5CYH2JZnDce7nF472CyNKs-3J4-l0T-S83NOXZwc_HRy9OTxu3OL5AkFhCVUaHs1QB9jqlD-0x0lKiJNEQ0oicu0VMXSqC9lHw0wsEj2NbUq_rIoEPXCdcwBzI7Isv0gH0f10ED0xkKEVolV_Qw3s1sfhNYmxRUcNjU1aIDq9LBi4VT8HvFrK7PfkPNGeDFkKEimE2LXDXgeU7Tnd-6VF16TFjR312RAZLVPokADaZ5cg1aR9ZoLPtGmh-lDhAj_JBdi2Mn3H-xqwK4DwTGIPUGewW55iatQpHcKQa08w2aGrDp2Vd6UGBeEaUt-VlsPakO3NlXoo-D6ToWYT35bK9SwVUUnX-acbFnUt1_3HPXmmjbPcc2LPjoUnA1fx0IqsUFCmJI99x7WFzdQT6MewkatYgjWTYZYlbXPS1JS9n0Hrl2yFek8T1KaOBHPSKXmuezfY9R0Y4rJIKmiQMGRyXb-Z6RZMDShltaMDiUDvjHOLc-Z26XI9nPpT0uWd9A8vdCrbXkVNUGtxXuY97WFodK8udXm8vylhsWfrfbYZq0ENhNdF0XQ62KpPIEYkxGYDg3aERxz4kQi4K521iXpzuXV43HXM1qJ4jvyjIyPud-v2Jm_Nug8ZpHHdQ3G2ZHGSJtXqXUYIT1mymL7LcN11XheQatoN6lKqOiUJZiq0tFFml0najWNpdtTC6QWPzLRDN2QEDgmKb1NxDZkrxckFVuGUIbKVHyTXlON4XaR0H49SlqsMAqkEPZ7p7IcDAgSGqaz6M45mPvgJtbqFPZUiqTru9GmOBjnRTCyo5vPr17jW3vX3NWi5u3GcgNbAjd9A9v-_YGI1rtxJxI52t-WjG0haS_meIwK6yUp2dbOxLc5Vb-MUbnxpxxRaKT-wKRcP3H1CTIODCbuJHVaRgCzAvmk5Jo7usYhiC4gRWZpRkk19AgBlyyRax8-NaromRTNyPhCiJDGm4mtyE0AdjXhj89s3-xvwMb1JH9u3weIAa2IF6sDNpNmulBofGCmgIEzNYVq9fhxdzldG0u2CVnNQGv7HB1iphpX1Lo06G_3qRDDWN_rlwBzLVIX-4ba2Fnjiuw_7HcuijuMJGrrKcVwrsm0WRR7tVNKf4vcn2P3J_sfB9e_o-nenWq5TDfTTdiLhNlblq1AngcBmNLB4HDNfsdCFHzSUVPjS8mxXcse2fMQZjmPRSAUe9aw4DFxqcWbZtrrhPNuYE2_fjrYwJ5GvAsv2xMCcDMzJwJwMzMnAnAzMycCcDMzJwJwMzMnAnAzMycCcDMzJwJwMzMlfjTmR1AoCYbkOtTsT9QZr6_D4khlZ25QHkbD8MAJA31Xl3tisY0_uPwFLUMe6o4AuvdxHWqKoY1BXy0ToBJ-jLfQkI4ymzncEHDlypu535PH37tReLp-MyeU8SSUknhIMgKtgH8zOjKYhSaG34EblxmJ7voNrWfB7Ssw8pZshj3GV24Bfm8DGd8B--mxa84bIMSPbRIc3jnEg5wr0gM-dFeEzqS5z0iBZBFXYoqUC1j9jKa6MKob0mrSRvxWCdRu72lifFZ9JL41vg1ZtLTN01PXp5cDmDWze353Ne8D35yBdQnHQ8m7m-u2EWG-nzxdoyKpjuUwZb-iqSiJix2oLGUB_h1g7ZgsJoDaZ1ODjlzbOb-CumhWvLagdemJm0dtX7qZnve4GxTA7fQEdteMrw1vpqI4WuJ2O-ka2uzuf1jEg3XL79qftHMf_htTxkMvhgvpOzKiIPEu6IgqpiwM-N4JOOgpsx7G5sALhURYxHkRgDt-KwtC2dxxpC69D3e28Tvf98YHXGXidgde5G68jLMEjB1INk8Ffh9cxQ4_7DT5d_8nABw180MAHDXzQwAcNfNDABw180MAHDXzQwAcNfNDABw180MAHDXzQ35sPOvn0XzVFjRM)

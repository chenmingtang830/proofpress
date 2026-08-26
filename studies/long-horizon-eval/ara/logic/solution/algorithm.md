[//]: # (ob:9d1e99a5)
# Algorithm

[//]: # (ob:4feb48f6)
## Inputs

[//]: # (ob:8ada3d1d)
- Frozen task definition, source revisions, rubric, model route, provider allowlist, and output caps.
- One S1-S3 sender state per model/task.
- Condition manifest: ordinary portable handoff or Proofpress governed ledger.
- Optional preregistered trust-stress fixture.

[//]: # (ob:3169d81e)
## Paired execution

[//]: # (ob:0dccccdd)
1. Verify task sources and experiment manifest before any receiver call.
2. Generate S1-S3 once; freeze its artifacts and telemetry.
3. For each clean/stress cell, construct byte-matched condition inputs.
4. Ordinary: expose the portable handoff without ledger current-state metadata.
5. Proofpress: import evidence, propose conclusions, run deterministic checks, batch policy review, record verdict receipts, admit eligible conclusions, and assemble a scoped working set.
6. Start fresh S4 workers with identical model route, tools, caps, and rubric.
7. Reject the entire pair on cap hit, invalid JSON, transport failure, model/provider mismatch, or cap mismatch.
8. Score valid deliverables for rubric quality and, for stress cells, unsafe propagation.
9. Repeat each receiver cell three times from the same frozen sender state.
10. Aggregate only result files named and hashed by the final receipt manifest.

[//]: # (ob:4a9455d5)
## Fail-closed admission

[//]: # (ob:38b0578f)
```text
proposed conclusion
  -> deterministic integrity/current-state checks
  -> transaction-level policy recommendation
  -> per-conclusion verdict receipt
  -> authorized admission or rejection/escalation
  -> current scoped working set
```

[//]: # (ob:6c54a20c)
An LM recommendation never grants admission by itself. Missing evidence, stale policy, superseded state, or an invalid receipt blocks reuse.

[//]: # (ob:682198db)
## Published estimands

[//]: # (ob:ebce6d57)
- **Quality**: passed matched rubric criteria per condition for the frozen panel.
- **Unsafe propagation**: count of fixture-defined unsafe state propagation among admitted stress pairs.
- **Operational overhead**: additional tokens and latency attributable to selection, judging, compilation, and evidence expansion where telemetry is complete.
- **Invalidity**: preserved attempt-level reasons, excluded from treatment summaries but retained as route and implementation evidence.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzY4MWI1Yjc1YjYzODgzZjc1NGEzYWU4MSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjQ2YTM4ZDc0IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8yMTgwZWQxZjk4NDcyODU4ZGFmN2YxZGYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzNkYmVmMzYwOGY1ZGQ1ODg5MzFjYTVkMiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWmuP27oR_SuE823rh96WXKBAcIEUt-ht0qTtl5uFQ5GUrbuypIjUbpzF_veeoSRb-_Am2Q36uEiwH2yJHHJmzpw5pHM94Y3JMy7MOpeT1aSu11HspmG6DNPIj2M_W4YB97mK3cl0klZyv5b5RmmDsXrLvTBayUy6nGcRD4LMDUUqAieLMzfIUpnGrs_dLONJxB1HOU6SRFkqlOM7y8CVy3jpiBR2Za5Fdama_WR1TV_M2vANVii4oaWm-JCqAg_-pZo8y3laKNaoy1znVcm2GF81e5bu2ZumqrK6UVpjTs3FBd8ocurW46b6TcHdtiGDW2NqvVosNrnZtulcVLuF2Kpyl5cbw8tN7DuLW7Mb9bHN8XndatWsRVVqVSIWpmnVzXSyVZyCGETcj-UymHRP1urSDkJw1dpzY0dJN0viYOnFYSx5tsxcmdHOqsaQa-siLxV2PmSkWPsyVZkfOXEWShnGceK7gofS69zpd7cWvNZtAYc92qeoGqknq1-vJ_3y1xNkuWo0fepeK7lOEfJfJ215UVZX5eQcPgx4oASbVuZKL4qq3My2VZN_rsqZuuTFgjccTze5WOiqaA3SsODFBiPMdjffycn0m2DFjWny1JpZp1znmtZWRbbmGlE2ytprDXZAe7_ISzKp99qoHd6UfEdJHnyYYqomYExWZVsU8EhskUnVxSItKnGB0Yl0VZLwEMORRKM-kb8vBxfwtF-FS2mXrwlu6gpPXrDxMLOvaXFKMyAzuTmfDuGeAM-0jbVoFO98sG-GgKi164cicoNUJr70kixyfVRNmnDyqTIWuD0iWI8IBmyKi7rKS2MB3tiVyM3hG3l5TlAqcrEfWRjDa2TEAveJyNNVZtYZvFZN3eQ9wHXqruTSCWTMMy9MlQw5ZimeofSXgL1SiR8FaZDEwklCmEZ406WgKDjCcdJIcCobbbixQO3iv3KRRnow8RwvmjnxzIv-4XqrMF65zh8cZ-U4mNQH3I6SbuAul5Ob0dPr_wa0Ld466G253mK8A04UxJNZmmCAtTFCYw_FL6Ds5mb6YF0rmZtDVSORpVmJSqpPk3PLFLIVp97eYYR7bz-2YOLD62274-WqyVFajSSi_L-iDrv7pzJHkKk0iLPoFnP8XNat0Y_Sxgt2GHQ3ndOj9ZhL7ktXfqP1GXvVVJ9VyQzXF0wqlGVOMZkyXbWNOHZLPWVNmyJxU7ZDcgvWVMcNFeikt3bju1EiY1fd2s0bjgYomfqkhI37F7x-YPgj_jtS4J-UT17RnTMrEvZdKDr3NeMlza_xZgdgM-Q_zwBoBnarGoXXe4TokUgEPAnCUN7uF694XsxEUWlsjstd3oHn8XCcmvNITPw4dcJlnD1v7Q8fPtDU9yV4oLbTYEwULc17XzI2-xNwY1QD6QPnc8FA6WqDstwvRNscd0iccGt7kUA9eo543vZeluyvvzBioR0yJDnlmZWguIZtGo7GdjRDSi83VOVz9gs9Om4OTZDf3lzsuUks09t4alMkeEuQgqfAgvxS6T4845GcKajcSIbL56w7Y2dnf295gRScna1YTZQmAV0jyERXxkwgQ0A1Z8A2ZVTaumd3oQwOFwXPdye57M4uegHyUkrNatq2sBmZIRdSsZdvXzLrFnoEOzLbCSJ7uunn0Fpr1JQB65e5RGR4UVRXFIqppQK8xY4ZKeb5KcZ7VkTuUdYJknv6Is8hOqFyKiyBqMxP0dyz3H-4_E-Q2tNX6jntFB093fBz2KjcMEWgKwUACCEL-d7JcXxrkRjEBFEhhYv3FaBZgmqhjHLZZaZGsqxqxFecMuen-Ox5-HyAik7w13PK9-kEBrQys1Us6wig5qUirJ6P-PR6crWlM85P1a7OEeXR8Ddv2Qs_ZKRC99TIKsZPbNabR2wQnOwKIrQiXiDdR4nEubotkG1sBjmCU_Swu3CAqYLeK96ILTMNR_VRrr7-_PfIVUAX5PHBbnyqGR_2rn-I1B8i9YdI_SFSfx8i9euvyO5eESU3D98Afek27LtceWWeSpWQvlD4i6VKUh56KlxylXHfD70wiLiCA7EMeOAtI24pP3GzNHN9PwhO-HPvystfOeHKdR-48jrcOf9Or7ymB2tZtEx8uj_0RDBYG_W7wdrjray3lSbCcV1QV-xmg61Rd-tt_UeOIe_LGXtdKvbOnb3zmQa9YLxVibZqrL0FbcCO_OlQREOXWEGkwD3e7Nnh2hjKQFZZRvLl-NMI29BPLSWqs1ASSO5WrskYFA2GNGqDHSrqZqZptZlpY-dl-SfTNhCk9ztQH07JAxG6wMQydoZwjtrzMTVf1297q97Sl0vphjKNxGB11IJ7q9_rPPS-9Obsz6pUDYW-ywZ6kPojtKVSnxWx-kExdvaNKtROmWaPyf6cvUK4FYcoFIXi5aKPnlAQc0R--N5Ca6Z7o2YDTx45MbeghaFgzl73CV2RB-hSVuHeS-4gWrtsMvRB0oazDjrYFuBsOAyG8xEIVizfkaXRUaVvuaOOa-Fc3um49tcDvElp6_3JhnXtYMq6W2SGYMocPvbnGYymvojFinyT095vrUEhpLaxozecaVHVCMlV1VyQ2tbKYPPRnL0ziDolQW_Zu8C-B89Z9xn5YKwiv1V3pqoKLED11S3TVSfsLefsraLfAW1MaTLAUAOVyDWNh8hHjQ7nsr-8e_23KWn8UtugZRAOqIS-yheH8kbvtxm15zqyMjzAijE8EAS5ziTmEeYok9oedvpW-bHrpbTbqX0-gg-caEvNM2VzxTdWf8B0Qs7UOGV0sDviGXPgH2DL0MlpnabaWYc13x3OSmOqgTHXmbOXmw1IgPBTlcW-PwWh_mmvdGkubTCpPPERQseevPLSHoi6E-xQZ4-QRaA8EUVJGIT-oSuMFOyRLL5BjQ485KHZpKm_TAN54KGjQO1NP09sjoqsK4l-ikUJqIGOmQXkTHGskbFs7EeDmGbHVe8WTj-o-wEj_zz2nxDWWARTu1Ya2B_b7Tf4QDG9L-H3A0q5Dx1kS-BzkfHIUrYN3Ug8D7-U_i_dj9wX1kN390IncALuROLQOEZae9SOvlY5D9DlKnUcDgljJYc1PBLTB9nwna8_qFGfnf3zHgWQdVG1SHeVDV16ZmUK1ukZo1cSx0mM7yAEO2I2NuCWZ4gDdb_S65qaYKcLSDNQJGgtKNS8f2yqC1V2XZD-s0YJnA8_ydkmZSpgruhQOmW_tZKuVagN0pUN757aFt0jgjod6of2d7WFBDn2VpZrO61QlqZofz93sBjiS5cxzSUVCRza1aYvv0ZxbfuM-oQyI2x1NEjXMlYT6Ha34w2kMcOuMdxwGziuuzZi95fTwjS6i92w3Xv0dn6Dv38DAkXpfA)

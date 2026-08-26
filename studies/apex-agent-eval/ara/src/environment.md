[//]: # (ob:005d7659)
# Environment and Provenance

[//]: # (ob:ccd38b8b)
## Product implementation

[//]: # (ob:224c20e3)
- Repository: Proofpress PR36 worktree.
- Frozen product revision: `proofpress-pr36@9f6e3f1`.
- Relevant implementation range: `516fa3c..9f6e3f1`.
- Runtime: Python 3 command-line implementation indexed in [artifacts.md](artifacts.md).

[//]: # (ob:2cfb2a74)
The product revision identifies the claim-centric ledger, verification, staging, typed-relation, selection, traversal, and governed-export mechanisms. It is distinct from the temporary application that orchestrated the APEX runs.

[//]: # (ob:ce8cec2d)
## Evaluation runtime

[//]: # (ob:1b888e51)
The experiment used a local, temporary Next.js-based harness to ingest the same 93-file APEX data room, call model providers, render deliverables, and record aggregate receipts. Its source labels are `temporary-evaluation-harness@1ff29dd` for Task 1 and `temporary-task2-harness@0b7ddf4` for Task 2. Those labels are provenance handles only: the harness is not Proofpress product source, is not redistributed here, and is not a public dependency.

[//]: # (ob:867d8bb0)
The public benchmark cases were `World425_cc6b53e5c08603a4b86024546b21cdac` and `World425_jcf-03`. The corpus and generated DOCX artifacts are deliberately excluded from this package.

[//]: # (ob:1b11d295)
## Models and grader

[//]: # (ob:0babb1a0)
The executor comparison used GPT-5.6 Sol, GPT-5.6 Luna, and Muse Spark 1.1 xHigh. Native APEX grading used Gemini 3.1 Pro through the local harness. The resulting native-verifier scores are descriptive pilot results and must not be represented as official APEX Pass@1 leaderboard measurements.

[//]: # (ob:9bab53aa)
## Comparison source

[//]: # (ob:05dd72e8)
The PR35 contrast is frozen at `proofpress-pr35@c96fd86`. It is an independent RelayBench/Harvey-style evaluation with a different task and outcome structure, so it is used only for mechanism-level comparison.

[//]: # (ob:ff6f3c03)
## Reproducibility limitations

[//]: # (ob:34bf4f45)
No formal preregistration established a single primary summary statistic; majority and mean are therefore co-primary descriptive summaries. Hardware details were not recorded in the frozen manifests. Credentials, provider secrets, runtime caches, raw prompts and outputs, private corpus files, and generated client deliverables are intentionally absent. Task 1 upstream telemetry may describe the preceding gap-resolution lineage rather than the exact final three-model snapshot; the study does not charge that telemetry to a final model cell without receipt-level linkage.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2Q5ZmFiNjQ5YjhlMzE4OGUyODAzOWE1NiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImQ2NjZkZjNlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9hOTllMjVlOTk5OTRlNzE2OTNiODZiM2YiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2RmYzgzMTYyZDlkMzkyMjk0NzcxMjc5NCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWmtz28YV_Ss7zJd2SlLA4kGA-RLXTZvMJI4n0bSdSTzUvkCuhVd2AUmMxv-99y4AErQl2iLjtNORxyOJAPbu3fs45-yC9xNmGp0x0ay0nCwndb2SacZ4HKY8UYGfJIomXpCyKJ5MJ7yS25XUa2UbeNZuGI3ipZKJ8gJFWUZlGlK6SJIs4MLnUsQpDRIKP6RPgzD0A-WlKuVc8DTLPB4GyYIpsCu1FdWNMtvJ8h4_NKuGrWGGnDU41RT-4CqHC_9URmea8VwRo2601VVJNvB8ZbaEb8lrU1VZbZS1MKZm4pqtFS7q4LKp3ipYbmvQ4KZparu8uFjrZtPyuaiKC7FRZaHLdcPKdRJ4Fwejjfq11fD3qrXKrERVWlVCLBrTqnfTyUYxDKKM41hmAa4Mr6zUjXsIgqtWLE0VjVQK_0K18OM04EnMgww9q0yDS1vlulTg-ZCRfCUzkQR-DPGVQUppGi4WPl2kYbec3ruVYLVtc1gwRT9FZaSdLH--n_TT308gy5Wx-Fd3W8kVh5D_PHnZL5lcwponb2AlQ1VgmptWamUvWK3uZuBW2czUDcsv5vupZ7zVubxghs1m1ojZTJU32lRlAQ_PCzmZPqnKWNMYzdsGkrvizGqLTqg8WzELQW-Us9c2m8rgUq51iSbt1jaqgDslKzDnh0uaggGL1TJZlm2ewwLFBq4rDNCb6RChCZQgPrQSRrFuHndncFqtkmzhJTxMEuplnpIL6od-oqIU560aV2t9EkmfRALlJK7rSpeNq0njZkInhk-9D3WVa7EdWRhXxMiIq7UTi8VWWbPKICrK1Eb3NWm5v1QB90QY0jTJhC_8MGUZz0KRpGmc8ZSGFPo09FWICUuDULAwjdLU54skojyJIrTdMFzKPcQWf0-oR-OZl8xofOkHSxouI_8vnrf0PHi2jzM8FXI_WIReNnk3unr_Xy0_nlfi2iXl3bvpg92jpG52vfNDrcoX35KXlVR3kzeuIWUrHr39Xud9ePvXFiDv_6kznWOnNOZ9lwoY43mRXMSuzQByG3WHq_96vxLCSongD6lipcDOGeaW0jlVI1uoW7jyBTk6rtnW6CTCNvg4wQIYnBBCBglP-IETr122G6KLOldokmFwjjrwBXl00JHZKQ0F9VRw5uwz8qOqK6uRMZcjviSvfwxicluZ68YoNf-lnJG_m-o3VZK6nwNM7D3MgXMP3RMZp2wRnune5UaNJ-wIXksYCrSvLGngvsiZLmYCrhktSK4koNmU3IyyB7jKDlOnEqEElYf1A63SOo-IaWGCQn0kbQ8OOJIynyfQPpF_xqwYD3VXg-px5QqiQxJGwD7LpwT4DliAgfR5Bbbnb6HZGT6wYabs1Mpj8UjihUw49870rG45cBbhqhSbgplrImB-S26VUeTqX5XJZUijlRAxjwIVCS-JvYCFPDnimc99X9I0OvDse0DH3LpmXRsmlflIoh56_kiePM4495l3-pxdmpRooa0IaEhYlrYQR5evf7y-nEXzmPxUQc6GD9-1JZs660eCkYJjUcDYgWMv9-Zt1Rrxsap96PljwYgkyBqVnD4nBgPQJCI43jAL_W9J1oEJa8jViJxqE0RfCdAYMomv5uTb5kgwsizOAuEdAiCAmUMLzXWumy2IrkJ3KGM_EpbjI48EKAhBGWVh9Hv48aoiWWUKlgPoQdOsAVVN14GgAUDdabtxDW_BiRyRURfY7rYtCvZ-qEA8OGR8lDnf86LXqy_wo8NVNwSaea3LEvn5lyMM-8uENJUbZVmpG_0b2Hjx-ut_E0f2RO2h5MWPL-aP0ejTPXqYUc7wZkSrT_fm06j0DOf2pPp0586hUtxkC-fUlEAhgtE10A1Um5wZlQ83VH5OGewp-YTC_ICqzvBkRNOnRflUgkaPcS8GCNk5XiiSBrNMQ6s73yVrGDHVGWsbEf2JFXQixcceDaMw5tQXkokrBx_759-KbOYFgPiXZ-VtJxWevrYP6P0MR0b64dQCOk06fA8PkZ9qTIs_98ndN3q9mZNX4OZNX0G4Nn0OPo4kyNPX9oFsOCfIe11yWpBPlST4KAPkLKWCvTriJ2iHnG3_ii1x8Q0zN2o7s832jLWNpM1JJPSY9DjDpZHKebpL58ga_I3u20aLL0nB3lYGV4XlXijIAwPggVmf3K9vRnLtfnK72R6sYWdjCiORJIWa8aot5TGrgwOO7_EsZksc4-NZ1iefKB45D-4iPT4qHB-YjY8P759PTZ5PTZ5PTZ5PTZ5PTZ5PTZ5PTZ52avLpr_iGV1y9T0s_ePfwu6yPvc77Xd7ZpUEUhODlIqZZmPiBvxBeGGcLGgapEmlEFfXTNPbSdBFRiq_iaeaxOBL44i7y5WMLeuDtXeAtQ_rA27vdi-7_wbd395MNsxsEx8xPFjHgqCew_JyNkTTqa_HpCqc3n0LolKfSwOOLwfxI9Azmn6ZfetteDE2TxJTzOBlsjyRNb_ssdeLEwvJ9fIm_SrNYBZl_5YbBhgeyVr7vOzEoOmFw5McZC8R8fjiq40Nwadts4OkAQb6A0M6w_t-3hRusO-hbXZKfh4RbyP-bP40__Xn-gJzqo0U5o1KGsVQ02EVrr7D6aP0R52JKdH8CLmFboOxwlIjfcSnhYRAnAAWwoUHZrm1hh40mfvdFl-AZIH_hXNnLFQZA0c8Od4ATKiM2ymFfv4txOxVQIXb-ACP0QZLQ_omXyGAh2K5c90JvX66fqtt6u6CLoCdZHDMWD3ZHUm4U_M99XFYVU5BUeU4KFCOYa9zRGTuFdEONGQJXNSQCkdh2ieleysMmbw10AuHEC0rXjcuL7dmbuC8hWbcDvdr5OtvvCWe9o1_5WUYBFq6Qpsgls9fE7w7A9qMauEp3AwA6pMzC0QA6J5ebyh5MWu8ACUJSSvCeVGUOLY_hGIIERQT7xjEKDMXerWI6PGEUFpt7nY8xBiLtYtHfZoNOHY49xPZIVQWcZsIHukzjHQiO5PK49T7zgSJ2b2XqthehqlRdf_zth5ewix-QxMUT64C72_kWqlLkLW73-86DMPRfIDuybJ5QGuFXYsS46HdafN9Mn6ite7OJBDANfEaBzXeMtZfbB730eU8O1701VehSkwAehcKC6JiqXW9c3bneHaqviz9UXZs3OLh0BmcdcELnWUiNGoJvhYEWwwlrnbuCxGFdkIoWuhzLkKM5rGOAC8QKKPkMMFjDnM7N1wz7DSAag8orZtwxkW2NY5ZjQLjw0iSiIfW9dMcWo63DPnefuBXozUYBcPMiDTL4scvdfncwyt3nPpAEWBydV93qZgNNLXWWKTw2IohALtZV20D1AKA2BmCiRRywgLRuHpd9BBmHTDu-moEcAGjdF92RONMoS0HPKiF9MQRktCvZx_nJe4tB33kqBg0sVZyqYYLRdqOf4I84k1QwA8LPbBg9LvLOEiiMOYEcyduuCRqm8x79OlDuvh2GKgi7qy8JEE06Az9h7EvAbdQqLAfuGrgNNIcwqkGK66gaUBW1AXxmt_hUUfeNBcmu28YN1TfIdD1YIov2ZLjHTJFrrJQxX7q1wi4EXahKYFkIA8fmnA9E19YQWcUAQxXKuwbCULAhFNwFClMglIOXNatBOtkqd18q231pEuaHeKLM6eKg7hiKIg0zIvooNevI3Zastpuq-bKTBO4MVlaqozAoVrNWnVbaOwMqgvWWOhtCgVbA9oDYDMTfFzi48yADvHkH__8DafEi5Q)

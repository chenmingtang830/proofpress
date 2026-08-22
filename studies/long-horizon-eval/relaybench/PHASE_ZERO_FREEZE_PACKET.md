[//]: # (ob:67fbc37c)
# RelayBench H4 Phase Zero freeze packet

[//]: # (ob:9593fbf6)
## Review status

[//]: # (ob:664294fc)
This packet is a local freeze-review candidate stacked on Proofpress PR #22. Phase Zero uses deterministic test doubles only. It contains no real or paid model call, Harvey LAB evaluation, benchmark result, or evidence that Proofpress improves legal reasoning or model intelligence.

[//]: # (ob:621f209a)
Reviewing this packet may freeze, revise, or reject the proposed inputs; it does not authorize real execution.

[//]: # (ob:8ac7637d)
## 1. Exact upstream revisions

[//]: # (ob:e9565f83)
- Proofpress canonical plan and flow: commit `10ee8c4c9a6d56dfedf563a0679e6a5bb167fa0a` from PR #22.
- Harvey LAB source: commit `7be41d57fd5a6e97b5f246a029e810f83d09cd96` from `https://github.com/harveyai/harvey-labs.git`.
- Harvey scenario: `tasks/contracts/commercial-vendor-customer/master-services-agreement-playbook-escalation/scenario-01`.
- Proofpress engine candidate remains `a5e5ea5e3174c2c51982ea36537cef362a973ce5`; this branch does not change `proofpress.py` or `proofpress_evidence.py`.

[//]: # (ob:1ae1cebc)
No moving branch, tag, or “latest” selector is permitted by the acquisition manifest.

[//]: # (ob:85003b5e)
## 2. Harvey source identity, hashes, and license

[//]: # (ob:0b49e834)
The candidate records a deterministic acquisition manifest at `bench/fixtures/h4-msa-escalation-candidate/HARVEY_SOURCE_MANIFEST.json`. Harvey binaries are not vendored.

[//]: # (ob:a27c7e4b)
Harvey LAB declares the MIT License at the pinned commit: `LICENSE`, Git blob `e04042669602230e08975f78d470c4f72ce2d027`, 1,066 bytes, SHA-256 `f92627d2ebe80fc0add3b171b2d7eee5e28a98dd0d0a4a5ee5829314243bb3b9`, copyright © 2026 Harvey AI. This packet reports repository metadata and does not offer a separate legal conclusion about downstream use.

[//]: # (ob:d12ed2bf)
| Scenario file relative to `scenario-01/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `task.json` | 25,808 | `ef7e3e968910508fd43b3f90708bdc6cd013f2cbc837ae921175ebe5b2d4394c` |
| `documents/akintola-business-case-email.eml` | 7,431 | `9e81cf1892b43fda51a9a0b43ab74e4e68e549b2d30a5115841958e8e5609874` |
| `documents/contracting-authority-matrix-v4-2.xlsx` | 14,308 | `f4756869ad95267056643ea32ebf0146651730c76876401442e88c89d0db48be` |
| `documents/deal-economics-summary.xlsx` | 11,199 | `d95f10e77d100fc0b6403d8efb4d4ef0f8679110f3d5ad42240ead17d9cf22c7` |
| `documents/designated-competitor-list-schedule-4.docx` | 44,747 | `6b39f5f8b6103f3905a469778aa5e8aa0fb61125c45c9454056a9b2e6c5c58c8` |
| `documents/exclusive-negotiation-letter.docx` | 45,658 | `a9495dd63aa52a4b61c4eb9bc735a6bc5b5b321ea06d04cbd0ebefb543abc852` |
| `documents/luminark-standard-agency-msa.docx` | 73,785 | `9e9849d5dd9e66a1e7146dad7cd76b4a4ed0659bfd129a01564659fff0ee6f8c` |
| `documents/negotiation-history-summary.docx` | 70,352 | `2840521f483f59ae89c5ce17c84419d72d00608640061969618c6ee7e15b20a1` |
| `documents/prism-msa-redline-v3.docx` | 86,862 | `f59438b282618d4f4a100f44a07d917aefc956405a8a69e54566ca0dfb42fea2` |
| `documents/tsao-escalation-request-email.eml` | 12,595 | `fae24224c14778d7d4fac43d8e54b886912384dee0f1a5e60f7855c8a4c79618` |
| `documents/whitfield-archer-legal-assessment.eml` | 20,819 | `8ca207cb93b052a87cef12e3c33d2fa317a663d822cbd025c2a8fd300d726790` |

[//]: # (ob:85069311)
The executable local releases under `test-double/` were not constructed by transforming or preserving these Harvey files. They are synthetic mechanics inputs and must not be described as Harvey material.

[//]: # (ob:63aaf5fe)
## 3. Complete proposed H4 release chain

[//]: # (ob:1578c6dd)
| Stage | Released material | Expected deliverable | Boundary |
| --- | --- | --- | --- |
| S1 | Standard agency MSA; deal-economics summary; exclusive-negotiation letter | Baseline issue register | Same first worker |
| S2 | Prism MSA redline v3; negotiation-history summary; Designated Competitor Schedule 4 | Updated negotiation-state register | Same first worker |
| S3 | Akintola business-case email; Whitfield Archer legal assessment; Contracting Authority Matrix v4.2 | Targeted revalidation and escalation plan | Fresh worker and workspace before release |
| S4 | Tsao escalation-request email | `escalation-approval-memo.docx` | Same fresh worker as S3 |

[//]: # (ob:62545e45)
The upstream Harvey task is single-stage. This composition is a proposed Proofpress long-horizon extension and remains approval-blocked.

[//]: # (ob:3f1514c1)
## 4. Proposed intermediate rubrics

[//]: # (ob:a2248dd6)
The machine-readable proposal is `bench/fixtures/h4-msa-escalation-candidate/proposed-intermediate-rubrics.json`. Every item below is proposed, excluded from Phase Zero metrics, hidden from receivers, and blocked pending Richard/Tommy approval.

[//]: # (ob:b8177699)
| Stage | Proposed deterministic criteria |
| --- | --- |
| S1 | Record the exact released source set; record only supported standard positions; bind released economics/timing constraints; mark unavailable counterparty/authority facts pending rather than guessing. |
| S2 | Select Prism v3 as operative; identify all seven issue families and current positions; distinguish negotiation status from approval; record the competitor schedule and Sable objection without inventing authority. |
| S3 | Apply the authority matrix to escalation boundaries; distinguish business preference, legal advice, and approval; selectively revalidate affected state after the cold boundary; do not infer final CMO/GC authorization. |
| S4 | Run the unchanged upstream 72-criterion evaluator only for the final memo; bind the final request and operative v3; carry all seven issue/evidence/authority states without unsafe propagation; report quality, state, recovery, false-stop, and cost families separately. |

[//]: # (ob:7647cc0b)
## 5. C1/C2 file-level information parity

[//]: # (ob:2db6159a)
C1 receives the complete ordinary workspace and readable handoff state. C2 receives byte-identical substantive files plus the Proofpress representation and verification affordance. The only Phase Zero C2-only path permitted is `proofpress/portable-carrier.test-only.json`.

[//]: # (ob:6476faa1)
The auditor inventories both packages, rejects C1-only paths, requires equality for every common byte, compares canonical path/SHA-256 projections, enforces a strict carrier key allowlist, recomputes every binding, and rejects added conclusions, recommendations, hidden rubric facts, or substantive summaries.

[//]: # (ob:73f4816e)
Run the focused positive and negative audit tests:

[//]: # (ob:3eecc2fc)
```sh
node --test bench/tests/parity.test.mjs
```

[//]: # (ob:1e47d019)
Run the paired end-to-end audit as part of readiness:

[//]: # (ob:b6fecc13)
```sh
npm run readiness
```

[//]: # (ob:39edbf33)
A passing machine projection does not replace human semantic-parity review.

[//]: # (ob:9a96e202)
## 6. Cold-boundary definition and evidence

[//]: # (ob:97d517c4)
S1/S2 must use one worker token. Before S3, the sender child exits; the harness creates and inventories a new empty workspace; copies only the declared, hash-recorded package; removes the sender workspace; starts a child with a different PID and minimal environment; and rejects Git, sender-ledger, transcript, conversation, hidden-memory, orchestrator, link, or special-file state. S3/S4 must use that second worker token.

[//]: # (ob:fddf1af1)
`bench/controller/stage-controller.mjs` refuses S3 without complete evidence. `bench/tests/stage-controller.test.mjs` covers missing, early, reused, and third-worker failures. `bench/tests/runner.test.mjs` covers workspace/process enforcement and forbidden transfer state.

[//]: # (ob:f7f17c15)
```sh
node --test bench/tests/stage-controller.test.mjs bench/tests/runner.test.mjs
```

[//]: # (ob:d5c5adbb)
## 7. Scoring families and claim boundaries

[//]: # (ob:9392685f)
The deterministic scorer keeps these outcome families separate:

[//]: # (ob:c5dd6bfd)
1. final legal-work-product all-pass and criterion pass rates from the unchanged Harvey evaluator;
2. unsafe propagation and state-consistency criteria;
3. stage disposition, recovery, revalidation, and false-stop outcomes; and
4. latency, turns, reads, tokens, provider cost, Proofpress overhead, and invalid-run reasons.

[//]: # (ob:f53a308a)
Horizon degradation is unavailable at H4 only. Phase Zero does not run or simulate the Harvey evaluator. Proofpress is not tested as an improvement to legal knowledge, drafting, retrieval, commercial judgment, factual truth, authorship, identity, authorization, or model intelligence.

[//]: # (ob:9e40e067)
## 8. Remaining freeze decisions

[//]: # (ob:e9d10ffa)
1. Approve the Proofpress, engine, and Harvey revisions or replace them explicitly.
2. Approve or replace the MSA scenario candidate.
3. Approve the S1–S4 release composition and all proposed intermediate criteria.
4. Approve C1 native continuity facilities and complete human semantic-parity review.
5. Freeze provider, route, resolved model, reasoning effort, temperature/seed support and values, tools, transport, and telemetry/cost availability.
6. Preregister runtime checkouts, timeout, attempts/retries, budgets, repeats, exclusions, invalidation, and statistical analysis.

[//]: # (ob:a0631bbe)
C0, clean-track execution, integrity-fault execution, H8/H12/H16, merge topology, and the 72-run pilot remain outside Phase Zero.

[//]: # (ob:87915c3a)
## 9. Reproduce validation

[//]: # (ob:5e66ec84)
From the Proofpress repository root:

[//]: # (ob:1919b0c6)
```sh
python3 -m unittest discover -s tests -v
node --test tests/npm.test.js
cd studies/long-horizon-eval/relaybench
npm ci
npm run check
node --test bench/tests/parity.test.mjs
node --test bench/tests/stage-controller.test.mjs bench/tests/runner.test.mjs
```

[//]: # (ob:8ab3ae9e)
To acquire and verify the exact Harvey source separately:

[//]: # (ob:6f5d9658)
```sh
git clone https://github.com/harveyai/harvey-labs.git /path/to/harvey-labs
git -C /path/to/harvey-labs checkout --detach 7be41d57fd5a6e97b5f246a029e810f83d09cd96
node scripts/bench-verify-harvey-source.mjs /path/to/harvey-labs
```

[//]: # (ob:22c26513)
The Harvey verification command requires the checkout to be at the exact commit and all 11 scenario files to match their expected SHA-256 values.

[//]: # (ob:85b9bc9a)
## 10. Interpretation stop

[//]: # (ob:b632fd8d)
The mock episodes demonstrate only that the controller, parity audit, cold-boundary checks, deterministic state scorer, exclusions, and report mechanics execute as designed. They are not model results, legal-work-product evaluations, Proofpress efficacy evidence, official Harvey LAB scores, or authorization to proceed into real calls.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzE2ZGE4Y2FkMjU1OTNiNTJjNTEzOGE2YyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjI0NzkyZDZlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9hZjcwZjJlNWJiMzAxZTliNzU0MzdlNjUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzQ0ODc5ODQyYWMwNzViMTlhNzc0ZmVlZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXOty3Mh1fhUU_SepDIa4NG7UL62stVTZ9W6JslOxd4ts9IXEEjMYAxhKs5cqv0P-Jg-Q18ij-EnynW7chqSGFEk7cYJyeUViBt2nT5_znTt_OuJ1W2gu2rNCHp0cbTZnfix5KrgMoigL8ygQkR-mPBZHi6O8krszWVyopsV3m0seRPGJH-tYe6nveZJlItFJnkbal1EstY9XPaESkQopZaAUV5kQfiJ5lMehF2Rp5kVYVxaNqK5VvTs6-Yl-ac9afoEdSt7SVgv8kKsSD36v6kIXPC-VU6vroimqtXOJ71f1zsl3zrd1VelNrZoG72y4uOIXig6197iuflA47ramBS_bdtOcHB9fFO3lNl-KanUsLtV6VawvWr6-SEPveO_tWv1pW-Dns22j6jNRrRu1Bi_aeqt-WRxdKk5MDFiSBTJWR_bJmbo2XwJz1RnXiacDFeV56Pkqy5OIhYmKiQubqm7paGdlsVagvL-R8oyxNMlSFnDhJVHuZzxJmFZK2eN01J0Jvmm2JQ4cEJ2iqmVzdPLHn4667X86wi1XdUM_2Y-VPMvB8j8efbNR65dvnVeVVB-PvsdBeqGgW263slDNcVmtL9zLqi5-rNauuublca1KvsvVWlwef_vm5enrsz-8fvfN2ZfvXr_-w-uzb1---ufX75crebT4LBHjbVsX-bbFzZ7lvCkaIkGV-ow34HirzHrbFoTQOa6KNS3Z7JpWrfDJmq_owvfOs8D7DUnK0cl6W5Y4nbjE1SrLnLysxBVeiROdizAhEnCrrfpIZ39HJ_yCTui8Yc63l7xRzh9UXTm6VupH5ZCIKZLPjg4upSFwQ8KpPuDJr5wHr9HuNkQ7SQyk7-iXxUhcBjbpXMc3iKM9nKbl7bY5SAMRsf_dA3vFMQsypsXj9noPbeyO5OAn7mBVXnZnde3XHMHXspDQbVoQX5UO1PjbeqRrw2u-R1TKRRKHidwjyl86rz9CrJztpmlrxVcDJtzHjsNvHmCOyqI40mn4HHS4E7gillTrgli1KfnaAYMcXVYfThwg0qponXPfUyoVTGQ8BrSOVJZAvz0Sfa58oXLxHCT-tnJW1TWY4OQ1hwQvHODywqlq5y9__ncLzn_583840E9F0EI3vlE16IWeEh4futHI86D6ao_MYOm84fW12jlNta2FcgoJ6Cra3cKB3lyqZmE4U95zvQ9dphAK-H34xr2cZSoN2bPT-f5STRShw2sojFQtsXCNey2EwwXsTVMQHDorvi40WO7wA3zlQSISxfJnp7db4KuXX4BEUXKIrdPiDF-_fe98ZTnp8NY82hTrNQTAiu6Jc_7VAXqlHygZ5PrZ6f3ZOQVRvC6AtIXxFyCwxbVy2so5b7qPXM8_Pnd-dr7YQZbx7-mbl24wVS9jkG8KbpyFvv9XEQj1UYmt2bMDTlCtYDEaZ7uWqnbOSeVcWW3xDRD-QdXKWVftIUWLQ851pPcVLVzCOK42JWTNgQexqRrcF8xTt50DC1ms79Gyh65xQLn8KElFLOXz0oZrBEwpXOc7-4qE6kCpCvDzZ-DgBmCFZ1KVEIfaMBsSUIHDvD5083EQsUix6HmppWsfULkTopY3VwSmDRhWKreh4ywdY1uhVNjDAkJx4NpDcr6Z2BdTtiSbY2ks1oQzShYGfrZ5XYj7zOYDXj9w2TwIWCpl_GwUEedWXFzCW4ZnwaW5SXsHuGnw6tw6p7r42G4BV8eXzF013FWNOISgeeonSZxlz0bnKI_DEvsgL-rCiKfz83frnx3XdZ3uv_TrIYlMYpYI4e2DfQSJ9I9fBQb23BLeP5ix1lUNJSCpwYEBTPdc9YMXOXDhgcxjP8r4M1P3yidrqaC71gCJXv1gQAug-s75UNVXDZxQZUB3EA14_YdwkiWx5tx_ZmpJSDkiKOMerSkSQwgFyvOqvXS6EBXWoVYUlDbYza3W5Q6ftJfNAWqTULPUj9UzU_tuuzY81ZXYkpxaqLm2jFyrC2tBzXkcMkXNySEIUkqI4EYk8XQaz8_Pm8vv1msEd9ASosKxem4IOrYLLOmX5eqH5rs1vj8SKfDWvglSLJGen_2VGLnhRQ0-qrV028rFPx3zOEVJdetU2sgnIKw5yMs81mCmH_6VeLlBQACKB1Lu41qYKZnr8LnJeYnvNGT0elx3umwNvS4rqA05O7VCjATlvtzCI0bwgf8CRQ8wL-NZrAIv2KM2JsNdSje3hn8HTNYAZLMVSTtogg8n1D1A-RnLHArwExn5iWDPTuGpf3waOKstlAQKjThbGXSEK9lWV2q9dL5QuCDlnIYLI6-NMn4mmF_KAxzVUmqfa__Z6e1MNi1aV2Wp6mPj_LjjA1Lqc8iA3pJbfBo6H4r2stq2ziEJ0IkGe_3o-ek9DEa3iO9hyXzrgILJSERc5vuWPVkipoH5gH5ovipKsiNEKKKxYuV0x8DDe0T2M5Y5JLJhFsRppJ-dQrKY-_5RgyUhlFdKbYzJJ0HetrD7atylUebSPy0CIoLvmWv57PT6SwDeGh5nCftYuqReLmBLbgVgvixdgjS7qHXzDBLiUQ338UAeR0chD72UPzu9b2wOFzy-qOEZ2UiCAkx-zYvSeEqI4xHCkCOynGYsZXUIZBXzlBcne_SmS8RgK0RAhmKb8JRKPChJd9-7B9N00ve05s9DCy745QY3SrkDyOaYtVvArl_AStngvovdhsQapcnqAxfMvTj081w9D5GvvAWkQPG129bwKrtMAt5amHjlgkyvq_m2bKcfvUmP3_jBoTRdkvmRCPc5mRGRVsSVc83LwkrRPff56bcO3GSk4liJlD11_y_ranXj9siPIPeWakd42B5yv_zMz3JPxE8lozMXmx1M1jp03BXUjrKlMBt9DcxxG-taO-71vmFpD9iLlOchV5l6KoHvK5tyrK3Lf031tp1hnDL54_0slwXdVpW7Q8yLdSSzOEqfiXkXcJ9FSZ7MHcW7S0MfL7ofXOBZs6Q3DvAuCEQQRzd868fwDlzq-GP4VggLrpQHtYGorR3aqPVSiStyW9oKvsDhTHme5eJGGO17S-ct5SGwfWu3adpqc1_d45NvHVDBPA4DLVP51P1NuqYiaNoUDe6gAbCtgGotSZAxNmBMl0EePaaFCRtusuf7RV_VPAKrCRzPBIIXWx40n_S1RnWWxRmPuO_lKucijwIditDTOYkjogmzZld4dbrCq72cTQXgNHXk2uxExcP-N6odfk8V27IQu8kK0yruZBFTH35kgbepdHsGB-OCeF10deQm908ynbAkZCpMEya5ztIkyGMWSS4TPA5kmIowYkGWRKmneQiDKL00yINQBmkgYxJ3queZerC9rRPGfgGjqeSKaCl2vdQNgvd-eBJ5J2HwT5534nl4q-M4qZISeUgZ0V8mT3_6H6weG5m1hV3Ku5sUcyayPOHcj4h2s8ak1tuJ89PKtN1WEYM_HGsvZirpt5pUbvutHlSN7akXCRc8yZlkeqB-LNB2Sz6l6DpYw2_fOb8Kgj1_z0RY-664NVWm_tB0DuLb1qgrfBYKzymHUJLrs-GFhL5LVWJraI4zKSCRAGy5dUGMCKx4fYU3G7gnprzYh14WESZUFivjiDXW2abNmsr4SnjJbkbeTlkWF_T68g5Y7TgbMh0xnXH8L-w5O6kyj5f12bXiboNcRYHH81xngeg3mJSPuw2eUgSWWkkdxSEcySRTMY_y3Idoc4-f4-7h73RX-t3anTLf2u5x0SRXzJdRomXEY5UleaQDFnMvyFQK0EhD6WUCBrxb9PwzrO75dO--5nbinFN9o7FBPjhLP61WqhYFwidgt6xqV2xhTvDseMUbyJ_bqPq6EKpx-QWkegUIdjeEH1V1ZfL5pZGm40ldz-494a711fdqrisjtOc8UpHCf0I_YYLgJEsDxcM4AkYoHcYBz5JQqOj8BeQRCmaL4WNCyvaTOOdjL85yszsnkZw8Outlmj5b3hEXdHKTAMlCISQLTF7fyM2kpt_JzVMr82Rk76otH9AYAcnKslQnio0aM1bxR415jvJ7t2ccSz_LNHTUxElmz0lFfsC_x5fS20NVIitV7rD28ZuX737_-l_PTr_53btXr8--fvnbt1--Pn2__AEgdD6cOqcqhInMu-qslWklDzBXJZ4OA-HD_LP-oJNSfnfQp9Tg3756_dvT1-cL5zdQetjJ3DlXHvNYEMdZ7AVBiOg9hbOgk1SyxBNMJ4FQgfSCBC_5Cy-OITgt3V5XJXfOgW1xkMhA5Qo-hvDgRoS5n_h5IBN4L5EKUp6lUnrS4wwKpqI0yEKfBSzM8zDPsLCoNru6uLhsnf_6T4e8jp6LL992Fc_OsFG0Vrd7UdsKrieuhRtxGrSx0hpRFB-Ck85UAG1EuTUdgzwnx1tWH9YdosPQHbgb7SUqAwZG8K_6u5m0LXR385R-gxuFv5Np_c-ApZUwPA6iReql-OFcQRFDlcVp5nuRl2oJnoY68xIvzaWIhfT8UAciF2mYIDIMfD-JcE8R7oaFGRPn3fKyElvC0-aYw3Vvq5K7OdhEVQAIfqNcQslyqVYl7Z8sWOjT9mQchPbTLMhZqCWPfJhSqGbI84QppuJURSzDZqGHz_woZX4WpQpPYw-uKru9fW8OAAGu7fCjlMWKt3Xx0b1mbrD8WDYfiQifLULLBM2SKE7h4MssCuLEi-AchYBuSKT2fBYjrEtCD1Y9TWKGByxQaSrSDBKZszRXt6mQcF9cIMi6WhWicZstYrd6N27tLwBItDV21LDHSSJ9j2QfvrcXylRpctaUhuGEVfZhQEPYVaB5wDzgm5_ITGhEnMldWzfFxZqCGJdqmqolKXfJPrgNggm5LZXLlvi-oYSxBfx_oiTOw0zDrchj3wt1mHkRZ3GWJCmHyuE_CHZi3w8iwSKRsYiBSxw3o2IRiQjcuE2J-mhU5Vq5a3VRtYWFwVLBetQjAdECQT0RwDOWUXY1xIYBZ9hNMEVBaxLCpchFlIeBr-CmSI-JXHoQQ51HJCoijYLb25fbFUHoFTU-UEJTwuoDo3eEy8P2SbhI0siKIkKnTIICeEEx91WCm6cwSMgkzhlnSnpxlOUaSgsZ9aOY4VetNbypWKd3aML01F178SAJw_7eIowC2j9IwdLA1ywNdZRxlQIqhPITkTIIvUyAoV7spZAPL_YRjcZ-KmKlEuVDGT3u394fgV6zMlYIVoOCRfc6HDZO40Uam42xGwvTHOEclkSEwDiJImPcg5T50Hot4HCCOI7wKIM-Qj0E9yRENNCK38H5tuHV1PJRyoI6jvYwwA8WUWY4r7kKSLKFzyBuMgENXDDSgojlKfTSD8KUSaU87UMWYw_GJYpEyplIiA23CfhwWbS6UCWuvIbMQ_xNUp2af5uGvtITEXiL1DeKiFAw8BKRw0fANfCUfDagM6J8RLoU-MKjikETlA6yBzXAdzRgycPNQEU9rHZXj0UH_mns50qkCqKcTbyevgVs4oE8tndLmBzIVvSeGfy5hoqmXVRDziM5v_jNlj46-0hGpiETiZ_J0Wh2a3xOjs5KkUMK9EIstNm2tkJgSoC0XU4J5UbURY79eNMv13dIHXIAOaVQ_DCJgmAIRsfustEBfEJnWO8EAz1igLqcRGeTZrHR5D660Wt3q9nmZuPNKdm50w6BHItAztenL184-zbC6ZDhhXMnbDoWNmlnUEjKDGe82ZKDcFE09pNTTqWsosYVddVZS0FgeoaABbSv02GBcx2-cO5AqJGOXw-GxNyDNSRwT6wNcRhW_d1Gms-n61A-4kFkhfjsZecsOHvOgmOA4oXzL70aOy-NGnc-2KjGL0DZYO6dl725d7425t65Zks6-3teXygis1ZjCtbWZgeMsrHyz86X0JPLnk76ytgFlNsady9-9hDEhfeAO-c23NlTGCdr_IybEhAufqVW1QDGlkV7W5ui9CFISXKR8yxIhZeNSZ2xt3ACKY_tC6TgZ1C8SQg8zcJBWlsEDD1D-2B4OKZJpR2MWSJ4MXAAk8AzdJtzTNoORzx4XN9gtwuHLY0lbJuK_TEyGloJJ9x6bC_grSivZ507JdbtiO2Dvdc0r-QUrVpBvsrqgwmxuxcXFgokzmsTMWNODTELrYJQuJAIi-3nXT9b3UXGHesRsa-JG867AohZy-P3COZ2ww0duJkY5srLZazgDPQ8m7Q13oLPx_QlGnh8Z2LtSX2o7oF4qBBB1W1EblP8zXZDcRx9o4fWXm6bFxQ6y3GNAWKP28KYQ2sqIactvmtyhtOqtQCyU0WC1-3ueIggHModNwMvERESHrWwkM7FVpluo-UEbk9NxqRD3euQ1LnawHhQKPeiy2ToHRX2cTYE9h2Y71fjtzUVCaYHo6E27LQtABRT42BzwFYK-osdGNZ3N3YA3gcBZo9Tc-Qq77uj-i4Y22NIJx04sJzC9mZTdtmfgUE2xKI4dYKqYy_BPvE93JNfgjibElqLHt0lpeisCI9nsSkocK_cjTCO7RGli04MzK-tuRU6MKxG35KDvSvjtRRrCuptn8Wrr785_s2r_gA_GnqXE1Tve--2a5uYkyOOJoE7dmF0WWhw1kgmbITtfTSbEMp38jg-7O0DnXCQCmOPBa_rW1Jx3Kf8JtJojtsM17VdN1xbpOIX5iQvukyH86cteEVJM_PKwggFYc4CwlY2hP7VxjJbVKDpRicMFWWXB80Q_PFICIQSUThURiYNxSN8P6UXuNuLxbmMVA5PWg9JzUl7cLfXUzp7ZaW15RSoDcZ1KGXlWrUln7zZ5oQ75t6MBw33Ydvc0RlAXve6HR2OvYouhBckcUrmkgNu5WcC8q-CsYt3knclMzQmhI_7cqBLwlN0zWHmxc7GHDC9TIg40VkWBQPATxqYJ0bxsb3Hi7FcrTpJNBqijNmjtCKBxI4Ek67JpCIn9Qsscdwnt8YeTtMxg1UEASVuC5awdbrTO1fKKFD1gTIeVtxXCF-IALMn6SLEatFdvaXZFC4nub2mexE-pvUWR0tr7bc1ByZTPpUF6zuDOQeYzmIdMT_RLFOjwox92P2o5HO0UHc70kS1VLmXaz4En5Ou6m7H52mI7iUrzH2udBKpZChiTnqkbxzyqe3NfZDt-X6eMYDB6BFPOp5vnPOhzcp9DZV5WZAnQvp8ONGkf7lb_Cmtx65lsWMrrQc9Zkn5jyBLxwh60pw8Qu7Tuoq73YihSipP-MEAupNG4263p3QIw-kryBWj5_BQjV9g-zCsIzQFHQ7h_4DIatNOYPwF5f-LrpRslunqGtLWitx-UL2HK7KOq6o3EB0tk-Wg0FQk4B19ZGapEFRo46vAr3v7a5sOATdXACq1vi7qam1D0imw_KYABtn1YfLkBXWimNQM_IdNS6C3Joe9K2JbiDGhIRnoioJe09hS4TUE7VcWcDbK1DhNfaCzVafhMZyWgf2m3t2Q4yv3r-GA8mRZnqZaRyocwrBJf3avPE9orO7N8FDB7KOpe5qczx3jsTTgtlEtoD-vyx1B9NZESdx4V0Ut3e6sGr48hWc3doC6r-9ad7h4CtmELfIa80L3aevnVZ1b-Ld5NexhGX8AdFPlB6EX5FDUgZ9j__jDQPdw4_cnznUPkDHOEkTDHjy24aInfeIjejytwbsXK61y-mMVcN34gB5jz_fExXhss3arDpiEKOZRnCZKSz4Y20kL9zjX_uje6y7q2o8UukTLEBq8-G4dLO_w0s2iRpLokhvKmFF6sI-Y8Vq4dIwQUPTUB4JTJ36a0rKaMLr1Pccag0nfrdnSoZo-dgAIbWvr5XCJfww44F-KtgqDyxU5TxNflraj6130iEy7up0BhZvZHOhFkImIoyTxPBUMpnPSl95XpZ_QUN7bVZBDAFmstnRQcyk3r2K51wdk3yPNsWlsmOOuN8joPoJZG5RereFQEn4vHFkjyjQwVFMShhY2zmvXeuL8sJUX9PLC-IjweYEZiNsWXaTZXBaIt8Zehr34c_HZDUgqTtKUanSZGvqDJj30ozY_og--L1yzQHqcw_Hxk7EFaWiNH3Xo0e3tnTuE91bwBTZlIYoWd2yUpl90_3smk92Xw8eujaVRmCkdp_5f_vxvp5OiwSTBaTIMiLU3d2YVeyVcGsXp10Rwuba-N6Fysd52uSEgUjsAZG_pDvp3360REX_ZtQV2egeZgs6aKL2pymvVtb4tJh1qioJGCFcLH4hSB7Bzx42iDIhNidkwE8KujF5XZdN5HBvzmrGV4AUlEHfHJuTv9ItOQDyPSUPUkL-HTrXFauw0puXwO37CYi1RQRbIaAI-yiH8qjXAsoED1yz6aoYJoTrYmIAVYZ8BfEr8AIF3wMADSKI4S2UWwFyJAc4nAxB9AuAJQwz4f7xwoMsX1HKxqcrqYtd7GIoSP4Qxm6I0XjypE4Fsg7ubANIhr8DLBIt8Qe1wQx1wHI4Y1fWzxhx6RdXCg8eWBpzJfvHJ5EO3-CNnGPo8OoBFZDJRPB5SBpOxhn235pEDCsapQXxmPRpyaARJyv0twDaqE8UY3Rmp_Yyg9m_piPEkFDzUKtKxGHtHhwGM3jV6xlGKPqJLEqlFIryMDRHdZLpi_w4fNydxbFI3bTX9wK7lvrrzw3GSwXXhCSJ4dh7aUdrdmg2pmmNzIa7lk9vtYLlj7utuyg6H_n6aygQgw_hwUZNpj4kP-9i5ja7bzt5o11HbWyffHw2dzTXinRVvwSG8U9RkMW0OvM-UWfQ_gEI-TyIIgRA6TMZuhGE-ZNK1_DmTHr3HD2wIgpRlqRZjFmYY_phW2h45xgEbavJDC5PlH7MbhqkwMzciCVMZsPHEvjmyt2KM5tjsYC2CImfQdlIpOWmPIG_R-me2zbxZ3BUzjI3pzZ4TDdsNqRC7IQReUJthYdzGaWs10WqTi3veIV28iVCtq9I1yVNb_O3L_v4XupI7_mYfvJv2E3-xz_wZQDI4n_r44N_7s3_V0HjS3efW_emf1s4_9F6vYWPn88h__Hv8U4HUx9He_5cCj0aK3UvmbshFcH-Ei-BaR8Ta9E_9LcHA14F3Y2LrwX9Cz37R9vuM7a8rvuuc_4X1wdXCetaUrrK52Hqq38OclAn6P0nfDSq6gahXJSccVNKqchd0dIMkRIkt791JStdzlJsO2y6865VBWcEffLelpbDn0U9HHy53w_YdjtQDO7CHoYR-ngSR3YYP2ewzpsZ4nlBLrQjhIgWx1DyjoSlj3y2TpuNg01Go6YjYT__7xePhw3I3h8X8X-4eBbtvLu5Zht9AVRyQuUoixNA6jLOQZdoPck8nEo6G76tMpHkAjz2mEQWe-kJyKXgSp3nC4k-c567Zt-iEeXfMvsUZdVNkYp59m2ff_s5m3-ATBzqT1DIdjg1oAyjtIdLjgKZLyhAwv3CKB1mCeVJvntSbJ_XmSb15Um-e1Jsn9eZJvXlSb57Umyf15km9eVJvntSbJ_XmSb15Um-e1Jsn9eZJvXlSb57Umyf15km9eVJvntSbJ_XmSb15Um-e1Jsn9eZJvXlSb57Umyf15km9eVJvntSbJ_XmSb15Um-e1Jsn9eZJvXlSb57U-787qWcLje95mVftzXG8v8tJOwsj7uhEgB21Te59atxu0uE5zlM9tLV5HLWCzJmZt1uFmLuH6Ca73l6gn6OztCvr2VB4iaNOUKQvZHUtwPc2840dwbYMSWHPWpj2kDhwqfSMC4XdN-hEokyLgzhFNVUcv-xxk15gkxcmHdfu0HFtVvnUiJ49mdlgJGI84T7vieP3kNOxAAd0zQHtEUwCkF_ZOGNvGskZgvnW5g4LSibe2Sf_WWN_OvF0oKI8Dz1fZXkSsTBRcfSpsb9hCuz-sb-_gZg-fIZxGH4blrsxzzeOt_1N5vnSxI8CCdxhcKQD4FKoMh74LApDzvEs9r0YfjFPmYdPchYEMhcqCZkMY-WbWsQnjnRrpC86CbwT5t8x0hewBIFPrD490jdP683TevO03jytN0_rzdN687TePK03T-s9YVovgFFIdRZpHrJ5Wm-e1pun9T57Wm-e15vn9eZ5vXleb57Xm-f15nm9eV5vnteb5_Xmeb15Xm-e15vn9eZ5vXleb57Xm-f15nm9eV5vnteb5_Xmeb15Xm-e15vn9eZ5vXleb57Xm-f15nm9eV5vnteb5_Xmeb15Xu__y7ze97_8N6xoDMg)

[//]: # (ob:168bc323)
# Governed Workflow v10: Private Legal Evaluation Decision

[//]: # (ob:a46dfb2b)
## Decision boundary

[//]: # (ob:a0c8368a)
This memo records a private, staged, model-adjudicated evaluation. The evaluated graphs are non-authoritative fixtures. Candidate claims, critic verdicts, silver locators, executor outputs, and evaluation scores are not lawyer admissions or matter authority. Licensed corpus content, quotations, prompts, trees, credentials, and private paths are excluded from this artifact.

[//]: # (ob:cfb573f0)
## Product decisions

[//]: # (ob:bb53029e)
| Product question | Decision | Evidence-bound reason |
| --- | --- | --- |
| Replace PR36 v7 claim construction with v10.1 | Do not promote | v10.1 materially reduced unsupported factual claims and improved honest gaps, but supported factual claim coverage fell materially. The preregistered construction gate stopped the full 12-task Legal E2E panel. |
| Make progressive disclosure the default agent-facing matter-context API | Promote | The 24-case deterministic safety panel passed all cases with zero blocked leakage, automatic admission, or unauthorized mutation. The 12-ask workflow panel completed every cell and graph-only context was the strongest tested graph treatment. |
| Ship the post-disclosure assimilation gate | Promote | Recommendation accuracy, dry-run immutability, valid submit state, stale-head rejection, duplicate rejection, and idempotency all passed the deterministic panel. Submission still creates only imported evidence or unresolved candidates and never admission. |
| Make PageIndex the default gap retriever | Do not promote | PageIndex and the hierarchical prior added no coverage at five over global BM25, recovered no global-BM25 misses, had no unique correct evidence at five, exceeded the latency threshold, and had incomplete cost telemetry. |
| Default gap retriever | Global BM25 | It matched or exceeded the hierarchical candidates in the frozen component panel and avoided PageIndex latency and telemetry failures. |

[//]: # (ob:c9c38e76)
## Claim-construction result

[//]: # (ob:0877724b)
The paired 12-task majority adjudication produced the following post-output metrics:

[//]: # (ob:69377aad)
| Metric | PR36 v7 | v10.1 |
| --- | ---: | ---: |
| Requirement recall | 100.00% | 100.00% |
| Unsupported factual claim rate | 29.94% | 13.15% |
| Honest-gap recall | 70.70% | 82.89% |
| Supported factual claim coverage | 82.18% | 43.44% |

[//]: # (ob:a4b0fec1)
The unsupported-rate and honest-gap improvements are meaningful, but they do not compensate for the supported-coverage loss. Development ablations did not identify a promotable repair:

[//]: # (ob:cd607272)
- multi-query RRF with a larger section set increased noise and reduced blinded supported coverage;
- a task-wide BM25 safety lane did not recover coverage;
- frozen v7 decomposition plus type-only normalization and the evidence-first pipeline still lost requirement and supported coverage;
- the loss is concentrated before or at claimability, not primarily in the layered critic.

[//]: # (ob:3ce974eb)
The full PR36-style 12-task Legal E2E panel was therefore not run. This is a preregistered safety stop, not missing data represented as a score.

[//]: # (ob:edc06532)
## Progressive-disclosure workflow result

[//]: # (ob:508131fc)
The frozen panel contained 12 lawyer-style asks across graph-covered, relation-dependent, partial-gap, and novel categories. It ran four conditions with two executors, producing 16 of 16 scored cells and zero inconclusives. Every model call had a terminal receipt. Total model cost was `$1.9346`; the diagnostic PageIndex call cost `$0.0022`.

[//]: # (ob:b42b3adc)
| Context condition | DeepSeek rubric | Ling rubric | Context upper bound |
| --- | ---: | ---: | ---: |
| PR36 v7 prefetched context | 24.60% | 23.81% | 20,255 tokens |
| Claim graph only | 29.37% | 25.66% | 18,063 tokens |
| Graph plus global BM25 | 25.13% | 15.87% | 23,998 tokens |
| Graph plus hierarchical hybrid | 24.60% | 15.87% | 23,976 tokens |

[//]: # (ob:25411a7d)
Graph-only context produced zero unsupported-claim, citation, and authority errors for both executors. Adding retrieval increased context and did not improve rubric performance. This panel supports progressive disclosure as the agent-facing API, but it does not support unconditional retrieval for every free-form ask: covered questions should remain graph-only, and retrieval should remain gap-triggered.

[//]: # (ob:f8934a39)
## PageIndex result

[//]: # (ob:475d6c05)
On nine tasks with frozen gaps, evidence-set coverage at five was 80.56% for global BM25, 68.52% for PageIndex tree retrieval, and 80.56% for the PageIndex-prior BM25 candidate. The prior-minus-BM25 paired mean was zero with a `[0, 0]` bootstrap interval. PageIndex contributed zero unique correct evidence at five and recovered zero of thirteen global-BM25 misses. Warm-query p95 was 82.16 seconds, and seven calls lacked cost telemetry.

[//]: # (ob:f10cdad5)
PageIndex remains a diagnostic adapter. Its top-down document/section routing is architecturally distinct from bottom-up BM25 span search, but this panel did not demonstrate incremental product value.

[//]: # (ob:dcf77705)
## Default model roles

[//]: # (ob:64858abf)
The frozen, qualified development route remains:

[//]: # (ob:d9eeebd3)
| Workflow role | Route | Boundary |
| --- | --- | --- |
| Requirement decomposition | Qwen 3.8 27B, high reasoning | Candidate requirements only; no rubric, gold, or silver input |
| Evidence-atom extraction | DeepSeek V4 Flash, batch size four | Exact source-bound atoms only |
| Evidence-to-claim proposal | DeepSeek V4 Flash | Unresolved candidates only |
| Layered evidence critic | GPT-5.6 Sol | Verdict reference, not admission authority |
| Primary workflow executor | DeepSeek V4 Flash | Cross-model primary |
| Sensitivity executor | Ling 3.0 Flash Fin, high reasoning | Sensitivity result only |
| Native artifact grader | Gemini 3.1 Pro | Blind post-output grader |

[//]: # (ob:a4058ae4)
All model calls use fixed providers through the Proofpress development AI Gateway with fallback forbidden. Missing terminal model, provider, fallback, usage, or cost telemetry remains inconclusive.

[//]: # (ob:d4006a73)
## Preserved architecture

[//]: # (ob:a721d6d1)
The product architecture remains domain-neutral at its core:

[//]: # (ob:d9def285)
```text
source corpus
→ evidence substrate
→ requirements
→ evidence atoms
→ deterministic claimability
→ unresolved candidate claims
→ evaluate / policy judge / authorized human review
→ admitted claim graph
→ claim-bounded progressive disclosure
→ gap-triggered retrieval
→ executor synthesis
→ explicit post-disclosure assimilation
```

[//]: # (ob:baa3e879)
The Legal profile supplies lifecycle categories, legal claim taxonomy, conflict/version rules, and lawyer admission policy. Retrieval receipts and valid evidence atoms never grant authority. `disclose` remains read-only; `assimilate --submit` remains explicit, authorized, stale-head protected, idempotent, and unable to admit a claim.

[//]: # (ob:6b806606)
## Result provenance

[//]: # (ob:0f0187ce)
The machine-readable decision report binds the frozen construction-majority, supported-coverage, hierarchical-retrieval, disclosure-conformance, and lawyer-workflow reports by SHA-256 digest. This Markdown memo contains only sanitized aggregates and product decisions; private raw artifacts remain in the authorized evaluation workspace and are not embedded in the portable capsule.

[//]: # (ob:fdff801c)
## Next construction experiment

[//]: # (ob:0fece524)
Future construction work should target evidence sufficiency and claimability coverage while retaining the v10 safety gains. It should not relax the human-admission boundary, remove honest gaps, or use PageIndex in primary claim construction. Any new route must qualify on a frozen development split before another formal or E2E panel is started.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzZhZDMzM2RlNDQzZjM5MGM5MjBhNzNkNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjZiY2Q4MzcxIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV82MzBmYTcwYzI0YzkxN2VlNDEyMGQ4OGUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzY3MjYzNmJlZWNhMTNjMzE1ZWU3Y2ExNiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXNl228aW_ZVaurefmqQxD8qTEzu5Xh0naTudPCReUgFVIBGDAC4GSYzl1_6A_sT-kt6nqjBQpmhF8lp9H_gik0ANp06dYZ-B_nDGmy7PeNpd5OLs_KyuLwIuXNcV0vPczI2tNHYsHrrCO1ucJZXYXYh8LdsOY9sNd_zgPA1DK8jsjIdeENsOTx3bt1LLF3bmJ06QpFwklsyyKJNYKcvS0LJ8xw5iz44C27GwrsjbtLqSze7s_AN96S46vsYOBe9oqwU-JLLAg19kk2c5TwrJGnmVt3lVsg3GV82OJTv2U1NVWd3ItsWcmqfv-VrSofYeN9UfEsftG1pw03V1e_7s2TrvNn2ySqvts3Qjy21erjteriPXerY3u5H_7HN8vuhb2VykVdnKErzoml5-XJxtJCcm4swickP7TD-5kFdqEJgrLwLXAqes1PHS2A6l9MABEUWSKKuajo52UeSlBOXDjRQXQegEbpBImXLbTV3blzLEx0Afx1B3kfK67Qsc2CE606oR7dn5bx_OzPYfznDLVdPSJ_1aiosELP_trC_fl9V1efYOZxjkgS6460Uu22e8ljdLEFR2S3nFi2ff_fjLyzc_vHxx8euPb_7j2-9__PXiF9u6ePHym1dvX_34w2orzhZ_Sax41zV50ne4zYuEt3lLe8siu-AtuNxJtV7fbaqGaH-fl7Rku2s7ucWbkm_pkoczLDC1JcE4Oy_7osCJ0g1uUmpeJEWVvsdoO4iS1HVcDMcldvKGzvsdyWApBfu1at5nRXXNrmzrHFKVX0EQ2fdyzQv28opjkiGCC6Goq0ka5TWe_I09dJWi53Ri9kKmSpCxTLer6SgkNBDAs4-LiWDuBSJLnGSP4GEqS6q-FBz6c4yyv7FD44_taaWRG0T88Xv-DOVkW7mtmBFIxlmtGbFgLZRcigXbVkIWSy7-gLSleCMYSVk_0Vbzhu8RlmaJH7qZtUcYlF_0aceEIbD9DDMOjT_CjCTxXcuJ5eP3vB23_GcPs0Y8vJ2u5BYykQtZpnKpOAuO8Zae_17esuVyIk7ZiH12xKkbyTDYI-2bgufbJVkoGKdU7QYr0RfdZ9hybN4R9lhRGIaOlzydhp83ktUcRlYw21l2vH3PtvyPqsm7HRuFhJaqFTcxrMOMrCqgakdkJojdMORcPJ3AW_ZawmCluLKf3rgBuwrxCTq-sofLWjL193z8hx6_0a7j2EVyL7Eymdpfhol92fY1ORUplg2ZHg6p2lQlZG-55jXLt-DgldzCrkMvGwlF5SXd6xHFE4EVOqHzdAKXbIsR-RKqAN_95s237BouGOah4M1aNqyVeqVWdiwvU1IG3HRZ5a1kE4EFfP8egW4q49CTX0gMMzgQdcfLttsBcwzyaGy48xKCWsqCXfOWhLCRWQU2ltURDkqRWoHvOnfNyJpceH4ll4SFiqrtsdD14EAepLgPXuSIFvtWZLt2ln5h6hQvm-pPWRqG0eI8L5WK48avd7IxLAZ7IYxpU7UtWze83hzhZeI5icvFl6b2ln2jVyMyRT4aalm_lfI9a_pEK__34N70Tc85pt2O79k2D8UXJvc74tKyKosdM8tOlvFP2VR7diAlVViwNO-UDT3C3CyKXY-78T618NivSiFvHiiSnw4_Inxe6IsAgcOjd_yxZLBfknVKiJQ9MVIHc9cuACuMgyWjogIOLM54x7L86hgnbCsVXDyervnYLcSeUJDI-bqsgAJSODVed7JZsVeww11VLwVwLBNV2sM0H6FLpBl87h1-vZAZBzkaVLGmKmT7WVB4aMaRewq8yI94kj1l38kiLICGeIGoDuIqEKoUVU0eCUv0nRwYdn6MDbGUMhHuU8i5ncA6jYU6v1Hb37KvDcq949qHv8qxH3fpFpglvadQ9xxeSA9NeVG0DLEnRPYGDCMHDpluyP2AYeuNwkJTGMzEMcZ5lhUgBrtjjyRiriuszZt0k3dww70CLcddzz2TjgUXoWOLQNhP3F2hRQOr53NGVRMV_bssZd81cNrQ9hxqhmBEHhcqITMn8p9I3eXlJc39vWyrvkklbVv37e_l__73_4zWiLV9AmACgKafmxSDgmX6yURnCinYd4GcuzIK4y_ARQ1qwMssL4ioui4Q_DOopkx3KR5RbLYGDpcwpYUarLzJMcspsiyy7H0H_YPxrBMYkze1bHI68Gfk7DNTj4UnOIT0He-LUPJtryRsbyY5bNZuqr5APEIQtptfcJblaY7PO3aXW-8WQ37mDP6IIsELArs66aHeDBkUeRGncSgsjydpJNM4iZ0wEq4TkAqVVafWNCkkZlJILN3I9H1d5epA2FHtRHmR4RulRd5R7qnI091shXk-araIynQ9MlXVVll3keFmZFM3ucmItYl9HnKZeFmcCDsJUztK7CgWkZekmZXYQeTEiRfFDk99KYRjxW6cuZYXRQHmhKHrBQT2W-AZldnSt3XuRB_BaEokOZYTLK1o6cQ_2965ZZ973r9b1rlFyQPDcbpkx0-4I0MIzfT0w_9HMkxJrE5WbXi70UGXF6WW7WXKHqk1ZvkrI8xfOvFkNldpJ25ndqLCUrX5LBc1bP7g3JJZ1rJwt0kUSpx9XHZKN5lln5I-UmdcMbJs5jveqIhCB7tlVS51UlFh4SvlUkmv2xX7BpFyLohpysLB3qUYBagGBmOTDg_avMAXhsvilFQFuLyRaY-PDMCh7mkIhdsTKawlnzPs3ZmoB-Bvm6t0Zcswd8u7jh4aunYrBBmpLCn01a5DQ_yyI9RUaQyPnWC0tzVt2TVSKmolLE-X88KQYZiG6Kszx5c3adFDVQiFbYEacnqspXR1wKIPophJN7Fl6EsleuraZsm4SRoemFwzy3JuRb7tB7btimHZWb7NLPuk_Nkh3CbrgsM8D0kcddd3rDrFECa1w15U6uKI2ZXChvoF7gw-A8Bshy112DWLuBhxtB98ZatuwyRehmSMiU6SvmP3TJuClUwSFhx31PINz9TIdd7iqRKU2QHWdOstgop6yJNRSuOePMZK8-U1f68w1RCXsllcSksIg161EQShFAdryV0OEejzn14xdV-GVUSm4y1T3tJ8jNzmZa6in5ZnstuZvEBNGX_AloKgbitNEKeiWGUX8a6QnMo6C1ISQDsdQBkdWpAO9aVRnz8xett3M0OAc9Oxx-B6SEZs60Jqw0HJqJR4TPe0_jSyNpkesLSpqKjQMapQDZaF9I93BB8MK99u8lqNrxHqzeN7nDPf5gWfLmnOrTewdlssI_R7nqZ9w9Pdgolmt2z6EhJEB0vyAjZiwWBjckEwcpt3ZBaNdSzkknQNUvmHTqZhfg9QR0Zy_lCJpJDbGpsTRCHum4vQ1z2_LiMob2kzxXPslNN1KdACI0bcgoBrKR4hkLoXyFNVkNyng33V-lAS36dbnIvhFDrPJY-ylw3lYNXEA5o5TaP1aeomhwIRGk4VyM0r2lColOLdVACopWXXRZVg7NevHX-h_M-VUi-M12-W9IYRzWRyN1y96sscxomMNWbMIKBZmdxEKqUwrKX6JnEcwZsEdiyEvgxaKy8HscRiSswKhARdszPceXEPK76bqMa3Vx0pJvCboBvY23uPIbMLyUttJ3TihIiAkUI8rnWFyONXVU6rTEwezqGYPRAKE5YX2p_eHoqQR5cSeUK6Xog4eXQpU0Fjcil_sTBhlo88K_GkxWPfD4flZ7WKEWg8vuZA1k-pt3b8bKuKAwdTFiOmij3fSr3Aj0bwMytPjO7uKWUGnUORlDDAa9uyVpb1b_NPNPa_7vNTrNEmyYlXsaemuSvbN7P-MZUQxg1CaxWq9SNnFcVm4NvPeTM13I5onueuPNrpiKRASISHiCKOFEY0UHSsmMyu8rGVDzhH7YdxuzsmtFUhFQAEo2UyKJGy_lM-dTgK7DoE_cUsgQXyNT6D_xRqpVyBsmynUCyZKtPIQJJ3TFzixJdJliSIf0YNmQox5txPKahwBZe0YCcI6Ui7J8kYzvjV7-US65F2LK9xFm1kjP8uYB7GgxpruT_TWBSIsZDKrLQ6tV4XgLV0dO1py6rZwp_9aVyfMd9j6jbLG1jDOq8lhZ7G-RRkIWd5EzXtngMou0vVhVyBaaBrlXvBwXX1hhxDpwV1dLDaueBBk5N3K43x3mm8pUKD1YGilLk_N_N824ntKE3T4f5mdaqZ3D623oTD9wri5OpY_A4iNFdEMFCfRTlamC1YfE7yR_miknjAabIKVI4EARF3hZ-5WeaI0aTOylp7QcCjK1JDZBCl0ndFKqPIG_aaFanmvHtkfWlpHDv5eK2wSyGh8EJFWTUFRfD1sBraN5cYXcxSYZS1h7UsYRv6ZioYGeTaXVdjYKjjNCgZcd4OWJXRX8VsoTCnBkMK7JL3LxGgEeuwxUuFS6cUsEII0ESFyyAZ0DeZ1wCdP8OmjLliUgqSlMu_26vY9YLLrzSImioPkwdXq6oZl38nB-E4l0ckwBVhlGVWnITJmBSYFeNGB_b4OlrHoL2wIDqUu8_fzdze4CIhyxB2hXgGzA435q0C5Z0cdxXZ6oO1cHyfddV7mHa9gsIXBscrS6Tcnxuq4f4qCJQfjBZW4O7NU_U3bcXWe-ALk2xXTfJXkV7GXcRxdN_sPUS22YEfYk773iphMK5yxGPaoZOlsSXc1B7D9VkVcmh7ekIBUSvFmK9gsmkg6cpRJhUUYBT-FXsuhLpoDVZxxMkLDdvSWqOz1D56EAwIQ0aeAQbbGDqt6Yay9r6A1cRre7EqglPt5hEuiQqYl_YzC-Gwo7QqzRqopSPp-DBrJPwQiCFjcs6GwGBISrRDGlhXIGZR5MI42mHJO-N4vcSb9ZpWO6J8np0ktrQkQMEIB2bF2pn5fVD11awqrEgIwGQulRFXq84KsmbVp1RYpTJGkbXyoUnEzb0AK4hWvqOfz2I-cHril2bfbAFV6xoGL3VQp3RvDGeG_AjeLGEq-1YHbQbqE-pTRCkpN3Dp8jdrwax3l5DfqqO6DOAipLMBAau5wYTIqqbFSUmORn7m6gdhUVPgAbpNDrUi_n0SU67Yr7zZGjxXx75mH_ByQFgOMmpyey1VCUxlsOAqR3InYrxflhzfcmwnTawkGg3ErNx9oNb9V-vX3bMBeFJBl7RPZRrHspTKm1HLL6xBp5ORMBxdtV32tQGYUHQckuYM4HzU_sFYCLlVcSGBdGVWaGddzVIJQ8rCHoU0ic2tJHSlkyQDH2bl9XmW-4HF8kFZHfhIJ3a8zB_ValY__wS_PLoaPl5o6gknEa7kwXiQqUA-euanlLtnOHsfyd-y_7yGKMLHMif8egGHtt6YNCxd_O0srz4vcipv-xVlT7StX7C1SoVAm02WPS8psFa7j0leDhmBe8Gdp3eRxS8e-7YAPyAulPzAKn9Kjc8w_wbjmS7HmkQxrWQSV_tbdJV2dyRGOCQvDm3CKIw-lNmaFvzeRAqjTTDVBHj_n35eAlqwtxWt_YuuLjCCMA0N1Gh9TIzN_KzGPCok2U2AeqxBHKbzG0K9Sy26tZmrA3UACVB0pTz4tIYCZu7KMgt8m5cH7nQ-V_uZ2cl_0JWVobJAvlDoNJWkjCIWtylKIMGjsHMvjzKMPYJvvDiM_BgIR0ZiygiMDRdG2p_SPjFTweev2He42Gu-M44PiyWwt-SKklzgZlfstQmsRmSu9l2MGy3GWQuQodLYVXPHXI9Gdh4EHLFddhaKCJxwgngE47PWjnk49vAujcGcJIGTZcKSws1GBk-NG_Ps2ZfrwRgSg2kcu6FIkjDzJlM2tmWYvb9Mh8XMW8MW6Gf7ee95QkC_P5TPNlWeYVFddmTPmC6vsz96saavswLFpgemZbq1QE8jde9U2mIKSPQb9UAbLS28BwCvHrmHJScEZegaNLzdlZD3Nh_ovaHiADDxsWLF7yU4fqAhxVwaQsLIjhGd29EUGU49KjOBeWy7CbDnTVVWW6BpqEcGirtnpmIP_1FIg4rullfNFazgvgb4baJmHXbrGsq-HJjCBG6AUkpTTfbS8EZejhIOiyiW2o9djuyScJq6KjMNHJi8mAnBXrUGHCH1oadjUabTZ-pLlTDsKi0jQGGKI0dsg-XLOMk8iyP8H_Hd1JQz2Ya_3lkzaKn0vNiORQrIMebXp2Ybs8NTOmbo5HPtm-KK602u8qeU6lFWF2J1ZVtDvmtNDFf5GbOLTk0WXBeTlOYtJwEZ-hYoEbSlyHOvOksFrHZej8rL0Yd-WjhGtFvuID7XBrht-7YzyG7HyJEPYdPcwbSQjG5IQ3IQu4HwqaC3oO2n9B_gLwSGwvFPrv7dR7qbA7_4kghpx997qWj4nHT35uyd-g2ZivYPv73zW7FP3qq4d3ytuHoOFLfhjaCf0P0r_ahMlld5U5XE7QuqV7f3_LZMHeKxPy0LksgKAmv_1zhvNDJSKY2Skhif6XQ7NP5oe5tlR2EqH78nmeQth-8u5ZKMmbI0Q_cG5YgpN5JgdrtfHiSZP9DTpv3gfXy5Q4VpXnsuhtpkc5dyZg69uu_Uh1d8Y0SX6d-sKvrJUAxVhZaXgK6wwM-GBpkRqQ7WYKWPMzD1w9n1htrkvs7vLjExSzUswUh3h1hqOKkJao0JqzUyG2zYQEzDr5eHCPoLLYNHfm6qeTTvBZz3wc37Az-c5Pw-OX94h-YnHYofD_cffq4Z84t0XEacWw71EMZhkAFU449tIZjywkS4cWQHTiACP7SFLUN8zRzHtRzXlX6WBFGayHvOc6jh0jv34gMNl-NvpE8Nl6eGy1PD5anh8tRweWq4PDVcnhouTw2Xp4bLU8PlqeHy1HB5arg8NVyeGi5PDZenhstTw-Wp4fLUcHlquDw1XJ4aLk8Nl6eGy1PD5anh8tRweWq4PDVcnhou_7UaLsM4joMg8uzYGnVo1igz2YYHNr4MywYpQpBY-tISU5fl2Aszu-XH9rboBP9ySMIvDqRcF3sB83IWJkyiS-WCIWycy8VyloPS4WOyY2__8Xzp-IFphjJR5mvevFd4VrUhmLySce5TsxVfQxXXY0Grvlv9_mreRDW6w3YI_UxGcWYWZn0DRCowcKpDiKF9QG4pHSzFMHf8r9bMf7t_6sI9deHOunDfffw_CYv-0g)

[//]: # (ob:2f7aae98)
# Retrieval adapter evaluation — preregistered plan

[//]: # (ob:be917805)
## Decision this evaluation supports

[//]: # (ob:af2a9640)
This evaluation decides whether a PageIndex-backed adapter improves evidence
location for the bounded Proofpress workload enough to justify operating it.
It does not decide whether a model answer is correct, whether a conclusion is
admissible, or whether any adapter should bypass human review.

[//]: # (ob:b35000cb)
## Compared systems

[//]: # (ob:b7801d33)
The evaluation runs the same frozen input corpus, task queries, and receipt
schema through three explicitly named systems:

[//]: # (ob:64412ec9)
| System | Candidate generation | Deep selection | Expected locator |
| --- | --- | --- | --- |
| `lexical-chunk/v1` | deterministic lexical document score | 900-character chunks with fixed overlap | `text_span` |
| `pageindex-tree/v1` | PageIndex section-tree search | resolved section and pages | `section_span` or `page_span` |
| `hybrid/v1` | fixed lexical + tree union rule | deterministic rerank configuration | typed locator matching the selected representation |

[//]: # (ob:7dccadb0)
No embeddings are part of this initial comparison. If a semantic or embedding
retriever is proposed later, it is a fourth named system with its own frozen
configuration and cannot overwrite these results.

[//]: # (ob:73142c84)
## Frozen inputs and reproducibility

[//]: # (ob:87d1f184)
Each run records:

[//]: # (ob:75c863a3)
- corpus manifest: source URI, byte digest, media type, and page count where
  available;
- task manifest: stable task ID, query, expected source, and gold evidence
  locator or adjudication packet;
- adapter name, exact version, canonical configuration, and configuration
  digest;
- machine-readable `proofpress/retrieval-evidence/v1` receipts for every
  returned candidate, not only the winner;
- wall-clock latency, source bytes processed, and a declared cost unit.

[//]: # (ob:22c08ac9)
The corpus and task manifests are versioned artifacts. A changed source digest,
query, gold label, or configuration starts a new evaluation run rather than
being folded into a prior denominator.

[//]: # (ob:bff754cf)
## Metrics

[//]: # (ob:eff9c14f)
Report every metric with numerator, denominator, exclusions, and confidence
interval where applicable.

[//]: # (ob:54ea01cf)
| Metric | Definition | Why it matters |
| --- | --- | --- |
| document recall@k | gold source appears in the first k candidates | did retrieval reach the right document? |
| locator recall@k | a returned typed locator overlaps the gold evidence | did it reach the right place? |
| quote binding rate | returned quotes verify against their claimed extracted representation | does the receipt bind a real excerpt? |
| citation precision | adjudicated returned citations that support the task claim / all adjudicated citations | avoids confusing retrieval with support |
| deterministic receipt pass rate | receipts accepted by the #39 contract / emitted receipts | measures operational integrity |
| p50 / p95 latency | end-to-end candidate retrieval duration | operational cost of the adapter |
| cost per task | declared local or API cost per completed task | makes trade-offs explicit |

[//]: # (ob:7cfd6f6b)
An unavailable source, unreadable file, or gold-label ambiguity is reported as
`inconclusive` with its reason; it is never silently scored as a miss or
removed from the denominator.

[//]: # (ob:ea7dc409)
## Adjudication and anti-leakage controls

[//]: # (ob:a73d5561)
Gold locators are created before reviewing system outputs where feasible. When
human adjudication is required, reviewers see the source and task but not the
adapter identity or rank. The final report separates deterministic locator
verification from support judgment and from downstream human admission.

[//]: # (ob:cbc6d19a)
Corpus source digests, task queries, adapter configuration digests, and random
seeds are fixed before the first scored run. Any tuning uses a declared
development split; the held-out comparison is run once after configuration is
frozen.

[//]: # (ob:7d34d742)
## Promotion rule

[//]: # (ob:2959865b)
PageIndex may move from experimental adapter to supported adapter only if, on
the held-out corpus, it meets all of the following relative to
`lexical-chunk/v1`:

[//]: # (ob:8db56a47)
1. no lower deterministic receipt pass rate;
2. a predeclared non-negative change in locator recall@k; and
3. no unreviewed regression in citation precision, p95 latency, or cost per
   task beyond the thresholds frozen with the task manifest.

[//]: # (ob:06661996)
The report must show the actual numbers. A positive result recommends further
product integration; it does not automatically change Proofpress policy or
admit any conclusion.

[//]: # (ob:22622fae)
## Deliverables

[//]: # (ob:9e1f0aed)
- frozen corpus and task manifests;
- one result table per named system plus raw receipt artifacts;
- a failure ledger covering missing mappings, invalid receipts, and
  inconclusive cases;
- a short decision memo stating keep, revise, or retire for the adapter.

[//]: # (ob:23df935a)
## Private operating procedure

[//]: # (ob:d568705b)
The runnable panel entrypoint is
`studies/apex-agent-eval/retrieval_adapter/run_private_panel.py`. It accepts an
authorized private manifest and private output directory; neither belongs in
this repository. The manifest binds World425/APEX sources by URI, byte digest,
media type, extracted-text representation, pre-output gold locators, and task
query. The runner emits raw receipts only into that private output directory
and writes a separate sanitized report containing source/query/gold hashes,
denominators, receipt counts, latency, cost, and inconclusive counts.

[//]: # (ob:d196e6d1)
The scored PageIndex and hybrid paths require the local sidecar from #40, an
explicit `openai/gpt-5.6-luna` request, `OPENAI_API_KEY` in the runtime
environment, and a `fallback_used: false` response. Missing source custody,
credential availability, sidecar protocol, latency, or cost telemetry is an
inconclusive failure for PageIndex/hybrid rather than a substituted result.
`lexical-chunk/v1`, `pageindex-tree/v1`, and `hybrid/v1` remain separately
named in every private record; a future Terra sensitivity panel must be kept
separate and is never pooled with this Luna panel.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzUxNTM4OTg1MDI5OTJjN2IxNTc2MWYxOSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImE2MzZhYTBmIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85ODI1ODIzNWUyNDk0YmYwNzBkM2Q1MDYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzgzZGY0ZDJiMDhmNGZjNTQzNGYzY2RkNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXO1uGzmWfRVC_XMku74_nB-7Rnd2YcxMT5DJzOxi3JBZJMuqdqlKXR92NHGAfYh9wn2SPZdklUq2ozh2doFdCAgcq8QiLy8vzz3nksmnGW-6IueiWxZydjbbbJahG_pJmoSOl6aeiDM3jCM3d9PZfJbVcruUxbVqO7RtV9wLozOeSZ5kSZgrx0kDLrMgyd0siRPXiyIe-1kQy8h18kQ6qcddEQaxkIkIvFCJQCYO-pVFK-pb1WxnZ5_oQ7fs-DVGKHlHQ83xS6ZKPPiraoq84FmpWKNui7aoK7ZC-7rZsmzL3jV1nW8a1bZ4Z8PFDb9WNKm9x039q8J0-4Y6XHXdpj07Pb0uulWfnYh6fSpWqloX1XXHq-vEd0733m7Ub32B35d9q5qlqKtWVfBF1_Tq83y2UpycyCM_4tzJZ-bJUt3qRnCuWqaJFyaeHyovSIMsd2JH-jJ0IrKsbjqa2rIsKgXLhxUpl4kv80B6mZPkQQ4H-kHuCyljMx1r3VLwTduXmLBHdoq6ke3s7O-fZnb4TzOsct209Jv5WsllBpf_fSZqqT7OfsEMhmjAwLIW7WmjuqZQt7xcbEpetafv3354f_H2r-d_WJ7_dP7uw9v3S_rwl_MPF3_6-WQtZ_Nviifeofes77CMy4y3RUtRpcp8yVu4t1O6v75b1Q0ZfVNU1GW7bTu1xjcVX9PqGuPneLGleJidVX1ZYipihQVUxgVZWYsbtPXymHOVJmiOtevUR5ro-2GOjEu-6VTD6EPPySz2X__xnwzubdR1oSPRGsGl1NZtKAzVHZ78wJ7fD_6SjByKHrrthmZBgYKgm32e76zNVOrGiRPuWfuTEibuOwT-dIS231AEtQeN_IE95_0DNvHc42kUON_Ppg8P3pHoTKqW3a1Ut4ITOXuHzXBRYZUXGfY0XDf4t9jZuuEN33eeHzqOI7I9Q3-s12iIHkwQfc1XTzQ_tFxYK1f6_otH_LBSU0c0fdXCo4q1CHSWN_U_VMWKatN3DLt307dz1vH2hv3WAxUPeCIKAtdTIn2xXffsz7oRu2c_8koWErDMrlWlGmPoPYJKbRh2LoDVPHj7cYPf0f3OLo1te4bFUgjkC-fFhv1cM7XOlKSlaBneYni1Y3VuArGoiq7AdhS6y6KtqxN2kSOgWrXmBxwW-27giSTYs-tfJv7HWJVEBgL4yl4UWVEW3fYrsfSc9w8EVxJLgOb3tOktFyuKMWZzxdkhj4QiiXzuf7_RFzaG2ZpXRY4sf8baum-EYn95fzFHMkeIGaYxZ2slC87ItrkeZmdoSaA8NdTzhJPwB7H-KkNpU1pT6U294wabTcyBuBD4ES7Z3NeesHOG_HMInvI8DgOR7xn6R8og4muotGt1IF5UnqfCDb65__eKABswBDYGx1N7dgdyxKp-Tfu9buZA6KoGQzIf1EdR9jT_dn5gumGguON--3Tv7Ww1xuR6Q2t8-dtqy4oOC9EhD7Ts_rK6Z4vFgu39PIg9IpdRHmXfatB5xfqK3_Ki1CzUxOwczxosgn6UFyUe1A27rku50MyV8XVWXPcH_KM4wDBw9uP2XP7ay0IYkKXg41VXLErFidcyatfU5dei5dmdHEr6MThqGLnf2bp_hYMYhqBAMltJwIuUNTKV143h-OoO1thkwOq-03v4bnXAlyITkXRT_p2t_dGAgEUpg017KVjh08BM0GGOFbcJUh6CVukHMg68PWshZNa1JQEI3MMr_KjxgZX00jBNojB74WgjE8POAzxAsxEvWQMENnDAGjpjwn67euB_mrId8EEiszDiQfxCq9wTVtUIpDsMKhWGBjghMQA1kNpUselAC9qWYTHUm8vKOwEDwMvgmSVi7kAycaIoctM0eqFZlDkaA6frvu1Yu6rvNJ9DhujhJyBqBvCiXLGpWyDbLbWHhOtYc8BZnhd5Xs7VAwZe4vWGAOjrAmCv6YFgSZWbO1z38O0jLQbG-sXkibVYMOTNYdIapBkCiVUPF-WX-aBiZzbbLi1UzOw3g9xUyxgCxfH8IHazRCRx6sdKeblLKqqqO-1SK7SZFdpI1UrcbOqi6nTdoNEjkYwcPpGK_IUUelmI7aSHqWqfdKLrAS8U9G2dd0tkumvVbJrC1g3azD0LM5HGPlcIysQNozgFaHAvjl0ppMpyKRMe-lnsxVwmacw9sKAo9zLuqNDlMtR9d7zT-t8s15kXQCfTk5nneNHCSRZe9MFzznz_LEx-5zhnDnFz63HK4nGgXBXmiJLd00__y0UDHZ1G1q94u0L7IPOEirKUuymtiO5jovRt4H5HgW7HFblysjxzApEkw7gTzT6M-2LNbYdx3CBM8zDPkjAahpnIcDvMa2T0Gmz4VtHreKUS6rLSWZm6QR7WmJXVPV6VkxIbu6ubm7LmkoEO9tcrwvtfgXNFvmX1RmtDJO6iO7msLjoma_SP_Wftmpi1riUxpKol-MYcgBeAbdD-XROgjyWZaHBZcbku2rbILM8a21XbcUrA2h7kIttq5F_1AB3LJk6egFbr6BC2pY6DDOln43ruygi79XxeXcD2muXCj7NQYe-6Y6-7UsG4fC_X_pp4aFWjs91l1QKL1lBMq8YszKpRinI00Kvoyi2jytlo_NmXHYL0BxXBVeircDB9Uk2wpr-mPGDZ3xcIvPlJX12V6iPYW7kQq766Ob11r_Dtfq63LRBpoicmwlpBHPKeYUnxGqYmNDOjDlqjafLiI2ygynPJN2h5RTNathteXdlhN9gzhd4zHXxox92xoNbMSH-JD7yBpL6nfFaXt-RhO2FaHOqppTHsQzsM5q4H2Rt1tc2aQtrRjJHD7H7H9Fh9NTCQR34AhvHq5gEDvdfyeedvCCexov2pY0yvjDKyWFFF2770lICyoeGlPudBhEwr5RAak3qODY3XFGgqmgxMHTu4rGxiMTgBzAJtojkh3iBEIQfxlAOx-ob06iTGzWoXEA71XWV302W17yFaI8ErgigKiLumQBTDO-3AT9oDyJEkQRT7vvCdYMwEkyrSDjleWAWyw7h5JJwY-9GN-TDMpDBkh3lOYWfY4ELmPliCkwVjapnUemyHr6nVbIy86rEfgdMNUgtjo3zWDHCPFKJnQ83004uf5hrhtnOtMHSMDoqbOieFPUlabAxv_OFTwUdnQarTww0ZguKDugUqDBWcOQVAXel9thccZrS9RzSambPudc1pO6nFWAW42h3MTPjQYKve2hauW51jdcGFOkXjvqFikhiwdK7zZl0BuGm3Qg8DWvWod7wEIhIf0pugEnCUXRlaFL1HBCxQ0syAMyt6aDJQJECR7uQJATTwG3BoJxVJzmU-8qpdgW2SuV5aIAPLlfuKen5Z2RXXi6vLJzrL7-9WRElDvbNK3T3Im6TziA506P6yyhShXI6-MBLodK3FX1E30yrWgZ0dpFEWE0EXoRiz9652t9vZB6tytjMZJEHoQo0o4Q2dTQp143nUy0twu0C1ewJTVg1RXr37GN8QCaAIPTDnHHDgBW4qw2zE9kkBb0z7ryjN0cMxUWMjIJD_-QZf6kW3AQFbkVEpS-i4z4sGIXuz2xeUTfEbG7cXfiPoo8ZNcb3qxhH-yQw4oMNkPL7bb_sJ0pICQ8L2cMaOWnSPhoNgEMqO9VsPrckycAeKPyo9aGJgx9LftrQxiC3za15UmBt6KhDoJS8odcHLmrI8TsuGTOtxbX2DxtFzgRMQDZCOw5xB-CwENoMIud9ho-58wBvbknrm3SBN9DB6T2u72CmD6_Y62L2Hjm_rQrY6ABGQNPFxbXQED52a9T9cqtH-sgjJhVAbXRg0GPiDn5qaHaH3KShC0Zm52Pb32De87eG1QYrUFWygzXCNxL41BmxCBy9v0nBAT7ynKrno6oWqJgA8mYXcEappxxpNNatRY4Ix7qcvqKShXXi_w1-Ks5Jw7fzdxa4VEaFS0VRs-zW_oaVuuFSLOs_bkcUfJGepk-dhEICfJSPOTAreQ0n0FaVs8iHYlilvEbBDll0V1SDUbtXVjnOhOzC7N5agVZq_tei5IimiSTq9T0oQqg6jEc-j0qI0tUXy6fOwOgmzlCsRydwd6wCTwvoOq19TEx-YU8i5E_DQ99XI-CZlcjvWayrcBNc5XEc69wSoSpTVCNk9aqNXQV9KQZI33RHstkoZbm-xdMjMGRQk0Ql8R0LaFgDg346WlMAR4uGEfdCAW2lM1Tu2VeRtAq0HqstM7rLSWDYYpRdu2Oww9lrjPBmhv5Gg4S10DF-zYUZa0YP_f3l1hZfJVCgpHD5y1Umpfzw-fnmVfmisaTl-1GtIaaWkWTmjw-y67RKSDWAQD3CaCvAEUoXl7FvVTvjWJeTirSrrjVGm2MPdG93JSmFn1VrWDxpILyl4TE3JhuePDaUaiBExh4oZSZaLzFV-6oidQBvPGnab4TnHB7ZP382DxMvzgEfxSAh3JwpDhfwVhwTmoea6RQ7oQcw_8JIpfhDBUIoyA7KRBV6QvLK-M1kHgE7l9K4GLD0qHRwQRDKUWRCmXpprRWUU1u50ws7wVQcOEu9Wi0pdGxMNCyaS85CevKFAvKx8PRihst7blOWuG3PXid56nODn05RmubPJL6QvLAyobU2QQMl9hd5WAKp2qDNp5B7z_sDlDwiFKPDBibMsC9Mx1iaHJxOh8NLzECjZNSKHbCR1T1MxsrmzSV37QOeYsdLI-64GC6W1RzhZP0_ql6aarxMO4U-nC4i7UuMhURAmeSS5G0R5sBNG47HMtPD7tbOWoUiY-DwJsa1cd1T2k-OXUYi_4kxlWg_ZYIoIz7sxXkdhZjQyy8EKQJ9YqeS1xh-Cd-wsDdP0N8g51XSwEyvwomLHveYmahmbsgFwKeCh7Rvr3pg6sI7hNZI96TldLr5RamPSWGuYB6hXQeBry9AWIR7F4i-fyZlP3HRUsuge3nPUtyYRO4-fP30v0lz7hHvHL-j25_-V-5JAY32u9ZLrkr7MUz_kDw5Ai1sixbsav64ygBl__aD60JsHDiJlGCWx8-jU-kV2aBTqq8psDF6B0sI_zVaf3OnUetV2oFeqPeUb9XGh3begJT2dmvnoWBY0JFIgI9_LRssrdsmUNrspDMPsbjXSPr0vjJxoQeQemojo1crtiyv7wAp7RqolvVWZGzuLAWXmBB0Lw1QNW2o5yf9_KLmwAC8A8LXcmmMj3mxPvrSeT4_-3lQuByfQvARvhhkThTDgRzBFBTAqA3eqVFQt2TJEsizh7JMvLdDTg_4e2NOyP0ATDUcjI-s1BIbyQ953hIsfVNNQmbrSeYqosw6lE-PvYf0_ze5W23E62pfqoxK9RWXr1vN3b__NRuIYHeD_hW4C3d_cmsAxrSfQL4hTVKaCbvxNM37-SfmBu-jGJdMj8Onx7_RY_NMROf7_Isfzr1Y8vFrgf3764sDXblF8l6sSkCjSEVDoMeRiLmTgp4onvusLN0rdSKVKgmfFjutAsbtO5MkYxkku0iB3pS--MJ_9mxLxB8c5C5OzMHjipsT4T0CONyWONyWONyWONyWONyWONyWONyWONyWONyWONyWONyWONyWONyWONyWONyWONyWONyWONyWONyWONyWONyWONyWONyWONyX-x29KTDypVBZFoUjiXc1ycm43xb1vPH0bKl-O8tIkVVCAY-afHMhNg_2lx2qWbS7tbE_R0dKelC7Niexme3XCLjpLjCkSEMT6jgSdVz862zalmGHCmmIg3VGZvW62b8DJCi2Zwe9qKtQVGnYtv8NORCNDCcb-SHC07G91U8rAC0_1Ya_JuS1x9Ed1octqWhgapc2CvPVA38wJyew5vC0CWAI1HwPeFgmMUeRmOstZa7K5C-rW5hES_VrSfMkBcB361RW_Vhcf7fH4eP4_wBYxQ0g1Tdf0ZE-1GafaSgoPkAvK9CNZbefjDtM1MHwecZlA2cxof6fodofAJ46zJJRxFkQjy50ctk7i76VHpnQpQWfsHwJnrkNrVB1X2C0VL06vN90iPIkWJRTEFbMXiebs6k_v3v58frGEqFn-_u2_Xw3aHUvUIfOjo-q2aOqKSMBQkrrKgc90IkX_-5w8A_SUraI-2w39R3Qn7I8Wcyyns5cC4OjJTQErY3QJdT5OAhu6q0Vdzh9nw929isLsnr1FGOCPYGd036l13aS-RNHSZ8j8XW_0J4HuyVOcY_7UWYJxwbTcD-WDABtDsERsGuDGQ1MQGoLYFHffEFYfvLxhcm2mAK36aGgIbh14gxzb1DWQfkj8hb0vYi9_PDxA_4w__w2ozO6u)

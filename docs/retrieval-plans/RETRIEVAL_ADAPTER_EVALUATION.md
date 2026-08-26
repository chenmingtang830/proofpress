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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzUxNTM4OTg1MDI5OTJjN2IxNTc2MWYxOSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjU3NGUxZTVmIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV83MmE5MDIzNDcxYjhjODc5MzdlZTJmMTUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzgzZGY0ZDJiMDhmNGZjNTQzNGYzY2RkNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNq9WtuS2ziS_RWE-nGkKt5FVj_sOrq9G47YnenwemYfpjpkEAAldlEgm5cqa10dMR8xX7hfsicB8KJyt2xXOTbCYUsUkJlIZJ48mfTHFW_7suCi35VydbNqml3sx2GapbEXZFkgtrkfbxO_8LPVepXX8rST5V51PdZ2Bx7EyU0uU-Gr0FcqS7IkiotEKlWoPPT9PMlzFYU8TyJ8jfKcizD1vTRVngxyvlW8CALIlWUn6nvVnlY3H-lLv-v5Hhoq3pOqNT7kqsKDv6m2LEqeV4q16r7sylqzA9bX7YnlJ_ZTW9dF06quw56Gizu-V3Sos8dt_YvCcYeWBB76vulurq_3ZX8Y8itRH6_FQeljqfc91_s09K7Pdrfq16HE593QqXYnat0pDV_07aB-W68OipMT422kfBUXK_tkp-7NIjhX7bYBz7wgjLZ-nop0m4VbpYLCj8myuu3paLuq1AqWjzdS7dJQFhE85qVFVIg4CqMiFFJu7XGcdTvBm26ocOCA7BR1K7vVzd8_rpz6jyvcct129Mn-rOQuh8v_vhK1VB9WP-MEYzRAsaxFd92qvi3VPa82TcV1d_329bu3b17_7dV_7F79-Oqnd6_f7ujLX1-9e_OXP18d5Wr9VfHEe0jPhx7XuMt5V3YUVaoqdryDe3tl5A39oW7J6LtSk8ju1PXqiF80P9LtWuPX2NhRPKxu9FBVOIo44AKVdUFe1eIOa4Niy7nKUizH3fXqAx307XhGxiVvetUy-jJwMov97z_-yeDeVu1LE4nOCC6lsa6hMFQPePId-3I5-Ecycigk9KeGTkGBgqBb_baerc1V5m9TLz6z9kclbNz3CPylhm5oKIK6i0Z-x75k_wWbkLEcWe59O5vePdkjIUyqjj0cVH-AEzn7CcnwRuOWNwCQO7hu9G8529rwlp87L4w9zxP5maE_1EcshAQbRJ_z1e8sv3RduCtfhuGzNb47qKUj2kF38KhiHQKdFW39P0qzUjdDz5C9zdCtWc-7O_brAFS84IkkivxAiezZdj2y_zKL2CP7gWtZSsAy2yutWmvoI4JKNQyZC2C1D15_aPAZ4me7DLadGbaVQnCZe8827M81U8dcSbqKjmEXw9ae1YUNxFKXfYl0FEZk2dX6ir0pEFCdOvILDtuiVgUijc7s-reF_6FLS1QggK8cRJmXVdmfPhNLX7L_QnClWwnQ_JY2vebiQDHGXK24ueSRWKRJyMNvp33jYpgduS4LVPkb1tVDKxT769s3axRzhJhlGmt2VLLkjGxbGzWzoRWB8tLQIBBeyp_E-osMpaR0ptJOk3GjzTbmQFwI_AiXXO3rrtgrhvpzCZ6KYhtHojgz9D-pgojPodK86kK8qKLIhB99tfy3igAbMAQ2BsfTevYAcsT0cKR8r9s1EFrXYEj2i_ogqoHO360vHDeOFPf8rz_uozutwZjCJLTBl_8-nFjZ4yJ61IGOPd7qR7bZbNjZ3xexRxQyKZL8aw16pdmg-T0vK8NCbcyu8azFJZhHRVnhQd2yfV3JjWGujB_zcj9c8I_iAMPIO4_bV_KXQZbCgiwFH9d9uakUJ17LaF1bV5-Lli8Wcqnob0MZx4n_ja37dziIQQUFkk0lAS9S1chVUbeW46sHWOOKAauH3uTww-GCL0UuEuln_Btb-4MFAYdSFpvOSrDCt5GZQGCBG3cFUl6CVhlGchsFZ9aikTnWjgQgcC_f8CeLL9xkkMVZmsT5M7VNTAyZB3hAz0a85AgQaOCAI_qMBfvt65H_Gcp2wQepzOOER9tnWuVfMV0jkB6gVCqoBjihMAA1UNpU2fSgBV3HcBnq-1sdXIEBYDN4ZoWYu1BMvCRJ_CxLnmkWVY7Wwulx6HrWHeoHw-dQIQb4CYiaA7yoVjR1B2S7p_Vo4XrWXnBWECRBUHD1hIFX2N4SAH2-AThbeiFYMuUXHjcSvl7TZmSsf1g8cRcbhro5HtqANEMgMf30Un5ej13sylXbnYOKlftlbDcvdti67o1LXaPNXKONUq3EXVOXujdzg9ZoojZy_EZd5M_UoVelOC0kLLv2hRAzD3hmQ9_VRb9DpdurtmlLNzfocv8mzkW2DblCUKZ-nGwzgAYPtltfCqnyQsqUx2G-DbZcptmWB2BBSRHk3FOxz2VsZPe8N_2_va6bIEKfTE9WgRckGy_dBMm7wLsJw5s4_ZPn3XjEzZ3Hl4ON3xZPP_4_Dw1MdNq2_sC7A9ZHeSBUkmfcz-hGjIxFp-8C9xs26E6vKJSXF7kXiTQd9S569lHvs3tup8bzozgr4iJP42RUs2jDnZqXtNFHsOF7RduxRQt1q01VJjGowwaz8nrAVrkYsbGHur2rai4Z6OCwPxDe_wKcK4sTqxvTG6Jwl_3VrX7TM1lDPvLP2bUw61hLYki6I_jGGYAXgG3Q_nkJ0MeRTCy41Vwey64rc8ezpnX6NB0JWDuAXOQng_yHAaDj2MTV70Crc3QM2zLPQ4UM8-k-5zHCfJ9fNhdwUvNChNs8Vshdf5I6jwqm63t-72-Ih-lqTLW71R2w6IiO6dDaizm0SlGNBnqVfXViNDmbjL_5Y4eg_KGL4CoOVTyavpgmONNfMh5w7O8PCLz9m356X6kPYG_VRhwGfXd977_Hr-e13q1ApImBmAjrBHHIR4YrxTYcTRhmRgI629MU5QfYQJPnijdY-Z5OtOsart87tQ1ypjQ508OHTu_Mgjp7IvMjvvAWLfUj1bO6uicPuwPT5ZCkjnS4h04Nzm6UnGk9nPK2lE6bNXI83Z-Y0TXokYF84gdgGNd3Txjoo2mfZ3-jcRIHyk8TY-ZmlG2LFU203abfa6BcaARZyHmUoNJKOYbGYp7jQuMlAxpNh4Gpk4Bb7QqLxQlgFmgTnQnxhkYU7SCeciDW0FK_uohxe9slGof6QbtsutXnHqI7ElwTRFFAPLQlohje6UZ-0l1AjjSNkm0YitCLpkqwmCLNyPHMKZBT4xeJ8LbIR3_LRzWLwZBT8yWDnTHBhSxCsAQvj6bSspj1OIEvmdU0tr0akI_A6RalhbGpfTYM8IwUQrKlZubpmx_XBuFOa9NhmBgdO24STh32omixKbzxhy8bPnoXpHqjbqwQFB8kFqgwTnDWFAC1Nnl2FhxW29kj0mbPbKQeOaWT2kxTgPfzi5kFHxptNant4LozNdYMXEgoFg8tDZPEiKVrUzdrDeCmbEU_DGg1Wh94BUQkPmSSQAs4yt0MXYrJEQELlLQn4Mw1PXQYdCRAkf7qdxqgkd-AQ3uZSAsui4lXzQO2ReV67oAMLFeed9TrW-1u3FyuGZ-YKn-erYiSlqQzrR6e1E3q84gO9BB_q3NFKFdAFjSBTtem-SvrdjnFupDZUZbkWyLoIhZT9Z5nd3NmX5zKOWEySqPYRzeiRDAKWwzqpvdRzx_BzYHqcgJHVi1RXpN9jDdEAihCL5y5ABwEkZ_JOJ-wfTHAm8r-C0Zz9HAq1EgEBPK_3uFHc-kuIGArKipVCRP3RdkiZO_mvKBqik9sSi98IuijxW25P_SThn-xCkd0WOjjc76dF0hHCiwJO8MZp7XsP1GHhkEop-vXAb0my8EdKP5o9GCIgdNlfu0oMYgt8z0vNc4GSSUCveIllS542VCWT8uyJdNGr5tvkB5zFjgB0YDWcTwzCJ-DwHZsQh5nbDTCR7xxK0ky78fWxKgxOW3sYtcMrjsTMO-D4Pu6lJ0JQAQkHXy6GxPBo1B7_5dHNcZfDiG5EKoxg0GLgd-FmZ3ZEXpfgyKUvT2LW_-IvOHdAK-NrUitYQMlwx6F_WQNaGIPm5ssHtET-5SWm77eKL0A4MUp5EyoloINmhpWo6YCY91PP9BIw7jwccZfirOKcO3VT2_mVUSEKkVHceuP_I6uuuVSbeqi6CYWf5GcZV5RxFEEfpZOOLMYeI8j0ReMssmHYFt2vEXAjrbsfanHRu1evZ85F8SB2X3vCJo2_K2DZE2tiCHptJ86QXR10EY8j0aL0s4WyadfhtVpnGdciUQW_jQHWAzWZ6x-yUx8ZE4x517E4zBUE-NbjMmdrpdMuAmuC7iO-twroCpRVtvInlEbcwvmP6WgyFtxBLudUpbbOywdK3OODpLoBH6jRtoNAODfnq6UwBHNwxV7ZwBXG0w1Gdsp8jaB1pOuyx7uVhssG40yFzcmO4zdG5wnI8wvEjS8Qx_Dj2w8kenowf__-HZFkMtMKCk8PnHVxah_en38_Cn9uNjQcvxVH9FKKyXtzdk-zN3bXJBcAIN4gNNowBNIFa5z6FS34Fu3aBfvVVU3tjNFDvffGyEHhcyqTVs_9kDmSsFjaio2vPjUUJqB2Cbm0jAjzQuR-yrMPDE3aNO7hjkZvuT1gZMZ-kWUBkUR8WQ7EcL5jcI4IX_BSwL70HDdsgD0IOafeMkOP4hgKEWVAdXIAS9IXlU_2KoDQKdxel8Dlj4ZHVxoiGQs8yjOgqwwHZXtsOa3E-6EL3rhILFXb7TaWxMtCyaS85SefE-BeKtDo4xQ2eQ2Vbl9a_-vE-36tMCvlyXNcWdbX6i_cDCgTjVBAhX3A6QdAFTdOGcyyD3V_ZHLX2gUkigEJ87zPM6mWFu8PFk0Cs99H4JO9ojIIRupu6ej2La5d0Xd-MDUmGnSyIe-Bgulu0c4OT8v5pd2mm8KDuFPbwaI86jxUlMQp0UiuR8lRTQ3RtNrmeXg93PvWsYhYRryNEZa-f7U2S9ev0yN-AveqSznIQ2OiPB8mOJ1asxsj8wKsALQJ1YpuTf4Q_COzDIwTf-CnNNMB5mowYvKmXutbdQytmQD4FLAQycb997aObCJ4SOKPfVzZlx8p1Rjy1hnmQeoV0ng68bQDiE-icWff8Of_wO3FZqS)

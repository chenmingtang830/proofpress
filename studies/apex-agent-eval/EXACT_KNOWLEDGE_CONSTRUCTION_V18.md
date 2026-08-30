[//]: # (ob:ffb9914f)
[//]: # (ob:v18-title)

[//]: # (ob:1b9c9fe5)
# Exact Knowledge Construction v18

[//]: # (ob:c7bae7d0)
[//]: # (ob:v18-status)

[//]: # (ob:0f9993df)
**Status:** Stage A completed on the five frozen zero-heavy tasks with no answer executor. The structural qualification gates passed, but the substrate is not ready for Stage B: only 19 of 44 substantive requirement slots were candidate-covered, 25 remained explicit gaps, no controlling-authority node passed validation, and no task was executor-ready. Stage B is blocked until authority coverage and exact calculation/period completeness improve. All constructed objects remain candidates until Human Approval.

[//]: # (ob:8771d08b)
[//]: # (ob:v18-decision)

[//]: # (ob:60e62598)
## Product decision inherited from PR55

[//]: # (ob:f9d861b8)
Keep the existing Claim Graph as the canonical governed substrate and keep small-seed disclosure as the current default executor interface. The v16 and v17 results did not justify replacing the graph or increasing retrieval breadth. They identified a construction mismatch: exact tasks ask for atomic numbers, periods, authorities, calculations, and output forms that an abstract claim may not contain.

[//]: # (ob:392c714e)
This phase therefore enriches the existing graph with typed exact-knowledge objects. It does not create a second graph, grant retrieved text admission, or turn calculation into authority. Human Approval remains the only path that authorizes downstream reliance.

[//]: # (ob:2f4ff133)
[//]: # (ob:v18-question)

[//]: # (ob:62625f07)
## Primary research question

[//]: # (ob:4e9d88ca)
Can requirement-aware exact-knowledge construction raise native APEX task success on the frozen zero-heavy tasks without weakening evidence lineage, authority boundaries, or admission semantics?

[//]: # (ob:26990aaa)
The mechanism hypothesis is narrower than “more context improves quality.” Before an executor runs, every atomic task requirement should have a declared completion path: exact evidence atom, controlling-authority candidate, deterministic derivation, or an explicit gap. Retrieval should fill a requirement slot instead of accumulating loosely relevant excerpts.

[//]: # (ob:73a7aea2)
[//]: # (ob:v18-invariants)

[//]: # (ob:547cae7b)
## Construction invariants

[//]: # (ob:65983f1d)
1. The requirement plan is compiled only from the task prompt and native output type. Rubrics, gold answers, and silver locators are forbidden inputs.
2. Every number-like source span is inventoried before semantic selection, including years and section numbers.
3. A material number in a proposed claim must bind to a custody-valid numeric atom, a recomputable derivation, or an exact authority citation span.
4. Numeric atoms preserve display text and normalize a decimal value while recording kind, unit or currency, entity, period, and precision.
5. Every derivation variable binds one digest-valid numeric atom with the same value. The expression, rounding rule, input units, output unit, entity, period, intermediate basis, result, and digest must recompute.
6. Authority candidates bind an exact source span, citation, proposition, jurisdiction, effective date, and authority level. They cannot self-confirm normativity.
7. Candidate coverage and governed coverage are separate metrics. Candidate construction cannot make an executor ready for governed reliance.
8. No candidate object or gate may admit itself. Human Approval remains the sole admission authority.

[//]: # (ob:cb719214)
[//]: # (ob:v18-pipeline)

[//]: # (ob:e2f12de5)
## Proposed pipeline

[//]: # (ob:0bb4210b)
```text
native task prompt
  -> atomic requirement plan
  -> requirement-routed source discovery
  -> exact numeric atoms / authority candidates / derivations
  -> candidate readiness matrix
  -> human governance of eligible objects
  -> small-seed task working set
  -> native executor and blind grading
```

[//]: # (ob:655e465a)
The implementation in this PR stops at candidate readiness and claimability. It deliberately does not manufacture a Human Approval receipt or run a paid executor.

[//]: # (ob:46e3560b)
[//]: # (ob:v18-artifacts)

[//]: # (ob:7b96cbb3)
## First implementation slice

[//]: # (ob:4b8b5a43)
- `retrieval_adapter/exact_knowledge_contract.py` defines fail-closed schemas and validators for requirement plans, numeric atoms, authority nodes, derivations, readiness, and proposed-claim number binding.
- `retrieval_adapter/run_exact_knowledge_readiness_private.py` accepts a private task bundle and emits a sanitized report containing digests, object counts, slot states, and gap IDs without reproducing prompts, source excerpts, numeric values, or authority text.
- `retrieval_adapter/run_exact_knowledge_stage_a_private.py` runs the frozen five-task construction audit through the fixed GPT-5.6 Sol compiler, extractor, and derivation roles without an answer executor.
- `retrieval_adapter/reaggregate_exact_knowledge_stage_a_private.py` recomputes readiness from saved private artifacts after deterministic contract corrections without making new model calls.
- `tests/test_exact_knowledge_contract.py` exercises exact receipt binding, decimal normalization, derivation recomputation, tamper rejection, authority boundaries, task-prompt-only planning, candidate/governed separation, numeric claim gating, and sanitized reporting.

[//]: # (ob:b3efe6f1)
[//]: # (ob:v18-qualification)

[//]: # (ob:9bf810f4)
## Qualification sequence

[//]: # (ob:b7822859)
### Stage A — substrate audit

[//]: # (ob:18b61671)
Run the candidate-readiness builder on the five frozen v17 zero-heavy tasks without an executor. Report per task and per slot:

[//]: # (ob:89d03e58)
- requirement count and type;
- candidate-covered, governed-covered, gap, and invalid-binding counts;
- the path used for each covered slot;
- numeric, authority, and derivation object counts;
- construction failures by invariant;
- construction calls, tokens, latency, and known cost.

[//]: # (ob:ec0994fa)
Stage A passes only if every task has exactly one output-structure slot, no invalid binding, no private content in the sanitized report, and every material proposed number passes the numeric binding gate. Gaps are allowed and must remain explicit.

[//]: # (ob:784763c5)
Stage A passed that structural definition across 49 slots: 24 were candidate-covered, including five mechanically covered output-structure slots; 25 were explicit gaps; and there were no invalid bindings or sanitized-report leaks. On the 44 substantive slots, candidate coverage was 19/44 (43.18%). The construction produced 49 general evidence atoms, 16 numeric atoms, 10 task parameters, 10 derivations, zero validated authority nodes, and 39 recorded invariant failures. The formal run used 15 model calls and cost $0.5762715 with complete terminal cost receipts. No answer executor ran, no claim was proposed, and no object was admitted.

[//]: # (ob:30dcb8e5)
Structural passage does not authorize the Stage B executor comparison. The current stop decision is to close three substrate blockers first: provide a controlled authoritative-source corpus and exact authority bindings; construct complete, recomputable inputs for exact tax and annual calculations; and require every declared period in a series before treating the slot as covered. The detailed evidence and task-level breakdown are recorded in `EXACT_KNOWLEDGE_STAGE_A_RESULTS.md`.

[//]: # (ob:3eb73212)
### Stage B — fixed development executor

[//]: # (ob:059dd987)
After Stage A passes and eligible objects follow the normal Human Approval path, compare the frozen v16 small-seed route with small-seed plus exact working set on the five zero-heavy tasks using one fixed development executor. Freeze task prompts, sources, graph version, approved objects, executor route, grader panel, output handling, and retry policy.

[//]: # (ob:1adc7e2d)
The mechanism advances only if it improves criterion coverage without increasing unsupported-claim, citation, authority, native-output, or governance errors. Report context, tool calls, model calls, tokens, latency, and known cost next to quality.

[//]: # (ob:70f596c6)
### Stage C — frozen three-executor confirmation

[//]: # (ob:b15cbd8a)
If Stage B advances, freeze the mechanism and run the same paired panel on GPT-5.6 Sol, DeepSeek, and GLM. This stage tests executor interaction; it is not another mechanism-tuning round. Report paired task deltas and intervals rather than treating model cells as independent samples.

[//]: # (ob:aba800da)
### Stage D — full native panel

[//]: # (ob:0a68a28a)
Run all 12 native APEX tasks only after the zero-heavy construction gate passes. Preserve the console, new-DOCX, and edited-DOCX denominators. The full panel estimates whether exact construction helps beyond the deliberately difficult subset and whether gains survive native artifact creation and validation.

[//]: # (ob:547f6374)
[//]: # (ob:v18-success)

[//]: # (ob:1a89deff)
## Success and stop rules

[//]: # (ob:ce1b9cee)
The phase succeeds as a mechanism test if exact construction increases atomic requirement coverage and native task quality on the frozen comparisons while preserving governance and staying within an explicitly reported cost envelope. A higher aggregate score does not excuse a regression in unsupported claims, citations, authority handling, artifact validity, or admission semantics.

[//]: # (ob:ce89e8b9)
Stop and diagnose before another paid run when a failure is attributable to requirement compilation, graph sufficiency, object construction, approval coverage, projection, execution, or delivery alignment. Do not compensate for a construction gap by silently expanding context or retrieval budgets.

[//]: # (ob:123fbd56)
[//]: # (ob:v18-claims)

[//]: # (ob:fe420096)
## Claim boundary

[//]: # (ob:aff04e5c)
Passing the deterministic contracts proves only that exact candidates are structurally bound and recomputable under this harness. It does not prove that a source is legally controlling, that a candidate is correct for a real matter, that a model answer is lawyer-approved, or that the mechanism improves legal quality. Those claims require the staged evidence above and, for real downstream reliance, Human Approval under the applicable organizational policy.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzkwZGEyYjk0M2QyZjQ4NzYwOTUxODU0YyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjBhMDViMmQ5IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV81Mjc2NTFjYjMxZTE0MTM3OTM2YzNhZWIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Q4N2RkZGU3MDU1ZjQzYjc0ZmYxZjY4MCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXVtv5Mh1_iuENgHsTbfE-0ULJBjPjjcLO7uTmbFjwDvoKVYVu7lik70kWxrtYAC_5Q8Efkpe88P8ECD_IuecqiLZN0ojybeYgLEedZNVp8798pX04YzVbZ4x3i5ycXZ5ttksElswN018T7iZH0ehnQROHPj8bHaWVuJ2IfKlbFp4tlkxNwgvPUf4IrYz6bsiFbEfpwnPYl9EIgmZbWdRICLHy2w_4CJ2BctYJPDHxPXtjEcC1hV5w6trWd-eXX7AH9pFy5awQ8Fa3GoG_0hlAR_8WtZ5lrO0kFYtr_Mmr0prBc9X9a2V3lov66rKNrVsGnhnw_gVW0o81M7HdfW9hONua1xw1bab5vLiYpm3q216zqv1BV_Jcp2Xy5aVy9izL3beruUP2xz-vdg2sl7wqmxkCbxo6638ODtbSYZMtJkdpK5IztQnC3lNDwFz5SJwozBweOo50vEdL0q8kHtMpkhZVbd4tEWRlxIoNxIpFiKOhBAysoMg87008rPMycLYVsfR1C042zTbAg7sIp28qkVzdvnbD2d6-w9nIOWqbvBf6mspFimw_Ldn2_KqrG7Ks7dwBqMPKOB2K3LZXLCNfD8Hgsp2Lq9ZcfHiN8-ev1n84ptv_-2XL7786sXi-bffvH7z6lfP33z97TeLXzvx-RqF-imKxdq2ztNtC_JcpKzJG9xdFtmCNcDnVtJ623ZV1Uj9VV7iks1t08o1fFOyNYrZnGIGrzaoGmeX5bYo4Ex8BbKUihtpUfEreDrL0iRx_AweBzG28j2e-Cf_8_t__9___v1P4UO9CQO-C-Iz6Ju8gU9-e3Hx9tL6zPpJlV5eO_G8zdtC4hvt7Ya0jdXs7OOs38kBg0gyGezs9OI9sMb6BRBcSLGU1nNQJdAijiywYNkxCj6z7vG2pgYVEJR5hyAepUxGwn4ygvZZ0rSs3TZjPLGzJEk8kT0ZCZ9__po2vfz8c4sP39usWCOtaiNLKSyWtbK2Xr4KgnPrm8rasFxY8v0InXEUOcKO0z8aq4Tk5MbGmBXaMnSDJN4hAnydgC0ts4CVlyvwjmArVlZXazrkqBJ9Zt1ziRFNyhIRh076tJT9QsqN1a4kSAZcO2xpPS9Yvra-qtlmZbGGvuOsrMqcs8JaYuRA4TbbtBnhope4PHJ8-aS0voHoo1UMqKplVtVAd1nnEEWa3UMsifwbCDQWkiisEVrBQYKL97wnpXVf9X7YQnC9S_Vc0LzMjvYIydcMIi5EHclqvrLMSnfq2-n3RpTMl6BlMWePp-E5Ky0dwdcYzdgNQ3GhOc-vOnPecR81y0G2JWvHpBUmic3YExD4BhRmLTFc5c3aWt1uKlAhCIcW_K9kdV3dgPtq4WvrD7_7zzXqmt7QytebeoTEyGMRk8x9PIn7WpSX16zOWdmO-vvAjzjEnF0_uuM3-3Xu0KLTb43oUAju08sc8dj9nXMLZTRQImtTgDhAPpA7bnLQIKsqi1tlkWj_LWuuLMjS1puewgJcwm5ETiMncR3_seTtC2eTbyRmk2OikW7muGIvPQFfs6kaOIxZ4e5QcvD8iDjsNPVdx04fvue7d-_wte9KMM38eshm-Myy5v9osbZa5_xAVOrbnjxeCbmnKoH0w4A9nDbUELDHgjZlWnygDKAkL19ZUK1sGqAOQ5jIBZQ4QCOyCJJWi40Iyg-lF4SPYdq-epgUfdR0ozQJeZruxqKf53XT7h-yKXJ-l6KMvjgWBNI4DZj_FFTMrXe1hHoDa5kFE2wDOeEFBYFFFwSwtGtr-Oh8c_sOIm6G4rEyNmLDqSczGWbOE1B4GKlZAXUvZ3eF6yTNYsfOdv3Ivw7fthqwB1neKaeTL43IKI1i142DZGd3SMshpj6DgPUflKEBV0HjGVSW7TgJn1njr44Q4sRp6ISR8xSEvNqWJuFU1jrvrTXd5oWAiFypRzJ0ROD4f5RYBkTWj2OFRSJsTwbxU5A433FyvNrCf4FaSjO_-K6cD2inNosUsy5rno9otOR2kvgZewoazWsbrOgbFSPzzJLY9VHOG5JolYrBN1UJJdu23WxbqCXH8hpPppHnOu4REn9GJGb5e3COAvYpqg3xR76XfNtW9f207x6rjMW5IBEiiaMnJu8ZlbF7LEWJQwRY5tgdq1JscoHHqoqiuiHtLKt6DeXSWKOCCR5JVzwxtbtJLRPXDDxJrwK5Sl5BHyGHwnKmRo9DisqWY3HJzgKITOERap8rapUltqtayrkhFBPmLAdO3E_891np7gomdQKeipj9EUj9OusU1XB2BstJ-SNVpEPGg37U2pk1bC2tzQhzWcpi2xbHKP5SUbwtCkvnXhtWyuJ-_Dz98pgVsTBmbvxExKBDZ_C845pXnr188RvyQVopVZcI-fSjrKs5kHR9q6rC8QonC73IfxoiDzpqWw6SHc3THAYxRWa7LbXX6j0SPiaeoAGFvKvCOvnSWE9RYptTykfujr5CtVPoxFI02PBhAzXGiQBFDmrCDWv1Ed5wGScyTpNHUvcan8LHRc6WJaTdVqo6PqzEQr1WDUU0spsVmDODhDEvtvA9ZP5jknO9LBVB-Ejq9nWGY9dsVGVwZmPbye7GqtmWQhYhWH17VzG-__CIirAss30Z8Afu9hLCHPbR0C6FBAtd5yW21rhlcvXG0mGErLhdsdZoyT4P3s7MVOQMwgw20xYc0jo1aKBvzNRCLmLGQ5FI34-knQnbTZkdxwnDJ0HqtKYe3Fh6cGPxleRXmyovW5pD1bQTziLMTziKeIsTH6gEbgcrDKdAg0VovvTAAVFTZe0CypelrDd1rudQTepc-k4oI5cFMXdAMIEQQRq4LgMvlknmh1GccC5CLw0TlrlREjIvljywQ1skrpN4mLlin5_mSUpal777ERiNwxvXdsO5Hc89-43rXvrRpe__g21f2kiR5jgmmIIFvuM7oCb9px_-PCMo0lI1IgL_s0Kz9FPfjlkGVSdaCK0xmBppBb73OEiv6gWB44YcxwrSrDqYEOlVHzriMZtEjh94UAx6gTCbDKY-J0g_PbbRy9phGHkJc-3ET8yyg0mOXvYxoxid-VB8pIogleBI0aOCn1UtFFpFteGyk9V1V7JjWJ-rvtCwSoIkSbmGcruGhJNDIZILrHCpbQTfqmlj3t72xRN8uut3oPTLr2lT-OpIN2dGzpt1e5BDtpbwzLn1DJKBjjnYNNQJO5DH8nKwqQXVXF5Y_7xds9J6tkEPx4rz0zJK7cyzRZw6cdbJaDDFOiH6sTGUXjhJRRK6MgafEJmFB5Mpo7iPGSvpnbiIg9SzszjK3M7w-kmT3ukxYyJdtIJ0rnCVBgqjYt5ILG7yhhdVg0HbLLGt0WWjRrFt0Zc8cCxQBnAvWhmvnZBWxMq_lg082sBqAuqu1vp-CxRm2GnfFIybKKYmQrQSRh-Kbl1nykpRj9oVLQ6FEmgnLJGj5exa1RqyItby1aXWaJXIYkWNJqO7oKCCKTjYmbXB8koMFDyXpLwF3xZGlfEUqvrGJdaNCqWgfow4hwGVOL1mt3Q6jL-gtCNKmaWuI-M4C3nqGIkO5nFaoo8Zpu0PcbQ9nVtfg-QqeJ0IpRgPDGwk0CzUKjP8v7I1nIe1aKDCBDAW1XeGEmq3dTnkEgq_6p3E-Z59ajNWRFM2smFIKvFRvfQj0CSqGxSkZGt4ocixehthYuI4EKD9MJWiM8DBoPCEZY9N-fTCUSKjLGJRlFGNpSy7H_wNLfuTBnh6eZ8FgQ35QODxLo4OZnomEXzEbG6niLN0rdR15VRtPSjllIWg8oCWWzeSXckSlaqLATq_GkYBnaGStaBZGe0AVQLBQzRo_uk0g7kDSUMUuGHsdT55MDTs1P8xwz9KfKlRDOr4h9_9l_UzU5r0HgviKAY-6rlpx0AcG7YPG2BKISD2XqOhgA8vQA6CpluFVGEcVNk4m52wOVOZeFUA_5bzIxH0dABVTEVSNxC-8xai5ObcetU5Q01VlkPYZLv0FmDYYGotKJ5VZRbjfLsmKwWJFhUUaQUqbAHLUL-KQx4MfuG0sJjLEylEzBMq5klYg_HpCTMbH4PqpQMvsCGfhOLBt83Sg8lob2ifNOM07iFzkwyyaZ-F3eKDsade_DEDTNVV1vamAwTSA4LapuClG2wrg5RY2dxQsKHaNS9A30ASnCH6zEKrBsVMcygZ8GywSHP-XemeWy9IL1Wkmhf5lbSaaluDbjUbRSAwAugFnQIadeFtrA_-UUiuNAmiabFF7li34KV0Ba2-NHEQNvQgB4MIhu1G0C_1OY7pGJ5VjdR0lIPYbaU59tMrjL3wYyVu56CVGNx1aqfUHzUTubhV5eAx9UajGVhGbpJWOCIQ5UMuPFgRC1pwtTWwG_ISkNOtjk0oBmrnQhhRVppjbxdo2krrZpUTPhIhfsgFrKhnkEaCVWFTkdIZfgt-ABjX3pqUQEkL9lNJGxATGJH057BIE_FsyJCG-vQKD3qEHzo8m3YjEae0D6y8ljq41uhYKfPZFnKmFIKIRUerdAx_OiSX0q-1FDmGdAINznTeNdM9GqRLic-IRcKxQhD8keReibiT0UD1Zp2YZlo3cvXD99s6b0Su1U5mGSoZyopcHeX-3UYFNs11LgebYjaCAMe57vEqccLb6L2_K6Nz63lXT-hWuMpXuzS2_5TMAF1Ni_GjRUPcfX3gS_TWawh5u5EB_MktJYzdBl1G8l0ZU4nWVzgquUJtWtKmoJcYEMEPt3io0WyoqUB7-vDZp1BHBlHas7lBmsZJEkWiL2kGiIkTHnkM-2AykwyKWQlBOEw6lzmAQ-yUNPeBN-hlpee6ngfZrQrvqkzuEQ962UciGHaSJTAiLK-00nZwav3kbqWrHMvF0QoXPh4Utfr1YzgF0NU6f68fWJG0leKgxmAY3p9E6UcHlRad96aqr9D4G2kOrbnRaSYqfVrkKltHTn9XAueO4DdM_SsdTwSuJ73I68NgB-kY5FoPhWiUOjKwNKdki0oMOC8EEHgSQmdXbwBbtth_omry0Ci4zDdkRdjfYLstkJEERfqub3sJD5O0K48H2JAT5jCK9TD5iZ04LIaa3mZ96tPDP3p7-FQUh8mDfT_MeBInMe_WHwA79PqPwWfkxRzLd7QFKBrXTImLYpNKPzJydrsGBYFjxziGeX8J6kWNn0GrZ6_BY_IF1XA3qQSGEzj-Oc7fj5wHRL7YP1O37mJDu0k6HCS0EjJWSkzoU2U5KYTNQsUECa4Xv2-gcmghI0Dfjb1iU5ijgaloiDFV-W5CCcCPlD5j40_q00DibX39ZV8ewVLUz8FFlHfCt5SjMdl0zz8K8rpE6niIclV8wOFNc4H_XYwKFKyghjxEakRAZyuaqbMu4zFZkA7Pg0yly8TUNy1bQ-IAn35v0sTjtd2gXzhXhTsoSEl7ds7gou8lqbhL6x10-eglSj735IJqcTraSeGlfurEPAxTYyQDbNHJMv8OiJCpbhzPFX7k2m7chbwBaqg38U8BAJn2sOCRFyYud6Ke8h4T1K39AGSP2SFI0kT63JF-3zzvwT56h8dAdk51CQbJEtalZF6oUGSL5AXgBzSmy5EuGKQV0g_CKIjjrjXb44A69_cINE__Cdso5cPqEbzfXJuONnxaCBlAfaktOkz0jJLxlaXXoNPQc1qzByajM-ze2na8iqJymHbqOWiDl7S6cvbwMQ7JAdpgdSXRz-L1L6pUqFGLd3vg8aYdsR3BOV5EE1Cqd5nXAMW0B2F6CBZpq6I58gZMvjLs7T0TfGb8NLVnylZlFvLADahzqV27QrQrPnUY0TQSgEc7GCNJNUj4im1UUc0Q6YPtYVhUFz00SjAtlZGMIrR9N3L8xIvirkM3QFYdGO7DQFHGCjLIzZIwSD2n22yAk9KbPQbitJdooYrPqLuBbBq0BLFjP0hIKYlWRevg002xNVFokKzu-I8Dp7GlVj4qzmkenVs_1yidPu_vImsz0x1uPRUFVaHT9IOi2aB2Q7rpBSH16KwrnVfAsqILRJiGQESjqfNYBwzda8CZdIKuWz_Ahh1tV34arEt2fnUw-tiWzXaDhmFSqWHhPXA9qkKYqxNSqjEoPWRdQ5rXuWjdIUWfUhXGv6whpyvu6WysEhsubdW1VkesyPFlGEUQve2u8hiA1A6s6HHYMiMrkUFEDFnmxF1tPICb6U0fgxJjOQYDNZEFCX718s08OA-t1xVo2ZdSbl5LeaW49tUv_wU7HFBDNbQZZXt78zJGnv4LUg9VJBnsTEfDvN1SykqdoT7YKjrIWkB8rU7taVGw8saCFGJlGuQ4U6EGsBa1BFHjPA88p9zIUlDjmGH5MtYJdmI3y6Sb-NIODG8HwLgDgX4SuM10bT0euqkAh8g7Wxvg3QYZzUMxaya4UqtGOdJz66XpK1KeBI9V2Hwr5c38y2-f_0ZHJoEzW_oAOF5W67ykGkrP3vGYSitwBrSm9sHNSpIQDsFZ1koWGxzn3-LgTWF4hiVznkGuieNVTAelynjMaktqHjXb-hpPrhlg6lk11KNWUl_pYQNzpICWqQ0VbsJS4Q7a8Aa-dwodcRqCZ9pJTmQLkYZ25PTZaY_K63PrTwHYGefip2nkchFFMe96YD3mbuCTHwqfM64Y4-xh42mnCTnsWGm_uDdtU9E2b2B93Y_WnWxKXHp3rTjAbvFjDAnYgO9TFprcqIignLEsKZAifsJa5UtUDrZc1pJ0u-E4EeiaL1CcQl5LPfml7jZjJjaIMqpUa_ows1P5D0KnUTXSLopBx0eAIzoXJCwLshRiQxL28utQiV1m-nCAoblDT-15CFi70sPRjg6lKrNotmhxuYp5Xfreq4NJOVjRyZ7a3139rPy6GW6gNau5IuRnJW56bn1ZaXgAlN5lgyIiRMK-W9pgVdCAjpQocJA9M5WKmm5Sx6ZDRWzFUo7O7xwPImLmBVni9NlLj7A8Yd2nwZIGUuVG0stcP5BOV7wN8JOD2d09IJGmXIm9iDtQ0DKv64cNUJLmitcjgI99Z5fGBLp-gVCiux46LRwMreBDqZFWK1ZjzbyLoaCdNJLB9IHg2QJsEFcdTIBn5qm-i0pTxrpGXVOqAA6nwOIHTtU9rmK2GiLS0uzmVtZzkwErPAY-upu5dNkmkdLlaxCs0I6UfI1RqPQGg7YYjLBTPBnDYZnqEsIqRxAas_36wnBMosWA3yI2VvUSyFJ9KaxBjufcbz-iNhz5BR0q9upfz_EtmM-zr63nwJf3Z2_pd36ILT_59d4v9zj8mlAb3fevcuBgLaw3DJTzL-o3gIC3z-uKnMkCVaQ58YtAaP7w0N8D8sjfRAHKSqisIwhjpXKnNjt8X6OJX2nx6faMsv2s4tSkMRavpovie8YlQZe6CKc6MBotOYaQPFc0miN_OLtZ3Xa707vX9Mt2qDOkNv9htyXYGo_ebzQK1zHbfgL2OmSpnbi2g_O0SLhSJomIo8DvuDUEVQ8BxUOg9Yc_sdzvjx_v8NPdapfOx-MA6bvQ4k8CCY-zwHd5JAIvgJokc1OZxiGHgBSlPJV-4CYpt_3QjWO0X-EEkSttO0piGfEsoar3xJGOgcLjyyA5AgqPs9jz04xPoPC_ElB4FPsRizPJZDaBwh8FCv8aPLfjHDp71UjB9xyv9_rYjsyw9akKBj3zHwSDhsLHhDWfsOYT1nzCmk9Y8wlrPmHNJ6z5hDWfsOYT1nzCmk9Y8wlrPmHNJ6z5hDWfsOYT1nzCmk9Y8wlrPmHNJ6z5hDWfsOYT1nzCmk9Y8wlrPmHNJ6z5hDWfsOYT1nzCmk9Y878FrPkpkPkpdPkEK_-Twsqf4i_iHK598Jc_ENIZejx48r_8IZQ19c5B9dNzlVTxuoJMxU-o5dFcWu7YX_6wBU9j-UQkduQglbhG54M6CBVZnals-uLpKYH_CNjbHaLOERhrKQxuP-NWbXpgpjkv1KfgVlWKY0ikrTtg5Pkp3bnjHoJKtFSvw-wGOUEp1bTM2OJ8kHKBB9N5Eo6WTqjVnix29-zzLLNlnxao9GFmshFVPlDCpoGQ56fUZHRLQvxp7zxX4YqWkLWGJCpoBjp3apnpXEkz--7LFBrTNJBZWfUlOGnoDEfaEGQYIkLFbhaMB1RHPUJoB36FTExJ3eiAwvP2eSaVWgRzG-ILl6atp872aVc0Rv6g8dErGh28_892RWPyoX8FPvT-F4H2_wiBOxvcPXE_Hr9a8ie5TuNEocv80AmDSIY-z2QU-XYUBXHIIu5FrkjCjHtZ4NlBHEQJUCcRUc_giDZ8m97ncAcXa7xLJ7n0nSMXa7o_Sz5drPmruFjjMvB9IUtS5rj3u1jTR0sTbI6MHo-OHXGUpKugfmjwZjUs4_au_y2p0lMOaQalsiqReoehO6492Eub_aUqHJ0EkTu-r97Alsa1PMDaAm2ylseGkG6gR04Ex-9xvA0NxY5DgxFeYTxo37ubaYSjxgixvolMk1wo6oy_ghOplEAcxNWdWG3K4S7AXigYYScWGg7rEnK6nTPdzplu50y3c6bbOdPtnOl2znQ7Z7qdM93OmW7nTLdzpts50-2c6XbOdDvn_-ntHCcVKUsCFvoOn27n_A3ezrkfHwg2sWA7XMDSZVjOYW9zTozYiW80sECoa7VdrnQTFPHRA0ypyXNrBBiRDlX1wW0DKGLkztWM_TbpqeN0U1B5v2OZxKQZeBhKvRuGrQgj8s56NQzzOErHQF_otwAZ4iHWo-xKeTOEJU-3pabbUtNtqem21HRb6i_xthQ4Fzt2Iy9JO6cwABYcY9snwgP8kzO2vntCtqgbklxDL5UmHmV_8wXO52jZndncFwbAAl_Qt4dSajBf6MQx19lLIdkVVLLfKmntDQ1px-Gv2uvv_YCuOMkFPP8T3zt34r__qWo67P7-QY1zRJ4sZSmRYfu_988J99NCx9ZVGshrjRFYfbaTHKLHMgmnFIeZJDLDSywDqOzNrzNKfftBoa-wNCB34ATD8N3jn_7OPg-i0I3ge-q3mHGjpRIEAlc3XcRuqJLfS2asGpscOEGlUIkMNGrfzUm1Q8HvqNRvETE0osA8S93EjyLWRZ4B7KRT4IeDRzr0vxauHtLRXYd-8Nhgz44KAnX9aRDcOpwX_ebIS0Idg_zVdI2a2APpqftgOusFwW22zWDoO8hctD5_0WtbJ5DZbnNQdT6Vl9dzu_eqZ1SWW1bsjOS-0CBqhSyWuimnO_N6zEyty0Zi1mSao90dJfJ2mOizxtiwYhukkYxavr3ul6oyn1PDioaQVzimIpc2UFrr3T485PWbZ_DfZ4tXL17_6pdvXp-vxbvpQuh0IXS6EDpdCJ0uhE4XQqcLodOF0OlC6HQhdLoQOl0InS6E_lkvhL79-H9sZYDw)

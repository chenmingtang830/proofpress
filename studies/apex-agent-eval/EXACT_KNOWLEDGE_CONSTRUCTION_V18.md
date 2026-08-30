[//]: # (ob:ffb9914f)
[//]: # (ob:v18-title)

[//]: # (ob:1b9c9fe5)
# Exact Knowledge Construction v18

[//]: # (ob:c7bae7d0)
[//]: # (ob:v18-status)

[//]: # (ob:0f9993df)
**Status:** construction phase opened after PR55. No paid executor panel has been run for this phase. The first implementation slice defines task-prompt requirements, exact numeric evidence atoms, authority candidates, deterministic derivations, candidate readiness, and a numeric claim gate. Its 11 focused contract tests and 13 adjacent workflow and discovery regressions pass. All constructed objects remain candidates until Human Approval.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzkwZGEyYjk0M2QyZjQ4NzYwOTUxODU0YyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjhmODM0YmZjIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV82YWIwOTIwMTIyMzM3ZDJlZTk5ZDg3NTQiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Q4N2RkZGU3MDU1ZjQzYjc0ZmYxZjY4MCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXFuP20h2_iuFnpfNROrm_dILJPDaXseYzYzXdjYDjA25WFWU6KZIDi_d1hgG9m3_QLBPyWt-2D4EyL_IOXUhKbXEbrd6kyygwWCmm2JVnTrX71xan89o3WYpZe0i42eXZ1W1iC1OnST2XO6kXhQGVuzbke-xs9lZUvLNgmdL0bTwbrOijh9cpqHDqevSlAUeLKO2ZYvQDVmacOEmzPVsGvrUjRzh8ERwmzNPMBbBP7Hn2IEF-_KsYeW1qDdnl5_xl3bR0iWckNMWj5rBD4nI4cEfRJ2lGU1yQWpxnTVZWZAVvF_WG5JsyKu6LNOqFk0DayrKruhS4KW2HtflRwHX7WrccNW2VXN5cbHM2lWXnLNyfcFWolhnxbKlxTJyrYut1bX4ucvg50XXiHrByqIRBfCirTvxZXa2EhSZGKWR6yUpcgyfLMS1fAmYKxYBTazYsWzHcd2QO0LEMY9C30PKyrrFqy3yrBBAuZFIvoA3OOcitHw_9dwk9NLUToPIUtfR1C0YrZouhws7SCcra96cXf70-Uwf__kMpFzWDf6kPhZ8kQDLfzrriquivCnO3sMdjD6ggNuOZ6K5oJX4NAeCinYurml-8fzHJ0_fLr77_od__d3zZy-eL57-8P2bt6__5enblz98v_iDHZ2v-dnsqxSLtm2dJV0L8lwktMkaPF3k6YI2wOdWyP26dlXWSP1VVuCWzaZpxRo-KegaxWxuMYOlDarG2WXR5Tncia1AlkJxI8lLdgVvp2kSx7aXwusgxlZ8whv_6r_-_Kf__s8__x081IdQ4DuXfAZ9Ezfw5KeLi_eX5BvyqzK5vLajeZu1ucAV7aaS2kZrevZlNpxkJzGLU-FvnfT8E7CGfAcE54IvBXkKqgRaxJAFBLadouAbco_VmhpUQFDmLYJYmFARcuvRCNplSdPStmumeGKlcRy7PH00Er799o089PLbbwkbr6tWtBGkrEQhOKFpK2ry6rXvn5PvS1LRjBPxaYLOKAxtbkXJX41VXDDpxqaYFVgicPw42iICfB2HI4nZgGTFCrwj2ApJ63ItLzmpRN-Qe24xoUkpOK_ATh6Xsu-EqEi7EiAZcO1wJHma02xNXtS0WhHayM8YLcoiYzQnS4wcKNymS5oJLrqxw0LbE49K61uIPlrFgKpapGUNdBd1BlGk2b7EUpJ_A4GGIImcTNAKDhJcvOs-Kq27qvdzB8H1LtVzQPNSK9whJFtTiLgQdQSt2YqYne7Ut8PrJpTME6BlEaPH0_CUFkRH8DVGM3pDUVxozvOr3py33EdNM5BtQdspaQVxbFH6CAS-BYVZCwxXWbMmq01VggpBOCTwb0HrurwB99XCx-Qvf_z3NeqaPpBk66qeIDF0aUgFdY4ncVeLsuKa1hkt2kl_73shg5iz7Ue3_Oawzx1adHjVhA4F4D7d1ObHnm-fE5TRSIlIlYM4QD6AHasMNIiURb5RFon239LmigBKW1cDhTm4hO2InIR27NjeseTtCqfKKoFocko0wklth-_AE_A1VdnAZcwOd4eSW-9PiMNKEsD-VvLwMz98-IDL3hVgmtn1mM3wjJD5PxDaluuM3RKV-nQgj5Vc7KiKL7zApw-nDTUE7DGXh1ItPlAGUJJXrwlkK1UD1GEI4xmHFAdoRBYBaCV0QlBeIFw_OIZpu-phIPqk6YZJHLAk2Y5Fv83qpt29ZJNn7C5FmVw4FQSSKPGp9xhUzMmHWkC-gbnMgnJaASa8kEFg0QcBTO3aGh6dV5sPEHFTFA9J6YQNJ65IRZDaj0Dh7UhNc8h7Gb0rXMdJGtlWuu1Hfj9eTRqwB1HcKaeDiyZklISR40R-vHU6wHKIqU8gYP2bRGjAVdB4CpllO03CN2R66QQhdpQEdhDaj0HI664wgFNZ63yw1qTLcg4RuVSvpOiIwPH_IjANCMkvU4lFzC1X-NFjkDjfcnKs7OC_QK2Emb9-V8xHtMsyi-CzHjXPJzRaMCuOvZQ-Bo1mWYUZfaNiZJYSgVUf5bwBRCsoBp-UBaRsXVt1LeSSU7jGFUnoOrazh8TfSBLT7BM4Rw7n5GUl-SM-Cda1ZX0_7bvHLlNxzo85j6Pwkcl7ItPYHZaixCECLDOsjpUJFrnAY5V5Xt5I7SzKeg3p0lShgnIWCoc_MrXboJbyawqeZFCBTIFX0EfAUJjO1OhxpKLS5VRcslIfIlOwh9qnilplie2qFmJuCEXAnGbAifuJ_z473Z3BJLbPEh7RvwKpL9NeUQ1nZ7CdEL_IjHTMeNCPWjuzhq4FqSaYSxMaWRbfR_EzRXGX50Rjr4oWIr8fPw8vnrIiGkTUiR6JGHToFN63HbPkyavnP0ofpJVSVYmQT7-IupwDSdcblRVOZzhp4Ibe4xB5q6LWMZDsJE6zKcQUkW6X1N6odVL4CDxBA3JxV4Z1cNFUTVFgmVOII09HX6HKKfLGgjdY8KEjNcaOgIwcsgg3ztUneMNEFIsoiY-k7g2-ha_zjC4LgN0kURUfWmCiXquCIhrZzQrMmQJgzPIOPgfkPyU5x00T7gdHUrerMwyrZpMqkwrPsax4-2BVbEsARXBab-5KxndfnlARmqaWJ3z2wNNeQZjDOhraJRdgoeuswNIaIwarN0SHEWnF7Yq2Rkt2efB-ZroiZxBmsJi2YADrVKNBfmK6FmIRURbwWHheKKyUW05CrSiKKb4JUpd76sYN0Y0bwlaCXVVlVrSyD1XLk7AXYX7DVsR77PhAJrAZ7TDuAo02kf2lBzaImjJtF5C-LEVd1ZnuQzWJfenZgQgd6kfMBsH4nPuJ7zgUvFgqqBeEUcwYD9wkiGnqhHFA3Ugw3wosHjt27CJyxTq_7CcpaV16zhdgNDZvHMsJ5lY0d623jnPphZee9_eWdWkhRZrjCDA59T3bs0FNhqef_29aUFJLVYsI_M8KzdJLPCuiKWSdaCFyj1HXSCvwvdtBelfX920nYNhWEGbXUYdI7_rQFo85JLQ934Vk0PW5OWTU9TlA-uG2jd7WCoLQjaljxV5sth11cvS2x7RiNPKR8VFmBIkAR4oeFfysKqHIXVQZLj2YXfcpO4b1uaoLjbMkAEnKNRTdGgAng0Qk45jhyrIRfKq6jVm7GZIneLrtdyD1y67lofDRnmrOTDpv2p8hHTJZwjvn5AmAgZ45WDTUgB3Io1kxOpRANpfl5J-6NS3Ikwo9HM3PD8sosVLX4lFiR2kvo1EX64Dop9pQeuM44XHgiAh8Qmg2HnWmjOIe01bSJzEe-YlrpVGYOr3hDZ0mfdIxbSKdtIJ0rnCXBhKjfN4ITG6yhuVlg0HbbNHV6LJRo2iXDykPXAuUAdyLVsZrO5A7YuZfiwZebWA3DnlXSz52QGGKlfYqp8xEMdURkjth9JHRra9MkQT1qF3JzSFRAu2ELTK0nG2rWgMqoi1bXWqNVkAWM2o0GV0FBRVMwMHOSIXpFR8peCak8uasy40q4y1U9o1brBsVSkH9qOQcBlTJ6TXdyNth_AWlnVDKNHFsEUVpwBLbSHTUj9MSPaaZttvE0fZ0Tl6C5EpYLgmVMR4Y2AigmatdZvi_ojWch71kQ4VyYCyq7wwl1HZ1MeYSCr8cnMT5jn1qM1ZESzRSUSRV8lEt-gVo4uUNClLQNSzIM8zeJpgY2zYEaC9IBO8NcNQoPGDZU10-vXEYizANaRimMsdSlj00_saW_VUNPL29R33fAjzgu6yPo6OengGCR_TmtpI4onOlviqncutRKqcsBJUHtJzcCHolClSqPgZofDWOAhqhSmtBszLaAaoEgodo0PzjYQYzG0BD6DtB5PY-edQ07NX_mOafBL6yUAzq-Jc__gf5jUlNBo8FcRQDn6y5accgOTYuHzbAlJxD7L1GQwEfnoMcuOxu5UKFcVBl42y2wuZMIfEyB_4t53si6OEAqpiKpFYQvrMWomR1Tl73zlBTlWYQNuk2vTkYNphaC4pHypRQxrq1tFKQaF5CkpajwuawjaxXMcDB4BcOC4s6LBacRyyWybwU1qh9esDMptugemvf9S3Ak5A8eJbZetQZHQztq3qcxj2kTpwCmvZo0G8-anvqzY9pYKqqsrY3HSCQHhBUl4CXbrCsDFKiRXMjg43MXbMc9A0kwShOnxG0alDMJIOUAe8GmzTn7wrnnDyXeqki1TzPrgRpyq4G3WoqRSAwAugFnQIadeJtrA9-yAVTmgTRNO-QO2QDXkpn0OpDEwfhQBcwGEQwLDeCfqnn2KajeFfVUtNRDmI3STKsp5cYe-HXkm_moJUY3DW0U-qPmolc7FQ6uE-90WhGlpEZ0ApXBKI8wMKjHTGhBVdbA7sBl4CcNjo2oRhkORfCiLLSDGu7QFMnyM0qk_OROOKHXMCMegYwEqwKi4oSzrAN-AFgXLsxkEBJC85ToA2I8Y1IhnsQqYl4N2RII-v0ah50Dz90eDblRkmc0j6w8lro4FqjY5XIp8vFTCmEJBYdrdIx_O02uRJ-rQXPMKTLocGZxl0zXaNBupT4jFgEXCsAwe8B90rEvYxGqjfrxTTTupGpXz52ddbwTKudSFNUMpSVdHUS-_cH5Vg011gODkU0ggOOc13jVeKE1ei93xXhOXna5xO6FK7wag9jh6fSDNDVtBg_WjTE7eUjX6KPXkPI244M4E82EjD2B_SI5F0RyRRtyHAUuEJtWspDQS8xIIIfbvFSk2ioKUF7hvA5QKg9jSjt2Rw_SaI4DkM-pDSjiYkDHnlq9sEgkxSSWQFBOIh7lzkah9hKae4z3qC3FS5O9wK6VeFdpcnDxIPe9sgJhi2wBEaE6ZVW2n6cWr-5nekqx3KxN8OFx6OkVi_fN6cAulpnn_QLKyltpTioMRiGdztR-tVRpiXve1PWV2j8jTCX1tzoNROVPskzhdaR0-8K4Nye-Q2T_wrb5b7jCjd0hzDYj3SMsNZDRzQKHRlokkmwJVMMuC8EEHgTQmefbwBbOqw_yWzytlEwkVXSirC-QbdLIBMARXiOZ7kxC-KkT49HsyEHzGFy1sPgEyu2aQQ5vUUH6DOMfwz28LVTHAYHe16QsjiKI9bvPxrs0PsfM5-R5XNM39EWIGlcUyUuGZsU_Eils9s2KAgcW8Yxxv0FqJcs_IxKPTsFHoMXVMHdQAkMJ3D9c-y_77kPiHyxe6d-30UlTxPycgBoBSBWCUzkU2U5CYTNXMUEAa4XP28gc2gBEaDvxlqxSczRwFQ0xJiqfLecEoBfJXzGwp_QtwHgTV4-G9Ij2ErWc3AT5Z1wlXI0Bk0P_JNBXqdIPQ9RrooP2LxpLvC_i0mBghXUgEOEngjobUUzddYjHoOCdHgeIZUeialPWroG4ABPPxqYuD-3G9UL5ypxBwUp5Jm9M7gYakkq7sr9blX55CIJPnfkgmpxONoJ7iZeYkcsCBJjJKPZooNp_h0jQia7sV2He6FjOVEf8kZTQ4OJf80AkCkPcxa6QewwOxwoH2aC-r0fMNljTvDjJBYes4U3FM-HYR99wjEjO4eqBCOwhHmpNC9UKGmL0gvAL2hMlxNVMIAVwvOD0I-ivjQ7zAH17u-IaZ7hCa2U8mH2CN5vrk1HG77cCBkg61IdOkz0jIKyFdF7yNvI97Rmj0xGI-zB2ra8iqJyDDt1H7TBP9Lq09nbrzEAB2iD5ZVAP4t__iUzFVmoxb_tgdebdsJ2OGNWKjwOqXqPvEZTTDsjTA-ZRepUNEfegMmXhr2DZ4Jnxk_L8kzRKmQhbrkBdS91ap-I9smnDiOaRjnAox2MkaRqJLyglUqqKU76YHkYNtVJj2wlmJLKBKIILM8JbS92w6iv0I0mq24Z7sOGoowVpIDN4sBPXLs_bDQnpQ87ZsRpB2ihis9kdQPZNCoJYsV-BEgliFZJ6-hplXcmCo3A6pb_uOU0OlnKR8U5zKNz8ls9pTPg_j6yNjNd4dZdUVAVeZuhUTQb5W5It1zAhW6d9anzCliW94EIYQhENNl1nqqAoXv1GRW231frR7Nhe8uVXzfWJXq_Omp9dEXTVWgYBkqNE--R61EZwlzdUEKNUeoh6hpgXu-idYUUfUqZG_-yBkyX39PZkAILLm3Zl1YnrMj2RBCGEL2tPvMYDandsqLjZsuMrHgKETGgqR31ufFo3EwfesyUGM0wGKiOLEjwxau3c_88IG9K0LJnQlRvhLhSXHvxu3_GCgfkUI08TKK9nX4ZlZ7-11I9VJJkZmd6GuZtJyGrrAwNwVbRIa0FxNdqaC83BStvCECIlSmQY09FFoC1qAWIGvt54DlFJQouC8cU05epSrAdOWkqnNgTlm94OxqMuyXQrxpuM1VblwVOwsEhst7WRvNuI0Tz0Jk1E1xlqUY50nPyytQVJU6C10osvhXiZv7sh6c_6sjEsWcrHwDHi3KdFTKH0r13vKbSCuwBrWX54GYlpBBuD2eRlcgrbOdvsPGmZnjGKXOWAtbE9irCQaEQj9ltKYtHTVdf4801A0w-q5p6spQ0ZHpYwJxIoEViQYYb04Q7ozK8Gd87NB1xeATPlJPs0OI8CazQHtDpMJU3YOuvGbAzzsVLktBhPAwj1tfAhpm7kU9-6PicccUYZ28XnraKkOOKlfaLO902FW2zBvbX9WhdyZbAZXDXigN0g48xJGABfoAssnOjIoJyxqKQgRTnJ8gqW6Jy0OWyFlK3G4Ydgb74Askp4FpZk1_qajMisVGUUalaM4SZrcx_FDqNqkntkjFofwtwQuf8mKZ-mkBsiINBfv1UYo9MHz5gaP6GXpbnIWBtSw9bOzqUKmTRdGhxmYp5PXwf1MFADpr3spfl7z5_Vn7dNDfQmlVfEfBZgYeek2elHg-A1LtoUERyImHXLVWYFTSgIwUKHGRPTaaiupuyYtNPRXR8KSb7d7YLETF1_TS2B_QyTFgesO7Dw5JmpMoJhZs6ni_sPnkbzU-Oenf3GIk06UrkhsyGhJa6fT1sNCVp_sTriMHHobIr2wQ6f4FQoqseGhaOmlbwUOhJqxWtMWfenqGQJ-lJBlMHgndzsEHcddQBnpm3hiqq7DLWNeqaUgVwODkmP3Cr_nUVs1UTUW5NbzainhsErOYx8NVt5NKjTUlKj9cgWKEdKfkao1DwBoM2H7WwE7wZxWaZqhLCLnsmNGa7-YXhmECLAb8l2VjWSyBL1aUwB9mPud9_QW3Y8wUdKvbqr-f4AcznyUvyFPjy6ey9_M4P3rGDH-98ucftj-XURv_56ww4WHPyloJy_r_6BhDw9lldSmeyQBVpDnwRiOw_PPR7QI78JgpQVjmVtWfCWKncocNur9fTxK-1-HR5Rtl-WjJZpDEWr7qL_CNlQo4u9RFOVWD0tOTUhOS5otFc-fPZzWrTny7XXssv25GVIXX4z9slwdZ49OGgyXEdc-xXzF5PfFuO4tZ4qHo8UDwetP78vyz3-8-P9_PT_W6X9pf9A9J3TYs_ykh4lPqew0Luuz7kJKmTiCQKGASkMGGJ8HwnTpjlBU4Uof1y2w8dYVlhHImQpbHMeg9cad9QeHTpx3uGwvtvTzoNhf9tDIWHkRfSKBVUpKeh8KOGwl-C57bt285eFVJwne0OXh_LkSmWPlXCoHv-o2DQyPBxmjU_zZqfZs1Ps-anWfPTrPlp1vw0a36aNT_Nmp9mzU-z5qdZ89Os-WnW_DRrfpo1P82an2bNT7Pmp1nz06z5adb8NGt-mjU_zZqfZs1Ps-anWfPTrPlp1vw0a36aNT_Nmp9mzU-z5qdZ87_5WfP3X_4Ht7aGEQ)

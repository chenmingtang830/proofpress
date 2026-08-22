[//]: # (ob:58635848)
# RelayBench H4 Phase Zero calibration protocol

[//]: # (ob:c7f229eb)
## Status and role

[//]: # (ob:0b5a7b86)
RelayBench is the execution, parity-audit, scoring, and reporting layer underneath Richard Tang's proposed Proofpress long-horizon research plan. It is not a competing benchmark protocol.

[//]: # (ob:f5f1834f)
This revision is stacked beneath Proofpress PR #22 head `10ee8c4c9a6d56dfedf563a0679e6a5bb167fa0a` and prepares one H4 C1/C2 Phase Zero calibration with deterministic test doubles only. No real or paid model call is authorized. Calibration output is always `TEST-ONLY`, is excluded from benchmark metrics, and is not a benchmark result.

[//]: # (ob:91ca81d4)
The complete freeze-review surface, upstream source identity, proposed stage chain, and unresolved decisions are indexed in `PHASE_ZERO_FREEZE_PACKET.md`.

[//]: # (ob:4992820d)
## Claim boundary

[//]: # (ob:5a786447)
Proofpress is not being tested as an improvement to legal knowledge, clause drafting, retrieval, commercial judgment, or model intelligence. The intervention is version-bound carriage of admitted decisions and evidence across a boundary. A receiving agent remains responsible for legal reasoning.

[//]: # (ob:de8ac702)
Proofpress verification may establish only the properties supported by the pinned engine and carrier. It does not establish factual truth, legal correctness, completeness, authorship, identity, or authority outside recorded admission state.

[//]: # (ob:0e8d3a4f)
## Calibration unit

[//]: # (ob:5a350d37)
One paired calibration unit is one candidate Harvey contract matter executed in two conditions:

[//]: # (ob:3b9882b0)
- `C1_ORDINARY_PORTABLE`: a complete ordinary portable matter workspace.
- `C2_PROOFPRESS`: the same substantive files, fields, instructions, tools, stage timing, and budget, with Proofpress representation, bindings, and verification affordance.

[//]: # (ob:ad281c0a)
The active horizon is H4: four consequential stages, exactly one session/worker boundary before stage 3, and no branch merge. H8, H12, H16, C0, the 72-run pilot, and real execution are out of scope.

[//]: # (ob:ef9ee785)
## Candidate matter and calibration fixture

[//]: # (ob:7e627c8a)
The recommended candidate is Harvey LAB's MSA playbook-escalation scenario recorded in `bench/fixtures/h4-msa-escalation-candidate/candidate.json`. Its exact upstream identity is recorded in `HARVEY_SOURCE_MANIFEST.json`, and its intermediate criteria are recorded in `proposed-intermediate-rubrics.json`. The candidate, release schedule, and intermediate rubrics are not frozen until Richard and Tommy approve them.

[//]: # (ob:e028575e)
The executable local fixture under that directory is a small synthetic state machine. It is labeled TEST-ONLY in every file. It tests orchestration, information parity, cold boundaries, and deterministic scoring mechanics; it is not Harvey content, a legal task result, or a difficulty calibration.

[//]: # (ob:cceb291d)
## Deterministic stage schedule

[//]: # (ob:5d06e74b)
The controller releases stages in the only valid order: `S1 → S2 → S3 → S4`.

[//]: # (ob:870ae1fe)
- S1 and S2 must use the same worker process and workspace.
- Before S3, the sender worker must exit, a new empty workspace must be created, the declared transfer package must be copied, the sender workspace must be removed, and a new worker process must start.
- S3 and S4 must use that same new worker process and workspace.
- Skips, repeats, an early worker change, a missing boundary, a third worker session, or a failed boundary audit are rejected deterministically.

[//]: # (ob:7fd8009c)
The test-only stage worker receives only the common instruction, current stage identifier, its isolated workspace, and (for C2 after the boundary) verifier evidence. It has a minimal environment and no Git repository, sender ledger, transcript, conversation, hidden memory, or orchestrator state.

[//]: # (ob:4e5382bd)
## Information parity

[//]: # (ob:95a708f5)
Parity is evaluated on complete paired input packages, not on a hand-picked visible snippet.

[//]: # (ob:ab307e7e)
The machine audit:

[//]: # (ob:859088bb)
1. inventories every file in C1 and C2;
2. requires byte-identical common substantive files;
3. canonicalizes the substantive path/hash projection and compares its SHA-256;
4. rejects any arm-only path except the enumerated C2 portable carrier;
5. validates that the TEST-ONLY C2 carrier contains only bindings and representation metadata;
6. verifies every carrier binding against the common file hash; and
7. verifies that the carrier's declared substantive-projection hash equals the C1/C2 projection.

[//]: # (ob:a6e9904e)
The verifier result is a permitted affordance difference and is not included as substantive matter content. A legal conclusion, recommendation, hidden rubric fact, or substantive summary in the C2-only carrier fails the audit.

[//]: # (ob:0d53fd4b)
The machine audit proves equality under the frozen projection and allowlist. It does not replace the required human semantic-parity review before real calls.

[//]: # (ob:9698918b)
## Stress-track separation

[//]: # (ob:5487cfa8)
The three concepts remain distinct:

[//]: # (ob:9c71f911)
- Clean continuity: ordinary negotiation plus boundary changes, with no deliberate fault.
- Evolving negotiation state: legitimate new positions, business instructions, approvals, and reopened issues. This is the active H4 calibration track and Richard's primary product track.
- Integrity fault: stale, mixed, missing, or corrupted provenance. This is a separate robustness track and is not executed here.

[//]: # (ob:1c9457dd)
No result may pool these tracks. Detecting a corrupted capsule cannot by itself support a long-horizon efficacy claim.

[//]: # (ob:e1b03f5a)
## C1 and C2 procedures

[//]: # (ob:6517c5ff)
C1 receives all ordinary matter releases, prior work product, and a readable handoff state. No Proofpress verifier evidence is available or implied.

[//]: # (ob:01c27143)
C2 receives the byte-identical substantive package. A portable carrier binds the same files and readable state. The harness runs the pinned verifier before the fresh receiver acts; the TEST-ONLY calibration substitutes a clearly labeled deterministic verifier. Formal execution must replace that substitute with the approved pinned Proofpress engine without changing task substance.

[//]: # (ob:70cf9417)
## Scoring and reporting

[//]: # (ob:9a260ff3)
Scoring is deterministic after evaluator inputs are fixed. It keeps these families separate:

[//]: # (ob:b29ea001)
- final legal-work-product all-pass and criterion pass rate from the existing LAB evaluator input;
- unsafe state propagation in the final work product;
- stage dispositions and operative-version selection;
- recovery/revalidation work;
- false stops and unnecessary revalidation;
- latency, turns, reads, tokens, provider cost, and Proofpress overhead;
- invalid/incomplete/inconclusive runs and reasons.

[//]: # (ob:48ed9bb4)
Horizon degradation is unavailable in an H4-only calibration. The test double does not run or simulate the LAB legal evaluator; legal-quality metrics remain unavailable. Its state-consistency checks are marked TEST-ONLY and excluded from published rates.

[//]: # (ob:01f1a3d2)
## Invalidation

[//]: # (ob:d2071a98)
A run is invalid if the frozen-file check fails; stage order or release hashes drift; the required cold boundary is absent; the transfer contains undeclared state; C1/C2 parity fails; C2 verification evidence is missing, malformed, unpinned, or non-`ok` in this clean mechanics calibration; adapter route or model metadata drifts; fallback occurs; required telemetry or records are missing; or TEST-ONLY output is placed in a publishable location.

[//]: # (ob:f1245585)
Invalid, partial, timed-out, and abstained attempts must be retained with their reason in any future real ledger. Missing evidence can never produce a green result.

[//]: # (ob:8733cda4)
## Freeze gate

[//]: # (ob:238518e3)
`BENCHMARK_MANIFEST.json` is a frozen-manifest candidate, not an approved preregistration. It records twelve classified freeze decisions. Real adapters remain blocked until every approval-blocked and provider-dependent field is resolved, the Harvey and Proofpress source pins are approved, the candidate matter and H4 composition are approved, human semantic-parity review passes, and formal execution policy is preregistered.

[//]: # (ob:e6a9ef2f)
Provider fallback and cross-provider retries remain disabled. RelayBench will not choose provider/model settings to make the readiness report green.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2UwODAyODRlN2RjNjhkNjc4YzQyOTgzYiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImU1Y2E1NzEzIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9iMjY3OTQ2MWU5ZDc0ZGJhYjkxN2EwYzUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhjYmFlZGZjMzQ2MmYwZDdhYWFjMWE0ZiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXFtz20aW_iso5SEztaSE-0V-UjTKyjVJ7JK8U5VMUlSjuyEiAgEGF9m0K6_7A_Yn7i_Zc043gKYkQzLpra3Z4ktMEeju0-f6nUv46YjVbZ4x3i5ycXR6tF4vpB3bbuzLSPAwFmEUc99NYi89mh2lldgsRH4rmxbebZbMDcJT25F2FgrPcVjqpNx108BOmOdHNnNgMQu9gDksE3YUO0kYxwlsyhzpOSJJIzuwYV-RN7y6l_Xm6PQT_tEuWnYLJxSsxaNm8CGVBXzxD1nnWc7SQlq1vM-bvCqtJbxf1Rsr3Vhv66rK1rVsGlizZvyO3Uq81NbXdfW7hOt2NW64bNt1c3pycpu3yy495tXqhC9lucrL25aVt7Fnn2ytruUfXQ6fF10j6wWvykaWwIu27uSfs6OlZMhEGXAWRI53pL5ZyHt6CZgrF6kbRokfOjIRkS9SliZOxGweIGVV3eLVFkVeSqC8l0ixiHnKpMi454duZouIMcYd5mfqOpq6BWfrpivgwi7SyataNEen__x0pI__dARSruoGP6nHUixSYPk_j96sZXn22jqvhPxw9BtcpFcKlHLbiVw2J0VV3s6XVZ1_rMq5vGfFSS0LtkllyZcn3138dH7549nV3xdvr968e3P-5ofjlTiafZFysbat87RrQaaLlDV5g4fLIluwBnjdStqva4EEvMFdXuKWzaZp5QqelGyFot66yQzWN6gjR6dlVxRwL74EoUrFlrSo-B0sCWLQ0NiP4XWQZys_4K2v8G7f4d2sS996u2SNtH6RdWVxVuRpzZBKC3gPizQlTAgicY2KKd_DN99YL92lrXhVwNp2s8ZLoNKAAh79ORup5FHmuolMt6i8blnbNRYrhVVXIPkpYr6xHr89cZ6dBixK43DX84yr543VLqUlP0hO0p1Za1bn7WbOQLPamQW2X8PxM7WvXFcjZfAi2yIrCzIn9kjzdyLrHXiL0XXA56YFNyGFBXosWbs0XIj19sr6xnUt5I5149hygiw_SdzYtcUWWecFy1dWWnWlYODapoXz6OUJ2YBk4tD3ox1PM64IDCirFi4PR1joa4ETDDlp5SvQy3u5AtdhtZVVyFtWWHflBA-EjBmPbHd_qu7Jy3NlHiu2sYAwcIx5s7SqstiQNgF1a_AK4Jmsppugypax8NgDhTk3zK8r8_Y52Tx-fVI6XmALL9r5xDclXI9BlBFbfgKXocAqeMxB13MB0dG6ZPW93Fh4Uo0O-_Oc8NIkjt3U3pmuuXVz7izeXP3t9U9nVz8v3r65enf23Q8XN6cWg_NX60ICPRBW8hJEbfXRDATYtobtgBjbLbqYcGOH22xnut6BOsDV83tp6fiEbLr0T62s6mqLgvQfHShyDioMmgQBYAbeCJYUmwl-ySyRMoqDB3T1jKdr1eR0TCll-Ye2q-WzGvXibSY0LZKhG_GYfXUKkaMIEVZg_oLUsN8TGas07oez775trB-vz6w1woCqupvLBs6Z4iiE_iAK5P8KvSq8kMbBcSBpvQ7UR8Cu7ZK1lgCj4gQW4R7MalasmKKXc5m6ibPt1f8GWl4DPgQ1zrlSJ4hgSym6ZwPwM0unfIqwQxn56VehBLlF_qIqCuAMwDgJwKTRpmHlJTlY8rQA83KBNi3rU-vm2rEmuBUD4JdOJr8KjXMLDkNNuHatVde0FuBtIqsBnGe9r-o7oBxiAMd4ge_hVw1Afnn8aznhbKJMxLad8K_GSAyac-KVWqdJAz2T4JCaMWChNaFnKhtIFiYdtS8DDxz1ttq9LrOqXmnESPDpGWV7csGEiiWAKuw4C_Y49S29gbaF-UHHEE3AwiE26KCWl-uutXR6Bq4YEcgU5mOpZ0cykntQhpJaMb6ExMoi1Hk6pchBYsdxmu5xnnMMt8S0C-KRRHZAbgsOCXwTWNe50uxz99WvpXts9SklJLCtnOdiMlaGMklsf19WKIBFagoZY6u84RptoCUEmMGGgpVcgsfMMllL_Ag0T-EsEXiZ8NOvKSSLICiw748O_BBoVu_KpZXV1UdJuRMm8_mU-iRhEidO_DBzQqQ5R8x0ZzUSFyGVz2ZQn1s15bv9OOIZi_c9n7zNspbkvLlct5jIrBgoFFZM8pJPKnXCIydLHGdfKuaQqUhWUgDJyw6kcjpivlLeVoCylLwLSMl64G9R4j2h2A5P_CASYl_yfqp6nca8YV1VBaoLxg7cpDmmGAwKA-kOgta67tYtAZz1ZBYhndT2suAB0urtWAUiAWCjeQ73Pb1kQnvCwIl4kGV7nQzvDwEJIM8oMA25eggAmXmdVzUFMdxaTAcq2-Fu5PjefrS5I21o2b0XBPVCFNd0KQTWktC9DhnH1pnOLiZoi2yeJb6znYVdq0rDUGioURGes_nPrJkKpcwN7Szz9ju7XwDOWWwBFJahzHSIBWlRPAXBAtYFzCvFsfV6gjGAaCWzbWc_4uZwVAniobrAHPVlrvUFFWy-ZhqWcXD6EGzI_8NXNeL8CTfgx1IkaervR9ylzgKFvK2ZUO4IuNiV7J7lBaUI4DXBiV36CroZ6cakumcO84T7IMQRRn5J9Hjw6oQCCdeOHJbEO510ZtUd3TdXC6w8M0LmnFAIgFtwqRlwo3mlgSuB_KnKm-P6QRAHO9Gk36PKH6bhM6vNV1LMq65VZT-GVg6BHz6BR1phcCPYn8rplMPzuGDb6vI9hMiP0rpl7XP52PabE_JwvThwYuntcs7NWBv_8eyn199fXL87_r2pyhuFurRUVqzMM0glxlQbcfFURApZIjM324WktwCrckRSGdhqisFVmWoFwXbdP6tlS9h1xBhoOI8g4G-zvr9wBKgSq6oLXkumyvX0pK_9ywVn0nUS7rlg44lMHDcKIg8yMizfVy3t2ReNdAtEKeq6ysuWOjo1nYTF_P4vrOX_hr2TIucbYwezn2JsQp2aHVstTZW1C3B7t7KGMKk7Ok3qnLJARin4fC_zhbQjkUUhKFEESTt3EpfxIHZd6YYQxv0AC9iMR7HMPM5834dXMBkF7W-pM6Okdeo7fwKjsQXi2m44t-O5675zvNPAPvXcf7PtUxvreJrjCDIBO4VpGoGOjN9--j_p45CGqhbLkjVLrDxmYRYknuPEHJ0n7WF0XbTyfpV2iT7Rdp1QJAISWun3JxodlP7EF_ZE-k39KBHc5kwQrKBNjTbJ487RFzc-KLJZsB7sj3Id1ZO4ygE-18J6Bxj624ZK31UDrtIomZtSRQQsWQ0ErAtWAhpo-zq_qtNKOoUEvmIK6BFHj59wN_rqWWi7aZolIuV2f3WjFaOvvk9zRYIG8YSFIghFBgYYhB6zwygBPxekqRNGGbPZDXEKNkDbV5VwUJRz5wRA5GfU5X0O527jJyzZWKLqwP5VfebYorSBITDGIoWwVpWQBe5TkJemrmP-EaGVWZiG6IWVDHyjeM82jXXzDrz7_M1PP_x8M6MyyAdedFhABS-_Mji-Qt_KGyX4QTbjc5XCTMjDcyPpZRCQpRP38jB6UKN-v6StpPdkNqCOhHGwYjFY6dhp0nvu0zyq3kMAuYXIxguG9TxRA5QlA1DB5h6BAVWda461-t87cYt7zFAuSiTgdmVR5LdYkTi2MCXGb2qMM1rntPeb051BhHWdE7zJLCZ0fUNITiqq7F5ivKMCB0VAFIRmFyYaKjch-HmL11HhENW8WcMOOQarDMhTdwQlgtAOb0_ILvXTILOjIEmywZaM3tljPn9xO2yNngTNTj_LSwRWsrylykrPFVmTaxCVVHIcd0VP38FtIFa2y5m-GibLkDmXQNFsKOmpv5R9NMt8DVpPmVu7IZlpw2k3aCoNPLL6wQMSBvXm0Um0coJfIeN2BplcGkg-uN2xq2fo-ovadL0FOTzjLs-knfJR24fOnd51n1Zcn1wr9091T6t9X-Fz8P6ofqefv7SQzHPSOJE-FfuIPKOBp8nbpyNXb5XMcScXg_6b799eXVxfwxZDtd1MwTF7AIlnuSwE_NtXs_E2gOmrqoB_VD4BAH-IbSkYsgQzJmdsaDY4coxVZctUeEwBscIi7Ri39H6sSR4_kT9qrkkIR54TeJ4Mg55rRntxCFO79wtJ5Hqq5ETX-ociVyqBRqnv76lLlJUFWoNoALwa1i4u45l16bj4n3BmndszYnTkzjFrW-dF1fZ4AE4foANl92BE6McANqynDCZy7cAJYgBcntdzwWhmmgazTxdygAYxpIY8AGQf9qcZjUmD57t2FBUtDZegxXk1uhCwpxsFWzWdzcnSn68aZiybDwedDJ9U-oXOr1Fitbo1qLFkq8F7WQRkjHMuz67-cfHz4vrNf1ydXzxI5HQYbxsViyCvzfFiuvTBSHRbm_UAbm6-D_JPERT01FGXbkwGdYlu6EvpQ80D9QZ0Hjp0XSPv4EbFgCFx1TsQw8ZiawrSqH6rCW2SQRzJQHq27w_yNRq5hnx37cBazaYEInTvrR2aAD1ypeE_YN0ArpCJY0uFXkP4Af4YQC98qLU7yR-1HzByFaK32FxqT7ONDzUsB4PFqjVw9JWVDxDacPKETJgOjy1retymQh-1TnIOf2_VlyY4DflgFnmMQSaVDUnL2IIe7fbL-8h90PO8LOaJD2l4OgS9sbVsyHLX_vB__-d_YcuW_vHUP_7NxJ1FbEN0z6KMU2uCKDIayUOc26MbPLe-U3752lO-tpGkj3oZ7Sc_5CTLUr63sPq0GXcY6lC6rKH2AAhZMIQFoGxlk-Hxqjg9vl6t8_5t48TtPQFNggkKXQOj4x_cht4EztctXQWYSnzwTT6AXREjnlj-mBnXd_m6QX-yhuuQ_luQLBabfqUakURmEEDDTFHHN_yuXea16F_VcVDrO1YTpRijoWrhKeeHTTr5wM7A8jcTsdxLg8hngRNm7gCTje69oau7tuCJdN7VWEbSS5X_x9boTDn0piqojT3wUInqLwj5IelUpXhqW-hr_3VsrvaJBTmoJWZGFt59hXG9vM_rqqQESaOEf89bqgE0ObrHWa8zlDEBNaRnEFLWLfqwErMc7eWWuYBjwFutaB0QNrpB-OM5eI2hO3B9Jw6zoaphTCCMXuelAwV63yCKQhE5jAl7ANjGjEGf5uwxMgCgCNhaivk6pyoD1h0w-DRlvl7LqfQ5kpkX-LYT2XLwOsaUgaFbzw4N9EldlEGY9OI0kwPmMuYI9I57jQXohphW4kegHFZ5x4gYIP_EePNR99O2G2jt8gQpHhvnpQJ9wG8qqaDSX1-ezd0ghA39Y2276EjAouuVsjPcB4sbct2qClfZAbol4WHfr88zdJoJGwXHlm4UEFVMLRsDOqzSL1PkoQybTuozgr5EZqQLWEXB7g6D_cPj3ux6rvbb6Q0ge8dNW9MPEOORG69w91_LyNhkoFHv820zunyDo3ODj8RXGlVQjFdlqfGFCV-X-ql00sCRWTAUSI1RD0Mfd53c6OFLXuqKFGu2NEMnABrWYOGjz_pxgfLyA37fdjwKdlLRgLyPuW3TrVYYCzRmOHf7fpsSDjWg6AnZ15SXEq7jhMJxAj8ZigDjyMnnLPYLJkiUIUBQqt6jeLZrI6B5BcbtltIYMkxhLbsVBM9GrvCyfK58oqW6LH0uSFkchrpmqpqXQsaaeK6fekPaakytmNXqL5g_6TeXYRz7MYvZ6IeNkRQzjn7xcMng_CSQHgcsCYcUwZg3GUDc7pMj6POpeACBUkgA0-RtQH-wTIqo5uK-KqhKZ25Eoe8UNTlvIey2CiFRiFUFixQ0u6RS5lYdQ2VGrGj6TBzybaygAR7qZIOpWd70xX1dSLj0txJnJSFcrPMuKtvnZAt9n5zeIeJfg9HdkvLQhU6RcMzwVtjNn_U4jIxrHFkhzS6ZroMqglivFKB4FVyOqnUGMdoJDBWpJTiICbfEQAUTLtzIdga9NAZ1tFz3GbmhIFFSFXmDsUcWWV-_xMzKbGpIzKYY32DxOJ9KWNPMd5gDpKdyqGMb8ztG-ePFwzh9AygNRQJpsBfRTrSzMZ8zDsDsPGzTJwLgNgSFUMQ3VZZpFId9ikeFYQNpkg4MMw44GgIwCrKQKW7xUPg-90MnGKur41xPf6c9hnRGIEDBuBkTN8ItfbFL3VffE90RmA2pb92VjVnHHm6tXaxy5hKCryaxRqOEpH0bYpjmSfTmbYdoBHSyUAlQX2fYrgb0xx1b3yP8NWtylIKNoQHTsGFj5a7IQ6g6i-jpNwSoS_L4Ktb2yNVRMwWLCZqpfAq8J1GQ2oJHbhYNfU5j8smIHC-fYuoxMgekHnkRBIoB0RqDTQ9mc3YZUmqtOynXjfYWGVvlBfUvtAubCDi273CRJiIIgyFnMeaahoCz-4wSNexU85bi3y1WJx9e5xU6b9BOlmnFpTYMIE3Vi1KYR9FgGjktU_kmBNchHBEt2MVhhCx1HwvYUSh8QssQgyG-PanlOHlDu9PjDIIW0lKt1XYdaBzWAdD9mCvoZcxsSw4pY9vVJZUEmKAq_p0syTvpSRBeNdoxGaqLVKDW0E560ugEcIJO3Oijgo73UpmwtvMGrjoRcwIumZdmrgNKPaSj41SYFu0-E17KuxhNYAPmdSUh2HzVIXNIfih3hYUH6b_SKtWDSt3O7RGTQYUqMpNuzLGvAJdFlquxFmUN2PDdKm5ST3KrcbzuqC8Hf6JuTiHJhAeCxyFgscwZvfkwtmYm88_Nog0YwJNe5ESB6w7YzhhP0zvuM3OGHO-r23goyEKAy21fbaNts3CrqscppoLqraEKN2SPCPT7fA3Z_6rPx5gGWkQGfLHVZTID6QC7wOlj5QOhWFcqJ05YDDLt-U11d6MsHVZwwrdD2dhUOkgxBVtT-K86asrphnafxKo7A0nDTFbFeVfDFwMHWmASqtpGcYz-B2-lQorSV_j9qEfjdAIFKGo9sF6Xhir9MzXpzE9DQHxJ5rpDxdiYBNweA9xpvK-W-kkfMPNauwllwiCrjroIlEqpctix9aOuTQ4CAxgJ6P5elT7By0LctW4hnymfH6YQmYyiMI6Y60VjDXqYLByN5tl5wd4KvTBOMuHKIBys0Bgh1BvuMxiIVUMDWNSA42_zvvFBobXXj_a9LMADgykAwwDHoEuhWwxDEMfWFXJW6-fgxWiMSwrdPlJFlT4xmvcP1TiOihNzIddYsyxb1R5WPbQG8rK-DK57Jw8iSVN1NSd0p7S5v9ZM11-e6FFitgWBRkfOB6sm03KM8H3XJ3uI59QQIVlMz1H4Zwo920ni-Unge2E0tGyMycxxlmPnectjcyrufQ75BEqfL6uqkQPrT5QvaWTbUrGsrYBbd325AvVTd9sxryKreHSn3_7Eaz3xUxFSADp6-oci6Ncn0NY-93jyZybUj2nQ2JB-riTXf1tbfxnasXhnfVnx13-tX6igsaHnf6DiaKR1vvTna5xmm3-UdUVN4ltd6PnMT1gkDmexI_zdfxVBjiV35R_m2mCars6o7TH0yLW99rJ5YiCYMvTPUviACj35e4Z_qtQQVLgYyMB0UraQKbU0wZKjd6nqvoyrKN4mVQPf3vUYjk4R1zPo09H75UadbJ5rzBFuc8Ik4XHGplyVqr0_GMBEqb14Rnri92EUp8zhZ3Pw1xyI_vSvoCUvHw5_OBzt_Pn06PNzc-BfZdhbBI6bZiG3IRUOY1t4geSOAy6DxWEScy9Lpcdd4ScszRLXjtPY94KE-3CZJAyj8DP3eWrWOzj17SdmvYefFzrMeh9mvQ-z3v_fZ70TG_iVSJ_b0TDrbbjyraGd3ZzzbFQzlZeDCubl7LOBlAA3RAlQdjXQ9vby7Ppi8cvF1ZvF91cXF79cLN6enf_94h04lJvDFPthiv0wxX6YYj9MsR-m2A9T7Icp9sMU-2GK_TDFfphiP0yxH6bYD1Pshyn2wxT7YYr9MMV-mGI_TLEfptgPU-yHKfbDFPthiv0wxX6YYj9MsR-m2A9T7Icp9sMU-2GK_TDFfphif-kU-29__g-GTvzJ)

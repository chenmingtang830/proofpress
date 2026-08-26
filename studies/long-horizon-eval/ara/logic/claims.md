[//]: # (ob:01b8a95d)
# Claims

[//]: # (ob:c84eefb7)
## C01: Phase Zero mechanics readiness

[//]: # (ob:8756ce27)
- **Statement**: The RelayBench H4 test-double harness can enforce a declared cold boundary, machine-check C1/C2 file-level parity, produce deterministic state-scoring records, and exclude TEST-ONLY output from benchmark metrics.
- **Status**: supported.
- **Provenance**: ai-executed; legacy id `C-LH-01`.
- **Falsification criteria**: Any released test that crosses the declared boundary, admits a parity mismatch, produces nondeterministic state scoring for the same fixture, or allows TEST-ONLY output into benchmark aggregation falsifies this mechanics claim.
- **Proof**: [E01].
- **Dependencies**: [].
- **Tags**: mechanics, harness-readiness, non-behavioral.

[//]: # (ob:c528753a)
## C02: Bounded quality result

[//]: # (ob:2a0398fe)
- **Statement**: Across 126 admitted paired runs in seven complete model panels and three legal task families, ordinary handoff passed 10,654/11,928 rubric criteria (89.3%) and Proofpress passed 11,141/11,928 (93.4%), a descriptive difference of +4.1 percentage points.
- **Status**: supported for the frozen panel.
- **Provenance**: ai-executed; legacy id `C-LH-02`.
- **Falsification criteria**: Recompute all admitted panel receipts under the frozen aggregation rules; any mismatch in pair count, denominators, passed criteria, or derived percentages falsifies the reported result.
- **Proof**: [E02].
- **Dependencies**: [C01].
- **Tags**: quality, descriptive, frozen-panel.

[//]: # (ob:8276420f)
## C03: Bounded safety result

[//]: # (ob:8a13c1ec)
- **Statement**: Across the 63 admitted controlled stress pairs, ordinary handoff propagated eight injected unsafe states and Proofpress propagated none; this is an observed panel count, not an estimate of a population event rate.
- **Status**: supported for the frozen fixtures.
- **Provenance**: ai-executed; legacy id `C-LH-03`.
- **Falsification criteria**: Re-run the deterministic fixture-specific endpoint over every admitted stress record; any event total other than ordinary 8 and Proofpress 0, or any ineligible record entering the denominator, falsifies the reported count.
- **Proof**: [E03].
- **Dependencies**: [C01].
- **Tags**: trust-stress, unsafe-propagation, descriptive.

[//]: # (ob:94129fbd)
## C04: Claim boundary

[//]: # (ob:fcb3d07b)
- **Statement**: The admitted results support a bounded product-mechanism signal for governed handoff; they do not establish an official Harvey score, statistical significance, population-level causality, improved legal intelligence, or correctness outside the frozen tasks.
- **Status**: supported as a scope constraint.
- **Provenance**: user-revised; legacy id `C-LH-04`.
- **Falsification criteria**: This boundary may be superseded only by separately preregistered evidence that directly supplies the missing official submission, representative sampling, uncertainty analysis, or substantive legal-correctness endpoint; the current panel cannot support those stronger claims.
- **Proof**: [E01, E02, E03, E04].
- **Dependencies**: [C01, C02, C03].
- **Tags**: scope, limitations, claim-boundary.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzkyNjY0NDczOGM0YTE5ODE5OGNkMmJmNyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjUwYzE2MjIxIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9kZjJhZmE3YTFlYjlhMzkzODQwNWIxNzYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzQzNDBjZWNiZjJiMTU5YmE5MmVjMjAxYSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtW-uO28YVfpWBggCJI-3yfpF_OW6KBEgTwzEKtKmhzI0Sa4pUOOTasmGgD9En7JP0nJkhxZUorbTr3FoDgbMrkTPnfr7zzey7Ca2bPKO8WeRiMp9sNovUi6IgiP2EB9RNE_iPC49l8WQ6YZXYLkS-lKqBZ9WKemE0j2Qk3VimiS8T5qWJk4UsTbzA8QTNktSRXhZ6TDhJHAiHcpnEHo8yP854lmY09mBdkSte3ch6O5m_w1-aRUOXsENBG9xqCj8wWcAHf5V1nuWUFZLU8iZXeVWSFTxf1VvCtuRZXVXZppZKwTsbyl_RpUSlbn1cV_-UoG5b44Krptmo-fX1Mm9WLbvi1fqar2S5zstlQ8tl4jvXt96u5c9tDj8vWiXrBa9KJUuwRVO38v10spIUjRg63I08z52YTxbyRj8ExpULkXkUtKauZCn1Uz8JnJC5cYSSVXWDqi2KvJQgeeeRYhH4gcMlZ5nH3DBlNPUk9xyXGnWsdAtON6otQGEP5eRVLdRk_uO7id3-3QS8XNUKfzJfS7FgYPIfJ99vZPnkG_K0EvLN5CUo0gUFerlpRS7VdVGVy9mqqvO3VTmTN7S4pjWFT5c5v-YFzdfqai0m04viiTZNnbO2ATcuGFW5wv1kkS2oAvM2Uq_XNrArCv0qL3FJtVWNXMM3JV2jd28JP4X3FYbFZF62RQGq8BX4URpLsKLir-AVx2UJTUNcHlzYyDeo6FNUAsJqCfEka_jK7keF0IJsMOLka_jkE3LwbLPdoCzobgidyfvpbjOeBFJmLL692ezbr2eOOyfPVlRJ8ndZV2QtUdacK1gYlzERd1wKEOPsVU7Il8RhxKX3weV7sZLkuSzo9ktZ8hX5OiCYzDNRtZi-K1rjAoTTksgyq2ouCSVCQijVeiEr8Qai7LY5Qw8k9umIuN6c_Llt2loSmWU5p3xLdGSSHPapSpE3Z9nz7mUgvmhx2qoedfw0yeQHF_P7stgSKtZ5A_mBniiIfCO5TiJtTdVusJKANQfCmh1OmDXx4ijwnGxEXn9O_iLB8eUyawuCaQXbQqU5z5qn3j4VldT1uSv5h5Lnm4w89YiopCJl1ZB8DYXzRhJFM9lspwQLIjYgsJlqpqSqSZaj2eQmV9W-2V5Ou5o6gXew2iw4OMLUK_1NV_zkwk-DOHNokgondITriZDxlPkB1q-q0Wvask9s2SfQgPirTZWXje5itd4J1ex-w2L2EvtFkfPtYIVhDxksorvTPduLqrJmAaZYynpT57aLKebOOUvc2GWuLyNHcseR0MwBAEDzzxzmZ9SFNRzmOo7vspCmIgxpFIooC9KAOl6CcaYa2uhuZLw1j6Fa4wcTz_GimZPMPO-FG8-DdO4EXzjO3HHgJWtwLARxmiSRE0LY7D5992u1Lh2npqtAhVzB87EEeMNowrMYLafXGDQaG8Ln9Q67ZAQbemGauUnKuiUH7aRb8oGNwG4mwHVZknmJlP1mg95gN3tIVYfkKgRhVVsKWkPSrSlfgVwzHavkqXsNGZrlhZwVkEQFgWDPMTchU0ULCwkJ9gJkBnbLOcHokTPAjRCWS2LxzpTQUkA95EUrJHnx1Q8vZt9_9-3fSNU2m7YhWV2tCUPB17R-BRYC-MHVFXkBGBKrL-0UmPUmM4VzqosGkyt6k1c11oWbXMA60ixJSQEgo8XkXQMMKa5GCq21sufyyGEJg0zjvUt3LW3fpQ_qRX1ghiKLw9ATrtttOWhPdsuH9BXSrGgzQN9kJYsNrIK_yBrKLNRTrLSwQ435lwvwHTHILn8LD5ZyWTU51XtpxxLK60opvdkgZq7INw0Kg94YyDMqgy3xihRyCYK-KqvXhRRLOSWiplmDUaNe5VBVQSaIA5RrSjD9W3gaSmaz0n0AGooEhAnebnqJtaAnnByJxPOhDnpZ5veptGuw-06-sEV2m0ROEmZRTCOR9pvsuqbd5CF9D1LoZzAGJCEB88saTA3h_laWYBTI7bU2wwz-BwmMzq6aCrz1n3_9G5aBT2FWowW4PC-xOwIuB-sWUJ1gXNsoeKpZ4c-t2BK1qtoCg047VDtSWwHWgciAbTCE2gamM5j7KLxX40MlvAAtCTuTxDDYFbwNxdBRtnI0fe4cuOzlezToyIAkIcD78QjyumzmFUQBzWfcDEl68sKydPqhvUHr2EM_t1BE-6dW7ZqWcyhNUI3EDOfQ33ook-VNXlflGqENfK-FHZvNtH4PGs1Ow_svsQ5ArHVhuY_7oPrmWT6cHy7H5pfvcSGY7jYwOXhPHU7j44u3OFAhDVwvzZgYWT-YWwzTVeWz5oCxt07ol3HmCydmD90f8cqgq6Ed1KB12Aoxs7VDrYnKl1gAob6REdxvkupYxB6a12L853JTUEQLppcPG6hVnrzOm5XRaBB7erurY8F7dLsnqDC0b8h4W7FnG1oCpLod01fHgvZOPTCBZ2aRcQVs4I3IPwjcs-SvmIYQAloQLjoDj23o0kAFDrvtaTGI272Y6NdGgLiB0Qm20PLNujjqVLk6FonjKz6rdQMhFXYZaHkalALM4LRViCkwonJsQIAXDUDViGSGvaso8qXGkdiFbcU2gdYF_bvJ69W2twn2zP0gwRWH9lbGFQjBOz37Nmns1sMpnJ3OHmWl8DOeRDJw3FTwOKAy8Wjks94Swxl1OKAN59Z3H6v-x6r_R6v653M6-5yGN92ZfR68H-cv7uJyPghhE6Y-j50s5QmLXTfzPOl5AdNcDOdR6AUeS5MwTFLpOCyTXpa6DvMj1xdRCuhQnqPcbfYmeuG6c9-fh-4IexP5ges7mfuRvfnI3vxx2BuZ0MB1fRjraXQee3O0rxx3JctE6odpIt3QO87XPDEEietFu0q3oTk6qgaoBC2fKKxb4Lb1pgDjG-WIBoJKW7pZ1VJaeqSh6hXM5-u8gJxDIgCk0pAIHgRgo0dqWNp1plEYXLvuNPUS2IiBCwgHT-OwTz5L0iv_08_14gMmpnvXnbqB2737WepfBZ9-PtURpmCJjR7zoZxksjaQKCNfBFcu2QAygvqL_tGEtjrloDR1GMATyaLkPOblWNM8kddMZLEMExbtguCQeLH-QcAW-TsXYVurq6LAHRtrnbwetbgFuvCkzJcrBHF4cN0jYZND6sDYu9fKqpSD9Ch3WNpMAxo-m-TAjIfERNYG7Q4tstq0hUGLBt3W8NUJw0MziwIfurcvw84oAzSxb_gzcUGXEZ7L0yyMoZ72Xh1AhUFxu2_TXyL-LuE9a300m9wSUWnrgGmgEedKg-oO5pOvKdhySyzaR2_o2gbf3Eb8O1Pa0mgGA10dLR9nRwIyHAk0GwdrQ3FsdC2DMqigbumQsjwcZi1UwKcYajOT3zqxMZlXWHArWEqanUpNvBKkb9abxhbbG32hghtHow3Q-mC8NYX6gRcssC_Aj7gnCCIhS9WDWLTT9Nlp3uw8wuz3wJfdeYlBS7wjytoS6enywdcX1KUDxfjlhEsO_s8cXEYvGTxsH0jI5oyrAb_0BHm_9Q-EH58ef-HJ8V7LH4g-PjWemtjOk3l8GrxsXSPsOHM3yKMTjBemqLIF0KB-0lT69yfPnxhJFCDIrayvjqXW0dW_w1OUIn9rN9glgD3kw1MnfEVvCelydSypTlBpQhmkgOS9aVOt0rAc6rVpUHgs03cB_VWVTUl37MU1IDRtZal0tzyQ5BwOdE_XUarzQGPvPuSnMDv0wBf9ZJZXMKysqR0zDthRS2gaDb3L2dEjGg65uQMF_fuwoxcoaEDmbAD4rH7-Xbzpnfrtkaf7mgV30ajnagYAawNjZlWCLgBLmqGSAO9kbXsmjCMAVox2wREW9SksDDPqEEM9e04-8UN7EgnLV4gVYR62-TBb1lQYQbwrmLUsMtAcKyAyohu0GWIN4tRnxoiF8ENzOVWDQjwLpzVM3aAFl-oy7vXEtdFR7rWnV-7mXj-iiY9o4iOauBBNnH800pOmO6o0fT_OhP4qPDBLmBsxGlLmZA68xKLADYWb-DBeM8dPKIw5gRd7LpVZGkNliAPuCtgo89yEhfK4Sgfsrz8H6_r-CPvb35D_nbC_vhfEoZs6ENbhnezvaSLW9WjsxJSJJLmD9X0g40vDKE1i18niID7O-M7Io0c_dPDv0aM5-V-kgP9Rdmq2CnW0pI8U9ptnPdjFb2k-MzfbpHiseReO4IX8ZGn4n-xLfx6i4p7jxAWelFjYCrzTJLT1zJUlTfhZbNRbbGcsTU0hS23MQta50lenevvgDa1yxEaksxFCG31pCiYSsPMbvEugWSJaFNVrdWgujWZ25qLLZS3t0bnF_FrcXO1PHju7VRlq_ONXjvvSfvinwVygv-u-eAHjAX7QrzU9JOSRbSxnOyr-aqQR2PgOGfWikPqex5LTXPs9eXaeJAGPaZhJ9wTPfpBA_8_E-9FE62PTgmqt7D2yz7s7-55LNGyLd0SLYugCM8IZjtJeWBxINAx-HBTUY7DWLgvRbejFjhSHAK8gDSlSmdPOkJ0YOulg_Vxz6b2V1K2skvY-Y09GjySVdzSpnu4SrssrG9rTodumtybYE9mUCO6nrp9EgeCnD0budygSY59NOeAR5h8_FDmWTL_1KcljUwU_0CnJ2Vlia7i6R6L45yTKDAqSbUfDrmK3namN5PgqdHqhE1yfAKAm9eAquHWAadAmaYyuTdVA_ap213F75yT75nZMmypxwJZFvszNX3DiirA5SgztzQjap930WDaZW1-HyeRfkkxN3QLqMbpNR-6W3cqyE3nF4ygN0gggvytOn3tdeObFHYdGzAmCMPCOn3mNwrsTh2AdJ3XRYRhmxx_mMOx48lEEX5pMIjsyaTT18I97Z_oPjEdzL7g79_Sha0-NrekWYFhHVqH9K_xrCwb2kniE1uBfRkCmdAQzFrPuioKGliJHxeEh1KboMgJ6l8LE6Z2gWqY_w_CFdEHGqWzM9XnAjPBiucRY5xIGStAdrw7SYqtyXVjxbfBbqR83NxSHBu9qxGND0LU1skpdibz9FxnNqtLX_OsKx097KXEMUk4JtED8x8d_glP5O0WYh__4-5msPTolRQ5Brx0B2tymJg_S9-V7-O-_vdLcxg)

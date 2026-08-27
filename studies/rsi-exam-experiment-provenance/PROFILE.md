[//]: # (ob:1bd66d7d)
# RSI-Exam experiment provenance profile

[//]: # (ob:5185cfc6)
Profile identifier: proofpress/rsi-exam-trajectory/v1

[//]: # (ob:ffea2487)
This profile is a small interpretation layer above the generic TRACE
decision-provenance import. It is passive and black-box at rollout time: it
does not replace TRACE, create a new trace warehouse, or gate the agent.

[//]: # (ob:26eda17c)
At execution time it observes exported identifiers and safe metadata only; any
active governance decision occurs after import during explicit review.

[//]: # (ob:17820b72)
## Event mapping

[//]: # (ob:2e46260c)
| Experiment fact | Source record | Proofpress meaning |
| --- | --- | --- |
| Rollout identity | TRACE session ID | External source/session identity |
| Saved method version | TRACE contribution event | Artifact checkpoint with parent version and digest |
| Experiment result | Evaluation receipt or safe tool metadata | Evidence bound to the exact checkpoint |
| Retain/discard/revise | TRACE decision event | External workflow disposition |
| Final submission | Submission event plus artifact evidence | Candidate final artifact identity |
| Hidden evaluation | Sealed score receipt | External evidence bound to final artifact and verifier |

[//]: # (ob:21476434)
The adapter may preserve safe descriptions and locators, but never needs to
copy raw prompts, reasoning, transcripts, tool inputs, tool outputs, or hidden
targets.

[//]: # (ob:fa16ba9a)
## Required bindings

[//]: # (ob:22df4c46)
Every checkpoint has a unique version ID, zero or more existing parent IDs, an
artifact locator, an artifact SHA-256, and one or more source event IDs.

[//]: # (ob:ff079f3d)
Every evaluation receipt identifies the checkpoint, evaluator digest, score
mapping/calibration digest, and receipt digest.

[//]: # (ob:764247f4)
The hidden result must identify the final submission version and repeat its
artifact digest. A verifier digest and calibration digest are required so that
the result cannot silently move across evaluation definitions.

[//]: # (ob:cf38ce0b)
## Governance boundary

[//]: # (ob:4c04d5ac)
Importing the profile creates source events and evidence receipts. It does not
create a claim or admission. A later claim may be proposed for a bounded
statement about exact result binding, coverage, or release eligibility. The
normal Proofpress deterministic checks, policy recommendation, and explicit
human review remain the admission boundary.

[//]: # (ob:2833eb81)
## Coverage and limitations

[//]: # (ob:36b5e27a)
An official manifest can enumerate all source event IDs and act as the coverage
anchor. A capsule without that manifest can still be internally consistent,
but its coverage is unverifiable. A capsule with a manifest that names
unrepresented events is partial.

[//]: # (ob:45c13414)
The profile verifies supplied records and files. It does not prove semantic
quality of the method, truth of the score, authorship, or completeness of an
untrusted source export.

[//]: # (ob:db189dfd)
## CLI

[//]: # (ob:6d290856)
The initial conformance verifier is study-local:

    [//]: # (ob:71be0bd0)
    python3 studies/rsi-exam-experiment-provenance/verify_capsule.py \
      studies/rsi-exam-experiment-provenance/fixtures/valid/capsule.json \
      --json

[//]: # (ob:922cda10)
The output keeps integrity and coverage as separate fields. A successful
integrity check with unverifiable coverage is not a complete provenance
verdict.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2FkNjU0ZGU3NDhmOTM2YTA1YTQ4ZGU1OCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImU1ZWU4ZDBkIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9iMTllNjViMmZkMzk5OTg2NjIzMGY2MjIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzM4YWVlYWEwNjNlMjExOWFmMWQ2ZGJjNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWllvG8kR_isN5jGkOPfBPAmON2tggyxsIy9Lg-jp7hF7NZzhziGZkfzf81XPSVmiZclIsAD9QJM9PVXVdX_VupvxstYpF_VGy9lqtt9vuAx8T6rQi9LYDbjlcy-Syo9m81lSyMNG6itV1dhbbbnjBysehL4Mfc_DXqk81xPcj-yES-mEXuJaUZSESeIEtuMljh_zMFC-KxzblqErQRh0pa5EcaPKw2x1Rz_qTc2vwCHjNbGa40uiMiz8W5U61TzJFCvVja50kbMt9hflgSUH9mtZFOm-VFWFd_ZcXPMrRYc6Wi6L3xWO25REcFvX-2q1XF7petskF6LYLcVW5TudX9U8v4pca3n0dqn-aDS-b5pKlRtR5JXKoYu6bNSX-WyrOClR-UpF0pKzdmWjbswmKFdtEjtWgZ84qXTjOI6CwHGtNHAckqwoazraJtO5guS9RbKNG3GlOLcCV0FvMU9tGchEhO1xOuk2gu-rJsOBHZJTFKWsZqvf7mYd-7sZrFyUFX1rHyu5SaDy32ZNfp0Xt_nsE87Q-wMZuG6kVtWyrPRCfeY7fOxhgB3ILcAXZHku1PLX9__66d0vby92dODvcSde16VOmhpW3CS80hXxVFm64RW0WytDr6m3RUkyX-ucSFaHqlY7PMn5jozbyz7HqxU5xGyVN1mGk4gtLKhaHSRZIa6x205kEMiQKMN4tfpM53z_4d3iLc7HxvOx8Xz0NdXQ67wXAa5tZNuTD6pbrPyFPZtGfdiT2OQYcLLZl_konG9HvkhF8IOF-7XdwrTEuwgfVa7Y6DajdeuSU2QglpY39ijpnpf8SMw0VdzxovAHi_kRgdzvY_jKWbXjWcY0WJTYVnNyFJbxgyoZT0Ca1VvFrlSuyhPS2mHkWEnoHEn7lkKC7fh-TzY4Zdi_sId7TxjQUV7gBJZ4Ga979nbUHcUQu2cfiqYUlOwoXvF7zHBsp3gOiux-nd-zxSiYySHHYtleGCAxv0ysj1Ayl3wPK2D7gRF3VUL7FU8Vk6oSpd6TaWCyXDLw5JRm5gyRfcqLuB0kPObHXtSmV8kSSAO5qm_Y5rH9p-zjyNQTXvBynm-pSjGUCHG9L-CZbMvJU5tc_9EohoemJL37-5z9R5UFK6CyolQICl2dVEZqhXHqytcKpm541rRxApdRsMsY9ZUJl1H0eb-7OCEY_MbxwtR7uWDkPluNZRIJ9Qk-11SDWAcjVKpznrGqSXbapPBekScEE6kbCWUlR4L9g5qINuEkRZNLjo7itAM9_sYJF_KE5Umfi9fwfbejUk-xS4fvU54oFbU7rGpD3lTtNqTwHrTVpoETKnEi11VJZB-J9oZEQzPRxqbe6TaNfiuwTrx2QjlukPjKCfmrJbjMWZGmWmi4xQ5pLkUbyATPmcqbHajVoIbSMFUVgq7V1gkNeb6wXc_2Xi3fx4ndbkxPSoZr0KtphEXXfBmCtKW6YO9qJgvsyYtTaUAmdhTL9DgNvPnl3beMZXacsEsgndiK_OB76NIRda5rMgFeSotyZxy8O25JJZoaxMOCMn62OpVE7ASRKq3vYc_wb39A75e77Jl9qJHsgDb4hCix4wjJbet7NVE09b6p2bVS-8p0JFelrg_GwmLwHyhEEceaMprKJOz-UJRP874dn3U5btPGPbE0T_rGWW2cJBVh6FkAEwnAkuJeovzQTan3LWpDs0MMrEMMk-xuAFBpOFE73P-ibvgTQY1Mi8OEwhR-TIgYYPNCZFIVab1BZr-i7k13AKhK7JWn0shxQyAh3_NtO3I9X8WhSqVt89BDggVkcOIQh7X8RAp8hkkchB5PgTRdl5BDhRg1QKa11sqO0e_TysyxnGBhRQsn_GgFK9tbWc5fLWtlkcX7qoJ6i0wZWRG1SePq3f8S-xiHbLEJWogt9luOiG10RdxzqKoZGhO40vnq65BGx8r1gyjgsR0nRhbDagI-OlY_Cjd0TLmQ4Ks8EVh2z3QCJTqmr0EBWrCP7y_fvF3nUgkzHJiYimlTdU0qJhbAmPqmTfpJxsX1Iik-M16zssgyRDurodkV0zWIdYkbeX2PnaplMu8KNiTM1S2DEvDkFkG2LZpKzan1u6LHJB1CJq8vnlZNoIQD_4jQ0YSD6Ufc0pv-WVikI-kIy_ViS_HACnqSE3jSkXwV5Fgs2NEnLb7vtNf6DDLkfast1oFzVGlGTGvql_oCvuwfjm8RrQ_8BsV0p1AE5NBa9_Qoe_fDg64BuGeXXQBOG_RbXW9Zm_wGImT0dozVcpoooetRsfZ1Kw2TGsxTF0VGcgEV1dxs7foz0_zhsTE6YuNYklZBeE3nS5p48VIuzRRLDafq_XY40aCp26K8TrPiFnJX-6LSRjBD8aeHzTM0N_5oCe2zBqHUa2foJ-_ZG6hCy7ZiEZlhz7Epfm4b-Am8ABPFM9inEgRwehVNJFZfaeUBC7LC0E3cPwZgO18OHctzFBehJYZ0NcG0Q-Z4OU5FCEMSfCq0bXWxzkWxP7CS31Iq2u1r7EKwVwV5_5xiPW-pYd04g87RHfQ_2l6hMimgRT7rvObllaqrEzlAusIzJTDm1pAeR4w85oBnYt4-6wZ-EApbyMgRg-5GGDwOA14MaykhdPGFFnwO5a7zwcadlml1NPyHny8Xjh_MjR2KXA30Hvbzp1JmInxHBdCPL8ZqMqDoo3O9DBWXXYqYty6-zru0u0S3q5OypddvoZP0tNu1E7InjqMiNwpU6Kte9gnQnvjzS4FzJ88eBQolrJoYpBOOXY6h12VC08t-dTRYjaK7c7mKUhtHTSTmnVSAZVQcKxTsvM4OsCSVVVEWKBgTzUuVGjiB-DuhmliF8E44ZyyHSjiB-mMUPBu49-FlS9_2pR9ayeAvEyzfEX4NMifbHyM9pJG-RRAZ1zvycy47U5EJ6H6j7J5RykoMT6R3qDqlze3ZlFzn1PEqU6HQ9CBhtdWlM0GXCeYDFjG5p1QZchbkzfSVTnSGbH7B4FVr2AtgLptWdqkgyQ4GQjyLNhwQyi1MMK3ADrylsWTr7Gg-8Yzao20DYMhatIT_dihvbdPTn3Qw0Am7exbaX9_2bEv4Q5oa5xmj3b9vMNFR9xMXXXQauEEyBNxkVtFRf83QwdSzLpd0Eq7JO7dFSYburmZMM2KaSwTRMQ_oHbQT1Ta6iGpEEl0vwSDgM1_nVKUQyiPcRBPb5DfDhdhDNnCegYFhR_clyARNjrxApRF8ZO_LpiEuCeufSlu-9JIgiX0VjCE0TlQmaeulo5EWx6BXhOTww3X-R8PJbWEXo9q2F6QC3OCA3aLJznBKc1FUbfXeOD88dp_BqXPybuykqtSgZUQKNXmsteFnAwmePrIV89B3bMGDlPdHngxpJm751Aim90DPTUOV-FYaDOBuMpWZ6O6VM5eOX8oDLoSrZMy9ocSMY5iO32uGLMbTLtAlrdfrnJl_zySR6s91Aw9cojhouexJ_Y72akJssaCFp08YWZanHGk7aTzE9GS6M9HoS2c3l3BbIeA_aZOt8_FFkx3bGJsG4FFkkjPzwQkn-HxNb0gtvva6T1_odI9c1iqp6-Gq9k0h1efZJ3PxKxvx9fqDq93JOlq5aiT0XostEAj7yOGpf4aLXwOiT977zk7LO3viTtgJFJwmFD_4PvOSirQSLUKlaQLSNysSg0mqLvUgFY3TlTYrGrTyyNjQdAlPCv5Aim4--CbjZd_k8qk4gxiG2wBlif_V2FilBOZvq25ywmRTUmfUV_6u5F-00vWKu5vdbmmw-E9-rYYhS8uu7QOJBzqcetFRfUCubxZ0q6P2UddRdEq_IEM-e4p64g8uWi1Nx6PT0eB0ZHr3J3ac50-Vv5qqfnl8ZvqtAfKPmRKHruXEbiw8V7leEHsej_wk8LgfyTROI1ukyPyoq1GoUh4ngRtZAUdptjioR0-d57Ehsb9y3EeGxMOf8ZyHxOch8f9_SGyJwI-sEA7ixgNEGjNQD2JekTyGOlDk2eFvWD8Aw4iaNDCpCsOMshCioddTArHfqBHn0fd59H0efZ9H3-fR93n0fR59n0ff59H3efR9Hn2fR9_n0fd59G1G35--_Bcqm35w)

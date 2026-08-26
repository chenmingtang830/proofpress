[//]: # (ob:88bec44c)
# Changelog

[//]: # (ob:a0ac1671)
Proofpress follows [Semantic Versioning](https://semver.org/). This file records
user-visible changes; GitHub Releases provide the corresponding tagged source
archives.

[//]: # (ob:45d5f7f4)
## Unreleased

[//]: # (ob:3fdc1e81)
## 0.5.0-alpha.2 — 2026-08-26

[//]: # (ob:b4f0792a)
### Added

[//]: # (ob:be515a4a)
- A legal-review claim graph and profile workflow that keeps deterministic
  gates, policy recommendation, and authorized counsel admission separate.
- A retrieval evidence-locator and provenance-receipt contract, including
  bounded, auditable imports into the v2 knowledge ledger.
- A conservative TRACE v0.3-v0.5 adapter that records safe decision-provenance
  evidence without importing raw prompts, transcripts, tool payloads, or
  treating TRACE dispositions as admission decisions.

[//]: # (ob:7943f01b)
### Added

[//]: # (ob:4412f40b)
- A local append-only knowledge-event ledger on `refs/proofpress/knowledge`.
- Flat `evidence`, `propose`, `evaluate`, `judge`, `review`, `supersede`,
  `context`, `import-v1`, and `ui` commands.
- A provider-neutral LM policy-judge adapter and a localhost review UI with
  trusted-context and lineage views.
- An illustrative legal cold-handoff fixture based on the workflow shape in
  PR 22; it is not a Harvey result or legal advice.

[//]: # (ob:5662006b)
### Compatibility

[//]: # (ob:f39f974e)
- The 0.4 file-backed `proofpress knowledge ...` group remains available for
  one alpha migration window. `import-v1` performs a one-way, idempotent import.

[//]: # (ob:ca6a4032)
## 0.4.0 — 2026-08-23

[//]: # (ob:f86ccfe9)
### Added

[//]: # (ob:bc0bc211)
- Verified knowledge ledger CLI: ingest bounded OTLP-style telemetry, bind
  evidence to candidate knowledge, apply policy and human review, and project
  governed current context for a fresh agent.
- A minimal telemetry fixture is included in the npm package for the
  end-to-end ledger quickstart.

[//]: # (ob:de2f1030)
### Changed

[//]: # (ob:94b5cc40)
- npm package messaging now describes Proofpress as verified knowledge
  infrastructure for agent-native workflows.

[//]: # (ob:389b1927)
## 0.3.0 — 2026-07-31

[//]: # (ob:b4cefe13)
### Added

[//]: # (ob:3bb7f15f)
- Draft Artifact Provenance Protocol with a format-agnostic evidence envelope,
  explicit verification levels, and adapter/provider registry boundaries.
- `provenance create` and `provenance verify` commands for conservative
  byte-level evidence on any file type.
- Built-in OOXML Word adapter and semantic provider with canonical DOCX
  verification that survives ZIP repackaging while detecting content changes.
- Built-in PDF recognition with version, encryption, linearization, and page
  count hints while conservatively retaining byte-level verification.
- A two-minute multi-format quickstart with portable Markdown and HTML history,
  DOCX semantic evidence, and reproducible CLI screenshots.

[//]: # (ob:cef1396e)
### Changed

[//]: # (ob:acea2835)
- Terminal output now uses semantic colors for native-ledger and provenance
  verification results while preserving plain piped output.
- Numeric deltas keep times such as `12:00` intact in display output without
  changing the capsule wire format used by existing portable artifacts.

[//]: # (ob:8961592f)
### Documentation

[//]: # (ob:a74eed7f)
- Expanded the FAQ to distinguish artifact provenance from workspace memory,
  local vaults, Git, C2PA, knowledge formats, and documentation systems.

[//]: # (ob:20b043a7)
### Compatibility

[//]: # (ob:5ce920e4)
- Existing Markdown and static HTML ledger, capsule, snapshot, and verification
  behavior is unchanged. Generic binary and PDF evidence never claim render,
  semantic, or native provenance; DOCX callers can still request exact `byte`
  verification explicitly.

[//]: # (ob:c8e27e08)
## 0.2.0 — 2026-07-26

[//]: # (ob:2918d404)
### Added

[//]: # (ob:0930bd81)
- Portable capsule V1 with stable event IDs and multi-parent history.
- `merge-plan` and `merge` for parallel Markdown and static HTML copies,
  including workflows that do not use Git.
- Portable, English-language official documentation and agent adapters.

[//]: # (ob:51f72ac8)
### Changed

[//]: # (ob:7cdcc2e1)
- npm and Python CLI versions are aligned at `0.2.0` for this stable
  release.
- The public documentation is action-first and includes explicit trust,
  privacy, and tamper-evidence boundaries.

[//]: # (ob:ec1e29fd)
## 0.1.0 — 2026-07-24

[//]: # (ob:ea2a7d0d)
- First stable npm release.
- Portable Markdown and static HTML revision history.
- Zero-dependency Python engine and npm-based agent setup.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzg5YzhhYjE5ZmY0ZmQ5MjQzZWE1NDQwNiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjA5NjdmY2FmIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV82ODE1NmFmODAzNGM1OWRhNWE2YjVlNzkiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhmNmFhMWFmNGRmMWQ3ZTU4OGVmOTU4OSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXemS20aSfhVE-89uLElVFc6if2nlSxE-NLbsnRhb0V1nExYI0ADYLY5CEfsQ84TzJJtVOAiS4Cl1r2QjwgqzedSVWZnf92UBeHvF8jLWTJTXsbyaXi0W1xEVEeOYau1pSYnnKuZ7HgquRlc8k6trGd-qooTvFjNG_GBKEOMRkaEknEpBPMGYUMqnmHo4YIRyRrUMpEA-w1y5gmOECKFaCN_3AulCuzIuRHan8tXV9K35o7wu2S30kLDSdDWCF1wl8MYvKo91zHiinFzdxUWcpc4Mvp_lK4evnBd5lulFrooCfrNg4jW7VWZSG2_n2e8KprvMTYOzslwU0ydPbuNytuQTkc2fiJlK53F6W7L0NnLRk41f5-qPZQyvr5eFyq9FlhYqhbUo86V6N7qaKWYWEdEg1ILpq-qda3VnvwSLq66DCPsB0xFyPeFTyXwWcF-F1Iwsy0szteskThWMvLFIch3pgDHMtCc1lqHyo0hp6ke0mk49umvBFsUygQkTM06R5bK4mv769qru_u0VWDnLC_Oq-ljJaw5L_uvVMn2dZvfp1SuYQ-MP0PWzb55-__WX3_7w9WQur0ZneQoryzzmyxIMdM1ZERfGX1Sir1kBC1cq296ynGW5Gc7rODVNFquiVHP4JGVzY7dmWCP4aWFsfTVNl0kCgxQzMI6qpseTTLyGb0cRV8LzBHwd7FKqN3YK9otJdgvv1r0wKW33C-NB6h7e-czpfq1cLUznxnLgBVfvRusuGGICByE-v4u1Zzo6S5LsvnB-_UnNWVrGwgGvNrOD3l79R-OQhZrDhphk-e2T9ZgWLGcbAxKRIqFC0caAfk5zlShW2CHsn_RnzsYXD0ybUBxJD3kbvTytWzzQwWdO86UDjSPqIi4jfF7jY-dFvVuc2u2dX7BzD7vYKaq3rdc7z78oHJZKZ75MyngM62e2QjueBELH5nqqkHOP0PMG4zhxKpKlmZpzn-WvtbVvOWOlIzMnzUoHooXzdVxODpjSdQUESMQuXYeR82V6CxOajRPwxyXEDyfTOhYxS2AUYjmHmTOzH-16wMfpgXXwsQ4JE1GPox-1-fprB6weCikEUfjcDsZOupjbGbxYQfRInWffPnfuqv0Dls6Vw5L4NlUww9K5QRMyQTew43Kwhjo0X0Wpx6Pw3OE4Tr2DDlk2gDwYypCeP9eXM-UsljyBGLFpwhjmKsyrsY7zorQLUvmgKhz1ZpEcmGuoaQjZRJ8_10Ue3zGxGtnuSjZfqHwMn0qVCuXwbJlKlseqOLQWSmAFuV9udI4meIKcf__vvxyCSDBG4Zh4R0LXnp8c8DjFCAsler-ex85Xdr3rGGN8sXGA39JOTPqO5a8lpC67UoUxmnC-2bbJq1GTmq9qD74WuWJVcrSfNJlWXTNYNaUJR24UsoCJEEsm3cAYEeKLXeqm7xo9OIBjxOtFFtuAV0c-mz-bv0z6fGVgB_jXqtNCF4p0GrEg50KUUmS6vNZgEpWDE9VgqOB4yr1QeTREWGAvZERQ7aIoEIHWUYB9RCNJJEBFJSJCkRIoJNSNRBBBGsahCEy0NMtrQU1lrin2ACCYd65amwYvMZniaOqT_0JoihD8ql5x4wOSBgwLBd6yfvftB8JB1vsqnDJjxczEeSwEh5DAlDRQxbbRgS61Yx6FJHVrLHB9SpRH5Lq1DkqpW3sf9PGfEwhDEG90bEG3hZW_pQb-jg0Atxm4QmOfmxT3zZI7P1ZbooCAkZnwYIKvAz-EASyy1KZJwPcQbpwiW-ZC_ZayXMziu_7QUc8UPMrTjAYC2axhZ9qBP826HUc1zcq5LoMWQ49GftNeB-i07R0EMY1Nte-FAQyEqKBpq4Nr6rbeB7M0LMeGmZu5ym_VeAGJ_sZ-s3qjSnRm3ZJEJf0x6OV334IlFhClRz0popmOF2qGuCC-DdTVUq-RUT2d90I9dU_cVTLQgYsC1vbUAUI7C3c-yIHcKNmiBB-f7J-w7_nKDV1NBG6H0YFAHV84CG7q1oAQu0LjkBBOmtY6eKed1OVIxkmhjdpp9s9Kat8XjCMMNLud1RrotGY8AGGaGQVA2JFLfaHdpqUOqmlndDleAROWDiSYojzglyyKAiR5SDVj7cKu0Uw7offAKXVPIQRUAvmGu6KdcAe6rIPN6TikmYPCKATDhMjqA1XLa2jSLuV74Ayzx7fVEfuzf6g8G0u1UKlZilXjeCq9hVRum4COxtyEznrvFKpcLnY2zqt3ZkI9soKScdmKCiKT6s3VKytRyKXYfX9LhOi8_8dSFeuG8hgSTC6NHvP_rVDYVVkLFNWQT5Mneqm63dab7hOs8ec8k7GOPwSB3m1plxacxMhOaOg0unNCQ71kfN1CrubZ3UMw8V4yeKzfE3hgL_E61u6lsQz2kUhYPN_rhLt2qInEs2y-SBRsAJtpYCzjOqQnbJmK2Tq0mBHlasHiHL5rrAfvCNgvsPiTfR76iL12HPoRe-14_yP22tkqO970YJ129snjddrZRA_c6avONn17dT9b2YB_SdNtlt7swxDOkwWAiPhRqHnEaOh6WPgB831XYdFOu8vsu6y2y_bfDplpyEwfQWY6XdxqxZ3WKlNv1A5o6r7rV3KOyVofRLvyJQ59QSUOoggGT6FzjxHNQ9hOfoBDyYWMPO76xNPY80Pl-ZIxoX0F_6D906a3o2S5UxROsd-jZPmh9CgmZFCyPmolK_I8EvgBCXjoH1Sy9sTgx9G0fORhV7oR81z5yWhav6WXxNltneFPqUr5SmvhY-55nv8gqhTsrMrkxgi7SWd7dqGvA-p5lBKsH1xTMkM6P1_tDHlQhQZV6MOqQh8bRO49hXAYCT7QEYResH5sJB-uYN6vn5yiZHyf5XMIkv8020X-zoTZMZsMcA5_QUi1cdOCCVE2gCM3u_AyLeMh-u24wz62_RDd7oooD9dtH81PP0jjZ_F7n5EIISkC5PkuBwgnMBcAiffx-xbrH-f3Q4z5eGPM6SpPD1UkHapI3vUzwU-YCW9Pr4cJYzL1-s50eBFxJUJ0YMIDE35vJgxNeNINw8jX6k_JhLvk4ZPgshIMAlFERJ799SNxWbNMAxsd2GgfG_2xYqMPzEShi9Rc6QGf2c4_MBmFrOzrUHsPezUB94TSCrsPcjWBy3mosa_PPUX_Rc506Tyt7WMuJALPYWYvwssyE1lShXJmAsSclWN2m2aFceUD8JIgjjyXbZ0qz-YL2AM8TuJydfQs_daXD8zcF4pCOPAu62zsfPkGhm9yxd79migJyG_UpLeRU6TwapadRp07zrU1iprRgZVMZuz4EWxtG1In-_ynv6Gv82y5KJxU3RuwUhkPxszsKtiYusdj-pv7scJHFvC0EVqld4DjFrAIubqFWZvrz6qgXYd0k2tENgc8Jrc67HjFoYUwv17brn8pOjY_PHZTnLZp1UmhyTvIMGrG7mLIdTb9WCiXAvy7qz6FEAIMVjjbCWm1hy83qbA-m9hZ92KZw4aqAndcFg5n4vU9BMpivDm9pgMYGGww1WSS8yi0B8TS5S6jVAAi19L1lKcw314OWI3Ww5qIbGFtveO7vtI5Or8mFccp9xBJh0j6YSLp6TLR9nUQ_rt-Rvw4ioBiTGqkSOAigonL4W_thsolMgDIGmnOiKRKhogSF_YoDgMWImBrigGOV2zPfDYlAPoSmL8fTZHbIwG4kgAdR3qQAD65yzo60fODXNbRiZNnEX-pIxQI4mFvfZC_ExZbHnR5yNvFE4YbtnTxzl7uLiqGmUAoSIoKXdSM-0ltiXwHhRiYY8WEbl6zibPWFDrv215WNy1cqUXtNR4wY-KrUo3tENaDtiLAqnIhs4oHyKpWhLEwhL0etRpKJ6h3-f_xQN20yanGEeE0oOvrG9axuzXP5fG4rFa7awa7Fg14ijvIauJ8XaMmHqcGybTLlMKqwYJaSFxXB6yZi3qrjhxoqsZla7McWMxBNhtks0E2G2SzT182M3jjI9DMZkuIxJfed-QUonRCVfQc1rGvuX7lZVfh2D08UBnM-eKHZ39v81IVA774qkYtbbw6IkHsNg5jMghjS9HYzqyOUPBBelv0aww1d7cKQ5Ur7WCbMdaDa_ZSA14nZykIkPyojnwXa6Sl8CSlSqNAk31F-JZjHFcEPi4vOV056avLvuvnWY9CLLEA0GNuL4WigCFTbdYUcWDCIsKc-QIGr4UfKY411wITzimwCZ8JQqSrebR_SjvcMpgiCvSyj1tSN6BYyoFbDtzyQm4ZMR3RSIUK4MHALU_glqbH_17GSTmOU-eHH_4OSOh_TEJoAr-FSY2DtmO3ayNYCs4qAIqblGF63Ji8xfbFMr8z7uT84_kLe-WWuXmc5QAzMwSpSiPAw9827AJ-ahLMxrhMJjIOf5vGtmnbfR0hRmAIka8WpX1tg2Ee_5NVf5rRLyA4msEJWGbDbSCd1L13FyxZQQ8li83u665cd0qPTMS9yJVhEHBFffoREvEGIvQR8tP5-OcV3hCGR-aF8SkYeZwkTo1pYWeZDXpjTHKz42PNtktWA68feP3A6wde_5Hw-n6m_uneZYMFzEMu2bqW2d2yuIuP3l-u9yfvWS896dJijV0aqAe78yIT4LuRrRieezdClc8hoyZOtiwXyxJi5r2JmcUadgEazepD8VX-HFcJ_cB8IxpgoCOby_ZFN5Ycm_X2lw_NPfSUkuGFnRkAs4AtV1_9_9XTvzll5sgK0ywhR_SeJtB5NnfuT1NqOt7bf57j2bI6Y8EEjHlpbo-8cZrB5DWHFZ37IFeOfOzEy65k87yK1bazKjXXItAfyxjYaQkzbe5xYCVAS-pMQimACajUQLYCAr79fSPJmKaLyT5v33sWBqhNffjFOtYGjTQ9tiCwI_n0unt_D435115cNn5eu7OZ532cq_bIignv8BsDMcH6gEwMT3mz3XPHsw_NbTNvNjMFxzqydB1fPnT2pzq21Phtxy_h0-p-yxX8UvOsc4bJOPeesz4LQ47yeg9UGFfJzYFaO2374FlCHFYuw65HXRUiYCo0ihB3IxntFeIaQeaEu10MGWLIEJ9Ghjhdnd45KzPqiJv4Xb92-Sh6bUCI5xOgRNwXCjFMEVUhdUPmU6nCCOMgDEVIkPbMXxzmFCmEiEspcFPto1Mmt6HcuvgljqauuTao78IgRbzIU2xQbv9Syq0XILAUFZSjlsJ1EkGXHJ4a1R9AE2Y-9wKB3VBEYtCEB034w2rCZlBPnfI-G0OOXpb7cb0d4KJXr7BCRa1PWNfZLBg3lhod5QZnamMdzHOmNib8SCIdUuqJsI2Za4Czvs3IxdClslPr3juuBIEQFroxmwnMYDZjKCAO4B6LeAGxserV2uj7hlqopAQu91qphVPGczOUpZgZeneDCeS1G-BXpdn_0EhDQ-rBGwvCS-s4Zo1sEJ6tlVjDZpqq_tIQR76CIFCL863lm9R3yFjS0zz0BPW5aqXHDmDrGOsEENae6xOEgYVchdcmW-OyTjnhUqwFNLlYmMsSKtpjPRlyN1j_jhlbjUxyGznPyIunI8ecBbGWrlesDolbvM1SqWIovAyFl6HwMhRehsLLUHg550ClbWG671jl1qdbJZudTzePWNqzjdP6blnjR7hd1oMfuNyj4HkbzhWNidsvcC_n3BxinP76ayX7wXv2x1evXh2UhnQUCKEVfZCr7bgwz9vAZz8F7ZdGgF2jlBqVQpCZOkaQga1h9zF86YeX374YF-XK8KcDiptURGPkogdTGKnHfSE8dNnTv-oHOwJ4K4qKjxmwDvFNgC-qjeoHgOVGoj50Q6KIgnuT8JEk4f7aT8e99pcLDNKtPL0R3OtWJ_u86Wht4O6QB63v47jHPw42b_OOjayZrg7ugvVKaHGujHSg4zflMt9qu-Mah5ehBp3jpmLSuxAdyx4c6XIhbS2t170mRw8kbwhklX3qNWzMVHH5quH6mujzjibjAOaBXFcF1NPIQwjhwKVc76uItELnxRWRIZ4O8fRTiaenlw_PqJSsawWPUikhAKKxebpRGISIuCKKiDm1DuhXecpzI6y0jKTCCmCx0j4OAqICwbiLZQB_0jMrJWZDv0Te1HenOOyplPAocP3AH24m_teqlGiqfRky5HuUHqmU9CaI86SQTg44SwoJKQwJY4Uq8ayquqxDfssMLw_nDUoZGTFL2ipJw4rLzIhQMjaQYd0wMGjY-SunChQ24VuW41QRbdTIxObh46a5W_PAc0P6xTK32ksdKi3zZ44Gr5hVzLJW7udxGs9ZsgugDOevKb5sztx043r90Dg7hxQoYDaG_zXrsNb9z1RNOkntTNUER5L7gGK0lG1rnQy2oZpclpvWVqnkJ52zosyXwq6WXV-zruNaamxFqQMr0FdA7KS5oYA4FBCHAuJQQBwKiEMBcSggDgXEoYA4FBCHAuJQQBwKiA9xfdh7VQ9D6rka2XtbfHjZ2fMw0R7i58rOT2v0wBbGX8ZZCoC8hQ3jKt7WYBF86CZXujBUCqjvoXuFBAFBKOCPctNM7VJNAWNdetPMl1Vly3KzsblLrKo4X8Pu1yBqMpncOLfmHr-w8eYsPu3Sqo7Zj5bE0MSHOMOSxYzVdvnulxf9BaaOwY82CxmqmVnXoiNHJxC3IaaPWg3oFnhvFVGr_n9-Ptln2qPdljMgTZAEV5Z1mwV35rDXkwqXYSeeG8Cu8sk-ex7tAbAUZIO8wl2JuoUBN3m6U-Q7r4bm76z_RWUzqRRBIfI4sAzhMcYVF54Qe8tmrep9vGw2BJI_fyA5vQi7XXrx3vUXUx6llKS0i0KD64lEiiGOvZAqFWEWRDwgXGjKI-1G2sP2v9APGWURMg_rQTQgcs98NqtH3kvkTgmdor5H0UodarAjHqpHf_k7JHXi5FlslUiOkCSaizWn7oTFFrxfHvKM7Z60X72xsP0rk4tvGgJzM7KxY5EV9qW6Y8nSSNLw-vel-c3INGhij3lVLIH8wBLB24YZ3dTxy3xUJdnxHb6p0vrNMl7r17Wy2ujL41QtIZsmzrff1dWkse1sQ5WuM-MsA-JSZ_Wfn1uWbrq29EzJcYMnLJKoIotjvlt3mfalbpElcgzOJ4EutyWmiqdkVXGpTe7FjC0g_VtF58WPDiGfO8ANwa8NKWfONyy_U6tavzTSTNUBk3exOPdmwZ0cdJHSBU7oIu0SINesrT6uU83G42YvSx-Git-xOLFcEdi3WZTMUD2LY-bxbc5q-R6W9n7S9QkH_MZog-axD_CT8T0DPg2uAF-wZYHqm4dWbKjaDlXboWo7VG2Hqu1QtR2qtkPVdqjaDlXboWo7VG2Hqu1QtR2qtn_652jU1dlHKM4Cg4jzLDWe94CP1NASPCnCWxeQ-BM0tmrKhGxKGMHRC0kO_vTgIxY1CilhD3ORkvKxzzx2QZHHCGnjWverEuttzhazBpRartTKdDboGkBZnPjAkPXyH38k6uba1ltwvJZa9jzDtV3WA89A7dwBsdOgXSAAxby_5fWa9rf80xLoJ7AtVbVvk5vcqlqap7qC6xu513A4FS9qQPTyx6fPvmx5ZjdO9pY3fypNAtu7Sh1BCpg9NGgG04D2s0bUgbr14M4rkwYR9gOmI-R6wqeS-SzgvgrpvjJpW9454cEnw15-tL18evF7u7znvuuv3j1OudJDxJWChop7PuUYMa79QFJFwygkyAfgJqKAuCEm5naCWkqhCfUijkkIhD7YM5_NcmXwkpCpS6eE9pQrEQ1CLdjwsNC_2G0BqUIh87kIZNteJ151Mey5QeegTtzGobOIoBsF2ggJiMi2hNUJO92C6IUhxWqbRhAzuoGw9Q7IF8WoKY8Y088B-smOVFkhP8in0qqVhTlYJOexBXmQ_I0JS1WrkOsc1nCNsdFfymxbTRvXOc5KrDnss9GaTVohoqr9wAjgrQrnVzUyU1Op7518R3bqR_UwNp51XiXQOzRxx3f22FGd3O2q1L7uFEwb4VdYwjDeVP1a2lTLb_VIjIfnzD4Kfb4w6hHMIzUFkOqPLEuATa-SjMnCCCBV1RbSs_ldNSaj7mWFVY9tnWS9rM1IDvGzoRQ_lOKHUvxQih9K8UMpfijFD6X4oRQ_lOKHUvxQih9K8UMpfijFD6X4oRQ_lOL_KqX4V-_-D3J5vWY)

[//]: # (ob:3d29c178)
# Constraints, Assumptions, and Limitations

[//]: # (ob:18f8786a)
## Authority constraints

[//]: # (ob:288f9ae4)
- Candidate claims are agent proposals and never self-validating.
- LM policy recommendations cannot admit claims.
- Staged claims are permitted only for bounded non-authoritative evaluation.
- No result in this artifact establishes legal correctness, factual truth, lawyer approval, identity, or external authority.

[//]: # (ob:eb0004a4)
## Evaluation constraints

[//]: # (ob:4cb418de)
- The pilot covers two tasks from one APEX world.
- Each normal cell has one executor artifact; verifier repetition does not estimate executor variance.
- Generation used local Codex CLI rather than the native Archipelago agent environment.
- The native Output LLM verifier boundary is preserved, but the result is not official APEX Pass@1.
- The composite treatment prevents component-level causal attribution.

[//]: # (ob:d0d2da72)
## Measurement constraints

[//]: # (ob:77ee4efb)
- Tokens and latency in the headline tables are executor-only.
- Task 1 upstream telemetry is partial but material; Task 2 upstream telemetry is incomplete.
- The recorded Task 1 upstream total may describe the immediately preceding gap-resolution lineage rather than the exact final three-model snapshot; that linkage remains unresolved and the value must not be charged to a specific final cell without further receipt matching.
- Dollar-cost fields are incomplete across model roles.
- Reuse by claim count does not weight claim importance or prove amortized savings.
- Task 1 Muse baseline includes a completed longer-timeout attempt after two censored timeouts.

[//]: # (ob:74e77a15)
## Safety constraints

[//]: # (ob:609bc148)
- The stress evidence covers tested material tax-status conflicts only.
- No corruption distribution, false-negative rate, false-positive rate, or adversarial evaluation was performed.
- A hard stop prevents output; it does not prove what the blocked executor would have written.

[//]: # (ob:457ab3ac)
## Development-set constraints

[//]: # (ob:f747fd73)
- The pipeline and prompts were developed on the same task family.
- Hidden grader wording was reportedly not fed into proposal repair, but this remains development evidence rather than independent confirmation.

[//]: # (ob:59dc0e4b)
## Implementation provenance

[//]: # (ob:8c6bcef3)
- Proofpress PR36 product mechanism: claim-centric CLI and ledger implementation through `9f6e3f1`, principally `proofpress_knowledge.py`, `proofpress.py`, tests, and the legal graph example.
- Task 1 temporary evaluation harness label: `1ff29dde8d395df085905e3e3b04b01f982160d6`.
- Task 2 temporary evaluation harness label: `0b7ddf43c44e143f6bba386dff4521802e5f8e79`.
- The temporary harnesses are not Proofpress product source, are not redistributed by this study, and are not required public dependencies.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzBiMzJiN2UxZDAwYjc3ZjEzNjBjN2Q4NyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImY0NGI4Y2QxIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8wNWFlOGRlMTBmMDk1MTRkNjE2YmVhNDYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2VkMWY2ZDk1NGIxMjhjZWI1NWJlNTE2YiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWmtv20YW_SsD9eNKNt8P5csaabFbIN0GbbBYoA2UedyRuKY4LIe0oxr573vvkJToxFYsq7soFgYKNKZm7uPcx7kz5N2MN22huWxXhZotZ3W98kQYiBR85XkiTbUfJp5MVZbO5jNh1G6lijXYFtfaDQ_iZBmrhPvA48AXWQ4ql77vh6Gn49yL4yiPk9wTAc9z4JH2dK68nAeS69jTIhVJFKFcVVhpbqDZzZZ39Ee7avkaNZS8JVVz_IeAEh_8E5pCF1yUwBq4KWxhKrbB9abZMbFjbxtjdN2Atbin5vKar4Gcuve4Mf8GdLdrSOCmbWu7vLxcF-2mExfSbC_lBqptUa1bXq2z0Lu8t7uB37oC_73qLDQraSoLFWLRNh18ms82wAlEHUUik8qf9U9WcOMWIbiw8mIOmQLf014e-5FK_EQgMglZZpqWXFuVRQVo-RiRcgXK14nK40j4QSZBxLGAGDf27gzWrSSvbVeiwwHZKU2j7Gz5y91sUH83wyibxtK_-p9BrQRC_svs9eAye4c-z96jJ2NWUJjbThVgL3kNHxdoVtUu4IaXlxcH1QvRFaW65A1fLEqzLuRiYU3ZtRiexYJAahteVK292KrZ_KSM423bFMJJWgluC0sGQalX3GIAWnDyunZjGnLruqhIpN3ZFrb4S8W3FP_77s1RgKXMmS2rrizRWbnB50BgvZ-PaM0wHWnRSjbAez3ul9FoWMU6yGLFeeiBVnnkZdKLVQgh6TWty7shoGwIKMPUkte1QShcfjZOExkx_jXYUJuykLuJhGl2TIS4vHtm4lij25VGVKCpm2LITyv8JYTCk1EU5JmWvvSjnGuhI5nleaJFHkRByiHyIUqiXORhJDnWeJ77Is3iQGRxTLJbTq7cIbb0_1ngBcnCyxZB8s4Pl0G0jMK_eN7S83DtgDOuQgEhdgox-zR5evenSUVRGnntAvTp0_zBqgJVtPua-rGG6up79too-Dh77wpVdfLRnz-ryC9__q3DVvj_WrHOyOcU7F0fFtwTqgCpJ81wOdrfwkdC4vXBkzm7srbb1mQY_sErxd4U2wIzlSTP95Yo5UysiV_gFp98w54qhQii3dXkAfV9dGBGmTJa6Gc6S7OE37PwykFRtDs2Qf2oOd-wx_Yc0R1kmc6xbs_TvWCv0eNCYUNksuTF1jJsW8xFj2Fy1cby0jpUKqyPhlHgF5h6uOVgX4mEfc84EJ7nRfy-cd_hts7BegIyj246Ak0kReQjJZ-pfcHebYDVRWla5oYZy9pbw1pury3TjdkyUwG7evvdv9itaUp18Wu1YN9xuWEVlsLj4ChPBYqnwT3zfgBuuwa2hPvT0Xl81xF40hQgAi3O1Y_4mGuo-uygwa6SO1ZUrEXUSC9xF3M01icVfATZYWddmKo8Ak8aQZpyP75n3s9cw0kV9eCGI6AkXi6QGrMztPb5giuxtzF8qBAQ2GeO6_VsizA1BS8Rl48LItXOknh9BI8oTrkIubxn2bdYjKWpKVwLC6ekzPGdRxDSaZRqlYZ_hB1jadXgkoQSCJsNNmHLbgFTRfViETDT55NFGnGVx45BFedKehDdz-zvt3Xp8rovftSDPM8xNF8B6ti-IzBlMhESdHi-DYvJ6Ye9_SlMWD9xtGwLxJeF3S77pr2QKLopJHv95vu-Gj8HCQeOvr0_xrCfWTHMu1f0pwuA28IErIuqIh7_9clMbH-dsdYMUayKtvgdRbqu2bMMHBrz1U9XF48R7OkGPkiGZxgzYdxnoPVsmm1RwMUZZk-4-HSzH2bNM6yZcPPp1pzKx883c8LRp5v5CJeeYc6Esp-B2rNZencOhBMeP93mL5n3DEsm3P68nHsep-OJH_nsXBgn9H-68Ufo-QyTJpPAc2v4OcTPt8V5UE7Gg9PtfpTCzzBoMiucbtDzhwNQa6SY4r5D7aYx3XrDPuQ6gVD7H-Yo8VTf3k-GnrvZ7WZ3z4e9jPm-lBbCdJU6JnU0wPlI9yA7htUIBOTTb_aO3NH2SE-v7KYXV9NrvLuXW4qXW4qXW4qXW4qXW4qXW4qXW4r_zi3F01_Jja-kBpuWfvjp4XdPX3v99oe8Y4tDzLsgS7IYt0aBjkMfsjz0EuFDEGdpKPwwib3EV6FIVQCRF2gtsoiHscaBiz_m0ANv20Jv6SUPvG3bv6T-k79tu5ttuN3geg8HE_BASuHavJMxGaeGrDx7Dhq0BUES8zDJM57no7bJaDRqO2nMGUT7uc4ViFSAtxc9mXwG0edMMf0lEDL3mx9Yn8yM3i9usVpV7zuTvMJZlnGFcAzy3Y6fW9SgphpraHBN6_pWuWPaNGwcwysMMx_8R7k3MJnGnbR_GFRsu7LtObQgiX0OMOQOrKfCbpBJS1gjfUjToJVthXk1Z7SmI05pUP4cqfh2hz7ymtoML-eMmKhF1OcM7UHEoKlw9WjM7uKBjjrAH2ZCREEoY66jEf7JbHeI7Clj2iA78ziXkEMs4myUPZnc9qE9YwjbElJQlgxVunXjCLKH9hW7cZ_JIF4N1IAokQvKINAUcgS-IMo-bLzhSN_YuJ2ev0EFTe91ZzHGWIeo0b2Idq0Yf9ug5BabtWOxqg_8VSM3RH18bcaDWXVTNKYihnCC3x0W_9i1ddeyN5iee1NdTvEGpy3LqLdAc0NHP4HrSM2YRr0PRutC0sjhQHrLrf2rv1eCiY7FUaCHLZ3wtn3BOKqw_Y8V9bKS-BjroLOUOIe31kdSJwDw4xjPhqlOx_BOJt9D6pw0ww7CRRp5KkIi8FUwCp-MtYfcOeeCjiCiicNnXU1THd_iFEc03g7IUxIhHgT7ONe96rcEj2wpKsK0hBb2ERg_ZvhSl2lR-JbvcBqyEhEHZ3iBnUkVqA77C0ZKAmHD1rxeYNgHPtl_RPN5AsJHaifIstQtNnjYX2wxWUtmK17bjcFywKUtbb9222GLsbCsq5xsTDIHJUmiege27WzrkkzQBzu8oXbYYlIzW4PEXJWDLleEtwU2HMRKd42ziowvaocd1sPQhb81Zckb5ENLdkKp-tAcgGNcNgYHot7wxmDw3MafAEuQPmxz7RgzqcN82hfyLRTrzdC86X6GJhSazrGi3TDG-BYfuVsYy2_QGDuN_w9ONLf9tIq2lJ2inGGjUVT6NLkssF0A-Yg1AsiljOuW8MeOhSOaNQ3h0y-xx9ouj4DjyJFHcbJP78Ox6FA7Tz3ljDWZhir1cq0S5Y1yJwefey33_JvZntOIqbq6b6vo5tg5iLVKC4sK6cz1OUxVGB-6lnR4SP1akXbuVE5usW6xryPnIs9iUTiNV9jrGwxia-pDIzOuh75ixSQj-rDfUrrvbwHRsX2jvzVdqVAYLWqI0481O59LLgMfwszbB2xybjsE7OTT16AAD18yVFokySEjJgeyz8jyjDtghPDvBU7JFVs3XAHh0LgOQ1AjRRr6LAlbD0GoURBabvYjFi3gRTMyUWH3HUQd_D6k1LQ74SEI-bdSAwvoAsn7KwwTRzoMBRdeouIRk8kJ8AD6iSe5QTz3FNCAEmYOYid-crjbQ_6_uC3GllPUvETcP0w-Yr2uzK0TclHvcNnkp_4B1eowylOw-8kRw1pviAhI7bTJUcMyDU0VkwLDYqIZk7mPipfsg691kGN6ZCrMY6W9jL5chpC-g4yE5-s8C_zEU8mHg-TgaZLxVKOUjkIZReBHoU6E4GGWKK2jOPAzL4AYzzRp_mHPnAexg6yBxik1J0EZ42FN10jsJuMS7MVjP8I8RuJwCevuwXvMDgvdd8xYSx0O4ZKNiSrxwPdFer7_hP_9B3lMo-8)

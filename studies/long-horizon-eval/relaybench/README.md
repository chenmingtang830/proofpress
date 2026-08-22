[//]: # (ob:7b8f6fa6)
# RelayBench v0.1 — H4 Phase Zero freeze candidate

[//]: # (ob:f912c31c)
RelayBench is the execution, information-parity, cold-boundary, deterministic aggregation, and reporting layer beneath Richard Tang's proposed Proofpress long-horizon Harvey research plan.

[//]: # (ob:ff436f24)
The current scope is deliberately small: one approval-blocked Harvey MSA candidate, H4 only, C1 ordinary portable workspace versus C2 Proofpress, one genuine process boundary, and deterministic TEST-ONLY execution. No real model/API call or benchmark result exists. Richard's single review entry point is `PHASE_ZERO_FREEZE_PACKET.md`.

[//]: # (ob:979c2fd0)
Repository integration note: this subtree is stacked on Proofpress PR #22 head `10ee8c4c9a6d56dfedf563a0679e6a5bb167fa0a`; it does not rewrite Richard's plan or flow files.

[//]: # (ob:83b60139)
## Review and validation

[//]: # (ob:3c4f2a78)
Requires Node.js 22 or newer. The project has no runtime package dependency.

[//]: # (ob:f79e70a9)
```sh
npm install
npm run check
```

[//]: # (ob:bf8dbb39)
Run the synthetic mechanics calibration in a disposable output directory:

[//]: # (ob:bbd0a989)
```sh
node scripts/bench-run.mjs --adapter deterministic-test --test-only --paired-replicates 1 --output /tmp/relaybench-h4/test-only
node scripts/bench-score.mjs --input /tmp/relaybench-h4/test-only --output /tmp/relaybench-h4/test-only/score.json
node scripts/bench-report.mjs --input /tmp/relaybench-h4/test-only --output /tmp/relaybench-h4/test-only/report.md
```

[//]: # (ob:4cb1cca8)
The scorer and reporter exclude both TEST-ONLY episodes and report “No benchmark result.” Do not attach a provider until the manifest's Richard/Tommy approval gates and provider-dependent fields are actually frozen.

[//]: # (ob:80648521)
Start with `PHASE_ZERO_FREEZE_PACKET.md`, then review `RICHARD_PLAN_ALIGNMENT.md`, `BENCHMARK_PROTOCOL.md`, `BENCHMARK_MANIFEST.json`, `CLAIM_BOUNDARIES.md`, and `BENCHMARK_READINESS_REPORT.md`.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2YwNTg5Y2ZmN2Q3OGVmMTcwOTNmN2E1ZCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6Ijg3MDZjMDcyIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9iZjZiMTA0OWY1YTVjZjRjNDFiYjk3MjciLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzA2Yjc2NjgzYzYxNjM1MGI0ZDUzNjNhZCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWVtv28gV_isD7UNbVJfhnVSfFEfbGBtfILsFmt2AnssZiWuK5A5JO4oRYH9EH9s_t7-kZyhKoh1bSeyk2AX8EovkzJzLdy7fmdz0mK4SxUQVJ7I37hVFrKgXRkKpQAYhKCugkaMC5slev8dzuYplMoeywrXlgtmeP-aeslUYBhEPWITbIkoD13P9kLquSz0aUOmFgeKRHUYy8EPwaeQpCaGMHC-KzLkyKUV-BXrVG9-Yhyqu2BwlpKwyovr4g0OKL_4JOlEJ4ykQDVdJmeQZWeD6XK8IX5FTneeq0FCWuKdg4pLNwRh167XOfwY0t9bmwEVVFeV4NJon1aLmQ5EvR2IB2TLJ5hXL5qFDR7d2a_ilTvB3XJegY5FnJWToi0rX8KHfWwAzTgwD6gsa2L31mxiumkXoXIi58rlF3Uh5zBPKFa7FeRTYgdEs15UxLU6TDFDzDSJpTH0e-H7oCN_yHY9yV3qO7zC5NqfVLhasKOsUDbaNniLXsuyNf7zpteJveohyrkvza_0ZZMzR5T_2TgrIJofkIJfwrvcWDdkEhUG5qmUC5SjNs_lgkevkfZ4N4IqlIw0pW3HIxGI0m05eHk2HS6PRlwQUqyqd8LpCHGPOyqQ0AiFVMSvRvxU0a-oKxRqtL5PMHFmuygqW-CVjSwPvLe37uL80cdEbZ3Waoi1igUDC2hU8zcUlbgl4qHzFfFyOGFbwzlg6M_a8MPaQKzq0yG-__pu8csnpgpVA3oDOidIA74EI3NbqwqSENQwYjnCNb74jn38Oy2QiMcbxgGpVGFtMvGDs9T70d8qqyLKFY4lvoGznlKQk1QIIvAPR4NEnSaZyvWTmYVAwnVSrPhF5Kgc8rzPJdkrjR3ZbY-U6vrLdb6DxOeooaq0xpAkWjQKM4hLShINGT6YrUi5Zmo5JngFhBaYHhuqgUQz2aBw63KeWE93R2AgliBLBQwxSJq72YW_Av3_PHnwd4SqbBeHTZM_aykSOMQ-GP5fEtkmuSQbXoIfEuK2tfAQdTrKc6DqrkiW-ZmIflEEEAWVPdMzFxUW5-CnLiiVGVVkhQOsH1IFgvRWXP2W4ZKeGQBtuqcFVKDl_Kj4zFGeCvFxl-KdKBFmCKQ-JKDEZMYZ0cwTqSBjBPlTkZdNr8roq9viIc4keCr-Sj9B0jGydFFU5aqrrAL00XCKigwGTrKhAY8Djv9iksPUlYoBNco_rXMEtIdgTw8sEEOabRuFmkwbTrfAB3om0Ro15Xi3I-fTsfHBy_PpfBIqkREXKZvG-vKO-G3q29TTlzipsOuQaezi5OH01OZvGb6azk_j72XT6ZhqfTg5-mJ5jc7roG_Qzst5HLmaHB68md5V72980zB4yEtNJYqGBrXtR82XT2CBmzEcqoyQHyoFzW7rUYlQYa7K8as5sezppe_o62os8yaqGouhGkulUmyfTqN4aMpAmYtU5oUsQOoc01OOR3KHMVRUrLEegC520FKXk1lg6nht5jggt7suIh64fKGqLwAHJqXQ9JDAiUhhUvkeF7zmWzSC0IfIBLF9FJhEwyauGaqzRGlsUW7F507Op7Q9oOLDtc8sZe3Ts2H-ldEwp7mo9jqukaSGeSzFadm9v_m_EpInPNWfAcrkwCmGJ9pwwFIoaLJozOjSiDd2v1_1bsdzzvADxcrxQbsR2CMHHvfWL-7jGx1v1hLD5XMOcrXfvsh01IygGkx59ixmxILMEq6eW5BwZ1p9K02CwYoLs8HDSRYe8YvoKVnhcCUyjrkXKsuE91WHj8kCaYEOIHH9r-45atLY_hRHIjUpHZ5MdIH0DWJ6l6JgDC5soYoJeIttcvs71ZYltE4iJzLokB3bH5H4jaA5ZjalofCKMH3a-Ng697e9O2dygNsQ2jn5iKVliGU1Hk9ND06FS09KbyF4yfWkcWacV7sJzyuEGDkSiRKzaGQkLHXqmUR9T3Phmb4ncAwcLwIocB2uHcDZwdHjTJgO-iAO1Rwfgcum7LnfDLdIdWrSN8sdTHDMKottxVJDovtUeMxV1vdBn3APlbqNux4JaXR7NaDbOdLBgOlR5rrW1uENyNhY_gbDUFb7BQc8Mx-OHzQULbBt9zxW3torsCM0dcx9FTir8aP4MTE7h74KhXnKAVQV7nBnxiYVvW51H1bLoVPDBwh1t996rQMNKWhWS7FNHfJ6g0frQn8s8u9_opiB-baGbU-UnYod6dhQwZVHhBBvIOiyvUxcfy9jWi7F3_QfL0N16M_zt1_-SlzkmWEVwgGdYyJnJvKtE4vEm5dImaJcYpwqNw3rUVqbReb5crrZFmMwb8I3AzfbBJkUrohJIJX7VWLVFVWOGrbB15u9hX8sQtuOia2wJbritUTuO2brmKXxx9jI-fT05jievD_9-fDQ9bhdevJgeH7w6msx-iE9nJ-cnByevP_pwNDk-_B4d3sSV-XTwenJ4FL84-cfxy8nscHq23mH80dllKMzh8fTsDH-dnszur9JvPxgn3HPTAzKpHrjnaS6PZC0e_Lz3lmh9F4bwbr8vakScbN5q8ufE4Ih0o4mUFmH5l9__BRO2ioaef-J-qXcrjweFYXiD98jwsCJUMF-X5t4DN1BREAlbSfpNLnWwDSTNnWhHEQMCjDGgkQGUNa_wIEMGsHU1PAgXGApzzzQkUpYsH1T-jhbt2DMxjy0PRaS6hLAVOODGJhPqWHbSnYYEuWpTfloLWoPXxg3XCm38ddO7XqzW0hpZu22DsgCRKOyXnxLXXujKRu5dYV8wCu651137pDvjdeeb7tx38wcPlc8fjz8aDz_cP_x9ahL-KuMuguaCCpQCy8LCgWOeI70gCD3lUMsC33fA82zXtwLHD3zm-UhNqRVFnqsiHAGjB-y5b9r1xi69Z9rd_o_B87T7PO0-T7u_h2lX8QCk7fPIoluS3anE21B8fAFtY-Z0Rr7DQdZkA7mwKEAoXBExX3q-VCAVlhtGfRxAsfJwbvmBYpRd_I0kON_lUDbkSsM1Rjp0fGKCzbhPpfk1UukUyufJ_nmyf57snyf758n-jzbZv_3wP72T5M4)

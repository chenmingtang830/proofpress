[//]: # (ob:1ce270d8)
# Contributing to Proofpress

[//]: # (ob:61836140)
Run the tests first. They finish in seconds.

[//]: # (ob:57a5f00e)
## Development setup

[//]: # (ob:04d2b288)
You need Python 3, Git, and Node 18+:

[//]: # (ob:08829457)
```sh
git clone https://github.com/chenmingtang830/proofpress.git
cd proofpress
python3 -m unittest discover -s tests -v
node --test tests/npm.test.js
```

[//]: # (ob:31d45337)
## Architecture constraint: one file, zero dependencies

[//]: # (ob:5b59c3c5)
`proofpress.py` is a single Python file with no third-party runtime
dependencies. This is the distribution model, not an accident: recipients
verify handoffs on machines that have nothing but `python3` and `git`, and
skills vendor the file directly. Please do not split it into packages or add
runtime dependencies. Internal section structure (carriers → blocks → diff →
ledger → commands) keeps it navigable.

[//]: # (ob:5fd936ad)
## Scope boundaries

[//]: # (ob:a0be59d8)
- Proofpress versions **Markdown and static HTML knowledge artifacts**. It

[//]: # (ob:56bb32f4)
  never versions source code — that is Git's job, and features that drift
  toward code files will be declined.

[//]: # (ob:c46dcd3e)
- The executable contract is [docs/PORTABLE_ARTIFACT_SPEC.md](docs/PORTABLE_ARTIFACT_SPEC.md).

[//]: # (ob:bdaa59b0)
  Behavior changes must keep the spec in sync (same PR).

[//]: # (ob:f2c66c00)
- Privacy invariants live in [docs/PRIVACY_AND_DISCLOSURE.md](docs/PRIVACY_AND_DISCLOSURE.md);

[//]: # (ob:0e2e65bb)
  changes that would leak local-only history are not accepted.

[//]: # (ob:327a0850)
## Wording discipline

[//]: # (ob:0ed25c68)
Proofpress is **tamper-evident**, not tamper-proof. Public-facing text
(README, spec, CLI output) says *checkable record*, *tamper-evident*,
*provenance that travels* — never *immutable*, *tamperproof*, *notarized*, or
*can't be faked*. PRs that cross this line will be asked to reword.

[//]: # (ob:23f94073)
## Update documentation

[//]: # (ob:ec80f405)
Every tracked Markdown or static HTML document in this repo is portable and
Proofpress-managed (see [AGENTS.md](AGENTS.md)):

[//]: # (ob:72e8e335)
1. Run `inspect`, then `import`, before editing.
2. Preserve anchors and write claims for changed blocks.
3. Run `snapshot`, then `verify`.
4. Commit the updated document and capsule in the PR.

[//]: # (ob:31fb88c4)
Do not push `refs/proofpress/ledger`. It is local working state; the capsule is
the public per-file record.

[//]: # (ob:69babc66)
## Pull requests

[//]: # (ob:578fa3b9)
- Include tests for behavior changes (`tests/test_portable.py` is black-box

[//]: # (ob:593d02a7)
  through the CLI; follow its style).

[//]: # (ob:9950245c)
- Keep commits focused; explain the *why* in the message body.
- CI must pass; the full suite runs in seconds.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2FjMWJiYjAzNDM4YjgwYjlmNDdkN2YwMCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjJmYTc2YmY5IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8yNzViNjI3MTc2YThjNjM2MTdlYzIxODkiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzdkMDNkNzFiZTQzMTVmYTcxZGEyNjUzNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtW-tu20YWfpWB-qOJKym8DS_KYgE3SbvGpqnhuF0UsSHNjRZriuRySDtqEGB_7QMs9gn7JHtmeBFlS4wtpUGx0J9EEskzZ86cy_edQ38YkLyIQsKKacQHk0GWTQkzKaWG7dg-9Q0ahI7HvdAwBsMBTflyyqMrIQu4V86Jhd0JYWEY-JwJjh0X84BZ2A5CTrFBsOE7LrGx6_iCebbvCAs7THiEmtiwPU4C38Ugl0eSpTciXw4mH9SXYlqQK1ghEe8LuBwTKmL4-rPIozAiNBYoFzeRjNIEzeHuNF8iukSneZqGWS6khGcywq7JlVBbWvs5T38VsNkyVwLnRZHJybNnV1ExL-mYpYtnbC6SRZRcFSS58m3j2drTufhnGcHnaSlFPmVpIkUClijyUnwcDuaCKBNaIfFcGgaD6pepuNE3gWnF1PIwdS3P9FziM9d2TU8wy_TVvVmaF2pr0zhKBGjenEc89bhhc8-kwrFNDMJNTiwX2161nVq7KSOZLGPYsKX0ZGnO5WDy7sOgXv7DAM44zaX6VF0WfErB4O8GLOXi_eASdtD4Aiz84sc352cn3_50fvLm-_GCD4aPchRSFHlEywJOaEqJjKQyNskTpShcA_8RWmRZzNNcqXQdJUqqXMKVBVxJyEKdXaXacCDhQZA1mCRlHIOibA7HI6oN0jhl13CvyYTlGdyH2-FkCuU6sA34VGmSXKEiXfeRelHCudYmU04lbuGXr1Dvc8UyU8qp04XLg4_DlRKu6cOpOsZnUOIc9ngtUZjmaJmWOYpAHDxTjDvPo0giuSBxjCAUsjLPUimeo2K-UjIjOVnTEHsEwyGJNQ1fgpfEabYAV0FSFGXWa52v0Kb7e6xiONyilu_vvubpEjwlQTYiCUffRwUiuYB9Cth3vER1XCpRlcHUFZFcQSSN0ZseYxi-bwUO9nZXbDabyfkFLFUgFqeJQI_JKSvNlKOvaWab3MG2va7Zcc7mUQH5q4Tdq_RT5ATcYoLUwmEUiyH6TeQp-sTpPVQMF5lIuEhYJD7h9pjigNkMf3ZtZ6sMN86WM-XvBElYHmpA7RNKEroFa6MkhYOPcj6Ccy6WqC8IQh7YLuFr-r5laSYQTcuEk7zacp8VN9zeYyFiUIGDO9npMSuOumEPtVLlQ4mOjn4g-TVPbxMdGbIgRcTQ385_eI2uk_Q2FvxKILJSLYZyuW4Jl1LbCp2d9UIogXjJVypJSFZMHTgX6Pd__ReOhBTq3CBqv5bo15QOtaqhIOAYPWfEHJczbos9LHau0sB7wUpdWZUPggsyrc07njL57PTHs_Pjb1-_mh6fnZ98d_zifPr29NWLqt5tsxjlhOCAGntY7FsxJzcR5Km6jqFFKQt0LUSmM5fMBIN0j-QyYeiJhFKITs-ejntsFVrMdZlh7OVd0Q1hS1j3Bu4mKpPG0Y1QetS2Ojv5-fjFL9PjNy-nL0_evnj949ufzl7128oQlnAxpXvYqjGRdqPbtIw5igW5RrACiUc6_TcYUNWEJIXawJjICtFjL9vyiOHjdXv9A0CRqtAKjUaZgmGfyAAbH-grg4JbmLn-Hquul_6jo4IsMpGP4DLk6eLoaKgNUP-qcyfAhZLGERuFPfaw7DBwDM9er4Nw6tqmPL0K07RSpRcVbHqgxx6C-UboGHiPVdvsBy5aVvUfHBaqgARQkKVa0MpmowVJAFpzCCohLpIeg7gBJRRiak21UwCfGmsACvtUdbh7b1_x9PyQ2DTYba0ROklYXEKyVbC6gj_0bn55MtMXn6l_pw3TGGd9dSGwuWERbzelEBxBnpZXc53PXrw-eQ56xXF6iyJQURbLWPTmsyDAhuVgtqtJ_q5SKUCvRaQtwoCv8edQCrKYaPcQ6Oh2vjxC9ZcF-Ab4BeSke8nsctgwqEFd4aYsh9Kll9RXGj4kpqbBBMbCpdgRDnMZCUPXDrFyIohKvdHa9KgmeXBAgl1nKcAizVlzvZIiOc03xXEuFTuEEF52JHQZY0eI5qI7kkmZhsU0BO8UeZZHNWeV1JzgwDOo6XMv8EUIMIZT27SEg-E5M-ChaWNBLB5ans8sZniYu8TwXF-oNYRP1P4VMNHcszqtiWUBi1O_DCzDckeGN7Lcc8ObOPbEcr8xjImuZbXFlUM4FhcOFJKPnV8_fD7Cqh2v4pNzIudwv4dtxyO-RQKhjKNldChm7ZOPZ4q1eM6M0COmYfum1YjvkMda_D4cUEhdDSH6NbCIioukqqFkuSn0mm1TlxJswjFh3ujVoYzNth9MAWuxhIYGIQ7nri66WmyHFTYRvgfLU3DT9L9R1kiEACe7SPRTzY1JtkAxKRMIlrxKlX1W8LjDQmY4NqetuiuuWKu7F_eT4yt1JIyj1U8XSaYtYKPRApVJpDslqOmOoZGsc_zo5iJJ1IZHI31Hldxhh2P1afwrCALdNrDLenuuEIYXgCt7Jm621yGcq0P-fEyxXtkOPFN4to0JJa17rchjY9g9WF9eJkW0gOre1WkMVCDSkaJcQXUYm_YUWoBt4go2kURBR42kJuBtAMci5WsXyY1qPALOBLdMw1CqQFsQsEzS4FIotzrY5ioJgGA0qw9ypl15Bkc907TnIpHXURwrBgeyKs_UW-Hg2ayIlxDZAG-lgj9aJwmQEAhLoUI_RXVXEzTIEYToRVLvFq1v9kSliYTEEJhMbxL2W1aH-ISRHEB3LtHv__4PqtKe_sijMFQfLhJNGnP9oyqhoLV8qnOIVHokgCyuNHzYHj40dBxOVJvTZ-0pryj3yr8exqEbqabnO4ZlEbGS2qHVtdR9eHJdMOTREdiw2ICOak2ETR1qmp5DudPub0Wka032Y8aNa3FwPcgTgKjSW5Lz6mnlMhLcH5I-VYfPVJ3nPSdiOZRA2XcDYrRx1yHYre12Z8yXT_qvd_HeXXt6zKfMZ57t2m6jXYdmt_b8bLy5Xje0BZiFe0AG2yLcodIdj9qVGzdW2Xb96fMeq3BXmASYqhcEbRFaEerWKrsz5D6PMV1mmdyjXsDb1Tu0eRXDD2XBTe3xBHYNCGEWuKtdtcS4QQJ78FzCNBQDQRfJk7NXxy9_eDXUvjFUTASlZZGVxVMkyRIka-xcj5TUVAQk311seJEcwRKQsUnCRGVmiAqAP_JIx3EV5kfRYlGFzUqG1kx9BW3Bc34TSn6ag0BGkq8LFbwhuYZfQfuz-gRZnkpZUVhlzDbKiYQbFcLMxS0o2pd-MfFw4PoU4qkxcYfhdzDcAwl7k_YwZWGATSPEYSO3w-FruXtR8nfH3796c_5WR0778elTSMdhhYBPz4CtkQQ0C4ElLatBoFD4oBHULAvHBqhMVgAyTtNs0lZltIYvkExIJufgT39RefWvswpXwI0KW-mx2UXSmWhVWVonGS26KpdPtgmH-2bgbQqlwAbvDS5rT6rWVPKUkXoO1zED7PiG7RkrJN3pVqwO9wEdiKY4EBZyLLgR2HSF-dumRJsGd280VBiOxgBfRjR9vz3n2aYpQg-ogo9X-HDVimhz3m7thcaEgSMMRoRBWctxOh2Hdr-7dxGW44tkhF6cVAUqI1I-r6CeOhNZAqRWOFUHBkC0FBDWvep4-VFpvGF6Kzg8fmd2qyfBvGT3f988661G2XoMW184i-AIc_7nGAODFXVDZIcp8KN7ioD_ozDqZr7KXcBGDM55sVX8_efrJs9LESo0huqJvKxrVQ1QIqKiMoQkUpGRTFct1CkwNc3QAdYkM6JhPGt7DQAnx5WOzSY_DMAX1QhdKP0L0RVea7KSnKcLJIDBrCSmOUBQjRiUx2exKJrMplouD26BAWADXmliz_Ztz7RCTIhhcv2SR2Wdbm-r29fp9rs-_OEn-_DGXdu4aqVNzI-bO1OfatN9ll4c9UyiUjO2LC8MITV6wqSA1CzL9wPDh_8Js81AwUTGHdWzIwFwJOECWTFdh2zf0qZunDsxN3XjgDQwYob40I07dOMO3bhDN-7QjTt04w7duEM37tCNO3TjDt24L9SNCwJsEezgABNvezfulXqtXhmIKX3btAtR2826Dc1c79TB_-0LC7pabmnboe1du0SddKETabRQwnSHpuajFwkVAAghx_FIAfYx-k5V0k6Dr33Pf4jWe3lrLbqKp4Nj6CYJWmvVzZrmXlXx0axCD_ANRCV1d0eLLTOuOC2qSzJIS1oO37R4Ts_GcEza27NSztEMmLzsoMhnVbWePdcYQbZUGsq4ptbgKtcqHJTtAa3dzhXYUILbddabAuD3Go80xL2KikN38NAdPHQHd-kO7vznGdt6SXv8kUO3cVguqFDn9-7dQNUEezi4vHzk25o_6fS13jDs0__BL2Q-VvA9dT1L-AJI5iOk3n-nzxyjszJBs6iqKE3-nlVVBb7eKSUXiaXaMkKK_Eb0vOdomyH1febspdxDSoLiMCrN3S0ED-s7dxx3a9_5BwBFvPIyXep0IWnq93ojWS0f6oyoeCyUx1wPuipyCtRyvM2zv_ziHWf_8os_pN3_hy3eiZs7nvdHr9wJii-x8qYxxgKAeNVsDMNID03WxVYiAB3lsoKXAiqI6iXCGoDmHzW06PmrzI1Di7b9_emhxaHgHArOn7_gPHyId-897mFniuR83Dwk-iKDMccTIsTMZRS7huV6HogQBjdIyAzfFK5lEpdwahEeeAFmgWU5TsCImikQG-up0ic3d3dEZpoT7E1MvGFE1v4V-P_LiMyxGbaIAxe8YPuITIWMyto1CVTZWXX7xRI-JxF460ZO84XGXj42HeYJizMcbB97_ZKWembVzDbsoWoJV92DZq41OQyrDsOqw7DqMKw6DKsOw6rDsOowrPp_GVYJbPqmi60Qqm3vsGoLY9l-eNgOmOOTgHvM_HOOq3pAHcfYAEgnTNdu60eHZdbK70UZQWU2T6G4qjx-m6shQNUH1KOUKlB5XXXhSbteqzPeqhar51twizMGrH9vvNXabvN4q6dyUUsYvmdhusp4HTLbvpC5OzMF_Z7fmYapt-Tuj8MOY7DDGKwZg11-_B-6u-zV)

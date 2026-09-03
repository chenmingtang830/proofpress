[//]: # (ob:62eb3106)
[//]: # (ob:repository-dogfood-title)

[//]: # (ob:b73545e9)
# Repository dogfood

[//]: # (ob:88e7f6f3)
[//]: # (ob:repository-dogfood-purpose)
The repository integration turns one bounded Git change into candidate evidence
for the same governed lifecycle used by every other Proofpress workflow. It is
for a single repository and a concrete base-to-head change. It is not a
multi-repository ingestion system, a PR-management tool, or an automatic
approval path.

[//]: # (ob:6e81cd20)
[//]: # (ob:repository-dogfood-flow)

[//]: # (ob:488c5685)
## What the integration binds

[//]: # (ob:4b26b612)
[//]: # (ob:repository-dogfood-diagram)

[//]: # (ob:efb02e73)
```text
base commit + head commit + changed paths + diff digest + check receipts
                                  |
                                  v
                    bounded repository evidence bundle
                                  |
                                  v
                 candidate conclusion + deterministic evaluation
                                  |
                                  v
                 independent human review before downstream reuse
```

[//]: # (ob:8fc6a452)
[//]: # (ob:repository-dogfood-boundary)
The bundle records the canonical repository identity, two commit IDs, a binary
diff digest, changed paths, and one or more check receipts bound to the head
commit. It deliberately avoids uploading the repository, source files, bearer
credentials, raw CI logs, or a full agent trace into Proofpress.

[//]: # (ob:407970d4)
[//]: # (ob:repository-dogfood-build)

[//]: # (ob:c8e57c12)
## Create bounded evidence

[//]: # (ob:74669b6e)
[//]: # (ob:repository-dogfood-command)
From the root of the Git repository, create a small JSON receipt for each
required check. A receipt needs a check name, `pass` or `fail` status, and the
exact head commit; it may also contain a public run URL, workflow name, run ID,
command, or output digest.

[//]: # (ob:bbdc846f)
```json
{
  "name": "Python tests",
  "status": "pass",
  "commit": "<40-character head commit>",
  "workflow": "CI",
  "url": "https://example.invalid/runs/123"
}
```

[//]: # (ob:7847860f)
[//]: # (ob:repository-dogfood-bundle-command)
Build the evidence bundle with the canonical CLI:

[//]: # (ob:28fee3be)
```sh
proofpress repo bundle \
  --workspace . \
  --base-ref origin/main \
  --head-ref HEAD \
  --check ./ci-receipt.json \
  --pr-number 123 \
  --pr-url https://github.com/example/project/pull/123 \
  --output ./proofpress-repo-evidence.json
```

[//]: # (ob:0ae587c4)
[//]: # (ob:repository-dogfood-next)

[//]: # (ob:1f0ac5e4)
## Propose, review, reuse

[//]: # (ob:7d5873e2)
[//]: # (ob:repository-dogfood-next-text)
An SDK, localhost/hosted HTTP client, or MCP-capable agent imports this bundle,
proposes a candidate conclusion, and runs deterministic evaluation. The helper
intentionally stops before Human Approval. The owner reviews the candidate in
the review surface; only an admitted, current, in-scope conclusion is later
returned to a successor agent as governed context.

[//]: # (ob:96dbd16b)
For the common product lifecycle, see the [repository README](../README.md).
For the hosted cross-device version of the same loop, see
[single-owner self-hosting](SELF_HOSTING.md).

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2ZlMGU3YzdiZjFlMDQwMGQxYzhhNThhYSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjQ2ZWM2MGE2IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8yZDZlMWE5Y2YwNmEzNzBjMzU4YjA0ZDAiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2YzYTFlMzQ5MzhlMjJkMDM0ZDZhM2E5YyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNq9WeluG8kRfpUG_cfG8ui5Z7hBAMey10q8K0FWEgSmQPUpznrYPZlDiqD4d95gHyGPFiBvkeqeg0PHGtEraxcLmezpqaqu-ur4mncTUlSpJKxap3yynOT5WgosIhZR6QjsY8wdFpMgJmQynVDNb9c8vRJlBXvLDXGDcBnzxA2wx13qRWEchizh3HW8hDpR5DqYRWEgReiHDuNRHMQ45ph6sXCFn3i-8EKQy9OS6WtR3E6Wd-ZLta7IFWjISGVUTeEDFRks_EUUqUwJzQQqxHVaplqhDezXxS2it-i00FrmhShLeCcn7CO5EuZQe8uF_lnAcevCCNxUVV4uF4urtNrUdM70dsE2Qm1TdVURdRV7eLH3diH-XqfweV2XolgzrUqhwBdVUYtP08lGEONEPxQsxMSczKysxbXdBM4Va5eHwiEJkzgkXoSZF8QU-xwby3RRmaOts1QJsLyLSLaWHnGEB_4Ct7kcez6Hl0FIc5zWujUjeVlncGDX2Ml0wcvJ8sPdpFV_N4Eo66I0n5rHgq8puPzDpFYflb5Rkws4Q4cHUM01Kxdnr09P3h-fn5z9bX108sObk5Oj-ZZPpl-FG1JVRUrrCsK1pqRMS4Mekck1KcGNlbDy6mqjC2Pcx1QZkeVtWYktPFFka6LYGTmFV0sT-clS1VkGJrMNhEo0h6WZZh9hd-gK6jnYxACiVIl_mAM9_88v__rvv395AYutEsK51Z4bOIkbWPmwWFws0TP0XNNlIXJdpgZdM66vpNZ8VqVVJoyA6ja32CIFmXya7hTTyAv8QCR7is96QagVNGbCM_TF_a1GAymA557SOBaRDKX3CKUPnDuvC1gTL1bqfGOSrxedgrqrEX-EIobMd_HTmSYzfTMWET-OWRDGwZ4Ff92QClVwFGt_QQw2EQULytHIPEOjL46EyKduSEPH_QZWPOAPnhIQtR1ziZAUuyLyvoExl5eX5v2VgsQWCAroNq3Qd8i4YPetyVCOclJtSvjOUynhzwA3THOxD2nJQuIHv4G_qK4VJ8Vti20K32x_sRUUjQELR0mEuf8bmFinGR8LKItFELHP0PWqENBAkT0fOB90caGYeADg9781gu7ID8OEhuKx-h_wgwEUURwi9abQW-tm6H8V0tJ8HqvKlLPYD-Vj7QO0_1xqtVJ3K4XQyvam1WQJn05voX8pZAaWcjWZNo_LilR12WzIodn1D9gI8qPYj-IQyyf2ZYPzgUv_YEBmfQoSRnzpxlIIj4pv4Mtys1K7Cca2lS7_VivjqdnsRhcfS5jlBJr3a6bUzAox4kNMRBBHzH9iHyoQPJaWjsSEBWLfDJhSTSudokaL-RemyQey8t6XxpKSgw884T5S-wE-mBnhAKGXCr0_-tMUgQEk2-iyWow4Jwk55U5IH2neG11Y0BogQwICnHjNKpSlUrBbloGoUgi748NgbDl7_fLox9efW3cx7ablCdARM2SumQWNUWmfdOPu6CSvdGVltgM9agd6aIOCfcw1dAbLTwqryQyx3Tczw14YJpCl7HYgYcgOBkIs7_iVxKHUslpLgIwo8iJt-UlJnSXmHg-BuzGMg9CBFpwEzIloDEeTJqcETTyHBlFIpJtgJwk8SR0ac5cwX4bEMbKh7Fme0URr6cQwpZuViYvdcIaTGXbPXWfp4KUXfIfxEhuvtR4fEqhPg9W7J6EmFowNddiQcmMGDycKsAshlcQIszIGbKLF6a-lCa0SYAmMSZ9xHotOyYA5tEoOJwKtWDiX50oeUiLDTuyAGxxm-_io3040VV2oEmm1K6c_wKTXzHlmo0YMukrKTcHtCu1KyTZXS2ib6MpQfgVv9qmKINW5IfLCXAYgDVuLAalHpheYaX-OjiuUlo08gkrwQrZnKaiGdagqkL2m4pt-UelZM5RaG1sRCFIVkZXa1lmVzvbOam45zEkbHjoFeadnM2iVkGBbSFVUaZ1NkTFAISCveguOYStFcqhA1ySzs-78fgQQR8YsZNjxvLiH2Y4rHRaq-6hPqwNznASYSkjRHg4DNtSh7OtJTSufBzKmjgh9QXEvf8dzDjvDCF1p1cDc5iZcejQStFMzYDCtmkcREYi1fQql1Uz-Is1hioNZ46H__nnIpusvb-oSZ4C6LlPaIehJLdjlp8mTrLaXaeARSJhim6oU0M_AIJLVFg5PagsgTeQC_kBebWpIsrb9IyogxQXUvhtVVtCJt808sFIQ7S-Mfy1gvNB3YuHFMZF9dR3wycNwOU4L7cRBlFYpTDp7RdIcIq1up6i60R3wjo9KU0Ago0DgSg1QN92H5NSWLlNWobBszdH3MdmABmqPNcBge6UaHbagcZGlVED-igyK4LVOwdI6z7TN3IYu9ZbCXKTrArAm00yAYipgBClWpmTaI5AMFgtyg14dwzx3VTa1DkkYVxDUQFMBCzOW22K_K9IjJS8CjuonWIZYBH252HHoA8NyHxVulbgiiRM3iaOYR52SATve1byv4rldwZNOiKM4cfygL6gD6nvYCcZJrO2jwyg1A6hpc1sCrv_j-5OfOjgg0_8EYcCi2otp3uBljl72e5QQgALSAskQ1im6NGT00gT0UpI0u0QNUW3QB0asYKiHAWpYPL9HYNeWAKyy0uBaVSSFxofymsKwiopaoT-fvZv2PbrVZNaPj6YNSkG6RZGuq7yu2gwY65GuE4bU58RnPWAGTH5X-L8NJ7fnbB78zsczSEwAOFTDoRt-32_vDtq88Oq4f1AXWbPW_bgAvtzmmZinCqppyhfgk3LhuN5qslKfHihlMaaQmJ7ElPRjwuCC4NCcGaP6w46DbtJq81lxe_XueHl_jMKIupS7iRtGfb4Nbgh2MXoc15eAm_QqVYutgV330ATGPnwLdK5fbZA-XzAz0dkkmBuA9M_zYqbqLdRJBEEYrkLk0Bd-EWrjt2h_OlrkUAIXw1dbPM8HvxXZWXLWeXfeAHQ00n7iJ4RJD2PMOkcOrjEOi_R9FxJdcUxCbIoXd71-YBvcUeyK49dcN7SyHcwTGYaxG9tC2yB1dwNxuP33XyaYP1Di3p6fnyKWpdCDbDn58dXpjJHcUu2mM6Vbw4lNl4YRvwHZ1KLPHMoWwy8MP031M8l57xA0R-e27Wa56ZRmWFZmGeryLZRQnZfdwPLWDjEvWy7QvAYzDECucWg_QLRWpICOpj3bsaesCyCw4nuYBEwjhzrLofbA2aEd1EVhD56qWcl0vje-wWnNb6aF6QeGoQk7KkDrqBkDUJoGbv1Dyh37au9exvo2EXEYM5JEXp_ig8ubNrKPuYe5eD6fL5qPQOFfzKE1ttLakLNCQ05x8A4Uh_ZKoGuYlkxmWudWw0p9aPjgrPG3-Z1xZqTA4sXz96_fvVm_PXl_fvzTD1bT_90AfYL__wcHXxYz)

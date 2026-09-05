[//]: # (ob:76e26c8c)
# Experimental TRACE evidence adapter

[//]: # (ob:5c8c28d6)
## Boundary

[//]: # (ob:0813cb3c)
This is an experimental, developer-facing integration reference. Proofpress
imports a pinned TRACE session JSON document as external decision-provenance
evidence. Two wire versions are accepted, each pinned to the upstream release
that carries it and to the SHA-256 of that release's `trace-v0.5.json`:

- `0.5.0`, release `v0.5.0` / commit `6260cfe7089815763667d8cc869673a40ca570e0`
  (`sha256:10459fb5e334889b17f9abae36de175490558f300077ba5273d2764f2cb58463`)
- `0.5.1`, release `v0.5.1` / commit `a97d4e81fb3b4ec5134e992882d28a6cf97fac04`
  (`sha256:ce7b5bf03b31ab669d12018b0d64fa2421d03b7e7ab2da156f98581e4d62c544`)

Any other `trace_version` is refused before event fields are projected. The
digests record which schema bytes each accepted version was reviewed against;
the adapter never fetches, hashes, or applies the schema at import time. TRACE
remains the producer of the run record; Proofpress remains the authority for
claim admission and governed context.

[//]: # (ob:d6858175)
## Import

[//]: # (ob:2e7206c4)
```sh
proofpress evidence import session.trace.json
```

[//]: # (ob:cfce713f)
The import appends one source event and one evidence receipt for each TRACE
event. Repeating the same session is idempotent. Reusing a session/event
identity with changed normalized content fails closed as an immutable source
conflict.

[//]: # (ob:b20ac71e)
## Data minimization

[//]: # (ob:081f8f23)
The adapter retains session/event identities, TRACE schema version, project
handle, timestamp, actor handle, decision disposition and revision links,
annotation/contribution metadata, and safe tool-call metadata such as server,
name, status, duration, host, and output hash.

[//]: # (ob:e1c0f001)
## Optional decision confidence

[//]: # (ob:e1c0f002)
TRACE v0.5 permits additive decision fields, and TRACE 0.5.1 types the
confidence measurement upstream. Proofpress continues to project only the
bounded fields below. When a `decision.confidence` object is present,
Proofpress imports only its interval (`lower`, `upper`, and optional `level`),
method name plus optional resample count, positive sample size, and named
SHA-256 evidence digests. The adapter rejects malformed bounds,
methods, sample sizes, or digests; it does not read the result files, rerun the
method, or infer a decision from the interval.

Accepting a wire version is not a promise to import every document valid under
it. This adapter applies its own bounded profile: a confidence object must
carry non-empty named evidence digests, even though TRACE 0.5.1 makes that
field optional.

[//]: # (ob:5af5e369)
It excludes tool inputs and outputs, raw prompts, transcripts, reasoning
summaries, state-change values, and learning-store recall data.

[//]: # (ob:eeca4c21)
## Admission boundary

[//]: # (ob:61d2b42e)
A TRACE decision disposition such as `accepted`, `revised`, or `rejected` is
an external workflow record. It is not a Proofpress claim state. TRACE import
creates no claim and no admission; an agent must explicitly propose a claim
from the imported evidence, which then independently passes deterministic
checks, configured policy, and human review.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2M2MDJhN2ExODRhNDAzOTZkMGRiMjA5OSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImQ2ZTlmY2Q2IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85YmFkMmYzZDkxNDVlNWZjNjFhODhhNjkiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzFmMGQ3MWIwMTAxOTdiYzBjOWZkNDViZiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWtuO20YS_ZWG8pJgJU2zeZefvImBzWKRGLax-xAZUl9HzFCkwiZnPB4Y2H_YP9wv2aomKXJsjeZmGFlATyPx0nU_VXVGNxNe1Znhsl5larKY7HYrGVHGY-4lAQ-on0aKKsFomk6mE1Gq65XKzrWt4Vm74SyMFoFJU55yFrAgDWXEEkNlxGPqCZ1Enm8YT_yYUs1krAIJn7w4SDUTqTJJRP0QzlWZleWlrq4nixv8Uq9qfg4Scl6jqCl8EDqHC__UVWYyLnJNKn2Z2awsyAaeL6trIq7J66osza7S1sI7Oy4v-LlGo25drsrfNZjbVHjgpq53dnF2dp7Vm0bMZbk9kxtdbLPivObFeeLTs1tvV_qPJoPPq8bqaiXLwuoCfFFXjf40nWw0RyeqSKdGqmjSXlnpS_cQOFevUsEVM75KvSDUoZGRx5OER-jdXVnVaNoqzwoNmvcRyVeeoSr2BPWol8ZCUpkaFYTCtOZ02q0k39kmB4MZ6inLStnJ4rebSSf-ZgJRLiuLn9rbWq0EuPy3iSyV_jB5Dxb02YBWlNKevXvz8sdXq5c_vXz97tWb-VZNpo9KGF7XVSaaGuK0EtxmFtNG52bFLfiv1u68pt6UFWp1kRV4pL22td7CnYJvMXytdlN40WLAJ4uiyXPQVW4gQrq1UeSlvIBn40izSCYSHofg1PoDWuKMIEpLlzAzcBl4hBdSE674rtYVPN3J5ko5pXaYXvoKrnxHHvJ6fb1DVTHckDqTT9NBpRDUYYnLhkGlv5ZNoTgk_DHJ35HRY0ck0MTzpfDloyUM9UKyLaafJbwz95LO_f_--z_wJySd48nf3_76C4G0aLaQUIQPSu14xW9ppKIkTLw4vKXRz07EPRbvHzpiL9Mxo5EMHnn6er22m2UxVAyBO0pjIFvre0PndcWlnv9uy2JZwFuDNpiKt1SRRuoYQO6Rqrzb7GVyQIVCWVIWmtiyqUAbV7CEF8pd3CsJRauzXX3E7VB2XMaevqXNT7zmBAAt22YfOVbiPRE49Pzx5DOJYf7TZaIzukoCG2ueFbaPxFnrCnRAndWZttMuPS2g9JaTyyPOCLkJte-Q9YmK_VwT_UHmjdKW1GWZk6zYNVgjGJmmxs9TUvErAim13eEXSJzCyup4lLSWPJDMu6XYS7XN2ioTD4OGgy8ciVPkKSYCpp8h9eVnUEigVe9Km6EfiW3khnBL1lxKDbFU6ylZuybtPn7uj_fTvi9NoPHjaStZad62BHen7y96ZQIvDETqq5BFLNU8ZLEwoRLYIsrandm1TtK1TgLpIS92ZVbUbhKonCTsG_03bBvvsefmmbwenTDuw6NDXId_You2palXBuKhq12VdZOAFd6CKi_inFJomDRMExXKFAxNIqXiIDSKB34ife0FgvMwYdr3vZR5nhDMQKvl0p1d89p19DZaC8-DxohXJoyyaEaTGYveMboI0oWf_oXSBaXwVudxeMrzPA5wmkKqDFdvvvYY4HKwbdQbbjeYjWnAmSdZFHJsW-6MUe_u0vPJvbeTEmptIpP62qe8lzJqx72U-_psd5piPg_CQIXG6P60UevtTnteT4We9AGsKni-LA5Z3TeDeXdkBSiIeFkDhsJjqpEAoqVx36umIO2g92JZjNQav9MOX1l9TUxZEZnzbAue7UEBge4cB_NCK9KhxvwAsnUOAl9HkdYppDTrHTSaBAZ3H2vy3Vna12EEW0UYctGfNer73Vlfs6V3gr3IM0Eo41iFYS941OX7kfIZDdy5WnOASxfDZeEen5M3egcACH5wkbEw_O6zJLPYA0Fe3T3ZWHyO3-6Ty6JrlNfkCvYZ0g7IihRlteV59rEPIuhmeJZbiHcJ6IxZx0HGdtu0INpasSzgYQPweCzkgMtJFAFOATD33hpNIUPIHzhVdMdCxcY09URqYjYqtX7QGAXhqYNDi3VT0q2DywJ8pXINLTzbws7Jt7spcfsS6W8c7HoY4_0mCk3hwk6XUKnQlpyRZ-jvfgMiW9BRgR-m7jXLjXZjxUzyPN_f3DdSWJBASzgO16ApQaRvwAzVVO7oKdmUtp6OhhGCzjsSqwD6CmcqloGiezQchqR-eH3G0IN3NIcag3AuC9tst7xyvkfl9azNR3LJ8wYv4om55hU-PcMd3lUI-gL9cAxnZBIGVBrDuOoNGQ1VQ9I9dEbqzuWQxCKBY5Xal_5obOpnpmdMQZBO8A0TDr5CVWOu7BGfXJXVhcnLqw615wRiAZUPyQSVPgLwFqadT_s-0GIRlKybofCdHswLrP8B019gqcPkAsWxbSzGegclntX5NQYU7ICSal9dFgYi7LCoPR2QooeyKbnaZGAp3ATggE6FEAhn4im42lvwDhiF9W7rTIJeOEpBzBFSsvOmgrPa0atNg02z5QVpB80vAv_-E8boAIuhVVbvOQxn06JjMhwvgs3wjruf8R9f3P0DEnQ4GrmeRQX28kohK_SnYUqc2waipCkuivKqeCBV8kDWYFuqzGRO_p0LjSepofT2QvPrDm2BrN7XiYu9S597Vpt7Xj2y5HSasK-iyX5oC8kOcxlBUEHKZZd6OApckys7J__CSuBk3d04sO64orozBF96u1ttXvejWqtO3-_qspvfXA04Lee0726VBlzFSobSauna-V0B-8z6TujP0LVc_bSiy889OBs86OCrcL6wgGs4a90VksOy3tYOsVCOQ2mwZo83rXedHT1QAZoVs2Fs7YF93vq4D_rN5Gpz3Xpv5Lz9JDbyYuc556p-DB_rcsjkbmhAm3HQgrZIzqEJutltND33SqJDHr7t-sZ4sGLEzEuVD1sh84ynAxntPTZeY8cr3Hi1vTmV_J-g5B_OY3y-x7PpEIWF9-nwyn4ff_FVSAoT0CiNfS6FFDFM5TKJUs2SJBKUpRFsNCYMTSCkDHQoZZj6fhp6CUu58hmVWj7EuBFhkc4oe8e8hccWITtAWGghpInBZyfC4n7CQgSe4NQk3IhHEha7rMCdf6gHbC7PpixG-xrMtZ0MwOBmZ2uAw23fuGBFb2WuyVnf02S5hXok64hFMPrrmCZp4oVx5EdRrBKJaRlBmsJewMOYarpeFt-vu39RejQIUyNg0_GDJEmFF5uUCw6Lj9JeHAYpDcPE-JTSOBZYlr5icRQYJkWYBJEPZ-HOvnYkwsyphkzC-ocTDXOiYU40zImGeQwNk_qCQvtOWOTFe_ZiGKeGWD1-Jup5DOkxBfWuk4HHGI1Jt_4r_rRZp5gPqgA4lgKD5zAdqh9iPSUHukpZ5NcExcB4AU4Fw75f5-WVrpAjaaB88QP4Ec7rLV_nkED5-ocpxmVTQg1hOe7yxg47CciANIF6kdATQXKbFJeudOHyEnaTj7oNEL6tyNu_vZxBVxgAoV2R7O0G1dI0lkDJAlDge24jwMRqdUFaqxWMAqwjd7qTXoCZ0CF1y91AZ1NtJ9C2yaHos1w7pgw7A1zvD3QnZIUB4XwUgT0J03ntxPCdGL4Tw3di-J74Y6hXHwBoMxzdIR8P0yLHmIBn_P7oLlrhMDc2Uv5Obuwf-LPAMTs23kpc3Y1s7a2cDQgPUOs2k7usuVPwjznHHyI62orXe3g-b2cCLGmFjasE8TPIDzckOoKpawmiKjko0-0K9S2q6BCN5Qw9wAIeMHMveLAPJknXd_cecJ24B8wegAA-an4BSuFcjPtWpff6YScAgHsckXXkp44Hiaz9an8_kfX_k9kPJ_f2LMnAjbBPh6mPb0L8BAmNDIM5VaQUBn5YjIXgsE-wQAWCpZR7YRpESRrDvSCEFipCFgQ0oBwECOHfbdIBuoclC3ro9yn7n9J-Y7pHycSXidBhGHnH6J6H5dy3InxCwRREJ438mN9N-Lzb4B77BXJMv8SsMaYNaDkaVGDVPVFGJ8roRBmdKKMTZXSijE6U0YkyOlFGJ8ro21BG7z_9DxhT-Uk)

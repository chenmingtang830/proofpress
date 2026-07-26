[//]: # (ob:c350cb3a)
<!-- Append to AGENTS.md — the Proofpress contract for Codex agents. -->

[//]: # (ob:51ac24b5)
## Proofpress: ledger Markdown and static HTML knowledge artifacts

[//]: # (ob:10265f5d)
For accepted, meaningful revisions to Markdown or static HTML knowledge
artifacts—never source code—close this loop. Do not snapshot every
conversational turn.

[//]: # (ob:af9efd22)
Before editing an existing target, run
`python3 proofpress.py capture --recorder codex-preflight <file>`. This
preserves any human drift as a separate version without guessing its author or
reason. Then:

[//]: # (ob:d181cc6e)
1. Read `python3 proofpress.py policy <file>`. If the user asks for portability,
   run `policy <file> portable` once; it remains sticky. Use `ingest <file>` for
   Git history not yet represented in the ledger.
2. Preserve carrier-native block anchors while editing: Markdown uses invisible
   `ob` markers; static HTML uses `data-proofpress-id`. Then run `anchor <file>`
   and inspect inherited/new/gone IDs.
3. Write claims JSON with one honest item per touched or removed block. Do not
   enumerate untouched blocks.
4. Snapshot with `--why`, claims, and explicit actors:

   [//]: # (ob:08f435e4)
   ```sh
   python3 proofpress.py snapshot <file> --kind agent --author codex \
     --produced-by codex --recorded-by codex \
     --attribution-basis harness_attested --note "<changelog>" \
     --claims <claims.json> --why "<actual reason>" \
     --rejected "<consequential dead branch — reason>"
   ```

   [//]: # (ob:b521eb3e)
   Omit `--rejected` unless the dead branch matters later. Never infer it from
   casual discussion or capture raw prompts/transcripts.

   [//]: # (ob:cd72eb83)
5. Run `verify <file>` and report its output verbatim. Never re-snapshot just to
   force green.

[//]: # (ob:bc88257e)
For an incoming file with a `proofpress:discovery` marker but no local CLI,
tell the user it carries verifiable revision history, show the marker's
canonical project URL, and ask whether to install `proofpress`. Never
download or execute it without explicit consent. If the CLI is available, run
`inspect` before trusting the capsule and then `import`.

[//]: # (ob:4d83fd2a)
For parallel portable copies of the same artifact, keep every original and run
`merge-plan TARGET --from COPY...`. Apply compatible block changes, ask the
user only about reported semantic conflicts, then `anchor` the resolved target,
write merge-relative claims, run `merge TARGET --from COPY...` with explicit
actors/reason, and `verify`. Use `merge-lineage`, not `merge`, when artifact IDs
or portable lineages differ.

[//]: # (ob:08efea88)
Fallback `capture` records only `recorded_by`; it cannot know authorship or
reasoning.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzcwM2MzZmE5MjZhYmI1MTJlNzE5OTMzMiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImYyN2Y4ODQ5IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9kNDQ2ZmNmNzJhZjFlZGNmMDNmOGY5ZmEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhkZTU1ZDI2NDlmMjAzZTgyZjQxNzAwMyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXNmOG8cV_ZUK_ZAEITnd1TstGHBkW3Zgy4YtJwhMgayVbE2zm-5FI0YQkLf8QOBPyIflIUD-IvdWL-yZ4VDjGXIkO3zRkL1Unbr7uRfU6wHLy1gzUc5iOZgM1utZYDnC0SyiPuPcs6kK7ChyHDoYDngmNzMZL1RRwrPFklHPn0jqBIGKKONUWtyylRdyy-eUSStgOvACSQMlPS4CakdawqqhRb0gciOfKq08WFfGhcheqnwzmLzGL-WsZAvYIWElbjWED1wlcOHPKo91zHiiSK5exkWcpWQJz2f5hvAN-SbPMr3OVVHAO2smztlC4aEuXc6zFwqOW-W44LIs18Xk7GwRl8uKj0W2OhNLla7idFGydBE61tmlt3P1YxXD51lVqHwmsrRQKciizCv1ZjhYKoZC1DTQYehGg_rKTL00D4Fw1Uy6rq-FDijTtpJCW44OdaQZIsvyEo82S-JUAfJWI8kslMrzJPXdSFPLUSHVrh1YllMfp0E3E2xdVAkcmCJOkeWyGEx-eD1otn89AC1neYGf6ttKzjiI_IeByKR6NXgOJ2itAdV7HidJcWbunX385NOnz74bFWkMhyjHKzkY_izLYWWZx7wqQWEzzoq4QNmzPEXccA-0rMySVbnMckR4Hqe4arGBOyu4k7IVqrJGOhwU8CKsNZikVZIAbrEEban6vDzJxDk-63iW4A6KFhRVqld4qt_956d__PdfP_0eLjZbMCnN3mu0KHUBVx79ZjQiH8NBU0nKjNRnhzOTf__9n6Rcqp6dEVw5ByEQneXkcYOu3KyN3bGcDd4Mt4g8mwnqcu8Sou1iE5IouVA5-Yrl5zK7SAkDBEXJyliQz_ch_uADcttlnn31JTlPswvzDAEdbvGisYLhX4JsW9T3tCcPDvkzkBcTQq1B80OyUiyFrXWVdI5doOy7ZeHp7Qn2iJjpSGlJ6cHx_lGBhhVRMi4BKLxG1CuIPPi5ZPlClUOSV-k0na83YMOpQ7aeOV7vASzt0BbCVwcHbI_Jt6BQshPQhqyzJBYb8kjHifpoPiZfaGPaGNcI2-JN4IyX8PrC0qHt8IPjJQQFCHD7wEgbFOckS4X6kMQlGMiKxWAeIHxxvhmT7wu1R74WZxAp3cMbBB2DzykQ10tFBMvzWOWjFF6Dr2ZvWEhAMCvIxRJO0hrOxGy0R74Wj3xl20eR7zzjc7KCF1VefHgpIoDaCzKXrGSjrZmMYgmG8Qzy4b6Y5nEe2IF7cLzOmPwlj0sQbsLiVUH-9N3XT8kF5GmwBEXAoiFpgDmoFVnD8mVWQeKWGCdykzBukq_DHWHbnn8M-aq0WqkcihZSpS0gs28x3iNBB7Rtu1Z4cETumHyXQlGwzMpacPPR6GK5mQ8bkQ7NSurVGhwO_KouDyb7bDPUruMp9yi2OZ8Xy2kKn3bHq6I9SRMYRiNcjWCF1wHG6uASYO5RW3FHHQPw1yuQGUg0V1hPKjkHpSdYEmAYlRh5eY4hABwOChyIA1jN5mPydI8pCBlQxUPn4Hg9SAYYXF9iAd1FffN6rjDGgicVJKvKdVUSeIjDkivACrVjvs-ZvFD5AYuOIV9It0KRRa5Uus97uAhDoBPqOAVKSuIUSAFmeRRZ7UYMktR2g468tKGV8GoPXleGDhQo7Ch4cbckUUmXNqE-XccQ2rM6uxdQRZO2bh-Sc6XW5LKKr-fPEEgaCw8fnT4DpBw4GpkDcSmrHFJ8w1ogwCcbMu-RlLlJ_IKlKQQAqF6v4n0-bFnOAE6D1eNM5IrVpMLcaUkKMDAJAcETnuv7UgAJZcJVzGOYcGF1s2YrvIaIEQjk4nydxWlpeGVudkLm0X5D4vEcGRyWLr0V-qyut4jhi3ckfEWmy5kGg1T5Oo8bXllwexIyZXs04n7kBG7gaVvygEdSe1QzLwj9SAA5pzqigQME1PUVtWBNzSMtpLAFKhjVZvhhra2JHQK1wisDCjRgZAUj6j-zgonrTGj0B8uaWBa81Ugca1ntU6EUBwPaXn19NFJZp1bD-ZasWGKYozLktrI810ZkZo0eDWys9378DlMOaHwMGeijHX7TIGFMh04Ugd6oapH06F-D5D68zYip2M3eGhCRLR2lQ88XXLcgeoSuAXEfJtbDNE07UCDHFMMKKbIKgziqG66JJCsUCDiGXJhl6zH5JCPo0F1qx3c2Uwi4KVoPw24BSwjEhp0ZoDmkplRYtnIiJbpD9lhgc8h70bcNaUIUwXRvolJuDvUKqmWlk3ixLLdM6hkccJquG25QwF4bsqxWsKWE5At1FlwihcJzQKXY-InJLJB_yaLC1gbAwoRc90NA5NMUwlmRpXU5PrlZGpa0uKs5p8oRrTR6FLORxn24YXFeGGeoo1ecxOVmuKNEaPFQ4YaBsB1HdtrpUcgGz324H5ljMCw6BSA4U0c-gefb5iCa2Ubh-0YvkMckZHZzqtrp9hiYom7ouxSCiiXbI_RYZXOE-9BB41eGgsUpulydOW6QKFUu49qm0nPDLZyONG4leme2V-uixttK1UgU4xFIfw31LvxdKqRn8ixVF2cL5GRffFLsEaOkUrmhpaXDO8vskccG931YH1RhDd9qQ8vNUmSBtrnwQqAzXXzuUcOtFH8ep2vzECSsQEESpZJ3q29pXrP6wfhZJ2GopyyuHMtnnWVsKVvPMu7MtdISvjRRyQRAMp2ahQhch0VkJZQc8U1zswuXvWu9F3pd4ZHpCpOrPWF4CIsyMh08qlu8Sbb4aDroL9IYyqP67_gFRElEDILEt0BoFcNUhtHzypstczOrYyv_xwoOGMPjffqGRUH3unkXxLeDczZKcEMZUce3tBCde_Zo6FYJd-aPJrPGqcZ_oS7Js5VBJViBJ0U6UpnmOHpFm7dydoE6Xq3L4gzqmbQQeQyf95hw5FkRiyCpesY961JqS0-bc9yHV8ITo87SXlTg12V2s3F7KnBcrUPhGgetXWpLP7dyfQtvbIO64wlLMh8CgNOpaUsl-6XRHTlgCQEI6hwBOnn85RfDKeScJNnmUcNnME0U5OXNU60hAelcmLfqhX8LpQXwoCyNceFmmEW-__bLOlhAdoYEo-B5DI4YrEugWX2s80b60xSzTpIxEz3VKyUq8LO47AqRLu40U66uDIDTEHBV9pLFCYJuK6cmM8wJr2stIDlNgbXElGiGUwZkiTlmHq_QPuZ7dMS4HQknlBZopdVRjz73dHRX3ruBs8eLGKtMY7LmHBDuF2q0TkDxzz7-9smnzyBUoJeRx19_89fxeAwSBPKQYDxbrcGecbs6xTdTqKFRA-w7TY2qDZ1lHIVaOwWEnAIKmRQTMkgXCkgomoeNXOq8Oze4QWFZglmtqVGn6YVJjjXEXCV1gdGmC5O3zb0bkNe222oWKnaTUs7q8FZbUOPK86a2qndqCCpkJiyk6ovw5QIBt2LF9D9Nu8JwS58LiEla7y2xIld4nhNxzRnfZq6u8dBq-h4dg4umli6W8bpXT4N5XoP1_A0i2zE1xZrt6szUTGBN1rt6ffeMtR4hm9zW3MhjMJtc4rj5wUewhUr0jBVgpDfMX03Kv9v49UCDrVUG1hMbdDePTA4y4rnFTgcadtxipwN1gm-x086B3naFpq5-mFHdjtHXW5EcY6i1c0j0ViR3HP_s6qG_da99VQ4EmToj3OSP142j6Xw-hoyWKMxPmH1gw9G64qBjqD0rLEW78qQp8Ficw7NoUg29NfH0Bt98wF17fvqAu_Z89gF37fnvNZM5olo7V324TXte-YCbbt3zyJs-7wWA1wPgrybh3mXpLilc3gPb8rcek1AegS1TH_yXg7KlkJFHuWkq1sfuzz_6vf_-TOT1qTI4VQanyuB9qgxuPw3tpoGdqUzcYbfrxH2ze_T3tjnoezfsvPl4V0eftjOxggm1d4w-NeUqtD12Gn2eRp-n0ec7GX0GjEcBE5AaLfpwo0_Te39_hpfX5lzc0p6l3YB64YMNL-spybsdP14VhOP72rd9LrWjHmr8aFDfKvdfm3acBoinAeIve4AY6kAGnDJXMv1wA0Rzkt0l8FVrP40ATyPA0wjwNAI8jQB_pSPA_a2SI_1-a2cjcD-SY_3SadfvivYjOUxBeff509MsX7Ek_hscj8kXTGC5eLmZ3RAKQ8PAuXJMfcCVPq84SCMFcnqLCdS1Bv4xtr0-gnqQbXtKP_q2uwYW6UEW_1mTij0_qd85qehade_9pOIUwN5ZALv9NGxHH9nu9ZGdN7vbxL_gNvnV4-1ok9t04gY72-TNf41xapOf2uSnNvm7aJNTS1EmHclCzv7P2uTT9FfT6J6mD9uqnqanZvOp2XxqNp-azadm86nZfGo2H7bZ_PzN_wAVjFr1)

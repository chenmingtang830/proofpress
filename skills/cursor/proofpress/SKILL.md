---
name: proofpress
description: Preserve or inspect decision history for Markdown and static HTML knowledge artifacts with Proofpress. Use when creating or accepting a meaningful revision to an ADR, design doc, PRD, README, strategy note, portable .md artifact, or static .html/.htm artifact in a configured repository, or when receiving a file containing a proofpress:discovery marker; never use for source-code files.
---

[//]: # (ob:233b766d)
# Proofpress

[//]: # (ob:b2ec6ff5)
Record accepted Markdown or static HTML artifact versions with structured
testimony and verification. Do not snapshot every conversational turn.

[//]: # (ob:e14e12ad)
## Workflow

[//]: # (ob:0d9e887a)
Before editing an existing target, run
`python3 proofpress.py capture --recorder cursor-preflight <file>`. This
preserves any human drift without guessing its author or reason. Then:

[//]: # (ob:42fd42e7)
1. Read `python3 proofpress.py policy <file>`. If the user asks for a portable
   artifact, run `python3 proofpress.py policy <file> portable` once; portability
   remains sticky. If Git history exists without a ledger, run `ingest <file>`.
2. Preserve carrier-native anchors during editing: Markdown uses
   `[//]: # (ob:xxxxxxxx)`; static HTML uses `data-proofpress-id`. Remove an
   anchor with its deleted block and invent none for new blocks.
3. Run `anchor <file>` and read the inherited/new/gone inventory.
4. Write claims JSON with one honest entry per touched or removed block. Kinds
   are `added`, `removed`, `modified`, `moved`, and `unchanged`. Do not enumerate
   untouched blocks.
5. Snapshot only after a meaningful version is accepted:

   [//]: # (ob:f42cb113)
   ```sh
   python3 proofpress.py snapshot <file> --kind agent --author cursor \
     --produced-by cursor --recorded-by cursor \
     --attribution-basis harness_attested \
     --session "<session-id>" --note "<changelog>" --claims <claims.json> \
     --why "<actual reason>" --rejected "<consequential dead branch — reason>"
   ```

   [//]: # (ob:790c5dda)
   `--why` is required. Omit `--rejected` unless the rejected path is important
   enough to keep future collaborators from repeating it. Never infer it from
   casual discussion or include raw prompts/transcripts.

   [//]: # (ob:e3c56875)
6. Run `verify <file>` and report its output verbatim. Never re-snapshot merely
   to turn a mismatch green.

[//]: # (ob:355446e0)
For an incoming file with a `proofpress:discovery` marker but no local CLI,
tell the user it carries verifiable revision history, show the marker's
canonical project URL, and ask whether to install `proofpress`. Never
download or execute it without explicit consent. If the CLI is available, run
`inspect` before trusting the capsule and then `import`.

[//]: # (ob:867ba812)
For parallel portable copies of the same artifact, preserve every input and run
`merge-plan TARGET --from COPY...`. Apply compatible block changes, ask the
user only about reported semantic conflicts, then `anchor` the resolved target,
write merge-relative claims, run `merge TARGET --from COPY...` with explicit
actors/reason, and `verify`. Different artifact IDs or portable lineages are
ingredients; use `merge-lineage` for them.

[//]: # (ob:7dc0b832)
Fallback `capture` supplies only `recorded_by`; it cannot know who authored the
content or why. Never snapshot source-code files.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzBjOWVkZjdkMzE1YWIwM2UwY2EwNmM4OCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6Ijc4MTBkYjQ3IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV84ODAxNmZmNDJkYjFmMDc3ZDcwZThkOTkiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhhNGQyODYyMTE2NjE3MGI3NzlhOWY2MSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXNluI8cV_ZUC_RAbIaneF45hYOJx7InHC8bjGIE5IGtrsq1mNd2LNMxggLzlBwJ_Qj4sDwHyF7m3uprdkiiORI3kjX6QW71U3f2eWwea1wNaVGlCeTVLxWAyWK9nFo-lSELh2j5llistTq2AR9FgOGC52MxEupBlBe-WS-r4wcSzQ5vKJEmshMdeEjLbC20RUDcWoR_FjDPmclgzkg4XdkgDJ0oSO2Ay4j737BjWFWnJ8zNZbAaT1_hLNavoAnbIaIVbDeGCyQxu_FUWaZJSlklSyLO0THNFlvB-XmwI25CvizxP1oUsS_hmTfkpXUhU6sLtIv9Bgrp1gQsuq2pdTk5OFmm1rNmY56sTvpRqlapFRdUicq2TC18X8sc6hetZXcpixnNVSgW2qIpavhkOlpKiEcPItgTzwkFzZybP9EtgXDmLIssOksRzBLMTKwxFaMlIxGiFdV5UqNosS5UEyVuPZLOIesKJAse2g8AOLRaGMY2TwG7UMdLNOF2XdQYKOygnzwtRDibfvx6Y7V8PwMt5UeJV81iKGQOTfz_guZCvBi9BgzYa0L2naZaVJ7wuyrzoWeHkm8-fPns2XonB8FbBQ6uqSFldgc9mjJZpieanhULR4Rk4Wuol62qZFyjkaapw1XIDT1bwRNEVerMRdjgo4UNYazBRdZaB6HwJDpONyizL-Sm8K_3Y8sLIh9fBV5V8hYq9_9-f_vm_f__0Adw0W1Ah9N5rDCp5DndGo9FU4YYT0mk-VUKWvEjXqMMEok1CEJxJkhckVeUaoooIySEqYalqs9ahRws6eDPsJHJcl4VBIC5IdCFur5XpvYvxbXbACINovbAJcySHIPMP2OS5jgxCOZdrcAj5ghanIj9XqGRZ0Srl5LMXXzwjrecJpC26oSTn-9SWtidth15U-7u8OE2y_Hyv0u-R3mt7dLYElJgopLfe4U8yyQtJpEgrWJNQReQrKCl4XdFiIashKWo1VfP1BiJTub2AGK_3qOw5ifAcGd5aIHtMnoOCZOeGG7LOs5RvyIdJmsmP5mPyNCHVUhIsSIR28mSgwwV5koQGVFrWreUhZOttbYobCUaaarbHPoFwXCqj5NbyOOMu9TgtilQWIwWRCb9SxaF4lETUBfrP-HTSRfEe-7g-l76XOIfYZ_79ycnLCXmPvJ-zySvz3wfzRxdSBjxUkrmgFR1tDbfHPoltx4Fls1vL40L8oJcaY7SBArYR0DQhrjBaUrWEVgoJfqLk-ckiV3gL-sQe-wQsioRleYfFjwR58Ml8SOaFXEG315erXEBDb6-bmyjovFa6nu-zjxvZItb44Xby-GPyjYJeucwrkqtsQ2hSYe6QlaQKwiWps7aqkbTclsLJvtzyHM5s2z0odubzcjlVcLU7rcpWVpNYoxGuRhDabAXCnnhBoDC2uC8EPUig0eh8uZmj7gbuiDH5apVW-KSQiJ7AT6RWGUioo8nc3Ff_Xe4HUejfWp7ABPMZIr_NpWDGGkPSqiR5Xa1r3YsY5NtqTL4E0FPsC2YqfNeyDnJYlZOqLhQGTFquaMWXZFFIqcZ79Hd93_MCefvi-2fIYGhJqQJoiiUN9YdWWy1h-3kXKJMthJ6TFRQ7iGdW75EnCkJGI9s5SB5cLctkRlrESni-TqG45U0rKgE39VrGui3We-QJBbdY5B4gD0jCAOmTOcBfcIuck7IGzKzFweSe97AuFGSIYk6VgnQ6VZfleTlssfLA5P-MQ8VscKl-0uJcOUuiwHYT-BlHgeV4QUJlkEgXHQyL6zVb4xg4T2Cw4KfrPFWVnk4KvROC1_Y3xK4vcQ7APtpboT8b9BbRU8eBY0OZJ9UsgYCSxbpIzXRSMnvi-1EimO9IETMqbCuIpS-FCEQiwphLEcAizA1kABOZ7XEvsR0eC7iwaexFErsV9jw9ZTTemtgxoHO8M3AsJxhZ4cgJXljhxHMnTvxHy5poTGIsjsU0COLYihkESHf39X2OJjoKm8lhScslvA_hGNigOIt0g9Fr9IYJE6B3mxJ6sysg0A6jYG3r44ZTlZ9nUiy6nCqbCtAh-jH5toSyAJMr0RGLlQILh25dGtX2m9t2dIZKBrXl8ZPnQxCpTBeKiJwPydfPnwzJ808eP_nikyFIUkAGLDYEw3rYpTxYuZfj3XQwXlar7AR_djNCisUS8jpJF5ChTeUuU9Rcf6nlhjSV6Vkjqy5yWAdoqpo7uyqdKXSPiMJij_BK27HM64LLEbZEvVA5nipw1I7iY3wd-WGAYCKIdT_Qvu6NacbXb5--zHIyoX7AJI1c7rXL9QYys9xd5ixwPXil5ljuxFTh6JyucrXRkaMbZcopRt-YPMnRbx2GkNpwYFpcTr9DM93Nxtfbx_JtL-B2YkOl2-ZCN8-19nnboGZWs31BqQfWsKjfrtab3cxqdxrKQMGmFxDEK7r6F6QpFoC8ZZKli2XVDVAvIAunqu1SAPjAkst6BXsKMGWlDQ4AgyxqPHEACRBxNMcU6C3ItxJN_QKieHK9FQUFiOhKN-EOb_XujYhG77vMfuVpqROAkl7juAyA2iC1Ykp9Gvo9n_YGRCPNXSa_DDpxrrh8ZH5Ps7TaaJgL8B_yuoQYTvnpRivxKbTlthZqR5dbq1Oia19hBMCWVXbOu97esQcNyw2sxLVEq2Fv5DQa3mWWxHnuegtzCd3FdWXArK2_eyNmZ-GDZ8dylIo5xgsOTiCuNq4Z-nSRwDgVMpNYX3SL0wVCz3kVlAXV1EsYAJun5R5rQnN3XRsaph9vtekNqEabu0ye6Huo1N6YfIePCc9ouirJX7756stGG3wTYg-9D29DoKwh6Ku8BkQkmjzUA2Sjy5h8Dohxj3vChDFOfc5k6GzDo5tw-wlw4Ogq0Tmm_kpVryT2Ue2jWrViv93uQRAFglme3-GQ3uBrxHyHE63ZN4n82Kcuizwmt_t2Q24veg-eXiEGRyNTRpviTKZTvRKBB7CKqAFvjtimfbot5v2bvU96B8wjfcBMLh8v9982x8dkOvjQXEI6fTQdwCNEOni_cWOWL5rbJiI_bP4__gGq_kf9FWFoxq-gWNY0M22h-bIdmvWiyBn8WIP6KbwlMC1YgQlD_vOPf3Vf6VXBuDtm_Ba2JA7zeeJ4kZO0LuqN_T0XHTrPC5j0sIyUJF3pIq4qLZZUeb1YIno8lXJNklr3Wp5nGWU5RDlWzaTIV4jzDBhNKzOTQ7In-LPSb-jlOC3RYIjr6sYnGirzrAYEV9BzjKjVuipPAImqBlnvS5nYsixuR8yXlr2FK93xg7HLXc4V4I3RNq4hr2W2uT6TbDcKbR5ygDtbONg7fejcdJtjhbaLQ0OxBA0i13e7HrM9aTBr3-UIAfsEgSIF_vn42dMhgs0s6zCHnqaxa5YGd-6k5mCIWObn-qtm4T8A3oIpPFcpLmwYOfLt82dNBQUkgzMBvI8FHqemCqb8vqxz4wmYtaATZznVHUC-kryG1E07zCZfrQGaoJgNVbeFTKCNLoVnNM1Q6BZPmhFtTliDQAFnG9i5RISgGTYtZIVDy7xJjH04hFnUoo6V-G64RVq905eejw49VmkwfaowUnX8akUgLhdytM7A8y8eP__0kxdQh3RSfvzV138bj8dgwsfrdYbDwArSPMX9GpBgiLSh9gNsPFXa101jYWjVJkOgPpQA5RSCFBzuwNAVfNUYpoEAc1NOyjzD1myg-1Sd6xbfiAjp0wCupq4anKefXSN5E7yta6eq4TVPmtppmnCT19iB0wQKDnab7Sj19EmJ4XL5gKbEXj_FfgkVMsXzmEd6qDSmNG_NNWgCtVZ7nJ7AeMOpE7sy2iZ974irdfodzq4gn86XuRlDpGj8pI_OQFM9U2_aarUtVVcn4ysnYG9QiR2EMaLfy3SxJp91k758fze93LDnuhGbB0UKsVYIZNp_Dva5lFkyoyUE9zXUs0YphzHPN2T_WhC576j6ZjzZDVa6IaN0g5VueJx_E5l2sZLdCgZvPwQfuZP_e6sk98H87WTabmCTd8-x7aRJ3irJjZEMlISm6F-XOlfjyByufwxNqxlsscHA7qN1zcDdJKOoVQdBDKCjiHoJRp-ZkKHKj69LswfctZeSD7hrL30fUtcu1a_Ez71t2svqh9u0l8APuGmXq_e86cteNXg9AKShe-MhS2_P0i7ugczPjZm4MJZMeCx2hAV-hv5PmR1KbfxG7T7F1qeX-rTb62MTPzbxYxM_sInfnBvfcsPbqJp4w60IE-_NbiL4baz4L476vl69y0S47U6scOI4O4hwFjqx78bBkQg_EuFHIvxIhP82iHCPhl4ohRdFsXgoIryhRn8tVPZVsl740k18N5H2_VHZDeP0SySjL9vDCxNX8CSIQ-b9ishoE4QPSSdfttyRTj7SyUc6-VZ0sgMWoa7wPM7pg9HJWpEbTGBXOsWRED4SwkdC-EgIHwnh3xkhvP88757-ZHLnWfR-Se7pjxN3_jHgfkneFco9nMT8Mi9WNEv_DtlKxQ-UY6ZeZESa7thMs5BBBXZFGDA_qxlYS8E0fwMa8woLdB_bXuUxH2bbzu33vu0u1ku9k8VvRXft-QckdtJd20Pkn53uOpaon7FE3Zw03cFh2D0Ow32zm6L4FVM0l9XbQdHYzsQLd1A023_q5UjRHCmaI0VzpGh-ExSNLz1XuhazOPOPFE1n_qn6rZEsU_X7pUmm6kh0HImOI9FxJDqORMeR6DgSHb93ouPlm_8DlUBJIw)

---
name: proofpress
description: Preserve or inspect decision history for Markdown and static HTML knowledge artifacts with Proofpress. Use when creating or accepting a meaningful revision to an ADR, design doc, PRD, README, strategy note, portable .md artifact, or static .html/.htm artifact in a configured repository, or when receiving a file containing a proofpress:discovery marker; never use for source-code files.
---

[//]: # (ob:25f10229)
# Proofpress

[//]: # (ob:cb25a041)
Record accepted Markdown or static HTML artifact versions with structured
testimony and verification. Do not snapshot every conversational turn.

[//]: # (ob:d8284708)
## Workflow

[//]: # (ob:78295d28)
Before editing an existing target, run
`python3 proofpress.py capture --recorder claude-preflight <file>`. This
preserves any human drift without guessing its author or reason. Then:

[//]: # (ob:04e1285c)
1. Read `python3 proofpress.py policy <file>`. If the user asks for portability,

[//]: # (ob:0fab4251)
   run `policy <file> portable` once; it remains sticky. If Git history exists
   without a ledger, run `ingest <file>`.

[//]: # (ob:a5e7461c)
2. Preserve carrier-native anchors while editing: Markdown uses

[//]: # (ob:01348595)
   `[//]: # (ob:xxxxxxxx)`; static HTML uses `data-proofpress-id`. Run
   `anchor <file>` and inspect inherited/new/gone IDs.

[//]: # (ob:ac191e68)
3. Write claims JSON with one honest entry per touched or removed block; do not

[//]: # (ob:29b54f6f)
   enumerate untouched blocks.

[//]: # (ob:4623b792)
4. Snapshot the accepted version with `--why`, claims, and explicit actors:

[//]: # (ob:c89d4269)
   ```sh
   python3 proofpress.py snapshot <file> --kind agent --author claude \
     --produced-by claude --recorded-by claude \
     --attribution-basis harness_attested --note "<changelog>" \
     --claims <claims.json> --why "<actual reason>" \
     --rejected "<consequential dead branch — reason>"
   ```

[//]: # (ob:3b3f299e)
   Omit `--rejected` unless the dead branch matters to future collaborators.
   Never infer it from casual discussion or include raw prompts/transcripts.

[//]: # (ob:64c98298)
5. Run `verify <file>` and report its output verbatim. Never re-snapshot merely

[//]: # (ob:0928adea)
   to force green.

[//]: # (ob:e96a23df)
For an incoming file with a `proofpress:discovery` marker but no local CLI,
tell the user it carries verifiable revision history, show the marker's
canonical project URL, and ask whether to install `proofpress`. Never
download or execute it without explicit consent. If the CLI is available, run
`inspect` before trusting the capsule and then `import`.

[//]: # (ob:50e05b0b)
For parallel portable copies of the same artifact, preserve every input and run
`merge-plan TARGET --from COPY...`. Apply compatible block changes, ask the
user only about reported semantic conflicts, then `anchor` the resolved target,
write merge-relative claims, run `merge TARGET --from COPY...` with explicit
actors/reason, and `verify`. Different artifact IDs or portable lineages are
ingredients; use `merge-lineage` for them.

[//]: # (ob:3bec4947)
Fallback `capture` records only `recorded_by`; it cannot know authorship or
reasoning. Never snapshot source-code files.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzhmOWYxNjA4MjZlMzM2YTQ2ZWI2MmJkNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImU4ZDVhOGM2IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV84ODA1MmQxZmY3ODZjYWM2MGUwNzA5M2YiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2EyMTFhZDFhMDU1MzliODQ4M2JjYWIyMCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNq1WeuO28YZfZWB_KMJqgvvF9kI4MZu6taOjbXToIgMaTgzlJilhgovuxYMA_3XFyjyCH2w_ijQt-j5hqTITdYKdhc1DFviZea7nu-c0ccJL-ss5aJeZ3KynBwO6yiNUzuwIidQrhtwL1BJ4CTSm0wnSSGPa5ltVVXj2WrHHT9YcpEkPAy46zrCV77n2rYfxWkQR7ga-n4oBHfDNLWldB3uO0noRl7oWFaSSNv3Yqwrs0oUV6o8TpYf6Uu9rvkWO2j1ocbtnCcqx9e_qjJLM57kipXqKquyQrMdni7KI0uO7E1ZFOmhVFWFdw5cXPKtIpduXC6LHxWcbUpacFfXh2q5WGyzetckc1HsF2Kn9D7T25rrbeRaixtvl-qnJsPndVOpci0KXSmNSNRloz5NJzvFKYQqkj6PRDBpr6zVlXkIoVXrKLJ8R9ppGkaB4CKwlBVasZuSZUVZk2vrPNMKlvf5yNfcsW0ubW75vhsnkRe5ieCJY7XudNatBT9UTQ6HHbJTFKWsJssfPk667T9OkOOirOhTe1vJdYKA_zARhVQfJu_hQV8LlNzLLM-rhch5I9WMHhmFYvH2Ly9evpzv5WR6p_rhdV1mSVMjceuEV1lFOeClJvtxD2WlzJJNvStKsvQy07RqdcSdPe5ovqeUthZPJxVexFqTpW7yHPaLHbKmWr-TvBCX9Gzi-IkV2ngcCaupopaTL_7z8z_--6-fv8TFbgsupdn7QJWlrnFlNputNG24ZIPnKy1VJcrsQD4sUXIKlXClWFGyTFcHlBaTSqA0sVR9PJj64yWffJoOFjl-aluOE9-w6EbxftamRzeLvNuBygwle2MTcptbnn2PTS5MeTAuhDogIewVLy9lca3JyarmdSbYn969esn6zDN0LqWhYtfn3JaRg763ohsWfV-Ul2leXJ91-hEbPXbG5zByYl86d9_hDyotSsWUzGqsybhm6gNwhT7XvNyqesrKRq_05nBEZWp3VBDzwxmXLU_ZTuSLOxtkz9kFHGS3bnhkhyLPxJE9SbNcfbWZsxcpq3eKESoxPtiTw4eb9qQ88RzfvrM9jFEAYM54Y9ZD1oYVWqjHLKuBy3uORkCdZOLyaCw7Ex_uq9AL7LvHx5kPrSd4WWaqnGlUJr5yLQAeqMUdbOxTuhyKuDkXH9v1Ij_27xOfzQ-Lxfsle8S-KJLlh-7Pl5vHN1oGGarYRvKaz04ZPRcfYce2Cu5e0O6cfV9mNYKT82xfsT-_ff0turPeIVOKoaIAtQxzAYPzgJqpiwZzT1KDl-pMfJw48b00SO8TH6WbvSo5bGp0v59Zt5qfiYAXOG4Sxs6dd_Tm7K3GSNwVtemNE5p1YNVGYzObXe-Om2kXpymqR7JzERBRLD0niO9VIZtNtVtpfLq9q6ve3q69ZjNajRGLORlEk--GQW7ipk4cq_sY9HqPjkUISkWcSMkNUpPDGBMwSfiTlNRObE_DGT1VFyxt6qY8k7DAEzFg-O4l6wPyCGKuiOSdsM0kpFSENICXihVNfWjMxEnQVfs5-xb8pjzX0rETcfhyn_iQu0UpFNuWSulzZarigDuuvHtj_BEth3GTaXBPGjfkdVuaHGh7Ko_liSFvkIzyEj2bNGfs8UEswXqSe9lDq-W5yk_4zkRxyABcRTtmKnCi0_CfskMPxGfscRMlvNgL724PLElA5dkG_BaVh1nTkVsgWX5kmxGX3ZgJJLjW6KFLXfzSnvfTngxPOhBYi1LxlnOaOz2HPUvUsbpZsw9Ox9cZEE1cHopM10Z-lGYnIqb9N-Kl74no0wwdrTAm_6NFjKy4py6oirRepygoVR7KrJMfVWIvPcmlq4QTgBumEcDVdpPEhXazg8AN4GaqgpDzyHGE64duHHoW5FsqoyQGyvjURjTPjIxos7W0YzBvujJxLCeYWeHMCd5Z4dJzl070e8taWmRRF_GxPvo0uvrx_6492lljpMGOVzsipMIKbF_JJLIJz80aI7XQVenDZMBIoQJKBhZCsDYmBijX61zJ7dBYVQsDA2Wfs-8qYAP0KTNlS3BB6GEGm6GtbK-4xqe0yQeBDBADwDx9djGFSVW21UwWYsreXDybsovnT5-9ej6FJTSYt0dGtT0d-h5RHjX6QP_nu3qfL-jfQQRkcApAodNsizZtQbvKyHPzprEbzaqyq9ZWg3QEBuCL7ZXb4K5Du8dME84TfzJxrIoGuGxKwyxUzVcaiboFgbpcR34YpG5kB7Hl9rke6bAu178tr7rlVMr9IFE8coU3Lp1OcXXLPURIIfXISiMI8-RKkzbO9oU-msoxMzITnKpvzp4VlLeBPigTOISWljPP8JxhnVsnWOeQ5dteIOzUjgKrd2gk2Pr4_JYS61fzAEcBouOmfr_aSJx1qz1IdcHBdiAw4i9mBpSsQww8kubZdlcPCukdunCl-1FVYbMj2zV77CkRytoEHNyCbRs6UoAFRDbac4iWFfOKQv0OVbw8E0VpJV6aJI5yRe_3SAN2fj9E3FWXlWmAtkWzPKuP01vYT49wkWOLRPoqEvJkz6ABO3seIu6-weUe4Ez2KkNw-3ByZkCtnLY70ECqhqx8PpAylJay_TSI3aQ3fCQWO8MfogKrsfD6VdyUJ5R0HI976SlugzYc4nZv0VfNMrkxjNfEa9Pae4P19oMk0ztFWk4utLpebEnAvXhWnQleouLYscM0wTQ_BW9Qkp31D5GIe2Bzp94eY5wQ_Hw-mDxM7UT4kesrdYLeQUgOwbybQuxW96VrSeXbsfSDfvWRaOxWf4ga_HBAW6DM2_PT5RlHbU-kkXJBlE6mjPTiqGruLQR1jS8dLLVgx1YrsxLDDawiGxTuLDn2d0_gOL44emV0IjszJ7Lsl-exeIhYAVtNnrTHq3mx_Wo1GS_SVdCT9v_5j4BKMhqxpLcQt4bnHYT-4s1eeZrV6Tj9pwY-Znh8LD___fd_Dq-3_bLZ3KKJuzx4UrpemLqWE4V9HkYyecjDvfUvEZc850mBakVNzI1NRomiW1P6t2ZpWeyBShX5TnSmMUfVLUMUOaWh5NeU-P2hrhYgYLollOeK3RaWw20_dHhwaqWR4O48e4iSxhOzU_mhG1V-PAOTXhqHXHmONRovg94eAv3bQrrnVa4vLMkDgMWJpo20dbfiQ0RzDbBiABVk5euXL6bErPJ8GLBGQNIkqTqSdeuvTWDMu-LavNUu_DuMPQjPQme0cPcjE_vu4mWLIRjbRIDxPAEpIXsNXTu2ddPFH8IC4ykvuEFa9UGJBr2XDQTlBEfdr08nfgBvGNqXX_EsJ6N78tSNkQ1LWroFUtlxrB1NTfOjkTGyJoa-yfZUIedmc2JxiztW6rvhiSqOzhtGObrvQUJLYDNN9Wmq1jiCatyC2-XI_LunF988fwf8ME329es3f5vP5wjhU8hiYr77A0qa9jPjg3U_C01NHrDxSptcmwMENHFTd30BHKpAcTRNblIyCHSNt9rAtBN6YwyHoUVOI7DjqSt9bUZpayKapiUh_Rgx3Mfc-4zlbfH2qV3pdtQsWsxrS6jrZjj5LEsBMTQKTroBfICdSOFwJIFqKOEskg0NkdEJxGOjoLpQdk9tDKGEW_szSac5Fvq25YthiI8OdfqkP-C05rqj29UuO8CZlW69h_E9NJ1w6dfq71dHPZ_w939BpkPt)

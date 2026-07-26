[//]: # (ob:e43408a0)
# Project instructions

[//]: # (ob:bbe579fd)
## Proofpress: ledger Markdown and static HTML knowledge artifacts

[//]: # (ob:34d3dbf3)
For accepted, meaningful revisions to Markdown or static HTML knowledge
artifacts—never source code—close this loop. Do not snapshot every
conversational turn.

[//]: # (ob:1be95c90)
1. Read `python3 proofpress.py policy <file>`. Every tracked Markdown or static

[//]: # (ob:665373b7)
   HTML knowledge artifact in this official repository must remain portable;

[//]: # (ob:950c5740)
   run `policy <file> portable` if needed. The setting is sticky. Use `ingest
   <file>` for Git history not yet represented in the local ledger.

[//]: # (ob:406bcda8)
2. Preserve carrier-native block anchors while editing: Markdown uses invisible

[//]: # (ob:3ce94304)
   `ob` markers; static HTML uses `data-proofpress-id`. Then run `anchor <file>`
   and inspect inherited/new/gone IDs.

[//]: # (ob:f5265244)
3. Write claims JSON with one honest item per touched or removed block. Do not

[//]: # (ob:2d919674)
   enumerate untouched blocks.

[//]: # (ob:fd4e6530)
4. Snapshot with `--why`, claims, and explicit actors (`requested_by`,

[//]: # (ob:1a021614)
   `produced_by`, `edited_by`, `recorded_by`, and `attribution_basis` when
   known). Omit `--rejected` unless a consequential dead branch should stop
   future collaborators from repeating it. Never capture raw prompts or
   transcripts.

[//]: # (ob:b2cfcee6)
5. Run `verify <file>` and report its output verbatim. Never re-snapshot just to

[//]: # (ob:94b5efc1)
   force green.

[//]: # (ob:32ab4de4)
For incoming portable files, run `inspect` and then `import`. Fallback `capture`
records only `recorded_by`; it cannot know authorship or reasoning.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzc5NWU0MTc0YjU2ZDdkNWNmODkxOTNlYSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjA4MTIyNmVlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9iYTBhOTUwNDgzMDA0ZDY5NzNjODY2MWMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2VjMDc0NjYxOTU5ZTM5Y2MwNzlmMDFiNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWduO28gR_ZWG9iVBNBpemjc5CBBkL9kk9i7WTvKwNqS-VEu9Q5FMk5yxMDCQj8gX5ktS3byIY49ke0ZGEmCebJHN7qpTVadO19zOmGm0YqJZaTlbzqpqlWQRUD-hPIplIiOh0szPQmCz-YyXcr-SegN1g2vrLQuieJmw2KMJTSOP-ZJzCPHjzMsSlkKYBTLw_cTzM8miNI0iClkUBzwRgoVKRVkqfdxX6lqU12D2s-Wt_dGsGrbBEwp42-DrnHHI8effwGilGc-BGLjWtS4LssXVpdkTvic_mrJUlYG6xm8qJq7YBqxLdx6b8hdAZ1tjN9w2TVUvLy83utm2fCHK3aXYQrHTxaZhxSYNvcs7Xxv4R6vx_6u2BrMSZVFDgUg0poV389kWmIXQS_0giAFm3ZMVXLtFCC2sOPNYFnkUd_aojLMkFGkc-8JaVprGurbKdQFo-RCPfAXCSyiuyqIMERX4K1Oez5POnd66lWBV3ebocGDtFKWR9Wz58-2sP_52hjEuTW3_170GueII-M8zUUp4O3uDHgy5gAf__rtvXrx6udjJ2fyzUoQ1jdG8bTA26G2tawszM4U1Ed9h5oDbsm22pbHGXOnC7lrv8c0O3xRsZ6PWGTWf1fgh7jVbFm2eo4lii4GBzjWel-IK1wINqZcyD5djTBqbNMvZj12kiS5qjI-wBtkQ9scxKZ0dlU0kuMEnX5EjXzT7yhpkY4l5MXs3PxyM2R5hMOT7B_cxWZIc5AYMec7MlSxvCsIKSeqGNVqQP5405ivyqdu8ev4XclWUN24NwVCdNjmkMpRchWc3-dvSECYEVBjgOdkBK_Bo1eZjqdakKQ_b4uqDBweTK2bYHXt9jowhMu_s9voL8hPiQ9bVHlOxCMmhlhbVnlRlrsWe_FbpHH63XpDvFWm2QGzhE3awN0f6uWMvVreIEnp-ewkhpi3Q3KlhZGCNNSkLAc-IbhDvHcMUxk21uNovyF9rOIEv9WIuJEvPbm-wwBQGhOsaiGDGaDAXBX6GP93ZuJFACqjJzRY9ISB1gwmzdAedwDcUkNHQo18C33XJ12SHH4Kpn90pMAx7TdaSNezikCYXWmJivMKGcQJfFQVxFNDz2xsuyN-NbhDcnOldTf708ocX5AYbGWYCEMxopFpMB9iRCrdvyhY7m7RlZxzNHsM3kEjlcfJF8IWi3YFhaHNbDAa5c-vFKQQlhTgKz19RdEFeFtg1t2XTAbe-uLjZ7tfzHtK52wneVlhwWFdd_yS_WlsVcAJBn3mBH_tfJkMx-2QrXOtGO9e2asYfk7a-7mxfj934BL48EEoAxGe3N0KGtYx1bWXbSKXucwOWuDA9a1K2TdU2BBdx3HK3IC9QsZhTDIuyA5TwvwS-qjQCyMYAFKdSMgwYpxLoF2miukAdilQ4cjuxwGE2OvpHZq9QpHQwYkeyj3Z25fp9e9_MB-03Q0BtB14JA6zTX-7NoOdglQSKy4xmzEt8EFwlUaiyLFBWj5WN23MwppenBKtXXFWlLhqnto07yYq04ZfVaG-srrX9arLDVOtONnEq-oEyuC5Vs1KIGZjK6F5t19xf-rG0joXK5xEPvVhklKbU9yG1PSRE_caF4owCKtpAyER5INOECU6p8iS3SNmwOdXcRWvpU1Sh9sks8IL4wksugviVlyxpuAyi33je0rNM1SNuq8CDEPxYYQIdnt6eQ2p31OmU8JbVW3v1iKUIacrRXQuz22MijvtE_Ryl22_MmErDLFPUD8aNJ-J32PgRqtV5fdqIzJchqDSKMUEHIyZytjfiMTp0YtPrYjTq3__8V2E5idRla-nBXk3wmcjLGrAEdU3ysqwW5OuSYLGQeugp9pv9a6zmwsadWZRZTprW3MstQwilx6niPIBQDE5ONHDv5GPEa31VW57r6UXnutnP76HbwZ5A0DQRfhjKEfSJxu3teYw4tZxmJwpjg0DjXhe443e4frjeW2D3YL-3TiK7oHTQhfOqS7MTkEJA05gGXkQ9Obgwkb29C4_Rqy6TnEbUhU2yjuWOIBoAZVihgYxoOqbxQdUeEH2wHO1i0dk7oOoQtRXYNxD8dwtWP8rLAm4uN1Y0fv91fQJGGWDHSz0lQz5m5kTd9nY_RpaW14MgHIrpOIosQZITURpGMDLSRLseUPw80dnvzilg_TEIgzgefT3o0H73xwhINwhxSu2Ejz61ZJf4KslGLjioy0mmPFQWDkOaNWY1FC5HLAMWv16QH3ZoMjpkwLYKkGvED2VITRhxgy90oWg0Epq0RMSNTTeCULS5ZfmycpupFunOMmaeM15iFCwAypQ7W8ioRazM0U2v-bDsKrfcsBtLaLvKysOOCxrcvxZG46MTYUNiyliWgWWnsU0d5G0P2GN0Ka64GAn-lxZzuSmPBzCCJKRKpQLjOJLnQb4eAvgR3TlUIERCcJB-xPnIHAcpOmmAD9WQC_Ity3POkO7WfTSQOfpxIlZwvr-bT47TBSssPdvEId1cr97qqqtpVpe2_37g1Jt31q97ZpNj6k4mk27OOeT3nef3TzK7Qe1QYfbFT1psmZH_7SEn6lknlx8w4zzTHGxXSq20s-7Y_SpGkktCp6vPfr86ovu6Vo5CqlQKqZLlrhBr7Vr_zlbZicvYmSZuHyIzXqM6Nj8Wjg-_769Mz5kEp1AOzlzcaHw2FmX_94QdZsXYJhbHgvEerv0hf8iZcefiSazXnJYtxRU--qjKPUTAodyps9G-xTGcj7r8Z5TdpJdzFmb8lOUXfQA2rZbYJfDQXG8KNM_1TAvQDtcyF-wRmk5JLjr8h7DezrC92oPZFUz162QDq2w7EMZc-owLiL2kffKl-cQfczo4prfh6U1wekO-far2_7Fq__TRyAejgflh32Xw7v4pwMdGImeZe4SJx7PAS4OIQkoT1CDYyFJfJlxJ32NpnMRKxhI8wFeQKMzgkOERHvXjLHVi6aPO3TcDiZf-fTOQ8U-iTzOQpxnIp8xAkhgd5NTz1dlmIN98pDMeV_FpQmkikpTxcFTxE9o8qPgH8917fffZcWhi6mUBT0Kfe-Lh4xitSAGAZe3mBaSGpruJ3TuXcfevyWzmk-cytvc_TWeepjNP05mn6czTdOb_bDrz5t1_AN11QMc)

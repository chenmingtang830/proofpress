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
   run `policy <file> portable` once; it remains sticky. If Git history exists
   without a ledger, run `ingest <file>`.
2. Preserve carrier-native anchors while editing: Markdown uses
   `[//]: # (ob:xxxxxxxx)`; static HTML uses `data-proofpress-id`. Run
   `anchor <file>` and inspect inherited/new/gone IDs.
3. Write claims JSON with one honest entry per touched or removed block; do not
   enumerate untouched blocks.
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

[//]: # (ob:056a6f4c)
Before continuing a governed multi-agent workflow, request scoped context with
`python3 proofpress.py context --scope <scope> --actor <agent-id> --format json`.
Treat only `knowledge` rows as eligible inherited context. Do not resurrect
blocked, rejected, expired, unresolved, or superseded conclusions; follow each
blocked row's `required_action` instead.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzhmOWYxNjA4MjZlMzM2YTQ2ZWI2MmJkNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjZiZGY2NDE1IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9mMTNjZjcxMzc4YTM2YjIwOTUzMzI5YmEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2EyMTFhZDFhMDU1MzliODQ4M2JjYWIyMCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXelyG8cRfpUp-IftCgDufUAqVymWYyuRj6LpuFKGCpidmQXWXOzCe4hCVKzKv7xAyo-QB8uPVOUt0j07e4AEQRA0Kdle_5DAPXr67q-7RfjtgGZFFFJWzCI-mAzW65kX-qHuaJ7hCNN0qOWIwDECbg2GgyDlmxmPFiIv4Nl8SQ3bmfgB9T2T66YbMOE4uumbjhWYwg0NK6Ca73CNhaFNKTc9Ww-Z8B1bsw0eWkDf9jWgy6Ocpa9FthlM3uIPxaygCzghpgUeNYQPgYjhwl9FFoURDWJBMvE6yqM0IUt4Ps02JNiQb7I0DdeZyHN4Z03ZOV0IFGrrcpb-KEDcMkOCy6JY55OTk0VULMtgzNLVCVuKZBUli4ImC8_UTrbezsRPZQSfZ2UushlLk1wkoIsiK8XlcLAUFJXoBDx0LN0eVFdm4rV8CJQrZqFustAFZXnUdAJD823TNECFyFmaFSjaLI4SAZzXFoln1NB1ynWq2bbpB57lmQGj8HIljuJuxug6L2MQ2EA-WZrxfDD54e1AHf92AFZOsxw_VbcFnwWg8h8GLOXizeAVSFB7A5r3PIrj_ITFtORihI90VHHy7V9evHw5XvHB8E4eRIsii4KyAMPNAppHOdqAZgnyD_fA2kKSLItlmiGn51GCVPMN3FnBnYSu0KQVx8NBDi8CrcEkKeMY-GdLsJqo5A7ilJ3js4FhB5qrw-NgsEK8Qek--u_P__zfv3_-GC6qIyjn8uw1epa4gCuj0Wia4IET0ko-TbjIWRatUYYJuJwAT3gtSJqRKMnX4FqECwauCaSKzVr6H83o4HLYcmTYoa4Zhr_F0Zbz3sjTB9tOrk5ANwOX3ToExaaapR9xyKl0D0IZE2swCPmSZuc8vUhQyLygRcTIF2dfviS15QnELpohJxf7xOae4Vmu5m1x9H2anYdxerFX6A9I57E9Mrue4dvcuPsJfxRhmgkieFQATUITIt5AXsHPBc0WohiSrEymyXy9Ac9MzI5DjNd7RNYsoRueze7MkD4mpyAg2XnghqzTOGIb8jSMYvHJfExehKRYCoJZidCWnxhk2OYnpIFl2Pqd-SEEFQDsdA8mdcqakzRh4gmJCsjLKwqBAH4SsfON5GyPfqgtXMvR764fY9yGHqNZFolslIBnwo80YZA8wBeXwGNt0knrxOU-_eim5dm-fYx-5j-cnLyakA_IR2kweaP--3j-ZCtkwEI5mXNa0FFj0X36YbqvC-fuDm2OyfdZVIByYhqtcvLnb7_-CqKzWIKlBAGPglRLoC5A4VyDzxRpCXWPY4BnYo9-oFTZVuiEx-hHJOVKZFDSSZnU50m6-XiPBizHMAPXN-58ojUm3yZQEpdpIWOjyWYqWVXamI9GF8vNfKj0NATv4WSfBpjnc8tw_KM8ZD7Pl9MEPu2O6rzmV4XXaITUCKKYhiGsfFsMmYEZGr4vjmHo6xVELKggE4iJBJ-DaWJgRiqMY_4JMgwnssLiDDFVpCQsizLbYzDHYj6k4bu7rA0pD1PMawR5TW6TBskEZhpILzlJy2JdyooTQFStxuQrwDfZvpD2DY-CLMfoB8VNMybIIhMi2eemgGqpYfK7B8afIOSg3EQJYE8sNyh15ZoUsm3jHpMGI8_BGNk5xGxQ7uHH1oQGqCc4ih-kFscibvI7Yek6gsSVVmUmB0zUFP8hWdeJeA8_ZiCY5Vvu3fkBTgKA8mQO-BY8D2qNAreQyeINmXew7FxWIEaTBGLoPEmv8vNqWIPhgUoCM5YJWmFOeafGsGLmedik6GHoeg6jzAF9uppvooGBuqRZK0fhdQIZjZ2v0ygpZPuRyZMQmNY_IS59hUAfa2iHQhf8d4jItuLIviBPw2IWgkOJbJ1Fqv3IA31icWjEBDMcwIahB8lVN4PApKapO47pgJihcFxKPcNgpu2avmtpjNGQe4EPWcbGMMJ6JtuIyloT3QfkjVcGhmY4I80dGc6Z5k4sc2J4f9C0iYYcKY1jrHjcph5zwEHaq28fvPeoao1sDZY0XyIgZZqj24IHno75XNLodAvKS-_XBnQ6VEglLQrBtNYFBuCuF7Hgizaw8ioNtJB9TL7LITdAf0qk22K6wOwhC5uErWQlaAKfwjJuG2RIYpBgnj0_HQJLebRICE_ZkHxz-nxITj979vzLz4bACRbmxYagbw_buActdwK9hf_jZbGKT_DPtgmIQChIFEkYLSBMq6SdRyi5fFPyDcEqotcVrzLTYTIAvFhd2ZXuVLZ7QhLM84ifpB7ztIS8LF1DEsrH0wQMtSMDKVt7tuuEpqc7vmbWtu70YcrWt7dXipwIqe0Egnoms7quozouRe4-jRSYHqxSMsx5fJpgbxyt0mQjPUfWyIhR9L4xeZ6i3Vr4IKTiQLVITj5DYwJ0dlYwJZBm65bD9FD3HK0WqNOw1fq5rROrqVmQjhzQjhnaNbVOc6ao3avrAgGrgkAQv8gakBGVMeCRMI4Wy6LtkM4gCqdJXapyOGxDluUKzuSgykIqHLAFWZQ4UgAOEGxUc4gKFdMcVX0GXjzZo0WuBVYYBIYwWS13pwdUct-nucvPcxkAVYhGcVRshjvQT53hPENnAbeFx3jDT9sDKn7u09x9DpfrBCetl0uAW6uTEpnUsmF1AhakvLXKzYrkLteEboeObwY1451mUTF-ny4w7zZe1_QmLCa4YVjUChu9tb1hq7ejm758FPG5RLxSX_OK3y3UWxeSKFkK7OX4SSIuThbYwL14nu9RXiB839DdMIBq3iiv7SQV9_dpEVeQm1X39gTKCaafm5VJ3VAPmO2ZthBN6m0byVaZd-sQFXWbmxoXtu5z26mpd5pGRf0-3eCbNYQFuHk1P53sEVS3WOgJE4BSw0qnX-x4zdGNYFLADyotVcmOTKeSEoEbQIWX4LijYFPfbZJj92Lnlc5EdiQnsuTqPBYeQlRApoOn1Xg1ThefTAddIsqDnlZ_j3-EVIlMgy7xLdBbSWOVQq-8WXeekjqO038qQcYIHu-2n__5x7_a16t4mc939MTKDhbnpuWGpmZ4bm2HTpvc2uHo_heBSxzTIAVvBZ8YS55kJwrRGuKfBQmzdAVZKUfZEc6UclRdIUQWoxkyeoGGX62L_AQAWFIByn3OrjPNoLrtGtRpQqnTcCvJ7tNJwxOjxv0gGkW82ZMmrdB3qbAMrVNe2n67VfTtjXSNq0ybaZw6kCwamNbprRXF-zTNBSQrAkkFrPLpyxdDRFZx3BZY2UBiJckVyNq5bQLEvEwv5FsV4Q-h7EHjmSYRElZLJvLd6csqh0DZRgAMz2MixcxeQF_b5XWu9A-NBZSnOKUy04o3gpUQe1ELUJp0pLZPDT4AaQiEL31NoxiZrsGTKiNzElRwC0ClwlhLrJpyaSSZLBChz6MVesi-2hxoVKOGFtqm20DFzryhY6NjBwkVgI0S9E_ptVIQ8MYFYLsYLH_27PTzz84gf8gg-_Trb_42Ho9Bhc-gLUbku1qDS-N5snwQtRYaSjvAwdNE2loOECCIy0LFBeShHCBOgpUbOxlQdAFvVYqpKvRcMg6MpjGWQIVTp8mFLKUVixA0FQipy4jEPvLeDZxXzlubdppUpeakynmVC6loBiGfRyGkGCwFTd8AeIA0oLAdSYA3ZCAsGBt6iAgnEE9kB6VUqZ6aS0AJYq32GB3rmGvrms3aIt4Z6tRGv8e05kLB7XwZrUGYaVJJD8zXqanJS9e7v2ujnkvkfcfqE5Hg1cWnXKPKwnn1-u5FabUHlsVR3cgicLGM4874ne1RcxGHM5qDY9-wRJXw4bgd6oF7rFXKIWPK028axx648TmE0mG7kQMoHTiyPoDSzv1aS0EB58fYrO3cZN3KyUPssHbujG7l5Lht0c5h_61n3YJOIN6rRH5TSFz3DzUi_hQKUSywrGDRgDNH6zIAMxNIBggrG1ihoBmNcHCGXqX6V0x-N4XPY57ahtojntoJy0c8tRPC17zm4Q5to_XxDu0E5iNK2kboAx_6qpMD3g6gF5U17xjSzdBo-wzcXxy8T9JdC4CRa3iOQU3P45rthpxqbiN2d1HUXZJ0l0dv--LcF-e-OO_a6R60uW02l423TKxhc_DEuty9prxtZ_veLWZvFu_qmlY3J5o7MbQda1rP5i73QrNf0_Zr2n5N269pf0NrWtPnjh5qpm4HzuOtaeWS4F0vWq-O8KF6MMd0fV9rdyW_-KK1Wtm8D6vSq-JDKjA9AyAQlNRHW5VKMQ7CUFfZ7Zed_bLzd7PsNDULEB8zoVUOHm3ZKYW7see4GgT9urJfV_bryn5d2a8rf0_ryv0zqwf61bSdE9X9nDzQL4Ht_JWs_Zz8kr-Mdfw67qs0W9E4-jucS_mPlGFO2p7tV9Wxat0glDKsitB4fVEGoJIEWtcDFnLX9hkPcuy1jdyjHNsx_YMfu2t_k_wixO-0uBGB6Vh-4BqOplk-cyiibc0wblrcNGPTd7646dPUO05Th68Ad0zu9c7k3rzcPZj_FS8mroq3YzGhGxPL2bGYcLitWYbF-sVEv5joFxP9YuI3tJiATGoJ5upGQMPfxWJimvzKVwvT5JGXA9OkH-_34_1-vN-P9_vxfj_e78f7v53xviyJk5uG_FfuXhn1X7u7PfCXSHWixv6j93vuL3lt5_5lgtZIDp382w51Qosd-w2A-FKUlFU_ucBsnUBcrcq4iEYVZLlQxCCOKiWT_MBfGGlZu8KFmpyeCQrlWZ4iq3NDH9IUBjdmSvhbyVUnUMVx1crtnppWhFWaF7xzBGZtQJqtpDXxYpml5WIp00sI-QPz-fhOc9M933S6c27aTHUOmJu-J0Y-fFJ87SuTLncPtB5loKe7emBSX4Qu8Om6DnScvs3swOGO0IWP40UKvTcFXl3LcbllGb7mGy61PD_QTP0GeToTPG9kWGeaOTF8OGzXBK_-htx-gtdP8PoJXj_B6yd4_QSvn-D1E7x-gtdP8PoJXj_B6yd4_QTvvZrgdb6CTYQ8DKhr06D9is92ILENbI-aNFTjnnoSg5a8GQCrh0Yj-RZ5Kv_CaictTp7KQwAi4aUQ__FcQbAeImw7ww5SqbHpPUG_6QWYOScC4LN0-QY21ac17QZwUcp_YTdNZFwIjlJUxWuI3offnjCEKla7d9VAlgCicsErglB7ZL_zBJwmBj0QnFU19JCbD3M0s_z_7vAZiAVPz2XGg4q4a9L66vL_AIYuXg)

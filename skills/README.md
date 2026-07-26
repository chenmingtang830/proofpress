[//]: # (ob:df70df88)
# Proofpress harness adapters

[//]: # (ob:93121540)
The skill captures rich decision context when an accepted Markdown or static
HTML artifact version is still fresh. The hook is only a best-effort fallback. `ingest`
backfills Git history, and the embedded capsule carries portable history beyond
Git.

[//]: # (ob:1744e48a)
| Layer | What it knows | Attribution rule |
|---|---|---|
| Skill | accepted version, claims, why, consequential rejection | supplies known actor roles and basis |
| Hook / `capture` | Git candidates, admitted ledger paths, or explicit files | supplies only `recorded_by` |
| `ingest` | committed content and Git author | attributes from Git metadata |
| Portable capsule | admitted records attached to the artifact | preserves recorded fields; invents none |

[//]: # (ob:50c32349)
## Shared contract

[//]: # (ob:666c5555)
Before editing an existing target, run `capture --recorder
<harness>-preflight <file>` so any human drift becomes a separate unattributed
version. Then:

[//]: # (ob:a2f15f7d)
1. Work only on Markdown or static HTML knowledge artifacts, never source code.
2. Read the artifact policy. Enable `portable` once when requested; it stays on

[//]: # (ob:23c62cea)
   until explicitly changed.

[//]: # (ob:7109fe56)
3. Preserve carrier-native block anchors (Markdown `ob` markers; static HTML

[//]: # (ob:f8ee70a6)
   `data-proofpress-id`), run `anchor`, and write honest claims for touched or
   removed blocks.

[//]: # (ob:9d481ea6)
4. Snapshot accepted, meaningful versions—not every turn or save—with `--why`

[//]: # (ob:9710997f)
   and explicit known actors.

[//]: # (ob:c8f43a25)
5. Use `--rejected` only for consequential dead branches. Never infer rejected

[//]: # (ob:41bb2485)
   paths from casual discussion or store raw prompts/transcripts.

[//]: # (ob:3991a868)
6. Run `verify` and report its output verbatim. A mismatch is evidence, not a

[//]: # (ob:a08bfb00)
   reason to manufacture another snapshot.

[//]: # (ob:a8bc86e1)
7. On receipt of a portable artifact, run `inspect` before `import`.

[//]: # (ob:f20cc96e)
8. When several portable copies share an artifact and lineage, preserve every

[//]: # (ob:bc82651b)
   original and run `merge-plan TARGET --from COPY...`. Apply compatible
   changes, ask the user about genuine conflict blocks, then run `anchor`,
   `merge TARGET --from COPY...`, and `verify`. Different artifact IDs are
   ingredients and must use `merge-lineage`, never `merge`.

[//]: # (ob:f5f3a858)
## Install

[//]: # (ob:8a9fcf71)
The npm installer is the recommended path. It installs package-aware adapters
that use `npx --no-install`, so agents never download the package implicitly:

[//]: # (ob:5ee2d540)
```sh
npm install --save-dev proofpress
npx --no-install proofpress setup --agent codex
```

[//]: # (ob:3328131b)
Use `--agent claude`, `--agent cursor`, or `--agent all` for the other supported
harnesses. Add `--badge README.md` only when the repository owner wants a
visible Proofpress provenance mark.

[//]: # (ob:041482f5)
For a vendored `proofpress.py`, install adapters manually:

[//]: # (ob:0e468706)
- Claude Code: copy `claude-code/proofpress/` to `.claude/skills/` and merge

[//]: # (ob:225dd61c)
  `claude-code/hooks-example.json` into `.claude/settings.json`.

[//]: # (ob:3e5fba6b)
- Codex: append `codex/AGENTS-snippet.md` to `AGENTS.md` and merge

[//]: # (ob:3ef5e70c)
  `codex/config-hooks.toml` into the Codex configuration.

[//]: # (ob:9d561c7d)
- Cursor: copy `cursor/proofpress/` to `.cursor/skills/proofpress/` or

[//]: # (ob:9cddddf2)
  `.agents/skills/proofpress/`, then start a new Agent chat.

[//]: # (ob:2202e132)
- Pi: install `pi/proofpress-skill.md`; `pi/extension-skeleton.ts` is an

[//]: # (ob:cc2d6144)
  intentionally untested extension sketch whose event API should be checked
  against the installed Pi version.

[//]: # (ob:c883ac9d)
Adapters expect `proofpress.py` at the repository root.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2U3NGJlMDlhOWQyOGYxODU1ZGI0YTAwNyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjVkNjE5ODQ0IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9hYTA0YWZkNjc5ZGQ5ZjE4MjM3YTU2NTUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Y1N2FjODMwNGFiODk5NTdjZGM2MTQzNiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNqtWulu3EYSfpXG5M8uVjPifYyDANrEmxjIYdjeDRZRIDa7qzWMZsgJm5Q8sAzsQ-wT7pNsVbN5SLEZa8aBY4hXd_VX11ef_G7B66ZQXDRXhVysF_v9FcRBDk7KU-klyk3CUOYBd5x4cbbIK3m4ksU16Abf1RvuhdFapb7jc_ByX3CexIEXRL4TS-Wnjse5yHOeRJ5I8zxJHI5rhQ7kbuTyQIhYQerhurLQorqF-rBYv6OL5qrh17hDCW8bfLzlOWzx8l9QF6rg-RZYDbeFLqqSbfDtqj6w_MBe1lWl9jVojd_subjh10BHenC7rn4DPGxb04Kbptnr9fn5ddFs2nwlqt252EC5K8rrhpfXie-cP_i6ht_bAn--ajXUV6IqNZSIRFO38P5ssQFOEIYyctMkCBbdnSu4NS8htHDFuRNwJaM4lTJFcD0_5mEUhmRZVTd0tKttUQJa3vtje6XCmAu0JeB5kqZhLKSI3MCPuuNY664E3-t2iwf2yE5R1VIv1r-8W9jt3y3Qx1Wt6afuMcirHAH_ZSEqCW8Xv-IJ-lgg594U260-f_X84psfnq92cnH2pEjhTVMXedugi65yrgtNaPO6JEvxGQYQmCXbZlPVZNNNUdKq-oBPdvik5DtyXmfb2ULjh7jWYl222y1aKjboH-hOmG8rcYPvShU7UiUJvo6uaSh21osxKJjdn3HJ9w3U5FC7K5fSmLOnsII7vPMFm_-wOezJPHIwBsvi_dloRuq7nhsGzucw480GmPEEQ_c2LX7P6kJsmATRhb_dgd1h2DKOf4QAXFWyH_ho5Z7X_IGJbhwEECT8c5h4z77nB6jZPft5wxtWNOymrO40Xl-MMcBqDE12f1neL5fL4X-8HI00wf_AytARvucH6QMrX6NteDy6UVOkzvnwC_bHt2ccF0WRCEOTjEft93dQVQ0MZNHg0uQNeIvViX5ueH0NzRnCULLMupItlzYR68vyyxlvcU-5oYrlsXa5K_ZzVd-wqtwe8C8MjfpGVnclq2qmG94Ugn335ofvjd-2IK-B9Zmuz0aztniUB2Z5vsC6DvxYsxhjbdkUW0Rpvy1E0aB1XVrL1QwaseukCsLo2G39FaY2YP2-BUyqui6gXpYIAl6aLdBvAmuSZn8ZcMqqPGM7vJpBQyUAscOjE9DIJG_4cizpy0Jmf7Ux0xmVnaF1kt3VRQNsU2GONkxs5zI9lUHiwvFmBSv2usTOsqmaobacsR3wEsNatVuGXZsKkf7ff_5b4jtAXZxheJvomsErJT-msToBL4Kijx0TvFT-qMfNhY9IVOAjbzl233DF_qmBZZS8xCRAZl1iYe4zwwh-b7HhFnyLRZpLltfkOtAr9iPMwBG4ee4FSXgCHHvebDRTdbXDuNYtGYC0qjV9s0t1qk41v2MYYrt9o89x1VKLegYtP01dpG_JsWZFK_aKwveWmNshMy6rgagONgrNqrbZtw3FUI4ZuFuxC7Yr9I432OKKGbS4k-Qqd5wT0KqBa8SlqTCxy5aKHZVkjjG8wWambczPRRJPcpFE4B5rRLxiP2FjBAHFvmGVYpz1HHAowDb7i1LvMdYylnctJpsrRJ4jRBrBsWYl2C2ITGhKZQyiwSZR7QvkH5qWMlTD2mic2pHWGbMQKy8K3fwEl1V1cV2UaJKJIsJlB9hWl_stWvPm4tW3z99gTzUJ8PVPL_-9Wq0yjChk0DNOVKHyeRI-DPAXJbbF7fZPuMX41gynSHiqhIrdp65PxK_c71jRvYohWWiGoUnxUu12UOIHJuNX7EXTv6WZmXpmjhsCePIxN_0Ec7Is05vLcmIRIq35LSwl3LKxZdErb_FRWS379_DhaBDR-YcFxvcS138UFp9gkK3BOCeVpgW2ErA5jnfaWpt2iXVvuIlLZlSmZ_BxAjdIPBU-1Zx_4D4c61gpKwrobERktT-gGT0YPaE2RQdvHNZzxkAQJbETPdWYJfvaAMK-RrTXlLcHJJ3m1pIcMJlpzzOqgNmqe3qu5xiO54USR1vxVHPYw803VXWjl_CW7_ZbWP2GRThDeB5YAQ2RZo0P51oThCrnUX4EOjRTrhnHgRwLSWZGzPOLb5__-Ob1UpcF3m5w4O2Q6W6bS6w6M-j4oEIkgEehYwzAr1RxvTTwrJpqt7WwUNIbi1n3RltzmqhWs6QvRD89Ghg-DRqTN0PMmKsPhUv3wGoE5vkc1RMS_1PeEdCsTObqBztZS84ImZIGGCQTnJVwxy663McxdA4dz3M8cH3v6ei8LNZDJmf7YmLO0hhIYfLMPMFFoSTihQ9gC80MOkJ4mFVGLnoiOhgexDSrkgoJzVJGVWHD3gz3JiZ1t6mwWhodiF28fIEdfJYfJz4X6ZNj56KvbMjIkao8LoGMN7Z97StdGMUOn__RT7-e9YLVwk4WVwKpWqcWmSe9-jQrpiGNM2v23MVqahgbIG72FSJnJMLa7ESSUn9FitKvJMbhVHGYrDAV6CaLGOnvSO1OV6q5UljooN7XhZUIde6ulRsHaZ4EuRtGESA9gSR0hYSIBxJc8ElaTUXs-ypS4OauG4Re7oIQEueaPCekaKw3Ul_nqLXvvUegSYTD4I-WTrz0ojdOvA78tZf8zXHWhktbxKca5vvJ3XefUR804dbJdxuOAbleyCROc5lHMRhfmzUmip6NxCN0Obu-QlLsBHGY5kHUrz-R6uz6pwhuj1WVy9LIKgNPtkASk9MNbaFweSRwtCeVfXpgRkmOPF83S1CKBiWFmZcjr1vRHEDSe3ZZ0rUiB7Bvcfa1GngnDlCWwS4HcjyzorAVOvRI5gfZHA5VKS9LXOZDNdNixwMndmM_l17k9dhNNESL3WlKIHttYL8fEbV4nRG_K3b6DDHHMz6csbshnNa9Z7rFjKNTTrQArDJbvEPAGBna7My-I7TPByUuw48JR4GvFRKLDe7F5a5oyAqjiNXddG345CA5oANAT_c1zssm6nrWbdf7Dd8l8t6tawKp7KYn2ryTwun8Fiywwzw93EHDSR3q1ns5jGTWvfejuVb6p1U4FirJLIUYovCe7a38pVlvKh4FtlI_w5ZCJVazsipx1Q-JszYicodjQjlJDLnTR8REr-2z9RMVWLuoB8oPgPNcimHRiShrFz1JZrUl46slgqC2xfWmYV-SH7_KmK5wrQPbtMjNmawL1WB2oL8ofHAappxoANvs4B9MGxuiJofL9ccTKPchEWmQ-JDm_ckmsq492SlCLRKgWxIuqrYWNKtLWF2W3oq9IhHqQQB0vW3FnpcmhrK-JpCOhZ-awka_6DJs4hmlMe59oOj-AIux5wu5G_IkT7AN8f58E33Ynu-Jim-PXep4Apse9tGhMUxEYLv2KbIuOvHZFOCPn9ODxMGhI8ahFXpbJsrveM6jtVwsdEZKbKrWpG-FUWvkql11i5dd35xBy3HBTWXkycQZcmgiAlsLT5N1afDHB3dFs6HpGstyNgOZ74Pje7mIEn8waBR_R8ieJOfaxSMkRq4nfZXw4bQThdcufopmS0lVlAr_7r_9-FETP3RT182jaMR-IuyORz1aqi3w5xk4VOqmWGJS1wlUb8BEwrUGnCLKIr-_LSRgocCKQ8HzcTRkGkSuRF4aOWPNG4XbEY3jpdi--gROCEqAj5x12GlUZ-1Op-itxY5ezVYfP60IAhVFaeIEMhwqwyjFWhtOEVcR8b5zd_k4U47jCOmfUthdhpI5EWBH6I-WVA_EZDCMCzTeFCj7C3ksavrG9Bv6JxKM5xhNDMfyFo9gBAxM78ZWMTvBP6iJZq3OiI_s35XNPnhX7JtCYXYaJtVj9uIbbNl1ZxfWM-QfhWE19OGuxTrbUjXoTmqxzfoG2t3OZqItUVImInHdMI0HT48y8kh9ZgXivjomrnCU40EghqlkohlPppJj1WA8I78zUWWnpMuyIXpuMHis1iIMRIOuOxJoAKFWua0sibArMswH28BnSA-yOSfGyhNF3nC2iQBtz3aatNyPghqads8G-Zf0sssSl_6A9Ny3DidKczdWoRBiqJWjGm2tO0VnNojZIoYjAqY6UUbLQKm7XEhJX-WcqNwwSdveZHjYI8kEXYGL3XETzMg-cSSl4jEZiRESZPCciBwxm5kwlkmaesAh9dXQKybytz3_ZxW2-2mSmnYUuyADd9h51Lrtzqeo2Eaa6BqbSeePV8o8j7AhSAhUPsToROgeKuXxEjY-nJus01AFjpMKEEPrmijbIxZHa9Z_hoDrcCf1UlCgnNGCQcyeIPC5ZOqeqToiFYmj8PxiZKqDcj0e_WhNun8-_ZXP4-NzDPg0z5FCiqGaTwTr8fifU4ruoU-F6yBbh8jLx-Ab1OkBgeN1Z3RAozPqFnxmekuDXECCtCwNhultIksPGBwvOFftFmm11V-pCiLdv-Z0JhM4fV-TeNR-9JjjezxJEj-KfJGkI-sfdGtr7-dSpN_jn_8DxY9Fnw)

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

[//]: # (ob:cb4fbca5)
Before continuing a governed multi-agent workflow, request scoped context with
`python3 proofpress.py context --scope <scope> --actor <agent-id> --format json`.
Treat only `knowledge` rows as eligible inherited context. Do not resurrect
blocked, rejected, expired, unresolved, or superseded conclusions; follow each
blocked row's `required_action` instead.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzcwM2MzZmE5MjZhYmI1MTJlNzE5OTMzMiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjUxMDEzZDljIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85OTFlMjJjOTJmM2U4ODQ4ODg0ZmQ0OTYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhkZTU1ZDI2NDlmMjAzZTgyZjQxNzAwMyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXetuG9cRfpVT5kdalKT2fmGMAKmTOCkSJ0iUFkVokOdKrrXcZfZimTUM9F9foMgj9MH6o0DfojNnL1xJJC1LpOwk-yMWudw9Z25n5vtmJObVgGZFpCgvZpEYTAbr9cw3bG4rGloeZcw1LembYWjb1mA4YKnYzES0kHkB9-ZLarnexAttR4bU9rhjK4sFzHQ8w3MNeNKThsss5hk-C4TtGdQMA6Ecy_Z8QwS-ZxuuYLCuiHKevpDZZjB5hW-KWUEXsENMC9xqCC-YjOHCX2QWqYiyWJJMvojyKE3IEu5Psw1hG_JtlqZqnck8h2fWlF_QhUSlrlzO0ucS1C0zXHBZFOt8cna2iIplycY8XZ3xpUxWUbIoaLIIbOPsytOZ_KmM4PWszGU242mSywRsUWSlfD0cLCVFI7qmYdoi5IPqyky-0DeBceUsDE1pWTy0lC2DwAngPyWc0EPJ0qxA1WZxlEiQvPFIPAuEdF1heU6oLAOes5Rj-oZhV-rU0s04XedlDApbKCdPM5EPJj--GtTbvxqAl9Msx1fVx1LMGJj8xwFPhXw5eAYaNNGA7r2I4jg_05-dffLks6fn34_yJAIlivFKDIZvFTm0KLKIlQU4bMZoHuVoe5olKDd8Bl6WesmyWKYZSngRJbhqvoFPVvBJQlfoykrS4SCHB2GtwSQp4xjk5kvwlqz0ZXHKL_Be2zU4syncDo4q5EvU6vf__fmf__v3z3-Ai_UWVAi99xojSl7ClUe_G43IJ6BoIkiRkkp30Jn85x__IsVSduKM4MoZGIGoNCOPa-mKzVrHHc3o4PVwK5FrUm45zL0i0XaxCYmlWMiMfE2zC5FeJoSCBHlBi4iTLw5J_MEH5LbLnH_9FblI0kt9DwEfbuXFYIXAvyKyaVieq1xxdJE_B3tRzuUaPD8kK0kT2FqVcXuwc7R9uyzcvdXggImpCqUSlnV0ef8kwcOSSBEVICg8RuRLyDz4uqDZQhZDkpXJNJmvNxDDiU22J3O8PiCwMAOTc08eXWBzTL4Dh5KdAm3IOo0jviGPVBTLj-dj8qXSoY15jdCtvDHoeEVejxsqMG12dHkJQQOCuF3BSJMU5yRNuPyIRAUEyIpGEB5gfH6xGZMfcnnAvgajkCmd4weENYYzJ8FcLyThNMsimY0SeAze6r1hIQ7JLCeXS9CkCZyJ3uiAfQ0WetI0T2LfecrmZAUPyiz_6EpGALfnZC5oQUfbMBlFAgLjHOrhoZzmMuabvnN0ee0x-WsWFWDcmEarnPz5-2-ekkuo0xAJkkBEQ9GAcJArsobli7SEwi0wT2S6YOyzr81sbpqudwr7yqRcyQxACymTRiC9bz4-YEEbvG06RnB0iZwx-T4BULBMi8pw89HocrmZD2uTDvVK8uUaDhycqwoeTA7FZqAc25XOSWJzPs-X0wRe7c5XeaNJnRhGI1yNIMJrBUZ0cEVg5lqmZLY8hcDfrMBmYNFMIp6UYg5OjxESYBoVmHlZhikADhwAHMgDiGazMXl6IBS48C3JAvvo8rpQDDC5vkAA3WZ9_XgmMcfCScpJWhbrsiBwE4MlVyArYMfs0GFyA-n5NDyFfaHcckkWmZTJodPDeBBYri9PA1ASEiVACrDKo8mqY0ShSG03aMlLk1oJKw_I64jABoBCTyIv7hbHMm7LJuDTdQSpPa2qew4omjS4fUgupFyTqy6-WT8DqSQNjp-dPgdJGXA0MgfiUpQZlPiatUCCjzdk3iEpc134OU0SSACAXq_L-2zYsJwBaIPoccYzSStSoT9pSIqcCQEJweWu43mCA_Oi3JHUpVhwYXW9ZmO8mogRSOT8Yp1GSaF5ZaZ3QubRvEPi8QwZHEKXzgpdVtdZRPPFOxK-PFXFTEFAymydRTWvzJk5Cag0XStkwMd9x3eVKZjPQqFcS1HXD7yQM-DkKrR8W3HleNIyYE3FQsUFNzk6GN2m-WHlrYkZALXCKwMLaMDI8EeWd274E8eeWOEfDWNiGPBUbXHEssqzuJQMAmh79dXJSGVVWjXnW9J8iWnOEgEzpeE6Jkqm1-jQwDp678fvsOSAx8dQgT7ecW5qSShVgR2G4DdLNpJ06F8tyX14mzZTvpu91UKEprClClyPM9UI0SF0tRD3YWIdmaZJKxTYMcG0QvK0xCSO7oZrPE5zCQaOoBam6XpMPk0JHui2tOMzmykk3ASjh2K3gMYEcsPOClArqSyLG6a0Q8lbJTsssFbyXvRtQ-oURbDc66yUaaVeAlqWKo4Wy2LLpM5BwWmyrrlBDnttyLJcwZYCii_gLLhEcol6AFKsz4muLFB_yaLE1gaIhQW56oeAyacJpLM8TSo4PtlvDUMYzFGMWdLmjTU6FLO2xn24YX6R68NQZa8ojorNcAdEaOSxuBP43LRt0XqnQyFree7D_cgck2HeOgCF0zjyCdzfNAcxzDYSn9d-gTomoLJrrapDdyDApOUEnmNBUjFEo0KHVdYq3IcO6nOlKViU4JGrKscei1rSoUyZlnCdYCtOSxq3Fr0z26t8UcnbWFVbFPMRWH8NeBd-LiXSM3GWyMuzBXKyLz_ND5hRWEI6gaGEzdrI7JDHWu77sD5AYTXfalLLfitSX5mMuwHQmTY_d6jh1opvx-maOgQFy5dQRC3d365W39K8evWj8bPWwoCnDCZtw6NtZGwpWycy7sy1kgLe1FlJJ0AyneqFCFyHRUTJpRixTf1hmy471zoPdLrCI90VJtd7wnATgjIyHTyqWrxxuvh4OuguUgfKo-rn-DlkSZQYDIlPgdFKiqUMs-e1JxvmplfHVv5PJSgYwe1d-oagoH1cPwvm28E5ayc4gQgt2zMU5-3x7NDQrRPuzB91ZY0Shf8CLsnSlZaK0xw1RTpS6uY4noqmbmX0En28Whf5GeCZJOdZBK8PhHDoGiENoai6-nhWUGpLT2s97sMr4Y5RG2nPSzjXRbo_uF3p245SAXf0Aa2O1JZ-bu36Bt7YJHXb5YagHiQAu3XTlkp2odEdOWABCQhwDgefPP7qy-EUak4cb-uo5jNYJnLyYv9Ua0jAOpf6qWrhDwFaAA9KkwgXrodZ5IfvvqqSBVRnKDAS7sfkiMm6AJrVlXVeW3-aYNWJU6qzp3wpeQnnLCpaINLmnXrK1cIA0IbAUaUvaBSj0A1yqivDnLAKawHJqQHWEkuiHk5pIQusMfNohfExP-AjysyQ24EwwCuNjzr0ueOju_LeDegeLSJEmTpktR6Q7hdytI7B8eeffPfks3NIFXjKyONvvv3beDwGCwJ5iDGfrdYQz7hdVeLrKdRQuwH2nSba1ZrOUoZGrQ4FpJwcgEyCBRmsCwASQPOwtktVd-dabnBYGmNVqzHqNLnUxbESMZNxBTCacqHrtv5sj-RV7DaeBcSuS8pZld6qCKqP8rzGVtVONUGFyoRAqroIby5R4MasWP6nSQsMt_Q5h5yk1EGIFTrcde2QKUbZtnK1jYfG0_foGFzWWDpfRusOnobwvCHWs9co2Y6pKWK26zNTPYHVVe_69d0z1mqErGtb_UEWQdhkAsfNDz6CzWWsZjSHIN0zf9Ul_27j1yMNtlYpRE-kpds_MjnKiOcWOx1p2HGLnY7UCb7FTjsHetsValz9MKO6HaOvN0pyiqHWziHRGyW54_hnVw_9jXsdQjmQZKqKsO883gyOuvP5GCpaLLE-YfWBDUfrkoGPAXuWCEVbeFIDPBplcC-GVE1vdT7dczYfcNfOOX3AXTtn9gF37ZzfGyFzQre2R_XhNu2cygfcdHs8T7zps04CeDUA_qoL7l2WbovC1T2wLX_rMYnFQohly4Pzy8DZgovQtZhuKlZqd-cf3d5_dybyqkcGPTLokcH7hAxuPw1tp4FtqEycYbvrxHm9e_T3pjnoezfs3K_e9dGnaU8Mf2KZO0afymIyMF3ajz770Wc_-nwno0-fstCnHEqjYT3c6FP33t-f4eWNORczlGsox7fc4MGGl9WU5N2OH68bwvY85ZkeE8qWDzV-1FLfqvbfmHb0A8R-gPjLHiAGyhc-s6gjqHq4AaLWZDcEvh7t_QiwHwH2I8B-BNiPAH-lI8DDrZIT_f3WzkbgYUlO9ZdOu_6u6LAkxwGUd58_PU2zFY2jv4N6VDynHOHi1WZ2TSg0DYPDlWHpA670RcnAGgmQ01tMoG408E-x7c0R1INs23H6ybfdNbBIjrL4W00qhON4iivfosqUgivDVoEKFd03qWhbde_9pKJPYO8sgd1-Grajj2x2-sj2691t4l9wm_y6ejva5KY1cfydbXJfBYET9m3yvk3et8nfSZvcMqRFhS1owOhvrE0-TX41je5p8rCt6mnSN5v7ZnPfbO6bzX2zuW82983mB28263I22ddyvvbptcbzjU-vtp819JzUTejR-9mF1jJuu9BlgjZObvtNgPgn8Zy6p_pSOFw0SkpNG8gCE3MCZ2hVxkU0qmDIZZpdqDi9hDNTGZ_kt_ut_Y7o16Sou3nnkkLVrRgnpuB2fchIeJAxKcLPWu8mV9YSawK1p5NXLVxndCk6W2CCBqC41bRZvFhmablY6lSiIFdg6h6_VS_vwNdj7unl1f2EN_fyfilBcPvu5o2va3m9u9XyIK0mAyh2SH2XOj5geNNigYPPupbwHI6vTMdwbYf73ILUawQ8gEueIzkTzA2ZuUefTm8pGFnOuYFfPbP7VzDbr13te0t9b6nvLfW9pb631PeW-t5S31vqe0t9b6nvLfW9pd9gb2krlgmQFEQCgrb9-rUOJb4KVO_EZauGQ9MLQO_sB7T1TaORfoo80j-wWGkvkkd6E0AzeEnhrxRBXgQV54AVzrF3UBuphf9gvfQyR3ArAQ_rMG7BTbNbi_hBilL_3tE00bGOxKOpPUOMKPwj6iEUoSZkh5p2lIB1cimqBXlcanLyEeToGOxAsFvSrofSfJijE_X_LkTMQC24e66TGBS0XT3AZ6__D7t3L1g)

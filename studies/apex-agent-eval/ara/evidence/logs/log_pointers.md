[//]: # (ob:003c4144)
# Public-safe provenance pointers

[//]: # (ob:f654648b)
The detailed run directories, proposal snapshots, prompts, raw model outputs, private corpus files, and generated DOCX artifacts are intentionally not redistributed. The frozen aggregate manifests retain run IDs, timestamps, artifact hashes, and telemetry sufficient for the filed descriptive tables. The source labels below identify the non-public temporary harness snapshots without making them product dependencies.

[//]: # (ob:eeedd3b1)
## N03 — Task 1 normal cells (C01, C02)

[//]: # (ob:cb45fce5)
- Frozen manifest: [`../raw/task1-three-model-finalized-v9.json`](../raw/task1-three-model-finalized-v9.json)
- Temporary harness source label: `temporary-evaluation-harness@1ff29dd`
- Run identifiers and artifact digests: retained inside the frozen manifest; detailed run directories withheld.

[//]: # (ob:6c82759f)
## N05 — Task 1 stress gate (C03)

[//]: # (ob:1bf4eda5)
- Stress receipt: retained in the Task 1 frozen manifest.
- Source harness label: `temporary-evaluation-harness@1ff29dd`; raw conflict packet and model transcript withheld.

[//]: # (ob:f6791561)
## N06 — Task 2 normal cells (C01, C02, C04)

[//]: # (ob:7f77fd75)
- Frozen manifest: [`../raw/task2-jcf03-three-model-manifest.json`](../raw/task2-jcf03-three-model-manifest.json)
- Temporary harness source label: `temporary-task2-harness@0b7ddf4`
- Run identifiers and artifact digests: retained inside the frozen manifest; detailed run directories withheld.

[//]: # (ob:1adead8a)
## N04/N08 — Upstream construction and reuse (C04, C05)

[//]: # (ob:13e0cbbc)
- Task 1 preparation summary: preserved in [upfront_and_reuse.md](../results/upfront_and_reuse.md), sourced from the frozen harness label `temporary-evaluation-harness@1ff29dd`.
- Task 2 aggregate reuse counts: preserved in the Task 2 frozen manifest.
- Proposal snapshots, detailed working-set exports, and per-claim event receipts: not redistributed.

[//]: # (ob:82d28ff1)
## N09 — PR35 source study (C06)

[//]: # (ob:e216065f)
- Public results: `proofpress-pr35@c96fd86:studies/long-horizon-eval/relaybench/PUBLIC_RESULTS.md`
- Claim boundaries: `proofpress-pr35@c96fd86:studies/long-horizon-eval/relaybench/CLAIM_BOUNDARIES.md`
- Frozen result JSON: `proofpress-pr35@c96fd86:studies/long-horizon-eval/relaybench/results/final-results-freeze-2026-08-26.json`
- Source visual: `proofpress-pr35@c96fd86:studies/long-horizon-eval/relaybench/visuals/proofpress-results.html`

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzM2NTE2YTBjMDNiNWU2NDQ4NjBhNzJmZiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImJjZjVjN2M5IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV82NWMzNjk5ODA3ZTJhZTUwZmFjZTNlY2EiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2EzMTI3YWMzMDBiYTk0YmMzZjhlNjgxOSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWutu2zgWfhVC82eKjWzdL54_k0m7QBfdNuhlMUBbuCR1aKuRJY1IJXWDAPsQ-4T7JHuoiy2nSezY6aCzCFCktkSdy3duHylfGrRSqaBcTdPEmBhlOXUD3w6oxS2X-RB4XhRYNHSEMI4MViTLaZLOQCpcK-fU8YMJWG7kCTuyhOdHfhxGQRQ4ENlgg8tcwT3hRgkNIUqEDQ4LPCv2bNd3aSQc24m13CSVvDiHamlMLvUXNVV0hhoyqrSqI_zAIMML_4IqFSllGZAKzlOZFjmZ4_qiWhK2JKdVUYiyAinxmZLyMzoD7dTG5ar4DOhuXWmBc6VKORmPZ6ma12zEi8WYzyFfpPlM0XwWudZ44-kK_qhT_DytJVRTXuQScsRCVTVcHRlzoBpExoXPQx4b7ZUpnDeLEFyYBj53gziOrBAcCr6F0IMLnGrLikpp16ZZmgNa3kckm1LXdkLKXctiNPYYd0UEQWTHrTuddVNOS1ln6LCj7eRFlUhj8v7S6NRfGhjlopL6U3sbkilDyN8bJ53L5C36bHxET_qs0GFWdZKCHNMSvphoVq5MOKfZeLRWbbI6zZIxraiJ99IEcg6mmRUz2fydlkWaK6jkaJEYR_fKOKpUlbJaYaCnjMpUaoMgE1MqMQAKGnm1mheVdusszbVIuZQKFngnpwsd_033jlCA1JljTPI6y9BZPsfroMH6eNSjZWA66kVTXgFt9TR3eqNh6ljMFnZse64IGdiR44NnCc613kI1edcFlHQBJZha_KwBo8nPqtGkjei_dTaURZby5UDCMDsGQpq82zNxZCHUVCAqUJVV2uWnZPYEq9binufEkeA2t72YCiY8HsVxIFjseCgQPBu8wItZ7HqcerEfxzYLI99hke9r2YpqVy4RW_2_4VhOYFqR6QRvbXfiWBMv_JtlTSwL13Y446rA5S5EIRhXg6uXP0wqsqzgZ02Arq6ObqwqSFK1qqlXJeTHz8lJkcAX42NTqEnNb719rSK_vf1Hja3w_7ViGyP3KdjLNiz4jGW53LM9D5djW1bwRSNxWjOsJFNSAQSdx5BRdJT03uHa3oAkaSwr9ViBC7zyE9n-sFqW2lzd5NFaQ6dFb44IfKyQiD2UOW_nQBJQNM0gIVWdkwTHkM48DPSRFlYWkmZE5jgE5oVqry1K_aFaW4pdhm6YCQBJ4jJ7w8yXlkv---__IPryjNgkL6oFiuaQZZL8fGLZR-TEcp7cCd5PZGchd4DImecLDv4DW2eSv1fFV8jJguapwLKakPefRqNxRS_GCqXapppXAOYCqy8zsUfSLP0KiXkejz6vDc6Qd2xYG_DICf2G0Ayt9YfWSqWrj8xwpGhj3e0obn38DvxsbNyQUP_BLDLJm3Y55h6kJQJX6ZzMMSfTnCjM0U6q2AR49CE3yR3QiSCMbT-4nobB2lDnlkDrP95WEHcVtAXPUIShSEL_O5i5LScd8zMXlruRmf3SO4C1aYJ-RPSaxd74pRU1Vr8rdQLQBdFcFukE142b0BybDNRyK7C7Cmpyy9Mo-Nty1gWLM8a_g8Vmn514SXfC5kFZLxa0Wk70RRxQ520qv69LTGGkeyh32sm9DePISZxIiOvJGzfWnr52fSKLusI-r-fyUgMRbC_7bU_fgSA4dmAFvngoe8xuEiK-uL9QckI-DYhEWbn-rxy5YRIFk555ZEU-M3HEp9dhQyrDM5oubp3d16zomPSx_tr0l-YRwmCW5rlmCB-2DdUPBlFF86jEclG6kZPj02e_k4ZzEE2M6jYTjl8fj26b4fc365CBTS9IU-GkqFVZt_fSc92hkSSWtSQCpeLVA3wbDP77-7bbCD7AusHgv791-w93WeSfPv68y-IDfBvQhH2Qv3t4H2DXgCzc3659acEhxbmiDPvAuDMjOMDEAV146Cy-iw7ckMe3LD8kW9bEYh_49-ENh1i7JhV7dPK9SQPg9rmNQzs5xzcteHKE8_gA3wb0Y59I3EkLDhkwaxay70zfh3B8LfL2sKOCjC4Z5Hw-Pn3324vnJ9PXz968e_H2DUL-6b5-fRxQqUvjYr7csH8l44iszlJYUefJXVJ7AxD5oIMc6wA0iLufQd5xmtyiPDxcHB6xDQ8cLx_PUx7PUx7PUx7PUx7PUx7PUx7PU_5q5ym7v5bsX8t1Nk1s5-rm92_bXkE-yHtGi7sxtlMWAOXcEUKETsCEC3bgMjfmtoj9yHFpjPcY9aPYd8IoikRixZSif-w2h2564xhMfOuGN46rF_U_-BvHS2NO5Vy7xazIsmOPO82vCxoZA6LW5eaeVKvTgUnDQ5x0Dg3CXseAfXU6_ozjLd2DEHKoNPklT1-dIJPu4JP4CYj2Jtddh2bZEieFwpLSPx9pXkBCMiLaym500tmsgmYq921edsO2Mf_5U1So0gVep4tSK-80EQ1Lb42CDBagqiW2OSFSnmpeL4qqGdWiwSIBySsc5ek5kKZaZGtG1yOaX7JI3OxkxQXRyYJals3jOe5cyrYxKFhgrWEXReVVrvnBCkdykao54oZenOm9Ej65IO27ZYW6S8h1AmIQRjew1C7CgFXuuT6N3Jj1ER4Q1z6LDuOcnS6RxIwJywIvWGXsgIZ2ug5hkLsf2rWLn2ju9PZbhAfxwY68CoG53raZ3dpfbSGcOMFtJEp6jcnTxTHF0mrSZJU77W-l5Aatk7i6zZdNl3-5tZ6amM8hS0Y3TM2-M1g-d0A4iaBuj_OAQA9jug8D7jPHtXxsx47rM6vXMiDFq2gewGrftHHow3KvePzS9BYc0gKrSBH9CzBQTUTafqMqmrfVuQukIuIUOLcDLwnWjXBFrIeQHsiHO4VxwL3IdiwauyuFA4q8Y608zNHgevl966UV2ofGYmGSCO9HKhU7AqQPLGFo1yqJ17x-GNeHo-Odbiu0LcGiKEhg1Q4HDH0V4j_jzFHHL9HQLoYYbxTejnXXFG6X_es52wLDizrXYd2wetUDnBt7wOkN9GEV8Yui0pPPlFja8EVz0m44l1CZzctF0lDivvug7m-Zwe3Z4XrIfqLQpZ6zGo6DHckwO_bYU_SVbjuUxthE4zhZTeD1NmOVBt_9HBTBPmkga84rqS6hQ7WcvDh-_s_pb6_evXx6_Pr5s5Wermu1vpB_vHn18lBNfYY3I97svpkC-9hXMNc7gLbpDWbLeSprmh2qvZUiB78P7k0YzdUi-_TNVu0K__0P_UUJwQ)

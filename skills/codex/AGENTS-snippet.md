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

[//]: # (ob:6c0f813b)
   run `policy <file> portable` once; it remains sticky. Use `ingest <file>` for
   Git history not yet represented in the ledger.

[//]: # (ob:0ba00342)
2. Preserve carrier-native block anchors while editing: Markdown uses invisible

[//]: # (ob:0b96e11b)
   `ob` markers; static HTML uses `data-proofpress-id`. Then run `anchor <file>`
   and inspect inherited/new/gone IDs.

[//]: # (ob:55bb7174)
3. Write claims JSON with one honest item per touched or removed block. Do not

[//]: # (ob:3b3c1156)
   enumerate untouched blocks.

[//]: # (ob:311b1408)
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

[//]: # (ob:358e67a9)
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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzcwM2MzZmE5MjZhYmI1MTJlNzE5OTMzMiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImRmNjJjZWViIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9kZGIzZTVjNTQ2NmRjNDk2YWM0ZWE1YWIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhkZTU1ZDI2NDlmMjAzZTgyZjQxNzAwMyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNq1WduO29YV_ZVT5aEtKml4F6kYBlwncVw4dmBPWhSRIZ3LpkQPRTK8zFgwDPStP1DkE_phfSjQv-g6hxdxnBm18cwAhkciec5Z-7b2XtSHCS_rJOayXidqspwUxXphudKNeeQEXAjfdmhhR5HrOpPpROTqsFbJlqoaz1Y77vjB0pe2HbiCItuyLRKR5ShHOEEo3Njz8dkPLL6InYWwg4W0yXYd4QVEjnJ9O8IN7KuSSuaXVB4myw_6S72u-RYnZPS-xu2UC0rx9c9UJnHCRUqspMukSvKM7fB0Xh6YOLDvyzyPi5KqCmsKLi_4lrRJ1y6X-TuCsU2pN9zVdVEtz862Sb1rxFzm-zO5o2yfZNuaZ9vQtc6urS7ppybB53VTUbmWeVZRBk_UZUMfp5Mdce1CFQeOJBKT9sqaLs1DcC2tlRIu-dL3gkBJLwq49Ij7XD9b5GWtTVunSUZA3scjXYeKfF85gRfFjuVS6MSevbAstzWnQ7eWvKiaFAY7GqfMS1VNlj9-mHTHf5ggxnlZ6U_tbVJrAYf_OJG5oveTt7CgzwUd3IskTaszc-_sybOvX56_mVVZAiPq-V5Npr8qb3hdl4loagRsLXiVVNr3vMw0btxDOpHZsql3eakRXiSZ3rU64M4edzK-16FskU4nFRZir8kya9IUuOUO0aLWXpHm8kI_6_qWFC7H4whUrTNpOfndv3_--3_--fPvcbE7gitlzi50RtEVrjz6zWzGnsDQTLE6Z63tsJn962__YPWORnnG9M4lnMDivGRPO3T1oTB5x0s--Tg9IvJtLh1P-NcQHTdbspTUlkr2HS8vVH6VMQ4EVc3rRLJvTyH-4gv2_25z_t0LdpHlV-YZhhge8epkReJfg2xbTuDHvrp3yN_AX1xKKhD5KdsTz3B03KRDYVfa98O2ePpowQkX8ziiWDnOveP9IyHCxEglNYBiGaP3YB79ueblluopK5tslW2KA3I4c9mxMufFCcDKDm0pA7p3wPacvUZA2Y2ADqzI00Qe2KM4SenxZs6exya1Na8xfsSbwsZreANpxaHtinvHy5h2IOCOgbGeFDcszyR9yZIaCbLnCdIDzpcXhzn7oaIT_rUEB1N6958Qzhw1R3DXJTHJyzKhcpZhGb6as7GRBJlV7GoHS_rEWZqDTvjXElFAtv0g_t3kYsP2WEhl9eU1RkDYK7ZRvOazY5rMEoXEOEc_PMVpvhALe-HdO153zv5SJjWcm_JkX7E_vXn1kl2hTyMTiCGj0TSQDrRnBbav8waNW2meKE3DuM2_rnAxrvjBQ_iXsmZPJQfmJusBmXOr-QkPuoi27VnhvSPy5uxNhqFgl9et4zaz2dXusJl2Lp2aneh9gYJDXbXjwfJUboax5_rkPUhubjbVbpXh0818VfWWdMQwm-ndmJ7wBsB6OrgGWPiOTRi4HgLwqz18Bo-WpOdJUhsEPdUjgaZRpZlXlJoCUHAYcMADKRKjnLOXJ1JBqoVDInTvHa-PZqDJ9VIP0APrm-UlaY5FJVUsb-qiqRkeEthyD6yYHctTxeSHFCx49BD-RbuVxLYlUXaqeoQMQ8df0MMMKBlLMogC3eW1y9oy4mhSxwMG6dJTKxPNCbyeCl0MKPxB8OrT0pTSoW1iPi0SUHvedvcKUzTr5_YpuyAq2PUQ_7J_hhQTD--fnb4BUgGNxjYQLnVTosV3qgUEnx7YZiRSNqbxS55lIABMr5_ifTvtVc4E1ujpcS1L4q2oMHd6kXJSgWF3s2fvvE6IMRC5vCjyJKuNrizNSVp59N-08HirFZweXUY7jFXdaBOjFz9T8FV5XK9jJCSVRZl0urIS9jLkZPtOJILIXXgLP7aVWIhIxb4Tc38RBpEUlu3EkbNwYxlDgDsW9oxFFEslbakDrMNm9GEbraUdQlrpKxMHMmBmLWZOcG4tlp67dKI_WNbSsrCq8_hY-H4cXf3wYKKyba1G8-14tdM056hQ2GT5nq2RmT1GMrDL3rvpO91yEPE5OtDjG-qmQ8J5HLpRhLg51CMZyb8OyV10m3FTdbN660BEtnIpDv1AirgHMRJ0HYi7KLERplU2gIIfM00rrMobTeI63Lgm07wiODhBL8zzYs6-ypku6KG16zWHFQg309nD9dsCnjJww40doDMydhxp2eRGJAcjRyqwM_JO8u3AOopiut0bViqNUe8xLVOcJttdfVRS5zBwlRWdNqhw1oHtmj2OVGi-mLNwiVWk7cCk2NWJ6Szov2zb6FcbgKUbcvs-BC5fZaCzKs_acXx5uzcsZQkvFsIhV_beGEnMzht30YbVRWWKoWWvJE3qw_SGEaHH40gvXEjbddUQnZGE7PDcRfuxjSbDagiABmfmyGd4vn85qNPsQHq9iQv6mEJnN1a1RXciwcjxwsBzQCqW6k0YqcrOhLvIQVNXRoIlmS65tnPc4lGHPC5i21G-Fx7hDKLx6NHPVnttLFq8vVeNRzUfwfsF5l383ZGWZ-oso6uzrdZkz7-qTrhROYq80IqVK4bMHInHDvddVB-msE5v9dRyuxf5IraF9EPImYGfR9Lw6MVfp-n6PoSGtSA0UUeJYfejzOt2vzd9NngY85QlyLUCPmTGUbKNMuOztVZW40vHSoYA2WplNmK4jk1UI0nNxKG7OdDl6Npoweit8My8FWafvhPGQ3ooY6vJo_YVb5pvH68m4026RHnU_p2_A0tqxHCkXgWnNVy3Ms2en6zslZvZXb_K_6mBgQkeH8s3PRQMy81auO8GzdkFwQtV5LiBFUs5lOdIhh6D8Nn60XTWJIv1_5hLynxvUEleaUu1HGnMy3FdFX3fKvmVjvG-qKszzDNZJcsEn0-kcORbEY_QVH1Tnu0odZSnnR130ZV4YjZk2rsGdV3ntye3TwvXi-NQeqZA25I6ys-jX_-HbuxJ3fWlpXgAAnCHMB2l5Hg0-kwNWIOAMOdIxOTpi-fTFXpOmh77qNEzuk1U7PL2X7WmDN65MqvajX-L0QI6KM8SvXH3Yxb74fWLlizQndFgCM9rctRkXUNmjbFuOu-vMt110pwb9qT3JBvUWVIPg8jAO92vXMMYAGsYSpVf8iTVoPvJqesMGybaWQsipxuwdrolmh-nDMha95hNstf5sTkRIy7sSLqhshCVPkYj-TyK0efq3gNsT7aJnjJNyho7QPdbmhUpAn_-5PWzr89BFbrK2NNX3_91Pp_DgxAPqeazfYF81se1Lb77FWpqwoBzV5kJtZGzXGintkUByqkwyGS6IcO7GCAxNE87v7R9d2NwI2B5qrtaN6OusivTHFuIJaXtgNG3C9O3zb1bkLe520cWE7tpKWctvbUZ1JXypput2pM6gYrOpAep9iK-XGnAvVt1-19lw2B4lM8VOCmOT45YkSd9341ELLg4dq7hxUMf6Tu8MbjqZulqlxSjeRrp-QtYbz_i338BZlZkIA)

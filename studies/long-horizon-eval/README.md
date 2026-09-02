[//]: # (ob:98f84bc3)
# Proofpress long-horizon handoff study

[//]: # (ob:967ea7df)
## Start here

[//]: # (ob:36d076ff)
This directory contains a frozen, bounded evaluation of governed agent handoffs. It is organized for two different readers: people evaluating the reported result, and engineers or researchers inspecting how that result was produced.

[//]: # (ob:bd9aa239)
Read the public-facing material in this order:

[//]: # (ob:9b0e173b)
1. [Public result](relaybench/PUBLIC_RESULTS.md) — the one-page descriptive result.
2. [Claim boundaries](relaybench/CLAIM_BOUNDARIES.md) — what the result does and does not establish.
3. [Publication copy](relaybench/PUBLICATION_COPY.md) — bounded language for communicating the result.
4. [Result visual](relaybench/visuals/proofpress-results.html) — the corresponding communication artifact.

[//]: # (ob:80ee0a4f)
## What this study is

[//]: # (ob:53e0aa1d)
The frozen panel contains seven models, three Proofpress-composed Harvey LAB-derived legal task families, and 126 valid paired runs. Within that panel, ordinary handoff completed 10,654/11,928 rubric criteria (89.3%) and the governed condition completed 11,141/11,928 (93.4%). In 63 controlled stress pairs, observed unsafe propagation was 8 events in the ordinary condition and 0 in the governed condition.

[//]: # (ob:e1fd3af0)
These are descriptive, bounded findings. They are not official Harvey leaderboard results, a population-level causal estimate, or a claim about production customer outcomes. The exact limits are in [Claim boundaries](relaybench/CLAIM_BOUNDARIES.md).

[//]: # (ob:f2f5515f)
## How the repository is organized

[//]: # (ob:2d89c2e8)
| Need | Canonical location | Why it exists |
| --- | --- | --- |
| Read the public conclusion | [`relaybench/PUBLIC_RESULTS.md`](relaybench/PUBLIC_RESULTS.md) | Human-readable, bounded synthesis. |
| Check allowed claims | [`relaybench/CLAIM_BOUNDARIES.md`](relaybench/CLAIM_BOUNDARIES.md) | Separates evidence from overreach. |
| Communicate the result | [`relaybench/PUBLICATION_COPY.md`](relaybench/PUBLICATION_COPY.md) and [`relaybench/visuals/`](relaybench/visuals/) | Reusable public wording and visual. |
| Re-run or inspect mechanics | [`relaybench/README.md`](relaybench/README.md) and [`relaybench/bench/`](relaybench/bench/) | Execution harness, fixtures, scoring, and checks. |
| Inspect frozen outcomes | [`relaybench/results/`](relaybench/results/) | Immutable per-model results and retained invalid attempts. |
| Audit evidence and lifecycle | [`ara/`](ara/) | Agent-Native Research Artifact, evidence index, receipts, and claim register. |

[//]: # (ob:be9112fa)
## Retention and change policy

[//]: # (ob:505342d7)
The existing folder names are intentionally retained: they are cited by receipts, ARA records, and historical evaluation materials. Do not rename, move, or overwrite frozen result files merely to improve presentation. New public summaries should link here; new experiments must use a separately preregistered study directory.

[//]: # (ob:a1e3ae22)
## Product meaning

[//]: # (ob:a2e157c7)
This study is implementation evidence for a bounded mechanism: governed context can make downstream reliance inspectable and can constrain unsupported propagation under the specified conditions. It does not replace design-partner evidence, establish general performance claims, or admit a conclusion without configured policy and authorized human review.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzEwMmM0Y2I2NWU0OGM1MzhkOWYyNWVhOSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImZhNzQyMzIyIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85N2RjOWVjZTY1MDRiNmUwZmViNzE0YWYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzlkZjBhZjZkMGMwMzBkNTVlODc3Y2RmOCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNq1WX9v20YS_SoLFQVanGTzhyiRur_cNEANpGngpFcc0kBZ7s5KPFMkyx921DjAfYj7hPdJ7s2SFKnEkFu7BwSOTO3OzM68efOW_jiRZZ0Yqep1oierSVGsXcdTcxUvApqHKvBDHRkvIBlNppM41_u1TjZU1VhbbaUXLFYL5fu-1Ip87S6MDpzAhAtHm7n2lImkksqQE5CeS-PreL7w5lobN15QIKPAXWrY1Uml8hsq95PVR_6lXtdyAw-prNnVFB9iSvHgH1QmJpFxSqKkm6RK8kxssT4v9yLei1dlnpuipKrCnkKqa7khPtTR4zL_F-G4TckGt3VdVKvz801Sb5v4TOW7c7WlbJdkm1pmm9B3zo92l_Rbk-DzuqmoXKs8qyhDLuqyoU_TyZYkJ9HI5dzzPW_SPlnTjV2E5NI6WmoVkaJF4MyRA8dQvHSRGo4sL2s-2jpNMkLkfUXSdaSNI81CO8rxHR0EFC6XSpuwPU4X3VrJompSHNjjOFVe6mqyevtx0rn_OEGV87LiT-3XpNcxUv520mTXWX6bTd7hDD0euMB1oxOqztM828y2eZn8nmczupHp-dXzi-9_fH624-L9GQDJui6TuKlRt3Usq6RiL5SatayQz5qsvaaGL47yOsnYZLWvatrhm0zuuJx9tFNsrRgCk1XWpCliV1vUjNpTx2murrE6Ck04j5WP5ShXTR_4ZANQxPhwAvt1bozgk--xo4tAam1DKxh0dIsnX4k_aqLeFxw0AwGgmnyajkJbLEkutTkK7XWNhIotlXTS_1fiaOEJLz5ws1yYx3h5g94SGnhXtsN4u0yySkhhyvx3yqYizpsMuwSjopFcV5EbsUEzD0EVspRHEcU6ktLzo0dEdIUDinpLomjiNFEzAA_nFTsQRZnIVCQZvkXQjO5ydSKGKHbIXfrxI2Jwz8TbV9Y9SAgdV7_7pqRU7mPK1Pb81c_fvbh8tr56_vrnF29eo0W-Ff_9939szHlGs2KIKQVxHcUUOkSOnB9X6petrNszWUSJpHoAF_duOIGPwIdT6eoneH2Dw7WIEIXMKB2QUjH5iF2uKa2mMFgSjTpnBr49USNyjfalcZ4WWUVCliQ0VapMijq5oQG2BvuQj-pMYOHersvyGhA2iUpORGY8EwRucFypH_JbW-aSirxKbMdYJG5klvxu4zpVtod3n6ihp8NIeRT-VfHciZeE9NyJZzLLs0Shs-Cp7e87IAyWakEfAOBK3P2a3YnZbCb6n0Oodpwdtz5FrusZeRToFdWYUGwb3ClaEhdFjgbbP5C00ztPgd4J_Lmnl39FHIx-mwtmIpOnYB7Bo6qyeEqyzqhM0z1qwX1BesWVAeBOYEy65EuyKuJocOlG1WJHKCLOdDo9X64-kRLpkRss1fKx_t6Me1IkuyKlHU7eggaLNOgRNJGXGB99_-2IszxmqDYN76a9aplAFvKMX6uSZCsQ7De92jipqNDL1mYnrEQnrFBaUtdFjtJYnVhaT6wh-t9YQrxjRWZrP1gYq7SREav_HingqtzUa_DQhsqiTDqdWMXuijw_RquQjj0nNpEXQkTHvtYhzb3lwsV33nwBKx4eLkIfSfCM75Prg5dYYbNtZN_qvbZaK3cOkcRPJp7jLWZONHO8N0648sKV6_7NcVYOc22X8bGQ_TR6-vH_KxEtHFsJt5XVFuuRNkeZ0Pf1kvvF2hipug6pT1JknSdfBzIMkGgTOwdPg0jrPT2svTp72g9D8pVaat_09kZyrLP3FJVVgksEoJbV_TExyy7rI6K3PVff5vBhDDG8QUMSLFWtREE5-vRgGATWTwxW452-mVo-pGwDWGMXLPMXJEu0AH5FrAVi581bO3Jk3W0Ut7IShaUQ0mf3cF2Xp3mkXSeOtJZzr8_TSCQe6PmJ2q_z5nqa3PlcmYXvHqo8yMHO29NUHrPMSHF0Js5-zTyYfZbKZNcWVZboniPLz15cXP64_u6nn19-f3F1-XywfdsKn96W0DlPGBTGfmDZgrsy6CeptvDjH8Jv8aLyYn_PCS7eXP70cv3sp1f_PPjpwZZi_DV8DoYPhNquyayxA0a6E83h6aoNCTfyRqZHbtpH1egWPWt3VmfbepcOacOFFF8UuRVkY388jjv-OLtHPPetGxizjChaRN68L-pITw-t-0flcWc38vxFFFMQGvumwtodKeZDCz9eAEOcIds_yPIGguDFxXczoBeQQQFoA1TXsroWRu6SFEhpO9H1FgINm2g4A22gTZsMbf9LgmNlbf_ZKKbcCkkmQSo9B7K_lLi1XWe6CObnrjvFaIGFuATSgVfbTOKbMDrzv_7WuuPqHLhGcYE6RB1MuVN37vamvon8s_nX34KGMrHwbSbKPE2xrqotOXPQOEke48rP50Tw0hDzBNqmLTjzRijsoK_avqbhLEMIHJ3Tf_9liCcYx7gRLcxSkZHUl3V03RjK-ujbA0rX1TS1ZBvnsuwJlesIYVk0qT3uLMVJgRnZVNiFLk6Y07h6WKYsWUj4rDsqbbPfVHW-g9LEc1SC2iCgQ9Em0Dm7pO7l5yP45kTiHNdXofHlnBzVJ250Gxr67FH3mc4JBi6UqJZhHAe9k9EVp3PypEuK_ckPP5sqjB6VNlVr5O37U5z__qGRcCd-aHYym_G4ZWE4QKfaZ_BZJSibjeIZi0mBK0J-ywjmglWf-7-nUu8fHh134jVxEWsMiUGFl_lOcL8gMrXtYzhwLo3nzL1ZOJob7x8eLNypR2b6ufD-3mnBYV8R2oFVe1eYW0sAG2uqXXfWV3AGAuRu6ZRIf61QX6TwIEqP3R4e3xNo-_N4ffuTg3z-gZR9nQmGBflU6GyTfKibkrm6wkxDxNPuOokK9-W-7ALtZkbfw5-H27HFZ977p-z_EiVr7zYFlTM7ZnqOsV77-yZS004MWde0K-o-kAvI93rABW9JE0Nqr2CSowFy2D3_x_4uWGrOXkoraq46ESguuvk8HSyBGunDFP4VgTa7wdVyWUkb9CSVCOG-VwX9QDcB6cBxZDSPD5pweHswEM2ffgfQOYjnrvIDx4u95UExjF4LjCb7Yy_3WKASHpDxfpSIi6sL0b2eb7PS_gHD8tdI4PeyFpX6PrdzBcodjqcQEzftcOAGvuWJ3eOo61iTpIgPw4EQVJ3zXbzEWsGSo7-Rn4E8b_vWqprdzk4GUW3zJmUMZNf2evN3kWEZfQC6kp2dxjsMHtHwWIS2aYkFXmC6L6sd9KysDleaE-PEd7VLrrOMnOBw4xq9-Biq_IdeZXRGQ0AnDDX0vOcfjA5vN8bXrke-r9itjuQGW8T45qJdQyvktxlLHclQTxPZtoNteNupFqaSBRQvA2JYATVFd-UayyB2Wlou5t2JScbqpr3oHcQ_5mwqlVUqySbDDaSsM2zuDzIdbgcCPUwl0Iai4ng7G2A7clrNoaEeWHkMk_AW0pIFCB6ZZNNwjdsOs4dp_2Jjr5pbnneifSf0RdnffcK__wGWXqIC)

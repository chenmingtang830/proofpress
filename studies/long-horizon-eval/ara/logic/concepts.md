[//]: # (ob:8dc2492f)
# Concepts

[//]: # (ob:fdb16762)
## Ordinary handoff

[//]: # (ob:5e5b2b11)
- **Definition**: A portable summary or artifact passed to the S4 receiver without Proofpress ledger state or deterministic current-state blocking.
- **Not equivalent to**: An unstructured raw transcript; the baseline is intentionally strong and portable.

[//]: # (ob:676ce865)
## Governed knowledge ledger

[//]: # (ob:dfaf11f1)
- **Definition**: An append-only representation binding proposed conclusions to evidence, artifact versions, scope, policy evaluation, admission state, supersession, and receipts.
- **Not equivalent to**: A claim that the admitted conclusion is legally correct.

[//]: # (ob:730c76ec)
## Verified handoff

[//]: # (ob:655ede9b)
- **Definition**: A receiver handoff assembled from current admitted ledger state whose evidence and receipt digests verify against the frozen protocol.
- **Not equivalent to**: A cryptographic identity proof or independent legal review.

[//]: # (ob:3377dfb4)
## Cold boundary

[//]: # (ob:84d24d9d)
- **Definition**: The S3-to-S4 transition where a fresh worker receives only the condition-specific handoff and permitted post-boundary materials; sender state is frozen before branching.

[//]: # (ob:0d8b2a28)
## Trust stress fixture

[//]: # (ob:e1bb26e8)
- **Definition**: A preregistered, byte-matched perturbation that introduces stale, unsupported, or revoked state at the cold boundary while preserving task, source, and artifact parity between conditions.

[//]: # (ob:61467ea3)
## Unsafe propagation

[//]: # (ob:24e3944d)
- **Definition**: The S4 deliverable relies on the injected state in the prohibited manner defined by the fixture-specific deterministic endpoint.

[//]: # (ob:3d254710)
## Admitted paired run

[//]: # (ob:76055810)
- **Definition**: A Raw/Proofpress condition pair that satisfies model/provider identity, cap parity, parser validity, transport completion, evaluator completion, and frozen-protocol checks.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2EwMzUwNGFlMWI5MzdhZTFjY2Q2MmRiZCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImUyOWUxMjFkIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV83NDgxNDY2OWNlMDNhNWE4NDBlYjcxYzMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2I1NjQ0ZDdjZDZkOTc3NWIyYjc5MzFkZCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWm1v47gR_iuE99vWTiTq3fdp0QL91h72rv1yXRh8GdlqZFFHUsn6gvz3DvViy4mt-JLg0hYBFhtbEofkM8_MPBz5fsa0LXIm7KqQs-WsrlfMCyIvZODzLEjwjxAyppLL2XzGldytZLEGY_FZs2E0ipce9_0YggA4zTwa0iSNvDzkkQiihPE89PIg8UOPpZJFaUZpQnFAGIYBS_3Qp4B2ZWGEugW9my3v3Re7smyNM5TMuqnm-IFDiRf-CbrIC8ZLIBpuC1OoimzweaV3hO_Ij1qpvNZgDI6pmbhha3CbOrqs1b8Bt9toZ3BjbW2W19frwm4afiXU9lpsoNoW1dqyap0G3vXRaA2_NgV-XjUG9EqoykCFWFjdwMN8tgHmQASagU99h5i7soLb9iEEF1ZJiLuO40yAF7CIpaEHPPFF4FamtHVbW5VFBbjywSPlikdxGMoEHSGzJIk45UkW-FJ22-lXtxKsNk2JG6ZunUJpaWbLX-5n_fT3M_Sy0sZ96m6DXHGE_JdZU91U6q6afcM9DHxwDraNLMBcl6paLzZKF7-pagG3rLxmmuHVdSGuEQIBtTVXW7ea30MmZq0ueGPRhyvOTGHcjFDmK2YQWwvtM43Fed2Kb4rKmTQ7Y2GLdyq2da4dVj7HocbRYbasmrLEfYgN-g86BHipxA0-nUpBw4zm-Diu28J3t8s_9zvAi_0kTErosEWOwR1e-URGT9ld7aZ2rkWazB6-zQeIZ8hht4iV0MC6HbR3BjhglScRDSRkXMg0CikPQfjME8ztSNmWrD0LSM8CgnwUN7UqKtuSWrczuU0O39wevzn6lIXYjSyMKTUy0pL1hWwzKrerHHcNutZFT2rD_aUnMcBFLPOACaA0goylEGAyCCESvvAxRUhf8jTwM8YilxnSMEwhZRmTSdB6xFhmW3J28C99dKK7MKMejRdeuqDxzz5dRsmSRn_yvKXn4aAecBd0AiImOJ09jK7e_3F0bjnW0W3DzAaf99MkF5gAo0j6-EBrY8TAnn7T1Hp4mJ8MYJCF3Ycveq-yS6EkfJ99a1OCbMS5u49C_8ndXxtMufvbm2bLqqUuMJq0dBnxfyBHtGt-aYrIJffjJKZHKeLvGt3BsMbgAKnyfDJVfCInHn_s2PlhxghciPn-i2dckM-f_wIYlYXD6fPnJflC9lnENNuts6M0GYAntUNPEquIPSytxDJ6tC5EQUAaR0fr-qsr0xUOdpiWIDE_tf_rZyCZGjeBjcxZ7vu5__o1nACpIgxTciUXqip3qCdcFcVgYO4BwtEQroZgMNUTICWBJ5IYxNECO5WCC7yMLicen4AkjiJwBeTFM56iCyYFKBDVYTxxDNkifyTJtdoS0WhXacgEEkGQJDLn4aPaWkrCVVNJ5OAzMDx-dgKDNJQ0lJl82VxPAfh5A-SnYGHV4qeQWM0q094idxvQQBhiAGZD7pS-mQDAkymnjKZHi_pZN8YSY51AI3nx3TYansHhzJAJODBzchrD62Y-mUU07n-NG8U_co4K28JiyyyKCUlqzL-N5m20TGURVLsJsOBobf-oDMuhjS22HixMYXJywAQiNIQgQxHzilnPsCQkEkoXKv0hpMTiR5AqFm8WlTtZIDZTYSJpFCa-d7SyL3JbWDewZni4kEQ3zwFyesQEIknsRVH6unlPUeQru7s-HLsI2pZd7DiTiApDDiLW5jEkqDVEyYrt2er7aBW9Ov4ipSF1w1Hqth5crDWTQL58_ULabaGWIacq8JmC-_JJXlN0Ox7tc-4dnj1VY0en176eESeJwVmRgCGIh1KErhBDNl50t3l5rmy_CsLzVfZMgX5TLC-uzcqB6gRm2ThtZxzAyFcJKDnnB_T7E4GZEyNUjXe60xJxSrVpreLDGA3mXHV_FZZPyvOZgv62dLy0qLMhCxyx7m6D0O6hJGiiM1hb0nWAjAO1yHcEk2lRYa1xvEbDv52TBa-C8Li6nxEDb4nf5ZoAIeuhdpUA6eqA2CfChalBoPfFwQ1VWz2H1KuMXQwbI1hd4ZyqeBV-J-XAGRHxxlnxQhHRFYuist3x1TgelhipTWWa2qVWN1o5rG_VDY7taMpsD_eIHuijooRzMuRVMJ7QEGd0x5tz8SLl0YFSdFdxlZuCu0YB8qqqwNURNItfeUfSngcHih7XGcy_57TLq0A8JTvOaJW3peKlYiV30G4V4u26vy4FauLyoC3sbk4Eq3GAbj_jX4M3sYoUsr3QZgrHVrS-rUtoS0sndwbZdT-72-zaA8u2Rp7u8yZU5Mev5FMQEddU2blQUJhoTu-TXsWH6jYoiLah4Sojbq8pMUNjuBSV6x65i12jHE2V7j4wLTZuuRhqV65pdnEPc6KF3fln3Jwcd-bGDcv7j-7LR_flo_vy0X356L58dF8-ui9_fPfl8heTT17MhQ-nX7w99xLyTd40ZjRPeBZkEctlSjMax3GSedILmcg8EeQZXpVpRkWesiiJshQthkC5YD5NRRKc29CTV43B0guXYXjqVePwfv__6VXj_GAsB5EIKqiXssHYSJgNxi5VWr1VrNM04XES4F4GqyPx1Vv9b2qrIci4h6t_VW5Rf1OWuN9-oA9dKbaqFzF4OrW6ES6_YwSzu66ACV3U9od2SZwZcMQnhXGK3mlxVbESNQ8ORHp07YB-i1cnclePX0DzOBdIO6-t8i1-I5F48MrvFHuD07MoSHgoMORhMD_Sf-fd826duvbHP62v8NEGC2L_enc-7lWZSfeRtgXd5Unnq30n7LBM57YS1q3DhEKCCDvhJAy_gEImJWV7ko9E6sFJl6nOvev9IPYwVvxwb3UkRCdC571agHiURZdbJVT5jAP0rrYKj7X1BiNwOGOT9ldN3elVgmOXG9O6gXT1cMIHuRejG8JcQrAPlJE8PvjgAsnbm_Q4516UJann8316Pajgsw54vx6iLlhpfiDGQTe4E5nc-4ZDrnABHFckNi7HTaQdCCLuCe5jQR22PtLaBzQvF8695QyiLJIBphixLzMjLT1VEN6po0ja3KZvXUazzNxg3lGNbrMXumNUklxvCEG2d4Bg771oJmCWaegziNMs48E-xA_i_QDzpVq8tyuyIE5FiOonkYPdkTyfZu67dBzbH6lNIMXyLAeeonAQ-2Q4kvUHpC4W6UPeoEnEeAJBKug-dx90-wQf36utONREpPD4qiNjF-iLIQl3PyJ8SsBvD_jvP4HEoGg)

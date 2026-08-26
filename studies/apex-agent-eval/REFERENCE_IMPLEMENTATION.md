[//]: # (ob:57147f33)
# APEX Legal Agent Reference Implementation

[//]: # (ob:f9c47b53)
## Purpose

[//]: # (ob:60065b2c)
The canonical study record lives in this directory. A separate private companion repository preserves the runnable Athena-shaped application used to exercise the same two-task APEX workflow. Access to that repository is a collaborator handoff, not part of the public evidence package:

[//]: # (ob:3b7ccf66)
- repository: [`chenmingtang830/athena-apex-proofpress`](https://github.com/chenmingtang830/athena-apex-proofpress)
- pinned commit: `38bd855daf5e0da3b505f5579fc9e0a52b5cbdb2`
- default branch: `main`
- access: repository collaborators only

[//]: # (ob:23104ba1)
The commit pin, not the moving branch name, identifies the referenced implementation. Authorized collaborators can reproduce the exact source snapshot with:

[//]: # (ob:f7ec7c44)
```sh
git clone git@github.com:chenmingtang830/athena-apex-proofpress.git
cd athena-apex-proofpress
git checkout 38bd855daf5e0da3b505f5579fc9e0a52b5cbdb2
pnpm install
pnpm check
pnpm build
```

[//]: # (ob:0e711f8a)
Corpus-dependent commands additionally require the locally licensed World425 data and provider configuration described in the companion repository. Neither is supplied by this repository.

[//]: # (ob:303ed286)
## Repository boundary

[//]: # (ob:f9bd9413)
This study package and the companion application serve different purposes:

[//]: # (ob:4953d702)
| Location | Authority | Contents |
| --- | --- | --- |
| This directory | Canonical study evidence | Frozen manifests, ARA, aggregate results, claim receipts, validation reports, denominators, exclusions, and study boundaries |
| Companion repository | Runnable reference application | Athena review UI, end-to-end orchestration, local runbooks, deterministic retrieval implementation, document generation, and demo-specific tests |
| Local licensed workspace | Restricted runtime input | The 93-file APEX World425 data room, credentials, transient runtime state, and heavyweight generated outputs |

[//]: # (ob:4bd3ee86)
The companion UI is an application-shaped adaptation, not the Proofpress core source and not evidence of an Athena production architecture. Reusable ledger, claim-relation, Legal profile, retrieval-receipt, and TRACE-import mechanisms are maintained in the Proofpress product source.

[//]: # (ob:6c1ef20f)
## Evidence sufficiency rule

[//]: # (ob:95285082)
The production repository retains the smallest evidence package sufficient to inspect the study claims and recompute its published summaries. It does not duplicate every generated artifact.

[//]: # (ob:d7898f6f)
Included here:

[//]: # (ob:4920330c)
- the paper and ARA lifecycle reports;
- the two frozen final evaluation manifests;
- structured result tables and the raw result records required by those tables;
- content-addressed claim receipts and validation outputs;
- explicit denominators, exclusions, and study limitations.

[//]: # (ob:77c794a3)
Retained only in the companion or licensed workspace:

[//]: # (ob:95949756)
- the full Next.js reference application and Athena-shaped review UI;
- raw data-room documents and derived source previews;
- generated DOCX files and render-contact sheets beyond representative study evidence;
- raw model transcripts, scratchpads, prompts, caches, and transient projections;
- credentials, provider configuration, and machine-local paths.

[//]: # (ob:1b1cd164)
[`ARTIFACT_INDEX.json`](ARTIFACT_INDEX.json) makes this boundary machine-readable and binds the companion documentation to the pinned commit with SHA-256 digests.

[//]: # (ob:8304869c)
## Interpretation boundary

[//]: # (ob:04cebd54)
The reference implementation demonstrates a bounded workflow from one APEX world through task decomposition, deterministic retrieval, evidence-bound candidate claims, policy recommendation, staging, execution gating, drafting, and evaluation. It does not establish official APEX Pass@1, general legal correctness, production readiness, customer validation, or human admission of the staged candidates.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzM4ZDg5NzBhNDU5MTI0ZWJlZDAwMDQ0NSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjE0ZDA0MjVhIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8yNWE4M2QwNTQ1NWUzNzVhY2U0YWExMzgiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2EwYzU5MjQwMTNiNjE0NjY5YzVmN2EzNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWmtvG7kV_SuE-qWLSs68H-qXNbJe1MBuNnDddoEkkDkkx5r1aGZ2Hna8Sf57z-U85SiKbaUFWuiLPaKG5OV9nHvupT7MeFknMRf1KpGz5awoVnYgg9A3uOOGpuWoSEnDMBzHnc1nUS7vVzK5VlWNd6s1t1xv6QnX85zIxTxfxZbBhYr8MA64ssOQB1bkcd93fD-I_cgKg1DYfhQbylSm70ShaWNdmVQiv1Xl_Wz5gT7Uq5pfY4eU17TVHA-RSjHwT1UmccKjVLFS3SZVkmdsjffz8p5F9-x1medxUaqqwpyCixt-rehQW8Nl_pvCcZuSFlzXdVEtX7y4Tup1E52IfPNCrFW2SbLrmmfXgW282Jpdqt-bBM-rplLlSuRZpTLooi4b9Wk-WytOSjQdaTiWy2ftyErd6pegXLXCcGBLw3VcV9m-C2U5nJt2QJLlZU1HW6VJpiB5b5F0xQ3hhpZjmHbkmY7nhcKNfW777XE66VaCF1WT4sAWySnyUlaz5ZsPs277DzNYOS8remq_VnIVQeVvZk12k-V32ewdztD7Axm4bmSiqhe8UO8XECirF-qWpy8uzn48uzh79fJsdf7z65_Ofj57dXl6ef7Lq5ONnM2f5FC8rsskamrYcRXxKqloV5XGK15Bv7XS6zX1Oi9J6pskoyWr-6pWG3yT8Q2Zt5d-jqkVucRsmTVpirOINWyoWi1EaS5u8Lbrm44f2-R2MF-t3tNJT1-f_cp-Utc8Zad0TnahYlWqTCh2vilStcEYh5SY1AnBpdTSFeSH6g4jf2KPXYVEre8Lkp38A742-zQfJYxD4fiIpy0JXzdlkVdqrwB_YuNbe9b3DMNzI0s8df3LtWKCZ3mWCJyQnOOetY7E0uRWVSzJWI1oZBIRQq52f8JOWaUKXvJRIv1pKo4d-ULEnvdUcRbYHO8ktNGSvbl6GLe8xgBfaOcdo-Tq3Z8R86M4KdBjSxzLNg0n4uaztJNvNknNiiSbsyyvoQ3FNvkthGJRyTOxZuSyc5ZIeAKADDqjV8o92ol9JXzhOE8V5-rqqlq_zYBrTKR5phievh9RbrlXW6M8IpdqSx5D-aYJcH-qPC_zsmiqhVSFyuj0Wlc8kxXDuwkFBU9T8ieNr1ot2FGPpfucx7CVtIJt57kY_IJFeZNJjsSyP252z9gbo5EMHdM-ZN9LipU2jLpcxaAQfXQop-AZZTcO_Ee8kYIQSuWtQnTFsdqjEid0bekb1iGifWQ_5d2mH9mpBuCkvsfzS1oxqyv28W32kS0WC7b1lwYv16NwOp9tSxdJW6nDDHa5paF_nDPokW-pagFuUigJ3-JFC7l9QO5RnCdM4i_xlmhntxSsQPCqieNEJHiGl1Ka3e9R--bt8avQtQLXCKzDZSAlAfZkI7QZR6zEY82TrIWeaoMQA8diqt-DXHGPkqQfhEHsfQMlnWcibTDI1siRy70ObRm2bYjDt1zoMxdwjVKH2unFKVJXrMS90IySGFj117dZ-159l7O4zP9QGYuTjO_JGb4v_NDh9uESXmjbQCl5BuTTCXXq63kJeYUC65TsLi9vKlhrr-5CN3RC3_W-le5iECv2Csuc_FZBYT29maKUVmybTbooLPeozoxMIU3POVzAN1enF5fnP56-vFydv_rh7FdImGdI9ztGv2MbfqOTL5CDEGePBpEcnQCMe0vAczyUBQWSPvIjs8yXZ-1BBMNBPSVd59D9CQ9GgyVbfJRJtUEpU5dUbzHerte5WJzmdw_V827eFxUzVG1EuVeiVLzl6_qbnvyrlR95kXADIzB9HvAQEBvGJvfIlEBkvWZX97Cu7mHgJuKmyJOs1mVcqXciSt9_Ikb_jgomON39ZIVpETVZRJdnz6yvqjyuVwj_a9J30pVxVWQuAw81rGd6BjcsL5JWGDuOEVO0ORz_fMM3bWG4MuKuH9rctgPTiqRSIg5cK9LFYQXt63KstdbSMlCz0MjMwpoLI1hY3qVlL01nadl_MYylYWBWp3EiIdzz7dgW8Jdx9MN_t4LTbtpWWGtercn1DBMExZGmH0Z4Qa8xKbo6Dz64Wup2s7jvWNKPhRUZ_W6TAqrf7SulUbdYKF1piCgORCj7xSbVUrfYIXVQTUk5uaX_I6pPcjPVKMTyusKgyTIdGdt4OkXbhlJBnTP1XpUiqVrmXKHKoPS1qHl10yq6D-VdyaI3HDzaCWFenLc__aQ4605_SNn1tVbL7rnfUUJGTUVpsa2wluzKDiIZuK7ksasMye3INdzYRajFIlQGpxATkYysK5osVcybtO6KMMzeIMnqb7gQ2GE5NYHI05RHOWyVl5XOwzvSV6cyxw4MX7mcu9HgMJMCcuowzywN-5iQDyD7pKflf2itTEWGb9J5NPdr_UG9RzSzKm9KyqkZL6o1RLiDIfa4gxtEcexxGwWfGiJrrEa7sx1UZw4mPsGMt5mAa-_8ulufED1vavZY27_NiqzYIBwBtGnafdKrdM9Rk6TybYYz7Kh4R0wIvEAALOQAMJMiuFPDIeVtT-j-lZepdCyXSV5zTaOgAWJCJVbL4uS6KftsXYkyicgnHhLE0Y9PQNNgBkymKrMhyMCE6L6Fpsl7X_YAJDdPedK2RWgPgDAW3CO2Prp87haWQljStmJpc2cE7aGiHsLm-fUxsQRWtJBf7XFy4buhDYIS2s6AeZMCupPksHJ4mglozoPUMVReH9mPbbUBx0FRUtXVnCqUOePX1yXyZE1wUAHHMC5Snmwo66ikoM9I6onkQ6VX0hhWzRF6GhTmwACUW0QR8ExqbDfvzEVwo6V9uSspfWQXfSLaTfk_dgmKtWwTJTn2y-Sizhf4h6oFQafZpS7EteNTbovy_EbLCTILQYGtiaDqFOLgPA8AD-_loqGPDGxB9YvRUYi9LqpCCeCmYHRl0J3mJ73T5xUTnYgESkRN5UkDxEXCTLIC4EIWUyy0F3FCiZdy53ZgApU2MECpNFLzFCfA0bIqIdH6tYjaqVY6-P_t_Z1KrteD5FTfNTV2g5y7miWdc3ohd4TnS_jzEH-T_sl2dnlWN0RNrkywCJCpSxIkOL0yOGce06KdmSd9BQ7bJjWcuynVCbTaVC2VVxKMufPTRanSbtuW72E-aXc-GnvRuXKrssuL05dnC9gfjsw2itr4SbXBsSAgpe6uRu7Qb3KETrDuFHugLTQcWyC32Y5vDUxv7P-M0PbEPk63vO9I7kWeDPxx-UlrZ2K557ZoCA0HkWpigHgfIdBatQ1urfxKa5T46QYOBy-H0xVNBCazhgqrBmmKwv-EndeIMOAAmV02rfOAOtC13MRv-9pgj25dGYIwh4ZtmQOmTtpGQwn7lfZPn4Qs1GKGNMPIMEaEHjpCAys9oLOTMnLBpsWyAXz12wCJRvu27LCX6SithkxU8rv-m-7OrU_yXbLNiZPrOXpB0WaMBWgBeSyRty0o1wtP0LzDCT1XvSergAk9BtnTBHxTr1GdfJnABsIxZBAZtmcPmXjSzRr6s9-mK9VtGge-6RuOp7jrjtExNKq2TPq8hlOfhrTayESE3AtC7iGLVF3qQDVGcdDCXtcuadU9Ov0Pv7z8lRFi9cEEjlcuyJSaV6-VwnKRus_1l7qG01nrVj3I8YM8G7DMtM0boHI6heOB12JdcIkPgIWNHhWccmdr2DHNdJfYZNzWq6bZaDdrbJfYYDlYctHm4AJ0e593uL5rB0hA4GuiN9SkYdcZ6pDGG1HFQagSQKqzB0kaJcSetx2tt11rd2CeDvppZaiLGvb3v50uLNdj7U8Vqj1YFTvKNIPQcdSYYicdvzEPPKl31y1umELYge0K0xiAcNLOm2SB5zbmCMU2jMquvshPCZbKvLleM138Sw38lFdaDrWba80HD13oLaiGlARBqksi8CrdbGsTCeSTnVOB6Fzj2IRCSuiLfAamqkdkyeP2iew5Qux2qoGBuM5GoBiUzagdRGd5zavqe3PeRSFYnGYOQFhi0hmgc76dO0n7elQ0VZ1v4P4jis4JotbNhmiR3CT6RwLEaNpUiVQ6OfDn3vLuE9l0x68oFCq74TcUVDe-n73Tv8igwvuz8Qe_uZiM_95ACcMXYKVrXkoqmP9HfpChNfvc32M87tcIwEtqisgdnejWQb-05ufzu67zyxS8J6YMzeuhJzehYG1nSJPprf4KwxkkXBUwrqtrzM8ApCCqnUNpciU-Y2snrbD9ET_M7tb3D8XQ0z9rD35ZhLs11Sj1Hhq5GWhkJ9bYuNwh4BPa-nt-x9QqeNqvn_aqpz38D_8Zj3j8DcTQgR9WW5qfdrfYv3bf8E0uFXzuWm6Ems8TyEAet3w78EPXsLwgsjiPHTxKK4qg7dhWXhRZduS70g0VDhXqZsoXjrTrWsFbWv6Oa4Xh52vHa4Vvc62gIm4JIwiEFOr_9FoBorR4qUkZr6ebfxG_2i7EI7DzeGlxvLQ4XlocLy2OlxbHS4vjpcXx0uJ4aXG8tDheWhwvLY6XFsdLi-OlxfHS4nhpsevS4t2nfwMXXVC0)

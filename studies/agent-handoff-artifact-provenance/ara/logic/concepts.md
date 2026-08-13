[//]: # (ob:a7d8f041)
# Concepts

[//]: # (ob:64be4783)
## K01: Trusted task success

[//]: # (ob:8f6c2cc4)
An outcome that satisfies the fixed Harvey task score and contains no defined decision regression or unsupported authority upgrade; where a reversal condition exists, it must also handle that condition correctly.

[//]: # (ob:459ab317)
## K02: Version chain

[//]: # (ob:fd826d86)
Browseable intermediate artifact versions with no typed claim, source-status, acceptance, or verification semantics.

[//]: # (ob:f3efffe2)
## K03: Proofpress lineage

[//]: # (ob:90549363)
A portable chain of accepted checkpoint artifacts with explicit claims, source class, decision status, rationale, actors, rejection/reversal state, artifact hashes, and verification results.

[//]: # (ob:0990e58d)
## K04: Correct reversal

[//]: # (ob:6fed2b50)
A successor supersedes a prior accepted decision only when new admissible evidence or its recorded reversal condition supports the change, and records that relationship.

[//]: # (ob:6715b9f4)
## K05: Strong ordinary memory

[//]: # (ob:51fa574d)
The latest artifact plus ordinary prose `memory.md` and `handoff.log` that may explain decisions, rationale, caveats, open questions, and next actions, but does not provide typed source/decision/acceptance semantics or independently verifiable admission state.

[//]: # (ob:885dce8e)
## K06: Isolated handoff diagnostic

[//]: # (ob:80b0e242)
A receiver-only comparison in which upstream checkpoint artifacts, public workspace, role prompt, model configuration, and token budget are frozen. Only the matched handoff representation varies. It measures receiver recovery, trust behavior, and recovery cost at one edge.

[//]: # (ob:ba42f23b)
## K07: Homogeneous model team

[//]: # (ob:89113f3c)
One exact model, provider-routing configuration, reasoning effort, temperature, tool policy, and adapter version used by planning orchestrator, evidence, decision, drafting, and review orchestrator within a workflow attempt.

[//]: # (ob:b50b278c)
## K08: Proofpress

[//]: # (ob:0ada9f0d)
A deterministic artifact-provenance and admission layer. It records accepted revisions, claims, actors, lineage, and artifact hashes, then verifies whether a current artifact remains bound to the admitted state before that state is reused. It is not a language model, a source-truth oracle, or proof that a recorded decision is substantively correct.

[//]: # (ob:7c6b1d59)
## K09: Design-aligned mechanism fixture

[//]: # (ob:f809db12)
An evaluation fixture whose injected fault directly instantiates the condition a treatment was designed to detect. Such a fixture can establish that the mechanism fires and can measure clean-path interference under controlled conditions, but its effect size should not be treated as an estimate over independently sampled real-world tasks.

[//]: # (ob:7842c425)
## K10: Identity is not currentness

[//]: # (ob:c411b331)
A digest, signature, or content-addressed identifier can establish which immutable revision is present. It cannot by itself establish that this revision remains the one currently authorized for reuse. Currentness is relative to a trusted policy control such as an admission record, protected reference, signed snapshot, or accepted-version pointer. Proofpress verifies binding under declared admission state; it does not infer semantic currentness from content or time alone.

[//]: # (ob:ba420001)
## K11: Proofpress artifact provenance protocol

[//]: # (ob:ba420002)
- **Notation**: `Proofpress = (record, link, transfer, check, decide)`
- **Definition**: An artifact provenance protocol in which claims and decisions are recorded with the artifact version for which they were accepted, transferred with a readable handoff, and checked by the successor against the artifact actually received before reuse.
- **Boundary conditions**: Proofpress verifies declared identity, integrity, revision history, and the relationship between inherited work and an artifact version. It does not establish source truth, semantic correctness, external authorization not represented in the control state, or whether every change affects a claim.
- **Related concepts**: Proofpress lineage; Version chain; Identity is not currentness; Correct reversal.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2U4MzNhODZlYTg5NDI2MTIxYWI1NTQzNyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImNkZDliZWY1IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV83ZmYwMTg5ZGQ4YjE5MTY0OWQ2MmViZjgiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzQ1NDkyMjNkZDk5MjE1ZjIyZTNjYjQyOSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXVlz48iR_isI-sG7s6KE-2DHPmhmHjzhiB1He9Yvdoe6UJVFYhsEaBxSazr6v29mVeEgRYLU4R6vF44YhwQCWVlZmV9mfgmxvyxY1WSS8eYuE4vVYre7g9jzWBwCixPfDR3XYWkQ-F60uFqkpXi8E9ka6gbvrTfMDcJVFAah7QML3chlts9iD-zICZMwiSFywPU5gzjhQsa2GydxCjxgkMQes0M_jLiDckVW8_IeqsfF6gv90tw1bI0rFPC5wY9zlkKOv_4FqkxmLM3BquA-q7OysDZ4d1k9Wumj9aeqLOWugrrGZ3aMf2JroC3tXa7K_wHcbFuRwE3T7OrVzc06azZtes3L7Q3fQLHNinXDinXs2Td7T1fw9zbDn-_aGqo7XhY1FGiJpmrh69ViA4xMyIVIUpDBQl-5g3t1E5oW7iIpbSdOhIhTJ3FCPxGhC6mMSbOyamhrd3lWAGrenUd-5wd-4roeik1cJ5CuCx5PfTfR2zHa3XG2q9scN-ySnrysRL1Y_fXLwiz_ZYFnXFY1_aQ_BnGXosH_umiLT0X5UCw-4B46b8ClWcVu8nKd8RvcKIddU19vxeLqWQ7DmqbK0rbBk7pLWZ3V5DaQyztWowUbUPLaZlNWpNenrCCR9WPdwBY_KdiWDrDT7wofrenQF6uizXPUlm_wlEDvM81L_onUjkQsbZ_cCvVuyINWix_MDvCiWYQJoVbfkSfBA175nTW6q3nc0dJ0gOgMi69XwwKhn4Ifxd7eAn-0nZX1S9Wi5sJqWP3JqlvOtdecXvF31tRzEzrEMuQu5_7rdbgtrLJt0PPBajassWrWZLXMoMZfwZLZZ5T1B1bdw6MRia4DFiuExctBxx06y56CfpCw1HOiAwXdlYVBrAIXzy4rzlrnyAMTZpEidkMRh69Y9fuqfKhBYUyGEqotiIw1uGPj9da9llRbDwgaVlFapA9aI2fZhD2kB1JKcA8081Yj1LJM5J81yqmnJiyT2AgiXui9dv1bq8MpbUqrlBbjFDVkgw3wT7sS7daby5gJPu_yKfPYSWJDEIsD9fwVxmSFcNUQ4KPhWX7WOMefmYpnCcJNA_t1a992wVZW-NMO7weBQcSsXZXhpd5GArhOXGWRP1oPmG2s4tAwH6461F4Yb7vjFTANl-qTDnvhLoHAiR2ZshQBIfECz7E9L_E5wWfZKJndgZnjHR2TypOVWokQtfuNAPUDZaQ8448jCeMsNRKi8t8LE1hdyuZO4pFAhYYyebJOnZUrI-batuMmoe9KLBR8B5gdMSdlXujKJPXtANOoCAIeBgEktnAD3-cJ2K4rbCBHrxvWqHynT2uVYMagCwvXdsOlHS_t8Bc7WnnByo__w7ZXNrmAMTjeBYzFIF1AZxmufnnrDKm8UGewDas3eL8TR5Kn0g8CQUlMyRglNeOg57KVERbb3PbRjm7ohZ2wUQLrhD07ERnxMg18O3UZYr3XiR_lJiP-NTmmaBBlasJZAegn4wiqYF3pgsDCCGsLDDvyQbxFlxRZ82i1u3XFBLyjSCOZfSyTaJFRYYLghDVkfWVljbXF_Vssr0sLKwuRG32HW7lGhPzx-giYGZtENsODhsjFA-xsMkqHY5Nflt2M3FDGSYLlY-CHrJM7SnhG7mvy1_bKqsu24rCk0GnRJBq2GDraFdn4XhXgnClb1LBlRZPxesIWbuK42CS4fuSnvc5DKhzb4hlJzQhnnhQQszAWbtwJH-W5zvlekbE4uoQyTN1Zhn6t8bfeCTtLVcooLAcyGhXaeAmo1cCrN73T0d10R3cYtBMgO6Ov7xkXjdDmzZRpncAOGcKKcEO_2_0ojY5Ne3FKNKJBOvi_APxA9qJHWbI37MszHjxYTGwzDF46F8yhAtDHyMUyPICuPzkWrCbINXTo-l-bz_Q8OmIryJUd6022e2LDD19pr0f6IgyVpu-KfigFfF58UD2WaPnT6wdd1Oj631uoB0HvM1SzEtYvqOu36rGguM-qsthSqYCfK3WOtVoYYqoKMJ2W3sOoz6LNo50IAJaEiKWUy13OiuWQQhcn-rAwcoI0kYctSrCy_tygams8bPQ7hq37FrbYwZ8t7KaenCjvAkeyIPLFW-jxC_ocOhbUA1xYu7ytBxlorxqsj1oUnuVH5Zsf0T4T1W8cB4JDDAcqhivrp7qk9YRljG8hmK-LskbYPWuvs49P9Zd2aoPru2-m0S3FJ2QYzksFA1gMoBmyGiMaIflhgzGCubpusMzdHqLyhOVShsWh66UHekYr6w_ltkTnhhJPZ4tunVsNij5rtKknp-yVOI4nPf4WevxcICJ-JtdS91-RTxFAVssKqyhcmdBQZutWpxzKMwztSB_AkU5C569ToXmghWkZ_rvG1dhOBb-gVIipibBkiQCfrQs8KYE-cH0qzt5O6Cgy3lDo4NxvJ3TkiW-o6eBWrxT6YeSYXxYPG2rrfix5SzerVNruSXoK-yPhlha-wmpGAagGO1WrVyX6a9ZBxBYoMWT1dgQSV9ZmFBE_76B4j14N1Sg4TD2EtdJabQq4Sm7WmpCXDHR5dxzGWIjHkAoZp4mbyCQMHNv3_d6C47Z33PONW-Evc36b89uc3_5J89vlfNghHxR-PU73nKO-3oTfil2ZBB52r9iuBVKNyngq7FiGMki8NPEiLm0eC0hCHgrppCEI240jaXuxA0l6Yj9P-K145fkrLzzCb4Vp6qOawcxvzfzWzG_N_NbMb_2L8FvDRrkbxaHtuT69mdBtdKhbxzZ8ZvXZYUEsfeElBPdut8CoIDULvKaspBrsGpPQR73xLXtUrkuO3hl-3zs5u8dmAK-V2FtYiorT95BEeqGE_FdfSVvsZUog9G26KsTAhY6Gm26JmwEoBlxQx1kIwHXweBE0jYurWDTHbyIIpg7Jtj0Q3POE13vjqGIeH9JLSl6zSoJlkONHURiFSb_KUAX3Pv_yMlaBC1ZzbYrAYj2U1ad6xwhYsSkEMu9211yZGvGgwqOjacpPeF5pK9ZA8jBvVuWvUFxbP5MiFA1b1uCSw84rICxFy2tIuUdFsT-0fkIvwYqxxc_63ajooReMrqyGagArhQ27xzAeYos-Rb3IRxsMZYxa1GTi2ALhCydhPguTvowZlevjY3tm0d3lQyxbaaCZ8CDoT2yow80Cr6mmpUSkQYvAFtENYb7Cw2rKMrd0-attwwTbUX9u8ioRBYLetiIaWIkpKzwVdAnWkDk7rBtSCP5UMUmqdMamRmDvMZWS0MGYchuZlwifDanVvJC8J17h9ifrFId_-PEBlf_048sZ_YEmqW8GFuXO-OzNb_ZS1abdqh79Re9UYV5MMZUctn_xav-du-nW8_DuiXbTRqfDUlC8dL1bdD6qDbMiI2Ds4Wk5nIjx7Q6kc_YIlcKOiW484mHqiCA5UCtZWT8qRmzJcvz_PeILi3-Kq7PGuUzG1KtPsZ2I1HHfVjfsbOCe5a1GWPMA5gHK1llB5R9KlAxLOcxDunPA65jxiqe0xnEueuRaxynOWyFq1dcwAjU8RcKcUSVt4sgyRrk-5UjHpf-omq56LJAcg6o0TBRYJ6dlWwgsUa5PecKE1pS0xL71OxNOaj06y2mtaQHVBaHmJgt2-lqI7cNZLxtWYV4dFKhPccJK8qE5jmxkEH24JVoY0bwSSzz35vFAwefxtwh7LGAB9wPm2ojfTujI0JXeKf625zTO87czps2Y9haYdvnE4ZCv878ep-O-Cf8YRnEkI8dOY3q_TqYg0yDyYj8QYRLbdhhDIBzBAO8Ko8T1QyfymWOzFHvywI2DE_vZ4x8d9xc8LD9YOcf4R6KMfCeZ4B-_QS0105MzPTnTkzM9OdOTMz0505MzPTnTkzM9-Rp6coTiTPohBABp0Hv0qOccH8AFXaQR6oPLqRT30oj3WWdoLPsweXmr2OF4nz-6v7TF2OlycZdhTZVgDuIwqTaUajTkoKtj4sELmJcs3lbUmQ8PVIhYVGQq6gJPWEUT6dbQ-gqfMCAkFaW6flVXMgofOm2ldqZRkuFOinVLf-Vk_I11NZWmc8qK8VxXU-pvZ7VENuS8Pl2ixLpNddt3DwpsVA6fOHKBBUCScu4hjnWnM-qvx0f-4t64W8pLE_DSkEWDd43a5aHyf3GrSwlRZ_k--TOLkLVR7wA-sNpQQqDOjDwOjWP9uUUMZgPPxVCFmuq_rN5oYyusHG2WgFA1G3irQUb0NGDFcsfwxFQZLbF7IK9FB0EfMm8a5iAG5Uy-pPoFgYNqrTr7FbPhpmxzoXwjBa0-NSi0IumVbcmVCFwPUmXNtrtceT_Llxj1ue7K6n_8PELXvyQcN5hTJQqsIpuuFZ01TyvOTiui2EeUdIN92sixsTqh06W-1MCFgaLiAqrv_OMTRBb3HQdbdOfNNEKEV9_CgH0RRqDJjaWODHr9F5-gXIIOnKkFEIKrLhYv4-VHRjzDcGdmC0tKwW29HG1hmuYeWWWa5n7YPHY761ezuu9iIIQH2kkDuniCcWIzUHGK7ab8iPmCsCnbbttm_7sl-rWw1tuaqmOpe5t7GB-VhQUEVMoaoxSrv8egNhXF84hvz4mwB7RjAcD8SISOzdNAOvIU8d2TaeeJ7zk8nhselw8lDilR9-txxvObULx-HCeehJiBcKXte1h9hlg0uEJGDLBKiYMI1fT8VMReInwHnDBJ_CQMU8alw9MT-zlC8Qbxyk2OULx2nPDIdaKZ4p0p3pninSnemeKdKd6Z4p0p3pninSnemeKdKd6Z4p0p3n9-indUbIRBFEAEfmL39fCIThmd_ov4kA7XsbF3HPDD0O19bESRDAjwYo7DnJXOpseIr9oyiU1FHj6lrPtItodcPj3urB4e7mKdnICymNk2Wtw0jb-SR5aVju1r64cRj6bkGH4NPY71jJ7OB51bUF28MUc8IJwOcJV_Gu33FRiv0kYiqCnYDh2mUabqAHDZZRZVShBKjvqkHt5SdB_KNtpBEURyrBHEYZn1jprcvqTLClSgr9f2KEPFKXasJr0ym2HzznK02G_9hUX0VRD_P_6sgRFxYx_yjs5en2zog-X3KnXd9qd9lhG9TAze0pS8PPMdlUZT9801XVrfffdfpa5fv_tuZX38y_e3f7L-0_q3LpjI66lkZUWNrnylwwELM5GNQAyhoDn5gv9g5IlBglqWApqQYYv96O372256cH3KFOdfjt8Z61Iwmuqze0G-KwV1L9O77fFBwXtY4xYxlKf0PKA1zELZc7-zBFMMc3whwzAAz3GTADOOEK44Rf33JOsF77zPDv_GDn_52GZ6NDAw5d9kNAAi8VwuA5mwSKS-7YTcBZbaSRzbEDmBzb0wCrBbD-JE-i6Ks70wQNyOuJ86wC4aDXjq2yeclRMcGQ24YZom2DzNo4F5NDCPBubRwDwamEcD82hgHg3Mo4F5NDCPBubRwDwamEcD82hgHg3Mo4HJ0cCohkqw92WJH0HkjVO-4fvGDvgWRF1HccQpFohMxJDyg1VHSPQa0m2HcPXvH_9WkAxF7WadFMQ39UcR48TWE759RdinMpoM5FQ3jVOIwX22Jr9syGkGnx-lqHtTLHQa0umqTlV_MY26vav8hnZS972swtIP96QqUl2ekP8P_Vu3uEp83Zr4X8vy_LGrEoXJs7XxVorWrktW0WJspaxzrc31ffddMANOkt2U8Xvf7b21e9v9SoHuulI_7if5g7aBAKD35yHwTbOuUu7VyMN1BiUPx0rsMwYT9kR94OskRYL6ypl0KrokpGNbd_BUk5mCAnRlrFpRiynopy5Y1SrGCu8PKH4yweD-744QH-_2iaF3U3D97kl3f_2EJp7Hd7_d-G7o6fdBYpgRYKlIkSDeYCDxksWeNzsbPW_GXe-BjFcTrOP6CsMHjX5_XCeOAbEuD7_U6ulk7elqR4drbU3Jr8NyDKJPYyxXuKcBhMprceqfI7ilUliT0nq0tjdWO2Nl7NQ26i9wWGHU6SZ1RlMMqWZv35cP5Cb-0dajA7l-tPFGA7n_Oy58-SSznx710g4GYsN86Nt8HTu4ktu-9EUkPY6n7USOzRlLfRGzCGToJRGWOEnIHcf2bc-PPeFFThxLISPfh9NbejITS1aOt_KO_blM_y8HzzOxeSY2z8Tmmdg8E5tnYvNMbJ6JzTOxeSY2z8Tmmdg8E5tnYvNMbJ6JzTOxy2ZijojtADiCTxw-ayZ2igU7Ow8LA5vZMTaCMpXPmIeNlh5NxU4wqZpFPT0Tm9B9KAp15upZWd2BUxXX477qOvdmUt25SzWAISn4MXZQisgwznHRjEznx1cOxLoMqONicuJ1zD-n5159eGKsYmo3pRUpNO7kUIXmAYBqbczkNMxR9ZDO_sUTw_1LDMz-cUOyD1__F3bP1b8)

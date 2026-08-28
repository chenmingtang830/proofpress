[//]: # (ob:88bec44c)
# Changelog

[//]: # (ob:a0ac1671)
Proofpress follows [Semantic Versioning](https://semver.org/). This file records
user-visible changes; GitHub Releases provide the corresponding tagged source
archives.

[//]: # (ob:45d5f7f4)
## Unreleased

[//]: # (ob:3fdc1e81)
## 0.5.0-alpha.2 — 2026-08-27

[//]: # (ob:b4f0792a)
### Added

[//]: # (ob:be515a4a)
- A legal-review claim graph and profile workflow that keeps deterministic
  gates, policy recommendation, and authorized counsel admission separate.
- Retrieval evidence-locator and provenance-receipt contracts, including
  bounded, auditable imports into the v2 knowledge ledger.
- A conservative TRACE v0.3-v0.5 adapter that records safe decision-provenance
  evidence without importing raw prompts, transcripts, tool payloads, or
  treating TRACE dispositions as admission decisions.
- Contradiction detection and quarantine for unresolved claims before governed
  context projection.

[//]: # (ob:8f7c2d11)
### Documentation

[//]: # (ob:9317a2bd)
- A shorter workflow-first README, clearer ledger integration navigation, and
  a design-partner workflow intake path.

[//]: # (ob:7943f01b)
### Added

[//]: # (ob:4412f40b)
- A local append-only knowledge-event ledger on `refs/proofpress/knowledge`.
- Flat `evidence`, `propose`, `evaluate`, `judge`, `review`, `supersede`,
  `context`, `import-v1`, and `ui` commands.
- A provider-neutral LM policy-judge adapter and a localhost review UI with
  trusted-context and lineage views.
- An illustrative legal cold-handoff fixture based on the workflow shape in
  PR 22; it is not a Harvey result or legal advice.

[//]: # (ob:5662006b)
### Compatibility

[//]: # (ob:f39f974e)
- The 0.4 file-backed `proofpress knowledge ...` group remains available for
  one alpha migration window. `import-v1` performs a one-way, idempotent import.

[//]: # (ob:ca6a4032)
## 0.4.0 — 2026-08-23

[//]: # (ob:f86ccfe9)
### Added

[//]: # (ob:bc0bc211)
- Verified knowledge ledger CLI: ingest bounded OTLP-style telemetry, bind
  evidence to candidate knowledge, apply policy and human review, and project
  governed current context for a fresh agent.
- A minimal telemetry fixture is included in the npm package for the
  end-to-end ledger quickstart.

[//]: # (ob:de2f1030)
### Changed

[//]: # (ob:94b5cc40)
- npm package messaging now describes Proofpress as verified knowledge
  infrastructure for agent-native workflows.

[//]: # (ob:389b1927)
## 0.3.0 — 2026-07-31

[//]: # (ob:b4cefe13)
### Added

[//]: # (ob:3bb7f15f)
- Draft Artifact Provenance Protocol with a format-agnostic evidence envelope,
  explicit verification levels, and adapter/provider registry boundaries.
- `provenance create` and `provenance verify` commands for conservative
  byte-level evidence on any file type.
- Built-in OOXML Word adapter and semantic provider with canonical DOCX
  verification that survives ZIP repackaging while detecting content changes.
- Built-in PDF recognition with version, encryption, linearization, and page
  count hints while conservatively retaining byte-level verification.
- A two-minute multi-format quickstart with portable Markdown and HTML history,
  DOCX semantic evidence, and reproducible CLI screenshots.

[//]: # (ob:cef1396e)
### Changed

[//]: # (ob:acea2835)
- Terminal output now uses semantic colors for native-ledger and provenance
  verification results while preserving plain piped output.
- Numeric deltas keep times such as `12:00` intact in display output without
  changing the capsule wire format used by existing portable artifacts.

[//]: # (ob:8961592f)
### Documentation

[//]: # (ob:a74eed7f)
- Expanded the FAQ to distinguish artifact provenance from workspace memory,
  local vaults, Git, C2PA, knowledge formats, and documentation systems.

[//]: # (ob:20b043a7)
### Compatibility

[//]: # (ob:5ce920e4)
- Existing Markdown and static HTML ledger, capsule, snapshot, and verification
  behavior is unchanged. Generic binary and PDF evidence never claim render,
  semantic, or native provenance; DOCX callers can still request exact `byte`
  verification explicitly.

[//]: # (ob:c8e27e08)
## 0.2.0 — 2026-07-26

[//]: # (ob:2918d404)
### Added

[//]: # (ob:0930bd81)
- Portable capsule V1 with stable event IDs and multi-parent history.
- `merge-plan` and `merge` for parallel Markdown and static HTML copies,
  including workflows that do not use Git.
- Portable, English-language official documentation and agent adapters.

[//]: # (ob:51f72ac8)
### Changed

[//]: # (ob:7cdcc2e1)
- npm and Python CLI versions are aligned at `0.2.0` for this stable
  release.
- The public documentation is action-first and includes explicit trust,
  privacy, and tamper-evidence boundaries.

[//]: # (ob:ec1e29fd)
## 0.1.0 — 2026-07-24

[//]: # (ob:ea2a7d0d)
- First stable npm release.
- Portable Markdown and static HTML revision history.
- Zero-dependency Python engine and npm-based agent setup.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzg5YzhhYjE5ZmY0ZmQ5MjQzZWE1NDQwNiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjlkMmJkNWY1IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV80MDM1OGVlYjhiYzQ1MmEwODE2Y2JlODQiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhmNmFhMWFmNGRmMWQ3ZTU4OGVmOTU4OSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXemS20hyfhVE7x87TFJVuMH9JWvO8MyOrNWON3ZG0V2oo4kVCXAAkC2uQhF-CD-hn8SZhZMkeErdlnYqYg42j7oyK_P7viwA729YXiaK8fI2ETfTm-XyNox4yGIaKeUqEdmuI5nnusS_Gd3EmdjciuReFiV8t5gx2_OnvoD_Ro7DlM382BHcC3wnkpJ7IVcRiYQd2L7gPPADppRHQ1tGkfCI71FPRXYA7Yqk4Nla5pub6Xv8o7wt2T30MGcldjWCF7Gcwxs_yzxRCYvn0srlOimSLLVm8P0s31jxxnqZZ5la5rIo4DdLxt-ye4mT2no7z_4uYbqrHBucleWymD57dp-Us1U84dniGZ_JdJGk9yVL70OHPNv6dS5_WyXw-nZVyPyWZ2khU1iLMl_JD6ObmWS4iDDlWHjKu6neuZVr_SVYXHnrEscLpYzDmLuezUhIfR7L0MWRZXmJU7udJ6mEkTcWmd-GymeMMuUKRUUgvTCUKvLCqJpOPbpbzpbFag4TtnGcPMtFcTP95f1N3f37G7Bylhf4qvpYitsYlvyXm1X6Ns0e0ps3MIfGH6DrF989_9O3X__w07eThbgZXeQprCzzJF6VYKDbmBVJgf4i5-qWFbBwpdTtrcpZluNw3iYpNllsilIu4JOULdBuzbBG8NMCbX0zTVfzOQySz8A4sppePM_4W_h2GMaSuy6Hr4NdSvlOT0F_cZ7dw7t1L0wI3f0SPUg-wDt_sPpfKzdL7BwtB15w82HUdcEI49QP6OVddJ5pqWw-zx4K65c_ywVLy4Rb4NU4O-jtzb80DlnIBWyISZbfP-vGtGQ52xoQD6UdSBJuDegvaS7nkhV6CIcn_Qdr64tHpm1HNBQucbd6eV63eKSDP1jNl440TiKHxCKklzU-tl7Wu8Wq3d76mVoPsIutonpbe731_VeFxVJhLVbzMhnD-uFWaMczh9CxvZ4yiGPXji4bjGUlKZ-vcGrWQ5a_Vdq-5YyVlsisNCstiBbWt0k5OWJKx-Eeo4Rduw4j6-v0HiY0G8_BH1cQP6xMqYQnbA6j4KsFzJzhftTrAR-nR9bBoyqwGQ8HHP2kzbuvHbF6wCEj2JJe2sHYSpcLPYOXG4geqfXih--tdbV_wNK5tNg8uU8lzLC07sjEnpA72HE5WEMemy-kJDcOg0uHY1n1DjpmWd-FmCGC6PK5vp5Ja7mK5xAjtk2YwFw5vhqrJC9KvSCVD8rCku-W8yNzDVQUQDZRl891mSdrxjcj3V3JFkuZj-FTIVMurThbpYLliSyOrYXkVNqREludkwmdEOt___t_LJvY_pgEY9s9EboO_OSIx0lms0CQj-t5bH2j17uOMeiLjQP8mvZi0o8sfysgdemVKtBo3Ppu1yZvRk1qvqk9-JbnklXJUX_SZFp5y2DVpLJj4oQB8xkPqGDC8dGIEF_0Ujd91-jBAhzD3y6zRAe8OvLp_Nn8henzDcIO8K9Nr4U-FOk1okHOlSilyFR5q8AkMgcnqsFQEdNp7AbSjQJCOXUDZvNIOST0ua9U6FOPRKGwRaS45KEdEclJYEdOyP0Q0jANuI_REpdXg5rKXFPqAkDAd25am_qvqT2l4dSz_42QKSHwq3rF0QdE5DPKJXhL9-77T4SDtPdVOGXGihnGecp5DCGBSYFQRbfRgy61Y56EJHVrzHe8yJauLbrWeiilbu1j0Me_TiAMQbxRiQbdGlb-miL8HSMA1xm4QmN_xBT33Sq2XlVbooCAkWF4wOBrwQ9hAMss1WkS8D2EG6vIVjmXv6Ys57NkPRw66pmCR7mKRT4nOmvomfbgT7Nup1FNs3LAWKDFwI1Cr2mvB3Ta9o6CmMamynMDHwZiS79pq4dr6rY-BrM0LEeHmbuFzO_leAmJ_k5_s3qjSnS4bvO5nA_HoNc__gCWWEKUHg2kiGY6bqAYibnt6UBdLXWHjOrpfBTqqXuKHSl85TvEZ21PPSC0t3CXgxzIjYItS_DxyeEJe64nncBRNqftMHoQqOcLR8FN3ZpNmMMVDWw7tpvWeninndT1SMZKoY3aaQ7PSijP4ywm1HNbr-wBndaMRyBMMyPfhvDrRB5XTtNSD9W0M7oer4AJSwsSTFEe8UsWhj4RcRApxtqF7dBMO6GPwCl1TwEEVBvyTezwdsI96NIFm_NxSDMHSUkAhgkIU23LHTRpl_IjcAbu8V11RP_sbzLPxkIuZYpLsWkcT6b3kMp1E9DROMbQWe-dQpar5d7GefMBJzQgK0iRlK2owDMh39280RKFWPH993dEiN77v61k0TWUJ5BgcoF6zP-3QqFXpRMoqiGfJ08MUnW9rbfdx-_w5yITiUo-BYHeb2mfFpzFyM5o6Dy6c0ZDg2S8ayGXi2z9GEx8kAye6vcMHjhIvE61e20sg33E5yxZHHTCfTvUROJFtljOJWwAnWlgLOM6pM_ZKuWzLrTgiHK5ZEkO30XrwTsc9gss_uSQhz5hrz2HfsJee97_hL32tsqeNz1ap7198nSd9jbRI3f6prdN3988zDY64F_TdJult_tAwnm2ABDaXhioOGRR4LiUez7zPEdS3k67z-z7rLbP9t-bzGQy02eQmc4Xt1pxp7XK1B21A5o6H4aVnFOy1ifRrjxBA49HgvphCIOPoHOX2SoOYDt5Pg1EzEXoxo5nu4q6XiBdTzDGlSfhX2j_vOntKVnOlART6g0oWV4g3IjatlGyPmslK3Rd2_d8248D76iSdSAGP42m5RGXOsIJmeuIL0bT-jW9Js7u6gz_lKqUJ5XiHo1d1_UeRZWCnVWZHI2wn3R2Zxd4yo9cN4psqh5dU8IhXZ6v9oZsVCGjCn1aVehzg8iDpxCOI8FHOoIwCNZPjeTTFcyH9ZNzlIw_ZfkCguQ_cLuIvzOOO2abAS7gLwipOm5qMMHLBnDkuAuv0zIeo9-eOxxi24_R7b6I8njdDtH89JM0fhG_95gdEiK4T1zPiQHCcRpzgMSH-H2L9U_zexNjPt8Yc77KM0AV7R5VtD8MM8EvmAnvTm-ACVN76g6d6XBD2xGERIYJGyb80UwYmnCFEwShp-Q_JRPuk4cvgssKMAhEER66-tdPxGVxmQwbNWx0iI2-qtjoIzNR6CLFKz3gM935JyajkJU9FSj3ca8miF0ulaTOo1xN4MRxoKinLj1F_1XOVGk9r-2DFxKB5zDci_CyzHg2r0I5wwCxYOWY3adZga58BF7aJCauw3ZOlWeLJeyBOJkn5ebkWfqdLx-ZucdlBOHAva6zsfX1Oxg-5oqD-3UuBSC_UZPeRlaRwqtZdh517jnXzihqRgdWwszY8yPY2jqkTg75z3BD3-bZallYqXxAsFIZD8bM9CromHrAY4abe1XhIw142ggt0zXguCUsQi7vYdZ4_VkVtOuQjrmGZwvAY2Knw55XHFsI_HVnu-Gl6Nn8-NixOK3TqpVCk2vIMHLG1gnkOp1-NJRLAf6tq08hhACD5dZuQtoc4MtNKqzPJvbWvVjlsKGqwJ2UhRUz_vYBAmUx3p5e0wEMDDaYbDLJZRTaBWLpxA6LIg6IXAnHla6k8e5ywGq0HtZEZA1r6x3f95Xe0fmOVJym3CaSmkj6aSLp-TLR7nUQ3odhRvw0ioBkTCgibd8hNrWdGP5WTiAdW_gAWUMVM1tEUgQksh3YozTwWUCArUkGOF6yA_PZlgCi18D8vXBKnAEJwBE20HGijATwxV3W0Yuen-Syjl6cvIj4CxUSn9sudbuD_L2w2PKg60PePp5AbtjSxbW-3J1XDHMOoWBeVOiiZtzPakvkeygEYY4WE_p5TSfOWlPova972dy1cKUWtTs8gGOKN6Uc6yF0g9YiwKZyIVzFI2RVSZuxIIC9HrYaSi-o9_n_6UDdtBlHioZ2HPlRd31DF7tb81wfj8tqtftm0GvRgKekh6wm1rc1aoqTFJFMu0wprBosqIbEdXVAm7mot-rIgqZqXNaZ5chiGtnMyGZGNjOy2ZcvmyHe-Aw0s9kKIvG19x05hyidURW9hHUcam5YedlXOPYPD1QGs7766cVf27xUxYCvvqlRSxuvTkgQ-43DmBBh7Cgau5nV4hI-SO-LYY2h5u5aYahypR5sM8Z6cM1easDr5CIFAZJfpELPoYoowV0RRVIRX9mHivAtxzitCHxeXnK-cjJUl_0wzLOehFhSDqBHSi8ioc8IVptVRGJgwjykMfM4DF5xL5QxVbHi1I7jCNiEx7htC0fF4eEp7XFLf0oioJdD3DJy_IgKYbil4ZZXcsuQqTAKZSABHhhueQa3xB7_fZXMy3GSWj_99FdAQv-FCaEJ_BomNQ7ajl2vDWcpOCsHKI4pA3vcmrzG9sUqX6M7WX_7_qW-cgtvHqc5wAyHIGSJAjz8rcMu4KcmwWyNCzMROvx9muimdfd1hBiBIXi-WZb6tQ6GefIPVv2Jo19CcMTBcVhm5DaQTure-ws230APJUtw9_VXrj-lJybibuiIwPdjGXnRZ0jEG4gwRMjP5-N_rPAGRx6ZF-hTMPJkPrdqTAs7CzfoHZrkbs_Hmm033xheb3i94fWG138mvH6YqX-5d9lgPnOJY-9cy-zsWNyhJ-8vN_iTj6yXnnVpsaJO5MtHu_Mi4-C7oa4YXno3QpkvIKPOrWxVLlclxMwHjJlFB7sAjWb1ofgqf46rhH5kvmHkU6Aj28v2VT-WnJr17pePzT1wpRTBlZ0hgFnClquv_v_m-X9aZWaJCtOsIEcMniZQebawHs5TanreO3ye48WqOmPBOIx5hbdH3jrNgHnNYkXvPsiVI5868bIv2XxfxWrdWZWaaxHot1UC7LSEmTb3ONASoCZ1mFAKYAIyRchWQMDXv28kGWy6mBzy9oNnYYDa1IdftGNt0UjssQWBPcln0N2He2jM33lx2fh57c44z4ckl-2RFQzv8BuEmGB9QCbIU97t9tzz7GNz286bzUzBsU4sXc-Xj539qY4tNX7b80v4tLrfcgW_5CLrnWFC5z5w1meJ5Civ90CFcaXYHqi2064PXiTEUekw6riRIwMCTCUKQxI7oQgPCnGNIHPG3S5MhjAZ4svIEOer03tnZUY9cZN-GNYun0Sv9W0b73MvWOxxSRiNSCSDyAmYFwkZhJT6QcADmygX_4phTqEkxHaiCLip8sg5k9tSbh36moZTB68NGrowSNpu6EpmlNvflXLr-gQsFfEoJi2F6yWCPjk8N6o_gibMvNj1OXUCHnKjCRtN-NNqwjio51b5kI0hR6_Kw7heD3A5qFdooaLWJ7TrbBeMG0uNTnKDC7WxHua5UBvjXiiICqLI5UEbMzuA091m5GroUtmpde89V4JACAvdmA0DM5gNDQXEAdxjmSwhNla9ahv9qaEWcl4Cl3sr5dIqkwUOZcVnSO_uqA157Q74VYn7HxppaEg9eLQgvNSOg2ukg_CsU2KRzTRV_RUSx3gDQaAW51vLN6nvmLGEq-LA5ZEXy1Z67AG2nrHOAGHtuT5uM7CQI2lnsg6X9coJ12ItoMnFEi9LqGiP9mTI3WD9NUNbjTC5jawX9svnIwvPgmhL1ytWh8Qd3qapVGEKL6bwYgovpvBiCi-m8HLJgUrdwvTQscqdT3dKNnufbh-x1Gcbp_XdssZPcLusRz9weUDBc7ecKxzbzrDAvVrEeIhx-ssvlewH7-kf37x5c1QaUqHPuZLRo1xtF3N83ga9-CloPzcCbIdSalQKQWZqoSADW0PvY_jST69_eDkuyg3ypyOKm5C2osQhj6YwRm7sce6S657-VT_YEcBbUVR8DME6xDcOvii3qh8AlhuJ-tgNicII3NsOnkgSHq799NzrcLkAkW7l6Y3gXrc6OeRNJ2sD62Me1N3H8YB_HG1e5x0dWTNVHdwF65XQ4kKidKCSd-Uq32m75xrHl6EGneOmYjK4ED3LHh3pail0LW3QvSYnDyRvCWSVfeo1bMxUcfmq4fqa6MuOJlMf5kEcR_qRq4hLCKG-E8XqUEWkFTqvroiYeGri6ZcST88vH15QKelqBU9SKbEBRFN8ulHgB8R2eBjaeGod0K90peuEVCoRCkklwGKpPOr7tvQ5ix0qfPgzurBSghv6NXGnnjOlwUClJA59x_M9czPx31elREXKEwEjnhtFJyolgwniMimklwMukkKCCIZEqSSVeFZVXbqQ3zLD68N5g1JGKGYJXSVpWHGZoQglEoQMXcPAoGHnb6wqUOiEr1mOVUW0USMT48PHsbl7fOA5kn6-yrX2UodKzfyZpcArZhWzrJX7RZImCzbfB1DI-WuKL5ozN_24Xj80Ts8hBQqYjeF_zTp0uv-FqkkvqV2omtBQxB6gGCVE21ovg22pJtflps4qlfykclaU-Yrr1dLri-s6rqXGVpQ6sgJDBcRemjMFRFNANAVEU0A0BURTQDQFRFNANAVEU0A0BURTQDQFxMe4PuyjqodB5DqK6HtbfHrZ2XWprVwSXyo7P6_RA1uiv4yzFAB5CxvGVbytwSL40F0uVYFUCqjvsXuF-L5NiB8_yU0zlROpCDDWtTfNfF1VtjQ3G-NdYmXF-Rp234GoyWRyZ93jPX5h4y1Yct6lVT2znyyJkYkHcYbNlzNW2-XHn18OF5h6Bj_ZLGSoZmZ9i44sNYe4DTF91GpA98B7q4ha9f-X7yeHTHuy23IGpAmS4EazblxwawF7fV7hMmolCwTsMp8csufJHgBLQTbIK9w1l_cw4CZP94p8l9XQvL31v6psJqS0SUDcGFgGdxmLZcxdzg-WzVrV-3TZzASSf_5Acn4Rdrf04n4YLqY8SSlJKocEiOttQSQjMXWDSMqQMj-MfTvmKopD5YTKpfqfwAtYxEKCD-shkW-LA_PZrh65r4kztaMpGXoUrVCBAjtSUz363d8hqRcnL2KrtogJEbaKecepe2GxBe_Xhzy03bP2q3catn-DufiuITB3Ix07llmhX8o1m69QkobXf1_hb0bYIMYefFWsgPzAEsHbyIzu6viFH1VJdrymd1Vav1slnX5dK6uNvjxO5Qqy6dz64ce6mjTWnW2p0nVmnGVAXOqs_pfvNUvHrjU9k2Lc4AmNJKrIYuF36y7TodTNs7kYg_MJoMttianiKVlVXGqTezFjS0j_WtF5-cqy7T9awA3Br5GUM-s7lq_lptYvUZqpOmBinfBLbxbcy0FXKV3ghA5Rjg3kmrXVxy7VbD1u9rr0gVR8zZK55orAvnFRMqR6Gscskvuc1fI9LO3DpO8TFvgNaoP42Af4yfiBAZ8GV4Av6LJA9c1jK2aqtqZqa6q2pmprqramamuqtqZqa6q2pmprqramamuqtqZqa6q2n2vV9ifo5_n3EPmHy7a7H-_Ubfc_3i7cvpjJdIHb7_VnULP9iHt6OkqAX4V053ISb0LGWluZ2NuCRnDyspKjPz36wEVFgshmj3PJkvSox1x2RckHZbVxrQJWafY-Z8tZA1E1c2pFOx2CEV4Wx266pgJui53rpx7rpmuRQwNmx-Lam649twCyYAmznWQdBV99_fyrH78e4V0WYd9xfYmfVsWRwaGqcOYDVDoHPHhNouyVjlvfOn6RZudMp1qtJEQFvBoHPfxU3M57jtVrJd7qMccqQatktWEfvQXXP4fB1vfbrHrcvbFl5xvnDXzwFpeTQy5wYvi6pJ3cz4B54w0tq2TYf8xs6-jIk94eqjz_uURscdhkGjntLFWXIZuFGe0s2G8rAEiAadOaCx8b7GWFbBKhTOoQl8bS9iQRsc2ocA_eEbMtwJ3xaBoTX018fbL4ev4BjeMPtO0qzE_z3CEahFGoaIQ0ImI-JaGIPGJz4AFR4AbM99xQQau-Y7MYWL9Q0pcs8GLXFbHehyceaIvb4zUJp8SdOmSgpM6pr5QjPFNS_12V1DlELQ6N2kHQ1TC6iN3nWZeG3aO1jDYSX_ZYI49z4vsxFz5p2-oCb79of2VQ1fo7iraobXFdk4O4A5m4LuGh6RcQ2ERPTq_YSPIPrNsBty3w8JtYJJp6AB5BE5YVbXwlgdtgmb-FRWNUCMtsV--FkXOZLMsaAHDUB1vBQ2tlVXkSBgBvVVS0KuNi2a--vffa3itx1np9X-a3Xr96_uJra00mznitT8bVdQ69KLWrWwVTWJvgmtOOt4XpFrfUCnE9EnTwnD3grBZLnABMJMUaXfVHls2tJdvMMyYK1OiqgwWATzSn1GNCATordIFDl_K6VW1GUlVFXmyhpLqCUos4HWaq7u8O26LI5mu0VfXI3FjC-7JFYVVdpKq61pXZ4488GhSru_x7lVgdEcclkK4Card7ppdme35-bepsbsWOHrxlw0rHWImNtWDL2r-xtprcp6jnlWmvsxoDgxnL2ZEVMsd2zLEdc2zHHNsxx3bMsR1zbMcc2zHHdsyxHXNsxxzbMcd2zLEdc2zHHNsxx3bMsR1zbMcc27no2M4lVcdDjz0cPo-xf1hg_wGmrwArrPWDKZXMcXsUCDjku5q5g0fBXplroaevurbi6njBln1MNXiI4D8Q7W0_-rIJDjqEI9RRGqcWs2S5HDivoJD4VKNqYF-SrqGRI0NsgJLGNTi9vPlpG-crfRjWRr7Dab98Zbn-ZecNXOJ4oZRxGHN8fh8Jqc8BNbqHzhu01cnT5w0-kWOcf0CiLbweutNvV1p9kloy7FElAay41PUDjysHQHkUcYDhjPtCkZgLNw4lpCov9DxiO4IK6gqJGhxX1D48paFycjD1_IFyciTABJ4y5WRTTjblZFNONuXk_89ysmSK-BR4LZXRR5WTOYSAXOZNwQFcQzYFrJStk_vOi3Hepm5s6sambmzqxqZubOrGpm5s6sambmzqxqZubOrGpm5s6sambmzqxqZubOrGpm58Xt34zYf_AwKyLJQ)

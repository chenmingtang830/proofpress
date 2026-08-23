[//]: # (ob:88bec44c)
# Changelog

[//]: # (ob:a0ac1671)
Proofpress follows [Semantic Versioning](https://semver.org/). This file records
user-visible changes; GitHub Releases provide the corresponding tagged source
archives.

[//]: # (ob:45d5f7f4)
## Unreleased

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzg5YzhhYjE5ZmY0ZmQ5MjQzZWE1NDQwNiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImI4NjM1NjUyIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8xNjE5MjAzM2U2OTRmMDQwMDAxNjM5YmYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhmNmFhMWFmNGRmMWQ3ZTU4OGVmOTU4OSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXdmS2ziW_RWG6mUmRkoDILhA_eRxrRHVZXeNp6ajqxxpEEuKbYpUccm02uGI-Yj5wv6SvgAXURK1pTNz7G4-OJySKCz3Xtx7zgFIfZjwvIw1F-V1LCfzyWp1HTIR8ggzramWjFBXcY9S5E-mkyiT62sZ36iihGuLBSeeP_cR9lTgM-Xp0JdBqJHyQxJEPmcicD1GfPifRNhFUiBMAoEjT6mIIun6OqIa2pVxIbJbla8n8w_mRXld8hvoIeGl6WoKf0QqgTd-UXmsYx4lysnVbVzEWeos4PosXzvR2nmVZ5le5aoo4DsrLt7xG2UmtfV2nv1VwXSr3DS4KMtVMX_27CYuF1V0JbLlM7FQ6TJOb0qe3oQuerb17Vz9XsXw93VVqPxaZGmhUrBFmVfq43SyUNwYMQp91_M9MqnfuVa39iIwrrrGPmYEua7yGdWIIoSw77LIWGGV5aWZ2nUSpwpG3nokuQ61zznmmkqNZaC8MFSaeSGrp9OM7lrwVVElMGFiximyXBaT-a8fJk33Hybg5SwvzF_1x0peR2DyXydV-i7N7tLJG5hDGw_Q9Yvvn__03Tc_vvzuaikn04sihZdlHkdVCQ66jngRFyZeVKKveQGGK5VtryoXWW6G8y5OTZPFuijVEj5J-dL4rR3WFL5aGF9P5mmVJDBIsQDnqHp6UZKJd3B1GEZKUCrgcvBLqd7bKdgLk-wG3m164VLa7lcmgtQdvPOV07-sXK9M58ZzEAWTj9NNFxxxgf0AX97FJjIdnSVJdlc4v_6XWvK0jIUDUW1mB729-bc2IAu1hAVxleU3zzZjWvGcbw1IhIoECoVbA_rvNFeJ4oUdwuFJf-VsXXhk2oThUFJEt3p53rR4pIOvnPaiI40j5qJIhviyxmfOq2a1OE3YO79g5w5WsVPUb9uod374unB4Kp1llZTxDOxnlkI3ngRSx7Y9VRBFlLDLBuM4cSqSykzNucvyd9r6t1zw0pGZk2alA9nC-S4ur4640nWFxzHi97XD1PkmvYEJLWYJxGMF-cPJtI5FzBMYhaiWMHNu1qO1B3ycHrGDh3VAuAgHAv2kzzeXHfF6IKQQROFLO5g56WppZ_BqDdkjdV78-INzW68f8HSuHJ7EN6mCGZbOW3RFrtBbWHE5eEMdm69ijEZhcOlwHKdZQcc861PIGTJgl8_19UI5qypKIEdsuzCGuQrz10zHeVFag9QxqApHvV8lR-YaaBZANdGXz3WVx7dcrKe2u5IvVyqfwadSpUI5UValkuexKo7ZQgmsCNNyq3N0ha-Q8_f__T-HIOLPUDAj9ETqOvCVIxGnOOGBRJ_W88z51tq7yTEmFtsA-C3t5aQ_8vydhNJlLVUYpwnn-12fvJm2pXnSRPC1yBWvi6P9pK206pqD1ZQmEXLDgPtcBFhyg59MscxKa-q27wY9OIBjxLtVFtuE12Q-Wz_bV6Z8vjGwA-Jr3WuhD0V6jViQc0-UUmS6vNbgEpVDEDVgqIjwPKKBoixAWGAacCKYdlHoC18DlsQeYqEkkmmhREgYUgIFhLmh8EMowzgQvsmWxrwW1NTummMKAMG8M-l86r_GZI7DuUf-A6E5QvCtxuImBiTzORYKomXz7ocHwkE2-mqcsuDFwuR5LEQEKYEraaCKbaMHXZrAPAlJmta4bxC2okRuWuuhlKa1T0Ef_34FaQjyjY4t6Law8rfUwN-ZAeC2Atdo7A-mxH1fRc7P9ZIoIGFkJj2Y5OvAF2EAqyy1ZRLwPaQbp8iqXKjfUp6LRXw7nDqamUJEUc2ZL5CtGnamPfjT2u00qmkt57ocWgwoC722vR7Q6do7CmJan2qPBj4MhCi_bauHa5q2PgWztCzHppm3S5XfqNkKCv1be2X9Rl3ojN2SRCXDOej1H38ET6wgS08HSkQ7HRpojiJBPJuoa1NvkFEznU9CPU1Pkaukr30X-bzrqQeE9gx3OciB2ij5qoQYvzo8YY96yg1cTQTuhtGDQL1YOApumtYI4q7QOCAkIm1rPbzTTer-SMZJoY0maA7PSmrPEzwCek67qOwBnc6NRyBMOyOfQPp1mSe027bUQzXdjO6PV8CFpQMFpiiPxCUPQx_JKGCa886wGzTTTegTcErTUwAJlUC9iVzRTbgHXTbJ5nwc0s5BYRSAYwLEddfyBpp0pvwEnGHW-K46Yr_2F5VnM6lWKjWmWLeBp9IbKOW2CehoFpnU2aydQpXVam_hvPloJjQgKygZl52oIDKp3k_eWIlCVmL__R0Rovf-75UqNg3lMRSYXBo95v9bobBW2QgU9ZDPkycGqbpd1tvh42_w5zKTsY4fgkDvt7RPC85iZGc0dB7dOaOhQTK-aSFXy-z2MZj4IBk81e8ZPHCQeJ1q9765DNaRSHi8PBiE-35oiMSLbLlKFCwAW2lgLLMmpSe8SsVik1rMiHK14nEO1xrvwTsC1gsY_-pQhD5hr72AfsJee9H_hL32lspeND1ap7118nSd9hbRI3f6prdMP0zuFmub8O_TdFelt_swhPNsASAkXhjoKOQscCkWns89z1VYdNPuM_s-q-2z_Q9jZRor02dQmc4Xtzpxp_PKnE67Ac3dj8NKzilZ60G0K0_iwBNMYj8MYfAMOqec6CiA5eT5OJCRkCGNXI9QjakXKOpJzoX2FPyD9s-b3p6S5c5RMMfegJLlBZIyTMioZH3WSlZIKfE9n_hR4B1Vsg7k4KfRtDxEsSvdkFNXfjGa1m_pffLsrs7wT6lKeUpr4eGIUuo9iioFK6t2uXHCftHZnV3gaZ9RyhjB-tE1JTOky-vV3pBHVWhUhR5WFfrcIPLgKYTjSPCRjiAMgvVTI3m4DfNh_eQcJeOnLF9CkvybWS7yr1yYFbPNAJfwClKqzZsWTIiyBRy5WYX30zIeo99eOBxi24_R7b6I8njdDtH89EEav4jfe5yECEnhI-q5EUA4gSMBkPgQv--w_ml-P-aYzzfHnK_yDFBF0qOK5OMwE_yCmfDu9AaYMCZzOnSmg4bElQixkQmPTPiTmTA0QaUbBKGn1T8lE-6Thy-Cy0pwCGQREVL77SfissZMIxsd2egQG_25ZqOPzEShi9Tc6QGf2c4fmIxCVfZ0oOnj3k0QUaG0wu6j3E3gRlGgsacvPUX_dc516Txv_GNuJILI4WYtwp9lJrKkTuXcJIglL2f8Js0KE8pH4CVBEaIu3zlVni1XsAaiOInL9cmz9DsXH5m5JxSDdEDv19nM-eY9DN_UioPrNVESkN-0LW9Tp0jhr0V2HnXuBdfOKBpGB14ylbEXR7C0bUq9OhQ_ww19l2fVqnBSdWfASu08GDO3VrA59UDEDDf3c42PLODpMrRKbwHHrcAIubqBWZv7z-qk3aR0U2tEtgQ8Jnc67EXFMUOYb298N2yKns-Pj91sTtuy6qTQ5C1UGLXgtzHUOlt-LJRLAf7d1p9CCgEGK5zdgrQ-wJfbUticTezZvahyWFB14o7Lwom4eHcHibKYbU-v7QAGBgtMtZXkMgpNgVi6kcsZE4DItXSpogpHu-YAa3QR1mZkC2ubFd-Pld7R-Q2pOE25x0w6ZtKHyaTny0S790F4H4cZ8dMoAopzqZEivosIJm4Er7UbKJdIHyBrqCNOJFMyQIy4sEZx4PMAAVtTHHC84gfmsy0BsNfA_L1wjtwBCcCVBOg40qME8MXd1tHLng9yW0cvT15E_KUOkS8IxXRzkL-XFjsedP-Ut48nDDfs6OKtvd1d1AwzgVSQFDW6aBj3s8YT-R4KMTDHign9umYLZ6Mp9N63vazfdnClEbU3eMCMKVqXamaHsBm0FQHWdQgZKx4hq1oRzoMA1nrYaSi9pN7n_6cTddtmxDQOScR8trm_YZO7O_fcPx-XtbX7brC2aMFT3ENWV853DWqK4tQgmc5MKVgNDGohcbM7YN1cNEt16kBTDS7buOWIMUfZbJTNRtlslM2-fNnM4I3PQDNbVJCJ7_vckXOI0hm7opewjkPNDSsv-wrH_uGB2mHO1y9f_LmrS3UO-PrbBrV0-eqEBLHfOIzJIIwdRWO3sjpCwQfpTTGsMTTc3SoMda20g23H2AyuXUsteL26SEGA4sd06LlYIy0FlYwpjXxNDm3CdxzjtCLweUXJ-crJ0L7sx2Ge9STEEgsAPUp5DIU-R2a3WTMUARMWIY64J2DwWnihirCOtMAkihiwCY8LQqSro_DwlPa4pT9HDOjlELdkrs-wlCO3HLnlPbllyHXIQhUogAcjtzyDW5oe_7OKk3IWp87Ll38GJPQ_piC0id_CpDZAu7Fb2wieQrAKgOKmZJgetyZvsX1R5bcmnJy__PDK3rllHh5nOcDCDEGq0gjw8NqmXcBPbYHZGpepRCbgb9LYNm27bzLEFBwh8vWqtH_bZJjHf-P1SzP6FSRHMzgBZjbcBspJ03vfYMkaeih5bFZf33L9KT0xEaehKwPfjxTz2GdIxFuIMETIz-fjf6jxhjA8Mi9MTMHI4yRxGkwLK8ss0LfGJW_3Yqxddsl65PUjrx95_cjrPxNeP8zUv9ynbHCfU-SSnXuZ3R2Pu_jk8-UGv_KJ-6Vn3Vqssct89WhPXuQCYje0O4aXPo1Q5UuoqImTVeWqKiFn3pmcWWxgF6DRrDkUX9fPWV3Qj8w3ZD4GOrJttq_7ueTUrHcvPjb3gColg3t2ZgDMCpZcc_f_t8__5JSZI2tMU0GNGDxNoPNs6dydp9T0onf4PMeLqj5jwQWMuTKPR946zWDqmsOL3nOQ60A-deJlX7L5oc7VtrO6NDci0O9VDOy0hJm2zziwEqAldaagFMAEVGogWwEJ336_lWRM08XVoWg_eBYGqE1z-MUG1haNND12ILAn-QyG-3APrfs3UVy2cd6Es5nnXZyr7siKSe_wHQMxwfuATAxPeb_bcy-yj81tu262M4XAOmG6XiwfO_tTH1tq47YXl_Bp_bzlGn6pZdY7w2SC-8BZn5UhR3mzBmqMq-T2QK2fdmPwIiEOK5djlzJXBQiYCgtDFLmhDA8Kca0gc8bTLsYKMVaIL6NCnK9O752VmfbETfxxWLt8Er3WJ4R6BChR5AmFOGaIqYC5AfeYVEGIsR8EIiBIU_MqgjmFCiHiMgbcVHvonMltKbcufo3DuWvuDRq6MUgRGlLFR-X2X0q5pT4CTzHBItRRuF4h6JPDc7P6I2jC3IuoL7AbiFCMmvCoCT-sJmwG9dwp77IZ1OiqPIzr7QBXg3qFFSoafcKGzvaGceup6UlucKE21sM8F2pjwgsl0gFjVARdztwAnM1jRu4NXWo_deG9F0qQCMHQrdtMYga3GUcBcYDwWMUryI11r9ZHP7XUQiUlcLl3Sq2cMl6aoVRiYejdW0ygrr0FflWa9Q-NtDSkGbzxIPxpA8fYyCbhxUaJNWym3dWvDHGM1pAEGnG-83xb-o45S1IdBVQwL1Kd9NgDbD1nnQHCunN9gnDwkKvwxmUbXNbbTrgv1gKaXKzMbQk17bGRDLUbvH_Lja-mprhNnRfk1fOpY86CWE83FmtS4g5vs1SqGDdexo2XceNl3HgZN17GjZdLDlTaFuaHjlXufLqzZbP36fYRS3u2cd48LWv2BI_LevQDlwcUPLoVXOGMuMMCd7WMzCHG-a-_1rIfvGe_PHnz5qg0pENfCK3Yo9xtFwnzexv44l9B-6UVYDcopUGlkGTmjhFkYGnYdQwXvXz946tZUa4NfzqiuElFNEYuejSFkdHIE4Ki-_36V_PDjgDeiqLmYwasQ34TEItqa_cDwHIrUR97IFHIILxJ8ESS8PDeTy-8Dm8XGKRbR3oruDetXh2KppN7A7fHImjzHMcD8XG0eVt3bGbNdH1wF7xXQotLZaQDHb8vq3yn7V5oHDdDAzpn7Y7JoCF6nj060mol7V7aYHhdnTyQvCWQ1f5pbNi6qebydcPNPdGXHU0-8ruhgzsindB57x2RMZ-O-fRLyafnbx9esFOy2St4kp0SAiAam183CvwAEVeEITGn1gH9KqqoG2KlZSgVVgCLlfaw7xPlCx65WPrwkl24U2IW9GtE5547x8HATkn3I8bjTsm_0k6JZtqTAUceZezETslggbhMCunVgIukkIDBkDBWqBbP6l2XTcrvmOH903mLUqZGzJJ2l6RlxWVmRCgZG8iwaRgYNKz8tVMnClvwLctx6ow2bWVi8-Pjprkb84PnhvSLKrfaS5MqLfPnjoaoWNTMslHul3EaL3myD6AM528ovmzP3PTzevOjcXYOKVDAbAb_tXbY6P4Xqia9onahaoJDGXmAYrSUXWu9CralmtyvNm28UstPOudFmVfCWsva19h11kiNnSh1xAJDG4i9MjduII4biOMG4riBOG4gjhuI4wbiuIE4biCOG4jjBuK4gfgwG4hvPv4Dr5KL7g)

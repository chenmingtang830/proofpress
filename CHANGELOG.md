[//]: # (ob:88bec44c)
# Changelog

[//]: # (ob:a0ac1671)
Proofpress follows [Semantic Versioning](https://semver.org/). This file records
user-visible changes; GitHub Releases provide the corresponding tagged source
archives.

[//]: # (ob:45d5f7f4)
## Unreleased

[//]: # (ob:ca6a4032)
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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzg5YzhhYjE5ZmY0ZmQ5MjQzZWE1NDQwNiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjRlMjQ4NGVhIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8xZTNhMTM0OTNlNzAzZTg5ODgwYjM4ZDgiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhmNmFhMWFmNGRmMWQ3ZTU4OGVmOTU4OSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXNmS20aW_RUE_TITQ5YSicSS7CeNZMuOcNsaj6ano21FKdciWiAAY6kSW6GI-Yj-wv6SuZlYCJLgVqqqkXr4UBEsEMy75r3nXCwfJ6yoYs1EdR3LyXyS59cRFRHjLtWaaEkx8RTzCUHBZDrhmVxdy_hGlRWcWy4Y9oM582WIkMe4oEIQxiNXSxF6jGGBIo-GPuJ-5CkRUo0JJSHCVEhXKhkhxXUUwroyLkV2q4rVZP7R_FNdV-wGJCSsMqKm8IGrBA78SRWxjhlPlFOo27iMs9RZwPlZsXL4ynldZJnOC1WW8JuciffsRhmjNg4X2V8VmFsXZsFFVeXl_Nmzm7ha1PxKZMtnYqHSZZzeVCy9iTz0bOPXhfq9juHzdV2q4lpkaalS8EVV1OrTdLJQzDiRKEwiotikOXKtbu1J4Fx17SqPuR6hngqRpyIaRYh7kYyMZllRGdOukzhVoHkXkeQ60gFjLtNEaleGyo8ipakf0cacVrtrwfKyTsBgbPQUWSHLyfzXj5NW_McJRDkrSvOp-VrJaw4u_3VSp-_T7C6dvAUbunwA0S--f_7Tq29__PnV1VJOpmdlCquqIuZ1BQG65qyMS5MvKtHXrATHVcquV1eLrDDqvI9Ts2S5Kiu1hG9StjRx69Sawk9LE-vJPK2TBJQUCwiOaszjSSbew9lRxJUgRMDpEJdKfbAm2BOT7AaOtlKYlFZ8bjJI3cGRb5zhadUqN8JN5CALJp-maxEMMeEGoXu-iHVmOjpLkuyudH79T7VkaRULB7LaWAfS3v5Ll5ClWsKGuMqKm2drnXJWsA2FRKRwqFC0odB_pYVKFCutCvuN_sbZOPGA2Zi6kSSIbEh53q54QMA3TnfSgcUR9RCXkXve4jPndbtbnDbtnT-5zh3sYqdsDtusd354WToslc6yTqp4Bv4zW6HXJ4HSselPFXJOMD1PGceJU5HUxjTnLiveaxvfasEqR2ZOmlUOVAvnVVxdHQil5wmfuYjd1w9T59v0BgxazBLIxxrqh5NpHYuYJaCFqJdgOTP70foDvk4P-MF3dYiZiEYS_WjM16cdiHoopBBYuecKmDlpvrQWvF5B9UidFz_-4Nw2-wciXSiHJfFNqsDCynmHrvAVegc7roBoqEP2KkoJt73oLHUcp91BhyIbEKgZMqTn2_pmoZy85gnUiM0QxmCrMJ9mOi7KyjqkyUFVOupDnhywNdQ0hG6iz7c1L-JbJlZTK65iy1wVM_hWqlQoh2d1KlkRq_KQL5RwFaZabghHV-4Vcv7xP393MMLBDIUzTI6Urj0_OZBximEWSvR5kmfOd9bfbY0xudglwG_poCb9kRXvJbQu66nSBE0432_H5O20a82TNoOvRaFY0xztN12nVdcMvKY05siLQhYwEbqSSS8wQYT6Yl3dyW7RgwM4RrzPs9gWvLby2f7Z_Wfa51sDOyC_VoMVhlBksIgFOfdEKWWmq2sNIVEFJFELhkruzjkJFaEhcoVLQkCMVHsoCkSgdRS4PqKRxJJqoUSEKVIChZh6kQgiaMNuKAJTLY17LahpwjV3CQAEc2TSxzR44-K5G819_G8IzRGCX7UeNzkgacBcoSBb1kc_PhAOstnX4JQFKxemzrtCcCgJTEkDVewaA-jSJuZRSNKuxgLPp1gRLNerDVBKu9rnoI9_vYIyBPVGxxZ0W1j5W2rg78wAcNuBGzT2B9Pivq-580uzJUooGJkpD6b4OvBDUCDPUtsmAd9DuXHKrC6E-i1lhVjEt-Olo7UUMopoRgOBbNewlg7gT-e346im85znMVgxJDTyu_UGQKdf7yCI6WKqfRIGoAhWQbfWANe0a30OZulYji0z75aquFGzHBr9O3tmc6BpdMZvSaKS8Rr05o8_QiRyqNLTkRbRmUNCzRAX2LeFunH1Ghm15nwW6mklcU_JQAceClgvaQCEdhx3PsiB3ihZXkGOX-032Ce-8kJPY-H2agwg0CAXDoKbdjWMmCe0G2LMcbfaAO_0Rt0fyTgprNEmzX6rpPZ9wThyfdJn5QDo9GE8AGE6iwIM5dejvtBet9IA1fQW3R-vQAgrBxpMWR3ISxZFAZI8pJqx3rFrNNMb9Bk4pZUUQkHF0G-4J3qDB9BlXWxOxyGdDcpFIQQmREz3K6-hSe_Kz8AZZo9vT0fsz_6iimwmVa5S44pVl3gqvYFWbpcAQTNuSme7d0pV1fnOxnn7yRg0MlZQMq76oYLIpPoweWtHFLIWu8e3hhCD47_XqlwvVMTQYApp5jH_1xMK65X1gKJR-bTxxChVt9t6M32CNf5cZjLW8UMQ6N2VdmnBSYzshIVOozsnLDRKxtcrFGqZ3T4GEx8lg8fknsADR4nXsXXvW8tgH4mExcu9Sbgbh5ZIvMiWeaJgA9hOA7rM2pKesDoVi3VpMRoVKmdxAeea6MERAfsFnH-1L0OfUOogoZ9Q6iD7n1DqYKvsZNOjCR3sk6cTOthEjyz07WCbfpzcLVa24N9n6b5Lb8owhPPkAUCE_SjUPGI09Igr_ID5vqdc0Zs9ZPZDVjtk-x8vnenSmb6AznT6cKsf7vRRmZNpr9Dc-zQ-yTk21nqQ2ZUv3dAXVLpBFIHyFIQThjUPYTv5gRtKLmREuOdjol3ih4r4kjGhfQV_sP5p5u1Msrw5CueuPzLJ8kNJqIvxZZL1RU-yIkJw4Ac44KF_cJK1pwY_zUzLR8T1pBcx4smvZqb1W3qfOrs9Z_innEr5Smvhu5wQ4j_KVAp2VhNyE4TdprNtXejrgBJCKXb1o8-UjErn96sdlS9ToctU6GGnQl8aRB69C-EwEnykWxBGwfoxTR7ugvn4_OSUScZPWbGEIvk3s13kX5kwO2aTAS7hPyiptm5aMCGqDnAUZhfeb5bxGHIH6bCPbT-G2N0hyuOJHaP56YMsfha_9xmOEJIiQMT3OEA44XIBkHgfv--x_nF-f6kxX26NOX3KM0IV8YAq4k_jTPArZsLb5o0wYRfPydg9HSTCnkSIXpjwhQl_NhOGJYj0wjDytfqnZMJD8vBVcFkJAYEqIiJif_1EXNa46cJGL2x0jI3-0rDRR2aiICI1T3rAd1b4A5NR6Mq-DjV53KcJOBFKK9d7lKcJPM5D7fr63LvoXxZMV87zNj7mQSLIHGb2InysMpElTSlnpkAsWTVjN2lWmlQ-AC8x4oh4bOuu8myZwx7gcRJXq6P30m-dfMByXygK5YDcT9jM-fYDqG96xd79migJyG_atbepU6bwaZGdRp0HybWlRcvoIEqmMw7yCLa2LalX-_JnfKFXRVbnpZOqOwNWmuCBzsx6wdbUPRkzvtwvDT6ygKev0Cq9BRyXgxMKdQNWm-fPmqLdlnTTa0S2BDwmtwQOsuKQI8yv17Ebd8Ug5od1NxenbVt1UljyFjqMWrDbGHqdbT8WyqUA_26bb6GEAIMVznZDWu3hy10rbO9NHPi9rAvYUE3hjqvS4Uy8v4NCWc42zesEgGKwwVTXSc6j0ASIpcc9RqkARK6lRxRRLt92B3ijz7CuIltY2-74Ya4Mbp1fk4rjlPtSSS-V9GEq6eljou3nIPxP44z4aSYCijGpkcKBh7CLPQ7_ay9UHpYBQNZIc4YlVTJEFHuwR90wYCECtqYY4HjF9tizOQKgb4D5-9EceSMjAE9ioONIX0YAX91jHYPq-SCPdQzq5FnEX-oIBQITl6xv5B-UxZ4H3b_k7eIJww17unhrH3cXDcNMoBQkZYMuWsb9rI1EsYNCDMyxw4RhX7ONs50pDI5bKat3PVxph9prPGB04qtKzawKa6XtEGDVpJDx4gGyqhVmLAxhr0f9DGVQ1If8_3ih7tbkVLsR5jSg6-cb1rW7D8_963HVeHsYBuuLDjzFA2R15bxqUROPU4Nkejel4DVwqIXE7dUBG-ay3apTB5Zqcdk6LAeceRmbXcZml7HZZWz29Y_NDN74AmZmixoq8X3fO3IKUTrhqug5rGPfcuOTl90Jx-7NA03AnJc_v_hz35eaGvDyuxa19PXqyAhid3HQySCMrYnGdmd1hIIv0ptyfMbQcnc7YWh6pVW207FVrttLHXi9OmuCAM2P6sj3XI20FERSqjQKNN53Eb7nGMcnAl9Wlpw-ORm7LvtpnGc9CbF0BYAepXyKooAhc7VZU8SBCYvI5cwXoLwWfqS4q7kWLuacApvwmcBYeppH-03a4ZbBHFGgl2PcknoBdaW8cMsLt7wnt4yYjmikQgXw4MItT-CWRuK_13FSzeLU-fnnPwMS-m_TELrCb2FSl6C97tY3gqWQrAKguGkZRuKG8Rbbl3Vxa9LJ-csPr-2TW-blcZYDLIwKUlVmAA__27IL-KlrMBt6mU5kEv4mje3SVnxbIaYQCFGs8sp-tsWwiP_Gmn-N9jkUR6OcADcbbgPtpJU-dFiyAgkVi83uG3puaNITE3ESeTIMAq6oT79AIt5BhDFCfjof_0ODN4ThkUVpcgo0j5PEaTEt7CyzQd-ZkLzbybFu2yWrC6-_8PoLr7_w-i-E148z9a_3LRssYAR5eOtZZm8r4p579P1yoz_5zOulJz1arF2PBurR3rzIBORuZK8Ynvs2QlUsoaMmTlZXeV1BzbwzNbNcwy5Ao1l7U3zTP2dNQz9gb0QDF-jIptteDmvJMau3Tz5ke0iUkuE9hRkAk8OWa5_-_-75fzhV5sgG09TQI0bvJtBFtnTuTpvUDLJ3_H6OF3VzjwUToHNtXo-8cTeD6WsOKwfvQW4S-dgdL7sjmx-aWm2FNa25HQL9XsfATiuwtHvHgR0BWlJnGkoJTEClBrKVUPDt77uRjFm6vNqX7XvvhQFq0978YhNrg0YaiT0IHIx8RtN9XEIX_nUWV12et-ls7LyLC9XfsmLKO_zGQEyIPiATw1M-bEseZPYh2zb7ZmcpJNYR1w1y-dC9P81tS13eDvISvm3et9zAL7XMBvcwmeTec69PbshR0e6BBuMquamojdN2Dp41iDvwluzxQVw3kDnhbReXDnHpEF9Hhzh9Or1zr8x0MNx0P43PLp9kXhtgTHwMlIj7QiHmUkRVSL2Q-VSqMHLdIAxFiJEm5j8ONkUKIexRCtxU--gU4zYmt577xo3mnnk2aOzBoO7V_JfJ7f-nyS0JEESKCspRT-EGjWBIDk-t6o8wE2Y-J4FwvVBE4jITvsyEH3YmbJR67lR32Qx6dF3tx_VWwXx0XmEHFe18wqbO5gXjLlLTo9zgzNnYAPOcORsTfiSRDiklIuxr5hrgrF8zcm_o0sSpT--dVIJCCI7uwmYKM4TNBAqIA6RHHudQGxupNkY_ddRCJRVwufdK5U4VL40qtVgYevfOxdDX3gG_qsz-h0U6GtIqbyIIH23iGB_ZIrxYT2INm-mu6teGOPIVFIF2ON9Hvmt9h4IlieYhEdTnqh89DgDbIFgngLD-vj6BGUTIU-46ZGtcNriccF-sBTS5zM1jCQ3tsZkMvRuif8tMrKamuU2dF_j186lj7gWxkW491pbELd5mqVR5ufByufByufByufByufByufDSX3h5--l_AU9hXKw)

[//]: # (ob:1ce270d8)
# Contributing to Proofpress

[//]: # (ob:61836140)
Thanks for your interest. Proofpress is small on purpose; these notes keep it
that way.

[//]: # (ob:57a5f00e)
## Development setup

[//]: # (ob:04d2b288)
Python 3 and Git are the only requirements for the engine. Node 18+ is needed
only for the npm launcher tests.

[//]: # (ob:08829457)
```sh
git clone https://github.com/chenmingtang830/proofpress.git
cd proofpress
python3 -m unittest discover -s tests -v
node --test tests/npm.test.js
```

[//]: # (ob:31d45337)
## Architecture constraint: one file, zero dependencies

[//]: # (ob:5b59c3c5)
`proofpress.py` is a single Python file with no third-party runtime
dependencies. This is the distribution model, not an accident: recipients
verify handoffs on machines that have nothing but `python3` and `git`, and
skills vendor the file directly. Please do not split it into packages or add
runtime dependencies. Internal section structure (carriers → blocks → diff →
ledger → commands) keeps it navigable.

[//]: # (ob:5fd936ad)
## Scope boundaries

[//]: # (ob:a0be59d8)
- Proofpress versions **Markdown and static HTML knowledge artifacts**. It

[//]: # (ob:56bb32f4)
  never versions source code — that is Git's job, and features that drift
  toward code files will be declined.

[//]: # (ob:c46dcd3e)
- The executable contract is [docs/PORTABLE_ARTIFACT_SPEC.md](docs/PORTABLE_ARTIFACT_SPEC.md).

[//]: # (ob:bdaa59b0)
  Behavior changes must keep the spec in sync (same PR).

[//]: # (ob:f2c66c00)
- Privacy invariants live in [docs/PRIVACY_AND_DISCLOSURE.md](docs/PRIVACY_AND_DISCLOSURE.md);

[//]: # (ob:0e2e65bb)
  changes that would leak local-only history are not accepted.

[//]: # (ob:327a0850)
## Wording discipline

[//]: # (ob:0ed25c68)
Proofpress is **tamper-evident**, not tamper-proof. Public-facing text
(README, spec, CLI output) says *checkable record*, *tamper-evident*,
*provenance that travels* — never *immutable*, *tamperproof*, *notarized*, or
*can't be faked*. PRs that cross this line will be asked to reword.

[//]: # (ob:23f94073)
## Docs are dogfooded

[//]: # (ob:ec80f405)
Every tracked Markdown or static HTML document in this repo is portable and
Proofpress-managed (see [AGENTS.md](AGENTS.md)). Inspect and import its capsule
before editing. For a meaningful revision, close the loop with honest claims,
actor attribution, `snapshot`, and `verify`, then commit the updated carrier
and capsule in the PR. Do not push `refs/proofpress/ledger`; it is complete
local working state, while the capsule is the public per-file handoff record.

[//]: # (ob:69babc66)
## Pull requests

[//]: # (ob:578fa3b9)
- Include tests for behavior changes (`tests/test_portable.py` is black-box

[//]: # (ob:593d02a7)
  through the CLI; follow its style).

[//]: # (ob:9950245c)
- Keep commits focused; explain the *why* in the message body.
- CI must pass; the full suite runs in seconds.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2FjMWJiYjAzNDM4YjgwYjlmNDdkN2YwMCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImQzZWNhMWY1IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85YjA5MjcxNTczODM3MTJmNWFhMDFkNjUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzdkMDNkNzFiZTQzMTVmYTcxZGEyNjUzNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWutu28gVfpWB-mMTryXzPqRSFPA63q3RbNZwvFsUUSDNjRbX1JDlkHa0RoD-6gMUfcJ9kp4ZXkQlNuNIadEfBoJYIodnzpzr9x3qbkSKMokJK-cJH01HeT4nzKaUWq7nhjS0aBR7mOPYskaHI5rx9ZwnV0KVsFYtieMHU8KwzWhgkTC2XWrZth97Liah5zoktnAoSICp4Exg1_ExiX3KQ0LjIAoczFwcg1yeKJbdiGI9mt7pL-W8JFewgxTvS7idEipS-PqLKJI4ITQVqBA3iUoyiZawOivWiK7ReZFlcV4IpeCZnLBrciX0kbYuF9mvAg5bFVrgsixzNT06ukrKZUUnLFsdsaWQq0RelUReha51tPV0If5eJfB5XilRzFkmlZBgibKoxIfD0VIQbULuCkbs2B_VV-bixiwC04p5RK3IwbaP3dDFthP7hFg2D_TaPCtKfbR5mkgBmrf-SOeYWy7HNhWeC7Yl2ObECXwX18dptJszkqsqhQM7Wk-WFVyNpm_vRs32dyPwcVYo_am-LficgsHfjljGxfvROzhBGwuw8clPry8vzr77-fLs9Q-TFR8dflGgkLIsElqV4KE5JSpR2tikkFpRuAfxI4zIqlxmhVbpOpFaqlrDnRXckWSlfVerdjhS8CDIGk1llaagKFuCe0R9QJpm7BrW2kw42OIhLAfPlDp04BjwqdZEXqEy246RZlPCudEm10ElbuHKH9Dgc-U618pp78Lt0YfDjRKBHbqB7VlfQYlLOOO1QnFWoHVWFSgBcfBMOek9jxKF1IqkKYJUyKsiz5R4gcrlRsmcFGRLQ0hBH5wktjR8CVGSZvkKQgUpUVb5oHX-gO5bP2AVy-MOdcJw9z3P1xApErmISI5-SEpECgHnFHDudI2avNSiaoPpO0JeQSZN0OsBY1hh6ESej3dXbLFYqOUMtioRSzMp0JfUlI1mOtC3NHNt7vmuu63ZccGWSQn1q4LT6_JTFgTCYor0xnGSikP0mygy9BnvPVYMF7mQXEiWiM-EvU_9iLnM_-raLjYVbpKvFzreCVKwPfSAJia0JHQL1kYyA8cnBR-Dn8s1GkqCmEduQPiWvm9YlgtEs0pyUtRHHrLiPcsHLEQsKvzoo-r0JTuO-2kPvVLXQ4UODn4kxTXPbqXJDFWSMmHoz5c_vkLXMrtNBb8SiGxUS6FdblsioNR1Ym9nvRCSkC_FRiUFxYpph3OBfv_Hv8ElpNR-g6z9RqFfM3poVI0FgcAY8BHzAs6gme5hsUtdBt4LVpnOqmMQQpAZbd7yjKmj858uLo-_e3U6P764PPv--ORy_ub89KTudw9ZjHJCfGjke1jsO7EkNwnUqaaPoVWlSnQtRG4ql8oFg3KP1Foy9ExBK0TnF88nA7aKHRYEzLL2iq7khrA17HsDq4mupGlyI7Qeja0uzn45Pvnb_Pj1y_nLszcnr3568_PF6bCtLOGIwKd0D1u1JjJhdJtVKUepINcIdiDp2JT_FgPqniAz6A2MibwUA_ZyHUys0N-2118BFOkOrdFokmsY9pkKcO8DQ21QcMdnQbjHrtut_-CgJKtcFGO4DXW6PDg4NAZorpraCXChomnCxvGAPRw3jjwLu9t9ELxubMqzqzjLalUGUcF9DwzYQ7DQij3L32PXrvpBiFZ1_4eAhS6gABTkmRG0sdl4RSRAaw5JJcRMDhgkiCihkFNbqp0D-DRYA1DY57rDx2uHmicOY-LSaLe9xuhMsrSCYqthdQ1_6Mf15dnC3DzS_89bpjHJh_pC5HLLIXg3pRC4oMiqq6WpZyevzl6AXmma3aIEVFTlOhWD9SyKfMvxfLarSf6iSylAr1ViLMKAr_EX0ArylJjwEOjgdrk-QM2XFcQGxAXUpE-K2bvDlkGNmg43ZwW0LrOludPyITG3LSZ8XwTU94THAkbiOHBjXwcRZKU5aGN61JA8cJBg13kGsMhw1sLspElO-01znHeaHUIKr3sS-oyxJ8Rw0R3JpMrich5DdIoiL5KGsypqT_0IW9QOOY5CEQOM4dS1HeH58JwdcWD9viAOjx0cModZ2OcBsXAQCr2HCIk-vwYmhnvW3po6DrA4fWXkWE4wtvDYCS4tPPXcqRN8a1lT08sai-uA8BwuPGgkH3pX774eYTWBV_PJJVFLWI9918MkdEgktHGMjB7FbGLyy5liI54zK8bEttzQdlrxPfLYiN-HAwpluiFkvwEWSTmTdQ8l6_tSrz02DSjxbXCTz1u9epSxPfajKWAjltDYIsTjPDBN14jtscI2w_dgeRpu2uG32hpSCAiymTRPtQtlvkIpqSQkS1GXyiErYO6xmFmey2mn7oYrNuruxf3U5Eq7hHG0uTSTubGAi8YrVMnETEpQOx1DY9XU-PHNTEp94PHYrKiLO5xwoj9NfgVBoNs97LI5XiCEhSMIZWz77fF6hHPj5K_HFJud3QjbAruuTyjpwmtDHlvD7sH6ikqWyQq6e1-nCVCBxGSKDgU9YWzHU2gFtklr2ESkho4GSU0h2gCOJTrWZvJGDx4BZ0JYZnGsdKKtCFhGtrgU2q1JtqUuAiAYLRpHLkwoL8DVC0N7ZlJdJ2mqGRzIqiPTHIVDZLMyXUNmA7xVGv4YnRRAQiAspU79DDVTTdCgQJCiM9mcFm0f9kyXCUlSSExmDgnnrWonPmOkANBdKPT7P_-F6rJnPvIkjvWHmTSksTAXdQsFrdVzU0OU1kMCsrgy8OHh9KGx53HoLdAEWOflDeXexNfjOHQr1cahZzkOERupPVrdSN2HJzcNQx0cgA3Le9BRo4lwqUdtG3uUe935NkS60WQ_ZtyGFofQgzoBiCq7JQWvn9YhoyD8oehT7Xym-zwf8IjjUQJtP4iI1eVdj2B3ttudMb97Nny_j_c-tidmIWUhw27gBq12PZrd2fOr8eZm39gVYBaOgQx2TbhHpXsRtSs3bq3y0P3nLwaswgNhE2CqOIq6JrQh1J1VdmfIQxFjB8yxOaY44t3uPdq8yeHHsuC292DhBxakMIuCzak6YtwigT14LmEGioGgmXx2cXr88sfTQxMbh5qJoKwq86p8jhRZg2SDnZtXSvqtCEj-eLPDmTyALaBiE8lEbWbICoA_6sDkcZ3mB8lqVafNRobRTH8FbSFyfhNaflaAQEbkN6VO3phcw1XQ_qLxICsypWoKq43ZZTlRsFAjzELcgqJD5dcn2I-CkEI-tSbuMfwehnskYW_Lnk9ZHPm2FftxK7fH4Ru5e1Hyt8c_nL6-fGMyp_v4_DmU47hGwOcXwNaIBM1iYEnr-kWg0PigFdRuC24DVKZqAJlmWT7tujLawhdISZKrJcTTH3Vd_dOixhWwUGMr89psJntvtOoqbYqMEV23y2cPCYd1C4g2jVLggJ-8uGwiqd5Ty9NGGnCuZ0e-F1outjZIujet2Dj3EROItjkQFnNfcCty6Qbzd0OJrgzuPmioMRxNAb6Mafb-4Zrn2raIMVCF0N_gw80ooqt5u40XWhNGnrAYERZlHcfpTRy68-4-RVhPZnKMTs7qBpUTpV7UUE_7RFUAqTVONYkBEC0DhPVJd3z3QWt8z9tbweHxj97dmjfBvGKfXr__XW_9Ktu8hm1uXCTgwoL_f7wGBiuagcgOb4G_eKYI-D-Jk37lq8MFbMTAz6sHxX_6fDPkeSlijcZQ80ZeNb2qASgJ0VkZQxGpyUhuuhbqNZiGZpgEa4sZMTCedbMGgJOTWsf2kHcjiEX9Cl1o_UvRF95ospFcZCskgMFsJGYFQFCDGHTE56ko28qmRy6PHoEN_MChtk5_ttWf6_TnXXf_dc8-fnDXDa46aVP7w_2Tqc-N6b7KLI5im-jS7DsOjmMojVjYFJCa44RhZIXwlzDXjjRMZNzTMzsSAUcSAZAVO_DIw0e6bxoXTO37pnHdT1yepnFP07inadzTNO5pGvc0jXuaxj1N456mcU_TuKdp3P9mGhdFvkN8z498gh-exp3qn9VrAzGtb1d2IWv7VbelmduTOvjb_WDBdMsHxnbo4amd1J4uTSFNVlqYmdA0fHQmqQBACDWOJxqwT9D3upP2Bnzd7_wP0fYsb2tEV_N0CAwzJEFbo7pFO9yrOz5a1OgBvoEo2Ux3jNgq55rToqYlgzTZcfh2xHN-MQE3mWjPK7VEC2Dyqocij-puvXhhMILqqDS0cUOtIVSudTpo2wNau11qsKEFd_tsDwUg7g0eaYl7nRVP08Gn6eAH-PcfIoQPDQ)

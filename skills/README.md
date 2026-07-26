[//]: # (ob:df70df88)
# Proofpress harness adapters

[//]: # (ob:93121540)
Install the adapter for your agent:

[//]: # (ob:1744e48a)
```sh
npm install --save-dev proofpress
npx --no-install proofpress setup --agent codex
```

[//]: # (ob:50c32349)
Use `--agent claude`, `cursor`, or `all` for another supported harness. Agents
never download Proofpress implicitly.

[//]: # (ob:666c5555)
## Every accepted edit

[//]: # (ob:a2f15f7d)
1. Work only on Markdown or static HTML knowledge artifacts, never source code.
2. Read the policy; enable `portable` once when requested.

[//]: # (ob:23c62cea)
3. Preserve anchors, run `anchor`, and claim only touched or removed blocks.

[//]: # (ob:9d481ea6)
4. Snapshot meaningful accepted versions with `--why`, then run `verify`.

[//]: # (ob:c8f43a25)
## When needed

[//]: # (ob:a8bc86e1)
- Before editing, `capture` human drift as a separate unattributed version.
- On receipt of a portable artifact, run `inspect` before `import`.
- Use `--rejected` only for consequential dead branches; never store raw

[//]: # (ob:c969f88e)
  prompts or transcripts.

[//]: # (ob:a64c64a7)
- For parallel copies, preserve every original, run `merge-plan`, resolve only

[//]: # (ob:1489a2e8)
  genuine conflicts, then run `merge` and `verify`.

[//]: # (ob:f20cc96e)
Different artifact IDs are ingredients and use `merge-lineage`, never `merge`.

[//]: # (ob:f5f3a858)
## What each layer knows

[//]: # (ob:8a9fcf71)
| Layer | What it knows | Attribution rule |
|---|---|---|
| Skill | accepted version, claims, reason | supplies known roles and basis |
| Hook / `capture` | candidate or explicit files | supplies only `recorded_by` |
| `ingest` | committed content and Git author | uses Git metadata |
| Capsule | admitted records in the artifact | preserves fields; invents none |

[//]: # (ob:041482f5)
## Manual adapter paths

[//]: # (ob:880f4f15)
For a vendored `proofpress.py`, install adapters manually:

[//]: # (ob:0e468706)
- Claude Code: copy `claude-code/proofpress/` to `.claude/skills/` and merge

[//]: # (ob:225dd61c)
  `claude-code/hooks-example.json` into `.claude/settings.json`.

[//]: # (ob:3e5fba6b)
- Codex: append `codex/AGENTS-snippet.md` to `AGENTS.md` and merge

[//]: # (ob:3ef5e70c)
  `codex/config-hooks.toml` into the Codex configuration.

[//]: # (ob:9d561c7d)
- Cursor: copy `cursor/proofpress/` to `.cursor/skills/proofpress/` or

[//]: # (ob:9cddddf2)
  `.agents/skills/proofpress/`, then start a new Agent chat.

[//]: # (ob:2202e132)
- Pi: install `pi/proofpress-skill.md`; `pi/extension-skeleton.ts` is an

[//]: # (ob:cc2d6144)
  intentionally untested extension sketch whose event API should be checked
  against the installed Pi version.

[//]: # (ob:c883ac9d)
Adapters expect `proofpress.py` at the repository root.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2U3NGJlMDlhOWQyOGYxODU1ZGI0YTAwNyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImNhZDA0MGE5IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV81MGQ4Y2Q1YWI2OTljZTM4MjgwMmViZGEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Y1N2FjODMwNGFiODk5NTdjZGM2MTQzNiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXHuPG7mR_yqE9p87ZKTp90MOAvh2nc0CcWJ4nQsOmcWITRZHnZG6le7WjAXbwH2IfMJ8klSx2Q_NSO2RNGsdDrPwGlY_yGKxWPzVj1X9acSLKlVcVNepHE1Hq9U1hF4CVsxj6UTKjnxfJh63rHB0MUpyubmW6Q2UFT5bzrnjB1PP9qSMYs9y8Z3Qif2Ih1K5lvIsEUWQcMXxAhe2cqwgDPwodiGOwlCCtPzY97FdmZYiv4NiM5p-oh_VdcVvsIcMPlZ4e8ETWODP_4YiVSlPFsAKuEvLNM_YHJ_Oiw1LNuxdkedqVUBZ4jsrLm75DdCQti4X-d8BB7suqMF5Va3K6eXlTVrN18lE5MtLMYdsmWY3Fc9uIte63Hq7gH-sU_z39bqE4lrkWQkZaqIq1vDlYjQHTioUXFqexeNRfeUa7vRDqFq49i0ZCenzJIhjAW7kRJYDieQkWV5UNLTrRZoBSt7Mx-Ja-SEXKIvHkyiO_VBIEdieG9TDMdJdC74q1wscsENyiryQ5Wj6t08j0_2nEc5xXpT0r_o2yOsEFf63kcglfBz9giNobIEm9zZdLMrL929e__D2zWQpRxcHWQqvqiJN1hVO0XXCy7QkbfMiI0nxHhoQ6CbX1TwvSKbbNKNWyw3eWeKdjC9p8mrZLkYlvohtjabZerFAScUc5wfqESaLXNzis1KFllRRhI_j1FRkO9NRZxTM9M-45KsKCppQ0yuXUouzIrOCe7zyHRt-sdqsSDyaYDSW0ZeLTozYtR3b96znEOPDHJieCYbTW63xfVakYs4kiNr8TQ_sHs2WcfwjBGCrkr3lnZQrXvAtEe3Q88CL-HOI-Jn9kW-gYJ_ZX-e8YmnFbrP8vsTfrzsbYAWaJvt8lX0ej8ft__izE1Ib_5aUviVcx_XiLSl_RtlweHShIEsdmsPv2OOnByYuCALh-9ohHdXff4HKC2Ag0wqbptmAj-id6N8VL26gukA1ZGxmppKNx2YhFlfZbwdmizvK9lUoj5XLnrC_5sUty7PFBv9C0yhuZX6fsbxgZcWrVLA_fHj7Rz1vC5A3wJqVXl50Yi1wKFtiOa4IHAH8WLEYY-usSheopdUiFWmF0tXLWk4GtBHaVqzAD47t1p3g0gb033eAi6ooUijGGSoBf-oucN4E-qSS_Uerp1mezNgSfw1oQ0UAocWDE7Qxk7zi486lj1M5-09jM7VQswuUTrL7Iq2AzXNcoxUTi6GVHksvsuF4sbwJ-znDnWWeV61vuWBL4BmatVovGO7a5IjKf_3vPzN8BmgXZ2je2roG9BXTPMahOkFfpIrGdrTxkvujPW7IfESkPBdxy7H9-hP2lxLYjBYvIQmQs3ph4dpnGhH8Y40bbsoX6KS5ZElBUwflhP0JBtTh2UnieJF_gjpWvJqXTBX5Eu26XJMACKvWet-slzp5p4LfMzSx5aoqL7HVrBTFgLbcOLZ5FETHihVM2Hsy3ztCbpuZnrICCOrgRlGyfF2t1hXZUIIrcDlhr9kyLZe8wi0uHdAWt6JEJZZ1grYK4CXqpcpxYWdrcnbkkjna8Bw3s9LY_JAl8SgRUQD2sUKEE_Zn3BhBQLqqWK4YZw0GbB2wWf1pVq7Q1mYsqbeY2ZAjciwh4gCOFSvC3YLARElLGY2olUnkqxTxR0lNaahhZNSTWoPWAbFQV07g28kJU5YX6U2aoUjaikgvS8BtdbxaoDQfXr__8c0H3FP1Avj-z-_-ZzKZzNCiEEEPTKLylcsjf9vAf8pwW1wsvoItuqcGMEXEYyVUaB_aPgG_bLVkaf0ommRaMjRNspd8uYQMX9ArfsJ-qpqnSqajnoHh-gCOfIhNnyDObDYr51dZTyLUdMnvYCzhjnVbFj3yEW9l-bh5Dm92AhGc33YwrhPZ7gOzeIJAxgdjnJTpLXAtATfH7sq6KPV2iX6vvYhNzshND-jHwmA2cpR_qDi_x344-rFM5mTQs04jk9UGxWiU0QBq7XTwwmY6JAx4QRRawaHCjNn3WiHse9T2lNbtBkGnvjSmCejFtJcz8oCzSX33shxCOI7jSxnY4lBx2Hbn8zy_LcfwkS9XC5j8HZ3wDNWzJQVUBJpLvDm0NYGvEh4kR2iHYsop4xiQoyOZ6RDz8vWPb_704edxmaV4ucKAt9ZMfVn_RK8zoB0XlI8A8CjtaAHwLZXejLV6JlW-XBi10KLXErP6iXXBKaKaDII-H-fpQcDwNNXoddPajP61y1zqG4Yj0PeHoJ6Q-J9yjlDNRK_ccqsnI8kFaSajAAbBBGcZ3LPX9drHMHRIO45jOWC7zuHaeZdO25U8W6U9ccZaQDKTV_oONgoZAS-8AQuoBrQjhIOryvMO1w6aByHNPCNHQrGUZlVY2zfDvglJ3c9z9JaaB2Kv3_2EO_ggPo5cLuKDbed149kQkSNUeegCGa_M9rXKy1Qzdnj_8Tz9ctEQViMTWVwLhGo1W6TvNOwTXHNueVzJIIyljJUdOW7I_UDH7wjjdJsNdjGcGtoGiNtVjprTFGGheyJKqflFjNIvRMZhVLHptdAn6HqNaOrvSO6uzFV1rdDRQbEqUkMRlok9VXboxUnkJbYfBIDwBCLfFhIC7kmwwZUKYbkIXVcFCuzEtj3fSWwQQmJckySkKQrrNdVXT9TUdb6goomEQ-MPxlY4doIPVjj13KkT_cayphpLG40TTkCTjCM0yi-9q5-ekR_U5lbTd3OOBjkdySiME5kEIei51m30GD1jiUfwcqZ9haDY8kI_Trygab9H1Zn2TyHcHrIqV5mmVVqcbBRJSK6sqAuFzSOAoz7J7dMNHUpyxPllNQalKFBSuPISxHUTigOIep9dZfRb0QSwHzH2NRx4TQ7QKoNlAjTxzJDChugoOzDf0uawyTN5lWEzu3ym0R33rNAO3UQ6gdPorschGt2dxgSyn7XaP3caNfq6IHyXLssL1DmOcTvGroNwavczK9e44miUPS4AvcwCr5BiNA2te2Z_IG1ftkzcDF8mPQp8LJXobLAvLpdpRVJoRqyoo2uNJ1vKAScAyn6_evJmPXZ9VnfXzBs-S-C9blcbUlZHT9R5TYXT-I2ywATzdHMJFSd2qG7vXRuSmen93IlrqH9qhaOjksxAiNYKP7OVob9K1oiKQ4GFLF_hlkIutmRZnmGru8hZYxGJxXFBWVEIidVYRI-vbVbrExlY06gDyvWA80SKttEeKWsaPYlmNS7jd2NUglqkN_OK_Zbm8XczVubY1obN14jNmSxSVeHqwPki88FomNZEBbjNtvODy8aYqF7D2XT_AkpciETsRS7ESTOyHq1rRnYKUYsA6I6Ii3xdCIrVJUyuMmfC3hMJtWUA9d42YW8ybUOzxicQj4WvasdGB10aTbyiZYx9b8i6d6AYMz6f2z6Pkgi3Id6Mr8cPm_EdyPg2uostR-Cmh_touzH0SGDT9im0Lk7iq76C94_TgcjCoCPEoBUaWXrMbzfOo7lcdHSaSqzytV6-OVqtpquW-R3-rPfNAW1ZNtixDBwZWe0a6pHARsLTaF0K_PHGfVrNKbpGtzwbUJnrguU6iQgitxWoI387lR1E55rGAwRGtiNdFfF2tD2G1zR-CmdLiyrNFP7dvLt_qJHr27FtJ0HQ6b5H7HZDPZqqTfHfA-pQsU2H67FteaoRoEfhGgFOIWUR39-lEtBRoMch49mvDRl7gS0RlwZW5_M64rbTxvFUbON9PMsHJcBFzNr21LGzpqdT-NZ0SY_OJvtHKzxPBUEcWZ70W8_QUbFGhlPIVdR4s3PX63HAHYcBwj-lcHdpXWaPgO1UfzSluiEkg2acovDaQZkDeXRq5a3ebyhFgvEErYlhWL7GIWgCA5d3ZbyYieC3fKJuqxZiT_-122yMd8J-SBWuTo2kGp399ANu2UUtF_ozxB-pRjX04nKNfnZN3qAeqdHtrNlA68uzAWuLlJSRiGzbj8N2pjsauYM-gwRx4x0jW1jKcsATbVTS44x7UcmxbDCOkd9rqzJR0lVWETzXOnjI1qIaCAbd1CBQK4S2ykVuQIRpkeF6MBv4AOhBNGeF6HmCwGnH1iOgzdhOo5abULCEar1iLf1LfNlVhk3voJ6brcMK4sQOlS-EaH1lx0Yb6U7hmbXGjBPDEAGXOkFGg0Bpd3ktJb2VcIJybSRt9iaNwx5QJjgV2Ng918aM6BNDUnIevZAYVYIInhOQI2QzYMYyimMHOMSuaveKHv1txv-sxHYTTdKmHYQ2SM9ue-64btPzKSy2pibqjU0v5_2eMkkC3BAkeCppbbRHdLee8ngKG28ORdaxrzzLigWIduvqMdudLo7mrL-mAdviVuzEoEBZnQQtmd3TwHPR1A1StUQsIktRnmCHVFvmuhv60Zx0c79_5PNw-BwNPk4ShJCi9eY9wrob_nNS0Y3qY2FbiNYhcJLO-Fp2utXA8bwzTkBVzmi34APRW-wlAiKEZbHXRm89WrrVwfGEc75eIKw2_Ct5QYT7N5zGpA2n2dckDrUJPYbwHo-iyA0CV0Rxh_pb3trI-1yM9BfqeUcWJREQD3ModUamXIvH13fnXNYppVqN5sb7FI2mkP9H0jG1zR-XjXl8GuQyl6lK-4HWMyYwPm780Zn0zrzD55J8Z5LhGx1et8QnWdZQo7sSDXYmCR7Y7tNS_E5tdGdK2qmN7kzr0qFWBlCfVR2mzl3JPU9s77FwcRCrKIKvN7brmM9QAAQxv8ICtMIHGE14PDymvzEjyEdNoj9emLj0YeTZxo0XW0HjgAoQV8bcgeg4FTwMILdCxzpg244KhzJ-duVHPXFmn5Y-pE8_gONGuNDnIfoU5FAD3Jk4dHDLj5Oqd2a4vNWgvXFoNT11sMAI5Tz0QQc0_I3yaHZmDHdSGGr1bEnCw5L8WnnBu9JvvyrJURm3O1Nbv9rVN8tmHZbkWyawflUnp-es7szC_Gq_v0bi5c5MxGFJvm0S4rAsz5l_iFFAffCzDz8_9sMmv-WtPhNqvKsZrI67mUqLsmaPb4p8vQJzCKgBPh2VNgeyVDindBCSic1kH8g-kwQ9JH4mCXpw_UwS9ID9mSToRQFnkqAXMpxJgl58cS476CKSc-mgC2MeALhvo4AuqjlH970I5hzd98KWM01_L9Y5kwS9mOhMEvSip3PpoAuzzmGGvVjqETr6NlbYhVDnEaAXOZ1HgF48dR4BemHUeQToRU_nEaAXRp1HgF70dCYb6EKmbyjAL70A7dPofk4Z-kt-C_VJu1Kp0DlcuVgvMeCq--I6PXjcdYlBdAqUYMdKwTPKcH9yxcHA5zvqQfdLCfpp9P3ygk8vxyUvxyUvxyUvxyUvxyUvxyUvxyUvxyUvxyUvxyUvxyWHHJc8vRD4YSGsd9H556ntXrTSTuMvuwtgv1YN_Cwlv7pw1xMYS0jbs0KQ0rES6cWJtFwfEmGHtsJngOopPN-jSAGiQDqJctBZcPvgkT6sBbbtqR9O7XBHLXD7PcP_P7XAiR-hul3Hkk64vxbY5O_XsanZkimte5OvizpH_sDk98cls-dKfhcQW1zZXCZOtL98c8-q3VqtbbJ761ebVPdmSiZ1MiyNYbugoDd7XT3BQNonhDxOXMsPYjveXx763Xdsd3S03xy4igOBHk04njxTdWbtYl4xeEpR5lAZkiDvHNmx7Yf7CzH7eM1As10ASZ9K1-PtyhH3lyI-lEVJy-ehE_nCjZ5WitgrQHxYBV6yfrlhP6B5HMQ8FCTAYFcACDfu8qwfVwmi4WzHNQPfEnCE8AI7dERX0_i44GzMtkuVL3oF5_0qY763wLjNhb7KxqcXr1EjR9VBvmrMtwGR-1XtWk4SxrbtSdFWlfTi-TaV_OlRepPzHThujFs7xGH7CYJe4N6q_PhwHNEZ2hU-mS_wSdLL_mGGivbjRHlO0NYu9GL2dpjPEYk3exY4cRQiNkBAur_AcH813KNKuJOK4FwZaQASJh4MFsHti8H3Ly6c0QAHFjkRj_eXxP3qH5sw0cOjz0o89YMS7cckvsU3I3Auyx0fivh-__ch0mz_ZyEO_hpEyG0n8nDriSJ_fy0ZWsMegmO_MeyqUutRJy9Vai9Vai9Vai9Vai9Val_wz78BCv5g-g)

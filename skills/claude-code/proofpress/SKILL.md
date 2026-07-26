---
name: proofpress
description: Preserve or inspect decision history for Markdown and static HTML knowledge artifacts with Proofpress. Use when creating or accepting a meaningful revision to an ADR, design doc, PRD, README, strategy note, portable .md artifact, or static .html/.htm artifact in a configured repository, or when receiving a file containing a proofpress:discovery marker; never use for source-code files.
---

[//]: # (ob:25f10229)
# Proofpress

[//]: # (ob:cb25a041)
Record accepted Markdown or static HTML artifact versions with structured
testimony and verification. Do not snapshot every conversational turn.

[//]: # (ob:d8284708)
## Workflow

[//]: # (ob:78295d28)
Before editing an existing target, run
`python3 proofpress.py capture --recorder claude-preflight <file>`. This
preserves any human drift without guessing its author or reason. Then:

[//]: # (ob:04e1285c)
1. Read `python3 proofpress.py policy <file>`. If the user asks for portability,
   run `policy <file> portable` once; it remains sticky. If Git history exists
   without a ledger, run `ingest <file>`.
2. Preserve carrier-native anchors while editing: Markdown uses
   `[//]: # (ob:xxxxxxxx)`; static HTML uses `data-proofpress-id`. Run
   `anchor <file>` and inspect inherited/new/gone IDs.
3. Write claims JSON with one honest entry per touched or removed block; do not
   enumerate untouched blocks.
4. Snapshot the accepted version with `--why`, claims, and explicit actors:

   [//]: # (ob:c89d4269)
   ```sh
   python3 proofpress.py snapshot <file> --kind agent --author claude \
     --produced-by claude --recorded-by claude \
     --attribution-basis harness_attested --note "<changelog>" \
     --claims <claims.json> --why "<actual reason>" \
     --rejected "<consequential dead branch — reason>"
   ```

   [//]: # (ob:3b3f299e)
   Omit `--rejected` unless the dead branch matters to future collaborators.
   Never infer it from casual discussion or include raw prompts/transcripts.

   [//]: # (ob:64c98298)
5. Run `verify <file>` and report its output verbatim. Never re-snapshot merely
   to force green.

[//]: # (ob:e96a23df)
For an incoming file with a `proofpress:discovery` marker but no local CLI,
tell the user it carries verifiable revision history, show the marker's
canonical project URL, and ask whether to install `proofpress`. Never
download or execute it without explicit consent. If the CLI is available, run
`inspect` before trusting the capsule and then `import`.

[//]: # (ob:50e05b0b)
For parallel portable copies of the same artifact, preserve every input and run
`merge-plan TARGET --from COPY...`. Apply compatible block changes, ask the
user only about reported semantic conflicts, then `anchor` the resolved target,
write merge-relative claims, run `merge TARGET --from COPY...` with explicit
actors/reason, and `verify`. Different artifact IDs or portable lineages are
ingredients; use `merge-lineage` for them.

[//]: # (ob:3bec4947)
Fallback `capture` records only `recorded_by`; it cannot know authorship or
reasoning. Never snapshot source-code files.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzhmOWYxNjA4MjZlMzM2YTQ2ZWI2MmJkNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjZkNTA0MjRjIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9lYjM2NDliNzI2MDA0OWM2YTM0N2YwMjIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2EyMTFhZDFhMDU1MzliODQ4M2JjYWIyMCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXOtuG8cVfpUB86MJSlJ7v9BBADdOE6dObChOgyI0yNmZWXKi5SyzF8msYKD_-gJFHqEP1h8F-hY9Z_YqiaIkKpJzoX_Y5F5mzvU735kD-nxAs0LGlBUzyQeTwXo9C-IwNj0jsDxh2x51PBF5VsSdwXAQpXwz43Ih8gKezZfUcr1JJLgbwyOUGmFguG7kBIHpuBa8Rqljc-aYJvc8FrihH8ATlPvCcR0urDgQBg1gXS5zlp6KbDOYnOOXYlbQBeyQ0AK3GsKHSCRw4a8ik7GkUSJIJk5lLlNFlvB8mm1ItCGvsjSN15nIc3hnTdkJXQhU6sLlLP1BgLplhgsui2KdT46OFrJYltGYpasjthRqJdWioGoR2MbRhbcz8WMp4fOszEU2Y6nKhQJbFFkp3g0HS0HRiB53Dcdy2KC6MhOn-iEwrpiJyPacMPItzzCckHnUdvzYsCyULM0KVG2WSCVA8sYjyYxapkm5ScG6dhgFTmBHjEaWUalTSzdjdJ2XCShsoZwszXg-mHx_Pqi3Px-Al9Msx0_VbcFnEZj8-wFLuXg7eAMaNNGA7j2RSZIfsYSWXIzwkZ4pjr75y_MXL8YrPhjeKYJoUWQyKgtw3CyiuczRBzRTKD_cA28LvWRZLNMMJT2RClfNN3BnBXcUXaFLK4mHgxxehLUGE1UmCcjPluA1UekdJSk7wWcjy40M34THwWGFeIvaffjfn_75v3__9BFcrLegnOu91xhZ4gyujEajqcINJ6TTfKq4yFkm16jDBEJOQCScCpJmRKp8DaFFuGAQmrBUsVnr-KMZHbwbdhJZbmyCz8MLEl0I3mtl-uBikNc7YJhByF7YBNWmhmPuscmxDg9CGRNrcAj5imYnPD1TqGRe0EIy8sXrr16QxvMEchfdkJOzXWrzwAoc3wguSPRdmp3ESXq2U-kPSO-xHTr7gRW63Lr7Dn8ScZoJIrgsYE1CFRFvAVfwc0GzhSiGJCvVVM3XG4hMZfcCYrzeobLhCNMKXHZngcwxOQYFydYNN2SdJpJtyMexTMQn8zF5HpNiKQiiEqGdPAnocFGemEaO5Zp3locQNACI09-YNJA1J6li4gmRBeDyikIiQJxIdrLRku2wD3WF73jm3e1jjbvUYzTLpMhGCiITvlLFADwgFpcgY-PSSRfE5S77mLYDhcrdxz7z74-O3kzIB-TDNJq8rf98NH9yIWXAQzmZc1rQUevRXfZhZmgK7-4BbY_Jd5kswDgJlaucfPnNy68hO4sleEoQiCiAWgJ1AQrnGmKmSEuoexwTPBM77GOFkevEXryPfYQqVyKDkk5K1eyn183HOyzgeJYd-aF15x2dMflGQUlcpoXOjRbNarCqrDEfjc6Wm_mwttMQooeTXRZgQcgdywv3ipD5PF9OFXzantV5I2-dXqMRrkaQxbQCYeW7IJAd2bEVhmIfgV6uIGPBBJlATiT4HFyTgDDaYBzxJ8owncgKizPkVJGSuCzKbIfDPIeFAMN3D1kXIA8h5hRJXott2iGZQKQBeMlJWhbrUlecCLJqNSZfA7_JdqV0aAUUdNnHPqhumjFBFpkQaleYitCjls3vnhh_hpSDciMVcE8sN6h1FZoU0LYNj0nLkefgjOwEcjYqd8jjGsIA1hPtJQ-uliQiafGdsHQtAbjSqszkwIna4j8k6waId8hjR4I5oePfXR6QJAIqT-bAbyHyoNbU5BaQLNmQeY_LznUFYlQpyKETlV6W582wIcODGgRmLBO04pz6TsNhxSyAXsbiZhz7gcco88CevhHa6GBYXa_ZGKfm6wQQjZ2sU6kK3X5keickps035KVvkOhjDe2t0Cf_vUV0W7FnX5CncTGLIaBEts5k3X7kkTlxOOW2YJYH3DAOAFxNO4psatum59keqBkLz6c0sCxmu74d-o7BGI15EIWAMi6mEdYz3UZU3pqYITBvvDKwDMsbGf7I8l4b_sSxJ1bwR8OYGChRbXHMlYC7NGAeBEh39fzBe4-q1ujWYEnzJRJSZnimK3gUmIjneo1et1BH6f3agF6HClDSsRCEtT4xgHA9SwRfdImVVzDQUfYx-TYHbID-lOiwRbhA9NCFTdNWshJUwae4TLoGGUAMAObps-MhiJTLhSI8ZUPy6vjZkBx_9vTZV58NQRIszIsNwdgednkPVu4lekf_x8tilRzh310TIEEpAAoVywWkaQXauUTN9ZtabkhWIU8rWTXSIRgAX6yubIO7Gu2eEIU4j_xJ2zFPS8BlHRp6oXw8VeCoLQhU-zpwfS-2A9MLDbvxda8Pq319c3tVLydi6nqRoIHNnH7o1B1Xvdx9GilwPXilZIh5fKqwN5arVG105OgaKRnF6BuTZyn6raMPQhsOTIvL6WdoQmCdrRWsVshwTcdjZmwGntEo1GvYGvvc1Ik1qzkARx5Yx47dZrVec1avdq-uCxSsCgJB_qJrQEZqxIBH4kQulkXXIb2GLJyqplTlsNmGLMsV7MnBlIU2OHALsijxSAEkQLJRnUNUrJjmaOrXEMWTHVbkRuTEUWQJmzV693rAWu_7NHf5Sa4ToEpRmchiM9zCfhqECyyTRdwVAeOtPF0PWMtzn-buc7jcAJz2Xq4JbmNOSjSoZcNqByxIeeeV6w3JfW4I04290I4awXvNYi34fbrAvN94XbGbcJjgluVQJ27t1vWGnd32bvrykeRzzXi1veaVvBdYb1NIpFoK7OX4kRJnRwts4J4_y3cYLxJhaJl-HEE1b43XdZK19PdpEVeAzXX39gTKCcLP9cakfmxGzA1sV4gWertGsjPm3TrEenWX2wYXrhly12tW7zWN9er36QbfriEtIMyr89PJDkVNh8WBsIEotaL0-sVe1OzdCKoCvtSwVIEdmU71SgRuwCq8hMAdRZvmbguO_Yu9V3onsiN9Iksun8fCQ8gKyHTwcXW8mqSLT6aD_iJ1BH1c_Tv-AaAShQZb4ltgt5ImNYReerPpPPXqeJz-Ywk6Sni8337-5x__6l6v8mU-39IT135wOMdjdduwAr_xQ69N7vywd_-LxCVJaJRCtEJMjLVMuhOFbI3x74LEWboCVMpRd6QzpT6qrhgiS9ANGT1Dx6_WRX4EBExVhHJXsJvMsKjp-hb12lTqNdy1ZvfppOGJURt-kI0i2eyASScOfSocy-iVl67f7gx9cyPd8CrbZQanHoBFS9N6vXW94n2a5gLAigCogFc-ffF8iMwqSboCqxtIrCR5TbK2TpuAMS_TM_1WtfAfoOxB45kqiQvXQyby7fGLCkOgbCMBhucRSBHZC-hr-7LOa_tDYwHlKUmpRlrxVrASck92BKWFo3r61PID0IZA-tJTKhMUuiFPdRmZk6iiW0Aqa461xKqph0ZayAIZ-lyuMEJ21ebIoAa1jNi1_ZYq9s4bej7a9yChIrBSYXzqqNWKQDQugNsl4PnXT48__-w14IdOsk9fvvrbeDwGEz6FthiZ72oNIY376fJB6rHQUPsBNp4q7Wt9gABJXBZ1XgAO5UBxFFZu7GTA0AW8VRmmqtBzLTgImiZYAmueOlVnupRWIkLSVCSkKSOa--h710heBW_j2qmqSs1RhXlVCNXZDEo-kzFADJaCtm8APkBaUtgdSUA0ZKAsOBt6CIknEE90B1Wbsn5qrgklqLXa4XSsY75rGi7rinjvUKdx-j1Oa85qup0v5RqUmapKexC-gaYWl652f1eOet6h7FtGn8gELw8-9RhVF87L17cPSqs5sC6O9Y1MQohlHGfG722OmoskntEcAvuaIaqmD_vNUG85x1qlHBBT737dcewtJz63Wel2s5FbrHTLI-tbrLR1vtatUBPnx5isbZ1k3SjJQ8ywts6MbpRkv2nR1sP-G_e6gZ1AvldAfl1KXI2P-oj4UyhEicCygkUD9hytywjcTAAMkFa2tKKmZlTiwRlGVd2_Ivhdlz6PuWuXao-4ay8tH3HXXgpfiZqH27TL1sfbtJeYj6hpl6EPvOmbHgacD6AX1TVvn6XbQ6OLe-D84tbzJNN3gBj5VuBZ1A4Cbrh-zKnht2r3B0X9IUl_eHR-KM6H4nwozttmurea3LaTyzZaJs6w3XjivNs-prxpZvuLG8xer97lMa1pTwx_YhlbxrSBy30exPZhTHsY0x7GtIcx7W9oTGuH3DNjwzbdyHu8Ma0eErzvQevlI3yoHsyz_TA0ulnJzz5orUY2v4RR6WX1AQrswAIKBCX10UalWo1bcajL4h6GnYdh5-9m2GkbDjA-ZkOrHD3asFMrd23PcTkJDuPKw7jyMK48jCsP48rf07hy95nVA_00beuJ6m5JHuhHYFt_krVbkp_zx1j7j-O-TrMVTeTfYV_Kf6AMMeni2X5VHavWDVIpw6oIjdcXZQQmUdC63mIgd2We8SDbXpnIPcq2Pdc_-Lbb5jfqZ1n8ToObHb_Y3zq4aY9N3_vg5gBT7xmmbj8C3HJyb_ZO7u132w_mf8WDicvqbRlMmNbE8bYMJtr_X-MwmDgMJg6DicNg4rczmAAkdQTzTSui8e9iMDFVv_LRwlQ98nBgqg7H-4fj_cPx_uF4_3C8fzjePxzv_0qO99-8-z9pC-GI)

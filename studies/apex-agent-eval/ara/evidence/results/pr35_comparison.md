[//]: # (ob:da7f7164)
# E05 — PR35 RelayBench design contrast

[//]: # (ob:5c5bbc3a)
- **Trace node**: N09
- **Claim**: C06
- **Sources**:
  - `proofpress-pr35@c96fd86/studies/long-horizon-eval/relaybench/PUBLIC_RESULTS.md` (SHA-256 `69525b3a5f55260075b7d7b3932388f47fc46e063fdcece5167fc8fbc2a87795`)
  - `proofpress-pr35@c96fd86/studies/long-horizon-eval/relaybench/CLAIM_BOUNDARIES.md`
  - Figure 1 source HTML (SHA-256 `7531947ee484b8e81807e05fee08ec799f4b6989967c871fbb5bc46570a89d1a`)

[//]: # (ob:c0667afb)
| Design attribute | PR35 RelayBench | APEX pilot |
| --- | --- | --- |
| Task stage | Fresh receiver after long-horizon handoff | End-to-end legal deliverable from a data room |
| Substantive input parity | Byte-identical handoff artifact content | Baseline full corpus versus treatment bounded working set |
| Treatment difference | Ledger current-state metadata and deterministic blocking | Retrieval, proposal, verification, staging, graph selection, bounded context, and gating |
| Executor replication | Frozen panel reports repeated paired runs | One generated artifact per normal cell |
| Quality result | Aggregate lift across the bounded frozen panel | Majority preservation; task/model heterogeneous means |
| Safety result | Observed unsafe propagation separation in controlled pairs | Both tested treatment conflicts hard-stop |
| Official benchmark status | Not official Harvey LAB | Not official APEX Pass@1 |

[//]: # (ob:a6101954)
## Inferred explanation, not an observed causal result

[//]: # (ob:767ebd5b)
The cleaner PR35 quality pattern may arise because its treatment preserves substantive information and targets reliance metadata at a handoff boundary. The APEX treatment can reduce search but can also starve an executor when the staged set under-covers task requirements. This explanation requires an ablation and is therefore retained as hypothesis C06.

[//]: # (ob:fe6a4b08)
The PR35 safety denominator is 63 controlled stress pairs: ordinary handoff recorded 8 / 63 observed unsafe propagation events and Proofpress recorded 0 / 63.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2EzYTE1ZTM4MWFkNjRhNzcyZGVhYjVkNyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImEwYzdmZDhjIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9jOGNlMGZiYTg0OTg4MGUyNzhjOTQwM2MiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzJlNmQ0MmYxYzE3YmFlODAxZjUxZWE2ZiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWetu3LgVfhVi9k83nbGpuzT9s47XixhwLps4RYFNMOHlcEZrjaSQlJOJbaAP0Sfsk_SQI9ly4qSJ7S3aIoDh0ZDU4Xe-cyXnbMK0LRUTdlHKyXzStgsWsSCBKA-YTGOWZaEExhOZTaYT3sjNQpZLMBbXmhULk3QOEBQiDGishKI5D4o4EnkehCEVVAGEKitySIpY5jKQmYqLGBLGJU25UhlPKcqVpRHNKejNZH7mvtiFZUvcoWLWbTXFBw4VDvwVdKlKxisgGk5LUzY1WeH6Rm8I35BnumlUq8EYfKdl4oQtwSl1bVg3vwOq22kncGVta-a7u8vSrjq-I5r1rlhBvS7rpWX1Mo_o7rW3NbztSnxedAb0QjS1gRq5sLqDi-lkBcyRyKjIlMzFZDuygFO_CMmFhcgFUMVZHhd5TiHMclHENHJr20Zbp9qiKmtA5INFqkUIqYxDFYgg4wxyGqgkAJaqrTo9uoVgrekqVDh0OEWjpZnMfzub9NufTdDKjTbuaTsNcsGR8t8m-73K5Bh1nrxGTQavcGa2nSzB7LIW3s8QVm1ncMqq3Z2rrWe8Kyu5yzSb4VwpoRYwm-FMV1kzm7U6SpCrdct0aZp6Zy0n02_yO2atLnln0dwLzkxpHCyo1IIZNIMFL6-zq0Y75U7K2ok0G2NhjTM1WzsvuK7kFAUY5z-Ted1VFaosVjgOjrLX04GzCTqlW7QQGth2Hz8zgIZFHidpTFUYBeiiKWVJkWaFFM6edWO99_VmJb1ZCTqYOGmbsrbeS7XfyYEYvvUY2qYqxWYkYewjIyHe-27pPqZRdqGQFdCtLnsvNTyYQ8SpiOOwyJXAF-OCKa5ikRdFqngRxmHGIA4gTuOCF1EsWFwkRRHwLE9CnieJk22ZU-UMuXWfk5CG6YzmszA9DqJ5SOcJ_TOlc-oyQM-zCx5gYcaTYHIxGj37L3NIXjXixJvp4mJ6Y4SBLO1lfD1tod47JPuNhPeT1z5oZSc-O_1RdH46_bbDtPj_Hb0e6m2C92xrHHxHskxlQRrjckzUFt47Pg5oQv7593-QZ8-jhDyHim0eor4rIsGUy5q4hZr5mjMAkdIjbF3BgXc48gP5eiF20zr4rgwg-olzlgFeIhLORcTuG96MPHhwrJkAUqPHPHgwJ09o8ap2w_sVK9duZJ-m25EXTacFGBx7VRMyI2_aK9AVFtZriAVN0wzzwH0jPic_bxcPngLk_BN552Tv2cHfSFtWjSXnr-pzMpvNcPQK7zZHjgGzNKBBkVz3gMNagdYgCbxvK1Yz55dT5MoSVpOGo0ue4qRgX3SBH8jXiukMq8g2mL7sD1maAZcJv3ewxyusORWwGvSW1bcdq0q7IS3yDboma7YhLriBcHCAgZTWEOtK3hVkDH92Da-ClMWc5n8IXo_TMAUIExNSg7HPMLWS0pA02jpVU1UoyliXwlCVUps5aT7Gi-lSOKf_bGb4CEVfs_fcV2IRiH8FeVmWde3yz6uvdfhXE2IbL8KwurTlBxToPdhnNuKScOfpIXvP93Y-lxm-Hd6noX97IKOA_3Ygt4nq20Mdhfq3Q71FLN8B6ijQb2HeOwTz2iFzJd_pY4jpOLZotS1PcU2tGr3eAmZ30G2UFG6n220DX2M-ZXgKxD5ANkqRoYciOdl1bw5W_FbdXo-y29nk3WpzTYdLGVNy2Tnxpqvll6QOAFDVlLj-bOPMA47Irz93fOEcuWV6fKAYt9XjQ8bZ977pe9_0vW_63jfd1Dd9_UXHcNDvMc3Ti5sP9P_uTuNeLi7ijKYQhbwIWSAljSCmAS8iFkVxFIJQVCRpHoVxjGkEZErDCI-pkmZRnHLMo-ln9LnpBiOb0-CmG4zh-u9_4gbjbLJiZoXrcxGHMQQFVeCM6mWMSkHvqHdM4v1eGK6SiZgnCqJhr1Fe7_e6Y0a-4tKx9ZMoUrRKujuQXzX1crZqdPmhqbf0a6cMd8rsPnv58Ohwf_H84MXLo-MXSO8b8qcXj_ZmYZKSN2mRhAmPWKKSJEwpzRKeyYxHRRRGea7iTIk4BZpGSgoQkAQpjuSKi5DlWVYkb368D4j7R3uHjxcPn7588vPe88MDD3Ir95dy2WkgATGeE_Lo-PHRCH6WREERZwBxHvMc8iCnGVA0BdAcRFYUKuZp4W76MpFngeI84ahQklGWFzJgb368odZdGjYNIZOC0jQbDDsqf71h71S4Rv_d4DEzJ5jN3MXqOfkFuVy53g-wqdWEKczTZMziZX94Tg5qObPNDGpJKlhisZFQubf8Xa3SzZowIpllBI203u714lrH3HbYTWP8Yao9Jw83FmYuTG0pUNawzRCSPixcK4grmQGX6YjCDg3HddsZ4vJEN27Thy7yXaNPXHdsoCfh-HKJLBUWDZcYUOoRSEyFRHTaNXczl8KArMEyrwKiQfWQDKwHaLFSbLtvJ_gcOUcjOO-a4uGgaRvjnk79Ly2iL0SOX1w8JUvN2hWCqUBsZwacfSmb-q2W-JoT7fAevAfRuRKkoa16gd5SzQeokb8aXJl3NcC4T9_u-rKEH7qrDa59imRhkkTTuLlLSlvUt3anFmQRkEq_3a99jd5mSudEy6VG81p3_66wnArdYN3zB5AeuhpDOSeP2e-NN2p_UvKI_0Is-tnuGvMQGtcx2ThEDdpsjR2C6f1jW3gv9346FG7UA6c8vWy5pcCAq7T-sazHldmXZOcnjV0R6y96R36BCxXSiGStmJZo56bd7v1UoblK5MJnhzXTPips50Q9wQhqhvlHDCFtyNHew49nfLw9Y8b8FJDzm_rDPsiDQmZplNO88B2ID_JRyzhUinvs9fqNMZPIvOA0FqoYNh61f_3G_4kjMjq5ZXoJ3mmrkrkgvIo21O8yA3gvw5PpDnG4PMUjayIPyE-HbxtgGrMeJkM_yirTOAMiDEcWDFH0boWu6o-eLuVJnxecG-uZ_wXVeD8l_c-Ubg_jNsb2b2SCYdo4yWjcK51KHxkaUFP3C6tlmKcw4tDZNi26IyZt4yruzg3t7dBFYE3EAkKDKLo00ajjHZnojz7p3xR0vqc1XtWr34qvJFAv4RPtXl_g378Arihrfw)

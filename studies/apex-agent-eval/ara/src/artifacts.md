[//]: # (ob:52578f04)
# Artifact Pointer Index

[//]: # (ob:73340d29)
## Product-source boundary

[//]: # (ob:892b69cd)
The Proofpress product contribution evaluated here is the claim-centric ledger and governed graph mechanism implemented in PR36. The APEX application used to orchestrate the experiment was a temporary evaluation harness; it is neither Proofpress product source nor a public dependency of this study package.

[//]: # (ob:6c7abba6)
## Proofpress claim-centric ledger engine

[//]: # (ob:f4508c92)
- [`proofpress_knowledge.py`](../../../../proofpress_knowledge.py) implements evidence-bound claim records, typed relations, task selection, bounded graph traversal, and governed working-set export.
- [`proofpress.py`](../../../../proofpress.py) exposes the corresponding command-line surface.
- Product revision: `proofpress-pr36@9f6e3f1`, incorporating the claim-centric sequence `516fa3c..9f6e3f1`.

[//]: # (ob:7e0c4b84)
These files support mechanism claims C03, C04, and C05. They do not establish the APEX outcome numbers, which remain in the frozen experiment manifests.

[//]: # (ob:cefc9e27)
## Product tests

[//]: # (ob:1f82865b)
- [`tests/test_local_mvp.py`](../../../../tests/test_local_mvp.py)
- [`tests/test_knowledge_ledger.py`](../../../../tests/test_knowledge_ledger.py)
- [`tests/test_claim_graph_apex.py`](../../../../tests/test_claim_graph_apex.py)

[//]: # (ob:7bc48b53)
The focused product checks can be run with:

[//]: # (ob:5b5ae8c1)
```sh
python3 -m unittest tests.test_local_mvp tests.test_knowledge_ledger tests.test_claim_graph_apex
```

[//]: # (ob:968e35f1)
The tests cover deterministic evidence binding, staging and admission boundaries, typed relations, selection, traversal, and policy-mediated export. They are implementation evidence for C03-C05, not substitutes for the native APEX grades.

[//]: # (ob:c0b11f2e)
## Legal graph example

[//]: # (ob:5cc3673c)
The legal worked example under [`examples/verified-knowledge-ledger/legal/`](../../../../examples/verified-knowledge-ledger/legal/) illustrates claim and relation shapes used by the mechanism. It is explanatory product material for C03 and C04; it is not the private APEX corpus and is not an experimental result.

[//]: # (ob:648a8f5b)
## Frozen experiment manifests

[//]: # (ob:b2029503)
- [Task 1 frozen manifest](../evidence/raw/task1-three-model-finalized-v9.json)
- [Task 2 frozen manifest](../evidence/raw/task2-jcf03-three-model-manifest.json)

[//]: # (ob:c7388741)
These audited aggregate receipts are the numeric source for C01-C05. The study package intentionally excludes the APEX corpus, generated DOCX files, credentials, runtime state, and raw model outputs.

[//]: # (ob:108b251b)
## Temporary evaluation-harness provenance

[//]: # (ob:70ff16cc)
`temporary-evaluation-harness@1ff29dd` and `temporary-task2-harness@0b7ddf4` are retained only as non-public provenance labels for the local orchestration that produced the frozen manifests. That harness is not the Proofpress product contribution, is not copied into this repository, and is not required to inspect the public study artifact.

[//]: # (ob:bb95f054)
## PR35 comparison source

[//]: # (ob:6add2532)
The historical contrast uses `proofpress-pr35@c96fd86:studies/long-horizon-eval/relaybench/PUBLIC_RESULTS.md` and its paired results poster. It is a separate experiment used to motivate the discussion of benchmark sensitivity; it is not pooled with either APEX task.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2I3M2Q1OWYxZGNkMWRiNWZhYzRjN2IxNSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6Ijg1NTA1NTEwIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV82MDdkNmZhNDhmNTExMDI2NjM5N2JiN2EiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2I2ZTEyMjhiZTg3ZThmZDc0NDJkNTQ1YyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtW2tv20YW_SsD9csGK0p8P7Rfks12gQABGrTpokASyPOUGFMkSw7tqEb--94ZkuLIlhmbcrrFwoCRSOTMnTv3ce49HOpmhiuZCkzlOmWz1aws1yTyWJAIh1HmMBLAPZ9GxAlm8xkp2H7N0g2vJYytt9gNwlXAfDdxhWcLgbETsECwOIq9gHE_8fQtn4QggTl-jP2A2ZjZQYId4iSUO6ENclla0-KKV_vZ6kZ9kWuJN7BChqVaag4fCM_gwn94lYoUk4yjil-ldVrkaAvji2qPyB69q4pClBWva5hTYnqJN1xt6uhyVXzmsN2mUgK3Upb1arncpHLbkAUtdku65fkuzTcS55vYs5dHsyv-e5PC53VT82pNi7zmOdhCVg3_Op9tOVZGjIPADgJH7UxdWfMrPQiMy9ehHbFQYD8WgePYbhh6SURIhJVmRSXV1tZZmnPQvPdItiYhd1w3JjyOeCxY5PsuC_yAttvptFtTXNZNBht2lZ60qFg9W324mXXL38zAy0VVq0_tbc7WBEz-Yfa62zJ6D3uefYKd9FGh3CwblvJ6iUv-xQK1cmnxK5wtF8PSFmnSjC1xhS2rrqhl9dPrxY7N5o-KMSxllZJGgmvXBNdprVTgmVjjGkwuuZbXyG1RqY1cprkSWe9ryXdwJ8c75fHjDc1BQK1iZbbKmyyD7dEtXOfKPJ_mvX1mEIBq0JpWHLfr6Du90nzt-L4QYRLFrhdjz7dDHFNK_VitW0gdaZ0LUedCBMFEL8sizaWOyEqvpJTov3U6lEWW0r0hwYwHQ4iOtImhUhdCrgVYhVdllXYRWRNnxT1iUxiYxII61PETLIjwaZwkoSCJ67sR5r7D_dBPCKQ0xX4SJIlDojhwCQS7ki2x2soN2Fb9P3MhtC07ttzwveOtXH_lx3-37ZWtcqKzM4wKHcJI4vuzr8bVm_9h8JGsoJfaJV-_zk9mDmepPOTNTyXPX71BrwvGv8w-6WRkDb339q2su3v79wbg7v8nK7VaU5LypnUEzAncIIqF7cNwAFvJv6i9v-oUR-9UTvAKvcmVCeeHdRnTCpWqRvBruPIDuneO3JdKOQXUoNtMub1fPPIgyZmbHC3-TvtYWnXRVJQjUjQ5w1C5xlb_Ad0_a2T9OHFJmFB27vrvt9wojaiNUomUzN6pSAVPo2APbXnFUVojCbNoNmgIeIWP1IOijgnB4W31-nVohtOdRblahaKMMwAexPMNQNa3rfUwISPGE35gxzRxn1g7C324MGruZV5c67mLcn_x6W-LxfLwd3fUoHAGPctxqHFAYBL7T6wteL7mSKQZr1HdlKpsoB1XiZbWu1ZojV7b3hz-8ecI5ww-BAsE8_Yjnqdc0IS70anARKplqx-WDoexI350ROzGYUCmraXcpQct1b9rkImz9e6qvOuuu6PG3EWg7JPAm6aUykdRUGgh2ZCMqsaDn3GOCDS3TY6uoSVdjTghIAHmMXWm6XBxcVFvP-blHjA795C1Q02eSjWtnbs4tpd58TIftKJQvI60SsKYe4FwpltGD0KaDyDGAaqhZoD9IexhFOO5Aj2YD3EyR9B2bFRFUYE7Fq82cRzh8iOl3vINztCmwuUW8S94V2bfgqXTM0ZiN6DUCyOPnrOuMkmmp1wX1SVETDcH_MXAQh8uuu_18kqTI86sAyiNgTeQMeAgx2n176r4g0Mt-FKCqB2ADdoBUogHJPT4zBETEegUk8D2nkIPSPb3uL5EDhKtgH6WzvQ-epYVvl5KGOdYcltxbu0ghrORZKeRF8eR7zyFii0g40Z3kQhvNhW4Vio2S3laQtwDKdCVN292XEF9V-ZFUY0FuGPHxA2cY2--5zsAfOgN-uIOdd7a4irvmgBobjHY4xuefbiUsU7KFsIJKX1q_QDbOxnWXRkvHSHchLELDQ_GUOV81xoxJyFJIOzgVjX-2QsAlnYwOq2hY2o9861Cd9-kEWOFIMkNPPfM1RVwtM9GUgDxttvDAO9Qdmpk9DBWWXnBSwpcj8XhquUVt20D7KRtFu5rzm9p0dHhV-qrDmc9BSoboHWuAPvjPU38xxmShZ5RQzrJ9A-Y_-rdj78hzSWMQEGvfn61uK9bf7w293TVZ6hjNO-PV-ecjv1Eo6jif6MKag6j28qz42fszej8J5n6AV3tGdoZnf_jtZve3etRL1CqirEqCPWhX7F0OLW7VUh_TpAPPGFSVE1mA4gVCJZAUOAwgRK51WtorYtGAjDpkkXO8ZvBKiYncNs9nqGEQTemBM9UrqFHvTgnMAZGMg1uHkhIzlDRICyPV7HlK9MXN3jJNPtMpSWY7VL9nKsvKimv50hVVwZYkGl14cI5MWvQm8fv7QQdOcfHA-OZZuapVMdqq8dSz1_eyjdj3jlVb6BMj9_bCF84QyWDPU1Aq8lkyRJpjjOlqHWVLD5DP3oOdBn8ampNm0aoXtuO1Rc4pBrfPeoODZFqSXOlLs6yc7pAg5hN2NvDCNI5VWPgZRMg-Qzy1Y-yScSY8C-0myoucapa1CLP9gjX0HCckxsDiZvQTpykW-eAx0DqpgHjVCpXL7Mi31hbmPsHuEcfEqm6syeQ39vlu1__-fbN6_XPPz52b58Mdnozu97uj_ZwkDG_1QWPSe0VAOOHXT5KwBxlyIcf0o4csLeWNk9fzTNI80T25vkw6vkw6vkw6vkw6vkw6vkw6vkw6vkw6vkw6vkw6vkw6i9zGPXwFzP7FxM7nVau_fX0G4jfegnzSd60jGLm2A4408YBBrARcYwdFwdMuHHiR7HNfBp7tpNQO_SCGAcOBu8HLo1DHgSxe9-GTrxz6dnwd-Kdy8PLyX-5dy5vZltcb1XE2zRiPk5i5im6o2UY3KsLwsfRqE40c5wEu34Y-4nfizaYVS_6kRypE-56dsJgYzFmUS_coE090vwJZ3t9U304jIJ7aa6Jdfu0q-XgEMaQjnpF3f8B_y4qaP5qSE7ZQr9RU64xVAQkTwAl6kDuHyiVStmcQ7sIup3YZmfPHEoIRmVDQAForEqeq3K4R4WAVUHC0dO4xQl07EzuOwkgOYWcinFvcoMKHvlzMovr1_I8GrskThz7sJZB7Lq1zuFkDz9CVC_3nzhFUMUE1TzjVF2Yo_6RSxsX4FWV8TibH0eN6uVgr1bNpfI3IN7iY368jzHttc5qnsJyHadFBdfLQvfFqk5AN8IsBaDA-yrIWK7l9414_0uO1e1CEL5MRMg94VzMIXpBqgo8qWTezYZavTyt2vGLwAkF9uhi0U9enGinOpfaUUxChyaE0EPGGux3yNjvfm5agfeutyndgjl2GHIV_tRIcX9rN5IWAXFCj0Uu95jT78vgyXdgboz79uAmosgTcegmQ6YZdNiI_jPPQPNbMg65sW5TdVTUicF3JWqPrXVOrFWRG5V4YvCL-wPKo5ET-wJqdcQOATXwc6METOfc_VKRL4Cs0JCF4aFKDjS8W-osan1sS_Pebat8zGGhE0y805UKLxKUEsjMoNfVIOeGWb73MeuAjbfQsG3-rB1nqS68HRC2SayI0AGVcVeiO3XakyRPnSTNdarXDQGFZQNb0Tc1g4JJV13eg9UYH8teIMNObNvYAaJyyN7hqcGQvQ9-BtALBlgLXcY9j5BDyAyPBQw3fO9j2PF5UAKzrGm7kK5eax_1jkT1FoKubpsWstcWPgDyAr3RTQg4MMNgd_XbwD7JdiCwSmFnndM6rPYPjQu4TwmDrv1KdUDaX6rwNLUe2g3BJiCDNChYTSZHPCoSnwQhTWgyeNR46DF49NGPLroFMOFc8DiwCfP6BYynGQM6P-mZb94LdB8m0LU-UwGpYortZ7Qi70fWmER-GNkRWPAAIcbDkKNS_X2Pg8E7NGtY1-wYITJHQJZ4peHjXz-9_q1tGeaIVpyp6TiDL4DsEjyrwEvyFnrAPEgbQ7UEZTNa2ZMoikPH9Xyf8UMZHh64DJF01qOSnogFQJYCoKPAvg7VbHh60peYP-EcOLc6rjBojvSPggeI1TXM4C8KJ-QWS9T_Ks_sp4YmCrwNY3rDGBjwDY4278fSokw1vdKnl3Cx4tAKpwp35iZodD8d1iwrzeuS0w5r2o21AdcT55EIwCGhnu9RB_rcQ6oPz4iM3u4Rj3t62YwQKMo4JuTQDxtPgIwC8b2Po3_59e37Xxa7Lm5SyNwSa-u1WAtfixqwvAd7DJVdGUoeMdae1O4K2eK5srf6sXnTtgrANvWyO1wp2pSD19KrVO7NclAWRaY4EjRjqKO1OuVV_N7x0qev8PdfVE1E2Q)

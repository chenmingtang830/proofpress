[//]: # (ob:98f84bc3)
# Proofpress long-horizon handoff study

[//]: # (ob:967ea7df)
## Start here

[//]: # (ob:36d076ff)
This directory is the stable entry point for a frozen, bounded evaluation of governed agent handoffs. It separates the public reading path from the reproducibility and audit path, so people evaluating the reported result do not have to start inside raw experiment records.

[//]: # (ob:bd9aa239)
Read the public-facing material in this order:

[//]: # (ob:9b0e173b)
1. [Public result](relaybench/PUBLIC_RESULTS.md) — the one-page descriptive result.
2. [Claim boundaries](relaybench/CLAIM_BOUNDARIES.md) — what the result does and does not establish.
3. [Publication copy](relaybench/PUBLICATION_COPY.md) — bounded language for communicating the result.
4. [Result visual](relaybench/visuals/proofpress-results.html) — the corresponding communication artifact.

[//]: # (ob:80ee0a4f)
## What this study is

[//]: # (ob:53e0aa1d)
The frozen panel contains seven models, three Proofpress-composed Harvey LAB-derived legal task families, and 126 valid paired runs. Within that panel, ordinary handoff completed 10,654/11,928 rubric criteria (89.3%) and the governed condition completed 11,141/11,928 (93.4%). In 63 controlled stress pairs, observed unsafe propagation was 8 events in the ordinary condition and 0 in the governed condition.

[//]: # (ob:e1fd3af0)
These are descriptive, bounded findings. They are not official Harvey leaderboard results, a population-level causal estimate, or a claim about production customer outcomes. The exact limits are in [Claim boundaries](relaybench/CLAIM_BOUNDARIES.md).

[//]: # (ob:f2f5515f)
## How the repository is organized

[//]: # (ob:2d89c2e8)
| Need | Canonical location | Why it exists |
| --- | --- | --- |
| Read the public conclusion | [`relaybench/PUBLIC_RESULTS.md`](relaybench/PUBLIC_RESULTS.md) | Human-readable, bounded synthesis. |
| Check allowed claims | [`relaybench/CLAIM_BOUNDARIES.md`](relaybench/CLAIM_BOUNDARIES.md) | Separates evidence from overreach. |
| Communicate the result | [`relaybench/PUBLICATION_COPY.md`](relaybench/PUBLICATION_COPY.md) and [`relaybench/visuals/`](relaybench/visuals/) | Reusable public wording and visual. |
| Re-run or inspect mechanics | [`relaybench/README.md`](relaybench/README.md) and [`relaybench/bench/`](relaybench/bench/) | Execution harness, fixtures, scoring, and checks. |
| Inspect frozen outcomes | [`relaybench/results/`](relaybench/results/) | Immutable per-model results and retained invalid attempts. |
| Audit evidence and lifecycle | [`ara/`](ara/) | Agent-Native Research Artifact, evidence index, receipts, and claim register. |

[//]: # (ob:be9112fa)
## Retention and change policy

[//]: # (ob:505342d7)
The existing folder names are intentionally retained: they are cited by receipts, ARA records, and historical evaluation materials. Do not rename, move, or overwrite frozen result files merely to improve presentation. New public summaries should link here; new experiments must use a separately preregistered study directory.

[//]: # (ob:a1e3ae22)
## Product meaning

[//]: # (ob:a2e157c7)
This study is implementation evidence for a bounded mechanism: governed context can make downstream reliance inspectable and can constrain unsupported propagation under the specified conditions. It does not replace design-partner evidence, establish general performance claims, or admit a conclusion without configured policy and authorized human review.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzEwMmM0Y2I2NWU0OGM1MzhkOWYyNWVhOSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6Ijk0YzIwZTE1IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8xN2FiOGM5ZGFhNzM0MzA5ZDliMmUzZDMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzlkZjBhZjZkMGMwMzBkNTVlODc3Y2RmOCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWW1v20YS_isLHQq0OMnmq0TqPrlpgAZI08BJrzikhrLcnZV4pkiVL3bUOMD9iPuF90vumSUpUY4jp06L-3D-ojjk7szszswzzwzfj2RZp0aqepHq0Xy02Sxcx1OBSqYhBZEK_UjHxgtJxqPxKCn0dqHTJVU11lYr6YXTeexMfYpcE5lZopxpEOhZjGfGd6czL4xc7cdTUhR7XiRJJ4EMKfGjCJK9OJEmgFydVqq4onI7mr_n_9SLWi6hIZM1qxrjj4QyPPg7lalJZZKRKOkqrdIiFyusL8qtSLbiZVkUZlNSVWHPRqpLuSQ-1MHjsvgn4bhNyQJXdb2p5qeny7ReNcmJKtanakX5Os2XtcyXke-cHuwu6dcmxd-LpqJyoYq8ohx3UZcNfRiPViT5EuNAeQ654ah9sqAruwiXSwt3JpNIxVrKmR_4TqzjxCNf-2xZUdZ8tEWW5gTLe49ki1gbR5qpdpTjOzoMKZrNlDZRe5zOuoWSm6rJcGCP7VRFqavR_M37Uaf-_QheLsqK_2pfk14kuPI3oya_zIvrfHSBM_TxwA6uG51SdZoV-XKyKsr0tyKf0JXMTs-fnn33w9OTtR6Nf1cAybou06Sp4bdFIqu0Yi2UmYWscJ81WXlNDV1s5WWas8hqW9W0xptcrtmdvbVjbK04BEbzvMky2K5W8Bm1p06yQl2yMyITBYniC4a7anrHJ9sHihgeTmC_LowRfPItdnQWSK2taRsOOrrGk7-IzxVRbzdsNAcCgmr0YTwwbTojOdPmwLRXNS5UrKiko_r_Ig4WHtHiI25mU_MQLa-RW0Ij3pXNMN4u07wSUpiy-I3ysUiKJscuwVHRSParKIxYIpn3Rm1kKQ8sSnQspefHD7DoHAcU9YrEpkmyVE0QeDivWAMoylRmIs3xFkZzdJfzIzbECTJ05icPsME9EW9eWvUAIWRcffF1SZncJpSr1enLn759_uzJ4vzpq5-ev36FFPlG_Odf_7Y2FzlNNnubMgDXgU2RQ-TI4NBTP69k3Z7JRpRIq3vi4s4NR-Ij9KFUuvoLtL7G4dqIEBuZU7aPlIrBR6wLTVk1hsCSaJA5E-DtER-Ra7QvjfNlllUkZElCU6XKdFOnV7QPW4N9uI_qRGDh1q7LixohbFKVHrHMeCYM3fDQU98X19bNJW2KKrUZYyNxKfP0N2vXMbfdv_uIDz0dxcqj6I-y50a8IFzPjXgi8yJPFTILmtr8vkGEQVIt6B0CuBI3v-Q3YjKZiP53b6otZ4epT7HrekYeGHpONSoUywZ2ihbExaZAgm3vubTjO48FvRP6gadnf4QdHP32LhiJTJEBeQSXqsrGU5p3QmWWbeELzgvSc_YMAu5IjEmXfEmed7tw6UbVYk1wIs50_Ho-Xn3kSqQHyjJTs4fqez3MSZGuNxmtcfI2aLBIAx4BE0WJ8tHn35r4locI1V7DxbhnLSPQQq7xC1WSbAmCfdOzDVrEM61iEMxp6ATJlBxDycwNJOcmctnK7IiV6IgVXEvqclPANZYnllYTc4j-f0whLpiRWd_vJQxZ2kCI5X8PJHBVYeoFcGhJ5aZMO55YJe6cPD9BqoAye05iYi9ymDhrHVHgzaYu3nnBFFI8PJxGPi7BM75Prg9c0tq4LBu3b_le6625G4Ak8ZOR53jTiRNPHO-1E829aO66f3WcucNY2904w5ycBZ6PEPwwePr-z6WINhxbCreS1QrrcW2OMpHv6xnni5UxYHVdpH4RI-s0-TqUUYiLNomz07Qnab2m-7lXJ0-jzyFfqZn2TS9vQMc6eV_CskpgiUCo5XV_TNSyZ_UB0Nucq68L6DCGOLwBQxIoVc3Fhgrk6U4wAKyvGMzGO34ztnhI-RJhjV2QzC9IlkgB_Be2bmA7b17ZkiPrbqO4lpXYWAghfXIH1nX3FMTadZJYaxl4_T0NSOIOnr-Q-3XaXE-TGwTKTH135-U9Hey0fRnLY5QZMI5OxMkvuQexTzKZrlunyhLZcyD5yfOzZz8svv3xpxffnZ0_e7qXfd0Sn16W0AVXGDjG_sG0Bb0y4CetVtDj78xv40UVm-0dJzh7_ezHF4snP778x05PH2wZyl_D5-DwAVFbN7kVtouR7kQBNJ23JqEjb2R2oKZ9VA266Em7szpZ1etsf21oSPFiU1hCNtTH5bjDj5M7yHOfuqExs5jiaewFvVMHfHqfup9Ljzu5sedP44TCyMx0L3fAmHcp_HACDHKG2_5ellcgBM_Pvp0gehEycAAtEdW1rC6Fkes0Q6S0meh6U4GETTWUATaQpk2OtP85xbHyNv-sFWNOhTSXAJUeA1lfRpzarjOehsGp645RWiAhKRHpiFebTOLrKD7xv_rGqmPv7LBGsYO6iNqJcsdu4Paivo79k-CrbwBDuZj69ibKIsuwrqotOLPROEmRoOXnc8J4aYhxAmnTOpxxIxK20FdtXtP-LHsT2Dqnf_-xiUcQx7gxTc1MkZHUu3XQbuzd-uDuAa7rfJpZsE0KWfaAyn4Esdw0mT3uJMNJETOyqbALWZwyprH3sExZsJDQWXdQ2t5-U9XFGkwTz-EJao0AD0WagOes07qnnw_AmyMX57i-iowvA3JUf3GDbmifZw_qZzolKLhgolpGSRL2SgYtTqfki5oU-8sPb1UVjh6VNVUr5M3bY5j_9r6ScCO-b9Yyn3C5ZWK4D51qm0NnlcJt1oonTCYFWoTimiOYHVbd1n-Hp97eXzpuxCtiJ9YoEnsWXhZrwfkCy9Sqt2GHuTSsM3fewkHdeHt_YeFMPRDT14W3d1YLNvuckA7M2jvHXFsAWFpR7bqT3oMTACBnS8dE-rZCfXSFO1J6qHb3-A5D29_D9e0vG_n0HSk7zgTCAnwqZLZJ39VNyVhdoabB4nHXTsLDvbufdYZ2NaPP4dvmdmhxS3v_lPU_g8va3mZD5cSWmR5jrNa-38TVtBVD1jWtN3VvyBnoe72PC96SpYbUVkEkW4PIYfX8D-s7Y6o5eSEtqTnvSKA46-rzeC8J0EjvxtCvCLDZFa4Wy0paIiephAl3jQr6gm5C0qHjyDhIdpxwPz3YA83vngF0CpLAVX7oeIk32zGGwVhgUNkf2txjgUq5QCbbwUWcnZ-Jbjzf3kr7AcPi14Dg97QWnvqusHUFzB2KxyATV21x4AS-5ordx1GXsSbNYB-KA8GouuBevMRawZSj78hPAJ7XfWpVzXptK4OoVkWTcQzkl7a9-ZvIsYzeIbrSta3GaxQe0XBZBLdpgQVaILp3qy30zKx2Lc2RcuK72iXXmcVOuOu4BoOPvZc_a5TRCY0QOlGkwec9fyd0P90Ytl0PnFes5wd0gyWifLPTLsEViuucqY7kUM9S2aaDTXibqTZMJRMoXoaIYQbUbLqWa0iDWGlpsZh3pyYdspu20duRf9TZTCrLVNJljg6krHNs7g8y3ncHAjlMJaINTsXx1tbAtuS0nEODPTDz2FfCa1BLJiB4ZNJlwz5uM8wepv1iY1vNFdc70c6EPnL7xQd20h2fo0hzmnQfoxRA7N3own7aso3j7ee3Pl4Nnv_a4JC7F0gpgLKe8Ie8_82nLcqv0rLIOawWDLzVJ75w2Vt76Aeuz_6-g-pgQ-iOYVvr_U-J_Xh_N1gDseTvsYjAum9OGS7apMKhwfnsgGyHFFWPOGWbtS0RQehaV6cJmpy6jykuTHsQbM3sz_d-dL3a7gzYtinS6uBwTai-Ju7FDpSNbysaDzRtZL2qbLZ3WNoeYmjA75hJHvnK217dcNg4HLQNB5Dv_zR3f_4EdTdB3Embux_uHhHeNy_9Q4aikasNzz29MDGer2Bm5M4CV-JX-zDcN4lOTOwn5OJMMy-gcOqjc0gSpWZTFX76SHeMRX137jp3jEV33_cfx6IPGovGTpToMCFJU_-zx6Jp1WZ5W0OH4NKW6IfPSvfgNGgDe4BiXGhRqmtmP4FUvA6Mv_i8iSrKti3aKwlaBoZW2YsDSUCxFqUcMq6eKz6OTx_Hp4_j08fx6eP49HF8-jg-fRyfPo5PH8enj-PTx_Hp4_j0_2h8evHhv61s3GI)

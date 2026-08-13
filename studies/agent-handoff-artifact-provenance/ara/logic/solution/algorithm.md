[//]: # (ob:bfcfd57a)
# Admission decision procedure

[//]: # (ob:8ab82529)
## Inputs

[//]: # (ob:a92eaa2d)
- A readable handoff containing inherited claims and decisions.
- A verifiable carrier naming the accepted artifact revision and governing admission state.
- The artifact revision currently held by the receiver.
- An affected-claim map when selective recovery is available.

[//]: # (ob:93115f81)
## Procedure

[//]: # (ob:73212bc1)
1. Verify carrier integrity and declared lineage.
2. Resolve the accepted artifact revision under the stated admission control.
3. Compute or verify the identity of the current artifact.
4. If integrity, lineage, or admission state cannot be established, return `stop/refuse`.
5. If the current artifact matches the accepted revision, return `proceed`.
6. If the artifact changed but no inherited claim is affected under the declared map, return `proceed` and record the checked change.
7. If one or more inherited claims may be affected, return `targeted_revalidate` with those claims as the revalidation scope.

[//]: # (ob:39339de2)
## Safety boundary

[//]: # (ob:fe7cb6f9)
The procedure verifies identity, integrity, declared history, and applicability under the configured policy. It does not establish claim truth, legal correctness, the completeness of the affected-claim map, or authorization that was never represented in the admission state.

[//]: # (ob:f8ab03ad)
## Implementation reference

[//]: # (ob:dd254c1e)
The persistent implementation is `proofpress.py`, exposed in this package through `src/execution/proofpress.py`; the link must resolve at the tagged repository revision used for release. Protocol objects and trust assumptions are specified in `architecture.md`.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2I3YjE5OTc1M2M0OGYwODU2OWJhMjMzYSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjE5YTg1ZjQzIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9hYTk0NGNjZWY3ZjcxNjViM2Q4NjJkYTciLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzcyNzUwOWU2NmQ0YTU2ZDUzZDAyNDI5MCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWcly28oV_ZUueBmKxDwwKycrr-J6cWXzoqIaPZCIQDReNyCZUenfc7oBkKAk07Kc4aVKG5cIdN_5nnsu_OBR3VWSsm5TcW_tte2mzMqgKLIkYnEu_TxJi5KGUUS9hVcqftjwaitMh7NmR8MkXcu4lGGeyiKMqB_lqfCzjAeMh0GQ58z3yzIt8jKNs6SMuQwKmYRREmdhEtCA0yKEXF4Zpu6EPnjrB_uj23R0Cw2N-NrhdU1LUePn34SuZEXLWhAt7ipTqYbscFrpAykP5LNWSrZaGIM7LWW3dCusS2ePtfqHgLO9tgJ3Xdea9Wq1rbpdXy6Z2q_YTjT7qtl2tNnmkb86u63Fb32Fvze9EXrDVGNEg0h0uhePC28nqA1hUNA8kXHkDU824s4dQmjFhtIijhkTMpNZkCZlxPM05DSzlindWdc2ddUIWD7lo95kYZb4hUhTHtMk5UnE_TAOC39wZ7Ruw2hr-hoOh9ZOpjQ33vrXB29U_-Ahx0ob-9fwWvBNiYD_6vXNbaPuG-8aPkzVANXia4t473Hb2ChADG2Y2Oxow5WUK6rpqlbbiq2MqvsOuVjReqs0Qrlf7rm3-KHKol2nq9KJ2ZTUVMbWl6jlhhqEuhNOXt_tlLYO3FaNFWkOphN7vGno3mZ6cmSBq8ZWh7du-rqGWwxWo2pdQMpasVucLiWTPMmsdmSys6W29j7yfeWuEi7YUGHwnQnea4GDo2LKubOotWUo7vHkA_nOze7QWhNtRaC6vMfFyZCclnmYhMWZIZ-atu_MRZUfyPHQBenoMEFpyH9Q-hX5iCaj3HXbmHNiBdCqgQpSNTtUBxJDWE2rvSE4Mnl-MqhGd55ZU0RBkMg8OLPm86si_IF8fl08sygMwpK9QUewJA5jDoRRrSuh4WYntvDzMPlXUw2fxx5d_r0Jl-QXgQ64Exe8joooKrgIzyz6K5UCckvVN5wC-i77_vz0hQhIkbESiPxWfV924lS85M7BrjCk4gADxGJxCsviFJMRiU-WtYCIc7NQ6X5En5Tivq2FRRlqmx81J4UWAJrvlf63r10IDOdhErNA_LQFLkJCA6g6XCTVuYjKkJsTNC_bw82CAE6VQZiq5mmErhcTSHt3ViQgkKH1BtBzbyYEFRsRizziYVgUiYilDII0jkpfpBYEVedkjnNkqlGCicZuW4WUubGonSaLi9MvC4vXdgDVFTvMJMyH0kyIG3dvnFdGyW4jkRWhW12NY9GUwTrL0jBgMip8P0uj1I-KMoyCQpQJ_C38NIg5ywofHCPgvvRpkcVJghhQFqUYuBbEDYLvxtuQrXUB3LcPvNAP0ys_vwqiL36xTvJ1lP_B99e-NWgMOE6xpMyKTHLUy-npw_9sILqKHQbWjpqddSMsM8mSzI9Sm24nYzbDxmJ-yyAaFcg0K6IClC1k8aRgNpsmBZfHzigrSiRLo1xmPo8mWbNJNMr6mSHTGKCvFXB3YoUTaoMP2OsdmpSCbbVWwhT8E3W0wraWdjpd9Bg2W0jCCbdd_vwe67Vtm_pAdqLmlnlaRSBVooKwwSpIlxJEU_ArZzrZ05bcg1sSsBo8x0l7w5FeCxf0jla19WH5whiZ8lPEKWdJXIZhPsV0Nk9P-fn8qnQHNGa-yDkv0mwSNxudo7ifGonfywAmEQTaQy7mfJYEWwVa1RAXLcmf1R4VJ4jSQ7aHiE_jiCjpfo95OerB3XhJPsn5tBqtXFhRTzIOBxtgKCkFwX6DXFRmJ_gC1na9bsgNplu7wnAA97-B6MSJfkkvct0BL82595PTJ4GuKwW3wtKjsKOQgbKivPqONOppK7iaGStsFsZjNlBuzxW5hA3kfzDcgrqV6FTBjMyZoRoX6b3C7H_WgXt6sBGadJ-UdFRvBZ5s4CitK46I3pB7gB9UYfAdO9iM3TIecuFnqr1U-Cm2JJHHIs2zYqrUGaU6Ff6rSNIoNAYWyTIL_CI-Cp3xplHozzChhYs3xUisGC2r2pbqKVUocFlte3t-mLyIfUe4gnRbhccSHPONodvtUL9iS2vcRcWxrgG5WIzCLAEBFcGTqR2eA9BQ9W6Lqv45hL7b0Y7cIykNiIZGWixjgW-OqAxinuDiC_xujCjL_BIDOsxjSY8RPVG-2fz4Ie425SvxoyyMU0bZEf1mdG6erzfyMriLA-OHA_zQqt_u0PearcRXwYaRfn59abG2U0zVRJX2w8IwopAsAzwwpt-39haeonpMi8mF8nG6bqhmOzQWQ_cI0IObZ4G9frTev7C-C24bclze_9KK5uMnICQXX71r90WA9-ybr5-s_s9f_9aj8o7vf6mADUCLLwCI_7_vA0ijI73j5wHmvHzdx4E3Lgp7xV2GX6D4A_59S8nz-yOd_8j5gJgd3WIcXGnQB2osgLpPUdYa0qlhHp6b59g6-MigfXLiwbvfWZL_p6rhF25ZmXTUSdoeSMTIqNoS5FfvKxc-eA0OzheROQufLycP_6UUvX7XOu4aR2nr4PHlbeJ7m9W_ZX2ijGdBGZVYhngUMZicFYEIhF-ULEklSJ0MWB4wv8C_RUwDbFFxgoUiyZMkCpNvu_R0gwqwOOXrMHhhgzp--HzfoN43qPcN6n2Det-g3jeo9w3qd7NBpZHIg8CPLCP43WxQf3QhAqjckr1dmvSIewjqifXaqCpTuf_oPUGf1SmVnnjpf3gXu378FxAVhic)

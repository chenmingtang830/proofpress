[//]: # (ob:5cd87791)
# proofpress

[//]: # (ob:095b959e)
For accepted, meaningful revisions to Markdown or static HTML knowledge
artifacts—never source code—close this loop. Do not snapshot every
conversational turn.

[//]: # (ob:211b5d98)
Before editing an existing target, run
`python3 proofpress.py capture --recorder pi-preflight <file>`. This preserves
any human drift without guessing its author or reason. Then:

[//]: # (ob:87ce54bb)
1. Read `python3 proofpress.py policy <file>`. If the user asks for portability,

[//]: # (ob:72f291a2)
   run `policy <file> portable` once; it remains sticky. Use `ingest <file>` for
   Git history not yet represented in the ledger.

[//]: # (ob:85972ea6)
2. Preserve carrier-native block anchors while editing: Markdown uses invisible

[//]: # (ob:b9f8ef49)
   `ob` markers; static HTML uses `data-proofpress-id`. Then run `anchor <file>`
   and inspect inherited/new/gone IDs.

[//]: # (ob:6f0d23b1)
3. Write claims JSON with one honest item per touched or removed block. Do not

[//]: # (ob:28f53262)
   enumerate untouched blocks.

[//]: # (ob:abd7c833)
4. Snapshot with `--why`, claims, and explicit actors:

[//]: # (ob:2c10e48d)
   ```sh
   python3 proofpress.py snapshot <file> --kind agent --author pi \
     --produced-by pi --recorded-by pi \
     --attribution-basis harness_attested --note "<changelog>" \
     --claims <claims.json> --why "<actual reason>" \
     --rejected "<consequential dead branch — reason>"
   ```

[//]: # (ob:4386e1e7)
   Omit `--rejected` unless the dead branch matters later. Never infer it from
   casual discussion or capture raw prompts/transcripts.

[//]: # (ob:dd7291a6)
5. Run `verify <file>` and report its output verbatim. Never re-snapshot just to

[//]: # (ob:8ac28d76)
   force green.

[//]: # (ob:2f7730eb)
For an incoming file with a `proofpress:discovery` marker but no local CLI,
tell the user it carries verifiable revision history, show the marker's
canonical project URL, and ask whether to install `proofpress`. Never
download or execute it without explicit consent. If the CLI is available, run
`inspect` before trusting the capsule and then `import`.

[//]: # (ob:19334051)
For parallel portable copies of the same artifact, preserve every input and run
`merge-plan TARGET --from COPY...`. Apply compatible block changes, ask the
user only about reported semantic conflicts, then `anchor` the resolved target,
write merge-relative claims, run `merge TARGET --from COPY...` with explicit
actors/reason, and `verify`. Different artifact IDs or portable lineages are
ingredients; use `merge-lineage` for them.

[//]: # (ob:72680124)
Fallback `capture` records only `recorded_by`; it cannot know authorship or
reasoning.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2M3Y2UwZDE1Yjg2YmI0MmJkMjg0MzRmYyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjYxMmVkMGVlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9mNTg2Yjk3OTFmMDQyNzllOTEzMTUwZDAiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzJlYjI2MDUwMDFmYTQ5Yzc5ZWJjNDUwZiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNq1WO2O29YRfZUL9Ud_VNLyUyRlI0CatKkLJw4cp0WRNaT7RelmKZK5JHctGAb6EH3CPknPXJIS7XoVRNsChleiyLkzZ2bOnOH7GbetyblsN0bN1rO63shEak_5sUhXQkSBUEEahVEuZ_OZqNRxo8xONy3ubfY8iFfrwPeVTHmu02wVe4prrXka-GHgpTpbrTIZSRGLMNChUnEehzJdeXGYyERHgYr9DHaVaWR1r-1xtn5PX9pNy3c4odTvWvxccKELfP2btiY3XBSaWX1vGlOVbI-7K3tk4si-t1WV11Y3DZ6pubzjO00hfXTZVj9rBNtZMrhv27pZ39zsTLvvxFJWhxu51-XBlLuWl7s09G4-etrqXzqDz5uu0XYjq7LRJZBobac_zGd7zQnClR9o5Wk9669s9L27CdDqTR4D1CzJ_NyLgiTTmR_6wMwjzyrbUmibwpQano_5KDaBFgEg8zw_51Em8ZiQUezlfTiDdxvJ66YrEHBAfsrKqma2_un9bDj-_Qw5rmxDn_qftdoIAP7TTFZKv5u9RQRjLVBy70xRNDe1mSCwcBeXBzWb_6ay4W1rjeha5GsjeGMagp7bktzGb6gm7Ux27b6y5OCdKclqc8QvB_xS8gNlsnd0PmvwIGzN1mVXFHBb7pEs3Ycrikre4d5YqjQB0LgdeWqpkD4pheEQrpQ7vaaS0g-48jv20X3tsabDKZeoi9mH-fkQL4tFFmf6ikP-XFnGpdQ1Yp-zg-YljOddcarshrUV-5bbO1U9lAx3Ny1vjWR_efPt2amaW_6RR2hGEassvcKjP-q8spppZVq4wnjJ9Ds0F31uud3pds5sV96W2_qIPJXhBKVlfcGlFIURR0Jc4ZK_ZK8BO_vskUdWV4WRR_Y8N4X-YrtkL3LW7jWj5mT87FGBKD7yKAnyIPN5cIVHjBEIcGh6NBt7d8uqUupnzLRI44EbJBEAyrvjkv3Y6EsYxVkSaL66wqNgCeLTCPleM8mtNdouSlQKvjrrSKREWzXsYQ9fx_SuXWldwEhkearzKLsOo20ltuyAE7Rtnk0q9yUlp2FbxVu-mBCLUUjfG1DvBYxWuaeCUFzT0eGS_d2aFgAV3Bwa9tcfXn3HHkD6yJdmqCxQEJKmD6xG6bRVhymgqOeso5_HMApSjLNgdWUd6bI7aMvhVVeORzrLzfICClyoRKZheMWZ0ZL9UGJK7Ku2D367WDzsj9v5AMscpaLQ9DVKGxXcz4v1pfil7-koVVfWyHbb7G9LfPp8dzejr0OTLRZkjdFQP7lEE-Ejl6IwXWlfJ9e59OqAuIGK1SQStNoiNQUec7SiiImEpXZCaWNsoacKpM8u2XcXEqZUQmRzTWvHoD8im3vSPSeec1mymjgHNduwqmvrrmW4SaDNDvAGI99eSFvKZZCqZHUdRhgSUrOd1bq8VKdBniShp8W1o7FkpoQeo-lDYfcFy0G8JxPrk2ocqYaJ7oJHfhaGkRf7V3pE9opCFyeyZ7KqDcis6qdOA43CRlU0Z_XIyRc8SoJV6vlBdI1H8EVA4rItdF_bWYyeQfSB0ooj20403tYNJMnLEs10V1afevR2PorEGdAk7bGRVvNelLlfRpF3UcDCurM5wjPoWAZik3d1ZcrWyXLrTiLlNn4j4faWBDCN1ImFqSieGHFy-0q93FR5u8lRVNrW1gyyvBH-2uexF0Wer70wzgLhiSRUcaAD7auYJ1IFfhIkcb7KlfK8PE9U7mG5Ef5K8lhJQWOSppyT13221n4CaUpXZoEXrBZesghWb7xkHYXrIPuD5609Qm1AfLo3fJhcff__0uT9pHGSec-bPXGpTFMhucy5o09nY6Kih_L8dXE8mMt8Feo8jVdS5KO5iV4ezD1FBr-kYn4otNrp23KMvfn3P_9VEgGypuqIqWhE4JosqkajUQ1Iu6rqJfu6YtQPpylDzxxvwTklgc9pWeEFQ2t9luaGINM8jQS1cZiEY5ATCT4E-SRlfWRDhzOaS66pQUYG6knnhdnt27P-fUPRjcTTAJPyyPbdAecpDJB-6GNasF1HCxROp_HRb1292OFNVfY6bP14zOh2EeVCYKGXY8wTjT_E_BTp3tw1NGYGpjWFaY_zz8yz0Z9ARjjfD0N1KrSJwh_8eYpwZ1tijOaENDnnhMs3uH98AUHFdNT0vMsA6FxhhLmoXInaC2WkgyhdRYEXR546QXpeCYYQnqL0Xfc47W1KaqyeXh9BNNARF7kfqDhKR3cm-8AZ0atlfp-L3t8RVYcoaRugX0N-4e9ek2pXN6V-uNmRVH_xdXMBRhUoyFEvV6E4VeZkaxj8fsoyALkxiPSRQB5HkSe5L2SchrF7F9Rzw3ljOKP42xaBwXqc8yzRmDSBEqP1yW4wWP-fSf7hVD9N8jDDVMyS06mTLWBSGVeL-7LFl4GUasNub50VhouwoDqp1UIc6ZcTHY4XJrdO3jgt3Bsn9un7JtxEgoXdzp73r4-KavfF7WxqZKiP5_3f5c8gR3IU-NFTwKrjxUCanzw57g_OOr0l_KVDXAa3T5cITKXz4-5ZoPaZ3WbAHhBnQbjycgzqEfvJunPG_uotxo1NU-b0f8tyWx2cV5I3FCnJ7c69eKNmGIeS5Q-U2kPdNjctzDbSGny-ULlZ7GU8y7SMk2iMY7IkDXE8ZffBHYtTgf3coZ3b6vGajnUCTZSn0IirE_meV6Qzrr-y-YxcHsbSUxySID5LgvMyNNU9V-44LXgHIkYiJ1-9fDG_xagpivP4dFqfpkPD7h9_YT5nQOfBPdUb_j0EA3aEqjRkeHhPzn58_bLnCAxlzBWN-4kTiaNbrCBTX7cD-rclDZui4o409TstO_SZOcuPE90ML9BP0x_RMLQqv-emIKdHWTQMhC0TvZDCAjCopz1NQvfe2znZ0mjZmgPVx_ZCjoTHPR544OLEG3M0WQ8nObp263NqEihRdbqadYGA5nd6URfI_JsvX3_zpzfgCmoz9tWr7_-xXC4B4ZfYYCD50FAoaDqvH-3DK-65ywMOvi1drt2uxwWh2ncFOKeBgClpEANeKERI4vkATD9vt85xOFoVNM0GBXpbPrih2LtoddELi3FMuHntfnvE8754x9RCe7pRctPzW19CQy8jyK9NDpIhqh-ho8nOTpLvvD2iGiyCRbIt9Awti8-oygdfFsNdTpFRWIdLvBPJOA4zkQsuzjrxtIGPSX_CYv0wiOlmb2pGErGPHs7_l1tvP-DffwAxzScO)

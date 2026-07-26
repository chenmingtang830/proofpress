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
   run `policy <file> portable` once; it remains sticky. Use `ingest <file>` for
   Git history not yet represented in the ledger.
2. Preserve carrier-native block anchors while editing: Markdown uses invisible
   `ob` markers; static HTML uses `data-proofpress-id`. Then run `anchor <file>`
   and inspect inherited/new/gone IDs.
3. Write claims JSON with one honest item per touched or removed block. Do not
   enumerate untouched blocks.
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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2M3Y2UwZDE1Yjg2YmI0MmJkMjg0MzRmYyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6Ijc2MDE0MWRiIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85ZmI2M2QxOTQxYjg1OTljMjkyYWU1NmMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzJlYjI2MDUwMDFmYTQ5Yzc5ZWJjNDUwZiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtW-luI8cRfpUG8yM_QlIzPTdtGHDsxHawPmCvEwTmguyTnNVwZjyHtIywQB4iT5gnSVXPwZFEcWVqRa8d_pHIObruqq-qwJsRK6pYM1EtYjmajfJ8IQKhLGl7PPQ5dymXNHQdV4vReMQzuV3IeKXKCp4t14x6_sx1nVBr5giHRY5i0hZCMEYtn0oeWU6gI06VGwnbjmgkpWMHKqSMy5AJqR0dwLkyLkV2pYrtaHaDX6pFxVZAIWEVkhrDB64SuPB3VcQ6ZjxRpFBXcRlnKVnD81mxJXxLviuyTOeFKkt4J2fikq0UCnXrcpG9ViBuXeCB66rKy9nFxSqu1jWfimxzIdYq3cTpqmLpKnSsi1tvF-rnOobPi7pUxUJkaalS0EVV1OrteLQG8eHQwLds15Z81FxZqCvzEChXLSLNfUfakWvz0IsiQSPKlOejdvOsqFC0RRKnCjjvLJIsqOLUtzzLsjUDTQaR4sL1LN2I03K3ECwv6wQEpsinyApZjmY_3Yxa8jcjsHJWlPipua3kgoPKfxqJTKo3o1cgQecNaN7LOEnKizweaGBiLk43cjT-RY7DqqqIeV2BvRaclXGJqmdFimzDPTCyMkfW1TorkMHLOMVTyy3c2cCdlG3Qkg2j41EJL8JZo1laJwmwLdZgLNWIy5NMXMKznpBhEEQ2PA52qtSb6q4rtESYlIZ6ji6lruHKH8it56ptjsTRluAXo7fjHREr8njkReoIIn_NCsKEUDnIPiYbxVI4XNdJ79klqTLyNSsuZXadEni6rFgVC_Lly693TOWsYLc4orbNPRmFR3D0Z6WzQhEl4wpYISwl6g0EF36uWLFS1ZgUdTpPl_kW7JQ6Ay1N8wMsheAYnsv5ESzZU_I9qJ3sJbkleZbEYks-1nGiPllOyVeaVGtFMDgJ23GUgBS3OAqoppHN6BEcEYJKAIaGpEkXu0uSpUJ9ROIKzLhhMRgRFCgut1PyY6kO6ciLAqqYfwRHdAqJT4HIV4oIVhSxKiYpeAp8NaeDIQWEVUmu18BrZ96Zca0DOuKRDpV2o-N0tMz4kmyAgirKjwae-wKNU5KlZBWbDBJLLMF8LyH1HtCRry1JHX5MRDtT8o8irkBBCYs3JfnbD99-Q64h6YO9FAHPghQERlMbkoPrVFkNVUBizBUm_TykIxpqz6H-kX6k0nqjCqhxpE47kubkcnpAC1A6AxE6zhE03Sn5IYUqsc6qRvjlZHK93i7HrVrG4CoSgj4H1wYPburF7JD8wraUG8ojfWS5LNfzFD7tj-6y47UNsskETyNY1HuWsCLcYgnQiK9sFRzH0rcbkBu0UigECUouwTQJvGbSisRMxAsMJ3BtKFsQUwhRiin55oDBpAww2RwT2h6kP0w2V4h7-jxnrFQozDngsyXJ6iqvKwIPcQizDXADJb84YDaAXjSUgX-cjqBICEVWhVLpIT-lOggcS_FjS2NK4hTwGFYfFLtxWAaJtz9i1uPGLtUQXh_gyI4cx7U8-0iO8LwkUUmf7InI8hiSWdZUnRIwCulQ0ZjkXU4-wFFA_dCyqXsMR8ALB4hLloD7qrqA0tOCPkhpyZYsBxhvaQqSYGkKwXSZZnc5ejXuQOIItInYYyEKxRpQZu50IE8ttAfwLgJcpS2XAhKNbMf2LGkhSMsqc2annhbHEkhs4jLP4rQysLwwlBC5dd8QuL1CAIwldXDCEBQPDjFw-0i8XGa6WmhwKlXkRdzC8pLbM5t5lutatrIcL6Lc4oEjPaqosqXHAiGpHdDA076W0rK0DqS2VORz2xfMk4JjmcQqZ-B1Y62ZHQA0xSsjalF_YgUT6r-0gpnrzGj0J8uaWai1VuNY32yqpKUwn-2u3jwXJm8qjYHMa1auMZeKMOSCCc1M-jRnDFB0657vBsftcZEtHaVDaG647o4b4OX2uKfA4BfozNeJkis1TzvZy__--z8pJkBSZjVmKiwRcE0kWakgUGNI2lmWT8nnGcF46KsMvrOdQ85JUfkMmxWWEAitvWmuFTLUocsxjJ3A6YQcQPBWyCch6y1pI5xgXTJBDckoBvSkdBKv1tUO_75E6brEU4JO0i1Z1xugJ6GANEUfqgVZ1dhAAXUsH03X1YAdVmZpg8NmD8sM0c5dzaGtd0Qn8wDjtzI_BbqXlyWWmTbTxklcbcd76lnHDxUu0LcdR_aONkD4LT9PAe5kiRmj7DWNzBng8gU83w0g0Jm2Ct83FoB0LqGEGamMixYH3EhRN_RdanmuJXuV7lqCVoSnIH0TPQZ7xykGVpNeH9AoVS7j2qbSc8OOnUE_sNPo0TC_sUXDb6dVo1HENqD9HOAX_F8rRO3yIlXXFyuE6l99Xh5Qo6QS4KilpcN7zxx0DS3fT2kGAG60IL1LIA9rkQXa5sILHU-pPjfsOoadFn9ZI9Ce7mkWBQoqDTWTJnP6oDdoT39vkL-laoeBdiKoilHQUx10AQPPOBrcpxV8aZNSHpP53JxC4CKcIGuh5IRv8U6fDrsLg0cHE6eJmTiRu_MmeAgBC5mPPm7GR0m2-mQ-Gh7S-sfHzf_pa0iOyCjoD98CXdUsaZPmnTe7_sGcjlPCn2uQK4bHh00EVKXd6-Zd0Nqe3qbVPag4oo5vaSjUne4H7c5O90d3MaZsxqnGvxXRRbYxXAlWoqQIt2szeMNg6IpSwa7RtJu8Ki8qOLYURQyfD3hu5FkRiyIlvMDt5Bg0Sa0cT-l94IlJ72CvawjnKnvYpz0VACbSIWBEv0--uxZpp9d3dD5dLnc8YUkGkMDbQYJdMzTEPUf2OBXkHQAxAmzy2YuvxnMoNUmyK58G62N1KMnVwwPzMQHtXJu3moP_CIABeoQsjfHgdk5Ofvz-RZMjoChDXVHwPOZEzNEVtCBDXpet9ucpFpskYyZpqjdK1BBn8Q5-9OmmHaD31R-kIRCq7IrFCTLdwaK2ICwJb4AUNAAtelpjJTRzb8NkhaVlGW_QP5YHbMQtZjFqQS4OrM5Gg_ZwYKNjuz6DJkFL6J3GZ40gkOZXapInYPmXn37_xV9eQq7AMCOfffvdP6fTKajwU-hgAPJBQIFDI72mtLcj7rGxAxCep8bWptdjHLXaRAXknBIATIqFGNQLCBEg8bhVTFNvl4ZxYDRLsJq1CHSeXpui2LBYqKQBFl2ZMPXa3HuA88Z5O9MC9jSl5KLJb40LtbEMQn4ea0gymOo71WFlJz3k23WP4A0FCAvGLgDPYLP4EXp5y8ukfcogMhRrcyjvuMLznIhrzvgOJ_YdeGf0JzTW1y2YLtdxThAiNtID8_fYevUWOduzm0HUdnczY_Y8pvTdvb5_k9MsqkyZa28UMThQIXGpdepFT6kSvWAleOsDWx5T849b8jx6tbDJJCRCQ__BqdhjR_CPOOvRo-pHnPXo-eEjztq7-Nid0ALcUyw89q4X3snJc6wV9g7x38nJccP7vZPXd9I6hDsg1psU_VBc3HeOdk73GZSYRGHBwHIABCd5zcHGgAZrBIc9YGghF4shAxN0qbbPNGntgQg6IdVBrJ2Q6iAqT0h1EL_3XObZiA5C9XREB1F5OqKD8Hxmoq8GCeBmBB2lKXzHHN0Pd27TwCHyo4f6MrAV09SxOKXMFdQNqc9c1-3FHk7rh5Pq4QT_5lyhzxX6XKGnD23XHrVD63dIvavM3HFPdea-3b8wetf27INbkT0s3t2Fme3MrGBG6Z6FWSB9SgNNzwuz88LsQ16YBQyinQkeOhY93cLMjG4_nJXXve0ItzQkHDegXniylVczZP91l1Z3FeH4vvZtn0vtqFMtrQzXjyqQ94bl57XTee30m1w7hYBIAg79jWT6dGsnI8l-eHjXyc-Lo_Pi6Lw4Oi-Ozouj38Hi6PDI4Jl-s7F3qHWYk2f6ZcTeXykc5uT9YMbj9yHfZMWGJfG_QDwmXzOBSeb2cLXtGUzKgOgpsMxBO_RlzUEbKXSZj9iI3BsoPwfZ-yuRk5AdGP3Zye4boKfv5fBfNDk_8HvOvZPzfmT1AUzOzynqV0tRj9-_7JmY2oOJqfN2_0D0NzwQvivenoGwTWduuG8g3P3y-jwQPg-EP-CBMLUUZdKRLOTs_2wgPE9_NyPdeXraoew8PY9Vz2PV81j1PFY9j1XPY9XzWPV9j1Vfvf0f_pslmw)

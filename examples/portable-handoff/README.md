[//]: # (ob:ed304302)
# Portable handoff demo

[//]: # (ob:894f03f7)
`strategy.md` is a self-contained Proofpress artifact. It has a real v1 → v2
revision record embedded in the file: a general volunteer session became a
focused planting day, with the stated reason, a consequential rejected
direction, and a checkable claim about the actual document change.

[//]: # (ob:6f729c3c)
To test the handoff as a recipient with no access to the source repository or
original session, start in a clean Git repository, install the current stable
release, and copy only `strategy.md` into it:

[//]: # (ob:0141eb16)
```sh
npm install --save-dev proofpress
curl -LO https://raw.githubusercontent.com/chenmingtang830/proofpress/main/examples/portable-handoff/strategy.md
npx --no-install proofpress inspect strategy.md
npx --no-install proofpress import strategy.md
npx --no-install proofpress verify strategy.md
```

[//]: # (ob:80c71b17)
`inspect` checks the portable capsule before importing. `import` reconstructs a
local ledger from the artifact alone. `verify` checks the recorded v2 claim
against the artifact's computed change; it does not present the stated reason or
actor identity as independently proven fact.

[//]: # (ob:20be43e3)
The demo intentionally uses fictional, non-sensitive community-planning
content. It is a proof object for the portable format, not a product
recommendation.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzExODc0OGU5NzQ5NDEzYTJmNWZiZGE0NCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImMxODY0ZGJhIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8wNGQ3YWZmMTY3YzAwZTA5ZjBmZTdmMDEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2U3ZmMyNDU2OTc3ZDNlMTQ3YWM4YjBhMCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNq1VttuGzcQ_RVi-9CHStbetBf1qUCDokCLFkXQl9iQeZVY75IbkqtYMPzaD-gn9ks6sxdbSuI0qVBADytyODxzZuYMHyLqglaUh60W0Sbqum2SVGVeybrM6zzJaKrWigma59EiYlYct0LvpA9g6_c0XRebmMdrJUtGRcVUzfOy4qJSnJZZLWSteFLzuGKFUrVMExrzTNF1nVWFqFOWpwr9Cu25PUh3jDYP-CdsA93BDUbeB9huKJMN_P1dOq00ZY0kTh6019aQPVhbdyTsSH511qrOSe_hTEf5Hd1JDOls2dk_JATbO3S4D6Hzm9Vqp8O-Z1fctiu-l6bVZheo2VVZvDo77eTbXsP3tvfSbbk1XhpgIrhePi6ivaRIIU-qIheMRuPKVh4GI6BWbuNclFSppCh5HMu4VjEwp-IEkVkXMLRto40E5HM-mi1Y8DRfF3VZikwmeUl5xWIaj-FM6Lacdr5vIOAUcXLrhI82bx6i6fqHCHJsncevcVuKLQPC30TcCnkf3UAEcy3AxfKetl0j_WrGtdxTI6xSq99efff9z6-uWhEtvqh4aAhOsz5A1raMeu0xAdQZBA97UFNycNmHvXUI804b9OqPsNPCjqEt5nOEu4g8HARf0cb0TQPgOQCEyhyCZo3ldxiFyOI8i1Mwh2wFLKdN9OsUEZkiIkK2Fiym-6gQA5AOa0y-g5WvyEtHwrFDSJhnqJnocfF8dVXnKs5UednVtz44GuTuCHzfEu0JJV42aokuKRSKOKl6MmfjivwY4IZnfB119Axcocq05hm_DNxrSzBtJOyfz1CECAWmOw11R95BZxFjCeUcEQY7GHvbfwJcnOSJZElxIXO3t35_bUzXEm18oE1DlktPD3Ip5IE8N8614SAGZPnTL2SWA0ffPcPDcjtPbMzLhCWXJhZAdaBEtwQUh9_5gZe518jUzIRJZZ0kusUdqLArcgvfn-AujZnMM5ldmFjAgjbAXIAsQpcBfUcCqueJ0nxcWEBezRIU0OugD4DZtm1v9PvgbhazBEWg8NixW-4kHZt92JnF45PyaGwYfM6hTCo5stdZADqIvhtuQkWY_6Eg3KC8NpofTzycSu6Jk0HM_6Mae6vCVkGapOucnkTfs2RTMVoWBaghp5liVVWyMivXRZzUYl2wOC95JtZJnXBVV4pWdF3Kei0oB--FKDl2MlRwGMR7zNamAMXDBch4WizjcpkWr-Nyk2ebtPomjjcxApoIPx1KjyerD_-v4A81Oerxnvo92NdZmtW5zLIkY2Aw-DiR6Klcv0huJ8_AIEtzoRiNnzyfKPDk-RI1HXWNNuSQkL___Isc0mvz9AoZJyqRLZOYHuiboZ-VbuQGzu2kkQ6P2qaHjpKOTMMLGpzDVCP02ijLob8E6RpqsNWJoMfFqJ-DZAZsGUTgrVmAz-H18bbH9gTPTuKzRoprI-CBMnQoGBmBhljco6o0VLeEMtuPmg3B9XBWwM0tivU4Qa8-Ii8Ty-t1ts6zLBc8j2eWT0bJxPIlY8FxfNt1FjQFX3XWXRvr9E6D3sycLZALF5BjCK6R1JAfdDg5tXgSfHQK6o4ygIeAA8wZHPFyZIfbDi4xoG3vlYYBSDpsXqaipNWas5SnSVzPVJwMrrngLhpCV-O7FB-bg5ib8C9P1FULVbx6uZNPYkRQ9wDG2OWM7NkPmYYT-fwDw4T6fPsDPuWP5_ZA1kfG7sR3GhcqK2TMKcueGvx5Es98XzBV4ft2aGRA63oePHYlSBhUXiMFaDpRzrZj40zSQGhjjYTjYzhnt86PbBCKsfGuDd1RpOLMxdceB2fXY3OP_fctFB70JIxamHkE6cLy_UADht4Y3vREC1SBcMQug5EuO2lwBaoaGIcJSwYZe7mWk2wdq4KCFX3i9uQhMbf1BY-CcFyirhkgG0p9qmXU1UGDh7oglqGEEUjNedZgoaVhMbAx2ApIDvYx-oZIKd78QXQ3j_D7B85HDk0)

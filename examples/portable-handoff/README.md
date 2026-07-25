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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzExODc0OGU5NzQ5NDEzYTJmNWZiZGE0NCIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)

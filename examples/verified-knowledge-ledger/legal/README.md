[//]: # (ob:be77b7ea)
# Illustrative legal design-partner fixture

[//]: # (ob:aeb16898)
This fixture adapts the cold-boundary shape described in Proofpress PR 22: an
initial MSA position is followed by a counterparty redline and a changed
business priority before a successor agent continues the work.

[//]: # (ob:b3aa05bd)
It is fictional product-demo data. It is not legal advice, a Harvey result, or
evidence that Proofpress improves legal drafting quality.

[//]: # (ob:296d3fb1)
From a clean Git repository containing Proofpress, run:

[//]: # (ob:d55f115b)
```sh
python3 examples/verified-knowledge-ledger/legal/setup_fixture.py
python3 proofpress.py ui --scope msa-negotiation
```

[//]: # (ob:61b1b719)
The resulting local ledger contains admitted, needs-review, rejected, and
superseded conclusions. In **Trusted Context**, request scope
`msa-negotiation` as `agent:successor` to see exactly what crosses the handoff.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2JkYmFkNzU4N2UyZDI4ZjhlNjA0YTExOCIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)

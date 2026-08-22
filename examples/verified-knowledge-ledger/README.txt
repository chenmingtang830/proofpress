Verified Knowledge Ledger MVP fixture

Run from the repository root:

  python3 proofpress.py knowledge ingest examples/verified-knowledge-ledger/demo.otlp.json -o /tmp/coframe-ledger.json
  python3 proofpress.py knowledge propose /tmp/coframe-ledger.json
  python3 proofpress.py knowledge review /tmp/coframe-ledger.json --claim <claim-id> --decision accept --reviewer human:demo
  python3 proofpress.py knowledge context /tmp/coframe-ledger.json
  python3 proofpress.py knowledge verify /tmp/coframe-ledger.json

The fixture contains two complete experiments and one failed experiment. The
failed candidate cannot pass the deterministic admission gate. An admitted
claim is the only claim exposed in fresh-agent context; proposed and rejected
claims remain visible as open work.

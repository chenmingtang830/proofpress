# Synthetic task-run dogfood

`demo.py` creates an isolated temporary Git workspace, admits one clearly
synthetic fixture claim as a simulated human test owner, and records two task
runs with different output hashes. It demonstrates linkage and historical
traceability only. It is not evidence that the second run improved.

```sh
PYTHONPATH=src python3 examples/task-run-tracking/demo.py
```

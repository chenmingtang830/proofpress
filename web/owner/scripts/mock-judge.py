"""Offline fixture adapter. Never calls a model provider."""
import json
import sys
import time

packet = json.load(sys.stdin)
time.sleep(0.3)
if "provider-failure" in packet["conclusion"]["statement"]:
    raise SystemExit(1)
print(json.dumps({"recommendation": "accept", "rationale": "Synthetic advice: the quoted source supports the statement; experiment identity is not established.", "model": "fixture/offline-judge", "adapter": "test-only"}))

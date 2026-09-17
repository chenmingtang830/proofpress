"""Offline, temporary browser fixture. Never imported by production code."""
import io
import json
import os
from pathlib import Path
import runpy
import subprocess
from unittest.mock import patch

from cryptography.fernet import Fernet
from proofpress.hosted import jev
from proofpress.kernel import operations

os.environ["PROOFPRESS_SECRET_ENCRYPTION_KEY"] = Fernet.generate_key().decode()
# Do not inherit a developer's paid model configuration into synthetic tests.
os.environ.pop("PROOFPRESS_JUDGE_MODEL", None)
os.environ.pop("PROOFPRESS_TEST_JUDGE", None)
original_run = subprocess.run


def fake_http(request, timeout):
    payload = json.loads(request.data)
    answers = {}
    for key, question in payload["questions"].items():
        if question["type"] == "choice":
            answers[key] = {"type": "choice", "choice": "accept", "confidence": .95,
                            "probabilities": {"accept": .98, "reject": .01, "escalate": .01}}
        else:
            answers[key] = {"type": "noul", "noul": .99}
    return io.BytesIO(json.dumps({"model": "jev-OFFLINE-FIXTURE", "answers": answers,
                                 "usage": {"input_tokens": 100, "output_tokens": 12}}).encode())


def offline_run(command, *args, **kwargs):
    if "proofpress.hosted.judge" not in command:
        return original_run(command, *args, **kwargs)
    if "typesafe" not in command:
        return subprocess.CompletedProcess(command, 1, "", "Offline fixture only supports TypeSafe")
    with patch.dict(os.environ, kwargs["env"], clear=True):
        result = jev.judge(json.loads(kwargs["input"]), opener=fake_http)
    return subprocess.CompletedProcess(command, 0, json.dumps(result), "")


with patch.object(operations.subprocess, "run", side_effect=offline_run):
    runpy.run_path(str(Path(__file__).with_name("owner-fixture.py")), run_name="__main__")

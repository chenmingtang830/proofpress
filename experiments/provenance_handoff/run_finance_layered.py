#!/usr/bin/env python3
"""Production-repository entrypoint for the frozen Finance layered study."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from pp_eval.apex_ib_pr36 import (
    frozen_protocol,
    host_preflight,
    run_calibration_pair,
    run_formal_matrix,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("freeze", "preflight", "calibration", "formal"):
        item = sub.add_parser(name)
        item.add_argument("--world-zip", required=True)
        if name != "preflight":
            item.add_argument("--tasks", required=True)
        if name in {"calibration", "formal", "preflight"}:
            item.add_argument("--checkout", required=True)
        if name in {"calibration", "formal"}:
            item.add_argument("--results-root", required=True)
            item.add_argument("--env-file")
        if name == "preflight":
            item.add_argument("--formal", action="store_true")
        if name == "freeze":
            item.add_argument("--output", required=True)
    args = parser.parse_args()
    world = Path(args.world_zip)
    if args.command == "freeze":
        result = frozen_protocol(Path(args.tasks), world)
        Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    elif args.command == "preflight":
        result = host_preflight(Path(args.checkout), world, formal=args.formal)
    elif args.command == "calibration":
        result = run_calibration_pair(
            Path(args.checkout), Path(args.results_root), Path(args.tasks), world,
            env_file=Path(args.env_file) if args.env_file else None,
        )
    else:
        result = run_formal_matrix(
            Path(args.checkout), Path(args.results_root), Path(args.tasks), world,
            env_file=Path(args.env_file) if args.env_file else None,
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("status") in {"passed", "completed"} or args.command == "freeze" else 1


if __name__ == "__main__":
    raise SystemExit(main())

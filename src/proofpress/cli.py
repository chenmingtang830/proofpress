"""Canonical CLI with isolated governed-run tracking and legacy portable flows."""

import sys

from proofpress.legacy.portable import main as portable_main


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if args[:1] == ["run"]:
        from proofpress.run_tracking import main as run_main
        return run_main(args[1:])
    if args[:1] == ["experiment"]:
        from proofpress.external_experiment import main as experiment_main
        return experiment_main(args[1:])
    return portable_main(args)

__all__ = ["main"]


if __name__ == "__main__":
    main()

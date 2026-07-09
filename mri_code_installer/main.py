"""mri-code's CLI entry point — dispatches install (default) / update / uninstall via the
vendored mri-installer-kit engine, driven by this repo's Spec (see spec.py).
"""
import sys

# ruff: noqa: I001 — order is load-bearing, see spec.py.
from mri_code_installer.spec import SPEC  # triggers package init -> vendored engine on sys.path
from cli import make_cli  # vendored


def main() -> None:
    make_cli(SPEC)(sys.argv[1:])


if __name__ == "__main__":
    main()

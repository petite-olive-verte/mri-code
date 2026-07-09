"""mri-code's CLI entry point — dispatches install (default) / update / uninstall via the
vendored mri-installer-kit engine, driven by this repo's installer.toml.
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT / ".mri-installer-kit"))
from cli import make_cli  # noqa: E402 — vendored, must follow the sys.path.insert above
from engine import load_spec, resolve_version  # noqa: E402 — same

SPEC = load_spec(_REPO_ROOT / "installer.toml", version=resolve_version(_REPO_ROOT))


def main() -> None:
    make_cli(SPEC)(sys.argv[1:])


if __name__ == "__main__":
    main()

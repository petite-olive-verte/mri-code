"""Smoke test : garantit que le package s'importe."""

import __PACKAGE_NAME__


def test_package_importable() -> None:
    assert __PACKAGE_NAME__.__version__

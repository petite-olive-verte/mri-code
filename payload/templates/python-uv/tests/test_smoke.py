"""Smoke test: ensures the package imports."""

import __PACKAGE_NAME__


def test_package_importable() -> None:
    assert __PACKAGE_NAME__.__version__

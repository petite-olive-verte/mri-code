"""Generic install/update/uninstall CLI, driven by a Spec.

Vendored into a consuming module's repo (mri-code, mri-slides...) and invoked through that
module's own bin/cli.py with its Spec instance — see make_cli().
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable


# Bare (not relative) import: this file is vendored as a flat, standalone module into consuming
# repos' `.mri-installer-kit/`, where there is no parent package — `mri_installer_kit/__init__.py`
# puts this directory on sys.path so `engine` resolves the same way in both contexts.
from engine import (
    Spec,
    compute_managed_paths,
    deploy,
    manifest_path,
    read_config,
    read_manifest,
    remove_managed_paths,
    remove_path,
    strip_json_ownerships,
    strip_markdown_blocks,
)


def _flag(argv: list[str], name: str) -> str | None:
    if name in argv:
        i = argv.index(name)
        if i + 1 < len(argv):
            return argv[i + 1]
    return None


def _target_arg(argv: list[str]) -> str | None:
    for a in argv:
        if not a.startswith("-"):
            return a
    return None


def _resolve_config(argv: list[str], spec: Spec, existing: dict | None) -> dict:
    """existing=None -> install mode (prompts interactively on a TTY); a dict -> update mode
    (flag > existing value > default, never prompts)."""
    cfg: dict = {}
    interactive = existing is None and sys.stdin.isatty()
    for f in spec.config_fields:
        value = _flag(argv, f.flag)
        if value is None and existing is not None:
            value = existing.get(f.key)
        if value is None and interactive:
            default = f.default(cfg) if callable(f.default) else f.default
            suffix = f" [{default}]" if default else ""
            value = input(f"{f.prompt}{suffix}: ").strip() or None
        if value is None:
            value = f.default(cfg) if callable(f.default) else f.default
        cfg[f.key] = value or ""
    return cfg


def _config_summary(spec: Spec, config: dict) -> str:
    parts = [f"{f.key}={config.get(f.key) or '(unset)'}" for f in spec.config_fields]
    return " · ".join(parts)


def _container_dirs(spec: Spec) -> list[Path]:
    dirs: set[Path] = set()
    for nd in spec.named_entry_dirs:
        for sub in filter(None, [nd.target_sub, nd.mirror_target_sub]):
            p = Path(sub)
            dirs.add(p)
            dirs.add(p.parent)
    dirs.discard(Path("."))
    return sorted(dirs, key=lambda p: len(p.parts), reverse=True)


def _cleanup_empty_dirs(target: Path, spec: Spec) -> None:
    for d in _container_dirs(spec):
        p = target / d
        if p.is_dir() and not any(p.iterdir()):
            p.rmdir()


def run_install(argv: list[str], spec: Spec) -> None:
    target = Path(_target_arg(argv) or ".").resolve()
    target.mkdir(parents=True, exist_ok=True)
    config = _resolve_config(argv, spec, existing=None)

    print(f"==> Installing {spec.name} into: {target}")
    if spec.config_fields:
        print(f"    {_config_summary(spec, config)}")
    deploy(target, config, spec)
    print("==> Done.")


def run_update(argv: list[str], spec: Spec) -> None:
    target = Path(_target_arg(argv) or ".").resolve()
    old_manifest = read_manifest(target, spec)
    if old_manifest is None:
        print(
            f"No {spec.name} installation found in {target} "
            f"({spec.data_dir_name}/.manifest.json missing). Run the installer first.",
            file=sys.stderr,
        )
        sys.exit(1)

    existing_config = read_config(target, spec) or {}
    config = _resolve_config(argv, spec, existing=existing_config)

    print(f"==> Updating {spec.name} in: {target}")
    if spec.config_fields:
        print(f"    {_config_summary(spec, config)}")
    print(f"    {old_manifest.get('version')} -> {spec.version}")

    new_manifest = deploy(target, config, spec)

    kept = set(new_manifest["paths"])
    for p in old_manifest.get("paths", []):
        if p not in kept and (target / p).exists():
            remove_path(target / p)
            print(f"    removed stale: {p}")

    print("==> Update done.")


def run_uninstall(argv: list[str], spec: Spec) -> None:
    yes = "--yes" in argv or "-y" in argv
    target = Path(_target_arg(argv) or ".").resolve()

    manifest = read_manifest(target, spec)
    paths = manifest["paths"] if manifest else compute_managed_paths(spec)
    existing = [p for p in paths if (target / p).exists()]
    md_dsts = manifest.get("markdown_blocks", []) if manifest else [mb.dst for mb in spec.markdown_blocks]
    json_ownership = manifest.get("json_ownership", {}) if manifest else {}

    if not existing and manifest is None:
        print(f"Nothing to uninstall in {target}.")
        return
    if manifest is None:
        print("(No manifest found — using the current spec as a best-effort fallback.)")

    print(f"==> Will remove from {target}:")
    for p in existing:
        print(f"    - {p}")
    if md_dsts:
        print(f"    - {spec.name} block(s) in: {', '.join(md_dsts)}")
    if json_ownership:
        print(f"    - {spec.name} entries in: {', '.join(json_ownership)}")
    print(f"    - {spec.data_dir_name}/.manifest.json")
    if spec.preserve_in_data_dir:
        preserved = ", ".join(f"{spec.data_dir_name}/{d}/" for d in spec.preserve_in_data_dir)
        print(f"==> Preserved (never touched): {preserved}")

    if not yes:
        answer = input("Proceed? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("Aborted.")
            return

    remove_managed_paths(target, existing)
    strip_markdown_blocks(target, spec, md_dsts)
    strip_json_ownerships(target, json_ownership)
    remove_path(manifest_path(target, spec))
    _cleanup_empty_dirs(target, spec)

    print(f"==> Uninstalled {spec.name}.")


def make_cli(spec: Spec) -> Callable[[list[str]], None]:
    """Dispatches install (default) / update / uninstall (alias: remove)."""

    def cli(argv: list[str]) -> None:
        if not argv:
            run_install(argv, spec)
            return
        cmd, rest = argv[0], argv[1:]
        if cmd == "update":
            run_update(rest, spec)
        elif cmd in ("uninstall", "remove"):
            run_uninstall(rest, spec)
        elif cmd == "install":
            run_install(rest, spec)
        else:
            run_install(argv, spec)

    return cli

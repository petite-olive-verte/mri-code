"""mri-code's CLI entry point — install (default) / update / uninstall.

Single self-contained module: no vendored engine, no TOML spec. Deployment is deterministic and
local — skills, hooks and `.mri_code/` data are copied straight from `payload/`. The 4 files a
project may already own (AGENTS.md, CLAUDE.md, .mcp.json, .claude/settings.json) are **never**
written automatically, even when absent: install/update print their rendered content plus a
ready-to-paste prompt so the user (or their coding agent) decides how to integrate them.
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

NAME = "mri-code"
REPO_ROOT = Path(__file__).resolve().parent.parent
PAYLOAD = REPO_ROOT / "payload"
DATA_DIR = ".mri_code"
MANIFEST_NAME = ".manifest.json"
PRESERVE_IN_DATA_DIR = ["docs"]
SEED_ONCE_FILES = ["constitution.md", "models.md"]  # copied only if absent from the target
REFRESH_DIRS = ["templates"]  # always removed + recopied

# (payload_sub, target_sub, mirror_target_sub, chmod_subdir) — one entry per name is deployed
# individually, so foreign entries the user added under the same target_sub survive.
NAMED_ENTRY_DIRS = [
    ("skills", ".claude/skills", ".agents/skills", "scripts"),
    ("hooks", ".claude/hooks", None, None),
]

# (src in payload, dst in target, substitute placeholders) — never auto-written, see module doc.
SHARED_FILES = [
    ("AGENTS.md", "AGENTS.md", True),
    ("CLAUDE.md", "CLAUDE.md", True),
    ("mcp/servers.json", ".mcp.json", False),
    ("settings.json", ".claude/settings.json", False),
]

# (config key, CLI flag, prompt, default). document_language defaults to communication_language;
# resolved after communication_language so the fallback below can read it from the partial config.
CONFIG_FIELDS = [
    ("communication_language", "--lang", "Communication language", "English"),
    ("document_language", "--doc-lang", "Document language", None),
    ("user_name", "--user", "How should the agent address you?", ""),
]


# --- filesystem helpers -------------------------------------------------------------------

def mkdirp(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def copy_path(src: Path, dst: Path) -> None:
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def remove_path(p: Path) -> None:
    if p.is_symlink() or p.is_file():
        p.unlink(missing_ok=True)
    elif p.is_dir():
        shutil.rmtree(p, ignore_errors=True)


def resolve_version() -> str:
    version_file = REPO_ROOT / "VERSION"
    if version_file.exists():
        return version_file.read_text().strip()
    raise FileNotFoundError(f"no VERSION file under {REPO_ROOT}")


# --- placeholders --------------------------------------------------------------------------

def resolve_placeholders(config: dict) -> dict[str, str]:
    user_name = config.get("user_name") or ""
    return {
        "{{COMMUNICATION_LANGUAGE}}": config.get("communication_language", ""),
        "{{DOCUMENT_LANGUAGE}}": config.get("document_language", ""),
        "{{USER_NAME}}": user_name or "the user",
        "{{USER_ADDRESS}}": f"as {user_name}" if user_name else "directly (no preferred name set)",
    }


def substitute(text: str, mapping: dict[str, str]) -> str:
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text


# --- config resolution ----------------------------------------------------------------------

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


def resolve_config(argv: list[str], existing: dict | None) -> dict:
    """existing=None -> install mode (prompts interactively on a TTY); a dict -> update mode
    (flag > existing value > default, never prompts)."""
    cfg: dict = {}
    interactive = existing is None and sys.stdin.isatty()
    for key, flag, prompt, default in CONFIG_FIELDS:
        if default is None:  # document_language falls back to communication_language
            default = cfg.get("communication_language", "")
        value = _flag(argv, flag)
        if value is None and existing is not None:
            value = existing.get(key)
        if value is None and interactive:
            suffix = f" [{default}]" if default else ""
            value = input(f"{prompt}{suffix}: ").strip() or None
        if value is None:
            value = default
        cfg[key] = value or ""
    return cfg


def config_summary(config: dict) -> str:
    return " · ".join(f"{k}={v or '(unset)'}" for k, v in config.items())


# --- manifest -------------------------------------------------------------------------------

def manifest_path(target: Path) -> Path:
    return target / DATA_DIR / MANIFEST_NAME


def read_manifest(target: Path) -> dict | None:
    p = manifest_path(target)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def read_config(target: Path) -> dict | None:
    p = target / DATA_DIR / "config.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def compute_managed_paths() -> list[str]:
    paths: list[str] = []
    for payload_sub, target_sub, mirror_target_sub, _chmod_subdir in NAMED_ENTRY_DIRS:
        names = sorted(p.name for p in (PAYLOAD / payload_sub).iterdir())
        paths.extend(f"{target_sub}/{n}" for n in names)
        if mirror_target_sub:
            paths.extend(f"{mirror_target_sub}/{n}" for n in names)
    paths.extend(f"{DATA_DIR}/{f}" for f in SEED_ONCE_FILES)
    paths.extend(f"{DATA_DIR}/{d}" for d in REFRESH_DIRS)
    paths.append(f"{DATA_DIR}/config.json")
    return paths


# --- deploy (shared by install/update) ------------------------------------------------------

def deploy(target: Path, config: dict, *, version: str) -> dict:
    if not PAYLOAD.exists():
        raise FileNotFoundError(f"payload directory not found: {PAYLOAD}")

    data_dir = mkdirp(target / DATA_DIR)
    for sub in PRESERVE_IN_DATA_DIR:
        mkdirp(data_dir / sub)

    for f in SEED_ONCE_FILES:  # seed-once: never overwrite a file the user may have edited
        dst = data_dir / f
        if not dst.exists():
            copy_path(PAYLOAD / f, dst)
    for d in REFRESH_DIRS:  # always fresh
        remove_path(data_dir / d)
        copy_path(PAYLOAD / d, data_dir / d)

    (data_dir / "config.json").write_text(json.dumps(config, indent=2) + "\n")

    for payload_sub, target_sub, mirror_target_sub, chmod_subdir in NAMED_ENTRY_DIRS:
        target_dir = mkdirp(target / target_sub)
        payload_sub_dir = PAYLOAD / payload_sub
        names = sorted(p.name for p in payload_sub_dir.iterdir())
        mirror_dir = mkdirp(target / mirror_target_sub) if mirror_target_sub else None
        for name in names:
            remove_path(target_dir / name)
            copy_path(payload_sub_dir / name, target_dir / name)
            if payload_sub == "hooks":
                (target_dir / name).chmod(0o755)
            if chmod_subdir:
                sdir = target_dir / name / chmod_subdir
                if sdir.exists():
                    for s in sdir.iterdir():
                        s.chmod(0o755)
            if mirror_dir is not None:
                remove_path(mirror_dir / name)
                copy_path(target_dir / name, mirror_dir / name)

    manifest = {
        "name": NAME,
        "version": version,
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "paths": compute_managed_paths(),
        "shared_files": [dst for _src, dst, _sub in SHARED_FILES],
    }
    manifest_path(target).write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


# --- shared files: print-only, never written -------------------------------------------------

def print_shared_files_prompt(config: dict, *, removal: bool = False) -> None:
    mapping = resolve_placeholders(config)
    print()
    print("==> Shared files (never modified automatically) — apply by hand or hand this to your agent:")
    for src, dst, sub in SHARED_FILES:
        content = (PAYLOAD / src).read_text()
        if sub:
            content = substitute(content, mapping)
        print()
        print(f"--- {dst} " + "-" * max(1, 60 - len(dst)))
        if removal:
            print(f"Retire la config {NAME} de `{dst}` si tu l'y avais ajoutée. Texte de référence "
                  f"(tel qu'installé) :")
            print(content)
        else:
            print(
                f"Intègre la configuration {NAME} suivante dans `{dst}` : crée le fichier s'il "
                f"n'existe pas, sinon fusionne sans perturber le contenu existant.\n"
            )
            print(content)


# --- commands ---------------------------------------------------------------------------------

def run_install(argv: list[str]) -> None:
    target = Path(_target_arg(argv) or ".").resolve()
    target.mkdir(parents=True, exist_ok=True)
    config = resolve_config(argv, existing=None)
    version = resolve_version()

    print(f"==> Installing {NAME} into: {target}")
    print(f"    {config_summary(config)}")
    deploy(target, config, version=version)
    print("==> Done.")
    print_shared_files_prompt(config)


def run_update(argv: list[str]) -> None:
    target = Path(_target_arg(argv) or ".").resolve()
    old_manifest = read_manifest(target)
    if old_manifest is None:
        print(
            f"No {NAME} installation found in {target} ({DATA_DIR}/{MANIFEST_NAME} missing). "
            f"Run the installer first.",
            file=sys.stderr,
        )
        sys.exit(1)

    existing_config = read_config(target) or {}
    config = resolve_config(argv, existing=existing_config)
    version = resolve_version()

    print(f"==> Updating {NAME} in: {target}")
    print(f"    {config_summary(config)}")
    print(f"    {old_manifest.get('version')} -> {version}")

    new_manifest = deploy(target, config, version=version)

    kept = set(new_manifest["paths"])
    for p in old_manifest.get("paths", []):
        if p not in kept and (target / p).exists():
            remove_path(target / p)
            print(f"    removed stale: {p}")

    print("==> Update done.")
    print_shared_files_prompt(config)


def _container_dirs() -> list[Path]:
    dirs: set[Path] = set()
    for _payload_sub, target_sub, mirror_target_sub, _chmod_subdir in NAMED_ENTRY_DIRS:
        for sub in filter(None, [target_sub, mirror_target_sub]):
            p = Path(sub)
            dirs.add(p)
            dirs.add(p.parent)
    dirs.discard(Path("."))
    return sorted(dirs, key=lambda p: len(p.parts), reverse=True)


def _cleanup_empty_dirs(target: Path) -> None:
    for d in _container_dirs():
        p = target / d
        if p.is_dir() and not any(p.iterdir()):
            p.rmdir()


def run_uninstall(argv: list[str]) -> None:
    yes = "--yes" in argv or "-y" in argv
    target = Path(_target_arg(argv) or ".").resolve()

    manifest = read_manifest(target)
    paths = manifest["paths"] if manifest else compute_managed_paths()
    existing = [p for p in paths if (target / p).exists()]
    shared_dsts = manifest.get("shared_files", []) if manifest else [dst for _s, dst, _sub in SHARED_FILES]

    if not existing and manifest is None:
        print(f"Nothing to uninstall in {target}.")
        return
    if manifest is None:
        print("(No manifest found — using the current payload as a best-effort fallback.)")
    removal_config = read_config(target) or {}

    print(f"==> Will remove from {target}:")
    for p in existing:
        print(f"    - {p}")
    print(f"    - {DATA_DIR}/{MANIFEST_NAME}")
    preserved = ", ".join(f"{DATA_DIR}/{d}/" for d in PRESERVE_IN_DATA_DIR)
    print(f"==> Preserved (never touched): {preserved}")
    print(f"==> Never touched (shared, not owned): {', '.join(shared_dsts)}")

    if not yes:
        answer = input("Proceed? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("Aborted.")
            return

    for p in existing:
        remove_path(target / p)
    remove_path(manifest_path(target))
    _cleanup_empty_dirs(target)

    print(f"==> Uninstalled {NAME}.")
    print_shared_files_prompt(removal_config, removal=True)


def main() -> None:
    argv = sys.argv[1:]
    if not argv:
        run_install(argv)
        return
    cmd, rest = argv[0], argv[1:]
    if cmd == "update":
        run_update(rest)
    elif cmd in ("uninstall", "remove"):
        run_uninstall(rest)
    elif cmd == "install":
        run_install(rest)
    else:
        run_install(argv)


if __name__ == "__main__":
    main()

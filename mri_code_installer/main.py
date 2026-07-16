"""mri-code's CLI entry point — install (default) / update / uninstall.

Single self-contained module: no vendored engine, no TOML spec. Deployment is deterministic and
local — skills, hooks and `.mri_code/` data are copied straight from `payload/`. The 4 files a
project may already own are handled non-destructively so the module drops cleanly into an
existing repo: the markdown docs (AGENTS.md, CLAUDE.md) and `.claude/settings.json` are written
only when **absent** (an existing file is never touched), while `.mcp.json` is **deep-merged** —
our two servers are added only if missing, never overwriting one another module owns. The
manifest records exactly what we created so `uninstall` undoes only that (docs removed only if
still unchanged; only our MCP servers stripped).
"""
from __future__ import annotations

import hashlib
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
REFRESH_DIRS = ["templates", "stacks"]  # always removed + recopied

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


# --- shared-file application (write-if-absent for docs, deep-merge for .mcp.json) -----------

def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_if_absent(dst: Path, content: str) -> str | None:
    """Write content only when dst is absent (or already byte-identical to ours, so
    a re-install is a no-op). Returns the content hash when we own the file, else
    None — meaning the project already has its own version, left untouched."""
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(content)
        return _sha(content)
    if _sha(dst.read_text()) == _sha(content):
        return _sha(content)
    return None


def merge_mcp_servers(dst: Path, incoming: dict) -> tuple[list[str], list[str]]:
    """Deep-merge incoming `mcpServers` into dst without ever overwriting a server
    already present under the same name (another module may own it). Returns
    (owned, added): owned = names whose entry equals ours (removable on uninstall),
    added = names newly written this run. Idempotent: a re-run adds nothing."""
    existing: dict = {}
    if dst.exists():
        try:
            existing = json.loads(dst.read_text())
        except (json.JSONDecodeError, OSError):
            existing = {}
    servers = existing.setdefault("mcpServers", {})
    owned: list[str] = []
    added: list[str] = []
    for name, spec in incoming.get("mcpServers", {}).items():
        if name not in servers:
            servers[name] = spec
            owned.append(name)
            added.append(name)
        elif servers[name] == spec:
            owned.append(name)
    if added or not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(json.dumps(existing, indent=2) + "\n")
    return owned, added


def apply_shared_files(target: Path, config: dict) -> dict:
    """Install the shared files non-destructively: the markdown docs and settings.json
    are written only if absent (or already ours); `.mcp.json` is deep-merged. Prints a
    concise summary and returns ownership info recorded in the manifest for uninstall."""
    mapping = resolve_placeholders(config)
    created: dict[str, str] = {}
    mcp_owned: list[str] = []
    skipped: list[str] = []
    print()
    print("==> Shared files (non-destructive):")
    for src, dst, sub in SHARED_FILES:
        content = (PAYLOAD / src).read_text()
        if sub:
            content = substitute(content, mapping)
        dst_path = target / dst
        if dst == ".mcp.json":
            mcp_owned, added = merge_mcp_servers(dst_path, json.loads(content))
            if added:
                print(f"    {dst}: merged +{', '.join(added)}")
            else:
                print(f"    {dst}: our servers already present (no change)")
        else:
            digest = write_if_absent(dst_path, content)
            if digest is None:
                skipped.append(dst)
                print(f"    {dst}: exists (yours) — left untouched")
            else:
                created[dst] = digest
                print(f"    {dst}: written")
    if skipped:
        print(f"    -> to fold {NAME} into your existing {', '.join(skipped)}, merge by hand.")
    return {"created_shared_files": created, "mcp_servers_added": mcp_owned}


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

def deploy(target: Path, config: dict, *, version: str, shared: dict | None = None) -> dict:
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
        "created_shared_files": (shared or {}).get("created_shared_files", {}),
        "mcp_servers_added": (shared or {}).get("mcp_servers_added", []),
    }
    manifest_path(target).write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


# --- shared files: precise, non-destructive removal on uninstall ----------------------------

def remove_shared_files(target: Path, manifest: dict | None) -> None:
    """Undo exactly what apply_shared_files did: delete the shared docs we created
    (only if still unchanged since install), and strip from `.mcp.json` only the
    servers we added (leaving any owned by the user or another module)."""
    created = (manifest.get("created_shared_files") if manifest else {}) or {}
    mcp_added = (manifest.get("mcp_servers_added") if manifest else []) or []

    for dst, digest in created.items():
        p = target / dst
        if not p.exists():
            continue
        if _sha(p.read_text()) == digest:
            p.unlink()
            print(f"    removed {dst}")
        else:
            print(f"    kept {dst} (modified since install)")

    if mcp_added:
        p = target / ".mcp.json"
        if not p.exists():
            return
        try:
            data = json.loads(p.read_text())
        except (json.JSONDecodeError, OSError):
            return
        if not isinstance(data, dict):
            return
        servers = data.get("mcpServers", {})
        ours = json.loads((PAYLOAD / "mcp/servers.json").read_text()).get("mcpServers", {})
        removed = []
        for name in mcp_added:
            if name in servers and servers[name] == ours.get(name):
                del servers[name]
                removed.append(name)
        if removed:
            if not servers and set(data.keys()) == {"mcpServers"}:
                p.unlink()  # the file only ever held our servers
            else:
                p.write_text(json.dumps(data, indent=2) + "\n")
            print(f"    .mcp.json: removed {', '.join(removed)}")


# --- commands ---------------------------------------------------------------------------------

def run_install(argv: list[str]) -> None:
    target = Path(_target_arg(argv) or ".").resolve()
    target.mkdir(parents=True, exist_ok=True)
    config = resolve_config(argv, existing=None)
    version = resolve_version()

    print(f"==> Installing {NAME} into: {target}")
    print(f"    {config_summary(config)}")
    shared = apply_shared_files(target, config)
    deploy(target, config, version=version, shared=shared)
    print("==> Done.")


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

    shared = apply_shared_files(target, config)
    new_manifest = deploy(target, config, version=version, shared=shared)

    kept = set(new_manifest["paths"])
    for p in old_manifest.get("paths", []):
        if p not in kept and (target / p).exists():
            remove_path(target / p)
            print(f"    removed stale: {p}")

    print("==> Update done.")


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
    created_shared = list((manifest.get("created_shared_files") if manifest else {}) or {})
    mcp_added = (manifest.get("mcp_servers_added") if manifest else []) or []

    if not existing and manifest is None:
        print(f"Nothing to uninstall in {target}.")
        return
    if manifest is None:
        print("(No manifest found — using the current payload as a best-effort fallback.)")

    print(f"==> Will remove from {target}:")
    for p in existing:
        print(f"    - {p}")
    print(f"    - {DATA_DIR}/{MANIFEST_NAME}")
    preserved = ", ".join(f"{DATA_DIR}/{d}/" for d in PRESERVE_IN_DATA_DIR)
    print(f"==> Preserved (never touched): {preserved}")
    if created_shared:
        print(f"==> Shared files we created (removed only if unchanged): {', '.join(created_shared)}")
    if mcp_added:
        print(f"==> MCP servers we added (stripped from .mcp.json): {', '.join(mcp_added)}")

    if not yes:
        answer = input("Proceed? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("Aborted.")
            return

    for p in existing:
        remove_path(target / p)
    remove_shared_files(target, manifest)
    remove_path(manifest_path(target))
    _cleanup_empty_dirs(target)

    print(f"==> Uninstalled {NAME}.")


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

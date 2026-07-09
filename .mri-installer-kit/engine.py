"""Deploy/manifest engine shared by install, update and uninstall.

A module (mri-code, mri-slides, ...) describes what it deploys with a `Spec`. `deploy()` writes it
into a target project and returns a manifest recording exactly what it owns, so a later `update` or
`uninstall` can act with precision — including when several mri-* modules coexist in the same
target and share files (AGENTS.md, CLAUDE.md, .mcp.json, .claude/settings.json).
"""
from __future__ import annotations

import json
import re
import shutil
import tomllib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_NAME = ".manifest.json"
_ENVELOPE_START = "<!-- mri-modules:start -->"
_ENVELOPE_END = "<!-- mri-modules:end -->"


@dataclass
class NamedEntryDir:
    """skills/, hooks/... — the only mechanism for a directory a user might extend themselves.

    Every entry from `payload_dir/payload_sub/<name>` is deployed/removed individually by name;
    the parent directory (target_sub) is never wiped as a whole, so foreign entries survive.
    """

    payload_sub: str
    target_sub: str
    chmod_subdir: str | None = None
    chmod_self: bool = False
    mirror_target_sub: str | None = None


@dataclass
class WholeFile:
    """1:1 copy. Only for a file no other module will ever touch — no collision possible."""

    src: str
    dst: str
    substitute: bool = False


@dataclass
class MarkdownBlock:
    """A file (AGENTS.md, CLAUDE.md...) that may be shared by several modules."""

    src: str
    dst: str
    substitute: bool = False


@dataclass
class JsonMerge:
    """A JSON file (.mcp.json, settings.json...) that may be shared by several modules."""

    src: str
    dst: str


@dataclass
class ConfigField:
    key: str
    flag: str
    prompt: str
    # Plain string, rendered by render_template() — e.g. "English", "{other_field}",
    # "{other_field|fallback}". Never a callable: a declarative Spec must stay data, not code.
    default: str = ""


@dataclass
class Spec:
    name: str
    version: str
    payload_dir: Path
    data_dir_name: str
    preserve_in_data_dir: list[str] = field(default_factory=list)
    data_files: list[str] = field(default_factory=list)
    data_dirs: list[str] = field(default_factory=list)
    named_entry_dirs: list[NamedEntryDir] = field(default_factory=list)
    whole_files: list[WholeFile] = field(default_factory=list)
    markdown_blocks: list[MarkdownBlock] = field(default_factory=list)
    json_merges: list[JsonMerge] = field(default_factory=list)
    config_fields: list[ConfigField] = field(default_factory=list)
    # {{TOKEN}} -> template string, rendered by render_template() against the resolved config.
    placeholders: dict[str, str] = field(default_factory=dict)


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


def remove_managed_paths(target: Path, paths: list[str]) -> list[str]:
    existing = [p for p in paths if (target / p).exists()]
    for p in existing:
        remove_path(target / p)
    return existing


# --- manifest / config ---------------------------------------------------------------------

def manifest_path(target: Path, spec: Spec) -> Path:
    return target / spec.data_dir_name / MANIFEST_NAME


def read_manifest(target: Path, spec: Spec) -> dict | None:
    p = manifest_path(target, spec)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def read_config(target: Path, spec: Spec) -> dict | None:
    p = target / spec.data_dir_name / "config.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def compute_managed_paths(spec: Spec) -> list[str]:
    """Paths (relative to target) owned as whole files/dirs — everything except markdown_blocks
    and json_merges, which are shared and tracked separately in the manifest."""
    paths: list[str] = [wf.dst for wf in spec.whole_files]
    for nd in spec.named_entry_dirs:
        names = sorted(p.name for p in (spec.payload_dir / nd.payload_sub).iterdir())
        paths.extend(f"{nd.target_sub}/{n}" for n in names)
        if nd.mirror_target_sub:
            paths.extend(f"{nd.mirror_target_sub}/{n}" for n in names)
    paths.extend(f"{spec.data_dir_name}/{f}" for f in spec.data_files)
    paths.extend(f"{spec.data_dir_name}/{d}" for d in spec.data_dirs)
    if spec.config_fields:
        paths.append(f"{spec.data_dir_name}/config.json")
    return paths


# --- primitive 1: markdown_blocks -----------------------------------------------------------
# All modules' blocks live inside one shared <!-- mri-modules:start/end --> envelope so they stay
# contiguous regardless of install order or user edits, instead of scattering across the file.

def _block_markers(name: str) -> tuple[str, str]:
    return f"<!-- {name}:start -->", f"<!-- {name}:end -->"


def apply_markdown_block(target_file: Path, name: str, content: str) -> None:
    start, end = _block_markers(name)
    block = f"{start}\n{content.rstrip()}\n{end}"
    text = target_file.read_text() if target_file.exists() else ""

    env_re = re.compile(re.escape(_ENVELOPE_START) + r"(.*?)" + re.escape(_ENVELOPE_END), re.DOTALL)
    env_match = env_re.search(text)
    if env_match is None:
        envelope = f"{_ENVELOPE_START}\n{block}\n{_ENVELOPE_END}\n"
        sep = "" if text == "" else ("\n" if text.endswith("\n") else "\n\n")
        target_file.write_text(text + sep + envelope)
        return

    inner = env_match.group(1)
    block_re = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if block_re.search(inner):
        new_inner = block_re.sub(block, inner)
    else:
        new_inner = inner.rstrip("\n") + f"\n{block}\n"
    text = text[: env_match.start()] + _ENVELOPE_START + new_inner + _ENVELOPE_END + text[env_match.end() :]
    target_file.write_text(text)


def strip_markdown_block(target_file: Path, name: str) -> None:
    if not target_file.exists():
        return
    text = target_file.read_text()
    start, end = _block_markers(name)

    env_re = re.compile(re.escape(_ENVELOPE_START) + r"(.*?)" + re.escape(_ENVELOPE_END), re.DOTALL)
    env_match = env_re.search(text)
    if env_match is None:
        return

    inner = env_match.group(1)
    block_re = re.compile(r"\n?" + re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    new_inner = block_re.sub("", inner)

    if new_inner.strip() == "":
        text = text[: env_match.start()] + text[env_match.end() :]
    else:
        text = text[: env_match.start()] + _ENVELOPE_START + new_inner + _ENVELOPE_END + text[env_match.end() :]

    if text.strip() == "":
        target_file.unlink(missing_ok=True)
    else:
        target_file.write_text(text)


def strip_markdown_blocks(target: Path, spec: Spec, dsts: list[str]) -> None:
    for dst in dsts:
        strip_markdown_block(target / dst, spec.name)


# --- primitive 2: json_merges ----------------------------------------------------------------
# One recursive algorithm handles both dict-merge-by-key (e.g. mcpServers.<name>) and array-union
# (e.g. permissions.allow, hooks.*): objects recurse, lists are unioned with per-module ownership
# tracked verbatim (duplicates across modules are tolerated — removal only ever drops one
# occurrence of a value this module itself contributed, never another module's).

def _merge_into(target_obj: dict, fragment: dict, old_owned: dict, new_owned: dict, path: list[str]) -> None:
    for key, value in fragment.items():
        pkey = ".".join(path + [key])
        if isinstance(value, dict):
            target_obj.setdefault(key, {})
            _merge_into(target_obj[key], value, old_owned, new_owned, path + [key])
        elif isinstance(value, list):
            arr = target_obj.setdefault(key, [])
            for old_item in old_owned.get(pkey, []):
                _remove_one(arr, old_item)
            arr.extend(value)
            new_owned[pkey] = value
        else:
            target_obj[key] = value
            new_owned[pkey] = value


def _remove_one(arr: list, item) -> None:
    for i, v in enumerate(arr):
        if v == item:
            del arr[i]
            return


def _prune_empty(obj) -> bool:
    if isinstance(obj, dict):
        for k in list(obj.keys()):
            if _prune_empty(obj[k]):
                del obj[k]
        return obj == {}
    if isinstance(obj, list):
        return obj == []
    return False


def _walk_to_parent(data: dict, pkey: str) -> tuple[dict | None, str | None]:
    parts = pkey.split(".")
    obj = data
    for part in parts[:-1]:
        if not isinstance(obj, dict) or part not in obj:
            return None, None
        obj = obj[part]
    return obj, parts[-1]


def merge_json_fragment(target_file: Path, fragment: dict, old_owned: dict) -> dict:
    data = json.loads(target_file.read_text()) if target_file.exists() else {}
    new_owned: dict = {}
    _merge_into(data, fragment, old_owned, new_owned, [])
    target_file.write_text(json.dumps(data, indent=2) + "\n")
    return new_owned


def strip_json_ownership(target_file: Path, owned: dict) -> None:
    if not target_file.exists() or not owned:
        return
    data = json.loads(target_file.read_text())
    for pkey, value in owned.items():
        parent, leaf = _walk_to_parent(data, pkey)
        if parent is None or leaf not in parent:
            continue
        if isinstance(value, list):
            arr = parent.get(leaf, [])
            for item in value:
                _remove_one(arr, item)
        else:
            del parent[leaf]
    _prune_empty(data)
    # Never delete the file itself: other modules may still rely on it existing.
    target_file.write_text(json.dumps(data, indent=2) + "\n")


def strip_json_ownerships(target: Path, ownership: dict[str, dict]) -> None:
    for dst, owned in ownership.items():
        strip_json_ownership(target / dst, owned)


# --- declarative template mini-language ------------------------------------------------------
# Used for ConfigField.default and Spec.placeholders values so a Spec can stay pure TOML data
# instead of hand-written Python callables. Deliberately not a general templating language — two
# composable forms only:
#   - "{field}" / "...{field|inline fallback}..." — per-token substitution, embeddable anywhere.
#   - "primary|whole fallback" (a "|" outside any {...}) — whole fallback used when every {field}
#     referenced in `primary` is empty; needed when the surrounding text itself must change, not
#     just a value within it (e.g. "as {user_name}|directly (no preferred name set)").

_TOKEN_RE = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)(?:\|([^{}]*))?\}")


def _split_top_level_pipe(value: str) -> tuple[str, str | None]:
    depth = 0
    for i, ch in enumerate(value):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth = max(0, depth - 1)
        elif ch == "|" and depth == 0:
            return value[:i], value[i + 1 :]
    return value, None


def _render_tokens(text: str, config: dict) -> str:
    def _sub(m: re.Match) -> str:
        value = config.get(m.group(1))
        return str(value) if value else (m.group(2) if m.group(2) is not None else "")

    return _TOKEN_RE.sub(_sub, text)


def render_template(value: str, config: dict) -> str:
    primary, whole_fallback = _split_top_level_pipe(value)
    if whole_fallback is not None:
        fields = _TOKEN_RE.findall(primary)
        if fields and all(not config.get(f) for f, _ in fields):
            return _render_tokens(whole_fallback, config)
    return _render_tokens(primary, config)


def resolve_placeholders(spec: Spec, config: dict) -> dict[str, str]:
    return {token: render_template(template, config) for token, template in spec.placeholders.items()}


# --- declarative spec loading -----------------------------------------------------------------

def resolve_version(repo_root: Path) -> str:
    version_file = repo_root / "VERSION"
    if version_file.exists():
        return version_file.read_text().strip()
    pyproject = repo_root / "pyproject.toml"
    if pyproject.exists():
        return tomllib.loads(pyproject.read_text())["project"]["version"]
    raise FileNotFoundError(f"no VERSION file or pyproject.toml with a version under {repo_root}")


def load_spec(toml_path: Path, *, version: str) -> Spec:
    data = tomllib.loads(toml_path.read_text())
    repo_root = toml_path.parent
    return Spec(
        name=data["name"],
        version=version,
        payload_dir=repo_root / data.get("payload_dir", "."),
        data_dir_name=data["data_dir_name"],
        preserve_in_data_dir=data.get("preserve_in_data_dir", []),
        data_files=data.get("data_files", []),
        data_dirs=data.get("data_dirs", []),
        named_entry_dirs=[NamedEntryDir(**d) for d in data.get("named_entry_dirs", [])],
        whole_files=[WholeFile(**d) for d in data.get("whole_files", [])],
        markdown_blocks=[MarkdownBlock(**d) for d in data.get("markdown_blocks", [])],
        json_merges=[JsonMerge(**d) for d in data.get("json_merges", [])],
        config_fields=[ConfigField(**d) for d in data.get("config_fields", [])],
        placeholders=data.get("placeholders", {}),
    )


# --- substitution ----------------------------------------------------------------------------

def _substitute_text(text: str, mapping: dict[str, str]) -> str:
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text


def _substitute_file(path: Path, mapping: dict[str, str]) -> None:
    if path.exists():
        path.write_text(_substitute_text(path.read_text(), mapping))


# --- deploy ------------------------------------------------------------------------------------

def deploy(target: Path, config: dict, spec: Spec) -> dict:
    if not spec.payload_dir.exists():
        raise FileNotFoundError(f"payload directory not found: {spec.payload_dir}")

    data_dir = mkdirp(target / spec.data_dir_name)
    for sub in spec.preserve_in_data_dir:
        mkdirp(data_dir / sub)

    for f in spec.data_files:
        copy_path(spec.payload_dir / f, data_dir / f)
    for d in spec.data_dirs:
        remove_path(data_dir / d)
        copy_path(spec.payload_dir / d, data_dir / d)

    if spec.config_fields:
        cfg_obj = {f.key: config[f.key] for f in spec.config_fields}
        (data_dir / "config.json").write_text(json.dumps(cfg_obj, indent=2) + "\n")

    for nd in spec.named_entry_dirs:
        target_dir = mkdirp(target / nd.target_sub)
        payload_sub_dir = spec.payload_dir / nd.payload_sub
        names = sorted(p.name for p in payload_sub_dir.iterdir())
        mirror_dir = mkdirp(target / nd.mirror_target_sub) if nd.mirror_target_sub else None
        for name in names:
            remove_path(target_dir / name)
            copy_path(payload_sub_dir / name, target_dir / name)
            if nd.chmod_self:
                (target_dir / name).chmod(0o755)
            if nd.chmod_subdir:
                sdir = target_dir / name / nd.chmod_subdir
                if sdir.exists():
                    for s in sdir.iterdir():
                        s.chmod(0o755)
            if mirror_dir is not None:
                remove_path(mirror_dir / name)
                copy_path(target_dir / name, mirror_dir / name)

    resolved_placeholders = resolve_placeholders(spec, config)

    for wf in spec.whole_files:
        copy_path(spec.payload_dir / wf.src, target / wf.dst)
        if wf.substitute:
            _substitute_file(target / wf.dst, resolved_placeholders)

    old_manifest = read_manifest(target, spec) or {}

    old_md_dsts = set(old_manifest.get("markdown_blocks", []))
    new_md_dsts: list[str] = []
    for mb in spec.markdown_blocks:
        content = (spec.payload_dir / mb.src).read_text()
        if mb.substitute:
            content = _substitute_text(content, resolved_placeholders)
        apply_markdown_block(target / mb.dst, spec.name, content)
        new_md_dsts.append(mb.dst)
    for stale_dst in old_md_dsts - set(new_md_dsts):
        strip_markdown_block(target / stale_dst, spec.name)

    old_json_ownership: dict[str, dict] = old_manifest.get("json_ownership", {})
    new_json_ownership: dict[str, dict] = {}
    new_json_dsts = {jm.dst for jm in spec.json_merges}
    for jm in spec.json_merges:
        fragment = json.loads((spec.payload_dir / jm.src).read_text())
        new_json_ownership[jm.dst] = merge_json_fragment(
            target / jm.dst, fragment, old_json_ownership.get(jm.dst, {})
        )
    for stale_dst in set(old_json_ownership) - new_json_dsts:
        strip_json_ownership(target / stale_dst, old_json_ownership[stale_dst])

    manifest = {
        "name": spec.name,
        "version": spec.version,
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "paths": compute_managed_paths(spec),
        "markdown_blocks": new_md_dsts,
        "json_ownership": new_json_ownership,
    }
    manifest_path(target, spec).write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest

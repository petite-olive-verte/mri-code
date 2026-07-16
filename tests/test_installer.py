"""Tests for the non-destructive shared-file handling of the installer.

Covers the two behaviours that make mri-code drop cleanly into an existing repo:
markdown/settings written only when absent, and `.mcp.json` deep-merged (never
overwriting a server another module owns), plus a precise, reversible uninstall.
"""
import json

from mri_code_installer import main


# --- write_if_absent -------------------------------------------------------------------------

def test_write_if_absent_writes_when_missing(tmp_path):
    p = tmp_path / "AGENTS.md"
    digest = main.write_if_absent(p, "hello")
    assert p.read_text() == "hello"
    assert digest == main._sha("hello")


def test_write_if_absent_owns_identical(tmp_path):
    p = tmp_path / "doc.md"
    p.write_text("same")
    assert main.write_if_absent(p, "same") == main._sha("same")


def test_write_if_absent_leaves_foreign_untouched(tmp_path):
    p = tmp_path / "doc.md"
    p.write_text("mine")
    assert main.write_if_absent(p, "theirs") is None
    assert p.read_text() == "mine"  # never clobbered


# --- merge_mcp_servers -----------------------------------------------------------------------

def test_merge_mcp_into_absent_file(tmp_path):
    p = tmp_path / ".mcp.json"
    owned, added = main.merge_mcp_servers(p, {"mcpServers": {"a": {"command": "x"}}})
    assert added == ["a"] and owned == ["a"]
    assert json.loads(p.read_text())["mcpServers"]["a"] == {"command": "x"}


def test_merge_mcp_preserves_foreign_and_is_idempotent(tmp_path):
    p = tmp_path / ".mcp.json"
    p.write_text(json.dumps({"mcpServers": {"foo": {"command": "f"}}}))
    incoming = {"mcpServers": {"pw": {"command": "p"}}}

    owned, added = main.merge_mcp_servers(p, incoming)
    assert added == ["pw"] and owned == ["pw"]
    assert set(json.loads(p.read_text())["mcpServers"]) == {"foo", "pw"}

    before = p.read_text()
    owned2, added2 = main.merge_mcp_servers(p, incoming)
    assert added2 == [] and owned2 == ["pw"]
    assert p.read_text() == before  # re-run is a no-op


def test_merge_mcp_never_overwrites_a_same_named_server(tmp_path):
    p = tmp_path / ".mcp.json"
    p.write_text(json.dumps({"mcpServers": {"pw": {"command": "USER"}}}))
    owned, added = main.merge_mcp_servers(p, {"mcpServers": {"pw": {"command": "OURS"}}})
    assert added == [] and owned == []  # differing spec => not ours, untouched
    assert json.loads(p.read_text())["mcpServers"]["pw"] == {"command": "USER"}


# --- full install/uninstall round-trip -------------------------------------------------------

def test_install_is_nondestructive_then_uninstall_is_precise(tmp_path):
    (tmp_path / "AGENTS.md").write_text("USER OWNED AGENTS")
    (tmp_path / ".mcp.json").write_text(json.dumps({"mcpServers": {"foo": {"command": "f"}}}))

    main.run_install([str(tmp_path), "--lang", "English", "--user", "T"])

    # existing doc untouched; absent docs created; mcp merged, foreign server kept
    assert (tmp_path / "AGENTS.md").read_text() == "USER OWNED AGENTS"
    assert (tmp_path / "CLAUDE.md").exists()
    assert (tmp_path / ".claude/settings.json").exists()
    servers = json.loads((tmp_path / ".mcp.json").read_text())["mcpServers"]
    assert {"foo", "playwright", "chrome-devtools"} <= set(servers)

    manifest = json.loads((tmp_path / ".mri_code/.manifest.json").read_text())
    assert set(manifest["created_shared_files"]) == {"CLAUDE.md", ".claude/settings.json"}
    assert set(manifest["mcp_servers_added"]) == {"playwright", "chrome-devtools"}

    main.run_uninstall([str(tmp_path), "--yes"])

    assert (tmp_path / "AGENTS.md").exists()          # never ours
    assert not (tmp_path / "CLAUDE.md").exists()      # ours + unchanged => removed
    servers = json.loads((tmp_path / ".mcp.json").read_text())["mcpServers"]
    assert "foo" in servers and "playwright" not in servers


def test_uninstall_keeps_a_shared_doc_modified_after_install(tmp_path):
    main.run_install([str(tmp_path), "--lang", "English", "--user", "T"])
    (tmp_path / "CLAUDE.md").write_text("user edited this after install")
    main.run_uninstall([str(tmp_path), "--yes"])
    assert (tmp_path / "CLAUDE.md").read_text() == "user edited this after install"


# --- Symfony support is deployed -------------------------------------------------------------

def test_install_deploys_symfony_skills_and_templates(tmp_path):
    main.run_install([str(tmp_path), "--lang", "English", "--user", "T"])

    for skill in ("mri-code-scaffold-symfony", "mri-code-scaffold-symfony-hexagonal"):
        assert (tmp_path / ".claude/skills" / skill / "SKILL.md").exists()
        assert (tmp_path / ".agents/skills" / skill / "SKILL.md").exists()

    # Both project templates land under the data dir, ready for the scaffold skills.
    assert (tmp_path / ".mri_code/templates/symfony/composer.json").exists()
    assert (tmp_path / ".mri_code/templates/symfony/.env").exists()
    assert (
        tmp_path / ".mri_code/templates/symfony-hexagonal/src/Domain/Model/Task.php"
    ).exists()


# --- React support is deployed ----------------------------------------------------------------

def test_install_deploys_react_skill_and_template(tmp_path):
    main.run_install([str(tmp_path), "--lang", "English", "--user", "T"])

    assert (tmp_path / ".claude/skills/mri-code-scaffold-react/SKILL.md").exists()
    assert (tmp_path / ".agents/skills/mri-code-scaffold-react/SKILL.md").exists()

    # The template lands under the data dir, ready for the scaffold skill. Hidden files
    # (.gitignore, .env.example) must come across too — the skill copies with `cp -r`.
    template = tmp_path / ".mri_code/templates/react"
    assert (template / "package.json").exists()
    # `.jsonc`, not `.json`: Biome silently ignores a `biome.json` that contains
    # comments — the whole config would be dead with no diagnostic.
    assert (template / "biome.jsonc").exists()
    assert (template / ".gitignore").exists()
    assert (template / "src/features/health/model/health-status.ts").exists()


# --- the constitution is stack-agnostic -------------------------------------------------------

def test_constitution_ships_agnostic_with_a_stack_placeholder(tmp_path):
    """The core constitution must name no tool: the stack is a devplan conclusion, sealed in
    later by a scaffold skill. A tool name leaking here would re-impose a default stack."""
    main.run_install([str(tmp_path), "--lang", "English", "--user", "T"])

    constitution = (tmp_path / ".mri_code/constitution.md").read_text()
    assert "<!-- mri-code:stack:start -->" in constitution
    assert "<!-- mri-code:stack:end -->" in constitution

    start = constitution.index("<!-- mri-code:stack:start -->")
    end = constitution.index("<!-- mri-code:stack:end -->")
    outside = constitution[:start] + constitution[end:]
    for tool in ("uv ", "ruff", "pytest", "mypy", "pyproject.toml", "snake_case", "composer", "pnpm"):
        assert tool not in outside, f"{tool!r} leaks into the stack-agnostic core"


def test_every_template_has_a_matching_stack_fragment(tmp_path):
    """One fragment per template: a scaffold skill with no fragment to seal would leave the
    constitution's Stack section empty."""
    main.run_install([str(tmp_path), "--lang", "English", "--user", "T"])

    templates = {p.name for p in (tmp_path / ".mri_code/templates").iterdir() if p.is_dir()}
    fragments = {p.stem for p in (tmp_path / ".mri_code/stacks").glob("*.md")}
    assert templates == fragments


def test_react_template_keeps_its_placeholders_unrendered(tmp_path):
    """The installed template is a source: tokens must survive install untouched,
    otherwise every scaffold rendered from it would be poisoned."""
    main.run_install([str(tmp_path), "--lang", "English", "--user", "T"])

    package_json = (tmp_path / ".mri_code/templates/react/package.json").read_text()
    assert "__PROJECT_NAME__" in package_json

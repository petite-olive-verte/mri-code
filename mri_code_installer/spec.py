"""mri-code's Spec instance — see mri-installer-kit's README for the contract this follows."""
# ruff: noqa: I001 — order is load-bearing: importing mri_code_installer first puts the
# vendored engine on sys.path, which `engine` (bare, no parent package) then resolves against.
from mri_code_installer import PAYLOAD_DIR, VERSION
from engine import ConfigField, JsonMerge, MarkdownBlock, NamedEntryDir, Spec  # vendored

SPEC = Spec(
    name="mri-code",
    version=VERSION,
    payload_dir=PAYLOAD_DIR,
    data_dir_name=".mri_code",
    preserve_in_data_dir=["docs"],
    data_files=["constitution.md", "models.md"],
    data_dirs=["templates"],
    named_entry_dirs=[
        NamedEntryDir(
            payload_sub="skills",
            target_sub=".claude/skills",
            chmod_subdir="scripts",
            mirror_target_sub=".agents/skills",
        ),
        NamedEntryDir(payload_sub="hooks", target_sub=".claude/hooks", chmod_self=True),
    ],
    markdown_blocks=[
        MarkdownBlock(src="AGENTS.md", dst="AGENTS.md", substitute=True),
        MarkdownBlock(src="CLAUDE.md", dst="CLAUDE.md", substitute=True),
    ],
    json_merges=[
        JsonMerge(src="mcp/servers.json", dst=".mcp.json"),
        JsonMerge(src="settings.json", dst=".claude/settings.json"),
    ],
    config_fields=[
        ConfigField(key="communication_language", flag="--lang", prompt="Communication language", default="English"),
        ConfigField(
            key="document_language",
            flag="--doc-lang",
            prompt="Document language",
            default=lambda cfg: cfg["communication_language"],
        ),
        ConfigField(key="user_name", flag="--user", prompt="How should the agent address you?", default=""),
    ],
    placeholders=lambda cfg: {
        "{{COMMUNICATION_LANGUAGE}}": cfg["communication_language"],
        "{{DOCUMENT_LANGUAGE}}": cfg["document_language"],
        "{{USER_ADDRESS}}": f"as {cfg['user_name']}" if cfg["user_name"] else "directly (no preferred name set)",
        "{{USER_NAME}}": cfg["user_name"] or "the user",
    },
)

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_skills.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_skill_repository_validation_passes():
    validator = load_module("validate_skills", VALIDATOR_PATH)
    assert validator.validate_repository() == []


def test_eval_skill_names_resolve_to_canonical_skills():
    skill_names = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
    for eval_path in (ROOT / "evals").glob("*.json"):
        data = json.loads(eval_path.read_text(encoding="utf-8"))
        assert data["skill_name"] in skill_names


def test_maahub_adapter_paths_exist():
    for metadata_path in (ROOT / "adapters" / "maahub" / "skills").glob("*.json"):
        data = json.loads(metadata_path.read_text(encoding="utf-8"))
        for field in ("entry", "readme"):
            target = (metadata_path.parent / data[field]).resolve()
            assert target.is_file(), f"{metadata_path.name}: missing {field} target {target}"


def test_relative_markdown_links_inside_skills_exist():
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for markdown_path in (ROOT / "skills").rglob("*.md"):
        text = markdown_path.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or "://" in target or target.startswith("<"):
                continue
            if not target.startswith(("../maa-", "../../maa-", "references/", "scripts/", "assets/")):
                continue
            resolved = (markdown_path.parent / target).resolve()
            assert resolved.exists(), f"{markdown_path.relative_to(ROOT)} -> {raw_target}"


def test_plugin_versions_and_mcp_presets_stay_in_sync():
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    claude = json.loads(
        (ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    codex = json.loads(
        (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    catalog = json.loads((ROOT / "mcp" / "catalog.json").read_text(encoding="utf-8"))
    native_mcp = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))

    assert package["version"] == claude["version"] == codex["version"]
    expected_servers = {
        name: {
            "command": catalog["servers"][name]["command"],
            "args": catalog["servers"][name]["args"],
        }
        for name in catalog["profiles"]["full"]
    }
    assert native_mcp["mcpServers"] == expected_servers

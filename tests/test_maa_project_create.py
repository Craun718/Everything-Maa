from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "maa-project-create"


def test_project_create_skill_routes_to_external_lifecycle_engine():
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

    assert "`create_project`" in text
    assert "`doctor`" in text
    assert "`diff`" in text
    assert "$maa-project-init" in text
    assert "Do not reproduce its templates" in text
    assert "resourcePackSlug" in text


def test_project_create_cli_reference_matches_catalog_pin():
    reference = (SKILL_DIR / "references" / "cli-and-reports.md").read_text(
        encoding="utf-8"
    )
    mcp_catalog = json.loads((ROOT / "mcp" / "catalog.json").read_text(encoding="utf-8"))
    integration_catalog = json.loads(
        (ROOT / "integrations" / "catalog.json").read_text(encoding="utf-8")
    )
    server = mcp_catalog["servers"]["create-maa-project"]

    assert server["version"] == "2.0.0"
    assert "create-maa-project==2.0.0" in reference
    assert "@latest" not in reference
    assert integration_catalog["tools"]["create-maa-project"]["mcpServer"] == (
        "create-maa-project"
    )


def test_project_create_openai_metadata_and_evals_are_discoverable():
    metadata = yaml.safe_load(
        (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    )
    evals = json.loads(
        (ROOT / "evals" / "maa-project-create.json").read_text(encoding="utf-8")
    )

    assert "$maa-project-create" in metadata["interface"]["default_prompt"]
    assert evals["skill_name"] == "maa-project-create"
    assert len(evals["evals"]) >= 4

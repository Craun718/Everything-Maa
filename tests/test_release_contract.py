from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_release_metadata_and_packaged_validator_are_present():
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    codex = json.loads(
        (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    claude = json.loads(
        (ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    )

    assert package["version"] == codex["version"] == claude["version"]
    assert package["publishConfig"]["access"] == "public"
    assert "scripts/check-release.mjs" in package["files"]
    assert "CHANGELOG.md" in package["files"]
    assert "release:check" in package["scripts"]


def test_release_workflow_publishes_only_for_tags_with_oidc():
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(
        encoding="utf-8"
    )

    assert 'tags:\n      - "v*"' in workflow
    assert "id-token: write" in workflow
    assert "npm publish" in workflow
    assert workflow.count("if: github.ref_type == 'tag'") >= 3
    assert "NPM_TOKEN" not in workflow

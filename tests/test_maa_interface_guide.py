from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "maa-interface-guide"


def test_interface_guide_enforces_scope_and_handoffs():
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

    assert "只接受 V2" in text
    assert "不得生成孤立的 Interface" in text
    assert "$maa-project-create" in text
    assert "$maa-pipeline-option" in text
    assert "Pipeline、Python Agent、图片和构建配置只读" in text


def test_interface_guide_prioritizes_project_evidence_and_uses_project_tooling():
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    validation = (SKILL_DIR / "references" / "validation.md").read_text(
        encoding="utf-8"
    )

    assert "项目内证据优先" in text
    assert "https://github.com/MaaXYZ/MaaFramework" in text
    assert "必须先询问用户" in text
    assert "`package.json`" in text
    assert "禁止直接执行 `node_modules`" in text
    assert "会写日志、缓存或其他文件" in text
    assert "packageManager" in validation
    assert "lockfile 一致的包管理器" in validation
    assert "node_modules/.bin" in validation
    assert "npx --no-install @nekosu/maa-tools check" in validation
    assert "只读审查不授权这些写入" in validation
    assert "不以 `npx ... init` 创建配置" in validation


def test_interface_guide_metadata_adapter_and_evals_are_discoverable():
    metadata = yaml.safe_load(
        (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    )
    adapter = json.loads(
        (ROOT / "adapters" / "maahub" / "skills" / "maa-interface-guide.json").read_text(
            encoding="utf-8"
        )
    )
    evals = json.loads(
        (ROOT / "evals" / "maa-interface-guide.json").read_text(encoding="utf-8")
    )

    assert "$maa-interface-guide" in metadata["interface"]["default_prompt"]
    assert adapter["entry"] == "../../../skills/maa-interface-guide/SKILL.md"
    assert evals["skill_name"] == "maa-interface-guide"
    assert len(evals["evals"]) >= 4


def test_interface_guide_documents_maa_tools_in_readmes():
    english = (ROOT / "README.md").read_text(encoding="utf-8")
    chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")

    assert "@nekosu/maa-tools" in english
    assert "@nekosu/maa-tools" in chinese

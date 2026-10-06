from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "maa-wiki"


def test_wiki_routes_to_authoritative_upstream_skill():
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    docs = (ROOT / "docs" / "skills" / "maa-wiki.md").read_text(encoding="utf-8")

    assert "## 加载上游 skill" in skill
    assert (
        "https://raw.githubusercontent.com/Windsland52/MaaLLMWiki/main/"
        "skills/maallmwiki/SKILL.md"
    ) in skill
    assert "路由权威" in skill
    assert "pinned commit" in skill
    assert "不要用本节替代上游 skill 的完整规则" in skill

    assert "上游 skill：" in docs
    assert "skills/maallmwiki/SKILL.md" in docs
    assert "`maallmwiki` skill" in docs


def test_wiki_has_disclosed_fallbacks_and_no_vendoring():
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    notices = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")

    assert "https://cdn.jsdelivr.net/gh/Windsland52/MaaLLMWiki@main/" in skill
    assert "https://raw.githubusercontent.com/Windsland52/MaaLLMWiki/main/README.md" in skill
    assert "回退时说明实际使用的入口" in skill
    assert "不要把 catalog 内容或上游 skill 写进用户项目" in skill
    assert "maallmwiki` Skill and catalog through raw GitHub URLs" in notices
    assert "neither is vendored" in notices


def test_wiki_evals_use_project_version_before_latest():
    data = json.loads((ROOT / "evals" / "maa-wiki.json").read_text(encoding="utf-8"))
    cases = {case["eval_name"]: case for case in data["evals"]}

    pinned = cases["route-project-pinned-pipeline-schema-fact"]
    assert "版本锁是 5.12.2" in pinned["prompt"]
    assert "目标项目锁定的 5.12.2" in pinned["expected_output"]

    verify = cases["verify-official-fact-for-other-skill"]
    assert "实际锁定或运行时" in verify["expected_output"]
    assert "版本未知时" in verify["expected_output"]

    prefer_project = cases["prefer-project-version-over-latest"]
    assert "运行时是 MaaFramework 5.11.1" in prefer_project["prompt"]
    assert (
        "不因为 MaaLLMWiki 有更新版本就改查 latest"
        in prefer_project["expected_output"]
    )

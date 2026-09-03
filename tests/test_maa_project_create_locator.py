from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "maa-project-create"
LOCATOR = SKILL_DIR / "scripts" / "find-create-maa-project-skill.mjs"


def run_locator(*args: Path | str, ambient: bool = False) -> dict[str, object]:
    result = subprocess.run(
        [
            "node",
            str(LOCATOR),
            *(("--no-ambient",) if not ambient else ()),
            *map(str, args),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    result.check_returncode()
    return json.loads(result.stdout)


def write_upstream_skill(root: Path, *, bundled: bool) -> Path:
    if not bundled:
        root.mkdir(parents=True)
        skill = root / "SKILL.md"
        skill.write_text(
            "---\nname: create-maa-project\ndescription: Test upstream Skill.\n---\n\n"
            "# Create Maa Project\n",
            encoding="utf-8",
        )
        return skill

    skill = root / "skills" / "create-maa-project" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(
        "---\nname: create-maa-project\ndescription: Test upstream Skill.\n---\n\n"
        "# Create Maa Project\n",
        encoding="utf-8",
    )
    return skill


def test_locator_prefers_an_explicit_upstream_skill(tmp_path: Path):
    expected = write_upstream_skill(tmp_path, bundled=True)

    result = run_locator("--root", tmp_path)

    assert result["status"] == "found"
    assert result["source"] == "explicit"
    assert Path(str(result["skillPath"])).resolve() == expected.resolve()
    assert result["pinnedVersion"] == "3.2.0"
    assert str(result["pinnedSkillUrl"]).endswith(
        "/create-maa-project/v3.2.0/skills/create-maa-project/SKILL.md"
    )


def test_locator_reads_an_npm_package_skill(tmp_path: Path):
    package = tmp_path / "create-maa-project"
    package.mkdir()
    (package / "package.json").write_text(
        json.dumps({"name": "create-maa-project", "version": "3.2.0"}),
        encoding="utf-8",
    )
    expected = write_upstream_skill(package, bundled=True)

    result = run_locator("--root", package)

    assert result["status"] == "found"
    assert result["source"] == "explicit-package"
    assert result["packageVersion"] == "3.2.0"
    assert Path(str(result["skillPath"])).resolve() == expected.resolve()


def test_locator_reports_a_package_without_a_skill(tmp_path: Path):
    package = tmp_path / "create-maa-project"
    package.mkdir()
    (package / "package.json").write_text(
        json.dumps({"name": "create-maa-project", "version": "2.0.0"}),
        encoding="utf-8",
    )

    result = run_locator("--root", package)

    assert result["status"] == "package-without-skill"
    assert result["skillPath"] is None
    assert result["packageVersion"] == "2.0.0"
    assert result["pinnedVersion"] == "3.2.0"


def test_locator_rejects_the_wrapper_skill_and_reports_the_fixed_fallback():
    result = run_locator("--root", SKILL_DIR)

    assert result["status"] == "not-found"
    assert result["skillPath"] is None
    assert result["pinnedVersion"] == "3.2.0"
    assert result["pinnedSkillUrl"] == (
        "https://raw.githubusercontent.com/Windsland52/create-maa-project/"
        "v3.2.0/skills/create-maa-project/SKILL.md"
    )


def test_locator_finds_an_installed_user_skill(tmp_path: Path):
    home = tmp_path / "home"
    expected = write_upstream_skill(
        home / ".codex" / "skills" / "create-maa-project",
        bundled=False,
    )
    environment = os.environ.copy()
    environment.update(
        {
            "HOME": str(home),
            "USERPROFILE": str(home),
            "CODEX_HOME": str(tmp_path / "codex-home"),
        }
    )

    result = subprocess.run(
        ["node", str(LOCATOR)],
        check=False,
        capture_output=True,
        text=True,
        cwd=tmp_path,
        env=environment,
    )

    result.check_returncode()
    payload = json.loads(result.stdout)
    assert payload["status"] == "found"
    assert payload["source"] == "installed-skill"
    assert Path(str(payload["skillPath"])).resolve() == expected.resolve()

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "maa-project-create"
LOCATOR = SKILL_DIR / "scripts" / "find-create-maa-project-skill.mjs"
PINNED_SKILL_SHA256 = (
    "4c0335f8483306a2fac56f68cc21a84a47fe49d928ae1e62e2ef3f1beb08f7a9"
)
TEST_SKILL = (
    "---\nname: create-maa-project\ndescription: Test upstream Skill.\n---\n\n"
    "# Create Maa Project\n"
)


def run_locator(
    *args: Path | str,
    ambient: bool = False,
    environment: dict[str, str] | None = None,
    cwd: Path | None = None,
) -> dict[str, object]:
    test_digest = hashlib.sha256(TEST_SKILL.encode("utf-8")).hexdigest()
    source = LOCATOR.read_text(encoding="utf-8")
    patched = re.sub(
        r'const PINNED_SKILL_SHA256 =\s*\n  "[0-9a-f]{64}"',
        f'const PINNED_SKILL_SHA256 = "{test_digest}"',
        source,
        count=1,
    )
    if patched == source:
        raise AssertionError("Could not patch the pinned Skill digest for the test")

    with tempfile.TemporaryDirectory() as temporary:
        test_locator = Path(temporary) / "find-create-maa-project-skill.mjs"
        test_locator.write_text(patched, encoding="utf-8")
        locator_environment = {
            **(environment or os.environ),
            "MAA_PROJECT_CREATE_ROOT": str(SKILL_DIR),
        }
        result = subprocess.run(
            [
                "node",
                str(test_locator),
                *(("--no-ambient",) if not ambient else ()),
                *map(str, args),
            ],
            check=False,
            capture_output=True,
            text=True,
            cwd=cwd,
            env=locator_environment,
        )

    result.check_returncode()
    return json.loads(result.stdout)


def test_locator_pins_the_immutable_release_digest():
    assert f'"{PINNED_SKILL_SHA256}"' in LOCATOR.read_text(encoding="utf-8")


def write_upstream_skill(root: Path, *, bundled: bool) -> Path:
    if not bundled:
        root.mkdir(parents=True)
        skill = root / "SKILL.md"
        skill.write_bytes(TEST_SKILL.encode("utf-8"))
        return skill

    skill = root / "skills" / "create-maa-project" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_bytes(TEST_SKILL.encode("utf-8"))
    return skill


def test_locator_prefers_an_explicit_upstream_skill(tmp_path: Path):
    expected = write_upstream_skill(tmp_path, bundled=True)

    result = run_locator("--root", tmp_path)

    assert result["status"] == "found"
    assert result["source"] == "explicit"
    assert result["skillVersion"] == "3.2.0"
    assert Path(str(result["skillPath"])).resolve() == expected.resolve()
    assert result["pinnedVersion"] == "3.2.0"
    assert str(result["pinnedSkillUrl"]).endswith(
        "/create-maa-project/v3.2.0/skills/create-maa-project/SKILL.md"
    )


def test_locator_skips_an_unrelated_explicit_root_skill(tmp_path: Path):
    (tmp_path / "SKILL.md").write_text(
        "---\nname: unrelated-skill\ndescription: Unrelated.\n---\n",
        encoding="utf-8",
    )
    expected = write_upstream_skill(tmp_path, bundled=True)

    result = run_locator("--root", tmp_path)

    assert result["status"] == "found"
    assert result["source"] == "explicit"
    assert Path(str(result["skillPath"])).resolve() == expected.resolve()


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
    assert result["skillVersion"] == "3.2.0"
    assert Path(str(result["skillPath"])).resolve() == expected.resolve()


def test_locator_reports_a_pinned_skill_in_an_outdated_package(tmp_path: Path):
    package = tmp_path / "create-maa-project"
    package.mkdir()
    (package / "package.json").write_text(
        json.dumps({"name": "create-maa-project", "version": "2.0.0"}),
        encoding="utf-8",
    )
    expected = write_upstream_skill(package, bundled=True)

    result = run_locator("--root", package)

    assert result["status"] == "version-mismatch"
    assert result["skillPath"] == str(expected.resolve())
    assert result["packageVersion"] == "2.0.0"
    assert result["skillVersion"] == "3.2.0"


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

    payload = run_locator(ambient=True, environment=environment, cwd=tmp_path)
    assert payload["status"] == "found"
    assert payload["source"] == "installed-skill"
    assert payload["skillVersion"] == "3.2.0"
    assert Path(str(payload["skillPath"])).resolve() == expected.resolve()


def test_locator_reports_an_outdated_installed_user_skill(tmp_path: Path):
    home = tmp_path / "home"
    expected = home / ".codex" / "skills" / "create-maa-project" / "SKILL.md"
    skill_directory = home / ".codex" / "skills" / "create-maa-project"
    skill_directory.mkdir(parents=True)
    (skill_directory / "SKILL.md").write_text(
        "---\nname: create-maa-project\ndescription: Outdated Skill.\n---\n\n"
        "# Old command contract\n",
        encoding="utf-8",
    )
    environment = os.environ.copy()
    environment.update(
        {
            "HOME": str(home),
            "USERPROFILE": str(home),
            "CODEX_HOME": str(tmp_path / "codex-home"),
        }
    )

    payload = run_locator(ambient=True, environment=environment, cwd=tmp_path)

    assert payload["status"] == "version-mismatch"
    assert payload["skillPath"] == str(expected.resolve())
    assert payload["skillVersion"] is None

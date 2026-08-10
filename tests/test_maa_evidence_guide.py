from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "maa-evidence-guide"
LOCATOR = SKILL_DIR / "scripts" / "find-maa-evidence-skill.mjs"


def run_locator_process(
    *args: Path | str, guide_root: Path | None = None
) -> subprocess.CompletedProcess[str]:
    command = ["node", str(LOCATOR)]
    for candidate in args:
        command.extend(["--root", str(candidate)])
    environment = os.environ.copy()
    if guide_root is not None:
        environment["MAA_EVIDENCE_GUIDE_ROOT"] = str(guide_root)
    return subprocess.run(
        command, check=False, capture_output=True, text=True, env=environment
    )


def run_locator(*args: Path, guide_root: Path | None = None) -> dict[str, object]:
    result = run_locator_process(*args, guide_root=guide_root)
    result.check_returncode()
    return json.loads(result.stdout)


def write_upstream_skill(root: Path) -> Path:
    skill = root / "skills" / "maa-evidence" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(
        "---\nname: maa-evidence\ndescription: Test upstream Skill.\n---\n\n# Maa Evidence\n",
        encoding="utf-8",
    )
    return skill


def test_guide_is_a_thin_upstream_handoff():
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    metadata = yaml.safe_load(
        (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    )

    assert "maafw.bak.<timestamp>.log" in text
    assert "another `maafw.*.log`" in text
    assert "read it completely" in text
    assert "Do not improvise" in text
    assert "$maa-evidence-guide" in metadata["interface"]["default_prompt"]


def test_locator_prefers_an_explicit_upstream_skill(tmp_path: Path):
    expected = write_upstream_skill(tmp_path)
    result = run_locator(tmp_path)

    assert result["status"] == "found"
    assert result["source"] == "explicit"
    assert Path(str(result["skillPath"])).resolve() == expected.resolve()


def test_locator_rejects_an_incomplete_root_argument():
    result = subprocess.run(
        ["node", str(LOCATOR), "--root"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert result.stdout == ""
    assert "Usage: find-maa-evidence-skill.mjs" in result.stderr


def test_locator_prefers_an_explicit_skill_over_an_explicit_package(
    tmp_path: Path,
):
    package = tmp_path / "maa-evidence-kit"
    package.mkdir()
    (package / "package.json").write_text(
        json.dumps({"name": "maa-evidence-kit", "version": "1.2.3"}),
        encoding="utf-8",
    )
    write_upstream_skill(package)
    standalone_skill = write_upstream_skill(tmp_path / "standalone")

    for roots in (
        (package, standalone_skill.parent),
        (standalone_skill.parent, package),
    ):
        result = run_locator(*roots)

        assert result["status"] == "found"
        assert result["source"] == "explicit"
        assert Path(str(result["skillPath"])).resolve() == standalone_skill.resolve()


def test_locator_reads_a_package_skill_and_version(tmp_path: Path):
    package = tmp_path / "maa-evidence-kit"
    package.mkdir()
    (package / "package.json").write_text(
        json.dumps({"name": "maa-evidence-kit", "version": "1.2.3"}),
        encoding="utf-8",
    )
    expected = write_upstream_skill(package)

    result = run_locator(package)

    assert result["status"] == "found"
    assert result["packageVersion"] == "1.2.3"
    assert Path(str(result["skillPath"])).resolve() == expected.resolve()


def test_locator_reports_a_package_without_a_skill(tmp_path: Path):
    (tmp_path / "package.json").write_text(
        json.dumps({"name": "maa-evidence-kit", "version": "2.0.0"}),
        encoding="utf-8",
    )

    result = run_locator(tmp_path)

    assert result == {
        "status": "package-without-skill",
        "source": "explicit-package",
        "skillPath": None,
        "packageRoot": str(tmp_path.resolve()),
        "packageVersion": "2.0.0",
    }


def test_locator_excludes_a_package_skill_under_the_guide_root(tmp_path: Path):
    guide_root = tmp_path / "maa-evidence-guide"
    package = guide_root / "maa-evidence-kit"
    package.mkdir(parents=True)
    (package / "package.json").write_text(
        json.dumps({"name": "maa-evidence-kit", "version": "1.2.3"}),
        encoding="utf-8",
    )
    write_upstream_skill(package)

    result = run_locator(package, guide_root=guide_root)

    assert result == {
        "status": "package-without-skill",
        "source": "explicit-package",
        "skillPath": None,
        "packageRoot": str(package.resolve()),
        "packageVersion": "1.2.3",
    }

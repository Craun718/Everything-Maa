from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "maa-evidence-guide"
LOCATOR = SKILL_DIR / "scripts" / "find-maa-evidence-skill.mjs"


def run_locator_process(
    *args: Path | str,
    guide_root: Path | None = None,
    cwd: Path | None = None,
    environment: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    command = ["node", str(LOCATOR), *map(str, args)]
    process_environment = os.environ.copy()
    if guide_root is not None:
        process_environment["MAA_EVIDENCE_GUIDE_ROOT"] = str(guide_root)
    if environment is not None:
        process_environment.update(environment)
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        env=process_environment,
        cwd=cwd,
    )


def run_locator(
    *args: Path | str,
    guide_root: Path | None = None,
    cwd: Path | None = None,
    environment: dict[str, str] | None = None,
    ambient: bool = False,
) -> dict[str, object]:
    result = run_locator_process(
        *(("--no-ambient",) if not ambient else ()),
        *args,
        guide_root=guide_root,
        cwd=cwd,
        environment=environment,
    )
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
    result = run_locator("--root", tmp_path)

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
    assert "Usage: find-maa-evidence-skill.mjs [--no-ambient]" in result.stderr


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
        result = run_locator(
            *(argument for root in roots for argument in ("--root", root))
        )

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

    result = run_locator("--root", package)

    assert result["status"] == "found"
    assert result["packageVersion"] == "1.2.3"
    assert Path(str(result["skillPath"])).resolve() == expected.resolve()


def test_locator_reports_a_package_without_a_skill(tmp_path: Path):
    (tmp_path / "package.json").write_text(
        json.dumps({"name": "maa-evidence-kit", "version": "2.0.0"}),
        encoding="utf-8",
    )

    result = run_locator("--root", tmp_path)

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

    result = run_locator("--root", package, guide_root=guide_root)

    assert result == {
        "status": "package-without-skill",
        "source": "explicit-package",
        "skillPath": None,
        "packageRoot": str(package.resolve()),
        "packageVersion": "1.2.3",
    }


def test_locator_reads_pnpm_global_package_layout(tmp_path: Path):
    package = tmp_path / "pnpm-global" / "v11" / "hashed" / "node_modules" / "package"
    package.mkdir(parents=True)
    (package / "package.json").write_text(
        json.dumps({"name": "maa-evidence-kit", "version": "3.4.5"}),
        encoding="utf-8",
    )
    write_upstream_skill(package)

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    node_path = shutil.which("node")
    assert node_path is not None
    npm_script = tmp_path / "package-manager.mjs"
    pnpm_report = tmp_path / "pnpm-report.json"
    pnpm_report.write_text(
        json.dumps(
            [
                {
                    "path": str(tmp_path / "pnpm-global" / "v11"),
                    "dependencies": {
                        "maa-evidence-kit": {"version": "3.4.5", "path": str(package)}
                    },
                }
            ]
        ),
        encoding="utf-8",
    )

    npm_script.write_text(
        "import { readFileSync } from 'node:fs';\n"
        f"const output = process.argv[2] === 'root' ? JSON.stringify(process.argv.slice(2)) : readFileSync({json.dumps(str(pnpm_report))}, 'utf8');\n"
        "console.log(output);\n",
        encoding="utf-8",
    )
    if sys.platform == "win32":
        (bin_dir / "npm.cmd").write_text(
            f'@"{node_path}" "{npm_script}" %*\n', encoding="utf-8"
        )
        (bin_dir / "pnpm.cmd").write_text(
            f'@"{node_path}" "{npm_script}" %*\n', encoding="utf-8"
        )
    else:
        (bin_dir / "npm").write_text(
            f'#!{node_path}\n'
            "import { readFileSync } from 'node:fs';\n"
            f"const output = process.argv[2] === 'root' ? JSON.stringify(process.argv.slice(2)) : readFileSync({json.dumps(str(pnpm_report))}, 'utf8');\n"
            "console.log(output);\n",
            encoding="utf-8",
        )
        (bin_dir / "npm").chmod(0o755)
        (bin_dir / "pnpm").symlink_to(bin_dir / "npm")

    home = tmp_path / "home"
    codex_home = tmp_path / "codex-home"
    home.mkdir()
    codex_home.mkdir()
    result = run_locator(
        ambient=True,
        cwd=tmp_path,
        environment={
            "HOME": str(home),
            "USERPROFILE": str(home),
            "CODEX_HOME": str(codex_home),
            "PATH": str(bin_dir) + os.pathsep + os.environ["PATH"],
        },
    )

    assert result == {
        "status": "found",
        "source": "pnpm-global-package",
        "skillPath": str((package / "skills" / "maa-evidence" / "SKILL.md").resolve()),
        "packageRoot": str(package.resolve()),
        "packageVersion": "3.4.5",
    }

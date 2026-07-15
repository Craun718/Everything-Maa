from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "skills" / "maa-pipeline-generate" / "scripts"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("script_name", ["generate_node.py", "generate_sweep.py"])
def test_find_project_root_uses_target_project_not_skill_location(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, script_name: str
):
    module = load_module(f"test_{script_name.replace('.', '_')}", SCRIPT_DIR / script_name)
    project_root = tmp_path / "MaaExample"
    nested = project_root / "assets" / "resource" / "base"
    nested.mkdir(parents=True)
    (project_root / "assets" / "interface.json").write_text("{}", encoding="utf-8")

    monkeypatch.chdir(nested)
    monkeypatch.delenv("MAAHUB_ROOT", raising=False)
    monkeypatch.delenv("PROJECT_ROOT", raising=False)

    assert module.find_project_root() == project_root.resolve()


@pytest.mark.parametrize("script_name", ["generate_node.py", "generate_sweep.py"])
def test_find_project_root_respects_explicit_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, script_name: str
):
    module = load_module(f"test_env_{script_name.replace('.', '_')}", SCRIPT_DIR / script_name)
    explicit_root = tmp_path / "ExplicitProject"
    explicit_root.mkdir()
    monkeypatch.setenv("PROJECT_ROOT", str(explicit_root))

    assert module.find_project_root() == explicit_root.resolve()

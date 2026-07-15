from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
ALLOWED_SKILL_ENTRIES = {"SKILL.md", "agents", "assets", "references", "scripts"}
WINDOWS_ABSOLUTE_PATH = re.compile(r"(?i)\b[a-z]:[\\/](?:users|workspace|home)[\\/]")


def read_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError("SKILL.md frontmatter is not closed")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ValueError("SKILL.md frontmatter must be a mapping")
    return data


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_dir.name}: missing SKILL.md"]

    try:
        frontmatter = read_frontmatter(skill_md)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [f"{skill_dir.name}: {exc}"]

    if set(frontmatter) != {"name", "description"}:
        errors.append(f"{skill_dir.name}: frontmatter must contain only name and description")
    if frontmatter.get("name") != skill_dir.name:
        errors.append(
            f"{skill_dir.name}: frontmatter name is {frontmatter.get('name')!r}"
        )
    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{skill_dir.name}: description is missing")

    unexpected = {item.name for item in skill_dir.iterdir()} - ALLOWED_SKILL_ENTRIES
    if unexpected:
        errors.append(f"{skill_dir.name}: unexpected entries: {sorted(unexpected)}")

    metadata_path = skill_dir / "agents" / "openai.yaml"
    if not metadata_path.is_file():
        errors.append(f"{skill_dir.name}: missing agents/openai.yaml")
    else:
        try:
            metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
            interface = metadata["interface"]
            short_description = interface["short_description"]
            default_prompt = interface["default_prompt"]
            if not 25 <= len(short_description) <= 64:
                errors.append(
                    f"{skill_dir.name}: short_description must be 25-64 characters"
                )
            if f"${skill_dir.name}" not in default_prompt:
                errors.append(
                    f"{skill_dir.name}: default_prompt must mention ${skill_dir.name}"
                )
        except (KeyError, TypeError, yaml.YAMLError) as exc:
            errors.append(f"{skill_dir.name}: invalid agents/openai.yaml: {exc}")

    for path in skill_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".py", ".json", ".yaml"}:
            text = path.read_text(encoding="utf-8")
            if WINDOWS_ABSOLUTE_PATH.search(text):
                errors.append(f"{skill_dir.name}: personal absolute path in {path.relative_to(ROOT)}")

    return errors


def validate_repository() -> list[str]:
    errors: list[str] = []
    if not SKILLS_DIR.is_dir():
        return ["missing skills directory"]
    for skill_dir in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
        errors.extend(validate_skill(skill_dir))
    return errors


def main() -> int:
    errors = validate_repository()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    count = sum(1 for path in SKILLS_DIR.iterdir() if path.is_dir())
    print(f"Validated {count} Maa skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

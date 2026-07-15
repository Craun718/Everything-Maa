# Everything Maa

Everything Maa is a focused toolkit of reusable AI skills for MaaFramework projects. Its canonical content is limited to Maa project discovery, Pipeline authoring, node generation, option wiring, graph analysis, testing, and history auditing.

> Status: Phase 1 development baseline. The skills and tests are available; native plugin manifests, MCP presets, and the `npx everything-maa` installer are planned for the next phase.

## Core skills

| Skill | Purpose |
| --- | --- |
| `maa-project-init` | Scan a Maa project and produce a reusable `basic_info.md` handoff. |
| `maa-pipeline-guide` | Design and review MaaFramework Pipeline JSON. |
| `maa-pipeline-generate` | Generate recognition/action nodes and sweep OCR ROIs. |
| `maa-pipeline-option` | Wire runtime options across UI, Pipeline, and Python. |
| `maa-pipeline-testing` | Validate resources, recognition, Custom wiring, and runtime flows. |
| `maa-pipeline-graph` | Map Pipeline state relationships and external Python entries. |
| `maa-pipeline-history-audit` | Learn Pipeline and Custom conventions from Git history. |

Project-specific workflows belong under `recipes/` and are not installed as core skills.

## Repository layout

- `skills/`: canonical Maa skills; each directory is independently installable.
- `recipes/`: optional project or task recipes.
- `evals/`: skill evaluation cases kept outside installed skill payloads.
- `adapters/`: distribution metadata for MaaHub and future agent harnesses.
- `tests/`: portable fixtures and repository invariants.

## Development

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
python scripts/validate_skills.py
```

The current baseline supports Python 3.10 and later. Do not assume a skill is installed under `.claude/skills`, a particular drive letter, or the Everything Maa checkout itself.

## Scope and dependencies

Everything Maa does not vendor MaaMCP, Playwright MCP, MaaFramework binaries, or OCR models. MCP launch presets will reference official upstream packages and pin versions per Everything Maa release.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for license boundaries and [README.zh-CN.md](README.zh-CN.md) for Chinese documentation.

## License

Everything Maa's own skills, scripts, tests, and documentation are released under the [MIT License](LICENSE). Third-party runtimes keep their upstream licenses.

Everything Maa is a community project and is not an official MaaFramework distribution unless explicitly stated otherwise.

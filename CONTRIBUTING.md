# Contributing

Contributions must remain directly useful to MaaFramework development or operation.

1. Put reusable workflows under `skills/maa-*` and project-specific workflows under `recipes/`.
2. Keep each skill's `SKILL.md` concise; move detailed tables to `references/` and deterministic tooling to `scripts/`.
3. Do not add personal absolute paths, secrets, copyrighted game assets, MaaMCP source, or MaaFramework binaries.
4. Add or update tests and evals for behavioral changes.
5. Run `python -m pytest` and `python scripts/validate_skills.py` before submitting a change.

By contributing, you agree that your contribution is licensed under the repository's MIT License.

---
name: maa-project-create
description: Create, extend, diagnose, and update MaaFramework application projects through the create-maa-project MCP server or CLI. Use when asked to start or scaffold a Maa project, choose Pipeline versus Python Agent templates, add dev tools, GitHub workflows, Agent support, or resource packs, run project doctor, sync metadata, update schema/runtime/OCR/dependencies, inspect or restore backups, or hand a newly created project to other Maa skills.
---

# Maa Project Create

## 官方兼容性核对

创建或更新项目涉及 MaaFramework schema、runtime、binding 兼容性或依赖版本时，通过 `$maa-wiki` 定位官方来源后再执行 `update` 或解释报告。`create-maa-project` 的报告是执行结果，不是 MaaFramework 官方契约本身。

Use `create-maa-project` as the project lifecycle engine. Do not reproduce its templates or manually imitate its managed-file behavior.

## Load the bundled upstream Skill

Before composing the first project-changing, doctor, add, sync, update, backup, or cache command, locate and read the authoritative upstream `create-maa-project` Skill. The bundled upstream Skill is the command and report authority; this wrapper supplies routing and safety only.

1. If the user supplies a create-maa-project checkout, npm package root, standalone Skill directory, or `SKILL.md`, pass each candidate to the locator with `--root PATH`.
2. Run `node scripts/find-create-maa-project-skill.mjs`. The read-only locator searches installed standalone Skills, project and user installations, and npm/pnpm packages while excluding this Skill's own root. It never installs, downloads, builds, or updates anything.
3. For `status: "found"`, read `skillPath` completely. Resolve its relative links from the directory containing that file and read only the references required by the requested operation.
4. For `status: "package-without-skill"` or `status: "not-found"`, use the pinned `v3.2.0` Skill URL returned by the locator. Do not substitute guidance from `main`; the Python wheel does not contain the upstream Skill.
5. Compare the Skill version with the resolved runtime version (`create-maa-project --cli-version`) or with the catalog pin before invoking it. If they do not match, obtain and read the Skill for the resolved runtime version before continuing.

Preserve the upstream Skill's non-interactive, JSON-report, version-checking, and backup requirements. Set `CREATE_MAA_PROJECT_AUTO_UPDATE=0` for a reproducible pinned run and do not re-enable automatic runtime or Skill updates. Prefer an installed CLI over a checkout's `dist` files. If a complete matching upstream Skill cannot be read, stop and report the locator result plus the release route attempted. Do not improvise create-maa-project commands from this Skill alone.

## Route the request

Choose the smallest operation that matches the user's intent:

| Intent | MCP tool | Mutation |
| --- | --- | --- |
| Create a project | `create_project` | Yes |
| Check project health | `doctor` | No |
| Change supported metadata | `sync` | Yes |
| Add Agent, resource pack, CI, or dev tooling | `add` | Yes |
| Update schema, MaaFW, runtime, OCR, or dependencies | `update` | Yes |
| Inspect backups | `list_backups` / `show_backup` | No |
| Restore a backup | `restore` | Yes, potentially destructive |
| Remove local cache | `clean_cache` | Yes |

Prefer MCP when it is configured. Use the pinned CLI fallback in [references/cli-and-reports.md](references/cli-and-reports.md) when MCP is unavailable or when a follow-up command must run with a different working directory. See [references/upstream-skill-discovery.md](references/upstream-skill-discovery.md) for the fixed-version handoff.

## Create workflow

1. Resolve the target directory and inspect whether it already exists. Do not use force flags or allow a non-Git non-empty directory without explicit user approval.
2. Collect the choices that materially affect the result:
   - project folder/path;
   - `pipeline` or `agent` template;
   - ASCII kebab-case slug and human display name when they differ;
   - controller targets (`Adb`, `Win32`, `MacOS`, `PlayCover`, `Gamepad`, `WlRoots`);
   - license;
   - Git initialization;
   - add-ons and optional resource-pack slug.
   - add-ons and optional resource-pack slug;
   - whether the tool may initialize Git and create the initial commit.
3. Default to `pipeline` only when the user does not need Python custom logic. Choose `agent` when they ask for CustomAction, CustomRecognition, AgentServer, or Python business logic.
4. For a normal maintained repository, recommend `dev-tools` and `github`; do not silently add them when the user asked for a minimal resource-only project.
5. Require `resourcePackSlug` whenever `resource-pack` is selected. Keep it ASCII kebab-case; use the label for localized display text.
6. Call `create_project` once with the resolved choices. Avoid a sequence of partially overlapping create calls.
7. Inspect the returned report before declaring success. Report written files, skipped files, pending actions, and suggested commands.
8. Run `doctor` from the new project root. The MCP server keeps the working directory it was launched with, so use the CLI fallback with its working directory set to the new project when necessary.
9. Run `$maa-project-init` against the completed project to create `basic_info.md`, then route further work to the relevant Maa skill.

In 3.2.0, Git initialization and the initial commit are enabled by default when the target is not already inside a Git repository. Keep `git=false` (or `--no-git`) when the user has not accepted an automatic initial commit, and report the `git` field from the create report.

## Maintain an existing project

1. Confirm the target is a create-maa-project project by locating `maa-project.json`.
2. Run `doctor --report` first. Use `doctor.checks[].summary` and `details`, not guesses, to identify scaffold or managed-file findings.
3. Prefer `sync`, `add`, or a specific `update` target over manual edits to tool-managed files. Migrate legacy schema v1 only with an explicit `sync config` request.
4. Never invent an `update all` operation. Use explicit update targets so pending actions and failures stay attributable.
5. Before restore, list backups, inspect the selected backup, run a dry-run preview, and obtain explicit confirmation when restoration can replace current work. Preserve both `backupId` and `preRestoreBackupId` in the result.

## Interpret reports

Treat the structured report as the source of truth:

- `ok: true` means the requested operation completed, but `pending` may still require follow-up.
- A doctor report with `ok: false` is a health finding, not proof that project creation failed.
- Show `pending[].command` and its reason. Execute it only when it is safe, in scope, and authorized.
- Read `doctor.checks`, `error.code`, `backupId`, `git`, and `logPath` as structured evidence. Do not infer a failure from human-readable stderr when stdout contains a report.
- Preserve the log path when reporting a failure.

## Safety boundaries

- Do not copy create-maa-project source or templates into Everything Maa. It remains an external AGPL runtime.
- Do not pass `--force`, `--allow-non-git-dir`, `--allow-pending-commit`, `--clear-stale-lock`, or restore operations by default. Use a protection-waiving flag only when the report asks for that exact flag and the user explicitly agrees.
- Do not hide downloads behind a dry-looking command. State when OCR models, runtimes, or dependencies may be fetched.
- Do not claim the project is ready while doctor findings or pending actions remain unexplained.
- Do not commit, push, publish, or create remote repositories unless the user requested those actions.

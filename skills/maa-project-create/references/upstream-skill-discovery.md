# Upstream Skill discovery

`create-maa-project` 3.2.0 is the first integrated release that bundles an agent Skill. The Python wheel contains only the launcher; it does not contain `skills/create-maa-project/SKILL.md`. Discovery therefore uses local installed Skills/packages first and a fixed release URL as the fallback.

## Locator

Run from the `maa-project-create` Skill root:

```bash
node scripts/find-create-maa-project-skill.mjs
```

For user-provided checkouts, package roots, standalone Skill directories, or `SKILL.md` files:

```bash
node scripts/find-create-maa-project-skill.mjs --root PATH
```

The locator validates the frontmatter `name: create-maa-project`, excludes Everything Maa's wrapper copy, and returns JSON with:

| Field | Meaning |
| --- | --- |
| `status` | `found`, `package-without-skill`, or `not-found` |
| `skillPath` | Local authoritative `SKILL.md`, when found |
| `packageRoot` / `packageVersion` | npm package metadata, when applicable |
| `pinnedVersion` / `pinnedSkillUrl` | Fixed `v3.2.0` fallback |

Search precedence is an explicit candidate, then an installed standalone Skill, then a project npm package, then npm/pnpm globals. Package metadata is not a substitute for the runtime version; query the CLI itself with `--cli-version`.

## Fixed fallback

When no complete local copy is available, read:

```text
https://raw.githubusercontent.com/Windsland52/create-maa-project/v3.2.0/skills/create-maa-project/SKILL.md
```

Resolve upstream relative links against:

```text
https://github.com/Windsland52/create-maa-project/tree/v3.2.0/skills/create-maa-project/
```

Do not use `main` as authoritative guidance for the pinned 3.2.0 runtime. If the resolved runtime is another version, read that version's formal release tag when it exists, and disclose an unpinned fallback if it does not.

## Version and updates

Check the runtime before operation:

```bash
CREATE_MAA_PROJECT_AUTO_UPDATE=0 uvx --from create-maa-project==3.2.0 create-maa-project --cli-version
```

The launcher can hand off to npm `latest` and synchronize its managed Skill. Disable both behaviors for reproducible use:

```text
CREATE_MAA_PROJECT_AUTO_UPDATE=0
```

Never let the locator install or update the runtime or Skill. If a matching complete `SKILL.md` cannot be read, stop instead of composing commands from memory.

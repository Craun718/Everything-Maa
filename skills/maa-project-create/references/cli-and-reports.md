# CLI fallback and report contract

Use the pinned external runtime. Do not use a moving release tag in automated workflows, and load the matching upstream Skill first as described in [upstream-skill-discovery.md](upstream-skill-discovery.md).

## Base command

```bash
CREATE_MAA_PROJECT_AUTO_UPDATE=0 uvx --from create-maa-project==3.2.0 create-maa-project
```

Verify the resolved CLI before use:

```bash
CREATE_MAA_PROJECT_AUTO_UPDATE=0 uvx --from create-maa-project==3.2.0 create-maa-project --cli-version
CREATE_MAA_PROJECT_AUTO_UPDATE=0 uvx --from create-maa-project==3.2.0 create-maa-project --help
```

The upstream Skill and `--help` define the command contract. Require `--report` for non-interactive agent use unless the operation is only `--cli-version` or `--help`.

## Create examples

```bash
# Pipeline project
CREATE_MAA_PROJECT_AUTO_UPDATE=0 uvx --from create-maa-project==3.2.0 create-maa-project ./maa-example \
  --template pipeline --controller Adb --license MIT \
  --add dev-tools --add github --no-interactive --yes --report

# Python Agent project without network downloads during scaffolding
CREATE_MAA_PROJECT_AUTO_UPDATE=0 uvx --from create-maa-project==3.2.0 create-maa-project ./maa-agent \
  --template agent --controller Adb,Win32 --license MIT \
  --skip-download --no-interactive --yes --report
```

Set the process working directory to the target project for maintenance commands:

```bash
CREATE_MAA_PROJECT_AUTO_UPDATE=0 uvx --from create-maa-project==3.2.0 create-maa-project --doctor --report
CREATE_MAA_PROJECT_AUTO_UPDATE=0 uvx --from create-maa-project==3.2.0 create-maa-project --add agent --report
CREATE_MAA_PROJECT_AUTO_UPDATE=0 uvx --from create-maa-project==3.2.0 create-maa-project --update schema --report
CREATE_MAA_PROJECT_AUTO_UPDATE=0 uvx --from create-maa-project==3.2.0 create-maa-project --list-backups --report
CREATE_MAA_PROJECT_AUTO_UPDATE=0 uvx --from create-maa-project==3.2.0 create-maa-project --show-backup BACKUP-ID --report
CREATE_MAA_PROJECT_AUTO_UPDATE=0 uvx --from create-maa-project==3.2.0 create-maa-project --restore BACKUP-ID --dry-run --report
```

There is no `--diff` or `--update all` mode in 3.2.0. Use `doctor` for health findings and one explicit update target at a time.

## Report fields

The CLI writes a single JSON document to stdout in report mode. Read these fields:

| Field | Meaning |
| --- | --- |
| `ok` / `exitCode` | Operation result; doctor findings may intentionally produce a failing status |
| `command` | `create`, `doctor`, `sync`, `update`, `add`, `backup`, or `clean-cache` |
| `root` | Project root used by the operation |
| `written` / `skipped` | Files changed or intentionally left alone |
| `pending` | Follow-up commands with reasons |
| `doctor.checks` | Individual pass, fail, or skipped health findings |
| `backupId` / `backup` | Snapshot created or inspected by this run |
| `git` | Whether the tool initialized Git or made the initial commit |
| `suggestedCommands` | Explicit next actions and whether the tool considers them auto-runnable |
| `logPath` | Diagnostic log to retain on failure |
| `error` | Structured failure message and optional code |

Do not parse human-readable stderr as the primary result when a JSON report exists.

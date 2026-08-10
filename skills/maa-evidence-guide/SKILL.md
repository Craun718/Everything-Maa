---
name: maa-evidence-guide
description: Locate and load the authoritative MaaEvidenceKit `maa-evidence` Skill before extracting or correlating traceable MaaFramework evidence. Use when a user mentions MaaEvidenceKit, `maa-evidence`, MLA or MSE evidence extraction, supplies `maafw.log`, a timestamped `maafw.bak` log, or another `maafw.*.log` file, or asks to diagnose MaaFramework runtime behavior from logs and issue-time project source.
---

# Maa Evidence Guide

Use this Skill only as an entry point. Do not reconstruct, summarize from memory, or duplicate the
MaaEvidenceKit workflow. Locate the upstream `maa-evidence` Skill, read it completely, load the
references it requires for the current task, and then continue the user's request under those
instructions. Treat `maafw.log`, `maafw.bak.<timestamp>.log`, and other `maafw.*.log` paths as
explicit reasons to perform this handoff.

## Locate the authoritative Skill

1. If the user supplies a candidate MaaEvidenceKit checkout, package root, skill directory, or
   `SKILL.md`, pass it to the locator with `--root PATH`.
2. Run `node scripts/find-maa-evidence-skill.mjs`. Add `--root PATH` once for each explicit candidate.
   The script is read-only and offline. It searches installed agent skills first, then local and
   global npm/pnpm installations of `maa-evidence-kit`, while excluding this guide.
3. Parse the JSON result:
   - For `status: "found"`, read `skillPath` completely. Resolve its relative links from the
     directory containing that file.
   - For `status: "package-without-skill"`, use `packageVersion` to read
     `https://github.com/Windsland52/MaaEvidenceKit/tree/v<version>/skills/maa-evidence`.
   - For `status: "not-found"`, query the latest formal GitHub Release of
     `Windsland52/MaaEvidenceKit` and read `skills/maa-evidence/SKILL.md` at that release tag.
     If no formal release exposes the Skill, read it from the repository's default branch and tell
     the user that the guidance is unpinned and may drift.
4. When a GitHub copy is used, read the raw `SKILL.md` completely and retrieve only the linked
   references required by the current task. Do not treat a search-result excerpt or repository
   landing page as the Skill contents.

Prefer an installed standalone `maa-evidence` Skill over a package copy. Prefer a package copy over
GitHub. When multiple candidates have the same precedence, use the first explicit `--root`, then
the nearest project installation, then the user-level installation.

## Hand off the task

After loading the upstream Skill, follow it directly and continue the current request without asking
the user to invoke another Skill. Treat MaaEvidenceKit as a deterministic evidence extractor, not as
a source of model-generated conclusions. Preserve the upstream Skill's installation, privacy,
telemetry, evidence, and version-matching requirements.

If no complete upstream Skill can be read, stop and report every location or GitHub route attempted.
Do not improvise MaaEvidenceKit commands from this guide alone.

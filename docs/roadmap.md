# Roadmap

Everything Maa is organized as six delivery phases. Phases describe repository capability, not public publication status.

| Phase | Outcome | Status |
| --- | --- | --- |
| 1 | Establish canonical Maa skills, provenance boundaries, tests, and repository structure. | Complete |
| 2 | Add native Codex/Claude plugin manifests, versioned MCP profiles, and the dependency-free `npx` installer. | Complete |
| 3 | Integrate create-maa-project as an external lifecycle engine and add project creation/maintenance guidance. | Complete |
| 4 | Add the maafw-cli low-context operation lane with JSON contracts and runtime routing against MaaMCP. | Complete |
| 5 | Add release-contract validation, cross-platform CI, dependency updates, and tag-gated npm trusted publishing. | Complete |
| 6 | Complete Claude marketplace metadata, MaaHub adapters, distribution catalog, and release documentation. | Complete locally |

## Public release gate

The repository remains pre-release until the maintainer creates the public GitHub repository, confirms package ownership, configures npm trusted publishing, reviews the first changelog version, and deliberately pushes the matching release tag. See [releasing.md](releasing.md).

## Post-release candidates

- Collect real-world eval traces for each skill and tune triggering descriptions where routing overlaps.
- Promote maafw-cli from experimental only after its command and JSON contracts stabilize upstream.
- Add a dedicated Codex marketplace bundle only if it can be generated without duplicating canonical skill sources.
- Add signed compatibility records for tested MaaFramework, MaaMCP, create-maa-project, and maafw-cli combinations.

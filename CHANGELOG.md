# Changelog

All notable changes to Everything Maa will be documented in this file. The project follows Semantic Versioning after the first public release.

## [Unreleased]

### Added

- `maa-wiki` skill that routes MaaFramework knowledge questions and other Maa skills to authoritative official documentation, schemas, APIs, bindings, releases, and semantic changes through the MaaLLMWiki catalog.
- Added `maa-interface-guide` for reviewing, diagnosing, and modifying existing MaaFramework Project Interface V2 files with project-first schema resolution and guarded `maa-tools` validation.

## [0.1.1] - 2026-07-19

### Added

- End-to-end Maa workflow orchestration that connects project initialization, Pipeline authoring, options, graph analysis, testing, and specialist feedback loops.
- Project initialization guidance that visualizes Python custom action and AgentServer relationships.

### Changed

- Upgraded GitHub Actions runtimes used by CI and release workflows.
- Made project context initialization and Pipeline graph invocation explicit in the orchestration contract.

### Fixed

- Defined ownership of specialist feedback loops so generated Maa workflows return to the correct orchestration stage.

## [0.1.0] - 2026-07-15

### Added

- Ten MaaFramework lifecycle skills covering intent-to-workflow orchestration, project creation and discovery, Pipeline authoring, generation, options, graphing, testing, history auditing, and CLI operation.
- Versioned `skills-only`, `core`, `authoring`, and `full` installation profiles for Codex and Claude Code.
- External integrations for MaaMCP, create-maa-project, maafw-cli, and isolated Playwright MCP.
- Dependency-free `everything-maa` installer with dry-run, doctor, managed uninstall, and conflict recovery.
- Cross-platform tests, upstream contract smoke tests, native plugin manifests, and release validation.
- Self-hosted Claude marketplace metadata, a complete ten-skill MaaHub adapter set, and a machine-readable distribution catalog.

[Unreleased]: https://github.com/KhazixW2/Everything-Maa/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/KhazixW2/Everything-Maa/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/KhazixW2/Everything-Maa/releases/tag/v0.1.0

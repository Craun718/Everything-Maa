from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "maa-diagnose"
WORKFLOW_DIR = ROOT / "skills" / "maa-workflow-build"

FAILURE_OWNERS = (
    "generate",
    "option",
    "testing",
    "workflow-design",
    "workflow-implement",
    "project-create",
    "user",
)


def read(*parts: str) -> str:
    return SKILL_DIR.joinpath(*parts).read_text(encoding="utf-8")


def test_skill_drives_the_external_runtime_instead_of_reimplementing_it():
    text = read("SKILL.md")

    assert "It does not parse MaaFramework logs itself" in text
    assert "does not contain a diagnostic engine" in text
    assert "references/runtime-discovery.md" in text
    assert "references/failure-map.md" in text


def test_skill_discovers_the_runtime_before_invoking_it():
    skill = read("SKILL.md")
    discovery = read("references", "runtime-discovery.md")

    assert "Never assume a command catalog from memory" in skill
    assert "maa-evidence --version" in discovery
    assert "maa-evidence --help" in discovery
    assert "Re-run discovery every session; never cache a command catalog" in discovery


def test_precedence_policy_orders_mcp_then_cli_then_local_checkout():
    discovery = read("references", "runtime-discovery.md")

    mcp = discovery.index("**Local MCP surface.**")
    cli = discovery.index("**Packaged CLI on `PATH`.**")
    checkout = discovery.index("**User-supplied local checkout.**")

    assert mcp < cli < checkout
    assert "Do not mix surfaces inside one diagnosis" in discovery
    assert "Never install, build, or upgrade the runtime" in discovery


def test_missing_or_incompatible_runtime_fails_safely():
    discovery = read("references", "runtime-discovery.md")

    assert "diagnostic-runtime-unavailable" in discovery
    assert "diagnostic-contract-unsupported" in discovery
    assert "diagnostic-runtime-host-unsupported" in discovery
    assert "## When the contract changes" in discovery


def test_supported_runtime_versions_are_documented_and_pinned():
    discovery = read("references", "runtime-discovery.md")
    integrations = json.loads(
        (ROOT / "integrations" / "catalog.json").read_text(encoding="utf-8")
    )
    notices = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    tool = integrations["tools"]["maa-evidence-kit"]

    assert tool["package"] == "maa-evidence-kit"
    assert tool["version"] == "0.3.2"
    assert tool["role"] == "diagnostic-runtime"
    assert tool["version"] in discovery
    assert ">=0.3.0 <0.4.0" in discovery
    assert "maa-evidence-kit" in notices and "0.3.2" in notices


def test_structured_contract_is_primary_and_output_is_read_only():
    skill = read("SKILL.md")

    assert "parse the JSON envelope" in skill
    assert "Never treat the human-readable text or diagram renderer as the primary contract" in skill
    assert "Never mutate the project" in skill
    assert "Recommend a repair; do not apply one." in skill


def test_runtime_side_effects_are_suppressed():
    discovery = read("references", "runtime-discovery.md")

    assert "MAA_EVIDENCE_AUTO_UPDATE=0" in discovery
    assert "Never run `feedback`" in discovery
    assert "Do not enable telemetry" in discovery


def test_normalized_result_covers_every_bounded_failure_owner():
    skill = read("SKILL.md")
    failure_map = read("references", "failure-map.md")

    for field in (
        "status",
        "summary",
        "findings",
        "evidence",
        "artifacts",
        "next_actions",
        "failure_owner",
        "stop_reason",
    ):
        assert f"{field}:" in skill, field
        assert f"| `{field}` |" in failure_map or f"{field}:" in failure_map, field

    for owner in FAILURE_OWNERS:
        assert owner in skill, owner
        assert f"`{owner}`" in failure_map, owner


def test_required_failure_classes_are_covered():
    failure_map = read("references", "failure-map.md")

    assert "Resource or schema failure" in failure_map
    assert "Environment or dependency failure" in failure_map
    assert "Runtime log failure" in failure_map
    assert "Missing runtime" in failure_map
    assert "Preserve the runtime's evidence ids verbatim" in failure_map


def test_skill_reuses_upstream_adapters():
    skill = read("SKILL.md")
    discovery = read("references", "runtime-discovery.md")

    assert "MaaLogAnalyzer" in skill and "maa-support-extension" in skill
    assert "Do not re-implement discovery, parsing, or retrieval here." in skill
    assert "MaaEvidenceKit" in discovery
    assert "MaaDiagnosticExpert" in discovery


def test_diagnosis_is_not_triggered_for_already_attributed_failures():
    skill = read("SKILL.md")
    recovery = (WORKFLOW_DIR / "references" / "recovery-policy.md").read_text(
        encoding="utf-8"
    )
    testing = (
        ROOT / "skills" / "maa-pipeline-testing" / "SKILL.md"
    ).read_text(encoding="utf-8")

    assert "already attributed the failure" in skill
    assert "must not trigger a broad diagnostic pipeline" in recovery
    assert "$maa-diagnose" in testing


def test_workflow_recover_routes_unknown_failures_to_the_skill():
    workflow = (WORKFLOW_DIR / "SKILL.md").read_text(encoding="utf-8")
    recovery = (WORKFLOW_DIR / "references" / "recovery-policy.md").read_text(
        encoding="utf-8"
    )

    assert "Invoke `$maa-diagnose` only from `RECOVER`" in workflow
    assert "| Unknown failure class after focused testing | `$maa-diagnose` |" in recovery
    assert "## Request diagnosis only when the owner is unknown" in recovery
    assert "### Consume the diagnostic result" in recovery
    assert "diagnostic-runtime-unavailable" in recovery
    for owner in FAILURE_OWNERS:
        assert f"`{owner}`" in recovery, owner


def test_metadata_docs_and_evals_are_discoverable():
    metadata = yaml.safe_load(read("agents", "openai.yaml"))
    evals = json.loads((ROOT / "evals" / "maa-diagnose.json").read_text(encoding="utf-8"))
    adapter = json.loads(
        (ROOT / "adapters" / "maahub" / "skills" / "maa-diagnose.json").read_text(
            encoding="utf-8"
        )
    )

    assert "$maa-diagnose" in metadata["interface"]["default_prompt"]
    assert evals["skill_name"] == "maa-diagnose"
    assert len(evals["evals"]) >= 6
    assert adapter["id"] == "KhazixW2/maa-diagnose"
    assert (ROOT / "docs" / "skills" / "maa-diagnose.md").is_file()


def test_routing_boundary_evals_exist():
    workflow_evals = json.loads(
        (ROOT / "evals" / "maa-workflow-build.json").read_text(encoding="utf-8")
    )
    testing_evals = json.loads(
        (ROOT / "evals" / "maa-pipeline-testing.json").read_text(encoding="utf-8")
    )
    diagnose_evals = json.loads(
        (ROOT / "evals" / "maa-diagnose.json").read_text(encoding="utf-8")
    )

    names = {case["eval_name"] for case in workflow_evals["evals"]}
    assert "do-not-diagnose-when-testing-named-the-owner" in names
    assert "request-diagnosis-only-for-unknown-failure-class" in names
    assert "continue-recovery-when-diagnostic-runtime-missing" in names

    assert "focused-recognition-failure-stays-with-generate" in {
        case["eval_name"] for case in testing_evals["evals"]
    }
    assert "do-not-broaden-focused-recognition-failure" in {
        case["eval_name"] for case in diagnose_evals["evals"]
    }


def test_skill_name_does_not_collide_with_project_create_doctor():
    skill_names = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}

    assert "maa-diagnose" in skill_names
    assert not any("doctor" in name for name in skill_names)

    doc = (ROOT / "docs" / "skills" / "maa-diagnose.md").read_text(encoding="utf-8")
    assert "doctor" in doc
    assert "$maa-project-create" in read("SKILL.md")

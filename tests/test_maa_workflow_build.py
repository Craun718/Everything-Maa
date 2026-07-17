from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "maa-workflow-build"


def test_workflow_build_owns_the_end_to_end_control_loop():
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

    for phase in (
        "SPECIFY",
        "DISCOVER",
        "DESIGN",
        "IMPLEMENT",
        "VERIFY",
        "COMPLETE",
        "RECOVER",
    ):
        assert phase in text

    for routed_skill in (
        "$maa-pipeline-guide",
        "$maa-pipeline-generate",
        "$maa-pipeline-option",
        "$maa-pipeline-testing",
        "$maa-cli-operate",
    ):
        assert routed_skill in text

    assert "Do not declare completion" in text
    assert "references/task-contract.md" in text
    assert "references/run-state.md" in text
    assert "references/acceptance-protocol.md" in text
    assert "references/recovery-policy.md" in text


def test_workflow_build_consumes_init_and_graph_artifacts_without_invoking_setup():
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

    assert "Never invoke `$maa-project-init` or `$maa-pipeline-graph` automatically" in text
    assert "only when the user explicitly requests" in text
    assert "basic_info.md" in text
    assert "pipeline_overview.html" in text
    assert "continue with targeted source discovery" in text


def test_workflow_contracts_define_state_feedback_and_exit_conditions():
    task_contract = (SKILL_DIR / "references" / "task-contract.md").read_text(
        encoding="utf-8"
    )
    run_state = (SKILL_DIR / "references" / "run-state.md").read_text(
        encoding="utf-8"
    )
    acceptance = (SKILL_DIR / "references" / "acceptance-protocol.md").read_text(
        encoding="utf-8"
    )
    recovery = (SKILL_DIR / "references" / "recovery-policy.md").read_text(
        encoding="utf-8"
    )

    for field in (
        "goal",
        "start_states",
        "success_states",
        "constraints",
        "acceptance_criteria",
    ):
        assert field in task_contract

    for field in (
        "status",
        "summary",
        "next_actions",
        "artifacts",
        "evidence",
        "stop_reason",
    ):
        assert field in run_state

    assert "observable evidence" in acceptance
    assert "root cause" in recovery
    assert "safe retry" in recovery
    assert "stop condition" in recovery


def test_workflow_build_metadata_adapter_docs_and_evals_are_discoverable():
    metadata = yaml.safe_load(
        (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    )
    adapter = json.loads(
        (
            ROOT
            / "adapters"
            / "maahub"
            / "skills"
            / "maa-workflow-build.json"
        ).read_text(encoding="utf-8")
    )
    evals = json.loads(
        (ROOT / "evals" / "maa-workflow-build.json").read_text(encoding="utf-8")
    )

    assert "$maa-workflow-build" in metadata["interface"]["default_prompt"]
    assert adapter["id"] == "KhazixW2/maa-workflow-build"
    assert evals["skill_name"] == "maa-workflow-build"
    assert len(evals["evals"]) >= 4
    assert any("体力药剂" in case["prompt"] for case in evals["evals"])
    stamina_eval = next(case for case in evals["evals"] if "体力药剂" in case["prompt"])
    assert "不自动调用 init 或 graph" in stamina_eval["expected_output"]
    assert (ROOT / "docs" / "skills" / "maa-workflow-build.md").is_file()


def test_specialist_skills_route_uncompiled_end_to_end_requests_to_workflow_build():
    for skill_name in (
        "maa-pipeline-guide",
        "maa-pipeline-generate",
        "maa-pipeline-option",
        "maa-pipeline-testing",
    ):
        text = (ROOT / "skills" / skill_name / "SKILL.md").read_text(
            encoding="utf-8"
        )
        assert "$maa-workflow-build" in text, skill_name


def test_specialist_skills_do_not_auto_invoke_project_init():
    for skill_name in (
        "maa-pipeline-guide",
        "maa-pipeline-generate",
        "maa-pipeline-graph",
        "maa-pipeline-option",
        "maa-pipeline-testing",
    ):
        text = (ROOT / "skills" / skill_name / "SKILL.md").read_text(
            encoding="utf-8"
        )
        assert "不得自动调用 `$maa-project-init`" in text, skill_name

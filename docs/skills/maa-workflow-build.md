# Maa Workflow Build

将模糊的 Maa 自动化需求转化为可执行、可恢复、可验收的端到端工作流。

## 包含内容

- `skills/maa-workflow-build/SKILL.md`：任务生命周期与跨 skill 编排协议
- `skills/maa-workflow-build/references/`：任务契约、运行状态、验收和恢复协议
- `evals/maa-workflow-build.json`：任务级编排评测案例

## 作用

本 skill 负责从用户意图开始，建立目标、起始状态、安全约束和验收条件，随后编排项目发现、Pipeline 设计、节点生成、选项接线与测试技能。只有在必要验收项获得证据后，任务才可以完成。

项目级 `basic_info.md` 与已有 Pipeline 图谱只作为可选上下文产物读取。本 skill 不自动调用 `maa-project-init` 或 `maa-pipeline-graph`；初始化、刷新和图谱生成由用户显式发起。

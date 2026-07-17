# Maa Workflow Build

将模糊的 Maa 自动化需求转化为可执行、可恢复、可验收的端到端工作流。

## 包含内容

- `skills/maa-workflow-build/SKILL.md`：任务生命周期与跨 skill 编排协议
- `skills/maa-workflow-build/references/`：任务契约、运行状态、验收和恢复协议
- `evals/maa-workflow-build.json`：任务级编排评测案例

## 作用

本 skill 负责从用户意图开始，建立目标、起始状态、安全约束和验收条件，随后编排项目发现、Pipeline 设计、节点生成、选项接线与测试技能。只有在必要验收项获得证据后，任务才可以完成。

项目级 `basic_info.md` 与已有 Pipeline 图谱只作为可选上下文产物读取。本 skill 不自动调用 `maa-project-init` 或 `maa-pipeline-graph`；初始化、刷新和图谱生成由用户显式发起。

## 专业 Skill 的职责

- `maa-pipeline-guide` 是规则与说明书；guide 不是执行阶段，也不负责生产节点。
- `maa-pipeline-generate` 是 OCR、TemplateMatch、ROI 和动作节点的主要生产者。
- `maa-pipeline-option` 只在任务要求用户可配置项时调用。
- `maa-pipeline-testing` 在每个可验证实现增量之后运行，并将失败反馈给对应责任方。
- `maa-workflow-build` 负责整体组装、状态机设计、失败路由和最终验收。

这些能力不是固定的 `guide → generate → option → testing` 流水线：

```mermaid
flowchart TD
    U[用户模糊需求] --> W[maa-workflow-build]
    W --> C[任务契约]
    C --> D[发现项目与页面状态]
    D --> M[设计完整状态机]

    GUIDE[(maa-pipeline-guide<br/>规则与说明书)]
    GUIDE -.约束.-> M
    GUIDE -.约束.-> A

    M --> O{需要用户配置吗}
    O -->|是| OPTION[maa-pipeline-option]
    O -->|否| GEN[maa-pipeline-generate]
    OPTION --> GEN
    GEN --> A[workflow-build 组装 Pipeline]
    A --> TEST[maa-pipeline-testing]
    TEST --> R{验收结果}

    R -->|识别或动作节点失败| GEN
    R -->|选项接线失败| OPTION
    R -->|状态模型错误| M
    R -->|集成或控制流错误| A
    R -->|通过| END[完成并提交证据]
    R -->|环境、权限或安全阻塞| STOP[安全停止并请求最小解阻]
```

测试不是一次性的末尾动作。局部识别测试通过后还要验证结构、选项接线、失败与恢复路径，最后才执行获得授权的端到端验收。

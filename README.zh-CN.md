# Everything Maa

Everything Maa 是一个严格面向 MaaFramework 项目的 AI skills 工具集。核心范围只包括 Maa 项目发现、Pipeline 编写与生成、选项接线、节点图谱、测试和历史审计。

> 当前状态：Phase 1 开发基线。核心 skills 与测试已经独立；原生插件清单、MCP 预设和 `npx everything-maa` 安装器将在下一阶段加入。

## 核心 skills

| Skill | 用途 |
| --- | --- |
| `maa-project-init` | 扫描 Maa 项目并生成可复用的 `basic_info.md` 接力文档。 |
| `maa-pipeline-guide` | 设计、修改和审查 MaaFramework Pipeline JSON。 |
| `maa-pipeline-generate` | 生成识别/动作节点并扫描 OCR ROI。 |
| `maa-pipeline-option` | 贯通 UI、Pipeline 与 Python 的运行时选项。 |
| `maa-pipeline-testing` | 验证资源、识别、Custom 映射和端到端流程。 |
| `maa-pipeline-graph` | 梳理 Pipeline 状态关系与 Python 外部入口。 |
| `maa-pipeline-history-audit` | 从 Git 历史学习 Pipeline 与 Custom 约定。 |

项目专用工作流放在 `recipes/`，不作为核心 skills 默认安装。

## 仓库结构

- `skills/`：规范化 Maa skills，每个目录可独立安装。
- `recipes/`：可选的项目或任务配方。
- `evals/`：与安装载荷分离的 skill 评测用例。
- `adapters/`：MaaHub 及后续 agent 平台的分发元数据。
- `tests/`：跨平台 fixture 和仓库结构约束。

## 开发与验证

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
python scripts/validate_skills.py
```

当前基线支持 Python 3.10 及以上。skill 不得假设自己安装在 `.claude/skills`、固定盘符或 Everything Maa 源码目录中。

## 范围与依赖

Everything Maa 不复制 MaaMCP、Playwright MCP、MaaFramework 二进制或 OCR 模型。后续 MCP 预设只调用官方上游发行包，并按 Everything Maa 版本锁定经过验证的版本。

许可证边界见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 许可证

Everything Maa 自有的 skills、脚本、测试和文档使用 [MIT License](LICENSE)。第三方运行时继续遵守各自的上游许可证。

Everything Maa 是社区项目；除非另有明确说明，它不是 MaaFramework 官方发行版。

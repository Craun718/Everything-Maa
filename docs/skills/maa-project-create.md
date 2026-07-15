# Maa Project Create

通过外部 create-maa-project 生命周期引擎创建、扩展、诊断和更新 MaaFramework 项目，不复制其 AGPL 模板或源码。

## 适用场景

- 创建 Pipeline 或 Python Agent 项目。
- 添加开发工具、GitHub workflows、Agent 或资源包。
- 运行 doctor、diff、sync 和显式 update。
- 创建完成后衔接 Maa Project Init。

实现位于 `skills/maa-project-create/SKILL.md`，MaaHub 发布元信息位于 `adapters/maahub/skills/maa-project-create.json`。

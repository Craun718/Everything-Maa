# Maa Project Create

通过外部 create-maa-project 生命周期引擎创建、扩展、诊断和更新 MaaFramework 项目，不复制其 AGPL 模板或源码。

## 适用场景

- 创建 Pipeline 或 Python Agent 项目。
- 添加开发工具、GitHub workflows、Agent 或资源包。
- 运行 doctor、sync、显式 update、备份检查和恢复预演。
- 创建完成后衔接 Maa Project Init。

## 上游 Skill 定位

- 首次组 MCP/CLI 操作前，先运行 `skills/maa-project-create/scripts/find-create-maa-project-skill.mjs`。
- 显式 checkout、npm 包根目录或独立 Skill 路径优先；随后查找已安装 Skill、项目 npm 包与 npm/pnpm 全局包。
- 找到本地 Skill 时完整读取 `SKILL.md`，并只加载当前操作需要的相对引用。
- 本地不可用时读取固定 `v3.2.0` release 的上游 Skill；不用 `main` 冒充固定运行时指引。
- Skill 版本必须与 `create-maa-project --cli-version` 或 catalog pin 匹配；无法读取完整匹配指引时安全停止。

实现位于 `skills/maa-project-create/SKILL.md`，MaaHub 发布元信息位于 `adapters/maahub/skills/maa-project-create.json`。

---
name: maa-wiki
description: Route MaaFramework questions and other Maa skills to the authoritative MaaLLMWiki maallmwiki skill, its version-pinned catalog, and the original MaaFramework documentation, schemas, APIs, bindings, releases, and semantic changes. Use when official Maa knowledge must be verified before designing, testing, or citing Maa ecosystem behavior.
---

# Maa Wiki

将 MaaFramework 相关问题和其它 Maa skill 路由到 MaaLLMWiki 的正式 `maallmwiki` skill，再由该 skill 定位权威官方材料。本 skill 是本地集成路由器，不是答案仓库；最终结论必须回到原始文档、schema 或源码。

## 用途与边界

- 覆盖 MaaFramework 官方文档、Pipeline/schema 规范、native API、binding API、release 历史、语义变化和兼容性证据。
- 项目专用 Pipeline 配置、用户项目事实、游戏 UI 状态和未经核实的诊断结论不在本 skill 范围内。
- 本 skill 不复制、缓存或内置 MaaLLMWiki catalog 或上游 `maallmwiki` skill；只按需读取上游 URL。

## 加载上游 skill

先完整读取 MaaLLMWiki 仓库中的权威路由 skill：

```text
https://raw.githubusercontent.com/Windsland52/MaaLLMWiki/main/skills/maallmwiki/SKILL.md
```

上游 skill 是版本选择、目录导航和 pinned-source 引用的路由权威。按它的流程确定目标 MaaFramework 版本，选择 `generated/maa-framework/<version>/` 下对应的文档、binding、schema 或 native API 索引，再回到 pinned commit 指向的原始来源。不要用本节替代上游 skill 的完整规则。

Raw GitHub 不可用时，依次尝试同一相对路径的 jsDelivr 镜像和 MaaLLMWiki 根 README：

```text
https://cdn.jsdelivr.net/gh/Windsland52/MaaLLMWiki@main/skills/maallmwiki/SKILL.md
https://raw.githubusercontent.com/Windsland52/MaaLLMWiki/main/README.md
```

回退时说明实际使用的入口；`@main` 镜像可能有最长 12 小时缓存延迟，涉及结论时仍必须回源到 pinned commit。

## 本地集成规则

- 只有上游 skill 无法读取时才使用根 README 作为披露过的降级入口；此时理解 `sources/`、`generated/` 和 `schemas/` 的用途后再定位文件。
- 所有上游读取都是临时参考；不要把 catalog 内容或上游 skill 写进用户项目。

## 引用纪律

- catalog 索引只说明“去哪里找”，不能作为最终权威。
- 引用官方行为、schema、API 或语义变化时，必须附上原始来源 URL 或 revision。
- 只能贴必要片段，不要大规模复制上游内容。
- URL 不可达、路径不存在或 revision 不明确时，把相关事实标记为“未验证”，并说明缺少的来源，不得凭模型记忆补全。

## 与其它 Maa skill 协作

- `maa-workflow-build`：任务契约、设计或验收依赖官方事实时，通过 `$maa-wiki` 核对原始来源。
- `maa-pipeline-guide`、`maa-pipeline-testing`、`maa-project-create`：涉及官方协议、schema、API、版本或兼容性判断时，可先调用本 skill。
- 普通项目文件扫描、已有项目内 Pipeline 编辑等低风险工作不强制先读 wiki；按需引用，避免为每个任务增加网络依赖。

## 失败处理

- 网络不可用时，允许复用当前会话已读过的原始来源，但不得把未读取的 catalog 内容当成已知事实。
- 导航失败后先报告失败的 URL 和已确认的路径；再决定是否继续其它技能工作流。
- 无法验证官方事实时，明确列出未验证项和需要的原始来源，不代替用户完成核对。

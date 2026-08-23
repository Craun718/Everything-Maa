# Maa Pipeline Option

本目录包含 MaaFramework runtime UI option 设计指南。

## 包含内容

- `SKILL.md`: option 使用规范与案例说明
- `references/protocol.md`: option 与 pipeline_override 协议参考
- `adapters/maahub/skills/maa-pipeline-option.json`: MaaHub 发布元信息

## 说明

本 skill 说明如何在 MaaFramework 中新增 UI option，并确保主 Interface / import 的 option 声明、任务 option 注册、声明资源根内预定义 Pipeline 节点三处联动正确。

## 发现规则

- 从主 `interface.json` / `interface.jsonc` 及其 `import[]` 读取 option 与 task 声明。
- 从主 Interface 的 `resource[].path` 定位 Pipeline 与图片资源。
- `assets/...` 是 MaaPracticeBoilerplate 系项目的常见有效布局示例，但不能脱离主 Interface 声明猜测。

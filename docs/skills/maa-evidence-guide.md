# Maa Evidence Guide

为 MaaEvidenceKit 提供轻量入口。当用户提交 `maafw.log`、
`maafw.bak.<timestamp>.log`、其他 `maafw.*.log`，或要求使用 MLA/MSE 提取可追溯证据时，
该入口会先定位并完整读取上游 `maa-evidence` Skill，再把当前任务交给上游流程。

## 定位顺序

1. 用户明确提供的 Skill、MaaEvidenceKit checkout 或包路径。
2. 当前项目或用户环境中安装的 `maa-evidence` Skill。
3. 当前项目或 npm/pnpm 全局安装的 `maa-evidence-kit` 包内 Skill。
4. GitHub 上匹配包版本或最新正式 Release 的 Skill；默认分支仅作为最后回退。

本入口不会安装 MaaEvidenceKit、复制上游 Skill 内容或自行替代其证据与隐私规则。实现位于
`skills/maa-evidence-guide/SKILL.md`，只读定位器位于
`skills/maa-evidence-guide/scripts/find-maa-evidence-skill.mjs`。

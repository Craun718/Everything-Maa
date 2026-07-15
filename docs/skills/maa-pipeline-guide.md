# Maa Pipeline Guide

本目录包含 MaaFramework pipeline 编写与审查指南。

## 包含内容

- `SKILL.md`: guide 说明文档
- `adapters/maahub/skills/maa-pipeline-guide.json`: MaaHub 发布元信息

## 作用

本 skill 介绍如何编写高质量 pipeline JSON，包括节点命名、识别算法、动作类型、状态机控制、以及可复用模式。

## 适用场景

- 设计 MaaFramework pipeline 时参考规范
- 审查 pipeline 文件时验证流程和识别策略
- 避免常见的 `next` 死循环、硬延迟、ROI 设计错误

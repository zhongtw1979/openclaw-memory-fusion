# OpenClaw Memory Fusion Publishing Notes

## Project Summary

`OpenClaw Memory Fusion` is a GitHub-ready OpenClaw skill for unified memory management.
It keeps OpenClaw compatible with ordinary official releases by relying on workspace Markdown files, documented `memorySearch` settings, and rollback-friendly manifests instead of patching OpenClaw internals.

## Short Description

English:
OpenClaw Memory Fusion is an upgrade-safe OpenClaw memory system that combines native Markdown memory, project memory, structured event memory, alias-based project routing, and semantic retrieval.

中文：
OpenClaw Memory Fusion 是一套面向 OpenClaw 的升级兼容记忆系统，整合原生 Markdown 记忆、项目记忆、结构化事件记忆、别名路由和语义检索。

## Suggested GitHub Topics

- `openclaw`
- `openclaw-skill`
- `ai-agents`
- `memory-management`
- `markdown`
- `semantic-search`
- `knowledge-base`
- `project-management`
- `workflow-automation`
- `personal-ai`
- `llm-tools`
- `upgrade-safe`

## Release Notes v0.1.0

### English

- Added a unified memory layer for OpenClaw based on Markdown files.
- Added project memory split into `overview`, `timeline`, `decisions`, and `artifacts`.
- Added structured event memory with manifests and rollback checkpoints.
- Added `memorySearch` integration with broad official OpenClaw compatibility assumptions.
- Added a human-editable alias registry with force-priority routing.
- Added migration support for legacy `PROJECTS.md`, `improvements.md`, and older alias layouts.
- Added smoke tests and a local installer for GitHub distribution.

### 中文

- 增加了基于 Markdown 文件的 OpenClaw 统一记忆层。
- 增加了按项目拆分的记忆结构，包括 `overview`、`timeline`、`decisions` 和 `artifacts`。
- 增加了结构化事件记忆，并配套 manifest 和回滚检查点。
- 增加了 `memorySearch` 接入，并以“尽量兼容官方版本”为前提。
- 增加了可人工编辑的别名注册表，支持强制优先路由。
- 增加了对旧版 `PROJECTS.md`、`improvements.md` 和旧别名布局的迁移支持。
- 增加了适合 GitHub 分发的 smoke tests 和本地安装脚本。

## Compatibility Assumptions

- The target OpenClaw installation exposes documented `memorySearch` configuration fields and memory CLI commands.
- The target OpenClaw installation uses workspace Markdown memory files as a supported input path.
- The skill should still be useful even when semantic retrieval is not available, because the Markdown project and event layers remain functional.
- The project intentionally avoids patching OpenClaw internals, so upgrades should mainly affect configuration rather than code.

## Recommended Release Message

English:
`OpenClaw Memory Fusion v0.1.0` is the first public release of a unified OpenClaw memory skill. It focuses on broad compatibility, file-based memory, project routing, structured events, and safe migration.

中文：
`OpenClaw Memory Fusion v0.1.0` 是统一 OpenClaw 记忆技能的首个公开版本，重点提供广泛兼容、文件化记忆、项目路由、结构化事件和安全迁移能力。

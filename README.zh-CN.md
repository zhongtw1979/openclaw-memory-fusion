# OpenClaw Memory Fusion

`OpenClaw Memory Fusion` 是这套技能的正式显示名称；仓库名和安装路径继续保持为 `openclaw-memory-fusion`。

[English README](./README.md)

它整合了：
- OpenClaw 原生记忆文件，如 `MEMORY.md`、`PROJECTS.md`、`memory/YYYY-MM-DD.md`
- 按项目拆分的记忆目录 `projects/<slug>/`
- 结构化事件记忆 `memory_fusion/events/`
- 供 `memorySearch` 使用的语义摘要
- 旧版 `PROJECTS.md`、`improvements.md`、历史别名表的迁移能力

## 为什么它适合绝大多数官方 OpenClaw 版本

这套 skill 的兼容策略是“尽量只依赖官方公开能力”：
- 以工作区 Markdown 文件为事实源
- 只写入官方文档中的 `agents.defaults.memorySearch` 配置字段
- 不修改 OpenClaw 的 `dist/` 运行时代码
- 不依赖内部 SQLite 表结构
- 能把旧版 `projects/ALIASES.md` 迁移到不参与检索的 `memory_fusion/project_aliases.md`

兼容性基线：
- 本机存在 `openclaw.json`
- 官方 CLI 提供 `openclaw memory index`、`openclaw memory status`、`openclaw memory search`
- 当前 OpenClaw 版本支持 `memorySearch`

如果目标机器上的 OpenClaw 版本还不支持 `memorySearch`，这套 skill 的迁移、项目记忆、事件记忆依然可以工作，只是不会接入语义检索层。

## 仓库结构

```text
openclaw-memory-fusion/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── .gitignore
├── scripts/
│   └── install_local.py
├── tests/
│   └── test_smoke.py
├── .github/workflows/
│   └── python-tests.yml
└── skill/
    ├── SKILL.md
    ├── scripts/
    │   └── openclaw_memory_fusion.py
    └── templates/
```

## 安装方式

克隆仓库后，直接执行安装脚本，把 `skill/` 目录安装到本地技能目录：

```bash
python3 scripts/install_local.py
```

安装脚本默认会按以下顺序选择一个已存在的技能根目录：
- `$CODEX_HOME/skills`
- `~/.agents/skills`
- `~/.codex/skills`

你也可以显式指定安装位置：

```bash
python3 scripts/install_local.py --dest ~/.agents/skills/openclaw-memory-fusion --force
```

## 快速开始

安装后可以先执行这些命令：

```bash
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py doctor
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py install --apply --provider local
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py migrate --apply
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py sync-aliases --apply
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py upgrade-check
```

## 安全设计

- 所有会改文件的命令默认都是 dry-run，只有加 `--apply` 才会真正写入
- 每次变更都会在 `workspace/memory_fusion/manifests/` 下留下 manifest
- 回退数据会写到 `workspace/memory_fusion/checkpoints/`
- 项目路由支持 `Force aliases`，优先于普通启发式匹配
- 开源版默认把别名表放在 `memory_fusion/project_aliases.md`，避免它污染 `projects/` 检索排序

## 本地测试

仓库自带基于 Python 标准库的 smoke tests：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

这些测试会验证：
- 在临时工作区里跑通安装和迁移
- 旧版 `projects/ALIASES.md` 可以迁移到新位置
- `Force aliases` 的项目命中优先级正确

## 这个仓库不会包含什么

- 任何用户自己的工作区数据
- 任何 manifest、checkpoint、sqlite、jsonl 运行产物
- 任何 OpenClaw 二进制或内部补丁
- 任何 API key 或机器私有配置

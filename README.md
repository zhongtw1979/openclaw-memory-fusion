# OpenClaw Memory Fusion

`OpenClaw Memory Fusion` is a GitHub-ready OpenClaw skill package. The repository name and install path remain `openclaw-memory-fusion`.

[中文说明](./README.zh-CN.md)

It combines:
- native OpenClaw memory files like `MEMORY.md`, `PROJECTS.md`, and `memory/YYYY-MM-DD.md`
- per-project memory under `projects/<slug>/`
- structured event memory under `memory_fusion/events/`
- semantic digests for `memorySearch`
- legacy migration from older `PROJECTS.md`, `improvements.md`, and old alias layouts

## Why this should work on most official OpenClaw versions

This skill is packaged to stay compatible with the majority of normal official OpenClaw builds:
- it uses workspace Markdown as the source of truth
- it only writes documented `agents.defaults.memorySearch` config fields
- it does not patch OpenClaw `dist/` files or internal runtime code
- it does not depend on private SQLite schema details
- it can migrate the legacy `projects/ALIASES.md` registry into the non-indexed `memory_fusion/project_aliases.md` path

Compatibility baseline:
- `openclaw.json` exists
- the official CLI exposes `openclaw memory index`, `openclaw memory status`, and `openclaw memory search`
- `memorySearch` is supported by the installed OpenClaw version

If `memorySearch` is unavailable in a target version, the migration and file-based memory layers still work, but semantic retrieval integration will not.

## Repository layout

```text
openclaw-memory-fusion/
├── README.md
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

## Install

Clone the repository, then install the skill folder into your local skills directory:

```bash
python3 scripts/install_local.py
```

By default the installer prefers an existing skills root in this order:
- `$CODEX_HOME/skills`
- `~/.agents/skills`
- `~/.codex/skills`

You can also install to an explicit destination:

```bash
python3 scripts/install_local.py --dest ~/.agents/skills/openclaw-memory-fusion --force
```

## Quick start

After installation:

```bash
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py doctor
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py install --apply --provider local
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py migrate --apply
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py sync-aliases --apply
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py upgrade-check
```

## Safety model

- mutating commands are dry-run by default unless `--apply` is provided
- every mutating command writes a manifest under `workspace/memory_fusion/manifests/`
- rollback data is stored under `workspace/memory_fusion/checkpoints/`
- alias routing supports explicit `Force aliases` before heuristic matching
- the public package keeps the alias registry outside the indexed `projects/` tree to avoid retrieval pollution

## Test locally

The repository ships with Python stdlib smoke tests:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

These tests verify:
- installation and migration on a temporary workspace
- legacy alias migration from `projects/ALIASES.md`
- force alias matching behavior

## What this repo does not include

- generated workspace data
- user manifests or checkpoints
- any OpenClaw binary patches
- any private API keys or machine-specific configuration

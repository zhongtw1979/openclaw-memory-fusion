#!/usr/bin/env python3
import argparse
import os
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_SOURCE = REPO_ROOT / "skill"
SKILL_NAME = "openclaw-memory-fusion"


def default_destination() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    candidates = []
    if codex_home:
        candidates.append(Path(codex_home).expanduser() / "skills" / SKILL_NAME)
    candidates.append(Path.home() / ".agents" / "skills" / SKILL_NAME)
    candidates.append(Path.home() / ".codex" / "skills" / SKILL_NAME)
    for candidate in candidates:
        if candidate.parent.exists():
            return candidate
    return candidates[0]


def install(dest: Path, force: bool, dry_run: bool) -> dict:
    if not SKILL_SOURCE.exists():
        raise SystemExit(f"Skill source not found: {SKILL_SOURCE}")
    existed_before = dest.exists()
    if dest.exists():
        if not force and not dry_run:
            raise SystemExit(f"Destination already exists: {dest}. Use --force to replace it.")
        if not dry_run:
            shutil.rmtree(dest)
    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(SKILL_SOURCE, dest)
    return {
        "installed": not dry_run,
        "dry_run": dry_run,
        "source": str(SKILL_SOURCE),
        "destination": str(dest),
        "force": force,
        "destination_exists": existed_before,
        "would_replace": existed_before,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the openclaw-memory-fusion skill locally.")
    parser.add_argument("--dest", help="Explicit destination directory for the installed skill.")
    parser.add_argument("--force", action="store_true", help="Replace an existing destination.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without copying files.")
    args = parser.parse_args()

    destination = Path(args.dest).expanduser() if args.dest else default_destination()
    result = install(destination, force=args.force, dry_run=args.dry_run)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

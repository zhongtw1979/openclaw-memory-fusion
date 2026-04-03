import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "skill" / "scripts" / "openclaw_memory_fusion.py"


def load_module():
    spec = importlib.util.spec_from_file_location("openclaw_memory_fusion", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run_cli(*args: str) -> dict:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def write_fixture_workspace(workspace: Path, config_path: Path) -> None:
    (workspace / "memory").mkdir(parents=True, exist_ok=True)
    (workspace / "MEMORY.md").write_text("# Long-term Memory\n\n- User prefers concise summaries.\n", encoding="utf-8")
    (workspace / "improvements.md").write_text("# Improvements\n\n- Reduce retrieval noise.\n", encoding="utf-8")
    (workspace / "memory" / "improvements.md").write_text("# Improvement History\n\n- Added rollback manifests.\n", encoding="utf-8")
    (workspace / "PROJECTS.md").write_text(
        "# Projects\n\n"
        "## ACME CRM migration\n\n"
        "- Goal: Complete the migration\n"
        "- Status: Data validation in progress\n"
        "- Next Step: Run the final cutover checklist\n\n"
        "## Northwind analytics pilot\n\n"
        "- Goal: Complete the pilot report\n"
        "- Status: Prototype review in progress\n"
        "- Next Step: Finalize the executive summary\n",
        encoding="utf-8",
    )
    (workspace / "memory" / "2026-04-01.md").write_text(
        "# 2026-04-01 工作记忆\n\n"
        "## CRM migration\n\n"
        "- Today: Run the cutover checklist\n"
        "- Note: The integration vendor confirmed the final test dataset\n\n"
        "## Analytics pilot\n\n"
        "- Status: Prototype review in progress\n"
        "- Next step: Finalize the pilot report\n",
        encoding="utf-8",
    )
    config_path.write_text(json.dumps({"agents": {"defaults": {}}}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class SmokeTests(unittest.TestCase):
    def test_install_migrate_and_doctor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            config_path = root / "openclaw.json"
            write_fixture_workspace(workspace, config_path)

            install = run_cli("install", "--apply", "--workspace", str(workspace), "--config", str(config_path), "--provider", "local")
            self.assertTrue(install["installed"])

            migrate = run_cli("migrate", "--apply", "--overwrite", "--workspace", str(workspace), "--config", str(config_path))
            self.assertTrue(migrate["migrated"])

            sync_aliases = run_cli("sync-aliases", "--apply", "--workspace", str(workspace), "--config", str(config_path))
            self.assertTrue(sync_aliases["synced"])

            doctor = run_cli("doctor", "--workspace", str(workspace), "--config", str(config_path))
            self.assertTrue(doctor["files"]["project_aliases"])
            self.assertFalse(doctor["files"]["legacy_project_aliases"])
            self.assertTrue(doctor["memory_search"]["enabled"])

    def test_sync_aliases_migrates_legacy_registry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            config_path = root / "openclaw.json"
            write_fixture_workspace(workspace, config_path)
            run_cli("migrate", "--apply", "--overwrite", "--workspace", str(workspace), "--config", str(config_path))
            (workspace / "projects" / "ALIASES.md").write_text(
                "# Project Aliases\n\n"
                "## acme-crm-migration\n"
                "- Title: ACME CRM migration\n"
                "- Aliases:\n"
                "  - crm-go-live\n",
                encoding="utf-8",
            )
            result = run_cli("sync-aliases", "--apply", "--workspace", str(workspace), "--config", str(config_path))

            self.assertTrue(result["removed_legacy_alias"])
            self.assertTrue((workspace / "memory_fusion" / "project_aliases.md").exists())
            self.assertFalse((workspace / "projects" / "ALIASES.md").exists())
            content = (workspace / "memory_fusion" / "project_aliases.md").read_text(encoding="utf-8")
            self.assertIn("crm-go-live", content)
            self.assertIn("Force aliases", content)

    def test_force_aliases_drive_matching(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            config_path = root / "openclaw.json"
            write_fixture_workspace(workspace, config_path)

            run_cli("migrate", "--apply", "--overwrite", "--workspace", str(workspace), "--config", str(config_path))
            run_cli("sync-aliases", "--apply", "--workspace", str(workspace), "--config", str(config_path))

            alias_file = workspace / "memory_fusion" / "project_aliases.md"
            alias_file.write_text(
                "# Project Aliases\n\n"
                "- Generated at: 2026-04-03T00:00:00\n"
                "- Edit this file by hand when you want to force specific phrases to map to a project.\n"
                "- `Force aliases` win before heuristic matching.\n"
                "- `sync-aliases` will preserve existing force aliases and refresh suggested aliases.\n\n"
                "## acme-crm-migration\n"
                "- Title: ACME CRM migration\n"
                "- Force aliases:\n"
                "  - crm-go-live\n"
                "- Suggested aliases:\n"
                "  - ACME CRM\n\n"
                "## northwind-analytics-pilot\n"
                "- Title: Northwind analytics pilot\n"
                "- Force aliases:\n"
                "  - analytics-review\n"
                "- Suggested aliases:\n"
                "  - Northwind analytics\n",
                encoding="utf-8",
            )

            layout = module.Layout(workspace, config_path)
            catalog = module.load_project_catalog(layout)
            matched = module.match_project(layout, "crm-go-live", "", catalog)
            self.assertIsNotNone(matched)
            self.assertEqual(matched["title"], "ACME CRM migration")


if __name__ == "__main__":
    unittest.main()

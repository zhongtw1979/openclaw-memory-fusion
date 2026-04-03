# Release Checklist

- Confirm `git status --short` is clean before tagging or publishing.
- Keep the first public commit limited to repo files under `README*`, `LICENSE`, `.gitignore`, `scripts/`, `skill/`, `tests/`, and `.github/workflows/`.
- Do not publish workspace artifacts, manifests, checkpoints, sqlite files, or API keys.
- Verify `python3 -m unittest discover -s tests -p 'test_*.py'` passes locally.
- Verify `python3 scripts/install_local.py --dry-run` succeeds on a fresh machine or temp path.
- Tag the first public release after the initial import, for example `v0.1.0`.
- If you add compatibility fixes later, keep them backward-compatible and preserve rollback paths.


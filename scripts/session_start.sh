#!/usr/bin/env bash
# Runs at every Claude Code session start (local and web). Idempotent and quiet.
# stdout becomes context for Claude, so keep it to a short status line.
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/..}" || exit 0

# 1. Git hooks are not part of a clone: point git at the versioned hooks folder.
git config core.hooksPath .githooks 2>/dev/null

# 2. Python runs only through uv. Create/refresh .venv from uv.lock.
if ! command -v uv >/dev/null 2>&1; then
  echo "[kb] uv is not installed - kb.py, the commit hook and /ingest will not work. Install uv: https://docs.astral.sh/uv/getting-started/installation/"
  exit 0
fi
if ! uv sync --quiet --locked >/dev/null 2>&1; then
  echo "[kb] 'uv sync --locked' failed (uv.lock out of date or no network). Run 'uv sync' and check."
fi

# 3. Register any new raw files and print a one-line status.
uv run --quiet scripts/kb.py register >/dev/null 2>&1 || true
uv run --quiet scripts/kb.py status 2>/dev/null || true
exit 0

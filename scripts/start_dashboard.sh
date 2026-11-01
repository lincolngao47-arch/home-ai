#!/usr/bin/env bash
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="${HOME_AI_PYTHON:-$PROJECT_DIR/.venv/bin/python}"
[[ -x "$PYTHON_BIN" ]] || { echo 'Run bash scripts/install.sh first, or set HOME_AI_PYTHON.'; exit 1; }
exec "$PYTHON_BIN" "$PROJECT_DIR/dashboard/dashboard_server.py"

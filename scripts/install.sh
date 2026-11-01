#!/usr/bin/env bash
# Install the hub; --with-chat also installs Open WebUI in its own environment.
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
case "${1:-}" in --help|-h) echo 'Usage: bash scripts/install.sh [--with-chat]'; exit 0;; ''|--with-chat) ;; *) echo 'Unknown option'; exit 2;; esac
PYTHON_BIN="${HOME_AI_PYTHON:-}"
if [[ -z "$PYTHON_BIN" ]]; then
  for candidate in python3.11 python3.12 python3; do
    if command -v "$candidate" >/dev/null && "$candidate" -c 'import sys;sys.exit(not ((3,11) <= sys.version_info[:2] <= (3,12)))' 2>/dev/null; then
      PYTHON_BIN="$candidate"; break
    fi
  done
fi
[[ -n "$PYTHON_BIN" ]] || { echo 'Install Python 3.11 or 3.12 from python.org, or set HOME_AI_PYTHON to its executable.'; exit 1; }
"$PYTHON_BIN" -c 'import sys;sys.exit(not ((3,11) <= sys.version_info[:2] <= (3,12)))' || { echo 'Python 3.11 or 3.12 is required.'; exit 1; }
"$PYTHON_BIN" -m venv "$PROJECT_DIR/.venv"
"$PROJECT_DIR/.venv/bin/python" -m pip install -r "$PROJECT_DIR/dashboard/requirements.txt"
if [[ "${1:-}" = --with-chat ]]; then
  "$PYTHON_BIN" -m venv "$PROJECT_DIR/.webui-venv"
  "$PROJECT_DIR/.webui-venv/bin/python" -m pip install 'open-webui==0.12.3'
fi
printf '\nInstalled. Start the hub: bash scripts/start_dashboard.sh\n'
if [[ "${1:-}" = --with-chat ]]; then
  echo 'Start chat in another terminal: bash scripts/start_chat.sh'
  echo 'Install Ollama from https://ollama.com/download and download a model suited to your memory.'
fi

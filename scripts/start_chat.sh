#!/usr/bin/env bash
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WEBUI_BIN="${HOME_AI_WEBUI_BIN:-$PROJECT_DIR/.webui-venv/bin/open-webui}"
[[ -x "$WEBUI_BIN" ]] || { echo 'Run bash scripts/install.sh --with-chat first.'; exit 1; }
export DATA_DIR="${DATA_DIR:-$PROJECT_DIR/open-webui-data}"
export OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://127.0.0.1:11434}"
export WEBUI_AUTH=true DEFAULT_USER_ROLE=pending
# Initial signup is needed to create the first administrator; approve later users in WebUI.
export ENABLE_SIGNUP="${ENABLE_SIGNUP:-true}"
export NO_PROXY="127.0.0.1,localhost"
# Avoid macOS's inherited 256-file soft limit during a full frontend load.
CURRENT_FILES=$(ulimit -Sn)
HARD_FILES=$(ulimit -Hn)
if [[ "$CURRENT_FILES" != unlimited && "$CURRENT_FILES" -lt 8192 ]]; then
    TARGET_FILES=8192
    if [[ "$HARD_FILES" != unlimited && "$HARD_FILES" -lt "$TARGET_FILES" ]]; then
        TARGET_FILES="$HARD_FILES"
    fi
    ulimit -Sn "$TARGET_FILES"
fi
mkdir -p "$DATA_DIR"
exec "$WEBUI_BIN" serve --host "${WEBUI_HOST:-127.0.0.1}" --port 3000

#!/usr/bin/env bash
set -uo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
FAILED=0
for service in open_webui ollama whisper; do
  bash "$PROJECT_DIR/scripts/service_control.sh" "$service" stop || FAILED=1
done
if command -v docker >/dev/null && docker container inspect n8n >/dev/null 2>&1; then
  bash "$PROJECT_DIR/scripts/service_control.sh" n8n stop || FAILED=1
fi
echo 'AI services stopped. The hub remains available for maintenance.'
exit "$FAILED"

#!/usr/bin/env bash
# Existing Mac mini stack. Optional services are started only when already installed.
set -uo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
export PATH="$PROJECT_DIR/.venv/bin:$PROJECT_DIR/.webui-venv/bin:/opt/anaconda3/envs/webui/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
FAILED=0
for service in ollama open_webui; do
  if ! bash "$PROJECT_DIR/scripts/service_control.sh" "$service" start; then echo "$service failed; check .home-ai/service-control.log"; FAILED=1; fi
done
if command -v docker >/dev/null && docker container inspect n8n >/dev/null 2>&1; then
  bash "$PROJECT_DIR/scripts/service_control.sh" n8n start || FAILED=1
fi
if [[ -f "$PROJECT_DIR/whisper/whisper_server.py" ]]; then
  bash "$PROJECT_DIR/scripts/service_control.sh" whisper start || FAILED=1
fi
if ! curl --noproxy '*' -fsS --max-time 2 http://127.0.0.1:8088/health >/dev/null; then
  PYTHON_BIN="${HOME_AI_PYTHON:-$(command -v python)}"
  nohup "$PYTHON_BIN" "$PROJECT_DIR/dashboard/dashboard_server.py" > "$PROJECT_DIR/dashboard/dashboard.log" 2>&1 < /dev/null &
fi
echo 'Home AI: http://127.0.0.1:8088 — Open WebUI: http://127.0.0.1:3000'
exit "$FAILED"

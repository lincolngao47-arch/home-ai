#!/usr/bin/env bash
# Single-service native macOS controls; never stop the dashboard itself.
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
export PATH="$PROJECT_DIR/.venv/bin:$PROJECT_DIR/.webui-venv/bin:/opt/anaconda3/envs/webui/bin:/opt/homebrew/bin:/usr/local/bin:/Applications/Ollama.app/Contents/Resources:$PATH"
export NO_PROXY='127.0.0.1,localhost'
SERVICE="${1:-}"; ACTION="${2:-}"
case "$SERVICE" in open_webui|ollama|n8n|whisper) ;; *) echo 'Unknown service'; exit 2;; esac
case "$ACTION" in start|stop|restart) ;; *) echo 'Unknown action'; exit 2;; esac
mkdir -p "$PROJECT_DIR/.home-ai"
exec >> "$PROJECT_DIR/.home-ai/service-control.log" 2>&1
printf '\n%s %s %s\n' "$(date -u)" "$SERVICE" "$ACTION"
if [[ "$ACTION" = stop || "$ACTION" = restart ]]; then
  case "$SERVICE" in
    open_webui) pkill -f '[o]pen-webui serve' || true;;
    ollama) pkill -x Ollama || true; pkill -f '[o]llama serve' || true;;
    n8n) docker stop n8n;;
    whisper) pkill -f '[w]hisper_server.py' || true;;
  esac
  sleep 2
fi
if [[ "$ACTION" = start || "$ACTION" = restart ]]; then
  case "$SERVICE" in
    open_webui)
      if ! pgrep -f '[o]pen-webui serve' >/dev/null; then
        export DATA_DIR="$PROJECT_DIR/open-webui-data"
        export OLLAMA_BASE_URL="http://127.0.0.1:11434" WEBUI_AUTH=true DEFAULT_USER_ROLE=pending
        export ENABLE_SIGNUP=false
        mkdir -p "$DATA_DIR"
        # Prefer the existing installation over the dashboard-only virtualenv.
        WEBUI_BIN="${HOME_AI_WEBUI_BIN:-$(command -v open-webui)}"
        nohup "$WEBUI_BIN" serve --port 3000 --host "${WEBUI_HOST:-127.0.0.1}" > "$DATA_DIR/open-webui.log" 2>&1 < /dev/null &
      fi
      URL=http://127.0.0.1:3000/health;;
    ollama)
      launchctl setenv OLLAMA_HOST '127.0.0.1:11434'
      launchctl setenv OLLAMA_ORIGINS 'http://localhost,http://127.0.0.1'
      open -a Ollama
      URL=http://127.0.0.1:11434/api/tags;;
    n8n)
      docker start n8n
      URL=http://127.0.0.1:5680/healthz;;
    whisper)
      if ! pgrep -f '[w]hisper_server.py' >/dev/null; then
        PYTHON_BIN="${HOME_AI_WHISPER_PYTHON:-/opt/anaconda3/envs/webui/bin/python}"
        nohup "$PYTHON_BIN" "$PROJECT_DIR/whisper/whisper_server.py" > "$PROJECT_DIR/whisper/server.log" 2>&1 < /dev/null &
      fi
      URL=http://127.0.0.1:8000/health;;
  esac
  for attempt in {1..20}; do
    if curl --noproxy '*' -fsS --max-time 2 "$URL" > /dev/null; then exit 0; fi
    sleep 2
  done
  echo 'Service did not become healthy within the startup window.'; exit 1
fi

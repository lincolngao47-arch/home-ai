#!/usr/bin/env bash
set -uo pipefail
FAILED=0
for entry in 'Home-AI:8088/health' 'Open-WebUI:3000/health' 'Ollama:11434/api/tags'; do
  NAME="${entry%%:*}"; ENDPOINT="${entry#*:}"
  if curl --noproxy '*' -fsS --max-time 5 "http://127.0.0.1:$ENDPOINT" > /dev/null; then
    echo "$NAME: online"
  else echo "$NAME: offline"; FAILED=1; fi
done
exit "$FAILED"

#!/usr/bin/env bash
# Serve only chat and the hub to your private tailnet. Never enable Funnel.
set -euo pipefail
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
command -v tailscale >/dev/null || { echo 'Install Tailscale: https://tailscale.com/download'; exit 1; }
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="${HOME_AI_PYTHON:-$PROJECT_DIR/.venv/bin/python}"
[[ -x "$PYTHON_BIN" ]] || PYTHON_BIN=/opt/anaconda3/envs/webui/bin/python
[[ -x "$PYTHON_BIN" ]] || PYTHON_BIN=python3
if ! STATE=$(tailscale status --json | "$PYTHON_BIN" -c '
import json,sys
try:
    print(json.load(sys.stdin).get("BackendState","Unknown"))
except (ValueError, TypeError):
    sys.exit("Tailscale could not report its state. Open its app and check the VPN connection. If it is stuck after an update, restart the Mac when convenient.")
'); then
    exit 1
fi
[[ "$STATE" = Running ]] || { echo "Tailscale state: $STATE. Open Tailscale and sign in, then run this script again."; exit 1; }
# Do not overwrite unrelated existing Serve routes.
tailscale serve status --json | "$PYTHON_BIN" -c '
import json,sys
config=json.load(sys.stdin)
for host, entry in config.get("Web",{}).items():
    port=host.rsplit(":",1)[-1]
    target={"443":"http://127.0.0.1:3000","8443":"http://127.0.0.1:8088"}.get(port)
    if target and entry.get("Handlers") != {"/":{"Proxy":target}}:
        sys.exit("Existing Serve configuration uses port " + port + ". Resolve that conflict before running setup.")
if config.get("AllowFunnel") and any(config["AllowFunnel"].values()):
    sys.exit("Funnel is already enabled. Review public access before configuring this private server.")
'
tailscale serve --bg --https=443 http://127.0.0.1:3000
tailscale serve --bg --https=8443 http://127.0.0.1:8088
tailscale serve status

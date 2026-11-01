# Home AI

A small, bilingual home page for your private AI server. Open chat, see which services are running, check your models, and connect your devices through Tailscale.

**Status: early preview.** Built and exercised on an Apple Silicon Mac with an existing Ollama + Open WebUI installation. The dashboard also runs on Linux; native service controls are macOS-only. Phones, tablets, Windows PCs, and Macs use the same responsive web interface.

[中文安装指南](docs/SETUP.zh-CN.md) · [Architecture](docs/ARCHITECTURE.md) · [Security](docs/SECURITY.md) · [Alternatives](docs/ALTERNATIVES.md) · [Validation](docs/VALIDATION.md) · [Fast models and measurements](docs/PERFORMANCE.md)

## What you get

- A responsive home page with English / 中文, light / dark / system themes, keyboard navigation, and mobile zoom.
- Actual service health and installed / loaded Ollama models; optional services can be offline without marking chat as broken.
- CPU, memory, disk space, and uptime from the host.
- Private HTTPS setup using Tailscale Serve, with no router port forwarding.
- Admin-key-protected macOS service controls with confirmation, validated inputs, and explicit failures.
- An explicit source-export allowlist that excludes conversations, account databases, keys, media, and logs.

Home AI is a companion to **Open WebUI**, not a replacement chat engine. Account permissions, document retrieval, conversation history, and chat sign-in remain in Open WebUI. Its branding and license are retained.

## Quick start: existing AI server

Install Python **3.11 or 3.12**, then clone this repository (or download its ZIP from GitHub):

```bash
git clone https://github.com/lincolngao47-arch/home-ai.git
cd home-ai
bash scripts/install.sh
bash scripts/start_dashboard.sh
```

Open **http://127.0.0.1:8088**. The dashboard expects:

| Service | Default address | Needed for chat? |
| --- | --- | --- |
| Open WebUI | `http://127.0.0.1:3000` | Yes |
| Ollama | `http://127.0.0.1:11434` | Yes |
| n8n | `http://127.0.0.1:5680` | No |
| Whisper | `http://127.0.0.1:8000` | No |

The installer creates an isolated dashboard environment. It does not alter existing chat data or install models. Leave the terminal running; `Ctrl+C` stops the dashboard.

## Starting from scratch

1. Install [Ollama](https://ollama.com/download) and Python 3.11 / 3.12. Start Ollama, then use its app or `ollama pull MODEL_NAME` to download a model suited to your hardware. Model weights can require many gigabytes; there is no automatic download.
2. Run `bash scripts/install.sh --with-chat`. This also installs Open WebUI 0.12.3 in a separate environment. Package downloads require internet access and may take several minutes.
3. Run `bash scripts/start_chat.sh`, open http://127.0.0.1:3000, and create the first administrator **before sharing access**. Later signups default to pending approval; review Open WebUI’s persistent signup settings in its admin panel.
4. In a second terminal, run `bash scripts/start_dashboard.sh`.
5. Add private remote access below.

These scripts support macOS and Linux. Windows users can use WSL2 for the server, or connect by browser to a server on another machine. A clean-machine installation and Windows / Linux end-to-end operation still need community testing. Optional n8n / Whisper are not installed by this starter.

## Start after login on macOS

Once the hub and chat have run successfully, install user login agents:

```bash
.venv/bin/python scripts/install_autostart.py --chat
```

The hub and native Open WebUI start after login and restart if they exit. Login agents use an 8,192-file soft limit so concurrent frontend downloads do not hit macOS’s default 256-file limit. For an existing Open WebUI installation, set `HOME_AI_WEBUI_BIN` to its executable. Add `--offline` only after its embedding model has been downloaded and cached. Repeating the installer preserves already-matching running jobs. Logs and previous agent configurations are saved under `.home-ai/`.

For the optional legacy Whisper server, `--whisper` additionally requires `whisper/whisper_server.py` and `HOME_AI_WHISPER_PYTHON` pointing to its existing environment. It does not install Whisper. If n8n uses Colima, arrange for Colima to start after login; an existing n8n container with a restart policy resumes when Docker starts.

These are login agents: they need a logged-in macOS user. On Linux, use an appropriate process manager.

## Make everyday chat faster

With Ollama running, download two small models (about 6 GB):

```bash
.venv/bin/python scripts/install_fast_models.py
```

The hub’s main button then opens `home-fast`, a Qwen 4B instruct model for quick text chat. Choose `home-vision` for images. Both use a 16K context with up to 2K reply tokens, and the larger models stay available. The hub’s model links override a browser’s old model selection.

On the development Mac, a greeting began showing text in about 2.1 seconds cold and 0.12 seconds warm through Open WebUI, versus about 14 seconds cold for the previous 27B default. These are individual local measurements; phone/network latency and task complexity vary. See [settings, tradeoffs, and reproduction](docs/PERFORMANCE.md).

## Optional chat UI polish

To apply the restrained chat stylesheet and remove the legacy floating guide controls, use the environment that contains Open WebUI:

```bash
.webui-venv/bin/python scripts/install_webui_polish.py
```

The helper backs up the affected assets, updates both the served and startup-copy source files, and versions their URLs so a reloaded phone page receives the changes. It preserves Open WebUI’s layout and branding. Reapply it after an Open WebUI package upgrade. Existing installations should use their own Open WebUI Python interpreter.

Keep instance system instructions concise; a full installation guide should not be sent with every greeting. If an older model profile explicitly specifies a 4K context, update it to 16,384 and set its reply budget to 2,048 in Open WebUI, or remove that override so the alias defaults apply.

## Access from another device

Install [Tailscale](https://tailscale.com/download) on the server and each client device. Sign in to your private network, then run:

```bash
bash scripts/setup_tailscale.sh
```

Tailscale may ask you to enable HTTPS in its admin console. Complete that step and rerun the command. The script sets up:

- `https://YOUR-SERVER.YOUR-TAILNET.ts.net` → Open WebUI, port 3000
- `https://YOUR-SERVER.YOUR-TAILNET.ts.net:8443` → Home AI, port 8088

It checks for conflicting Serve routes and never enables Funnel. Access is governed by your tailnet policy; membership alone is not a substitute for narrow grants when sharing with others. Open WebUI still requires its own sign-in. Raw Ollama, n8n, and Whisper are not published by this script.

If Tailscale reports a control-plane timeout, fix its connection and rerun the script. The hub only labels HTTPS ready after matching Serve routes exist. Test from a second device on cellular data before relying on access away from home. See [Tailscale Serve documentation](https://tailscale.com/docs/features/tailscale-serve).

## Maintenance and configuration

Read `.home-ai/admin-token` on the server and enter it in **Maintenance**. The key stays only in the current tab’s memory. Lock or reload to clear it. The file is created with owner-only permissions. Do not send the key to other people or commit it to Git.

Service controls are designed for a dedicated Mac with the native Ollama app, native Open WebUI, and optionally an existing Docker container named `n8n` and the legacy Whisper server. Stopping a service affects its users. The hub itself stays available. Use a process manager appropriate to your OS for unattended operation.

| Environment variable | Purpose |
| --- | --- |
| `HOME_AI_PYTHON` | Python executable used by setup / launch scripts |
| `DASHBOARD_HOST` | Listen address; default `127.0.0.1` |
| `DASHBOARD_PORT` | Hub port; default `8088` |
| `WEBUI_URL`, `OLLAMA_URL`, `N8N_URL`, `WHISPER_URL` | Backend health / model endpoints |
| `HOME_AI_STATE_DIR` | Location of the generated admin key |
| `HOME_AI_CONTROLS=false` | Disable service controls |
| `HOME_AI_WEBUI_BIN` | Existing native `open-webui` executable for controls |
| `HOME_AI_WHISPER_PYTHON` | Python environment containing the optional Whisper dependencies |

The Tailscale setup script uses standard ports 3000 and 8088. Custom backend endpoints are for health polling; browser links assume services on the same server and their configured ports. If using external hosts or a different reverse proxy, adapt the links and Serve routes before sharing.

## Development

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install -r dashboard/requirements.txt
.venv/bin/python -m unittest discover -s tests -v
node --check dashboard/app.js
bash scripts/check_health.sh
.venv/bin/python scripts/export_source.py
```

The export is `release/home-ai-source.zip`. Always distribute this source package or a clean repository created from it, **not a copy of your live AI directory**. See [security boundaries](docs/SECURITY.md).

Contributions that improve installation, accessibility, localization, and real-device testing are welcome. Report platform, Python version, expected behavior, and a redacted error. Never attach databases, admin keys, or private conversations.

## Why this project?

Its niche is an approachable front door for a household AI server, with private remote access and useful operational status. It is not trying to outbuild established chat applications. Whether it finds an audience needs real user feedback; no popularity claim is implied.

Home AI source is MIT licensed. Third-party software keeps its own license; this repository does not redistribute Open WebUI, Ollama, n8n, or model weights.

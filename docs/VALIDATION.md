# Preview validation

Checked on 2026-11-01 on macOS / Apple Silicon:

- Installed dashboard dependencies into a new Python 3.11 virtual environment using `scripts/install.sh`.
- Ten backend tests passed in both the existing environment and the new isolated environment: authentication, invalid actions, disabled controls, command failures, key persistence / permissions, removed account routes, static assets / headers, Tailscale route detection, and failed health checks.
- JavaScript syntax and shell-script syntax checks passed.
- Live integration reported Open WebUI, Ollama, n8n, and Whisper online, and retrieved the installed model list from Ollama.
- Browser checks covered English / Chinese, light / dark themes, invalid maintenance-key feedback, and responsive layouts. A narrow-screen metrics overflow was found and corrected.

Known limits:

- Tailscale sign-in succeeded on the development host, but Serve setup hit a control-plane timeout. Its network diagnostic found no responding relay. Private HTTPS and an off-LAN phone connection are **not yet verified** there.
- A complete new Open WebUI / model installation was not exercised; existing chat and model services were retained.
- No destructive stop/restart actions were run against active AI services during verification. Action validation and failure behavior were tested with isolated test doubles.
- Linux / Windows / WSL2 server operation and physical iOS / Android devices require further testing. Responsive browser emulation is not a substitute for those tests.
- No full WCAG conformance audit has been performed. The hub provides zoom support, keyboard focus states, labeled inputs, native dialogs, reduced-motion behavior, and text status indicators.

This is an early preview, not a claim of production readiness across all platforms.

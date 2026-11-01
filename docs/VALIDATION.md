# Preview validation

Checked on 2026-11-01 on macOS / Apple Silicon:

- Installed dashboard dependencies into a new Python 3.11 virtual environment using `scripts/install.sh`.
- Ten backend tests passed in both the existing environment and the new isolated environment: authentication, invalid actions, disabled controls, command failures, key persistence / permissions, removed account routes, static assets / headers, Tailscale route detection, and failed health checks.
- JavaScript syntax and shell-script syntax checks passed.
- Live integration reported Open WebUI, Ollama, n8n, and Whisper online, and retrieved the installed model list from Ollama.
- Browser checks covered English / Chinese, light / dark themes, invalid maintenance-key feedback, and responsive layouts. A narrow-screen metrics overflow was found and corrected.

Known limits:

- After a macOS restart cleared an obsolete Tailscale extension, private Serve routes for chat and the hub passed HTTPS health checks with certificate verification. A maintenance request through HTTPS without an admin key returned 401. A physical off-LAN phone test remains separate from these same-host checks.
- A complete new Open WebUI / model installation was not exercised; existing chat and model services were retained.
- Small Qwen and Gemma models were downloaded and exposed through tuned aliases. The Qwen profile was exercised through Open WebUI’s streaming endpoint; greeting timings are recorded in PERFORMANCE.md. The Gemma profile correctly identified a synthetic red PNG through the same endpoint (about 2.1 seconds to first visible text for that one image test).
- After the reboot exposed an unreliable detached startup process, chat and Whisper were placed under macOS login-agent supervision. A controlled Open WebUI restart passed health checks and remained online after its controller exited. The existing n8n container resumed with its restart policy after Colima was enabled as a login service. No conversation or account data was removed.
- Linux / Windows / WSL2 server operation and physical iOS / Android devices require further testing. Responsive browser emulation is not a substitute for those tests.
- No full WCAG conformance audit has been performed. The hub provides zoom support, keyboard focus states, labeled inputs, native dialogs, reduced-motion behavior, and text status indicators.

This is an early preview, not a claim of production readiness across all platforms.

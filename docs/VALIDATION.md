# Preview validation

Checked on 2026-11-01 on macOS / Apple Silicon:

- Installed dashboard dependencies into a new Python 3.11 virtual environment using `scripts/install.sh`.
- Ten backend tests passed in both the existing environment and the new isolated environment: authentication, invalid actions, disabled controls, command failures, key persistence / permissions, removed account routes, static assets / headers, Tailscale route detection, and failed health checks.
- JavaScript syntax and shell-script syntax checks passed. Three additional launcher tests verify raising a low inherited file limit, respecting a lower hard limit, and preserving an already-higher limit (13 tests total).
- Live integration reported Open WebUI, Ollama, n8n, and Whisper online, and retrieved the installed model list from Ollama.
- Browser checks covered English / Chinese, light / dark themes, invalid maintenance-key feedback, and responsive layouts. A narrow-screen metrics overflow was found and corrected.

A physical phone’s first chat-page load exposed macOS’s inherited 256-file limit, causing JavaScript downloads to fail with `Too many open files`. The login agents now set an 8,192-file soft limit and a 16,384-file hard limit; the terminal chat launcher also raises its soft limit where permitted. A subsequent HTTPS test downloaded all 850 frontend JS/CSS assets with 128 concurrent requests, verified their contents, and recorded zero failures and zero new open-file errors.

Known limits:

- After a macOS restart cleared an obsolete Tailscale extension, private Serve routes for chat and the hub passed HTTPS health checks with certificate verification. A maintenance request through HTTPS without an admin key returned 401. The user subsequently confirmed that the phone page loaded normally after installing Tailscale and applying the open-file limit fix. Phone response latency has not been measured.
- A complete new Open WebUI / model installation was not exercised; existing chat and model services were retained.
- Small Qwen and Gemma models were downloaded and exposed through tuned aliases. The Qwen profile was exercised through Open WebUI’s streaming endpoint; greeting timings are recorded in PERFORMANCE.md. The Gemma profile correctly identified a synthetic red PNG through the same endpoint (about 2.1 seconds to first visible text for that one image test).
- After the reboot exposed an unreliable detached startup process, chat and Whisper were placed under macOS login-agent supervision. A controlled Open WebUI restart passed health checks and remained online after its controller exited. The existing n8n container resumed with its restart policy after Colima was enabled as a login service. No conversation or account data was removed.
- Linux / Windows / WSL2 server operation and physical iOS / Android devices require further testing. Responsive browser emulation is not a substitute for those tests.
- No full WCAG conformance audit has been performed. The hub provides zoom support, keyboard focus states, labeled inputs, native dialogs, reduced-motion behavior, and text status indicators.

This is an early preview, not a claim of production readiness across all platforms.

# Security boundaries

- Default hub binding is loopback. Use private Tailscale Serve for remote access; do not enable Funnel or router port forwarding for this stack.
- Read-only status is visible to anyone who can reach the hub. It includes host / model metadata. Limit tailnet grants when adding other people.
- Every mutating endpoint requires the admin key, including loopback and proxied requests. No wildcard CORS policy is enabled. Responses restrict scripts and framing.
- Admin keys are generated randomly and stored with mode 0600 under `.home-ai/`. The browser keeps the key only in tab memory. Rotate it by stopping the hub, replacing the file with a new cryptographically random value of at least 32 characters, and restarting. No keys appear in URLs.
- Use localhost or HTTPS for maintenance. Do not enter admin credentials into a plain-HTTP LAN connection.
- Open WebUI owns login, accounts, passwords, and document permissions. Create its initial administrator locally before connecting other users. Inspect existing persistent signup settings rather than assuming environment defaults override them.
- The Tailscale script configures only chat and the hub. It does not close ports already exposed by older Ollama, Whisper, or Docker installations. Audit existing bindings separately; adopting this hub does not automatically isolate legacy services.
- Models are local only when your upstream model/provider settings are local. Selecting cloud providers, external tools, web search, or remote document integrations can send data outside the machine.
- A generated source ZIP includes only explicitly listed files. Do not publish the live working directory, backups, account databases, model files, logs, or desktop wrappers containing private addresses.
- Third-party packages and models retain their own licenses. This repository ships original hub code and setup helpers, not third-party application builds.

Report security problems privately to the repository owner. Include a minimal reproduction with synthetic data; never post secrets or live account databases in public issues.

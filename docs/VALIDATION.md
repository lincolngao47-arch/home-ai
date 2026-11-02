# Preview validation

Checked on 2026-11-01 on macOS / Apple Silicon:

- Installed dashboard dependencies into a new Python 3.11 virtual environment using `scripts/install.sh`.
- Ten backend tests passed in both the existing environment and the new isolated environment: authentication, invalid actions, disabled controls, command failures, key persistence / permissions, removed account routes, static assets / headers, Tailscale route detection, and failed health checks.
- JavaScript syntax and shell-script syntax checks passed. Three additional launcher tests verify raising a low inherited file limit, respecting a lower hard limit, and preserving an already-higher limit alongside two UI-installer tests (15 tests total).
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


## Mobile chat regression and correction

A subsequent physical iPhone screenshot exposed two gaps that page-load checks did not catch: the legacy floating guide toolbar overlapped the composer, and the original 4K fast-model budget rejected a full chat request. The deployment now uses 16K context / 2K reply limits, concise system instructions, short model names, and a restrained stylesheet without floating controls. The installer updates WebUI’s startup-copy sources as well as served files and versions asset URLs.

The real browser chat interface was tested against an isolated local WebUI data directory using the same model settings. It successfully answered both “hi” and “Hello” at phone-sized viewports, including a 390×470 viewport representing reduced space while typing. Checks found 16px editor text, no legacy floating bar, and no horizontal overflow. This does not emulate the actual iOS keyboard or Safari engine; the physical iPhone retest remains user validation.

The production streaming endpoint also answered a greeting and accepted a synthetic request longer than the old context budget. Two installer regression tests check that the new assets survive WebUI’s startup copy, backups remain intact on reapplication, and unknown package layouts are left unchanged.


## November 2: model picker, LAN choice, and sustained browser use

- Renamed the ambiguous fast profiles to identify Qwen 3 4B Instruct and Gemma 3 4B. All five household profiles, including both larger Qwen models and DeepSeek R1, were visible through an existing regular account's filtered model endpoint. No role change was needed.
- Disabled unsolicited knowledge-base browsing for these simple profiles. Historical failed knowledge activity uses a truthful neutral details label with the error still expandable; chat data was retained.
- Full-interface model switching exposed Gemma's rejection of browser-injected tools, which a bare API greeting had missed. Queried actual Ollama capabilities and disabled native built-in tools on incompatible profiles. Browser regeneration then returned “4”; desktop upload of a synthetic red PNG returned “Red”.
- Real browser interaction covered an English poem, a Chinese follow-up, model switching, response regeneration, image upload, and a subsequent greeting. Checked 1280×900 desktop, 390×844 phone, 320×568 narrow phone, and 390×470 reduced-height layouts. In the reduced-height view, the composer remained within the viewport, editor text was16px, and the page did not overflow horizontally.
- Hub checks covered EN/ZH, light/dark, same-Wi-Fi/Tailscale choice, generated links, and persistence. Corrected radio buttons inheriting text-input sizing, stale section navigation labels, and refresh-related keyboard focus loss.
- Enabled the existing Mac's chat listener for LAN access, preserving authentication. Host-side LAN and private HTTPS health checks passed; anonymous model access returned401. HTTP LAN session refresh set a non-Secure HttpOnly SameSite=Lax cookie, and a subsequent cookie-only models request returned200. Physical Safari login was not tested. These origins have separate sessions.
- All five production profiles answered a synthetic arithmetic request through the LAN WebUI endpoint. This is a functional smoke check, not a model-quality or sustained-load benchmark.
- A single scoped Gemini browser review suggested memory/session follow-ups. The existing Mac allowed four parallel generations; reduced it to one while retaining its two-model load limit, updated its login settings, and confirmed the new process environment. Also corrected the native app launcher to pass its intended environment explicitly, since LaunchServices reused older values despite launchctl updates. The running Ollama listener was rechecked on loopback. This is a case-specific tuning choice, not a recommended universal concurrency setting.
- Seventeen unit tests passed, including LAN discovery excluding VPN/bridge/public/inactive interfaces and withholding unreachable chat URLs. Syntax checks passed.

Physical iOS Safari keyboard behavior, access from a guest Wi-Fi, and simultaneous multi-user load remain unverified. Phone-sized browser use is not physical-phone certification.

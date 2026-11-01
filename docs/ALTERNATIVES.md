# Which chat application belongs behind this hub?

Assessment: 2026-11-01. Features and installation requirements can change; follow upstream documentation before migration.

| Choice | Best reason to use it here | Tradeoff |
| --- | --- | --- |
| Open WebUI | Keep the existing Ollama-backed, multi-user household chat and document workflow | Its own branding / license terms remain relevant; extensive features can make onboarding busy |
| LibreChat | Prioritize agents, MCP tools, artifacts, and multiple provider workflows | A separate deployment and configuration project; existing account and chat migration needs testing |
| AnythingLLM | Prioritize document workspaces, retrieval, and agents with an approachable packaged app | Desktop is a single-user experience; shared household use needs the server / Docker edition |

**Recommendation:** keep Open WebUI for the current server, improve the front door and device setup, and trial LibreChat separately only when specific agent workflows justify migration. If document research becomes the main job, trial AnythingLLM with representative documents first. There is no universal winner based on feature count.

Sources:

- [Open WebUI documentation](https://docs.openwebui.com/): self-hosted interface and local operation.
- [Open WebUI license](https://docs.openwebui.com/license/): current redistribution and branding terms. This hub does not redistribute or rebrand its UI.
- [LibreChat features](https://www.librechat.ai/docs/features): agents, MCP, artifacts, RAG, and conversation tools.
- [AnythingLLM introduction](https://docs.anythingllm.com/introduction) and [desktop overview](https://docs.anythingllm.com/installation-desktop/overview): product scope and desktop / Docker distinctions.

## Is a public repository worthwhile?

A modest starter is worthwhile if it solves a narrow, repeated problem: making a private family AI server approachable and easy to connect to. Another general chat clone would need far more maintenance and differentiation. Popularity cannot be predicted reliably from this prototype.

Release a small preview, document what has actually been tested, and measure successful installs and useful issue reports. The next investment should follow evidence: installation friction, mobile usage, and requests for features that upstream tools do not already provide.

# Fast everyday chat

Large reasoning models can spend time loading weights and producing internal reasoning before any answer appears. A small instruct model is a useful default for greetings, translation, rewriting, and short questions. Keep larger models available for tasks that need their capabilities.

## Install the fast options

With Ollama running, explicitly download about 6 GB of model weights:

```bash
.venv/bin/python scripts/install_fast_models.py
```

This creates two aliases that reuse the downloaded weights:

| Alias | Base model | Use |
| --- | --- | --- |
| `home-fast:latest` | `qwen3:4b-instruct` | Fast bilingual text chat |
| `home-vision:latest` | `gemma3:4b` | Small text and image model |

Both aliases now use a 16,384-token context with a 2,048-token reply cap. The previous 4K setting could reject normal browser chats once system instructions and tool definitions were included. The hub puts them first and opens them through Open WebUI’s `model` URL parameter, overriding a browser’s previously selected model. Base-model duplicates are hidden in the hub when their aliases exist; all installed models remain available to Ollama.

In Open WebUI, set the instance’s selected/default model to `home-fast:latest`. For a longer warm period, set its `keep_alive` model parameter to `30m`. Use it as the task model for titles and other background tasks, and disable typing autocomplete if it competes with chat requests. These are instance settings: the public download script does not authenticate to or change an existing Open WebUI installation.

The development instance uses those settings, has streaming enabled for both fast profiles, and retains the large models. Existing conversations keep their selected model; start a new chat with the hub’s **Open fast chat** button to switch.

## Measured on the development Mac

Historical measurements before the context-budget fix: one greeting request per condition, Apple M4 Pro / 64 GB, 4K context, maximum 128 output tokens, local HTTP. These short API measurements did not cover the phone browser’s full chat payload. These are observations, not guaranteed latency or a quality benchmark.

| Request | First visible text | Model loading |
| --- | --- | --- |
| Existing `qwen3.8:27b`, cold | 14.00 s | 9.10 s |
| `home-fast`, cold | 2.11 s | 2.03 s |
| `home-fast`, warm | 0.023 s | 0.001 s |
| Warm `home-fast` through Open WebUI | 0.119 s | Included in request |
| `home-vision`, cold, text greeting | 1.21 s | 1.07 s |

The small text model produced roughly 71 tokens/second during these short tests. The vision model’s text greeting is not an image-processing latency benchmark. Phone rendering, Wi-Fi, Tailscale, long conversation history, document retrieval, and other requests add latency.

Reproduce a local greeting measurement without saving a conversation:

```bash
.venv/bin/python scripts/benchmark_chat.py home-fast --keep-alive 0
.venv/bin/python scripts/benchmark_chat.py home-fast --keep-alive 30m
.venv/bin/python scripts/benchmark_chat.py home-fast --keep-alive 30m
```

The first command may use already-loaded weights, then unloads the model. The second therefore measures cold loading, and the third measures warm reuse. The script reports both first visible text and first reasoning text, avoiding confusion between internal reasoning and a user-visible answer.

The current 16K budget leaves room for ordinary chat overhead; avoid attaching a lengthy installation guide as a default system prompt. After this fix, a warm production WebUI greeting began replying in about 0.10 seconds locally, a synthetic request longer than the old 4K budget completed successfully, and greetings completed through the full browser UI in an isolated preview with matching settings. For long documents, long conversations, or difficult reasoning, choose an appropriate larger model. Short outputs do not establish factual accuracy or task quality.

Sources: [Qwen model](https://ollama.com/library/qwen3:4b-instruct), [Gemma model](https://ollama.com/library/gemma3:4b), [Open WebUI model URL parameters](https://docs.openwebui.com/features/chat-conversations/chat-features/url-params/).


## Browser tools and concurrent model loads

A later browser model-switch test showed that a successful bare API reply does not prove compatibility with the tools Open WebUI injects into normal chat. Query each installed model's capabilities and disable native built-in tools on profiles that do not support them. Gemma 3 image upload and chat regeneration were checked after this correction.

For this 64GB development Mac, the existing four-generation parallel setting was reduced to one while retaining a two-model resident limit. Fast profiles keep their30-minute lifetime, and larger profiles use5minutes. This reduces simultaneous context-buffer pressure; it does not make a32B reasoning model as fast as a4B text model. Tune concurrency to measured memory and workload on other machines.

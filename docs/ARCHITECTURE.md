# Architecture

```text
Phone / tablet / computer
          |
    private Tailscale network
          |
  Tailscale Serve (HTTPS)
       /             \
  :443 → :3000    :8443 → :8088
   Open WebUI       Home AI
       |          health + model queries
     Ollama       (no chat/account DB access)
```

The hub is a FastAPI service with buildless HTML, CSS, and JavaScript. It needs no CDN, web fonts, frontend bundler, or third-party analytics. External help / download links are visited only when selected.

Health checks execute concurrently with short timeouts, bypass system HTTP proxies for backend requests, and share a five-second cache. Browsers refresh every 15 seconds while visible. Model availability comes from Ollama, not a hardcoded list. Host statistics come from psutil; memory accounting may differ from macOS Activity Monitor.

Read-only status includes the machine hostname, resource usage, model names, and private Tailscale hostname. Therefore the dashboard is intended for trusted LAN / tailnet users. Backend URLs are operator-controlled environment settings and are not accepted from browser input.

All mutating API calls require a randomly generated admin key, including requests from loopback. This matters because Tailscale Serve forwards from localhost. The frontend stores the key in memory rather than localStorage. Account management remains in Open WebUI, avoiding fragile direct SQLite writes.

Native macOS service controls use an enumerated service/action schema and argument-array subprocess execution. The shell controller operates on a dedicated machine's matching service processes; multiple parallel Open WebUI / Ollama installations on one host are outside its intended use. Concurrent control requests are rejected. Startup must pass a health check before success is returned.

The hub does not proxy model APIs or chat traffic. It preserves Open WebUI’s own login and features. Tailscale Serve establishes private HTTPS; it does not automatically grant arbitrary devices membership in the network.

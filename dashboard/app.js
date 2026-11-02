"use strict";
const $ = (s) => document.querySelector(s);
const zh = {
  connectionChoice: "自由选择",
  chooseConnection: "选择连接方式",
  wifiChoice: "同一 Wi-Fi",
  wifiDescription: "连接服务器所在的家庭网络，无需安装 App。使用 Open WebUI 账号登录。",
  wifiUnavailable: "服务器尚未开启 Wi-Fi 访问。请查看安装指南，开启局域网访问。",
  wifiPrivacy: "仅限家庭网络。此 HTTP 连接未加密，请使用可信 Wi-Fi；语音录制需要 HTTPS。",
  wifiReady: "Wi-Fi 访问已就绪",
  wifiNetworkReady: "同一家庭网络内无需安装 App。出门后可切换到 Tailscale。",
  wifiOpen: "打开 Wi-Fi 对话 ↗",
  wifiHub: "Wi-Fi 首页 ↗",
  wifiPending: "Wi-Fi 访问未就绪",
  secureMaintenance: "请在服务器本机或 Tailscale HTTPS 首页进行维护管理。",

  skip: "跳转到内容",
  privateSpace: "你的私密空间",
  overview: "概览",
  services: "服务",
  models: "你的模型",
  connect: "连接设备",
  localFirst: "本地优先，由你掌控。",
  localDescription: "你的服务器，你的模型。从这里开始。",
  help: "Open WebUI 使用帮助 ↗",
  workspace: "工作空间",
  maintenance: "维护管理",
  homeServer: "家庭服务器 / 私人智能",
  welcome: "多一点智能。<br>多一份自主。",
  intro: "属于你的 AI 空间，随时准备就绪。",
  checking: "正在检查服务器…",
  dailyCompanion: "你的日常好帮手",
  chatTitle: "尽情探索。<br>私密对话。",
  chatDescription: "通过 Open WebUI 提出问题、读懂文档，或一起推敲下一个灵感。",
  openChat: "打开 AI 对话",
  fastChat: "打开快速对话",
  fastEveryday: "Qwen 3 4B · 快聊",
  fastVision: "Gemma 3 4B · 看图",
  textModel: "快速文字对话 · 16K 上下文",
  visionModel: "快速图片理解 · 16K 上下文",
  chatNote: "使用你的 Open WebUI 账号登录。",
  checkingShort: "检查中",
  anywhere: "在家里。<br>也在远方。",
  networkDescription: "同一 Wi-Fi 直接访问，或通过 Tailscale 远程连接。",
  setupDevices: "设置你的设备 →",
  processor: "处理器",
  memory: "内存使用",
  storage: "可用存储",
  uptime: "连续运行",
  waiting: "等待服务器",
  storageNote: "用于模型和文档的剩余空间",
  behindScenes: "幕后运行",
  servicesTitle: "各就其位，井然有序。",
  refresh: "刷新状态 ↻",
  modelDescription: "在 Open WebUI 中选择一个模型，开始对话。",
  loadingModels: "正在加载模型库…",
  step1: "安装 Tailscale",
  step1Description: "在手机、平板或电脑上安装，登录同一个私有网络。",
  download: "下载 Tailscale ↗",
  step2: "打开你的私有地址",
  remotePending: "完成服务器设置后，即可获取 HTTPS 地址。",
  copy: "复制对话地址",
  remoteRequirement: "使用此地址的每台设备都需要安装并连接 Tailscale。",
  step3: "让它成为日常",
  step3Description:
    "iPhone / iPad：Safari → 分享 → 添加到主屏幕。Android：浏览器菜单 → 添加到主屏幕。电脑：将此页面加入书签。",
  familyTitle: "给全家人的 AI 空间。",
  familyDescription: "在 Open WebUI 管理面板中管理邀请、账号与权限。",
  manageAccounts: "管理账号 ↗",
  footer: "让 AI 有个舒适的家。",
  powered: "对话由 Open WebUI + Ollama 提供",
  unlockTitle: "服务器维护",
  unlockDescription:
    "输入服务器 .home-ai/admin-token 文件中的管理密钥。密钥仅保存在当前标签页内存中，锁定或刷新后清除。",
  adminKey: "管理密钥",
  unlock: "解锁维护",
  confirmTitle: "更改此服务？",
  cancel: "取消",
  confirm: "确认",
  ready: "AI 对话已就绪",
  attention: "核心服务需要检查",
  connected: "私有连接已就绪",
  loginNeeded: "需要登录",
  serveNeeded: "需要设置 HTTPS",
  unavailable: "暂不可用",
  online: "在线",
  offline: "离线",
  optional: "可选",
  open: "打开 ↗",
  localOnly: "仅限服务器本机",
  start: "启动",
  stop: "停止",
  restart: "重启",
  lock: "锁定维护",
  running: "运行中",
  installed: "已安装",
  noModels: "还没有可用模型。在服务器上使用 ollama pull 下载模型，然后刷新。",
  updated: "更新于",
  stale: "无法连接服务器。显示的是上次获取的数据，请检查连接后重试。",
  copied: "对话地址已复制。",
  copyFailed: "无法复制，请手动选择上方地址。",
  done: "操作完成，正在检查服务状态。",
  changing: "正在更改服务，请稍候…",
  confirmAction: "此操作可能中断正在进行的对话或任务。",
  controlsDisabled: "此部署不支持服务控制。",
  themeAuto: "主题：跟随系统",
  themeLight: "主题：浅色",
  themeDark: "主题：深色",
  networkReady: "私有 HTTPS 已就绪。在其他设备上连接 Tailscale 后，即可使用。",
  networkLogin: "在这台服务器上登录 Tailscale，即可开始远程连接。",
  networkUnavailable:
    "Tailscale 暂未连接。在服务器上打开 Tailscale 并检查连接状态。",
  networkSetup:
    "Tailscale 已连接。运行 scripts/setup_tailscale.sh，开启私有 HTTPS。",
  webuiDesc: "对话、文档与图片理解。",
  ollamaDesc: "本地模型推理引擎。",
  n8nDesc: "自动化与重复任务。",
  whisperDesc: "音视频转写。",
  usedOf: "已用 / 共",
  days: "天",
  hours: "小时",
  notReachable: "当前地址不可用",
  fetchError: "请求失败，请稍后重试。",
  authError: "密钥无效，请检查服务器上的 admin-token 文件。",
};
const en = {
  connectionChoice: "Your choice",
  chooseConnection: "How do you want to connect?",
  wifiChoice: "Same Wi-Fi",
  wifiDescription: "Connect to the same home network as the server. No app to install; sign in with your Open WebUI account.",
  wifiUnavailable: "Wi-Fi access is not enabled on the server yet. See the setup guide to enable LAN access.",
  wifiPrivacy: "Home network only. This HTTP connection is unencrypted; use trusted Wi-Fi. Voice recording requires HTTPS.",
  wifiReady: "Wi-Fi access ready",
  wifiNetworkReady: "No app needed on your home network. Switch to Tailscale when you are away.",
  wifiOpen: "Open Wi-Fi chat ↗",
  wifiHub: "Wi-Fi home page ↗",
  wifiPending: "Wi-Fi access unavailable",
  secureMaintenance: "Open the hub on the server itself or through Tailscale HTTPS for maintenance.",

  remoteRequirement:
    "Install and connect Tailscale on every device that uses this address.",
  fastChat: "Open fast chat",
  fastEveryday: "Qwen 3 4B · Fast",
  fastVision: "Gemma 3 4B · Images",
  textModel: "Quick text chat · 16K context",
  visionModel: "Quick image understanding · 16K context",
  ready: "AI chat is ready",
  attention: "Core services need attention",
  connected: "Private access ready",
  loginNeeded: "Sign-in needed",
  serveNeeded: "HTTPS setup needed",
  unavailable: "Unavailable",
  online: "Online",
  offline: "Offline",
  optional: "Optional",
  open: "Open ↗",
  localOnly: "Server only",
  start: "Start",
  stop: "Stop",
  restart: "Restart",
  lock: "Lock maintenance",
  running: "Loaded",
  installed: "Installed",
  noModels:
    "No models available yet. Run ollama pull on the server to download one, then refresh.",
  updated: "Updated",
  stale:
    "Cannot reach your server. Last known data is shown; check your connection and try again.",
  copied: "Chat address copied.",
  copyFailed: "Could not copy. Select the address above to copy it manually.",
  done: "Action completed. Checking service status…",
  changing: "Changing service. This may take a moment…",
  confirmAction: "This may interrupt active conversations or tasks.",
  controlsDisabled: "Service controls are not available in this deployment.",
  themeAuto: "Theme: Auto",
  themeLight: "Theme: Light",
  themeDark: "Theme: Dark",
  networkReady:
    "Private HTTPS is ready. Connect to Tailscale on your other device to use it.",
  networkLogin: "Sign in to Tailscale on this server to enable remote access.",
  networkUnavailable:
    "Tailscale is not connected. Open Tailscale on the server and check its connection.",
  networkSetup:
    "Tailscale is connected. Run scripts/setup_tailscale.sh to enable private HTTPS.",
  webuiDesc: "Conversations, documents, and vision.",
  ollamaDesc: "The engine for your local models.",
  n8nDesc: "Workflows and everyday automations.",
  whisperDesc: "Turn audio and video into text.",
  usedOf: "used of",
  days: "d",
  hours: "h",
  notReachable: "Address unavailable",
  fetchError: "Request failed. Please try again.",
  authError: "Invalid key. Check the admin-token file on your server.",
};
document
  .querySelectorAll("[data-i18n]")
  .forEach((el) => (en[el.dataset.i18n] = el.innerHTML));
let lang =
  localStorage.getItem("home-ai-language") ||
  (navigator.language.startsWith("zh") ? "zh" : "en");
let theme = localStorage.getItem("home-ai-theme") || "auto";
let connection = localStorage.getItem("home-ai-connection") ||
  (location.hostname.endsWith(".ts.net") ? "tailscale" : "wifi");
if (!["wifi", "tailscale"].includes(connection)) connection = "wifi";
let adminKey = "",
  data = null,
  refreshing = false,
  pendingAction = null,
  toastTimer,
  actionBusy = false;
const t = (key) => (lang === "zh" ? zh[key] : en[key]) || en[key] || key;
const escapeHTML = (value) =>
  String(value ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
function toast(message) {
  $("#toast").textContent = message;
  $("#toast").hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => ($("#toast").hidden = true), 6000);
}
function applyTheme() {
  document.documentElement.dataset.theme =
    theme === "auto"
      ? matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light"
      : theme;
  $("#theme").textContent = t(
    "theme" + theme[0].toUpperCase() + theme.slice(1),
  );
}
function translate() {
  document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";
  document
    .querySelectorAll("[data-i18n]")
    .forEach((el) => (el.innerHTML = t(el.dataset.i18n)));
  $("#language").textContent = lang === "zh" ? "EN" : "中文";
  $("#language").setAttribute(
    "aria-label",
    lang === "zh" ? "Switch language to English" : "切换到中文",
  );
  applyTheme();
  updateNavigation();
  if (data) render();
}
function updateNavigation() {
  const view = ["overview", "services", "models", "connect"].includes(location.hash.slice(1))
    ? location.hash.slice(1) : "overview";
  document.querySelector(".breadcrumb strong").textContent = t(view);
  document.querySelectorAll("nav a").forEach((link) => {
    const active = link.getAttribute("href") === "#" + view;
    link.classList.toggle("active", active);
    if (active) link.setAttribute("aria-current", "location");
    else link.removeAttribute("aria-current");
  });
}
function updateMarkup(selector, markup) {
  const element = $(selector);
  // Polling should not destroy a keyboard user's focused link.
  if (element.innerHTML === markup) return;
  const focused = element.contains(document.activeElement) ? document.activeElement.closest("a")?.href : null;
  element.innerHTML = markup;
  if (focused) [...element.querySelectorAll("a")].find((link) => link.href === focused)?.focus({preventScroll: true});
}
$("#language").onclick = () => {
  lang = lang === "zh" ? "en" : "zh";
  localStorage.setItem("home-ai-language", lang);
  translate();
};
$("#theme").onclick = () => {
  theme = ["auto", "light", "dark"][
    (["auto", "light", "dark"].indexOf(theme) + 1) % 3
  ];
  localStorage.setItem("home-ai-theme", theme);
  applyTheme();
};
matchMedia("(prefers-color-scheme: dark)").addEventListener(
  "change",
  applyTheme,
);
function linkFor(service) {
  if (service === "open_webui") {
    if (connection === "tailscale") return data?.tailscale.chat_url || null;
    // Keep local browsing local, but use a verified LAN endpoint on other devices.
    if (["localhost", "127.0.0.1", "[::1]"].includes(location.hostname)) {
      const url = new URL(location.origin);
      url.protocol = "http:";
      url.port = data?.services.open_webui.port || "3000";
      url.pathname = "/";
      return url.href;
    }
    const addresses = data?.lan?.addresses || [];
    return addresses.find((item) => item.address === location.hostname)?.chat_url || data?.lan?.chat_url || null;
  }
  // Other backends are intentionally not exposed with Wi-Fi chat.
  if (!["localhost", "127.0.0.1", "[::1]"].includes(location.hostname) || location.protocol === "https:") return null;
  const port = data?.services[service]?.port;
  if (!port) return null;
  const url = new URL(location.origin);
  url.port = port;
  url.pathname = service === "whisper" ? "/docs" : "/";
  return url.href;
}
function setLink(el, href, available = true) {
  if (href && available) {
    el.href = href;
    el.removeAttribute("aria-disabled");
    el.removeAttribute("tabindex");
  } else {
    el.removeAttribute("href");
    el.setAttribute("aria-disabled", "true");
    el.tabIndex = -1;
  }
}
function modelLink(model) {
  const base = linkFor("open_webui");
  if (!base) return null;
  const url = new URL(base);
  url.searchParams.set("model", model);
  return url.href;
}
function render() {
  const coreReady =
    data.services.open_webui.online && data.services.ollama.online;
  $("#overall").textContent = t(coreReady ? "ready" : "attention");
  $("#overall").classList.toggle("warn", !coreReady);
  const net = data.tailscale;
  const wifi = connection === "wifi";
  document.querySelectorAll('input[name="connection"]').forEach((input) => {
    input.checked = input.value === connection;
  });
  $("#wifi-instructions").hidden = !wifi;
  $("#tailscale-instructions").hidden = wifi;
  const lanAddresses = data.lan?.addresses || [];
  $("#wifi-unavailable").hidden = Boolean(data.lan?.chat_url);
  updateMarkup("#wifi-addresses", lanAddresses.map((item) => {
    if (!item.chat_url) return "";
    return `<div><a href="${escapeHTML(item.chat_url)}">${t("wifiOpen")}</a><code>${escapeHTML(item.chat_url)}</code>${item.dashboard_url ? `<a href="${escapeHTML(item.dashboard_url)}">${t("wifiHub")}</a>` : ""}</div>`;
  }).join(""));
  $("#network-badge").textContent = t(
    wifi ? (data.lan?.chat_url ? "wifiReady" : "wifiPending") : net.chat_url
      ? "connected"
      : net.state === "NeedsLogin"
        ? "loginNeeded"
        : net.state === "Running"
          ? "serveNeeded"
          : "unavailable",
  );
  $("#network-description").textContent = t(
    wifi ? (data.lan?.chat_url ? "wifiNetworkReady" : "wifiUnavailable") : net.chat_url
      ? "networkReady"
      : net.state === "Running"
        ? "networkSetup"
        : net.state === "NeedsLogin"
          ? "networkLogin"
          : "networkUnavailable",
  );
  $("#remote-help").textContent = net.chat_url || t("remotePending");
  $("#copy-url").hidden = !net.chat_url;
  const fastAvailable = data.ollama.installed.some(
    (model) => model.name === "home-fast:latest",
  );
  setLink(
    $("#chat-link"),
    fastAvailable ? modelLink("home-fast:latest") : linkFor("open_webui"),
    coreReady,
  );
  $('#chat-link [data-i18n="openChat"]').textContent = t(
    fastAvailable ? "fastChat" : "openChat",
  );
  const chat = linkFor("open_webui");
  setLink(
    $("#accounts-link"),
    chat ? new URL("/admin", chat).href : null,
    data.services.open_webui.online,
  );
  const hw = data.hardware;
  $("#cpu").textContent = hw.cpu.used_pct + "%";
  $("#chip").textContent = hw.chip;
  $("#memory").textContent = hw.memory.used_gb + " GB";
  $("#memory-detail").textContent = `${t("usedOf")} ${hw.memory.total_gb} GB`;
  $("#disk").textContent = hw.disk.free_gb + " GB";
  for (const kind of ["cpu", "memory", "disk"])
    $("#" + kind + "-bar").style.width =
      Math.min(100, Math.max(0, hw[kind].used_pct)) + "%";
  const hours = Math.floor(hw.uptime_seconds / 3600);
  $("#uptime").textContent =
    `${Math.floor(hours / 24)}${t("days")} ${hours % 24}${t("hours")}`;
  $("#host").textContent = hw.os + " · " + hw.hostname;
  const descriptions = {
      open_webui: "webuiDesc",
      ollama: "ollamaDesc",
      n8n: "n8nDesc",
      whisper: "whisperDesc",
    },
    icons = { open_webui: "✳", ollama: "◉", n8n: "⌘", whisper: "≋" };
  const markup = Object.entries(data.services)
    .map(([key, service]) => {
      const href = linkFor(key),
        canOpen = href && service.online;
      return `<article class="service-card"><div class="card-top"><span class="icon-box" aria-hidden="true">${icons[key]}</span><span class="badge ${service.online ? "" : "warn"}">${t(service.online ? "online" : "offline")}</span></div><h3>${escapeHTML(service.name)}</h3><p>${t(descriptions[key])}</p><div class="service-bottom"><span>${service.online ? service.latency_ms + " ms" : t(service.required ? "attention" : "optional")}</span>${canOpen ? `<a href="${escapeHTML(href)}" aria-label="${t("open")} ${escapeHTML(service.name)}">${t("open")}</a>` : `<span>${t("localOnly")}</span>`}</div>${adminKey && data.controls_enabled ? `<div class="service-controls">${(service.online ? ["restart", "stop"] : ["start"]).map((action) => `<button data-service="${key}" data-action="${action}" ${actionBusy ? "disabled" : ""}>${t(action)}</button>`).join("")}</div>` : ""}</article>`;
    })
    .join("");
  if ($("#service-grid").innerHTML !== markup) {
    const focused = document.activeElement,
      service = focused?.dataset.service,
      action = focused?.dataset.action;
    $("#service-grid").innerHTML = markup;
    if (service && action)
      $(`[data-service="${service}"][data-action="${action}"]`)?.focus();
  }
  $("#updated").textContent =
    `${t("updated")} ${new Date(data.timestamp * 1000).toLocaleTimeString(lang === "zh" ? "zh-CN" : "en", { hour: "2-digit", minute: "2-digit", second: "2-digit" })}`;
  const allModels = data.ollama.installed;
  const names = new Set(allModels.map((model) => model.name));
  const models = allModels
    .filter(
      (model) =>
        !(
          model.name === "qwen3:4b-instruct" && names.has("home-fast:latest")
        ) && !(model.name === "gemma3:4b" && names.has("home-vision:latest")),
    )
    .sort((a, b) => {
      const rank = (name) =>
        name === "home-fast:latest" ? 0 : name === "home-vision:latest" ? 1 : 2;
      return rank(a.name) - rank(b.name);
    });
  $("#model-count").textContent = models.length;
  const modelMarkup = models.length
    ? models
        .map((model) => {
          const label =
            model.name === "home-fast:latest"
              ? t("fastEveryday")
              : model.name === "home-vision:latest"
                ? t("fastVision")
                : model.name;
          const detail =
            model.name === "home-fast:latest"
              ? t("textModel")
              : model.name === "home-vision:latest"
                ? t("visionModel")
                : `${model.params} · ${model.size_gb} GB`;
          const href = coreReady ? modelLink(model.name) : null;
          const title = href
            ? `<a href="${escapeHTML(href)}">${escapeHTML(label)} ↗</a>`
            : escapeHTML(label);
          return `<div class="model-row"><span class="model-symbol" aria-hidden="true">◇</span><div class="model-info"><strong>${title}</strong><small>${escapeHTML(detail)}</small></div><span class="badge">${t(data.ollama.loaded.includes(model.name) ? "running" : "installed")}</span></div>`;
        })
        .join("")
    : `<p>${t("noModels")}</p>`;
  updateMarkup("#model-list", modelMarkup);
  $("#admin").textContent = t(adminKey ? "lock" : "maintenance");
}
async function refresh() {
  if (refreshing) return;
  refreshing = true;
  $("#refresh").disabled = true;
  try {
    const response = await fetch("/api/stats", {
      signal: AbortSignal.timeout(15000),
    });
    if (!response.ok) throw Error();
    data = await response.json();
    render();
    $("#error-banner").hidden = true;
  } catch {
    $("#error-banner").textContent = t("stale");
    $("#error-banner").hidden = false;
    $("#overall").textContent = t("unavailable");
    $("#overall").classList.add("warn");
    setLink($("#chat-link"), null);
  } finally {
    refreshing = false;
    $("#refresh").disabled = false;
  }
}
document.querySelectorAll('input[name="connection"]').forEach((input) => {
  input.onchange = () => {
    connection = input.value;
    localStorage.setItem("home-ai-connection", connection);
    if (data) render();
  };
});
$("#refresh").onclick = refresh;
$("#copy-url").onclick = async () => {
  try {
    await navigator.clipboard.writeText(data.tailscale.chat_url);
    toast(t("copied"));
  } catch {
    toast(t("copyFailed"));
  }
};
$("#admin").onclick = () => {
  if (!window.isSecureContext) {
    toast(t("secureMaintenance"));
    return;
  }
  if (adminKey) {
    adminKey = "";
    render();
    return;
  }
  $("#unlock-error").textContent = "";
  $("#admin-dialog").showModal();
  $("#admin-key").focus();
};
$("#close-admin").onclick = () => $("#admin-dialog").close();
$("#admin-dialog").addEventListener("close", () => {
  $("#admin-key").value = "";
});
$("#unlock-form").onsubmit = async (event) => {
  event.preventDefault();
  const key = $("#admin-key").value.trim();
  try {
    const response = await fetch("/api/unlock", {
      method: "POST",
      headers: { Authorization: "Bearer " + key },
      signal: AbortSignal.timeout(10000),
    });
    if (!response.ok) throw Error(t("authError"));
    adminKey = key;
    $("#admin-dialog").close();
    if (data) render();
    if (data && !data.controls_enabled) toast(t("controlsDisabled"));
  } catch (error) {
    $("#unlock-error").textContent = error.message || t("fetchError");
  }
};
$("#service-grid").onclick = (event) => {
  const button = event.target.closest("button[data-service]");
  if (!button || actionBusy) return;
  pendingAction = {
    service: button.dataset.service,
    action: button.dataset.action,
  };
  $("#confirm-description").textContent =
    `${t(pendingAction.action)} ${data.services[pendingAction.service].name}? ${t("confirmAction")}`;
  $("#confirm-dialog").showModal();
  $("#cancel-action").focus();
};
$("#cancel-action").onclick = () => $("#confirm-dialog").close();
$("#confirm-action").onclick = async () => {
  const action = pendingAction;
  $("#confirm-dialog").close();
  actionBusy = true;
  render();
  toast(t("changing"));
  try {
    const response = await fetch("/api/service", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + adminKey,
      },
      body: JSON.stringify(action),
      signal: AbortSignal.timeout(95000),
    });
    if (!response.ok) {
      if (response.status === 401) adminKey = "";
      const info = await response.json();
      throw Error(
        typeof info.detail === "string" ? info.detail : t("fetchError"),
      );
    }
    toast(t("done"));
  } catch (error) {
    toast(error.message || t("fetchError"));
  } finally {
    actionBusy = false;
    await refresh();
    if (data) render();
  }
};
window.addEventListener("hashchange", updateNavigation);
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) refresh();
});
translate();
refresh();
setInterval(() => {
  if (
    !document.hidden &&
    !$("#confirm-dialog").open &&
    !$("#admin-dialog").open &&
    !actionBusy
  )
    refresh();
}, 15000);

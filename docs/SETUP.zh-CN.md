# Home AI 安装与使用

Home AI 是家庭 AI 服务器的入口：打开 Open WebUI 对话、查看模型和服务状态，并通过 Tailscale 在外访问。它不会替代 Open WebUI，也不会读取或修改聊天、账号数据库。

当前为早期预览：已在 Apple Silicon Mac 上验证现有服务集成。浏览器支持手机、平板和电脑；服务器脚本支持 macOS / Linux，维护控制仅支持 macOS。Windows 可使用 WSL2 或直接访问另一台服务器。

## 已有 Ollama 和 Open WebUI

安装 Python 3.11 或 3.12，下载源码并进入项目文件夹：

```bash
bash scripts/install.sh
bash scripts/start_dashboard.sh
```

打开 http://127.0.0.1:8088。终端保持运行，Ctrl+C 可停止入口服务。默认端口：Open WebUI 3000，Ollama 11434；可选 n8n 5680、Whisper 8000。可选服务离线不会影响核心对话就绪状态。

## 从零开始

1. 从 https://ollama.com/download 安装并启动 Ollama。选择适合设备内存的模型，通过应用或 `ollama pull 模型名称` 下载。
2. 运行 `bash scripts/install.sh --with-chat`，在独立环境中安装 Open WebUI。
3. 运行 `bash scripts/start_chat.sh`，打开 http://127.0.0.1:3000，先创建首个管理员，再开放其他设备访问。
4. 在另一个终端运行 `bash scripts/start_dashboard.sh`。

新用户默认等待审批。现有安装的持久化设置以 Open WebUI 管理面板为准。本项目不会自动下载模型，也不会安装 n8n 或 Whisper。首次完整安装和 Linux / WSL2 端到端使用仍需更多测试。

## 登录后自动启动（macOS）

先成功运行一次入口和对话服务，再执行 `.venv/bin/python scripts/install_autostart.py --chat`。系统会在登录后启动服务，并在进程退出时自动重启。现有 Open WebUI 可用 `HOME_AI_WEBUI_BIN` 指向其启动程序。模型缓存完整后可加 `--offline`，减少启动时的网络依赖。日志和旧配置保存在 `.home-ai/`。

## 更快的日常对话

在 Ollama 运行时执行 `.venv/bin/python scripts/install_fast_models.py`，明确下载约 6 GB 模型。入口会优先显示日常快聊 `home-fast` 和轻量看图 `home-vision`，主按钮直接选择快聊模型，避免手机记住旧的大模型。

两者使用 16K 上下文和最多 2K 回复预算；长文档和复杂任务可以选择原有大模型。开发机上一次简单问候的首字延迟约为冷启动 2.1 秒、经过 Open WebUI 热启动 0.12 秒，原来的 27B 模型约 14 秒。手机网络和任务复杂度会影响实际速度。默认模型、保温时间和后台任务模型的设置见 PERFORMANCE.md。

聊天页面的可选简洁样式：使用安装 Open WebUI 的 Python 环境运行 `scripts/install_webui_polish.py`。它会备份原文件，移除旧的悬浮指南栏，并为手机设置易读输入字号与触控尺寸。升级 Open WebUI 后需要重新应用。旧模型配置中的 4K 上下文也需更新为 16384，回复预算设为 2048。

## 外出访问：Tailscale（方案 A）

在服务器和手机 / 平板 / 电脑上安装 Tailscale，登录同一私有网络，然后运行：

```bash
bash scripts/setup_tailscale.sh
```

若提示开启 HTTPS，按 Tailscale 的提示在管理控制台完成，再重新运行。对话使用服务器的 `https://设备名.网络名.ts.net` 地址；入口使用相同地址加 `:8443`。脚本不会开启公开互联网访问的 Funnel，也不会共享原始模型 API。

iPhone / iPad：Safari → 分享 → 添加到主屏幕。
Android：浏览器菜单 → 添加到主屏幕。
电脑：将地址加入书签。

只有实际发现对应 Serve 配置后，入口才显示 HTTPS 已就绪。如发生连接超时，先检查 Tailscale 连接，再重试。最后用手机蜂窝网络实测一次远程访问。

## 维护与隐私

从服务器 `.home-ai/admin-token` 文件读取密钥，在「维护管理」输入。密钥仅保存在当前标签页内存中，锁定或刷新后清除。不要分享密钥。账号、密码和权限请在 Open WebUI 自带管理面板操作。

默认仅监听本机，由 Tailscale 提供远程入口。不要将现有聊天数据、数据库、下载文件或日志上传 GitHub。使用 `python scripts/export_source.py` 生成明确允许的源码包。

更多配置与限制见英文 README 和 SECURITY.md。


## 不装手机 App：同一 Wi-Fi 访问

在首页「连接设备」选择「同一 Wi-Fi」或「Tailscale」，主对话按钮和模型链接会随之切换，浏览器会记住选择。Mac 可接网线，只要手机和服务器在同一家庭局域网即可。

macOS 登录后自动启动的部署，可执行：

```bash
.venv/bin/python scripts/install_autostart.py --chat --lan
```

已有 Open WebUI 环境请同时设置 `HOME_AI_WEBUI_BIN` 为对应可执行文件。手动启动时，分别用 `WEBUI_HOST=0.0.0.0 bash scripts/start_chat.sh` 和 `DASHBOARD_HOST=0.0.0.0 bash scripts/start_dashboard.sh`。首页会检查真实可达的局域网地址，再显示链接；VPN、Docker 网桥地址不会当作 Wi-Fi 地址。

同一 Wi-Fi 无需安装 Tailscale，仍需 Open WebUI 登录。HTTP 不加密密码与对话，只在可信家庭网络使用；语音录制需要 HTTPS，可切换 Tailscale。访客 Wi-Fi 可能隔离设备。不要把这些端口转发到公网。

原 Everyday 实际是 Qwen 3 4B Instruct，现使用清晰名称「Qwen 3 4B · Fast」；看图模型为「Gemma 3 4B · Images」。已下载的大 Qwen、DeepSeek 模型还需要在 Open WebUI 工作空间中创建/编辑模型配置并授予家庭用户读取权限，普通账号才能选择。无需提升账号角色。

简单对话配置可关闭「内置工具 → 知识库」，避免写诗等任务自动搜索知识库。旧失败搜索的红叉改为中性文字提示，仍可展开查看错误详情。

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

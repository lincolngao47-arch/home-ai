#!/usr/bin/env python3
"""Home AI: a small, private service hub. No access to chat/account databases."""
import asyncio
import hmac
import json
import os
import platform
import secrets
import socket
import subprocess
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse

import httpx
import psutil
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

ROOT = Path(os.environ.get('HOME_AI_DIR', Path(__file__).resolve().parents[1]))
STATE = Path(os.environ.get('HOME_AI_STATE_DIR', ROOT / '.home-ai'))
STATIC = Path(__file__).resolve().parent
PORT = int(os.environ.get('DASHBOARD_PORT', '8088'))
CONTROL_ENABLED = os.environ.get('HOME_AI_CONTROLS', 'true').lower() == 'true' and platform.system() == 'Darwin'
SERVICES = {
    'open_webui': ('Open WebUI', os.environ.get('WEBUI_URL', 'http://127.0.0.1:3000'), '/health'),
    'ollama': ('Ollama', os.environ.get('OLLAMA_URL', 'http://127.0.0.1:11434'), '/api/tags'),
    'n8n': ('n8n', os.environ.get('N8N_URL', 'http://127.0.0.1:5680'), '/healthz'),
    'whisper': ('Whisper', os.environ.get('WHISPER_URL', 'http://127.0.0.1:8000'), '/health'),
}
TOKEN = ''
cache = {'at': 0, 'value': None}
lock = asyncio.Lock()
control_lock = asyncio.Lock()


def load_token():
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = STATE / 'admin-token'
    try:
        with open(path, 'x', encoding='utf-8', opener=lambda p, f: os.open(p, f, 0o600)) as f:
            f.write(secrets.token_urlsafe(32))
    except FileExistsError:
        pass
    path.chmod(0o600)
    value = path.read_text().strip()
    if len(value) < 32:
        raise RuntimeError('Admin token must contain at least 32 characters')
    return value


@asynccontextmanager
async def lifespan(app):
    global TOKEN
    TOKEN = os.environ.get('HOME_AI_ADMIN_TOKEN') or load_token()
    if len(TOKEN) < 32:
        raise RuntimeError('HOME_AI_ADMIN_TOKEN must contain at least 32 characters')
    yield


app = FastAPI(title='Home AI', version='0.1.0', lifespan=lifespan, docs_url=None, redoc_url=None)


@app.middleware('http')
async def security_headers(request: Request, call_next):
    # Bearer auth is required even for loopback: Tailscale's proxy also uses loopback.
    if request.url.path.startswith('/api/') and request.method not in ('GET', 'HEAD'):
        supplied = request.headers.get('authorization', '').removeprefix('Bearer ')
        if not TOKEN or not hmac.compare_digest(supplied.encode(), TOKEN.encode()):
            return JSONResponse({'detail': 'Unlock maintenance with the server admin key.'}, status_code=401)
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
    response.headers['Cache-Control'] = 'no-store'
    return response


def command(args, timeout=8):
    env = os.environ.copy()
    env['PATH'] = '/opt/homebrew/bin:/usr/local/bin:/Applications/Ollama.app/Contents/Resources:' + env.get('PATH', '')
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=timeout, env=env, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None


def tailscale_status():
    result = command(['tailscale', 'status', '--json'], 3)
    if result is None:
        return {'state': 'Unavailable', 'dns': '', 'chat_url': None, 'dashboard_url': None}
    try:
        info = json.loads(result.stdout)
        own = info.get('Self') or {}
        dns = own.get('DNSName', '').rstrip('.')
        state = info.get('BackendState', 'Unknown')
        serve = command(['tailscale', 'serve', 'status', '--json'], 3)
        config = json.loads(serve.stdout) if serve and serve.returncode == 0 else {}
        web = config.get('Web', {})
        def served(port, target):
            handlers = web.get(f'{dns}:{port}', {}).get('Handlers', {})
            return handlers.get('/', {}).get('Proxy', '').rstrip('/') == target
        running = state == 'Running' and bool(dns)
        return {'state': state, 'dns': dns,
                'chat_url': f'https://{dns}' if running and served(443, SERVICES['open_webui'][1]) else None,
                'dashboard_url': f'https://{dns}:8443' if running and served(8443, f'http://127.0.0.1:{PORT}') else None}
    except (ValueError, TypeError):
        return {'state': 'Unavailable', 'dns': '', 'chat_url': None, 'dashboard_url': None}


def hardware():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(str(ROOT))
    chip = platform.processor() or platform.machine()
    if platform.system() == 'Darwin':
        result = command(['sysctl', '-n', 'machdep.cpu.brand_string'])
        if result and result.returncode == 0:
            chip = result.stdout.strip()
    return {'chip': chip, 'os': platform.system(), 'hostname': socket.gethostname(),
            'uptime_seconds': int(time.time() - psutil.boot_time()),
            'cpu': {'used_pct': psutil.cpu_percent(interval=0.15)},
            'memory': {'total_gb': round(memory.total / 1024**3, 1), 'used_gb': round(memory.used / 1024**3, 1), 'used_pct': memory.percent},
            'disk': {'free_gb': round(disk.free / 1024**3, 1), 'used_pct': disk.percent}}


async def probe(client, key, spec):
    name, base, path = spec
    start = time.monotonic()
    try:
        response = await client.get(base + path)
        response.raise_for_status()
        online = True
    except httpx.HTTPError:
        online = False
    return key, {'name': name, 'online': online, 'latency_ms': round((time.monotonic() - start) * 1000) if online else None,
                 'port': urlparse(base).port, 'required': key in ('open_webui', 'ollama')}


async def models(client):
    result = {'installed': [], 'loaded': []}
    async def get(path):
        try:
            r = await client.get(SERVICES['ollama'][1] + path)
            r.raise_for_status()
            return r.json().get('models', [])
        except (httpx.HTTPError, ValueError):
            return []
    installed, loaded = await asyncio.gather(get('/api/tags'), get('/api/ps'))
    for item in installed:
        result['installed'].append({'name': item.get('name', ''), 'size_gb': round(item.get('size', 0) / 1024**3, 1),
                                    'params': item.get('details', {}).get('parameter_size', '')})
    result['loaded'] = [item.get('name') for item in loaded]
    return result


@app.get('/api/stats')
async def stats():
    async with lock:
        if cache['value'] is not None and time.monotonic() - cache['at'] < 5:
            return cache['value']
        async with httpx.AsyncClient(timeout=2, trust_env=False) as client:
            results, model_info, hw, network = await asyncio.gather(
                asyncio.gather(*(probe(client, key, spec) for key, spec in SERVICES.items())),
                models(client), asyncio.to_thread(hardware), asyncio.to_thread(tailscale_status))
        data = {'timestamp': int(time.time()), 'services': dict(results), 'ollama': model_info,
                'hardware': hw, 'tailscale': network, 'controls_enabled': CONTROL_ENABLED}
        cache.update(at=time.monotonic(), value=data)
        return data


@app.post('/api/unlock')
async def unlock():
    return {'status': 'ok'}


class ServiceAction(BaseModel):
    service: Literal['open_webui', 'ollama', 'n8n', 'whisper']
    action: Literal['start', 'stop', 'restart']


@app.post('/api/service')
async def service_action(form: ServiceAction):
    if not CONTROL_ENABLED:
        raise HTTPException(403, 'Service controls are available only on native macOS installations.')
    if control_lock.locked():
        raise HTTPException(409, 'Another service action is still running.')
    async with control_lock:
        script = ROOT / 'scripts' / 'service_control.sh'
        result = await asyncio.to_thread(command, ['bash', str(script), form.service, form.action], 90)
        cache['at'] = 0
        if result is None or result.returncode != 0:
            raise HTTPException(502, 'Service action did not complete. Check .home-ai/service-control.log on the server.')
        return {'status': 'ok', 'service': form.service, 'action': form.action}


@app.get('/health')
async def health():
    return {'status': 'ok'}


@app.get('/')
async def index():
    return FileResponse(STATIC / 'index.html')


@app.get('/assets/{name}')
async def asset(name: str):
    if name not in ('app.js', 'style.css', 'icon.svg', 'manifest.webmanifest'):
        raise HTTPException(404)
    return FileResponse(STATIC / name)


if __name__ == '__main__':
    uvicorn.run(app, host=os.environ.get('DASHBOARD_HOST', '127.0.0.1'), port=PORT, proxy_headers=False)

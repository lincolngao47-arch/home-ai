#!/usr/bin/env python3
"""Install macOS login agents for the hub and, optionally, native Open WebUI."""
import argparse
import os
from pathlib import Path
import platform
import plistlib
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def build_agent(label, command, environment):
    return {
        'Label': label,
        'ProgramArguments': command,
        'WorkingDirectory': str(ROOT),
        'EnvironmentVariables': environment,
        'RunAtLoad': True,
        'KeepAlive': True,
        'ThrottleInterval': 10,
        'StandardOutPath': str(ROOT / '.home-ai' / (label + '.log')),
        'StandardErrorPath': str(ROOT / '.home-ai' / (label + '.log')),
    }


def install(label, command, environment):
    agents = Path.home() / 'Library' / 'LaunchAgents'
    agents.mkdir(parents=True, exist_ok=True)
    state = ROOT / '.home-ai'
    state.mkdir(mode=0o700, exist_ok=True)
    path = agents / (label + '.plist')
    desired = build_agent(label, command, environment)
    domain = f'gui/{os.getuid()}'
    if path.exists() and plistlib.loads(path.read_bytes()) == desired:
        loaded = subprocess.run(['launchctl', 'print', domain + '/' + label], capture_output=True)
        if loaded.returncode == 0:
            print('Already configured:', label)
            return
    if path.exists():
        backup = state / (label + '.before.plist')
        if not backup.exists():
            shutil.copy2(path, backup)
    subprocess.run(['launchctl', 'bootout', domain + '/' + label], capture_output=True)
    # bootout can return before launchd has finished removing the old job.
    for _ in range(30):
        result = subprocess.run(['launchctl', 'print', domain + '/' + label], capture_output=True)
        if result.returncode != 0:
            break
        time.sleep(0.1)
    path.write_bytes(plistlib.dumps(desired))
    for attempt in range(10):
        result = subprocess.run(['launchctl', 'bootstrap', domain, str(path)], capture_output=True, text=True)
        if result.returncode == 0:
            break
        if attempt == 9:
            raise RuntimeError(f'Could not load {label}: {result.stderr.strip()}')
        time.sleep(0.2)
    print('Installed:', label)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chat', action='store_true', help='Also supervise an installed native Open WebUI')
    parser.add_argument('--offline', action='store_true', help='Use already-cached WebUI embedding models; run chat once before selecting this')
    parser.add_argument('--whisper', action='store_true', help='Supervise an existing whisper/whisper_server.py using HOME_AI_WHISPER_PYTHON')
    args = parser.parse_args()
    if platform.system() != 'Darwin':
        parser.error('macOS only; use your OS process manager on other platforms')
    python = Path(os.environ.get('HOME_AI_PYTHON', ROOT / '.venv' / 'bin' / 'python'))
    webui = Path(os.environ.get('HOME_AI_WEBUI_BIN', ROOT / '.webui-venv' / 'bin' / 'open-webui'))
    if not python.is_file():
        parser.error('Install the hub first, or set HOME_AI_PYTHON')
    if args.chat and not webui.is_file():
        parser.error('Install chat first, or set HOME_AI_WEBUI_BIN')
    whisper_python = os.environ.get('HOME_AI_WHISPER_PYTHON')
    if args.whisper and (not whisper_python or not Path(whisper_python).is_file() or not (ROOT / 'whisper/whisper_server.py').is_file()):
        parser.error('Whisper requires an existing server and HOME_AI_WHISPER_PYTHON with its dependencies')
    environment = {'PATH': '/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'}
    # Preserve an existing operator-selected listen address.
    previous = Path.home() / 'Library/LaunchAgents/com.homeai.dashboard.plist'
    old_host = plistlib.loads(previous.read_bytes()).get('EnvironmentVariables', {}).get('DASHBOARD_HOST', '127.0.0.1') if previous.exists() else '127.0.0.1'
    install('com.homeai.dashboard', [str(python), str(ROOT / 'dashboard/dashboard_server.py')],
            {**environment, 'DASHBOARD_HOST': os.environ.get('DASHBOARD_HOST', old_host)})
    if args.chat:
        chat_environment = {**environment, 'HOME_AI_WEBUI_BIN': str(webui), 'ENABLE_SIGNUP': 'false'}
        if args.offline:
            chat_environment.update(OFFLINE_MODE='true', HF_HUB_OFFLINE='1')
        install('com.homeai.open-webui', ['/bin/bash', str(ROOT / 'scripts/start_chat.sh')], chat_environment)
    if args.whisper:
        install('com.homeai.whisper', [whisper_python, str(ROOT / 'whisper/whisper_server.py')], environment)
    print('Services start after login and restart if they exit. Logs are in .home-ai/.')


if __name__ == '__main__':
    main()

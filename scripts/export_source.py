#!/usr/bin/env python3
"""Export an explicit source allowlist, never a copy of the live server folder."""
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
FILES=['README.md','LICENSE','.gitignore','dashboard/dashboard_server.py','dashboard/index.html','dashboard/app.js','dashboard/style.css','dashboard/icon.svg','dashboard/manifest.webmanifest','dashboard/requirements.txt','scripts/install.sh','scripts/start_dashboard.sh','scripts/start_chat.sh','scripts/service_control.sh','scripts/start_services.sh','scripts/stop_services.sh','scripts/check_health.sh','scripts/setup_tailscale.sh','scripts/export_source.py','tests/test_dashboard.py','docs/SETUP.zh-CN.md','docs/ARCHITECTURE.md','docs/ALTERNATIVES.md','docs/SECURITY.md','docs/VALIDATION.md','.github/workflows/checks.yml']
def export():
    target=ROOT/'release'/'home-ai-source.zip'
    target.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
        for name in FILES:
            path=ROOT/name
            if path.is_symlink() or not path.is_file():
                raise ValueError(f'Missing or symlinked source: {name}')
            archive.write(path,'home-ai/'+name)
    print(target)
if __name__=='__main__': export()

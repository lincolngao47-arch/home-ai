#!/usr/bin/env python3
"""Apply the optional chat stylesheet using the Python environment with Open WebUI."""
from pathlib import Path
import importlib.util
import hashlib
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
VERSION = 'homeai-' + hashlib.sha256((ROOT / 'webui/custom.css').read_bytes() + (ROOT / 'webui/loader.js').read_bytes()).hexdigest()[:12]


def main():
    spec = importlib.util.find_spec('open_webui')
    if spec is None or not spec.submodule_search_locations:
        raise SystemExit('Run this with the Python environment containing Open WebUI.')
    package = Path(next(iter(spec.submodule_search_locations)))
    index = package / 'frontend' / 'index.html'
    static = package / 'static'
    if not index.is_file() or not static.is_dir():
        raise SystemExit('This Open WebUI layout is not recognized; no files changed.')
    backup = ROOT / '.home-ai' / 'webui-ui-backup'
    backup.mkdir(parents=True, exist_ok=True)
    source_static = package / 'frontend' / 'static'
    targets = [static] + ([source_static] if source_static.is_dir() else [])
    for path in [index] + [directory / name for directory in targets for name in ('custom.css', 'loader.js')]:
        saved = backup / (('frontend-' if path.parent == source_static else '') + path.name)
        if path.exists() and not saved.exists():
            shutil.copy2(path, saved)
    for directory in targets:
        for name in ('custom.css', 'loader.js'):
            shutil.copy2(ROOT / 'webui' / name, directory / name)
    html = index.read_text()
    for name in ('custom.css', 'loader.js'):
        pattern = r'/static/' + re.escape(name) + r'(?:\?[^"\s<>]*)?'
        url = f'/static/{name}?v={VERSION}'
        if re.search(pattern, html):
            html = re.sub(pattern, url, html)
        else:
            tag = f'<link rel="stylesheet" href="{url}">' if name.endswith('.css') else f'<script src="{url}" defer></script>'
            html = html.replace('</head>', tag + '\n</head>')
    index.write_text(html)
    print('Applied chat polish and versioned assets. Backups: .home-ai/webui-ui-backup/')


if __name__ == '__main__':
    main()

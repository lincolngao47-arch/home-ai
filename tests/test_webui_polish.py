"""Check that the optional theme survives WebUI's startup asset copy."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('polish', ROOT / 'scripts/install_webui_polish.py')
polish = importlib.util.module_from_spec(spec)
spec.loader.exec_module(polish)


class WebUIPolishTests(unittest.TestCase):
    def test_startup_copy_keeps_new_assets_and_backups(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project, package = root / 'project', root / 'package'
            (project / 'webui').mkdir(parents=True)
            for name in ('custom.css', 'loader.js'):
                shutil.copy2(ROOT / 'webui' / name, project / 'webui' / name)
                for target in (package / 'static', package / 'frontend/static'):
                    target.mkdir(parents=True, exist_ok=True)
                    (target / name).write_text('old overlay asset')
            index = package / 'frontend/index.html'
            index.write_text('<head><script src="/static/loader.js"></script><link href="/static/custom.css"></head>')
            fake_spec = SimpleNamespace(submodule_search_locations=[str(package)])
            with patch.object(polish, 'ROOT', project), patch.object(polish.importlib.util, 'find_spec', return_value=fake_spec):
                polish.main()
                for name in ('custom.css', 'loader.js'):
                    # WebUI does this copy each time its service starts.
                    shutil.copy2(package / 'frontend/static' / name, package / 'static' / name)
                    self.assertEqual((package / 'static' / name).read_bytes(), (project / 'webui' / name).read_bytes())
                polish.main()
            self.assertEqual(index.read_text().count('/static/loader.js?v='), 1)
            self.assertEqual(index.read_text().count('/static/custom.css?v='), 1)
            self.assertEqual((project / '.home-ai/webui-ui-backup/loader.js').read_text(), 'old overlay asset')
            self.assertEqual((project / '.home-ai/webui-ui-backup/frontend-loader.js').read_text(), 'old overlay asset')

    def test_unknown_package_layout_leaves_files_alone(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory)
            marker = package / 'untouched'
            marker.write_text('original')
            fake_spec = SimpleNamespace(submodule_search_locations=[str(package)])
            with patch.object(polish.importlib.util, 'find_spec', return_value=fake_spec):
                with self.assertRaises(SystemExit):
                    polish.main()
            self.assertEqual(marker.read_text(), 'original')
            self.assertEqual(list(package.iterdir()), [marker])


if __name__ == '__main__':
    unittest.main()

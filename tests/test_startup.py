"""Exercise the chat launcher under the low limits that broke first-page loads."""
import os
from pathlib import Path
import resource
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ChatLauncherLimitsTests(unittest.TestCase):
    def launch_with_limits(self, soft, hard):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            executable = path / 'fake-webui'
            executable.write_text('#!/bin/bash\nulimit -Sn\n')
            executable.chmod(0o700)
            environment = {**os.environ, 'HOME_AI_WEBUI_BIN': str(executable), 'DATA_DIR': str(path / 'data')}
            def limits():
                resource.setrlimit(resource.RLIMIT_NOFILE, (soft, hard))
            result = subprocess.run(['bash', str(ROOT / 'scripts/start_chat.sh')], env=environment,
                                    capture_output=True, text=True, check=True, preexec_fn=limits)
            return int(result.stdout.strip())

    def test_low_inherited_soft_limit_is_raised(self):
        self.assertGreaterEqual(self.launch_with_limits(256, 16384), 8192)

    def test_lower_hard_limit_does_not_prevent_startup(self):
        self.assertEqual(self.launch_with_limits(256, 1024), 1024)

    def test_existing_higher_limit_is_preserved(self):
        self.assertEqual(self.launch_with_limits(12000, 16384), 12000)


if __name__ == '__main__':
    unittest.main()

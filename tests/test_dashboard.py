import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient

spec = importlib.util.spec_from_file_location('dashboard', Path(__file__).resolve().parents[1] / 'dashboard/dashboard_server.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.state = patch.object(m, 'STATE', Path(self.temp.name))
        self.state.start()
        self.client = TestClient(m.app)
        self.client.__enter__()
    def tearDown(self):
        self.client.__exit__(None,None,None)
        self.state.stop()
        self.temp.cleanup()
    def test_mutations_require_key_even_on_loopback(self):
        with patch.object(m, 'command') as command:
            r = self.client.post('/api/service', json={'service':'ollama','action':'stop'}, headers={'X-Forwarded-For':'127.0.0.1'})
            self.assertEqual(r.status_code,401)
            command.assert_not_called()
    def test_invalid_key_is_rejected(self):
        r = self.client.post('/api/unlock', headers={'Authorization':'Bearer wrong-key'})
        self.assertEqual(r.status_code,401)
    def test_unlock_and_invalid_service(self):
        headers = {'Authorization':'Bearer ' + m.TOKEN}
        self.assertEqual(self.client.post('/api/unlock',headers=headers).status_code,200)
        with patch.object(m, 'command') as command:
            r = self.client.post('/api/service',headers=headers,json={'service':'ollama; touch /tmp/pwn','action':'stop'})
            self.assertEqual(r.status_code,422)
            command.assert_not_called()
    def test_controls_can_be_disabled(self):
        with patch.object(m,'CONTROL_ENABLED',False):
            r = self.client.post('/api/service',headers={'Authorization':'Bearer '+m.TOKEN},json={'service':'ollama','action':'start'})
            self.assertEqual(r.status_code,403)
    def test_failure_is_not_reported_as_success(self):
        with patch.object(m,'CONTROL_ENABLED',True), patch.object(m,'command',return_value=None):
            r = self.client.post('/api/service',headers={'Authorization':'Bearer '+m.TOKEN},json={'service':'ollama','action':'start'})
            self.assertEqual(r.status_code,502)
    def test_private_token_and_stable_restart(self):
        path = Path(self.temp.name)/'admin-token'
        self.assertEqual(path.stat().st_mode & 0o777,0o600)
        self.assertEqual(m.load_token(),m.TOKEN)
        self.assertGreaterEqual(len(m.TOKEN),32)
    def test_database_routes_removed(self):
        self.assertEqual(self.client.get('/api/users').status_code,404)
    def test_static_and_headers(self):
        response=self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.headers['x-frame-options'],'DENY')
        self.assertNotIn('maximum-scale',response.text)
        for name in ('app.js','style.css','icon.svg','manifest.webmanifest'):
            self.assertEqual(self.client.get('/assets/'+name).status_code,200)
        self.assertEqual(self.client.get('/assets/admin-token').status_code,404)
        self.assertNotIn('access-control-allow-origin',response.headers)
    def test_tailscale_requires_matching_serve_route(self):
        from subprocess import CompletedProcess
        status=CompletedProcess([],0,'{"BackendState":"Running","Self":{"DNSName":"example.ts.net."}}','')
        empty=CompletedProcess([],0,'{}','')
        with patch.object(m,'command',side_effect=[status,empty]):
            self.assertIsNone(m.tailscale_status()['chat_url'])
        config=CompletedProcess([],0,'{"Web":{"example.ts.net:443":{"Handlers":{"/":{"Proxy":"http://127.0.0.1:3000"}}}}}','')
        with patch.object(m,'command',side_effect=[status,config]):
            self.assertEqual(m.tailscale_status()['chat_url'],'https://example.ts.net')
    def test_probes_report_offline_on_failure(self):
        import asyncio,httpx
        async def run():
            async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: httpx.Response(503))) as client:
                key, result = await m.probe(client,'test',('Test','http://localhost:1234','/health'))
                self.assertFalse(result['online'])
                self.assertIsNone(result['latency_ms'])
        asyncio.run(run())

if __name__ == '__main__': unittest.main()

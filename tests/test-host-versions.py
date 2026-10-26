import importlib.machinery
import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch
loader = importlib.machinery.SourceFileLoader('versions', str(Path(__file__).resolve().parents[1] / 'SOURCES/xcp-hl-versions'))
spec = importlib.util.spec_from_loader(loader.name, loader)
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)
class VersionsTest(unittest.TestCase):
    def test_fixed_commands_and_inventory(self):
        with patch.object(module.subprocess, 'check_output', return_value=b'1.2-3') as rpm, patch('builtins.open', return_value=io.StringIO("OTHER='x'\nBUILD_NUMBER='ce42'\n")):
            value = json.loads(module.versions(None, {'path': '/etc/shadow'}))
        self.assertEqual(value['iso'], 'ce42')
        self.assertEqual(value['xoa-proxy'], '1.2-3')
        self.assertEqual([c.args[0][-1] for c in rpm.call_args_list], list(module.PACKAGES))
    def test_absent_components(self):
        with patch.object(module.subprocess, 'check_output', side_effect=module.subprocess.CalledProcessError(1, 'rpm')), patch('builtins.open', side_effect=IOError):
            self.assertTrue(all(v is None for v in json.loads(module.versions(None, {})).values()))
if __name__ == '__main__': unittest.main()

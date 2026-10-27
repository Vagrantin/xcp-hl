import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('audit',Path(__file__).resolve().parents[1]/'ci/audit-product-rpms.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class Audit(unittest.TestCase):
    def test_publication_time_wins_over_list_and_commit_order(self):
        releases=[{'tag_name':'v1.0','published_at':'2026-10-27T01:00:00Z','created_at':'2026-10-27','draft':False}, {'tag_name':'v1.1','published_at':'2026-10-27T03:00:00Z','created_at':'2026-01-01','draft':False}]
        self.assertEqual(module.select_release(releases,r'v[0-9.]+')['tag_name'],'v1.1')
    def test_drafts_and_default_prereleases_do_not_count(self):
        with self.assertRaises(ValueError):module.select_release([{'tag_name':'v1','published_at':'now','prerelease':True}],r'v[0-9]+')
        self.assertEqual(module.select_release([{'tag_name':'v1','published_at':'now','prerelease':True}],r'v[0-9]+','v1')['tag_name'],'v1')
    def test_unsigned_nokey_and_bad_signatures_never_pass(self):
        for code,output in [(0,'file.rpm: digests OK'),(0,'file.rpm: NOKEY digests signatures OK'),(1,'file.rpm: digests signatures NOT OK')]:
            self.assertFalse(module.signature_ok(code,output))
        self.assertTrue(module.signature_ok(0,'file.rpm: digests signatures OK'))
    def test_only_flagged_license_payload_is_accepted(self):
        entries=module.license_entries('/opt/xo/LICENSE\t\t42\n/usr/share/licenses/xoa-hl/LICENSE\tl\t34520\n')
        self.assertEqual(entries,[{'path':'/usr/share/licenses/xoa-hl/LICENSE','size':34520}])
    def test_new_rpm_size_headers_and_directory_flags(self):
        rows='/usr/share/licenses/package\tl\t0\tdrwxr-xr-x\n/usr/share/licenses/package/LICENSE\tl\t(none)\t-rw-r--r--\n'
        self.assertEqual(module.license_entries(rows),[{'path':'/usr/share/licenses/package/LICENSE','size':None}])
    def test_unexpected_license_path_is_not_extracted(self):
        with self.assertRaises(ValueError):module.license_entries('/usr/share/licenses/../../etc/passwd\tl\t20\n')
if __name__=='__main__':unittest.main()

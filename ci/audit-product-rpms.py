#!/usr/bin/env python3
"""Read-only technical audit of published XCP-HL RPMs (#8, #272). Never installs RPMs."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
import urllib.parse
import urllib.request

PRODUCTS = {
    'xcp-hl': ('xcp-hl-release', r'v[0-9][0-9.]*', True),
    'xolite-ce': ('xo-lite-ce', r'v[0-9.]+-ce[0-9]+', True),
    'xoa-proxy': ('xoa-proxy', r'v[0-9][0-9.]*', True),
    'xoa-hl': ('xoa-hl', r'v.*-ce[0-9]+', False),
}
API = 'https://api.github.com/repos/Vagrantin/'


def api_json(path):
    request = urllib.request.Request(API + path, headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'XCP-HL-RPM-audit'})
    token = os.environ.get('GH_TOKEN')
    if token:
        request.add_header('Authorization', 'Bearer ' + token)
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read(8 * 1024 * 1024 + 1)
    if len(data) > 8 * 1024 * 1024:
        raise ValueError('GitHub metadata response too large')
    return json.loads(data)


def select_release(releases, pattern, tag=None):
    eligible = [r for r in releases if not r.get('draft') and r.get('published_at') and
                re.fullmatch(pattern, r.get('tag_name', '')) and
                (r.get('tag_name') == tag if tag else not r.get('prerelease'))]
    if not eligible:
        raise ValueError('No matching published RPM release')
    # Commit dates and raw API list order are not publication time.
    return max(eligible, key=lambda r: (r['published_at'], r['tag_name']))


def run(args):
    result = subprocess.run(args, capture_output=True, text=True, timeout=180)
    return result.returncode, result.stdout + result.stderr


def signature_ok(code, output):
    lower = output.lower()
    return code == 0 and 'digests signatures ok' in lower and not any(s in lower for s in ['nokey', 'not ok', 'unsigned', 'not trusted'])


def license_entries(output):
    entries = []
    for line in output.splitlines():
        parts = line.split('\t')
        if len(parts) != 3:
            continue
        path, flags, size = parts
        if 'l' not in flags:
            continue
        parsed = PurePosixPath(path)
        if not path.startswith('/usr/share/licenses/') or '..' in parsed.parts or not re.fullmatch(r'/[A-Za-z0-9_./+:-]+', path):
            raise ValueError('Unexpected flagged license path')
        entries.append({'path': path, 'size': int(size)})
    return entries


def public_bytes(url, limit):
    # Deliberately no GitHub token on public raw/download URLs or redirects.
    request = urllib.request.Request(url, headers={'User-Agent': 'XCP-HL-RPM-audit'})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError('Public reference exceeds size budget')
    return data


def download_asset(repo, asset, path):
    url = urllib.parse.urlsplit(asset['browser_download_url'])
    if url.scheme != 'https' or url.hostname != 'github.com' or not url.path.startswith('/Vagrantin/' + repo + '/releases/download/') or url.username:
        raise ValueError('Unexpected release asset URL')
    count = 0
    digest = hashlib.sha256()
    request = urllib.request.Request(asset['browser_download_url'], headers={'User-Agent': 'XCP-HL-RPM-audit'})
    with urllib.request.urlopen(request, timeout=180) as source, path.open('wb') as target:
        while True:
            chunk = source.read(1024 * 1024)
            if not chunk:
                break
            count += len(chunk)
            if count > 256 * 1024 * 1024:
                raise ValueError('RPM exceeds download budget')
            digest.update(chunk)
            target.write(chunk)
    if count != asset['size']:
        raise ValueError('Downloaded size differs from release metadata')
    return digest.hexdigest()


def license_bytes(rpm, path):
    # Stream only the selected file to stdout. Never extract paths to disk.
    with subprocess.Popen(['rpm2cpio', str(rpm)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as source:
        try:
            result = subprocess.run(['cpio', '--quiet', '-i', '--to-stdout', '--', '.' + path], stdin=source.stdout, capture_output=True, timeout=180)
            source.stdout.close()
            code = source.wait(timeout=30)
            if result.returncode != 0 or code != 0 or len(result.stdout) > 1024 * 1024:
                raise ValueError('Could not inspect packaged license bytes')
            return result.stdout
        except BaseException:
            source.kill()
            raise


def audit(repo, tag=None):
    package, pattern, host = PRODUCTS[repo]
    if tag is not None and not re.fullmatch(pattern, tag):
        raise ValueError('Invalid release tag for product')
    releases = [api_json(repo + '/releases/tags/' + urllib.parse.quote(tag, safe=''))] if tag else api_json(repo + '/releases?per_page=100')
    release = select_release(releases, pattern, tag)
    assets = [a for a in release['assets'] if re.fullmatch(re.escape(package) + r'-[0-9].*\.(?:noarch|x86_64)\.rpm', a['name']) and a.get('state') == 'uploaded']
    if len(assets) != 1:
        raise ValueError('Release must carry exactly one product RPM')
    asset = assets[0]
    commit = api_json(repo + '/commits/' + urllib.parse.quote(release['tag_name'], safe=''))['sha']
    if not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('Release tag does not resolve to a commit')
    base = f'https://raw.githubusercontent.com/Vagrantin/{repo}/{commit}/'
    key = public_bytes(base + 'xcp-ng-ce-public.asc', 128 * 1024)
    reference = public_bytes(base + 'LICENSE', 1024 * 1024)
    result = {'repository': 'Vagrantin/' + repo, 'tag': release['tag_name'], 'release_url': release['html_url'],
              'published_at': release['published_at'], 'source_commit': commit, 'asset': asset['name'],
              'expected_license_metadata': 'AGPL-3.0-only', 'checks': {}, 'license_files': []}
    with tempfile.TemporaryDirectory(prefix='rpm-audit-') as directory:
        root = Path(directory)
        rpm = root / 'product.rpm'
        result['sha256'] = download_asset(repo, asset, rpm)
        declared = asset.get('digest')
        result['checks']['asset_digest_when_provided'] = (declared == 'sha256:' + result['sha256']) if declared else None
        rpmdb = root / 'rpmdb'; rpmdb.mkdir()
        keypath = root / 'key.asc'; keypath.write_bytes(key)
        for args in [['rpm', '--dbpath', str(rpmdb), '--initdb'], ['rpm', '--dbpath', str(rpmdb), '--import', str(keypath)]]:
            code, output = run(args)
            if code:
                raise ValueError('Could not initialize isolated RPM key verification')
        code, output = run(['rpm', '--dbpath', str(rpmdb), '--checksig', str(rpm)])
        result['signature_output'] = output.replace(str(rpm), asset['name']).strip()
        result['checks']['signature_verified'] = signature_ok(code, output)
        # Keep query warnings separate from machine-readable metadata.
        queried = subprocess.run(['rpm', '-qp', '--qf', '%{NAME}\n%{VERSION}-%{RELEASE}\n%{LICENSE}\n%{PAYLOADCOMPRESSOR}\n', str(rpm)], capture_output=True, text=True, timeout=180)
        values = queried.stdout.strip().splitlines()
        if queried.returncode or len(values) != 4:
            raise ValueError('Could not query RPM metadata')
        name, version, license_id, compressor = values
        result.update(name=name, version=version, license=license_id, payload_compressor=compressor)
        result['checks']['package_name'] = name == package
        result['checks']['license_metadata'] = license_id == 'AGPL-3.0-only'
        result['checks']['host_payload_xz'] = compressor == 'xz' if host else None
        scripts = subprocess.run(['rpm', '-qp', '--scripts', str(rpm)], capture_output=True, text=True, timeout=180)
        result['checks']['scriptlets_expanded'] = scripts.returncode == 0 and not re.search(r'%\{[^}\n]+\}', scripts.stdout)
        files = subprocess.run(['rpm', '-qp', '--qf', '[%{FILENAMES}\t%{FILEFLAGS:fflags}\t%{FILESIZES}\n]', str(rpm)], capture_output=True, text=True, timeout=180)
        if files.returncode:
            raise ValueError('Could not query packaged license flags')
        entries = license_entries(files.stdout)
        result['checks']['nonempty_flagged_license'] = bool(entries) and all(e['size'] > 0 for e in entries)
        reference_hash = hashlib.sha256(reference).hexdigest()
        result['project_license_sha256'] = reference_hash
        for entry in entries[:16]:
            data = license_bytes(rpm, entry['path'])
            result['license_files'].append({**entry, 'sha256': hashlib.sha256(data).hexdigest(), 'matches_project_license': data == reference})
    result['technical_status'] = 'findings' if any(v is False for v in result['checks'].values()) else 'pass'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('rpm-audit'))
    parser.add_argument('--strict', action='store_true', help='fail on findings or unavailable evidence')
    args = parser.parse_args()
    refs = json.loads(os.environ.get('AUDIT_REFS_JSON', '{}'))
    if not isinstance(refs, dict) or set(refs) - PRODUCTS.keys() or not all(isinstance(v, str) and v for v in refs.values()):
        raise ValueError('AUDIT_REFS_JSON must map fixed product repositories to nonempty release tags')
    report = {'schema': 1, 'audited_at': datetime.now(timezone.utc).isoformat(), 'license_grant_review': 'pending maintainer confirmation', 'installation_and_host_validation': 'not performed', 'products': []}
    for repo in PRODUCTS:
        try:
            result = audit(repo, refs.get(repo))
        except Exception as error:
            result = {'repository': 'Vagrantin/' + repo, 'technical_status': 'unavailable', 'error': str(error)}
        report['products'].append(result)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    lines = ['# Published RPM technical audit', '', '| Repository | Release | Technical result |', '|---|---|---|']
    for p in report['products']:
        lines.append(f"| {p['repository']} | {p.get('tag', 'unavailable')} | {p['technical_status']} |")
    lines += ['', 'See report.json for exact commits, hashes, signature output, license metadata/files and individual checks.', '', 'This does not confirm license intent, bundled-license completeness, installation/upgrade or dom0 acceptance.']
    summary = '\n'.join(lines) + '\n'
    (args.output / 'summary.md').write_text(summary)
    print(summary)
    if args.strict and any(p['technical_status'] != 'pass' for p in report['products']):
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

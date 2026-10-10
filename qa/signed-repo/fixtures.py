#!/usr/bin/env python3
"""Fixtures for the signed yum repository validation plan (xcp-hl#144).

Runs on the fixture host (a disposable AlmaLinux VM, or any Linux box with
gpg, and createrepo_c + rpmsign for the optional `resigned-rpm` variant).
Never on a consumer under test, and never anywhere near the real signing key.

    fixtures.py mirror   BASEURL KEY.asc DEST     copy a published repo, verifying the whole chain
    fixtures.py variants DEST OUT                 build valid / unsigned / wrong-key / tampered trees
    fixtures.py repofile SHIPPED.repo SECTION URL OUT.repo
                                                  one test section per variant, settings copied
                                                  verbatim from the shipped section, only baseurl
                                                  (and gpgkey for key-swap, resigned-rpm) changed

Serve OUT over HTTP (python3 -m http.server -d OUT 8000) and point the
consumer at it with the generated .repo file. See qa/signed-repo-validation.md.
"""
import configparser
import gzip
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import xml.etree.ElementTree as ET

NS = {'repo': 'http://linux.duke.edu/metadata/repo',
      'common': 'http://linux.duke.edu/metadata/common'}

# Order matters only for readability of the generated .repo file.
VARIANTS = ['valid', 'unsigned', 'wrong-key', 'key-swap', 'tampered-repomd',
            'tampered-primary', 'tampered-rpm', 'resigned-rpm']


def die(msg):
    sys.exit('fixtures: ' + msg)


def sha(path, kind):
    h = hashlib.new(kind)
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def gpg(home, *args, **kw):
    return subprocess.run(['gpg', '--homedir', home, '--batch', '--yes'] + list(args),
                          check=True, **kw)


def repodata(root):
    """[(type, href, checksum_type, checksum)] from repodata/repomd.xml."""
    tree = ET.parse(os.path.join(root, 'repodata', 'repomd.xml'))
    out = []
    for d in tree.getroot().findall('repo:data', NS):
        c = d.find('repo:checksum', NS)
        out.append((d.get('type'), d.find('repo:location', NS).get('href'),
                    c.get('type'), c.text.strip()))
    return out


def packages(root):
    """[(href, checksum_type, checksum)] from the primary.xml the repo lists."""
    href = [h for t, h, _, _ in repodata(root) if t == 'primary'][0]
    opener = gzip.open if href.endswith('.gz') else open
    with opener(os.path.join(root, href), 'rb') as f:
        tree = ET.parse(f)
    out = []
    for p in tree.getroot().findall('common:package', NS):
        c = p.find('common:checksum', NS)
        out.append((p.find('common:location', NS).get('href'), c.get('type'), c.text.strip()))
    return out


def fetch(base, href, dest):
    path = os.path.join(dest, href)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with urllib.request.urlopen(base + href) as r, open(path, 'wb') as f:
        shutil.copyfileobj(r, f)
    return path


def mirror(baseurl, key, dest):
    base = baseurl.rstrip('/') + '/'
    if os.path.exists(dest):
        die(dest + ' exists, refusing to mix two mirrors')
    os.makedirs(dest)
    manifest = []
    for href in ('repodata/repomd.xml', 'repodata/repomd.xml.asc'):
        fetch(base, href, dest)

    with tempfile.TemporaryDirectory() as home:
        gpg(home, '--import', key, stderr=subprocess.DEVNULL)
        status = gpg(home, '--status-fd', '1', '--verify',
                     os.path.join(dest, 'repodata/repomd.xml.asc'),
                     os.path.join(dest, 'repodata/repomd.xml'),
                     stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode()
    valid = [l.split()[2] for l in status.splitlines() if l.startswith('[GNUPG:] VALIDSIG')]
    if not valid:
        die('repomd.xml signature did not verify against ' + key)
    print('repomd.xml  signature OK, signing key ' + valid[0])
    manifest.append(('repodata/repomd.xml', sha(os.path.join(dest, 'repodata/repomd.xml'), 'sha256')))

    for kind, href, ctype, want in repodata(dest):
        got = sha(fetch(base, href, dest), ctype)
        if got != want:
            die('%s %s: %s %s, repomd.xml says %s' % (kind, href, ctype, got, want))
        print('%-11s %s OK  %s' % (kind, ctype, href))
        manifest.append((href, got))

    for href, ctype, want in packages(dest):
        got = sha(fetch(base, href, dest), ctype)
        if got != want:
            die('%s: %s %s, primary says %s' % (href, ctype, got, want))
        print('package     %s OK  %s' % (ctype, href))
        manifest.append((href, sha(os.path.join(dest, href), 'sha256')))

    with open(os.path.join(dest, 'MANIFEST.sha256'), 'w') as f:
        f.writelines('%s  %s\n' % (h, p) for p, h in manifest)
    print('chain verified: repomd.xml signature -> metadata checksums -> %d package(s)'
          % len(packages(dest)))
    print('wrote ' + os.path.join(dest, 'MANIFEST.sha256'))


def flip(path):
    """Change one byte in the middle, size unchanged, so only a hash can catch it."""
    with open(path, 'r+b') as f:
        size = os.fstat(f.fileno()).st_size
        f.seek(size // 2)
        b = f.read(1)
        f.seek(size // 2)
        f.write(bytes([b[0] ^ 0x01]))


def throwaway_key(home, name):
    gpg(home, '--pinentry-mode', 'loopback', '--passphrase', '', '--quick-gen-key', '%s <qa@invalid>' % name,
        'rsa3072', 'sign', '1d', stderr=subprocess.DEVNULL)


def variants(src, out):
    if not os.path.isfile(os.path.join(src, 'repodata', 'repomd.xml.asc')):
        die(src + ' is not a signed mirror (run `mirror` first)')
    if os.path.exists(out):
        die(out + ' exists')
    os.makedirs(out)
    home = tempfile.mkdtemp(prefix='qa-gnupg-')
    try:
        for v in VARIANTS:
            if v == 'resigned-rpm' and not (shutil.which('rpmsign') and shutil.which('createrepo_c')):
                print('skip  resigned-rpm (needs rpmsign and createrepo_c)')
                continue
            d = os.path.join(out, v)
            shutil.copytree(src, d, ignore=shutil.ignore_patterns('MANIFEST.sha256'))
            repomd = os.path.join(d, 'repodata', 'repomd.xml')
            if v == 'unsigned':
                os.remove(repomd + '.asc')
            elif v == 'wrong-key':
                throwaway_key(home, 'QA wrong key')
                gpg(home, '--armor', '--detach-sign', '-u', 'QA wrong key',
                    '--output', repomd + '.asc', repomd)
            elif v == 'key-swap':
                # wrong-key, plus the attacker's public key served next to it:
                # what someone who can write to the Pages site can publish.
                throwaway_key(home, 'QA swapped key')
                gpg(home, '--armor', '--detach-sign', '-u', 'QA swapped key',
                    '--output', repomd + '.asc', repomd)
                with open(os.path.join(d, 'served-key.asc'), 'wb') as f:
                    f.write(gpg(home, '--armor', '--export', 'QA swapped key',
                                stdout=subprocess.PIPE).stdout)
            elif v == 'tampered-repomd':
                flip(repomd)
            elif v == 'tampered-primary':
                # yum 3.4 reads primary_db, dnf reads primary: tamper both.
                for kind, href, _, _ in repodata(d):
                    if kind in ('primary', 'primary_db'):
                        flip(os.path.join(d, href))
            elif v == 'tampered-rpm':
                for href, _, _ in packages(d):
                    flip(os.path.join(d, href))
            elif v == 'resigned-rpm':
                resign(home, d)
            print('built %s' % v)
    finally:
        shutil.rmtree(home, ignore_errors=True)


def resign(home, d):
    """Packages re-signed by an unrelated key, inside metadata that a *test* key
    signs correctly. Stands in for "a differently signed RPM named in
    legitimately signed metadata", which cannot be built without the real key."""
    throwaway_key(home, 'QA rpm signer')
    throwaway_key(home, 'QA trusted metadata key')
    env = dict(os.environ, GNUPGHOME=home)
    for href, _, _ in packages(d):
        rpm = os.path.join(d, href)
        subprocess.run(['rpmsign', '--delsign', rpm], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(['rpmsign', '--define', '_gpg_name QA rpm signer', '--addsign', rpm],
                       check=True, env=env, stdout=subprocess.DEVNULL)
    shutil.rmtree(os.path.join(d, 'repodata'))
    # Same flags as the publishing workflows, so XCP-ng 8.3 yum can read it.
    zck = subprocess.run(['createrepo_c', '--help'], stdout=subprocess.PIPE).stdout
    subprocess.run(['createrepo_c', '--database', '--compress-type=gz', '--checksum=sha256',
                    '--quiet', d] + (['--no-zck'] if b'--no-zck' in zck else []), check=True)
    repomd = os.path.join(d, 'repodata', 'repomd.xml')
    gpg(home, '--armor', '--detach-sign', '-u', 'QA trusted metadata key',
        '--output', repomd + '.asc', repomd)
    with open(os.path.join(d, 'trusted-test-key.asc'), 'wb') as f:
        f.write(gpg(home, '--armor', '--export', 'QA trusted metadata key',
                    stdout=subprocess.PIPE).stdout)


def repofile(shipped, section, url, out):
    src = configparser.RawConfigParser()
    src.optionxform = str
    if not src.read(shipped) or section not in src:
        die('no [%s] in %s' % (section, shipped))
    dst = configparser.RawConfigParser()
    dst.optionxform = str
    base = url.rstrip('/') + '/'
    for v in VARIANTS + ['outage']:
        s = 'qa-' + v
        dst[s] = dict(src[section])
        dst[s]['name'] = 'QA %s (%s)' % (v, section)
        # Nothing is served under /outage/: a 404, i.e. an unavailable repo.
        dst[s]['baseurl'] = base + v + '/'
        dst[s]['enabled'] = '0'
        if v == 'key-swap':
            dst[s]['gpgkey'] = base + v + '/served-key.asc'
        if v == 'resigned-rpm':
            dst[s]['gpgkey'] = base + v + '/trusted-test-key.asc'
    with open(out, 'w') as f:
        f.write('# Generated by qa/signed-repo/fixtures.py from [%s] in %s.\n'
                '# Every option is the shipped value except name, baseurl, enabled=0\n'
                '# and, for qa-key-swap and qa-resigned-rpm, gpgkey. Enable one with --enablerepo.\n\n'
                % (section, shipped))
        dst.write(f, space_around_delimiters=False)
    print('wrote %s (%d sections from [%s])' % (out, len(dst.sections()), section))


def main(argv):
    cmds = {'mirror': (mirror, 3), 'variants': (variants, 2), 'repofile': (repofile, 4)}
    if len(argv) < 2 or argv[1] not in cmds or len(argv) - 2 != cmds[argv[1]][1]:
        sys.exit(__doc__)
    cmds[argv[1]][0](*argv[2:])


if __name__ == '__main__':
    main(sys.argv)

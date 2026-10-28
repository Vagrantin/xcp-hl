# Signed yum repository validation

Out-of-band test plan for the signed XCP-HL yum repositories
([#144](https://github.com/Vagrantin/xcp-hl/issues/144)). It is a prerequisite
for the testing-to-stable cutover in
[#145](https://github.com/Vagrantin/xcp-hl/issues/145) /
[#154](https://github.com/Vagrantin/xcp-hl/issues/154), and is deliberately not
part of the documentation build.

**Status.** The dnf column below was rehearsed with dnf 4.14.0 (the dnf version
AlmaLinux 9 ships) against a synthetic repository signed the way CI signs the
real ones: a certify-only primary key, a signing subkey, and the publishing
workflows' `createrepo_c` flags. The yum 3.4.3 column (XCP-ng 8.3 dom0) is
**not yet run**: its expected messages are what to look for, to be replaced by
the observed ones on the first run. No case has been run against the live
repositories yet.

## What the configuration promises

Every shipped `.repo` file sets `repo_gpgcheck=1` and `gpgcheck=0`. Trust is a
chain:

```
repomd.xml.asc --GPG--> repomd.xml --sha256--> primary.xml.gz / primary.sqlite.gz --sha256--> each .rpm
```

So a consumer rejects unsigned, wrongly signed or modified metadata, and any RPM
whose bytes differ from what the signed metadata records. It does **not** check
the RPM's own signature: a differently signed RPM named in legitimately signed
metadata installs. That is the deliberate trade-off for rpm 4.11 reporting
`NOKEY` on subkey signatures (see the comment in
[`SOURCES/xcp-hl.repo`](../../SOURCES/xcp-hl.repo)); this plan records it, it
does not report package-signature enforcement.

| Consumer | `.repo` file | Sections | `gpgkey` | `skip_if_unavailable` |
|---|---|---|---|---|
| XCP-HL host, managed | `xcp-hl/SOURCES/xcp-hl.repo` (from `xcp-hl-release`) | `xcp-hl-base`, `xcp-hl-xolite`, `xcp-hl-xoa-proxy` | `file:///etc/pki/rpm-gpg/RPM-GPG-KEY-xcp-ng-ce` | `True` |
| XCP-HL host, bootstrap | `xcp-hl/pages/xcp-hl.repo` | same three | `https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc` | `True` |
| XOA-HL appliance | `xoa-hl/SOURCES/xoa-hl.repo` (from `xoa-hl`) | `xoa-hl` | `https://vagrantin.github.io/xoa-hl/xcp-ng-ce-public.asc` | `False` |
| (published, not in the documented steps) | `xolite-ce/pages/xcp-hl-xolite.repo` | `xcp-hl-xolite` | `https://vagrantin.github.io/xolite-ce/xcp-ng-ce-public.asc` | `False` |

Expected key (`xcp-ng-ce-public.asc`, identical in all three repositories):

```
pub  rsa4096/6DA00DCA5BBA215A [C] expires 2028-05-09
     2F59 1DB9 D2C1 28C4 C3D9  63F4 6DA0 0DCA 5BBA 215A
sub  rsa4096/A056674605F2A215 [S] expires 2027-05-10
sub  rsa4096/F6A459A03D61B7AB [S] expires 2027-05-10
```

After 2027-05-10 every case below fails on signature until the subkeys are
extended and the key re-imported; a run after that date tests the key, not the
repository.

## Environments

| Role | What | Notes |
|---|---|---|
| **H** host consumer | XCP-ng 8.3, fresh install (a nested VM is fine) | yum 3.4.3 / rpm 4.11. Runs the documented bootstrap. For the upgrade path, also a host installed from an older XCP-HL ISO |
| **A** appliance consumer | XOA-HL, freshly deployed from the current XVA | AlmaLinux 9, dnf. Snapshot it before part 2 |
| **F** fixture host | disposable AlmaLinux 9 VM reachable from H and A | `dnf install -y gpg createrepo_c rpm-sign python3`. Serves the tampered repositories. Never holds the real signing key |

[`fixtures.py`](fixtures.py) runs on F only.

## Recording a run

Keep with the result, in the release or production-readiness notes:

- date, this plan's commit, and per consumer `rpm -q yum rpm` or `rpm -q dnf rpm`;
- `rpm -q xcp-hl-release xo-lite-ce xoa-proxy` (H) or `rpm -q xoa-hl` (A), and the ISO / XVA tag the consumer came from;
- the `MANIFEST.sha256` files from P3 (the exact `repomd.xml` and RPM digests tested);
- the full terminal transcript (`script -a qa-144-$(hostname).log`);
- one row per case:

```
| case | consumer | exit | reason line (verbatim) | verdict: pass / fail / inconclusive |
```

## Part 1: legitimate repositories

**P1 reachable.** On H and A:

```bash
for u in xcp-hl/repo xolite-ce xoa-proxy xoa-hl; do
  for f in repomd.xml repomd.xml.asc; do
    curl -fsS -o /dev/null -w "%{http_code} $u/$f\n" \
      "https://vagrantin.github.io/$u/8.3/x86_64/repodata/$f"
  done
done
```

Expect `200` for all eight.

**P2 key.** On F:

```bash
curl -fsSO https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc
gpg --show-keys --with-subkey-fingerprints xcp-ng-ce-public.asc
for u in xoa-hl xolite-ce; do
  curl -fsS "https://vagrantin.github.io/$u/xcp-ng-ce-public.asc" | cmp - xcp-ng-ce-public.asc
done
```

Expect the fingerprints above and no `cmp` output.

**P3 chain, out of band.** On F, for each repository:

```bash
for u in xcp-hl/repo xolite-ce xoa-proxy xoa-hl; do
  ./fixtures.py mirror "https://vagrantin.github.io/$u/8.3/x86_64/" \
    xcp-ng-ce-public.asc "mirror-${u%%/*}"
done
```

Expect `repomd.xml  signature OK, signing key <one of the two subkey
fingerprints>`, an `OK` line per metadata file and per package, and
`chain verified`. Any mismatch exits non-zero. Keep `mirror-*/MANIFEST.sha256`.

**P4 host, documented steps only.** On H, run the
[first-time setup](../../docs/updates.md#first-time-setup-on-an-existing-host)
verbatim, then:

```bash
yum makecache </dev/null           # without -y: record the key prompt (key ID, fingerprint, From)
yum -y makecache                   # expect the three xcp-hl repos with no signature error
ls -d /var/lib/yum/repos/*/*/xcp-hl-*/gpgdir   # per-repository keyring that repo_gpgcheck uses
ls -l /etc/yum.repos.d/xcp-hl.repo*             # .rpmorig next to the packaged copy
yum repolist enabled | grep xcp-hl              # exactly xcp-hl-base, xcp-hl-xolite, xcp-hl-xoa-proxy
yum --showduplicates list xcp-hl-release xo-lite-ce xoa-proxy
yum install --assumeno xo-lite-ce xoa-proxy     # dependency resolution, versions, arch, repository
yum -y install --downloadonly --downloaddir=/root/qa-dl xo-lite-ce xoa-proxy
sha256sum /root/qa-dl/*.rpm                     # must equal the mirror-*/MANIFEST.sha256 lines
rpm -K /root/qa-dl/*.rpm                        # NOKEY expected on rpm 4.11: why gpgcheck=0, not a failure
yum -y install xo-lite-ce xoa-proxy
yum info installed xo-lite-ce xoa-proxy | grep -E '^(Name|Arch|Version|Release|From repo)'
```

Record whether the `rpm --import` in the documented steps is what makes the
key prompt go away, or whether yum still imports into `gpgdir` from `gpgkey=`
(on dnf the per-repository keyring is filled only from `gpgkey=`).

**P5 appliance.** On A (`xoa-hl` is already installed):

```bash
dnf --refresh makecache </dev/null      # record the key prompt; dnf shows the *signing subkey* fingerprint
dnf --refresh -y makecache
ls -d /var/cache/dnf/xoa-hl-*/pubring   # keyring; survives `dnf clean all` (rehearsed)
dnf --showduplicates list xoa-hl
dnf -y reinstall --downloadonly --downloaddir=/root/qa-dl xoa-hl
sha256sum /root/qa-dl/*.rpm             # equals mirror-xoa-hl/MANIFEST.sha256
curl -fsSO https://vagrantin.github.io/xoa-hl/xcp-ng-ce-public.asc
rpm --import xcp-ng-ce-public.asc; rpm -K /root/qa-dl/*.rpm   # informational: rpm 4.16 checks subkey signatures
dnf repoquery --requires xoa-hl; dnf install --assumeno xoa-hl
```

## Part 2: rejected repositories

On F, build the variants from a P3 mirror and generate a test `.repo` file from
the **file actually installed on the consumer** (copy it to F first), so every
option except `baseurl` is the shipped value:

```bash
./fixtures.py variants mirror-xolite-ce out-host
./fixtures.py repofile xcp-hl.repo.from-H xcp-hl-xolite http://F:8000/out-host qa-host.repo
./fixtures.py variants mirror-xoa-hl out-appl
./fixtures.py repofile xoa-hl.repo.from-A xoa-hl http://F:8000/out-appl qa-appl.repo
firewall-cmd --add-port=8000/tcp
python3 -m http.server 8000
```

`F` stands for the fixture host's address. Copy `qa-host.repo` to H and `qa-appl.repo` to A under `/etc/yum.repos.d/`. Its
sections are `enabled=0`, so they never mix with the real ones. Run each case
with only that section enabled, cache cleared, and `skip_if_unavailable` forced
off so a rejection cannot be swallowed:

```bash
# H
v=wrong-key
yum --disablerepo='*' --enablerepo=qa-$v clean all
yum --disablerepo='*' --enablerepo=qa-$v --setopt=qa-$v.skip_if_unavailable=0 -y \
  reinstall --downloadonly --downloaddir=/root/qa-$v xo-lite-ce; echo "exit=$?"

# A
v=wrong-key
dnf --disablerepo='*' --enablerepo=qa-$v clean all
dnf --refresh --disablerepo='*' --enablerepo=qa-$v --setopt=qa-$v.skip_if_unavailable=0 -y \
  reinstall --downloadonly --downloaddir=/root/qa-$v xoa-hl; echo "exit=$?"
```

Cleaning matters: with metadata still cached, a changed repository is not
fetched at all and the run exits 0 (rehearsed).

| Case | What `fixtures.py` changed | dnf 4.14 (rehearsed) | yum 3.4.3 (look for, then record) | Verdict rule |
|---|---|---|---|---|
| `valid` | nothing (control) | `Complete!`, exit 0 | exit 0 | Must pass in the same session before any negative counts. Downloaded RPM sha256 equals `MANIFEST.sha256` |
| `unsigned` | `repomd.xml.asc` removed | `GPG verification is enabled, but GPG signature is not available ... 404 for .../repomd.xml.asc`, exit 1 | failure naming `repomd.xml.asc` or the signature | non-zero exit **and** the signature reason |
| `wrong-key` | `repomd.xml` signed by a throwaway key | `repomd.xml GPG signature verification error: Bad GPG signature`, exit 1 | `repomd.xml signature could not be verified for qa-wrong-key` | same |
| `tampered-repomd` | one byte of `repomd.xml` flipped, old signature kept | same as `wrong-key` | same as `wrong-key` | same |
| `tampered-primary` | one byte of `primary.xml.gz` and `primary.sqlite.gz` flipped | `Downloading successful, but checksum doesn't match. Calculated: ... Expected: ...` for the primary file, exit 1 | `Metadata file does not match checksum` | non-zero exit **and** a checksum reason |
| `tampered-rpm` | one byte in the middle of each RPM, size unchanged, metadata untouched | `[MIRROR] <rpm>: Downloading successful, but checksum doesn't match`, exit 1 | `Package does not match intended download` | non-zero exit **and** a checksum reason; nothing left in `/root/qa-tampered-rpm` |
| `outage` | nothing served (404) | `Cannot download repomd.xml ... All mirrors were tried`, exit 1 | `HTTP Error 404` on `repomd.xml` | Control for the reason classes: an availability error, never a signature one |
| `resigned-rpm` | RPMs re-signed by an unrelated key, metadata regenerated and signed by a **test** key the section trusts | installs, exit 0. With `--setopt=qa-resigned-rpm.gpgcheck=1`: `Public key for ... is not installed`, `GPG check FAILED` | installs (NOKEY with `gpgcheck=1`) | Documents the limitation: not rejected for its RPM signature while `gpgcheck=0` |
| `key-swap` | `wrong-key`, plus the throwaway public key served in the tree and named by `gpgkey=` | **imports the served key and installs, exit 0**, also when the real key is already in that repository's keyring | record | Documents behaviour for an `https` `gpgkey` on the same origin as `baseurl` (finding 1) |

A negative case that fails for an availability reason (404 on `repomd.xml`,
connection refused, DNS, proxy) is **inconclusive**, not a pass: the fixture
host was not reached, so nothing was verified.

**With the shipped `skip_if_unavailable`.** Repeat `wrong-key` and `outage`
without the `--setopt`, using `check-update`:

- H ships `True`. Rehearsed on dnf, both cases print `Ignoring repositories:
  qa-...` and `check-update` **exits 0**; only an install of a package from that
  repository fails. A tampered repository therefore looks exactly like an
  outage: no XCP-HL updates listed, stock XCP-ng updates still shown. That is
  the intended behaviour of the setting, and why a zero exit is never evidence
  of a security check passing.
- A ships `False`: both exit 1. Also record what `systemctl start
  xoa-hl-check-update.service` writes to `/run/xoa-hl/status` for each.

Optional, H: point `baseurl` of the real `[xcp-hl-xolite]` at
`http://F:8000/out-host/wrong-key/` and open the host's Patches tab in XOA-HL.
Expect stock updates listed and no XCP-HL ones, with no error. `yum -y
reinstall xcp-hl-release` restores the file.

## Part 3: upgrades

| Case | Steps | Expect |
|---|---|---|
| U1 host packages | `yum -y downgrade xo-lite-ce-<previous> xoa-proxy-<previous>` (from P4's `--showduplicates`), then `yum -y update xo-lite-ce xoa-proxy` | newest versions back, `From repo` the matching `xcp-hl-*` id |
| U2 repository config | `yum -y downgrade xcp-hl-release-<previous>`, `yum -y update xcp-hl-release` | `/etc/yum.repos.d/xcp-hl.repo` byte-identical to `SOURCES/xcp-hl.repo` of the installed release (not `%config`, so replaced outright); signature checks still pass without a new key prompt |
| U3 older ISO | a host installed from an older XCP-HL ISO: `yum -y update` | lands on the versions recorded in P3's manifests |
| U4 appliance | `dnf -y downgrade xoa-hl-<previous>`, then `systemctl start xoa-hl-update.service` and `journalctl -u xoa-hl-update.service` | newest `xoa-hl`, `xo-server` restarted once after the transaction |

The rollback window is the five most recent releases each publishing workflow
keeps (`KEEP_RELEASES`), so U1, U2 and U4 need at least two published releases.

## Findings from the rehearsal

1. **An `https` `gpgkey` on the same origin as `baseurl` does not protect
   against a compromised Pages site.** On dnf 4.14 with `-y`, a `repomd.xml`
   that fails verification makes dnf import whatever key `gpgkey=` serves and
   retry, even when the real key is already in that repository's keyring. The
   XOA-HL appliance ships `gpgkey=https://vagrantin.github.io/xoa-hl/...`, and
   `xoa-hl-update.service` runs `dnf -y update`. The managed host copy is not
   affected this way (its key is a local file), the bootstrap copy is until
   `xcp-hl-release` replaces it (yum behaviour still to record). A possible
   follow-up, outside this issue: ship the key inside the `xoa-hl` package and
   point `gpgkey` at a `file://` path, as `xcp-hl-release` does, and publish the
   primary fingerprint in the docs so the bootstrap `rpm --import` can be
   checked.
2. Answering `N` to the key prompt (or running without `-y` and no terminal) is
   reported by dnf as `Bad GPG signature`, the same text as a wrong key. Read
   P4/P5's prompt record before calling a failure tampering.
3. Cached metadata hides repository changes; every case starts from `clean all`
   and `--refresh`.
4. `dnf clean all` keeps the per-repository keyring under `/var/cache/dnf/*/pubring`.

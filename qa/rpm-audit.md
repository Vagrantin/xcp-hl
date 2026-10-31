# Published RPM evidence for issues #8 and #272

The `Audit published product RPMs` workflow inspects the four public product
release streams without building or installing packages and without signing
secrets. It downloads actual published bytes, resolves each release's source
commit and uses the public key and project LICENSE from that immutable commit.
Only a temporary RPM verification database is used.

The report records exact tags, source commits, asset SHA-256, available GitHub
asset digest comparison, signature output, package/license metadata, host xz
compression, unresolved scriptlet macros and nonempty `%license`-flagged files.
License file hashes and comparison with the project LICENSE are evidence, not
a determination of the intended grant or bundled-dependency license expression.
No packaged scriptlet executes; license bytes are streamed to stdout rather
than extracting archive paths to disk. The report contains no private key or
credential.

PR runs test the reader and produce a nonblocking report of existing releases;
a published artifact finding is distinct from a code-test failure. Manual runs
can use strict mode for release acceptance and select exact tags with `refs`,
for example `{"xolite-ce":"v0.21.0-ce36"}`. Explicit prerelease tags are allowed;
omitted products select the newest published stable matching RPM release by
`published_at`, never commit date or raw API order.

`published-rpm-audit` contains report.json and summary.md. A technical pass does
not confirm license intent, completeness of bundled licenses, RPM 4.11 subkey
support, signed repository metadata, installation/upgrade or appliance QA. The
host's deliberate `gpgcheck=0` / `repo_gpgcheck=1` settings are not changed. A
findings or unavailable result must not be described as a pass.

Summary: XCP-ng HomeLab Edition repository configuration and GPG key
Name:    xcp-hl-release
Version: %{_version}
# _release, _shortcommit and _version are all passed via --define from CI, the
# same convention xo-lite-ce and xoa-proxy use. The leading number is the CI run
# counter, so every build has a distinct, upgradeable NEVRA even when the
# version is unchanged; g<shortcommit> identifies the xcp-hl commit that
# produced this repository configuration, which Version alone does not.
Release: %{_release}.g%{_shortcommit}.xcpng8.3
License: AGPL3-only
URL:     https://github.com/Vagrantin/xcp-hl
BuildArch: noarch

Source0: xcp-hl.repo
Source1: RPM-GPG-KEY-xcp-ng-ce

%description
Repository configuration and package signing key for XCP-ng HomeLab Edition.

Installs /etc/yum.repos.d/xcp-hl.repo, which defines the three XCP-HL package
repositories (xcp-hl-base, xcp-hl-xolite, xcp-hl-xoa-proxy), and registers the
community signing key with rpm.

Owning this configuration in a package is what makes it maintainable: yum never
re-reads a .repo file once it is present, so before this package existed a
change to repository configuration could only reach a host by asking its
administrator to curl the file again. Repository settings now ship through the
same channel as everything else, via yum update xcp-hl-release.

The repository IDs defined here are also a contract with xoa-hl, which patches
Xen Orchestra to pass them to XCP-ng's updater.py plugin so that XCP-HL updates
appear in the Patches tab in XOA.

%prep
# Nothing to unpack: both sources are installed verbatim.

%build
# Nothing to build.

%install
install -d -m 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/yum.repos.d/xcp-hl.repo

install -d -m 755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-xcp-ng-ce

# The scriptlet below is written out longhand rather than with any macro. This
# package is built in a rockylinux:9 container but targets a CentOS 7 dom0, and
# an undefined macro survives into the scriptlet as a literal line starting with
# a percent sign, which the target shell reads as a job spec ("fg: no job
# control") and fails on. That stranded a package in the rpmdb once already on
# xoa-proxy, so CI greps the built package for it and this scriptlet uses none.
%post
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-xcp-ng-ce >/dev/null 2>&1 || :

%files
%config(noreplace) %{_sysconfdir}/yum.repos.d/xcp-hl.repo
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-xcp-ng-ce

%changelog

---
title: Other XCP-ng clients
weight: 6
translationKey: other-clients
aliases: ["/other-clients.html", "/docs/guides/other-clients/"]
---

XO Lite and Xen Orchestra are not the only way to manage an XCP-ng host.
Here are other community tools worth knowing about.

## XenAdminQt

[XenAdminQt](https://github.com/benapetr/XenAdminQt) is a C++/Qt6 rewrite of
the classic XenAdmin thick client, bringing it to macOS and GNU/Linux (and,
in principle, any platform Qt supports) instead of Windows-only .NET. It
talks to the same xapi JSON-RPC API that powers XCP-ng and XenServer, giving
you host/VM consoles and performance metrics from a native desktop app.
It is BSD-2-Clause licensed and still alpha, but it's a great
alternative for anyone who wants a native, cross-platform desktop client
for XCP-ng. Shout-out to [benapetr](https://github.com/benapetr) for
building and maintaining it.

## XenCenter (xenadmin) XCP - Jumphp

[XenCenter (xenadmin) XCP - Jumphp](https://jumphp.net/xencenter-xenadmin-xcp-jumphp)
is a JumPHP port of the XenCenter (xenadmin) client for managing XCP-ng and
XenServer servers: pools, hosts, VMs, storage, networks and performance. It
runs in the browser (as a web app or PWA) and on the desktop, and it also
works on phones. The source is on
[git.jumphp.net](https://git.jumphp.net/duchnoun/xencenter-xenadmin-xcp-jumphp).
Shout-out to duchnoun for building and maintaining it.

---

Know another XCP-ng client worth listing here? Open an issue on
[xcp-hl](https://github.com/Vagrantin/xcp-hl).

---
layout: default
title: Other XCP-ng Clients
nav_order: 4.5
---

# Other XCP-ng Clients
{: .no_toc }

XO Lite and Xen Orchestra are not the only way to manage an XCP-ng host.
Here are other community tools worth knowing about.

---

## XenAdminQt

[XenAdminQt](https://github.com/benapetr/XenAdminQt) is a C++/Qt6 rewrite of
the classic XenAdmin thick client, bringing it to macOS and GNU/Linux (and,
in principle, any platform Qt supports) instead of Windows-only .NET. It
talks to the same xapi JSON-RPC API that powers XCP-ng and XenServer, giving
you host/VM consoles and performance metrics from a native desktop app.
It is BSD-2-Clause licensed and still alpha quality, but it's a great
alternative for anyone who wants a native, cross-platform desktop client
for XCP-ng. Shout-out to [benapetr](https://github.com/benapetr) for
building and maintaining it.

---

Know another XCP-ng client worth listing here? Open an issue or PR on
[xcp-hl](https://github.com/Vagrantin/xcp-hl).

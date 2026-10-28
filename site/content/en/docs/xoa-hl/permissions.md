---
title: "Manage users, groups and permissions"
linkTitle: "Users and permissions"
description: "Create users and groups, grant access to a VM, delegate resources and test LDAP or SAML sign-in."
weight: 70
translationKey: xoa-manual-permissions
translationStatus: source
sourceRevision: sha256:f565451a1844a1556c044e9aee08213bbb2c4d048289c39c26260b5d6676aa9d
glossaryTerms: ["appliance", "vm", "host", "pool"]
---

Create a test user, give it access to one VM, then try a group, a delegated resource set and an external sign-in (LDAP or SAML). You work as an administrator in the **XOA-HL appliance**, and sign in as the test user in a second, separate browser session. Use a disposable test VM. Keep your administrator session open throughout. Never change the last administrator account, or your own rights, while you test. To add one-time codes to a local account's sign-in, see [Protect sign-in with a one-time code](/docs/xoa-hl/sign-in-otp/).

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261022-a280852`, package `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Based on the released code; not yet tested on a lab system. Permissions control what a user can do, not what the user can read: in this release, any signed-in account can read the whole inventory through the API. In this build's default open-source plan, the code enables the ACL and Self service screens: no Vates subscription is needed.
{{< /callout >}}

**D3 observations (2026-10-28):** one normal test account and one disposable guest on XOA-HL `v5.113.2_e281c536-ce47` (`ca44911`), on one nested XCP-HL v8.3-ce44 host. In the web interface, the account with no grants saw "There are no VMs!". Settings users and ACL pages returned "Page not found". Viewer start and edit requests were refused with "not enough permissions" and left the VM unchanged. With Operator, start worked, but rename and delete were refused. Start was still refused after the Viewer grant was revoked. These are the access restrictions enforced by the web interface and its action requests in the [D3 record](https://github.com/Vagrantin/xcp-hl/issues/198#issuecomment-6459388202). Group grants in operation were not tested; the group procedures below remain based on source review.

The API object list is not limited to granted objects ([#309](https://github.com/Vagrantin/xcp-hl/issues/309)), so do not give API access to an account that must not see the inventory.

## Know the two kinds of roles {#roles}

**Settings → Users** (`/#/settings/users`) sets each account's global permission:

- **User** is a normal account.
- **Admin** is an administrator. It bypasses every object rule.

An access rule (ACL) gives a user or a group a role on one object. The object role **Admin** is not the global **Admin**: it applies only to the selected object and its scope.

| Object role | What it allows |
| --- | --- |
| Viewer | View |
| Operator | View and operate |
| Admin | View, operate and administer |

Start with **Viewer** on one test VM. A rule on a host or a pool can give access to more objects than a rule on one VM. A rule for a group applies to all its members. Permissions add up, and there is no rule that denies access. Removing one rule does not remove access that still comes from another group, object or parent object.

## Give a test user access to one VM {#vm-access}

These four steps form one test: create a normal user, give it **Viewer** on one disposable VM, check what it can do, then remove the access.

### Create a test user

1. In **Settings → Users**, create a separate test user with its own email or login and a unique password.
2. Select **User**, not **Admin**. Check the permission that the account shows.
3. In the second browser session, sign in as this user. Note what it can see before you add any rule.

Check that this session really is the test user, not a reused administrator login. Do not use real credentials, and never write passwords in your notes. Keep the test user: the group test below uses it again.

### Grant Viewer on one VM {#grant-viewer}

1. As the administrator, open **Settings → ACLs** (`/#/settings/acls`).
2. Select only the test user as the subject, only the disposable VM as the object, and **Viewer** as the role. Select **Create**.
3. Check the subject, object and role of the new row.

Do not select all objects or the whole pool. The form accepts several subjects and objects, and creates one rule for each pair. Check identities rather than similar display names. Object and tag filters select the objects that exist now; they set no rule for future objects.

### Check what the user can do

1. In the test user's session, refresh the page or sign in again.
2. Check that the VM is visible and that its basic details can be read.
3. Check that start, stop and administration actions are not available. If an action can still be requested, it must be refused, and the VM must not change.

Run this test only on the disposable VM. A hidden button alone does not prove that the server refuses the action.

If an action succeeds unexpectedly, stop. As the administrator, check the account's global permission, its groups and any other rule on the VM, its host or its pool. Do not widen permissions to fix an access error you cannot explain. If the ACL page is missing, note the versions and the error and [report it](/docs/xoa-hl/troubleshooting/). Do not assume that a paid plan of another edition is needed.

### Revoke and check again

1. As the administrator, remove the exact test rule.
2. In the test user's session, refresh or sign in again. Check that the VM access has gone.
3. Check that your administrator can still sign in and manage the intended objects.

If access remains, look for other direct, group and inherited rules: removing one row does not remove every grant.

**Check:** the user could read the VM but not change it, and lost access once you removed the rule. Note the account type, the rule's scope, and the expected and actual results, without credentials.

Keep the test user until all the tests on this page are done. Backup-job delegation and API token scope are not covered here. Before wider changes, see [Hosts and pools](/docs/xoa-hl/hosts-pools/) and [export your configuration](/docs/xoa-hl/configuration-backup/).

## Grant access through local groups {#group-access}

A group applies its object rules to all its members. Adding a user to a group does not change the user's global permission.

**Before you start**

- Finish [Give a test user access to one VM](#vm-access). Its direct rule must be removed, and the user must get no access to the VM from another group or a parent object.
- Use the same normal test user and the same disposable VM.
- Keep a second normal test account outside the group, to compare with.
- Keep the administrator session open.

### Create the group and its rule

1. Open **Settings → Groups** (`/#/settings/groups`). Enter a distinct name, such as `lab-vm-viewers`, in **New group name** and select **Create**.
2. Check that the new group has no users. If the name already exists, choose another one: do not reuse a group you do not know, with its grants.
3. In **Settings → ACLs**, select only this group as the subject, only the test VM as the object, and **Viewer** as the role. Select **Create**, then check the exact group, VM and role in the new row.
4. Check that both normal accounts still see only what they saw before. An empty group gives no access.

### Add the user and check access

1. In **Groups**, in the **Add user** column of this group, select only the test user. The change is sent at once; there is no separate save button.
2. Expand the **Users** count with the plus icon and check the login.
3. In **Settings → Users**, check that the user's groups include this group, and that the account is still **User**. After any error, refresh both views: the two membership records are written separately, so one list that looks right is not enough.
4. In the member's session, refresh or sign in again. Check that the user can read the VM, and that start, stop and administration are unavailable or refused without changing the VM.
5. Check that the second account still has no access to the VM.

If the results differ, stop. Check the actual identity, global permission, groups and all direct and parent rules. Do not add wider grants to make the test pass.

### Remove the member

1. In **Groups**, expand the member list and select the remove icon next to the exact test login. The removal is sent at once, without confirmation.
2. Check that the login has left the group, and that the group has left the user's details.
3. In the former member's session, refresh or sign in again. Check that the group's VM access has gone.

The group's rule stays in place: any other members keep its access.

### Check that grants add up

1. Add the user back to the group and check that Viewer access returns.
2. Add a separate direct **Viewer** rule for this user on the same VM.
3. Remove only the group's rule on the VM. The user can still read the VM through the direct rule.
4. Remove the direct rule and check again. With no other grant, the access disappears, even though the user is still a member.

A missing group rule does not deny anything, and a global **Admin** bypasses all object rules.

### Clean up the group test

1. Remove the test rules while their users and groups still exist.
2. Remove the test memberships, then check the results for both normal accounts.
3. Check the row and name of the empty test group. Select **Delete group** on that row and confirm. The confirmation does not name the group, so identify it before you open it.
4. Refresh the Groups, ACLs and Users views. Keep the independent administrator.

XO removes a deleted group's rules and memberships in the background. The group disappearing does not prove that every related record is gone. The ACL table can hide rows whose subject no longer exists. If a request failed or the records disagree, stop. Note the identities and errors without secrets, and [report the inconsistency](/docs/xoa-hl/troubleshooting/) before you retry or delete anything else.

Groups synchronized from an authentication provider are not covered here, nor are nested groups, renaming and wider delegation. Their local name and member controls are restricted. Do not use **Synchronize LDAP groups**, or detach an authentication provider, to get around these limits.

## Test a delegated resource set quota {#resource-set-delegation}

A resource set lets a normal user create VMs from chosen templates, SRs and networks, within CPU, RAM and disk limits (quotas). Here you test one set, for one user, on a disposable pool.

**Before you start**

- Use only a disposable pool and a dedicated normal test user with no broad rule on that pool.
- Keep an independent administrator session, and an independent backup of anything you want to keep.
- Do not add a production user, and do not share production storage or networks.
- Use two browser sessions: the XOA-HL administrator session, and a separate session for the normal user.

### Create the resource set

1. As the administrator, choose one disposable pool, one known stopped template, one writable test SR with enough free space, and one isolated lab network that the eligible hosts can reach.
2. Note their exact UUIDs, and the template's CPU, RAM and disk defaults. If the template's disks or network cannot be placed on these resources, stop.
3. Check that the test user is **User**, not a global **Admin**, and cannot create a VM in this pool yet.
4. Open **Self service → Resource sets** (`/#/self`) and select **New**. Give the set a unique lab name. Select only that user and that pool, then only the chosen **Templates**, **SRs** and **Networks**.
5. Check the host list. The editor shows eligible and excluded hosts, based on SR and network access. At least one intended host must be eligible.
6. Set finite values in **Maximum CPUs**, **Maximum RAM** and **Maximum disk space**. They must allow one small VM from the template, but stay below the over-limit request you will try next.
7. Leave **Share VMs by default** off, add no IP pool, and select **Save**. The editor creates the set, then edits it: after a save error, refresh the list and look for an empty or partial set before you retry.
8. Reload the set. Check its ID, user, templates, SRs, networks, hosts and the three limits. Note the current usage, normally zero.

If the page shows an upgrade prompt, or the set is missing, note the version and stop. Do not assume that a Vates plan is needed, and do not bypass the interface with an unreviewed API call.

### Check the quota

1. In the normal user's session, open **New VM** (`/#/vms/new`) and select the exact resource set.
2. Request a VM that exceeds the CPU limit. Keep the template, SR, network, RAM and disk valid. The server must refuse it, with no new VM and no unexpected disk.
3. As the administrator, check the inventory and the quota usage. A hidden control alone does not prove that the limit is enforced. If a partial VM or disk exists, stop and list it before any cleanup.
4. As the normal user, request one VM within every limit, using only the selected objects. Leave it stopped. Remove or disconnect inherited VIFs before any isolated start.
5. Check the new VM's UUID, its disk SR, its network, its resource set, and the quota's **Used** and **Total** values.
6. Check that the normal user can see and administer this VM, and that another normal account without the set cannot.

Never test the limit on a production VM. By default, XO gives the VM's creator the object role **Admin** on it. Turning on **Share VMs by default** extends this to the set's users. The test user needs no administrator rule on the whole pool.

**Check:** the over-limit request was refused without leftovers, and the VM within the limits appears in the quota usage.

### Remove the user from the set

1. As the administrator, remove the test user from the set. Refresh the normal user's session.
2. Check that the user can no longer select the set, or create another VM through it.
3. Check the remaining direct or inherited rules on the existing VM separately. Removing a user from a set removes the set's VM rules, but another grant can keep access.

If access or usage does not match, stop, and note the set and VM IDs and the error without secrets. Do not use **Recompute all limits** as a repair you cannot explain.

### Clean up the resource set test

1. Stop the new VM and confirm its exact VM and VDI IDs. Remove its VIFs.
2. Delete **only** that disposable VM. Check that its disks and snapshots were handled as you intended.
3. Refresh the quota usage and the set's VM count. Check that no VM remains in the set.
4. Select **Delete resource set** on the exact set. Deleting a set only detaches its VMs; it does not delete them.
5. Check the normal user, the independent administrator and the pool inventory again.

Note the expected and actual IDs, the refusals, the quota figures and the cleanup, without credentials. Group subjects, IP pools, default sharing, several VMs at once, cleanup after a failed creation and production delegation are not covered here.

## Test an external LDAP sign-in {#ldap-sign-in}

An LDAP sign-in can create an XO account, or link to an existing one. Use a disposable directory and one dedicated, non-administrator test identity.

{{< callout type="warning" >}}
The defaults are `createUserOnFirstSignin = true` and `mergeProvidersUsers = true`. A directory username that matches a local XO username can therefore link to that account and clear its local password. Use a test username that matches **no** existing XO account.
{{< /callout >}}

**Before you start**

- Keep an independent local administrator session and a recovery path.
- As the administrator, note the image, package and XO versions and the effective authentication settings. Keep a private [configuration export](/docs/xoa-hl/configuration-backup/).
- In **Settings → Plugins** (`/#/settings/plugins`), check that `auth-ldap` is listed with a version. Note its configuration, loaded and auto-load states, without secrets. If it is missing, or already serves real users, stop.
- With the directory owner, prepare an isolated LDAPS or StartTLS endpoint with a trusted CA, a unique and stable user ID attribute, a narrow user base and filter, and a dedicated search identity if needed.
- Do not change the last local administrator, or an existing provider, to make this test work.

### Configure and load the plugin

1. During an approved lab window, enter in the plugin form only the values from the directory owner: URI, CA path, certificate checking on, StartTLS choice, base, user filter, ID attribute and search credentials.
2. Leave **Synchronize groups** unset. It can import memberships and change who can access what.
3. Check the TLS identity and reachability separately. Never turn off certificate checking to hide an error.
4. Save the configuration. Then load the plugin and read back its loaded and auto-load states. Loading from this page also turns on auto-load.

Saving alone does not prove that sign-in works. Keep secrets private: out of screenshots, logs and issue reports.

### Sign in once and check the account

Do **not** use **Test** as a harmless connection check. It runs the real sign-in path, which can create an XO account and, if configured, synchronize groups.

1. In a fresh, separate browser session, sign in once with the unique directory test identity.
2. From the administrator session, check the new XO user ID, its provider, its global permission (**User**), its groups and what it can see. A successful sign-in grants no object access by itself.
3. Give this account **Viewer** on one disposable VM only, as in [Grant Viewer on one VM](#grant-viewer). In its session, check that it can read the VM, and that operate and administer actions are missing or refused without any change.
4. Remove that exact rule. In a refreshed session, check that the access has gone.
5. Try a wrong directory password, without disclosing it. Check that the independent local administrator can still sign in.

If an existing XO account is linked, an unexpected administrator role or group appears, or the provider or certificate result is unclear: stop, keep sanitized evidence and follow the owner's recovery plan. Do not sign in again or grant more rights.

### Clean up the LDAP test

1. Remove only the test rules and any test membership. Sign out of the external session.
2. Unload `auth-ldap` and read back its loaded and auto-load states. The local administrator must keep working.
3. Before you delete the test account, identify the exact user, its tokens and its rules. Deleting the account and purging the plugin configuration are separate actions. Never purge a provider that serves other users.

If loading, sign-in or unloading fails, save the sanitized errors and the actual user and provider states before you retry. Never relax TLS checks or merge accounts to work around a failure. Note the provider, version, TLS trust, identity mapping, user and rule IDs before and after, the allowed and refused results, and the local sign-in you kept. Group synchronization, directory outages, credential rotation, identity renames, tokens, OTP and failover are not covered here.

## Test an external SAML sign-in {#saml-sign-in}

You need an isolated identity provider (IdP) application, one uniquely named non-administrator test identity and an independent local XO administrator. The plugin takes the XO username from the profile attribute named in `usernameField`.

{{< callout type="warning" >}}
With the default `createUserOnFirstSignin` and `mergeProvidersUsers` settings, a username that matches an existing XO account can link to it and clear its local password. Never test with an existing XO username or a production single sign-on (SSO) application.
{{< /callout >}}

**Before you start**

- With the IdP owner, note the image, package, XO and plugin versions, the effective authentication settings and the public HTTPS address. Keep a private [configuration export](/docs/xoa-hl/configuration-backup/).
- Check that `auth-saml` is listed in **Settings → Plugins** (`/#/settings/plugins`) and serves no real users.
- Agree on a stable, unique profile attribute for `usernameField`. Before you load the plugin, check its test value against **all** XO usernames.
- Keep a working local administrator session and a separate console recovery path.
- If the public address, the proxy or the account mapping is unclear, stop.

### Register the appliance with the IdP

1. Register only this lab service provider with the IdP. Its callback URL must match `https://<appliance-name>/signin/saml/callback`, reachable from outside. Check the exact DNS name, the certificate trust and the redirect through any proxy.
2. Get the IdP's **signing certificate**, entry point and agreed issuer through the owner's private channel. This certificate is not the appliance's HTTPS certificate.
3. Require a signed SAML response or assertion, as agreed with the IdP owner. The plugin defaults `wantAssertionsSigned` and `wantAuthnResponseSigned` are both `false`, but that does **not** make unsigned messages acceptable.

Review these options with the IdP owner. Never weaken signature or TLS checks to hide a mismatch.

### Configure, load and sign in

1. Enter only the lab certificate, entry point, issuer and username field, and any callback or strictness options that the owner approved.
2. Save the configuration. Then load the plugin and read back its loaded and auto-load states. Saving alone does not activate it; loading from this page also turns on auto-load.
3. In a fresh, separate browser session, start the SAML sign-in from the XO sign-in page. Authenticate once with the assigned lab identity.
4. Ask the IdP owner to confirm the signed response and the selected attribute, without publishing the assertion.

Never paste certificates, assertions, profile data or session tokens into public issues.

### Check the new account

1. From the administrator session, check the **new** XO user ID, its `saml` provider, its global permission (**User**), its groups and what it can see.
2. Give it **Viewer** on one disposable VM only, as in [Grant Viewer on one VM](#grant-viewer). Check read access and a refused operation.
3. Remove that exact rule. In a refreshed session, check that the access has gone.
4. Ask the IdP owner to refuse an unassigned lab control identity in a fresh session. This tests a new sign-in, not the revocation of existing XO tokens.
5. Check that the local administrator can still sign in.

If an existing user is linked, a privileged role appears, the attribute is missing, or the signature or callback result is unclear: stop and keep only sanitized evidence. When the username field is missing, the plugin logs the full profile, so treat failure logs as sensitive.

### Clean up the SAML test

1. Sign out of the SAML test session and remove the test rules.
2. Unload only the isolated `auth-saml` plugin. Check its loaded and auto-load states, and the local sign-in.
3. Before you delete the account, list the exact test user and its tokens. Signing out, or disabling the provider, does not prove that existing XO tokens are invalid. Never purge a provider that serves real users.

On failure, note the redacted callback and error, and the actual user, provider and token states, before you retry. Note the callback address, the IdP certificate identity and expiry, the signing policy, the mapped attribute, the plugin state, user and rule IDs before and after, the results and the local access you kept, without secrets. IdP outages, signing-key rotation, clock skew, attribute changes, token and session revocation, OTP and production federation are not covered here.

{{< details title="Sources" closed="true" >}}
- **Users, ACLs and build plan**: [users UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js), [ACL UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/acls/index.js), [build plan default](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js), [roles and global admin bypass](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/acls.mjs), [object permission inheritance](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-acl-resolver/index.js), [xoa-hl build script](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
- **Groups**: [groups UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/groups/index.js), [group API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/group.mjs), [membership and deletion](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs), [combined user and group ACLs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/acls.mjs), [subject selector](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/select-objects.js).
- **Resource sets**: [resource-set editor and plan gate](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/self/index.js), [resource-set API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/resource-set.mjs), [constraints, quota accounting and deletion](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/resource-sets.mjs), [VM creation and ACL](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [New VM resource-set selection](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js).
- **LDAP**: [schema, TLS, test, registration and optional group sync](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server-auth-ldap/src/index.js), [plugin page: configuration, loading and test](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/plugins/index.js), [user registration and username collision handling](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs), [authentication defaults](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml), [XOA-HL build workspaces](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh), [RPM content](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec).
- **SAML**: [plugin schema, profile mapping and registration](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server-auth-saml/src/index.js), [web callback, sign-in and token creation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [plugin loading page](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/plugins/index.js), [user collision behavior](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs), [upstream XO 5 SAML guide](https://docs.xen-orchestra.com/users-and-access/users#saml).
{{< /details >}}

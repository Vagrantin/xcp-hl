---
title: Manage users, groups and permissions
description: Check direct and local-group Viewer grants, membership and revocation on one disposable VM.
weight: 26
translationKey: xoa-manual-permissions
translationStatus: source
sourceRevision: sha256:a166e82b0ae994e465cf73b0b63ffb66552e8f8eba7e7968c2e7040d49f3d93d
glossaryTerms: ["appliance", "vm", "host", "pool"]
---

Use an existing administrator session in the **XOA-HL appliance**, a disposable VM and a separate browser session for a new test user. Keep the administrator session available throughout the exercise. Do not change the last administrator's account or your own rights while testing.

{{< callout type="info" >}}
Source-reviewed preview for image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` and XO 5.113.2. Source review finds the ACL screen enabled by the build's default open-source plan; installed UI and allow/deny/revocation tests remain pending. This is not a Vates subscription requirement.
{{< /callout >}}

## 1. Distinguish account and object roles

**Settings → Users** (`/#/settings/users`) assigns a global account permission. **User** is a normal account; **Admin** is an administrator that bypasses object ACL checks. An object-level **Admin** grant is a different concept: it applies to the selected object and its permission scope.

| Object ACL role | Granted operations |
| --- | --- |
| Viewer | View |
| Operator | View and operate |
| Admin | View, operate and administrate |

Start with **Viewer** on one test VM. A host or pool grant can give broader object access than a single-VM grant. A grant to a group applies to all its members. Permissions are additive: removing one ACL does not revoke access still provided through another group, object or parent grant. There is no deny rule in this pilot.

## 2. Create a normal test identity

In **Settings → Users**, create a separate test user with an email/login and a unique password. Select **User**, not global **Admin**. Confirm the account's displayed permission. Do not use production credentials or include passwords in your evidence record.

Log in as that user in the separate browser session and record its starting visibility before adding an ACL. Ensure this is actually the test identity, not a reused administrator login. Keep the original administrator session open to correct or revoke the test grant.

## 3. Grant Viewer on one VM

As the administrator, open **Settings → ACLs** (`/#/settings/acls`). Select only the test user as the subject, only the disposable VM as the object and **Viewer** as the role; then add the rule. Check the resulting row's subject, object and role. Do not select all objects or grant access to the whole pool for this exercise.

The form permits multiple subjects and objects, creating a rule for each combination. Object/tag filters help select current objects; this exercise does not establish a policy for future objects. Confirm identities rather than relying on similar display names.

## 4. Check visibility and restricted actions

Refresh or log in again as the normal user. Check that the intended VM is visible and its basic details can be read. Check that start/stop and administrative actions are unavailable; if an operation can be requested, it must be refused without changing the VM. Use only the disposable VM for this negative test. Do not treat a hidden button alone as complete backend authorization acceptance.

If an action succeeds unexpectedly, stop the exercise. Inspect global account permission, group membership and other VM/host/pool grants as the administrator. Do not broaden permissions to fix an unexplained access error. If the ACL page is absent on the installed release, record versions and the error and [report it](/docs/xoa-hl/troubleshooting/); do not assume another edition's paid tier applies.

## 5. Revoke and check again

As the administrator, remove the precise test ACL. Refresh or log in again as the test user and verify that the VM's access has gone. If it remains, inspect other direct, group and inherited grants; removing one row is not a universal revocation. Recheck that the retained administrator can still log in and manage the intended objects.

Record the account type, ACL scope and expected/actual results without credentials. Keep the test identity for the local-group exercise below; delete it only after all exercises are complete. This pilot does not validate every delegated operation, resource sets, external authentication, backup-job delegation or API-token scope. Use [host/pool ownership](/docs/xoa-hl/hosts-pools/) and [configuration export](/docs/xoa-hl/configuration-backup/) before wider changes.

[Protect a local account’s sign-in with one-time codes (OTP)](/docs/xoa-hl/sign-in-otp/).

## 6. Grant access through a local group {#group-access}

Use a new local group, the normal test user from section 2 and the same disposable VM. Complete section 5 first: the direct test ACL must be removed, and the user must have no remaining access through another group or parent object. Keep a second normal test account outside the group as a control and retain the administrator session. A group applies its object ACLs to its members; adding a user does not change that account's global permission.

1. Open **Settings → Groups** (`/#/settings/groups`). Enter a distinct name such as `lab-vm-viewers` in **New group name** and select **Create**. Check that the new group has no users. If the name already exists, choose another name rather than reusing an unfamiliar group and its grants.
2. In **Settings → ACLs**, select only this group as the subject, only the test VM as the object and **Viewer** as the role. Create the rule and check the exact group/VM/role row. An empty group does not give the test user access: verify both normal accounts still have their baseline visibility.
3. Back in **Groups**, select only the intended user in that group's **Add user** column. Selecting the user sends the membership change immediately; there is no separate Save button. Expand the **Users** count with the plus icon and check the login. In **Settings → Users**, inspect that user's group count/details and confirm it includes this group; recheck that the account is still **User**. Refresh both views after any error: the two membership records are separate writes, so one successful-looking list is not sufficient.
4. Refresh or sign in again as the member. Verify the VM can be read, while start/stop and administrative operations remain unavailable or are refused without changing this disposable VM. Check the control account still lacks the VM grant. If results differ, stop and inspect the actual identity, global permission, memberships and all direct/parent ACLs; do not add broader grants to make the test pass.
5. In **Groups**, expand the member list and use the remove icon next to the exact test login. This sends removal immediately without a confirmation dialog. Check that the login has gone from the group and the group has gone from the user's details. Refresh/sign in again and verify the former member loses this group's VM access. The group ACL remains: other members, if any, keep its grant.

To check additive grants, add the user back and confirm Viewer access returns. Add a separate direct **Viewer** ACL for that user on the same VM, then remove only the group's VM ACL. The user should still read the VM through the direct ACL. Remove that direct ACL and recheck access; with no other grants, the VM access should disappear even while group membership remains. A missing group rule is not a deny rule, and a global administrator bypasses these object ACL checks.

For cleanup, remove the test ACLs while their subjects still exist, remove the test memberships and verify both normal accounts' results. Only then recheck the empty local test group’s row/name, select **Delete group** on that row and confirm deletion. The confirmation is generic; identify the group before opening it. Refresh the group/ACL/user views and retain the independent administrator. Group deletion schedules ACL and membership cleanup asynchronously; the group disappearing is not proof that every related record was cleaned. The ACL table can hide rows whose subject no longer exists. If a request failed or records disagree, stop, record sanitized identities/errors and [report the inconsistency](/docs/xoa-hl/troubleshooting/) before retrying or deleting more objects.

Provider-synchronized groups are outside this exercise. Their local name/membership controls are restricted; do not press **Synchronize LDAP groups** or detach an authentication provider to bypass those restrictions. Group nesting, renaming, external directory synchronization and wider delegation still need separate acceptance. A bounded resource-set pilot follows.

## 7. Test one delegated resource set and its quota {#resource-set-delegation}

This **source-reviewed preview** applies to XO 5.113.2 in `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38`. The pinned UI shows **Self service** when the build plan exceeds 3; the released build script does not override the upstream default open-source plan 5. Neither source fact proves the installed menu or an enforced quota. Use only a disposable pool and a dedicated normal test user with no broad pool ACL. Retain an independent administrator session and an independent backup of anything you intend to preserve. Do not add a production subject or share production storage/network access.

1. As administrator in the **XOA-HL browser**, choose one disposable pool, one stopped, known template, one writable test SR with enough free capacity, and one isolated lab network reachable on eligible hosts. Record the exact object UUIDs and the template's CPU, RAM and disk defaults. If the template's inherited disks or network cannot be placed on the selected resources, stop. Confirm the test user is **User**, has no global Admin permission and cannot create a VM in this pool before the new grant.
2. Open **Self service → Resource sets** (`/#/self`). Choose **New**, give the set a unique lab name, select only that user and pool, then only the chosen **Templates**, **SRs** and **Networks**. The editor displays eligible/excluded hosts based on SR and network reachability; verify at least one intended host is eligible. Set finite **Maximum CPUs**, **Maximum RAM** and **Maximum disk space** high enough for one small VM made from the selected template, but below the proposed over-limit request. Leave **Share VMs by default** off, use no IP pool, and choose **Save**. The new-set UI creates the set and then edits it: after any save error, refresh the list and look for an empty or partial set before retrying.
3. Reload the set as administrator. Check its ID, subject, pool-derived template/SR/network objects, host list and all three quota totals. Record current usage, normally zero before the first test VM. If the installed page shows an upgrade prompt or the set is missing, record the release and stop; do not assume a Vates plan or bypass the UI with an unreviewed API call.
4. In the separate **normal-user browser**, open **New VM** (`/#/vms/new`) and select the exact resource set. Request a configuration that exceeds its CPU quota while keeping the template, SR, network, RAM and disk otherwise valid. The server should refuse the request without a new VM or unexpected disk; check the inventory and quota usage from the administrator view. A hidden control alone does not prove enforcement. If a partial VM/disk exists, stop and inventory it before cleanup. Do not test the limit against a production VM.
5. Request one VM within every limit, using only the selected objects. Leave it stopped and remove or disconnect inherited VIFs before any isolated boot. Check the new VM UUID, disk SR, network selection, resource-set association and the quota **Used/Total** readback. Verify that the normal user can see and administer this new VM while an independent normal account without the set cannot. Creation grants object Admin to the creator by default; switching on default sharing broadens this to the set's subjects. No blanket pool administrative grant is required for the tested subject.
6. As administrator, remove the test user from the set and refresh the normal-user session. Verify it can no longer select the set or create another VM through it. Inspect any remaining direct or inherited ACL on the existing VM separately: removing a subject removes set-related VM ACLs, but another grant can keep access. Stop if access or usage disagrees; record sanitized set/VM IDs and the error. Do not use **Recompute all limits** as an unexplained repair.

For cleanup, stop the new VM and confirm its exact VM/VDI IDs, remove its VIFs, then delete **only** that disposable VM and verify its disks and snapshots have been handled as intended. Refresh quota usage and the set's VM count; confirm there are no surviving set VMs before selecting **Delete resource set** on the exact set. Deleting a set dissociates its VMs; it is not a VM-deletion operation. Recheck the normal user, independent administrator and pool inventory. Record expected and actual IDs, refusals, quota figures and cleanup without credentials. Installed plan availability, actual quota enforcement, failed-create cleanup, group subjects, IP pools, default sharing, multi-VM concurrency and production delegation remain pending lab acceptance.

## Sources

XO 5 pin `e281c536`: [users UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js), [ACL UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/acls/index.js), [build plan default](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js), [roles and global admin bypass](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/acls.mjs) and [object permission inheritance](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-acl-resolver/index.js). Package build: [xoa-hl build script](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).

[groups UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/groups/index.js) / [group API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/group.mjs) / [membership/delete implementation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs) / [combined user/group ACLs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/acls.mjs) / [subject selector](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/select-objects.js).

[resource-set editor and plan gate](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/self/index.js) / [resource-set API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/resource-set.mjs) / [constraints, quota accounting and deletion](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/resource-sets.mjs) / [VM creation and ACL](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs) / [New VM resource-set selection](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js).

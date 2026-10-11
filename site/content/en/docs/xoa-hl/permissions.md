---
title: Manage users and permissions
description: Create a normal user and check a Viewer grant on one disposable VM.
weight: 26
translationKey: xoa-manual-permissions
translationStatus: source
sourceRevision: sha256:d8daa96b46c3ce4ed28fa321add33fe542bcc8706409be2deec2fa44af49cfcb
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

Start with **Viewer** on one test VM. A host, pool or group grant can give broader access than a single-VM grant. Permissions are additive: removing one ACL does not revoke access still provided through another group, object or parent grant. There is no deny rule in this pilot.

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

Record the account type, ACL scope and expected/actual results without credentials. Delete the test identity only after the exercise is complete. This pilot does not validate every delegated operation, resource sets, external authentication, backup-job delegation or API-token scope. Use [host/pool ownership](/docs/xoa-hl/hosts-pools/) and [configuration export](/docs/xoa-hl/configuration-backup/) before wider changes.

## Sources

XO 5 pin `e281c536`: [users UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js), [ACL UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/acls/index.js), [build plan default](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js), [roles and global admin bypass](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/acls.mjs) and [object permission inheritance](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-acl-resolver/index.js). Package build: [xoa-hl build script](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).

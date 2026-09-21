---
title: Manage groups and membership
description: Use a group to apply a common permission set to several users. Verify the resulting grants whenever
  membership changes.
weight: 1110
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- security-engineers
- operators
source_material:
- live-3.2.5
- proposed-kv
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\secure\groups.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/secure/manage-groups.md
related:
- how-to/security/create-update-and-remove-users
- how-to/security/grant-and-revoke-permissions
- reference/commands/riak/admin/security
- tutorials/security/apply-and-test-group-permissions
- foundations/security/security-boundaries-and-trust
- foundations/security/identities-authentication-and-permissions
- foundations/security/tls-and-certificate-trust
previous_page: how-to/security/create-update-and-remove-users
next_page: how-to/security/configure-authentication-sources
---

Use a group to apply a common permission set to several users. Verify the resulting grants whenever membership changes.

## Create the group

The group name in this example is a deliberate application choice:

{{< cli-example key="shell:riak admin security add-group" args="inventory-readers" >}}

## Assign membership and permissions

Use {{< cli key="shell:riak admin security alter-user" >}} with the supported `groups` option to set a user's intended memberships. Inspect its current membership first so the change preserves any groups it still requires. Grant the group's operations on the intended type or bucket with {{< cli key="shell:riak admin security grant" >}}.

Inspect the group with {{< cli key="shell:riak admin security print-group" >}} and the effective grants with {{< cli key="shell:riak admin security print-grants" >}}.

## Verify changes

Authenticate as a member and test an allowed read and a denied write. Remove the membership, establish a fresh connection, and repeat the tests. Confirm that permissions granted directly to the user do not still allow the operation you intended to revoke.

Delete an unused group only after reviewing its members and grants.

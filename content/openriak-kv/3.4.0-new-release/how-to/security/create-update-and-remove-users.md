---
title: Create, update, and remove users
description: Create an application user, verify its effective access, and remove the identity when it is no longer
  needed. Keep a working administrative connection while making security changes.
weight: 1100
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
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\secure\users.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/secure/manage-users.md
related:
- how-to/security/manage-groups-and-membership
- how-to/security/configure-authentication-sources
- how-to/security/grant-and-revoke-permissions
- how-to/security/authenticate-an-application-client
- reference/commands/riak/admin/security
- foundations/security/security-boundaries-and-trust
- foundations/security/identities-authentication-and-permissions
- foundations/security/tls-and-certificate-trust
previous_page: how-to/security/configure-and-rotate-tls-certificates
next_page: how-to/security/manage-groups-and-membership
---

Create an application user, verify its effective access, and remove the identity when it is no longer needed. Keep a working administrative connection while making security changes.

## Create or change the identity

The following name is an example; choose a dedicated identity for each application role. Supply credentials through your approved administrative procedure and avoid retaining passwords in shared shell history.

{{< cli-example key="shell:riak admin security add-user" args="inventory-app" >}}

Use {{< cli key="shell:riak admin security alter-user" >}} to change supported user options and {{< cli key="shell:riak admin security print-user" >}} to inspect the resulting record. Configure an authentication source for the client's origin and grant only its required operations.

## Verify access

Connect using the application's actual protocol, credentials, trust material, and namespace. Test one permitted operation and one denied operation. A successful login does not establish that the permission scope is correct.

## Remove the user

Revoke application access and stop clients using the identity, then use {{< cli key="shell:riak admin security del-user" >}}. Confirm that a fresh connection using the removed identity is rejected. Rotate any shared credential that the retired identity also knew.

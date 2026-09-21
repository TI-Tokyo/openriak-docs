---
title: Identities, authentication, and permissions
description: A user identifies a client, an authentication source selects how a connection proves that identity,
  and permissions determine which operations it can perform. Groups allow related users to share permission assignments.
weight: 390
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- security-engineers
- architects
- operators
source_material:
- live-3.2.5
- proposed-kv
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/security/authentication-sources.md
- foundations/security/users-groups-and-permissions.md
related:
- how-to/security/create-update-and-remove-users
- how-to/security/manage-groups-and-membership
- how-to/security/configure-authentication-sources
- how-to/security/grant-and-revoke-permissions
- reference/commands/riak/admin/security
- foundations/security/tls-and-certificate-trust
---

A user identifies a client, an authentication source selects how a connection proves that identity, and permissions determine which operations it can perform. Groups allow related users to share permission assignments.

## Authentication sources

A source rule connects a user or group and network origin with an authentication method. Credentials alone are not sufficient if the connection does not match an appropriate source rule. Conversely, a broad rule can admit connections from more places than intended.

## Permissions and scope

Grants associate supported operations with users or groups and a resource scope. Scope matters: permission for one bucket is not necessarily permission for another namespace. Group membership changes can alter several effective grants at once.

## Identity lifecycle

Applications need a way to rotate credentials, remove departed identities, and check the resulting permissions. Sharing one unrestricted user makes those changes harder to isolate and obscures which application needs which access.

## A useful verification model

For each role, test an allowed operation and a deliberately denied operation against the intended endpoint and namespace. Also test a connection from an unapproved origin. These checks distinguish successful authentication from correct authorization.

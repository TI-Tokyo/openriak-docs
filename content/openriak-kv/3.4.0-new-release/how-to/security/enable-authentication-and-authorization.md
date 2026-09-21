---
title: Enable authentication and authorization
description: Enable authentication and authorization after preparing identities, source rules, grants, and TLS.
  Keep an administrative shell available while testing access so you can correct a mistaken rule.
weight: 1090
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- security-engineers
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\secure\basics.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\security\basics.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#enabling-riak-security
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#enabling-security-and-restricting-source
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/secure/enable-security.md
related:
- how-to/security/create-update-and-remove-users
- how-to/security/manage-groups-and-membership
- how-to/security/configure-authentication-sources
- how-to/security/grant-and-revoke-permissions
- how-to/security/configure-and-rotate-tls-certificates
- tutorials/security/make-an-authenticated-tls-client-connection
- foundations/security/security-boundaries-and-trust
- foundations/security/identities-authentication-and-permissions
- foundations/security/tls-and-certificate-trust
previous_page: how-to/security/grant-and-revoke-permissions
next_page: how-to/security/authenticate-an-application-client
---

Enable authentication and authorization after preparing identities, source rules, grants, and TLS. Keep an administrative shell available while testing access so you can correct a mistaken rule.

## Prepare identities and transport

Create users and groups using [Create, update, and remove users]({{< product-version-root >}}how-to/security/create-update-and-remove-users/) and [Manage groups and membership]({{< product-version-root >}}how-to/security/manage-groups-and-membership/). Configure certificates with [Configure and rotate TLS certificates]({{< product-version-root >}}how-to/security/configure-and-rotate-tls-certificates/), source authentication with [Configure authentication sources]({{< product-version-root >}}how-to/security/configure-authentication-sources/), and the minimum required permissions with [Grant and revoke permissions]({{< product-version-root >}}how-to/security/grant-and-revoke-permissions/). Test these changes first in an isolated environment.

## Enable security

{{< cli-example key="shell:riak admin security enable" >}}
{{< cli-example key="shell:riak admin security status" >}}

Check the state from every intended member. For PB, the existing listener switches to the security handshake; clients must support it. For HTTP, use the HTTPS listener for credentials and update application endpoints accordingly.

## Verify allowed and denied access

Open new client connections and test a permitted read, a forbidden write, invalid credentials, and an unmatched source address. Test query permissions separately from object reads. Some interfaces have source protection without separate operation grants; network isolation remains necessary.

Restore traffic only after real application clients pass. If a rule is wrong, correct the specific source or grant from the administrative shell rather than disabling all security as a permanent workaround.

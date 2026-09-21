---
title: Configure authentication sources
description: Associate users and client networks with the intended authentication method. A source rule determines
  how a connection authenticates; grants determine which operations it may perform.
weight: 1120
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
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\secure\security-sources.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\security\managing-sources.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
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
- how-to/secure/manage-sources.md
related:
- how-to/security/enable-authentication-and-authorization
- how-to/security/grant-and-revoke-permissions
- how-to/security/configure-and-rotate-tls-certificates
- how-to/security/restrict-client-node-and-administrative-network-access
- reference/commands/riak/admin/security
- foundations/security/security-boundaries-and-trust
- foundations/security/identities-authentication-and-permissions
- foundations/security/tls-and-certificate-trust
previous_page: how-to/security/manage-groups-and-membership
next_page: how-to/security/grant-and-revoke-permissions
---

Associate users and client networks with the intended authentication method. A source rule determines how a connection authenticates; grants determine which operations it may perform.

## Inspect existing rules

{{< cli-example key="shell:riak admin security print-sources" >}}

Record the user or group scope, source CIDR, method, and overlapping rules. Determine the address Riak actually sees when clients connect through a proxy or NAT.

## Add a restricted source

{{< cli-example key="shell:riak admin security add-source" >}}

Use the metadata syntax with the intended identity, narrow network range, and supported method. Prefer a verified certificate or password over a trust rule for clients outside a tightly controlled local environment. Match certificate identity and username when certificate authentication is selected.

## Test and remove obsolete rules

Open a new client connection from an allowed address and another from a denied address. Test invalid credentials as well. Once the replacement rule is working, remove the exact obsolete rule:

{{< cli-example key="shell:riak admin security del-source" >}}

Print sources again and retain the final policy in deployment records. Keep the administrative recovery path until all production clients have reconnected successfully.

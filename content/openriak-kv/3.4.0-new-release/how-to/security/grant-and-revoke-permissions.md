---
title: Grant and revoke permissions
description: Grant the minimum operations an identity needs on the intended type and bucket, then test both permitted
  and forbidden requests.
weight: 1130
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
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#granting-permissions-for-specific-actions
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/secure/manage-permissions.md
related:
- how-to/security/manage-groups-and-membership
- how-to/security/configure-authentication-sources
- how-to/security/authenticate-an-application-client
- tutorials/security/apply-and-test-group-permissions
- reference/commands/riak/admin/security
- foundations/security/security-boundaries-and-trust
- foundations/security/identities-authentication-and-permissions
- foundations/security/tls-and-certificate-trust
previous_page: how-to/security/configure-authentication-sources
next_page: how-to/security/enable-authentication-and-authorization
---

Grant the minimum operations an identity needs on the intended type and bucket, then test both permitted and forbidden requests.

## Inspect the effective grants

{{< cli-example key="shell:riak admin security print-grants" args="APP_USER" >}}

Check direct grants and inherited group membership. A permission removed from one group may still be granted by another membership or a direct user grant.

## Grant or revoke the scoped operation

This example grants read access to `customers` in the untyped namespace:

{{< cli-example key="shell:riak admin security grant" args="riak_kv.get on default customers to APP_GROUP" >}}

To remove that grant:

{{< cli-example key="shell:riak admin security revoke" args="riak_kv.get on default customers from APP_GROUP" >}}

Use the command help for other scopes. Object, index/query, listing, and MapReduce operations have different permissions; do not assume read access implies all discovery operations are allowed.

## Verify with fresh connections

Read a permitted key, attempt a forbidden write, and test another bucket outside the grant. Reconnect PB clients when checking changed grants because permission state can be cached for a connection. Record the observed allowed and denied outcomes before applying the policy more broadly.

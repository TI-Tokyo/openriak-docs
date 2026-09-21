---
title: Audit deployment security
description: Audit the access actually exposed by a deployment, then record the changes needed to meet its security
  requirements.
weight: 1170
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- security-operators
source_material:
- legacy-3.2.5
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\security\best-practices.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/secure/best-practices.md
related:
- reference/configuration/authentication-authorization-and-tls-settings
- reference/commands/riak/admin/security
- how-to/security/restrict-client-node-and-administrative-network-access
- foundations/security/security-boundaries-and-trust
- foundations/security/identities-authentication-and-permissions
- foundations/security/tls-and-certificate-trust
---

Audit the access actually exposed by a deployment, then record the changes needed to meet its security requirements.

## Inventory access

List client listeners, replication endpoints, node distribution ports, administrative hosts, and load-balancer paths. Compare the configured bindings and network rules with the clients and peers that should reach them.

## Check identities and trust

Inspect users, groups, authentication sources, and grants through the security command reference. Remove unused identities and overbroad permissions. Check certificate names, chains, expiry, private-key permissions, and the clients' trust stores.

## Exercise the boundaries

From representative client locations, test allowed and rejected connections and operations. Confirm that administrative access is restricted independently of application bucket permissions. Verify that log collection and backups do not expose credentials or private keys.

## Close and verify findings

Apply one controlled change at a time, retain administrative recovery access, and repeat the failed check after remediation. Record the endpoint, identity, operation, expected result, observed result, and date so the next audit can compare the same boundaries.

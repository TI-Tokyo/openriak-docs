---
title: Restrict client, node, and administrative network access
description: Restrict database access to the clients, peer nodes, and administrators that need it. Apply rules to
  the actual listener addresses and distribution range configured for the deployment.
weight: 1150
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
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\secure\networking.md
source_material:
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#network
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/secure/secure-networking.md
related:
- how-to/node-configuration/configure-http-and-protocol-buffers-listeners
- how-to/replication-and-reconciliation/secure-next-generation-replication-connections
- how-to/security/enable-authentication-and-authorization
- how-to/troubleshooting/diagnose-client-connection-and-request-failures
- reference/configuration/listeners-and-networking-settings
- foundations/security/security-boundaries-and-trust
- foundations/security/identities-authentication-and-permissions
- foundations/security/tls-and-certificate-trust
---

Restrict database access to the clients, peer nodes, and administrators that need it. Apply rules to the actual listener addresses and distribution range configured for the deployment.

## Inventory traffic

Separate client HTTP/HTTPS and PB traffic, Erlang node discovery and distribution, inter-cluster replication, and host administration. Read the configured ports and ranges here:

{{< configuration-reference-table >}}
^listener\.
^erlang\.distribution\.
{{< /configuration-reference-table >}}

Erlang's port mapper normally uses TCP 4369; verify the running environment if it is customized. Restrict it and the distribution range to cluster peers. A shared cookie is not a substitute for network isolation.

## Apply narrowly scoped rules

Bind services to intended interfaces. Allow client ports only from application networks or proxies, peer ports only between cluster members, and replication listeners only from the intended remote clusters. Restrict SSH and console access to administrative paths. Avoid public wildcard rules for database or distribution ports.

## Test connectivity and denial

From each required source, test the actual protocol and authentication. From an unauthorized source, confirm the connection is blocked. Recheck membership and replication after changes so an overly narrow rule does not partition the cluster. Retain a host-access recovery path while changing firewall rules.

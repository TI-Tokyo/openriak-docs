---
title: Configure HTTP and Protocol Buffers listeners
description: Bind HTTP and Protocol Buffers to the interfaces and ports that the intended clients can reach. Keep
  administrative and distribution access separate from public client access.
weight: 210
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\guides\configure-listeners.md
source_material:
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---key-riakconf-changes
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/api-listeners.md
related:
- how-to/security/configure-and-rotate-tls-certificates
- how-to/security/restrict-client-node-and-administrative-network-access
- how-to/node-configuration/configure-a-load-balancing-proxy
- how-to/troubleshooting/diagnose-client-connection-and-request-failures
- reference/configuration/listeners-and-networking-settings
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
- foundations/cluster-architecture/the-lifecycle-of-a-read-and-a-write
previous_page: how-to/node-configuration/configure-node-identity-directories-and-the-initial-ring
next_page: how-to/node-configuration/validate-configuration-before-startup
---

Bind HTTP and Protocol Buffers to the interfaces and ports that the intended clients can reach. Keep administrative and distribution access separate from public client access.

## Choose the bindings

For each listener, record its interface address, port, allowed source networks, and whether TLS is required. A loopback listener accepts only local clients or a local proxy. A wildcard listener may expose the service on every interface.

{{< configuration-reference-table >}}
^listener\.
^ssl\.
{{< /configuration-reference-table >}}

## Apply and validate

Edit the corresponding named listener entries in `riak.conf`; use distinct names when defining more than one listener. Avoid port collisions with another process. Validate the configuration, then restart one node at a time if the cluster is already serving traffic.

{{< cli-example key="shell:riak chkconfig" >}}

Align firewall rules, proxy upstreams, certificates, and application endpoints with the new binding. For TLS, verify the certificate against the hostname clients actually use.

## Verify from the client network

Request `/ping` over HTTP or HTTPS and make an authenticated operation if security is enabled. Test Protocol Buffers with the real client library. Check both an allowed connection and a connection that should be denied. A successful loopback test alone does not prove remote reachability.

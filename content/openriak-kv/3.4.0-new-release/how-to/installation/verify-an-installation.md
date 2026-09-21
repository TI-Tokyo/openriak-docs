---
title: Verify an installation
description: Verify that an installed node starts, serves requests, and reports the expected cluster state before
  admitting application traffic.
weight: 190
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\install\verifying-installation.md
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\verify.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\installing\verify.md
- Package, platform, installation, upgrade, or downgrade details require release-specific verification for OpenRiak
  KV 3.4.0.
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InstallAndStartGuide.html#local-release
- https://openriak.github.io/riak/InstallAndStartGuide.html#starting-riak
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/install/verify-installation.md
related:
- how-to/cluster-lifecycle/start-stop-or-restart-a-node
- how-to/node-configuration/configure-http-and-protocol-buffers-listeners
- how-to/monitoring-and-diagnostics/perform-routine-cluster-health-checks
- how-to/troubleshooting/diagnose-client-connection-and-request-failures
- reference/http-api/ping
- foundations/overview/what-openriak-kv-is
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
previous_page: how-to/node-configuration/validate-configuration-before-startup
next_page: how-to/cluster-lifecycle/add-nodes-to-a-cluster
---

Verify that an installed node starts, serves requests, and reports the expected cluster state before admitting application traffic.

## Check configuration and process health

Run the configuration validator, then start the node using [Start, stop, or restart a node]({{< product-version-root >}}how-to/cluster-lifecycle/start-stop-or-restart-a-node/) if it is not already running:

{{< cli-example key="shell:riak chkconfig" >}}
{{< cli-example key="shell:riak ping" >}}
{{< cli-example key="shell:riak admin status" >}}

Expect a successful configuration check and `pong`. Inspect startup logs for backend, permission, certificate, and listener errors. Confirm the installed package and OTP versions match the deployment record.

## Test the configured HTTP endpoint

Set `RIAK_HTTP` to the listener that your client is allowed to reach. Add your deployment's TLS and authentication options when required:

```sh
curl --fail "$RIAK_HTTP/ping"
curl --fail -i -X PUT "$RIAK_HTTP/buckets/installation-check/keys/probe" -H 'Content-Type: text/plain' --data-binary 'installation verified'
curl --fail "$RIAK_HTTP/buckets/installation-check/keys/probe"
```

Expect `OK` and `installation verified`. Use a unique test key if checks can run concurrently. Delete the probe with its fetched causal context after verification.

## Check cluster readiness

{{< cli-example key="shell:riak admin member-status" >}}
{{< cli-example key="shell:riak admin transfers" >}}

An unjoined installation has one member; a joined node must show the intended cluster membership. Resolve unexpected nodes, unreachable members, or incomplete handoffs before enabling traffic. Also test the application's actual Protocol Buffers connection if HTTP is not its production interface.

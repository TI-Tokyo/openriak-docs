---
title: Start, stop, or restart a node
description: Start and stop a node through the process manager that owns it. Before stopping a cluster member, check
  surviving capacity and use [[H75]] for a rolling change.
weight: 700
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InstallAndStartGuide.html#local-release-or-cluster
- https://openriak.github.io/riak/InstallAndStartGuide.html#package-deployment
- https://openriak.github.io/riak/InstallAndStartGuide.html#starting-riak
- https://openriak.github.io/riak/InstallAndStartGuide.html#starting-riak-by-make-method
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/start-stop-restart-node.md
related:
- how-to/cluster-lifecycle/perform-a-rolling-restart
- how-to/troubleshooting/diagnose-a-node-that-will-not-start
- how-to/monitoring-and-diagnostics/perform-routine-cluster-health-checks
- reference/commands/riak
- tutorials/cluster-operations-and-recovery/perform-a-rolling-restart
- foundations/cluster-architecture/membership-gossip-and-handoff
- foundations/cluster-lifecycle/failure-and-recovery
- foundations/cluster-lifecycle/rolling-maintenance-and-recovery-headroom
---

Start and stop a node through the process manager that owns it. Before stopping a cluster member, check surviving capacity and use [Perform a rolling restart]({{< product-version-root >}}how-to/cluster-lifecycle/perform-a-rolling-restart/) for a rolling change.

## Native packages

Use the service variant for the installed operating system and service manager. These commands require the corresponding packaged service definition and a running service manager.

### Start

{{< service-command action="start" >}}

### Stop

{{< service-command action="stop" >}}

To restart, stop the service, wait for the process to exit, then start it with the same manager. Do not mix a managed service with a second direct launcher.

## Direct release and containers

For an unmanaged release, use its direct launcher:

{{< cli-example key="shell:riak daemon" >}}
{{< cli-example key="shell:riak stop" >}}

For Compose, use `docker compose stop SERVICE`, `start SERVICE`, or `restart SERVICE` in the deployment directory. Allow the configured graceful-stop period; forced termination may require extra recovery.

## Verify

{{< cli-example key="shell:riak ping" >}}
{{< cli-example key="shell:riak admin member-status" >}}
{{< cli-example key="shell:riak admin transfers" >}}

After startup, inspect logs and wait for recovery before returning client traffic or stopping another member.

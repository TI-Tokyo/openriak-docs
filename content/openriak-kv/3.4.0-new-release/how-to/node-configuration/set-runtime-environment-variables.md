---
title: Set runtime environment variables
description: Change an Erlang application environment value on a running node when the target component supports
  reading it at runtime. A successful environment update does not mean a process that cached the value has reconfigured
  it
weight: 230
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#setting-environment-variables-at-runtime
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/runtime-environment-variables.md
related:
- how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console
- how-to/node-configuration/inspect-and-manage-effective-configuration
- reference/configuration/runtime-environment-variables
- reference/replication-interfaces/next-generation-replication-runtime-controls
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
- foundations/cluster-architecture/the-lifecycle-of-a-read-and-a-write
---

Change an Erlang application environment value on a running node when the target component supports reading it at runtime. A successful environment update does not mean a process that cached the value has reconfigured itself.

## Identify the exact key

Use [All configuration settings and defaults]({{< product-version-root >}}reference/configuration/all-configuration-settings-and-defaults/) to find the application name, internal setting name, and data type. Check the component's runtime control interface first; a dedicated function may update active processes as well as the environment.

## Record and change

Open the remote console using [Inspect a node through the remote console]({{< product-version-root >}}how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console/). Read the existing value with Erlang's `application:get_env/2`, record it, then use `application:set_env/3` with the exact application, key, and Erlang value. Apply the change only to the intended nodes; this API changes the local VM unless a separate cluster-wide function is documented.

## Verify and persist

Read the environment back and exercise the affected feature. Compare logs, metrics, and request behaviour. If the component requires a restart or a dedicated refresh, schedule that explicitly. For a lasting change, update the corresponding configuration file as well; an ad hoc runtime change is normally lost on restart.

Revert to the recorded value if behaviour worsens, and record the change with its scope and expiry.

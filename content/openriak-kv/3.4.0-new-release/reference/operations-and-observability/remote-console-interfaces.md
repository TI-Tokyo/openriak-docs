---
title: Remote-console interfaces
description: The Erlang remote console exposes node-local and cluster operations through the release's exported
  administrative interfaces. Arity, argument types, availability, and help are listed in the command metadata.
weight: 1080
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\runtime-interaction.md
source_material:
- legacy-3.2.5
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#remote-console
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#riak_client-remote_console-commands
- https://openriak.github.io/riak/OtherAPI.html#aae-folds-via-the-remote-console
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/operations/remote-console.md
related:
- how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console
- how-to/node-configuration/set-runtime-environment-variables
- how-to/data-inspection-and-repair/repair-a-vnode-or-node-from-surviving-replicas
- reference/replication-interfaces/next-generation-replication-runtime-controls
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

The Erlang remote console exposes node-local and cluster operations through the release's exported administrative interfaces. Arity, argument types, availability, and help are listed in the command metadata.

{{< cli-command-index category="Erlang shell" >}}

## Scope and lifecycle

Some functions change only the current node; others explicitly operate across members. A runtime setting change is not automatically persisted in `riak.conf`, and a queued repair is not complete when its submission returns.

Use the shell's detach sequence described in [Inspect a node through the remote console]({{< product-version-root >}}how-to/monitoring-and-diagnostics/inspect-a-node-through-the-remote-console/). Calling VM termination functions in an attached shell stops the database node.

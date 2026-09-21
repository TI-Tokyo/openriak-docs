---
title: Inspect a node through the remote console
description: Open an Erlang shell on a running node to inspect supported runtime interfaces. The shell has the node's
  privileges; use a known, bounded operation and record which node you are connected to.
weight: 920
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
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#remote-console
- https://openriak.github.io/riak/OtherAPI.html#aae-folds-via-the-remote-console
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/use-remote-console.md
related:
- how-to/monitoring-and-diagnostics/inspect-stored-objects-and-metadata
- how-to/data-inspection-and-repair/run-and-retrieve-a-long-running-aae-fold
- how-to/troubleshooting/investigate-a-running-node-with-erlang-diagnostics
- reference/operations-and-observability/remote-console-interfaces
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Open an Erlang shell on a running node to inspect supported runtime interfaces. The shell has the node's privileges; use a known, bounded operation and record which node you are connected to.

## Connect

From the node's installation environment:

{{< cli-example key="shell:riak remote_console" >}}

For the Docker learning lab, use `kvi node1` before this command as described in [Build and explore a Docker cluster]({{< product-version-root >}}tutorials/first-cluster/build-and-explore-a-docker-cluster/). The helper supplies the active VM arguments and an interactive terminal.

## Inspect a supported interface

Use the Erlang command catalogue in [Remote-console interfaces]({{< product-version-root >}}reference/operations-and-observability/remote-console-interfaces/) to find the exact function and arity for this release. Erlang expressions end in a period; variables are single-assignment within a shell session. Keep large object or result output out of the terminal unless it is necessary for the investigation.

For a repeatable one-shot operation, the release also provides:

{{< cli-example key="shell:riak eval" >}}

Pass the intended expression using its documented argument form. Do not turn an unreviewed sequence of shell experiments into an automated repair script.

## Detach cleanly

Use `Ctrl-G`, then `q`, to leave the remote shell. Do not execute `q()` or `init:stop()` on the attached node: those terminate its VM. Check for abandoned remote-console client processes after an interrupted SSH session, and distinguish them from the actual Riak process before stopping anything.

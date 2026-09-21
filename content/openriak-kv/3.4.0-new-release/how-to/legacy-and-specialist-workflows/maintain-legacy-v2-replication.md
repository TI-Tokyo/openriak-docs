---
title: Maintain legacy v2 replication
description: Assess and maintain a deployment that still uses legacy v2 replication. Do not mix v2 peer and fullsync
  commands with current-generation replication queues.
weight: 1390
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\v2-multi-datacenter.md
- Legacy multi-datacenter replication terminology and commands require compatibility review.
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ReplicationGuide.html#legacy-replication---riak_repl
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/replication/configure-v2-multi-datacenter.md
related:
- reference/orientation-and-compatibility/replication-generation-compatibility
- reference/replication-interfaces/legacy-riak-repl-runtime-controls
- reference/legacy-and-experimental-features/legacy-aae-and-riak-repl-settings
- how-to/legacy-and-specialist-workflows/maintain-legacy-v3-replication
- how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Assess and maintain a deployment that still uses legacy v2 replication. Do not mix v2 peer and fullsync commands with current-generation replication queues.

## Identify the actual protocol

Record both clusters' versions, listener/client configuration, TLS settings, and bucket replication policy. Check [Replication-generation compatibility]({{< product-version-root >}}reference/orientation-and-compatibility/replication-generation-compatibility/) and the availability labels in [Legacy riak_repl runtime controls]({{< product-version-root >}}reference/replication-interfaces/legacy-riak-repl-runtime-controls/) before issuing a command; an old runbook may name a command that is not supported by the selected release.

## Verify the existing relationship

Inspect source and destination status through the available legacy controls. Write, update, and delete a unique test key and confirm delivery. Check fullsync completion as well as real-time status. Preserve the working configuration before changing peers or certificates.

## Plan a supported transition

Prefer moving to current-generation replication using [Connect clusters with next-generation replication]({{< product-version-root >}}how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication/). Establish its source queues and consumers independently, seed and reconcile, and verify the application before retiring the old relationship. Keep rollback and conflict handling explicit if both paths are temporarily active. Do not infer protocol compatibility from a shared `riak repl` executable name.

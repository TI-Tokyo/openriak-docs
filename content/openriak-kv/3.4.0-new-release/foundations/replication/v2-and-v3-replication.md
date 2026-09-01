---
title: 'Legacy and current replication generations'
description: 'Explain legacy and current replication generations, its data flow, failure behavior, and operational trade-offs.'
weight: 11
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\v2-multi-datacenter.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\v3-multi-datacenter.md'
  - 'Legacy multi-datacenter replication terminology and commands require compatibility review.'
source_material:
  - 'legacy-3.2.5'
  - 'source-code-release-notes-3.4'
  - 'openriak-discussions'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ReplicationGuide.html#legacy-replication---riak_repl'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain legacy and current replication generations, its data flow, failure behavior, and operational trade-offs.

## Overview

### V2 Multi-Datacenter Replication Reference

[v2 mdc arch]: {{< product-version-root >}}foundations/foundations/clusters-rings-and-partitions/
[v2 mdc fullsync]: {{< product-version-root >}}foundations/replication/v2-and-v3-replication/

**Deprecation Warning**
v2 Multi-Datacenter Replication is deprecated and will be removed in a future version. Please use [v3]({{< product-version-root >}}foundations/replication/v2-and-v3-replication/) instead.

#### In This Section

##### [V2 Multi-Datacenter Replication Reference: Architecture][v2 mdc arch]

Overview of the architecture undergirding OpenRiak's Multi-Datacenter Replication capabilities.

[Learn More >>][v2 mdc arch]

###### [V2 Multi-Datacenter Replication Reference: Scheduling Fullsync][v2 mdc fullsync]

Brief tutorial on scheduling fullsync operations.

[Learn More >>][v2 mdc fullsync]

### V3 Multi-Datacenter Replication Reference

[v3 mdc arch]: {{< product-version-root >}}foundations/foundations/clusters-rings-and-partitions/
[v3 mdc aae]: {{< product-version-root >}}reference/commands/aae/
[v3 mdc cascade]: {{< product-version-root >}}foundations/replication/cascading-writes/
[v3 mdc fullsync]: {{< product-version-root >}}foundations/replication/v2-and-v3-replication/

#### In This Section

##### [V3 Multi-Datacenter Replication Reference: Architecture][v3 mdc arch]

Overview of the architecture undergirding OpenRiak's Version 3 Multi-Datacenter Replication capabilities.

[Learn More >>][v3 mdc arch]

###### [V3 Multi-Datacenter Replication Reference: With Active Anti-Entropy][v3 mdc aae]

Overview of using OpenRiak KV's active anti-entropy (AAE) subsystem with Multi-Datacenter.

[Learn More >>][v3 mdc aae]

###### [V3 Multi-Datacenter Replication Reference: Cascading Realtime Writes][v3 mdc cascade]

Details the cascading realtime writes feature.

[Learn More >>][v3 mdc cascade]

###### [V3 Multi-Datacenter Replication Reference: Scheduling Fullsync][v3 mdc fullsync]

[Learn More >>][v3 mdc fullsync]

#### Legacy Replication - riak_repl

The previous replication solution in Riak, `riak_repl`, is still available to configure.  The `riak_repl` solution is stable, and has not been modified since Riak 2.2.3 (other than the conversion to be fully open-source in Riak 2.2.5).

The [legacy documentation]({{<baseurl>}}openriak-kv/2.2.3/configuring/v3-multi-datacenter/index.html) can be used to set up `riak_repl`.  The v3 of riak_repl should always be used in preference to previous versions.

Some notes on `riak_repl` and the comparison to NextGen replication in Riak:

- `riak_repl` is not under active development, but remains functional.
- `riak-repl` has no support for replication and reconciliation between clusters with different ring sizes, so cannot be used to reliably transition between clusters of different ring sizes.
- `riak_repl` uses a PUSH model to replicate real-time changes.
- `riak_repl` will attempt to migrate queues between nodes when nodes go down.
  - Despite the additional resilience, anecdotal evidence indicates that real-time replication is generally less reliable than NextGen replication (i.e. it is more likely to drop replication events).
- `riak_repl` has an anti-entropy based method of full-sync reconciliation, using the legacy active anti-entropy service.
  - The AAE-based full-sync in `riak_repl` is faster at resolving deltas, but will fail to complete during tree rebuilds;
  - Users of full-sync have needed to use manually prompted rebuild windows to address this problem (i.e. a period where full-sync is suspended, and rebuilds are completed in parallel).
  - As clusters scale, the AAE rebuild windows will be an ongoing management overhead, and clusters may scale to the point that rebuilds cannot complete in the available window.
- `riak_repl` has a keylisting form of full-sync which will do a full key and clock comparison on a vnode-by-vnode basis.
  - A keylisting full-sync can be resource intensive and will take a significant amount of time to complete on clusters of non-trivial scale.

The use of `riak_repl` is deprecated, and when a retirement schedule is agreed it will be advertised via [OpenRiak discussions](https://github.com/orgs/OpenRiak/discussions).

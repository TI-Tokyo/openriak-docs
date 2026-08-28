---
title: 'Enable TicTac active anti-entropy'
description: 'Show operators how to enable tictac active anti-entropy and validate data movement.'
weight: 11
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\tutorials_howto\tutorials\enabling-tictac.md'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\active-anti-entropy\tictac-aae.md'
source_material:
  - 'legacy-3.2.5'
  - 'source-code-release-notes-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#intra-cluster-data-resilience---changing-the-choice'
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#proactive-reconciliation'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#configuration-of-all-cluster-reconciliation'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#enable-tictac-aae'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to enable tictac active anti-entropy and validate data movement.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### TicTac Active Anti-Entropy

[configure next-gen-repl]: ../../next-gen-replication

The configuration for TicTac AAE is kept in
 the `riak.conf` configuration file.

#### Validate Settings

Once your configuration is set, you can verify its correctness by
running the `riak` command-line tool:

```bash
riak chkconfig
```

#### riak.conf Settings

Setting | Options | Default | Description
:-------|:--------|:--------|:-----------
`tictacaae_active` | `active`, `passive` | `passive` | Enable or disable tictacaae. Note that disabling tictacaae will set the use of tictacaae_active only at startup - setting the environment variable at runtime will have no impact.
`aae_tokenbucket` | `enabled`, `disabled` | `enabled` | To protect against unbounded queues developing and subsequent timeouts/crashes of the AAE process, back-pressure signalling is used to block the vnode should a backlog develop on the AAE process. This can be disabled.
`tictacaae_dataroot` | `` | `"$platform_data_dir/tictac_aae"` | Set the path for storing tree caches and parallel key stores. Note that at startup folders may be created for every partition, and not removed when that partition hands off (although the contents should be cleared).
`tictacaae_parallelstore` | `leveled_ko`, `leveled_so` | `leveled_so` | On startup, if tictacaae is enabled, then the vnode will detect of the vnode backend has the capability to be a "native" store. If not, then parallel mode will be entered, and a parallel AAE keystore will be started. There are two potential parallel store backends - leveled_ko(Key ordered leveled), and leveled_so(Segment ordered leveled).
`tictacaae_rebuildwait` | `` | `336` | This is the number of hours between rebuilds of the Tictac AAE system for each vnode. A rebuild will invoke a rebuild of the key store (which is a null operation when in native mode), and then a rebuild of the tree cache from the rebuilt store.
`tictacaae_rebuilddelay` | `` | `345600` | Once the AAE system has expired (due to the rebuild wait), the rebuild will not be triggered until the rebuild delay which will be a random number up to the size of this delay (in seconds).
`tictacaae_storeheads` | `enabled`, `disabled` | `disabled` | By default only a small amount of metadata is required for AAE purposes, and with storeheads disabled only that small amount of metadata is stored. Enabling storeheads will allow for greater functionality (notably with [`aae_fold`](../../../using/cluster-operations/tictac-aae-fold/)) at the cost of disk space and memory.
`tictacaae_exchangetick` | `` | `240000` | Exchanges are prompted every exchange tick, on each vnode. By default there is a tick every 4 minutes. Exchanges will skip when previous exchanges have not completed, in order to prevent a backlog of fetch-clock scans developing.
`tictacaae_rebuildtick` | `` | `3600000` | Rebuilds will be triggered depending on the riak_kv.tictacaae_rebuildwait, but they must also be prompted by a tick. The tick size can be modified at run-time by setting the environment variable via riak attach.
`tictacaae_maxresults` | `` | `256` | The Merkle tree used has 4096 * 1024 leaves. When a large discrepancy is discovered, only part of the discrepancy will be resolved each exchange - active anti-entropy is intended to be a background process for repairing long-term loss of data, hinted handoff and read-repair are the short-term and immediate answers to entropy. How much of the tree is repaired each pass is defined by the tictacaae_maxresults.

#### See also

[Next Gen Replication][configure next-gen-repl] makes extensive use of TicTac AAE, and has some replication-specific TicTac AAE settings.

#### Proactive reconciliation

Riak has support for proactive reconciliation within a cluster; known as [active anti-entropy (AAE)]({{< baseurl >}}kv/3.4.1/explanation/replication/active-anti-entropy/).  Configuring AAE will trigger a background process that will continually verify that the most recent version of each object is correctly stored in all required locations, and prompt repairs should the verification process highlight discrepancies.  This is in addition to reactive management which is always enabled within Riak: as part of every GET request a read repair process may be triggered if all vnodes are not up-to-date; as part of failure management a handoff process will merge data captured on temporary fallback vnodes back into primary vnodes.

Proactive reconciliation provides continuous assurance that data is correctly secured across multiple devices within a cluster: it is verification as well as correction.  It is of particular use where data may be stored for long periods without being read, nullifying the trigger for reactive management via read repair.

There are two forms of proactive intra-cluster reconciliation in Riak:

- Tictac AAE (recommended).
  - Uses the [configuration option `tictacaae_active`]({{< baseurl >}}kv/3.4.1/how-to/configure/basic-node-settings/).
  - A prerequisite for efficient inter-cluster reconciliation.
  - A prerequisite for the use of the [AAE Fold API]({{< baseurl >}}kv/3.4.1/reference/aae-fold-api/).
  - Requires a secondary keystore if not using the leveled backend.
  - Limits the pace of repair activity when discrepancies are discovered.
- Legacy hashtree AAE (default).
  - Uses the configuration option `anti-entropy`.
  - Has a dependency on the deprecated `eleveldb` backend.
  - Requires a separate keystore for all backends.
  - More aggressive than Tictac AAE at resolving discovered discrepancies.

> If Tictac AAE is not enabled, there is an increased risk of data loss when Riak is used to store _cold_ data that is very rarely read.

Enabling Tictac AAE also adds to the cluster support for the operator-functionality associated with [AAE Folds]({{< baseurl >}}kv/3.4.1/reference/aae-fold-api/).

#### Intra-cluster data resilience - changing the choice

The `n_val` is in theory configurable by bucket, which allows for multiple nvals to be used within the cluster.  However, each unique n_val will increase the overhead of running anti-entropy (anti-entropy comparisons are per n_val, and separate caches are required for each n_val), and the complexity of configuring inter-cluster reconciliation.  Once a `n_val` has been set on a bucket, there is no tested way of reducing it and converging on a clean state - other than replicating to a new cluster and transitioning between clusters.  Increasing the `n_val` should eventually converge into an expected state.

The `target_n_val` and `target_location_n_val` configuration is used each time a cluster change is planned (i.e. adding or removing a node).  So using a new value will take effect once the next change is made within a cluster.

Both anti-entropy mechanisms can be deployed in parallel to help with transition.  Enabling anti-entropy takes time to take effect (as caches are built).  Disabling it is immediate, although garbage collecting any legacy on-disk overhead is a manual operator task.

#### Configuration of All-Cluster Reconciliation

It is commonly most efficient to reconcile all data, rather than partial data.  If all data is not required, then [per-bucket reconciliation]({{< baseurl >}}kv/3.4.1/how-to/configure/replication/per-bucket-reconciliation/) can be enabled.  All-cluster reconciliation is much more common than per-bucket reconciliation in production systems, as it commonly has lower overheads.

#### Enable Tictac AAE

To use the inter-cluster reconciliation then Tictac AAE must be enabled in `riak.conf` - `tictacaae_active = active`.  Enabling `tictacaae_active` will place extra load on the cluster at write time, if the `leveled` backend is not used as a sole backend.  In this case there will be a need for a parallel key store (as opposed to a native leveled store), which will require keys and metadata to be written to a dedicated AAE store.

> The configuration option `tictacaae_storeheads` is not required to run all-cluster reconciliation, but is recommended to get the full operational feature set of AAE folds.

When enabling Tictac AAE for the first time, it will not be usable by reconciliation until all trees have been built.  Trees will periodically rebuild, and full-sync reconciliation checks should continue to operate as expected during rebuilds.

[assumptions]: {{< baseurl >}}kv/3.4.1/how-to/configure/replication/enable-tictac-aae/
[architecture]: {{< baseurl >}}kv/3.4.1/how-to/configure/replication/enable-tictac-aae/
[check]: {{< baseurl >}}kv/3.4.1/how-to/configure/replication/enable-tictac-aae/
[applychanges]: {{< baseurl >}}kv/3.4.1/how-to/configure/replication/enable-tictac-aae/

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.

# QuickDocs 3.4 content migration report

Generated: 2026-08-28T01:36:07.2911522+09:00

## Outcome

QuickDocs content was split at heading boundaries and copied into **385** versioned Diátaxis pages; **10** additional pages retain mappings for headings that had no body text.

- Source pages: 10
- Source headings: 282 (265 substantive, 17 bodyless)
- Versioned route placements with imported content: 755
- Destination pages mapped: 395
- Internal links rewritten before route replication: 511
- Versioned links validated after replication: 886
- Changed Markdown files: 395

Pages receiving content are marked migrated-needs-review and draft, with quickdocs_content_import set to mechanical-section-split and quickdocs_rewrite_status set to content-migrated-needs-review.

## Migration method

Each QuickDocs heading owns only the body text before the next heading, so parent and child topics can be routed independently without copying a whole QuickDocs page. Imported material is placed after migrated 3.2.5 content when present, or after the page summary otherwise. QuickDocs-relative links are rewritten to the matching versioned route, and Jekyll-only presentation attributes are removed.

The imported blocks are deliberately marked as unreviewed source material: they still need a page-specific rewrite and verification before publication.

## Version handling

OpenRiak KV 3.4.1-only fragments were removed from the 3.4.0 imports. The following source sections required filtering:

| Source page | Section | Anchor |
|---|---|---|
| OperationsAndTroubleshootingGuide | Vnode Status | vnode-status |
| OperationsAndTroubleshootingGuide | Garbage collecting .bak files in leveled | garbage-collecting-bak-files-in-leveled |
| OperationsAndTroubleshootingGuide | Operation Checklist | operation-checklist |
| QueryAPI | accumulation_option (optional - default = keys) | accumulation_option-optional---default--keys |

## Source inventory

| QuickDocs source | Headings | Bytes | SHA-256 |
|---|---:|---:|---|
| [OpenRiak QuickDocs 3.4](https://raw.githubusercontent.com/OpenRiak/riak/openriak-3.4/docs/index.md) | 3 | 3201 | a54ff4780526cf661c0584f072dc621574d8c555ed8a225b9e74473449d487c2 |
| [Riak KV - Building and Scaling a Cluster](https://raw.githubusercontent.com/OpenRiak/riak/openriak-3.4/docs/BuildAndScaleClusterGuide.md) | 15 | 28638 | 81aaab9484994dea200177d112eafa51a469459e65d4be77b6005f5b0e744b0f |
| [Riak KV - Initial Design Decisions](https://raw.githubusercontent.com/OpenRiak/riak/openriak-3.4/docs/InitialDesignDecisions.md) | 26 | 34340 | 471c63c632ba63ca60b56cbbaf34b077abbb9e269152771d9cfbf89917b96e31 |
| [Riak KV - Install and Start](https://raw.githubusercontent.com/OpenRiak/riak/openriak-3.4/docs/InstallAndStartGuide.md) | 31 | 33816 | 4e62784b2764a4fd42522725d0baec563665330a12840c342c9b9084e7d177d5 |
| [Riak KV - Object API](https://raw.githubusercontent.com/OpenRiak/riak/openriak-3.4/docs/ObjectAPI.md) | 24 | 29714 | 01d42beebdc0949ce7508d5881c806040f0b23b873fbbc806ffa538f45297248 |
| [Riak KV - Operations and Troubleshooting](https://raw.githubusercontent.com/OpenRiak/riak/openriak-3.4/docs/OperationsAndTroubleshootingGuide.md) | 56 | 75943 | 6bb86ccbdd3c7794dafcfe413dcba4f6ccd14805cbd676ede20f7c1360099d3a |
| [Riak KV - Other APIs](https://raw.githubusercontent.com/OpenRiak/riak/openriak-3.4/docs/OtherAPI.md) | 30 | 27686 | 71da54e52afa0cc991f8fc044e3309c1ce1c86730ee68c3891f7e23f3d3e1c09 |
| [Riak KV - Query API](https://raw.githubusercontent.com/OpenRiak/riak/openriak-3.4/docs/QueryAPI.md) | 45 | 66295 | c054688f1d866d337cab20c03f189f8a1aabe0aadde25bf98767dfb51be5f4aa |
| [Riak KV - Replication and Reconciliation](https://raw.githubusercontent.com/OpenRiak/riak/openriak-3.4/docs/ReplicationGuide.md) | 35 | 59025 | 58a0eec0277832b72fb7cc0f430bfce8663bf2a180d5831f4976aab360031dde |
| [Riak KV - Theory Guide](https://raw.githubusercontent.com/OpenRiak/riak/openriak-3.4/docs/RiakTheoryGuide.md) | 17 | 37446 | 692dfbd6a1103d467727686d1a20f593681f0ba10720f86db4583591036ad15b |

## Bodyless destination mappings

| Version | Destination |
|---|---|
| 3.4.0 | [explanation/data-model/deletion-policies.md](content/kv/3.4.0/explanation/data-model/deletion-policies.md) |
| 3.4.0 | [explanation/foundations/intra-cluster-resilience.md](content/kv/3.4.0/explanation/foundations/intra-cluster-resilience.md) |
| 3.4.0 | [explanation/operations/garbage-collection.md](content/kv/3.4.0/explanation/operations/garbage-collection.md) |
| 3.4.0 | [explanation/replication/multi-datacenter-architecture.md](content/kv/3.4.0/explanation/replication/multi-datacenter-architecture.md) |
| 3.4.0 | [how-to/operate/check-vnode-status.md](content/kv/3.4.0/how-to/operate/check-vnode-status.md) |
| 3.4.0 | [reference/commands/vnode-status.md](content/kv/3.4.0/reference/commands/vnode-status.md) |
| 3.4.1 | [explanation/data-model/deletion-policies.md](content/kv/3.4.1/explanation/data-model/deletion-policies.md) |
| 3.4.1 | [explanation/foundations/intra-cluster-resilience.md](content/kv/3.4.1/explanation/foundations/intra-cluster-resilience.md) |
| 3.4.1 | [explanation/operations/garbage-collection.md](content/kv/3.4.1/explanation/operations/garbage-collection.md) |
| 3.4.1 | [explanation/replication/multi-datacenter-architecture.md](content/kv/3.4.1/explanation/replication/multi-datacenter-architecture.md) |

## Destination inventory

| Version | Destination | Sections imported | Mapped headings | Source pages | Version-filtered |
|---|---|---:|---:|---|---:|
| 3.4.0 | [explanation/consistency/conditional-requests.md](content/kv/3.4.0/explanation/consistency/conditional-requests.md) | 3 | 3 | ObjectAPI | 0 |
| 3.4.0 | [explanation/consistency/eventual-consistency.md](content/kv/3.4.0/explanation/consistency/eventual-consistency.md) | 1 | 1 | RiakTheoryGuide | 0 |
| 3.4.0 | [explanation/consistency/index.md](content/kv/3.4.0/explanation/consistency/_index.md) | 1 | 1 | QueryAPI | 0 |
| 3.4.0 | [explanation/consistency/read-write-quorums.md](content/kv/3.4.0/explanation/consistency/read-write-quorums.md) | 1 | 1 | RiakTheoryGuide | 0 |
| 3.4.0 | [explanation/consistency/strong-consistency.md](content/kv/3.4.0/explanation/consistency/strong-consistency.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [explanation/data-model/deletion-policies.md](content/kv/3.4.0/explanation/data-model/deletion-policies.md) | 0 | 1 | InitialDesignDecisions | 0 |
| 3.4.0 | [explanation/data-model/keys-objects-and-buckets.md](content/kv/3.4.0/explanation/data-model/keys-objects-and-buckets.md) | 1 | 2 | InitialDesignDecisions | 0 |
| 3.4.0 | [explanation/data-model/latch-objects.md](content/kv/3.4.0/explanation/data-model/latch-objects.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.0 | [explanation/data-model/mapreduce.md](content/kv/3.4.0/explanation/data-model/mapreduce.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [explanation/data-model/merge-strategies.md](content/kv/3.4.0/explanation/data-model/merge-strategies.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.0 | [explanation/data-model/query-api.md](content/kv/3.4.0/explanation/data-model/query-api.md) | 3 | 4 | QueryAPI | 0 |
| 3.4.0 | [explanation/data-model/version-vectors-and-siblings.md](content/kv/3.4.0/explanation/data-model/version-vectors-and-siblings.md) | 3 | 3 | ObjectAPI, QueryAPI, RiakTheoryGuide | 0 |
| 3.4.0 | [explanation/foundations/clusters-rings-and-partitions.md](content/kv/3.4.0/explanation/foundations/clusters-rings-and-partitions.md) | 1 | 2 | InitialDesignDecisions, RiakTheoryGuide | 0 |
| 3.4.0 | [explanation/foundations/history.md](content/kv/3.4.0/explanation/foundations/history.md) | 1 | 1 | index | 0 |
| 3.4.0 | [explanation/foundations/index.md](content/kv/3.4.0/explanation/foundations/_index.md) | 2 | 2 | index, RiakTheoryGuide | 0 |
| 3.4.0 | [explanation/foundations/intra-cluster-resilience.md](content/kv/3.4.0/explanation/foundations/intra-cluster-resilience.md) | 0 | 1 | InitialDesignDecisions | 0 |
| 3.4.0 | [explanation/foundations/use-cases.md](content/kv/3.4.0/explanation/foundations/use-cases.md) | 1 | 1 | index | 0 |
| 3.4.0 | [explanation/foundations/virtual-nodes.md](content/kv/3.4.0/explanation/foundations/virtual-nodes.md) | 1 | 1 | RiakTheoryGuide | 0 |
| 3.4.0 | [explanation/foundations/why-openriak.md](content/kv/3.4.0/explanation/foundations/why-openriak.md) | 1 | 1 | index | 0 |
| 3.4.0 | [explanation/operations/backups-and-restores.md](content/kv/3.4.0/explanation/operations/backups-and-restores.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [explanation/operations/garbage-collection.md](content/kv/3.4.0/explanation/operations/garbage-collection.md) | 0 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [explanation/operations/index.md](content/kv/3.4.0/explanation/operations/_index.md) | 1 | 1 | RiakTheoryGuide | 0 |
| 3.4.0 | [explanation/operations/node-failure-and-recovery.md](content/kv/3.4.0/explanation/operations/node-failure-and-recovery.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [explanation/operations/ring-changes-and-handoffs.md](content/kv/3.4.0/explanation/operations/ring-changes-and-handoffs.md) | 1 | 1 | RiakTheoryGuide | 0 |
| 3.4.0 | [explanation/operations/upgrade-and-downgrade.md](content/kv/3.4.0/explanation/operations/upgrade-and-downgrade.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [explanation/performance/index.md](content/kv/3.4.0/explanation/performance/_index.md) | 2 | 2 | OtherAPI | 0 |
| 3.4.0 | [explanation/performance/latency-throughput-and-capacity.md](content/kv/3.4.0/explanation/performance/latency-throughput-and-capacity.md) | 2 | 3 | ObjectAPI | 0 |
| 3.4.0 | [explanation/performance/query-execution.md](content/kv/3.4.0/explanation/performance/query-execution.md) | 9 | 9 | QueryAPI | 0 |
| 3.4.0 | [explanation/performance/storage-and-filesystem-effects.md](content/kv/3.4.0/explanation/performance/storage-and-filesystem-effects.md) | 2 | 3 | ObjectAPI | 0 |
| 3.4.0 | [explanation/replication/active-anti-entropy.md](content/kv/3.4.0/explanation/replication/active-anti-entropy.md) | 2 | 2 | InitialDesignDecisions, RiakTheoryGuide | 0 |
| 3.4.0 | [explanation/replication/index.md](content/kv/3.4.0/explanation/replication/_index.md) | 2 | 2 | ReplicationGuide | 0 |
| 3.4.0 | [explanation/replication/legacy-aae.md](content/kv/3.4.0/explanation/replication/legacy-aae.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [explanation/replication/multi-datacenter-architecture.md](content/kv/3.4.0/explanation/replication/multi-datacenter-architecture.md) | 0 | 1 | InitialDesignDecisions | 0 |
| 3.4.0 | [explanation/replication/queues.md](content/kv/3.4.0/explanation/replication/queues.md) | 2 | 2 | ReplicationGuide, RiakTheoryGuide | 0 |
| 3.4.0 | [explanation/replication/reconciliation-scope.md](content/kv/3.4.0/explanation/replication/reconciliation-scope.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.0 | [explanation/replication/references-and-triggers.md](content/kv/3.4.0/explanation/replication/references-and-triggers.md) | 2 | 2 | ReplicationGuide | 0 |
| 3.4.0 | [explanation/replication/tictac-aae.md](content/kv/3.4.0/explanation/replication/tictac-aae.md) | 1 | 1 | RiakTheoryGuide | 0 |
| 3.4.0 | [explanation/replication/v2-and-v3-replication.md](content/kv/3.4.0/explanation/replication/v2-and-v3-replication.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.0 | [explanation/storage/bitcask.md](content/kv/3.4.0/explanation/storage/bitcask.md) | 2 | 2 | InitialDesignDecisions, RiakTheoryGuide | 0 |
| 3.4.0 | [explanation/storage/choosing-backend.md](content/kv/3.4.0/explanation/storage/choosing-backend.md) | 1 | 2 | InitialDesignDecisions, RiakTheoryGuide | 0 |
| 3.4.0 | [explanation/storage/index.md](content/kv/3.4.0/explanation/storage/_index.md) | 1 | 1 | RiakTheoryGuide | 0 |
| 3.4.0 | [explanation/storage/leveldb.md](content/kv/3.4.0/explanation/storage/leveldb.md) | 1 | 1 | InitialDesignDecisions | 0 |
| 3.4.0 | [explanation/storage/leveled.md](content/kv/3.4.0/explanation/storage/leveled.md) | 7 | 7 | InitialDesignDecisions, RiakTheoryGuide | 0 |
| 3.4.0 | [explanation/storage/memory.md](content/kv/3.4.0/explanation/storage/memory.md) | 1 | 1 | InitialDesignDecisions | 0 |
| 3.4.0 | [explanation/storage/multi-backend.md](content/kv/3.4.0/explanation/storage/multi-backend.md) | 1 | 1 | InitialDesignDecisions | 0 |
| 3.4.0 | [how-to/configure/advanced-configuration.md](content/kv/3.4.0/how-to/configure/advanced-configuration.md) | 1 | 2 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/configure/api-listeners.md](content/kv/3.4.0/how-to/configure/api-listeners.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.0 | [how-to/configure/backends/bitcask-merge-window.md](content/kv/3.4.0/how-to/configure/backends/bitcask-merge-window.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/configure/backends/bitcask.md](content/kv/3.4.0/how-to/configure/backends/bitcask.md) | 2 | 2 | InitialDesignDecisions, InstallAndStartGuide | 0 |
| 3.4.0 | [how-to/configure/backends/change-backend.md](content/kv/3.4.0/how-to/configure/backends/change-backend.md) | 1 | 1 | InitialDesignDecisions | 0 |
| 3.4.0 | [how-to/configure/backends/index.md](content/kv/3.4.0/how-to/configure/backends/_index.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.0 | [how-to/configure/backends/leveldb.md](content/kv/3.4.0/how-to/configure/backends/leveldb.md) | 1 | 1 | InitialDesignDecisions | 0 |
| 3.4.0 | [how-to/configure/backends/leveled-compaction-window.md](content/kv/3.4.0/how-to/configure/backends/leveled-compaction-window.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/configure/backends/leveled.md](content/kv/3.4.0/how-to/configure/backends/leveled.md) | 2 | 2 | InitialDesignDecisions, InstallAndStartGuide | 0 |
| 3.4.0 | [how-to/configure/backends/memory.md](content/kv/3.4.0/how-to/configure/backends/memory.md) | 1 | 1 | InitialDesignDecisions | 0 |
| 3.4.0 | [how-to/configure/backends/multi.md](content/kv/3.4.0/how-to/configure/backends/multi.md) | 1 | 1 | InitialDesignDecisions | 0 |
| 3.4.0 | [how-to/configure/basic-node-settings.md](content/kv/3.4.0/how-to/configure/basic-node-settings.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.0 | [how-to/configure/global-object-expiration.md](content/kv/3.4.0/how-to/configure/global-object-expiration.md) | 1 | 1 | InitialDesignDecisions | 0 |
| 3.4.0 | [how-to/configure/load-balancing-proxy.md](content/kv/3.4.0/how-to/configure/load-balancing-proxy.md) | 1 | 1 | BuildAndScaleClusterGuide | 0 |
| 3.4.0 | [how-to/configure/logging.md](content/kv/3.4.0/how-to/configure/logging.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/configure/manage-configuration.md](content/kv/3.4.0/how-to/configure/manage-configuration.md) | 1 | 2 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/configure/replication/configure-fullsync.md](content/kv/3.4.0/how-to/configure/replication/configure-fullsync.md) | 3 | 3 | ReplicationGuide | 0 |
| 3.4.0 | [how-to/configure/replication/configure-real-time-replication.md](content/kv/3.4.0/how-to/configure/replication/configure-real-time-replication.md) | 2 | 3 | ReplicationGuide | 0 |
| 3.4.0 | [how-to/configure/replication/configure-sink-nodes.md](content/kv/3.4.0/how-to/configure/replication/configure-sink-nodes.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.0 | [how-to/configure/replication/configure-v2-multi-datacenter.md](content/kv/3.4.0/how-to/configure/replication/configure-v2-multi-datacenter.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.0 | [how-to/configure/replication/enable-tictac-aae.md](content/kv/3.4.0/how-to/configure/replication/enable-tictac-aae.md) | 4 | 4 | InitialDesignDecisions, ReplicationGuide | 0 |
| 3.4.0 | [how-to/configure/replication/exclude-bucket-from-aae.md](content/kv/3.4.0/how-to/configure/replication/exclude-bucket-from-aae.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.0 | [how-to/configure/replication/index.md](content/kv/3.4.0/how-to/configure/replication/_index.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.0 | [how-to/configure/replication/migrate-cluster.md](content/kv/3.4.0/how-to/configure/replication/migrate-cluster.md) | 3 | 3 | InitialDesignDecisions, ReplicationGuide | 0 |
| 3.4.0 | [how-to/configure/replication/per-bucket-reconciliation.md](content/kv/3.4.0/how-to/configure/replication/per-bucket-reconciliation.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.0 | [how-to/configure/replication/secure-replication.md](content/kv/3.4.0/how-to/configure/replication/secure-replication.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.0 | [how-to/configure/runtime-environment-variables.md](content/kv/3.4.0/how-to/configure/runtime-environment-variables.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/configure/verify-configuration.md](content/kv/3.4.0/how-to/configure/verify-configuration.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.0 | [how-to/develop/create-object.md](content/kv/3.4.0/how-to/develop/create-object.md) | 2 | 2 | ObjectAPI | 0 |
| 3.4.0 | [how-to/develop/delete-object.md](content/kv/3.4.0/how-to/develop/delete-object.md) | 2 | 2 | ObjectAPI | 0 |
| 3.4.0 | [how-to/develop/index.md](content/kv/3.4.0/how-to/develop/_index.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.0 | [how-to/develop/query-with-query-api.md](content/kv/3.4.0/how-to/develop/query-with-query-api.md) | 1 | 1 | QueryAPI | 0 |
| 3.4.0 | [how-to/develop/read-object.md](content/kv/3.4.0/how-to/develop/read-object.md) | 2 | 2 | ObjectAPI | 0 |
| 3.4.0 | [how-to/develop/send-conditional-object-request.md](content/kv/3.4.0/how-to/develop/send-conditional-object-request.md) | 3 | 3 | ObjectAPI | 0 |
| 3.4.0 | [how-to/develop/update-object.md](content/kv/3.4.0/how-to/develop/update-object.md) | 2 | 2 | ObjectAPI | 0 |
| 3.4.0 | [how-to/develop/use-write-once-path.md](content/kv/3.4.0/how-to/develop/use-write-once-path.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [how-to/develop/write-commit-hook.md](content/kv/3.4.0/how-to/develop/write-commit-hook.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.0 | [how-to/install/index.md](content/kv/3.4.0/how-to/install/_index.md) | 2 | 3 | InstallAndStartGuide | 0 |
| 3.4.0 | [how-to/install/source.md](content/kv/3.4.0/how-to/install/source.md) | 6 | 6 | InstallAndStartGuide | 0 |
| 3.4.0 | [how-to/install/verify-installation.md](content/kv/3.4.0/how-to/install/verify-installation.md) | 1 | 2 | InstallAndStartGuide | 0 |
| 3.4.0 | [how-to/operate/aae-fold/erase-keys.md](content/kv/3.4.0/how-to/operate/aae-fold/erase-keys.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [how-to/operate/aae-fold/find-keys.md](content/kv/3.4.0/how-to/operate/aae-fold/find-keys.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [how-to/operate/aae-fold/find-tombstones.md](content/kv/3.4.0/how-to/operate/aae-fold/find-tombstones.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [how-to/operate/aae-fold/index.md](content/kv/3.4.0/how-to/operate/aae-fold/_index.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [how-to/operate/aae-fold/list-buckets.md](content/kv/3.4.0/how-to/operate/aae-fold/list-buckets.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [how-to/operate/aae-fold/object-statistics.md](content/kv/3.4.0/how-to/operate/aae-fold/object-statistics.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [how-to/operate/aae-fold/reap-tombstones.md](content/kv/3.4.0/how-to/operate/aae-fold/reap-tombstones.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [how-to/operate/aae-fold/repair-key-range.md](content/kv/3.4.0/how-to/operate/aae-fold/repair-key-range.md) | 2 | 2 | OperationsAndTroubleshootingGuide, OtherAPI | 0 |
| 3.4.0 | [how-to/operate/aae-fold/run-from-command-line.md](content/kv/3.4.0/how-to/operate/aae-fold/run-from-command-line.md) | 2 | 2 | OperationsAndTroubleshootingGuide, OtherAPI | 0 |
| 3.4.0 | [how-to/operate/add-node.md](content/kv/3.4.0/how-to/operate/add-node.md) | 2 | 2 | BuildAndScaleClusterGuide | 0 |
| 3.4.0 | [how-to/operate/back-up-node.md](content/kv/3.4.0/how-to/operate/back-up-node.md) | 5 | 5 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/operate/check-vnode-status.md](content/kv/3.4.0/how-to/operate/check-vnode-status.md) | 0 | 1 | OperationsAndTroubleshootingGuide | 1 |
| 3.4.0 | [how-to/operate/index.md](content/kv/3.4.0/how-to/operate/_index.md) | 2 | 2 | BuildAndScaleClusterGuide, OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/operate/inspect-data.md](content/kv/3.4.0/how-to/operate/inspect-data.md) | 2 | 2 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/operate/manage-bucket-types.md](content/kv/3.4.0/how-to/operate/manage-bucket-types.md) | 11 | 11 | InstallAndStartGuide | 0 |
| 3.4.0 | [how-to/operate/manage-handoffs.md](content/kv/3.4.0/how-to/operate/manage-handoffs.md) | 1 | 1 | BuildAndScaleClusterGuide | 0 |
| 3.4.0 | [how-to/operate/monitor-active-anti-entropy.md](content/kv/3.4.0/how-to/operate/monitor-active-anti-entropy.md) | 4 | 4 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/operate/monitor-read-repairs.md](content/kv/3.4.0/how-to/operate/monitor-read-repairs.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/operate/monitor-reconciliation.md](content/kv/3.4.0/how-to/operate/monitor-reconciliation.md) | 3 | 4 | OperationsAndTroubleshootingGuide, ReplicationGuide | 0 |
| 3.4.0 | [how-to/operate/monitor-worker-pools.md](content/kv/3.4.0/how-to/operate/monitor-worker-pools.md) | 4 | 4 | OperationsAndTroubleshootingGuide, OtherAPI, ReplicationGuide | 0 |
| 3.4.0 | [how-to/operate/plan-and-commit-cluster-change.md](content/kv/3.4.0/how-to/operate/plan-and-commit-cluster-change.md) | 4 | 4 | BuildAndScaleClusterGuide | 0 |
| 3.4.0 | [how-to/operate/rebuild-aae-trees.md](content/kv/3.4.0/how-to/operate/rebuild-aae-trees.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/operate/remove-leveled-backup-files.md](content/kv/3.4.0/how-to/operate/remove-leveled-backup-files.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 1 |
| 3.4.0 | [how-to/operate/remove-node.md](content/kv/3.4.0/how-to/operate/remove-node.md) | 1 | 1 | BuildAndScaleClusterGuide | 0 |
| 3.4.0 | [how-to/operate/repair-leveled-store.md](content/kv/3.4.0/how-to/operate/repair-leveled-store.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/operate/repair-vnode.md](content/kv/3.4.0/how-to/operate/repair-vnode.md) | 2 | 2 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/operate/replace-node.md](content/kv/3.4.0/how-to/operate/replace-node.md) | 3 | 3 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/operate/rereplicate-time-window.md](content/kv/3.4.0/how-to/operate/rereplicate-time-window.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.0 | [how-to/operate/restore-node.md](content/kv/3.4.0/how-to/operate/restore-node.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/operate/rolling-replacement.md](content/kv/3.4.0/how-to/operate/rolling-replacement.md) | 2 | 2 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/operate/rolling-restart.md](content/kv/3.4.0/how-to/operate/rolling-restart.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/operate/routine-operations-checklist.md](content/kv/3.4.0/how-to/operate/routine-operations-checklist.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 1 |
| 3.4.0 | [how-to/operate/schedule-object-reaping.md](content/kv/3.4.0/how-to/operate/schedule-object-reaping.md) | 2 | 3 | InitialDesignDecisions, OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/operate/start-stop-restart-node.md](content/kv/3.4.0/how-to/operate/start-stop-restart-node.md) | 3 | 4 | InstallAndStartGuide | 0 |
| 3.4.0 | [how-to/operate/upgrade-cluster.md](content/kv/3.4.0/how-to/operate/upgrade-cluster.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/operate/use-remote-console.md](content/kv/3.4.0/how-to/operate/use-remote-console.md) | 2 | 2 | OperationsAndTroubleshootingGuide, OtherAPI | 0 |
| 3.4.0 | [how-to/plan/choose-deletion-policy.md](content/kv/3.4.0/how-to/plan/choose-deletion-policy.md) | 2 | 3 | InitialDesignDecisions, InstallAndStartGuide | 0 |
| 3.4.0 | [how-to/plan/choose-intra-cluster-resilience.md](content/kv/3.4.0/how-to/plan/choose-intra-cluster-resilience.md) | 3 | 4 | InitialDesignDecisions | 0 |
| 3.4.0 | [how-to/plan/choose-multi-cluster-topology.md](content/kv/3.4.0/how-to/plan/choose-multi-cluster-topology.md) | 1 | 2 | InitialDesignDecisions | 0 |
| 3.4.0 | [how-to/plan/choose-ring-size.md](content/kv/3.4.0/how-to/plan/choose-ring-size.md) | 1 | 2 | InitialDesignDecisions | 0 |
| 3.4.0 | [how-to/plan/choose-storage-backend.md](content/kv/3.4.0/how-to/plan/choose-storage-backend.md) | 1 | 2 | InitialDesignDecisions | 0 |
| 3.4.0 | [how-to/plan/index.md](content/kv/3.4.0/how-to/plan/_index.md) | 2 | 2 | BuildAndScaleClusterGuide, InitialDesignDecisions | 0 |
| 3.4.0 | [how-to/plan/map-data-to-objects.md](content/kv/3.4.0/how-to/plan/map-data-to-objects.md) | 2 | 3 | InitialDesignDecisions | 0 |
| 3.4.0 | [how-to/plan/production-readiness-checklist.md](content/kv/3.4.0/how-to/plan/production-readiness-checklist.md) | 1 | 1 | BuildAndScaleClusterGuide | 0 |
| 3.4.0 | [how-to/plan/size-cluster.md](content/kv/3.4.0/how-to/plan/size-cluster.md) | 2 | 2 | BuildAndScaleClusterGuide | 0 |
| 3.4.0 | [how-to/secure/configure-tls.md](content/kv/3.4.0/how-to/secure/configure-tls.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/secure/enable-security.md](content/kv/3.4.0/how-to/secure/enable-security.md) | 2 | 2 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/secure/index.md](content/kv/3.4.0/how-to/secure/_index.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/secure/manage-permissions.md](content/kv/3.4.0/how-to/secure/manage-permissions.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/secure/manage-sources.md](content/kv/3.4.0/how-to/secure/manage-sources.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/secure/secure-networking.md](content/kv/3.4.0/how-to/secure/secure-networking.md) | 1 | 1 | BuildAndScaleClusterGuide | 0 |
| 3.4.0 | [how-to/troubleshoot/erlang-vm.md](content/kv/3.4.0/how-to/troubleshoot/erlang-vm.md) | 5 | 5 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/troubleshoot/index.md](content/kv/3.4.0/how-to/troubleshoot/_index.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/troubleshoot/recover-failed-node.md](content/kv/3.4.0/how-to/troubleshoot/recover-failed-node.md) | 3 | 3 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/tune/benchmark-cluster.md](content/kv/3.4.0/how-to/tune/benchmark-cluster.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [how-to/tune/set-open-files-limit.md](content/kv/3.4.0/how-to/tune/set-open-files-limit.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.0 | [index.md](content/kv/3.4.0/_index.md) | 1 | 1 | index | 0 |
| 3.4.0 | [reference/aae-fold-api/erase-keys.md](content/kv/3.4.0/reference/aae-fold-api/erase-keys.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [reference/aae-fold-api/find-keys.md](content/kv/3.4.0/reference/aae-fold-api/find-keys.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [reference/aae-fold-api/find-tombstones.md](content/kv/3.4.0/reference/aae-fold-api/find-tombstones.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [reference/aae-fold-api/index.md](content/kv/3.4.0/reference/aae-fold-api/_index.md) | 13 | 13 | OtherAPI | 0 |
| 3.4.0 | [reference/aae-fold-api/list-buckets.md](content/kv/3.4.0/reference/aae-fold-api/list-buckets.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [reference/aae-fold-api/object-statistics.md](content/kv/3.4.0/reference/aae-fold-api/object-statistics.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [reference/aae-fold-api/reap-tombstones.md](content/kv/3.4.0/reference/aae-fold-api/reap-tombstones.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [reference/aae-fold-api/repair-key-range.md](content/kv/3.4.0/reference/aae-fold-api/repair-key-range.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [reference/commands/aae.md](content/kv/3.4.0/reference/commands/aae.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [reference/commands/vnode-status.md](content/kv/3.4.0/reference/commands/vnode-status.md) | 0 | 1 | OperationsAndTroubleshootingGuide | 1 |
| 3.4.0 | [reference/configuration/bucket-properties.md](content/kv/3.4.0/reference/configuration/bucket-properties.md) | 14 | 14 | InitialDesignDecisions, InstallAndStartGuide | 0 |
| 3.4.0 | [reference/configuration/networking.md](content/kv/3.4.0/reference/configuration/networking.md) | 1 | 1 | BuildAndScaleClusterGuide | 0 |
| 3.4.0 | [reference/configuration/replication.md](content/kv/3.4.0/reference/configuration/replication.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.0 | [reference/data/content-types.md](content/kv/3.4.0/reference/data/content-types.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.0 | [reference/data/distributed-data-types.md](content/kv/3.4.0/reference/data/distributed-data-types.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [reference/data/index.md](content/kv/3.4.0/reference/data/_index.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.0 | [reference/data/keys-and-objects.md](content/kv/3.4.0/reference/data/keys-and-objects.md) | 2 | 2 | ObjectAPI | 0 |
| 3.4.0 | [reference/data/object-metadata.md](content/kv/3.4.0/reference/data/object-metadata.md) | 3 | 3 | ObjectAPI | 0 |
| 3.4.0 | [reference/data/secondary-indexes.md](content/kv/3.4.0/reference/data/secondary-indexes.md) | 2 | 2 | ObjectAPI, QueryAPI | 0 |
| 3.4.0 | [reference/data/version-vectors.md](content/kv/3.4.0/reference/data/version-vectors.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.0 | [reference/http-api/conditional-requests.md](content/kv/3.4.0/reference/http-api/conditional-requests.md) | 4 | 4 | ObjectAPI | 0 |
| 3.4.0 | [reference/http-api/delete-object.md](content/kv/3.4.0/reference/http-api/delete-object.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.0 | [reference/http-api/fetch-object.md](content/kv/3.4.0/reference/http-api/fetch-object.md) | 2 | 2 | ObjectAPI | 0 |
| 3.4.0 | [reference/http-api/index.md](content/kv/3.4.0/reference/http-api/_index.md) | 2 | 2 | ObjectAPI | 0 |
| 3.4.0 | [reference/http-api/mapreduce.md](content/kv/3.4.0/reference/http-api/mapreduce.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [reference/http-api/object-request-options.md](content/kv/3.4.0/reference/http-api/object-request-options.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.0 | [reference/http-api/store-object.md](content/kv/3.4.0/reference/http-api/store-object.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.0 | [reference/operations/cluster-claim-algorithms.md](content/kv/3.4.0/reference/operations/cluster-claim-algorithms.md) | 3 | 3 | BuildAndScaleClusterGuide | 0 |
| 3.4.0 | [reference/operations/custom-code.md](content/kv/3.4.0/reference/operations/custom-code.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.0 | [reference/operations/log-files.md](content/kv/3.4.0/reference/operations/log-files.md) | 1 | 2 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [reference/operations/object-deletion.md](content/kv/3.4.0/reference/operations/object-deletion.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.0 | [reference/operations/remote-console.md](content/kv/3.4.0/reference/operations/remote-console.md) | 3 | 3 | OperationsAndTroubleshootingGuide, OtherAPI | 0 |
| 3.4.0 | [reference/operations/replication-statistics.md](content/kv/3.4.0/reference/operations/replication-statistics.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.0 | [reference/operations/statistics-and-monitoring.md](content/kv/3.4.0/reference/operations/statistics-and-monitoring.md) | 2 | 4 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [reference/query-api/accumulation-options.md](content/kv/3.4.0/reference/query-api/accumulation-options.md) | 2 | 2 | QueryAPI | 1 |
| 3.4.0 | [reference/query-api/expressions.md](content/kv/3.4.0/reference/query-api/expressions.md) | 5 | 5 | QueryAPI | 0 |
| 3.4.0 | [reference/query-api/index.md](content/kv/3.4.0/reference/query-api/_index.md) | 2 | 2 | QueryAPI | 0 |
| 3.4.0 | [reference/query-api/limits.md](content/kv/3.4.0/reference/query-api/limits.md) | 8 | 9 | QueryAPI | 0 |
| 3.4.0 | [reference/query-api/request.md](content/kv/3.4.0/reference/query-api/request.md) | 8 | 9 | QueryAPI | 0 |
| 3.4.0 | [reference/query-api/responses.md](content/kv/3.4.0/reference/query-api/responses.md) | 1 | 1 | QueryAPI | 0 |
| 3.4.0 | [reference/releases/downloads.md](content/kv/3.4.0/reference/releases/downloads.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.0 | [reference/releases/supported-platforms.md](content/kv/3.4.0/reference/releases/supported-platforms.md) | 2 | 2 | InstallAndStartGuide | 0 |
| 3.4.0 | [reference/replication-api/index.md](content/kv/3.4.0/reference/replication-api/_index.md) | 3 | 3 | OtherAPI, ReplicationGuide | 0 |
| 3.4.0 | [reference/replication-api/runtime-controls.md](content/kv/3.4.0/reference/replication-api/runtime-controls.md) | 11 | 12 | ReplicationGuide | 0 |
| 3.4.0 | [reference/specialized-apis/cluster-metadata.md](content/kv/3.4.0/reference/specialized-apis/cluster-metadata.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.0 | [reference/specialized-apis/data-type-api.md](content/kv/3.4.0/reference/specialized-apis/data-type-api.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [reference/specialized-apis/fetch-api.md](content/kv/3.4.0/reference/specialized-apis/fetch-api.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [reference/specialized-apis/index.md](content/kv/3.4.0/reference/specialized-apis/_index.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [reference/specialized-apis/legacy-query-api.md](content/kv/3.4.0/reference/specialized-apis/legacy-query-api.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [reference/specialized-apis/list-api.md](content/kv/3.4.0/reference/specialized-apis/list-api.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [reference/specialized-apis/strong-consistency-api.md](content/kv/3.4.0/reference/specialized-apis/strong-consistency-api.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [reference/specialized-apis/write-once-api.md](content/kv/3.4.0/reference/specialized-apis/write-once-api.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.0 | [tutorials/first-cluster/index.md](content/kv/3.4.0/tutorials/first-cluster/_index.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.0 | [tutorials/query-api/build-search-index.md](content/kv/3.4.0/tutorials/query-api/build-search-index.md) | 12 | 12 | QueryAPI | 0 |
| 3.4.0 | [tutorials/query-api/index.md](content/kv/3.4.0/tutorials/query-api/_index.md) | 1 | 1 | QueryAPI | 0 |
| 3.4.1 | [explanation/consistency/conditional-requests.md](content/kv/3.4.1/explanation/consistency/conditional-requests.md) | 3 | 3 | ObjectAPI | 0 |
| 3.4.1 | [explanation/consistency/eventual-consistency.md](content/kv/3.4.1/explanation/consistency/eventual-consistency.md) | 1 | 1 | RiakTheoryGuide | 0 |
| 3.4.1 | [explanation/consistency/index.md](content/kv/3.4.1/explanation/consistency/_index.md) | 1 | 1 | QueryAPI | 0 |
| 3.4.1 | [explanation/consistency/read-write-quorums.md](content/kv/3.4.1/explanation/consistency/read-write-quorums.md) | 1 | 1 | RiakTheoryGuide | 0 |
| 3.4.1 | [explanation/consistency/strong-consistency.md](content/kv/3.4.1/explanation/consistency/strong-consistency.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [explanation/data-model/deletion-policies.md](content/kv/3.4.1/explanation/data-model/deletion-policies.md) | 0 | 1 | InitialDesignDecisions | 0 |
| 3.4.1 | [explanation/data-model/keys-objects-and-buckets.md](content/kv/3.4.1/explanation/data-model/keys-objects-and-buckets.md) | 1 | 2 | InitialDesignDecisions | 0 |
| 3.4.1 | [explanation/data-model/latch-objects.md](content/kv/3.4.1/explanation/data-model/latch-objects.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.1 | [explanation/data-model/mapreduce.md](content/kv/3.4.1/explanation/data-model/mapreduce.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [explanation/data-model/merge-strategies.md](content/kv/3.4.1/explanation/data-model/merge-strategies.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.1 | [explanation/data-model/query-api.md](content/kv/3.4.1/explanation/data-model/query-api.md) | 3 | 4 | QueryAPI | 0 |
| 3.4.1 | [explanation/data-model/version-vectors-and-siblings.md](content/kv/3.4.1/explanation/data-model/version-vectors-and-siblings.md) | 3 | 3 | ObjectAPI, QueryAPI, RiakTheoryGuide | 0 |
| 3.4.1 | [explanation/foundations/clusters-rings-and-partitions.md](content/kv/3.4.1/explanation/foundations/clusters-rings-and-partitions.md) | 1 | 2 | InitialDesignDecisions, RiakTheoryGuide | 0 |
| 3.4.1 | [explanation/foundations/history.md](content/kv/3.4.1/explanation/foundations/history.md) | 1 | 1 | index | 0 |
| 3.4.1 | [explanation/foundations/index.md](content/kv/3.4.1/explanation/foundations/_index.md) | 2 | 2 | index, RiakTheoryGuide | 0 |
| 3.4.1 | [explanation/foundations/intra-cluster-resilience.md](content/kv/3.4.1/explanation/foundations/intra-cluster-resilience.md) | 0 | 1 | InitialDesignDecisions | 0 |
| 3.4.1 | [explanation/foundations/use-cases.md](content/kv/3.4.1/explanation/foundations/use-cases.md) | 1 | 1 | index | 0 |
| 3.4.1 | [explanation/foundations/virtual-nodes.md](content/kv/3.4.1/explanation/foundations/virtual-nodes.md) | 1 | 1 | RiakTheoryGuide | 0 |
| 3.4.1 | [explanation/foundations/why-openriak.md](content/kv/3.4.1/explanation/foundations/why-openriak.md) | 1 | 1 | index | 0 |
| 3.4.1 | [explanation/operations/backups-and-restores.md](content/kv/3.4.1/explanation/operations/backups-and-restores.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [explanation/operations/garbage-collection.md](content/kv/3.4.1/explanation/operations/garbage-collection.md) | 0 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [explanation/operations/index.md](content/kv/3.4.1/explanation/operations/_index.md) | 1 | 1 | RiakTheoryGuide | 0 |
| 3.4.1 | [explanation/operations/node-failure-and-recovery.md](content/kv/3.4.1/explanation/operations/node-failure-and-recovery.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [explanation/operations/ring-changes-and-handoffs.md](content/kv/3.4.1/explanation/operations/ring-changes-and-handoffs.md) | 1 | 1 | RiakTheoryGuide | 0 |
| 3.4.1 | [explanation/operations/upgrade-and-downgrade.md](content/kv/3.4.1/explanation/operations/upgrade-and-downgrade.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [explanation/performance/index.md](content/kv/3.4.1/explanation/performance/_index.md) | 2 | 2 | OtherAPI | 0 |
| 3.4.1 | [explanation/performance/latency-throughput-and-capacity.md](content/kv/3.4.1/explanation/performance/latency-throughput-and-capacity.md) | 2 | 3 | ObjectAPI | 0 |
| 3.4.1 | [explanation/performance/query-execution.md](content/kv/3.4.1/explanation/performance/query-execution.md) | 9 | 9 | QueryAPI | 0 |
| 3.4.1 | [explanation/performance/storage-and-filesystem-effects.md](content/kv/3.4.1/explanation/performance/storage-and-filesystem-effects.md) | 2 | 3 | ObjectAPI | 0 |
| 3.4.1 | [explanation/replication/active-anti-entropy.md](content/kv/3.4.1/explanation/replication/active-anti-entropy.md) | 2 | 2 | InitialDesignDecisions, RiakTheoryGuide | 0 |
| 3.4.1 | [explanation/replication/index.md](content/kv/3.4.1/explanation/replication/_index.md) | 2 | 2 | ReplicationGuide | 0 |
| 3.4.1 | [explanation/replication/legacy-aae.md](content/kv/3.4.1/explanation/replication/legacy-aae.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [explanation/replication/multi-datacenter-architecture.md](content/kv/3.4.1/explanation/replication/multi-datacenter-architecture.md) | 0 | 1 | InitialDesignDecisions | 0 |
| 3.4.1 | [explanation/replication/queues.md](content/kv/3.4.1/explanation/replication/queues.md) | 2 | 2 | ReplicationGuide, RiakTheoryGuide | 0 |
| 3.4.1 | [explanation/replication/reconciliation-scope.md](content/kv/3.4.1/explanation/replication/reconciliation-scope.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.1 | [explanation/replication/references-and-triggers.md](content/kv/3.4.1/explanation/replication/references-and-triggers.md) | 2 | 2 | ReplicationGuide | 0 |
| 3.4.1 | [explanation/replication/tictac-aae.md](content/kv/3.4.1/explanation/replication/tictac-aae.md) | 1 | 1 | RiakTheoryGuide | 0 |
| 3.4.1 | [explanation/replication/v2-and-v3-replication.md](content/kv/3.4.1/explanation/replication/v2-and-v3-replication.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.1 | [explanation/storage/bitcask.md](content/kv/3.4.1/explanation/storage/bitcask.md) | 2 | 2 | InitialDesignDecisions, RiakTheoryGuide | 0 |
| 3.4.1 | [explanation/storage/choosing-backend.md](content/kv/3.4.1/explanation/storage/choosing-backend.md) | 1 | 2 | InitialDesignDecisions, RiakTheoryGuide | 0 |
| 3.4.1 | [explanation/storage/index.md](content/kv/3.4.1/explanation/storage/_index.md) | 1 | 1 | RiakTheoryGuide | 0 |
| 3.4.1 | [explanation/storage/leveldb.md](content/kv/3.4.1/explanation/storage/leveldb.md) | 1 | 1 | InitialDesignDecisions | 0 |
| 3.4.1 | [explanation/storage/leveled.md](content/kv/3.4.1/explanation/storage/leveled.md) | 7 | 7 | InitialDesignDecisions, RiakTheoryGuide | 0 |
| 3.4.1 | [explanation/storage/memory.md](content/kv/3.4.1/explanation/storage/memory.md) | 1 | 1 | InitialDesignDecisions | 0 |
| 3.4.1 | [explanation/storage/multi-backend.md](content/kv/3.4.1/explanation/storage/multi-backend.md) | 1 | 1 | InitialDesignDecisions | 0 |
| 3.4.1 | [how-to/configure/advanced-configuration.md](content/kv/3.4.1/how-to/configure/advanced-configuration.md) | 1 | 2 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/configure/api-listeners.md](content/kv/3.4.1/how-to/configure/api-listeners.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.1 | [how-to/configure/backends/bitcask-merge-window.md](content/kv/3.4.1/how-to/configure/backends/bitcask-merge-window.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/configure/backends/bitcask.md](content/kv/3.4.1/how-to/configure/backends/bitcask.md) | 2 | 2 | InitialDesignDecisions, InstallAndStartGuide | 0 |
| 3.4.1 | [how-to/configure/backends/change-backend.md](content/kv/3.4.1/how-to/configure/backends/change-backend.md) | 1 | 1 | InitialDesignDecisions | 0 |
| 3.4.1 | [how-to/configure/backends/index.md](content/kv/3.4.1/how-to/configure/backends/_index.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.1 | [how-to/configure/backends/leveldb.md](content/kv/3.4.1/how-to/configure/backends/leveldb.md) | 1 | 1 | InitialDesignDecisions | 0 |
| 3.4.1 | [how-to/configure/backends/leveled-compaction-window.md](content/kv/3.4.1/how-to/configure/backends/leveled-compaction-window.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/configure/backends/leveled.md](content/kv/3.4.1/how-to/configure/backends/leveled.md) | 2 | 2 | InitialDesignDecisions, InstallAndStartGuide | 0 |
| 3.4.1 | [how-to/configure/backends/memory.md](content/kv/3.4.1/how-to/configure/backends/memory.md) | 1 | 1 | InitialDesignDecisions | 0 |
| 3.4.1 | [how-to/configure/backends/multi.md](content/kv/3.4.1/how-to/configure/backends/multi.md) | 1 | 1 | InitialDesignDecisions | 0 |
| 3.4.1 | [how-to/configure/basic-node-settings.md](content/kv/3.4.1/how-to/configure/basic-node-settings.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.1 | [how-to/configure/global-object-expiration.md](content/kv/3.4.1/how-to/configure/global-object-expiration.md) | 1 | 1 | InitialDesignDecisions | 0 |
| 3.4.1 | [how-to/configure/load-balancing-proxy.md](content/kv/3.4.1/how-to/configure/load-balancing-proxy.md) | 1 | 1 | BuildAndScaleClusterGuide | 0 |
| 3.4.1 | [how-to/configure/logging.md](content/kv/3.4.1/how-to/configure/logging.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/configure/manage-configuration.md](content/kv/3.4.1/how-to/configure/manage-configuration.md) | 1 | 2 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/configure/replication/configure-fullsync.md](content/kv/3.4.1/how-to/configure/replication/configure-fullsync.md) | 3 | 3 | ReplicationGuide | 0 |
| 3.4.1 | [how-to/configure/replication/configure-real-time-replication.md](content/kv/3.4.1/how-to/configure/replication/configure-real-time-replication.md) | 2 | 3 | ReplicationGuide | 0 |
| 3.4.1 | [how-to/configure/replication/configure-sink-nodes.md](content/kv/3.4.1/how-to/configure/replication/configure-sink-nodes.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.1 | [how-to/configure/replication/configure-v2-multi-datacenter.md](content/kv/3.4.1/how-to/configure/replication/configure-v2-multi-datacenter.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.1 | [how-to/configure/replication/enable-tictac-aae.md](content/kv/3.4.1/how-to/configure/replication/enable-tictac-aae.md) | 4 | 4 | InitialDesignDecisions, ReplicationGuide | 0 |
| 3.4.1 | [how-to/configure/replication/exclude-bucket-from-aae.md](content/kv/3.4.1/how-to/configure/replication/exclude-bucket-from-aae.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.1 | [how-to/configure/replication/index.md](content/kv/3.4.1/how-to/configure/replication/_index.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.1 | [how-to/configure/replication/migrate-cluster.md](content/kv/3.4.1/how-to/configure/replication/migrate-cluster.md) | 3 | 3 | InitialDesignDecisions, ReplicationGuide | 0 |
| 3.4.1 | [how-to/configure/replication/per-bucket-reconciliation.md](content/kv/3.4.1/how-to/configure/replication/per-bucket-reconciliation.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.1 | [how-to/configure/replication/secure-replication.md](content/kv/3.4.1/how-to/configure/replication/secure-replication.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.1 | [how-to/configure/runtime-environment-variables.md](content/kv/3.4.1/how-to/configure/runtime-environment-variables.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/configure/verify-configuration.md](content/kv/3.4.1/how-to/configure/verify-configuration.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.1 | [how-to/develop/create-object.md](content/kv/3.4.1/how-to/develop/create-object.md) | 2 | 2 | ObjectAPI | 0 |
| 3.4.1 | [how-to/develop/delete-object.md](content/kv/3.4.1/how-to/develop/delete-object.md) | 2 | 2 | ObjectAPI | 0 |
| 3.4.1 | [how-to/develop/index.md](content/kv/3.4.1/how-to/develop/_index.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.1 | [how-to/develop/query-with-query-api.md](content/kv/3.4.1/how-to/develop/query-with-query-api.md) | 1 | 1 | QueryAPI | 0 |
| 3.4.1 | [how-to/develop/read-object.md](content/kv/3.4.1/how-to/develop/read-object.md) | 2 | 2 | ObjectAPI | 0 |
| 3.4.1 | [how-to/develop/send-conditional-object-request.md](content/kv/3.4.1/how-to/develop/send-conditional-object-request.md) | 3 | 3 | ObjectAPI | 0 |
| 3.4.1 | [how-to/develop/update-object.md](content/kv/3.4.1/how-to/develop/update-object.md) | 2 | 2 | ObjectAPI | 0 |
| 3.4.1 | [how-to/develop/use-write-once-path.md](content/kv/3.4.1/how-to/develop/use-write-once-path.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [how-to/develop/write-commit-hook.md](content/kv/3.4.1/how-to/develop/write-commit-hook.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.1 | [how-to/install/index.md](content/kv/3.4.1/how-to/install/_index.md) | 2 | 3 | InstallAndStartGuide | 0 |
| 3.4.1 | [how-to/install/source.md](content/kv/3.4.1/how-to/install/source.md) | 6 | 6 | InstallAndStartGuide | 0 |
| 3.4.1 | [how-to/install/verify-installation.md](content/kv/3.4.1/how-to/install/verify-installation.md) | 1 | 2 | InstallAndStartGuide | 0 |
| 3.4.1 | [how-to/operate/aae-fold/erase-keys.md](content/kv/3.4.1/how-to/operate/aae-fold/erase-keys.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [how-to/operate/aae-fold/find-keys.md](content/kv/3.4.1/how-to/operate/aae-fold/find-keys.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [how-to/operate/aae-fold/find-tombstones.md](content/kv/3.4.1/how-to/operate/aae-fold/find-tombstones.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [how-to/operate/aae-fold/index.md](content/kv/3.4.1/how-to/operate/aae-fold/_index.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [how-to/operate/aae-fold/list-buckets.md](content/kv/3.4.1/how-to/operate/aae-fold/list-buckets.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [how-to/operate/aae-fold/object-statistics.md](content/kv/3.4.1/how-to/operate/aae-fold/object-statistics.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [how-to/operate/aae-fold/reap-tombstones.md](content/kv/3.4.1/how-to/operate/aae-fold/reap-tombstones.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [how-to/operate/aae-fold/repair-key-range.md](content/kv/3.4.1/how-to/operate/aae-fold/repair-key-range.md) | 2 | 2 | OperationsAndTroubleshootingGuide, OtherAPI | 0 |
| 3.4.1 | [how-to/operate/aae-fold/run-from-command-line.md](content/kv/3.4.1/how-to/operate/aae-fold/run-from-command-line.md) | 2 | 2 | OperationsAndTroubleshootingGuide, OtherAPI | 0 |
| 3.4.1 | [how-to/operate/add-node.md](content/kv/3.4.1/how-to/operate/add-node.md) | 2 | 2 | BuildAndScaleClusterGuide | 0 |
| 3.4.1 | [how-to/operate/back-up-node.md](content/kv/3.4.1/how-to/operate/back-up-node.md) | 5 | 5 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/check-vnode-status.md](content/kv/3.4.1/how-to/operate/check-vnode-status.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/index.md](content/kv/3.4.1/how-to/operate/_index.md) | 2 | 2 | BuildAndScaleClusterGuide, OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/inspect-data.md](content/kv/3.4.1/how-to/operate/inspect-data.md) | 2 | 2 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/manage-bucket-types.md](content/kv/3.4.1/how-to/operate/manage-bucket-types.md) | 11 | 11 | InstallAndStartGuide | 0 |
| 3.4.1 | [how-to/operate/manage-handoffs.md](content/kv/3.4.1/how-to/operate/manage-handoffs.md) | 1 | 1 | BuildAndScaleClusterGuide | 0 |
| 3.4.1 | [how-to/operate/monitor-active-anti-entropy.md](content/kv/3.4.1/how-to/operate/monitor-active-anti-entropy.md) | 4 | 4 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/monitor-read-repairs.md](content/kv/3.4.1/how-to/operate/monitor-read-repairs.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/monitor-reconciliation.md](content/kv/3.4.1/how-to/operate/monitor-reconciliation.md) | 3 | 4 | OperationsAndTroubleshootingGuide, ReplicationGuide | 0 |
| 3.4.1 | [how-to/operate/monitor-worker-pools.md](content/kv/3.4.1/how-to/operate/monitor-worker-pools.md) | 4 | 4 | OperationsAndTroubleshootingGuide, OtherAPI, ReplicationGuide | 0 |
| 3.4.1 | [how-to/operate/plan-and-commit-cluster-change.md](content/kv/3.4.1/how-to/operate/plan-and-commit-cluster-change.md) | 4 | 4 | BuildAndScaleClusterGuide | 0 |
| 3.4.1 | [how-to/operate/rebuild-aae-trees.md](content/kv/3.4.1/how-to/operate/rebuild-aae-trees.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/remove-leveled-backup-files.md](content/kv/3.4.1/how-to/operate/remove-leveled-backup-files.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/remove-node.md](content/kv/3.4.1/how-to/operate/remove-node.md) | 1 | 1 | BuildAndScaleClusterGuide | 0 |
| 3.4.1 | [how-to/operate/repair-leveled-store.md](content/kv/3.4.1/how-to/operate/repair-leveled-store.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/repair-vnode.md](content/kv/3.4.1/how-to/operate/repair-vnode.md) | 2 | 2 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/replace-node.md](content/kv/3.4.1/how-to/operate/replace-node.md) | 3 | 3 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/rereplicate-time-window.md](content/kv/3.4.1/how-to/operate/rereplicate-time-window.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.1 | [how-to/operate/restore-node.md](content/kv/3.4.1/how-to/operate/restore-node.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/resync-bucket.md](content/kv/3.4.1/how-to/operate/resync-bucket.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.1 | [how-to/operate/rolling-replacement.md](content/kv/3.4.1/how-to/operate/rolling-replacement.md) | 2 | 2 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/rolling-restart.md](content/kv/3.4.1/how-to/operate/rolling-restart.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/routine-operations-checklist.md](content/kv/3.4.1/how-to/operate/routine-operations-checklist.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/schedule-object-reaping.md](content/kv/3.4.1/how-to/operate/schedule-object-reaping.md) | 2 | 3 | InitialDesignDecisions, OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/start-stop-restart-node.md](content/kv/3.4.1/how-to/operate/start-stop-restart-node.md) | 3 | 4 | InstallAndStartGuide | 0 |
| 3.4.1 | [how-to/operate/upgrade-cluster.md](content/kv/3.4.1/how-to/operate/upgrade-cluster.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/operate/use-remote-console.md](content/kv/3.4.1/how-to/operate/use-remote-console.md) | 2 | 2 | OperationsAndTroubleshootingGuide, OtherAPI | 0 |
| 3.4.1 | [how-to/plan/choose-deletion-policy.md](content/kv/3.4.1/how-to/plan/choose-deletion-policy.md) | 2 | 3 | InitialDesignDecisions, InstallAndStartGuide | 0 |
| 3.4.1 | [how-to/plan/choose-intra-cluster-resilience.md](content/kv/3.4.1/how-to/plan/choose-intra-cluster-resilience.md) | 3 | 4 | InitialDesignDecisions | 0 |
| 3.4.1 | [how-to/plan/choose-multi-cluster-topology.md](content/kv/3.4.1/how-to/plan/choose-multi-cluster-topology.md) | 1 | 2 | InitialDesignDecisions | 0 |
| 3.4.1 | [how-to/plan/choose-ring-size.md](content/kv/3.4.1/how-to/plan/choose-ring-size.md) | 1 | 2 | InitialDesignDecisions | 0 |
| 3.4.1 | [how-to/plan/choose-storage-backend.md](content/kv/3.4.1/how-to/plan/choose-storage-backend.md) | 1 | 2 | InitialDesignDecisions | 0 |
| 3.4.1 | [how-to/plan/index.md](content/kv/3.4.1/how-to/plan/_index.md) | 2 | 2 | BuildAndScaleClusterGuide, InitialDesignDecisions | 0 |
| 3.4.1 | [how-to/plan/map-data-to-objects.md](content/kv/3.4.1/how-to/plan/map-data-to-objects.md) | 2 | 3 | InitialDesignDecisions | 0 |
| 3.4.1 | [how-to/plan/production-readiness-checklist.md](content/kv/3.4.1/how-to/plan/production-readiness-checklist.md) | 1 | 1 | BuildAndScaleClusterGuide | 0 |
| 3.4.1 | [how-to/plan/size-cluster.md](content/kv/3.4.1/how-to/plan/size-cluster.md) | 2 | 2 | BuildAndScaleClusterGuide | 0 |
| 3.4.1 | [how-to/secure/configure-tls.md](content/kv/3.4.1/how-to/secure/configure-tls.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/secure/enable-security.md](content/kv/3.4.1/how-to/secure/enable-security.md) | 2 | 2 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/secure/index.md](content/kv/3.4.1/how-to/secure/_index.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/secure/manage-permissions.md](content/kv/3.4.1/how-to/secure/manage-permissions.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/secure/manage-sources.md](content/kv/3.4.1/how-to/secure/manage-sources.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/secure/secure-networking.md](content/kv/3.4.1/how-to/secure/secure-networking.md) | 1 | 1 | BuildAndScaleClusterGuide | 0 |
| 3.4.1 | [how-to/troubleshoot/erlang-vm.md](content/kv/3.4.1/how-to/troubleshoot/erlang-vm.md) | 5 | 5 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/troubleshoot/index.md](content/kv/3.4.1/how-to/troubleshoot/_index.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/troubleshoot/recover-failed-node.md](content/kv/3.4.1/how-to/troubleshoot/recover-failed-node.md) | 3 | 3 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/tune/benchmark-cluster.md](content/kv/3.4.1/how-to/tune/benchmark-cluster.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [how-to/tune/set-open-files-limit.md](content/kv/3.4.1/how-to/tune/set-open-files-limit.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.1 | [index.md](content/kv/3.4.1/_index.md) | 1 | 1 | index | 0 |
| 3.4.1 | [reference/aae-fold-api/erase-keys.md](content/kv/3.4.1/reference/aae-fold-api/erase-keys.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [reference/aae-fold-api/find-keys.md](content/kv/3.4.1/reference/aae-fold-api/find-keys.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [reference/aae-fold-api/find-tombstones.md](content/kv/3.4.1/reference/aae-fold-api/find-tombstones.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [reference/aae-fold-api/index.md](content/kv/3.4.1/reference/aae-fold-api/_index.md) | 13 | 13 | OtherAPI | 0 |
| 3.4.1 | [reference/aae-fold-api/list-buckets.md](content/kv/3.4.1/reference/aae-fold-api/list-buckets.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [reference/aae-fold-api/object-statistics.md](content/kv/3.4.1/reference/aae-fold-api/object-statistics.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [reference/aae-fold-api/reap-tombstones.md](content/kv/3.4.1/reference/aae-fold-api/reap-tombstones.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [reference/aae-fold-api/repair-key-range.md](content/kv/3.4.1/reference/aae-fold-api/repair-key-range.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [reference/commands/aae.md](content/kv/3.4.1/reference/commands/aae.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [reference/commands/vnode-status.md](content/kv/3.4.1/reference/commands/vnode-status.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [reference/configuration/bucket-properties.md](content/kv/3.4.1/reference/configuration/bucket-properties.md) | 14 | 14 | InitialDesignDecisions, InstallAndStartGuide | 0 |
| 3.4.1 | [reference/configuration/networking.md](content/kv/3.4.1/reference/configuration/networking.md) | 1 | 1 | BuildAndScaleClusterGuide | 0 |
| 3.4.1 | [reference/configuration/replication.md](content/kv/3.4.1/reference/configuration/replication.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.1 | [reference/data/content-types.md](content/kv/3.4.1/reference/data/content-types.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.1 | [reference/data/distributed-data-types.md](content/kv/3.4.1/reference/data/distributed-data-types.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [reference/data/index.md](content/kv/3.4.1/reference/data/_index.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.1 | [reference/data/keys-and-objects.md](content/kv/3.4.1/reference/data/keys-and-objects.md) | 2 | 2 | ObjectAPI | 0 |
| 3.4.1 | [reference/data/object-metadata.md](content/kv/3.4.1/reference/data/object-metadata.md) | 3 | 3 | ObjectAPI | 0 |
| 3.4.1 | [reference/data/secondary-indexes.md](content/kv/3.4.1/reference/data/secondary-indexes.md) | 2 | 2 | ObjectAPI, QueryAPI | 0 |
| 3.4.1 | [reference/data/version-vectors.md](content/kv/3.4.1/reference/data/version-vectors.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.1 | [reference/http-api/conditional-requests.md](content/kv/3.4.1/reference/http-api/conditional-requests.md) | 4 | 4 | ObjectAPI | 0 |
| 3.4.1 | [reference/http-api/delete-object.md](content/kv/3.4.1/reference/http-api/delete-object.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.1 | [reference/http-api/fetch-object.md](content/kv/3.4.1/reference/http-api/fetch-object.md) | 2 | 2 | ObjectAPI | 0 |
| 3.4.1 | [reference/http-api/index.md](content/kv/3.4.1/reference/http-api/_index.md) | 2 | 2 | ObjectAPI | 0 |
| 3.4.1 | [reference/http-api/mapreduce.md](content/kv/3.4.1/reference/http-api/mapreduce.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [reference/http-api/object-request-options.md](content/kv/3.4.1/reference/http-api/object-request-options.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.1 | [reference/http-api/store-object.md](content/kv/3.4.1/reference/http-api/store-object.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.1 | [reference/operations/cluster-claim-algorithms.md](content/kv/3.4.1/reference/operations/cluster-claim-algorithms.md) | 3 | 3 | BuildAndScaleClusterGuide | 0 |
| 3.4.1 | [reference/operations/custom-code.md](content/kv/3.4.1/reference/operations/custom-code.md) | 1 | 1 | ObjectAPI | 0 |
| 3.4.1 | [reference/operations/log-files.md](content/kv/3.4.1/reference/operations/log-files.md) | 1 | 2 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [reference/operations/object-deletion.md](content/kv/3.4.1/reference/operations/object-deletion.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.1 | [reference/operations/remote-console.md](content/kv/3.4.1/reference/operations/remote-console.md) | 3 | 3 | OperationsAndTroubleshootingGuide, OtherAPI | 0 |
| 3.4.1 | [reference/operations/replication-statistics.md](content/kv/3.4.1/reference/operations/replication-statistics.md) | 1 | 1 | ReplicationGuide | 0 |
| 3.4.1 | [reference/operations/statistics-and-monitoring.md](content/kv/3.4.1/reference/operations/statistics-and-monitoring.md) | 2 | 4 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [reference/query-api/accumulation-options.md](content/kv/3.4.1/reference/query-api/accumulation-options.md) | 2 | 2 | QueryAPI | 0 |
| 3.4.1 | [reference/query-api/expressions.md](content/kv/3.4.1/reference/query-api/expressions.md) | 5 | 5 | QueryAPI | 0 |
| 3.4.1 | [reference/query-api/index.md](content/kv/3.4.1/reference/query-api/_index.md) | 2 | 2 | QueryAPI | 0 |
| 3.4.1 | [reference/query-api/limits.md](content/kv/3.4.1/reference/query-api/limits.md) | 8 | 9 | QueryAPI | 0 |
| 3.4.1 | [reference/query-api/request.md](content/kv/3.4.1/reference/query-api/request.md) | 8 | 9 | QueryAPI | 0 |
| 3.4.1 | [reference/query-api/responses.md](content/kv/3.4.1/reference/query-api/responses.md) | 1 | 1 | QueryAPI | 0 |
| 3.4.1 | [reference/releases/downloads.md](content/kv/3.4.1/reference/releases/downloads.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.1 | [reference/releases/supported-platforms.md](content/kv/3.4.1/reference/releases/supported-platforms.md) | 2 | 2 | InstallAndStartGuide | 0 |
| 3.4.1 | [reference/replication-api/index.md](content/kv/3.4.1/reference/replication-api/_index.md) | 3 | 3 | OtherAPI, ReplicationGuide | 0 |
| 3.4.1 | [reference/replication-api/runtime-controls.md](content/kv/3.4.1/reference/replication-api/runtime-controls.md) | 11 | 12 | ReplicationGuide | 0 |
| 3.4.1 | [reference/specialized-apis/cluster-metadata.md](content/kv/3.4.1/reference/specialized-apis/cluster-metadata.md) | 1 | 1 | OperationsAndTroubleshootingGuide | 0 |
| 3.4.1 | [reference/specialized-apis/data-type-api.md](content/kv/3.4.1/reference/specialized-apis/data-type-api.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [reference/specialized-apis/fetch-api.md](content/kv/3.4.1/reference/specialized-apis/fetch-api.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [reference/specialized-apis/index.md](content/kv/3.4.1/reference/specialized-apis/_index.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [reference/specialized-apis/legacy-query-api.md](content/kv/3.4.1/reference/specialized-apis/legacy-query-api.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [reference/specialized-apis/list-api.md](content/kv/3.4.1/reference/specialized-apis/list-api.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [reference/specialized-apis/strong-consistency-api.md](content/kv/3.4.1/reference/specialized-apis/strong-consistency-api.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [reference/specialized-apis/write-once-api.md](content/kv/3.4.1/reference/specialized-apis/write-once-api.md) | 1 | 1 | OtherAPI | 0 |
| 3.4.1 | [tutorials/first-cluster/index.md](content/kv/3.4.1/tutorials/first-cluster/_index.md) | 1 | 1 | InstallAndStartGuide | 0 |
| 3.4.1 | [tutorials/query-api/build-search-index.md](content/kv/3.4.1/tutorials/query-api/build-search-index.md) | 12 | 12 | QueryAPI | 0 |
| 3.4.1 | [tutorials/query-api/index.md](content/kv/3.4.1/tutorials/query-api/_index.md) | 1 | 1 | QueryAPI | 0 |

## Source-section inventory

| Source | Seq. | Heading | Body bytes | 3.4.0 routes | 3.4.1 routes |
|---|---:|---|---:|---|---|
| index | 1 | OpenRiak QuickDocs 3.4 | 85 | index.md<br>explanation/foundations/index.md | index.md<br>explanation/foundations/index.md |
| index | 2 | What is Riak? | 2154 | explanation/foundations/why-openriak.md<br>explanation/foundations/use-cases.md | explanation/foundations/why-openriak.md<br>explanation/foundations/use-cases.md |
| index | 3 | Riak History | 822 | explanation/foundations/history.md | explanation/foundations/history.md |
| BuildAndScaleClusterGuide | 1 | Riak KV - Building and Scaling a Cluster | 232 | how-to/plan/index.md<br>how-to/operate/index.md | how-to/plan/index.md<br>how-to/operate/index.md |
| BuildAndScaleClusterGuide | 2 | Choosing infrastructure | 728 | how-to/plan/size-cluster.md<br>how-to/plan/production-readiness-checklist.md | how-to/plan/size-cluster.md<br>how-to/plan/production-readiness-checklist.md |
| BuildAndScaleClusterGuide | 3 | Nodes | 6605 | how-to/plan/size-cluster.md | how-to/plan/size-cluster.md |
| BuildAndScaleClusterGuide | 4 | Network | 4693 | reference/configuration/networking.md<br>how-to/secure/secure-networking.md | reference/configuration/networking.md<br>how-to/secure/secure-networking.md |
| BuildAndScaleClusterGuide | 5 | Load-balancing | 5359 | how-to/configure/load-balancing-proxy.md | how-to/configure/load-balancing-proxy.md |
| BuildAndScaleClusterGuide | 6 | Forming and Expanding a Riak cluster | 2467 | how-to/operate/add-node.md<br>how-to/operate/plan-and-commit-cluster-change.md | how-to/operate/add-node.md<br>how-to/operate/plan-and-commit-cluster-change.md |
| BuildAndScaleClusterGuide | 7 | Join process - staging a change | 814 | how-to/operate/add-node.md | how-to/operate/add-node.md |
| BuildAndScaleClusterGuide | 8 | Join process - plan a change | 1827 | how-to/operate/plan-and-commit-cluster-change.md | how-to/operate/plan-and-commit-cluster-change.md |
| BuildAndScaleClusterGuide | 9 | Join process - choose_claim_v2 (default) | 155 | reference/operations/cluster-claim-algorithms.md | reference/operations/cluster-claim-algorithms.md |
| BuildAndScaleClusterGuide | 10 | Join process - choose_claim_v3 | 472 | reference/operations/cluster-claim-algorithms.md | reference/operations/cluster-claim-algorithms.md |
| BuildAndScaleClusterGuide | 11 | Join process - choose_claim_v4 (recommended) | 767 | reference/operations/cluster-claim-algorithms.md | reference/operations/cluster-claim-algorithms.md |
| BuildAndScaleClusterGuide | 12 | Join process - verify the plan | 737 | how-to/operate/plan-and-commit-cluster-change.md | how-to/operate/plan-and-commit-cluster-change.md |
| BuildAndScaleClusterGuide | 13 | Join process - commit the plan | 439 | how-to/operate/plan-and-commit-cluster-change.md | how-to/operate/plan-and-commit-cluster-change.md |
| BuildAndScaleClusterGuide | 14 | Join process - await handoffs | 1930 | how-to/operate/manage-handoffs.md | how-to/operate/manage-handoffs.md |
| BuildAndScaleClusterGuide | 15 | Shrinking a cluster | 813 | how-to/operate/remove-node.md | how-to/operate/remove-node.md |
| InitialDesignDecisions | 1 | Riak KV - Initial Design Decisions | 896 | how-to/plan/index.md | how-to/plan/index.md |
| InitialDesignDecisions | 2 | Database backend | 0 | how-to/plan/choose-storage-backend.md<br>explanation/storage/choosing-backend.md | how-to/plan/choose-storage-backend.md<br>explanation/storage/choosing-backend.md |
| InitialDesignDecisions | 3 | Database backend - making a choice | 2035 | how-to/plan/choose-storage-backend.md | how-to/plan/choose-storage-backend.md |
| InitialDesignDecisions | 4 | Leveled | 1856 | explanation/storage/leveled.md<br>how-to/configure/backends/leveled.md | explanation/storage/leveled.md<br>how-to/configure/backends/leveled.md |
| InitialDesignDecisions | 5 | Bitcask | 1887 | explanation/storage/bitcask.md<br>how-to/configure/backends/bitcask.md | explanation/storage/bitcask.md<br>how-to/configure/backends/bitcask.md |
| InitialDesignDecisions | 6 | Eleveldb (deprecated) | 1096 | explanation/storage/leveldb.md<br>how-to/configure/backends/leveldb.md | explanation/storage/leveldb.md<br>how-to/configure/backends/leveldb.md |
| InitialDesignDecisions | 7 | In-memory (deprecated) | 627 | explanation/storage/memory.md<br>how-to/configure/backends/memory.md | explanation/storage/memory.md<br>how-to/configure/backends/memory.md |
| InitialDesignDecisions | 8 | Multi-backend | 503 | explanation/storage/multi-backend.md<br>how-to/configure/backends/multi.md | explanation/storage/multi-backend.md<br>how-to/configure/backends/multi.md |
| InitialDesignDecisions | 9 | Database backend - changing the choice | 890 | how-to/configure/backends/change-backend.md | how-to/configure/backends/change-backend.md |
| InitialDesignDecisions | 10 | Ring size | 0 | how-to/plan/choose-ring-size.md<br>explanation/foundations/clusters-rings-and-partitions.md | how-to/plan/choose-ring-size.md<br>explanation/foundations/clusters-rings-and-partitions.md |
| InitialDesignDecisions | 11 | Ring size - making a choice | 2403 | how-to/plan/choose-ring-size.md | how-to/plan/choose-ring-size.md |
| InitialDesignDecisions | 12 | Ring size - changing the choice | 557 | how-to/configure/replication/migrate-cluster.md | how-to/configure/replication/migrate-cluster.md |
| InitialDesignDecisions | 13 | Intra-cluster data resilience | 0 | how-to/plan/choose-intra-cluster-resilience.md<br>explanation/foundations/intra-cluster-resilience.md | how-to/plan/choose-intra-cluster-resilience.md<br>explanation/foundations/intra-cluster-resilience.md |
| InitialDesignDecisions | 14 | Intra-cluster data resilience - making a choice | 414 | how-to/plan/choose-intra-cluster-resilience.md | how-to/plan/choose-intra-cluster-resilience.md |
| InitialDesignDecisions | 15 | Data distribution guarantees | 3505 | how-to/plan/choose-intra-cluster-resilience.md<br>reference/configuration/bucket-properties.md | how-to/plan/choose-intra-cluster-resilience.md<br>reference/configuration/bucket-properties.md |
| InitialDesignDecisions | 16 | Proactive reconciliation | 2110 | explanation/replication/active-anti-entropy.md<br>how-to/configure/replication/enable-tictac-aae.md | explanation/replication/active-anti-entropy.md<br>how-to/configure/replication/enable-tictac-aae.md |
| InitialDesignDecisions | 17 | Intra-cluster data resilience - changing the choice | 1104 | how-to/configure/replication/enable-tictac-aae.md<br>how-to/plan/choose-intra-cluster-resilience.md | how-to/configure/replication/enable-tictac-aae.md<br>how-to/plan/choose-intra-cluster-resilience.md |
| InitialDesignDecisions | 18 | Interconnecting multiple clusters | 0 | how-to/plan/choose-multi-cluster-topology.md<br>explanation/replication/multi-datacenter-architecture.md | how-to/plan/choose-multi-cluster-topology.md<br>explanation/replication/multi-datacenter-architecture.md |
| InitialDesignDecisions | 19 | Interconnecting multiple clusters - making a choice | 4026 | how-to/plan/choose-multi-cluster-topology.md | how-to/plan/choose-multi-cluster-topology.md |
| InitialDesignDecisions | 20 | Interconnecting multiple clusters - changing the choice | 452 | how-to/configure/replication/migrate-cluster.md | how-to/configure/replication/migrate-cluster.md |
| InitialDesignDecisions | 21 | Deleting data | 0 | how-to/plan/choose-deletion-policy.md<br>explanation/data-model/deletion-policies.md | how-to/plan/choose-deletion-policy.md<br>explanation/data-model/deletion-policies.md |
| InitialDesignDecisions | 22 | Deleting data - making a choice | 4285 | how-to/plan/choose-deletion-policy.md | how-to/plan/choose-deletion-policy.md |
| InitialDesignDecisions | 23 | Deleting data - changing the choice | 387 | how-to/operate/schedule-object-reaping.md<br>how-to/configure/global-object-expiration.md | how-to/operate/schedule-object-reaping.md<br>how-to/configure/global-object-expiration.md |
| InitialDesignDecisions | 24 | Mapping data to objects | 0 | how-to/plan/map-data-to-objects.md<br>explanation/data-model/keys-objects-and-buckets.md | how-to/plan/map-data-to-objects.md<br>explanation/data-model/keys-objects-and-buckets.md |
| InitialDesignDecisions | 25 | Mapping data to objects - making a choice | 3396 | how-to/plan/map-data-to-objects.md | how-to/plan/map-data-to-objects.md |
| InitialDesignDecisions | 26 | Mapping data to objects - changing the choice | 881 | how-to/plan/map-data-to-objects.md<br>explanation/data-model/keys-objects-and-buckets.md | how-to/plan/map-data-to-objects.md<br>explanation/data-model/keys-objects-and-buckets.md |
| InstallAndStartGuide | 1 | Riak KV - Install and Start | 0 | how-to/install/index.md | how-to/install/index.md |
| InstallAndStartGuide | 2 | Installation | 1048 | how-to/install/index.md | how-to/install/index.md |
| InstallAndStartGuide | 3 | Install Erlang/OTP | 1608 | how-to/install/source.md<br>reference/releases/supported-platforms.md | how-to/install/source.md<br>reference/releases/supported-platforms.md |
| InstallAndStartGuide | 4 | Download Riak | 877 | reference/releases/downloads.md | reference/releases/downloads.md |
| InstallAndStartGuide | 5 | Make Riak | 221 | how-to/install/source.md | how-to/install/source.md |
| InstallAndStartGuide | 6 | Local release | 213 | how-to/install/source.md<br>how-to/install/verify-installation.md | how-to/install/source.md<br>how-to/install/verify-installation.md |
| InstallAndStartGuide | 7 | Local cluster | 229 | tutorials/first-cluster/index.md<br>how-to/install/source.md | tutorials/first-cluster/index.md<br>how-to/install/source.md |
| InstallAndStartGuide | 8 | Generating a package | 603 | how-to/install/source.md | how-to/install/source.md |
| InstallAndStartGuide | 9 | Using pre-built packages | 550 | how-to/install/index.md<br>reference/releases/supported-platforms.md | how-to/install/index.md<br>reference/releases/supported-platforms.md |
| InstallAndStartGuide | 10 | Starting Riak | 0 | how-to/operate/start-stop-restart-node.md<br>how-to/install/verify-installation.md | how-to/operate/start-stop-restart-node.md<br>how-to/install/verify-installation.md |
| InstallAndStartGuide | 11 | Starting Riak by Make Method | 441 | how-to/install/source.md<br>how-to/operate/start-stop-restart-node.md | how-to/install/source.md<br>how-to/operate/start-stop-restart-node.md |
| InstallAndStartGuide | 12 | Local Release or Cluster | 1388 | how-to/operate/start-stop-restart-node.md | how-to/operate/start-stop-restart-node.md |
| InstallAndStartGuide | 13 | Package Deployment | 590 | how-to/operate/start-stop-restart-node.md | how-to/operate/start-stop-restart-node.md |
| InstallAndStartGuide | 14 | Setting ulimit | 505 | how-to/tune/set-open-files-limit.md | how-to/tune/set-open-files-limit.md |
| InstallAndStartGuide | 15 | Configuration of Riak - key riak.conf changes | 3338 | how-to/configure/basic-node-settings.md<br>how-to/configure/api-listeners.md<br>how-to/configure/verify-configuration.md | how-to/configure/basic-node-settings.md<br>how-to/configure/api-listeners.md<br>how-to/configure/verify-configuration.md |
| InstallAndStartGuide | 16 | Configuration of Riak - leveled backend | 1717 | how-to/configure/backends/leveled.md | how-to/configure/backends/leveled.md |
| InstallAndStartGuide | 17 | Configuration of Riak - bitcask backend | 579 | how-to/configure/backends/bitcask.md | how-to/configure/backends/bitcask.md |
| InstallAndStartGuide | 18 | Configuration of Riak - Delete Mode | 734 | how-to/plan/choose-deletion-policy.md<br>reference/operations/object-deletion.md | how-to/plan/choose-deletion-policy.md<br>reference/operations/object-deletion.md |
| InstallAndStartGuide | 19 | Configuration of Riak - Bucket Properties | 3364 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| InstallAndStartGuide | 20 | Property - dvv_enabled | 644 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| InstallAndStartGuide | 21 | Property - allow_mult | 1850 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| InstallAndStartGuide | 22 | Property - last_write_wins | 1193 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| InstallAndStartGuide | 23 | Property - n_val | 1200 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| InstallAndStartGuide | 24 | Property - node_confirms | 1134 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| InstallAndStartGuide | 25 | Property - sync_on_write | 2182 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| InstallAndStartGuide | 26 | Property - aae_tree_exclude | 2149 | how-to/configure/replication/exclude-bucket-from-aae.md<br>reference/configuration/bucket-properties.md | how-to/configure/replication/exclude-bucket-from-aae.md<br>reference/configuration/bucket-properties.md |
| InstallAndStartGuide | 27 | Property - small_vclock | 969 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| InstallAndStartGuide | 28 | Property - notfound_ok | 495 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| InstallAndStartGuide | 29 | Property - pr and pw | 1861 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| InstallAndStartGuide | 30 | Property - backend | 112 | reference/configuration/bucket-properties.md<br>how-to/configure/backends/index.md | reference/configuration/bucket-properties.md<br>how-to/configure/backends/index.md |
| InstallAndStartGuide | 31 | Property - General read/write parameters | 973 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| ObjectAPI | 1 | Riak KV - Object API | 2447 | reference/http-api/index.md<br>reference/data/index.md<br>how-to/develop/index.md | reference/http-api/index.md<br>reference/data/index.md<br>how-to/develop/index.md |
| ObjectAPI | 2 | Object Identifier - the URL | 1324 | reference/data/keys-and-objects.md<br>reference/http-api/index.md | reference/data/keys-and-objects.md<br>reference/http-api/index.md |
| ObjectAPI | 3 | Object Value - the request body | 2005 | reference/data/keys-and-objects.md<br>reference/data/content-types.md | reference/data/keys-and-objects.md<br>reference/data/content-types.md |
| ObjectAPI | 4 | Object Meta Content - the request and response headers | 135 | reference/data/object-metadata.md | reference/data/object-metadata.md |
| ObjectAPI | 5 | Version Vector | 859 | reference/data/version-vectors.md<br>explanation/data-model/version-vectors-and-siblings.md | reference/data/version-vectors.md<br>explanation/data-model/version-vectors-and-siblings.md |
| ObjectAPI | 6 | User Metadata | 358 | reference/data/object-metadata.md | reference/data/object-metadata.md |
| ObjectAPI | 7 | Object Metadata | 558 | reference/data/object-metadata.md | reference/data/object-metadata.md |
| ObjectAPI | 8 | Index Entries | 1006 | reference/data/secondary-indexes.md | reference/data/secondary-indexes.md |
| ObjectAPI | 9 | GET and PUT Options | 2805 | reference/http-api/object-request-options.md | reference/http-api/object-request-options.md |
| ObjectAPI | 10 | Conditional Requests | 5760 | reference/http-api/conditional-requests.md<br>how-to/develop/send-conditional-object-request.md<br>explanation/consistency/conditional-requests.md | reference/http-api/conditional-requests.md<br>how-to/develop/send-conditional-object-request.md<br>explanation/consistency/conditional-requests.md |
| ObjectAPI | 11 | Use of Request Header - If-None-Match | 319 | reference/http-api/conditional-requests.md<br>how-to/develop/send-conditional-object-request.md<br>explanation/consistency/conditional-requests.md | reference/http-api/conditional-requests.md<br>how-to/develop/send-conditional-object-request.md<br>explanation/consistency/conditional-requests.md |
| ObjectAPI | 12 | Use of Request Header - X-Riak-If-Not-Modified (non-standard Riak header) | 1055 | reference/http-api/conditional-requests.md<br>how-to/develop/send-conditional-object-request.md<br>explanation/consistency/conditional-requests.md | reference/http-api/conditional-requests.md<br>how-to/develop/send-conditional-object-request.md<br>explanation/consistency/conditional-requests.md |
| ObjectAPI | 13 | Conditional requests and latch objects | 527 | explanation/data-model/latch-objects.md<br>reference/http-api/conditional-requests.md | explanation/data-model/latch-objects.md<br>reference/http-api/conditional-requests.md |
| ObjectAPI | 14 | Commit Hooks | 469 | how-to/develop/write-commit-hook.md<br>reference/operations/custom-code.md | how-to/develop/write-commit-hook.md<br>reference/operations/custom-code.md |
| ObjectAPI | 15 | HTTP API Definition - Store | 1545 | reference/http-api/store-object.md<br>how-to/develop/create-object.md<br>how-to/develop/update-object.md | reference/http-api/store-object.md<br>how-to/develop/create-object.md<br>how-to/develop/update-object.md |
| ObjectAPI | 16 | Example PUT request | 333 | how-to/develop/create-object.md<br>how-to/develop/update-object.md | how-to/develop/create-object.md<br>how-to/develop/update-object.md |
| ObjectAPI | 17 | HTTP API Definition - Fetch | 1367 | reference/http-api/fetch-object.md<br>how-to/develop/read-object.md | reference/http-api/fetch-object.md<br>how-to/develop/read-object.md |
| ObjectAPI | 18 | Example GET request | 116 | how-to/develop/read-object.md | how-to/develop/read-object.md |
| ObjectAPI | 19 | HTTP API Definition - Delete | 881 | reference/http-api/delete-object.md<br>how-to/develop/delete-object.md | reference/http-api/delete-object.md<br>how-to/develop/delete-object.md |
| ObjectAPI | 20 | Example DELETE request | 162 | how-to/develop/delete-object.md | how-to/develop/delete-object.md |
| ObjectAPI | 21 | Accessing Legacy Objects | 308 | reference/http-api/fetch-object.md<br>explanation/data-model/merge-strategies.md | reference/http-api/fetch-object.md<br>explanation/data-model/merge-strategies.md |
| ObjectAPI | 22 | Performance and Efficiency | 0 | explanation/performance/latency-throughput-and-capacity.md<br>explanation/performance/storage-and-filesystem-effects.md | explanation/performance/latency-throughput-and-capacity.md<br>explanation/performance/storage-and-filesystem-effects.md |
| ObjectAPI | 23 | Notes on Implementation | 2374 | explanation/performance/latency-throughput-and-capacity.md<br>explanation/performance/storage-and-filesystem-effects.md | explanation/performance/latency-throughput-and-capacity.md<br>explanation/performance/storage-and-filesystem-effects.md |
| ObjectAPI | 24 | Performance Expectations | 2144 | explanation/performance/latency-throughput-and-capacity.md<br>explanation/performance/storage-and-filesystem-effects.md | explanation/performance/latency-throughput-and-capacity.md<br>explanation/performance/storage-and-filesystem-effects.md |
| OperationsAndTroubleshootingGuide | 1 | Riak KV - Operations and Troubleshooting | 963 | how-to/operate/index.md<br>how-to/troubleshoot/index.md | how-to/operate/index.md<br>how-to/troubleshoot/index.md |
| OperationsAndTroubleshootingGuide | 2 | Replace, Repair and Recover | 996 | explanation/operations/node-failure-and-recovery.md<br>how-to/troubleshoot/recover-failed-node.md | explanation/operations/node-failure-and-recovery.md<br>how-to/troubleshoot/recover-failed-node.md |
| OperationsAndTroubleshootingGuide | 3 | Proactive Replacement | 2335 | how-to/operate/rolling-replacement.md | how-to/operate/rolling-replacement.md |
| OperationsAndTroubleshootingGuide | 4 | Reactive Replacement | 702 | how-to/operate/replace-node.md<br>how-to/troubleshoot/recover-failed-node.md | how-to/operate/replace-node.md<br>how-to/troubleshoot/recover-failed-node.md |
| OperationsAndTroubleshootingGuide | 5 | Administratively Downing a Node | 866 | how-to/operate/replace-node.md | how-to/operate/replace-node.md |
| OperationsAndTroubleshootingGuide | 6 | Forcing a Replace | 987 | how-to/operate/replace-node.md | how-to/operate/replace-node.md |
| OperationsAndTroubleshootingGuide | 7 | Completing a Repair | 1958 | how-to/troubleshoot/recover-failed-node.md<br>how-to/operate/repair-vnode.md | how-to/troubleshoot/recover-failed-node.md<br>how-to/operate/repair-vnode.md |
| OperationsAndTroubleshootingGuide | 8 | Rolling Replacement | 930 | how-to/operate/rolling-replacement.md | how-to/operate/rolling-replacement.md |
| OperationsAndTroubleshootingGuide | 9 | Rolling restart | 723 | how-to/operate/rolling-restart.md | how-to/operate/rolling-restart.md |
| OperationsAndTroubleshootingGuide | 10 | Repair an individual leveled store | 1632 | how-to/operate/repair-leveled-store.md | how-to/operate/repair-leveled-store.md |
| OperationsAndTroubleshootingGuide | 11 | Repair an individual vnode | 1892 | how-to/operate/repair-vnode.md | how-to/operate/repair-vnode.md |
| OperationsAndTroubleshootingGuide | 12 | Repair key ranges | 1584 | how-to/operate/aae-fold/repair-key-range.md | how-to/operate/aae-fold/repair-key-range.md |
| OperationsAndTroubleshootingGuide | 13 | Upgrading a node | 2843 | how-to/operate/upgrade-cluster.md<br>explanation/operations/upgrade-and-downgrade.md | how-to/operate/upgrade-cluster.md<br>explanation/operations/upgrade-and-downgrade.md |
| OperationsAndTroubleshootingGuide | 14 | Remote Console | 1406 | how-to/operate/use-remote-console.md<br>reference/operations/remote-console.md | how-to/operate/use-remote-console.md<br>reference/operations/remote-console.md |
| OperationsAndTroubleshootingGuide | 15 | Accessing objects | 888 | how-to/operate/inspect-data.md | how-to/operate/inspect-data.md |
| OperationsAndTroubleshootingGuide | 16 | Running AAE Folds | 135 | how-to/operate/aae-fold/run-from-command-line.md | how-to/operate/aae-fold/run-from-command-line.md |
| OperationsAndTroubleshootingGuide | 17 | riak_client remote_console commands | 1063 | reference/operations/remote-console.md | reference/operations/remote-console.md |
| OperationsAndTroubleshootingGuide | 18 | Extending configuration | 0 | how-to/configure/advanced-configuration.md<br>how-to/configure/manage-configuration.md | how-to/configure/advanced-configuration.md<br>how-to/configure/manage-configuration.md |
| OperationsAndTroubleshootingGuide | 19 | Using advanced.config | 984 | how-to/configure/advanced-configuration.md | how-to/configure/advanced-configuration.md |
| OperationsAndTroubleshootingGuide | 20 | Setting environment variables at runtime | 1145 | how-to/configure/runtime-environment-variables.md | how-to/configure/runtime-environment-variables.md |
| OperationsAndTroubleshootingGuide | 21 | Accessing configuration | 530 | how-to/configure/manage-configuration.md | how-to/configure/manage-configuration.md |
| OperationsAndTroubleshootingGuide | 22 | Logging and Statistics | 0 | reference/operations/statistics-and-monitoring.md<br>reference/operations/log-files.md | reference/operations/statistics-and-monitoring.md<br>reference/operations/log-files.md |
| OperationsAndTroubleshootingGuide | 23 | Logging | 2497 | how-to/configure/logging.md<br>reference/operations/log-files.md | how-to/configure/logging.md<br>reference/operations/log-files.md |
| OperationsAndTroubleshootingGuide | 24 | Riak Stats | 1057 | reference/operations/statistics-and-monitoring.md | reference/operations/statistics-and-monitoring.md |
| OperationsAndTroubleshootingGuide | 25 | Vnode Status | 399 | how-to/operate/check-vnode-status.md<br>reference/commands/vnode-status.md | how-to/operate/check-vnode-status.md<br>reference/commands/vnode-status.md |
| OperationsAndTroubleshootingGuide | 26 | Monitoring Operational Services | 0 | reference/operations/statistics-and-monitoring.md | reference/operations/statistics-and-monitoring.md |
| OperationsAndTroubleshootingGuide | 27 | Monitoring Anti-Entropy | 262 | how-to/operate/monitor-active-anti-entropy.md | how-to/operate/monitor-active-anti-entropy.md |
| OperationsAndTroubleshootingGuide | 28 | Monitoring and Controlling AAE - Command Line | 5113 | how-to/operate/monitor-active-anti-entropy.md<br>how-to/operate/rebuild-aae-trees.md | how-to/operate/monitor-active-anti-entropy.md<br>how-to/operate/rebuild-aae-trees.md |
| OperationsAndTroubleshootingGuide | 29 | Monitoring AAE - Logs and Statistics | 2101 | how-to/operate/monitor-active-anti-entropy.md<br>reference/operations/statistics-and-monitoring.md | how-to/operate/monitor-active-anti-entropy.md<br>reference/operations/statistics-and-monitoring.md |
| OperationsAndTroubleshootingGuide | 30 | Monitoring legacy AAE | 226 | explanation/replication/legacy-aae.md<br>how-to/operate/monitor-active-anti-entropy.md | explanation/replication/legacy-aae.md<br>how-to/operate/monitor-active-anti-entropy.md |
| OperationsAndTroubleshootingGuide | 31 | Logging and monitoring of read repairs | 2157 | how-to/operate/monitor-read-repairs.md | how-to/operate/monitor-read-repairs.md |
| OperationsAndTroubleshootingGuide | 32 | Monitoring inter-cluster reconciliation | 158 | how-to/operate/monitor-reconciliation.md | how-to/operate/monitor-reconciliation.md |
| OperationsAndTroubleshootingGuide | 33 | Monitoring node worker pools | 293 | how-to/operate/monitor-worker-pools.md | how-to/operate/monitor-worker-pools.md |
| OperationsAndTroubleshootingGuide | 34 | Enabling Riak Security | 1065 | how-to/secure/index.md<br>how-to/secure/enable-security.md | how-to/secure/index.md<br>how-to/secure/enable-security.md |
| OperationsAndTroubleshootingGuide | 35 | TLS Enablement | 1474 | how-to/secure/configure-tls.md | how-to/secure/configure-tls.md |
| OperationsAndTroubleshootingGuide | 36 | Enabling Security and Restricting Source | 4746 | how-to/secure/enable-security.md<br>how-to/secure/manage-sources.md | how-to/secure/enable-security.md<br>how-to/secure/manage-sources.md |
| OperationsAndTroubleshootingGuide | 37 | Granting permissions for specific actions | 1262 | how-to/secure/manage-permissions.md | how-to/secure/manage-permissions.md |
| OperationsAndTroubleshootingGuide | 38 | Garbage Collection - Reap, Erase and Scheduled Compaction | 0 | explanation/operations/garbage-collection.md<br>how-to/operate/schedule-object-reaping.md | explanation/operations/garbage-collection.md<br>how-to/operate/schedule-object-reaping.md |
| OperationsAndTroubleshootingGuide | 39 | Riak KV Eraser and Riak KV Reaper | 2533 | how-to/operate/schedule-object-reaping.md | how-to/operate/schedule-object-reaping.md |
| OperationsAndTroubleshootingGuide | 40 | bitcask merge window | 1497 | how-to/configure/backends/bitcask-merge-window.md | how-to/configure/backends/bitcask-merge-window.md |
| OperationsAndTroubleshootingGuide | 41 | leveled compaction high/low hour | 2955 | how-to/configure/backends/leveled-compaction-window.md | how-to/configure/backends/leveled-compaction-window.md |
| OperationsAndTroubleshootingGuide | 42 | Garbage collecting .bak files in leveled | 1085 | how-to/operate/remove-leveled-backup-files.md | how-to/operate/remove-leveled-backup-files.md |
| OperationsAndTroubleshootingGuide | 43 | Data inspection | 284 | how-to/operate/inspect-data.md | how-to/operate/inspect-data.md |
| OperationsAndTroubleshootingGuide | 44 | Volume and performance testing | 2223 | how-to/tune/benchmark-cluster.md | how-to/tune/benchmark-cluster.md |
| OperationsAndTroubleshootingGuide | 45 | Backup options | 2027 | explanation/operations/backups-and-restores.md<br>how-to/operate/back-up-node.md | explanation/operations/backups-and-restores.md<br>how-to/operate/back-up-node.md |
| OperationsAndTroubleshootingGuide | 46 | Backup - the preferred building block | 1404 | how-to/operate/back-up-node.md | how-to/operate/back-up-node.md |
| OperationsAndTroubleshootingGuide | 47 | Leveled - hot backups | 3488 | how-to/operate/back-up-node.md | how-to/operate/back-up-node.md |
| OperationsAndTroubleshootingGuide | 48 | Leveled - restore a backup | 467 | how-to/operate/restore-node.md | how-to/operate/restore-node.md |
| OperationsAndTroubleshootingGuide | 49 | Bitcask - backups | 308 | how-to/operate/back-up-node.md | how-to/operate/back-up-node.md |
| OperationsAndTroubleshootingGuide | 50 | Backup - ring folder, and cluster metadata | 440 | how-to/operate/back-up-node.md<br>reference/specialized-apis/cluster-metadata.md | how-to/operate/back-up-node.md<br>reference/specialized-apis/cluster-metadata.md |
| OperationsAndTroubleshootingGuide | 51 | Operation Checklist | 4045 | how-to/operate/routine-operations-checklist.md | how-to/operate/routine-operations-checklist.md |
| OperationsAndTroubleshootingGuide | 52 | Advanced - troubleshoot via the Erlang VM | 130 | how-to/troubleshoot/erlang-vm.md | how-to/troubleshoot/erlang-vm.md |
| OperationsAndTroubleshootingGuide | 53 | Recon | 1469 | how-to/troubleshoot/erlang-vm.md | how-to/troubleshoot/erlang-vm.md |
| OperationsAndTroubleshootingGuide | 54 | Microstate accounting | 739 | how-to/troubleshoot/erlang-vm.md | how-to/troubleshoot/erlang-vm.md |
| OperationsAndTroubleshootingGuide | 55 | Eprof | 1071 | how-to/troubleshoot/erlang-vm.md | how-to/troubleshoot/erlang-vm.md |
| OperationsAndTroubleshootingGuide | 56 | Tracing with dbg | 484 | how-to/troubleshoot/erlang-vm.md | how-to/troubleshoot/erlang-vm.md |
| OtherAPI | 1 | Riak KV - Other APIs | 510 | reference/specialized-apis/index.md<br>reference/aae-fold-api/index.md | reference/specialized-apis/index.md<br>reference/aae-fold-api/index.md |
| OtherAPI | 2 | AAE Fold API | 1226 | reference/aae-fold-api/index.md<br>how-to/operate/aae-fold/index.md | reference/aae-fold-api/index.md<br>how-to/operate/aae-fold/index.md |
| OtherAPI | 3 | Supported fold types | 45 | reference/aae-fold-api/index.md | reference/aae-fold-api/index.md |
| OtherAPI | 4 | merge_root_nval | 227 | reference/aae-fold-api/index.md | reference/aae-fold-api/index.md |
| OtherAPI | 5 | merge_branch_nval | 321 | reference/aae-fold-api/index.md | reference/aae-fold-api/index.md |
| OtherAPI | 6 | fetch_clocks_nval | 636 | reference/aae-fold-api/index.md | reference/aae-fold-api/index.md |
| OtherAPI | 7 | merge_tree_range | 320 | reference/aae-fold-api/index.md | reference/aae-fold-api/index.md |
| OtherAPI | 8 | fetch_clocks_range | 222 | reference/aae-fold-api/index.md | reference/aae-fold-api/index.md |
| OtherAPI | 9 | repl_keys_range | 668 | reference/aae-fold-api/index.md<br>reference/replication-api/index.md | reference/aae-fold-api/index.md<br>reference/replication-api/index.md |
| OtherAPI | 10 | repair_keys_range | 566 | reference/aae-fold-api/repair-key-range.md<br>how-to/operate/aae-fold/repair-key-range.md | reference/aae-fold-api/repair-key-range.md<br>how-to/operate/aae-fold/repair-key-range.md |
| OtherAPI | 11 | find_keys | 595 | reference/aae-fold-api/find-keys.md<br>how-to/operate/aae-fold/find-keys.md | reference/aae-fold-api/find-keys.md<br>how-to/operate/aae-fold/find-keys.md |
| OtherAPI | 12 | find_tombs | 228 | reference/aae-fold-api/find-tombstones.md<br>how-to/operate/aae-fold/find-tombstones.md | reference/aae-fold-api/find-tombstones.md<br>how-to/operate/aae-fold/find-tombstones.md |
| OtherAPI | 13 | erase_keys | 583 | reference/aae-fold-api/erase-keys.md<br>how-to/operate/aae-fold/erase-keys.md | reference/aae-fold-api/erase-keys.md<br>how-to/operate/aae-fold/erase-keys.md |
| OtherAPI | 14 | reap_tombs | 589 | reference/aae-fold-api/reap-tombstones.md<br>how-to/operate/aae-fold/reap-tombstones.md | reference/aae-fold-api/reap-tombstones.md<br>how-to/operate/aae-fold/reap-tombstones.md |
| OtherAPI | 15 | object_stats | 521 | reference/aae-fold-api/object-statistics.md<br>how-to/operate/aae-fold/object-statistics.md | reference/aae-fold-api/object-statistics.md<br>how-to/operate/aae-fold/object-statistics.md |
| OtherAPI | 16 | list_buckets | 428 | reference/aae-fold-api/list-buckets.md<br>how-to/operate/aae-fold/list-buckets.md | reference/aae-fold-api/list-buckets.md<br>how-to/operate/aae-fold/list-buckets.md |
| OtherAPI | 17 | Performance and Efficiency | 1903 | reference/aae-fold-api/index.md<br>explanation/performance/index.md | reference/aae-fold-api/index.md<br>explanation/performance/index.md |
| OtherAPI | 18 | Node worker pools | 2143 | how-to/operate/monitor-worker-pools.md | how-to/operate/monitor-worker-pools.md |
| OtherAPI | 19 | AAE Fold efficiency | 2315 | reference/aae-fold-api/index.md<br>explanation/performance/index.md | reference/aae-fold-api/index.md<br>explanation/performance/index.md |
| OtherAPI | 20 | AAE Folds via the Command Line | 1606 | how-to/operate/aae-fold/run-from-command-line.md<br>reference/commands/aae.md | how-to/operate/aae-fold/run-from-command-line.md<br>reference/commands/aae.md |
| OtherAPI | 21 | AAE Folds via the Remote Console | 2819 | how-to/operate/use-remote-console.md<br>reference/operations/remote-console.md | how-to/operate/use-remote-console.md<br>reference/operations/remote-console.md |
| OtherAPI | 22 | AAE Folds via HTTP | 1855 | reference/aae-fold-api/index.md | reference/aae-fold-api/index.md |
| OtherAPI | 23 | AAE Folds via PB | 170 | reference/aae-fold-api/index.md | reference/aae-fold-api/index.md |
| OtherAPI | 24 | The Fetch API | 844 | reference/specialized-apis/fetch-api.md | reference/specialized-apis/fetch-api.md |
| OtherAPI | 25 | The Data Type API | 1835 | reference/specialized-apis/data-type-api.md<br>reference/data/distributed-data-types.md | reference/specialized-apis/data-type-api.md<br>reference/data/distributed-data-types.md |
| OtherAPI | 26 | The Map/Reduce API | 674 | reference/http-api/mapreduce.md<br>explanation/data-model/mapreduce.md | reference/http-api/mapreduce.md<br>explanation/data-model/mapreduce.md |
| OtherAPI | 27 | The List API | 839 | reference/specialized-apis/list-api.md | reference/specialized-apis/list-api.md |
| OtherAPI | 28 | Legacy Query API | 949 | reference/specialized-apis/legacy-query-api.md | reference/specialized-apis/legacy-query-api.md |
| OtherAPI | 29 | Strong Consistency API | 536 | reference/specialized-apis/strong-consistency-api.md<br>explanation/consistency/strong-consistency.md | reference/specialized-apis/strong-consistency-api.md<br>explanation/consistency/strong-consistency.md |
| OtherAPI | 30 | Write Once Path API | 709 | reference/specialized-apis/write-once-api.md<br>how-to/develop/use-write-once-path.md | reference/specialized-apis/write-once-api.md<br>how-to/develop/use-write-once-path.md |
| QueryAPI | 1 | Riak KV - Query API | 3231 | tutorials/query-api/index.md<br>reference/query-api/index.md<br>explanation/data-model/query-api.md | tutorials/query-api/index.md<br>reference/query-api/index.md<br>explanation/data-model/query-api.md |
| QueryAPI | 2 | Secondary Indexes - Adding Index Entries to an Object | 3521 | reference/data/secondary-indexes.md<br>tutorials/query-api/build-search-index.md | reference/data/secondary-indexes.md<br>tutorials/query-api/build-search-index.md |
| QueryAPI | 3 | Secondary Indexes - Querying Index Entries Overview | 681 | how-to/develop/query-with-query-api.md<br>reference/query-api/index.md | how-to/develop/query-with-query-api.md<br>reference/query-api/index.md |
| QueryAPI | 4 | Querying - Functional Summary | 3151 | explanation/data-model/query-api.md | explanation/data-model/query-api.md |
| QueryAPI | 5 | Querying - Non-functional Summary | 2026 | explanation/performance/query-execution.md | explanation/performance/query-execution.md |
| QueryAPI | 6 | Example (1) - A Simple People Search Index | 1506 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| QueryAPI | 7 | Example (1) - Simple Range Query | 747 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| QueryAPI | 8 | Example (1) - Finding an Exact Match | 5846 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| QueryAPI | 9 | Example (1) - Inexact Match | 1517 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| QueryAPI | 10 | Example (1) - Inexact Match of Given Name | 1573 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| QueryAPI | 11 | Example (1) - Wildcards within terms | 1631 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| QueryAPI | 12 | Example (1) - More Extensible Index Schema | 798 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| QueryAPI | 13 | Example (2) - An Alternative People Search | 4619 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| QueryAPI | 14 | Example (2) - Simple Variations and Limitations | 549 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| QueryAPI | 15 | Example (3) - Reporting index | 2550 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| QueryAPI | 16 | Example (3) - Simple Variations and Limitations | 441 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| QueryAPI | 17 | Query - Definition | 0 | reference/query-api/request.md | reference/query-api/request.md |
| QueryAPI | 18 | API Endpoint - THe URI | 1099 | reference/query-api/request.md | reference/query-api/request.md |
| QueryAPI | 19 | Query JSON - Definition | 154 | reference/query-api/request.md | reference/query-api/request.md |
| QueryAPI | 20 | aggregation_expression (optional) | 401 | reference/query-api/expressions.md | reference/query-api/expressions.md |
| QueryAPI | 21 | accumulation_option (optional - default = keys) | 2212 | reference/query-api/accumulation-options.md | reference/query-api/accumulation-options.md |
| QueryAPI | 22 | accumulation_term (optional - default = $term) | 272 | reference/query-api/accumulation-options.md | reference/query-api/accumulation-options.md |
| QueryAPI | 23 | max_results (optional) | 1070 | reference/query-api/request.md | reference/query-api/request.md |
| QueryAPI | 24 | continuation (optional) | 135 | reference/query-api/request.md | reference/query-api/request.md |
| QueryAPI | 25 | substitutions (optional) | 487 | reference/query-api/request.md | reference/query-api/request.md |
| QueryAPI | 26 | timeout (optional) | 221 | reference/query-api/request.md | reference/query-api/request.md |
| QueryAPI | 27 | inactivity_timeout (optional) | 827 | reference/query-api/request.md | reference/query-api/request.md |
| QueryAPI | 28 | query_list (required) | 984 | reference/query-api/request.md | reference/query-api/request.md |
| QueryAPI | 29 | Query Json - Expressions | 240 | reference/query-api/expressions.md | reference/query-api/expressions.md |
| QueryAPI | 30 | Evaluation Expression - Definition | 6044 | reference/query-api/expressions.md | reference/query-api/expressions.md |
| QueryAPI | 31 | Filter Expression - Definition | 877 | reference/query-api/expressions.md | reference/query-api/expressions.md |
| QueryAPI | 32 | Query Responses | 1971 | reference/query-api/responses.md | reference/query-api/responses.md |
| QueryAPI | 33 | Performance and Efficiency | 1219 | explanation/performance/query-execution.md<br>reference/query-api/limits.md | explanation/performance/query-execution.md<br>reference/query-api/limits.md |
| QueryAPI | 34 | Setup and Distribute the Query | 1330 | explanation/performance/query-execution.md<br>reference/query-api/limits.md | explanation/performance/query-execution.md<br>reference/query-api/limits.md |
| QueryAPI | 35 | Scanning | 1380 | explanation/performance/query-execution.md<br>reference/query-api/limits.md | explanation/performance/query-execution.md<br>reference/query-api/limits.md |
| QueryAPI | 36 | Filtering | 1178 | explanation/performance/query-execution.md<br>reference/query-api/limits.md | explanation/performance/query-execution.md<br>reference/query-api/limits.md |
| QueryAPI | 37 | Buffering | 3386 | explanation/performance/query-execution.md<br>reference/query-api/limits.md | explanation/performance/query-execution.md<br>reference/query-api/limits.md |
| QueryAPI | 38 | Aggregation of Combination Queries | 1274 | explanation/performance/query-execution.md<br>reference/query-api/limits.md | explanation/performance/query-execution.md<br>reference/query-api/limits.md |
| QueryAPI | 39 | Central Collation of Query Results | 987 | explanation/performance/query-execution.md<br>reference/query-api/limits.md | explanation/performance/query-execution.md<br>reference/query-api/limits.md |
| QueryAPI | 40 | Transformation of Results | 610 | explanation/performance/query-execution.md<br>reference/query-api/limits.md | explanation/performance/query-execution.md<br>reference/query-api/limits.md |
| QueryAPI | 41 | Notes on Implementation | 0 | explanation/data-model/query-api.md<br>reference/query-api/limits.md | explanation/data-model/query-api.md<br>reference/query-api/limits.md |
| QueryAPI | 42 | Siblings | 261 | explanation/data-model/version-vectors-and-siblings.md | explanation/data-model/version-vectors-and-siblings.md |
| QueryAPI | 43 | Unicode support | 407 | reference/query-api/expressions.md | reference/query-api/expressions.md |
| QueryAPI | 44 | Consistency | 940 | explanation/consistency/index.md | explanation/consistency/index.md |
| QueryAPI | 45 | Further Improvements | 225 | explanation/data-model/query-api.md | explanation/data-model/query-api.md |
| ReplicationGuide | 1 | Riak KV - Replication and Reconciliation | 3252 | explanation/replication/index.md<br>how-to/configure/replication/index.md<br>reference/replication-api/index.md | explanation/replication/index.md<br>how-to/configure/replication/index.md<br>reference/replication-api/index.md |
| ReplicationGuide | 2 | Overview | 2185 | explanation/replication/index.md | explanation/replication/index.md |
| ReplicationGuide | 3 | Concepts - Queues and Workers | 3572 | explanation/replication/queues.md<br>how-to/operate/monitor-worker-pools.md | explanation/replication/queues.md<br>how-to/operate/monitor-worker-pools.md |
| ReplicationGuide | 4 | Concepts - Replication References | 544 | explanation/replication/references-and-triggers.md | explanation/replication/references-and-triggers.md |
| ReplicationGuide | 5 | Concepts - Replication Triggers | 3588 | explanation/replication/references-and-triggers.md | explanation/replication/references-and-triggers.md |
| ReplicationGuide | 6 | Configuration of Real-Time Replication | 0 | how-to/configure/replication/configure-real-time-replication.md | how-to/configure/replication/configure-real-time-replication.md |
| ReplicationGuide | 7 | Enable a Real-Time Source | 1827 | how-to/configure/replication/configure-real-time-replication.md | how-to/configure/replication/configure-real-time-replication.md |
| ReplicationGuide | 8 | Enable a Real-Time Sink | 2496 | how-to/configure/replication/configure-real-time-replication.md<br>how-to/configure/replication/configure-sink-nodes.md | how-to/configure/replication/configure-real-time-replication.md<br>how-to/configure/replication/configure-sink-nodes.md |
| ReplicationGuide | 9 | Security Configuration | 1524 | how-to/configure/replication/secure-replication.md | how-to/configure/replication/secure-replication.md |
| ReplicationGuide | 10 | Additional Configuration | 1853 | reference/configuration/replication.md | reference/configuration/replication.md |
| ReplicationGuide | 11 | Configuration of All-Cluster Reconciliation | 340 | how-to/configure/replication/configure-fullsync.md<br>how-to/configure/replication/enable-tictac-aae.md | how-to/configure/replication/configure-fullsync.md<br>how-to/configure/replication/enable-tictac-aae.md |
| ReplicationGuide | 12 | Enable Tictac AAE | 862 | how-to/configure/replication/enable-tictac-aae.md | how-to/configure/replication/enable-tictac-aae.md |
| ReplicationGuide | 13 | Initial Configuration | 3562 | how-to/configure/replication/configure-fullsync.md | how-to/configure/replication/configure-fullsync.md |
| ReplicationGuide | 14 | Enabling Checks | 4527 | how-to/configure/replication/configure-fullsync.md | how-to/configure/replication/configure-fullsync.md |
| ReplicationGuide | 15 | Tuning checks - the maximum results limit | 1621 | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| ReplicationGuide | 16 | Configuration of Per-Bucket Reconciliation | 2225 | how-to/configure/replication/per-bucket-reconciliation.md | how-to/configure/replication/per-bucket-reconciliation.md |
| ReplicationGuide | 17 | Migrating a cluster | 1846 | how-to/configure/replication/migrate-cluster.md | how-to/configure/replication/migrate-cluster.md |
| ReplicationGuide | 18 | Replication API | 723 | reference/replication-api/index.md | reference/replication-api/index.md |
| ReplicationGuide | 19 | Monitoring and Runtime Changes | 0 | how-to/operate/monitor-reconciliation.md<br>reference/replication-api/runtime-controls.md | how-to/operate/monitor-reconciliation.md<br>reference/replication-api/runtime-controls.md |
| ReplicationGuide | 20 | Monitoring real-time replication via logs | 737 | how-to/operate/monitor-reconciliation.md | how-to/operate/monitor-reconciliation.md |
| ReplicationGuide | 21 | Making runtime changes to the Source | 626 | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| ReplicationGuide | 22 | Making runtime changes to the Sink | 1234 | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| ReplicationGuide | 23 | Monitoring reconciliation exchanges via logs | 3503 | how-to/operate/monitor-reconciliation.md | how-to/operate/monitor-reconciliation.md |
| ReplicationGuide | 24 | Statistics available via Riak stats | 2118 | reference/operations/replication-statistics.md | reference/operations/replication-statistics.md |
| ReplicationGuide | 25 | Prompting a reconciliation check | 313 | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| ReplicationGuide | 26 | Configure and monitor work queues | 1102 | how-to/operate/monitor-worker-pools.md<br>reference/replication-api/runtime-controls.md | how-to/operate/monitor-worker-pools.md<br>reference/replication-api/runtime-controls.md |
| ReplicationGuide | 27 | Update the request limits | 808 | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| ReplicationGuide | 28 | Overriding the range | 1194 | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| ReplicationGuide | 29 | Re-replicating keys for a given time period | 240 | how-to/operate/rereplicate-time-window.md | how-to/operate/rereplicate-time-window.md |
| ReplicationGuide | 30 | Re-Sync a Bucket | 2927 | reference/replication-api/runtime-controls.md | how-to/operate/resync-bucket.md<br>reference/replication-api/runtime-controls.md |
| ReplicationGuide | 31 | Participate in Coverage | 966 | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| ReplicationGuide | 32 | Suspend full-sync | 1125 | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| ReplicationGuide | 33 | Trigger Tree Repairs | 1734 | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| ReplicationGuide | 34 | Legacy Replication - riak_repl | 2189 | explanation/replication/v2-and-v3-replication.md<br>how-to/configure/replication/configure-v2-multi-datacenter.md | explanation/replication/v2-and-v3-replication.md<br>how-to/configure/replication/configure-v2-multi-datacenter.md |
| ReplicationGuide | 35 | Replication scope | 336 | explanation/replication/reconciliation-scope.md | explanation/replication/reconciliation-scope.md |
| RiakTheoryGuide | 1 | Riak KV - Theory Guide | 447 | explanation/foundations/index.md | explanation/foundations/index.md |
| RiakTheoryGuide | 2 | The Ring - The distribution of vnodes | 3475 | explanation/foundations/clusters-rings-and-partitions.md<br>explanation/foundations/virtual-nodes.md | explanation/foundations/clusters-rings-and-partitions.md<br>explanation/foundations/virtual-nodes.md |
| RiakTheoryGuide | 3 | Eventual Consistency | 3589 | explanation/consistency/eventual-consistency.md | explanation/consistency/eventual-consistency.md |
| RiakTheoryGuide | 4 | Quorum on Read, Write and Query | 1795 | explanation/consistency/read-write-quorums.md | explanation/consistency/read-write-quorums.md |
| RiakTheoryGuide | 5 | Version vectors | 3025 | explanation/data-model/version-vectors-and-siblings.md | explanation/data-model/version-vectors-and-siblings.md |
| RiakTheoryGuide | 6 | Background processes | 723 | explanation/operations/index.md | explanation/operations/index.md |
| RiakTheoryGuide | 7 | Anti-Entropy | 6691 | explanation/replication/active-anti-entropy.md<br>explanation/replication/tictac-aae.md | explanation/replication/active-anti-entropy.md<br>explanation/replication/tictac-aae.md |
| RiakTheoryGuide | 8 | Disk-backed Queues | 858 | explanation/replication/queues.md | explanation/replication/queues.md |
| RiakTheoryGuide | 9 | Riak Core cluster management | 2858 | explanation/operations/ring-changes-and-handoffs.md | explanation/operations/ring-changes-and-handoffs.md |
| RiakTheoryGuide | 10 | Backend Design | 126 | explanation/storage/index.md<br>explanation/storage/choosing-backend.md | explanation/storage/index.md<br>explanation/storage/choosing-backend.md |
| RiakTheoryGuide | 11 | The bitcask backend | 987 | explanation/storage/bitcask.md | explanation/storage/bitcask.md |
| RiakTheoryGuide | 12 | The leveled backend | 3986 | explanation/storage/leveled.md | explanation/storage/leveled.md |
| RiakTheoryGuide | 13 | Caching and Acceleration | 1264 | explanation/storage/leveled.md | explanation/storage/leveled.md |
| RiakTheoryGuide | 14 | File Formats | 1513 | explanation/storage/leveled.md | explanation/storage/leveled.md |
| RiakTheoryGuide | 15 | Data safety and security | 591 | explanation/storage/leveled.md | explanation/storage/leveled.md |
| RiakTheoryGuide | 16 | Compaction | 4127 | explanation/storage/leveled.md | explanation/storage/leveled.md |
| RiakTheoryGuide | 17 | Head-only Mode | 860 | explanation/storage/leveled.md | explanation/storage/leveled.md |

## Validation

- Migration issues: 0
- Full-tree metadata issues: 0
- Duplicate sibling sidebar positions: 0
- Missing destinations: 0
- Unresolved QuickDocs-relative links: 0
- Changes to the read-only 3.2.5 source: 0
- WSL source worktree dirty: False
- Total Markdown files checked: 776
# Riak QuickDocs 3.4 to Diátaxis coverage audit

Generated: 2026-08-28T01:18:08+09:00

## Outcome

The audit inventoried all **10** published QuickDocs pages and all **282** H1-H4 headings. Every heading is mapped to Diátaxis destinations: **197** pages for OpenRiak KV 3.4.0 and **198** pages for OpenRiak KV 3.4.1.

No QuickDocs prose was copied. The audit added **20** versioned one-sentence stubs for missing topics and added exact source anchors plus rewrite status to **395** mapped pages.

## Method

- Audit unit: every published H1-H4 heading.
- Diátaxis treatment: mixed QuickDocs chapters are split among tutorials, how-to guides, reference, and explanation.
- Content treatment: destinations retain or receive a single-sentence content suggestion; full prose is intentionally deferred.
- Traceability: each destination contains exact QuickDocs anchors in quickdocs_sources and quickdocs_rewrite_status: planned.
- Versioning: shared 3.4 topics map into both version trees, with a 3.4.1-specific bucket-resynchronization destination.

## Source inventory

| QuickDocs page | URL | HTTP | Bytes | Headings | SHA-256 |
|---|---|---:|---:|---:|---|
| OpenRiak QuickDocs 3.4 | https://openriak.github.io/riak/ | 200 | 13381 | 3 | 58EC6F5E4BF96A3D94B40FD7BAEEB3830A23AA66DFE873D5CEB7D79EA11F1250 |
| Riak KV - Building and Scaling a Cluster | https://openriak.github.io/riak/BuildAndScaleClusterGuide.html | 200 | 47157 | 15 | 77E4A78EB3905F05A6D1D7E9FB3B7502A2FCF5020126ACFC6A2B16D40A4505E9 |
| Riak KV - Initial Design Decisions | https://openriak.github.io/riak/InitialDesignDecisions.html | 200 | 54815 | 26 | F2F06FD2421BE2C83C746D58E139479DC542DBF6F2787936E95038D648D33908 |
| Riak KV - Install and Start | https://openriak.github.io/riak/InstallAndStartGuide.html | 200 | 66037 | 31 | F99A5F70AC3FC2E04554067E682E2097301D811B0E296000A1D207ED1AED6506 |
| Riak KV - Object API | https://openriak.github.io/riak/ObjectAPI.html | 200 | 51841 | 24 | A99FB58D01FDF321F07D949D7A515C6F32A3DB1546B41EC4D9DCFBC19ACF275B |
| Riak KV - Operations and Troubleshooting | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html | 200 | 125208 | 56 | 23E735B01EB22429F654BAD899328A2B2E432D8B8FF23C07DCAA7780D8090385 |
| Riak KV - Other APIs | https://openriak.github.io/riak/OtherAPI.html | 200 | 61688 | 30 | E5AD1179B075975FD01D7142249CBD2F2C4A93B1AADA31DD87F8B1D4E0FE467B |
| Riak KV - Query API | https://openriak.github.io/riak/QueryAPI.html | 200 | 131393 | 45 | 451273A58059DAD494CC6037B56294761FBCAD21E4D05C7B443DC5541AC01213 |
| Riak KV - Replication and Reconciliation | https://openriak.github.io/riak/ReplicationGuide.html | 200 | 102103 | 35 | 94099480FB6371EECEF11A3DFD920DFE3D95C7347F17ED3239C9CE189171C8D3 |
| Riak KV - Theory Guide | https://openriak.github.io/riak/RiakTheoryGuide.html | 200 | 57117 | 17 | D891FBF026CFC33EB5549EAA25020DB197E7A016AACA20B724BC650D28128E4F |

## Diátaxis distribution

| Version | Diátaxis type | Destinations |
|---|---|---:|
| 3.4.0 | explanation | 46 |
| 3.4.0 | how-to | 96 |
| 3.4.0 | reference | 52 |
| 3.4.0 | tutorial | 3 |
| 3.4.1 | explanation | 46 |
| 3.4.1 | how-to | 97 |
| 3.4.1 | reference | 52 |
| 3.4.1 | tutorial | 3 |

## New stubs

| Version | Destination | Type | Content suggestion |
|---|---|---|---|
| 3.4.0 | explanation/foundations/history.md | explanation | Explain the evolution of Riak from its original release through community stewardship and OpenRiak. |
| 3.4.0 | how-to/operate/check-vnode-status.md | how-to | Show operators how to use riak admin vnode-status to inspect vnodes and their storage backends. |
| 3.4.0 | how-to/operate/routine-operations-checklist.md | how-to | Show operators how to perform a repeatable health and maintenance review of an OpenRiak cluster. |
| 3.4.0 | how-to/plan/choose-multi-cluster-topology.md | how-to | Show architects how to choose between locations, multiple clusters, and replication topologies for resilience and scale. |
| 3.4.0 | how-to/plan/choose-ring-size.md | how-to | Show architects how to select a ring size from node count, CPU capacity, query workload, and expected growth. |
| 3.4.0 | how-to/plan/choose-storage-backend.md | how-to | Show architects how to select a storage backend from durability, query, memory, compaction, and operational requirements. |
| 3.4.0 | reference/commands/vnode-status.md | reference | Define the syntax, output fields, scope, and operational cautions for riak admin vnode-status. |
| 3.4.0 | reference/configuration/bucket-properties.md | reference | Define supported bucket properties, defaults, interactions, and version-specific constraints. |
| 3.4.0 | reference/http-api/object-request-options.md | reference | Define common OpenRiak Object API GET and PUT parameters, defaults, and response behavior. |
| 3.4.0 | reference/operations/cluster-claim-algorithms.md | reference | Compare choose_claim_v2, choose_claim_v3, and choose_claim_v4 inputs, guarantees, and compatibility. |
| 3.4.0 | reference/specialized-apis/data-type-api.md | reference | Define endpoints, request and response formats, options, and constraints for OpenRiak distributed data types. |
| 3.4.1 | explanation/foundations/history.md | explanation | Explain the evolution of Riak from its original release through community stewardship and OpenRiak. |
| 3.4.1 | how-to/operate/routine-operations-checklist.md | how-to | Show operators how to perform a repeatable health and maintenance review of an OpenRiak cluster. |
| 3.4.1 | how-to/plan/choose-multi-cluster-topology.md | how-to | Show architects how to choose between locations, multiple clusters, and replication topologies for resilience and scale. |
| 3.4.1 | how-to/plan/choose-ring-size.md | how-to | Show architects how to select a ring size from node count, CPU capacity, query workload, and expected growth. |
| 3.4.1 | how-to/plan/choose-storage-backend.md | how-to | Show architects how to select a storage backend from durability, query, memory, compaction, and operational requirements. |
| 3.4.1 | reference/configuration/bucket-properties.md | reference | Define supported bucket properties, defaults, interactions, and version-specific constraints. |
| 3.4.1 | reference/http-api/object-request-options.md | reference | Define common OpenRiak Object API GET and PUT parameters, defaults, and response behavior. |
| 3.4.1 | reference/operations/cluster-claim-algorithms.md | reference | Compare choose_claim_v2, choose_claim_v3, and choose_claim_v4 inputs, guarantees, and compatibility. |
| 3.4.1 | reference/specialized-apis/data-type-api.md | reference | Define endpoints, request and response formats, options, and constraints for OpenRiak distributed data types. |

## Validation

| Check | Result |
|---|---:|
| live_pages | 10 |
| live_headings | 282 |
| unmapped_headings | 0 |
| mapping_records | 564 |
| unique_destinations_3_4_0 | 197 |
| unique_destinations_3_4_1 | 198 |
| created_stub_files | 20 |
| missing_mapped_targets | 0 |
| missing_exact_source_attributions | 0 |
| missing_rewrite_status | 0 |
| missing_source_material_tags | 0 |
| target_markdown_files | 776 |
| front_matter_errors | 0 |
| product_version_errors | 0 |
| created_stub_content_errors | 0 |
| duplicate_sidebar_positions | 0 |
| live_http_errors | 0 |
| mapped_non_draft_pages | 4 |
| mapped_missing_descriptions | 0 |
| report_json_parse_errors | 0 |
| report_json_source_section_rows | 282 |
| report_json_destination_rows | 395 |
| report_markdown_source_section_rows | 282 |
| report_markdown_destination_rows | 395 |
| legacy_source_hash_changes | 0 |

## Complete section mapping

| QuickDocs page | Level | Heading | Source anchor | Mapping basis | 3.4.0 destinations | 3.4.1 destinations |
|---|---:|---|---|---|---|---|
| OpenRiak QuickDocs 3.4 | H1 | OpenRiak QuickDocs 3.4 | https://openriak.github.io/riak/#openriak-quickdocs-34 | exact | index.md<br>explanation/foundations/index.md | index.md<br>explanation/foundations/index.md |
| OpenRiak QuickDocs 3.4 | H2 | What is Riak? | https://openriak.github.io/riak/#what-is-riak | exact | explanation/foundations/why-openriak.md<br>explanation/foundations/use-cases.md | explanation/foundations/why-openriak.md<br>explanation/foundations/use-cases.md |
| OpenRiak QuickDocs 3.4 | H2 | Riak History | https://openriak.github.io/riak/#riak-history | exact | explanation/foundations/history.md | explanation/foundations/history.md |
| Riak KV - Building and Scaling a Cluster | H1 | Riak KV - Building and Scaling a Cluster | https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#riak-kv---building-and-scaling-a-cluster | exact | how-to/plan/index.md<br>how-to/operate/index.md | how-to/plan/index.md<br>how-to/operate/index.md |
| Riak KV - Building and Scaling a Cluster | H2 | Choosing infrastructure | https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#choosing-infrastructure | exact | how-to/plan/size-cluster.md<br>how-to/plan/production-readiness-checklist.md | how-to/plan/size-cluster.md<br>how-to/plan/production-readiness-checklist.md |
| Riak KV - Building and Scaling a Cluster | H3 | Nodes | https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#nodes | exact | how-to/plan/size-cluster.md | how-to/plan/size-cluster.md |
| Riak KV - Building and Scaling a Cluster | H3 | Network | https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#network | exact | reference/configuration/networking.md<br>how-to/secure/secure-networking.md | reference/configuration/networking.md<br>how-to/secure/secure-networking.md |
| Riak KV - Building and Scaling a Cluster | H3 | Load-balancing | https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#load-balancing | exact | how-to/configure/load-balancing-proxy.md | how-to/configure/load-balancing-proxy.md |
| Riak KV - Building and Scaling a Cluster | H2 | Forming and Expanding a Riak cluster | https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#forming-and-expanding-a-riak-cluster | exact | how-to/operate/add-node.md<br>how-to/operate/plan-and-commit-cluster-change.md | how-to/operate/add-node.md<br>how-to/operate/plan-and-commit-cluster-change.md |
| Riak KV - Building and Scaling a Cluster | H3 | Join process - staging a change | https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---staging-a-change | exact | how-to/operate/add-node.md | how-to/operate/add-node.md |
| Riak KV - Building and Scaling a Cluster | H3 | Join process - plan a change | https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---plan-a-change | exact | how-to/operate/plan-and-commit-cluster-change.md | how-to/operate/plan-and-commit-cluster-change.md |
| Riak KV - Building and Scaling a Cluster | H4 | Join process - choose_claim_v2 (default) | https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---choose_claim_v2-default | exact | reference/operations/cluster-claim-algorithms.md | reference/operations/cluster-claim-algorithms.md |
| Riak KV - Building and Scaling a Cluster | H4 | Join process - choose_claim_v3 | https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---choose_claim_v3 | exact | reference/operations/cluster-claim-algorithms.md | reference/operations/cluster-claim-algorithms.md |
| Riak KV - Building and Scaling a Cluster | H4 | Join process - choose_claim_v4 (recommended) | https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---choose_claim_v4-recommended | exact | reference/operations/cluster-claim-algorithms.md | reference/operations/cluster-claim-algorithms.md |
| Riak KV - Building and Scaling a Cluster | H3 | Join process - verify the plan | https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---verify-the-plan | exact | how-to/operate/plan-and-commit-cluster-change.md | how-to/operate/plan-and-commit-cluster-change.md |
| Riak KV - Building and Scaling a Cluster | H3 | Join process - commit the plan | https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---commit-the-plan | exact | how-to/operate/plan-and-commit-cluster-change.md | how-to/operate/plan-and-commit-cluster-change.md |
| Riak KV - Building and Scaling a Cluster | H3 | Join process - await handoffs | https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#join-process---await-handoffs | exact | how-to/operate/manage-handoffs.md | how-to/operate/manage-handoffs.md |
| Riak KV - Building and Scaling a Cluster | H2 | Shrinking a cluster | https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#shrinking-a-cluster | exact | how-to/operate/remove-node.md | how-to/operate/remove-node.md |
| Riak KV - Initial Design Decisions | H1 | Riak KV - Initial Design Decisions | https://openriak.github.io/riak/InitialDesignDecisions.html#riak-kv---initial-design-decisions | exact | how-to/plan/index.md | how-to/plan/index.md |
| Riak KV - Initial Design Decisions | H2 | Database backend | https://openriak.github.io/riak/InitialDesignDecisions.html#database-backend | exact | how-to/plan/choose-storage-backend.md<br>explanation/storage/choosing-backend.md | how-to/plan/choose-storage-backend.md<br>explanation/storage/choosing-backend.md |
| Riak KV - Initial Design Decisions | H3 | Database backend - making a choice | https://openriak.github.io/riak/InitialDesignDecisions.html#database-backend---making-a-choice | exact | how-to/plan/choose-storage-backend.md | how-to/plan/choose-storage-backend.md |
| Riak KV - Initial Design Decisions | H4 | Leveled | https://openriak.github.io/riak/InitialDesignDecisions.html#leveled | exact | explanation/storage/leveled.md<br>how-to/configure/backends/leveled.md | explanation/storage/leveled.md<br>how-to/configure/backends/leveled.md |
| Riak KV - Initial Design Decisions | H4 | Bitcask | https://openriak.github.io/riak/InitialDesignDecisions.html#bitcask | exact | explanation/storage/bitcask.md<br>how-to/configure/backends/bitcask.md | explanation/storage/bitcask.md<br>how-to/configure/backends/bitcask.md |
| Riak KV - Initial Design Decisions | H4 | Eleveldb (deprecated) | https://openriak.github.io/riak/InitialDesignDecisions.html#eleveldb-deprecated | exact | explanation/storage/leveldb.md<br>how-to/configure/backends/leveldb.md | explanation/storage/leveldb.md<br>how-to/configure/backends/leveldb.md |
| Riak KV - Initial Design Decisions | H4 | In-memory (deprecated) | https://openriak.github.io/riak/InitialDesignDecisions.html#in-memory-deprecated | exact | explanation/storage/memory.md<br>how-to/configure/backends/memory.md | explanation/storage/memory.md<br>how-to/configure/backends/memory.md |
| Riak KV - Initial Design Decisions | H4 | Multi-backend | https://openriak.github.io/riak/InitialDesignDecisions.html#multi-backend | exact | explanation/storage/multi-backend.md<br>how-to/configure/backends/multi.md | explanation/storage/multi-backend.md<br>how-to/configure/backends/multi.md |
| Riak KV - Initial Design Decisions | H3 | Database backend - changing the choice | https://openriak.github.io/riak/InitialDesignDecisions.html#database-backend---changing-the-choice | exact | how-to/configure/backends/change-backend.md | how-to/configure/backends/change-backend.md |
| Riak KV - Initial Design Decisions | H2 | Ring size | https://openriak.github.io/riak/InitialDesignDecisions.html#ring-size | exact | how-to/plan/choose-ring-size.md<br>explanation/foundations/clusters-rings-and-partitions.md | how-to/plan/choose-ring-size.md<br>explanation/foundations/clusters-rings-and-partitions.md |
| Riak KV - Initial Design Decisions | H3 | Ring size - making a choice | https://openriak.github.io/riak/InitialDesignDecisions.html#ring-size---making-a-choice | exact | how-to/plan/choose-ring-size.md | how-to/plan/choose-ring-size.md |
| Riak KV - Initial Design Decisions | H3 | Ring size - changing the choice | https://openriak.github.io/riak/InitialDesignDecisions.html#ring-size---changing-the-choice | exact | how-to/configure/replication/migrate-cluster.md | how-to/configure/replication/migrate-cluster.md |
| Riak KV - Initial Design Decisions | H2 | Intra-cluster data resilience | https://openriak.github.io/riak/InitialDesignDecisions.html#intra-cluster-data-resilience | exact | how-to/plan/choose-intra-cluster-resilience.md<br>explanation/foundations/intra-cluster-resilience.md | how-to/plan/choose-intra-cluster-resilience.md<br>explanation/foundations/intra-cluster-resilience.md |
| Riak KV - Initial Design Decisions | H3 | Intra-cluster data resilience - making a choice | https://openriak.github.io/riak/InitialDesignDecisions.html#intra-cluster-data-resilience---making-a-choice | exact | how-to/plan/choose-intra-cluster-resilience.md | how-to/plan/choose-intra-cluster-resilience.md |
| Riak KV - Initial Design Decisions | H4 | Data distribution guarantees | https://openriak.github.io/riak/InitialDesignDecisions.html#data-distribution-guarantees | exact | how-to/plan/choose-intra-cluster-resilience.md<br>reference/configuration/bucket-properties.md | how-to/plan/choose-intra-cluster-resilience.md<br>reference/configuration/bucket-properties.md |
| Riak KV - Initial Design Decisions | H4 | Proactive reconciliation | https://openriak.github.io/riak/InitialDesignDecisions.html#proactive-reconciliation | exact | explanation/replication/active-anti-entropy.md<br>how-to/configure/replication/enable-tictac-aae.md | explanation/replication/active-anti-entropy.md<br>how-to/configure/replication/enable-tictac-aae.md |
| Riak KV - Initial Design Decisions | H3 | Intra-cluster data resilience - changing the choice | https://openriak.github.io/riak/InitialDesignDecisions.html#intra-cluster-data-resilience---changing-the-choice | exact | how-to/configure/replication/enable-tictac-aae.md<br>how-to/plan/choose-intra-cluster-resilience.md | how-to/configure/replication/enable-tictac-aae.md<br>how-to/plan/choose-intra-cluster-resilience.md |
| Riak KV - Initial Design Decisions | H2 | Interconnecting multiple clusters | https://openriak.github.io/riak/InitialDesignDecisions.html#interconnecting-multiple-clusters | exact | how-to/plan/choose-multi-cluster-topology.md<br>explanation/replication/multi-datacenter-architecture.md | how-to/plan/choose-multi-cluster-topology.md<br>explanation/replication/multi-datacenter-architecture.md |
| Riak KV - Initial Design Decisions | H3 | Interconnecting multiple clusters - making a choice | https://openriak.github.io/riak/InitialDesignDecisions.html#interconnecting-multiple-clusters---making-a-choice | exact | how-to/plan/choose-multi-cluster-topology.md | how-to/plan/choose-multi-cluster-topology.md |
| Riak KV - Initial Design Decisions | H3 | Interconnecting multiple clusters - changing the choice | https://openriak.github.io/riak/InitialDesignDecisions.html#interconnecting-multiple-clusters---changing-the-choice | exact | how-to/configure/replication/migrate-cluster.md | how-to/configure/replication/migrate-cluster.md |
| Riak KV - Initial Design Decisions | H2 | Deleting data | https://openriak.github.io/riak/InitialDesignDecisions.html#deleting-data | exact | how-to/plan/choose-deletion-policy.md<br>explanation/data-model/deletion-policies.md | how-to/plan/choose-deletion-policy.md<br>explanation/data-model/deletion-policies.md |
| Riak KV - Initial Design Decisions | H3 | Deleting data - making a choice | https://openriak.github.io/riak/InitialDesignDecisions.html#deleting-data---making-a-choice | exact | how-to/plan/choose-deletion-policy.md | how-to/plan/choose-deletion-policy.md |
| Riak KV - Initial Design Decisions | H3 | Deleting data - changing the choice | https://openriak.github.io/riak/InitialDesignDecisions.html#deleting-data---changing-the-choice | exact | how-to/operate/schedule-object-reaping.md<br>how-to/configure/global-object-expiration.md | how-to/operate/schedule-object-reaping.md<br>how-to/configure/global-object-expiration.md |
| Riak KV - Initial Design Decisions | H2 | Mapping data to objects | https://openriak.github.io/riak/InitialDesignDecisions.html#mapping-data-to-objects | exact | how-to/plan/map-data-to-objects.md<br>explanation/data-model/keys-objects-and-buckets.md | how-to/plan/map-data-to-objects.md<br>explanation/data-model/keys-objects-and-buckets.md |
| Riak KV - Initial Design Decisions | H3 | Mapping data to objects - making a choice | https://openriak.github.io/riak/InitialDesignDecisions.html#mapping-data-to-objects---making-a-choice | exact | how-to/plan/map-data-to-objects.md | how-to/plan/map-data-to-objects.md |
| Riak KV - Initial Design Decisions | H3 | Mapping data to objects - changing the choice | https://openriak.github.io/riak/InitialDesignDecisions.html#mapping-data-to-objects---changing-the-choice | exact | how-to/plan/map-data-to-objects.md<br>explanation/data-model/keys-objects-and-buckets.md | how-to/plan/map-data-to-objects.md<br>explanation/data-model/keys-objects-and-buckets.md |
| Riak KV - Install and Start | H1 | Riak KV - Install and Start | https://openriak.github.io/riak/InstallAndStartGuide.html#riak-kv---install-and-start | exact | how-to/install/index.md | how-to/install/index.md |
| Riak KV - Install and Start | H2 | Installation | https://openriak.github.io/riak/InstallAndStartGuide.html#installation | exact | how-to/install/index.md | how-to/install/index.md |
| Riak KV - Install and Start | H3 | Install Erlang/OTP | https://openriak.github.io/riak/InstallAndStartGuide.html#install-erlangotp | exact | how-to/install/source.md<br>reference/releases/supported-platforms.md | how-to/install/source.md<br>reference/releases/supported-platforms.md |
| Riak KV - Install and Start | H3 | Download Riak | https://openriak.github.io/riak/InstallAndStartGuide.html#download-riak | exact | reference/releases/downloads.md | reference/releases/downloads.md |
| Riak KV - Install and Start | H3 | Make Riak | https://openriak.github.io/riak/InstallAndStartGuide.html#make-riak | exact | how-to/install/source.md | how-to/install/source.md |
| Riak KV - Install and Start | H4 | Local release | https://openriak.github.io/riak/InstallAndStartGuide.html#local-release | exact | how-to/install/source.md<br>how-to/install/verify-installation.md | how-to/install/source.md<br>how-to/install/verify-installation.md |
| Riak KV - Install and Start | H4 | Local cluster | https://openriak.github.io/riak/InstallAndStartGuide.html#local-cluster | exact | tutorials/first-cluster/index.md<br>how-to/install/source.md | tutorials/first-cluster/index.md<br>how-to/install/source.md |
| Riak KV - Install and Start | H4 | Generating a package | https://openriak.github.io/riak/InstallAndStartGuide.html#generating-a-package | exact | how-to/install/source.md | how-to/install/source.md |
| Riak KV - Install and Start | H3 | Using pre-built packages | https://openriak.github.io/riak/InstallAndStartGuide.html#using-pre-built-packages | exact | how-to/install/index.md<br>reference/releases/supported-platforms.md | how-to/install/index.md<br>reference/releases/supported-platforms.md |
| Riak KV - Install and Start | H2 | Starting Riak | https://openriak.github.io/riak/InstallAndStartGuide.html#starting-riak | exact | how-to/operate/start-stop-restart-node.md<br>how-to/install/verify-installation.md | how-to/operate/start-stop-restart-node.md<br>how-to/install/verify-installation.md |
| Riak KV - Install and Start | H3 | Starting Riak by Make Method | https://openriak.github.io/riak/InstallAndStartGuide.html#starting-riak-by-make-method | exact | how-to/install/source.md<br>how-to/operate/start-stop-restart-node.md | how-to/install/source.md<br>how-to/operate/start-stop-restart-node.md |
| Riak KV - Install and Start | H4 | Local Release or Cluster | https://openriak.github.io/riak/InstallAndStartGuide.html#local-release-or-cluster | exact | how-to/operate/start-stop-restart-node.md | how-to/operate/start-stop-restart-node.md |
| Riak KV - Install and Start | H4 | Package Deployment | https://openriak.github.io/riak/InstallAndStartGuide.html#package-deployment | exact | how-to/operate/start-stop-restart-node.md | how-to/operate/start-stop-restart-node.md |
| Riak KV - Install and Start | H4 | Setting ulimit | https://openriak.github.io/riak/InstallAndStartGuide.html#setting-ulimit | exact | how-to/tune/set-open-files-limit.md | how-to/tune/set-open-files-limit.md |
| Riak KV - Install and Start | H3 | Configuration of Riak - key riak.conf changes | https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---key-riakconf-changes | exact | how-to/configure/basic-node-settings.md<br>how-to/configure/api-listeners.md<br>how-to/configure/verify-configuration.md | how-to/configure/basic-node-settings.md<br>how-to/configure/api-listeners.md<br>how-to/configure/verify-configuration.md |
| Riak KV - Install and Start | H3 | Configuration of Riak - leveled backend | https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---leveled-backend | exact | how-to/configure/backends/leveled.md | how-to/configure/backends/leveled.md |
| Riak KV - Install and Start | H3 | Configuration of Riak - bitcask backend | https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---bitcask-backend | exact | how-to/configure/backends/bitcask.md | how-to/configure/backends/bitcask.md |
| Riak KV - Install and Start | H3 | Configuration of Riak - Delete Mode | https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---delete-mode | exact | how-to/plan/choose-deletion-policy.md<br>reference/operations/object-deletion.md | how-to/plan/choose-deletion-policy.md<br>reference/operations/object-deletion.md |
| Riak KV - Install and Start | H3 | Configuration of Riak - Bucket Properties | https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---bucket-properties | exact | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| Riak KV - Install and Start | H4 | Property - dvv_enabled | https://openriak.github.io/riak/InstallAndStartGuide.html#property---dvv_enabled | inherited-h3 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| Riak KV - Install and Start | H4 | Property - allow_mult | https://openriak.github.io/riak/InstallAndStartGuide.html#property---allow_mult | inherited-h3 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| Riak KV - Install and Start | H4 | Property - last_write_wins | https://openriak.github.io/riak/InstallAndStartGuide.html#property---last_write_wins | inherited-h3 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| Riak KV - Install and Start | H4 | Property - n_val | https://openriak.github.io/riak/InstallAndStartGuide.html#property---n_val | inherited-h3 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| Riak KV - Install and Start | H4 | Property - node_confirms | https://openriak.github.io/riak/InstallAndStartGuide.html#property---node_confirms | inherited-h3 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| Riak KV - Install and Start | H4 | Property - sync_on_write | https://openriak.github.io/riak/InstallAndStartGuide.html#property---sync_on_write | inherited-h3 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| Riak KV - Install and Start | H4 | Property - aae_tree_exclude | https://openriak.github.io/riak/InstallAndStartGuide.html#property---aae_tree_exclude | exact | how-to/configure/replication/exclude-bucket-from-aae.md<br>reference/configuration/bucket-properties.md | how-to/configure/replication/exclude-bucket-from-aae.md<br>reference/configuration/bucket-properties.md |
| Riak KV - Install and Start | H4 | Property - small_vclock | https://openriak.github.io/riak/InstallAndStartGuide.html#property---small_vclock | inherited-h3 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| Riak KV - Install and Start | H4 | Property - notfound_ok | https://openriak.github.io/riak/InstallAndStartGuide.html#property---notfound_ok | inherited-h3 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| Riak KV - Install and Start | H4 | Property - pr and pw | https://openriak.github.io/riak/InstallAndStartGuide.html#property---pr-and-pw | inherited-h3 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| Riak KV - Install and Start | H4 | Property - backend | https://openriak.github.io/riak/InstallAndStartGuide.html#property---backend | exact | reference/configuration/bucket-properties.md<br>how-to/configure/backends/index.md | reference/configuration/bucket-properties.md<br>how-to/configure/backends/index.md |
| Riak KV - Install and Start | H4 | Property - General read/write parameters | https://openriak.github.io/riak/InstallAndStartGuide.html#property---general-readwrite-parameters | inherited-h3 | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md | reference/configuration/bucket-properties.md<br>how-to/operate/manage-bucket-types.md |
| Riak KV - Object API | H1 | Riak KV - Object API | https://openriak.github.io/riak/ObjectAPI.html#riak-kv---object-api | exact | reference/http-api/index.md<br>reference/data/index.md<br>how-to/develop/index.md | reference/http-api/index.md<br>reference/data/index.md<br>how-to/develop/index.md |
| Riak KV - Object API | H2 | Object Identifier - the URL | https://openriak.github.io/riak/ObjectAPI.html#object-identifier---the-url | exact | reference/data/keys-and-objects.md<br>reference/http-api/index.md | reference/data/keys-and-objects.md<br>reference/http-api/index.md |
| Riak KV - Object API | H2 | Object Value - the request body | https://openriak.github.io/riak/ObjectAPI.html#object-value---the-request-body | exact | reference/data/keys-and-objects.md<br>reference/data/content-types.md | reference/data/keys-and-objects.md<br>reference/data/content-types.md |
| Riak KV - Object API | H2 | Object Meta Content - the request and response headers | https://openriak.github.io/riak/ObjectAPI.html#object-meta-content---the-request-and-response-headers | exact | reference/data/object-metadata.md | reference/data/object-metadata.md |
| Riak KV - Object API | H3 | Version Vector | https://openriak.github.io/riak/ObjectAPI.html#version-vector | exact | reference/data/version-vectors.md<br>explanation/data-model/version-vectors-and-siblings.md | reference/data/version-vectors.md<br>explanation/data-model/version-vectors-and-siblings.md |
| Riak KV - Object API | H3 | User Metadata | https://openriak.github.io/riak/ObjectAPI.html#user-metadata | exact | reference/data/object-metadata.md | reference/data/object-metadata.md |
| Riak KV - Object API | H3 | Object Metadata | https://openriak.github.io/riak/ObjectAPI.html#object-metadata | exact | reference/data/object-metadata.md | reference/data/object-metadata.md |
| Riak KV - Object API | H3 | Index Entries | https://openriak.github.io/riak/ObjectAPI.html#index-entries | exact | reference/data/secondary-indexes.md | reference/data/secondary-indexes.md |
| Riak KV - Object API | H2 | GET and PUT Options | https://openriak.github.io/riak/ObjectAPI.html#get-and-put-options | exact | reference/http-api/object-request-options.md | reference/http-api/object-request-options.md |
| Riak KV - Object API | H2 | Conditional Requests | https://openriak.github.io/riak/ObjectAPI.html#conditional-requests | exact | reference/http-api/conditional-requests.md<br>how-to/develop/send-conditional-object-request.md<br>explanation/consistency/conditional-requests.md | reference/http-api/conditional-requests.md<br>how-to/develop/send-conditional-object-request.md<br>explanation/consistency/conditional-requests.md |
| Riak KV - Object API | H3 | Use of Request Header - If-None-Match | https://openriak.github.io/riak/ObjectAPI.html#use-of-request-header---if-none-match | inherited-h2 | reference/http-api/conditional-requests.md<br>how-to/develop/send-conditional-object-request.md<br>explanation/consistency/conditional-requests.md | reference/http-api/conditional-requests.md<br>how-to/develop/send-conditional-object-request.md<br>explanation/consistency/conditional-requests.md |
| Riak KV - Object API | H3 | Use of Request Header - X-Riak-If-Not-Modified (non-standard Riak header) | https://openriak.github.io/riak/ObjectAPI.html#use-of-request-header---x-riak-if-not-modified-non-standard-riak-header | inherited-h2 | reference/http-api/conditional-requests.md<br>how-to/develop/send-conditional-object-request.md<br>explanation/consistency/conditional-requests.md | reference/http-api/conditional-requests.md<br>how-to/develop/send-conditional-object-request.md<br>explanation/consistency/conditional-requests.md |
| Riak KV - Object API | H3 | Conditional requests and latch objects | https://openriak.github.io/riak/ObjectAPI.html#conditional-requests-and-latch-objects | exact | explanation/data-model/latch-objects.md<br>reference/http-api/conditional-requests.md | explanation/data-model/latch-objects.md<br>reference/http-api/conditional-requests.md |
| Riak KV - Object API | H2 | Commit Hooks | https://openriak.github.io/riak/ObjectAPI.html#commit-hooks | exact | how-to/develop/write-commit-hook.md<br>reference/operations/custom-code.md | how-to/develop/write-commit-hook.md<br>reference/operations/custom-code.md |
| Riak KV - Object API | H2 | HTTP API Definition - Store | https://openriak.github.io/riak/ObjectAPI.html#http-api-definition---store | exact | reference/http-api/store-object.md<br>how-to/develop/create-object.md<br>how-to/develop/update-object.md | reference/http-api/store-object.md<br>how-to/develop/create-object.md<br>how-to/develop/update-object.md |
| Riak KV - Object API | H3 | Example PUT request | https://openriak.github.io/riak/ObjectAPI.html#example-put-request | exact | how-to/develop/create-object.md<br>how-to/develop/update-object.md | how-to/develop/create-object.md<br>how-to/develop/update-object.md |
| Riak KV - Object API | H2 | HTTP API Definition - Fetch | https://openriak.github.io/riak/ObjectAPI.html#http-api-definition---fetch | exact | reference/http-api/fetch-object.md<br>how-to/develop/read-object.md | reference/http-api/fetch-object.md<br>how-to/develop/read-object.md |
| Riak KV - Object API | H3 | Example GET request | https://openriak.github.io/riak/ObjectAPI.html#example-get-request | exact | how-to/develop/read-object.md | how-to/develop/read-object.md |
| Riak KV - Object API | H2 | HTTP API Definition - Delete | https://openriak.github.io/riak/ObjectAPI.html#http-api-definition---delete | exact | reference/http-api/delete-object.md<br>how-to/develop/delete-object.md | reference/http-api/delete-object.md<br>how-to/develop/delete-object.md |
| Riak KV - Object API | H3 | Example DELETE request | https://openriak.github.io/riak/ObjectAPI.html#example-delete-request | exact | how-to/develop/delete-object.md | how-to/develop/delete-object.md |
| Riak KV - Object API | H2 | Accessing Legacy Objects | https://openriak.github.io/riak/ObjectAPI.html#accessing-legacy-objects | exact | reference/http-api/fetch-object.md<br>explanation/data-model/merge-strategies.md | reference/http-api/fetch-object.md<br>explanation/data-model/merge-strategies.md |
| Riak KV - Object API | H2 | Performance and Efficiency | https://openriak.github.io/riak/ObjectAPI.html#performance-and-efficiency | exact | explanation/performance/latency-throughput-and-capacity.md<br>explanation/performance/storage-and-filesystem-effects.md | explanation/performance/latency-throughput-and-capacity.md<br>explanation/performance/storage-and-filesystem-effects.md |
| Riak KV - Object API | H3 | Notes on Implementation | https://openriak.github.io/riak/ObjectAPI.html#notes-on-implementation | inherited-h2 | explanation/performance/latency-throughput-and-capacity.md<br>explanation/performance/storage-and-filesystem-effects.md | explanation/performance/latency-throughput-and-capacity.md<br>explanation/performance/storage-and-filesystem-effects.md |
| Riak KV - Object API | H3 | Performance Expectations | https://openriak.github.io/riak/ObjectAPI.html#performance-expectations | inherited-h2 | explanation/performance/latency-throughput-and-capacity.md<br>explanation/performance/storage-and-filesystem-effects.md | explanation/performance/latency-throughput-and-capacity.md<br>explanation/performance/storage-and-filesystem-effects.md |
| Riak KV - Operations and Troubleshooting | H1 | Riak KV - Operations and Troubleshooting | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#riak-kv---operations-and-troubleshooting | exact | how-to/operate/index.md<br>how-to/troubleshoot/index.md | how-to/operate/index.md<br>how-to/troubleshoot/index.md |
| Riak KV - Operations and Troubleshooting | H2 | Replace, Repair and Recover | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#replace-repair-and-recover | exact | explanation/operations/node-failure-and-recovery.md<br>how-to/troubleshoot/recover-failed-node.md | explanation/operations/node-failure-and-recovery.md<br>how-to/troubleshoot/recover-failed-node.md |
| Riak KV - Operations and Troubleshooting | H3 | Proactive Replacement | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#proactive-replacement | exact | how-to/operate/rolling-replacement.md | how-to/operate/rolling-replacement.md |
| Riak KV - Operations and Troubleshooting | H3 | Reactive Replacement | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#reactive-replacement | exact | how-to/operate/replace-node.md<br>how-to/troubleshoot/recover-failed-node.md | how-to/operate/replace-node.md<br>how-to/troubleshoot/recover-failed-node.md |
| Riak KV - Operations and Troubleshooting | H4 | Administratively Downing a Node | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#administratively-downing-a-node | exact | how-to/operate/replace-node.md | how-to/operate/replace-node.md |
| Riak KV - Operations and Troubleshooting | H4 | Forcing a Replace | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#forcing-a-replace | exact | how-to/operate/replace-node.md | how-to/operate/replace-node.md |
| Riak KV - Operations and Troubleshooting | H4 | Completing a Repair | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#completing-a-repair | exact | how-to/troubleshoot/recover-failed-node.md<br>how-to/operate/repair-vnode.md | how-to/troubleshoot/recover-failed-node.md<br>how-to/operate/repair-vnode.md |
| Riak KV - Operations and Troubleshooting | H3 | Rolling Replacement | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#rolling-replacement | exact | how-to/operate/rolling-replacement.md | how-to/operate/rolling-replacement.md |
| Riak KV - Operations and Troubleshooting | H3 | Rolling restart | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#rolling-restart | exact | how-to/operate/rolling-restart.md | how-to/operate/rolling-restart.md |
| Riak KV - Operations and Troubleshooting | H3 | Repair an individual leveled store | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#repair-an-individual-leveled-store | exact | how-to/operate/repair-leveled-store.md | how-to/operate/repair-leveled-store.md |
| Riak KV - Operations and Troubleshooting | H3 | Repair an individual vnode | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#repair-an-individual-vnode | exact | how-to/operate/repair-vnode.md | how-to/operate/repair-vnode.md |
| Riak KV - Operations and Troubleshooting | H3 | Repair key ranges | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#repair-key-ranges | exact | how-to/operate/aae-fold/repair-key-range.md | how-to/operate/aae-fold/repair-key-range.md |
| Riak KV - Operations and Troubleshooting | H2 | Upgrading a node | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#upgrading-a-node | exact | how-to/operate/upgrade-cluster.md<br>explanation/operations/upgrade-and-downgrade.md | how-to/operate/upgrade-cluster.md<br>explanation/operations/upgrade-and-downgrade.md |
| Riak KV - Operations and Troubleshooting | H2 | Remote Console | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#remote-console | exact | how-to/operate/use-remote-console.md<br>reference/operations/remote-console.md | how-to/operate/use-remote-console.md<br>reference/operations/remote-console.md |
| Riak KV - Operations and Troubleshooting | H3 | Accessing objects | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#accessing-objects | exact | how-to/operate/inspect-data.md | how-to/operate/inspect-data.md |
| Riak KV - Operations and Troubleshooting | H3 | Running AAE Folds | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#running-aae-folds | exact | how-to/operate/aae-fold/run-from-command-line.md | how-to/operate/aae-fold/run-from-command-line.md |
| Riak KV - Operations and Troubleshooting | H3 | riak_client remote_console commands | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#riak_client-remote_console-commands | exact | reference/operations/remote-console.md | reference/operations/remote-console.md |
| Riak KV - Operations and Troubleshooting | H2 | Extending configuration | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#extending-configuration | exact | how-to/configure/advanced-configuration.md<br>how-to/configure/manage-configuration.md | how-to/configure/advanced-configuration.md<br>how-to/configure/manage-configuration.md |
| Riak KV - Operations and Troubleshooting | H3 | Using advanced.config | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#using-advancedconfig | exact | how-to/configure/advanced-configuration.md | how-to/configure/advanced-configuration.md |
| Riak KV - Operations and Troubleshooting | H3 | Setting environment variables at runtime | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#setting-environment-variables-at-runtime | exact | how-to/configure/runtime-environment-variables.md | how-to/configure/runtime-environment-variables.md |
| Riak KV - Operations and Troubleshooting | H3 | Accessing configuration | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#accessing-configuration | exact | how-to/configure/manage-configuration.md | how-to/configure/manage-configuration.md |
| Riak KV - Operations and Troubleshooting | H2 | Logging and Statistics | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#logging-and-statistics | exact | reference/operations/statistics-and-monitoring.md<br>reference/operations/log-files.md | reference/operations/statistics-and-monitoring.md<br>reference/operations/log-files.md |
| Riak KV - Operations and Troubleshooting | H3 | Logging | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#logging | exact | how-to/configure/logging.md<br>reference/operations/log-files.md | how-to/configure/logging.md<br>reference/operations/log-files.md |
| Riak KV - Operations and Troubleshooting | H3 | Riak Stats | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#riak-stats | exact | reference/operations/statistics-and-monitoring.md | reference/operations/statistics-and-monitoring.md |
| Riak KV - Operations and Troubleshooting | H3 | Vnode Status | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#vnode-status | exact | how-to/operate/check-vnode-status.md<br>reference/commands/vnode-status.md | how-to/operate/check-vnode-status.md<br>reference/commands/vnode-status.md |
| Riak KV - Operations and Troubleshooting | H2 | Monitoring Operational Services | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-operational-services | exact | reference/operations/statistics-and-monitoring.md | reference/operations/statistics-and-monitoring.md |
| Riak KV - Operations and Troubleshooting | H3 | Monitoring Anti-Entropy | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-anti-entropy | exact | how-to/operate/monitor-active-anti-entropy.md | how-to/operate/monitor-active-anti-entropy.md |
| Riak KV - Operations and Troubleshooting | H4 | Monitoring and Controlling AAE - Command Line | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-and-controlling-aae---command-line | exact | how-to/operate/monitor-active-anti-entropy.md<br>how-to/operate/rebuild-aae-trees.md | how-to/operate/monitor-active-anti-entropy.md<br>how-to/operate/rebuild-aae-trees.md |
| Riak KV - Operations and Troubleshooting | H4 | Monitoring AAE - Logs and Statistics | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-aae---logs-and-statistics | exact | how-to/operate/monitor-active-anti-entropy.md<br>reference/operations/statistics-and-monitoring.md | how-to/operate/monitor-active-anti-entropy.md<br>reference/operations/statistics-and-monitoring.md |
| Riak KV - Operations and Troubleshooting | H4 | Monitoring legacy AAE | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-legacy-aae | exact | explanation/replication/legacy-aae.md<br>how-to/operate/monitor-active-anti-entropy.md | explanation/replication/legacy-aae.md<br>how-to/operate/monitor-active-anti-entropy.md |
| Riak KV - Operations and Troubleshooting | H3 | Logging and monitoring of read repairs | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#logging-and-monitoring-of-read-repairs | exact | how-to/operate/monitor-read-repairs.md | how-to/operate/monitor-read-repairs.md |
| Riak KV - Operations and Troubleshooting | H3 | Monitoring inter-cluster reconciliation | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-inter-cluster-reconciliation | exact | how-to/operate/monitor-reconciliation.md | how-to/operate/monitor-reconciliation.md |
| Riak KV - Operations and Troubleshooting | H3 | Monitoring node worker pools | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-node-worker-pools | exact | how-to/operate/monitor-worker-pools.md | how-to/operate/monitor-worker-pools.md |
| Riak KV - Operations and Troubleshooting | H2 | Enabling Riak Security | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#enabling-riak-security | exact | how-to/secure/index.md<br>how-to/secure/enable-security.md | how-to/secure/index.md<br>how-to/secure/enable-security.md |
| Riak KV - Operations and Troubleshooting | H3 | TLS Enablement | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#tls-enablement | exact | how-to/secure/configure-tls.md | how-to/secure/configure-tls.md |
| Riak KV - Operations and Troubleshooting | H3 | Enabling Security and Restricting Source | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#enabling-security-and-restricting-source | exact | how-to/secure/enable-security.md<br>how-to/secure/manage-sources.md | how-to/secure/enable-security.md<br>how-to/secure/manage-sources.md |
| Riak KV - Operations and Troubleshooting | H3 | Granting permissions for specific actions | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#granting-permissions-for-specific-actions | exact | how-to/secure/manage-permissions.md | how-to/secure/manage-permissions.md |
| Riak KV - Operations and Troubleshooting | H2 | Garbage Collection - Reap, Erase and Scheduled Compaction | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#garbage-collection---reap-erase-and-scheduled-compaction | exact | explanation/operations/garbage-collection.md<br>how-to/operate/schedule-object-reaping.md | explanation/operations/garbage-collection.md<br>how-to/operate/schedule-object-reaping.md |
| Riak KV - Operations and Troubleshooting | H3 | Riak KV Eraser and Riak KV Reaper | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#riak-kv-eraser-and-riak-kv-reaper | exact | how-to/operate/schedule-object-reaping.md | how-to/operate/schedule-object-reaping.md |
| Riak KV - Operations and Troubleshooting | H3 | bitcask merge window | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#bitcask-merge-window | exact | how-to/configure/backends/bitcask-merge-window.md | how-to/configure/backends/bitcask-merge-window.md |
| Riak KV - Operations and Troubleshooting | H3 | leveled compaction high/low hour | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#leveled-compaction-highlow-hour | exact | how-to/configure/backends/leveled-compaction-window.md | how-to/configure/backends/leveled-compaction-window.md |
| Riak KV - Operations and Troubleshooting | H3 | Garbage collecting .bak files in leveled | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#garbage-collecting-bak-files-in-leveled | exact | how-to/operate/remove-leveled-backup-files.md | how-to/operate/remove-leveled-backup-files.md |
| Riak KV - Operations and Troubleshooting | H2 | Data inspection | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#data-inspection | exact | how-to/operate/inspect-data.md | how-to/operate/inspect-data.md |
| Riak KV - Operations and Troubleshooting | H2 | Volume and performance testing | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#volume-and-performance-testing | exact | how-to/tune/benchmark-cluster.md | how-to/tune/benchmark-cluster.md |
| Riak KV - Operations and Troubleshooting | H2 | Backup options | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#backup-options | exact | explanation/operations/backups-and-restores.md<br>how-to/operate/back-up-node.md | explanation/operations/backups-and-restores.md<br>how-to/operate/back-up-node.md |
| Riak KV - Operations and Troubleshooting | H3 | Backup - the preferred building block | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#backup---the-preferred-building-block | exact | how-to/operate/back-up-node.md | how-to/operate/back-up-node.md |
| Riak KV - Operations and Troubleshooting | H4 | Leveled - hot backups | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#leveled---hot-backups | exact | how-to/operate/back-up-node.md | how-to/operate/back-up-node.md |
| Riak KV - Operations and Troubleshooting | H4 | Leveled - restore a backup | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#leveled---restore-a-backup | exact | how-to/operate/restore-node.md | how-to/operate/restore-node.md |
| Riak KV - Operations and Troubleshooting | H4 | Bitcask - backups | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#bitcask---backups | exact | how-to/operate/back-up-node.md | how-to/operate/back-up-node.md |
| Riak KV - Operations and Troubleshooting | H4 | Backup - ring folder, and cluster metadata | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#backup---ring-folder-and-cluster-metadata | exact | how-to/operate/back-up-node.md<br>reference/specialized-apis/cluster-metadata.md | how-to/operate/back-up-node.md<br>reference/specialized-apis/cluster-metadata.md |
| Riak KV - Operations and Troubleshooting | H2 | Operation Checklist | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#operation-checklist | exact | how-to/operate/routine-operations-checklist.md | how-to/operate/routine-operations-checklist.md |
| Riak KV - Operations and Troubleshooting | H2 | Advanced - troubleshoot via the Erlang VM | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#advanced---troubleshoot-via-the-erlang-vm | exact | how-to/troubleshoot/erlang-vm.md | how-to/troubleshoot/erlang-vm.md |
| Riak KV - Operations and Troubleshooting | H3 | Recon | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#recon | inherited-h2 | how-to/troubleshoot/erlang-vm.md | how-to/troubleshoot/erlang-vm.md |
| Riak KV - Operations and Troubleshooting | H3 | Microstate accounting | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#microstate-accounting | inherited-h2 | how-to/troubleshoot/erlang-vm.md | how-to/troubleshoot/erlang-vm.md |
| Riak KV - Operations and Troubleshooting | H3 | Eprof | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#eprof | inherited-h2 | how-to/troubleshoot/erlang-vm.md | how-to/troubleshoot/erlang-vm.md |
| Riak KV - Operations and Troubleshooting | H3 | Tracing with dbg | https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#tracing-with-dbg | inherited-h2 | how-to/troubleshoot/erlang-vm.md | how-to/troubleshoot/erlang-vm.md |
| Riak KV - Other APIs | H1 | Riak KV - Other APIs | https://openriak.github.io/riak/OtherAPI.html#riak-kv---other-apis | exact | reference/specialized-apis/index.md<br>reference/aae-fold-api/index.md | reference/specialized-apis/index.md<br>reference/aae-fold-api/index.md |
| Riak KV - Other APIs | H2 | AAE Fold API | https://openriak.github.io/riak/OtherAPI.html#aae-fold-api | exact | reference/aae-fold-api/index.md<br>how-to/operate/aae-fold/index.md | reference/aae-fold-api/index.md<br>how-to/operate/aae-fold/index.md |
| Riak KV - Other APIs | H3 | Supported fold types | https://openriak.github.io/riak/OtherAPI.html#supported-fold-types | exact | reference/aae-fold-api/index.md | reference/aae-fold-api/index.md |
| Riak KV - Other APIs | H4 | merge_root_nval | https://openriak.github.io/riak/OtherAPI.html#merge_root_nval | inherited-h3 | reference/aae-fold-api/index.md | reference/aae-fold-api/index.md |
| Riak KV - Other APIs | H4 | merge_branch_nval | https://openriak.github.io/riak/OtherAPI.html#merge_branch_nval | inherited-h3 | reference/aae-fold-api/index.md | reference/aae-fold-api/index.md |
| Riak KV - Other APIs | H4 | fetch_clocks_nval | https://openriak.github.io/riak/OtherAPI.html#fetch_clocks_nval | inherited-h3 | reference/aae-fold-api/index.md | reference/aae-fold-api/index.md |
| Riak KV - Other APIs | H4 | merge_tree_range | https://openriak.github.io/riak/OtherAPI.html#merge_tree_range | inherited-h3 | reference/aae-fold-api/index.md | reference/aae-fold-api/index.md |
| Riak KV - Other APIs | H4 | fetch_clocks_range | https://openriak.github.io/riak/OtherAPI.html#fetch_clocks_range | inherited-h3 | reference/aae-fold-api/index.md | reference/aae-fold-api/index.md |
| Riak KV - Other APIs | H4 | repl_keys_range | https://openriak.github.io/riak/OtherAPI.html#repl_keys_range | exact | reference/aae-fold-api/index.md<br>reference/replication-api/index.md | reference/aae-fold-api/index.md<br>reference/replication-api/index.md |
| Riak KV - Other APIs | H4 | repair_keys_range | https://openriak.github.io/riak/OtherAPI.html#repair_keys_range | exact | reference/aae-fold-api/repair-key-range.md<br>how-to/operate/aae-fold/repair-key-range.md | reference/aae-fold-api/repair-key-range.md<br>how-to/operate/aae-fold/repair-key-range.md |
| Riak KV - Other APIs | H4 | find_keys | https://openriak.github.io/riak/OtherAPI.html#find_keys | exact | reference/aae-fold-api/find-keys.md<br>how-to/operate/aae-fold/find-keys.md | reference/aae-fold-api/find-keys.md<br>how-to/operate/aae-fold/find-keys.md |
| Riak KV - Other APIs | H4 | find_tombs | https://openriak.github.io/riak/OtherAPI.html#find_tombs | exact | reference/aae-fold-api/find-tombstones.md<br>how-to/operate/aae-fold/find-tombstones.md | reference/aae-fold-api/find-tombstones.md<br>how-to/operate/aae-fold/find-tombstones.md |
| Riak KV - Other APIs | H4 | erase_keys | https://openriak.github.io/riak/OtherAPI.html#erase_keys | exact | reference/aae-fold-api/erase-keys.md<br>how-to/operate/aae-fold/erase-keys.md | reference/aae-fold-api/erase-keys.md<br>how-to/operate/aae-fold/erase-keys.md |
| Riak KV - Other APIs | H4 | reap_tombs | https://openriak.github.io/riak/OtherAPI.html#reap_tombs | exact | reference/aae-fold-api/reap-tombstones.md<br>how-to/operate/aae-fold/reap-tombstones.md | reference/aae-fold-api/reap-tombstones.md<br>how-to/operate/aae-fold/reap-tombstones.md |
| Riak KV - Other APIs | H4 | object_stats | https://openriak.github.io/riak/OtherAPI.html#object_stats | exact | reference/aae-fold-api/object-statistics.md<br>how-to/operate/aae-fold/object-statistics.md | reference/aae-fold-api/object-statistics.md<br>how-to/operate/aae-fold/object-statistics.md |
| Riak KV - Other APIs | H4 | list_buckets | https://openriak.github.io/riak/OtherAPI.html#list_buckets | exact | reference/aae-fold-api/list-buckets.md<br>how-to/operate/aae-fold/list-buckets.md | reference/aae-fold-api/list-buckets.md<br>how-to/operate/aae-fold/list-buckets.md |
| Riak KV - Other APIs | H3 | Performance and Efficiency | https://openriak.github.io/riak/OtherAPI.html#performance-and-efficiency | exact | reference/aae-fold-api/index.md<br>explanation/performance/index.md | reference/aae-fold-api/index.md<br>explanation/performance/index.md |
| Riak KV - Other APIs | H4 | Node worker pools | https://openriak.github.io/riak/OtherAPI.html#node-worker-pools | exact | how-to/operate/monitor-worker-pools.md | how-to/operate/monitor-worker-pools.md |
| Riak KV - Other APIs | H4 | AAE Fold efficiency | https://openriak.github.io/riak/OtherAPI.html#aae-fold-efficiency | exact | reference/aae-fold-api/index.md<br>explanation/performance/index.md | reference/aae-fold-api/index.md<br>explanation/performance/index.md |
| Riak KV - Other APIs | H3 | AAE Folds via the Command Line | https://openriak.github.io/riak/OtherAPI.html#aae-folds-via-the-command-line | exact | how-to/operate/aae-fold/run-from-command-line.md<br>reference/commands/aae.md | how-to/operate/aae-fold/run-from-command-line.md<br>reference/commands/aae.md |
| Riak KV - Other APIs | H3 | AAE Folds via the Remote Console | https://openriak.github.io/riak/OtherAPI.html#aae-folds-via-the-remote-console | exact | how-to/operate/use-remote-console.md<br>reference/operations/remote-console.md | how-to/operate/use-remote-console.md<br>reference/operations/remote-console.md |
| Riak KV - Other APIs | H3 | AAE Folds via HTTP | https://openriak.github.io/riak/OtherAPI.html#aae-folds-via-http | exact | reference/aae-fold-api/index.md | reference/aae-fold-api/index.md |
| Riak KV - Other APIs | H3 | AAE Folds via PB | https://openriak.github.io/riak/OtherAPI.html#aae-folds-via-pb | exact | reference/aae-fold-api/index.md | reference/aae-fold-api/index.md |
| Riak KV - Other APIs | H2 | The Fetch API | https://openriak.github.io/riak/OtherAPI.html#the-fetch-api | exact | reference/specialized-apis/fetch-api.md | reference/specialized-apis/fetch-api.md |
| Riak KV - Other APIs | H2 | The Data Type API | https://openriak.github.io/riak/OtherAPI.html#the-data-type-api | exact | reference/specialized-apis/data-type-api.md<br>reference/data/distributed-data-types.md | reference/specialized-apis/data-type-api.md<br>reference/data/distributed-data-types.md |
| Riak KV - Other APIs | H2 | The Map/Reduce API | https://openriak.github.io/riak/OtherAPI.html#the-mapreduce-api | exact | reference/http-api/mapreduce.md<br>explanation/data-model/mapreduce.md | reference/http-api/mapreduce.md<br>explanation/data-model/mapreduce.md |
| Riak KV - Other APIs | H2 | The List API | https://openriak.github.io/riak/OtherAPI.html#the-list-api | exact | reference/specialized-apis/list-api.md | reference/specialized-apis/list-api.md |
| Riak KV - Other APIs | H2 | Legacy Query API | https://openriak.github.io/riak/OtherAPI.html#legacy-query-api | exact | reference/specialized-apis/legacy-query-api.md | reference/specialized-apis/legacy-query-api.md |
| Riak KV - Other APIs | H2 | Strong Consistency API | https://openriak.github.io/riak/OtherAPI.html#strong-consistency-api | exact | reference/specialized-apis/strong-consistency-api.md<br>explanation/consistency/strong-consistency.md | reference/specialized-apis/strong-consistency-api.md<br>explanation/consistency/strong-consistency.md |
| Riak KV - Other APIs | H2 | Write Once Path API | https://openriak.github.io/riak/OtherAPI.html#write-once-path-api | exact | reference/specialized-apis/write-once-api.md<br>how-to/develop/use-write-once-path.md | reference/specialized-apis/write-once-api.md<br>how-to/develop/use-write-once-path.md |
| Riak KV - Query API | H1 | Riak KV - Query API | https://openriak.github.io/riak/QueryAPI.html#riak-kv---query-api | exact | tutorials/query-api/index.md<br>reference/query-api/index.md<br>explanation/data-model/query-api.md | tutorials/query-api/index.md<br>reference/query-api/index.md<br>explanation/data-model/query-api.md |
| Riak KV - Query API | H2 | Secondary Indexes - Adding Index Entries to an Object | https://openriak.github.io/riak/QueryAPI.html#secondary-indexes---adding-index-entries-to-an-object | exact | reference/data/secondary-indexes.md<br>tutorials/query-api/build-search-index.md | reference/data/secondary-indexes.md<br>tutorials/query-api/build-search-index.md |
| Riak KV - Query API | H2 | Secondary Indexes - Querying Index Entries Overview | https://openriak.github.io/riak/QueryAPI.html#secondary-indexes---querying-index-entries-overview | exact | how-to/develop/query-with-query-api.md<br>reference/query-api/index.md | how-to/develop/query-with-query-api.md<br>reference/query-api/index.md |
| Riak KV - Query API | H3 | Querying - Functional Summary | https://openriak.github.io/riak/QueryAPI.html#querying---functional-summary | exact | explanation/data-model/query-api.md | explanation/data-model/query-api.md |
| Riak KV - Query API | H3 | Querying - Non-functional Summary | https://openriak.github.io/riak/QueryAPI.html#querying---non-functional-summary | exact | explanation/performance/query-execution.md | explanation/performance/query-execution.md |
| Riak KV - Query API | H2 | Example (1) - A Simple People Search Index | https://openriak.github.io/riak/QueryAPI.html#example-1---a-simple-people-search-index | exact | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| Riak KV - Query API | H3 | Example (1) - Simple Range Query | https://openriak.github.io/riak/QueryAPI.html#example-1---simple-range-query | inherited-h2 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| Riak KV - Query API | H3 | Example (1) - Finding an Exact Match | https://openriak.github.io/riak/QueryAPI.html#example-1---finding-an-exact-match | inherited-h2 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| Riak KV - Query API | H3 | Example (1) - Inexact Match | https://openriak.github.io/riak/QueryAPI.html#example-1---inexact-match | inherited-h2 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| Riak KV - Query API | H3 | Example (1) - Inexact Match of Given Name | https://openriak.github.io/riak/QueryAPI.html#example-1---inexact-match-of-given-name | inherited-h2 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| Riak KV - Query API | H3 | Example (1) - Wildcards within terms | https://openriak.github.io/riak/QueryAPI.html#example-1---wildcards-within-terms | inherited-h2 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| Riak KV - Query API | H3 | Example (1) - More Extensible Index Schema | https://openriak.github.io/riak/QueryAPI.html#example-1---more-extensible-index-schema | inherited-h2 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| Riak KV - Query API | H2 | Example (2) - An Alternative People Search | https://openriak.github.io/riak/QueryAPI.html#example-2---an-alternative-people-search | exact | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| Riak KV - Query API | H3 | Example (2) - Simple Variations and Limitations | https://openriak.github.io/riak/QueryAPI.html#example-2---simple-variations-and-limitations | inherited-h2 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| Riak KV - Query API | H2 | Example (3) - Reporting index | https://openriak.github.io/riak/QueryAPI.html#example-3---reporting-index | exact | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| Riak KV - Query API | H3 | Example (3) - Simple Variations and Limitations | https://openriak.github.io/riak/QueryAPI.html#example-3---simple-variations-and-limitations | inherited-h2 | tutorials/query-api/build-search-index.md | tutorials/query-api/build-search-index.md |
| Riak KV - Query API | H2 | Query - Definition | https://openriak.github.io/riak/QueryAPI.html#query---definition | exact | reference/query-api/request.md | reference/query-api/request.md |
| Riak KV - Query API | H3 | API Endpoint - THe URI | https://openriak.github.io/riak/QueryAPI.html#api-endpoint---the-uri | exact | reference/query-api/request.md | reference/query-api/request.md |
| Riak KV - Query API | H3 | Query JSON - Definition | https://openriak.github.io/riak/QueryAPI.html#query-json---definition | exact | reference/query-api/request.md | reference/query-api/request.md |
| Riak KV - Query API | H4 | aggregation_expression (optional) | https://openriak.github.io/riak/QueryAPI.html#aggregation_expression-optional | exact | reference/query-api/expressions.md | reference/query-api/expressions.md |
| Riak KV - Query API | H4 | accumulation_option (optional - default = keys) | https://openriak.github.io/riak/QueryAPI.html#accumulation_option-optional---default--keys | exact | reference/query-api/accumulation-options.md | reference/query-api/accumulation-options.md |
| Riak KV - Query API | H4 | accumulation_term (optional - default = $term) | https://openriak.github.io/riak/QueryAPI.html#accumulation_term-optional---default--term | exact | reference/query-api/accumulation-options.md | reference/query-api/accumulation-options.md |
| Riak KV - Query API | H4 | max_results (optional) | https://openriak.github.io/riak/QueryAPI.html#max_results-optional | inherited-h3 | reference/query-api/request.md | reference/query-api/request.md |
| Riak KV - Query API | H4 | continuation (optional) | https://openriak.github.io/riak/QueryAPI.html#continuation-optional | inherited-h3 | reference/query-api/request.md | reference/query-api/request.md |
| Riak KV - Query API | H4 | substitutions (optional) | https://openriak.github.io/riak/QueryAPI.html#substitutions-optional | inherited-h3 | reference/query-api/request.md | reference/query-api/request.md |
| Riak KV - Query API | H4 | timeout (optional) | https://openriak.github.io/riak/QueryAPI.html#timeout-optional | inherited-h3 | reference/query-api/request.md | reference/query-api/request.md |
| Riak KV - Query API | H4 | inactivity_timeout (optional) | https://openriak.github.io/riak/QueryAPI.html#inactivity_timeout-optional | inherited-h3 | reference/query-api/request.md | reference/query-api/request.md |
| Riak KV - Query API | H4 | query_list (required) | https://openriak.github.io/riak/QueryAPI.html#query_list-required | inherited-h3 | reference/query-api/request.md | reference/query-api/request.md |
| Riak KV - Query API | H3 | Query Json - Expressions | https://openriak.github.io/riak/QueryAPI.html#query-json---expressions | exact | reference/query-api/expressions.md | reference/query-api/expressions.md |
| Riak KV - Query API | H4 | Evaluation Expression - Definition | https://openriak.github.io/riak/QueryAPI.html#evaluation-expression---definition | exact | reference/query-api/expressions.md | reference/query-api/expressions.md |
| Riak KV - Query API | H4 | Filter Expression - Definition | https://openriak.github.io/riak/QueryAPI.html#filter-expression---definition | exact | reference/query-api/expressions.md | reference/query-api/expressions.md |
| Riak KV - Query API | H3 | Query Responses | https://openriak.github.io/riak/QueryAPI.html#query-responses | exact | reference/query-api/responses.md | reference/query-api/responses.md |
| Riak KV - Query API | H2 | Performance and Efficiency | https://openriak.github.io/riak/QueryAPI.html#performance-and-efficiency | exact | explanation/performance/query-execution.md<br>reference/query-api/limits.md | explanation/performance/query-execution.md<br>reference/query-api/limits.md |
| Riak KV - Query API | H3 | Setup and Distribute the Query | https://openriak.github.io/riak/QueryAPI.html#setup-and-distribute-the-query | inherited-h2 | explanation/performance/query-execution.md<br>reference/query-api/limits.md | explanation/performance/query-execution.md<br>reference/query-api/limits.md |
| Riak KV - Query API | H3 | Scanning | https://openriak.github.io/riak/QueryAPI.html#scanning | inherited-h2 | explanation/performance/query-execution.md<br>reference/query-api/limits.md | explanation/performance/query-execution.md<br>reference/query-api/limits.md |
| Riak KV - Query API | H3 | Filtering | https://openriak.github.io/riak/QueryAPI.html#filtering | inherited-h2 | explanation/performance/query-execution.md<br>reference/query-api/limits.md | explanation/performance/query-execution.md<br>reference/query-api/limits.md |
| Riak KV - Query API | H3 | Buffering | https://openriak.github.io/riak/QueryAPI.html#buffering | inherited-h2 | explanation/performance/query-execution.md<br>reference/query-api/limits.md | explanation/performance/query-execution.md<br>reference/query-api/limits.md |
| Riak KV - Query API | H3 | Aggregation of Combination Queries | https://openriak.github.io/riak/QueryAPI.html#aggregation-of-combination-queries | inherited-h2 | explanation/performance/query-execution.md<br>reference/query-api/limits.md | explanation/performance/query-execution.md<br>reference/query-api/limits.md |
| Riak KV - Query API | H3 | Central Collation of Query Results | https://openriak.github.io/riak/QueryAPI.html#central-collation-of-query-results | inherited-h2 | explanation/performance/query-execution.md<br>reference/query-api/limits.md | explanation/performance/query-execution.md<br>reference/query-api/limits.md |
| Riak KV - Query API | H3 | Transformation of Results | https://openriak.github.io/riak/QueryAPI.html#transformation-of-results | inherited-h2 | explanation/performance/query-execution.md<br>reference/query-api/limits.md | explanation/performance/query-execution.md<br>reference/query-api/limits.md |
| Riak KV - Query API | H2 | Notes on Implementation | https://openriak.github.io/riak/QueryAPI.html#notes-on-implementation | exact | explanation/data-model/query-api.md<br>reference/query-api/limits.md | explanation/data-model/query-api.md<br>reference/query-api/limits.md |
| Riak KV - Query API | H3 | Siblings | https://openriak.github.io/riak/QueryAPI.html#siblings | exact | explanation/data-model/version-vectors-and-siblings.md | explanation/data-model/version-vectors-and-siblings.md |
| Riak KV - Query API | H3 | Unicode support | https://openriak.github.io/riak/QueryAPI.html#unicode-support | exact | reference/query-api/expressions.md | reference/query-api/expressions.md |
| Riak KV - Query API | H3 | Consistency | https://openriak.github.io/riak/QueryAPI.html#consistency | exact | explanation/consistency/index.md | explanation/consistency/index.md |
| Riak KV - Query API | H3 | Further Improvements | https://openriak.github.io/riak/QueryAPI.html#further-improvements | exact | explanation/data-model/query-api.md | explanation/data-model/query-api.md |
| Riak KV - Replication and Reconciliation | H1 | Riak KV - Replication and Reconciliation | https://openriak.github.io/riak/ReplicationGuide.html#riak-kv---replication-and-reconciliation | exact | explanation/replication/index.md<br>how-to/configure/replication/index.md<br>reference/replication-api/index.md | explanation/replication/index.md<br>how-to/configure/replication/index.md<br>reference/replication-api/index.md |
| Riak KV - Replication and Reconciliation | H2 | Overview | https://openriak.github.io/riak/ReplicationGuide.html#overview | exact | explanation/replication/index.md | explanation/replication/index.md |
| Riak KV - Replication and Reconciliation | H3 | Concepts - Queues and Workers | https://openriak.github.io/riak/ReplicationGuide.html#concepts---queues-and-workers | exact | explanation/replication/queues.md<br>how-to/operate/monitor-worker-pools.md | explanation/replication/queues.md<br>how-to/operate/monitor-worker-pools.md |
| Riak KV - Replication and Reconciliation | H3 | Concepts - Replication References | https://openriak.github.io/riak/ReplicationGuide.html#concepts---replication-references | exact | explanation/replication/references-and-triggers.md | explanation/replication/references-and-triggers.md |
| Riak KV - Replication and Reconciliation | H3 | Concepts - Replication Triggers | https://openriak.github.io/riak/ReplicationGuide.html#concepts---replication-triggers | exact | explanation/replication/references-and-triggers.md | explanation/replication/references-and-triggers.md |
| Riak KV - Replication and Reconciliation | H2 | Configuration of Real-Time Replication | https://openriak.github.io/riak/ReplicationGuide.html#configuration-of-real-time-replication | exact | how-to/configure/replication/configure-real-time-replication.md | how-to/configure/replication/configure-real-time-replication.md |
| Riak KV - Replication and Reconciliation | H3 | Enable a Real-Time Source | https://openriak.github.io/riak/ReplicationGuide.html#enable-a-real-time-source | exact | how-to/configure/replication/configure-real-time-replication.md | how-to/configure/replication/configure-real-time-replication.md |
| Riak KV - Replication and Reconciliation | H3 | Enable a Real-Time Sink | https://openriak.github.io/riak/ReplicationGuide.html#enable-a-real-time-sink | exact | how-to/configure/replication/configure-real-time-replication.md<br>how-to/configure/replication/configure-sink-nodes.md | how-to/configure/replication/configure-real-time-replication.md<br>how-to/configure/replication/configure-sink-nodes.md |
| Riak KV - Replication and Reconciliation | H3 | Security Configuration | https://openriak.github.io/riak/ReplicationGuide.html#security-configuration | exact | how-to/configure/replication/secure-replication.md | how-to/configure/replication/secure-replication.md |
| Riak KV - Replication and Reconciliation | H3 | Additional Configuration | https://openriak.github.io/riak/ReplicationGuide.html#additional-configuration | exact | reference/configuration/replication.md | reference/configuration/replication.md |
| Riak KV - Replication and Reconciliation | H2 | Configuration of All-Cluster Reconciliation | https://openriak.github.io/riak/ReplicationGuide.html#configuration-of-all-cluster-reconciliation | exact | how-to/configure/replication/configure-fullsync.md<br>how-to/configure/replication/enable-tictac-aae.md | how-to/configure/replication/configure-fullsync.md<br>how-to/configure/replication/enable-tictac-aae.md |
| Riak KV - Replication and Reconciliation | H3 | Enable Tictac AAE | https://openriak.github.io/riak/ReplicationGuide.html#enable-tictac-aae | exact | how-to/configure/replication/enable-tictac-aae.md | how-to/configure/replication/enable-tictac-aae.md |
| Riak KV - Replication and Reconciliation | H3 | Initial Configuration | https://openriak.github.io/riak/ReplicationGuide.html#initial-configuration | exact | how-to/configure/replication/configure-fullsync.md | how-to/configure/replication/configure-fullsync.md |
| Riak KV - Replication and Reconciliation | H3 | Enabling Checks | https://openriak.github.io/riak/ReplicationGuide.html#enabling-checks | exact | how-to/configure/replication/configure-fullsync.md | how-to/configure/replication/configure-fullsync.md |
| Riak KV - Replication and Reconciliation | H3 | Tuning checks - the maximum results limit | https://openriak.github.io/riak/ReplicationGuide.html#tuning-checks---the-maximum-results-limit | exact | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| Riak KV - Replication and Reconciliation | H2 | Configuration of Per-Bucket Reconciliation | https://openriak.github.io/riak/ReplicationGuide.html#configuration-of-per-bucket-reconciliation | exact | how-to/configure/replication/per-bucket-reconciliation.md | how-to/configure/replication/per-bucket-reconciliation.md |
| Riak KV - Replication and Reconciliation | H2 | Migrating a cluster | https://openriak.github.io/riak/ReplicationGuide.html#migrating-a-cluster | exact | how-to/configure/replication/migrate-cluster.md | how-to/configure/replication/migrate-cluster.md |
| Riak KV - Replication and Reconciliation | H2 | Replication API | https://openriak.github.io/riak/ReplicationGuide.html#replication-api | exact | reference/replication-api/index.md | reference/replication-api/index.md |
| Riak KV - Replication and Reconciliation | H2 | Monitoring and Runtime Changes | https://openriak.github.io/riak/ReplicationGuide.html#monitoring-and-runtime-changes | exact | how-to/operate/monitor-reconciliation.md<br>reference/replication-api/runtime-controls.md | how-to/operate/monitor-reconciliation.md<br>reference/replication-api/runtime-controls.md |
| Riak KV - Replication and Reconciliation | H3 | Monitoring real-time replication via logs | https://openriak.github.io/riak/ReplicationGuide.html#monitoring-real-time-replication-via-logs | exact | how-to/operate/monitor-reconciliation.md | how-to/operate/monitor-reconciliation.md |
| Riak KV - Replication and Reconciliation | H3 | Making runtime changes to the Source | https://openriak.github.io/riak/ReplicationGuide.html#making-runtime-changes-to-the-source | exact | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| Riak KV - Replication and Reconciliation | H3 | Making runtime changes to the Sink | https://openriak.github.io/riak/ReplicationGuide.html#making-runtime-changes-to-the-sink | exact | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| Riak KV - Replication and Reconciliation | H3 | Monitoring reconciliation exchanges via logs | https://openriak.github.io/riak/ReplicationGuide.html#monitoring-reconciliation-exchanges-via-logs | exact | how-to/operate/monitor-reconciliation.md | how-to/operate/monitor-reconciliation.md |
| Riak KV - Replication and Reconciliation | H3 | Statistics available via Riak stats | https://openriak.github.io/riak/ReplicationGuide.html#statistics-available-via-riak-stats | exact | reference/operations/replication-statistics.md | reference/operations/replication-statistics.md |
| Riak KV - Replication and Reconciliation | H3 | Prompting a reconciliation check | https://openriak.github.io/riak/ReplicationGuide.html#prompting-a-reconciliation-check | exact | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| Riak KV - Replication and Reconciliation | H3 | Configure and monitor work queues | https://openriak.github.io/riak/ReplicationGuide.html#configure-and-monitor-work-queues | exact | how-to/operate/monitor-worker-pools.md<br>reference/replication-api/runtime-controls.md | how-to/operate/monitor-worker-pools.md<br>reference/replication-api/runtime-controls.md |
| Riak KV - Replication and Reconciliation | H3 | Update the request limits | https://openriak.github.io/riak/ReplicationGuide.html#update-the-request-limits | exact | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| Riak KV - Replication and Reconciliation | H3 | Overriding the range | https://openriak.github.io/riak/ReplicationGuide.html#overriding-the-range | exact | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| Riak KV - Replication and Reconciliation | H3 | Re-replicating keys for a given time period | https://openriak.github.io/riak/ReplicationGuide.html#re-replicating-keys-for-a-given-time-period | exact | how-to/operate/rereplicate-time-window.md | how-to/operate/rereplicate-time-window.md |
| Riak KV - Replication and Reconciliation | H3 | Re-Sync a Bucket | https://openriak.github.io/riak/ReplicationGuide.html#re-sync-a-bucket | exact | reference/replication-api/runtime-controls.md | how-to/operate/resync-bucket.md<br>reference/replication-api/runtime-controls.md |
| Riak KV - Replication and Reconciliation | H4 | Participate in Coverage | https://openriak.github.io/riak/ReplicationGuide.html#participate-in-coverage | inherited-h3 | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| Riak KV - Replication and Reconciliation | H4 | Suspend full-sync | https://openriak.github.io/riak/ReplicationGuide.html#suspend-full-sync | inherited-h3 | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| Riak KV - Replication and Reconciliation | H4 | Trigger Tree Repairs | https://openriak.github.io/riak/ReplicationGuide.html#trigger-tree-repairs | inherited-h3 | reference/replication-api/runtime-controls.md | reference/replication-api/runtime-controls.md |
| Riak KV - Replication and Reconciliation | H2 | Legacy Replication - riak_repl | https://openriak.github.io/riak/ReplicationGuide.html#legacy-replication---riak_repl | exact | explanation/replication/v2-and-v3-replication.md<br>how-to/configure/replication/configure-v2-multi-datacenter.md | explanation/replication/v2-and-v3-replication.md<br>how-to/configure/replication/configure-v2-multi-datacenter.md |
| Riak KV - Replication and Reconciliation | H2 | Replication scope | https://openriak.github.io/riak/ReplicationGuide.html#replication-scope | exact | explanation/replication/reconciliation-scope.md | explanation/replication/reconciliation-scope.md |
| Riak KV - Theory Guide | H1 | Riak KV - Theory Guide | https://openriak.github.io/riak/RiakTheoryGuide.html#riak-kv---theory-guide | exact | explanation/foundations/index.md | explanation/foundations/index.md |
| Riak KV - Theory Guide | H2 | The Ring - The distribution of vnodes | https://openriak.github.io/riak/RiakTheoryGuide.html#the-ring---the-distribution-of-vnodes | exact | explanation/foundations/clusters-rings-and-partitions.md<br>explanation/foundations/virtual-nodes.md | explanation/foundations/clusters-rings-and-partitions.md<br>explanation/foundations/virtual-nodes.md |
| Riak KV - Theory Guide | H2 | Eventual Consistency | https://openriak.github.io/riak/RiakTheoryGuide.html#eventual-consistency | exact | explanation/consistency/eventual-consistency.md | explanation/consistency/eventual-consistency.md |
| Riak KV - Theory Guide | H3 | Quorum on Read, Write and Query | https://openriak.github.io/riak/RiakTheoryGuide.html#quorum-on-read-write-and-query | exact | explanation/consistency/read-write-quorums.md | explanation/consistency/read-write-quorums.md |
| Riak KV - Theory Guide | H3 | Version vectors | https://openriak.github.io/riak/RiakTheoryGuide.html#version-vectors | exact | explanation/data-model/version-vectors-and-siblings.md | explanation/data-model/version-vectors-and-siblings.md |
| Riak KV - Theory Guide | H2 | Background processes | https://openriak.github.io/riak/RiakTheoryGuide.html#background-processes | exact | explanation/operations/index.md | explanation/operations/index.md |
| Riak KV - Theory Guide | H3 | Anti-Entropy | https://openriak.github.io/riak/RiakTheoryGuide.html#anti-entropy | exact | explanation/replication/active-anti-entropy.md<br>explanation/replication/tictac-aae.md | explanation/replication/active-anti-entropy.md<br>explanation/replication/tictac-aae.md |
| Riak KV - Theory Guide | H3 | Disk-backed Queues | https://openriak.github.io/riak/RiakTheoryGuide.html#disk-backed-queues | exact | explanation/replication/queues.md | explanation/replication/queues.md |
| Riak KV - Theory Guide | H3 | Riak Core cluster management | https://openriak.github.io/riak/RiakTheoryGuide.html#riak-core-cluster-management | exact | explanation/operations/ring-changes-and-handoffs.md | explanation/operations/ring-changes-and-handoffs.md |
| Riak KV - Theory Guide | H2 | Backend Design | https://openriak.github.io/riak/RiakTheoryGuide.html#backend-design | exact | explanation/storage/index.md<br>explanation/storage/choosing-backend.md | explanation/storage/index.md<br>explanation/storage/choosing-backend.md |
| Riak KV - Theory Guide | H3 | The bitcask backend | https://openriak.github.io/riak/RiakTheoryGuide.html#the-bitcask-backend | exact | explanation/storage/bitcask.md | explanation/storage/bitcask.md |
| Riak KV - Theory Guide | H3 | The leveled backend | https://openriak.github.io/riak/RiakTheoryGuide.html#the-leveled-backend | exact | explanation/storage/leveled.md | explanation/storage/leveled.md |
| Riak KV - Theory Guide | H4 | Caching and Acceleration | https://openriak.github.io/riak/RiakTheoryGuide.html#caching-and-acceleration | inherited-h3 | explanation/storage/leveled.md | explanation/storage/leveled.md |
| Riak KV - Theory Guide | H4 | File Formats | https://openriak.github.io/riak/RiakTheoryGuide.html#file-formats | inherited-h3 | explanation/storage/leveled.md | explanation/storage/leveled.md |
| Riak KV - Theory Guide | H4 | Data safety and security | https://openriak.github.io/riak/RiakTheoryGuide.html#data-safety-and-security | inherited-h3 | explanation/storage/leveled.md | explanation/storage/leveled.md |
| Riak KV - Theory Guide | H4 | Compaction | https://openriak.github.io/riak/RiakTheoryGuide.html#compaction | inherited-h3 | explanation/storage/leveled.md | explanation/storage/leveled.md |
| Riak KV - Theory Guide | H4 | Head-only Mode | https://openriak.github.io/riak/RiakTheoryGuide.html#head-only-mode | inherited-h3 | explanation/storage/leveled.md | explanation/storage/leveled.md |

## Complete destination ledger

| Version | Destination | Type | Status | Draft | Created by audit | QuickDocs sections |
|---|---|---|---|---|---|---:|
| 3.4.0 | explanation/consistency/conditional-requests.md | explanation | stub | True | False | 3 |
| 3.4.0 | explanation/consistency/eventual-consistency.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.0 | explanation/consistency/index.md | explanation | stub | True | False | 1 |
| 3.4.0 | explanation/consistency/read-write-quorums.md | explanation | stub | True | False | 1 |
| 3.4.0 | explanation/consistency/strong-consistency.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.0 | explanation/data-model/deletion-policies.md | explanation | stub | True | False | 1 |
| 3.4.0 | explanation/data-model/keys-objects-and-buckets.md | explanation | migrated-needs-review | True | False | 2 |
| 3.4.0 | explanation/data-model/latch-objects.md | explanation | stub | True | False | 1 |
| 3.4.0 | explanation/data-model/mapreduce.md | explanation | stub | True | False | 1 |
| 3.4.0 | explanation/data-model/merge-strategies.md | explanation | stub | True | False | 1 |
| 3.4.0 | explanation/data-model/query-api.md | explanation | stub | True | False | 4 |
| 3.4.0 | explanation/data-model/version-vectors-and-siblings.md | explanation | stub | True | False | 3 |
| 3.4.0 | explanation/foundations/clusters-rings-and-partitions.md | explanation | migrated-needs-review | True | False | 2 |
| 3.4.0 | explanation/foundations/history.md | explanation | stub | True | True | 1 |
| 3.4.0 | explanation/foundations/index.md | explanation | migrated-needs-review | True | False | 2 |
| 3.4.0 | explanation/foundations/intra-cluster-resilience.md | explanation | stub | True | False | 1 |
| 3.4.0 | explanation/foundations/use-cases.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.0 | explanation/foundations/virtual-nodes.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.0 | explanation/foundations/why-openriak.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.0 | explanation/operations/backups-and-restores.md | explanation | stub | True | False | 1 |
| 3.4.0 | explanation/operations/garbage-collection.md | explanation | stub | True | False | 1 |
| 3.4.0 | explanation/operations/index.md | explanation | stub | True | False | 1 |
| 3.4.0 | explanation/operations/node-failure-and-recovery.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.0 | explanation/operations/ring-changes-and-handoffs.md | explanation | stub | True | False | 1 |
| 3.4.0 | explanation/operations/upgrade-and-downgrade.md | explanation | stub | True | False | 1 |
| 3.4.0 | explanation/performance/index.md | explanation | stub | True | False | 2 |
| 3.4.0 | explanation/performance/latency-throughput-and-capacity.md | explanation | stub | True | False | 3 |
| 3.4.0 | explanation/performance/query-execution.md | explanation | stub | True | False | 9 |
| 3.4.0 | explanation/performance/storage-and-filesystem-effects.md | explanation | stub | True | False | 3 |
| 3.4.0 | explanation/replication/active-anti-entropy.md | explanation | migrated-needs-review | True | False | 2 |
| 3.4.0 | explanation/replication/index.md | explanation | migrated-needs-review | True | False | 2 |
| 3.4.0 | explanation/replication/legacy-aae.md | explanation | stub | True | False | 1 |
| 3.4.0 | explanation/replication/multi-datacenter-architecture.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.0 | explanation/replication/queues.md | explanation | stub | True | False | 2 |
| 3.4.0 | explanation/replication/reconciliation-scope.md | explanation | stub | True | False | 1 |
| 3.4.0 | explanation/replication/references-and-triggers.md | explanation | migrated-needs-review | True | False | 2 |
| 3.4.0 | explanation/replication/tictac-aae.md | explanation | stub | True | False | 1 |
| 3.4.0 | explanation/replication/v2-and-v3-replication.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.0 | explanation/storage/bitcask.md | explanation | migrated-needs-review | True | False | 2 |
| 3.4.0 | explanation/storage/choosing-backend.md | explanation | migrated-needs-review | True | False | 2 |
| 3.4.0 | explanation/storage/index.md | explanation | stub | True | False | 1 |
| 3.4.0 | explanation/storage/leveldb.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.0 | explanation/storage/leveled.md | explanation | migrated-needs-review | True | False | 7 |
| 3.4.0 | explanation/storage/memory.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.0 | explanation/storage/multi-backend.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/configure/advanced-configuration.md | how-to | stub | True | False | 2 |
| 3.4.0 | how-to/configure/api-listeners.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/configure/backends/bitcask-merge-window.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/configure/backends/bitcask.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.0 | how-to/configure/backends/change-backend.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/configure/backends/index.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/configure/backends/leveldb.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/configure/backends/leveled-compaction-window.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/configure/backends/leveled.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.0 | how-to/configure/backends/memory.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/configure/backends/multi.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/configure/basic-node-settings.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/configure/global-object-expiration.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/configure/load-balancing-proxy.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/configure/logging.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/configure/manage-configuration.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.0 | how-to/configure/replication/configure-fullsync.md | how-to | migrated-needs-review | True | False | 3 |
| 3.4.0 | how-to/configure/replication/configure-real-time-replication.md | how-to | migrated-needs-review | True | False | 3 |
| 3.4.0 | how-to/configure/replication/configure-sink-nodes.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/configure/replication/configure-v2-multi-datacenter.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/configure/replication/enable-tictac-aae.md | how-to | migrated-needs-review | True | False | 4 |
| 3.4.0 | how-to/configure/replication/exclude-bucket-from-aae.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/configure/replication/index.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/configure/replication/migrate-cluster.md | how-to | stub | True | False | 3 |
| 3.4.0 | how-to/configure/replication/per-bucket-reconciliation.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/configure/replication/secure-replication.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/configure/runtime-environment-variables.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/configure/verify-configuration.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/develop/create-object.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.0 | how-to/develop/delete-object.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.0 | how-to/develop/index.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/develop/query-with-query-api.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/develop/read-object.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.0 | how-to/develop/send-conditional-object-request.md | how-to | stub | True | False | 3 |
| 3.4.0 | how-to/develop/update-object.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.0 | how-to/develop/use-write-once-path.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/develop/write-commit-hook.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/install/index.md | how-to | migrated-needs-review | True | False | 3 |
| 3.4.0 | how-to/install/source.md | how-to | migrated-needs-review | True | False | 6 |
| 3.4.0 | how-to/install/verify-installation.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.0 | how-to/operate/aae-fold/erase-keys.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/operate/aae-fold/find-keys.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/operate/aae-fold/find-tombstones.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/operate/aae-fold/index.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/operate/aae-fold/list-buckets.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/operate/aae-fold/object-statistics.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/operate/aae-fold/reap-tombstones.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/operate/aae-fold/repair-key-range.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.0 | how-to/operate/aae-fold/run-from-command-line.md | how-to | stub | True | False | 2 |
| 3.4.0 | how-to/operate/add-node.md | how-to | stub | True | False | 2 |
| 3.4.0 | how-to/operate/back-up-node.md | how-to | migrated-needs-review | True | False | 5 |
| 3.4.0 | how-to/operate/check-vnode-status.md | how-to | stub | True | True | 1 |
| 3.4.0 | how-to/operate/index.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.0 | how-to/operate/inspect-data.md | how-to | stub | True | False | 2 |
| 3.4.0 | how-to/operate/manage-bucket-types.md | how-to | migrated-needs-review | True | False | 11 |
| 3.4.0 | how-to/operate/manage-handoffs.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/operate/monitor-active-anti-entropy.md | how-to | migrated-needs-review | True | False | 4 |
| 3.4.0 | how-to/operate/monitor-read-repairs.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/operate/monitor-reconciliation.md | how-to | stub | True | False | 4 |
| 3.4.0 | how-to/operate/monitor-worker-pools.md | how-to | stub | True | False | 4 |
| 3.4.0 | how-to/operate/plan-and-commit-cluster-change.md | how-to | stub | True | False | 4 |
| 3.4.0 | how-to/operate/rebuild-aae-trees.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/operate/remove-leveled-backup-files.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/operate/remove-node.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/operate/repair-leveled-store.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/operate/repair-vnode.md | how-to | stub | True | False | 2 |
| 3.4.0 | how-to/operate/replace-node.md | how-to | migrated-needs-review | True | False | 3 |
| 3.4.0 | how-to/operate/rereplicate-time-window.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/operate/restore-node.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/operate/rolling-replacement.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.0 | how-to/operate/rolling-restart.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/operate/routine-operations-checklist.md | how-to | stub | True | True | 1 |
| 3.4.0 | how-to/operate/schedule-object-reaping.md | how-to | stub | True | False | 3 |
| 3.4.0 | how-to/operate/start-stop-restart-node.md | how-to | stub | True | False | 4 |
| 3.4.0 | how-to/operate/upgrade-cluster.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/operate/use-remote-console.md | how-to | stub | True | False | 2 |
| 3.4.0 | how-to/plan/choose-deletion-policy.md | how-to | stub | True | False | 3 |
| 3.4.0 | how-to/plan/choose-intra-cluster-resilience.md | how-to | stub | True | False | 4 |
| 3.4.0 | how-to/plan/choose-multi-cluster-topology.md | how-to | stub | True | True | 2 |
| 3.4.0 | how-to/plan/choose-ring-size.md | how-to | stub | True | True | 2 |
| 3.4.0 | how-to/plan/choose-storage-backend.md | how-to | stub | True | True | 2 |
| 3.4.0 | how-to/plan/index.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.0 | how-to/plan/map-data-to-objects.md | how-to | migrated-needs-review | True | False | 3 |
| 3.4.0 | how-to/plan/production-readiness-checklist.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/plan/size-cluster.md | how-to | migrated | False | False | 2 |
| 3.4.0 | how-to/secure/configure-tls.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/secure/enable-security.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.0 | how-to/secure/index.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/secure/manage-permissions.md | how-to | stub | True | False | 1 |
| 3.4.0 | how-to/secure/manage-sources.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/secure/secure-networking.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/troubleshoot/erlang-vm.md | how-to | stub | True | False | 5 |
| 3.4.0 | how-to/troubleshoot/index.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/troubleshoot/recover-failed-node.md | how-to | migrated-needs-review | True | False | 3 |
| 3.4.0 | how-to/tune/benchmark-cluster.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | how-to/tune/set-open-files-limit.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.0 | index.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.0 | reference/aae-fold-api/erase-keys.md | reference | stub | True | False | 1 |
| 3.4.0 | reference/aae-fold-api/find-keys.md | reference | stub | True | False | 1 |
| 3.4.0 | reference/aae-fold-api/find-tombstones.md | reference | stub | True | False | 1 |
| 3.4.0 | reference/aae-fold-api/index.md | reference | migrated-needs-review | True | False | 13 |
| 3.4.0 | reference/aae-fold-api/list-buckets.md | reference | stub | True | False | 1 |
| 3.4.0 | reference/aae-fold-api/object-statistics.md | reference | stub | True | False | 1 |
| 3.4.0 | reference/aae-fold-api/reap-tombstones.md | reference | stub | True | False | 1 |
| 3.4.0 | reference/aae-fold-api/repair-key-range.md | reference | stub | True | False | 1 |
| 3.4.0 | reference/commands/aae.md | reference | stub | True | False | 1 |
| 3.4.0 | reference/commands/vnode-status.md | reference | stub | True | True | 1 |
| 3.4.0 | reference/configuration/bucket-properties.md | reference | stub | True | True | 14 |
| 3.4.0 | reference/configuration/networking.md | reference | migrated | False | False | 1 |
| 3.4.0 | reference/configuration/replication.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.0 | reference/data/content-types.md | reference | stub | True | False | 1 |
| 3.4.0 | reference/data/distributed-data-types.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.0 | reference/data/index.md | reference | stub | True | False | 1 |
| 3.4.0 | reference/data/keys-and-objects.md | reference | stub | True | False | 2 |
| 3.4.0 | reference/data/object-metadata.md | reference | stub | True | False | 3 |
| 3.4.0 | reference/data/secondary-indexes.md | reference | migrated-needs-review | True | False | 2 |
| 3.4.0 | reference/data/version-vectors.md | reference | stub | True | False | 1 |
| 3.4.0 | reference/http-api/conditional-requests.md | reference | stub | True | False | 4 |
| 3.4.0 | reference/http-api/delete-object.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.0 | reference/http-api/fetch-object.md | reference | migrated-needs-review | True | False | 2 |
| 3.4.0 | reference/http-api/index.md | reference | migrated-needs-review | True | False | 2 |
| 3.4.0 | reference/http-api/mapreduce.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.0 | reference/http-api/object-request-options.md | reference | stub | True | True | 1 |
| 3.4.0 | reference/http-api/store-object.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.0 | reference/operations/cluster-claim-algorithms.md | reference | stub | True | True | 3 |
| 3.4.0 | reference/operations/custom-code.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.0 | reference/operations/log-files.md | reference | migrated-needs-review | True | False | 2 |
| 3.4.0 | reference/operations/object-deletion.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.0 | reference/operations/remote-console.md | reference | migrated-needs-review | True | False | 3 |
| 3.4.0 | reference/operations/replication-statistics.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.0 | reference/operations/statistics-and-monitoring.md | reference | migrated-needs-review | True | False | 4 |
| 3.4.0 | reference/query-api/accumulation-options.md | reference | stub | True | False | 2 |
| 3.4.0 | reference/query-api/expressions.md | reference | stub | True | False | 5 |
| 3.4.0 | reference/query-api/index.md | reference | stub | True | False | 2 |
| 3.4.0 | reference/query-api/limits.md | reference | stub | True | False | 9 |
| 3.4.0 | reference/query-api/request.md | reference | stub | True | False | 9 |
| 3.4.0 | reference/query-api/responses.md | reference | stub | True | False | 1 |
| 3.4.0 | reference/releases/downloads.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.0 | reference/releases/supported-platforms.md | reference | migrated-needs-review | True | False | 2 |
| 3.4.0 | reference/replication-api/index.md | reference | stub | True | False | 3 |
| 3.4.0 | reference/replication-api/runtime-controls.md | reference | migrated-needs-review | True | False | 12 |
| 3.4.0 | reference/specialized-apis/cluster-metadata.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.0 | reference/specialized-apis/data-type-api.md | reference | stub | True | True | 1 |
| 3.4.0 | reference/specialized-apis/fetch-api.md | reference | stub | True | False | 1 |
| 3.4.0 | reference/specialized-apis/index.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.0 | reference/specialized-apis/legacy-query-api.md | reference | stub | True | False | 1 |
| 3.4.0 | reference/specialized-apis/list-api.md | reference | stub | True | False | 1 |
| 3.4.0 | reference/specialized-apis/strong-consistency-api.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.0 | reference/specialized-apis/write-once-api.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.0 | tutorials/first-cluster/index.md | tutorial | migrated-needs-review | True | False | 1 |
| 3.4.0 | tutorials/query-api/build-search-index.md | tutorial | stub | True | False | 12 |
| 3.4.0 | tutorials/query-api/index.md | tutorial | stub | True | False | 1 |
| 3.4.1 | explanation/consistency/conditional-requests.md | explanation | stub | True | False | 3 |
| 3.4.1 | explanation/consistency/eventual-consistency.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.1 | explanation/consistency/index.md | explanation | stub | True | False | 1 |
| 3.4.1 | explanation/consistency/read-write-quorums.md | explanation | stub | True | False | 1 |
| 3.4.1 | explanation/consistency/strong-consistency.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.1 | explanation/data-model/deletion-policies.md | explanation | stub | True | False | 1 |
| 3.4.1 | explanation/data-model/keys-objects-and-buckets.md | explanation | migrated-needs-review | True | False | 2 |
| 3.4.1 | explanation/data-model/latch-objects.md | explanation | stub | True | False | 1 |
| 3.4.1 | explanation/data-model/mapreduce.md | explanation | stub | True | False | 1 |
| 3.4.1 | explanation/data-model/merge-strategies.md | explanation | stub | True | False | 1 |
| 3.4.1 | explanation/data-model/query-api.md | explanation | stub | True | False | 4 |
| 3.4.1 | explanation/data-model/version-vectors-and-siblings.md | explanation | stub | True | False | 3 |
| 3.4.1 | explanation/foundations/clusters-rings-and-partitions.md | explanation | migrated-needs-review | True | False | 2 |
| 3.4.1 | explanation/foundations/history.md | explanation | stub | True | True | 1 |
| 3.4.1 | explanation/foundations/index.md | explanation | migrated-needs-review | True | False | 2 |
| 3.4.1 | explanation/foundations/intra-cluster-resilience.md | explanation | stub | True | False | 1 |
| 3.4.1 | explanation/foundations/use-cases.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.1 | explanation/foundations/virtual-nodes.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.1 | explanation/foundations/why-openriak.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.1 | explanation/operations/backups-and-restores.md | explanation | stub | True | False | 1 |
| 3.4.1 | explanation/operations/garbage-collection.md | explanation | stub | True | False | 1 |
| 3.4.1 | explanation/operations/index.md | explanation | stub | True | False | 1 |
| 3.4.1 | explanation/operations/node-failure-and-recovery.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.1 | explanation/operations/ring-changes-and-handoffs.md | explanation | stub | True | False | 1 |
| 3.4.1 | explanation/operations/upgrade-and-downgrade.md | explanation | stub | True | False | 1 |
| 3.4.1 | explanation/performance/index.md | explanation | stub | True | False | 2 |
| 3.4.1 | explanation/performance/latency-throughput-and-capacity.md | explanation | stub | True | False | 3 |
| 3.4.1 | explanation/performance/query-execution.md | explanation | stub | True | False | 9 |
| 3.4.1 | explanation/performance/storage-and-filesystem-effects.md | explanation | stub | True | False | 3 |
| 3.4.1 | explanation/replication/active-anti-entropy.md | explanation | migrated-needs-review | True | False | 2 |
| 3.4.1 | explanation/replication/index.md | explanation | migrated-needs-review | True | False | 2 |
| 3.4.1 | explanation/replication/legacy-aae.md | explanation | stub | True | False | 1 |
| 3.4.1 | explanation/replication/multi-datacenter-architecture.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.1 | explanation/replication/queues.md | explanation | stub | True | False | 2 |
| 3.4.1 | explanation/replication/reconciliation-scope.md | explanation | stub | True | False | 1 |
| 3.4.1 | explanation/replication/references-and-triggers.md | explanation | migrated-needs-review | True | False | 2 |
| 3.4.1 | explanation/replication/tictac-aae.md | explanation | stub | True | False | 1 |
| 3.4.1 | explanation/replication/v2-and-v3-replication.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.1 | explanation/storage/bitcask.md | explanation | migrated-needs-review | True | False | 2 |
| 3.4.1 | explanation/storage/choosing-backend.md | explanation | migrated-needs-review | True | False | 2 |
| 3.4.1 | explanation/storage/index.md | explanation | stub | True | False | 1 |
| 3.4.1 | explanation/storage/leveldb.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.1 | explanation/storage/leveled.md | explanation | migrated-needs-review | True | False | 7 |
| 3.4.1 | explanation/storage/memory.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.1 | explanation/storage/multi-backend.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/configure/advanced-configuration.md | how-to | stub | True | False | 2 |
| 3.4.1 | how-to/configure/api-listeners.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/configure/backends/bitcask-merge-window.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/configure/backends/bitcask.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.1 | how-to/configure/backends/change-backend.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/configure/backends/index.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/configure/backends/leveldb.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/configure/backends/leveled-compaction-window.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/configure/backends/leveled.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.1 | how-to/configure/backends/memory.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/configure/backends/multi.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/configure/basic-node-settings.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/configure/global-object-expiration.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/configure/load-balancing-proxy.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/configure/logging.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/configure/manage-configuration.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.1 | how-to/configure/replication/configure-fullsync.md | how-to | migrated-needs-review | True | False | 3 |
| 3.4.1 | how-to/configure/replication/configure-real-time-replication.md | how-to | migrated-needs-review | True | False | 3 |
| 3.4.1 | how-to/configure/replication/configure-sink-nodes.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/configure/replication/configure-v2-multi-datacenter.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/configure/replication/enable-tictac-aae.md | how-to | migrated-needs-review | True | False | 4 |
| 3.4.1 | how-to/configure/replication/exclude-bucket-from-aae.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/configure/replication/index.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/configure/replication/migrate-cluster.md | how-to | stub | True | False | 3 |
| 3.4.1 | how-to/configure/replication/per-bucket-reconciliation.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/configure/replication/secure-replication.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/configure/runtime-environment-variables.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/configure/verify-configuration.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/develop/create-object.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.1 | how-to/develop/delete-object.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.1 | how-to/develop/index.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/develop/query-with-query-api.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/develop/read-object.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.1 | how-to/develop/send-conditional-object-request.md | how-to | stub | True | False | 3 |
| 3.4.1 | how-to/develop/update-object.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.1 | how-to/develop/use-write-once-path.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/develop/write-commit-hook.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/install/index.md | how-to | migrated-needs-review | True | False | 3 |
| 3.4.1 | how-to/install/source.md | how-to | migrated-needs-review | True | False | 6 |
| 3.4.1 | how-to/install/verify-installation.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.1 | how-to/operate/aae-fold/erase-keys.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/operate/aae-fold/find-keys.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/operate/aae-fold/find-tombstones.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/operate/aae-fold/index.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/operate/aae-fold/list-buckets.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/operate/aae-fold/object-statistics.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/operate/aae-fold/reap-tombstones.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/operate/aae-fold/repair-key-range.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.1 | how-to/operate/aae-fold/run-from-command-line.md | how-to | stub | True | False | 2 |
| 3.4.1 | how-to/operate/add-node.md | how-to | stub | True | False | 2 |
| 3.4.1 | how-to/operate/back-up-node.md | how-to | migrated-needs-review | True | False | 5 |
| 3.4.1 | how-to/operate/check-vnode-status.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/operate/index.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.1 | how-to/operate/inspect-data.md | how-to | stub | True | False | 2 |
| 3.4.1 | how-to/operate/manage-bucket-types.md | how-to | migrated-needs-review | True | False | 11 |
| 3.4.1 | how-to/operate/manage-handoffs.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/operate/monitor-active-anti-entropy.md | how-to | migrated-needs-review | True | False | 4 |
| 3.4.1 | how-to/operate/monitor-read-repairs.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/operate/monitor-reconciliation.md | how-to | stub | True | False | 4 |
| 3.4.1 | how-to/operate/monitor-worker-pools.md | how-to | stub | True | False | 4 |
| 3.4.1 | how-to/operate/plan-and-commit-cluster-change.md | how-to | stub | True | False | 4 |
| 3.4.1 | how-to/operate/rebuild-aae-trees.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/operate/remove-leveled-backup-files.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/operate/remove-node.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/operate/repair-leveled-store.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/operate/repair-vnode.md | how-to | stub | True | False | 2 |
| 3.4.1 | how-to/operate/replace-node.md | how-to | migrated-needs-review | True | False | 3 |
| 3.4.1 | how-to/operate/rereplicate-time-window.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/operate/restore-node.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/operate/resync-bucket.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/operate/rolling-replacement.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.1 | how-to/operate/rolling-restart.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/operate/routine-operations-checklist.md | how-to | stub | True | True | 1 |
| 3.4.1 | how-to/operate/schedule-object-reaping.md | how-to | stub | True | False | 3 |
| 3.4.1 | how-to/operate/start-stop-restart-node.md | how-to | stub | True | False | 4 |
| 3.4.1 | how-to/operate/upgrade-cluster.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/operate/use-remote-console.md | how-to | stub | True | False | 2 |
| 3.4.1 | how-to/plan/choose-deletion-policy.md | how-to | stub | True | False | 3 |
| 3.4.1 | how-to/plan/choose-intra-cluster-resilience.md | how-to | stub | True | False | 4 |
| 3.4.1 | how-to/plan/choose-multi-cluster-topology.md | how-to | stub | True | True | 2 |
| 3.4.1 | how-to/plan/choose-ring-size.md | how-to | stub | True | True | 2 |
| 3.4.1 | how-to/plan/choose-storage-backend.md | how-to | stub | True | True | 2 |
| 3.4.1 | how-to/plan/index.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.1 | how-to/plan/map-data-to-objects.md | how-to | migrated-needs-review | True | False | 3 |
| 3.4.1 | how-to/plan/production-readiness-checklist.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/plan/size-cluster.md | how-to | migrated | False | False | 2 |
| 3.4.1 | how-to/secure/configure-tls.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/secure/enable-security.md | how-to | migrated-needs-review | True | False | 2 |
| 3.4.1 | how-to/secure/index.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/secure/manage-permissions.md | how-to | stub | True | False | 1 |
| 3.4.1 | how-to/secure/manage-sources.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/secure/secure-networking.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/troubleshoot/erlang-vm.md | how-to | stub | True | False | 5 |
| 3.4.1 | how-to/troubleshoot/index.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/troubleshoot/recover-failed-node.md | how-to | migrated-needs-review | True | False | 3 |
| 3.4.1 | how-to/tune/benchmark-cluster.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | how-to/tune/set-open-files-limit.md | how-to | migrated-needs-review | True | False | 1 |
| 3.4.1 | index.md | explanation | migrated-needs-review | True | False | 1 |
| 3.4.1 | reference/aae-fold-api/erase-keys.md | reference | stub | True | False | 1 |
| 3.4.1 | reference/aae-fold-api/find-keys.md | reference | stub | True | False | 1 |
| 3.4.1 | reference/aae-fold-api/find-tombstones.md | reference | stub | True | False | 1 |
| 3.4.1 | reference/aae-fold-api/index.md | reference | migrated-needs-review | True | False | 13 |
| 3.4.1 | reference/aae-fold-api/list-buckets.md | reference | stub | True | False | 1 |
| 3.4.1 | reference/aae-fold-api/object-statistics.md | reference | stub | True | False | 1 |
| 3.4.1 | reference/aae-fold-api/reap-tombstones.md | reference | stub | True | False | 1 |
| 3.4.1 | reference/aae-fold-api/repair-key-range.md | reference | stub | True | False | 1 |
| 3.4.1 | reference/commands/aae.md | reference | stub | True | False | 1 |
| 3.4.1 | reference/commands/vnode-status.md | reference | stub | True | False | 1 |
| 3.4.1 | reference/configuration/bucket-properties.md | reference | stub | True | True | 14 |
| 3.4.1 | reference/configuration/networking.md | reference | migrated | False | False | 1 |
| 3.4.1 | reference/configuration/replication.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.1 | reference/data/content-types.md | reference | stub | True | False | 1 |
| 3.4.1 | reference/data/distributed-data-types.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.1 | reference/data/index.md | reference | stub | True | False | 1 |
| 3.4.1 | reference/data/keys-and-objects.md | reference | stub | True | False | 2 |
| 3.4.1 | reference/data/object-metadata.md | reference | stub | True | False | 3 |
| 3.4.1 | reference/data/secondary-indexes.md | reference | migrated-needs-review | True | False | 2 |
| 3.4.1 | reference/data/version-vectors.md | reference | stub | True | False | 1 |
| 3.4.1 | reference/http-api/conditional-requests.md | reference | stub | True | False | 4 |
| 3.4.1 | reference/http-api/delete-object.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.1 | reference/http-api/fetch-object.md | reference | migrated-needs-review | True | False | 2 |
| 3.4.1 | reference/http-api/index.md | reference | migrated-needs-review | True | False | 2 |
| 3.4.1 | reference/http-api/mapreduce.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.1 | reference/http-api/object-request-options.md | reference | stub | True | True | 1 |
| 3.4.1 | reference/http-api/store-object.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.1 | reference/operations/cluster-claim-algorithms.md | reference | stub | True | True | 3 |
| 3.4.1 | reference/operations/custom-code.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.1 | reference/operations/log-files.md | reference | migrated-needs-review | True | False | 2 |
| 3.4.1 | reference/operations/object-deletion.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.1 | reference/operations/remote-console.md | reference | migrated-needs-review | True | False | 3 |
| 3.4.1 | reference/operations/replication-statistics.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.1 | reference/operations/statistics-and-monitoring.md | reference | migrated-needs-review | True | False | 4 |
| 3.4.1 | reference/query-api/accumulation-options.md | reference | stub | True | False | 2 |
| 3.4.1 | reference/query-api/expressions.md | reference | stub | True | False | 5 |
| 3.4.1 | reference/query-api/index.md | reference | stub | True | False | 2 |
| 3.4.1 | reference/query-api/limits.md | reference | stub | True | False | 9 |
| 3.4.1 | reference/query-api/request.md | reference | stub | True | False | 9 |
| 3.4.1 | reference/query-api/responses.md | reference | stub | True | False | 1 |
| 3.4.1 | reference/releases/downloads.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.1 | reference/releases/supported-platforms.md | reference | migrated-needs-review | True | False | 2 |
| 3.4.1 | reference/replication-api/index.md | reference | stub | True | False | 3 |
| 3.4.1 | reference/replication-api/runtime-controls.md | reference | migrated-needs-review | True | False | 12 |
| 3.4.1 | reference/specialized-apis/cluster-metadata.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.1 | reference/specialized-apis/data-type-api.md | reference | stub | True | True | 1 |
| 3.4.1 | reference/specialized-apis/fetch-api.md | reference | stub | True | False | 1 |
| 3.4.1 | reference/specialized-apis/index.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.1 | reference/specialized-apis/legacy-query-api.md | reference | stub | True | False | 1 |
| 3.4.1 | reference/specialized-apis/list-api.md | reference | stub | True | False | 1 |
| 3.4.1 | reference/specialized-apis/strong-consistency-api.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.1 | reference/specialized-apis/write-once-api.md | reference | migrated-needs-review | True | False | 1 |
| 3.4.1 | tutorials/first-cluster/index.md | tutorial | migrated-needs-review | True | False | 1 |
| 3.4.1 | tutorials/query-api/build-search-index.md | tutorial | stub | True | False | 12 |
| 3.4.1 | tutorials/query-api/index.md | tutorial | stub | True | False | 1 |

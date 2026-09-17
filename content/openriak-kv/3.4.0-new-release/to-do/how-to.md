---
title: 'How-to'
description: "Complete proposed How-to structure: 148 task guides in 15 subsections."
weight: 20
recommendations: true
product: 'OpenRiak KV'
product_version: '3.4.0'
---

This is the complete proposed **How-to** structure for OpenRiak KV 3.4.0. It includes retained, reorganised, and new pages. Each row names one proposed task guide and the outcome it should help the reader achieve.

The proposal covers **148 pages in 15 subsections**, based on the existing 155 How-to files, including 13 landing pages. In [Diátaxis, how-to guides](https://diataxis.fr/how-to-guides/) help a reader accomplish a specific task or solve a problem.

Each subsection also has a short landing page that helps readers choose a task. Platform, backend, client, and legacy procedures must use the version applicability recorded in Reference; inclusion in this proposal is not a support claim.

## Proposed pages

### Quick Start

| Section | Name | Explanation |
| --- | --- | --- |
| Quick Start | Start a local node with Docker | Reach a working node, perform a first write and read, and stop the environment using the shortest verified path. |
| Quick Start | Start a local cluster with Docker | Start the supplied development cluster, verify membership and a client request, and identify the cleanup command. |
| Quick Start | Start a node from an installed package | Take an installed native package through minimal configuration, service startup, and a verified request; link to platform installation prerequisites. |

### Planning a deployment

| Section | Name | Explanation |
| --- | --- | --- |
| Planning a deployment | Map application data to objects and buckets | Choose keys, object boundaries, bucket types, and access patterns for a concrete workload; record how updates and object discovery will work. |
| Planning a deployment | Size a cluster and reserve recovery headroom | Estimate storage, memory, CPU, and network needs from the workload, replication, indexes, growth, and recovery requirements. |
| Planning a deployment | Choose a ring size | Use expected cluster size and workload to select the initial ring size and identify the migration required to change it later. |
| Planning a deployment | Choose a storage backend | Select a backend against persistence, indexing, memory, and workload requirements, using the release-specific capability reference. |
| Planning a deployment | Choose replication and acknowledgement policies | Translate availability and durability requirements into replica placement, read/write acknowledgements, primary requirements, and persistence choices. |
| Planning a deployment | Choose a multi-cluster topology | Select replication directions, failure boundaries, and recovery objectives for the deployment, then identify the required connections and validation checks. |
| Planning a deployment | Choose a deletion and retention policy | Match tombstone retention, expiry, reaping, and repair schedules to the application's data lifecycle and recovery requirements. |
| Planning a deployment | Check production readiness | Verify deployment, capacity, security, monitoring, backup, restore, and failure-handling readiness before admitting production traffic. |

### Installation

| Section | Name | Explanation |
| --- | --- | --- |
| Installation | Install on Debian or Ubuntu | Install a release-matched package and dependencies, configure the service, and verify startup on the selected supported distribution. |
| Installation | Install on RHEL, Rocky Linux, or Oracle Linux | Cover the RPM installation paths actually provided for this release, with distribution-specific prerequisites and service verification. |
| Installation | Install on Amazon Linux | Install the appropriate package for the chosen architecture and verify service and network access; keep cloud sizing in the deployment guides. |
| Installation | Install on Alpine Linux | Document the release's Alpine package, dependencies, service integration, and installation checks once that platform path is verified. |
| Installation | Install on Raspberry Pi OS | Specify the verified operating-system and architecture combination, installation method, resource prerequisites, and startup checks. |
| Installation | Run OpenRiak with persistent Docker storage | Configure persistent volumes, networking, settings, and container lifecycle for an existing container-based workflow; link to image downloads. |
| Installation | Build and install from source | Select the release and compatible Erlang/OTP toolchain, build a release, install it, and verify the resulting executable and service. |
| Installation | Verify an installation | Check configuration, startup, node identity, listeners, diagnostics, and a write/read round trip before joining a cluster. |

### Node configuration

| Section | Name | Explanation |
| --- | --- | --- |
| Node configuration | Configure node identity, directories, and the initial ring | Set the essential node settings before cluster formation and verify paths, identity, and ring compatibility. |
| Node configuration | Configure HTTP and Protocol Buffers listeners | Bind the required interfaces and ports, apply access restrictions, and verify reachability using the intended client protocol. |
| Node configuration | Add advanced configuration | Add settings that require advanced.config, check precedence and syntax, and confirm the effective values after startup. |
| Node configuration | Set runtime environment variables | Supply supported variables through the deployment's service or container mechanism and verify what the process receives. |
| Node configuration | Inspect and manage effective configuration | Locate the active configuration, inspect resolved settings, compare nodes, and apply a controlled configuration change. |
| Node configuration | Validate configuration before startup | Run configuration checks, interpret validation failures, and confirm the node can start with the intended settings. |
| Node configuration | Configure a load-balancing proxy | Configure listener routing, health checks, timeouts, and maintenance draining for a verified proxy deployment. |
| Node configuration | Configure logging and change runtime log levels | Choose destinations and levels, temporarily increase diagnostic detail, verify the output, and restore the intended logging level. |
| Node configuration | Configure split and JSON log handlers | Route log categories to the intended handlers, enable structured output, and verify parsing and rotation with sample events. |
| Node configuration | Configure object expiration | Apply retention and expiry settings to the intended scope, verify the resulting object lifecycle, and describe how to change or disable expiry. |

### Storage maintenance

| Section | Name | Explanation |
| --- | --- | --- |
| Storage maintenance | Configure Bitcask | Set the storage location and workload-specific Bitcask options, start the node, and verify persistence and backend health. |
| Storage maintenance | Configure Leveled | Configure Leveled storage and relevant resource settings, then verify backend startup, reads, writes, and indexing. |
| Storage maintenance | Schedule Bitcask merges | Choose a merge window, observe merge progress, and confirm space reclamation without unacceptable workload interference. |
| Storage maintenance | Schedule Leveled compaction | Set an appropriate compaction window and verify its effect on disk work, space consumption, and foreground traffic. |
| Storage maintenance | Migrate to another storage backend | Move existing data through a verified migration or replacement procedure, with backup, data validation, and a recovery plan. |
| Storage maintenance | Remove obsolete Leveled backup files | Identify eligible orphaned backup files, check the required preconditions, reclaim their space, and verify store health. |
| Storage maintenance | Repair a Leveled store | Diagnose the affected store, preserve recovery evidence, perform the documented rebuild, and verify recovered data and indexes. |

### Application data

| Section | Name | Explanation |
| --- | --- | --- |
| Application data | Create and activate bucket types | Create a type with deliberate properties, validate it, activate it, and verify its behaviour before applications use it. |
| Application data | Use bucket types in an application | Address typed buckets correctly in client requests and confirm the intended namespace and inherited properties. |
| Application data | Create and store an object | Store a value with an explicit or generated key and verify the returned identity, metadata, and persisted content. |
| Application data | Read an object and handle missing values | Fetch the value and causal context, distinguish absent objects from failures, and handle responses that contain siblings. |
| Application data | Update an object with causal context | Fetch an object, preserve its context, apply a change, and verify the update without unintentionally discarding concurrent work. |
| Application data | Delete an object | Delete a selected object with the relevant context and options, then check the observable result and expected deletion lifecycle. |
| Application data | Store and retrieve different content types | Set media types and encodings for structured or binary values and verify that clients preserve the intended representation. |
| Application data | Resolve concurrent object updates | Retrieve siblings, apply an application-specific merge, write the resolved value with context, and verify the outcome under another concurrent update. |
| Application data | Make conditional reads and writes | Use the supported validators, handle failed preconditions, and verify the application's retry or conflict response. |
| Application data | Coordinate an update with a latch object | Apply the supported latch pattern to a specific coordination task, handling contention, interruption, and the limits of the mechanism. |
| Application data | Update distributed counters | Create a correctly configured counter, increment or decrement it, and verify results using the supported client and data-type API. |
| Application data | Add and remove members of distributed sets | Apply additions and context-dependent removals, preserve the required context, and verify the resulting set. |
| Application data | Add members to grow-only sets | Configure the data type, add members, and verify set membership while respecting the absence of a removal operation. |
| Application data | Update distributed maps | Create and update typed map fields, preserve causal context, and verify nested updates and removals. |
| Application data | Estimate distinct values with HyperLogLog | Configure the data type, add observations, retrieve the estimate, and interpret it as an estimate rather than an exact count. |
| Application data | Store immutable data through the write-once path | Configure the required bucket policy, perform immutable writes, and verify behaviour when an application tries to reuse a key. |
| Application data | Install and use a commit hook | Implement a supported hook, deploy it consistently, attach it to a bucket policy, and verify success and failure behaviour. |

### Indexes and queries

| Section | Name | Explanation |
| --- | --- | --- |
| Indexes and queries | Add and query secondary indexes | Add index entries to objects, run exact and range lookups, and retrieve or page through the matching results. |
| Indexes and queries | Run exact and range queries with the Query API | Construct a minimal query over an existing index, submit it, and verify the returned keys or terms. |
| Indexes and queries | Filter queries using projected attributes | Encode the required attributes in index terms, write evaluation and filter expressions, and verify matches against known data. |
| Indexes and queries | Combine queries and accumulate results | Combine index scans and select the required key, term, or count accumulation mode, including deliberate duplicate handling. |
| Indexes and queries | Retrieve paginated or asynchronous query results | Follow the supported result-delivery mechanism, preserve continuations, and handle timeouts and incomplete responses correctly. |

### Replication and reconciliation

| Section | Name | Explanation |
| --- | --- | --- |
| Replication and reconciliation | Enable TicTac anti-entropy | Configure the prerequisites and local reconciliation settings, verify tree creation and exchanges, and check repair progress. |
| Replication and reconciliation | Connect clusters with next-generation replication | Configure a complete source-to-sink connection with matching queue and endpoint settings, then verify data movement end to end. |
| Replication and reconciliation | Enable real-time replication | Enable replication for the intended data, verify the source and sink path, and check delivery of a new write and deletion. |
| Replication and reconciliation | Configure replication queues and filters | Define queues, filters, capacity, and compression for the workload, then verify which objects enter each queue. |
| Replication and reconciliation | Configure sink nodes and consumers | Connect the intended consumers to source queues, configure their concurrency, and verify fetching and applying replicated objects. |
| Replication and reconciliation | Configure and schedule fullsync | Configure current-generation fullsync, schedule exchanges, verify convergence, and inspect the results of an interrupted or incomplete run. |
| Replication and reconciliation | Reconcile selected buckets | Configure bucket-scoped reconciliation and verify that the intended data converges without expanding the scope unnecessarily. |
| Replication and reconciliation | Exclude temporary data from cached AAE trees | Apply the exclusion to a suitable bucket policy and check its effect on repair and replication requirements. |
| Replication and reconciliation | Re-replicate a key range or time window | Select the affected data, enqueue it for the intended destination, and verify delivery and convergence. |
| Replication and reconciliation | Migrate to another cluster using replication | Seed and catch up a destination cluster, validate data, switch application traffic, and retain a documented recovery path. |
| Replication and reconciliation | Secure next-generation replication connections | Apply the current replication transport's authentication and TLS controls and verify trusted, rejected, and interrupted connections. |

### Cluster lifecycle

| Section | Name | Explanation |
| --- | --- | --- |
| Cluster lifecycle | Start, stop, or restart a node | Use the deployment's service mechanism, account for ongoing traffic and background work, and verify the resulting service state. |
| Cluster lifecycle | Plan and commit a membership change | Stage a change, inspect the plan and placement consequences, commit it, and monitor the transition to completion. |
| Cluster lifecycle | Add nodes to a cluster | Prepare compatible nodes, join them, inspect the membership plan, and verify ownership and handoff completion. |
| Cluster lifecycle | Remove a node from a cluster | Check capacity and replica placement, plan the departure, drain ownership, and verify the remaining cluster. |
| Cluster lifecycle | Replace a failed node | Decide whether replacement is appropriate, apply the required replacement procedure, and validate data recovery and membership. |
| Cluster lifecycle | Replace nodes without stopping the cluster | Perform controlled replacements one at a time, using health and recovery checkpoints before proceeding to the next node. |
| Cluster lifecycle | Perform a rolling restart | Drain and restart nodes in an appropriate order, waiting for cluster and background-work recovery between nodes. |
| Cluster lifecycle | Monitor and control handoffs | Inspect transfers, change the relevant controls when necessary, and confirm that paused or throttled transfers eventually complete. |
| Cluster lifecycle | Change node names, addresses, or cluster identity | Follow the applicable identity-change procedure, update dependent configuration, and verify membership and replication connectivity. |
| Cluster lifecycle | Upgrade to OpenRiak KV 3.4.0 | Verify the source-version path and prerequisites, upgrade in stages, and check application, storage, and replication compatibility. |
| Cluster lifecycle | Roll back a compatible cluster upgrade | Determine whether rollback remains supported for the actual data and activated features, then follow the version-specific downgrade procedure. |
| Cluster lifecycle | Back up node data and cluster metadata | Choose a supported backend-specific backup procedure, capture the required metadata, and verify that the backup can be restored. |
| Cluster lifecycle | Restore node data from a backup | Restore the appropriate backend and metadata into the intended recovery environment and verify data before returning traffic. |
| Cluster lifecycle | Recover a cluster after a widespread failure | Assess surviving data and backups, choose a recovery sequence, restore service, and validate the recovered dataset and application behaviour. |

### Monitoring and diagnostics

| Section | Name | Explanation |
| --- | --- | --- |
| Monitoring and diagnostics | Perform routine cluster health checks | Check availability, capacity, repairs, replication, backups, and errors against an agreed operational baseline. |
| Monitoring and diagnostics | Inspect node and cluster health | Use status commands and metrics to identify unhealthy nodes, membership disagreement, resource pressure, and stalled background work. |
| Monitoring and diagnostics | Inspect vnode and backend status | Locate affected partitions and stores, interpret the relevant status fields, and identify evidence needed for further diagnosis. |
| Monitoring and diagnostics | Monitor anti-entropy progress | Check trees, exchanges, backlogs, and failures for the configured anti-entropy implementation and identify incomplete convergence. |
| Monitoring and diagnostics | Investigate read-repair activity | Measure read repairs, relate them to workload and recent failures, and identify patterns that require investigation. |
| Monitoring and diagnostics | Monitor replication and inter-cluster reconciliation | Observe queue growth, delivery, exchange results, and lag to distinguish healthy catch-up from a stalled replication path. |
| Monitoring and diagnostics | Inspect worker queues and saturation | Compare queue length, wait times, and worker activity to identify constrained background or foreground work. |
| Monitoring and diagnostics | Collect diagnostic evidence | Gather the relevant status, logs, metrics, and configuration into a reproducible incident record without exposing credentials. |
| Monitoring and diagnostics | Inspect a node through the remote console | Attach to the intended node, perform a bounded diagnostic operation, and exit without unintentionally changing node state. |
| Monitoring and diagnostics | Inspect stored objects and metadata | Examine object representations, causal context, and backend state using the supported diagnostic interfaces. |

### Data inspection and repair

| Section | Name | Explanation |
| --- | --- | --- |
| Data inspection and repair | Run and retrieve a long-running AAE fold | Start the selected fold through the CLI or remote console, track completion, and retrieve its output after a timeout or disconnect. |
| Data inspection and repair | Inventory buckets using AAE folds | List the buckets in the intended scope and use the result to plan inspection or maintenance work. |
| Data inspection and repair | Find oversized objects or excessive siblings | Select key ranges and object-size or sibling filters, retrieve the matching objects, and verify the findings before corrective action. |
| Data inspection and repair | Count objects in a selected scope | Use the documented count mode and filters to obtain the count required for a migration, audit, or maintenance check. |
| Data inspection and repair | Measure object sizes and sibling distributions | Collect aggregate object statistics over a bounded scope and interpret the result for capacity or conflict investigation. |
| Data inspection and repair | Locate tombstones | Find deletion markers in the intended bucket, key range, or time window before investigating retention or reclamation. |
| Data inspection and repair | Count retained tombstones | Use the documented count mode to measure deletion markers and compare retention or reaping outcomes. |
| Data inspection and repair | Repair a selected key range | Select the damaged or divergent scope, trigger the documented repair, and verify recovery without repairing unrelated data. |
| Data inspection and repair | Erase a selected set of keys | Verify the filter and candidate set before erasure, execute the bounded operation, and check the resulting deletion state. |
| Data inspection and repair | Reap eligible tombstones | Check the retention and replication prerequisites, identify eligible markers, perform reaping, and verify the result. |
| Data inspection and repair | Schedule erasure and tombstone reaping | Configure recurring reclamation work with an appropriate scope, rate, and observation of its effect on the workload. |
| Data inspection and repair | Rebuild AAE trees | Select the affected trees, request a rebuild, monitor completion, and verify that subsequent exchanges operate correctly. |
| Data inspection and repair | Repair a vnode or node from surviving replicas | Identify the affected ownership, trigger the applicable repair, monitor progress, and verify the reconstructed data. |
| Data inspection and repair | Control repair impact during application traffic | Set and observe repair concurrency and resource use so that recovery proceeds within the application's service requirements. |
| Data inspection and repair | Repair inconsistent secondary indexes | Identify a supported index-repair path, run and monitor the repair, and verify queries against known object data. |

### Security

| Section | Name | Explanation |
| --- | --- | --- |
| Security | Enable authentication and authorization | Prepare administrative access, enable the controls, and verify both allowed and rejected operations before opening application access. |
| Security | Create, update, and remove users | Manage user identities and credentials, verify authentication, and revoke access when an identity is no longer needed. |
| Security | Manage groups and membership | Create groups, assign users, change membership, and verify the resulting effective permissions. |
| Security | Configure authentication sources | Match connections to the intended authentication methods and verify source precedence and rejected connections. |
| Security | Grant and revoke permissions | Apply permissions to the intended users, groups, and bucket scopes, then test permitted and denied actions. |
| Security | Configure and rotate TLS certificates | Install a verified trust chain and listener configuration, validate peers, and rotate certificates while preserving required access. |
| Security | Restrict client, node, and administrative network access | Apply interface and network restrictions appropriate to each connection type and verify allowed and blocked paths. |
| Security | Authenticate an application client | Configure credentials and trust material in a verified client, connect to the intended endpoint, and handle authentication failures. |
| Security | Audit deployment security | Check identities, permissions, exposed interfaces, certificates, secrets, and logging against the deployment's security requirements. |

### Performance

| Section | Name | Explanation |
| --- | --- | --- |
| Performance | Benchmark a representative workload | Define data, access patterns, concurrency, and success metrics, run repeatable measurements, and retain the environment and results. |
| Performance | Reduce request latency | Identify the dominant source of delay, make one relevant change, and compare tail latency and throughput against the baseline. |
| Performance | Set and verify file-descriptor limits | Apply limits through the actual service or container environment and verify the running process receives them. |
| Performance | Tune the Erlang VM for a measured bottleneck | Use evidence to select applicable scheduler, process, port, or distribution settings and verify the effect under representative load. |
| Performance | Tune a deployment on AWS | Measure storage, instance, network, and operating-system constraints, then validate workload-specific infrastructure changes. |
| Performance | Tune replication throughput and lag | Measure the configured replication generation's bottlenecks, adjust its relevant controls, and verify delivery and application impact. |
| Performance | Tune filesystems, memory, and network settings | Apply supported operating-system changes to a measured deployment and verify their effect; extract actionable steps from the existing performance landing page. |
| Performance | Reduce Query API cost | Measure scan size, selectivity, projections, accumulation, and result delivery, then compare query changes against correctness and latency targets. |

### Troubleshooting

| Section | Name | Explanation |
| --- | --- | --- |
| Troubleshooting | Diagnose a node that will not start | Work through configuration, permissions, identity, ports, and storage evidence to identify and correct the startup failure. |
| Troubleshooting | Diagnose node crashes | Preserve logs and crash evidence, distinguish runtime, resource, and storage failures, and verify the selected recovery action. |
| Troubleshooting | Diagnose a slow or overloaded cluster | Correlate client latency with queues, resource usage, background work, and recent changes before applying a targeted remedy. |
| Troubleshooting | Diagnose client connection and request failures | Separate connectivity, protocol, authentication, timeout, and client-library problems with minimal reproducible checks. |
| Troubleshooting | Diagnose unexpected API responses | Interpret status codes and error payloads, including unexpected HTTP 204 responses, and verify the request and object state. |
| Troubleshooting | Diagnose missing, stale, or conflicting data | Check namespace, causal context, consistency options, replicas, deletion, and replication state against the observed application result. |
| Troubleshooting | Diagnose stalled or incomplete replication | Check connectivity, queues, sinks, exchange results, and generation-specific controls to locate the failed part of the pipeline. |
| Troubleshooting | Recover a failed node or choose replacement | Determine whether the original node can rejoin safely or needs repair or replacement, then verify the chosen recovery path. |
| Troubleshooting | Investigate a running node with Erlang diagnostics | Use bounded process, scheduler, profiling, or tracing checks to answer a specific incident question and remove diagnostic overhead afterward. |

### Legacy and specialist workflows

| Section | Name | Explanation |
| --- | --- | --- |
| Legacy and specialist workflows | Maintain a legacy LevelDB deployment | Document configuration and maintenance needed by existing installations, with explicit version applicability and a link to backend migration. |
| Legacy and specialist workflows | Maintain an in-memory backend deployment | State the data-loss and lifecycle constraints, configure a verified use case, and identify the applicable release limitations. |
| Legacy and specialist workflows | Maintain multi-backend and prefix routing | Configure supported routing for existing deployments and document the prerequisites and consequences of changing a route. |
| Legacy and specialist workflows | Maintain legacy active anti-entropy | Configure and monitor an existing legacy AAE installation and connect the procedure to the current repair and migration guidance. |
| Legacy and specialist workflows | Maintain legacy v2 replication | Keep a clearly scoped procedure for existing v2 deployments, with verified commands, compatibility boundaries, and migration links. |
| Legacy and specialist workflows | Maintain legacy v3 replication | Document v3 riak_repl setup and maintenance without presenting it as the current next-generation replication architecture. |
| Legacy and specialist workflows | Configure legacy replication through NAT | Preserve the generation-specific address and listener procedure for deployments that require it, and verify both connection directions. |
| Legacy and specialist workflows | Secure legacy replication connections | Separate the v2 and v3 trust and configuration paths, verify peer validation, and remove unrelated placeholder material. |
| Legacy and specialist workflows | Implement a legacy replication hook | Define the intended filtering or transformation, deploy the hook for the applicable replication generation, and test send and receive behaviour. |
| Legacy and specialist workflows | Configure and run a MapReduce job | Prepare the required execution environment, submit a bounded job, and verify results while identifying release-specific restrictions. |
| Legacy and specialist workflows | Evaluate experimental strong consistency | Provide a disposable evaluation procedure with its documented compatibility and failure boundaries; keep it outside the normal production setup path. |
| Legacy and specialist workflows | Set up a compatible Redis add-on deployment | Specify the verified component versions, configure the add-on and backing buckets, and check its connection and cache behaviour. |
| Legacy and specialist workflows | Use and monitor the Redis add-on | Perform the supported cache workflow, verify read-through and write behaviour, and inspect its operational metrics. |
| Legacy and specialist workflows | Develop an application using the Redis add-on | Apply the add-on's object and cache semantics to an application, including configuration, conflicting values, and deletion behaviour. |

## Boundaries and authoring conventions

A guide should state its outcome and prerequisites, give the actions and decisions needed for the task, and finish with independent verification and applicable recovery steps. Link to Foundations for design rationale and Reference for full option definitions. Keep Quick Starts concise and connect them to the longer first-cluster tutorials.

Use the defaults-table component for reference tables embedded in a guide and `load-value` wherever a default is stated. Label deliberate example values and overrides. The [Reference proposal](../reference/#reference-tables-and-default-values) defines the shared conventions.

## Review basis

The existing task coverage is extensive, but several pages mix procedures, explanations, and complete reference lists. The proposal gives those kinds of material separate homes and makes current replication workflows distinct from legacy riak_repl procedures.

Some apparent guides still need their actual procedure: user and group management, prefix routing, and several troubleshooting pages contain migration notices or specifications. The security best-practices page contains placeholder text, and the replication-security and secondary-index-repair pages include unrelated placeholder passages. Use verified source material when writing the proposed guides rather than treating the existing editorial status as technical validation.

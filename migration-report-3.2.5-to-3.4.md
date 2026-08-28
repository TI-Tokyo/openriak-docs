# OpenRiak KV 3.2.5 to 3.4 documentation migration report

Generated: 2026-08-28T01:03:48+09:00

## Outcome

The migration considered all **291** Markdown files in the read-only 3.2.5 archive. It incorporated **286** content pages into **208** Diátaxis destinations for each of OpenRiak KV 3.4.0 and 3.4.1, touching **416** versioned target pages in total.

Six legacy-only subjects required new pages in each version (**12** files total). Five source files were deliberately not published: two navigation/support files, two version-specific pages superseded by 3.4 material, and one upgrade page tied specifically to 3.2.5.

The source archive remained unchanged. Every inherited content block is marked status: migrated-needs-review and draft: true pending version-specific technical review.

## Scope and policy

- Source: C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5 (read-only, OpenRiak KV 3.2.5)
- Destination: C:\Users\pjacl\Downloads\openriak-docs\content\kv
- Versions: OpenRiak KV 3.4.0 and 3.4.1
- Structure: Diátaxis tutorials, how-to guides, reference, and explanation
- Content precedence: established 3.4 content remains authoritative; useful legacy material is placed before proposed material without replacing 3.4 release notes, downloads, or version-specific guidance.

## Dispositions

| Disposition | Files | Meaning |
|---|---:|---|
| create | 6 | Legacy subject was missing, so a new Diátaxis page was created in both versions. |
| merge | 140 | Legacy material was consolidated into an existing destination, sometimes with related legacy pages. |
| migrate | 140 | Legacy material was routed to its direct Diátaxis destination. |
| superseded | 2 | Obsolete version-specific material was not allowed to replace 3.4 content. |
| support-only | 2 | Navigation or shared-link data was used for migration support but not published as prose. |
| version-specific | 1 | Instructions tied to 3.2.5 were excluded from 3.4 pages. |

## New pages created in each version

- explanation/foundations/new-to-nosql.md
- how-to/secure/best-practices.md
- reference/faq.md
- reference/operations/errors-and-messages.md
- reference/specialized-apis/backend-api.md
- reference/specialized-apis/cluster-metadata.md

## Deliberately excluded or superseded

| Source | Disposition | Rationale |
|---|---|---|
| _index.md | support-only | Generated navigation metadata; no prose migration. |
| _reference-links.md | support-only | Shared legacy link definitions are consumed during link rewriting, not published as a page. |
| downloads.md | superseded | 3.2.5 download links and packages must not replace the version-specific 3.4 download reference. |
| release-notes.md | superseded | 3.2.5 release notes are historical and the 3.4 release-note pages remain authoritative. |
| setup/upgrading/version.md | version-specific | Instructions specifically for upgrading to 3.2.5 are not copied into 3.4 version pages. |

## Automated transformations

- Rewrote legacy internal /riak/kv/3.2.5 routes to the matching /kv/3.4.0 or /kv/3.4.1 Diataxis route.
- Converted supported legacy Hugo note shortcodes to Markdown callouts.
- Replaced legacy example-domain and security-contact shortcodes with portable prose.
- Normalized product prose from Riak KV to OpenRiak KV where safe while preserving command names such as riak.
- Recorded exact legacy sources and review requirements in YAML front matter.
- Placed migrated legacy material before proposed content while retaining existing 3.4 summaries and version-specific material.

## Validation

| Check | Result |
|---|---:|
| target_markdown_files | 756 |
| version_3_4_0_files | 374 |
| version_3_4_1_files | 381 |
| legacy_touched_pages | 416 |
| front_matter_errors | 0 |
| product_version_mismatches | 0 |
| marker_errors | 0 |
| remaining_hugo_template_files | 0 |
| remaining_3_2_5_url_files | 0 |
| cross_version_link_files | 0 |
| unresolved_internal_routes | 0 |
| missing_source_coverage | 0 |
| unexpected_dispositions | 0 |
| duplicate_sidebar_positions | 0 |
| legacy_source_hash_changes | 0 |
| import_errors | 0 |
| touched_status_errors | 0 |
| touched_draft_errors | 0 |
| touched_source_metadata_errors | 0 |
| touched_review_metadata_errors | 0 |
| touched_warning_errors | 0 |
| missing_exact_source_attributions | 0 |
| report_json_parse_errors | 0 |
| report_markdown_source_ledger_rows | 291 |
| report_markdown_destination_ledger_rows | 208 |

## Publication gate

- Verify commands, defaults, package names, compatibility claims, and platform support against OpenRiak KV 3.4.0 and 3.4.1.
- Review security, replication, storage backend, and upgrade guidance against the matching release behavior.
- Remove draft status only after technical and editorial review.

## Complete source-page ledger

| Source | Title | Bytes | Disposition | Diátaxis destination | Rationale |
|---|---|---:|---|---|---|
| _index.md |  | 133 | support-only |  | Generated navigation metadata; no prose migration. |
| _reference-links.md | Riak KV 3.2.5 Reference Links List | 12767 | support-only |  | Shared legacy link definitions are consumed during link rewriting, not published as a page. |
| add-ons.md | Add-ons | 590 | merge | how-to/redis-add-on/index.md | Add-on overview merged with the Redis add-on landing page. |
| add-ons/redis.md | Riak Redis Add-on | 2228 | merge | how-to/redis-add-on/index.md | Redis add-on overview. |
| add-ons/redis/developing-rra.md | Developing with Riak Redis Add-on | 14055 | migrate | how-to/redis-add-on/develop.md | Redis add-on development guidance. |
| add-ons/redis/redis-add-on-features.md | Riak Redis Add-on Features | 6809 | merge | how-to/redis-add-on/index.md | Redis add-on feature overview. |
| add-ons/redis/set-up-rra.md | Setting Up Riak Redis Add-on | 8784 | merge | how-to/redis-add-on/set-up.md | Redis add-on setup guidance. |
| add-ons/redis/set-up-rra/deployment-models.md | Riak Redis Add-on Deployment Models | 5893 | merge | how-to/redis-add-on/set-up.md | Redis deployment models support setup decisions. |
| add-ons/redis/using-rra.md | Using Riak Redis Add-on | 8688 | migrate | how-to/redis-add-on/use.md | Redis add-on usage guidance. |
| configuring.md | Configuring Riak KV | 2003 | migrate | how-to/configure/index.md | Configuration section introduction. |
| configuring/active-anti-entropy.md | Active Anti-Entropy | 2440 | migrate | reference/configuration/active-anti-entropy.md | AAE configuration overview. |
| configuring/active-anti-entropy/legacy-aae.md | Legacy Active Anti-Entropy | 4110 | migrate | how-to/configure/replication/configure-legacy-aae.md | Legacy AAE configuration procedure. |
| configuring/active-anti-entropy/tictac-aae.md | TicTac Active Anti-Entropy | 4110 | migrate | how-to/configure/replication/enable-tictac-aae.md | TicTac AAE configuration procedure. |
| configuring/backend.md | Backend Configuration | 21957 | merge | how-to/configure/backends/index.md | Backend configuration overview. |
| configuring/basic.md | Basic Riak KV Configuration | 9215 | migrate | how-to/configure/basic-node-settings.md | Basic node settings. |
| configuring/global-object-expiration.md | Configure Global Object Expiration | 2604 | migrate | how-to/configure/global-object-expiration.md | Global object-expiration procedure. |
| configuring/load-balancing-proxy.md | Load Balancing and Proxy Configuration | 9579 | migrate | how-to/configure/load-balancing-proxy.md | Load balancer and proxy configuration. |
| configuring/managing.md | Managing Your Configuration | 3325 | migrate | how-to/configure/manage-configuration.md | Configuration management. |
| configuring/mapreduce.md | MapReduce Settings | 7131 | migrate | how-to/configure/mapreduce.md | MapReduce configuration. |
| configuring/next-gen-replication.md | Next Gen Replication | 6231 | merge | how-to/configure/replication/configure-next-generation-replication.md | Next-generation replication overview. |
| configuring/next-gen-replication/fullsync.md | FullSync | 10202 | migrate | how-to/configure/replication/configure-fullsync.md | Fullsync configuration. |
| configuring/next-gen-replication/queuing.md | Queuing System | 5387 | migrate | how-to/configure/replication/configure-replication-queues.md | Replication queue configuration. |
| configuring/next-gen-replication/realtime.md | RealTime | 2537 | migrate | how-to/configure/replication/configure-real-time-replication.md | Real-time replication configuration. |
| configuring/next-gen-replication/reference.md | Configuration Reference | 8161 | migrate | reference/configuration/replication.md | Replication configuration reference. |
| configuring/next-gen-replication/sink.md | Sink Nodes | 5780 | migrate | how-to/configure/replication/configure-sink-nodes.md | Sink-node configuration. |
| configuring/reference.md | Riak KV Configuration Reference | 61814 | merge | reference/configuration/index.md | Comprehensive legacy configuration reference. |
| configuring/strong-consistency.md | Implementing Strong Consistency | 35642 | migrate | how-to/configure/strong-consistency.md | Strong-consistency configuration. |
| configuring/v2-multi-datacenter.md | V2 Multi-Datacenter Replication | 9001 | migrate | how-to/configure/replication/configure-v2-multi-datacenter.md | Legacy v2 replication configuration. |
| configuring/v2-multi-datacenter/nat.md | With NAT | 2317 | merge | how-to/configure/replication/configure-replication-through-nat.md | NAT configuration for replication. |
| configuring/v2-multi-datacenter/quick-start.md | Quickstart | 11784 | merge | tutorials/replication/two-cluster-replication.md | Legacy v2 replication walkthrough. |
| configuring/v2-multi-datacenter/ssl.md | SSL | 5088 | merge | how-to/configure/replication/secure-replication.md | Replication TLS setup. |
| configuring/v3-multi-datacenter.md | V3 Multi-Datacenter Replication | 9174 | migrate | how-to/configure/replication/configure-v3-multi-datacenter.md | Current-generation replication configuration background. |
| configuring/v3-multi-datacenter/nat.md | With NAT | 4989 | merge | how-to/configure/replication/configure-replication-through-nat.md | NAT configuration for replication. |
| configuring/v3-multi-datacenter/quick-start.md | Quickstart | 5180 | merge | tutorials/replication/two-cluster-replication.md | Replication walkthrough. |
| configuring/v3-multi-datacenter/ssl.md | SSL | 5411 | merge | how-to/configure/replication/secure-replication.md | Replication TLS setup. |
| deprecated/riak-search.md | Riak Search | 655 | merge | reference/releases/deprecations.md | Historical Riak Search deprecation information. |
| developing.md | Developing with Riak KV | 1834 | migrate | how-to/develop/index.md | Development section introduction. |
| developing/api.md | APIs | 722 | merge | reference/index.md | API overview. |
| developing/api/backend.md | Backend API | 3794 | create | reference/specialized-apis/backend-api.md | Backend API reference missing from the new scaffold. |
| developing/api/http.md | HTTP API | 4754 | migrate | reference/http-api/index.md | HTTP API overview. |
| developing/api/http/counters.md | HTTP Counters | 2041 | migrate | reference/http-api/counters.md | HTTP API operation reference. |
| developing/api/http/delete-object.md | HTTP Delete Object | 2224 | migrate | reference/http-api/delete-object.md | HTTP API operation reference. |
| developing/api/http/fetch-object.md | HTTP Fetch Object | 8877 | migrate | reference/http-api/fetch-object.md | HTTP API operation reference. |
| developing/api/http/get-bucket-props.md | HTTP Get Bucket Properties | 2704 | migrate | reference/http-api/get-bucket-properties.md | HTTP API operation reference. |
| developing/api/http/link-walking.md | HTTP Link Walking | 4235 | migrate | reference/http-api/link-walking.md | HTTP API operation reference. |
| developing/api/http/list-buckets.md | HTTP List Buckets | 1417 | migrate | reference/http-api/list-buckets.md | HTTP API operation reference. |
| developing/api/http/list-keys.md | HTTP List Keys | 2092 | migrate | reference/http-api/list-keys.md | HTTP API operation reference. |
| developing/api/http/list-resources.md | HTTP List Resources | 4228 | migrate | reference/http-api/list-resources.md | HTTP API operation reference. |
| developing/api/http/mapreduce.md | HTTP MapReduce | 2386 | migrate | reference/http-api/mapreduce.md | HTTP API operation reference. |
| developing/api/http/ping.md | HTTP Ping | 1148 | migrate | reference/http-api/ping.md | HTTP API operation reference. |
| developing/api/http/reset-bucket-props.md | HTTP Reset Bucket Properties | 1493 | migrate | reference/http-api/reset-bucket-properties.md | HTTP API operation reference. |
| developing/api/http/secondary-indexes.md | HTTP Secondary Indexes | 2601 | migrate | reference/http-api/secondary-indexes.md | HTTP API operation reference. |
| developing/api/http/set-bucket-props.md | HTTP Set Bucket Properties | 6423 | migrate | reference/http-api/set-bucket-properties.md | HTTP API operation reference. |
| developing/api/http/status.md | HTTP Status | 7317 | migrate | reference/http-api/status.md | HTTP API operation reference. |
| developing/api/http/store-object.md | HTTP Store Object | 5418 | migrate | reference/http-api/store-object.md | HTTP API operation reference. |
| developing/api/protocol-buffers.md | Protocol Buffers Client API | 5740 | migrate | reference/protocol-buffers/index.md | Protocol Buffers overview. |
| developing/api/protocol-buffers/auth-req.md | PBC Auth Request | 800 | migrate | reference/protocol-buffers/authentication.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/coverage-queries.md | PBC Coverage Queries | 2981 | migrate | reference/protocol-buffers/coverage-queries.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/delete-object.md | PBC Delete Object | 3544 | migrate | reference/protocol-buffers/delete-object.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/dt-counter-store.md | PBC Data Type Counter Store | 962 | migrate | reference/protocol-buffers/update-counter.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/dt-fetch.md | PBC Data Type Fetch | 4794 | migrate | reference/protocol-buffers/fetch-data-type.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/dt-map-store.md | PBC Data Type Map Store | 3207 | migrate | reference/protocol-buffers/update-map.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/dt-set-store.md | PBC Data Type Set Store | 904 | migrate | reference/protocol-buffers/update-set.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/dt-store.md | PBC Data Type Store | 5701 | migrate | reference/protocol-buffers/store-data-type.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/dt-union.md | PBC Data Type Union | 826 | migrate | reference/protocol-buffers/union-data-type.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/fetch-object.md | PBC Fetch Object | 6953 | migrate | reference/protocol-buffers/fetch-object.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/get-bucket-props.md | PBC Get Bucket Properties | 3361 | migrate | reference/protocol-buffers/get-bucket-properties.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/get-bucket-type.md | PBC Get Bucket Type | 912 | migrate | reference/protocol-buffers/get-bucket-type.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/get-client-id.md | PBC Get Client ID | 1560 | migrate | reference/protocol-buffers/client-id.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/list-buckets.md | PBC List Buckets | 1424 | migrate | reference/protocol-buffers/list-buckets.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/list-keys.md | PBC List Keys | 1713 | migrate | reference/protocol-buffers/list-keys.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/mapreduce.md | PBC MapReduce | 4636 | migrate | reference/protocol-buffers/mapreduce.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/ping.md | PBC Ping | 711 | migrate | reference/protocol-buffers/ping.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/reset-bucket-props.md | PBC Reset Bucket Properties | 1326 | migrate | reference/protocol-buffers/reset-bucket-properties.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/secondary-indexes.md | PBC Secondary Indexes | 4345 | migrate | reference/protocol-buffers/secondary-indexes.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/server-info.md | PBC Server Info | 1246 | migrate | reference/protocol-buffers/server-information.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/set-bucket-props.md | PBC Set Bucket Properties | 1587 | migrate | reference/protocol-buffers/set-bucket-properties.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/set-bucket-type.md | PBC Set Bucket Type | 954 | migrate | reference/protocol-buffers/set-bucket-type.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/set-client-id.md | PBC Set Client ID | 1351 | migrate | reference/protocol-buffers/client-id.md | Protocol Buffers operation reference. |
| developing/api/protocol-buffers/store-object.md | PBC Store Object | 6069 | migrate | reference/protocol-buffers/store-object.md | Protocol Buffers operation reference. |
| developing/api/repl-hooks.md | Hooks API | 6059 | merge | how-to/develop/write-replication-hook.md | Replication hook API guidance. |
| developing/app-guide.md | Riak KV Application Guide | 18500 | merge | tutorials/first-application/index.md | Application guide overview. |
| developing/app-guide/advanced-mapreduce.md | Advanced MapReduce | 31655 | merge | how-to/develop/run-mapreduce.md | Advanced MapReduce guidance. |
| developing/app-guide/cluster-metadata.md | Cluster Metadata | 3399 | create | reference/specialized-apis/cluster-metadata.md | Cluster metadata reference missing from the new scaffold. |
| developing/app-guide/reference.md | Reference | 342 | merge | reference/specialized-apis/index.md | Specialized application API reference links. |
| developing/app-guide/replication-properties.md | Replication Properties | 27195 | merge | explanation/replication/references-and-triggers.md | Replication-property behavior. |
| developing/app-guide/strong-consistency.md | Strong Consistency | 12686 | merge | reference/specialized-apis/strong-consistency-api.md | Strong-consistency application behavior. |
| developing/app-guide/write-once.md | Write Once | 6453 | merge | reference/specialized-apis/write-once-api.md | Write-once behavior. |
| developing/client-libraries.md | Client Libraries | 13271 | migrate | reference/client-libraries/index.md | Client-library overview. |
| developing/data-modeling.md |  | 398 | merge | how-to/plan/map-data-to-objects.md | Data-modeling guidance. |
| developing/data-types.md | Data Types | 9061 | merge | reference/data/distributed-data-types.md | Distributed data-type overview. |
| developing/data-types/counters.md | Data Types: Counters | 17294 | migrate | how-to/develop/use-counters.md | Distributed data-type usage. |
| developing/data-types/gsets.md | Data Types:GSets | 16879 | migrate | how-to/develop/use-gsets.md | Distributed data-type usage. |
| developing/data-types/hyperloglogs.md | Data Types: HyperLogLogs | 15301 | migrate | how-to/develop/use-hyperloglogs.md | Distributed data-type usage. |
| developing/data-types/maps.md | Data Types: Maps | 49925 | migrate | how-to/develop/use-maps.md | Distributed data-type usage. |
| developing/data-types/sets.md | Data Types: Sets | 20237 | migrate | how-to/develop/use-sets.md | Distributed data-type usage. |
| developing/faq.md | Frequently Asked Questions | 29332 | create | reference/faq.md | Frequently asked questions missing from the new scaffold. |
| developing/getting-started.md | Getting Started Overview | 2461 | merge | tutorials/first-application/index.md | Getting-started overview. |
| developing/getting-started/csharp.md | Getting Started with C Sharp | 2915 | merge | tutorials/first-application/csharp.md | Language-specific getting-started material merged into the csharp tutorial. |
| developing/getting-started/csharp/crud-operations.md | CRUD Operations with C Sharp | 4718 | merge | tutorials/first-application/csharp.md | Language-specific getting-started material merged into the csharp tutorial. |
| developing/getting-started/csharp/object-modeling.md | Object Modeling with C Sharp | 4744 | merge | tutorials/first-application/csharp.md | Language-specific getting-started material merged into the csharp tutorial. |
| developing/getting-started/csharp/querying.md | Querying with C Sharp | 8310 | merge | tutorials/first-application/csharp.md | Language-specific getting-started material merged into the csharp tutorial. |
| developing/getting-started/erlang.md | Getting Started with Erlang | 1634 | merge | tutorials/first-application/erlang.md | Language-specific getting-started material merged into the erlang tutorial. |
| developing/getting-started/erlang/crud-operations.md | CRUD Operations with Erlang | 4850 | merge | tutorials/first-application/erlang.md | Language-specific getting-started material merged into the erlang tutorial. |
| developing/getting-started/erlang/object-modeling.md | Object Modeling with Erlang | 11923 | merge | tutorials/first-application/erlang.md | Language-specific getting-started material merged into the erlang tutorial. |
| developing/getting-started/erlang/querying.md | Querying with Erlang | 11584 | merge | tutorials/first-application/erlang.md | Language-specific getting-started material merged into the erlang tutorial. |
| developing/getting-started/golang.md | Getting Started with Go | 1759 | merge | tutorials/first-application/golang.md | Language-specific getting-started material merged into the golang tutorial. |
| developing/getting-started/golang/crud-operations.md |  | 7797 | merge | tutorials/first-application/golang.md | Language-specific getting-started material merged into the golang tutorial. |
| developing/getting-started/golang/object-modeling.md | Object Modeling with Go | 13558 | merge | tutorials/first-application/golang.md | Language-specific getting-started material merged into the golang tutorial. |
| developing/getting-started/golang/querying.md | Querying with Go | 15874 | merge | tutorials/first-application/golang.md | Language-specific getting-started material merged into the golang tutorial. |
| developing/getting-started/java.md | Getting Started with Java | 2615 | merge | tutorials/first-application/java.md | Language-specific getting-started material merged into the java tutorial. |
| developing/getting-started/java/crud-operations.md | CRUD Operations with Java | 5440 | merge | tutorials/first-application/java.md | Language-specific getting-started material merged into the java tutorial. |
| developing/getting-started/java/object-modeling.md | Object Modeling with Java | 14127 | merge | tutorials/first-application/java.md | Language-specific getting-started material merged into the java tutorial. |
| developing/getting-started/java/querying.md | Querying with Java | 10784 | merge | tutorials/first-application/java.md | Language-specific getting-started material merged into the java tutorial. |
| developing/getting-started/nodejs.md | Getting Started with NodeJS | 3025 | merge | tutorials/first-application/nodejs.md | Language-specific getting-started material merged into the nodejs tutorial. |
| developing/getting-started/nodejs/crud-operations.md | CRUD Operations with NodeJS | 3685 | merge | tutorials/first-application/nodejs.md | Language-specific getting-started material merged into the nodejs tutorial. |
| developing/getting-started/nodejs/object-modeling.md | Object Modeling with NodeJS | 5783 | merge | tutorials/first-application/nodejs.md | Language-specific getting-started material merged into the nodejs tutorial. |
| developing/getting-started/nodejs/querying.md | Querying with NodeJS | 6576 | merge | tutorials/first-application/nodejs.md | Language-specific getting-started material merged into the nodejs tutorial. |
| developing/getting-started/php.md | Getting Started with PHP | 2656 | merge | tutorials/first-application/php.md | Language-specific getting-started material merged into the php tutorial. |
| developing/getting-started/php/crud-operations.md | CRUD Operations with PHP | 7381 | merge | tutorials/first-application/php.md | Language-specific getting-started material merged into the php tutorial. |
| developing/getting-started/php/querying.md | Querying with PHP | 12380 | merge | tutorials/first-application/php.md | Language-specific getting-started material merged into the php tutorial. |
| developing/getting-started/python.md | Getting Started with Python | 2806 | merge | tutorials/first-application/python.md | Language-specific getting-started material merged into the python tutorial. |
| developing/getting-started/python/crud-operations.md | CRUD Operations with Python | 3393 | merge | tutorials/first-application/python.md | Language-specific getting-started material merged into the python tutorial. |
| developing/getting-started/python/object-modeling.md | Object Modeling with Python | 8788 | merge | tutorials/first-application/python.md | Language-specific getting-started material merged into the python tutorial. |
| developing/getting-started/python/querying.md | Querying with Python | 8651 | merge | tutorials/first-application/python.md | Language-specific getting-started material merged into the python tutorial. |
| developing/getting-started/ruby.md | Getting Started with Ruby | 1671 | merge | tutorials/first-application/ruby.md | Language-specific getting-started material merged into the ruby tutorial. |
| developing/getting-started/ruby/crud-operations.md | CRUD Operations with Ruby | 3529 | merge | tutorials/first-application/ruby.md | Language-specific getting-started material merged into the ruby tutorial. |
| developing/getting-started/ruby/object-modeling.md | Object Modeling with Ruby | 8917 | merge | tutorials/first-application/ruby.md | Language-specific getting-started material merged into the ruby tutorial. |
| developing/getting-started/ruby/querying.md | Querying with Ruby | 8688 | merge | tutorials/first-application/ruby.md | Language-specific getting-started material merged into the ruby tutorial. |
| developing/key-value-modeling.md | Riak KV Key/Value Modeling | 18352 | merge | how-to/plan/map-data-to-objects.md | Key/value modeling guidance. |
| developing/usage.md | Usage Overview | 2459 | merge | how-to/develop/index.md | Development usage overview. |
| developing/usage/bucket-types.md | Bucket Types | 2264 | migrate | how-to/develop/use-bucket-types.md | Bucket type application guidance. |
| developing/usage/commit-hooks.md | Using Commit Hooks | 8929 | migrate | how-to/develop/write-commit-hook.md | Commit-hook guidance. |
| developing/usage/conflict-resolution.md | Conflict Resolution | 27880 | merge | how-to/develop/resolve-conflicts.md | Conflict-resolution overview. |
| developing/usage/conflict-resolution/csharp.md | C Sharp | 3915 | merge | how-to/develop/resolve-conflicts.md | Language-specific conflict-resolution example. |
| developing/usage/conflict-resolution/golang.md | Go | 2502 | merge | how-to/develop/resolve-conflicts.md | Language-specific conflict-resolution example. |
| developing/usage/conflict-resolution/java.md | Java | 11712 | merge | how-to/develop/resolve-conflicts.md | Language-specific conflict-resolution example. |
| developing/usage/conflict-resolution/nodejs.md | NodeJS | 2514 | merge | how-to/develop/resolve-conflicts.md | Language-specific conflict-resolution example. |
| developing/usage/conflict-resolution/php.md | PHP | 9996 | merge | how-to/develop/resolve-conflicts.md | Language-specific conflict-resolution example. |
| developing/usage/conflict-resolution/python.md | Python | 10815 | merge | how-to/develop/resolve-conflicts.md | Language-specific conflict-resolution example. |
| developing/usage/conflict-resolution/ruby.md | Ruby | 10394 | merge | how-to/develop/resolve-conflicts.md | Language-specific conflict-resolution example. |
| developing/usage/content-types.md | Content Types | 5700 | migrate | how-to/develop/use-content-types.md | Content-type guidance. |
| developing/usage/creating-objects.md | Creating Objects in Riak KV | 15003 | migrate | how-to/develop/create-object.md | Object creation. |
| developing/usage/deleting-objects.md | Deleting Objects | 4092 | migrate | how-to/develop/delete-object.md | Object deletion. |
| developing/usage/mapreduce.md | Using MapReduce | 8877 | merge | how-to/develop/run-mapreduce.md | MapReduce usage. |
| developing/usage/next-gen-replication.md | Next-Gen Replication | 16598 | merge | explanation/replication/next-generation-replication.md | Next-generation replication usage. |
| developing/usage/reading-objects.md | Reading Objects | 6370 | migrate | how-to/develop/read-object.md | Object reads. |
| developing/usage/replication.md | Replication | 27169 | merge | explanation/replication/index.md | Replication overview. |
| developing/usage/secondary-indexes.md | Using Secondary Indexes (2i) | 59070 | migrate | how-to/develop/query-secondary-indexes.md | Secondary-index queries. |
| developing/usage/security.md | Client Security | 4788 | merge | how-to/develop/authenticate-client.md | Client-security overview. |
| developing/usage/security/erlang.md | Erlang | 5129 | merge | how-to/develop/authenticate-client.md | Language-specific client authentication example. |
| developing/usage/security/java.md | Java | 4644 | merge | how-to/develop/authenticate-client.md | Language-specific client authentication example. |
| developing/usage/security/php.md | PHP | 4337 | merge | how-to/develop/authenticate-client.md | Language-specific client authentication example. |
| developing/usage/security/python.md | Python | 7314 | merge | how-to/develop/authenticate-client.md | Language-specific client authentication example. |
| developing/usage/security/ruby.md | Ruby | 6277 | merge | how-to/develop/authenticate-client.md | Language-specific client authentication example. |
| developing/usage/updating-objects.md | Updating Objects | 26354 | migrate | how-to/develop/update-object.md | Object updates. |
| downloads.md | Download for Riak KV 3.2.5 | 540 | superseded |  | 3.2.5 download links and packages must not replace the version-specific 3.4 download reference. |
| index.md | Riak KV 3.2.5 | 2460 | migrate | index.md | General product introduction. |
| learn.md | Learn About Riak KV | 970 | migrate | explanation/foundations/index.md | Conceptual introduction. |
| learn/concepts.md | Concepts | 2067 | merge | explanation/foundations/index.md | Concept index. |
| learn/concepts/active-anti-entropy.md | Active Anti-Entropy | 4847 | migrate | explanation/replication/active-anti-entropy.md | AAE concept. |
| learn/concepts/buckets.md | Buckets | 7946 | merge | explanation/data-model/keys-objects-and-buckets.md | Bucket concept. |
| learn/concepts/capability-negotiation.md | Capability Negotiation | 1600 | migrate | explanation/foundations/capability-negotiation.md | Capability negotiation. |
| learn/concepts/causal-context.md | Causal Context | 13851 | migrate | explanation/data-model/causal-context.md | Causal context. |
| learn/concepts/clusters.md | Clusters | 5197 | merge | explanation/foundations/clusters-rings-and-partitions.md | Cluster and ring concepts. |
| learn/concepts/crdts.md | Data Types | 11070 | merge | explanation/data-model/distributed-data-types.md | CRDT concepts. |
| learn/concepts/eventual-consistency.md | Eventual Consistency | 9485 | migrate | explanation/consistency/eventual-consistency.md | Eventual consistency. |
| learn/concepts/keys-and-objects.md | Keys and Objects | 2131 | merge | explanation/data-model/keys-objects-and-buckets.md | Keys and objects. |
| learn/concepts/replication.md | Replication | 14228 | merge | explanation/replication/index.md | Replication concepts. |
| learn/concepts/strong-consistency.md | Strong Consistency | 4795 | migrate | explanation/consistency/strong-consistency.md | Strong consistency. |
| learn/concepts/vnodes.md | Vnodes | 7218 | migrate | explanation/foundations/virtual-nodes.md | Virtual nodes. |
| learn/dynamo.md | Dynamo: Amazon’s Highly Available Key-value Store | 108188 | migrate | explanation/foundations/dynamo-model.md | Dynamo model background. |
| learn/glossary.md | Riak KV Glossary | 13145 | migrate | explanation/foundations/glossary.md | Terminology. |
| learn/new-to-nosql.md | New to NoSQL? | 376 | create | explanation/foundations/new-to-nosql.md | NoSQL introduction missing from the new scaffold. |
| learn/use-cases.md | Use Cases For Riak KV | 19124 | migrate | explanation/foundations/use-cases.md | Use cases. |
| learn/why-riak-kv.md | Why Riak KV? | 10263 | migrate | explanation/foundations/why-openriak.md | Product rationale. |
| release-notes.md | Riak KV 3.2.5 Release Notes | 985 | superseded |  | 3.2.5 release notes are historical and the 3.4 release-note pages remain authoritative. |
| setup.md | Setup Riak KV | 911 | migrate | how-to/install/index.md | Setup section introduction. |
| setup/downgrade.md | Downgrading | 3538 | merge | how-to/operate/downgrade-cluster.md | Downgrade procedure. |
| setup/installing.md | Installing Riak KV | 2059 | merge | how-to/install/index.md | Installation overview. |
| setup/installing/alpine-linux.md | Alpine Linux | 1769 | migrate | how-to/install/alpine-linux.md | Historical Alpine installation guidance; no current package is listed. |
| setup/installing/amazon-web-services.md | Amazon Web Services | 4852 | migrate | how-to/install/amazon-linux.md | Amazon Linux installation guidance. |
| setup/installing/debian-ubuntu.md | Debian and Ubuntu | 2960 | migrate | how-to/install/debian-ubuntu.md | Debian and Ubuntu installation guidance. |
| setup/installing/oracle-linux.md | Oracle Linux | 1655 | merge | how-to/install/rhel-rocky.md | Oracle Linux guidance grouped with RPM-family installation. |
| setup/installing/rhel-centos.md | RHEL and CentOS | 3097 | merge | how-to/install/rhel-rocky.md | RHEL-family installation guidance. |
| setup/installing/source.md | Riak KV From Source | 3165 | merge | how-to/install/source.md | Source installation. |
| setup/installing/source/erlang.md | Installing Erlang | 14379 | merge | how-to/install/source.md | Erlang prerequisite details. |
| setup/installing/verify.md | Verifying a Riak KV Installation | 6547 | migrate | how-to/install/verify-installation.md | Installation verification. |
| setup/planning.md | Planning Overview | 1517 | merge | how-to/plan/index.md | Planning overview. |
| setup/planning/backend.md | Choosing a Backend | 2469 | merge | explanation/storage/choosing-backend.md | Backend selection. |
| setup/planning/backend/bitcask.md | Bitcask | 34442 | migrate | explanation/storage/bitcask.md | Bitcask architecture. |
| setup/planning/backend/leveldb.md | LevelDB | 20060 | migrate | explanation/storage/leveldb.md | LevelDB architecture. |
| setup/planning/backend/leveled.md | Leveled | 6487 | migrate | explanation/storage/leveled.md | Leveled architecture. |
| setup/planning/backend/memory.md | Memory | 4618 | migrate | explanation/storage/memory.md | Memory backend architecture. |
| setup/planning/backend/multi.md | Multi-backend | 8648 | migrate | explanation/storage/multi-backend.md | Multi-backend architecture. |
| setup/planning/best-practices.md | Scaling and Operating Riak Best Practices | 5885 | merge | how-to/plan/production-readiness-checklist.md | Operational best practices. |
| setup/planning/bitcask-capacity-calc.md | Bitcask Capacity Calculator | 3933 | merge | explanation/storage/capacity-planning.md | Bitcask capacity calculation. |
| setup/planning/cluster-capacity.md | Cluster Capacity Planning | 11625 | merge | explanation/storage/capacity-planning.md | Cluster capacity planning. |
| setup/planning/future.md | Planning for the Future | 354 | merge | how-to/plan/production-readiness-checklist.md | Future growth planning. |
| setup/planning/operating-system.md | Operating System Support | 773 | merge | reference/releases/supported-platforms.md | Historical operating-system support information. |
| setup/planning/start.md | Start Planning | 1958 | merge | how-to/plan/index.md | Planning entry point. |
| setup/upgrading.md | Upgrading Riak KV | 732 | merge | how-to/operate/upgrade-cluster.md | Upgrade overview. |
| setup/upgrading/checklist.md | Production Checklist | 10693 | merge | how-to/operate/upgrade-cluster.md | Upgrade readiness checklist. |
| setup/upgrading/cluster.md | Upgrading a Cluster | 8492 | merge | how-to/operate/upgrade-cluster.md | Cluster upgrade procedure. |
| setup/upgrading/multi-datacenter.md | Upgrading Multi-Datacenter | 413 | merge | how-to/operate/upgrade-cluster.md | Multi-datacenter upgrade considerations. |
| setup/upgrading/version.md | Upgrading to Riak KV 3.2.5 | 10077 | version-specific |  | Instructions specifically for upgrading to 3.2.5 are not copied into 3.4 version pages. |
| using.md | Using Riak KV | 1871 | migrate | how-to/operate/index.md | Operations section introduction. |
| using/admin.md | Cluster Administration | 1285 | merge | reference/commands/index.md | Administration command overview. |
| using/admin/commands.md | Cluster Administration Commands | 14444 | merge | reference/commands/index.md | Administration command list. |
| using/admin/riak-admin.md | riak admin Command Line Interface | 23999 | migrate | reference/commands/riak-admin.md | riak-admin command reference. |
| using/admin/riak-cli.md | riak Command Line Interface | 6723 | migrate | reference/commands/riak.md | riak command reference. |
| using/admin/riak-control.md | Riak Control | 8175 | migrate | reference/commands/riak-control.md | Riak Control reference. |
| using/cluster-operations.md | Cluster Operations | 2342 | merge | how-to/operate/index.md | Cluster operations overview. |
| using/cluster-operations/active-anti-entropy.md | Legacy Active Anti-Entropy | 8859 | merge | how-to/operate/monitor-active-anti-entropy.md | AAE operations. |
| using/cluster-operations/adding-removing-nodes.md | Adding / Removing Nodes | 7203 | merge | tutorials/operations/change-cluster-membership.md | Combined node membership procedure. |
| using/cluster-operations/backend.md | Backend | 352 | merge | how-to/configure/backends/change-backend.md | Backend operation navigation. |
| using/cluster-operations/backing-up.md | Backing Up | 10332 | migrate | how-to/operate/back-up-node.md | Backup procedure. |
| using/cluster-operations/bucket-types.md | Bucket Types | 2114 | migrate | how-to/operate/manage-bucket-types.md | Bucket-type administration. |
| using/cluster-operations/changing-cluster-info.md | Changing Cluster Information | 18633 | migrate | how-to/operate/change-cluster-information.md | Cluster identity changes. |
| using/cluster-operations/handoff.md | Enabling and Disabling Handoff | 3963 | migrate | how-to/operate/manage-handoffs.md | Handoff operation. |
| using/cluster-operations/inspecting-node.md | Inspecting a Node | 28529 | merge | how-to/operate/inspect-node-and-cluster.md | Node inspection. |
| using/cluster-operations/load-balancing.md | Load Balancing | 410 | merge | how-to/configure/load-balancing-proxy.md | Load-balancing navigation. |
| using/cluster-operations/logging.md | Enabling and Disabling Debug Logging | 1554 | migrate | how-to/operate/change-log-level.md | Runtime debug logging. |
| using/cluster-operations/replacing-node.md | Replacing a Node | 3534 | migrate | how-to/operate/replace-node.md | Node replacement. |
| using/cluster-operations/secondary-indexes.md | Secondary Indexes | 3093 | merge | how-to/troubleshoot/repair-secondary-indexes.md | Secondary-index operations. |
| using/cluster-operations/strong-consistency.md | Monitoring Strong Consistency | 4567 | merge | explanation/consistency/strong-consistency.md | Strong-consistency monitoring details. |
| using/cluster-operations/tictac-aae-fold.md | TicTac AAE Folds | 8272 | merge | how-to/operate/aae-fold/index.md | AAE fold overview. |
| using/cluster-operations/tictac-aae-fold/count-keys.md | Count Keys | 4641 | migrate | how-to/operate/aae-fold/count-keys.md | TicTac AAE fold operation. |
| using/cluster-operations/tictac-aae-fold/count-tombs.md | Count Tombstones | 4736 | migrate | how-to/operate/aae-fold/count-tombstones.md | TicTac AAE fold operation. |
| using/cluster-operations/tictac-aae-fold/erase-keys.md | Erase Keys | 4734 | migrate | how-to/operate/aae-fold/erase-keys.md | TicTac AAE fold operation. |
| using/cluster-operations/tictac-aae-fold/filters.md | Filters | 7890 | migrate | reference/aae-fold-api/filters.md | TicTac AAE fold operation. |
| using/cluster-operations/tictac-aae-fold/find-keys.md | Find keys | 6968 | migrate | how-to/operate/aae-fold/find-keys.md | TicTac AAE fold operation. |
| using/cluster-operations/tictac-aae-fold/find-tombs.md | Find Tombstones | 4030 | migrate | how-to/operate/aae-fold/find-tombstones.md | TicTac AAE fold operation. |
| using/cluster-operations/tictac-aae-fold/list-buckets.md | List Buckets | 2800 | migrate | how-to/operate/aae-fold/list-buckets.md | TicTac AAE fold operation. |
| using/cluster-operations/tictac-aae-fold/object-stats.md | Get Object Statistics | 4880 | migrate | how-to/operate/aae-fold/object-statistics.md | TicTac AAE fold operation. |
| using/cluster-operations/tictac-aae-fold/reap-tombs.md | Reap Tombstones | 4742 | migrate | how-to/operate/aae-fold/reap-tombstones.md | TicTac AAE fold operation. |
| using/cluster-operations/tictac-aae-fold/repair-keys-range.md | Repair Keys | 4122 | migrate | how-to/operate/aae-fold/repair-key-range.md | TicTac AAE fold operation. |
| using/cluster-operations/tictac-active-anti-entropy.md | TicTac Active Anti-Entropy | 1599 | merge | how-to/operate/monitor-active-anti-entropy.md | TicTac AAE operation. |
| using/cluster-operations/v2-multi-datacenter.md | Replication Operations | 11102 | merge | reference/replication-api/runtime-controls.md | Legacy replication runtime operations. |
| using/cluster-operations/v3-multi-datacenter.md | Replication Operations | 12299 | merge | reference/replication-api/runtime-controls.md | Replication runtime operations. |
| using/performance.md | Improving Performance | 9733 | merge | how-to/tune/index.md | Performance overview. |
| using/performance/amazon-web-services.md | Amazon Web Services Performance Tuning | 10508 | migrate | how-to/tune/tune-aws-deployment.md | AWS tuning. |
| using/performance/benchmarking.md | Benchmarking | 19116 | migrate | how-to/tune/benchmark-cluster.md | Benchmarking. |
| using/performance/erlang.md | Erlang VM Tuning | 16831 | migrate | how-to/tune/tune-erlang-vm.md | Erlang VM tuning. |
| using/performance/latency-reduction.md | Latency Reduction Checklist | 14433 | migrate | how-to/tune/reduce-latency.md | Latency reduction. |
| using/performance/multi-datacenter-tuning.md | System Tuning | 1318 | migrate | how-to/tune/tune-multi-datacenter.md | Multi-datacenter tuning. |
| using/performance/open-files-limit.md | Open Files Limit | 9310 | migrate | how-to/tune/set-open-files-limit.md | Open-files tuning. |
| using/performance/v2-scheduling-fullsync.md | V2 Scheduling Fullsync | 1280 | merge | how-to/configure/replication/configure-fullsync.md | Legacy Fullsync scheduling. |
| using/reference.md | Riak KV Usage Reference | 2647 | merge | reference/operations/index.md | Operations reference overview. |
| using/reference/architecture.md | Architecture Reference | 357 | merge | explanation/foundations/clusters-rings-and-partitions.md | Architecture navigation. |
| using/reference/bucket-types.md | Bucket Types | 26053 | merge | reference/data/buckets-and-bucket-types.md | Bucket-type reference. |
| using/reference/custom-code.md | Installing Custom Code | 5100 | migrate | reference/operations/custom-code.md | Custom code constraints. |
| using/reference/failure-recovery.md | Failure & Recovery Reference | 3092 | merge | explanation/operations/node-failure-and-recovery.md | Failure recovery reference. |
| using/reference/handoff.md | Handoff Reference | 6060 | migrate | reference/operations/handoff.md | Handoff reference. |
| using/reference/jmx.md | JMX Monitoring | 5518 | migrate | reference/operations/jmx.md | JMX integration. |
| using/reference/logging.md | Logging Reference | 9891 | merge | reference/operations/log-files.md | Logging reference. |
| using/reference/multi-datacenter.md | Multi-Datacenter Reference | 1211 | merge | explanation/replication/multi-datacenter-architecture.md | Multi-datacenter reference overview. |
| using/reference/multi-datacenter/comparison.md | Multi-Datacenter Replication Reference: Comparsion | 4709 | migrate | reference/operations/multi-datacenter-comparison.md | Replication feature comparison. |
| using/reference/multi-datacenter/monitoring.md | Multi-Datacenter Replication Reference: Monitoring | 7820 | merge | reference/operations/statistics-and-monitoring.md | Replication monitoring. |
| using/reference/multi-datacenter/per-bucket-replication.md | Multi-Datacenter Replication Reference: Per Bucket | 1862 | merge | explanation/replication/references-and-triggers.md | Per-bucket replication behavior. |
| using/reference/multi-datacenter/statistics.md | Multi-Datacenter Replication Reference: Statistics | 15238 | migrate | reference/operations/replication-statistics.md | Replication statistics. |
| using/reference/object-deletion.md | Object Deletion Reference | 7798 | migrate | reference/operations/object-deletion.md | Object deletion reference. |
| using/reference/runtime-interaction.md | Runtime Interaction Reference | 2623 | migrate | reference/operations/remote-console.md | Runtime interaction reference. |
| using/reference/secondary-indexes.md | Secondary Indexes Reference | 3395 | merge | reference/data/secondary-indexes.md | Secondary-index reference. |
| using/reference/snmp.md | Simple Network Management Protocol | 4571 | migrate | reference/operations/snmp.md | SNMP integration. |
| using/reference/statistics-monitoring.md | Statistics & Monitoring Reference | 16899 | migrate | reference/operations/statistics-and-monitoring.md | Statistics and monitoring. |
| using/reference/strong-consistency.md | Strong Consistency Reference | 7014 | merge | reference/specialized-apis/strong-consistency-api.md | Strong-consistency reference. |
| using/reference/v2-multi-datacenter.md | V2 Multi-Datacenter Replication Reference | 1024 | merge | explanation/replication/v2-and-v3-replication.md | Legacy v2 replication reference. |
| using/reference/v2-multi-datacenter/architecture.md | V2 Multi-Datacenter Replication Reference: Architecture | 5281 | merge | explanation/replication/multi-datacenter-architecture.md | Legacy replication architecture. |
| using/reference/v2-multi-datacenter/scheduling-fullsync.md | V2 Multi-Datacenter Replication Reference: Scheduling Fullsync | 1387 | merge | how-to/configure/replication/configure-fullsync.md | Legacy Fullsync scheduling. |
| using/reference/v3-multi-datacenter.md | V3 Multi-Datacenter Replication Reference | 1237 | merge | explanation/replication/v2-and-v3-replication.md | V3 replication reference. |
| using/reference/v3-multi-datacenter/aae.md | Fullsync via Active Anti-Entropy | 4813 | merge | explanation/replication/real-time-and-fullsync.md | AAE-driven Fullsync. |
| using/reference/v3-multi-datacenter/architecture.md | Architecture | 5813 | merge | explanation/replication/multi-datacenter-architecture.md | Replication architecture. |
| using/reference/v3-multi-datacenter/cascading-writes.md | Cascading Realtime Writes | 3083 | migrate | explanation/replication/cascading-writes.md | Cascading writes. |
| using/reference/v3-multi-datacenter/scheduling-fullsync.md | Scheduling Fullsync | 2170 | merge | how-to/configure/replication/configure-fullsync.md | Fullsync scheduling. |
| using/repair-recovery.md | Repair & Recovery | 1064 | merge | explanation/operations/node-failure-and-recovery.md | Repair and recovery overview. |
| using/repair-recovery/errors.md | Errors & Messages | 34450 | create | reference/operations/errors-and-messages.md | Error and message reference missing from the new scaffold. |
| using/repair-recovery/failed-node.md | Recovering a Failed Node | 3104 | migrate | how-to/troubleshoot/recover-failed-node.md | Failed-node recovery. |
| using/repair-recovery/failure-recovery.md | Failure & Recovery | 6263 | migrate | how-to/troubleshoot/recover-cluster-failure.md | Failure recovery. |
| using/repair-recovery/repairs.md | Repairs | 13768 | merge | explanation/operations/repair-granularity.md | Repair behavior and scope. |
| using/repair-recovery/rolling-replaces.md | Rolling Replaces | 1797 | migrate | how-to/operate/rolling-replacement.md | Rolling replacement. |
| using/repair-recovery/rolling-restart.md | Rolling Restarts | 1823 | migrate | how-to/operate/rolling-restart.md | Rolling restart. |
| using/repair-recovery/secondary-indexes.md | Repairing Secondary Indexes | 5418 | merge | how-to/troubleshoot/repair-secondary-indexes.md | Secondary-index repair. |
| using/running-a-cluster.md | Running a Cluster | 11830 | merge | how-to/operate/index.md | Running-cluster overview. |
| using/security.md | Security & Firewalls | 6845 | merge | how-to/secure/index.md | Security and firewall overview. |
| using/security/basics.md | Security Basics | 28490 | migrate | how-to/secure/enable-security.md | Security setup. |
| using/security/best-practices.md | Security Best Practices | 3082 | create | how-to/secure/best-practices.md | Security best-practices page missing from the new scaffold. |
| using/security/managing-sources.md | Managing Security Sources | 10299 | migrate | how-to/secure/manage-sources.md | Authentication source management. |
| using/security/v2-v3-ssl-ca.md | V2 / V3 SSL & CA Validation | 3093 | merge | how-to/configure/replication/secure-replication.md | Replication certificate validation. |
| using/troubleshooting.md | Troubleshooting | 434 | merge | how-to/troubleshoot/index.md | Troubleshooting overview. |
| using/troubleshooting/http-204.md | HTTP 204 | 610 | migrate | how-to/troubleshoot/http-204.md | HTTP 204 troubleshooting. |

## Complete destination ledger

| Diátaxis destination | Legacy source pages | Created from legacy | 3.4.0 | 3.4.1 |
|---|---|---|---|---|
| explanation/consistency/eventual-consistency.md | learn/concepts/eventual-consistency.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/consistency/strong-consistency.md | learn/concepts/strong-consistency.md<br>using/cluster-operations/strong-consistency.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/data-model/causal-context.md | learn/concepts/causal-context.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/data-model/distributed-data-types.md | learn/concepts/crdts.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/data-model/keys-objects-and-buckets.md | learn/concepts/buckets.md<br>learn/concepts/keys-and-objects.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/foundations/capability-negotiation.md | learn/concepts/capability-negotiation.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/foundations/clusters-rings-and-partitions.md | learn/concepts/clusters.md<br>using/reference/architecture.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/foundations/dynamo-model.md | learn/dynamo.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/foundations/glossary.md | learn/glossary.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/foundations/index.md | learn.md<br>learn/concepts.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/foundations/new-to-nosql.md | learn/new-to-nosql.md | True | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/foundations/use-cases.md | learn/use-cases.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/foundations/virtual-nodes.md | learn/concepts/vnodes.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/foundations/why-openriak.md | learn/why-riak-kv.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/operations/node-failure-and-recovery.md | using/reference/failure-recovery.md<br>using/repair-recovery.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/operations/repair-granularity.md | using/repair-recovery/repairs.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/replication/active-anti-entropy.md | learn/concepts/active-anti-entropy.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/replication/cascading-writes.md | using/reference/v3-multi-datacenter/cascading-writes.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/replication/index.md | developing/usage/replication.md<br>learn/concepts/replication.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/replication/multi-datacenter-architecture.md | using/reference/multi-datacenter.md<br>using/reference/v2-multi-datacenter/architecture.md<br>using/reference/v3-multi-datacenter/architecture.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/replication/next-generation-replication.md | developing/usage/next-gen-replication.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/replication/real-time-and-fullsync.md | using/reference/v3-multi-datacenter/aae.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/replication/references-and-triggers.md | developing/app-guide/replication-properties.md<br>using/reference/multi-datacenter/per-bucket-replication.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/replication/v2-and-v3-replication.md | using/reference/v2-multi-datacenter.md<br>using/reference/v3-multi-datacenter.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/storage/bitcask.md | setup/planning/backend/bitcask.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/storage/capacity-planning.md | setup/planning/bitcask-capacity-calc.md<br>setup/planning/cluster-capacity.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/storage/choosing-backend.md | setup/planning/backend.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/storage/leveldb.md | setup/planning/backend/leveldb.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/storage/leveled.md | setup/planning/backend/leveled.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/storage/memory.md | setup/planning/backend/memory.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| explanation/storage/multi-backend.md | setup/planning/backend/multi.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/backends/change-backend.md | using/cluster-operations/backend.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/backends/index.md | configuring/backend.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/basic-node-settings.md | configuring/basic.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/global-object-expiration.md | configuring/global-object-expiration.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/index.md | configuring.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/load-balancing-proxy.md | configuring/load-balancing-proxy.md<br>using/cluster-operations/load-balancing.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/manage-configuration.md | configuring/managing.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/mapreduce.md | configuring/mapreduce.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/replication/configure-fullsync.md | configuring/next-gen-replication/fullsync.md<br>using/performance/v2-scheduling-fullsync.md<br>using/reference/v2-multi-datacenter/scheduling-fullsync.md<br>using/reference/v3-multi-datacenter/scheduling-fullsync.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/replication/configure-legacy-aae.md | configuring/active-anti-entropy/legacy-aae.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/replication/configure-next-generation-replication.md | configuring/next-gen-replication.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/replication/configure-real-time-replication.md | configuring/next-gen-replication/realtime.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/replication/configure-replication-queues.md | configuring/next-gen-replication/queuing.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/replication/configure-replication-through-nat.md | configuring/v2-multi-datacenter/nat.md<br>configuring/v3-multi-datacenter/nat.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/replication/configure-sink-nodes.md | configuring/next-gen-replication/sink.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/replication/configure-v2-multi-datacenter.md | configuring/v2-multi-datacenter.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/replication/configure-v3-multi-datacenter.md | configuring/v3-multi-datacenter.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/replication/enable-tictac-aae.md | configuring/active-anti-entropy/tictac-aae.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/replication/secure-replication.md | configuring/v2-multi-datacenter/ssl.md<br>configuring/v3-multi-datacenter/ssl.md<br>using/security/v2-v3-ssl-ca.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/configure/strong-consistency.md | configuring/strong-consistency.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/authenticate-client.md | developing/usage/security.md<br>developing/usage/security/erlang.md<br>developing/usage/security/java.md<br>developing/usage/security/php.md<br>developing/usage/security/python.md<br>developing/usage/security/ruby.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/create-object.md | developing/usage/creating-objects.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/delete-object.md | developing/usage/deleting-objects.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/index.md | developing.md<br>developing/usage.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/query-secondary-indexes.md | developing/usage/secondary-indexes.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/read-object.md | developing/usage/reading-objects.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/resolve-conflicts.md | developing/usage/conflict-resolution.md<br>developing/usage/conflict-resolution/csharp.md<br>developing/usage/conflict-resolution/golang.md<br>developing/usage/conflict-resolution/java.md<br>developing/usage/conflict-resolution/nodejs.md<br>developing/usage/conflict-resolution/php.md<br>developing/usage/conflict-resolution/python.md<br>developing/usage/conflict-resolution/ruby.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/run-mapreduce.md | developing/app-guide/advanced-mapreduce.md<br>developing/usage/mapreduce.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/update-object.md | developing/usage/updating-objects.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/use-bucket-types.md | developing/usage/bucket-types.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/use-content-types.md | developing/usage/content-types.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/use-counters.md | developing/data-types/counters.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/use-gsets.md | developing/data-types/gsets.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/use-hyperloglogs.md | developing/data-types/hyperloglogs.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/use-maps.md | developing/data-types/maps.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/use-sets.md | developing/data-types/sets.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/write-commit-hook.md | developing/usage/commit-hooks.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/develop/write-replication-hook.md | developing/api/repl-hooks.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/install/alpine-linux.md | setup/installing/alpine-linux.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/install/amazon-linux.md | setup/installing/amazon-web-services.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/install/debian-ubuntu.md | setup/installing/debian-ubuntu.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/install/index.md | setup.md<br>setup/installing.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/install/rhel-rocky.md | setup/installing/oracle-linux.md<br>setup/installing/rhel-centos.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/install/source.md | setup/installing/source.md<br>setup/installing/source/erlang.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/install/verify-installation.md | setup/installing/verify.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/aae-fold/count-keys.md | using/cluster-operations/tictac-aae-fold/count-keys.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/aae-fold/count-tombstones.md | using/cluster-operations/tictac-aae-fold/count-tombs.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/aae-fold/erase-keys.md | using/cluster-operations/tictac-aae-fold/erase-keys.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/aae-fold/find-keys.md | using/cluster-operations/tictac-aae-fold/find-keys.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/aae-fold/find-tombstones.md | using/cluster-operations/tictac-aae-fold/find-tombs.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/aae-fold/index.md | using/cluster-operations/tictac-aae-fold.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/aae-fold/list-buckets.md | using/cluster-operations/tictac-aae-fold/list-buckets.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/aae-fold/object-statistics.md | using/cluster-operations/tictac-aae-fold/object-stats.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/aae-fold/reap-tombstones.md | using/cluster-operations/tictac-aae-fold/reap-tombs.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/aae-fold/repair-key-range.md | using/cluster-operations/tictac-aae-fold/repair-keys-range.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/back-up-node.md | using/cluster-operations/backing-up.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/change-cluster-information.md | using/cluster-operations/changing-cluster-info.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/change-log-level.md | using/cluster-operations/logging.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/downgrade-cluster.md | setup/downgrade.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/index.md | using.md<br>using/cluster-operations.md<br>using/running-a-cluster.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/inspect-node-and-cluster.md | using/cluster-operations/inspecting-node.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/manage-bucket-types.md | using/cluster-operations/bucket-types.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/manage-handoffs.md | using/cluster-operations/handoff.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/monitor-active-anti-entropy.md | using/cluster-operations/active-anti-entropy.md<br>using/cluster-operations/tictac-active-anti-entropy.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/replace-node.md | using/cluster-operations/replacing-node.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/rolling-replacement.md | using/repair-recovery/rolling-replaces.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/rolling-restart.md | using/repair-recovery/rolling-restart.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/operate/upgrade-cluster.md | setup/upgrading.md<br>setup/upgrading/checklist.md<br>setup/upgrading/cluster.md<br>setup/upgrading/multi-datacenter.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/plan/index.md | setup/planning.md<br>setup/planning/start.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/plan/map-data-to-objects.md | developing/data-modeling.md<br>developing/key-value-modeling.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/plan/production-readiness-checklist.md | setup/planning/best-practices.md<br>setup/planning/future.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/redis-add-on/develop.md | add-ons/redis/developing-rra.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/redis-add-on/index.md | add-ons.md<br>add-ons/redis.md<br>add-ons/redis/redis-add-on-features.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/redis-add-on/set-up.md | add-ons/redis/set-up-rra.md<br>add-ons/redis/set-up-rra/deployment-models.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/redis-add-on/use.md | add-ons/redis/using-rra.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/secure/best-practices.md | using/security/best-practices.md | True | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/secure/enable-security.md | using/security/basics.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/secure/index.md | using/security.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/secure/manage-sources.md | using/security/managing-sources.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/troubleshoot/http-204.md | using/troubleshooting/http-204.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/troubleshoot/index.md | using/troubleshooting.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/troubleshoot/recover-cluster-failure.md | using/repair-recovery/failure-recovery.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/troubleshoot/recover-failed-node.md | using/repair-recovery/failed-node.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/troubleshoot/repair-secondary-indexes.md | using/cluster-operations/secondary-indexes.md<br>using/repair-recovery/secondary-indexes.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/tune/benchmark-cluster.md | using/performance/benchmarking.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/tune/index.md | using/performance.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/tune/reduce-latency.md | using/performance/latency-reduction.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/tune/set-open-files-limit.md | using/performance/open-files-limit.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/tune/tune-aws-deployment.md | using/performance/amazon-web-services.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/tune/tune-erlang-vm.md | using/performance/erlang.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| how-to/tune/tune-multi-datacenter.md | using/performance/multi-datacenter-tuning.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| index.md | index.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/aae-fold-api/filters.md | using/cluster-operations/tictac-aae-fold/filters.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/client-libraries/index.md | developing/client-libraries.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/commands/index.md | using/admin.md<br>using/admin/commands.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/commands/riak-admin.md | using/admin/riak-admin.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/commands/riak-control.md | using/admin/riak-control.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/commands/riak.md | using/admin/riak-cli.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/configuration/active-anti-entropy.md | configuring/active-anti-entropy.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/configuration/index.md | configuring/reference.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/configuration/replication.md | configuring/next-gen-replication/reference.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/data/buckets-and-bucket-types.md | using/reference/bucket-types.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/data/distributed-data-types.md | developing/data-types.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/data/secondary-indexes.md | using/reference/secondary-indexes.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/faq.md | developing/faq.md | True | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/http-api/counters.md | developing/api/http/counters.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/http-api/delete-object.md | developing/api/http/delete-object.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/http-api/fetch-object.md | developing/api/http/fetch-object.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/http-api/get-bucket-properties.md | developing/api/http/get-bucket-props.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/http-api/index.md | developing/api/http.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/http-api/link-walking.md | developing/api/http/link-walking.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/http-api/list-buckets.md | developing/api/http/list-buckets.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/http-api/list-keys.md | developing/api/http/list-keys.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/http-api/list-resources.md | developing/api/http/list-resources.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/http-api/mapreduce.md | developing/api/http/mapreduce.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/http-api/ping.md | developing/api/http/ping.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/http-api/reset-bucket-properties.md | developing/api/http/reset-bucket-props.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/http-api/secondary-indexes.md | developing/api/http/secondary-indexes.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/http-api/set-bucket-properties.md | developing/api/http/set-bucket-props.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/http-api/status.md | developing/api/http/status.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/http-api/store-object.md | developing/api/http/store-object.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/index.md | developing/api.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/operations/custom-code.md | using/reference/custom-code.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/operations/errors-and-messages.md | using/repair-recovery/errors.md | True | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/operations/handoff.md | using/reference/handoff.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/operations/index.md | using/reference.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/operations/jmx.md | using/reference/jmx.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/operations/log-files.md | using/reference/logging.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/operations/multi-datacenter-comparison.md | using/reference/multi-datacenter/comparison.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/operations/object-deletion.md | using/reference/object-deletion.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/operations/remote-console.md | using/reference/runtime-interaction.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/operations/replication-statistics.md | using/reference/multi-datacenter/statistics.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/operations/snmp.md | using/reference/snmp.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/operations/statistics-and-monitoring.md | using/reference/multi-datacenter/monitoring.md<br>using/reference/statistics-monitoring.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/authentication.md | developing/api/protocol-buffers/auth-req.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/client-id.md | developing/api/protocol-buffers/get-client-id.md<br>developing/api/protocol-buffers/set-client-id.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/coverage-queries.md | developing/api/protocol-buffers/coverage-queries.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/delete-object.md | developing/api/protocol-buffers/delete-object.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/fetch-data-type.md | developing/api/protocol-buffers/dt-fetch.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/fetch-object.md | developing/api/protocol-buffers/fetch-object.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/get-bucket-properties.md | developing/api/protocol-buffers/get-bucket-props.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/get-bucket-type.md | developing/api/protocol-buffers/get-bucket-type.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/index.md | developing/api/protocol-buffers.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/list-buckets.md | developing/api/protocol-buffers/list-buckets.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/list-keys.md | developing/api/protocol-buffers/list-keys.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/mapreduce.md | developing/api/protocol-buffers/mapreduce.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/ping.md | developing/api/protocol-buffers/ping.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/reset-bucket-properties.md | developing/api/protocol-buffers/reset-bucket-props.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/secondary-indexes.md | developing/api/protocol-buffers/secondary-indexes.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/server-information.md | developing/api/protocol-buffers/server-info.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/set-bucket-properties.md | developing/api/protocol-buffers/set-bucket-props.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/set-bucket-type.md | developing/api/protocol-buffers/set-bucket-type.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/store-data-type.md | developing/api/protocol-buffers/dt-store.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/store-object.md | developing/api/protocol-buffers/store-object.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/union-data-type.md | developing/api/protocol-buffers/dt-union.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/update-counter.md | developing/api/protocol-buffers/dt-counter-store.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/update-map.md | developing/api/protocol-buffers/dt-map-store.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/protocol-buffers/update-set.md | developing/api/protocol-buffers/dt-set-store.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/releases/deprecations.md | deprecated/riak-search.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/releases/supported-platforms.md | setup/planning/operating-system.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/replication-api/runtime-controls.md | using/cluster-operations/v2-multi-datacenter.md<br>using/cluster-operations/v3-multi-datacenter.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/specialized-apis/backend-api.md | developing/api/backend.md | True | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/specialized-apis/cluster-metadata.md | developing/app-guide/cluster-metadata.md | True | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/specialized-apis/index.md | developing/app-guide/reference.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/specialized-apis/strong-consistency-api.md | developing/app-guide/strong-consistency.md<br>using/reference/strong-consistency.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| reference/specialized-apis/write-once-api.md | developing/app-guide/write-once.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| tutorials/first-application/csharp.md | developing/getting-started/csharp.md<br>developing/getting-started/csharp/crud-operations.md<br>developing/getting-started/csharp/object-modeling.md<br>developing/getting-started/csharp/querying.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| tutorials/first-application/erlang.md | developing/getting-started/erlang.md<br>developing/getting-started/erlang/crud-operations.md<br>developing/getting-started/erlang/object-modeling.md<br>developing/getting-started/erlang/querying.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| tutorials/first-application/golang.md | developing/getting-started/golang.md<br>developing/getting-started/golang/crud-operations.md<br>developing/getting-started/golang/object-modeling.md<br>developing/getting-started/golang/querying.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| tutorials/first-application/index.md | developing/app-guide.md<br>developing/getting-started.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| tutorials/first-application/java.md | developing/getting-started/java.md<br>developing/getting-started/java/crud-operations.md<br>developing/getting-started/java/object-modeling.md<br>developing/getting-started/java/querying.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| tutorials/first-application/nodejs.md | developing/getting-started/nodejs.md<br>developing/getting-started/nodejs/crud-operations.md<br>developing/getting-started/nodejs/object-modeling.md<br>developing/getting-started/nodejs/querying.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| tutorials/first-application/php.md | developing/getting-started/php.md<br>developing/getting-started/php/crud-operations.md<br>developing/getting-started/php/querying.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| tutorials/first-application/python.md | developing/getting-started/python.md<br>developing/getting-started/python/crud-operations.md<br>developing/getting-started/python/object-modeling.md<br>developing/getting-started/python/querying.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| tutorials/first-application/ruby.md | developing/getting-started/ruby.md<br>developing/getting-started/ruby/crud-operations.md<br>developing/getting-started/ruby/object-modeling.md<br>developing/getting-started/ruby/querying.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| tutorials/operations/change-cluster-membership.md | using/cluster-operations/adding-removing-nodes.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |
| tutorials/replication/two-cluster-replication.md | configuring/v2-multi-datacenter/quick-start.md<br>configuring/v3-multi-datacenter/quick-start.md | False | migrated-needs-review, draft=True | migrated-needs-review, draft=True |

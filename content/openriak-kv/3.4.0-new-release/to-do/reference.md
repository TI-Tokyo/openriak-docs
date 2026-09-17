---
title: 'Reference'
description: "Complete proposed Reference structure: 136 lookup pages in 13 subsections."
weight: 30
recommendations: true
product: 'OpenRiak KV'
product_version: '3.4.0'
---

This is the complete proposed **Reference** structure for OpenRiak KV 3.4.0. It includes retained, reorganised, and new pages. Each row names one proposed lookup page and the contract or facts it should document.

The proposal covers **136 pages in 13 subsections**, based on the existing 129 Reference files, including 13 landing pages. [Diátaxis reference](https://diataxis.fr/reference/) describes the product precisely and consistently, so readers can find an authoritative answer while working.

Each subsection also has a short landing page with an index of its interfaces or topics. Describe the verified 3.4.0 implementation and distinguish public contracts, internal interfaces, and legacy or experimental features.

## Proposed pages

### Orientation and compatibility

| Section | Name | Explanation |
| --- | --- | --- |
| Orientation and compatibility | Glossary | Define the terminology used across the documentation and link each substantial concept to its Foundations explanation. |
| Orientation and compatibility | Platforms, architectures, and Erlang/OTP compatibility | Record the verified platform, package, architecture, and runtime combinations for this release, including applicable lifecycle information. |
| Orientation and compatibility | Cluster, client, and replication compatibility | State supported mixed-version combinations, protocol and client constraints, and upgrade or downgrade boundaries. |
| Orientation and compatibility | Feature status and deprecations | Identify current, legacy, experimental, deprecated, and removed features with release applicability and links to alternatives. |
| Orientation and compatibility | Replication-generation compatibility | Compare next-generation replication and legacy v2/v3 capabilities, wire compatibility, topology constraints, and migration boundaries. |
| Orientation and compatibility | Backend capability matrix | Record each backend's persistence, indexing, data-type, expiry, and operational capabilities for the documented release. |

### Configuration

| Section | Name | Explanation |
| --- | --- | --- |
| Configuration | All configuration settings and defaults | Provide the searchable generated defaults table as the complete setting index, with names, descriptions, types, constraints, and platform-specific defaults. |
| Configuration | Configuration files, syntax, and precedence | Define riak.conf and advanced.config syntax, supported value forms, precedence, validation, and restart requirements. |
| Configuration | Node identity, directories, and ring settings | Describe node names, cookies, paths, ring creation, and related node settings using filtered generated configuration metadata. |
| Configuration | Listeners and networking settings | Define client and inter-node listeners, addresses, ports, socket controls, and applicable network limits. |
| Configuration | Erlang VM and runtime settings | List supported scheduler, process, port, memory, distribution, and shutdown settings with their types, units, and applicability. |
| Configuration | Runtime environment variables | Catalogue supported variables, their meanings, resolution rules, and interactions with configuration files and service startup. |
| Configuration | Bucket properties and defaults | Define every supported bucket and bucket-type property, inheritance rules, allowed combinations, and effective defaults. |
| Configuration | Bitcask settings | Provide generated definitions for storage, I/O, key-directory, merge, expiry, and other Bitcask settings available in this release. |
| Configuration | Leveled settings | Provide generated definitions for journal, ledger, caches, compaction, snapshots, and other supported Leveled settings. |
| Configuration | TicTac anti-entropy settings | Define current tree, exchange, scheduling, and repair controls; distinguish legacy settings through explicit links and applicability. |
| Configuration | Next-generation replication settings | Define source queues, real-time replication, fullsync, sink consumers, and transport settings from the release metadata. |
| Configuration | Repair and handoff settings | Specify repair, transfer, concurrency, throttling, and background-work controls and their interaction constraints. |
| Configuration | Authentication, authorization, and TLS settings | Define supported security settings, value formats, trust configuration, and applicability to each interface. |
| Configuration | Logging and handler settings | Define log destinations, levels, rotation, category routing, and structured handler configuration using generated values. |
| Configuration | Object expiration and reclamation settings | Catalogue expiration, tombstone retention, erasure, and reaping controls, distinguishing their scopes and units. |
| Configuration | Query execution settings | Define configurable query timeouts, buffers, worker limits, and other supported query controls, linking request-specific fields to the API reference. |

### Commands

| Section | Name | Explanation |
| --- | --- | --- |
| Commands | riak command | Define service, console, configuration, version, and process commands with syntax, options, exit behaviour, and concise output examples. |
| Commands | riak admin command index | Provide the complete administrative command index and shared invocation conventions, routing command families to their detailed pages. |
| Commands | Cluster membership commands | Define join, leave, replace, forced operations, plan, commit, clear, and membership-status commands and their arguments and states. |
| Commands | Bucket-type commands | Define type creation, activation, update, listing, and status commands, including validation failures and lifecycle constraints. |
| Commands | Security commands | Define user, group, source, permission, and security-status commands and their exact argument forms. |
| Commands | Handoff commands | Define transfer inspection and control commands, concurrency options, and the fields returned by status and detail output. |
| Commands | AAE commands | Define fold invocation, tree rebuild, status, completion, and output-file options available through the command line. |
| Commands | Vnode and backend status commands | Define vnode-status invocation, filters, fields, and backend-specific output without embedding an incident procedure. |
| Commands | Repair and recovery commands | Define supported node, vnode, index, backup, restore, and object-conversion commands with their applicability and return states. |
| Commands | Diagnostic commands | Define stat, status, diag, cluster-info, service checks, and other diagnostic command outputs and exit conditions. |

### Data model contracts

| Section | Name | Explanation |
| --- | --- | --- |
| Data model contracts | Keys and object representations | Define identifiers, namespaces, encodings, payload representation, size constraints, and transport-independent object fields. |
| Data model contracts | Buckets and bucket types | Define naming, addressing, lifecycle states, property inheritance, and type restrictions; link procedural administration to How-to. |
| Data model contracts | Media types and content encodings | Specify supported content-type and encoding metadata, serialization expectations, and protocol representations. |
| Data model contracts | Object metadata | Define user metadata, system metadata, index entries, timestamps, validators, and their scope and mutability. |
| Data model contracts | Causal-context and version-vector representations | Define how context is represented and transported, when it must be preserved, and how absent or invalid context is handled. |
| Data model contracts | Distributed data-type contracts | Catalogue each type, its operations, context requirements, nested-type rules, and backend or bucket prerequisites. |
| Data model contracts | Secondary-index terms and projected attributes | Define index names, term encodings, ordering, multi-valued entries, and projected-attribute representation. |
| Data model contracts | Deletion, tombstone, and expiration states | Define observable deletion states, retained metadata, expiry scope, and the interfaces that report or act on those states. |

### HTTP API

| Section | Name | Explanation |
| --- | --- | --- |
| HTTP API | HTTP conventions, authentication, and errors | Define URL structure, typed namespaces, authentication, headers, media types, status conventions, streaming, and shared error representations. |
| HTTP API | Fetch object | Specify GET and HEAD requests, conditional retrieval, context and sibling responses, not-found handling, and request options. |
| HTTP API | Store object | Specify PUT and POST forms, generated keys, request metadata, returned representations, write options, and failures. |
| HTTP API | Delete object | Specify the deletion request, context and acknowledgement options, response statuses, and repeated-deletion behaviour. |
| HTTP API | Conditional requests and latch objects | Define supported validators and preconditions, latch-related request forms, success and failure responses, and consistency boundaries. |
| HTTP API | Object request options | Catalogue read and write parameters, accepted values, per-request overrides, defaults, and relationships to bucket policies. |
| HTTP API | Bucket property operations | Specify property retrieval, modification, and reset requests, including typed-bucket paths, response fields, and validation errors. |
| HTTP API | Bucket-type operations | Document the HTTP operations actually exposed for bucket types, their request forms, and the operations requiring administrative commands instead. |
| HTTP API | Distributed data-type operations | Specify HTTP fetch and update representations for the supported data types, including operations, context, responses, and errors. |
| HTTP API | Secondary-index queries | Define exact and range requests, returned terms, continuation, streaming, request options, and error responses. |
| HTTP API | Ping | Define the health-check request and response and the limits of what a successful ping establishes. |
| HTTP API | Status and statistics | Define the status endpoint, response representation, collection controls, and links to metric definitions. |
| HTTP API | Resource discovery | Define resource-list requests, representations, content negotiation, and advertised links. |
| HTTP API | Legacy bucket and key listing | Preserve the list endpoints, streaming and pagination details, restrictions, and links to the current AAE fold alternatives. |
| HTTP API | Legacy HTTP counters | Define the older counter endpoint separately from the typed data API and state its compatibility and migration context. |
| HTTP API | Legacy HTTP link walking | Define link-walking syntax, representations, result handling, and release applicability for existing integrations. |
| HTTP API | HTTP MapReduce transport | Define job submission, content negotiation, streaming results, error responses, and links to the MapReduce job specification. |

### Protocol Buffers API

| Section | Name | Explanation |
| --- | --- | --- |
| Protocol Buffers API | Protocol framing, message codes, and errors | Define connection framing, message identifiers, serialization, streaming completion, and the shared error message contract. |
| Protocol Buffers API | Authentication messages | Define authentication and transport prerequisites, request fields, successful completion, and authentication failure responses. |
| Protocol Buffers API | Fetch object messages | Define request fields, read options, content and sibling responses, context, and not-found semantics. |
| Protocol Buffers API | Store object messages | Define content, key generation, write options, context handling, returned bodies, and response fields. |
| Protocol Buffers API | Delete object messages | Define bucket and key addressing, context, acknowledgement options, completion, and errors. |
| Protocol Buffers API | Bucket property messages | Define retrieval, update, and reset messages, property encodings, responses, and validation constraints. |
| Protocol Buffers API | Bucket-type messages | Define type-property lookup and update messages and their constraints relative to type creation and activation. |
| Protocol Buffers API | Fetch data-type messages | Define the type-aware fetch request, context and value fields, options, and errors. |
| Protocol Buffers API | Update data-type messages | Define the common data-type update envelope, operation encoding, context, return options, and response. |
| Protocol Buffers API | Counter operations | Define counter operation fields and their use within the common data-type update message. |
| Protocol Buffers API | Set operations | Define additions, removals, context requirements, and set operation encoding. |
| Protocol Buffers API | Map operations | Define typed field identifiers, nested operations, removals, and context requirements for map updates. |
| Protocol Buffers API | Grow-only and union operations | Define the documented union message and its type-specific fields, supported uses, and version applicability. |
| Protocol Buffers API | Secondary-index query messages | Define exact and range terms, returned keys or terms, streaming completion, continuation, and options. |
| Protocol Buffers API | Coverage-plan messages | Define coverage requests, plan entries, continuation or replacement details, and validity constraints. |
| Protocol Buffers API | Ping and server information messages | Define health and server-information requests, responses, and the fields identifying the responding server. |
| Protocol Buffers API | Legacy listing messages | Define bucket and key listing requests, streaming response completion, applicability, and links to current alternatives. |
| Protocol Buffers API | Legacy client identifier messages | Define get and set client-ID messages and explain their protocol applicability without promoting them as current causality controls. |
| Protocol Buffers API | MapReduce messages | Define job request encoding, phases, streamed results, completion, and errors for the Protocol Buffers transport. |

### Query API

| Section | Name | Explanation |
| --- | --- | --- |
| Query API | Endpoints and request schema | Define paths, JSON fields, required and optional values, substitutions, timeouts, validation, and default values. |
| Query API | Expression grammar and operators | Specify evaluation, filtering, aggregation, composition, supported operators, and Unicode rules with small syntax examples. |
| Query API | Accumulation modes | Define keys, terms, counts, grouped counts, raw variants, duplicate treatment, and the shape associated with each mode. |
| Query API | Responses and errors | Define response fields, ordering, result shapes, errors, and completion conditions for each supported delivery mode. |
| Query API | Continuations and result delivery | Specify continuation handling, pagination boundaries, asynchronous delivery where supported, and timeout or partial-result contracts. |
| Query API | Limits and behavioural constraints | Record actual limits, snapshot boundaries, timeout behaviour, and supported combinations; link performance rationale to Foundations. |

### AAE fold API

| Section | Name | Explanation |
| --- | --- | --- |
| AAE fold API | Fold invocation and result conventions | Define supported HTTP, Protocol Buffers, CLI, and console entry points, arguments, result envelopes, and completion handling. |
| AAE fold API | Fold filters | Define bucket, key range, segment, modification time, sibling-count, and object-size filters and their combination rules. |
| AAE fold API | List buckets | Define arguments and the bucket inventory result returned by the fold operation. |
| AAE fold API | Find keys | Define selection, object-size and sibling-count modes, result tuples, and applicable filters. |
| AAE fold API | Count keys | Define the documented counting mode, filters, and result shape without implying a separate API operation where counting is an option. |
| AAE fold API | Find tombstones | Define the tombstone-search operation, accepted filters, and the returned fields. |
| AAE fold API | Count tombstones | Define the documented count mode for tombstone operations, its filters, and the meaning of the count. |
| AAE fold API | Object statistics | Define the aggregate statistics returned by object_stats, including fields, units, filters, and empty-result behaviour. |
| AAE fold API | Repair keys in a range | Define the repair request, selected scope, result or job identifiers, completion, and restrictions. |
| AAE fold API | Erase keys | Define count and execution modes, scope, output, and the exact semantics of erasure. |
| AAE fold API | Reap tombstones | Define count and execution modes, eligibility requirements, arguments, and completion results. |
| AAE fold API | Replicate keys in a range | Specify the queue, range, and time-selection parameters for repl_keys_range and its result and completion behaviour. |
| AAE fold API | Tree and clock exchange operations | Define merge_root_nval, merge_branch_nval, fetch_clocks_nval, merge_tree_range, and fetch_clocks_range, including internal-use boundaries. |

### Replication interfaces

| Section | Name | Explanation |
| --- | --- | --- |
| Replication interfaces | Next-generation replication runtime controls | Define supported source, sink, queue, fullsync, and reconciliation controls separately from legacy riak_repl commands. |
| Replication interfaces | Replication references and queue payloads | Specify queued references, object versions, trigger behaviour, payload fields, and compatibility constraints. |
| Replication interfaces | Internal fetch and membership API | Define membership discovery and queue GET/POST contracts, marking the interface's internal status and version-sensitive boundaries. |
| Replication interfaces | Fullsync requests and results | Define current fullsync control parameters, result fields, status states, and selection or scheduling contracts. |
| Replication interfaces | Legacy riak_repl runtime controls | Preserve the legacy v2/v3 command families, arguments, states, and outputs under explicit generation labels. |

### Operations and observability

| Section | Name | Explanation |
| --- | --- | --- |
| Operations and observability | Node and cluster metrics | Catalogue current metric names, meanings, units, counter or gauge semantics, collection scope, and reset behaviour. |
| Operations and observability | Replication metrics | Separate current and legacy replication statistics and define queue, delivery, exchange, and fullsync measurements. |
| Operations and observability | AAE, repair, and worker-pool metrics | Define tree, exchange, repair, queue, wait-time, and worker measurements used by monitoring guides. |
| Operations and observability | Log files and event formats | Define log destinations, categories, event fields, structured representations, rotation artefacts, and timestamps. |
| Operations and observability | Error and diagnostic message catalogue | Catalogue stable errors and recognisable messages with meanings and links to the relevant troubleshooting procedure. |
| Operations and observability | Handoff states and transfer records | Define handoff types, ownership transitions, observable states, and status fields; keep control procedures in How-to. |
| Operations and observability | Claim algorithms and placement constraints | Describe version-specific algorithm choices, inputs, supported location constraints, guarantees, and compatibility. |
| Operations and observability | Remote-console interfaces | Define supported diagnostic entry points, arguments, returned structures, and boundaries between supported interfaces and implementation details. |
| Operations and observability | Runtime files and backup contents | Identify data, ring, metadata, configuration, journal, ledger, and backup artefacts, their purposes, and backend-specific relationships. |
| Operations and observability | SNMP objects and integration contract | Define exposed objects, metric mappings, configuration references, and the applicability of the integration to this release. |
| Operations and observability | JMX attributes and integration contract | Define exported attributes, metric mappings, connection details, and applicable component versions. |

### Client libraries

| Section | Name | Explanation |
| --- | --- | --- |
| Client libraries | Client compatibility and capability matrix | Record verified library versions, runtimes, protocols, authentication, data types, and feature coverage; distinguish maintained and legacy clients. |
| Client libraries | C# client | Record the tested package and runtime, connection options, API mapping, feature coverage, and upstream reference for C# integrations. |
| Client libraries | Erlang client | Record compatible client and OTP versions, connection configuration, operation mapping, and known protocol or feature constraints. |
| Client libraries | Go client | Record the tested module and Go version, connection settings, operation mapping, data-type support, and compatibility constraints. |
| Client libraries | Java client | Record tested dependency and Java versions, cluster and connection configuration, asynchronous behaviour, and supported API features. |
| Client libraries | Node.js client | Record the verified package and runtime, connection and error conventions, API coverage, and known limitations. |
| Client libraries | PHP client | Record verified Composer package and runtime requirements, supported transports, operation mapping, and feature limitations. |
| Client libraries | Python client | Record the verified package and Python runtime, transport and authentication requirements, API coverage, and compatibility limitations. |
| Client libraries | Ruby client | Record the verified gem and runtime, transport and data-type conventions, connection settings, and compatibility limitations. |
| Client libraries | Rust client | Identify and verify the proposed library, toolchain, protocol coverage, and limitations before describing any integration as supported. |

### Extensions and specialist interfaces

| Section | Name | Explanation |
| --- | --- | --- |
| Extensions and specialist interfaces | Backend callback interface | Define required and optional callbacks, arguments, return values, capabilities, and version dependencies for backend implementers. |
| Extensions and specialist interfaces | Custom code and hook interfaces | Define deployment and loading constraints plus commit-hook signatures, return contracts, ordering, and error behaviour. |
| Extensions and specialist interfaces | Cluster metadata interfaces | Define supported metadata operations, keys, values, persistence, and version or compatibility boundaries. |
| Extensions and specialist interfaces | Write-once interface | Define required policies, request and response contracts, immutable-write behaviour, acknowledgement options, and compatibility constraints. |
| Extensions and specialist interfaces | Replication hook interface | Define legacy send and receive callbacks, expected representations, failure handling, and applicable replication generations. |
| Extensions and specialist interfaces | Redis add-on commands and configuration | Define the verified add-on's commands, settings, cache semantics, metrics, and compatible component versions. |

### Legacy and experimental features

| Section | Name | Explanation |
| --- | --- | --- |
| Legacy and experimental features | Legacy LevelDB settings | Retain generated setting definitions needed by existing deployments, with release status and links to backend migration. |
| Legacy and experimental features | Memory backend settings | Define available in-memory backend settings, expiry and capacity controls, and release-specific restrictions. |
| Legacy and experimental features | Multi-backend and prefix-routing settings | Define routing syntax, backend definitions, supported policy combinations, and the release's migration or deprecation context. |
| Legacy and experimental features | Legacy AAE and riak_repl settings | Retain generated legacy repair and replication configuration definitions with explicit v2/v3 and subsystem applicability. |
| Legacy and experimental features | MapReduce jobs and functions | Define job JSON, input selection, phases, function forms, execution options, and result contracts shared by both transports. |
| Legacy and experimental features | Riak Control interface | Record the verified availability, interface controls, authentication requirements, and limitations of the legacy administration UI. |
| Legacy and experimental features | DTrace probes and settings | Catalogue probes, fields, required build capabilities, and configuration only for release and platform combinations that provide them. |
| Legacy and experimental features | Experimental strong-consistency interface | Preserve exact operation contracts, errors, prerequisites, and documented limitations without presenting the feature as production-ready. |
| Legacy and experimental features | Legacy query interface | Define the retained legacy query contract, version applicability, and mapping to the current query interfaces. |

## Reference tables and default values

Use the **defaults-table component for every reference table**. For configuration settings, the existing `configuration-reference-table` shortcode provides the generated names, descriptions, datatypes, constraints, and defaults. Use `configuration-reference-item` for one setting.

For command, API, metric, or compatibility tables, extend that component to accept the required columns and authoritative data source. The current configuration shortcode does not yet render those other schemas. Keep the same table presentation and controls instead of maintaining separate hand-written reference tables.

For example, select one configuration setting with:

```text
{{</* configuration-reference-table */>}}
^ring_size$
{{</* /configuration-reference-table */>}}
```

Or render its individual reference entry:

```text
{{</* configuration-reference-item config-name="ring_size" */>}}
```

Use the **value shortcode for every stated default**, including defaults in prose, request descriptions, and examples that intentionally demonstrate the default:

```text
The default ring size is {{</* load-value key="ring_size" */>}}.
```

Add missing configuration or API defaults to the authoritative metadata first. Preserve version and operating-system context, and distinguish no default from an empty value, zero, or `false`. Label deliberate example overrides clearly. Apply these rules in all four documentation areas.

The Section / Name / Explanation tables on these proposal pages are editorial inventories, not product reference tables.

## Reference page contract

Use a consistent structure for each interface: purpose, exact syntax or request schema, parameters and constraints, default values, results, errors, version applicability, and small examples. Define shared protocol conventions once. Keep procedures in How-to, guided exercises in Tutorials, and mechanisms and trade-offs in Foundations.

## Review basis

The existing configuration landing page contains a large manually maintained catalogue, while many configuration and all nine language-client leaf pages are still specifications. The proposed generated catalogue and topic pages provide complete lookup coverage without copying defaults.

Several current reference pages contain substantial explanation or task material: bucket types include creation procedures, the Query API limits page describes execution cost, and the strong-consistency page combines conceptual discussion and setup. Move those bodies to the corresponding areas while retaining their factual contracts here. Split the mixed replication material by generation. Distribute the current FAQ's answers to their appropriate pages and use the glossary and section indexes for discovery.

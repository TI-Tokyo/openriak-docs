---
title: 'Tutorials'
description: "Complete proposed Tutorials structure: 39 learning paths in seven subsections."
weight: 40
recommendations: true
product: 'OpenRiak KV'
product_version: '3.4.0'
---

This is the complete proposed **Tutorials** structure for OpenRiak KV 3.4.0. It includes retained, reorganised, and new learning paths. Each row names one proposed tutorial and the concrete experience the learner should complete.

The proposal covers **39 pages in seven subsections**, based on the existing 25 Tutorial files, including seven landing pages. [Diátaxis tutorials](https://diataxis.fr/tutorials/) teach through a guided practical experience with a reliable outcome.

Each subsection also has a short landing page showing the learning sequence and prerequisites. The first-cluster and first-application pages offer alternative environments or languages; readers choose one verified path rather than completing every alternative.

## Proposed pages

### First cluster

| Section | Name | Explanation |
| --- | --- | --- |
| First cluster | Build and explore a Docker cluster | Create a disposable cluster, observe its membership, write and read sample data, and clean up the environment at the end. |
| First cluster | Build and explore a cluster on Ubuntu | Follow one verified native-package path through installation, node configuration, joining, and a first request against a small learning cluster. |
| First cluster | Build a learning cluster in the cloud | Use one named, tested provider and infrastructure recipe, verify connectivity and membership, and remove all chargeable resources after the exercise. |
| First cluster | Build a learning cluster with Vagrant | Provide a reproducible VM-based alternative with pinned compatible images, membership checks, sample requests, and complete teardown. |

### First application

| Section | Name | Explanation |
| --- | --- | --- |
| First application | Build a small application with C# | Implement the shared sample application's model, create/read/update/delete flow, and indexed lookup using a verified C# client and runtime. |
| First application | Build a small application with Erlang | Build the same sample workflow with a verified Erlang client, observing returned values, context, and a simple indexed lookup. |
| First application | Build a small application with Go | Implement the shared sample with a verified Go module and toolchain, including data modelling, updates, deletion, and a query. |
| First application | Build a small application with Java | Use a verified Java dependency and runtime to connect, model sample data, perform object operations, and retrieve indexed results. |
| First application | Build a small application with Node.js | Use a verified Node.js client to complete the sample workflow with explicit asynchronous results, error checks, and a final query. |
| First application | Build a small application with PHP | Use a verified Composer package and runtime to build the sample, checking request results and the selected transport throughout. |
| First application | Build a small application with Python | Complete the sample using a verified Python runtime and client, replacing obsolete setup instructions with a reproducible environment. |
| First application | Build a small application with Ruby | Use a verified gem and runtime to complete the shared object and query workflow with observable checkpoints. |
| First application | Build a small application with Rust | Create a complete sample only after verifying the client and toolchain; demonstrate the actual supported object and query operations. |

### Data and concurrency

| Section | Name | Explanation |
| --- | --- | --- |
| Data and concurrency | Explore objects, buckets, and metadata with HTTP | Store a small dataset, inspect keys and metadata, update and delete objects, and observe responses without requiring a language client. |
| Data and concurrency | Apply different policies with bucket types | Create and activate two deliberate bucket policies, write test data, and observe the resulting differences in a disposable environment. |
| Data and concurrency | Create and resolve concurrent updates | Produce a controlled sibling conflict with two clients, inspect causal context, merge the values, and verify the resolved object. |
| Data and concurrency | Practise conditional updates | Make a conditional request succeed, make a stale precondition fail, and implement a bounded retry or conflict response. |
| Data and concurrency | Build a shared counter and collection | Use counters, sets, and grow-only sets in a small shared application and observe additions, removals, and context requirements. |
| Data and concurrency | Build a record with a distributed map | Create a map with several field types, update it from two clients, and observe nested operations and convergence. |
| Data and concurrency | Estimate unique activity with HyperLogLog | Add a known set of sample observations, compare the estimated count with the known total, and explore repeated observations. |

### Indexes and querying

| Section | Name | Explanation |
| --- | --- | --- |
| Indexes and querying | Build and query a people-search index | Load a small known dataset, create secondary-index terms, and run exact and range queries with predictable results. |
| Indexes and querying | Search projected attributes | Extend the same dataset with projected attributes, apply evaluation and filtering expressions, and check each query against known matches. |
| Indexes and querying | Combine query conditions | Build several scans over the learning dataset, combine their results, and observe how the aggregation expression changes the answer. |
| Indexes and querying | Produce counts and grouped results | Use accumulation modes to build a small report and compare deduplicated and raw results with the known dataset. |
| Indexes and querying | Retrieve a larger result set | Expand the sample data, follow the supported pagination or delivery workflow, and check that the application handles the complete result. |

### Cluster operations and recovery

| Section | Name | Explanation |
| --- | --- | --- |
| Cluster operations and recovery | Add and remove cluster members | Add a disposable node, inspect and commit the plan, observe handoffs, then remove the node and verify the remaining cluster. |
| Cluster operations and recovery | Practise a backend migration | Move a small known dataset through a verified backend-change workflow and compare the resulting data and index behaviour. |
| Cluster operations and recovery | Observe a node failure and recovery | Stop a node in a controlled exercise, record client behaviour, restore it, and observe recovery and repair. |
| Cluster operations and recovery | Back up and restore a sample dataset | Take a backend-appropriate backup, restore it into a disposable recovery environment, and verify objects and required metadata. |
| Cluster operations and recovery | Perform a rolling restart | Restart a learning cluster one node at a time while a small client workload runs, checking health before each next step. |
| Cluster operations and recovery | Inspect and repair a bounded data range | Run AAE inspection and count operations on known data, perform a supported repair exercise, and compare before-and-after results. |

### Replication and reconciliation

| Section | Name | Explanation |
| --- | --- | --- |
| Replication and reconciliation | Replicate data between two clusters | Build two disposable clusters using next-generation replication, connect a source and sink, and verify a write and deletion at the destination. |
| Replication and reconciliation | Catch up after a replication interruption | Interrupt a controlled connection, make sample changes, restore connectivity, and observe delivery and fullsync reconciliation. |
| Replication and reconciliation | Explore bidirectional replication | Connect the two learning clusters in both directions, write from each side, and inspect concurrent changes and final application results. |
| Replication and reconciliation | Reconcile selected buckets | Configure a deliberately bounded reconciliation scope, compare included and excluded sample data, and verify the result. |
| Replication and reconciliation | Re-replicate a selected time window | Modify a known group of objects, enqueue the selected window, and verify which objects are delivered to the second cluster. |

### Security

| Section | Name | Explanation |
| --- | --- | --- |
| Security | Make an authenticated TLS client connection | Create a disposable trust setup, configure a user and listener, make one successful request, and demonstrate a rejected untrusted connection. |
| Security | Apply and test group permissions | Create two identities with different groups, grant scoped permissions, and test both allowed and denied operations. |
| Security | Rotate a certificate in a learning environment | Replace a certificate using a controlled trust transition, verify client access during the exercise, and remove the obsolete trust material. |

## Learning sequence and authoring conventions

Start with one first-cluster path, then either an HTTP data exercise or one language-specific first application. Use the data and concurrency exercises before advanced query or replication work where their concepts are prerequisites. Operators can continue from a working cluster into the lifecycle and recovery exercises.

Every tutorial needs a tested starting state, one coherent scenario, exact actions, observable checkpoints, a final result, and cleanup. Pin the environment, dependency versions, and sample data needed to reproduce the lesson. Link to How-to for adapting the work to an existing deployment, Reference for complete contracts, and Foundations for deeper understanding.

Use the defaults-table component for reference tables and `load-value` for stated defaults. Label values chosen for the exercise as examples or overrides. Keep exhaustive option lists outside the learning sequence.

## Review basis

The Docker, Ubuntu, and Vagrant first-cluster pages and the backend-change exercise currently contain orientation and migration guidance without a complete exercise. The cloud, Rust, and security paths also need their specified lessons written and verified.

The existing two-cluster tutorial teaches legacy v2 replication; the proposed primary learning path uses next-generation replication and gives reconciliation and interruption recovery their own exercises. The long Query API example supplies material for a sequence of smaller lessons. The language tutorials need verified dependencies and a consistent sample application; their inherited runtime instructions are not evidence of current client support.

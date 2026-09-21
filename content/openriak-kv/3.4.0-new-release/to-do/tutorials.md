---
title: Tutorials
description: Implemented tutorials page inventory and remaining verification.
weight: 40
recommendations: true
product: OpenRiak KV
product_version: 3.4.0
draft: true
hide_provenance: true
layout: single
---

The 39 planned topics have been moved into the current tutorials structure and reviewed for their Diátaxis purpose. This inventory links to their current locations; it replaces the earlier proposal table.

## Current page locations

| Section | Page | Review focus |
| --- | --- | --- |
| First cluster | [Build and explore a Docker cluster]({{< product-version-root >}}tutorials/first-cluster/build-and-explore-a-docker-cluster/) | Create a disposable cluster, observe its membership, write and read sample data, and clean up the environment at the end. |
| First cluster | [Build and explore a cluster on Ubuntu]({{< product-version-root >}}tutorials/first-cluster/build-and-explore-a-cluster-on-ubuntu/) | Follow one verified native-package path through installation, node configuration, joining, and a first request against a small learning cluster. |
| First cluster | [Build a learning cluster on AWS EC2]({{< product-version-root >}}tutorials/first-cluster/cloud/aws-ec2/) | Use one named, tested provider and infrastructure recipe, verify connectivity and membership, and remove all chargeable resources after the exercise. |
| First cluster | [Build a learning cluster with Vagrant]({{< product-version-root >}}tutorials/first-cluster/build-a-learning-cluster-with-vagrant/) | Provide a reproducible VM-based alternative with pinned compatible images, membership checks, sample requests, and complete teardown. |
| First application | [Build a small application with C#]({{< product-version-root >}}tutorials/first-application/build-a-small-application-with-csharp/) | Implement the shared sample application's model, create/read/update/delete flow, and indexed lookup using a verified C# client and runtime. |
| First application | [Build a small application with Erlang]({{< product-version-root >}}tutorials/first-application/build-a-small-application-with-erlang/) | Build the same sample workflow with a verified Erlang client, observing returned values, context, and a simple indexed lookup. |
| First application | [Build a small application with Go]({{< product-version-root >}}tutorials/first-application/build-a-small-application-with-go/) | Implement the shared sample with a verified Go module and toolchain, including data modelling, updates, deletion, and a query. |
| First application | [Build a small application with Java]({{< product-version-root >}}tutorials/first-application/build-a-small-application-with-java/) | Use a verified Java dependency and runtime to connect, model sample data, perform object operations, and retrieve indexed results. |
| First application | [Build a small application with Node.js]({{< product-version-root >}}tutorials/first-application/build-a-small-application-with-node-js/) | Use a verified Node.js client to complete the sample workflow with explicit asynchronous results, error checks, and a final query. |
| First application | [Build a small application with PHP]({{< product-version-root >}}tutorials/first-application/build-a-small-application-with-php/) | Use a verified Composer package and runtime to build the sample, checking request results and the selected transport throughout. |
| First application | [Build a small application with Python]({{< product-version-root >}}tutorials/first-application/build-a-small-application-with-python/) | Complete the sample using a verified Python runtime and client, replacing obsolete setup instructions with a reproducible environment. |
| First application | [Build a small application with Ruby]({{< product-version-root >}}tutorials/first-application/build-a-small-application-with-ruby/) | Use a verified gem and runtime to complete the shared object and query workflow with observable checkpoints. |
| First application | [Build a small application with Rust]({{< product-version-root >}}tutorials/first-application/build-a-small-application-with-rust/) | Create a complete sample only after verifying the client and toolchain; demonstrate the actual supported object and query operations. |
| Data and concurrency | [Explore objects, buckets, and metadata with HTTP]({{< product-version-root >}}tutorials/data-and-concurrency/explore-objects-buckets-and-metadata-with-http/) | Store a small dataset, inspect keys and metadata, update and delete objects, and observe responses without requiring a language client. |
| Data and concurrency | [Apply different policies with bucket types]({{< product-version-root >}}tutorials/data-and-concurrency/apply-different-policies-with-bucket-types/) | Create and activate two deliberate bucket policies, write test data, and observe the resulting differences in a disposable environment. |
| Data and concurrency | [Create and resolve concurrent updates]({{< product-version-root >}}tutorials/data-and-concurrency/create-and-resolve-concurrent-updates/) | Produce a controlled sibling conflict with two clients, inspect causal context, merge the values, and verify the resolved object. |
| Data and concurrency | [Practise conditional updates]({{< product-version-root >}}tutorials/data-and-concurrency/practise-conditional-updates/) | Make a conditional request succeed, make a stale precondition fail, and implement a bounded retry or conflict response. |
| Data and concurrency | [Build a shared counter and collection]({{< product-version-root >}}tutorials/data-and-concurrency/build-a-shared-counter-and-collection/) | Use counters, sets, and grow-only sets in a small shared application and observe additions, removals, and context requirements. |
| Data and concurrency | [Build a record with a distributed map]({{< product-version-root >}}tutorials/data-and-concurrency/build-a-record-with-a-distributed-map/) | Create a map with several field types, update it from two clients, and observe nested operations and convergence. |
| Data and concurrency | [Estimate unique activity with HyperLogLog]({{< product-version-root >}}tutorials/data-and-concurrency/estimate-unique-activity-with-hyperloglog/) | Add a known set of sample observations, compare the estimated count with the known total, and explore repeated observations. |
| Indexes and querying | [Build and query a people-search index]({{< product-version-root >}}tutorials/indexes-and-querying/build-and-query-a-people-search-index/) | Load a small known dataset, create secondary-index terms, and run exact and range queries with predictable results. |
| Indexes and querying | [Search projected attributes]({{< product-version-root >}}tutorials/indexes-and-querying/search-projected-attributes/) | Extend the same dataset with projected attributes, apply evaluation and filtering expressions, and check each query against known matches. |
| Indexes and querying | [Combine query conditions]({{< product-version-root >}}tutorials/indexes-and-querying/combine-query-conditions/) | Build several scans over the learning dataset, combine their results, and observe how the aggregation expression changes the answer. |
| Indexes and querying | [Produce counts and grouped results]({{< product-version-root >}}tutorials/indexes-and-querying/produce-counts-and-grouped-results/) | Use accumulation modes to build a small report and compare deduplicated and raw results with the known dataset. |
| Indexes and querying | [Retrieve a larger result set]({{< product-version-root >}}tutorials/indexes-and-querying/retrieve-a-larger-result-set/) | Expand the sample data, follow the supported pagination or delivery workflow, and check that the application handles the complete result. |
| Cluster operations and recovery | [Add and remove cluster members]({{< product-version-root >}}tutorials/cluster-operations-and-recovery/add-and-remove-cluster-members/) | Add a disposable node, inspect and commit the plan, observe handoffs, then remove the node and verify the remaining cluster. |
| Cluster operations and recovery | [Practise a backend migration]({{< product-version-root >}}tutorials/cluster-operations-and-recovery/practise-a-backend-migration/) | Move a small known dataset through a verified backend-change workflow and compare the resulting data and index behaviour. |
| Cluster operations and recovery | [Observe a node failure and recovery]({{< product-version-root >}}tutorials/cluster-operations-and-recovery/observe-a-node-failure-and-recovery/) | Stop a node in a controlled exercise, record client behaviour, restore it, and observe recovery and repair. |
| Cluster operations and recovery | [Back up and restore a sample dataset]({{< product-version-root >}}tutorials/cluster-operations-and-recovery/back-up-and-restore-a-sample-dataset/) | Take a backend-appropriate backup, restore it into a disposable recovery environment, and verify objects and required metadata. |
| Cluster operations and recovery | [Perform a rolling restart]({{< product-version-root >}}tutorials/cluster-operations-and-recovery/perform-a-rolling-restart/) | Restart a learning cluster one node at a time while a small client workload runs, checking health before each next step. |
| Cluster operations and recovery | [Inspect and repair a bounded data range]({{< product-version-root >}}tutorials/cluster-operations-and-recovery/inspect-and-repair-a-bounded-data-range/) | Run AAE inspection and count operations on known data, perform a supported repair exercise, and compare before-and-after results. |
| Replication and reconciliation | [Replicate data between two clusters]({{< product-version-root >}}tutorials/replication-and-reconciliation/replicate-data-between-two-clusters/) | Build two disposable clusters using next-generation replication, connect a source and sink, and verify a write and deletion at the destination. |
| Replication and reconciliation | [Catch up after a replication interruption]({{< product-version-root >}}tutorials/replication-and-reconciliation/catch-up-after-a-replication-interruption/) | Interrupt a controlled connection, make sample changes, restore connectivity, and observe delivery and fullsync reconciliation. |
| Replication and reconciliation | [Explore bidirectional replication]({{< product-version-root >}}tutorials/replication-and-reconciliation/explore-bidirectional-replication/) | Connect the two learning clusters in both directions, write from each side, and inspect concurrent changes and final application results. |
| Replication and reconciliation | [Reconcile selected buckets]({{< product-version-root >}}tutorials/replication-and-reconciliation/reconcile-selected-buckets/) | Configure a deliberately bounded reconciliation scope, compare included and excluded sample data, and verify the result. |
| Replication and reconciliation | [Re-replicate a selected time window]({{< product-version-root >}}tutorials/replication-and-reconciliation/re-replicate-a-selected-time-window/) | Modify a known group of objects, enqueue the selected window, and verify which objects are delivered to the second cluster. |
| Security | [Make an authenticated TLS client connection]({{< product-version-root >}}tutorials/security/make-an-authenticated-tls-client-connection/) | Create a disposable trust setup, configure a user and listener, make one successful request, and demonstrate a rejected untrusted connection. |
| Security | [Apply and test group permissions]({{< product-version-root >}}tutorials/security/apply-and-test-group-permissions/) | Create two identities with different groups, grant scoped permissions, and test both allowed and denied operations. |
| Security | [Rotate a certificate in a learning environment]({{< product-version-root >}}tutorials/security/rotate-a-certificate-in-a-learning-environment/) | Replace a certificate using a controlled trust transition, verify client access during the exercise, and remove the obsolete trust material. |

## Remaining verification

The local 3.4.0 Docker data fixtures and Python, Node.js, and Java HTTP examples have been exercised. AWS EC2, Vagrant, native multi-host Ubuntu, the remaining language runtimes, and the complete maintenance/replication/security lesson sequences still need end-to-end rehearsal. Do not label those paths runtime-verified until their results are recorded.

Use [For Review]({{< product-version-root >}}to-do/for-review/) for per-page technical review status. The machine-readable source-to-destination map is retained in `notes/reports/diataxis-page-map.json`.

## Runtime review results

The people fixture passed exact/projected searches, intersection/union/subtraction, direct city-index grouped counts, and secondary-index pagination on the five-node 3.4.0 Alpine/OTP 26 lab. The larger-result exercise uses the secondary-index interface because Query API continuations reproduced a release failure. Projected-attribute grouping also needs investigation. See the [review overview](../#runtime-issues-found-during-this-review) for the observations.

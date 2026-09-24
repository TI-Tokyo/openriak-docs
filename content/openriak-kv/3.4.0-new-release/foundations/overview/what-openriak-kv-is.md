---
title: What OpenRiak KV is
description: OpenRiak KV stores values under keys and distributes copies across a cluster of servers. An application
  supplies a bucket and key to write or retrieve an object; OpenRiak locates the responsible partitions and coordinate
weight: 10
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: Reviewed
draft: true
audience:
- new-readers
source_material:
- legacy-3.2.5
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\new-to-nosql.md
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: complete
last_reviewed: '2026-09-23'
review-by: TI Tokyo/JOM
review_scope: editorial & technical
restructured_from:
- foundations/foundations/new-to-nosql.md
related:
- tutorials/first-cluster/build-and-explore-a-docker-cluster
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/eventual-consistency-and-convergence
- reference/orientation-and-compatibility/glossary
---

OpenRiak KV stores values under keys and distributes copies across a cluster of servers. An application supplies a bucket and key to write or retrieve an object; OpenRiak locates the responsible partitions and coordinates the request.

## A distributed key/value store

A key/value store works much like a massive distributed Dictionary: you provide a key, and the system returns the value associated with that key. A value can be any byte sequence—JSON, text, an image, or arbitrary binary data. The application defines what the data means, how keys are chosen, and how conflicting updates are resolved.

Nodes share responsibility for the keyspace. Replicas allow a request to continue when some servers are unavailable, provided the request's acknowledgement requirements can still be met. Reaching a single node is not by itself a guarantee that a read or write will succeed.

## The application contract

OpenRiak's ordinary object operations are eventually consistent. Applications preserve causal context when updating an object and handle concurrent values when the bucket policy allows them. Distributed data types provide merge rules for supported counters and collections.

Key lookup is the basic access path. Secondary indexes and the Query API add indexed discovery when the selected backend supports them. They do not turn the database into a relational system with cross-object transactions.
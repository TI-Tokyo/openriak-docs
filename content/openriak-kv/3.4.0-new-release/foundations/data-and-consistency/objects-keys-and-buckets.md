---
title: Objects, keys, and buckets
description: An object is a value and its metadata, addressed by a bucket and key. A bucket type can add a namespace
  and a shared data policy to that address.
weight: 80
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: Reviewed
draft: true
audience:
- architects
- developers
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\concepts\buckets.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\concepts\keys-and-objects.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#mapping-data-to-objects
- https://openriak.github.io/riak/InitialDesignDecisions.html#mapping-data-to-objects---changing-the-choice
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: complete
last_reviewed: '2026-09-24'
review-by: TI Tokyo/JOM
review_scope: editorial & technical
restructured_from:
- foundations/data-model/keys-objects-and-buckets.md
related:
- foundations/data-and-consistency/bucket-types-and-data-policies
- foundations/data-and-consistency/causality-version-vectors-and-siblings
- how-to/planning-a-deployment/map-application-data-to-objects-and-buckets
- reference/data-model-contracts/keys-and-object-representations
- reference/data-model-contracts/buckets-and-bucket-types
---

An object is a value and its metadata, addressed by a bucket and key. A bucket type can add a namespace and a shared data policy to that address.

## Keys and values

The key identifies the object within its bucket. Values are byte sequences with metadata such as a media type; a JSON value is an application convention rather than a schema enforced across the bucket. Choose an object boundary that matches what the application reads and updates together.

An object can have multiple concurrent contents, called siblings. A read is therefore not always a single value, even when the client requested one key.

## Buckets and types

Buckets group keys and provide a policy scope. A typed bucket is addressed using its type as well as its bucket name. The same textual bucket name under two types identifies two namespaces; dropping the type from a request can make existing data appear missing.

### A small example

An application might store one customer profile under the example key `customer-42` in a `profiles` bucket. Orders can be separate objects with their own identifiers. That separation avoids rewriting a whole customer history for every order, but the application must coordinate any relationship between those objects.

Indexes support discovering keys by selected attributes. They do not make a bucket a relational table.

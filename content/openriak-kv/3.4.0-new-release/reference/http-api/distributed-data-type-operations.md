---
title: Distributed data-type operations
description: The HTTP data-type API fetches structured values and applies datatype operations within an active bucket
  type.
weight: 490
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#the-data-type-api
tags:
- diataxis
- kv
- reference
- quickdocs
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/specialized-apis/data-type-api.md
related:
- how-to/application-data/update-distributed-counters
- how-to/application-data/add-and-remove-members-of-distributed-sets
- how-to/application-data/add-members-to-grow-only-sets
- how-to/application-data/update-distributed-maps
- how-to/application-data/estimate-distinct-values-with-hyperloglog
- reference/data-model-contracts/distributed-data-type-contracts
- reference/protocol-buffers-api/fetch-data-type-messages
- reference/protocol-buffers-api/update-data-type-messages
- foundations/data-and-consistency/conflict-free-replicated-data-types
---

The HTTP data-type API fetches structured values and applies datatype operations within an active bucket type.

## Endpoints

`GET /types/TYPE/buckets/BUCKET/datatypes/KEY`

`POST /types/TYPE/buckets/BUCKET/datatypes/KEY`

A POST to the datatype collection without a key requests server key assignment. The enclosing bucket type determines the datatype; ordinary object PUT is not the update interface.

## Operations

- Counter: `{"increment":2}` adds a signed amount.
- Set: `{"add_all":["a","b"]}` adds members; `remove_all` requires observed context.
- Grow-only set: `add_all` adds members; removal is not supported.
- Map: `{"update":{"name_register":"Aiko","visits_counter":{"increment":1}}}` changes typed fields. `remove` removes observed fields with context.
- HyperLogLog: `{"add_all":["visitor-a","visitor-b"]}` adds identifiers to the estimator.

Fetch responses identify `type` and `value`, with context where applicable. Include the opaque `context` in updates that need observed state. Successful updates can acknowledge without a body or return a representation when requested.

## Constraints

Datatype updates are not generic idempotent replacements. Retrying an uncertain increment can increment twice. Large or hot datatype objects can become a bottleneck, and the ordinary Query API does not query their internal fields.

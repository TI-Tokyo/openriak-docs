---
title: Add members to grow-only sets
description: Update a distributed gset through the data-type API. Set `RIAK_HTTP` to the intended endpoint and include
  the deployment's authentication options.
weight: 490
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\data-types\gsets.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/develop/use-gsets.md
related:
- reference/data-model-contracts/distributed-data-type-contracts
- reference/http-api/distributed-data-type-operations
- tutorials/data-and-concurrency/build-a-shared-counter-and-collection
- foundations/data-and-consistency/conflict-free-replicated-data-types
---

Update a distributed gset through the data-type API. Set `RIAK_HTTP` to the intended endpoint and include the deployment's authentication options.

## Prepare the bucket type

Create the type if it does not already exist, inspect its properties, and activate it:

{{< cli-example key="shell:riak admin bucket-type create" args=`gsets '{"props":{"datatype":"gset"}}'` >}}
{{< cli-example key="shell:riak admin bucket-type status" args="gsets" >}}
{{< cli-example key="shell:riak admin bucket-type activate" args="gsets" >}}

In the Alpine Docker lab, run these through the `kv` helper from [Build and explore a Docker cluster]({{< product-version-root >}}tutorials/first-cluster/build-and-explore-a-docker-cluster/). An existing active type should be inspected and reused, not recreated with a different datatype.

## Submit and read an operation

```sh
curl --fail -i -X POST "$RIAK_HTTP/types/gsets/buckets/example/datatypes/sample" -H 'Content-Type: application/json' --data-binary '{"add_all":["music","walking"]}'
curl --fail "$RIAK_HTTP/types/gsets/buckets/example/datatypes/sample"
```

Grow-only sets support additions, not member removal. Re-adding an existing member does not create a duplicate. Choose an ordinary set when the application must remove members.

## Verify concurrent behaviour

Run two clients against a disposable key, then fetch the converged value. Preserve opaque context returned by the data-type API; it is not interchangeable with an ordinary object's vector-clock header. See [Distributed data-type operations]({{< product-version-root >}}reference/http-api/distributed-data-type-operations/) for response fields and operations, and [Build a shared counter and collection]({{< product-version-root >}}tutorials/data-and-concurrency/build-a-shared-counter-and-collection/) for a guided exercise.

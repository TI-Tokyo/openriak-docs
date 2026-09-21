---
title: Update distributed counters
description: Update a distributed counter through the data-type API. Set `RIAK_HTTP` to the intended endpoint and
  include the deployment's authentication options.
weight: 470
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\data-types\counters.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/develop/use-counters.md
related:
- reference/data-model-contracts/distributed-data-type-contracts
- reference/http-api/distributed-data-type-operations
- tutorials/data-and-concurrency/build-a-shared-counter-and-collection
- foundations/data-and-consistency/conflict-free-replicated-data-types
---

Update a distributed counter through the data-type API. Set `RIAK_HTTP` to the intended endpoint and include the deployment's authentication options.

## Prepare the bucket type

Create the type if it does not already exist, inspect its properties, and activate it:

{{< cli-example key="shell:riak admin bucket-type create" args=`counters '{"props":{"datatype":"counter"}}'` >}}
{{< cli-example key="shell:riak admin bucket-type status" args="counters" >}}
{{< cli-example key="shell:riak admin bucket-type activate" args="counters" >}}

In the Alpine Docker lab, run these through the `kv` helper from [Build and explore a Docker cluster]({{< product-version-root >}}tutorials/first-cluster/build-and-explore-a-docker-cluster/). An existing active type should be inspected and reused, not recreated with a different datatype.

## Submit and read an operation

```sh
curl --fail -i -X POST "$RIAK_HTTP/types/counters/buckets/example/datatypes/sample" -H 'Content-Type: application/json' --data-binary '{"increment":2}'
curl --fail "$RIAK_HTTP/types/counters/buckets/example/datatypes/sample"
```

Use a negative increment to subtract. An increment is not an idempotent replacement: retrying after an uncertain timeout can apply it twice.

## Verify concurrent behaviour

Run two clients against a disposable key, then fetch the converged value. Preserve opaque context returned by the data-type API; it is not interchangeable with an ordinary object's vector-clock header. See [Distributed data-type operations]({{< product-version-root >}}reference/http-api/distributed-data-type-operations/) for response fields and operations, and [Build a shared counter and collection]({{< product-version-root >}}tutorials/data-and-concurrency/build-a-shared-counter-and-collection/) for a guided exercise.

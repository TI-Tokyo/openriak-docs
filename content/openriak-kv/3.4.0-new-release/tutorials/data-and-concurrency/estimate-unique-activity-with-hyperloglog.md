---
title: Estimate unique activity with HyperLogLog
weight: 200
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Estimate unique visitors using a distributed data type. Use a fresh learning cluster or a fresh key
  so earlier runs do not change the observation.
related:
- tutorials/indexes-and-querying/build-and-query-a-people-search-index
- how-to/application-data/estimate-distinct-values-with-hyperloglog
- reference/data-model-contracts/distributed-data-type-contracts
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
- foundations/data-and-consistency/conflict-free-replicated-data-types
previous_page: tutorials/data-and-concurrency/build-a-record-with-a-distributed-map
next_page: tutorials/indexes-and-querying/build-and-query-a-people-search-index
---

Estimate unique visitors using a distributed data type. Use a fresh learning cluster or a fresh key so earlier runs do not change the observation.

## Create and activate the type

The following type and data-type choices are deliberate exercise values.

{{< cli-example key="shell:riak admin bucket-type create" prefix="kv node1" args="docs-hll '{\"props\":{\"datatype\":\"hll\"}}'" >}}

{{< cli-example key="shell:riak admin bucket-type activate" prefix="kv node1" args="docs-hll" >}}

## Apply an operation

```sh
url="$RIAK_HTTP/types/docs-hll/buckets/learning/datatypes/visitors"
curl --fail -i -X POST "$url?returnbody=true" \
  -H 'Content-Type: application/json' --data-binary '{"add_all":["aiko","sam","aiko"]}'
curl --fail "$url"
```

The returned value is a distinct-count estimate. Adding the repeated identifier does not represent another distinct visitor.

## Repeat and inspect

Submit the same update once more and fetch the result. Compare it with replacing an ordinary object: the data-type endpoint applies operations with the type's merge semantics. Preserve returned context for later operations that require it, particularly removals.

## Cleanup

Delete the exercise key through its object endpoint when you are finished, or discard the disposable cluster at the end of the learning sequence. Keep the type if continuing with more examples; deleting a value does not delete the type.

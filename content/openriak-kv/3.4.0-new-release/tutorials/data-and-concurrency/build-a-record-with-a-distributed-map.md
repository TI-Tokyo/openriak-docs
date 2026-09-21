---
title: Build a record with a distributed map
weight: 190
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Build a profile using a distributed data type. Use a fresh learning cluster or a fresh key so earlier
  runs do not change the observation.
related:
- tutorials/data-and-concurrency/estimate-unique-activity-with-hyperloglog
- how-to/application-data/update-distributed-maps
- reference/data-model-contracts/distributed-data-type-contracts
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
- foundations/data-and-consistency/conflict-free-replicated-data-types
previous_page: tutorials/data-and-concurrency/build-a-shared-counter-and-collection
next_page: tutorials/data-and-concurrency/estimate-unique-activity-with-hyperloglog
---

Build a profile using a distributed data type. Use a fresh learning cluster or a fresh key so earlier runs do not change the observation.

## Create and activate the type

The following type and data-type choices are deliberate exercise values.

{{< cli-example key="shell:riak admin bucket-type create" prefix="kv node1" args="docs-maps '{\"props\":{\"datatype\":\"map\"}}'" >}}

{{< cli-example key="shell:riak admin bucket-type activate" prefix="kv node1" args="docs-maps" >}}

## Apply an operation

```sh
url="$RIAK_HTTP/types/docs-maps/buckets/learning/datatypes/profile"
curl --fail -i -X POST "$url?returnbody=true" \
  -H 'Content-Type: application/json' --data-binary '{"update":{"name_register":"Aiko","visits_counter":{"increment":1},"interests_set":{"add_all":["music","walking"]}}}'
curl --fail "$url"
```

The value contains the name register, a visits counter, and the two set members.

## Repeat and inspect

Submit the same update once more and fetch the result. Compare it with replacing an ordinary object: the data-type endpoint applies operations with the type's merge semantics. Preserve returned context for later operations that require it, particularly removals.

## Cleanup

Delete the exercise key through its object endpoint when you are finished, or discard the disposable cluster at the end of the learning sequence. Keep the type if continuing with more examples; deleting a value does not delete the type.

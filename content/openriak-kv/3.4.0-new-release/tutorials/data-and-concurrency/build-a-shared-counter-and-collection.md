---
title: Build a shared counter and collection
weight: 180
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Count visits using a distributed data type. Use a fresh learning cluster or a fresh key so earlier
  runs do not change the observation.
related:
- tutorials/data-and-concurrency/build-a-record-with-a-distributed-map
- reference/data-model-contracts/distributed-data-type-contracts
- how-to/application-data/update-distributed-counters
- how-to/application-data/add-and-remove-members-of-distributed-sets
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
- foundations/data-and-consistency/conflict-free-replicated-data-types
previous_page: tutorials/data-and-concurrency/practise-conditional-updates
next_page: tutorials/data-and-concurrency/build-a-record-with-a-distributed-map
---

Count visits using a distributed data type. Use a fresh learning cluster or a fresh key so earlier runs do not change the observation.

## Create and activate the type

The following type and data-type choices are deliberate exercise values.

{{< cli-example key="shell:riak admin bucket-type create" prefix="kv node1" args="docs-counters '{\"props\":{\"datatype\":\"counter\"}}'" >}}

{{< cli-example key="shell:riak admin bucket-type activate" prefix="kv node1" args="docs-counters" >}}

## Apply an operation

```sh
url="$RIAK_HTTP/types/docs-counters/buckets/learning/datatypes/visits"
curl --fail -i -X POST "$url?returnbody=true" \
  -H 'Content-Type: application/json' --data-binary '{"increment":2}'
curl --fail "$url"
```

The value is 2 after the first update and 4 after submitting the same update again.

## Repeat and inspect

Submit the same update once more and fetch the result. Compare it with replacing an ordinary object: the data-type endpoint applies operations with the type's merge semantics. Preserve returned context for later operations that require it, particularly removals.

## Add a shared collection

Create and activate a set type:

{{< cli-example key="shell:riak admin bucket-type create" prefix="kv node1" args="docs-sets '{\"props\":{\"datatype\":\"set\"}}'" >}}

{{< cli-example key="shell:riak admin bucket-type activate" prefix="kv node1" args="docs-sets" >}}

Add two interests and read them back:

```sh
set_url="$RIAK_HTTP/types/docs-sets/buckets/learning/datatypes/interests"
curl --fail -X POST "$set_url?returnbody=true" \
  -H 'Content-Type: application/json' \
  --data-binary '{"add_all":["music","walking"]}'
curl --fail "$set_url"
```

The returned `value` contains `music` and `walking`. Repeat the POST: each member still appears once. Compare this with the counter, where repeating an increment changes the value again.

## Try a grow-only collection

Create a grow-only set for events that should never be removed:

{{< cli-example key="shell:riak admin bucket-type create" prefix="kv node1" args="docs-gsets '{\"props\":{\"datatype\":\"gset\"}}'" >}}

{{< cli-example key="shell:riak admin bucket-type activate" prefix="kv node1" args="docs-gsets" >}}

```sh
gset_url="$RIAK_HTTP/types/docs-gsets/buckets/learning/datatypes/visited"
curl --fail -X POST "$gset_url?returnbody=true" \
  -H 'Content-Type: application/json' \
  --data-binary '{"add_all":["Tokyo","Osaka"]}'
curl --fail "$gset_url"
```

The response contains both cities. A grow-only set has no removal operation. For context-preserving removals from an ordinary set, follow [Add and remove members of distributed sets]({{< product-version-root >}}how-to/application-data/add-and-remove-members-of-distributed-sets/).

## Cleanup

Keep the cluster and types for the next exercise. At the end of the learning sequence, discard the disposable cluster using the cleanup instructions in [Build your first cluster with Docker]({{< product-version-root >}}tutorials/first-cluster/build-and-explore-a-docker-cluster/).

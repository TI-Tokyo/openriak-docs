---
title: Apply different policies with bucket types
weight: 150
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Create a bucket type for the remaining object exercises and observe that typed and untyped buckets
  are separate namespaces.
related:
- tutorials/data-and-concurrency/explore-objects-buckets-and-metadata-with-http
- tutorials/data-and-concurrency/create-and-resolve-concurrent-updates
- how-to/application-data/create-and-activate-bucket-types
- reference/configuration/bucket-properties-and-defaults
- reference/data-model-contracts/buckets-and-bucket-types
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
- foundations/data-and-consistency/conflict-free-replicated-data-types
previous_page: tutorials/data-and-concurrency/explore-objects-buckets-and-metadata-with-http
next_page: tutorials/data-and-concurrency/create-and-resolve-concurrent-updates
---

Create a bucket type for the remaining object exercises and observe that typed and untyped buckets are separate namespaces.

## Create the policy

Use the running learning cluster. The type name `docs` and sibling-preserving choice below are deliberate lab values:

{{< cli-example key="shell:riak admin bucket-type create" prefix="kv node1" args="docs '{\"props\":{\"allow_mult\":true}}'" >}}

{{< cli-example key="shell:riak admin bucket-type activate" prefix="kv node1" args="docs" >}}

{{< cli-example key="shell:riak admin bucket-type status" prefix="kv node1" args="docs" >}}

Wait until the type is active before using it. If it already exists from an earlier run, inspect its properties rather than assuming it matches this exercise.

## Compare namespaces

```sh
export RIAK_HTTP=http://127.0.0.1:18098
curl --fail -i -X PUT "$RIAK_HTTP/types/docs/buckets/learning/keys/example"   -H 'Content-Type: text/plain' --data-binary 'typed value'
curl --fail "$RIAK_HTTP/types/docs/buckets/learning/keys/example"
curl -i "$RIAK_HTTP/buckets/learning/keys/example"
```

The typed read returns `typed value`. In a fresh lab the untyped read is missing. Both URLs contain the same bucket and key names, but only one contains the type.

## Continue

Delete the typed example object when finished. Keep the `docs` type for the concurrency and query exercises; it is not removed by deleting one object.

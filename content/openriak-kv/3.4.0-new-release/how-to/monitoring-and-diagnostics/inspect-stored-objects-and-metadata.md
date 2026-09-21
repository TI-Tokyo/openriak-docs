---
title: Inspect stored objects and metadata
description: Inspect a small set of known objects and their metadata when diagnosing a data problem. Start with
  the public API so you can compare what the application sees.
weight: 930
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#accessing-objects
- https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#data-inspection
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/operate/inspect-data.md
related:
- how-to/application-data/read-an-object-and-handle-missing-values
- how-to/application-data/resolve-concurrent-object-updates
- how-to/data-inspection-and-repair/find-oversized-objects-or-excessive-siblings
- how-to/data-inspection-and-repair/measure-object-sizes-and-sibling-distributions
- reference/data-model-contracts/object-metadata
- reference/data-model-contracts/causal-context-and-version-vector-representations
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Inspect a small set of known objects and their metadata when diagnosing a data problem. Start with the public API so you can compare what the application sees.

## Capture the object response

Fetch headers and body using [Read an object and handle missing values]({{< product-version-root >}}how-to/application-data/read-an-object-and-handle-missing-values/). Record the type, bucket, key, content type, index terms, user metadata, causal context, and any siblings. Keep raw evidence if an application decoder rejects the value.

## Inspect the internal representation when needed

Open the remote console and create a local client handle using the documented helper:

{{< cli-example key="erlang:riak:local_client" >}}

Bind its successful result to a client variable, then use the release's get interface:

{{< cli-example key="erlang:riak_client:get" >}}

Supply the exact bucket/type, key, and client handle using the function's argument contract. Avoid printing a very large value or enumerating the whole database during an incident.

## Compare and retain context

Compare the internal object with the API representation and the application's expected encoding. Use bounded AAE statistics or key-finding folds for a wider pattern. Do not rewrite the inspected object unless you have a defined repair or conflict-resolution rule.
